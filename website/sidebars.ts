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
        'database/vrpt',
        'database/contacts',
        'database/emdb',
        'database/ihm',
      ],
    },
  ],
};

export default sidebars;
