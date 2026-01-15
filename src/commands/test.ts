/*
  Copyright (C) 2021 Gert-Jan Bekker
  mine2updater - Test command (create test DB and run pipelines to verify TypeScript code)
*/

import { spawn } from "child_process";
import * as process from "process";
import * as path from "path";
import * as url from "url";
import * as fs from "fs";
import yaml from "js-yaml";

import * as general from "../modules/general.js";
import type { Config } from "../types/index.js";
import type { PipelineName } from "./update.js";

const fsp = fs.promises;

const ALL_PIPELINES: PipelineName[] = ["pdbj", "cc", "ccmodel", "prd", "vrpt", "contacts"];

export interface TestOptions {
  configFile?: string;
  drop?: boolean;
  pipelines?: string;
  limit?: number;
}

interface DBConfig {
  dbname: string;
  user: string;
  port: string;
}

function parseConnectionString(connString: string): DBConfig {
  const config: DBConfig = { dbname: "", user: "", port: "5432" };
  const matches = connString.match(/dbname=['"]([^'"]+)['"]/);
  if (matches) config.dbname = matches[1];
  const userMatch = connString.match(/user=['"]([^'"]+)['"]/);
  if (userMatch) config.user = userMatch[1];
  const portMatch = connString.match(/port=(\d+)/);
  if (portMatch) config.port = portMatch[1];
  return config;
}

async function runPsql(
  dbConfig: DBConfig,
  database: string,
  command: string
): Promise<{ stdout: string; stderr: string }> {
  return new Promise((resolve, reject) => {
    const args = ["-U", dbConfig.user, "-p", dbConfig.port, "-d", database, "-t", "-A", "-c", command];
    const psql = spawn("psql", args, {
      stdio: ["ignore", "pipe", "pipe"],
      env: { ...process.env, PGPASSWORD: process.env.PGPASSWORD || "" },
    });

    let stdout = "";
    let stderr = "";

    psql.stdout?.on("data", (data) => {
      stdout += data.toString();
    });

    psql.stderr?.on("data", (data) => {
      stderr += data.toString();
    });

    psql.on("error", (error) => {
      reject(new Error(`psql failed: ${error.message}`));
    });

    psql.on("close", (code) => {
      if (code !== 0 && stderr && !stderr.includes("does not exist")) {
        reject(new Error(`psql exited with code ${code}: ${stderr}`));
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

async function createDatabase(dbConfig: DBConfig, dbName: string): Promise<void> {
  console.log(`==> Creating test database: ${dbName}...`);
  // Use current user to create database (like setup-test-db.sh does)
  const currentUser = process.env.USER || process.env.USERNAME || "postgres";
  const args = ["-U", currentUser, "-p", dbConfig.port, "-d", "postgres", "-c", `CREATE DATABASE ${dbName} OWNER ${dbConfig.user};`];
  
  return new Promise((resolve, reject) => {
    const psql = spawn("psql", args, {
      stdio: "inherit",
      env: { ...process.env, PGPASSWORD: process.env.PGPASSWORD || "" },
    });

    psql.on("error", (error) => {
      reject(new Error(`Failed to create database: ${error.message}`));
    });

    psql.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`Failed to create database: psql exited with code ${code}`));
      } else {
        resolve();
      }
    });
  });
}

async function dropDatabase(dbConfig: DBConfig, dbName: string): Promise<void> {
  console.log(`==> Dropping existing test database: ${dbName}...`);
  // Use current user to drop database (like setup-test-db.sh does)
  const currentUser = process.env.USER || process.env.USERNAME || "postgres";
  
  // First, terminate all connections to the database
  const terminateArgs = [
    "-U", currentUser,
    "-p", dbConfig.port,
    "-d", "postgres",
    "-c",
    `SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '${dbName}' AND pid <> pg_backend_pid();`
  ];
  
  await new Promise<void>((resolve) => {
    const psql = spawn("psql", terminateArgs, {
      stdio: "ignore",
      env: { ...process.env, PGPASSWORD: process.env.PGPASSWORD || "" },
    });
    psql.on("close", () => resolve());
  });
  
  // Wait a bit for connections to be terminated
  await new Promise((resolve) => setTimeout(resolve, 500));
  
  // Now drop the database
  const args = ["-U", currentUser, "-p", dbConfig.port, "-d", "postgres", "-c", `DROP DATABASE IF EXISTS ${dbName};`];
  
  return new Promise((resolve, reject) => {
    const psql = spawn("psql", args, {
      stdio: "inherit",
      env: { ...process.env, PGPASSWORD: process.env.PGPASSWORD || "" },
    });

    psql.on("error", (error) => {
      // Ignore errors if database doesn't exist
      resolve();
    });

    psql.on("close", (code) => {
      resolve();
    });
  });
}

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

async function checkTableCounts(dbConfig: DBConfig, dbName: string, schemas: string[]): Promise<void> {
  console.log("\n==> Checking table counts...");

  try {
    const schemaList = schemas.map((s) => `'${s}'`).join(", ");
    const result = await runPsql(
      dbConfig,
      dbName,
      `SELECT schemaname, relname AS tablename, n_live_tup AS row_count FROM pg_stat_user_tables WHERE schemaname IN (${schemaList}) ORDER BY schemaname, relname;`
    );

    const lines = result.stdout
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    if (lines.length === 0) {
      console.log("  No tables found");
      return;
    }

    console.log("\n=== Table Counts ===");
    let currentSchema = "";
    for (const line of lines) {
      const parts = line.split("|").map((p) => p.trim());
      if (parts.length >= 3) {
        const [schema, table, count] = parts;
        if (schema !== currentSchema) {
          currentSchema = schema;
          console.log(`\n  [${schema}]`);
        }
        console.log(`    ${table}: ${count}`);
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not check table counts: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export async function testCommand(options: TestOptions): Promise<void> {
  const configFile = options.configFile || "config.test.yml";

  console.log("==> Starting test DB setup...");
  console.log(`==> Using config file: ${configFile}`);

  // Load test config
  if (!fs.existsSync(configFile)) {
    throw new Error(`Test config file not found: ${configFile}`);
  }

  const config = yaml.load(await fsp.readFile(configFile, "utf8")) as Config;
  global.config = config;
  config.argv = {};
  // Set limit for test runs (default to 10 if not specified)
  if (options.limit !== undefined) {
    config.argv.limit = options.limit;
  } else {
    config.argv.limit = 10; // Default test limit
  }
  config.defines = config.defines || {};

  const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
  config.defines.CWD = path.join(__dirname, "../../");

  general.solveDefines(config.defines);

  global.moduleFolder = path.join(__dirname, "../modules/");
  global.pipelineFolder = path.join(__dirname, "../pipelines/");

  // Parse database config from connection string
  const dbConfig = parseConnectionString(config.rdb.constring);
  const testDbName = dbConfig.dbname;

  if (!testDbName) {
    throw new Error("Could not parse database name from connection string");
  }

  // Check if database exists
  let dbExists = false;
  try {
    const checkResult = await runPsql(
      dbConfig,
      "postgres",
      `SELECT 1 FROM pg_database WHERE datname = '${testDbName}';`
    );
    dbExists = checkResult.stdout.trim().length > 0;
  } catch (error) {
    // If query fails, assume database doesn't exist
    dbExists = false;
  }

  // Drop database if requested or if it exists
  if (dbExists) {
    if (options.drop) {
      // Drop existing database
      await dropDatabase(dbConfig, testDbName);
      // Wait a bit for the database to be fully dropped
      await new Promise((resolve) => setTimeout(resolve, 500));
    } else {
      throw new Error(
        `Database ${testDbName} already exists. Use --drop to recreate it.`
      );
    }
  }

  // Create test database
  await createDatabase(dbConfig, testDbName);

  // Determine which pipelines to run
  let pipelinesToRun: PipelineName[] = ALL_PIPELINES;
  if (options.pipelines) {
    const requestedPipelines = options.pipelines.split(",").map((p) => p.trim()) as PipelineName[];
    const invalidPipelines = requestedPipelines.filter((p) => !ALL_PIPELINES.includes(p));
    if (invalidPipelines.length > 0) {
      throw new Error(`Invalid pipelines: ${invalidPipelines.join(", ")}`);
    }
    pipelinesToRun = requestedPipelines;
  }

  console.log(`==> Running pipelines: ${pipelinesToRun.join(", ")}`);

  // Run each pipeline
  for (const pipelineName of pipelinesToRun) {
    console.log(`\n==> Running ${pipelineName}.load pipeline...`);
    try {
      await runPipeline(pipelineName, config);
      console.log(`==> ${pipelineName}.load completed successfully`);
    } catch (error) {
      console.error(`==> Error in ${pipelineName}.load:`, error instanceof Error ? error.message : String(error));
      throw error;
    }
  }

  // Check results - show table counts for all schemas
  const schemas = ["pdbj", "cc", "ccmodel", "prd", "vrpt", "contacts"];
  await checkTableCounts(dbConfig, testDbName, schemas);

  console.log("\n==> Test completed successfully!");
  console.log(`==> Test database: ${testDbName}`);
  console.log(`==> Connect with: psql -U ${dbConfig.user} -p ${dbConfig.port} -d ${testDbName}`);
}
