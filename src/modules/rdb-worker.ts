/* eslint-disable @typescript-eslint/no-explicit-any */
import cluster from "cluster";
import pgformat from "pg-format";

import {
  deltaTable,
  updateRDB,
  cleanArray,
  nativePSQLpool,
  NativePSQLPool,
  init as rdbInit,
} from "./rdb-helper.js";
import type { Config } from "../types/index.js";

// Type definitions
type TypeConverter = (value: unknown, isPK?: boolean) => unknown;
type SqlTyping = Record<string, Record<string, TypeConverter>>;
type SqlPK = Record<string, [string, string][]>;
type SqlPKRef = Record<string, Record<string, number>>;
type SqlStruct = Record<string, [string, string][]>;
type KeywordFields = Record<string, Record<string, boolean>>;
type IndexFields = Record<string, Record<string, boolean>>;

interface RdbTable {
  name: string;
  columns: [string, string][];
  primary_key: string[];
  foreign_keys?: [string[], string, string[]][];
  unique_keys?: string[][];
  pk_trashed?: boolean;
}

interface RdbDef {
  config: {
    primaryKey: string;
    schema: string;
    [key: string]: unknown;
  };
  tables: RdbTable[];
}

interface JobPayload {
  entryId: string;
  mtime?: Date;
  [key: string]: unknown;
}

interface MemObj {
  entryId: string;
  mmjson: Record<string, Record<string, unknown[]>>;
  sql: Record<string, Record<string, unknown[]>>;
  updates: [string, [number, number, number[]][]][];
  inserts: [string, number[]][];
  deletes: [string, number[]][];
  newEntry: boolean;
  mtime?: Date;
  payload: JobPayload;
  optionalFailRetry?: string[];
}

interface Pipeline {
  load_data: (payload: JobPayload, config: Config) => Promise<Record<string, Record<string, Record<string, unknown[]>>> | null>;
  brief_summary: (memObj: MemObj, primaryKey: string, config: Config) => Promise<void>;
}

// Module-level variables
let rdb_def: RdbDef;
let scriptStartDate: Date;
let config: Config;
let pipeline: Pipeline;
let sql_typing: SqlTyping;
let sql_PK: SqlPK;
let sql_PKref: SqlPKRef;
let sql_struct: SqlStruct;
let index_elementFields: IndexFields;
let index_attribFields: IndexFields;
let keyword_fields: KeywordFields;
let brief_summary_update_date_IDX: number | undefined;
let mineSchema: string;
let __primaryKey__: string;
let rdbRef: Record<string, RdbTable>;
let dbconnect: NativePSQLPool;

const jobId = process.argv[2];

async function processEntry(payload: JobPayload): Promise<void> {
  let jso: Record<string, Record<string, Record<string, unknown[]>>> | null | undefined;
  if (!payload.entryId) jso = await pipeline.load_data(payload, config);

  const memObj: MemObj = {
    entryId: payload.entryId,
    mmjson: {},
    sql: {},
    updates: [],
    inserts: [],
    deletes: [],
    newEntry: false,
    mtime: payload.mtime,
    payload,
  };

  const tableNames = Object.keys(sql_typing);
  let results = dbconnect.query(
    tableNames
      .map((table) =>
        pgformat(
          "select * from %I.%I where %I=%L;",
          mineSchema,
          table,
          __primaryKey__,
          memObj.entryId
        )
      )
      .join(" ")
  ) as Promise<Record<string, unknown[]>[]>;

  if (jso === undefined) jso = await pipeline.load_data(payload, config);
  if (jso == null) {
    getJob();
    return;
  }

  for (const [, data] of Object.entries(jso)) {
    for (const [tableName, table] of Object.entries(data)) {
      memObj.mmjson[tableName] = table;

      const tbl_nfo = sql_typing[tableName];
      if (!tbl_nfo) continue; // skip unknown tables...

      // tableが空オブジェクトの場合はスキップ
      const tableValues = Object.values(table);
      if (!tableValues.length || tableValues[0] === undefined) continue;
      const nor = (tableValues[0] as unknown[]).length;
      for (let [columnName, column] of Object.entries(table)) {
        const c_ = columnName.replace(/\[/g, "").replace(/\]/g, "");
        if (columnName !== c_) {
          table[c_] = column;
          delete table[columnName];
          columnName = c_;
        }
        const col_nfo = tbl_nfo[columnName];
        if (!col_nfo) continue; // skip unknown columns
        for (let r = 0; r < nor; r++) {
          (column as unknown[])[r] = col_nfo((column as unknown[])[r]);
        }
      }
    }
  }

  const resolvedResults = await results;
  resolvedResults.forEach((table, idx) => {
    memObj.sql[tableNames[idx]] = table;
  });
  await pipeline.brief_summary(memObj, __primaryKey__, config);
  processKeywords(memObj);

  Object.keys(sql_typing).forEach((e) =>
    deltaTable(e, memObj as any, sql_PK, sql_struct, __primaryKey__)
  );

  try {
    await updateRDB(
      memObj as any,
      scriptStartDate,
      sql_PK,
      sql_struct,
      mineSchema,
      __primaryKey__,
      dbconnect
    );
  } catch (e) {
    if (memObj.optionalFailRetry !== undefined && memObj.optionalFailRetry.length) {
      memObj.optionalFailRetry.forEach((x) => delete memObj.mmjson[x]);
      memObj.updates = [];
      memObj.inserts = [];
      memObj.deletes = [];
      Object.keys(sql_typing).forEach((e) =>
        deltaTable(e, memObj as any, sql_PK, sql_struct, __primaryKey__)
      );
      await updateRDB(
        memObj as any,
        undefined,
        sql_PK,
        sql_struct,
        mineSchema,
        __primaryKey__,
        dbconnect
      );
    } else throw e;
  }

  getJob(memObj.entryId);
}

function processKeywords(memObj: MemObj): void {
  const tbl = memObj.mmjson.brief_summary as Record<string, unknown[]> & {
    keywords?: unknown[];
  };

  tbl.keywords = tbl.keywords || [];

  // extract additional data from mmjson
  for (const t in memObj.mmjson) {
    if (t === "brief_summary" || !(t in sql_PK)) continue;
    const cat = memObj.mmjson[t];
    const tbl_nfo = sql_typing[t];
    const pkref = sql_PKref[t];

    // catが空オブジェクトの場合はスキップ
    const catValues = Object.values(cat);
    if (!catValues.length || catValues[0] === undefined) continue;
    const nor = (catValues[0] as unknown[]).length;

    if (t in keyword_fields) {
      const eF = keyword_fields[t];
      for (const c in cat) {
        if (c in eF) tbl.keywords = tbl.keywords!.concat(cat[c] as unknown[]);
      }
    }

    const pk = sql_PK[t];
    for (let c = 0; c < pk.length; c++) {
      // work around very crappy xsd file messing up rdb...
      if (!(pk[c][1] in cat)) {
        cat[pk[c][1]] = [];
        const col_nfo = tbl_nfo[pk[c][1]](null, true);
        for (let r = 0; r < nor; r++) (cat[pk[c][1]] as unknown[]).push(col_nfo);
      }
    }
  }

  // clean keywords
  tbl.keywords = cleanArray((tbl.keywords as string[]).unique());
  tbl.keywords = (tbl.keywords as string[]).map((x) =>
    x.toLowerCase().replace(/\n/g, " ")
  );
  tbl.keywords = (tbl.keywords as string[]).filter(
    (x) => isNaN(Number(x) - parseFloat(x)) || x.length > 4
  ); // filter out numbers, unless it's a large number
  tbl.keywords = (tbl.keywords as string[]).unique();
  (tbl.keywords as string[]).sort();
  tbl.keywords = [tbl.keywords];
}

interface MainMessage {
  cmd: string;
  payload?: unknown;
}

async function respond2Main(msg: MainMessage): Promise<void> {
  if (msg.cmd === "init") {
    init(msg.payload as { rdb_def: RdbDef; scriptStartDate: Date; config: Config });
  } else if (msg.cmd === "done") {
    process.exit();
  } else if (msg.cmd === "job") {
    try {
      await processEntry(msg.payload as JobPayload);
    } catch (e) {
      console.error(`Error processing ${(msg.payload as JobPayload).entryId}...`, e);
    }
  }
}

function getJob(entryId?: string): void {
  if (process.send) process.send({ cmd: "getjob", jobId, entryId });
}

async function init(payload: {
  rdb_def: RdbDef;
  scriptStartDate: Date;
  config: Config;
}): Promise<void> {
  rdb_def = payload.rdb_def;
  scriptStartDate = payload.scriptStartDate;
  config = payload.config;
  global.config = config;
  global.moduleFolder = (config as any).moduleFolder;
  global.pipelineFolder = (config as any).pipelineFolder;

  pipeline = await import((config as any).pipeline);

  [
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
  ] = rdbInit(rdb_def as any);

  dbconnect = new NativePSQLPool(config.rdb.constring, 1);
  getJob();
}

if (!cluster.isPrimary) {
  if (process.on) process.on("message", respond2Main);
  if (process.send) process.send({ cmd: "init", jobId });
}

// update brief_summary table stuff

// initialize schema data structure
