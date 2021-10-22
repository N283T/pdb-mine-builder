// script to load mmjson-plus-noatom data into the rdb...

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");

export async function pipeline_exec(config) {
  const rdb_def = yaml.load(await fsp.readFile(general.expandPath(config.pipelines.ccmodel.deffile), 'utf8'));
  var jm = await rdbLoader.init(config, rdb_def);
  
  var dir = general.expandPath(config.pipelines.ccmodel.data);
  if (! dir.endsWith("/")) dir += "/";
  
  (await fsp.readdir(dir)).forEach(x => jm.jobs.push({path: dir+x, entryId: x.split(".")[0]}));

  jm.scandone = true;
  await jm.waiter.promise;
};


export function brief_summary(memObj, __primaryKey__) {
  var t, tbl, pk, c, col_nfo, tbl_nfo, nor, mmjson = memObj.mmjson, tmp, sequences;
  
  tbl = mmjson.brief_summary = {};

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId.split("_")[1])];
  
  if (mmjson.pdbx_chem_comp_model_audit && mmjson.pdbx_chem_comp_model_audit.date) {
    tbl.pdbx_initial_date = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_chem_comp_model_audit, "date", "action_type", "initial release")[0]];
    tbl.pdbx_modified_date = [mmjson.pdbx_chem_comp_model_audit.date[mmjson.pdbx_chem_comp_model_audit.date.length-1]];
    if (! tbl.pdbx_initial_date[0]) tbl.pdbx_initial_date = [mmjson.pdbx_chem_comp_model_audit.date[0]];
  }
  
  if (mmjson.pdbx_chem_comp_model_reference) tbl.csd_id = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_chem_comp_model_reference, "db_code", "db_name", "CSD")[0]];
  
  if (mmjson.pdbx_chem_comp_model) tbl.comp_id = [mmjson.pdbx_chem_comp_model.comp_id[0]];
  
  tbl.update_date = [null];
}


export async function load_data(payload) {
  return JSON.parse((await general.gunzip(await fsp.readFile(payload.path))).toString());
}

