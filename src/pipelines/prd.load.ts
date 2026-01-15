/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load PRD data into the rdb
*/

import yaml from "js-yaml";
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
type PRDMMJson = Record<string, AnyCategory>;

interface PRDPayload extends JobPayload {
  path: string;
}

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = yaml.load(
    await fsp.readFile(general.expandPath(config.pipelines.prd.deffile as string), "utf8")
  ) as rdbLoader.RdbDef;
  const jm = await rdbLoader.init(config, rdb_def);

  let dir = general.expandPath(config.pipelines.prd.data as string);
  if (!dir.endsWith("/")) dir += "/";

  // Get limit from argv (--limit N)
  const argv = config.argv as Record<string, unknown>;
  const limit = typeof argv.limit === "number" ? argv.limit : undefined;

  let files = await fsp.readdir(dir);
  if (limit) {
    files = files.slice(0, limit);
    console.log(`Processing ${files.length} entries (limited)`);
  }

  files.forEach((x) =>
    jm.jobs.push({ path: dir + x, entryId: x.split(".")[0] })
  );

  setScandone(jm);
  await jm.waiter.promise;
}

export function brief_summary(
  memObj: PipelineMemObj,
  __primaryKey__: string
): void {
  const mmjson = memObj.mmjson as unknown as PRDMMJson;

  const tbl: AnyCategory = (mmjson.brief_summary = {});

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [parseInt(memObj.entryId.substring(4))];

  if (mmjson.pdbx_prd_audit && mmjson.pdbx_prd_audit.date) {
    tbl.pdbx_initial_date = [
      rdbHelper.mmjsonAt_IC(
        mmjson.pdbx_prd_audit,
        "date",
        "action_type",
        "initial release"
      )[0] || null,
    ];
    tbl.pdbx_modified_date = [
      mmjson.pdbx_prd_audit.date[mmjson.pdbx_prd_audit.date.length - 1],
    ];
    if (!tbl.pdbx_initial_date[0])
      tbl.pdbx_initial_date = [mmjson.pdbx_prd_audit.date[0]];
  }

  try {
    tbl.name = [mmjson.chem_comp.name[0]];
  } catch {
    tbl.name = [""];
  }
  try {
    tbl.formula = [mmjson.chem_comp.formula[0]];
  } catch {
    tbl.formula = [""];
  }
  try {
    tbl.description = [mmjson.pdbx_reference_molecule.description[0]];
  } catch {
    tbl.description = [""];
  }

  tbl.update_date = [null];
}

export async function load_data(
  payload: PRDPayload,
  _config: Config
): Promise<PRDMMJson> {
  const mmjson = JSON.parse(
    (await general.gunzip(await fsp.readFile(payload.path))).toString()
  ) as PRDMMJson;
  const keys = Object.keys(mmjson);
  if (!keys.length) return mmjson;
  const id = keys[0].split("_").slice(-1)[0];

  if ("data_PRDCC_" + id in mmjson) {
    const prdccData = mmjson["data_PRDCC_" + id] as AnyCategory;
    const prdccValues = Object.values(prdccData);
    if (prdccValues.length && prdccValues[0] !== undefined) {
      const firstValue = prdccValues[0] as unknown as Record<string, unknown>;
      for (const [k, v] of Object.entries(firstValue))
        mmjson["data_PRD_" + id][k] = v as any[];
    }
    delete mmjson["data_PRDCC_" + id];
  }
  return mmjson;
}
