import type {ReactNode} from 'react';
import React, {useState, useEffect, useMemo, useCallback, useRef} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import BrowserOnly from '@docusaurus/BrowserOnly';
import type {Column, Table, Schema} from '@site/src/types/schema';
import {SCHEMA_PRIORITY} from '@site/src/types/schema';

interface TableEntry {
  schema: string;
  table: string;
  columns: Set<string>;
}

/** Maximum number of tables that can be selected. */
const MAX_TABLES = 8;

/** Columns that are too generic to indicate a meaningful relationship. */
const GENERIC_COLUMNS = new Set([
  'id', 'type', 'name', 'details', 'ordinal', 'method', 'description',
  'date', 'code', 'source', 'value', 'title', 'text',
]);

/** Preset examples for quick exploration. */
const PRESETS: {label: string; description: string; tables: string[]}[] = [
  {
    label: 'cc: Chemical Components',
    description: 'Component dictionary with atoms, bonds, and descriptors',
    tables: ['cc.brief_summary', 'cc.chem_comp', 'cc.chem_comp_atom', 'cc.chem_comp_bond'],
  },
  {
    label: 'pdbj: Entity Relations',
    description: 'Entity data with polymer sequences and naming',
    tables: ['pdbj.entity', 'pdbj.entity_poly', 'pdbj.entity_poly_seq', 'pdbj.entity_keywords'],
  },
  {
    label: 'pdbj: Structure & Refinement',
    description: 'Crystal structure, symmetry, and refinement data',
    tables: ['pdbj.struct', 'pdbj.cell', 'pdbj.symmetry', 'pdbj.refine', 'pdbj.exptl'],
  },
  {
    label: 'pdbj: Citations',
    description: 'Publication information with authors',
    tables: ['pdbj.citation', 'pdbj.citation_author', 'pdbj.citation_editor'],
  },
  {
    label: 'prd: BIRD Reference',
    description: 'Biologically Interesting Reference Dictionary',
    tables: ['prd.brief_summary', 'prd.pdbx_reference_molecule', 'prd.pdbx_reference_molecule_details', 'prd.pdbx_reference_molecule_synonyms'],
  },
];


function useSchemaData() {
  const [schemas, setSchemas] = useState<Schema[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dataUrl = useBaseUrl('/data/allSchemas.json');

  useEffect(() => {
    fetch(dataUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: Schema[]) => setSchemas(data))
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load data.'))
      .finally(() => setLoading(false));
  }, [dataUrl]);

  return {schemas, loading, error};
}

/** Schema tab selector + table list within that schema. */
function SchemaTablePicker({
  schemas,
  allTables,
  selected,
  onAdd,
  onRemove,
  onClearAll,
}: {
  schemas: Schema[];
  allTables: TableEntry[];
  selected: string[];
  onAdd: (key: string) => void;
  onRemove: (key: string) => void;
  onClearAll: () => void;
}) {
  const [activeSchema, setActiveSchema] = useState<string | null>(null);
  const [tableFilter, setTableFilter] = useState('');
  const selectedSet = useMemo(() => new Set(selected), [selected]);

  const sortedSchemas = useMemo(
    () =>
      [...schemas].sort(
        (a, b) =>
          (SCHEMA_PRIORITY[a.schema] ?? 99) - (SCHEMA_PRIORITY[b.schema] ?? 99),
      ),
    [schemas],
  );

  const filteredTables = useMemo(() => {
    if (!activeSchema) return [];
    const lower = tableFilter.toLowerCase();
    return allTables
      .filter(
        (t) =>
          t.schema === activeSchema &&
          (!lower || t.table.toLowerCase().includes(lower)),
      )
      .sort((a, b) => a.table.localeCompare(b.table));
  }, [allTables, activeSchema, tableFilter]);

  return (
    <div className="table-relations__picker">
      {/* Selected tags */}
      {selected.length > 0 && (
        <div className="table-relations__tags">
          {selected.map((key) => (
            <span key={key} className="table-relations__tag">
              {key}
              <button
                onClick={() => onRemove(key)}
                className="table-relations__tag-remove"
                aria-label={`Remove ${key}`}
              >
                ×
              </button>
            </span>
          ))}
          <button
            onClick={onClearAll}
            className="table-relations__clear-btn"
          >
            Clear all
          </button>
        </div>
      )}

      {/* Schema tabs */}
      <div className="table-relations__schema-tabs">
        {sortedSchemas.map((s) => (
          <button
            key={s.schema}
            onClick={() => {
              setActiveSchema(activeSchema === s.schema ? null : s.schema);
              setTableFilter('');
            }}
            className={`table-relations__schema-tab ${activeSchema === s.schema ? 'active' : ''}`}
          >
            {s.schema}
            <span className="table-relations__col-count">({s.tables.length})</span>
          </button>
        ))}
      </div>

      {/* Table list for active schema */}
      {activeSchema && (
        <div className="table-relations__table-list">
          <input
            type="text"
            placeholder={`Filter tables in ${activeSchema}...`}
            value={tableFilter}
            onChange={(e) => setTableFilter(e.target.value)}
            className="schema-filter__input table-relations__table-filter"
          />
          <div className="table-relations__table-grid">
            {filteredTables.map((t) => {
              const key = `${t.schema}.${t.table}`;
              const isSelected = selectedSet.has(key);
              const disabled = !isSelected && selected.length >= MAX_TABLES;
              return (
                <button
                  key={key}
                  onClick={() => (isSelected ? onRemove(key) : onAdd(key))}
                  className={`table-relations__table-btn ${isSelected ? 'selected' : ''}`}
                  disabled={disabled}
                  title={`${t.columns.size} columns`}
                >
                  {t.table}
                </button>
              );
            })}
          </div>
          {selected.length >= MAX_TABLES && (
            <p className="table-relations__limit-msg">
              Maximum {MAX_TABLES} tables selected. Remove a table to add another.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

interface SharedColumn {
  name: string;
  tables: string[];
  type: string;
}

function SharedColumnsView({
  selected,
  tableMap,
  columnDetails,
}: {
  selected: string[];
  tableMap: Map<string, TableEntry>;
  columnDetails: Map<string, Map<string, Column>>;
}) {
  const baseUrl = useBaseUrl('/docs/database/');

  const shared = useMemo(() => {
    if (selected.length < 2) return [];

    const colCount = new Map<string, string[]>();
    const colType = new Map<string, string>();

    for (const key of selected) {
      const entry = tableMap.get(key);
      if (!entry) continue;
      const details = columnDetails.get(key);
      if (!details) continue;

      for (const colName of entry.columns) {
        if (GENERIC_COLUMNS.has(colName)) continue;
        const existing = colCount.get(colName) || [];
        existing.push(key);
        colCount.set(colName, existing);

        if (!colType.has(colName)) {
          const col = details.get(colName);
          if (col) colType.set(colName, col.type);
        }
      }
    }

    const result: SharedColumn[] = [];
    for (const [name, tables] of colCount) {
      if (tables.length >= 2) {
        result.push({name, tables, type: colType.get(name) || ''});
      }
    }
    result.sort((a, b) => b.tables.length - a.tables.length || a.name.localeCompare(b.name));
    return result;
  }, [selected, tableMap, columnDetails]);

  if (selected.length < 2) return null;

  if (shared.length === 0) {
    return <p>No shared columns found between the selected tables (excluding generic columns).</p>;
  }

  return (
    <div>
      <h3>Shared Columns</h3>
      <p className="schema-search__count">
        {shared.length} shared columns across {selected.length} tables
      </p>
      <table className="table-relations__results">
        <thead>
          <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Shared By</th>
          </tr>
        </thead>
        <tbody>
          {shared.map((col) => (
            <tr key={col.name}>
              <td><code>{col.name}</code></td>
              <td>{col.type}</td>
              <td>
                {col.tables.map((key, i) => {
                  const [schema, table] = key.split('.', 2);
                  return (
                    <span key={key}>
                      {i > 0 && ', '}
                      <Link to={`${baseUrl}${schema}#${table}`}>{key}</Link>
                    </span>
                  );
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** Mermaid ER diagram helpers. */
const MERMAID_TYPE_MAP: Record<string, string> = {
  text: 'text', integer: 'int', bigint: 'bigint',
  'double precision': 'float', real: 'float', float: 'float',
  date: 'date', 'timestamp without time zone': 'timestamp', boolean: 'bool',
};

function mermaidType(t: string): string {
  return MERMAID_TYPE_MAP[t] || t.replace(/\s+/g, '_');
}

function sanitizeName(name: string): string {
  return name.replace(/[^a-zA-Z0-9_]/g, '_');
}

function buildMermaidDef(
  selected: string[],
  tableMap: Map<string, TableEntry>,
  columnDetails: Map<string, Map<string, Column>>,
  schemaEntryPks: Map<string, string>,
): string {
  if (selected.length < 2) return '';

  const colToTables = new Map<string, string[]>();
  for (const key of selected) {
    const entry = tableMap.get(key);
    if (!entry) continue;
    for (const col of entry.columns) {
      if (GENERIC_COLUMNS.has(col)) continue;
      const existing = colToTables.get(col) || [];
      existing.push(key);
      colToTables.set(col, existing);
    }
  }

  const sharedCols = new Map<string, string[]>();
  for (const [col, tables] of colToTables) {
    if (tables.length >= 2) sharedCols.set(col, tables);
  }

  const lines: string[] = ['erDiagram'];

  const addedRels = new Set<string>();
  for (const [col, tables] of sharedCols) {
    for (let i = 0; i < tables.length; i++) {
      for (let j = i + 1; j < tables.length; j++) {
        const a = sanitizeName(tables[i]);
        const b = sanitizeName(tables[j]);
        const relKey = [a, b].sort().join('--') + ':' + col;
        if (!addedRels.has(relKey)) {
          addedRels.add(relKey);
          lines.push(`    ${a} ||--o{ ${b} : "${sanitizeName(col)}"`);;
        }
      }
    }
  }

  for (const key of selected) {
    const entry = tableMap.get(key);
    const details = columnDetails.get(key);
    if (!entry || !details) continue;
    const safe = sanitizeName(key);
    const pk = schemaEntryPks.get(entry.schema) || '';
    lines.push(`    ${safe} {`);
    for (const [colName, col] of details) {
      const mt = mermaidType(col.type);
      const marker = colName === pk ? ' PK' : '';
      lines.push(`        ${mt} ${sanitizeName(colName)}${marker}`);
    }
    lines.push('    }');
  }

  return lines.join('\n');
}

function MermaidDiagram({
  selected, tableMap, columnDetails, schemaEntryPks,
}: {
  selected: string[];
  tableMap: Map<string, TableEntry>;
  columnDetails: Map<string, Map<string, Column>>;
  schemaEntryPks: Map<string, string>;
}) {
  const mermaidDef = useMemo(
    () => buildMermaidDef(selected, tableMap, columnDetails, schemaEntryPks),
    [selected, tableMap, columnDetails, schemaEntryPks],
  );
  if (!mermaidDef) return null;
  return (
    <BrowserOnly>
      {() => <MermaidRenderer definition={mermaidDef} />}
    </BrowserOnly>
  );
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function MermaidRenderer({definition}: {definition: string}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [svgContent, setSvgContent] = useState<string | null>(null);
  const idRef = useRef(0);

  useEffect(() => {
    let cancelled = false;
    setError(null);
    (async () => {
      if (!containerRef.current) return;
      try {
        const mermaid = (await import('mermaid')).default;
        mermaid.initialize({
          startOnLoad: false,
          theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default',
          er: {useMaxWidth: true},
        });
        idRef.current += 1;
        const {svg} = await mermaid.render(`mermaid-er-${idRef.current}`, definition);
        if (!cancelled && containerRef.current) {
          containerRef.current.innerHTML = svg;
          setSvgContent(svg);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to render diagram');
      }
    })();
    return () => { cancelled = true; };
  }, [definition]);

  const handleDownloadSvg = useCallback(() => {
    if (!svgContent) return;
    const blob = new Blob([svgContent], {type: 'image/svg+xml'});
    downloadBlob(blob, 'table-relations.svg');
  }, [svgContent]);

  const handleDownloadPng = useCallback(() => {
    try {
      const svgEl = containerRef.current?.querySelector('svg');
      if (!svgEl) return;
      const svgData = new XMLSerializer().serializeToString(svgEl);
      const canvas = document.createElement('canvas');
      const bbox = svgEl.getBoundingClientRect();
      const scale = 2;
      canvas.width = bbox.width * scale;
      canvas.height = bbox.height * scale;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const img = new Image();
      img.onerror = () => {
        setError('Failed to render PNG. Try downloading SVG instead.');
      };
      img.onload = () => {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          if (blob) downloadBlob(blob, 'table-relations.png');
        });
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    } catch {
      setError('Failed to export PNG. Try downloading SVG instead.');
    }
  }, []);

  if (error) return <p className="schema-search__error">Diagram error: {error}</p>;
  return (
    <div>
      {svgContent && (
        <div className="table-relations__download-bar">
          <button onClick={handleDownloadSvg} className="table-relations__download-btn">
            Download SVG
          </button>
          <button onClick={handleDownloadPng} className="table-relations__download-btn">
            Download PNG
          </button>
        </div>
      )}
      <div ref={containerRef} className="table-relations__diagram" />
    </div>
  );
}

/** Suggest related tables. */
function SuggestedTables({
  selected, allTables, tableMap, onAdd,
}: {
  selected: string[];
  allTables: TableEntry[];
  tableMap: Map<string, TableEntry>;
  onAdd: (key: string) => void;
}) {
  const suggestions = useMemo(() => {
    if (selected.length === 0) return [];
    const selectedSet = new Set(selected);
    const scored = new Map<string, number>();

    for (const selKey of selected) {
      const entry = tableMap.get(selKey);
      if (!entry) continue;
      for (const t of allTables) {
        const key = `${t.schema}.${t.table}`;
        if (selectedSet.has(key) || t.schema !== entry.schema) continue;
        let score = 0;
        if (t.table.startsWith(entry.table + '_') || entry.table.startsWith(t.table + '_')) score += 3;
        for (const col of entry.columns) {
          if (col.endsWith('_id') && !GENERIC_COLUMNS.has(col) && t.columns.has(col)) score += 1;
        }
        if (score > 0) scored.set(key, (scored.get(key) || 0) + score);
      }
    }
    return Array.from(scored.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([key]) => key);
  }, [selected, allTables, tableMap]);

  if (suggestions.length === 0 || selected.length >= MAX_TABLES) return null;

  return (
    <div className="table-relations__suggestions">
      <strong>Suggested:</strong>{' '}
      {suggestions.map((key, i) => (
        <span key={key}>
          {i > 0 && ' '}
          <button onClick={() => onAdd(key)} className="table-relations__suggestion-btn">
            + {key}
          </button>
        </span>
      ))}
    </div>
  );
}

export default function TableRelationsPage(): ReactNode {
  const {schemas, loading, error} = useSchemaData();
  const [selected, setSelected] = useState<string[]>([]);

  const {allTables, tableMap, columnDetails, schemaEntryPks} = useMemo(() => {
    const tables: TableEntry[] = [];
    const map = new Map<string, TableEntry>();
    const details = new Map<string, Map<string, Column>>();
    const pks = new Map<string, string>();

    for (const schema of schemas) {
      pks.set(schema.schema, schema.primaryKey);
      for (const table of schema.tables) {
        const key = `${schema.schema}.${table.name}`;
        const colSet = new Set(table.columns.map((c) => c.name));
        const entry: TableEntry = {schema: schema.schema, table: table.name, columns: colSet};
        tables.push(entry);
        map.set(key, entry);
        const colMap = new Map<string, Column>();
        for (const col of table.columns) colMap.set(col.name, col);
        details.set(key, colMap);
      }
    }
    return {allTables: tables, tableMap: map, columnDetails: details, schemaEntryPks: pks};
  }, [schemas]);

  const handleAdd = useCallback((key: string) => {
    setSelected((prev) => (prev.includes(key) || prev.length >= MAX_TABLES ? prev : [...prev, key]));
  }, []);

  const handleRemove = useCallback((key: string) => {
    setSelected((prev) => prev.filter((k) => k !== key));
  }, []);

  const handleClearAll = useCallback(() => {
    setSelected([]);
  }, []);

  const handlePreset = useCallback((tables: string[]) => {
    setSelected(tables.slice(0, MAX_TABLES));
  }, []);

  return (
    <Layout title="Table Relations" description="Explore relationships between database tables">
      <main className="container margin-vert--lg">
        <h1>Table Relations</h1>
        <p>
          Select tables to visualize shared columns and relationships.
          Tables in the same schema sharing column names indicate implicit relationships.
        </p>

        {loading && <p>Loading schema data...</p>}
        {error && <p className="schema-search__error">Error: {error}</p>}
        {!loading && !error && (
          <>
            {/* Presets - show when nothing selected */}
            {selected.length === 0 && (
              <div className="table-relations__presets">
                <h3>Examples</h3>
                <div className="table-relations__preset-grid">
                  {PRESETS.map((p) => (
                    <button
                      key={p.label}
                      onClick={() => handlePreset(p.tables)}
                      className="table-relations__preset-btn"
                    >
                      <strong>{p.label}</strong>
                      <span>{p.description}</span>
                      <span className="table-relations__col-count">
                        {p.tables.length} tables
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <SchemaTablePicker
              schemas={schemas}
              allTables={allTables}
              selected={selected}
              onAdd={handleAdd}
              onRemove={handleRemove}
              onClearAll={handleClearAll}
            />

            <SuggestedTables
              selected={selected}
              allTables={allTables}
              tableMap={tableMap}
              onAdd={handleAdd}
            />

            <MermaidDiagram
              selected={selected}
              tableMap={tableMap}
              columnDetails={columnDetails}
              schemaEntryPks={schemaEntryPks}
            />

            <SharedColumnsView
              selected={selected}
              tableMap={tableMap}
              columnDetails={columnDetails}
            />
          </>
        )}
      </main>
    </Layout>
  );
}
