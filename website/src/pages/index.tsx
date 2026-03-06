import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/getting-started/installation">
            Getting Started
          </Link>
          <Link
            className="button button--secondary button--lg"
            style={{marginLeft: '1rem'}}
            to="/docs/database/overview">
            Database Reference
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="Build a MINE-schema database from PDB data">
      <HomepageHeader />
      <main>
        <section style={{padding: '2rem 0'}}>
          <div className="container">
            <div className="row">
              <div className="col col--6">
                <Heading as="h2">Getting Started</Heading>
                <p>
                  Install pdb-mine-builder, configure your environment,
                  sync data from PDBj, and load it into PostgreSQL.
                </p>
                <Link to="/docs/getting-started/installation">Read the guide →</Link>
              </div>
              <div className="col col--6">
                <Heading as="h2">Database Reference</Heading>
                <p>
                  Explore the database schemas, table definitions,
                  and SQL query examples for structural biology data.
                </p>
                <Link to="/docs/database/overview">Browse schemas →</Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
