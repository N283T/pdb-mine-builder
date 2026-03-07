export interface Column {
  name: string;
  type: string;
  description: string;
}

export interface Table {
  name: string;
  columns: Column[];
}

export interface Schema {
  schema: string;
  primaryKey: string;
  tables: Table[];
}

// Display priority order (lower = higher priority).
// Keep in sync with SIDEBAR_POSITIONS in scripts/generate_schema_docs.py.
export const SCHEMA_PRIORITY: Record<string, number> = {
  pdbj: 0,
  cc: 1,
  ccmodel: 2,
  prd: 3,
  prd_family: 4,
  vrpt: 5,
  contacts: 6,
  emdb: 7,
  ihm: 8,
};
