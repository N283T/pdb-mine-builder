import type {ReactNode} from 'react';
import React, {useState, useEffect, useMemo, useCallback} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import type {Column, Table} from '@site/src/types/schema';

interface Schema {
  schema: string;
  primaryKey: string;
  tables: Table[];
}

interface SearchResult {
  schema: string;
  table: string;
  column: Column;
}

// Display priority order (lower = higher priority).
// Keep in sync with SIDEBAR_POSITIONS in scripts/generate_rdb_docs.py.
const SCHEMA_PRIORITY: Record<string, number> = {
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

function SchemaCheckboxes({
  schemas,
  enabled,
  onToggle,
}: {
  schemas: Schema[];
  enabled: Set<string>;
  onToggle: (name: string) => void;
}) {
  return (
    <div className="schema-search__checkboxes">
      {schemas.map((s) => (
        <label key={s.schema} className="schema-search__checkbox">
          <input
            type="checkbox"
            checked={enabled.has(s.schema)}
            onChange={() => onToggle(s.schema)}
          />
          <span>{s.schema}</span>
          <span className="schema-search__table-count">({s.tables.length})</span>
        </label>
      ))}
    </div>
  );
}

function SearchResults({query, schemas}: {query: string; schemas: Schema[]}) {
  const baseUrl = useBaseUrl('/docs/database/');
  const lowerQuery = query.toLowerCase();

  const results = useMemo(() => {
    if (!lowerQuery || lowerQuery.length < 2) return [];
    const matches: SearchResult[] = [];
    for (const schema of schemas) {
      for (const table of schema.tables) {
        const tableMatch = table.name.toLowerCase().includes(lowerQuery);
        for (const col of table.columns) {
          if (
            tableMatch ||
            col.name.toLowerCase().includes(lowerQuery) ||
            col.type.toLowerCase().includes(lowerQuery) ||
            col.description.toLowerCase().includes(lowerQuery)
          ) {
            matches.push({schema: schema.schema, table: table.name, column: col});
          }
        }
      }
    }
    return matches;
  }, [schemas, lowerQuery]);

  if (!lowerQuery || lowerQuery.length < 2) {
    return <p className="schema-search__hint">Type at least 2 characters to search.</p>;
  }

  if (results.length === 0) {
    return <p>No results for "{query}".</p>;
  }

  // Group by schema.table, sorted by schema priority
  const grouped = new Map<string, {schema: string; table: string; columns: Column[]}>();
  for (const r of results) {
    const key = `${r.schema}.${r.table}`;
    const existing = grouped.get(key);
    if (existing) {
      existing.columns.push(r.column);
    } else {
      grouped.set(key, {schema: r.schema, table: r.table, columns: [r.column]});
    }
  }

  const sortedGroups = Array.from(grouped.values()).sort((a, b) => {
    const pa = SCHEMA_PRIORITY[a.schema] ?? 99;
    const pb = SCHEMA_PRIORITY[b.schema] ?? 99;
    if (pa !== pb) return pa - pb;
    return a.table.localeCompare(b.table);
  });

  return (
    <div>
      <p className="schema-search__count">
        {results.length} columns in {grouped.size} tables
      </p>
      {sortedGroups.map(({schema, table, columns}) => (
        <div key={`${schema}.${table}`} className="schema-search__group">
          <h3>
            <Link to={`${baseUrl}${schema}#${table}`}>
              {schema}.{table}
            </Link>
          </h3>
          <table>
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col) => (
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
    </div>
  );
}

function getInitialQuery(): string {
  if (typeof window === 'undefined') return '';
  const params = new URLSearchParams(window.location.search);
  return params.get('q') || '';
}

export default function SchemaSearchPage(): ReactNode {
  const [query, setQuery] = useState(getInitialQuery);
  const [allSchemas, setAllSchemas] = useState<Schema[]>([]);
  const [enabledSchemas, setEnabledSchemas] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dataUrl = useBaseUrl('/data/allSchemas.json');

  // Sync query to URL parameter
  useEffect(() => {
    const url = new URL(window.location.href);
    if (query) {
      url.searchParams.set('q', query);
    } else {
      url.searchParams.delete('q');
    }
    window.history.replaceState({}, '', url.toString());
  }, [query]);

  useEffect(() => {
    fetch(dataUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: Schema[]) => {
        const sorted = [...data].sort(
          (a, b) => (SCHEMA_PRIORITY[a.schema] ?? 99) - (SCHEMA_PRIORITY[b.schema] ?? 99),
        );
        setAllSchemas(sorted);
        setEnabledSchemas(new Set(sorted.map((s) => s.schema)));
      })
      .catch((err) => {
        console.error('Failed to load schema data:', err);
        setError(err instanceof Error ? err.message : 'Failed to load schema data.');
      })
      .finally(() => setLoading(false));
  }, [dataUrl]);

  const handleToggle = useCallback(
    (name: string) => {
      setEnabledSchemas((prev) => {
        const next = new Set(prev);
        if (next.has(name)) {
          next.delete(name);
        } else {
          next.add(name);
        }
        return next;
      });
    },
    [],
  );

  const filteredSchemas = useMemo(
    () => allSchemas.filter((s) => enabledSchemas.has(s.schema)),
    [allSchemas, enabledSchemas],
  );

  const totalTables = allSchemas.reduce((sum, s) => sum + s.tables.length, 0);
  const totalColumns = allSchemas.reduce(
    (sum, s) => sum + s.tables.reduce((ts, t) => ts + t.columns.length, 0),
    0,
  );

  return (
    <Layout title="Schema Search" description="Search across all database schemas">
      <main className="container margin-vert--lg">
        <h1>Schema Search</h1>
        <p>
          Search across {allSchemas.length} schemas, {totalTables} tables,{' '}
          {totalColumns} columns.
        </p>
        <div className="schema-search__bar">
          <input
            type="text"
            placeholder="Search tables, columns, types, descriptions..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="schema-filter__input"
            autoFocus
          />
        </div>
        {!loading && !error && (
          <SchemaCheckboxes
            schemas={allSchemas}
            enabled={enabledSchemas}
            onToggle={handleToggle}
          />
        )}
        {loading && <p>Loading schema data...</p>}
        {error && <p className="schema-search__error">Error: {error}</p>}
        {!loading && !error && <SearchResults query={query} schemas={filteredSchemas} />}
      </main>
    </Layout>
  );
}
