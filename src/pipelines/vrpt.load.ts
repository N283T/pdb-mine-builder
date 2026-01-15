/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load validation report data into the rdb
*/

import * as fs from "fs";

import * as rdbHelper from "../modules/rdb-helper.js";
import * as general from "../modules/general.js";
import * as rdbLoader from "../modules/rdb-loader.js";
import { setScandone } from "../modules/rdb-loader.js";
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

  // Get limit from argv (--limit N)
  const argv = config.argv as Record<string, unknown>;
  const limit = typeof argv.limit === "number" ? argv.limit : undefined;

  let filesToProcess = files;
  if (limit) {
    filesToProcess = files.slice(0, limit);
    console.log(`Processing ${filesToProcess.length} entries (limited)`);
  }

  for (const ciffile of filesToProcess) {
    const pdbid = ciffile.name.split("_")[0];
    jm.jobs.push({
      path: ciffile.path,
      entryId: pdbid,
      mode: "cif",
      mtime: ciffile.stats!.mtime.getTime() / 1000,
    });
  }
  setScandone(jm);
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
  try {
    const content = await general.gunzip(await fsp.readFile(payload.path));
    const data = JSON.parse(content.toString()) as VRPTMMJson;
    return data;
  } catch (e) {
    console.error(`Error loading JSON from ${payload.path}:`, e);
    return null;
  }
}
