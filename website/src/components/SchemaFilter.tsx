import React, {useState, useMemo} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

interface Column {
  name: string;
  type: string;
  description: string;
}

interface Table {
  name: string;
  columns: Column[];
}

interface SchemaFilterProps {
  tables: Table[];
}

function SchemaFilterInner({tables}: SchemaFilterProps) {
  const [query, setQuery] = useState('');
  const lowerQuery = query.toLowerCase();

  const filtered = useMemo(() => {
    if (!lowerQuery) return tables;
    return tables
      .map((table) => {
        const tableMatch = table.name.toLowerCase().includes(lowerQuery);
        if (tableMatch) return table;
        const matchedCols = table.columns.filter(
          (col) =>
            col.name.toLowerCase().includes(lowerQuery) ||
            col.type.toLowerCase().includes(lowerQuery) ||
            col.description.toLowerCase().includes(lowerQuery),
        );
        if (matchedCols.length === 0) return null;
        return {...table, columns: matchedCols};
      })
      .filter(Boolean) as Table[];
  }, [tables, lowerQuery]);

  const totalCols = filtered.reduce((sum, t) => sum + t.columns.length, 0);

  return (
    <div>
      <div className="schema-filter">
        <input
          type="text"
          placeholder="Filter tables and columns..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="schema-filter__input"
        />
        {lowerQuery && (
          <span className="schema-filter__count">
            {filtered.length} tables, {totalCols} columns
          </span>
        )}
      </div>
      {filtered.map((table) => (
        <div key={table.name}>
          <h2 id={table.name}>{table.name}</h2>
          <table>
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {table.columns.map((col) => (
                <tr key={col.name}>
                  <td>{col.name}</td>
                  <td>{col.type}</td>
                  <td>{col.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
      {filtered.length === 0 && lowerQuery && (
        <p>No tables or columns match "{query}".</p>
      )}
    </div>
  );
}

export default function SchemaFilter(props: SchemaFilterProps) {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <SchemaFilterInner {...props} />}
    </BrowserOnly>
  );
}
