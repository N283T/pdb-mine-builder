#!/bin/zsh

# Usage: ./do-update.sh [OPTIONS]
#   --sync, -s    : Run rsync only (fetch data)
#   --update, -u  : Run node update only (RDB update)
#   --all, -a     : Run both (default if no option specified)
#   --help, -h    : Show this help message

set -e

DO_SYNC=false
DO_UPDATE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --sync|-s)
            DO_SYNC=true
            shift
            ;;
        --update|-u)
            DO_UPDATE=true
            shift
            ;;
        --all|-a)
            DO_SYNC=true
            DO_UPDATE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "  --sync, -s    : Run rsync only (fetch data)"
            echo "  --update, -u  : Run node update only (RDB update)"
            echo "  --all, -a     : Run both (default if no option specified)"
            echo "  --help, -h    : Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Default: run both if no option specified
if [[ "$DO_SYNC" == "false" && "$DO_UPDATE" == "false" ]]; then
    DO_SYNC=true
    DO_UPDATE=true
fi

# Rsync section: fetch data from pdbj's ftp
if [[ "$DO_SYNC" == "true" ]]; then
    echo "==> Starting rsync..."
    mkdir -p data
    cd data
    echo "==> Syncing mmjson-noatom..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-noatom .
    echo "==> Syncing plus..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-plus/ plus
    echo "==> Syncing cc..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/cc/mmjson/ cc
    echo "==> Syncing ccmodel..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/ccmodel/mmjson/ ccmodel
    echo "==> Syncing prd..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/prd/mmjson/ prd
    echo "==> Syncing vrpt..."
    rsync -ah --delete --info=progress2 data.pdbj.org::ftp/validation_reports/*/*/*_validation.cif.gz vrpt
    echo "==> Syncing contacts..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/data/pdb/contacts .
    cd ..
    echo "==> Syncing schemas..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/mine2/schemas .
    echo "==> Syncing dictionaries..."
    rsync -ah --delete --info=progress2 data.pdbj.org::rsync/pdbjplus/dictionaries .
    echo "==> Rsync completed."
fi

# Node section: RDB updater modules
if [[ "$DO_UPDATE" == "true" ]]; then
    echo "==> Starting RDB update..."

    # update pdbj schema (PDB metadata & plus-data)
    node --max-old-space-size=8192 mine2.js pdbj.load

    # update cc schema (chem_comp)
    node --max-old-space-size=8192 mine2.js cc.load

    # update ccmodel schema (chem_comp linkage to csd)
    node --max-old-space-size=8192 mine2.js ccmodel.load

    # update prd schema (BIRD, Biologically Interesting Molecule Reference Dictionary)
    node --max-old-space-size=8192 mine2.js prd.load

    # update vrpt schema (wwPDB validation reports)
    node --max-old-space-size=8192 mine2.js vrpt.load

    # update contacts schema (intermolecular contacts in the AU)
    node --max-old-space-size=8192 mine2.js contacts.load

    echo "==> RDB update completed."
fi

echo "==> Done."
