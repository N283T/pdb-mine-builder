
# fetch data from pdbj's ftp
mkdir -p data
cd data
rsync -a --delete data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-noatom .
rsync -a --delete data.pdbj.org::rsync/pdbjplus/data/pdb/mmjson-plus/ plus
rsync -a --delete data.pdbj.org::rsync/pdbjplus/data/cc/mmjson/ cc
rsync -a --delete data.pdbj.org::rsync/pdbjplus/data/ccmodel/mmjson/ ccmodel
rsync -a --delete data.pdbj.org::rsync/pdbjplus/data/prd/mmjson/ prd
rsync -a --delete data.pdbj.org::ftp/validation_reports/*/*/*_validation.cif.gz vrpt
cd ..
rsync -a --delete data.pdbj.org::rsync/pdbjplus/mine2/schemas .
rsync -a --delete data.pdbj.org::rsync/pdbjplus/dictionaries .

# RDB updater modules, comment out whatever is not required

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
