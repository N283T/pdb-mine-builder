# MINE2 Updater (TypeScript)

Modern, maintainable RDB updater for MINE2. This repository is a TypeScript refactor of the original mine2updater.

The CLI synchronizes data from PDBj (Protein Data Bank Japan) via rsync and loads/updates a PostgreSQL database through named pipelines.

## Highlights

- TypeScript conversion with stricter types and clearer module boundaries
- Command-based CLI for sync/update/test workflows
- Config-driven pipelines for repeatable updates

## Requirements

- PostgreSQL 12+ (with libpq-dev)
- Node.js 14+ (LTS recommended)
- OpenBabel (for chemical component fingerprinting)
- rsync

## Install

```bash
git clone https://gitlab.com/pdbjapan/mine2updater.git
cd mine2updater
npm install
npm run build
```

The `postinstall` script patches `libpq` automatically.

## Configuration

Edit `config.yml` to match your environment.

```yaml
rdb:
  nworkers: 16
  constring: "dbname='mine2' user='pdbj' port=5433"

obabel: /usr/bin/obabel

pipelines:
  pdb:
    deffile: ${CWD}schemas/pdbj.def.yml
    data: ${CWD}data/mmjson-noatom/
    data-plus: ${CWD}data/plus/
```

Notes:
- The CLI pipeline name is `pdbj`, but the config key is `pipelines.pdb`.
- `${CWD}` is resolved to the repository root at runtime.
- `config.test.yml` is used by the `test` command by default.

## Usage

After building, run the CLI through npm:

```bash
npm start -- --help
```

You can also run `node dist/mine2.js ...` directly.

### Sync data

```bash
npm start -- sync [targets...]
```

Targets: `pdbj`, `cc`, `ccmodel`, `prd`, `vrpt`, `contacts`, `schemas`, `dictionaries`

Examples:

```bash
npm start -- sync
npm start -- sync pdbj cc prd
```

### Update database

```bash
npm start -- update [pipelines...]
```

Pipelines: `pdbj`, `cc`, `ccmodel`, `prd`, `vrpt`, `contacts`

Examples:

```bash
npm start -- update
npm start -- update pdbj cc
```

### Full update (sync + update)

```bash
npm start -- all
```

### Test

```bash
npm start -- test [options]
```

Options:
- `-c, --config <file>`: test config (default: `config.test.yml`)
- `-d, --drop`: drop existing test DB before creating
- `-p, --pipelines <pipelines>`: comma-separated pipeline list
- `-n, --limit <number>`: limit files per pipeline
- `-m, --mode <mode>`: vrpt mode (`json`|`cif`|`both`, default: `json`)

Example:

```bash
npm start -- test -p pdbj,cc -n 5
```

### VRPT conversion (CIF to JSON)

```bash
npm start -- convert-vrpt
```

### Legacy pipeline invocation

```bash
npm start -- pdbj
npm start -- cc
```

## Pipelines

- `pdbj`: Main structure data (mmjson-noatom + mmjson-plus)
- `cc`: Chemical component dictionary
- `ccmodel`: Chemical component model data
- `prd`: BIRD data
- `vrpt`: Validation report data (JSON or CIF)
- `contacts`: Protein contact data

## Utilities

- `setup-db.sh`: create a local PostgreSQL instance and database on port 5433
- `setup-test-db.sh`: create a smaller test DB from the main database

## Troubleshooting

- Old dump migrations: run the `pdbj` update twice if schema differences prevent a single-pass update.
- Memory errors: increase `--max-old-space-size` in `package.json` if needed.

## Development

```bash
npm run typecheck
npm run dev
```
