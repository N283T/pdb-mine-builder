// script to load mmjson-plus-noatom data into the rdb...

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");

export async function pipeline_exec(config) {
  const rdb_def = yaml.safeLoad(await fsp.readFile(general.expandPath(config.pipelines.prd.deffile), 'utf8'));
  var jm = await rdbLoader.init(config, rdb_def, true);
  
  var dir = general.expandPath(config.pipelines.prd.data);
  if (! dir.endsWith("/")) dir += "/";
  
  (await fsp.readdir(dir)).forEach(x => jm.jobs.push({path: dir+x, entryId: x.split(".")[0]}));

  jm.scandone = true;
  await jm.waiter.promise;
};


export function brief_summary(memObj, __primaryKey__) {
  var t, tbl, pk, c, col_nfo, tbl_nfo, nor, mmjson = memObj.mmjson, tmp, sequences;
  
  tbl = mmjson.brief_summary = {};

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [parseInt(memObj.entryId.substr(4))];
  
  if (mmjson.pdbx_prd_audit && mmjson.pdbx_prd_audit.date) {
    tbl.pdbx_initial_date = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_prd_audit, "date", "action_type", "initial release")[0]];
    tbl.pdbx_modified_date = [mmjson.pdbx_prd_audit.date[mmjson.pdbx_prd_audit.date.length-1]];
    if (! tbl.pdbx_initial_date[0]) tbl.pdbx_initial_date = [mmjson.pdbx_prd_audit.date[0]];
  }
  
  try {tbl.name = [mmjson.chem_comp.name[0]];} catch (e) {tbl.name = [""];}
  try {tbl.formula = [mmjson.chem_comp.formula[0]];} catch (e) {tbl.formula = [""];}
  try {tbl.description = [mmjson.pdbx_reference_molecule.description[0]];} catch (e) {tbl.description = [""];}
  
  tbl.update_date = [null];
}


export async function load_data(payload) {
  const mmjson = JSON.parse((await general.gunzip(await fsp.readFile(payload.path))).toString());
  const id = Object.keys(mmjson)[0].split("_").slice(-1)[0];

  if ("data_PRDCC_"+id in mmjson) {
    for (const [k,v] of Object.entries(Object.values(mmjson["data_PRDCC_"+id])[0])) mmjson["data_PRD_"+id][k] = v;
    delete mmjson["data_PRDCC_"+id];
  }
  return mmjson;
}

