/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load contacts data into the rdb
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
type ContactsMMJson = Record<string, AnyCategory>;

interface ContactsPayload extends JobPayload {
  path: string;
  mtime: number;
}

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = yaml.load(
    await fsp.readFile(
      general.expandPath(config.pipelines.contacts.deffile as string),
      "utf8"
    )
  ) as rdbLoader.RdbDef;
  const jm = await rdbLoader.init(config, rdb_def);

  let dir = general.expandPath(config.pipelines.contacts.data as string);
  if (!dir.endsWith("/")) dir += "/";

  // Get limit from argv (--limit N)
  const argv = config.argv as Record<string, unknown>;
  const limit = typeof argv.limit === "number" ? argv.limit : undefined;

  let files = await fsp.readdir(dir);
  if (limit) {
    files = files.slice(0, limit);
    console.log(`Processing ${files.length} entries (limited)`);
  }

  for (const x of files) {
    const stat = await fsp.stat(dir + x);
    jm.jobs.push({
      path: dir + x,
      entryId: x.split(".")[0],
      mtime: stat.mtimeMs / 1000,
    });
  }

  setScandone(jm);
  await jm.waiter.promise;
}

export function brief_summary(
  memObj: PipelineMemObj & { mtimeMs?: number },
  __primaryKey__: string
): void {
  const mmjson = memObj.mmjson as unknown as ContactsMMJson;

  const tbl: AnyCategory = (mmjson.brief_summary = {});

  tbl[__primaryKey__] = [memObj.entryId];
  tbl.modification_date = [memObj.mtimeMs || null];
  tbl.update_date = [null];
}

export async function load_data(
  payload: ContactsPayload,
  _config: Config
): Promise<ContactsMMJson> {
  const list = JSON.parse(
    (await general.gunzip(await fsp.readFile(payload.path))).toString()
  );
  const output: ContactsMMJson = {};
  output[`data_${payload.entryId.toUpperCase()}`] = { list };
  return output;
}
