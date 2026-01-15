/*!
 * cif.ts
 *
 * JavaScript CIF parser: https://github.com/gjbekker/cif-parsers
 *
 * By Gert-Jan Bekker
 * License: MIT
 *   See https://github.com/gjbekker/cif-parsers/blob/master/LICENSE
 */

import type { CIFData, CIFDatablock, CIFCategory } from "../types/index.js";

const cifDicPath = "https://pdbj.org/cif-editor/dictionaries/mmcif_pdbx.json";

type TypeConverter = (value: string) => number | boolean | number[];
type CIFDict = Record<string, Record<string, TypeConverter>>;

let __CIFDICT__: CIFDict | null = null;

// pdbml

interface XMLElement {
  localName: string | null;
  textContent: string | null;
  childNodes: NodeListOf<ChildNode>;
  attributes: NamedNodeMap;
  getAttribute(name: string): string | null;
}

interface XMLDocument {
  documentElement: XMLElement;
}

class PDBMLparser {
  data: CIFData = {};

  parse(data: XMLDocument): void {
    const root = data.documentElement;
    const datablockName = root.getAttribute("datablockName") || "unknown";
    const rootJS: CIFDatablock = (this.data["data_" + datablockName] = {});
    let catName: string;
    let loopMode: boolean;
    let cat: XMLElement;
    let scat: XMLElement;
    let skip: string[];
    let item: Attr | XMLElement;
    let n: number;

    for (let i = 0; i < root.childNodes.length; i++) {
      cat = root.childNodes[i] as unknown as XMLElement;
      catName = cat.localName as string;
      if (!catName) continue;
      catName = catName.substring(0, catName.length - 8);
      const category: CIFCategory = (rootJS[catName] = {});
      loopMode = cat.childNodes.length > 3;
      n = 0;
      for (let j = 0; j < cat.childNodes.length; j++) {
        scat = cat.childNodes[j] as unknown as XMLElement;
        if (!scat.localName) continue;
        skip = [];
        for (let k = 0; k < scat.attributes.length; k++) {
          item = scat.attributes.item(k)!;
          if (loopMode) {
            if (!Object.prototype.hasOwnProperty.call(category, item.localName)) {
              category[item.localName] = new Array(n).fill(null);
            }
            category[item.localName].push(item.nodeValue);
            skip.push(item.localName);
          } else {
            category[item.localName] = [item.nodeValue];
          }
        }
        for (let k = 0; k < scat.childNodes.length; k++) {
          item = scat.childNodes[k] as unknown as XMLElement;
          if (!item.localName) continue;
          if (loopMode) {
            if (!Object.prototype.hasOwnProperty.call(category, item.localName)) {
              category[item.localName] = new Array(n).fill(null);
            }
            category[item.localName].push(item.textContent);
            skip.push(item.localName);
          } else {
            category[item.localName] = [item.textContent];
          }
        }
        if (loopMode) {
          for (const k in category) {
            if (skip.indexOf(k) === -1) category[k].push(null);
          }
        }
        n++;
      }
    }
  }
}

export async function loadPDBML(
  data: XMLDocument,
  noCnT?: boolean
): Promise<CIFData> {
  const parser = new PDBMLparser();
  parser.parse(data);

  if (noCnT) return parser.data;
  if (!__CIFDICT__) await loadCIFdic();

  for (const e in parser.data) {
    for (const e2 in parser.data[e]) {
      if (!Object.prototype.hasOwnProperty.call(__CIFDICT__, e2)) continue;
      for (const e3 in parser.data[e][e2]) {
        if (!Object.prototype.hasOwnProperty.call(__CIFDICT__![e2], e3)) continue;
        const func = __CIFDICT__![e2][e3];
        const arr = parser.data[e][e2][e3];
        if (Array.isArray(arr)) {
          for (let i = 0; i < arr.length; i++) {
            if (arr[i] !== null) {
              (arr as unknown[])[i] = func.call(null, arr[i] as string);
            }
          }
        } else {
          (parser.data[e][e2] as Record<string, unknown>)[e3] = func.call(
            null,
            arr as unknown as string
          );
        }
      }
    }
  }
  return parser.data;
}

// mmjson tree

function partition(obj: string, splt: string): [string, string] {
  const [pre, ...post] = obj.split(splt);
  return [pre, post.join(".")];
}

// mmcif parser

type TargetArray = (string | null)[];

class _loop {
  private parserObj: CIFparser;
  length = 0;
  private refID = -1;
  private refList: TargetArray[] = [];
  namesDefined = false;

  constructor(parserObj: CIFparser) {
    this.parserObj = parserObj;
  }

  addName(name: string): void {
    const catName = partition(name, ".");

    const ref = this.parserObj.currentTarget[
      this.parserObj.currentTarget.length - 2
    ] as Record<string, unknown>;
    if (catName[1]) {
      if (!Object.prototype.hasOwnProperty.call(ref, catName[0])) {
        ref[catName[0]] = {};
      }
      const cat = ref[catName[0]] as Record<string, TargetArray>;
      if (!Object.prototype.hasOwnProperty.call(cat, catName[1])) {
        cat[catName[1]] = [];
      }
      this.refList.push(cat[catName[1]]);
    } else {
      if (!Object.prototype.hasOwnProperty.call(ref, catName[0])) {
        ref[catName[0]] = [];
      }
      this.refList.push(ref[catName[0]] as TargetArray);
    }
    this.length = this.refList.length;
  }

  pushValue(value: string): void {
    this.namesDefined = true;
    const target = this.nextTarget();
    if (value === "stop_") {
      this.stopPush();
      return;
    }
    target.push(value);
  }

  private nextTarget(): TargetArray {
    this.refID = (this.refID + 1) % this.length;
    return this.refList[this.refID];
  }

  private stopPush(): void {
    this.refID = -1;
  }
}

type CurrentTargetItem =
  | CIFData
  | CIFDatablock
  | null
  | [Record<string, unknown>, string];
type CurrentTarget = CurrentTargetItem[];

export class CIFparser {
  data: CIFData = {};
  currentTarget: CurrentTarget = [];
  private loopPointer: _loop | null = null;
  private dataSet: boolean = false;
  error: [string, number, unknown] | null = null;
  private buffer: string[] = [];
  private multi_line_mode = false;

  constructor() {
    this.selectGlobal();
  }

  parseLine(line: string, i: number): void {
    let Z: string;
    try {
      Z = line.substring(0, 1);
      if (Z === "#") return;
      line = line.trim();
      if (Z === ";") {
        if (this.multi_line_mode) this.setDataValue(this.buffer.join("\n"));
        else this.buffer = [];
        this.multi_line_mode = !this.multi_line_mode;
        line = line.substring(1).trim();
      }
      if (this.multi_line_mode) this.buffer.push(line);
      else this.processContent(this.specialSplit(line));
    } catch (e) {
      this.error = [line, i, e];
    }
  }

  parse(lines: string | string[]): void {
    const lineArray = Array.isArray(lines) ? lines : lines.split("\n");
    for (let i = 0; i < lineArray.length; i++) {
      if (this.error) break;
      this.parseLine(lineArray[i], i);
    }
    if (this.error) {
      console.error(`Error found in line ${this.error[1]}:`);
      console.error("  ", this.error[2]);
      console.log("  ", this.error[0]);
    }
  }

  specialSplit(content: string): [string, boolean][] {
    const output: [string, boolean][] = [["", false]];
    let quote = false;
    let qtype = "";
    const length = content.length;
    let isWS: boolean;
    let olast = 0;

    for (let i = 0; i < length; i++) {
      isWS = content[i] === " " || content[i] === "\t";
      if (
        (content[i] === "'" || content[i] === '"') &&
        (((i === 0 || content[i - 1] === " " || content[i - 1] === "\t") &&
          !quote) ||
          ((i === length - 1 ||
            content[i + 1] === " " ||
            content[i + 1] === "\t") &&
            quote &&
            content[i] === qtype))
      ) {
        quote = !quote;
        qtype = content[i];
      } else if (!quote && isWS && output[olast][0] !== "") {
        output.push(["", false]);
        olast++;
      } else if (!quote && content[i] === "#" && output[olast][0] === "") {
        break;
      } else if (!isWS || quote) {
        output[olast][0] += content[i];
        output[olast][1] = quote;
      }
    }
    if (output[olast][0] === "") output.pop();
    return output;
  }

  processContent(content: [string, boolean][]): void {
    for (let i = 0; i < content.length; i++) {
      if (content[i][0] === "global_" && !content[i][1]) {
        this.loopPointer = null;
        this.selectGlobal();
      } else if (
        content[i][0].substring(0, 5) === "data_" &&
        !content[i][1]
      ) {
        this.loopPointer = null;
        this.selectData(content[i][0]);
      } else if (
        content[i][0].substring(0, 5) === "save_" &&
        !content[i][1]
      ) {
        this.loopPointer = null;
        if (content[i][0].substring(5).length) this.selectFrame(content[i][0]);
        else this.endFrame();
      } else if (content[i][0] === "loop_" && !content[i][1]) {
        this.loopPointer = new _loop(this);
      } else if (
        content[i][0].substring(0, 1) === "_" &&
        !content[i][1] &&
        this.dataSet !== false
      ) {
        this.setDataName(content[i][0].substring(1));
      } else {
        if (!this.loopPointer && this.dataSet) continue;
        this.setDataValue(content[i][0]);
      }
    }
  }

  setDataName(name: string): void {
    if (this.loopPointer != null) {
      if (this.loopPointer.namesDefined) {
        this.loopPointer = null;
      } else {
        this.loopPointer.addName(name);
        return;
      }
    }
    const nameParts = partition(name, ".");
    this.currentTarget.pop();
    const targetObj = this.currentTarget[
      this.currentTarget.length - 1
    ] as Record<string, unknown>;

    if (nameParts[1]) {
      if (!Object.prototype.hasOwnProperty.call(targetObj, nameParts[0])) {
        targetObj[nameParts[0]] = {};
      }
      (targetObj[nameParts[0]] as Record<string, unknown>)[nameParts[1]] = "";
      this.currentTarget.push([
        targetObj[nameParts[0]] as Record<string, unknown>,
        nameParts[1],
      ]);
    } else {
      targetObj[nameParts[0]] = "";
      this.currentTarget.push([
        targetObj as Record<string, unknown>,
        nameParts[0],
      ]);
    }
    this.dataSet = false;
  }

  setDataValue(value: string): void {
    if (this.loopPointer != null) {
      this.loopPointer.pushValue(value);
    } else {
      const tmp = this.currentTarget[
        this.currentTarget.length - 1
      ] as [Record<string, unknown>, string];
      tmp[0][tmp[1]] = [value];
      this.dataSet = true;
    }
  }

  selectGlobal(): void {
    this.currentTarget = [this.data, this.data, null];
  }

  selectData(name: string): void {
    if (!Object.prototype.hasOwnProperty.call(this.data, name)) {
      this.data[name] = {};
    }
    this.currentTarget = [this.data, this.data[name], null];
  }

  selectFrame(name: string): void {
    const target = this.currentTarget[1] as Record<string, unknown>;
    if (!Object.prototype.hasOwnProperty.call(target, name)) {
      target[name] = {};
    }
    this.currentTarget = this.currentTarget.slice(0, 2);
    this.currentTarget.push(target[name] as CIFDatablock);
    this.currentTarget.push(null);
  }

  endData(): void {
    this.currentTarget = this.currentTarget.slice(0, 2);
  }

  endFrame(): void {
    this.currentTarget = this.currentTarget.slice(0, 3);
  }
}

interface DictionaryData {
  [key: string]: {
    item_type?: {
      code: string[];
    };
    [key: string]: unknown;
  };
}

export function parseCIFdictionary(
  data: Record<string, DictionaryData>
): Record<string, Record<string, string>> {
  const keys = Object.keys(data);
  if (!keys.length) return {};
  const ref = data[keys[0]];
  const dic: Record<string, Record<string, string>> = {};

  for (const e in ref) {
    if (
      typeof ref[e] !== "object" ||
      Array.isArray(ref[e]) ||
      !Object.prototype.hasOwnProperty.call(ref[e], "item_type")
    )
      continue;
    const name = partition(e.substring(6), ".");
    if (!Object.prototype.hasOwnProperty.call(dic, name[0])) dic[name[0]] = {};
    dic[name[0]][name[1]] = ref[e].item_type!.code[0].trim();
  }
  return dic;
}

export function parse(data: string | string[]): CIFData {
  const parser = new CIFparser();
  parser.parse(data);
  return parser.data;
}

export async function __loadCIFdic(
  dic?: string | Record<string, Record<string, string>>
): Promise<void> {
  if (__CIFDICT__ != null) return;
  await loadCIFdic(dic);
}

export async function loadCIFdic(
  dic?: string | Record<string, Record<string, string>>,
  reset = true
): Promise<CIFDict> {
  if (!dic || typeof dic === "string") {
    const request = await fetch(dic || cifDicPath);

    if (cifDicPath.endsWith(".json")) {
      dic = await request.json();
    } else {
      const parser = new CIFparser();
      parser.parse(await request.text());
      dic = parser.data as unknown as Record<string, Record<string, string>>;
    }
    dic = parseCIFdictionary(
      dic as unknown as Record<string, DictionaryData>
    );
  }

  const typing: CIFDict = reset ? {} : __CIFDICT__ || {};

  for (const e in dic) {
    for (const e2 in dic[e]) {
      const typeCode = dic[e][e2];
      if (typeCode === "int" || typeCode === "positive_int") {
        if (!Object.prototype.hasOwnProperty.call(typing, e)) typing[e] = {};
        typing[e][e2] = parseInt;
      } else if (typeCode === "float") {
        if (!Object.prototype.hasOwnProperty.call(typing, e)) typing[e] = {};
        typing[e][e2] = parseFloat;
      } else if (typeCode === "int-range") {
        if (!Object.prototype.hasOwnProperty.call(typing, e)) typing[e] = {};
        typing[e][e2] = parseIntRange;
      } else if (typeCode === "float-range") {
        if (!Object.prototype.hasOwnProperty.call(typing, e)) typing[e] = {};
        typing[e][e2] = parseFloatRange;
      } else if (typeCode === "boolean") {
        if (!Object.prototype.hasOwnProperty.call(typing, e)) typing[e] = {};
        typing[e][e2] = parseBoolean;
      }
    }
  }

  __CIFDICT__ = typing;
  return typing;
}

function parseIntRange(inp: string): number[] {
  try {
    const pos = inp.indexOf("-", 1);
    if (pos === -1) throw -1;
    return [parseInt(inp.substring(0, pos)), parseInt(inp.substring(pos + 1))];
  } catch {
    return [parseInt(inp)];
  }
}

function parseFloatRange(inp: string): number[] {
  try {
    const pos = inp.indexOf("-", 1);
    if (pos === -1) throw -1;
    return [
      parseFloat(inp.substring(0, pos)),
      parseFloat(inp.substring(pos + 1)),
    ];
  } catch {
    return [parseFloat(inp)];
  }
}

function parseBoolean(inp: string): boolean {
  return inp.toLowerCase() === "yes";
}

export async function loadCIF(data: string, noCnT?: boolean): Promise<CIFData> {
  const parser = new CIFparser();
  parser.parse(data);

  if (noCnT) return parser.data;
  if (!__CIFDICT__) await loadCIFdic();

  cleanJSON_withDict(parser.data);

  return parser.data;
}

export function cleanJSON_withDict(
  data: CIFData,
  cifdic?: CIFDict
): CIFData {
  cifdic = cifdic || __CIFDICT__!;

  for (const e in data) {
    for (const e2 in data[e]) {
      for (const e3 in data[e][e2]) {
        const arr = data[e][e2][e3];
        if (Array.isArray(arr)) {
          for (let i = 0; i < arr.length; i++) {
            arr[i] =
              arr[i] !== "?" && arr[i] !== "." ? arr[i] : null;
          }
        } else {
          (data[e][e2] as unknown as Record<string, string | null>)[e3] =
            arr !== "?" && arr !== "." ? (arr as string) : null;
        }
      }
    }
  }

  for (const e in data) {
    for (const e2 in data[e]) {
      if (!Object.prototype.hasOwnProperty.call(cifdic, e2)) continue;
      for (const e3 in data[e][e2]) {
        if (!Object.prototype.hasOwnProperty.call(cifdic[e2], e3)) continue;
        const func = cifdic[e2][e3];
        const arr = data[e][e2][e3];
        if (Array.isArray(arr)) {
          for (let i = 0; i < arr.length; i++) {
            (arr as unknown[])[i] =
              arr[i] == null ? null : func.call(null, arr[i] as string);
          }
        } else {
          (data[e][e2] as Record<string, unknown>)[e3] =
            arr == null ? null : func.call(null, arr as unknown as string);
        }
      }
    }
  }
  return data;
}

interface DumpSettings {
  omitHash?: boolean;
  forceLoop?: boolean;
  splitLoop?: string;
}

export function dumpCIF(data: CIFData, settings?: DumpSettings): string {
  settings = settings || {};
  let output = "";

  const cifStrCheck = new RegExp("[\\s()]");
  const cifStrNLCheck = new RegExp("[\n]");

  let sliceConst = "";
  for (let i = 0; i < 1024; i++) sliceConst += " ";
  const padString = function (inp: string, flength: number): string {
    return inp + sliceConst.slice(inp.length, flength);
  };

  const dumpStr = function (inp: unknown): string {
    if (inp == null) return "?";
    else {
      if (typeof inp !== "string") return inp + "";
      if (cifStrNLCheck.test(inp)) return "\n;" + inp + "\n;";
      if (cifStrCheck.test(inp)) return "'" + inp + "'";
      return inp;
    }
  };

  const dumpCat = function (k: string, v: CIFCategory): void {
    if (!settings!.omitHash) output += "#\n";
    let noi: number;
    let pad: number | number[];
    const keys = Object.keys(v);
    if (keys.length === 0) return;
    noi = v[keys[0]].length;
    if (noi === 0 && !settings!.forceLoop) return;
    if (noi === 1 && !settings!.forceLoop) {
      pad = 0;
      for (const k2 in v) if (k2.length > pad) pad = k2.length;
      pad += 3;
      for (const k2 in v) {
        output += "_" + k + "." + padString(k2, pad) + dumpStr(v[k2][0]) + "\n";
      }
    } else {
      output += "loop_\n";
      pad = [];
      for (const k2 in v) {
        output += "_" + k + "." + k2 + "\n";
        pad.push(0);
      }
      if (settings!.splitLoop) output += "#" + settings!.splitLoop + "#\n";

      for (let i = 0; i < noi; i++) {
        let j = 0;
        for (const k2 in v) {
          const tmp1 = dumpStr(v[k2][i]);
          if (tmp1.substring(0, 2) !== "\n;" && tmp1.length > pad[j]) {
            pad[j] = tmp1.length;
          }
          j++;
        }
      }

      for (let j = 0; j < pad.length; j++) pad[j]++;

      for (let i = 0; i < noi; i++) {
        let j = 0;
        let tmp1 = "";
        for (const k2 in v) {
          tmp1 += padString(dumpStr(v[k2][i]), pad[j]);
          j++;
        }
        output += tmp1 + "\n";
        if (i % 200000 === 0) output[0]; // prevent chrome (aka V8) from crapping out
      }
    }
    if (output.length && output[output.length - 1] !== "\n") output += "\n";
  };

  let inner = true;
  const dumpPart = function (
    part: Record<string, unknown>,
    skip?: boolean
  ): void {
    for (const k in part) {
      if (typeof part[k] === "object" && !Array.isArray(part[k])) {
        if (
          k.substring(0, 5) !== "data_" &&
          k.substring(0, 5) !== "save_" &&
          k.substring(0, 7) !== "global_"
        ) {
          dumpCat(k, part[k] as CIFCategory);
        } else {
          output += k + "\n";
          dumpPart(part[k] as Record<string, unknown>);
          inner = false;
        }
      }
    }
    if (!(skip || !inner)) output += (settings!.omitHash ? "" : "#") + "\n";
    output[0]; // prevent chrome (aka V8) from crapping out
  };
  dumpPart(data);

  return output;
}
