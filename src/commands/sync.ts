/*
  Copyright (C) 2021 Gert-Jan Bekker
  mine2updater - Sync command (rsync data from PDBj)
*/

import { spawn } from "child_process";
import * as fs from "fs";
import * as path from "path";

export type SyncTarget =
  | "pdbj"
  | "cc"
  | "ccmodel"
  | "prd"
  | "vrpt"
  | "contacts"
  | "schemas"
  | "dictionaries";

interface SyncConfig {
  source: string;
  dest: string;
  description: string;
  cwd?: string;
  includes?: string[];
  excludes?: string[];
}

const SYNC_CONFIGS: Record<SyncTarget, SyncConfig> = {
  pdbj: {
    source: "data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-noatom",
    dest: ".",
    description: "mmjson-noatom",
    cwd: "data",
  },
  cc: {
    source: "data.pdbj.org::rsync/pdbjplus/data/cc/mmjson/",
    dest: "data/cc",
    description: "Chemical Component (cc)",
  },
  ccmodel: {
    source: "data.pdbj.org::rsync/pdbjplus/data/ccmodel/mmjson/",
    dest: "data/ccmodel",
    description: "CC Model (ccmodel)",
  },
  prd: {
    source: "data.pdbj.org::rsync/pdbjplus/data/prd/mmjson/",
    dest: "data/prd",
    description: "BIRD (prd)",
  },
  vrpt: {
    source: "data.pdbj.org::ftp/validation_reports/*/*/*_validation.cif.gz",
    dest: "data/vrpt",
    description: "Validation Reports (vrpt)",
  },
  contacts: {
    source: "data.pdbj.org::rsync/pdbjplus/data/pdb/contacts/",
    dest: "data/contacts",
    description: "Intermolecular contacts",
  },
  schemas: {
    source: "data.pdbj.org::rsync/pdbjplus/mine2/schemas/",
    dest: "schemas",
    description: "DB schemas",
  },
  dictionaries: {
    source: "data.pdbj.org::rsync/pdbjplus/dictionaries/",
    dest: "dictionaries",
    description: "Dictionaries",
  },
};

// Special handling for pdbj (includes plus)
const PDBJ_PLUS_CONFIG: SyncConfig = {
  source: "data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-plus/",
  dest: "plus",
  description: "mmjson-plus",
  cwd: "data",
};

async function runRsync(config: SyncConfig, baseDir: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const cwd = config.cwd ? path.join(baseDir, config.cwd) : baseDir;
    // If cwd is set, use relative path; otherwise use absolute path
    const destPath = config.cwd ? config.dest : path.join(baseDir, config.dest);

    // Ensure destination directory exists
    if (config.cwd) {
      fs.mkdirSync(cwd, { recursive: true });
    } else {
      const destDir = path.dirname(destPath);
      fs.mkdirSync(destDir, { recursive: true });
    }

    console.log(`==> Syncing ${config.description}...`);

    const args = ["-ah", "--delete", "--info=progress2"];

    // Add include patterns (order matters: includes before excludes)
    if (config.includes) {
      for (const pattern of config.includes) {
        args.push(`--include=${pattern}`);
      }
    }

    // Add exclude patterns
    if (config.excludes) {
      for (const pattern of config.excludes) {
        args.push(`--exclude=${pattern}`);
      }
    }

    args.push(config.source, destPath);

    const rsync = spawn("rsync", args, {
      cwd,
      stdio: "inherit",
    });

    rsync.on("error", (error) => {
      reject(new Error(`rsync failed: ${error.message}`));
    });

    rsync.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`rsync exited with code ${code}`));
      } else {
        resolve();
      }
    });
  });
}

export async function convertVrptToJson(baseDir: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const cifDir = path.join(baseDir, "data", "vrpt");
    const jsonDir = path.join(baseDir, "data", "vrpt-json");
    const scriptPath = path.join(baseDir, "scripts", "cif2json.py");
    const cifPattern = "*_validation.cif*";

    // Check if script exists
    if (!fs.existsSync(scriptPath)) {
      reject(new Error(`cif2json.py not found at ${scriptPath}`));
      return;
    }

    // Check if input directory exists and has files
    if (!fs.existsSync(cifDir)) {
      console.log(`==> Skipping vrpt conversion: ${cifDir} does not exist`);
      resolve();
      return;
    }

    // Check if there are any CIF files in the flat directory
    const items = fs.readdirSync(cifDir, { withFileTypes: true });
    const hasCifFiles = items.some(
      (item) =>
        item.isFile() &&
        (item.name.endsWith(".cif.gz") || item.name.endsWith(".cif"))
    );

    if (!hasCifFiles) {
      console.log(`==> Skipping vrpt conversion: No CIF files found in ${cifDir}`);
      resolve();
      return;
    }

    console.log(`==> Converting vrpt CIF files to JSON...`);

    // Use uv to run the script (PEP723 support)
    const python = spawn(
      "uv",
      ["run", "--script", scriptPath, cifDir, jsonDir, "--pattern", cifPattern],
      {
        cwd: baseDir,
        stdio: "inherit",
      }
    );

    python.on("error", (error) => {
      reject(new Error(`cif2json.py failed: ${error.message}`));
    });

    python.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`cif2json.py exited with code ${code}`));
      } else {
        console.log("==> vrpt conversion completed.");
        resolve();
      }
    });
  });
}

export async function syncCommand(targets: SyncTarget[]): Promise<void> {
  const baseDir = process.cwd();
  const allTargets: SyncTarget[] = targets.length > 0 ? targets : (Object.keys(SYNC_CONFIGS) as SyncTarget[]);

  console.log("==> Starting rsync...");

  // Special handling: if pdbj is included, also sync plus
  const targetsToSync = new Set<SyncTarget>(allTargets);
  if (targetsToSync.has("pdbj")) {
    targetsToSync.add("pdbj" as SyncTarget); // Keep pdbj
  }

  // Ensure data directory exists
  if (allTargets.some((t) => t !== "schemas" && t !== "dictionaries")) {
    fs.mkdirSync(path.join(baseDir, "data"), { recursive: true });
  }

  // Sync pdbj targets (noatom + plus)
  if (targetsToSync.has("pdbj")) {
    await runRsync(SYNC_CONFIGS.pdbj, baseDir);
    await runRsync(PDBJ_PLUS_CONFIG, baseDir);
  }

  // Sync other targets
  for (const target of allTargets) {
    if (target === "pdbj") continue; // Already handled above

    const config = SYNC_CONFIGS[target];
    if (config) {
      await runRsync(config, baseDir);
      
      // After vrpt sync, convert CIF to JSON
      if (target === "vrpt") {
        await convertVrptToJson(baseDir);
      }
    }
  }

  console.log("==> Rsync completed.");
}
