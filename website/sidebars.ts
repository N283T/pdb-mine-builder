import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  gettingStarted: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/installation',
        'getting-started/configuration',
        'getting-started/sync',
        'getting-started/update',
        'getting-started/query',
        'getting-started/migration',
      ],
    },
  ],
  database: [
    {
      type: 'category',
      label: 'Database Reference',
      collapsed: false,
      items: [
        'database/overview',
        'database/pdbj',
        'database/cc',
        'database/ccmodel',
        'database/prd',
        'database/prd_family',
        'database/vrpt',
        'database/contacts',
        'database/emdb',
        'database/ihm',
      ],
    },
    {
      type: 'category',
      label: 'ER Diagrams',
      collapsed: true,
      items: [
        'database/er-pdbj',
        'database/er-cc',
        'database/er-ccmodel',
        'database/er-prd',
        'database/er-prd_family',
        'database/er-vrpt',
        'database/er-contacts',
        'database/er-emdb',
        'database/er-ihm',
      ],
    },
  ],
};

export default sidebars;
