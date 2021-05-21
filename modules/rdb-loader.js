const cluster = await import("cluster");

const rdbHelper = await import("./rdb-helper.js");
const general = await import("./general.js");

var scriptStartDate = new Date();

// HELPER FUNCTIONS

// code to upgrade the RDB schema
async function upgradeSchema(config, usePool) {
  var fkbad = new Set(), fkref = {}, nukedtables = new Set();
  
  if (usePool) var pool = usePool;
  else var pool = new rdbHelper.nativePSQLpool(config.rdb.constring, 1);
  const client = await pool.connect();
  
  var tmp1, tmp2, i, queries = [], q;
  
  tmp1 = await client.query("SELECT ccu.table_name as tablename, tc.table_name as reftable, tc.constraint_name FROM information_schema.table_constraints AS tc JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.constraint_schema = '"+mineSchema.replace(/"/g, "")+"'");
  const FKTblIds = {};
  for (i=0; i<tmp1.tablename.length; i++) {
    if (! (tmp1.tablename[i] in FKTblIds)) FKTblIds[tmp1.tablename[i]] = [];
    FKTblIds[tmp1.tablename[i]].push([tmp1.reftable[i], tmp1.constraint_name[i]]);
  }

  tmp1 = await client.query(`SELECT table_name FROM information_schema.tables WHERE table_schema = '${mineSchema.replace(/"/g, "")}'`);
  if (tmp1.table_name.length == 0) queries.push(`CREATE SCHEMA IF NOT EXISTS ${mineSchema};`);

  tmp2 = new Set();
  for (i=0; i<tmp1.table_name.length; i++) {
    tmp2.add(tmp1.table_name[i]);
  }
  
  const deletedConstraints = new Set();
  for (let i of tmp2) {
    if (! sql_PK.hasOwnProperty(i)) await upgradeSchema_deleteTable(queries, i, FKTblIds, deletedConstraints);
  }
  
  for (i in sql_PK) {
    if (! tmp2.has(i)) upgradeSchema_createTable(queries, i);
    else await upgradeSchema_checkTable(queries, i, client, fkbad, fkref, nukedtables);
  }
  
  var fk_tableRedo = new Set(), fkKill = {};
  for (var e of fkbad) {
    if (! (e in fkref)) continue;
    Object.entries(fkref[e]).forEach(x => {fkKill[x[0]] = x[1][0];});
    Object.values(fkref[e]).forEach(x => {x[1].forEach(fk_tableRedo.add, fk_tableRedo);});
  }
  for (const [constr, tableName] of Object.entries(fkKill)) queries.unshift(`ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${constr}" CASCADE;`);
  
  // add the foreign key stuff later to ensure that all tables have been defined...
  var q1 = [], q2 = [];
  for (i=0; i<queries.length; i++) {
    if (queries[i].indexOf(' ADD FOREIGN KEY ("') != -1 && queries[i].indexOf('") REFERENCES ') != -1) q2.push(queries[i]);
    else q1.push(queries[i]);
  }
  
  if (queries.length) {

    await client.query("BEGIN");
    for (q of q1) {
      //console.log("A>", q);
      await client.query(q);
    }
    for (q of q2) {
      //console.log("B>", q);
      await client.query(q);
    }
    await client.query("COMMIT");
  }
  
  queries = [];
  for (var e of fk_tableRedo) fkTable(queries, e, client, {});
  if (queries.length) {
    await client.query("BEGIN");
    for (q of queries) {
      //console.log("C>", q);
      await client.query(q);
    }
    await client.query("COMMIT");
  }
  
  queries = [];
  
  for (var e of nukedtables) await upgradeSchema_createTable(queries, e);
  
  if (queries.length) {
    await client.query("BEGIN");
    for (q of queries) {
      //console.log("D>", q);
      await client.query(q);
    }
    await client.query("COMMIT");
  }
  
  client.release();
  if (! usePool) pool.end();
}

// create a new table
function upgradeSchema_createTable(queries, tableName) { // create new table... 
  if (tableName == "brief_summary_with_hit_score") return;
  
  var query = "", i, tmp1, tmp2;
  
  query += `CREATE TABLE ${mineSchema}."${tableName}" (\n`;
  
  for (const column of rdbRef[tableName].columns) query += `  "${column[0]}" ${column[1]},\n`;
  
  // unique
  for (const key of (rdbRef[tableName].unique_keys || [])) {
    tmp1 = rdbHelper.arrayModifier(key, function(j) {return `"${j}"`;}).join(",");
    query += `  UNIQUE (${tmp1}),\n`;
  }
  
  // primary
  tmp1 = rdbHelper.arrayModifier(rdbRef[tableName].primary_key, function(i) {return `"${i}"`;});
  if (tmp1.length) query += `  PRIMARY KEY (${tmp1})\n);`;
  else query = query.slice(0, -2) + "\n);"
  queries.push(query);
  
  for (const key of (rdbRef[tableName].foreign_keys || [])) {
    tmp1 = key[0].map(j => {return `"${j}"`}).join(",");
    tmp2 = key[2].map(j => {return `"${j}"`}).join(",");
    
    //tmp1 = rdbHelper.arrayModifier(key[0], function(j) {return `"${j}"`;}).join(",");
    //tmp2 = rdbHelper.arrayModifier(key[2], function(j) {return `"${j}"`;}).join(",");
    if (tmp1 == '"'+__primaryKey__+'"' && tmp2 == '"'+__primaryKey__+'"' && key[1] == "brief_summary") queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${key[1]}" (${tmp2}) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;`);
    else queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${key[1]}" (${tmp2}) DEFERRABLE INITIALLY DEFERRED;`);
  }
  
  for (const index of (rdbRef[tableName].indexes || [])) {
    const columns = index.map(x=>`"${x}"`).join(",");
    queries.push(`create index on ${mineSchema}."${tableName}" (${columns});`);
  }
}

async function upgradeSchema_deleteTable(queries, tableName, FKTblIds, deletedConstraints) {
  if (tableName == "brief_summary_with_hit_score") return;
  
  // delete foreign keys that refer to the to-be-deleted table
  for (const [reftable, constraint_name] of (FKTblIds[tableName] || [])) {
    if (deletedConstraints.has(constraint_name) || deletedConstraints.has("table:"+reftable)) continue; // skip already dropped constraints/tables
    queries.push(`ALTER TABLE ${mineSchema}."${reftable}" DROP CONSTRAINT "${constraint_name}";`);
    deletedConstraints.add(constraint_name);
  }

  deletedConstraints.add("table:"+tableName);
  queries.push(`DROP TABLE ${mineSchema}."${tableName}";`);
}

function bakaCopySortString(arr) {return JSON.stringify(JSON.parse(JSON.stringify(arr)).sort());}

// modify an existing table
async function upgradeSchema_checkTable(queries, tableName, client, fkbad, fkref, nukedtables) {
  if (tableName == "brief_summary_with_hit_score") return;
  
  var columns = {}, i, data_type, tmp1, tmp2, tmp3, tmp4, tmp5;

  // identify modified columns
  for (i=0; i<rdbRef[tableName].columns.length; i++) columns[rdbRef[tableName].columns[i][0]] = rdbRef[tableName].columns[i];
  
  // primary key part 1
  var pkey_tmp = await client.query("SELECT tc.constraint_name, array_agg(cast(kcu.column_name as text)) FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name WHERE tc.table_name = $1 AND tc.table_schema = '"+mineSchema.replace(/"/g, "")+"' AND tc.constraint_type = 'PRIMARY KEY' group by tc.constraint_name;", [tableName]), pname, pkeys;

  if (pkey_tmp.constraint_name.length == 0) {
    pname = null;
    pkeys = [];
  }
  else {
    pname = pkey_tmp.constraint_name[0];
    pkeys = pkey_tmp.array_agg[0];
  }
  if (bakaCopySortString(pkeys) != bakaCopySortString(rdbRef[tableName].primary_key)) {
    if (pname) { // drop the old primary key
      queries.push(`ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${pname}";`);
    }
  }

  tmp1 = await client.query("select column_name, data_type, column_default from INFORMATION_SCHEMA.COLUMNS where table_schema='"+mineSchema.replace(/"/g, "")+"' and table_name=$1;", [tableName]);
  
  tmp3 = new Set();
  for (i=0; i<tmp1.column_name.length; i++) {
    if (tmp1.data_type[i] == "integer" && tmp1.column_default[i] == "nextval('"+(mineSchema.replace(/"/g, "").toLowerCase() != "public" ? mineSchema.replace(/"/g, "").toLowerCase()+"." : "")+tableName.toLowerCase()+"_"+tmp1.column_name[i].toLowerCase()+"_seq'::regclass)") tmp1.data_type[i] = "serial";
    
    if (! columns.hasOwnProperty(tmp1.column_name[i])) { // delete column if it doesn't exist in the yaml file
      if (tmp1.column_name[i].startsWith("_") && columns.hasOwnProperty(tmp1.column_name[i].substr(1))) {
        queries.push(`ALTER TABLE ${mineSchema}."${tableName}" RENAME COLUMN "${tmp1.column_name[i]}" TO "${tmp1.column_name[i].substr(1)}";`);
        tmp3.add(tmp1.column_name[i].substr(1));
        continue;
      }
      queries.push(`ALTER TABLE ${mineSchema}."${tableName}" DROP COLUMN "${tmp1.column_name[i]}";`);
      continue;
    }

    tmp3.add(tmp1.column_name[i]);
    
    data_type = columns[tmp1.column_name[i]][1]; // data_type in schema
    
    // figure out the correct array type
    if (tmp1.data_type[i] == "ARRAY") { // change it to fit text[] or integer[]
      tmp2 = (await client.query("select udt_name from INFORMATION_SCHEMA.COLUMNS where table_schema='"+mineSchema.replace(/"/g, "")+"' and table_name=$1 and column_name=$2;", [tableName, tmp1.column_name[i]])).udt_name[0];
      if (tmp2 == "_text") tmp1.data_type[i] = "text[]";
      else if (tmp2 == "_int4") tmp1.data_type[i] = "integer[]";
      else {
        console.error("Unknown format", tableName, tmp1.column_name[i], tmp1.data_type[i], tmp2);
        process.exit();
      }
    }
    
    // figure out the char length
    if (data_type == "character") {
      tmp2 = (await client.query("select character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_schema='"+mineSchema.replace(/"/g, "")+"' and table_name=$1 and column_name=$2;", [tableName, tmp1.column_name[i]])).character_maximum_length[0];
      data_type = "char("+tmp2+")";
    }
    
    // if the types don't match -> modify the type
    if (data_type != tmp1.data_type[i]) {
      //queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${tmp1.column_name[i]}" DROP NOT NULL;`);
      if (rdbRef[tableName].primary_key.indexOf(tmp1.column_name[i]) != -1) { // struct_ncs_oper.id isn't working properly.............
        queries.push(`DROP TABLE ${mineSchema}."${tableName}";`);
        nukedtables.add(tableName);
        return;
      }
      else {
        queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${tmp1.column_name[i]}" DROP DEFAULT;`);
        queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${tmp1.column_name[i]}" TYPE ${data_type} USING NULL;`); 
        fkbad.add(`${tableName}.${tmp1.column_name[i]}`);
      }
    }
  }
  
  for (i in columns) {
    if (! tmp3.has(i)) { // add new column if it doesn't exist in the rdb
      data_type = columns[i][1];
      if (rdbRef[tableName].primary_key.indexOf(i) != -1) {
        tmp4 = "''";
        if (data_type == "integer") tmp4 = "0";
        if (data_type == "real") tmp4 = "0.0";
        // how to deal with new columns???
        queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD COLUMN "${i}" ${data_type} DEFAULT ${tmp4};`);
      }
      else queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD COLUMN "${i}" ${data_type};`);
    }
  }
  
  // primary keys part 2

  if (bakaCopySortString(pkeys) != bakaCopySortString(rdbRef[tableName].primary_key)) {
    // add a new primary key
    pkey_tmp = rdbHelper.arrayModifier(rdbRef[tableName].primary_key, function(j) {return `"${j}"`;}).join(",");
    queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD PRIMARY KEY (${pkey_tmp});`); ////
    // remove the NOT NULL constraint on the removed keys...
    for (i=0; i<pkeys.length; i++) if (rdbRef[tableName].primary_key.indexOf(pkeys[i]) == -1 && pkeys[i] in columns) queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${pkeys[i]}" DROP NOT NULL;`);
  }
  
  // unique restraints...
  tmp1 = await client.query("SELECT tc.constraint_name, array_agg(cast(kcu.column_name as text)) FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name WHERE tc.table_name = $1 AND tc.table_schema = '"+mineSchema.replace(/"/g, "")+"' AND tc.constraint_type = 'UNIQUE' group by tc.constraint_name;", [tableName]);

  tmp4 = {};

  for (i=0; i<tmp1.constraint_name.length; i++) tmp4[bakaCopySortString(tmp1.array_agg[i])] = i;

  tmp5 = {};
  if (rdbRef[tableName].unique_keys) {
    for (i=0; i<rdbRef[tableName].unique_keys.length; i++) tmp5[bakaCopySortString(rdbRef[tableName].unique_keys[i])] = i;
  }
  
  for (i in tmp4) {// delete uk not in yaml
    if (! tmp5.hasOwnProperty(i)) {
      queries.push(`ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${tmp1.constraint_name[tmp4[i]]}" CASCADE;`);
    }
  }
  
  var n = Object.keys(tmp4).length;

  for (i in tmp5) { // new uk not in rdb
    if (! tmp4.hasOwnProperty(i)) {
      pkeys = rdbRef[tableName].unique_keys[tmp5[i]];
      
      // add a new unique key
      tmp1 = rdbHelper.arrayModifier(pkeys, function(j) {return `"${j}"`;}).join(",");
      tmp2 = tableName+"_"+n+'_ukey';
      queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD CONSTRAINT "${tmp2}" UNIQUE (${tmp1});`);
      // remove the NOT NULL constraint on the removed keys...

      for (i=0; i<pkeys.length; i++) if (rdbRef[tableName].primary_key.indexOf(pkeys[i]) == -1) queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${pkeys[i]}" DROP NOT NULL;`);
      n++;
    }
  }

  // foreign keys
  await fkTable(queries, tableName, client, fkref);
}

async function fkTable(queries, tableName, client, fkref) {
  if (tableName == "brief_summary_with_hit_score") return;
  
  var tmp1, tmp2, tmp3, tmp4, tmp5, i;
  tmp1 = await client.query(`select array_agg(att2.attname) as "columns", cl.relname as "foreign_table", array_agg(att.attname) as "foreign_columns", con.conname from (select unnest(con1.conkey) as "parent", unnest(con1.confkey) as "child", con1.confrelid, con1.conrelid, relname as "child_table", con1.conname from pg_class cl join pg_namespace ns on cl.relnamespace = ns.oid join pg_constraint con1 on con1.conrelid = cl.oid where ns.nspname = '${mineSchema.replace(/"/g, "")}' and con1.contype = 'f' and relname = $1) con join pg_attribute att on att.attrelid = con.confrelid and att.attnum = con.child join pg_class cl on cl.oid = con.confrelid join pg_attribute att2 on att2.attrelid = con.conrelid and att2.attnum = con.parent group by con.confrelid, cl.relname, con.conname;`, [tableName]);
  
  const fkrefHandler = function(tN, cN, tNalt, constr, primTN) {
    if (fkref === undefined) return;
    if (! (`${tN}.${cN}` in fkref)) fkref[`${tN}.${cN}`] = {};
    if (! (constr in fkref[`${tN}.${cN}`])) fkref[`${tN}.${cN}`][constr] = [primTN, []];
    fkref[`${tN}.${cN}`][constr][1].push(tN, tNalt);
  };
  
  tmp4 = {}; // hash for rdb keys
  for (i=0; i<tmp1.conname.length; i++) {
    tmp2 = tmp1.columns[i]; tmp2 = tmp2.substr(1, tmp2.length-2).split(",");
    tmp3 = tmp1.foreign_columns[i]; tmp3 = tmp3.substr(1, tmp3.length-2).split(",");
    tmp2.forEach(x => {fkrefHandler(tableName, x, tmp1.foreign_table[i], tmp1.conname[i], tableName);});
    tmp3.forEach(x => {fkrefHandler(tmp1.foreign_table[i], x, tableName, tmp1.conname[i], tableName);});
    tmp4[bakaCopySortString(tmp2) + tmp1.foreign_table[i] + bakaCopySortString(tmp3)] = i;
  }
  
  tmp5 = {}; // hash for yaml keys
  if (rdbRef[tableName].foreign_keys) {
    for (i=0; i<rdbRef[tableName].foreign_keys.length; i++) {
      tmp5[bakaCopySortString(rdbRef[tableName].foreign_keys[i][0]) + rdbRef[tableName].foreign_keys[i][1] + bakaCopySortString(rdbRef[tableName].foreign_keys[i][2])] = i;
    }
  }

  for (i in tmp4) {// delete fk not in yaml
    if (! tmp5.hasOwnProperty(i)) queries.push(`ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${tmp1.conname[tmp4[i]]}" CASCADE;`);
  }
  
  for (i in tmp5) { // new fk not in rdb
    if (! tmp4.hasOwnProperty(i)) {
      
      tmp1 = rdbHelper.arrayModifier(rdbRef[tableName].foreign_keys[tmp5[i]][0], function(j) {return `"${j}"`;}).join(",");
      tmp2 = rdbHelper.arrayModifier(rdbRef[tableName].foreign_keys[tmp5[i]][2], function(j) {return `"${j}"`;}).join(",");
      //console.log(rdbRef[tableName].foreign_keys, i);

      if (tmp1 == '"'+__primaryKey__+'"' && tmp2 == '"'+__primaryKey__+'"' && rdbRef[tableName].foreign_keys[tmp5[i]][1] == "brief_summary") queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${rdbRef[tableName].foreign_keys[tmp5[i]][1]}" (${tmp2}) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;`);
      else queries.push(`ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${rdbRef[tableName].foreign_keys[tmp5[i]][1]}" (${tmp2}) DEFERRABLE INITIALLY DEFERRED;`);
      
    }
  }
}


var jobcontainer = [];

export async function schemaPrep(config, rdb_def, dbconnect) {
  [sql_typing, sql_PK, sql_PKref, sql_struct, index_elementFields, index_attribFields, keyword_fields, brief_summary_update_date_IDX, mineSchema, __primaryKey__, rdbRef] = rdbHelper.init(rdb_def);
  if (config.argv["skip-schema"]) console.warn("Skipping schema upgrade for", mineSchema);
  else await upgradeSchema(config, dbconnect);
}

export async function init(config, rdb_def) {
  await schemaPrep(config, rdb_def);

  var workers = [], worker;
  const obj = {workers, rdb_def, jobs: [], entries_processed: [], scandone: false, jobId: jobcontainer.length, config, waiter: new general.Deferred()}; jobcontainer.push(obj);

  cluster.setupMaster({
    exec: './modules/rdb-worker.js',
    args: [obj.jobId]
  });

  for (var i=0; i<config.rdb.nworkers; i++) {
    worker = cluster.fork();
    worker.on("message", respond2Worker);
    worker.on("error", console.error);
    workers.push(worker);
    worker.on("exit", async function() {
      obj.workers.splice(obj.workers.indexOf(this), 1);
      if (obj.workers.length == 0 && ! ("test-entry" in config.argv)) {
        await removeObsolete(obj);
        obj.waiter.resolve();
      }
    });
  }

  return obj;
}

function respond2Worker(msg) {
  if (msg.cmd == "init") {
    const jc = jobcontainer[msg.jobId];
    return this.send({cmd: "init", payload: {rdb_def: jc.rdb_def, scriptStartDate, config: jc.config}});
  }
  if (msg.cmd == "getjob") {
    const jc = jobcontainer[msg.jobId];
    if (! jc) {
      console.log("unknown jobId", msg.jobId);
      process.exit();
    }
    if (msg.entryId) {
      jc.entries_processed.push(msg.entryId);
      delete msg.entryId;
    }
    if (jc.jobs.length == 0) {
      if (jc.scandone) return this.send({cmd: "done"});
      else {
        var worker = this;
        return setImmediate(() => {respond2Worker.apply(worker, [msg]);});
      }
    }
    else {
      this.send({cmd: "job", payload: jc.jobs.shift()});
    }
  }
}

export async function removeObsolete(jc) {
  const pool = new rdbHelper.nativePSQLpool(jc.config.rdb.constring, 1);
  
  const in_pdb = new Set(jc.entries_processed);
  const remove_ids = (await pool.query(`select ${__primaryKey__} from ${mineSchema}.brief_summary`))[__primaryKey__].filter(x=>(! in_pdb.has(x)));
  if (remove_ids.length) {
    const stuff = remove_ids.map((x,i)=>`$${i+1}`).join(",");
    await pool.query(`delete from ${mineSchema}.brief_summary where ${__primaryKey__} in (${stuff})`, remove_ids);
  }

  pool.end();
}


var sql_typing, sql_PK, sql_PKref, sql_struct, index_elementFields, index_attribFields, keyword_fields , brief_summary_update_date_IDX, rdbRef, mineSchema, __primaryKey__;
