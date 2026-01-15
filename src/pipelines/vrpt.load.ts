/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load validation report data into the rdb
*/

import * as fs from "fs";

import * as rdbHelper from "../modules/rdb-helper.js";
import * as general from "../modules/general.js";
import * as rdbLoader from "../modules/rdb-loader.js";
import * as cif from "../modules/cif.js";
import type { Config, PipelineMemObj } from "../types/index.js";
import type { JobPayload } from "../modules/rdb-loader.js";

const fsp = fs.promises;

/* eslint-disable @typescript-eslint/no-explicit-any */
type AnyCategory = Record<string, any[]>;
type VRPTMMJson = Record<string, AnyCategory>;

interface VRPTPayload extends JobPayload {
  path: string;
  mode: string;
  mtime: number;
}

// Load CIF dictionary at module initialization
async function loadDictionary(): Promise<void> {
  const vrptConfig = global.config?.pipelines?.["vrpt"];
  if (!vrptConfig?.dic) return;

  const dicPath = general.expandPath(vrptConfig.dic as string);
  if (dicPath.endsWith(".gz")) {
    await cif.loadCIFdic(
      cif.parseCIFdictionary(
        cif.parse((await general.gunzip(await fsp.readFile(dicPath))).toString())
      )
    );
  } else {
    await cif.loadCIFdic(
      cif.parseCIFdictionary(
        cif.parse((await fsp.readFile(dicPath)).toString())
      )
    );
  }
}

// Initialize dictionary loading
loadDictionary().catch(console.error);

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = await rdbHelper.import_rdb_def(
    config.pipelines["vrpt"].deffile as string,
    config
  );
  const jm = await rdbLoader.init(config, rdb_def);

  const files = await general.walkPattern(
    general.expandPath(config.pipelines["vrpt"].data as string),
    { stats: true }
  );

  for (const ciffile of files) {
    const pdbid = ciffile.name.split("_")[0];
    jm.jobs.push({
      path: ciffile.path,
      entryId: pdbid,
      mode: "cif",
      mtime: ciffile.stats!.mtime.getTime() / 1000,
    });
  }
  jm.scandone = true;
  await jm.waiter.promise;
}

export function brief_summary(
  memObj: PipelineMemObj,
  __primaryKey__: string
): void {
  const mmjson = memObj.mmjson as unknown as VRPTMMJson;

  const tbl: AnyCategory = (mmjson.brief_summary = {});

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId)];

  tbl.update_date = [null];
}

export async function load_data(
  payload: VRPTPayload,
  _config: Config
): Promise<VRPTMMJson | null> {
  const parser = new cif.CIFparser();
  try {
    await general.readlineGZ(payload.path, function (line: string) {
      parser.parseLine(line, 0);
      if (parser.error) {
        console.error(`Error found in line ${parser.error[1]}:`);
        console.error("  ", parser.error[2]);
        console.log("  ", parser.error[0]);
        parser.error = null;
      }
    });
  } catch {
    console.log(payload.path);
    return null;
  }

  cif.cleanJSON_withDict(parser.data);

  return parser.data as unknown as VRPTMMJson;
}
