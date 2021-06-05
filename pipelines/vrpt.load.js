const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");
const cif = await import("../modules/cif.js");

await cif.loadCIFdic(cif.parseCIFdictionary(cif.parse((await fsp.readFile(general.expandPath(global.config.pipelines["vrpt"].dic))).toString())));

export async function pipeline_exec(config) {
  const rdb_def = await rdbHelper.import_rdb_def(config.pipelines["vrpt"].deffile, config);
  var jm = await rdbLoader.init(config, rdb_def);

  const files = await general.walkPattern(general.expandPath(config.pipelines["vrpt"].data), {stats: true});

  for (const ciffile of files) {
    const pdbid = ciffile.name.split("_")[0];
    jm.jobs.push({path: ciffile.path, entryId: pdbid, mode: "cif", mtime: ciffile.stats.mtime.getTime()/1000});
  }
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
  const parser = new cif.CIFparser();
  try {
    await general.readlineGZ(payload.path, function(line) {
      parser.parseLine(line);
      if (parser.error) {
        console.error(`Error found in line ${parser.error[1]}:`);
        console.error("  ", parser.error[2]);
        console.log("  ", parser.error[0]);
        parser.error = null;
      }
    });
  }
  catch (e) {
    console.log(payload.path);
    return null;
  }

  cif.cleanJSON_withDict(parser.data);

  return parser.data;
}
