/*
  Copyright (C) 2021 Gert-Jan Bekker
  gertjan.bekker@gmail.com
*/

import * as fs from "fs";
import * as readline from "readline";
import * as path from "path";
import * as zlib from "zlib";
import * as child_process from "child_process";

import Long from "long";
import picomatch from "picomatch";

import type {
  WalkOptions,
  WalkFile,
  WalkContainer,
  MemObj,
  ExecCommandOptions,
  ChemCompAtom,
  ChemCompBond,
  MMJsonDatablock,
} from "../types/index.js";

const fsp = fs.promises;

interface WalkFileWithPendingStats extends WalkFile {
  _pendingStats?: Promise<fs.Stats>;
}

export async function walkPattern(
  pattern: string,
  options: WalkOptions = {}
): Promise<WalkFile[]> {
  const base = path.dirname(pattern.substring(0, pattern.indexOf("*"))) + "/";
  const matchObj = picomatch(pattern);

  const files: WalkFileWithPendingStats[] = [];
  const pattern_handler = function (pth: string): void {
    if (!matchObj(pth)) return;
    const obj: WalkFileWithPendingStats = { path: pth, name: path.basename(pth) };
    if (options.stats) {
      obj._pendingStats = fsp.stat(pth);
    }
    files.push(obj);
  };

  await walk(base, { pattern_handler });
  if (options.stats) {
    for (const file of files) {
      if (file._pendingStats) {
        file.stats = await file._pendingStats;
        delete file._pendingStats;
      }
    }
  }
  return files;
}

export async function walk(cwd: string, container: WalkContainer): Promise<void> {
  let items: fs.Dirent[];
  try {
    items = await fsp.readdir(cwd, { withFileTypes: true });
  } catch (e) {
    console.error(e);
    return;
  }
  const jobs: Promise<void>[] = [];
  for (const item of items) {
    const pth = cwd + item.name;
    if (item.isDirectory()) {
      jobs.push(walk(pth + "/", container));
    } else {
      container.pattern_handler(pth, container);
    }
  }
  await Promise.all(jobs);
}

export function solveDefines(defines: Record<string, string>): void {
  let N = 0;
  while (true) {
    let bad = false;
    for (const [k, v] of Object.entries(defines)) {
      if (v.indexOf("${") !== -1) {
        bad = true;
        defines[k] = expandPath(v);
      }
    }
    if (!bad) break;
    N++;
    if (N > 10) {
      console.error("Cannot resolve defines...");
      process.exit();
    }
  }
  for (const [k, v] of Object.entries(defines)) {
    defines[k] = path.normalize(expandPath(v));
  }
}

export async function exists(loc: string): Promise<boolean> {
  try {
    await fsp.access(loc, fs.constants.F_OK);
  } catch {
    return false;
  }
  return true;
}

export function expandPath(pth: string): string {
  for (const [name, repl] of Object.entries(global.config?.defines || {})) {
    pth = pth.replace("${" + name + "}", repl);
  }
  return path.normalize(pth);
}

interface PoolClient {
  id: number;
  release: () => void;
}

export class ArbitraryPooler {
  private max: number;
  private pool: PoolClient[] = [];
  private clients: PoolClient[] = [];

  constructor(mx: number) {
    this.max = mx;
  }

  async request(): Promise<PoolClient> {
    if (this.clients.length < this.max) {
      const client: PoolClient = {
        id: this.clients.length,
        release: () => {
          this.pool.push(client);
        },
      };
      this.clients.push(client);
      return client;
    }

    while (true) {
      if (this.pool.length) {
        return this.pool.shift()!;
      }
      await wait();
    }
  }
}

// Legacy function for backward compatibility
export function arbitraryPooler(mx: number): ArbitraryPooler {
  return new ArbitraryPooler(mx);
}

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

export function wait(): Promise<void> {
  return new Promise((resolve) => {
    setImmediate(resolve);
  });
}

// cc

export async function mdl2fp(
  mdl: string,
  obabel: string
): Promise<(string | number)[]> {
  const obabelIn: ExecCommandOptions = {
    input: mdl,
    encoding: "utf8",
    stdio: "pipe",
  };
  let smiles: string | undefined;
  let fpt: string | undefined;

  try {
    smiles = (
      await execCommand(obabel, ["-imdl", "-ocan", "---errorlevel 1"], obabelIn)
    ).trim();
  } catch {
    // ignore
  }
  if (!smiles) {
    try {
      smiles = (
        await execCommand(obabel, ["-imdl", "-osmi", "---errorlevel 1"], obabelIn)
      ).trim();
    } catch {
      // ignore
    }
  }

  if (smiles) {
    obabelIn.input = smiles;
    try {
      fpt = (
        await execCommand(obabel, ["-ismi", "-ofpt", "---errorlevel 1"], obabelIn)
      ).trim();
    } catch {
      // ignore
    }
  } else {
    // mdl input
    obabelIn.input = mdl;
    try {
      fpt = (
        await execCommand(obabel, ["-imdl", "-ofpt", "---errorlevel 1"], obabelIn)
      ).trim();
    } catch {
      // ignore
    }
  }

  // fptが空またはundefinedの場合はデフォルト値を返す
  if (!fpt || fpt.trim() === "") {
    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  }

  const fptLines = fpt.split("\n");
  fptLines.splice(0, 1);
  const fptParts = fptLines.join("").split(" ");
  const fpt_int: (string | number)[] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  let i = 0;
  while (fptParts.length) {
    const a = fptParts.shift()!;
    const b = fptParts.length ? fptParts.shift()! : "";
    // 空文字列の場合はスキップ
    if ((a + b).trim() === "") continue;
    fpt_int[i] = Long.fromString(a + b, true, 16).toString();
    i++;
  }

  return fpt_int;
}

export async function mdl2svg(memObj: MemObj, obabel: string): Promise<string> {
  if (!memObj.mdl) cc2mdl(memObj);
  let svg: string | undefined;
  let raw: string | undefined;
  const options: ExecCommandOptions = {
    input: memObj.mdl,
    encoding: "utf8",
    stdio: "pipe",
  };

  try {
    raw = await execCommand(
      obabel,
      ["-xX", "-imdl", "-osvg", "---errorlevel 1", memObj.mdl_noH || ""],
      options
    );
  } catch (e) {
    console.log(e);
  }

  try {
    // deal with bad svg content from openbabel...
    const tmp = raw!.split('viewBox="');
    const viewBox = tmp[tmp.length - 1].split('"')[0].split(" ");
    svg = raw!.split('stroke-linecap="round">')[1].split("</svg>")[0];
    svg =
      `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cml="http://www.xml-cml.org/schema" width="${viewBox[2]}" height="${viewBox[3]}" x="0" y="0" font-family="sans-serif" stroke="rgb(0,0,0)" stroke-width="1" stroke-linecap="round" viewBox="0 0 ${viewBox[2]} ${viewBox[3]}">\n` +
      svg +
      "\n</svg>";
  } catch {
    console.error(
      "\n\tSVG failed:",
      memObj.entryId,
      options.error,
      options.stderr,
      raw,
      "\n"
    ); // 0CR FDC
  }

  return svg || "";
}

export function cc2mdl(memObj: MemObj): void {
  const mmjson = memObj.mmjson as MMJsonDatablock;

  let noha = 0;

  const chem_comp_atom = getObjectValue<ChemCompAtom>(mmjson, "chem_comp_atom", {
    atom_id: [],
    type_symbol: [],
    charge: [],
    model_Cartn_x: [],
    model_Cartn_y: [],
    model_Cartn_z: [],
    pdbx_model_Cartn_x_ideal: [null],
    pdbx_model_Cartn_y_ideal: [],
    pdbx_model_Cartn_z_ideal: [],
  });
  const chem_comp_bond = getObjectValue<ChemCompBond>(mmjson, "chem_comp_bond", {
    atom_id_1: [],
    atom_id_2: [],
    value_order: [],
  });

  const okAtoms: Record<string, number> = {};
  let Natoms = 0;
  let Nbonds = 0;
  let mol = "";

  if (chem_comp_atom.pdbx_model_Cartn_x_ideal[0] == null) {
    for (let i = 0; i < chem_comp_atom.atom_id.length; i++) {
      if (
        chem_comp_atom.type_symbol[i] !== "H" &&
        chem_comp_atom.type_symbol[i] !== "D"
      ) {
        noha += 1;
      }

      const charge = chem_comp_atom.charge[i];
      const symbol = chem_comp_atom.type_symbol[i]
        .toLowerCase()
        .replace(/^\w/, (c) => c.toUpperCase());
      mol += `M V30 ${i + 1} ${symbol} ${(chem_comp_atom.model_Cartn_x[i] || 0.0).toFixed(3)} ${(chem_comp_atom.model_Cartn_y[i] || 0.0).toFixed(3)} ${(chem_comp_atom.model_Cartn_z[i] || 0.0).toFixed(3)} 0${charge ? " CHG=" + charge : ""}\n`;

      okAtoms[chem_comp_atom.atom_id[i]] = Natoms;
      Natoms++;
    }
  } else {
    for (let i = 0; i < chem_comp_atom.atom_id.length; i++) {
      if (
        chem_comp_atom.type_symbol[i] !== "H" &&
        chem_comp_atom.type_symbol[i] !== "D"
      ) {
        noha += 1;
      }

      const charge = chem_comp_atom.charge[i];
      const symbol = chem_comp_atom.type_symbol[i]
        .toLowerCase()
        .replace(/^\w/, (c) => c.toUpperCase());
      mol += `M V30 ${i + 1} ${symbol} ${(chem_comp_atom.pdbx_model_Cartn_x_ideal[i] || 0.0).toFixed(3)} ${(chem_comp_atom.pdbx_model_Cartn_y_ideal[i] || 0.0).toFixed(3)} ${(chem_comp_atom.pdbx_model_Cartn_z_ideal[i] || 0.0).toFixed(3)} 0${charge ? " CHG=" + charge : ""}\n`;

      okAtoms[chem_comp_atom.atom_id[i]] = Natoms;
      Natoms++;
    }
  }

  mol += "M V30 END ATOM\nM V30 BEGIN BOND\n";

  for (let i = 0; i < chem_comp_bond.atom_id_1.length; i++) {
    const idx1 = okAtoms[chem_comp_bond.atom_id_1[i]];
    const idx2 = okAtoms[chem_comp_bond.atom_id_2[i]];
    if (idx1 === undefined || idx2 === undefined) continue;
    let bondType: string = chem_comp_bond.value_order[i].toLowerCase();
    if (bondType === "sing") bondType = "1";
    else if (bondType === "doub") bondType = "2";
    else if (bondType === "trip") bondType = "3";

    mol += `M V30 ${i + 1} ${bondType} ${idx1 + 1} ${idx2 + 1}\n`;

    Nbonds++;
  }

  mol = `\n\n\n 0 0 0 0 0 999 V3000
M V30 BEGIN CTAB
M V30 COUNTS ${Natoms} ${Nbonds} 0 0 1
M V30 BEGIN ATOM
${mol}M V30 END BOND
M V30 END CTAB
M END`;

  memObj.mdl = mol;
  memObj.mdl_noH = noha > 1 ? "-d" : "";
  memObj.mdl_Natoms = Natoms;
}

// end cc

export function getObjectValue<T>(
  object: Record<string, unknown>,
  field: string,
  defaultValue: T
): T {
  if (field in object) return object[field] as T;
  else return defaultValue;
}

export function execCommand(
  cmd: string,
  args: string[],
  options?: ExecCommandOptions
): Promise<string>;
export function execCommand(
  cmd: string,
  args: string[],
  options: ExecCommandOptions & { extended: true }
): Promise<[Error | null, string, string]>;
export function execCommand(
  cmd: string,
  args: string[],
  options: ExecCommandOptions = {}
): Promise<string | [Error | null, string, string]> {
  const deferred = new Deferred<string | [Error | null, string, string]>();
  const proc = child_process.execFile(
    cmd,
    args,
    function (error, stdout, stderr) {
      if (options.extended) {
        deferred.resolve([error, stdout, stderr]);
      } else {
        options.error = error;
        options.stderr = stderr;
        deferred.resolve(stdout);
      }
    }
  );
  if (options.input) {
    proc.stdin!.write(options.input);
    proc.stdin!.end();
  }
  return deferred.promise;
}

export async function* walkdir(loc: string): AsyncGenerator<string, void, unknown> {
  const items = await fsp.readdir(loc, { withFileTypes: true });
  for (const i of items) {
    if (i.isDirectory()) {
      yield* walkdir(loc + "/" + i.name);
    } else {
      yield loc + "/" + i.name;
    }
  }
}

export class Deferred<T> {
  promise: Promise<T>;
  resolve!: (value: T | PromiseLike<T>) => void;
  reject!: (reason?: unknown) => void;

  constructor() {
    this.promise = new Promise<T>((resolve, reject) => {
      this.resolve = resolve;
      this.reject = reject;
    });
  }
}

export function gzip(
  input: zlib.InputType,
  options?: zlib.ZlibOptions
): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    zlib.gzip(input, options || {}, (error, result) => {
      if (!error) resolve(result);
      else reject(new Error(String(error)));
    });
  });
}

export function gunzip(
  input: zlib.InputType,
  options?: zlib.ZlibOptions
): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    zlib.gunzip(input, options || {}, (error, result) => {
      if (!error) resolve(result);
      else reject(new Error(String(error)));
    });
  });
}

export async function readlineGZ(
  loc: string,
  todo: (line: string) => void
): Promise<void> {
  const deferred = new Deferred<void>();

  let inp: fs.ReadStream | zlib.Gunzip = fs.createReadStream(loc);
  if (loc.endsWith(".gz")) {
    inp = inp.pipe(zlib.createGunzip());
  }
  inp.on("error", () => {
    deferred.reject();
  });

  const readInterface = readline.createInterface({
    input: inp,
    terminal: false,
  });
  readInterface.on("line", todo);

  readInterface.on("close", () => {
    deferred.resolve();
  });

  return deferred.promise;
}
