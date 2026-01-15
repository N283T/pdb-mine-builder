/* eslint-disable @typescript-eslint/no-explicit-any */
import cluster from "cluster";
import type { Worker } from "cluster";
import * as path from "path";
import * as url from "url";

import {
  nativePSQLpool,
  NativePSQLPool,
  arrayModifier,
  init as rdbInit,
} from "./rdb-helper.js";
import { Deferred } from "./general.js";
import type { Config } from "../types/index.js";

const __filename = url.fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const scriptStartDate = new Date();

// Type definitions
interface RdbTable {
  name: string;
  columns: [string, string][];
  primary_key: string[];
  foreign_keys?: [string[], string, string[]][];
  unique_keys?: string[][];
  indexes?: (string | string[])[];
  pk_trashed?: boolean;
}

export interface RdbDef {
  config: {
    primaryKey: string;
    schema: string;
    [key: string]: unknown;
  };
  tables: RdbTable[];
}

type SqlTyping = Record<string, Record<string, (value: unknown) => unknown>>;
type SqlPK = Record<string, [string, string][]>;
type SqlPKRef = Record<string, Record<string, number>>;
type SqlStruct = Record<string, [string, string][]>;
type KeywordFields = Record<string, Record<string, boolean>>;
type IndexFields = Record<string, Record<string, boolean>>;

export interface JobPayload {
  entryId: string;
  [key: string]: unknown;
}

export interface JobContainer {
  workers: Worker[];
  rdb_def: RdbDef;
  jobs: JobPayload[];
  entries_processed: string[];
  scandone: boolean;
  jobId: number;
  config: Config;
  waiter: Deferred<void>;
  totalJobs?: number;
}

interface FkRef {
  [key: string]: {
    [constr: string]: [string, string[]];
  };
}

interface QueryResult {
  [column: string]: unknown[];
}

// Module-level variables
let sql_typing: SqlTyping;
let sql_PK: SqlPK;
let sql_PKref: SqlPKRef;
let sql_struct: SqlStruct;
let index_elementFields: IndexFields;
let index_attribFields: IndexFields;
let keyword_fields: KeywordFields;
let brief_summary_update_date_IDX: number | undefined;
let rdbRef: Record<string, RdbTable>;
let mineSchema: string;
let __primaryKey__: string;

const jobcontainer: JobContainer[] = [];

// HELPER FUNCTIONS

interface PoolClient {
  query: (text: string, values?: unknown[]) => Promise<QueryResult>;
  release: () => void;
}

// code to upgrade the RDB schema
async function upgradeSchema(config: Config, usePool?: NativePSQLPool): Promise<void> {
  const fkbad = new Set<string>();
  const fkref: FkRef = {};
  const nukedtables = new Set<string>();

  const pool = usePool || new NativePSQLPool(config.rdb.constring, 1);
  const client = (await pool.connect()) as PoolClient;

  let tmp1: QueryResult;
  let tmp2: Set<string>;
  const queries: string[] = [];

  tmp1 = (await client.query(
    "SELECT ccu.table_name as tablename, tc.table_name as reftable, tc.constraint_name FROM information_schema.table_constraints AS tc JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.constraint_schema = '" +
      mineSchema.replace(/"/g, "") +
      "'"
  )) as QueryResult;
  const FKTblIds: Record<string, [string, string][]> = {};
  const tableNames = tmp1.tablename as string[];
  for (let i = 0; i < tableNames.length; i++) {
    const tblName = tableNames[i];
    if (!(tblName in FKTblIds)) FKTblIds[tblName] = [];
    FKTblIds[tblName].push([
      tmp1.reftable[i] as string,
      tmp1.constraint_name[i] as string,
    ]);
  }

  tmp1 = (await client.query(
    `SELECT table_name FROM information_schema.tables WHERE table_schema = '${mineSchema.replace(/"/g, "")}'`
  )) as QueryResult;
  if ((tmp1.table_name as string[]).length === 0)
    queries.push(`CREATE SCHEMA IF NOT EXISTS ${mineSchema};`);

  tmp2 = new Set();
  for (let i = 0; i < (tmp1.table_name as string[]).length; i++) {
    tmp2.add(tmp1.table_name[i] as string);
  }

  const deletedConstraints = new Set<string>();
  for (const i of tmp2) {
    if (!Object.prototype.hasOwnProperty.call(sql_PK, i))
      await upgradeSchema_deleteTable(queries, i, FKTblIds, deletedConstraints);
  }

  for (const i in sql_PK) {
    if (!tmp2.has(i)) upgradeSchema_createTable(queries, i);
    else await upgradeSchema_checkTable(queries, i, client, fkbad, fkref, nukedtables);
  }

  const fk_tableRedo = new Set<string>();
  const fkKill: Record<string, string> = {};
  for (const e of fkbad) {
    if (!(e in fkref)) continue;
    Object.entries(fkref[e]).forEach((x) => {
      fkKill[x[0]] = x[1][0];
    });
    Object.values(fkref[e]).forEach((x) => {
      x[1].forEach((t) => fk_tableRedo.add(t));
    });
  }
  for (const [constr, tableName] of Object.entries(fkKill))
    queries.unshift(
      `ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${constr}" CASCADE;`
    );

  // add the foreign key stuff later to ensure that all tables have been defined...
  const q1: string[] = [];
  const q2: string[] = [];
  for (let i = 0; i < queries.length; i++) {
    if (
      queries[i].indexOf(' ADD FOREIGN KEY ("') !== -1 &&
      queries[i].indexOf('") REFERENCES ') !== -1
    )
      q2.push(queries[i]);
    else q1.push(queries[i]);
  }

  if (queries.length) {
    await client.query("BEGIN");
    for (const q of q1) {
      await client.query(q);
    }
    for (const q of q2) {
      await client.query(q);
    }
    await client.query("COMMIT");
  }

  const queries2: string[] = [];
  for (const e of fk_tableRedo) await fkTable(queries2, e, client, {});
  if (queries2.length) {
    await client.query("BEGIN");
    for (const q of queries2) {
      await client.query(q);
    }
    await client.query("COMMIT");
  }

  const queries3: string[] = [];
  for (const e of nukedtables) upgradeSchema_createTable(queries3, e);

  if (queries3.length) {
    await client.query("BEGIN");
    for (const q of queries3) {
      await client.query(q);
    }
    await client.query("COMMIT");
  }

  client.release();
  if (!usePool) pool.end();
}

// create a new table
function upgradeSchema_createTable(queries: string[], tableName: string): void {
  if (tableName === "brief_summary_with_hit_score") return;

  let query = "";
  let tmp1: string;
  let tmp2: string;

  query += `CREATE TABLE ${mineSchema}."${tableName}" (\n`;

  for (const column of rdbRef[tableName].columns)
    query += `  "${column[0]}" ${column[1]},\n`;

  // unique
  for (const key of rdbRef[tableName].unique_keys || []) {
    tmp1 = arrayModifier(key, (j) => `"${j}"`).join(",");
    query += `  UNIQUE (${tmp1}),\n`;
  }

  // primary
  tmp1 = arrayModifier(
    rdbRef[tableName].pk_trashed ? [] : rdbRef[tableName].primary_key,
    (i) => `"${i}"`
  ).join(",");
  if (tmp1.length) query += `  PRIMARY KEY (${tmp1})\n);`;
  else query = query.slice(0, -2) + "\n);";
  queries.push(query);

  for (const key of rdbRef[tableName].foreign_keys || []) {
    tmp1 = key[0].map((j) => `"${j}"`).join(",");
    tmp2 = key[2].map((j) => `"${j}"`).join(",");

    if (
      tmp1 === '"' + __primaryKey__ + '"' &&
      tmp2 === '"' + __primaryKey__ + '"' &&
      key[1] === "brief_summary"
    )
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${key[1]}" (${tmp2}) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;`
      );
    else
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${tmp1}) REFERENCES ${mineSchema}."${key[1]}" (${tmp2}) DEFERRABLE INITIALLY DEFERRED;`
      );
  }

  for (let index of rdbRef[tableName].indexes || []) {
    if (typeof index === "string") index = [index];
    const columns = (index as string[]).map((x) => `"${x}"`).join(",");
    queries.push(`create index on ${mineSchema}."${tableName}" (${columns});`);
  }
}

async function upgradeSchema_deleteTable(
  queries: string[],
  tableName: string,
  FKTblIds: Record<string, [string, string][]>,
  deletedConstraints: Set<string>
): Promise<void> {
  if (tableName === "brief_summary_with_hit_score") return;

  // delete foreign keys that refer to the to-be-deleted table
  for (const [reftable, constraint_name] of FKTblIds[tableName] || []) {
    if (
      deletedConstraints.has(constraint_name) ||
      deletedConstraints.has("table:" + reftable)
    )
      continue;
    queries.push(
      `ALTER TABLE ${mineSchema}."${reftable}" DROP CONSTRAINT "${constraint_name}";`
    );
    deletedConstraints.add(constraint_name);
  }

  deletedConstraints.add("table:" + tableName);
  queries.push(`DROP TABLE ${mineSchema}."${tableName}";`);
}

function bakaCopySortString(arr: unknown[]): string {
  return JSON.stringify(JSON.parse(JSON.stringify(arr)).sort());
}

// modify an existing table
async function upgradeSchema_checkTable(
  queries: string[],
  tableName: string,
  client: PoolClient,
  fkbad: Set<string>,
  fkref: FkRef,
  nukedtables: Set<string>
): Promise<void> {
  if (tableName === "brief_summary_with_hit_score") return;

  const columns: Record<string, [string, string]> = {};
  let tmp1: QueryResult;
  let tmp2: string;
  let tmp3: Set<string>;
  let tmp4: Record<string, number>;
  let tmp5: Record<string, number>;
  let data_type: string;

  // identify modified columns
  for (let i = 0; i < rdbRef[tableName].columns.length; i++)
    columns[rdbRef[tableName].columns[i][0]] = rdbRef[tableName].columns[i];

  // primary key part 1
  const pkey_tmp = (await client.query(
    "SELECT tc.constraint_name, array_agg(cast(kcu.column_name as text)) FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name WHERE tc.table_name = $1 AND tc.table_schema = '" +
      mineSchema.replace(/"/g, "") +
      "' AND tc.constraint_type = 'PRIMARY KEY' group by tc.constraint_name;",
    [tableName]
  )) as QueryResult;
  let pname: string | null;
  let pkeys: string[];

  if ((pkey_tmp.constraint_name as string[]).length === 0) {
    pname = null;
    pkeys = [];
  } else {
    pname = pkey_tmp.constraint_name[0] as string;
    pkeys = pkey_tmp.array_agg[0] as string[];
  }
  if (
    bakaCopySortString(pkeys) !==
    bakaCopySortString(rdbRef[tableName].pk_trashed ? [] : rdbRef[tableName].primary_key)
  ) {
    if (pname) {
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${pname}";`
      );
    }
  }

  tmp1 = (await client.query(
    "select column_name, data_type, column_default from INFORMATION_SCHEMA.COLUMNS where table_schema='" +
      mineSchema.replace(/"/g, "") +
      "' and table_name=$1;",
    [tableName]
  )) as QueryResult;

  tmp3 = new Set();
  for (let i = 0; i < (tmp1.column_name as string[]).length; i++) {
    if (
      tmp1.data_type[i] === "integer" &&
      tmp1.column_default[i] ===
        "nextval('" +
          (mineSchema.replace(/"/g, "").toLowerCase() !== "public"
            ? mineSchema.replace(/"/g, "").toLowerCase() + "."
            : "") +
          tableName.toLowerCase() +
          "_" +
          (tmp1.column_name[i] as string).toLowerCase() +
          "_seq'::regclass)"
    )
      tmp1.data_type[i] = "serial";

    const colName = tmp1.column_name[i] as string;
    if (!Object.prototype.hasOwnProperty.call(columns, colName)) {
      if (
        (tmp1.column_name[i] as string).startsWith("_") &&
        Object.prototype.hasOwnProperty.call(
          columns,
          (tmp1.column_name[i] as string).substring(1)
        )
      ) {
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" RENAME COLUMN "${tmp1.column_name[i]}" TO "${(tmp1.column_name[i] as string).substring(1)}";`
        );
        tmp3.add((tmp1.column_name[i] as string).substring(1));
        continue;
      }
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" DROP COLUMN "${tmp1.column_name[i]}";`
      );
      continue;
    }

    tmp3.add(tmp1.column_name[i] as string);

    data_type = columns[tmp1.column_name[i] as string][1];

    // figure out the correct array type
    if (tmp1.data_type[i] === "ARRAY") {
      tmp2 = (
        (await client.query(
          "select udt_name from INFORMATION_SCHEMA.COLUMNS where table_schema='" +
            mineSchema.replace(/"/g, "") +
            "' and table_name=$1 and column_name=$2;",
          [tableName, tmp1.column_name[i]]
        )) as QueryResult
      ).udt_name[0] as string;
      if (tmp2 === "_text") tmp1.data_type[i] = "text[]";
      else if (tmp2 === "_int4") tmp1.data_type[i] = "integer[]";
      else {
        console.error(
          "Unknown format",
          tableName,
          tmp1.column_name[i],
          tmp1.data_type[i],
          tmp2
        );
        process.exit();
      }
    }

    // figure out the char length
    if (data_type === "character") {
      tmp2 = String(
        (
          (await client.query(
            "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_schema='" +
              mineSchema.replace(/"/g, "") +
              "' and table_name=$1 and column_name=$2;",
            [tableName, tmp1.column_name[i]]
          )) as QueryResult
        ).character_maximum_length[0]
      );
      data_type = "char(" + tmp2 + ")";
    }

    // if the types don't match -> modify the type
    if (data_type !== tmp1.data_type[i]) {
      if (rdbRef[tableName].primary_key.indexOf(tmp1.column_name[i] as string) !== -1) {
        queries.push(`DROP TABLE ${mineSchema}."${tableName}";`);
        nukedtables.add(tableName);
        return;
      } else {
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${tmp1.column_name[i]}" DROP DEFAULT;`
        );
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${tmp1.column_name[i]}" TYPE ${data_type} USING NULL;`
        );
        fkbad.add(`${tableName}.${tmp1.column_name[i]}`);
      }
    }
  }

  for (const i in columns) {
    if (!tmp3.has(i)) {
      data_type = columns[i][1];
      if (rdbRef[tableName].primary_key.indexOf(i) !== -1) {
        let tmp4Default = "''";
        if (data_type === "integer") tmp4Default = "0";
        if (data_type === "real") tmp4Default = "0.0";
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ADD COLUMN "${i}" ${data_type} DEFAULT ${tmp4Default};`
        );
      } else
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ADD COLUMN "${i}" ${data_type};`
        );
    }
  }

  // primary keys part 2
  if (
    bakaCopySortString(pkeys) !==
    bakaCopySortString(rdbRef[tableName].pk_trashed ? [] : rdbRef[tableName].primary_key)
  ) {
    const pkey_tmp2 = arrayModifier(
      rdbRef[tableName].pk_trashed ? [] : rdbRef[tableName].primary_key,
      (j) => `"${j}"`
    ).join(",");
    if (pkey_tmp2.length)
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" ADD PRIMARY KEY (${pkey_tmp2});`
      );
    for (let i = 0; i < pkeys.length; i++)
      if (
        rdbRef[tableName].primary_key.indexOf(pkeys[i]) === -1 &&
        pkeys[i] in columns
      )
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${pkeys[i]}" DROP NOT NULL;`
        );
  }

  // unique restraints...
  tmp1 = (await client.query(
    "SELECT tc.constraint_name, array_agg(cast(kcu.column_name as text)) FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name WHERE tc.table_name = $1 AND tc.table_schema = '" +
      mineSchema.replace(/"/g, "") +
      "' AND tc.constraint_type = 'UNIQUE' group by tc.constraint_name;",
    [tableName]
  )) as QueryResult;

  tmp4 = {};
  for (let i = 0; i < (tmp1.constraint_name as string[]).length; i++)
    tmp4[bakaCopySortString(tmp1.array_agg[i] as unknown[])] = i;

  tmp5 = {};
  if (rdbRef[tableName].unique_keys) {
    for (let i = 0; i < rdbRef[tableName].unique_keys!.length; i++)
      tmp5[bakaCopySortString(rdbRef[tableName].unique_keys![i])] = i;
  }

  for (const i in tmp4) {
    if (!Object.prototype.hasOwnProperty.call(tmp5, i) && tmp4[i] !== undefined) {
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${tmp1.constraint_name[tmp4[i]]}" CASCADE;`
      );
    }
  }

  let n = Object.keys(tmp4).length;

  for (const i in tmp5) {
    if (!Object.prototype.hasOwnProperty.call(tmp4, i) && tmp5[i] !== undefined) {
      pkeys = rdbRef[tableName].unique_keys![tmp5[i]];

      const ukeyTmp = arrayModifier(pkeys, (j) => `"${j}"`).join(",");
      const ukeyName = tableName + "_" + n + "_ukey";
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" ADD CONSTRAINT "${ukeyName}" UNIQUE (${ukeyTmp});`
      );

      for (let j = 0; j < pkeys.length; j++)
        if (rdbRef[tableName].primary_key.indexOf(pkeys[j]) === -1)
          queries.push(
            `ALTER TABLE ${mineSchema}."${tableName}" ALTER COLUMN "${pkeys[j]}" DROP NOT NULL;`
          );
      n++;
    }
  }

  // foreign keys
  await fkTable(queries, tableName, client, fkref);
}

async function fkTable(
  queries: string[],
  tableName: string,
  client: PoolClient,
  fkref: FkRef
): Promise<void> {
  if (tableName === "brief_summary_with_hit_score") return;

  let tmp1: QueryResult;
  let tmp2: string[];
  let tmp3: string[];
  let tmp4: Record<string, number>;
  let tmp5: Record<string, number>;

  tmp1 = (await client.query(
    `select array_agg(att2.attname) as "columns", cl.relname as "foreign_table", array_agg(att.attname) as "foreign_columns", con.conname from (select unnest(con1.conkey) as "parent", unnest(con1.confkey) as "child", con1.confrelid, con1.conrelid, relname as "child_table", con1.conname from pg_class cl join pg_namespace ns on cl.relnamespace = ns.oid join pg_constraint con1 on con1.conrelid = cl.oid where ns.nspname = '${mineSchema.replace(/"/g, "")}' and con1.contype = 'f' and relname = $1) con join pg_attribute att on att.attrelid = con.confrelid and att.attnum = con.child join pg_class cl on cl.oid = con.confrelid join pg_attribute att2 on att2.attrelid = con.conrelid and att2.attnum = con.parent group by con.confrelid, cl.relname, con.conname;`,
    [tableName]
  )) as QueryResult;

  const fkrefHandler = function (
    tN: string,
    cN: string,
    tNalt: string,
    constr: string,
    primTN: string
  ): void {
    if (fkref === undefined) return;
    if (!(`${tN}.${cN}` in fkref)) fkref[`${tN}.${cN}`] = {};
    if (!(constr in fkref[`${tN}.${cN}`]))
      fkref[`${tN}.${cN}`][constr] = [primTN, []];
    fkref[`${tN}.${cN}`][constr][1].push(tN, tNalt);
  };

  tmp4 = {};
  for (let i = 0; i < (tmp1.conname as string[]).length; i++) {
    tmp2 = (tmp1.columns[i] as string).substring(1, (tmp1.columns[i] as string).length - 1).split(",");
    tmp3 = (tmp1.foreign_columns[i] as string)
      .substring(1, (tmp1.foreign_columns[i] as string).length - 1)
      .split(",");
    tmp2.forEach((x) => {
      fkrefHandler(tableName, x, tmp1.foreign_table[i] as string, tmp1.conname[i] as string, tableName);
    });
    tmp3.forEach((x) => {
      fkrefHandler(
        tmp1.foreign_table[i] as string,
        x,
        tableName,
        tmp1.conname[i] as string,
        tableName
      );
    });
    tmp4[bakaCopySortString(tmp2) + tmp1.foreign_table[i] + bakaCopySortString(tmp3)] = i;
  }

  tmp5 = {};
  if (rdbRef[tableName].foreign_keys) {
    for (let i = 0; i < rdbRef[tableName].foreign_keys!.length; i++) {
      tmp5[
        bakaCopySortString(rdbRef[tableName].foreign_keys![i][0]) +
          rdbRef[tableName].foreign_keys![i][1] +
          bakaCopySortString(rdbRef[tableName].foreign_keys![i][2])
      ] = i;
    }
  }

  for (const i in tmp4) {
    if (!Object.prototype.hasOwnProperty.call(tmp5, i))
      queries.push(
        `ALTER TABLE ${mineSchema}."${tableName}" DROP CONSTRAINT "${tmp1.conname[tmp4[i]]}" CASCADE;`
      );
  }

  for (const i in tmp5) {
    if (!Object.prototype.hasOwnProperty.call(tmp4, i)) {
      const fkCols = arrayModifier(
        rdbRef[tableName].foreign_keys![tmp5[i]][0],
        (j) => `"${j}"`
      ).join(",");
      const fkRefCols = arrayModifier(
        rdbRef[tableName].foreign_keys![tmp5[i]][2],
        (j) => `"${j}"`
      ).join(",");

      if (
        fkCols === '"' + __primaryKey__ + '"' &&
        fkRefCols === '"' + __primaryKey__ + '"' &&
        rdbRef[tableName].foreign_keys![tmp5[i]][1] === "brief_summary"
      )
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${fkCols}) REFERENCES ${mineSchema}."${rdbRef[tableName].foreign_keys![tmp5[i]][1]}" (${fkRefCols}) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;`
        );
      else
        queries.push(
          `ALTER TABLE ${mineSchema}."${tableName}" ADD FOREIGN KEY (${fkCols}) REFERENCES ${mineSchema}."${rdbRef[tableName].foreign_keys![tmp5[i]][1]}" (${fkRefCols}) DEFERRABLE INITIALLY DEFERRED;`
        );
    }
  }
}

// プログレスバー表示関数
function showProgress(jc: JobContainer): void {
  const total = jc.totalJobs || jc.jobs.length + jc.entries_processed.length;
  const done = jc.entries_processed.length;
  const percent = total > 0 ? Math.floor((done / total) * 100) : 0;
  const barWidth = 30;
  const filled = Math.floor((barWidth * done) / total);
  const bar =
    "=".repeat(filled) + ">" + " ".repeat(Math.max(0, barWidth - filled - 1));
  process.stdout.write(`\r[${bar}] ${percent}% (${done}/${total})`);
}

export async function schemaPrep(
  config: Config,
  rdb_def: RdbDef,
  dbconnect?: NativePSQLPool
): Promise<void> {
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
  if ((config.argv as Record<string, unknown>)["skip-schema"])
    console.warn("Skipping schema upgrade for", mineSchema);
  else await upgradeSchema(config, dbconnect);
}

export async function init(config: Config, rdb_def: RdbDef): Promise<JobContainer> {
  await schemaPrep(config, rdb_def);

  const workers: Worker[] = [];
  const obj: JobContainer = {
    workers,
    rdb_def,
    jobs: [],
    entries_processed: [],
    scandone: false,
    jobId: jobcontainer.length,
    config,
    waiter: new Deferred<void>(),
  };
  jobcontainer.push(obj);

  (cluster as any).setupMaster({
    exec: path.join(__dirname, "rdb-worker.js"),
    args: [String(obj.jobId)],
  });

  for (let i = 0; i < config.rdb.nworkers; i++) {
    const worker = cluster.fork();
    worker.on("message", respond2Worker);
    worker.on("error", console.error);
    workers.push(worker);
    worker.on("exit", async function (this: Worker) {
      obj.workers.splice(obj.workers.indexOf(this), 1);
      if (
        obj.workers.length === 0 &&
        !("test-entry" in (config.argv as Record<string, unknown>))
      ) {
        // 進捗表示をクリアして改行
        process.stdout.write("\r" + " ".repeat(50) + "\r");
        await removeObsolete(obj);
        obj.waiter.resolve();
      }
    });
  }

  return obj;
}

/**
 * Mark job container as done scanning and set totalJobs for accurate progress display.
 * Call this after all jobs have been pushed to the queue.
 */
export function setScandone(jc: JobContainer): void {
  jc.totalJobs = jc.jobs.length;
  jc.scandone = true;
}

interface WorkerMessage {
  cmd: string;
  jobId: number;
  entryId?: string;
}

interface WorkerResponse {
  cmd: string;
  payload?: unknown;
}

function respond2Worker(this: Worker, msg: WorkerMessage): void {
  if (msg.cmd === "init") {
    const jc = jobcontainer[msg.jobId];
    this.send({
      cmd: "init",
      payload: { rdb_def: jc.rdb_def, scriptStartDate, config: jc.config },
    } as WorkerResponse);
    return;
  }
  if (msg.cmd === "getjob") {
    const jc = jobcontainer[msg.jobId];
    if (!jc) {
      console.log("unknown jobId", msg.jobId);
      process.exit();
    }
    if (msg.entryId) {
      jc.entries_processed.push(msg.entryId);
      delete msg.entryId;
      showProgress(jc);
    }
    if (jc.jobs.length === 0) {
      if (jc.scandone) {
        // 全ジョブ数が確定した時点で設定
        if (!jc.totalJobs) {
          jc.totalJobs = jc.entries_processed.length;
          showProgress(jc);
        }
        this.send({ cmd: "done" } as WorkerResponse);
        return;
      } else {
        const worker = this;
        setImmediate(() => {
          respond2Worker.apply(worker, [msg]);
        });
        return;
      }
    } else {
      this.send({ cmd: "job", payload: jc.jobs.shift() } as WorkerResponse);
    }
  }
}

export async function removeObsolete(jc: JobContainer): Promise<void> {
  const pool = new NativePSQLPool(jc.config.rdb.constring, 1);

  const in_pdb = new Set(jc.entries_processed);
  const queryResult = (await pool.query(
    `select ${__primaryKey__} from ${mineSchema}.brief_summary`
  )) as QueryResult;
  const remove_ids = (queryResult[__primaryKey__] as string[]).filter(
    (x) => !in_pdb.has(x)
  );
  if (remove_ids.length) {
    const stuff = remove_ids.map((_, i) => `$${i + 1}`).join(",");
    await pool.query(
      `delete from ${mineSchema}.brief_summary where ${__primaryKey__} in (${stuff})`,
      remove_ids
    );
  }

  pool.end();
}
