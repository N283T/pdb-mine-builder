
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

    // tableが空オブジェクトの場合はスキップ
    const tableValues = Object.values(table);
    if (!tableValues.length || tableValues[0] === undefined) continue;
    nor = tableValues[0].length;
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
        column[r] = col_nfo(column[r]);
      }
    } 
  }

  results = await results;
  results.forEach((table, idx) => memObj.sql[tableNames[idx]] = table);
  await pipeline.brief_summary(memObj, __primaryKey__, config);
  processKeywords(memObj);
  
  Object.keys(sql_typing).map(e => rdbHelper.deltaTable(e, memObj, sql_PK, sql_struct, __primaryKey__));
  
  try {
    await rdbHelper.updateRDB(memObj, scriptStartDate, sql_PK, sql_struct, mineSchema, __primaryKey__, dbconnect);
  }
  catch (e) {
    if (memObj.optionalFailRetry !== undefined && memObj.optionalFailRetry.length) {
      memObj.optionalFailRetry.map(x=>delete memObj.mmjson[x]);
      memObj.updates = []; memObj.inserts = []; memObj.deletes = [];
      Object.keys(sql_typing).map(e => rdbHelper.deltaTable(e, memObj, sql_PK, sql_struct, __primaryKey__));
      await rdbHelper.updateRDB(memObj, undefined, sql_PK, sql_struct, mineSchema, __primaryKey__, dbconnect);
    }
    else throw e;
  }
  
  //console.log("done", memObj.entryId);
  
  getJob(memObj.entryId);
}

function processKeywords(memObj) {
  var tbl = memObj.mmjson.brief_summary;
  
  var eF, aF, cat, pkref, t, tbl_nfo, nor, c, r, pk, col_nfo;
  
  tbl.keywords = tbl.keywords || [];
  
  // extract additional data from mmjson
  for (t in memObj.mmjson) {
    if (t == "brief_summary" || ! (t in sql_PK)) continue;
    cat = memObj.mmjson[t];
    tbl_nfo = sql_typing[t];
    pkref = sql_PKref[t];
    
    // catが空オブジェクトの場合はスキップ
    const catValues = Object.values(cat);
    if (!catValues.length || catValues[0] === undefined) continue;
    nor = catValues[0].length;

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
  tbl.keywords = tbl.keywords.map(x=>x.toLowerCase().replace(/\n/g, " "));
  tbl.keywords = tbl.keywords.filter(x=>(isNaN(x - parseFloat(x)) || x.length > 4)); // filter out numbers, unless it's a large number, which might correspond to some external id
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
  if (process.send) process.send({cmd: "getjob", jobId, entryId});
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
  if (process.on) process.on("message", respond2Main);
  if (process.send) process.send({cmd: "init", jobId});
}


// update brief_summary table stuff


// initialize schema data structure
