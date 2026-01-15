/*
  Copyright (C) 2021 Gert-Jan Bekker
  mine2updater - Main entry point
*/

import * as process from "process";
import minimist from "minimist";
import yaml from "js-yaml";
import * as fs from "fs";
import * as path from "path";
import * as url from "url";

import * as general from "./modules/general.js";
import type { Config } from "./types/index.js";

const fsp = fs.promises;

interface ParsedArgs {
  _: string[];
  [key: string]: unknown;
}

async function main(): Promise<void> {
  const argv: ParsedArgs = minimist(process.argv.slice(2));

  const config = yaml.load(await fsp.readFile("config.yml", "utf8")) as Config;
  global.config = config;
  config.argv = argv;
  config.defines = config.defines || {};

  const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
  config.defines.CWD = __dirname + "/../";

  general.solveDefines(config.defines);

  global.moduleFolder = process.cwd() + "/modules/";
  global.pipelineFolder = process.cwd() + "/pipelines/";

  const pipeline = argv._[0];
  if (pipeline) {
    config.pipelines = config.pipelines || {};
    // Set pipeline path for worker processes
    const extConfig = config as unknown as Record<string, unknown>;
    extConfig.pipeline = path.join(__dirname, `pipelines/${pipeline}.js`);
    extConfig.moduleFolder = __dirname + "/modules/";
    extConfig.pipelineFolder = __dirname + "/pipelines/";
    
    const pipelineModule = await import(`./pipelines/${pipeline}.js`);
    await pipelineModule.pipeline_exec(config);
  }
}

main().catch(console.error);
