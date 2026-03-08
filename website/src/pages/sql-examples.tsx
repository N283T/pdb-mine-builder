import type {ReactNode} from 'react';
import React, {useState, useEffect, useMemo, useCallback} from 'react';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';

interface Example {
  id: number;
  title: string;
  description: string;
  sql: string;
}

interface Category {
  id: string;
  label: string;
  description: string;
  count: number;
  examples: Example[];
}

function useExamplesData() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dataUrl = useBaseUrl('/data/sqlExamples.json');

  useEffect(() => {
    fetch(dataUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: Category[]) => setCategories(data))
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load data.'))
      .finally(() => setLoading(false));
  }, [dataUrl]);

  return {categories, loading, error};
}

function CopyButton({text}: {text: string}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [text]);

  return (
    <button
      onClick={handleCopy}
      className="sql-examples__copy-btn"
      title="Copy SQL to clipboard"
    >
      {copied ? 'Copied!' : 'Copy'}
    </button>
  );
}

function ExampleCard({example}: {example: Example}) {
  return (
    <div className="sql-examples__card expanded">
      <div className="sql-examples__card-header">
        <span className="sql-examples__card-title">{example.title}</span>
      </div>
      <div className="sql-examples__card-body">
        <p className="sql-examples__card-desc">{example.description}</p>
        <div className="sql-examples__code-wrapper">
          <CopyButton text={example.sql} />
          <pre className="sql-examples__code">
            <code>{example.sql}</code>
          </pre>
        </div>
      </div>
    </div>
  );
}

function CategoryTabs({
  categories,
  active,
  onSelect,
}: {
  categories: Category[];
  active: string | null;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="sql-examples__tabs">
      {categories.map((cat) => (
        <button
          key={cat.id}
          onClick={() => onSelect(cat.id)}
          className={`sql-examples__tab ${active === cat.id ? 'active' : ''}`}
        >
          {cat.label}
          <span className="sql-examples__tab-count">{cat.count}</span>
        </button>
      ))}
    </div>
  );
}

function SearchBar({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="sql-examples__search">
      <input
        type="text"
        placeholder="Search examples by title, description, or SQL..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="schema-filter__input sql-examples__search-input"
      />
    </div>
  );
}

export default function SqlExamplesPage(): ReactNode {
  const {categories, loading, error} = useExamplesData();
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Set default category once loaded
  useEffect(() => {
    if (categories.length > 0 && !activeCategory) {
      setActiveCategory(categories[0].id);
    }
  }, [categories, activeCategory]);

  const filteredExamples = useMemo(() => {
    const query = searchQuery.toLowerCase();

    if (query) {
      // Search mode: search across all categories
      const results: {category: Category; examples: Example[]}[] = [];
      for (const cat of categories) {
        const matches = cat.examples.filter(
          (ex) =>
            ex.title.toLowerCase().includes(query) ||
            ex.description.toLowerCase().includes(query) ||
            ex.sql.toLowerCase().includes(query),
        );
        if (matches.length > 0) {
          results.push({category: cat, examples: matches});
        }
      }
      return results;
    }

    // Category mode
    const cat = categories.find((c) => c.id === activeCategory);
    if (!cat) return [];
    return [{category: cat, examples: cat.examples}];
  }, [categories, activeCategory, searchQuery]);

  const totalResults = filteredExamples.reduce((sum, g) => sum + g.examples.length, 0);

  return (
    <Layout title="SQL Examples" description="SQL query examples for pdb-mine-builder database">
      <main className="container margin-vert--lg">
        <h1>SQL Query Examples</h1>
        <p>
          A collection of {categories.reduce((sum, c) => sum + c.count, 0)} SQL query examples
          adapted from{' '}
          <a href="https://pdbj.org/help/mine-sql" target="_blank" rel="noopener noreferrer">
            PDBj Mine
          </a>{' '}
          with schema-prefixed table names for pdb-mine-builder.
        </p>

        <div className="sql-examples__info-box">
          <strong>How to run:</strong> Use{' '}
          <code>pmb query "SQL"</code> or{' '}
          <code>pixi run psql -c "SQL"</code>.
          Click <strong>Copy</strong> to copy any query to your clipboard.
        </div>

        {loading && <p>Loading examples...</p>}
        {error && <p className="schema-search__error">Error: {error}</p>}

        {!loading && !error && (
          <>
            <SearchBar value={searchQuery} onChange={setSearchQuery} />

            {!searchQuery && (
              <CategoryTabs
                categories={categories}
                active={activeCategory}
                onSelect={(id) => {
                  setActiveCategory(id);
                  setSearchQuery('');
                }}
              />
            )}

            {/* Category description */}
            {!searchQuery && filteredExamples.length === 1 && (
              <p className="sql-examples__cat-desc">
                {filteredExamples[0].category.description}
              </p>
            )}

            {/* Search result count */}
            {searchQuery && (
              <p className="schema-search__count">
                {totalResults} example{totalResults !== 1 ? 's' : ''} matching "{searchQuery}"
              </p>
            )}

            {/* Examples */}
            {filteredExamples.map(({category, examples}) => (
              <div key={category.id} className="sql-examples__group">
                {searchQuery && (
                  <h3 className="sql-examples__group-title">
                    {category.label}
                    <span className="sql-examples__tab-count"> ({examples.length})</span>
                  </h3>
                )}
                {examples.map((ex) => (
                  <ExampleCard key={ex.id} example={ex} />
                ))}
              </div>
            ))}

            {filteredExamples.length === 0 && (
              <p className="sql-examples__empty">No examples found matching your search.</p>
            )}

            {/* Array operators reference */}
            <div className="sql-examples__ref-box">
              <h3>PostgreSQL Array Operators Reference</h3>
              <p>Many examples use these operators on <code>brief_summary</code> array columns:</p>
              <table>
                <thead>
                  <tr>
                    <th>Operator</th>
                    <th>Meaning</th>
                    <th>Example</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><code>{'<@'}</code></td>
                    <td>is contained by (all elements match)</td>
                    <td><code>{"'{1,2}' <@ chain_type_ids"}</code></td>
                  </tr>
                  <tr>
                    <td><code>{'&&'}</code></td>
                    <td>overlaps (any element matches)</td>
                    <td><code>{"'{2001}' && citation_year"}</code></td>
                  </tr>
                  <tr>
                    <td><code>ANY()</code></td>
                    <td>matches any array element</td>
                    <td><code>6 = ANY(exptl_method_ids)</code></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </Layout>
  );
}
