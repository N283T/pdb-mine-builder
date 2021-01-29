
const cluster = await import("cluster");
const fs = await import("fs");
const fsp = fs.promises;
const pgformat = await import("pg-format");

const rdbHelper = await import("./rdb-helper.js");

var rdb_def, scriptStartDate, config, pipeline, sql_typing, sql_PK, sql_PKref, sql_struct, index_elementFields, index_attribFields, keyword_fields, brief_summary_update_date_IDX, mineSchema, __primaryKey__, rdbRef, dbconnect;

const jobId = process.argv[2];

async function processEntry(payload) {
  var jso;
  if (! payload.entryId) jso = await pipeline.load_data(payload, config);

  var memObj = {entryId: payload.entryId, mmjson: {}, sql: {}, updates: [], inserts: [], deletes: [], newEntry: false, mtime: payload.mtime, payload};

  var tableNames = Object.keys(sql_typing);
  var results = dbconnect.query(tableNames.map(table => pgformat.default("select * from %I.%I where %I=%L;", mineSchema, table, __primaryKey__, memObj.entryId)).join(" ")); 
  
  if (jso === undefined) jso = await pipeline.load_data(payload, config);
  if (jso == null) return getJob();
  
  var c_, nor, tbl_nfo, col_nfo, columnName, column, r;
  for (const [dataName, data] of Object.entries(jso)) for (const [tableName, table] of Object.entries(data)) {
    memObj.mmjson[tableName] = table;
    
    tbl_nfo = sql_typing[tableName];
    if (! tbl_nfo) continue; // skip unknown tables...

    nor = Object.values(table)[0].length;
    for ([columnName, column] of Object.entries(table)) {
      c_ = columnName.replace(/\[/g, "").replace(/\]/g, "");
      if (columnName != c_) {
        table[c_] = column;
        delete table[columnName];
        columnName = c_;
      }
      col_nfo = tbl_nfo[columnName];
      if (! col_nfo) continue; // skip unknown columns
      for (r=0; r<nor; r++) {
        if (column[r] instanceof Array) { // deal with arrays, since the xsd can't
          if (column[r][0] == null) column[r] = null;
          else column[r] = rdbHelper.removeNull(column[r]).join("-");
        }
        column[r] = col_nfo(column[r]);
      }
    } 
  }

  results = await results;
  results.forEach((table, idx) => memObj.sql[tableNames[idx]] = table);
  await pipeline.brief_summary(memObj, __primaryKey__, config);
  processKeywords(memObj);
  
  Object.keys(sql_typing).map(e => deltaTable(e, memObj));
  await updateRDB(memObj);
  
  //console.log("done", memObj.entryId);
  
  getJob(memObj.entryId);
}

// compare the contents of the SQL data with the mmjson data for a single table/category
function deltaTable(table, memObj) {
  var from_mmjson = memObj.mmjson[table];
  var from_sql = memObj.sql[table];
  
  if (table == "brief_summary") {
    if (from_sql) from_sql.update_date[0] = null; // set it to ignore the update_date
    if (! from_sql || from_sql[__primaryKey__].length == 0) memObj.newEntry = true;
  }
  
  var mmjson_hash = {}, sql_hash = {}, bad;
  
  var inserts = [], updates = [], deletes = [], cols, c, r_m, r_s, m_v, s_v;
  var pk = sql_PK[table], k, nor, rpk, r, isdate = pk.map(x => false);
  nor = from_sql ? from_sql[__primaryKey__].length : 0;
  
  for (r=0; r<nor; r++) {
    rpk = [];
    bad = false;
    for (k=0; k<pk.length; k++) {
      if (! (pk[k][0] in from_sql)) {bad=true; break;}
      s_v = from_sql[pk[k][0]][r];
      if (from_sql[pk[k][0]][r] instanceof Date) {
        s_v = (new Date(s_v.getTime() - s_v.getTimezoneOffset()*60000)).getTime();
        isdate[k] = true;
      }
      rpk.push(s_v);
    }
    
    if (!bad) sql_hash[JSON.stringify(rpk)] = r;
  }

  try {nor = from_mmjson ? from_mmjson[pk.length ? pk[0][0] : __primaryKey__].length : 0;}
  catch (e) {nor = Object.values(from_mmjson)[0].length;}
  for (r=0; r<nor; r++) {
    rpk = [];
    bad = false;
    for (k=0; k<pk.length; k++) {
      if (! (pk[k][1] in from_mmjson)) {bad=true; break;}
      m_v = from_mmjson[pk[k][1]][r];
      if (isdate[k]) m_v = new Date(m_v).getTime()
      rpk.push(m_v);
    }
    if (!bad) mmjson_hash[JSON.stringify(rpk)] = r;
  }

  
  var tbl_struct = sql_struct[table];
  for (r in mmjson_hash) {
    if (r in sql_hash) {
      r_m = mmjson_hash[r];
      r_s = sql_hash[r];
      cols = [];
      for (c=0; c<tbl_struct.length; c++) {
        s_v = tbl_struct[c][0] in from_sql ? from_sql[tbl_struct[c][0]][r_s] : null;
        m_v = tbl_struct[c][1] in from_mmjson ? from_mmjson[tbl_struct[c][1]][r_m] : null;
        
        if (s_v instanceof Date) {
          s_v = new Date(s_v.getTime() - s_v.getTimezoneOffset()*60000);
          if (s_v.getTime() != new Date(m_v).getTime()) cols.push(c);
        }
        else if (s_v instanceof Array) {
          if ((s_v.length || m_v.length) && (s_v.length != m_v.length || ! s_v.every(function(element, idx) {return element === m_v[idx];}))) {
            cols.push(c);
          }}
        else {if (s_v !== m_v) cols.push(c);}
      }
      if (cols.length) updates.push([sql_hash[r], mmjson_hash[r], cols]); // sql row id, mmjson row id, columns-to-update list
    } // maybe update --> first perform row delta
    else inserts.push(mmjson_hash[r]); // row to insert from mmjson
  }
  for (r in sql_hash) {
    if (! (r in mmjson_hash)) deletes.push(sql_hash[r]); // row to delete from sql
  }
  
  
  if (table == "brief_summary") {
    if (inserts.length) memObj.inserts.unshift([table, inserts]);
    if (updates.length) memObj.updates.unshift([table, updates]);
    if (deletes.length) memObj.deletes.unshift([table, deletes]);
  }
  else {
    if (inserts.length) memObj.inserts.push([table, inserts]);
    if (updates.length) memObj.updates.push([table, updates]);
    if (deletes.length) memObj.deletes.push([table, deletes]);
  }
}

// generate insert/delete/update queries to sync the SQL data with the mmjson data
async function updateRDB(memObj) {
  var queries = [], keys, values, table, data, from_mmjson, from_sql, rid, rid2, cidx, c, cols, where, pk, colnames, i, ins, col, upd, e, client, q, opts, chunk, del;
  
  if (memObj.inserts.length || memObj.deletes.length || memObj.updates.length) {
    if (! memObj.newEntry) {
      c = sql_struct.brief_summary.map(x => x[0]).indexOf("update_date");
      for (i=0; i<memObj.updates.length; i++) if (memObj.updates[i][0] == "brief_summary") {memObj.updates[i][1][0][2].push(c); break;}
      if (i == memObj.updates.length) memObj.updates.push(["brief_summary", [[0, 0, [c]]]]);
    }

    memObj.mmjson.brief_summary.update_date[0] = scriptStartDate;
    
    client = await dbconnect.connect();
    await client.query("BEGIN");
  }
  
  
  for (ins of memObj.inserts) {
    table = ins[0];
    data = ins[1]; from_mmjson = memObj.mmjson[table]; 
    values = [];
    cols = sql_struct[table].filter(c => c[1] in from_mmjson);
    
    colnames = [__primaryKey__, ...cols.map(c=>c[1])];
    for (rid of data) {
      values.push(memObj.entryId);
      cols.forEach(col => values.push(from_mmjson[col[1]][rid]));
      if (values.length >= 30000) { // chunks of ~ 30000 items...
        q = `insert into %I.%I (${colnames.map(x => "%I").join(",")}) values ${rdbHelper.expand(values.length/colnames.length, colnames.length)}`;
        await rdbHelper.sendQuery(client, q, values, [mineSchema, table, ...colnames]);
        values = [];
      }
    }
    if (values.length) {
      q = `insert into %I.%I (${colnames.map(x => "%I").join(",")}) values ${rdbHelper.expand(values.length/colnames.length, colnames.length)}`;
      await rdbHelper.sendQuery(client, q, values, [mineSchema, table, ...colnames]);
    }
  }

  for (upd of memObj.updates) {
    table = upd[0]; cols = sql_struct[table]; pk = sql_PK[table];
    data = upd[1]; from_mmjson = memObj.mmjson[table]; from_sql = memObj.sql[table];
    
    for ([rid, rid2, cidx] of data) {
      keys = []; values = [];
      for (col of cidx) {
        keys.push(cols[col][0]);
        if (cols[col][0] in from_mmjson) values.push(from_mmjson[cols[col][0]][rid2]);
        else values.push(null);
      }
      q = keys; 
      opts = [mineSchema, table, ...keys]; keys = [__primaryKey__]; values.push(memObj.entryId);
      for (c of pk) {keys.push(c[0]); values.push(from_sql[c[0]][rid]);}
      where = keys.map((x,i)=>"%I=$"+(i+opts.length-1)).join(" AND "); opts.push(...keys);
      if (q.length == 1) q = `UPDATE %I.%I SET %I=$1 where ${where}`;
      else q = `UPDATE %I.%I SET (${q.map(x=>"%I").join(",")})=(${q.map((x,i)=>"$"+(i+1)).join(",")}) where ${where}`;
      await rdbHelper.sendQuery(client, q, values, opts);
    }
  }

  for (del of memObj.deletes) {
    table = del[0]; pk = sql_PK[table]
    data = del[1]; from_sql = memObj.sql[table];

    for (rid of data) {
      opts = [mineSchema, table, __primaryKey__]; values = [memObj.entryId];
      for (c of pk) {opts.push(c[0]); values.push(from_sql[c[0]][rid]);}
      where = values.map((x,i)=>"%I=$"+(i+1)).join(" AND ");
      q = "DELETE from %I.%I where "+where;
      await rdbHelper.sendQuery(client, q, values, opts);
    }
  }
  
  if (client) {
    await client.query("COMMIT");
    client.release();
  }

  //console.log('done', memObj.entryId);
  
}

function processKeywords(memObj) {
  var tbl = memObj.mmjson.brief_summary;
  
  var eF, aF, cat, pkref, t, tbl_nfo, nor, c, r, pk, col_nfo;
  
  tbl.keywords = [];
  
  // extract additional data from mmjson
  for (t in memObj.mmjson) {
    if (t == "brief_summary" || ! (t in sql_PK)) continue;
    cat = memObj.mmjson[t];
    tbl_nfo = sql_typing[t];
    pkref = sql_PKref[t];
    nor = cat[Object.keys(cat)[0]].length;

    if (t in keyword_fields) {
      eF = keyword_fields[t];
      for (c in cat) {
        if (c in eF) tbl.keywords = tbl.keywords.concat(cat[c]); // how about some additional checks to remove junk? (e.g. integers and such)
      }
    }
  
    pk = sql_PK[t];
    for (c=0; c<pk.length; c++) { // work around very crappy xsd file messing up rdb...
      if (! (pk[c][1] in cat)) {
        cat[pk[c][1]] = [];
        col_nfo = tbl_nfo[pk[c][1]](null, true);
        for (r=0; r<nor; r++) cat[pk[c][1]].push(col_nfo);
      }
    }
    
  }
  
  // clean keywords
  tbl.keywords = rdbHelper.cleanArray(tbl.keywords.unique());
  for (var i=0; i<tbl.keywords.length; i++) tbl.keywords[i] = tbl.keywords[i].toLowerCase();
  tbl.keywords = tbl.keywords.unique();
  tbl.keywords.sort();
  tbl.keywords = [tbl.keywords];
}

async function respond2Main(msg) {
  if (msg.cmd == "init") {
    init(msg.payload);
  }
  else if (msg.cmd == "done") {
    process.exit();
  }
  else if (msg.cmd == "job") {
    try {
      processEntry(msg.payload);
    }
    catch (e) {
      console.error(`Error processing ${msg.payload.entryId}...`, e);
    }
  }
}

function getJob(entryId) {
  process.send({cmd: "getjob", jobId, entryId});
}

async function init(payload) {
  rdb_def = payload.rdb_def;
  scriptStartDate = payload.scriptStartDate;
  config = payload.config;
  global.config = config;
  global.moduleFolder = config.moduleFolder;
  global.pipelineFolder = config.pipelineFolder;
 
  pipeline = await import(config.pipeline);

  [sql_typing, sql_PK, sql_PKref, sql_struct, index_elementFields, index_attribFields, keyword_fields, brief_summary_update_date_IDX, mineSchema, __primaryKey__, rdbRef] = rdbHelper.init(rdb_def);

  dbconnect = new rdbHelper.nativePSQLpool(config.rdb.constring, 1);
  getJob();
}

if (! cluster.isMaster) {
  process.on("message", respond2Main);
  process.send({cmd: "init", jobId});
}


// update brief_summary table stuff


// initialize schema data structure
