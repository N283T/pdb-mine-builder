export interface Column {
  name: string;
  type: string;
  description: string;
}

export interface Table {
  name: string;
  columns: Column[];
}
