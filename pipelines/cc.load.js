// script to load mmjson-plus-noatom data into the rdb...

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");

export async function pipeline_exec(config) {
  const rdb_def = yaml.load(await fsp.readFile(general.expandPath(config.pipelines.cc.deffile), 'utf8'));
  var jm = await rdbLoader.init(config, rdb_def);
  
  var dir = general.expandPath(config.pipelines.cc.data);
  if (! dir.endsWith("/")) dir += "/";
  
  (await fsp.readdir(dir)).forEach(x => jm.jobs.push({path: dir+x, entryId: x.split(".")[0]}));

  jm.scandone = true;
  await jm.waiter.promise;
};


export async function brief_summary(memObj, __primaryKey__, config) {
  var t, tbl, pk, c, col_nfo, tbl_nfo, nor, mmjson = memObj.mmjson, tmp, sequences;
  
  tbl = mmjson.brief_summary = {};

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId)];
  
  tbl.pdbx_initial_date = [mmjson.chem_comp.pdbx_initial_date[0]];
  tbl.pdbx_modified_date = [mmjson.chem_comp.pdbx_modified_date[0]];
  
  if (mmjson.pdbx_chem_comp_audit && mmjson.pdbx_chem_comp_audit.date) tbl.release_date = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_chem_comp_audit, "date", "action_type", "initial release")[0]];
  else tbl.release_date = [null];
  if (tbl.release_date[0] === undefined) tbl.release_date[0] = null;

  tbl.update_date = [null];
  tbl.name = [mmjson.chem_comp.name[0]];
  tbl.formula = [mmjson.chem_comp.formula[0]];
  
  tbl.pdbx_synonyms = [mmjson.chem_comp.pdbx_synonyms[0]];
  if (tbl.pdbx_synonyms[0] != null) tbl.pdbx_synonyms[0] = tbl.pdbx_synonyms[0].split(";");
  else tbl.pdbx_synonyms = [[]];
  
  
  if (mmjson.pdbx_chem_comp_identifier) tbl.identifier = [mmjson.pdbx_chem_comp_identifier.identifier ? mmjson.pdbx_chem_comp_identifier.identifier[0] : ""];
  else tbl.identifier = [null];

  tbl.smiles = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_chem_comp_descriptor, "descriptor", "type", "smiles")];
  tbl.inchi = [rdbHelper.mmjsonAt_IC(mmjson.pdbx_chem_comp_descriptor, "descriptor", "type", "inchi")];
  
  // add support for fingerprints...
  if (config.obabel) {
    await general.cc2mdl(memObj);
    var fp2 = await general.mdl2fp(memObj.mdl, config.obabel);
    tbl.byte0 = [BigInt(fp2[0])];
    tbl.byte1 = [BigInt(fp2[1])];
    tbl.byte2 = [BigInt(fp2[2])];
    tbl.byte3 = [BigInt(fp2[3])];
    tbl.byte4 = [BigInt(fp2[4])];
    tbl.byte5 = [BigInt(fp2[5])];
    tbl.byte6 = [BigInt(fp2[6])];
    tbl.byte7 = [BigInt(fp2[7])];
    tbl.byte8 = [BigInt(fp2[8])];
    tbl.byte9 = [BigInt(fp2[9])];
    tbl.byte10 = [BigInt(fp2[10])];
    tbl.byte11 = [BigInt(fp2[11])];
    tbl.byte12 = [BigInt(fp2[12])];
    tbl.byte13 = [BigInt(fp2[13])];
    tbl.byte14 = [BigInt(fp2[14])];
    tbl.byte15 = [BigInt(fp2[15])];
  }
}

export async function load_data(payload) {
  return JSON.parse((await general.gunzip(await fsp.readFile(payload.path))).toString());
}

