/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load validation report data into the rdb
*/

import * as fs from "fs";

import * as rdbHelper from "../modules/rdb-helper.js";
import * as general from "../modules/general.js";
import * as rdbLoader from "../modules/rdb-loader.js";
import { setScandone } from "../modules/rdb-loader.js";
import * as cif from "../modules/cif.js";
import type { Config, PipelineMemObj, WalkFile } from "../types/index.js";
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

  // Get mode from argv (--mode json|cif|both, default: json)
  const argv = config.argv as Record<string, unknown>;
  const mode = typeof argv.mode === "string" ? argv.mode : "json";
  const limit = typeof argv.limit === "number" ? argv.limit : undefined;

  const vrptConfig = config.pipelines["vrpt"];
  const jsonPath = general.expandPath(vrptConfig.data as string);
  const cifPath = vrptConfig["data-cif"]
    ? general.expandPath(vrptConfig["data-cif"] as string)
    : null;

  // Scan files based on mode
  let jsonFiles: WalkFile[] = [];
  let cifFiles: WalkFile[] = [];

  if (mode === "json" || mode === "both") {
    try {
      jsonFiles = await general.walkPattern(jsonPath, { stats: true });
    } catch (e) {
      if (mode === "json") {
        console.error(`Error scanning JSON files: ${e}`);
        return;
      }
      jsonFiles = [];
    }
  }

  if (mode === "cif" || mode === "both") {
    try {
      cifFiles = cifPath
        ? await general.walkPattern(cifPath, { stats: true })
        : [];
    } catch (e) {
      if (mode === "cif") {
        console.error(`Error scanning CIF files: ${e}`);
        return;
      }
      cifFiles = [];
    }
  }

  // Build maps for quick lookup (only files with stats)
  const jsonMap = new Map<string, { path: string; stats: fs.Stats }>();
  for (const file of jsonFiles) {
    if (file.stats) {
      const pdbid = file.name.split("_")[0];
      if (!jsonMap.has(pdbid)) {
        jsonMap.set(pdbid, { path: file.path, stats: file.stats });
      }
    }
  }

  const cifMap = new Map<string, { path: string; stats: fs.Stats }>();
  for (const file of cifFiles) {
    if (file.stats) {
      const pdbid = file.name.split("_")[0];
      if (!cifMap.has(pdbid)) {
        cifMap.set(pdbid, { path: file.path, stats: file.stats });
      }
    }
  }

  // Collect all entry IDs
  const allEntryIds = new Set<string>();
  if (mode === "cif") {
    cifMap.forEach((_, pdbid) => allEntryIds.add(pdbid));
  } else if (mode === "both") {
    jsonMap.forEach((_, pdbid) => allEntryIds.add(pdbid));
    cifMap.forEach((_, pdbid) => allEntryIds.add(pdbid));
  } else {
    jsonMap.forEach((_, pdbid) => allEntryIds.add(pdbid));
  }

  let filesToProcess = Array.from(allEntryIds);
  if (limit) {
    filesToProcess = filesToProcess.slice(0, limit);
    console.log(`Processing ${filesToProcess.length} entries (limited, mode: ${mode})`);
  } else {
    console.log(`Processing ${filesToProcess.length} entries (mode: ${mode})`);
  }

  // Add jobs with appropriate mode
  for (const pdbid of filesToProcess) {
    const jsonFile = jsonMap.get(pdbid);
    const cifFile = cifMap.get(pdbid);

    if (mode === "json") {
      if (jsonFile) {
        jm.jobs.push({
          path: jsonFile.path,
          entryId: pdbid,
          mode: "json",
          mtime: jsonFile.stats.mtime.getTime() / 1000,
        });
      }
    } else if (mode === "cif") {
      if (cifFile) {
        jm.jobs.push({
          path: cifFile.path,
          entryId: pdbid,
          mode: "cif",
          mtime: cifFile.stats.mtime.getTime() / 1000,
        });
      }
    } else if (mode === "both") {
      // both mode: prefer JSON, fallback to CIF
      if (jsonFile) {
        jm.jobs.push({
          path: jsonFile.path,
          entryId: pdbid,
          mode: "json",
          mtime: jsonFile.stats.mtime.getTime() / 1000,
        });
      } else if (cifFile) {
        jm.jobs.push({
          path: cifFile.path,
          entryId: pdbid,
          mode: "cif",
          mtime: cifFile.stats.mtime.getTime() / 1000,
        });
      }
    }
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
  if (payload.mode === "json") {
    try {
      const content = await general.gunzip(await fsp.readFile(payload.path));
      const data = JSON.parse(content.toString()) as VRPTMMJson;
      return data;
    } catch (e) {
      console.error(`Error loading JSON from ${payload.path}:`, e);
      return null;
    }
  } else if (payload.mode === "cif") {
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
    } catch (e) {
      console.log(`Error reading CIF from ${payload.path}:`, e);
      return null;
    }

    cif.cleanJSON_withDict(parser.data);

    return parser.data as unknown as VRPTMMJson;
  } else {
    console.error(`Unknown mode: ${payload.mode}`);
    return null;
  }
}
