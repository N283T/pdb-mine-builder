
# fetch data from pdbj's ftp
mkdir -p data
cd data
rsync -a --delete ftp.pdbj.org::rsync/mine2/data/mmjson/plus-noatom .
rsync -a --delete ftp.pdbj.org::rsync/mine2/data/cc/mmjson/ cc
rsync -a --delete ftp.pdbj.org::rsync/mine2/data/ccmodel/mmjson/ ccmodel
rsync -a --delete ftp.pdbj.org::rsync/mine2/data/prd/mmjson/ prd
rsync -a --delete ftp.pdbj.org::rsync/mine2/data/vrpt/mmjson/ vrpt
cd ..
rsync -a --delete ftp.pdbj.org::rsync/mine2/schemas .

# RDB updater modules, comment out whatever is not required

# update pdbj schema (PDB metadata & plus-data)
node --max-old-space-size=8192 mine2.js pdbj.load

# update cc schema (chem_comp)
node --max-old-space-size=8192 mine2.js cc.load

# update ccmodel schema (chem_comp linkage to csd)
node --max-old-space-size=8192 mine2.js ccmodel.load

# update prd schema (BIRD, Biologically Interesting Molecule Reference Dictionary)
node --max-old-space-size=8192 mine2.js prd.load

# update vrpt schema (validation reports, pdbj version)
node --max-old-space-size=8192 mine2.js vrpt.load
