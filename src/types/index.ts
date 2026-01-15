/*
  Copyright (C) 2021 Gert-Jan Bekker
  TypeScript type definitions for mine2updater
*/

// Config types
export interface PipelineConfig {
  definition?: string;
  dataFolder?: string;
  pattern?: string;
  method?: string;
  loaderModule?: string;
  [key: string]: unknown;
}

export interface Config {
  rdb: {
    nworkers: number;
    constring: string;
  };
  pipelines: Record<string, PipelineConfig>;
  defines: Record<string, string>;
  argv: Record<string, unknown>;
}

// mmJSON data types
export type MMJsonValue = string | number | null;

export interface MMJsonCategory {
  [field: string]: MMJsonValue[];
}

export interface MMJsonDatablock {
  [category: string]: MMJsonCategory;
}

export interface MMJsonData {
  [datablock: string]: MMJsonDatablock;
}

// CIF parsing types
export interface CIFCategory {
  [field: string]: (string | null)[];
}

export interface CIFDatablock {
  [category: string]: CIFCategory;
}

export interface CIFData {
  [datablock: string]: CIFDatablock;
}

// RDB types
export interface TableColumn {
  name: string;
  type: string;
  pk?: boolean;
  fk?: string;
  index?: boolean;
  default?: unknown;
}

export interface TableDef {
  name: string;
  columns: TableColumn[];
  primaryKey?: string[];
  foreignKeys?: Array<{
    columns: string[];
    references: {
      table: string;
      columns: string[];
    };
  }>;
}

export interface RdbConfig {
  primaryKey: string;
  schema: string;
  delete_on_update?: boolean;
  [key: string]: unknown;
}

export interface RdbDef {
  config: RdbConfig;
  tables: TableDef[];
}

// Walk options
export interface WalkOptions {
  stats?: boolean;
}

export interface WalkFile {
  path: string;
  name: string;
  stats?: import("fs").Stats;
}

export interface WalkContainer {
  pattern_handler: (path: string, container: WalkContainer) => void;
}

// Chemical compound types
export interface ChemCompAtom {
  atom_id: string[];
  type_symbol: string[];
  charge: (number | null)[];
  model_Cartn_x: (number | null)[];
  model_Cartn_y: (number | null)[];
  model_Cartn_z: (number | null)[];
  pdbx_model_Cartn_x_ideal: (number | null)[];
  pdbx_model_Cartn_y_ideal: (number | null)[];
  pdbx_model_Cartn_z_ideal: (number | null)[];
}

export interface ChemCompBond {
  atom_id_1: string[];
  atom_id_2: string[];
  value_order: string[];
}

export interface MemObj {
  entryId?: string;
  mmjson?: MMJsonDatablock;
  mdl?: string;
  mdl_noH?: string;
  mdl_Natoms?: number;
  [key: string]: unknown;
}

// Exec command options
export interface ExecCommandOptions {
  input?: string;
  encoding?: BufferEncoding;
  stdio?: string;
  extended?: boolean;
  error?: Error | null;
  stderr?: string;
}

// Pipeline related types
export interface JobPayload {
  entryId: string;
  path: string;
  pathPlus?: string;
  [key: string]: unknown;
}

export interface PipelineMemObj {
  entryId: string;
  mmjson: MMJsonDatablock;
  mdl?: string;
  mdl_noH?: string;
  mdl_Natoms?: number;
  [key: string]: unknown;
}

// Global config extension
declare global {
  var config: Config;
  var moduleFolder: string;
  var pipelineFolder: string;
}

export {};
