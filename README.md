### About
This is the repository for the new Mine 2 RDB updater system, replacing the old dump & delta file system.

### Requirements
- PostgreSQL 12 or newer
- Nodejs 14 or newer
- Openbabel (for chem_comp fingerprinting)

### Installation
This application requires nodejs (latest LTS from https://nodejs.org/en/download/ or via your OS' package manager). 

Then, obtain mine2updater:
- `git clone https://gitlab.com/pdbjapan/mine2updater.git`  
- `cd mine2updater`

And install the dependencies (via nodejs' package manager):<br />
- `npm install`

Create a psql databases and modify `rdb.constring` in `config.yml`, so that the `dbname`, `user`, `password` and `port` settings match the settings used for your database.

Modify `do-update.sh` and disable all schema's you do not need. Otherwise, keep the file as it is.

### Usage
Simply execute `bash do-update.sh`, which will download all modified entries & update all configured schemas.

Note: to upgrade from an RDB created via an old dump file, it might be necessary to execute the update for the `pdbj` schema twice, as the schema differences might in some cases be too incompatible to update in a single iteration.
