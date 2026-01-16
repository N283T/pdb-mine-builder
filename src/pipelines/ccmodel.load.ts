/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load chemical component model data into the rdb
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
type CCModelMMJson = Record<string, AnyCategory>;

interface CCModelPayload extends JobPayload {
  path: string;
}

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = yaml.load(
    await fsp.readFile(
      general.expandPath(config.pipelines.ccmodel.deffile as string),
      "utf8"
    )
  ) as rdbLoader.RdbDef;
  const jm = await rdbLoader.init(config, rdb_def);

  let dir = general.expandPath(config.pipelines.ccmodel.data as string);
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
  const mmjson = memObj.mmjson as unknown as CCModelMMJson;

  const tbl: AnyCategory = (mmjson.brief_summary = {});

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId.split("_")[1])];

  if (mmjson.pdbx_chem_comp_model_audit && mmjson.pdbx_chem_comp_model_audit.date) {
    tbl.pdbx_initial_date = [
      rdbHelper.mmjsonAt_IC(
        mmjson.pdbx_chem_comp_model_audit,
        "date",
        "action_type",
        "initial release"
      )[0] || null,
    ];
    tbl.pdbx_modified_date = [
      mmjson.pdbx_chem_comp_model_audit.date[
        mmjson.pdbx_chem_comp_model_audit.date.length - 1
      ],
    ];
    if (!tbl.pdbx_initial_date[0])
      tbl.pdbx_initial_date = [mmjson.pdbx_chem_comp_model_audit.date[0]];
  }

  if (mmjson.pdbx_chem_comp_model_reference)
    tbl.csd_id = [
      rdbHelper.mmjsonAt_IC(
        mmjson.pdbx_chem_comp_model_reference,
        "db_code",
        "db_name",
        "CSD"
      )[0] || null,
    ];

  if (mmjson.pdbx_chem_comp_model)
    tbl.comp_id = [mmjson.pdbx_chem_comp_model.comp_id[0]];

  tbl.update_date = [null];
}

export async function load_data(
  payload: CCModelPayload,
  _config: Config
): Promise<CCModelMMJson> {
  return JSON.parse(
    (await general.gunzip(await fsp.readFile(payload.path))).toString()
  );
}
