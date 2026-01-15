/*
  Copyright (C) 2021 Gert-Jan Bekker
  mine2updater - Update command (run RDB update pipelines)
*/

import * as process from "process";
import * as path from "path";
import * as url from "url";
import * as fs from "fs";
import yaml from "js-yaml";

import * as general from "../modules/general.js";
import type { Config } from "../types/index.js";

const fsp = fs.promises;

export type PipelineName = "pdbj" | "cc" | "ccmodel" | "prd" | "vrpt" | "contacts";

const ALL_PIPELINES: PipelineName[] = ["pdbj", "cc", "ccmodel", "prd", "vrpt", "contacts"];

async function runPipeline(pipelineName: PipelineName, config: Config): Promise<void> {
  const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
  const pipelinePath = path.join(__dirname, `../pipelines/${pipelineName}.load.js`);

  // Set pipeline path for worker processes
  const extConfig = config as unknown as Record<string, unknown>;
  extConfig.pipeline = pipelinePath;
  extConfig.moduleFolder = path.join(__dirname, "../modules/");
  extConfig.pipelineFolder = path.join(__dirname, "../pipelines/");

  const pipelineModule = await import(`../pipelines/${pipelineName}.load.js`);
  await pipelineModule.pipeline_exec(config);
}

export async function updateCommand(pipelines: PipelineName[]): Promise<void> {
  console.log("==> Starting RDB update...");

  // Load config
  const config = yaml.load(await fsp.readFile("config.yml", "utf8")) as Config;
  global.config = config;
  config.argv = {};
  config.defines = config.defines || {};

  const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
  config.defines.CWD = path.join(__dirname, "../../");

  general.solveDefines(config.defines);

  global.moduleFolder = path.join(__dirname, "../modules/");
  global.pipelineFolder = path.join(__dirname, "../pipelines/");

  // Determine which pipelines to run
  const pipelinesToRun: PipelineName[] =
    pipelines.length > 0 ? pipelines : ALL_PIPELINES;

  // Run each pipeline
  for (const pipelineName of pipelinesToRun) {
    console.log(`==> Running ${pipelineName}.load pipeline...`);
    await runPipeline(pipelineName, config);
  }

  console.log("==> RDB update completed.");
}
