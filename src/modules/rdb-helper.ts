/* eslint-disable @typescript-eslint/no-explicit-any */
import * as crypto from "crypto";
import * as fs from "fs";
import pgformat from "pg-format";
import yaml from "js-yaml";

import { Client } from "./pg-native-custom.js";
import { Deferred, expandPath, readlineGZ } from "./general.js";
import { CIFparser } from "./cif.js";
import type { MMJsonDatablock } from "../types/index.js";

const fsp = fs.promises;

// Extend built-in types
declare global {
  interface Array<T> {
    unique(): T[];
  }
  interface String {
    ljust(length: number, chr?: string): string;
    rjust(length: number, chr?: string): string;
  }
}

Array.prototype.unique = function <T>(this: T[]): T[] {
  return Array.from(new Set(this));
};

String.prototype.ljust = function (length: number, chr = " "): string {
  const fill: string[] = [];
  while (fill.length + this.length < length) fill[fill.length] = chr;
  return this + fill.join("");
};

String.prototype.rjust = function (length: number, chr = " "): string {
  const fill: string[] = [];
  while (fill.length + this.length < length) fill[fill.length] = chr;
  return fill.join("") + this;
};

// Type definitions
type TypeConverter = (value: unknown) => unknown;
type SqlTyping = Record<string, Record<string, TypeConverter>>;
type SqlPK = Record<string, [string, string][]>;
type SqlPKRef = Record<string, Record<string, number>>;
type SqlStruct = Record<string, [string, string][]>;
type KeywordFields = Record<string, Record<string, boolean>>;
type IndexFields = Record<string, Record<string, boolean>>;

interface RdbConfig {
  primaryKey: string;
  primaryKeyFormat?: string;
  schema: string;
  cifDicts?: string[];
  type_overwrites?: Record<string, string>;
  skip_foreign_keys?: boolean;
  [key: string]: unknown;
}

interface RdbTable {
  name: string;
  columns: [string, string][];
  primary_key: string[];
  foreign_keys: [string[], string, string[]][];
  unique_keys: string[][];
  keywords: string[];
  pkout?: boolean;
  pk_trashed?: boolean;
}

interface RdbDef {
  config: RdbConfig;
  tables: RdbTable[];
  hashPKey?: Record<string, string[]>;
  trash_pkeys?: string[];
  "skip-keywords"?: string[];
  index_elementFields?: Record<string, string[]>;
  index_attribFields?: Record<string, string[]>;
}

interface PoolClient {
  connect: Client["connect"];
  query: Client["query"];
  end: Client["end"];
  release: () => void;
  rowMode: number | boolean;
}

interface MemObj {
  entryId: string;
  mmjson: Record<string, Record<string, unknown[]>>;
  sql: Record<string, Record<string, unknown[]>>;
  inserts: [string, number[]][];
  updates: [string, [number, number, number[]][]][];
  deletes: [string, number[]][];
  newEntry?: boolean;
}

// CIF to SQL type conversion
const cif2sqlTypeConversion: Record<string, string> = {
  line_array: "text[]",
  int: "integer",
  positive_int: "integer",
  bigint: "bigint",
  float: "double precision",
  double: "double precision",
  date: "date",
  "yyyy-mm-dd": "date",
  timestamp: "timestamp with time zone",
  "yyyy-mm-dd:hh:mm": "timestamp with time zone",
  "yyyy-mm-dd:hh:mm-flex": "text",
  serial: "serial",
  boolean: "boolean",
};

const cif_kwTypes = new Set([
  "line",
  "text",
  "orcid_id",
  "pdbx_PDB_obsoleted_db_id",
  "pdbx_related_db_id",
  "exp_data_doi",
  "pdb_id",
  "author",
  "emd_id",
]);

function is_subset_of(list: string[], parent: string[]): boolean {
  const tmp = new Set(parent);
  return list.every((x) => tmp.has(x));
}

export function expand(
  rowCount: number,
  columnCount: number,
  startAt = 1
): string {
  let index = startAt;
  return Array(rowCount)
    .fill(0)
    .map(
      () =>
        `(${Array(columnCount)
          .fill(0)
          .map(() => `$${index++}`)
          .join(", ")})`
    )
    .join(", ");
}

export async function sendQuery(
  client: PoolClient | Client,
  query: string,
  values: unknown[],
  options?: unknown[]
): Promise<unknown> {
  if (options) query = pgformat(query, ...options);
  if (query.startsWith("select")) return client.query(query, values);
  values = values.map((v) => prepareValue(v));
  return client.query(query, values);
}

export class NativePSQLPool {
  private constring: string;
  private max: number;
  private clients: PoolClient[] = [];
  private pool: PoolClient[] = [];
  private queue: Deferred<PoolClient>[] = [];

  constructor(constring: string, max = 1) {
    this.constring = constring;
    this.max = max;
  }

  async connect(): Promise<PoolClient> {
    if (this.pool && this.pool.length) return this.pool.shift()!;
    if (this.clients.length < this.max) {
      const poolObj = this;
      const client = Client() as unknown as PoolClient;
      this.clients.push(client);
      client.release = function () {
        this.rowMode = false;
        if (poolObj.queue && poolObj.queue.length) {
          const waiter = poolObj.queue.shift();
          if (waiter && waiter.resolve) waiter.resolve(this);
        } else if (poolObj.pool) {
          poolObj.pool.push(this);
        }
      };
      await client.connect(this.constring);
      return client;
    }

    const waiter = new Deferred<PoolClient>();
    if (this.queue) this.queue.push(waiter);
    return waiter.promise;
  }

  async query(
    text: string,
    values?: unknown[],
    rowMode?: number | boolean
  ): Promise<unknown> {
    const client = await this.connect();
    if (!client) throw new Error("Failed to get database client");
    client.rowMode = rowMode || false;
    try {
      return await client.query(text, values);
    } finally {
      if (client.release) client.release();
    }
  }

  async end(): Promise<void> {
    this.pool = [];
    for (const client of this.clients) await client.end();
  }
}

// Legacy function for backward compatibility
export function nativePSQLpool(constring: string, max?: number): NativePSQLPool {
  return new NativePSQLPool(constring, max);
}

export function arrayModifier<T, U>(arr: T[], func: (item: T) => U): U[] {
  const temp: U[] = [];
  arr.forEach(function (i, idx) {
    temp[idx] = func(i);
  });
  return temp;
}

// rdb-worker stuff

export function deltaTable(
  table: string,
  memObj: MemObj,
  sql_PK: SqlPK,
  sql_struct: SqlStruct,
  __primaryKey__: string,
  sqlMode?: boolean
): void {
  const from_mmjson = memObj.mmjson[table] ;
  const from_sql = memObj.sql[table];

  if (table === "brief_summary") {
    if (from_sql && !sqlMode) from_sql.update_date[0] = null;
    if (!from_sql || (from_sql[__primaryKey__] as unknown[]).length === 0)
      memObj.newEntry = true;
  }

  const mmjson_hash: Record<string, number> = {};
  const sql_hash: Record<string, number> = {};
  let bad: boolean;

  const inserts: number[] = [];
  const updates: [number, number, number[]][] = [];
  const deletes: number[] = [];
  let r_m: number, r_s: number, m_v: unknown, s_v: unknown;
  const pk = sql_PK[table];
  let nor: number;
  let rpk: unknown[];
  const isdate = pk.map(() => false);

  nor = from_sql ? (from_sql[__primaryKey__] as unknown[]).length : 0;

  for (let r = 0; r < nor; r++) {
    rpk = [];
    bad = false;
    for (let k = 0; k < pk.length; k++) {
      if (!(pk[k][0] in from_sql)) {
        bad = true;
        break;
      }
      s_v = (from_sql[pk[k][0]] as unknown[])[r];
      if (s_v instanceof Date) {
        s_v = s_v.getTime();
        isdate[k] = true;
      }
      rpk.push(s_v);
    }

    if (!bad) sql_hash[JSON.stringify(rpk)] = r;
  }

  try {
    nor = from_mmjson
      ? ((from_mmjson[pk.length ? pk[0][0] : __primaryKey__] as unknown[]) || [])
          .length
      : 0;
  } catch {
    const vals = Object.values(from_mmjson || {});
    nor = vals.length && vals[0] !== undefined ? (vals[0] as unknown[]).length : 0;
  }

  for (let r = 0; r < nor; r++) {
    rpk = [];
    bad = false;
    for (let k = 0; k < pk.length; k++) {
      if (!(pk[k][1] in from_mmjson)) {
        bad = true;
        break;
      }
      m_v = (from_mmjson[pk[k][1]] as unknown[])[r];
      if (isdate[k]) {
        if (sqlMode) m_v = (m_v as Date).getTime();
        else m_v = new Date(m_v as string | number).getTime();
      }
      rpk.push(m_v);
    }
    if (!bad) mmjson_hash[JSON.stringify(rpk)] = r;
  }

  const tbl_struct = sql_struct[table];
  for (const r in mmjson_hash) {
    if (r in sql_hash) {
      r_m = mmjson_hash[r];
      r_s = sql_hash[r];
      const cols: number[] = [];
      for (let c = 0; c < tbl_struct.length; c++) {
        s_v =
          tbl_struct[c][0] in from_sql
            ? (from_sql[tbl_struct[c][0]] as unknown[])[r_s]
            : null;
        m_v =
          tbl_struct[c][1] in from_mmjson
            ? (from_mmjson[tbl_struct[c][1]] as unknown[])[r_m]
            : null;

        if (s_v instanceof Date) {
          if (!sqlMode)
            m_v = (from_mmjson[tbl_struct[c][1]] as Date[])[r_m] = new Date(
              m_v as string | number
            );
          if (s_v.getTime() !== (m_v as Date).getTime()) cols.push(c);
        } else if (Array.isArray(s_v)) {
          const m_arr = m_v as unknown[];
          if (
            (s_v.length || m_arr?.length) &&
            (s_v.length !== m_arr?.length ||
              !s_v.every((element, idx) => element === m_arr[idx]))
          ) {
            cols.push(c);
          }
        } else {
          if (s_v !== m_v) cols.push(c);
        }
      }
      if (cols.length) updates.push([sql_hash[r], mmjson_hash[r], cols]);
    } else {
      inserts.push(mmjson_hash[r]);
    }
  }
  for (const r in sql_hash) {
    if (!(r in mmjson_hash)) deletes.push(sql_hash[r]);
  }

  if (table === "brief_summary") {
    if (inserts.length) memObj.inserts.unshift([table, inserts]);
    if (updates.length) memObj.updates.unshift([table, updates]);
    if (deletes.length) memObj.deletes.unshift([table, deletes]);
  } else {
    if (inserts.length) memObj.inserts.push([table, inserts]);
    if (updates.length) memObj.updates.push([table, updates]);
    if (deletes.length) memObj.deletes.push([table, deletes]);
  }
}

export async function updateRDB(
  memObj: MemObj,
  setDate: Date | undefined,
  sql_PK: SqlPK,
  sql_struct: SqlStruct,
  mineSchema: string,
  __primaryKey__: string,
  dbconnect: NativePSQLPool
): Promise<void> {
  let client: PoolClient | undefined;

  try {
    if (
      memObj.inserts.length ||
      memObj.deletes.length ||
      memObj.updates.length
    ) {
      if (setDate !== undefined) {
        if (!memObj.newEntry) {
          const c = sql_struct.brief_summary
            .map((x) => x[0])
            .indexOf("update_date");
          let i: number;
          for (i = 0; i < memObj.updates.length; i++) {
            if (memObj.updates[i][0] === "brief_summary") {
              memObj.updates[i][1][0][2].push(c);
              break;
            }
          }
          if (i === memObj.updates.length)
            memObj.updates.push(["brief_summary", [[0, 0, [c]]]]);
        }
        (memObj.mmjson.brief_summary ).update_date[0] =
          setDate;
      }

      client = await dbconnect.connect();
      await client.query("BEGIN");
    }

    for (const ins of memObj.inserts) {
      const table = ins[0];
      const data = ins[1];
      const from_mmjson = memObj.mmjson[table] ;
      const values: unknown[] = [];
      const cols = sql_struct[table].filter((c) => c[1] in from_mmjson);

      const colnames = [__primaryKey__, ...cols.map((c) => c[1])];
      for (const rid of data) {
        values.push(memObj.entryId);
        cols.forEach((col) => values.push(from_mmjson[col[1]][rid]));
        if (values.length >= 30000) {
          const q = `insert into %I.%I (${colnames.map(() => "%I").join(",")}) values ${expand(values.length / colnames.length, colnames.length)}`;
          try {
            await sendQuery(client!, q, values, [mineSchema, table, ...colnames]);
          } catch (e) {
            console.log(memObj.entryId);
            console.error(e);
          }
          values.length = 0;
        }
      }
      if (values.length) {
        const q = `insert into %I.%I (${colnames.map(() => "%I").join(",")}) values ${expand(values.length / colnames.length, colnames.length)}`;
        try {
          await sendQuery(client!, q, values, [mineSchema, table, ...colnames]);
        } catch (e) {
          console.log(memObj.entryId);
          console.error(e);
        }
      }
    }

    for (const upd of memObj.updates) {
      const table = upd[0];
      const cols = sql_struct[table];
      const pk = sql_PK[table];
      const data = upd[1];
      const from_mmjson = memObj.mmjson[table] ;
      const from_sql = memObj.sql[table];

      for (const [rid, rid2, cidx] of data) {
        const keys: string[] = [];
        const values: unknown[] = [];
        for (const colIdx of cidx) {
          keys.push(cols[colIdx][0]);
          if (cols[colIdx][0] in from_mmjson)
            values.push(from_mmjson[cols[colIdx][0]][rid2]);
          else values.push(null);
        }
        let q: string | string[] = keys;
        const opts: unknown[] = [mineSchema, table, ...keys];
        const whereKeys: string[] = [__primaryKey__];
        values.push(memObj.entryId);
        for (const c of pk) {
          whereKeys.push(c[0]);
          values.push((from_sql[c[0]] as unknown[])[rid]);
        }
        const where = whereKeys
          .map((_, i) => "%I=$" + (i + opts.length - 1))
          .join(" AND ");
        opts.push(...whereKeys);
        if ((q as string[]).length === 1)
          q = `UPDATE %I.%I SET %I=$1 where ${where}`;
        else
          q = `UPDATE %I.%I SET (${(q as string[]).map(() => "%I").join(",")})=(${(q as string[]).map((_, i) => "$" + (i + 1)).join(",")}) where ${where}`;
        try {
          await sendQuery(client!, q, values, opts);
        } catch (e) {
          console.log(memObj.entryId);
          console.error(e);
        }
      }
    }

    for (const del of memObj.deletes) {
      const table = del[0];
      const pk = sql_PK[table];
      const data = del[1];
      const from_sql = memObj.sql[table];

      for (const rid of data) {
        const opts: unknown[] = [mineSchema, table, __primaryKey__];
        const values: unknown[] = [memObj.entryId];
        for (const c of pk) {
          opts.push(c[0]);
          values.push((from_sql[c[0]] as unknown[])[rid]);
        }
        const where = values.map((_, i) => "%I=$" + (i + 1)).join(" AND ");
        const q = "DELETE from %I.%I where " + where;
        try {
          await sendQuery(client!, q, values, opts);
        } catch (e) {
          console.log(memObj.entryId);
          console.error(e);
        }
      }
    }

    if (client) {
      await client.query("COMMIT");
      client.release();
    }
  } catch (e) {
    if (client) {
      await client.query("ROLLBACK");
      client.release();
    }
    throw e;
  }
}

// end rdb-worker stuff

export async function import_rdb_def(
  deffile: string,
  _config?: unknown
): Promise<RdbDef> {
  const rdb_def = yaml.load(
    await fsp.readFile(expandPath(deffile), "utf8")
  ) as RdbDef;
  rdb_def.tables = rdb_def.tables || [];

  const primaryKey = rdb_def.config.primaryKey;
  const primaryKeyFormat = rdb_def.config.primaryKeyFormat || "text";
  const typeRefRef: Record<string, string> = {};
  const tblRef: Record<string, RdbTable> = {};
  const typeRef: Record<string, Record<string, string>> = {};
  const mandatoryRef = new Set<string>();
  const type_overwrites = rdb_def.config.type_overwrites || {};

  const cifDicts = rdb_def.config.cifDicts || [];
  const skipKeywords = new Set(rdb_def["skip-keywords"] || []);

  for (const dict of cifDicts) {
    const parser = new CIFparser();
    await readlineGZ(expandPath(dict), function (line) {
      parser.parseLine(line, 0);
      if (parser.error) {
        console.error(`Error found in line ${parser.error[1]}:`);
        console.error("  ", parser.error[2]);
        console.log("  ", parser.error[0]);
        parser.error = null;
      }
    });

    const parserValues = Object.values(parser.data);
    if (!parserValues.length) continue;
    const doc = parserValues[0] as unknown as Record<string, Record<string, Record<string, unknown[]>>>;

    for (const i in doc) {
      if (!i.startsWith("save_") || i[5] === "_") continue;
      const catName = i.slice(5);
      if (catName === "datablock") continue;
      const tbl: RdbTable = {
        name: catName,
        columns: [[primaryKey, primaryKeyFormat]],
        primary_key: [
          primaryKey,
          ...(doc[i].category_key?.name || [])
            .filter((x: unknown) => (x as string).split(".")[1] !== primaryKey)
            .map((x: unknown) => (x as string).split(".")[1]),
        ],
        foreign_keys: [[[primaryKey], "brief_summary", [primaryKey]]],
        unique_keys: [],
        keywords: [],
      };
      rdb_def.tables.push(tbl);
      tblRef[catName] = tbl;
      typeRef[catName] = {};
      typeRef[catName][primaryKey] = primaryKeyFormat;
      mandatoryRef.add(`${catName}.${primaryKey}`);
    }

    for (const i in doc) {
      if (!i.startsWith("save__")) continue;

      let typecode: string | undefined;
      try {
        typecode = (doc[i].item_type?.code as string[])?.[0];
      } catch {
        continue;
      }
      if (!typecode) continue;
      typeRefRef[i.slice(6)] = typecode;
      if ("item_linked" in doc[i]) {
        const childNames = doc[i].item_linked?.child_name as string[] | undefined;
        childNames?.forEach((x: string) => (typeRefRef[x.slice(1)] = typecode!));
      }
    }

    for (const i in doc) {
      if (!i.startsWith("save__")) continue;
      const [catName, rawColName] = i.slice(6).split(".", 2);
      const colName = rawColName
        .replace(/\[/g, "")
        .replace(/\]/g, "")
        .replace(/\//g, "")
        .replace(/%/g, "");
      const tbl = tblRef[catName];

      if (colName !== primaryKey) {
        let typecode: string | undefined;
        if (!("item_type" in doc[i])) {
          try {
            typecode =
              typeRefRef[i.slice(6)] ||
              typeRefRef[(doc[i].item_linked?.parent_name as string[])?.[0]?.slice(1)];
          } catch {
            typecode = undefined;
          }
        } else {
          try {
            typecode = (doc[i].item_type?.code as string[])?.[0];
          } catch {
            typecode = undefined;
          }
        }

        let colType = cif2sqlTypeConversion[typecode || ""] || "text";
        if (`${catName}.${colName}` in type_overwrites)
          colType = type_overwrites[`${catName}.${colName}`];
        if (typeRef[catName][colName] === undefined) {
          tbl.columns.push([colName, colType]);
          if (
            cif_kwTypes.has(typecode || "") &&
            !doc[i].item_enumeration &&
            !skipKeywords.has(`${catName}.${colName}`)
          )
            tbl.keywords.push(colName);
        }
        typeRef[catName][colName] = colType;

        try {
          if ((doc[i].item?.mandatory_code as string[])?.[0] === "yes")
            mandatoryRef.add(`${catName}.${colName}`);
        } catch {
          // ignore
        }
      } else {
        tbl.pkout = true;
      }
    }

    if ("pdbx_item_linked_group_list" in doc) {
      const fgroups: Record<string, [string, string][]> = {};
      const ilgl = doc.pdbx_item_linked_group_list as unknown as Record<string, string[]>;
      for (let i = 0; i < ilgl.child_category_id.length; i++) {
        const id =
          ilgl.child_category_id[i] +
          ":" +
          ilgl.parent_category_id[i] +
          ":" +
          ilgl.link_group_id[i];
        if (!(id in fgroups)) fgroups[id] = [];
        fgroups[id].push([ilgl.child_name[i].slice(1), ilgl.parent_name[i].slice(1)]);
      }

      const fkey_cache = new Set<string>();

      for (const [, fkey] of Object.entries(fgroups)) {
        const key: [string[], string | null, string[]] = [
          [primaryKey],
          null,
          [primaryKey],
        ];
        const parentPK = new Set<string>();
        let child_tab = "";
        for (const part of fkey) {
          const [ct, rawChildCol] = part[0].split(".", 2);
          const [parent_tab, rawParentCol] = part[1].split(".", 2);
          child_tab = ct;
          const child_col = rawChildCol
            .replace(/\[/g, "")
            .replace(/\]/g, "")
            .replace(/\//g, "")
            .replace(/%/g, "");
          const parent_col = rawParentCol
            .replace(/\[/g, "")
            .replace(/\]/g, "")
            .replace(/\//g, "")
            .replace(/%/g, "");

          key[1] = parent_tab;

          if (child_col === primaryKey || parent_col === primaryKey) {
            if (parent_col !== primaryKey) parentPK.add(parent_col);
            continue;
          }
          key[0].push(child_col);
          key[2].push(parent_col);
        }
        if (key[1] == null || !key[0] || !key[2]) continue;

        const id1 = `${child_tab}(${[...key[0]].sort().join("|")})${key[1]}(${[...key[2]].sort().join("|")})`;
        const id2 = `${key[1]}(${[...key[2]].sort().join("|")})${child_tab}(${[...key[2]].sort().join("|")})`;
        if (fkey_cache.has(id1) || fkey_cache.has(id2)) continue;

        let ok = true;
        for (let i = 0; i < key[0].length; i++) {
          if (
            typeRef[child_tab] &&
            typeRef[key[1]] &&
            typeRef[child_tab][key[0][i]] !== typeRef[key[1]][key[2][i]]
          )
            ok = false;
          if (!mandatoryRef.has(`${child_tab}.${key[0][i]}`)) ok = false;
          if (!mandatoryRef.has(`${key[1]}.${key[2][i]}`)) ok = false;
        }

        if (
          (key[0].unique().length !== key[0].length ||
            key[2].unique().length !== key[2].length)
        )
          ok = false;
        if (
          !is_subset_of(
            tblRef[key[1]].primary_key.filter((x) => !parentPK.has(x)),
            key[2]
          )
        )
          ok = false;
        if (!ok) continue;

        if (!rdb_def.config.skip_foreign_keys) {
          fkey_cache.add(id1);
          tblRef[child_tab].foreign_keys.push(key as [string[], string, string[]]);
        }
        if (
          tblRef[key[1]].primary_key.length !== key[2].length &&
          tblRef[key[1]].unique_keys.filter(
            (x) => JSON.stringify(x) === JSON.stringify(key[2])
          ).length === 0
        )
          tblRef[key[1]].unique_keys.push(key[2]);
      }
    }
  }

  const hashPKey = rdb_def.hashPKey || {};
  for (const [k, v] of Object.entries(hashPKey)) {
    for (const field of v) {
      let idx = tblRef[k].columns.findIndex((x) => x[0] === field);
      if (idx !== -1) {
        tblRef[k].columns.splice(idx + 1, 0, ["_hash_" + field, "text"]);
        idx = tblRef[k].primary_key.findIndex((x) => x === field);
        if (idx !== -1) tblRef[k].primary_key[idx] = "_hash_" + field;
      }
    }
  }

  for (const k of rdb_def.trash_pkeys || []) tblRef[k].pk_trashed = true;

  delete rdb_def.hashPKey;
  delete rdb_def.config.cifDicts;

  return rdb_def;
}

export function init(
  rdb_setup: RdbDef
): [
  SqlTyping,
  SqlPK,
  SqlPKRef,
  SqlStruct,
  IndexFields,
  IndexFields,
  KeywordFields,
  number | undefined,
  string,
  string,
  Record<string, RdbTable>
] {
  const sql_typing: SqlTyping = {};
  const sql_PK: SqlPK = {};
  const sql_PKref: SqlPKRef = {};
  const sql_struct: SqlStruct = {};
  const keyword_fields: KeywordFields = {};
  let brief_summary_update_date_IDX: number | undefined;
  const rdbRef: Record<string, RdbTable> = {};
  const __primaryKey__ = rdb_setup.config.primaryKey;
  const mineSchema = rdb_setup.config.schema;

  for (let i = 0; i < rdb_setup.tables.length; i++) {
    rdbRef[rdb_setup.tables[i].name] = rdb_setup.tables[i];

    const pkref: Record<string, number> = (sql_PKref[rdb_setup.tables[i].name] = {});
    sql_PK[rdb_setup.tables[i].name] = [];

    for (let j = 0; j < rdb_setup.tables[i].primary_key.length; j++) {
      const cn = rdb_setup.tables[i].primary_key[j];
      if (cn !== __primaryKey__) {
        sql_PK[rdb_setup.tables[i].name].push([
          rdb_setup.tables[i].primary_key[j],
          cn,
        ]);
        sql_PKref[rdb_setup.tables[i].name][cn] = 1;
      }
    }

    sql_typing[rdb_setup.tables[i].name] = {};
    sql_struct[rdb_setup.tables[i].name] = [];
    for (let j = 0; j < rdb_setup.tables[i].columns.length; j++) {
      const cn = rdb_setup.tables[i].columns[j][0];
      let data_type: TypeConverter;
      if (
        rdb_setup.tables[i].columns[j][1] === "double precision" ||
        rdb_setup.tables[i].columns[j][1] === "real"
      ) {
        if (pkref[cn]) data_type = enforceFloatPK;
        else data_type = enforceFloat;
      } else if (rdb_setup.tables[i].columns[j][1] === "integer") {
        if (pkref[cn]) data_type = enforceIntegerPK;
        else data_type = enforceInteger;
      } else if (rdb_setup.tables[i].columns[j][1] === "bigint") {
        if (pkref[cn]) data_type = enforceBigIntegerPK;
        else data_type = enforceBigInteger;
      } else if (rdb_setup.tables[i].columns[j][1] === "serial") {
        data_type = enforceInteger;
      } else if (rdb_setup.tables[i].columns[j][1] === "bigserial") {
        data_type = enforceBigInteger;
      } else if (
        rdb_setup.tables[i].columns[j][1] === "text" ||
        rdb_setup.tables[i].columns[j][1] === "char(4)"
      ) {
        if (pkref[cn]) data_type = enforceStringPK;
        else data_type = enforceString;
      } else if (rdb_setup.tables[i].columns[j][1] === "citext") {
        data_type = enforceStringLC;
      } else if (rdb_setup.tables[i].columns[j][1] === "date") {
        data_type = enforceDate;
      } else if (
        rdb_setup.tables[i].columns[j][1] === "timestamp without time zone" ||
        rdb_setup.tables[i].columns[j][1] === "timestamp with time zone"
      ) {
        data_type = enforceTimestamp;
      } else if (rdb_setup.tables[i].columns[j][1] === "text[]") {
        data_type = enforceStringArray;
      } else if (rdb_setup.tables[i].columns[j][1] === "boolean") {
        data_type = enforceBoolean;
      } else {
        data_type = defaultType;
      }
      sql_typing[rdb_setup.tables[i].name][cn] = data_type;
      if (cn !== __primaryKey__)
        sql_struct[rdb_setup.tables[i].name].push([
          rdb_setup.tables[i].columns[j][0],
          cn,
        ]);
    }

    keyword_fields[rdb_setup.tables[i].name] = {};
    if (rdb_setup.tables[i].keywords) {
      for (let j = 0; j < rdb_setup.tables[i].keywords.length; j++)
        keyword_fields[rdb_setup.tables[i].name][
          rdb_setup.tables[i].keywords[j]
        ] = true;
    }
  }

  const index_elementFields: IndexFields = {};
  for (const e in rdb_setup.index_elementFields) {
    index_elementFields[e] = {};
    for (let i = 0; i < rdb_setup.index_elementFields[e].length; i++)
      index_elementFields[e][rdb_setup.index_elementFields[e][i]] = true;
  }

  const index_attribFields: IndexFields = {};
  for (const e in rdb_setup.index_attribFields) {
    index_attribFields[e] = {};
    for (let i = 0; i < rdb_setup.index_attribFields[e].length; i++)
      index_attribFields[e][rdb_setup.index_attribFields[e][i]] = true;
  }

  if (sql_struct.brief_summary) {
    for (let i = 0; i < sql_struct.brief_summary.length; i++) {
      if (sql_struct.brief_summary[i][0] === "update_date") {
        brief_summary_update_date_IDX = i;
        break;
      }
    }
  }

  return [
    sql_typing,
    sql_PK,
    sql_PKref,
    sql_struct,
    index_elementFields,
    index_attribFields,
    keyword_fields,
    brief_summary_update_date_IDX,
    mineSchema,
    __primaryKey__,
    rdbRef,
  ];
}

export function gen_docid(inp: string): number {
  inp = inp.ljust(4, " ").rjust(8, "0");
  const components: number[] = [];
  for (let i = 0; i < 8; i++) {
    if (inp[i] === " ") components.push(36);
    else components.push(parseInt(inp[i], 36));
  }
  return (
    (components[0] << 64) |
    (components[1] << 48) |
    (components[2] << 32) |
    components[3] |
    (components[4] << 24) |
    (components[5] << 16) |
    (components[6] << 8) |
    components[7]
  );
}

export function mmjsonAt<T>(
  table: Record<string, T[]> | undefined,
  get_field: string,
  cond_field: string,
  cond_val: unknown
): T[] {
  const out: T[] = [];
  if (!table || !(get_field in table) || !(cond_field in table)) return out;
  for (let i = 0; i < table[get_field].length; i++) {
    if (table[cond_field][i] === cond_val) out.push(table[get_field][i]);
  }
  return out;
}

export function mmjsonAt_IC<T>(
  table: Record<string, T[]> | undefined,
  get_field: string,
  cond_field: string,
  cond_val: string
): T[] {
  cond_val = cond_val.toLowerCase();
  const out: T[] = [];
  if (!table || !(get_field in table) || !(cond_field in table)) return out;
  for (let i = 0; i < table[get_field].length; i++) {
    if (String(table[cond_field][i]).toLowerCase() === cond_val) {
      out.push(table[get_field][i]);
    }
  }
  return out;
}

export function mmjsonGet<T>(
  table: Record<string, T[]> | undefined,
  get_field: string,
  n?: number
): T | T[] | null {
  if (table && get_field in table) {
    if (n !== undefined) return table[get_field][n];
    else return table[get_field];
  }
  if (n !== undefined) return null;
  else return [];
}

// sha256 hash...
export function hex_sha256(s: string): string {
  return crypto.createHash("sha256").update(s).digest("hex");
}

export function getObjectValue<T>(
  object: Record<string, unknown>,
  field: string,
  defaultValue: T
): T {
  if (field in object) return object[field] as T;
  else return defaultValue;
}

export function str(inp: unknown): string {
  return inp + "";
}

export function cleanArray<T>(array: T[]): T[] {
  let result = Array.from(new Set(array));
  let idx = result.indexOf(null as unknown as T);
  if (idx !== -1) result.splice(idx, 1);
  idx = result.indexOf(undefined as unknown as T);
  if (idx !== -1) result.splice(idx, 1);
  idx = result.indexOf("" as unknown as T);
  if (idx !== -1) result.splice(idx, 1);
  result.sort();
  return result;
}

export function removeNull<T>(array: (T | null | undefined)[]): T[] {
  return array.filter((val): val is T => val != null);
}

function enforceStringPK(i: unknown): string {
  if (i == null) return "";
  if (Array.isArray(i)) return i.join("-");
  return i + "";
}

function enforceString(i: unknown): string | null {
  if (i == null) return null;
  if (Array.isArray(i)) return i.join("-");
  return i + "";
}

function enforceStringLC(i: unknown): string | null {
  if (i == null) return null;
  if (Array.isArray(i)) return i.join("-").toLowerCase();
  return (i + "").toLowerCase();
}

function enforceInteger(i: unknown): number | null {
  if (i == null) return null;
  const tmp = parseInt(String(i));
  return isNaN(tmp) ? null : tmp;
}

function enforceBoolean(i: unknown): boolean | null {
  if (i === true || i === 1 || (i + "").toLowerCase() === "true") return true;
  if (i === false || i === 0 || (i + "").toLowerCase() === "false") return false;
  return null;
}

function enforceIntegerPK(i: unknown): number {
  if (i == null) return 0;
  else {
    if (isNaN(parseInt(String(i)))) console.log(i);
    return parseInt(String(i));
  }
}

function enforceBigInteger(i: unknown): bigint | null {
  if (i == null) return null;
  try {
    return BigInt(i as string | number | bigint);
  } catch {
    return null;
  }
}

function enforceBigIntegerPK(i: unknown): bigint {
  if (i == null) return BigInt(0);
  else return BigInt(i as string | number | bigint);
}

function defaultType(i: unknown): unknown {
  return i;
}

function enforceFloat(i: unknown): number | null {
  if (i == null) return null;
  const tmp = parseFloat(parseFloat(String(i)).toPrecision(15));
  return isNaN(tmp) ? null : tmp;
}

function enforceFloatPK(i: unknown): number {
  if (i == null) return 0.0;
  else return parseFloat(parseFloat(String(i)).toPrecision(15));
}

function enforceDate(i: unknown): string | null {
  if (i) {
    const parts = String(i).split("-");
    if (parts[0].length < 4) {
      if (parseInt(parts[0]) < 50) parts[0] = "20" + parts[0];
      else parts[0] = "19" + parts[0];
    }
    if (parts[1]?.length < 2) parts[1] = "0" + parts[1];
    if (parts[2]?.length < 2) parts[2] = "0" + parts[2];
    return parts.join("-");
  }
  return i as string | null;
}

function enforceTimestamp(i: unknown): unknown {
  if (i == null) return null;
  return i;
}

export function enforceStringArray(col: unknown): (string | null)[] {
  if (!Array.isArray(col)) col = [col];
  return (col as unknown[]).map((x) => (x ? x + "" : null));
}

// pg util

export const prep_defaults = { parseInputDatesAsUTC: false };

function prepareValue(val: unknown, seen?: unknown[]): unknown {
  if (val instanceof Buffer) {
    return val;
  }
  if (ArrayBuffer.isView(val)) {
    const buf = Buffer.from(
      val.buffer as ArrayBuffer,
      val.byteOffset,
      val.byteLength
    );
    if (buf.length === val.byteLength) {
      return buf;
    }
    return buf.slice(val.byteOffset, val.byteOffset + val.byteLength);
  }
  if (val instanceof Date) {
    if (prep_defaults.parseInputDatesAsUTC) {
      return dateToStringUTC(val);
    } else {
      return dateToString(val);
    }
  }
  if (Array.isArray(val)) {
    return arrayString(val);
  }
  if (val === null || typeof val === "undefined") {
    return null;
  }
  if (typeof val === "object") {
    return prepareObject(val, seen);
  }
  return String(val);
}

function pad(number: number | string, digits: number): string {
  let num = "" + number;
  while (num.length < digits) {
    num = "0" + num;
  }
  return num;
}

function dateToStringUTC(date: Date): string {
  let year = date.getUTCFullYear();
  const isBCYear = year < 1;
  if (isBCYear) year = Math.abs(year) + 1;

  let ret =
    pad(year, 4) +
    "-" +
    pad(date.getUTCMonth() + 1, 2) +
    "-" +
    pad(date.getUTCDate(), 2) +
    "T" +
    pad(date.getUTCHours(), 2) +
    ":" +
    pad(date.getUTCMinutes(), 2) +
    ":" +
    pad(date.getUTCSeconds(), 2) +
    "." +
    pad(date.getUTCMilliseconds(), 3);

  ret += "+00:00";
  if (isBCYear) ret += " BC";
  return ret;
}

function dateToString(date: Date): string {
  let offset = -date.getTimezoneOffset();

  let year = date.getFullYear();
  const isBCYear = year < 1;
  if (isBCYear) year = Math.abs(year) + 1;

  let ret =
    pad(year, 4) +
    "-" +
    pad(date.getMonth() + 1, 2) +
    "-" +
    pad(date.getDate(), 2) +
    "T" +
    pad(date.getHours(), 2) +
    ":" +
    pad(date.getMinutes(), 2) +
    ":" +
    pad(date.getSeconds(), 2) +
    "." +
    pad(date.getMilliseconds(), 3);

  if (offset < 0) {
    ret += "-";
    offset *= -1;
  } else {
    ret += "+";
  }

  ret += pad(Math.floor(offset / 60), 2) + ":" + pad(offset % 60, 2);
  if (isBCYear) ret += " BC";
  return ret;
}

function escapeElement(elementRepresentation: string): string {
  const escaped = elementRepresentation
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"');
  return '"' + escaped + '"';
}

function arrayString(val: unknown[]): string {
  let result = "{";
  for (let i = 0; i < val.length; i++) {
    if (i > 0) {
      result = result + ",";
    }
    if (val[i] === null || typeof val[i] === "undefined") {
      result = result + "NULL";
    } else if (Array.isArray(val[i])) {
      result = result + arrayString(val[i] as unknown[]);
    } else if (val[i] instanceof Buffer) {
      result += "\\\\x" + (val[i] as Buffer).toString("hex");
    } else {
      result += escapeElement(prepareValue(val[i]) as string);
    }
  }
  result = result + "}";
  return result;
}

interface ToPostgresObject {
  toPostgres: (prepareValue: (val: unknown, seen?: unknown[]) => unknown) => unknown;
}

function prepareObject(val: object, seen?: unknown[]): unknown {
  if (val && typeof (val as ToPostgresObject).toPostgres === "function") {
    seen = seen || [];
    if (seen.indexOf(val) !== -1) {
      throw new Error(
        'circular reference detected while preparing "' + val + '" for query'
      );
    }
    seen.push(val);

    return prepareValue((val as ToPostgresObject).toPostgres(prepareValue), seen);
  }
  return JSON.stringify(val);
}

// end pg util
