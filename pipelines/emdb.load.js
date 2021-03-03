// load mmjson-noatom-plus files (for initial load)

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const xml2js = await import("xml2js");

const rdbLoader = await import(global.moduleFolder+"rdb-loader.js");
const rdbHelper = await import(global.moduleFolder+"rdb-helper.js");
const general = await import(global.moduleFolder+"general.js");

export async function pipeline_exec(config) {
  const rdb_def = await rdbHelper.import_rdb_def(config.pipelines["emdb"].deffile, config);
  var jm = await rdbLoader.init(config, rdb_def);

  const emdb_data = general.expandPath(config.pipelines.emdb.data);
  for (const file of await general.walkPattern(emdb_data)) {
    const entryId = file.path.split("/").slice(-1)[0].split("-v")[0].toUpperCase();
    jm.jobs.push({path: file.path, entryId});
  }

  jm.scandone = true;
  await jm.waiter.promise;
};

export function brief_summary(memObj, __primaryKey__) {
  var tbl, mmjson = memObj.mmjson;
  
  tbl = mmjson.brief_summary = {};
  
  tbl.docid = [parseInt(memObj.entryId.split("-")[1])];

  var deposition_date, header_release_date, map_release_date, modification_date;

  deposition_date = mmjson.admin[0].key_dates[0].deposition[0];
  header_release_date = mmjson.admin[0].key_dates[0].header_release[0];
  try {map_release_date = mmjson.admin[0].key_dates[0].map_release[0];}
  catch (e) {map_release_date = null;}
  modification_date = mmjson.admin[0].key_dates[0].update[0];

  tbl.deposition_date = [deposition_date];
  tbl.header_release_date = [header_release_date];
  tbl.map_release_date = [map_release_date];
  tbl.modification_date = [modification_date];
  
  const shallowCopy = {};
  for (const [k,v] of Object.entries(mmjson)) {
    if (k != "brief_summary") shallowCopy[k] = v;
  }
  
  tbl.content = [shallowCopy];
  
  tbl.update_date = [null];
}

export async function load_data(payload, config) {
  const parser = new xml2js.Parser();
  return await parser.parseStringPromise(await fsp.readFile(payload.path, "utf8"));
}
