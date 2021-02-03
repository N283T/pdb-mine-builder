// script to load mmjson-plus-noatom data into the rdb...

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");

export async function pipeline_exec(config) {
  const rdb_def = yaml.safeLoad(await fsp.readFile(general.expandPath(config.pipelines.vrpt.deffile), 'utf8'));
  var jm = await rdbLoader.init(config, rdb_def, true);
  
  var dir = general.expandPath(config.pipelines.vrpt.data);
  if (! dir.endsWith("/")) dir += "/";
  
  (await fsp.readdir(dir)).forEach(x => jm.jobs.push({path: dir+x, entryId: x.split("-")[0]}));

  jm.scandone = true;
  await jm.waiter.promise;
};

export function brief_summary(memObj, __primaryKey__) {
  var t, tbl, pk, c, col_nfo, tbl_nfo, nor, mmjson = memObj.mmjson, tmp, sequences;
  
  tbl = mmjson.brief_summary = {};

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId)];
  
  tbl.update_date = [null];
}

export async function load_data(payload, config) {
  return JSON.parse((await general.gunzip(await fsp.readFile(payload.path))).toString());
}

