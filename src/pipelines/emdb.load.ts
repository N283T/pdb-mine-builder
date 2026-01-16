/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load EMDB data into the rdb
*/

import * as fs from "fs";
import * as xml2js from "xml2js";

import * as rdbLoader from "../modules/rdb-loader.js";
import { setScandone } from "../modules/rdb-loader.js";
import * as rdbHelper from "../modules/rdb-helper.js";
import * as general from "../modules/general.js";
import type { Config, PipelineMemObj } from "../types/index.js";
import type { JobPayload } from "../modules/rdb-loader.js";

const fsp = fs.promises;

/* eslint-disable @typescript-eslint/no-explicit-any */
type AnyCategory = Record<string, any[]>;
type EMDBMMJson = Record<string, AnyCategory>;

interface EMDBPayload extends JobPayload {
  path: string;
}

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = await rdbHelper.import_rdb_def(
    config.pipelines["emdb"].deffile as string,
    config
  );
  const jm = await rdbLoader.init(config, rdb_def);

  const emdb_data = general.expandPath(config.pipelines.emdb.data as string);
  for (const file of await general.walkPattern(emdb_data)) {
    const entryId = file.path.split("/").slice(-1)[0].split("-v")[0].toUpperCase();
    jm.jobs.push({ path: file.path, entryId });
  }

  setScandone(jm);
  await jm.waiter.promise;
}

export function brief_summary(
  memObj: PipelineMemObj,
  __primaryKey__: string
): void {
  const mmjson = memObj.mmjson as unknown as EMDBMMJson;

  const tbl: AnyCategory = (mmjson.brief_summary = {});

  tbl.docid = [parseInt(memObj.entryId.split("-")[1])];

  let deposition_date: string | null;
  let header_release_date: string | null;
  let map_release_date: string | null;
  let modification_date: string | null;

  // EMDB XML structure has nested arrays
  const admin = mmjson.admin as any;
  deposition_date = admin?.[0]?.key_dates?.[0]?.deposition?.[0] || null;
  header_release_date = admin?.[0]?.key_dates?.[0]?.header_release?.[0] || null;
  try {
    map_release_date = admin[0].key_dates[0].map_release[0];
  } catch {
    map_release_date = null;
  }
  modification_date = admin?.[0]?.key_dates?.[0]?.update?.[0] || null;

  tbl.deposition_date = [deposition_date];
  tbl.header_release_date = [header_release_date];
  tbl.map_release_date = [map_release_date];
  tbl.modification_date = [modification_date];

  const shallowCopy: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(mmjson)) {
    if (k !== "brief_summary") shallowCopy[k] = v;
  }

  tbl.content = [shallowCopy];

  tbl.update_date = [null];

  tbl.keywords = [];
}

export async function load_data(
  payload: EMDBPayload,
  _config: Config
): Promise<EMDBMMJson> {
  const parser = new xml2js.Parser();
  return (await parser.parseStringPromise(
    await fsp.readFile(payload.path, "utf8")
  )) as EMDBMMJson;
}
