const pgnat = await import("./pg-native-custom.js");
const general = await import("./general.js");
const crypto = await import("crypto");
const pgformat = await import("pg-format");
const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const cif = await import("../modules/cif.js");

export function expand(rowCount, columnCount, startAt=1){
  var index = startAt
  return Array(rowCount).fill(0).map(v => `(${Array(columnCount).fill(0).map(v => `$${index++}`).join(", ")})`).join(", ")
}

export function sendQuery(client, query, values, options) {
  if (options) query = pgformat.default(query, ...options);
  if (query.startsWith("select")) return client.query(query, values);
  values = values.map(prepareValue);
  //console.log(query, values); return;
  return client.query(query, values);
}

export function nativePSQLpool(constring, max) {
  if (new.target === undefined) return new nativePSQLpool(constring, max);
  this.constring = constring;
  this.max = max || 1;
  this.clients = [];
  this.pool = [];
  this.queue = [];
}

nativePSQLpool.prototype.connect = async function() {
  if (this.pool.length) return this.pool.shift();
  if (this.clients.length < this.max) {
    const poolObj = this;
    const pgnat = await import("./pg-native-custom.js");
    if (this.clients.length < this.max) {
      const client = pgnat.Client();
      client.release = function() {
        if (poolObj.queue.length) poolObj.queue.shift().resolve(this);
        else poolObj.pool.push(this);
      }; 
      this.clients.push(client);
      await client.connect(this.constring);
      return client;
    }
  }
  
  const waiter = new general.Deferred();
  this.queue.push(waiter);
  return waiter.promise;
}
nativePSQLpool.prototype.query = async function(text, values, rowMode) {
  const client = await this.connect();
  client.rowMode = rowMode;
  const output = await client.query(text, values);
  client.rowMode = false;
  client.release();
  return output;
};

nativePSQLpool.prototype.end = async function() {
  this.pool = [];
  for (var client of this.clients) await client.end();
};

export function arrayModifier(arr, func) {
  var temp = [];
  arr.forEach(function(i, idx, self) {temp[idx] = func(i);});
  return temp;
}

const cif2sqlTypeConversion = {line_array: "text[]", int: "integer", positive_int: "integer", bigint: "bigint", float: "double precision", double: "double precision", date: "date", "yyyy-mm-dd": "date", timestamp: "timestamp with time zone", "yyyy-mm-dd:hh:mm": "timestamp with time zone", "yyyy-mm-dd:hh:mm-flex": "text", serial: "serial", boolean: "boolean"};
const cif_kwTypes = new Set(["text", "orcid_id", "pdbx_PDB_obsoleted_db_id", "pdbx_related_db_id", "exp_data_doi", "pdb_id", "author", "emd_id"]);

function is_subset_of(list, parent) {
  var tmp = new Set(parent);
  return list.every(x => tmp.has(x));
};

// rdb-worker stuff

export function deltaTable(table, memObj, sql_PK, sql_struct, __primaryKey__, sqlMode) {
  var from_mmjson = memObj.mmjson[table];
  var from_sql = memObj.sql[table];
  
  if (table == "brief_summary") {
    if (from_sql && ! sqlMode) from_sql.update_date[0] = null; // set it to ignore the update_date
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
        s_v = s_v.getTime();
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
      if (isdate[k]) {
        if (sqlMode) m_v = m_v.getTime();
        else m_v = new Date(m_v).getTime();
      }
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
          if (! sqlMode) m_v = new Date(m_v);
          if (s_v.getTime() != m_v.getTime()) cols.push(c);
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
export async function updateRDB(memObj, setDate, sql_PK, sql_struct, mineSchema, __primaryKey__, dbconnect) {
  var queries = [], keys, values, table, data, from_mmjson, from_sql, rid, rid2, cidx, c, cols, where, pk, colnames, i, ins, col, upd, e, client, q, opts, chunk, del;
  
  if (memObj.inserts.length || memObj.deletes.length || memObj.updates.length) {
    if (setDate !== undefined) {
      if (! memObj.newEntry) {
        c = sql_struct.brief_summary.map(x => x[0]).indexOf("update_date");
        for (i=0; i<memObj.updates.length; i++) if (memObj.updates[i][0] == "brief_summary") {memObj.updates[i][1][0][2].push(c); break;}
        if (i == memObj.updates.length) memObj.updates.push(["brief_summary", [[0, 0, [c]]]]);
      }
      memObj.mmjson.brief_summary.update_date[0] = setDate;
    }
    
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
        q = `insert into %I.%I (${colnames.map(x => "%I").join(",")}) values ${expand(values.length/colnames.length, colnames.length)}`;
        await sendQuery(client, q, values, [mineSchema, table, ...colnames]);
        values = [];
      }
    }
    if (values.length) {
      q = `insert into %I.%I (${colnames.map(x => "%I").join(",")}) values ${expand(values.length/colnames.length, colnames.length)}`;
      await sendQuery(client, q, values, [mineSchema, table, ...colnames]);
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
      await sendQuery(client, q, values, opts);
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
      await sendQuery(client, q, values, opts);
    }
  }
  
  if (client) {
    await client.query("COMMIT");
    client.release();
  }

  //console.log('done', memObj.entryId);
  
}

// end rdb-worker stuff

export async function import_rdb_def(deffile, config) {
  const rdb_def = yaml.safeLoad(await fsp.readFile(general.expandPath(deffile), 'utf8'));
  rdb_def.tables = rdb_def.tables || {};

  var primaryKey = rdb_def.config.primaryKey, primaryKeyFormat = rdb_def.config.primaryKeyFormat || "text";
  var typeRefRef = {}, doc, i, catName, tblRef = {}, tbl, typeRef = {}, mandatoryRef = new Set(), typecode, colName, fgroups, ilgl, id, fkey_cache, fkey, key, part, child_tab, child_col, parent_tab, parent_col, id1, id2, ok;
  
  var cifDicts = rdb_def.config.cifDicts || {};

  for (let dict of cifDicts) {
    const parser = new cif.CIFparser();
    await general.readlineGZ(general.expandPath(dict), function(line) {
      parser.parseLine(line);
      if (parser.error) {
        console.error(`Error found in line ${parser.error[1]}:`);
        console.error("  ", parser.error[2]);
        console.log("  ", parser.error[0]);
        parser.error = null;
      }
    });
    
    // implement...
    doc = Object.values(parser.data)[0];

    for (i in doc) {
      if (! i.startsWith("save_") || i[5] == "_") continue;
      catName = i.slice(5);
      if (catName == "datablock") continue;
      rdb_def.tables.push(tblRef[catName] = tbl = {});
      typeRef[catName] = {};
      tbl.name = catName;
      tbl.columns = [[primaryKey, primaryKeyFormat]];
      tbl.primary_key = [primaryKey, ...doc[i].category_key.name.filter(x => x.split(".")[1] != primaryKey).map(x => x.split(".")[1])];
      tbl.foreign_keys = [[[primaryKey], "brief_summary", [primaryKey]]];
      tbl.unique_keys = [];
      tbl.keywords = [];
      typeRef[catName][primaryKey] = primaryKeyFormat;
      mandatoryRef.add(`${catName}.${primaryKey}`);
    }
    
    for (i in doc) {
      if (! i.startsWith("save__")) continue;
      
      try {typecode = doc[i].item_type.code[0];}
      catch (e) {continue;}
      if (! typecode) continue;
      typeRefRef[i.slice(6)] = typecode;
      if ("item_linked" in doc[i]) doc[i].item_linked.child_name.forEach(x => typeRefRef[x.slice(1)] = typecode);
    }
    
    for (i in doc) {
      if (! i.startsWith("save__")) continue;
      [catName, colName] = i.slice(6).split(".", 2);
      colName = colName.replace(/\[/g, "").replace(/\]/g, "").replace(/\//g, "").replace(/\%/g, "");
      tbl = tblRef[catName];
      
      if (colName != primaryKey) { // maybe also do this more advanced type matching for mmjson?????
        if (! ("item_type" in doc[i])) {
          try {typecode = typeRefRef[i.slice(6)] || typeRefRef[doc[i].item_linked.parent_name[0].slice(1)];}
          catch (e) {typecode = undefined;}
        }
        else {
          try {typecode = doc[i].item_type.code[0];}
          catch (e) {typecode = undefined;}
        }

        typeRef[catName][colName] = cif2sqlTypeConversion[typecode] || "text";
        tbl.columns.push([colName, typeRef[catName][colName]]);
        
        try {if (doc[i].item.mandatory_code[0] == "yes") mandatoryRef.add(`${catName}.${colName}`);}
        catch (e) {}
        
        if (cif_kwTypes.has(typecode) && ! doc[i].item_enumeration) tbl.keywords.push(colName);
      }
      else tbl.pkout = true;
    }
    
    if ("pdbx_item_linked_group_list" in doc) {
      fgroups = {};
      ilgl = doc.pdbx_item_linked_group_list;
      for (i=0; i<ilgl.child_category_id.length; i++) {
        id = ilgl.child_category_id[i]+":"+ilgl.parent_category_id[i]+":"+ilgl.link_group_id[i];
        if (! (id in fgroups)) fgroups[id] = [];
        
        //if (ilgl.parent_category_id[i] == "entity_poly_seq" && ilgl.child_category_id[i] == "pdbx_poly_seq_scheme") console.log(ilgl.child_name[i].slice(1), ilgl.parent_name[i].slice(1));
        
        fgroups[id].push([ilgl.child_name[i].slice(1), ilgl.parent_name[i].slice(1)])
      }
      
      fkey_cache = new Set();
      
      for ([id, fkey] of Object.entries(fgroups)) {
        key = [["pdbid"], null, ["pdbid"]];
        for (part of fkey) {
          [child_tab, child_col] = part[0].split(".", 2);
          [parent_tab, parent_col] = part[1].split(".", 2);
          child_col = child_col.replace(/\[/g, "").replace(/\]/g, "").replace(/\//g, "").replace(/\%/g, "");
          parent_col = parent_col.replace(/\[/g, "").replace(/\]/g, "").replace(/\//g, "").replace(/\%/g, "");
 
          key[0].push(child_col);
          key[1] = parent_tab;
          key[2].push(parent_col);
        }
        if (key[1] == null) continue; // skip junk

        id1 = `${child_tab}(${[...key[0]].sort().join("|")})${parent_tab}(${[...key[2]].sort().join("|")})`;
        id2 = `${parent_tab}(${[...key[2]].sort().join("|")})${child_tab}(${[...key[2]].sort().join("|")})`;
        if (fkey_cache.has(id1) || fkey_cache.has(id2)) continue; // is this really what we want? shouldn't this be directional? (so only id1 should be checked, not also id2....)
      
        ok = true;
        for (i=0; i<key[0].length; i++) {
          if (typeRef[child_tab][key[0][i]] != typeRef[parent_tab][key[2][i]]) ok = false;
          if (! mandatoryRef.has(`${child_tab}.${key[0][i]}`)) ok = false;
          if (! mandatoryRef.has(`${parent_tab}.${key[2][i]}`)) ok = false;
        }
        
        if (key[0].unique().length != key[0].length || key[2].unique().length != key[2].length) ok = false; // number of items is not unique
        if (! is_subset_of(tblRef[parent_tab].primary_key, key[2])) ok = false; // items not unique
        if (! ok) continue;
        
        fkey_cache.add(id1);
        tblRef[child_tab].foreign_keys.push(key);
        if (tblRef[parent_tab].primary_key.length != key[2].length && tblRef[parent_tab].unique_keys.filter(x => JSON.stringify(x) == JSON.stringify(key[2])) == 0) tblRef[parent_tab].unique_keys.push(key[2]);
      }
    }
  }
  
  const hashPKey = rdb_def.hashPKey || {};
  for (let [k,v] of Object.entries(hashPKey)) {
    for (let field of v) {
      let idx = tblRef[k].columns.findIndex(x => x[0] == field);
      if (idx != -1) {
        tblRef[k].columns.splice(idx+1, 0, ["_hash_"+field, "text"]);
        idx = tblRef[k].primary_key.findIndex(x => x == field);
        if (idx != -1) tblRef[k].primary_key[idx] = "_hash_"+field;
      }
    }
  }
  delete rdb_def.hashPKey;
  delete rdb_def.cifDicts;
  
  return rdb_def;
}

export function init(rdb_setup) {
  // instead of loading the schema file, load the dictionaries and generate the object from there....
  
  var sql_typing = {}, sql_PK = {}, sql_PKref = {}, sql_struct = {}, index_elementFields, index_attribFields, keyword_fields = {}, brief_summary_update_date_IDX, rdbRef = {}, __primaryKey__ = rdb_setup.config.primaryKey, mineSchema = rdb_setup.config.schema;
  
  
  var data_type, i, j, cn, pkref;
  for (i=0; i<rdb_setup.tables.length; i++) {
    
    rdbRef[rdb_setup.tables[i].name] = rdb_setup.tables[i];
    
    pkref = sql_PKref[rdb_setup.tables[i].name] = {};
    sql_PK[rdb_setup.tables[i].name] = [];
    
    for (j=0; j<rdb_setup.tables[i].primary_key.length; j++) {
      cn = rdb_setup.tables[i].primary_key[j];
      if (cn != __primaryKey__) {
        sql_PK[rdb_setup.tables[i].name].push([rdb_setup.tables[i].primary_key[j], cn]);
        sql_PKref[rdb_setup.tables[i].name][cn] = 1;
      }
    }
    
    sql_typing[rdb_setup.tables[i].name] = {};
    sql_struct[rdb_setup.tables[i].name] = [];
    for (j=0; j<rdb_setup.tables[i].columns.length; j++) {
      cn = rdb_setup.tables[i].columns[j][0];
      if (rdb_setup.tables[i].columns[j][1] == "double precision" || rdb_setup.tables[i].columns[j][1] == "real") {
        if (pkref[cn]) data_type = enforceFloatPK;
        else data_type = enforceFloat;
      }
      else if (rdb_setup.tables[i].columns[j][1] == "integer") {
        if (pkref[cn]) data_type = enforceIntegerPK;
        else data_type = enforceInteger;
      }
      else if (rdb_setup.tables[i].columns[j][1] == "bigint") {
        if (pkref[cn]) data_type = enforceBigIntegerPK;
        else data_type = enforceBigInteger;
      }
      else if (rdb_setup.tables[i].columns[j][1] == "serial") data_type = enforceInteger;
      else if (rdb_setup.tables[i].columns[j][1] == "bigserial") data_type = enforceBigInteger;
      else if (rdb_setup.tables[i].columns[j][1] == "text" || rdb_setup.tables[i].columns[j][1] == "char(4)") {
        if (pkref[cn]) data_type = enforceStringPK;
        else data_type = enforceString;
      }
      else if (rdb_setup.tables[i].columns[j][1] == "citext") data_type = enforceStringLC;
      else if (rdb_setup.tables[i].columns[j][1] == "date") data_type = enforceDate;
      else if (rdb_setup.tables[i].columns[j][1] == "timestamp without time zone" || rdb_setup.tables[i].columns[j][1] == "timestamp with time zone") data_type = enforceTimestamp;
      else if (rdb_setup.tables[i].columns[j][1] == "text[]") data_type = enforceStringArray;
      else if (rdb_setup.tables[i].columns[j][1] == "boolean") data_type = enforceBoolean;
      else data_type = defaultType;
      sql_typing[rdb_setup.tables[i].name][cn] = data_type;
      if (cn != __primaryKey__) sql_struct[rdb_setup.tables[i].name].push([rdb_setup.tables[i].columns[j][0], cn]);
    }
        
    keyword_fields[rdb_setup.tables[i].name] = {};
    for (j=0; j<rdb_setup.tables[i].keywords.length; j++) keyword_fields[rdb_setup.tables[i].name][rdb_setup.tables[i].keywords[j]] = true;
  }
  
  index_elementFields = {};
  for (var e in rdb_setup.index_elementFields) {
    index_elementFields[e] = {};
    for (var i=0; i<rdb_setup.index_elementFields[e].length; i++) index_elementFields[e][rdb_setup.index_elementFields[e][i]] = true;
  }
  
  index_attribFields = {};
  for (var e in rdb_setup.index_attribFields) {
    index_attribFields[e] = {};
    for (var i=0; i<rdb_setup.index_attribFields[e].length; i++) index_attribFields[e][rdb_setup.index_attribFields[e][i]] = true;
  }
  
  for (i=0; i<sql_struct.brief_summary.length; i++) if (sql_struct.brief_summary[i][0] == "update_date") {brief_summary_update_date_IDX = i; break;}
  
  return [sql_typing, sql_PK, sql_PKref, sql_struct, index_elementFields, index_attribFields, keyword_fields , brief_summary_update_date_IDX, mineSchema, __primaryKey__, rdbRef];
}

export function gen_docid(inp) {
  inp = inp.ljust(4, " ");
  var components = []
  for (var i=0; i<4; i++) {
    if (inp[i] == " ") components.push(36); // an empty space is classified as char type 36
    else components.push(parseInt(inp[i], 36)); // ranges from 0-35
  }
  return components[0] << 24 | components[1] << 16 | components[2] << 8 | components[3];
}

export function mmjsonAt(table, get_field, cond_field, cond_val) {
  var out = [], i;
  if (! table || ! (get_field in table) || ! (cond_field in table)) return out;
  for (i=0; i<table[get_field].length; i++) if (table[cond_field][i] == cond_val) out.push(table[get_field][i]);
  return out;
}

export function mmjsonAt_IC(table, get_field, cond_field, cond_val) {
  cond_val = cond_val.toLowerCase();
  var out = [], i;
  if (! table || ! (get_field in table) || ! (cond_field in table)) return out;
  for (i=0; i<table[get_field].length; i++) if (table[cond_field][i].toLowerCase() == cond_val) {out.push(table[get_field][i]);}
  return out;
}

export function mmjsonGet(table, get_field, n) {
  if (table && get_field in table) {
    if (n || n == 0) return table[get_field][n];
    else return table[get_field];
  }
  if (n || n == 0) return null;
  else return [];
}

// sha256 hash...
export function hex_sha256(s){return crypto.createHash('sha256').update(s).digest('hex');}

Array.prototype.unique = function () {
  return Array.from(new Set(this));
};

export function getObjectValue(object, field, defaultValue) {
  if (field in object) return object[field];
  else return defaultValue;
}

String.prototype.ljust = function(length, chr) {
  if (arguments.length < 2) chr = " ";
  var fill = [];
  while (fill.length+this.length<length) fill[fill.length] = chr;
  return this + fill.join('');
}

String.prototype.rjust = function(length, chr) {
  if (arguments.length < 2) chr = " ";
  var fill = [];
  while (fill.length+this.length<length) fill[fill.length] = chr;
  return fill.join('') + this;
}

export function str(inp) {return inp+'';}


export function cleanArray(array) {
  array = Array.from(new Set(array));
  var idx = array.indexOf(null);
  if (idx != -1) array.splice(idx, 1);
  var idx = array.indexOf(undefined);
  if (idx != -1) array.splice(idx, 1);
  var idx = array.indexOf('');
  if (idx != -1) array.splice(idx, 1);
  array.sort();
  return array;
}

export function removeNull(array) {
  return array.filter(function(val) {return val != null;});
}

function sqlSavePTArray(i) {
  return out = "'{" + i.join(",") + "}'";
}

function enforceStringPK(i) { // find some way to deal with ranges....
  if (i == null) return "";
  if (i instanceof Array) return i.join('-');
  return i+'';
}

function enforceString(i) { // find some way to deal with ranges....
  if (i == null) return i;
  if (i instanceof Array) return i.join('-');
  return i+'';
}

function enforceStringLC(i) { // find some way to deal with ranges....
  if (i == null) return i;
  if (i instanceof Array) return i.join('-').toLowerCase();
  return (i+'').toLowerCase();
}

function enforceInteger(i) {
  if (i == null) return null;
  var tmp = parseInt(i);
  return isNaN(tmp) ? null : tmp;
}

function enforceBoolean(i) {
  if (i === true || i === 1 || (i+"").toLowerCase() === "true") return true;
  if (i === false || i === 0 || (i+"").toLowerCase() === "false") return false;
  return null;
}

function enforceIntegerPK(i) {
  if (i == null) return 0;
  else return parseInt(i);
}

function enforceBigInteger(i) {
  if (i == null) return null;
  var tmp = BigInt(i);
  return isNaN(tmp) ? null : tmp;
}

function enforceBigIntegerPK(i) {
  if (i == null) return 0;
  else return BigInt(i);
}

function defaultType(i) {return i;}

function enforceFloat(i) {
  if (i == null) return null;
  var tmp = parseFloat(parseFloat(i).toPrecision(15));
  return isNaN(tmp) ? null : tmp;
} 

function enforceFloatPK(i) {
  if (i == null) return 0.0;
  else return parseFloat(parseFloat(i).toPrecision(15));
} 

function enforceDate(i) {
  if (i) { // work around crappy cif data (primarily chem_comp)
    i = i.split("-");
    if (i[0].length < 4) {
      if (parseInt(i[0]) < 50) i[0] = "20"+i[0];
      else i[0] = "19"+i[0];
    }
    if (i[1].length < 2) i[1] = "0"+i[1];
    if (i[2].length < 2) i[1] = "0"+i[2];
    i = i.join("-");
  }
  return i;
}

function enforceTimestamp(i) {
  if (i == null) return null;
  return i;
}

export function enforceStringArray(col) {
  if (! (col instanceof Array)) col = [col];
  return col.map(x => x ? x+"" : null);
}

// pg util

export const prep_defaults = {parseInputDatesAsUTC: false};
// from https://github.com/brianc/node-postgres/blob/36342c9a84b68123f666879a9f34ac319a44727a/packages/pg/lib/utils.js
function prepareValue (val, seen) {
  if (val instanceof Buffer) {
    return val
  }
  if (ArrayBuffer.isView(val)) {
    var buf = Buffer.from(val.buffer, val.byteOffset, val.byteLength)
    if (buf.length === val.byteLength) {
      return buf
    }
    return buf.slice(val.byteOffset, val.byteOffset + val.byteLength) // Node.js v4 does not support those Buffer.from params
  }
  if (val instanceof Date) {
    if (prep_defaults.parseInputDatesAsUTC) {
      return dateToStringUTC(val)
    } else {
      return dateToString(val)
    }
  }
  if (Array.isArray(val)) {
    return arrayString(val)
  }
  if (val === null || typeof val === 'undefined') {
    return null
  }
  if (typeof val === 'object') {
    return prepareObject(val, seen)
  }
  return val.toString()
}

function pad(number, digits) {
  number = '' + number
  while (number.length < digits) {
    number = '0' + number
  }
  return number
}

function dateToStringUTC(date) {
  var year = date.getUTCFullYear()
  var isBCYear = year < 1
  if (isBCYear) year = Math.abs(year) + 1 // negative years are 1 off their BC representation

  var ret =
    pad(year, 4) +
    '-' +
    pad(date.getUTCMonth() + 1, 2) +
    '-' +
    pad(date.getUTCDate(), 2) +
    'T' +
    pad(date.getUTCHours(), 2) +
    ':' +
    pad(date.getUTCMinutes(), 2) +
    ':' +
    pad(date.getUTCSeconds(), 2) +
    '.' +
    pad(date.getUTCMilliseconds(), 3)

  ret += '+00:00'
  if (isBCYear) ret += ' BC'
  return ret
}

function dateToString(date) {
  var offset = -date.getTimezoneOffset()

  var year = date.getFullYear()
  var isBCYear = year < 1
  if (isBCYear) year = Math.abs(year) + 1 // negative years are 1 off their BC representation

  var ret =
    pad(year, 4) +
    '-' +
    pad(date.getMonth() + 1, 2) +
    '-' +
    pad(date.getDate(), 2) +
    'T' +
    pad(date.getHours(), 2) +
    ':' +
    pad(date.getMinutes(), 2) +
    ':' +
    pad(date.getSeconds(), 2) +
    '.' +
    pad(date.getMilliseconds(), 3)

  if (offset < 0) {
    ret += '-'
    offset *= -1
  } else {
    ret += '+'
  }

  ret += pad(Math.floor(offset / 60), 2) + ':' + pad(offset % 60, 2)
  if (isBCYear) ret += ' BC'
  return ret
}

function escapeElement(elementRepresentation) {
  var escaped = elementRepresentation.replace(/\\/g, '\\\\').replace(/"/g, '\\"')
  return '"' + escaped + '"'
}

// convert a JS array to a postgres array literal
// uses comma separator so won't work for types like box that use
// a different array separator.
function arrayString(val) {
  var result = '{'
  for (var i = 0; i < val.length; i++) {
    if (i > 0) {
      result = result + ','
    }
    if (val[i] === null || typeof val[i] === 'undefined') {
      result = result + 'NULL'
    } else if (Array.isArray(val[i])) {
      result = result + arrayString(val[i])
    } else if (val[i] instanceof Buffer) {
      result += '\\\\x' + val[i].toString('hex')
    } else {
      result += escapeElement(prepareValue(val[i]))
    }
  }
  result = result + '}'
  return result
}

function prepareObject(val, seen) {
  if (val && typeof val.toPostgres === 'function') {
    seen = seen || []
    if (seen.indexOf(val) !== -1) {
      throw new Error('circular reference detected while preparing "' + val + '" for query')
    }
    seen.push(val)

    return prepareValue(val.toPostgres(prepareValue), seen)
  }
  return JSON.stringify(val)
}

// end pg util
