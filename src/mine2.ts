/*
  Copyright (C) 2021 Gert-Jan Bekker
  mine2updater - Main entry point (CLI)
*/

import { Command } from "commander";
import { syncCommand, convertVrptToJson, type SyncTarget } from "./commands/sync.js";
import { updateCommand, type PipelineName } from "./commands/update.js";
import { testCommand, type TestOptions } from "./commands/test.js";

const program = new Command();

program
  .name("mine2")
  .description("MINE2 updater - Sync data and update RDB")
  .version("0.1.0");

// Sync command
program
  .command("sync")
  .description("Sync data from PDBj using rsync")
  .argument("[targets...]", "Targets to sync: pdbj, cc, ccmodel, prd, vrpt, contacts, schemas, dictionaries")
  .action(async (targets: string[]) => {
    const validTargets: SyncTarget[] = [
      "pdbj",
      "cc",
      "ccmodel",
      "prd",
      "vrpt",
      "contacts",
      "schemas",
      "dictionaries",
    ];

    const invalidTargets = targets.filter((t) => !validTargets.includes(t as SyncTarget));
    if (invalidTargets.length > 0) {
      console.error(`Error: Invalid targets: ${invalidTargets.join(", ")}`);
      console.error(`Valid targets: ${validTargets.join(", ")}`);
      process.exit(1);
    }

    try {
      await syncCommand(targets.length > 0 ? (targets as SyncTarget[]) : []);
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  });

// Update command
program
  .command("update")
  .description("Run RDB update pipelines")
  .argument("[pipelines...]", "Pipelines to run: pdbj, cc, ccmodel, prd, vrpt, contacts")
  .action(async (pipelines: string[]) => {
    const validPipelines: PipelineName[] = ["pdbj", "cc", "ccmodel", "prd", "vrpt", "contacts"];

    const invalidPipelines = pipelines.filter((p) => !validPipelines.includes(p as PipelineName));
    if (invalidPipelines.length > 0) {
      console.error(`Error: Invalid pipelines: ${invalidPipelines.join(", ")}`);
      console.error(`Valid pipelines: ${validPipelines.join(", ")}`);
      process.exit(1);
    }

    try {
      await updateCommand(pipelines.length > 0 ? (pipelines as PipelineName[]) : []);
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  });

// All command (sync + update)
program
  .command("all")
  .description("Run both sync and update (full update)")
  .action(async () => {
    try {
      await syncCommand([]);
      await updateCommand([]);
      console.log("==> Done.");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  });

// Test command
program
  .command("test")
  .description("Create test DB and run pipelines to verify TypeScript code")
  .option("-c, --config <file>", "Test config file", "config.test.yml")
  .option("-d, --drop", "Drop existing test DB before creating")
  .option("-p, --pipelines <pipelines>", "Comma-separated list of pipelines to run")
  .option("-n, --limit <number>", "Limit number of files to process per pipeline")
  .action(async (options: Record<string, unknown>) => {
    try {
      // Check process.argv directly as fallback for boolean flags
      const argv = process.argv;
      const hasDropFlag = argv.includes("--drop") || argv.includes("-d");
      const dropFlag = options.drop === true || hasDropFlag;
      
      // Parse limit option (default to 10 if not specified)
      let limitValue: number | undefined;
      if (options.limit !== undefined) {
        limitValue = parseInt(String(options.limit), 10);
        if (isNaN(limitValue) || limitValue < 1) {
          throw new Error("--limit must be a positive number");
        }
      }
      
      const testOptions: TestOptions = {
        configFile: options.config as string | undefined,
        drop: dropFlag,
        pipelines: options.pipelines as string | undefined,
        limit: limitValue,
      };
      await testCommand(testOptions);
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  });

// Convert vrpt command (CIF to JSON)
program
  .command("convert-vrpt")
  .description("Convert vrpt CIF files to JSON (without syncing)")
  .action(async () => {
    try {
      await convertVrptToJson(process.cwd());
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  });

// Parse arguments to check for legacy usage
const args = process.argv.slice(2);
const subcommands = ["sync", "update", "all", "test", "convert-vrpt", "help", "--help", "-h"];

// Legacy support: if first arg is not a subcommand, treat it as a pipeline name
if (args.length > 0 && !subcommands.includes(args[0])) {
  const pipeline = args[0];
  // Remove .load suffix if present
  const pipelineName = pipeline.replace(/\.load$/, "") as PipelineName;
  const validPipelines: PipelineName[] = ["pdbj", "cc", "ccmodel", "prd", "vrpt", "contacts"];

  if (validPipelines.includes(pipelineName)) {
    try {
      await updateCommand([pipelineName]);
      process.exit(0);
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : String(error));
      process.exit(1);
    }
  } else {
    console.error(`Error: Invalid pipeline: ${pipelineName}`);
    console.error(`Valid pipelines: ${validPipelines.join(", ")}`);
    console.error("\nUse 'mine2 --help' for usage information.");
    process.exit(1);
  }
} else {
  program.parse();
}
