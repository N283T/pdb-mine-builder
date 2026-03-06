import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'pdb-mine-builder',
  tagline: 'Build a MINE-schema database from PDB data',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://n283t.github.io',
  baseUrl: '/pdb-mine-builder/',

  organizationName: 'N283T',
  projectName: 'pdb-mine-builder',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/N283T/pdb-mine-builder/tree/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'pdb-mine-builder',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'gettingStarted',
          position: 'left',
          label: 'Getting Started',
        },
        {
          type: 'docSidebar',
          sidebarId: 'database',
          position: 'left',
          label: 'Database',
        },
        {
          href: 'https://github.com/N283T/pdb-mine-builder',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} pdb-mine-builder. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'sql', 'yaml', 'python'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
