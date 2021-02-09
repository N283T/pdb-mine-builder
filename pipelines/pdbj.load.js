// script to load mmjson-plus-noatom data into the rdb...

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const dateformat = (await import("dateformat")).default;
const fsp = fs.promises;

const rdbHelper = await import("../modules/rdb-helper.js");
const general = await import("../modules/general.js");
const rdbLoader = await import("../modules/rdb-loader.js");

// loading from scratch (excluding schema): ~ 50-60 minutes
// update: ~ 12-15 minutes

var chain_type_mapping = {"polypeptide(D)": 1, "polypeptide(L)": 2, "polydeoxyribonucleotide": 3, "polyribonucleotide": 4, "polysaccharide(D)": 5, "polysaccharide(L)": 6, "polydeoxyribonucleotide/polyribonucleotide hybrid": 7, "cyclic-pseudo-peptide": 8, "other": 9, "peptide nucleic acid": 10};
var exptl_method_mapping = {"X-RAY DIFFRACTION": 1, "NEUTRON DIFFRACTION": 2, "FIBER DIFFRACTION": 3, "ELECTRON CRYSTALLOGRAPHY": 4, "ELECTRON MICROSCOPY": 5, "SOLUTION NMR": 6, "SOLID-STATE NMR": 7, "SOLUTION SCATTERING": 8, "POWDER DIFFRACTION": 9, "INFRARED SPECTROSCOPY": 10, "EPR": 11, "FLUORESCENCE TRANSFER": 12, "THEORETICAL MODEL": 13, "HYBRID": 14, "THEORETICAL MODEL (obsolete)": 15};

export async function pipeline_exec(config) {
  const rdb_def = yaml.safeLoad(await fsp.readFile(general.expandPath(config.pipelines.pdb.deffile), 'utf8'));
  var jm = await rdbLoader.init(config, rdb_def);

  var dir = general.expandPath(config.pipelines.pdb.data);
  if (! dir.endsWith("/")) dir += "/";
  
  var dir_plus = general.expandPath(config.pipelines.pdb["data-plus"]);
  if (! dir_plus.endsWith("/")) dir_plus += "/";
  const plusFiles = Object.fromEntries((await fsp.readdir(dir_plus)).map(x=>[x.split("-")[0].split(".")[0], dir_plus+x]));
  (await fsp.readdir(dir)).forEach(x => jm.jobs.push({path: dir+x, pathPlus: plusFiles[x.split("-")[0].split(".")[0]], entryId: x.split("-")[0]}));

  jm.scandone = true;
  await jm.waiter.promise;
  
  const dbconnect = new rdbHelper.nativePSQLpool(config.rdb.constring, 1);
  const update_date = dateformat((await dbconnect.query("select max(release_date) as rdate from brief_summary")).rdate[0], "yyyy-mm-dd");
  await dbconnect.query(`CREATE OR REPLACE FUNCTION UPDATE_DATE() RETURNS date LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$SELECT TO_DATE('${update_date}', 'YYYY-MM-DD')$$`);
  dbconnect.end();
};

export function brief_summary(memObj, __primaryKey__) {
  var t, tbl, pk, c, col_nfo, tbl_nfo, nor, mmjson = memObj.mmjson, tmp, sequences;
  
  if (mmjson.pdbx_struct_assembly_gen) {
    tbl = mmjson.pdbx_struct_assembly_gen;
    tbl._hash_asym_id_list = tbl.asym_id_list.map(x => rdbHelper.hex_sha256(x));
  }
  
  tbl = mmjson.brief_summary = {};
  
  if (mmjson.entity_poly) sequences = mmjson.entity_poly.pdbx_seq_one_letter_code_can;
  else sequences = [];
  
  tbl[__primaryKey__] = [memObj.entryId];
  
  tbl.docid = [rdbHelper.gen_docid(memObj.entryId)];

  tbl.deposition_date = [mmjson.pdbx_database_status.recvd_initial_deposition_date ? mmjson.pdbx_database_status.recvd_initial_deposition_date[0] : null];

  tbl.release_date = [mmjson.pdbx_audit_revision_history.revision_date ? mmjson.pdbx_audit_revision_history.revision_date[0] : null];
  tbl.modification_date = [mmjson.pdbx_audit_revision_history.revision_date ? mmjson.pdbx_audit_revision_history.revision_date[mmjson.pdbx_audit_revision_history.revision_date.length-1] : null];

  tbl.deposit_author = [mmjson.audit_author.name];
  if (mmjson.citation_author) {
    tbl.citation_author = [mmjson.citation_author.name];
    tbl.citation_author_pri = [rdbHelper.mmjsonAt(mmjson.citation_author, "name", "citation_id", "primary")];
  }
  else {
    tbl.citation_author = [[]];
    tbl.citation_author_pri = [[]];
  }
  
  if (mmjson.citation) {
    tbl.citation_title = [rdbHelper.removeNull(mmjson.citation.title)];
    
    tbl.citation_journal = [rdbHelper.removeNull(mmjson.citation.journal_abbrev)];
    tbl.citation_year = [rdbHelper.removeNull(mmjson.citation.year)];
    
    tbl.citation_volume = [rdbHelper.removeNull(mmjson.citation.journal_volume)];
    tbl.citation_title_pri = rdbHelper.mmjsonAt(mmjson.citation, "title", "id", "primary");
    tbl.citation_journal_pri = rdbHelper.mmjsonAt(mmjson.citation, "journal_abbrev", "id", "primary");
    tbl.citation_year_pri = rdbHelper.mmjsonAt(mmjson.citation, "year", "id", "primary");
    tbl.citation_volume_pri = rdbHelper.mmjsonAt(mmjson.citation, "journal_volume", "id", "primary");
    
    if (tbl.citation_title_pri.length == 0) {
      tbl.citation_title_pri = [null];
      tbl.citation_journal_pri = [null];
      tbl.citation_year_pri = [null];
      tbl.citation_volume_pri = [null];
    }

    tbl.db_pubmed = [rdbHelper.removeNull(mmjson.citation.pdbx_database_id_PubMed).map(x => x+"")];
    tbl.db_doi = [rdbHelper.removeNull(mmjson.citation.pdbx_database_id_DOI)];
  }
  else {
    tbl.citation_title = [[]];
    tbl.citation_journal = [[]];
    tbl.citation_year = [[]];
    
    tbl.citation_volume = [[]];
    tbl.citation_title_pri = [null];
    tbl.citation_journal_pri = [null];
    tbl.citation_year_pri = [null];
    tbl.citation_volume_pri = [null];
    
    tbl.db_pubmed = [[]];
    tbl.db_doi = [[]];
  }

  if (mmjson.entity_poly) tmp = rdbHelper.cleanArray(mmjson.entity_poly.type);
  else tmp = [];
  tbl.chain_type = [tmp];  
  tbl.chain_type_ids = [rdbHelper.cleanArray(tmp.map(x => chain_type_mapping[x]))];
  
  tmp = rdbHelper.mmjsonAt(mmjson.entity, "pdbx_number_of_molecules", "type", "polymer");
  if (tmp.length == 0) tbl.chain_number = [0];
  else tbl.chain_number = [tmp.reduce((a,b) => a+b)];
  tbl.chain_length = [sequences.map(x => x.replace(/\n/g, '').length)];
  
  tbl.pdbx_descriptor = [rdbHelper.cleanArray(mmjson.entity.pdbx_description.unique()).join(', ')];
  
  tbl.struct_title = [mmjson.struct.title[0]];

  tbl.ligand = [rdbHelper.cleanArray(rdbHelper.mmjsonAt_IC(mmjson.chem_comp, "name", "type", "non-polymer").concat(rdbHelper.mmjsonAt_IC(mmjson.chem_comp, "pdbx_synonyms", "type", "non-polymer")).concat(rdbHelper.mmjsonAt_IC(mmjson.chem_comp, "id", "type", "non-polymer")))];

  tmp = rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.exptl, "method")); if (tmp.length > 1) tmp.push("HYBRID");
  tbl.exptl_method = [tmp];
  tbl.exptl_method_ids = [rdbHelper.cleanArray(tmp.map(function(x) {return exptl_method_mapping[x];}))];
  
  
  tbl.resolution = [rdbHelper.mmjsonGet(mmjson.refine, "ls_d_res_high", 0) || rdbHelper.mmjsonGet(mmjson.em_3d_reconstruction, "resolution", 0)];

  tbl.biol_species = [rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.entity_src_gen, "pdbx_gene_src_scientific_name").concat(rdbHelper.mmjsonGet(mmjson.entity_src_gen, "gene_src_common_name")).concat(rdbHelper.mmjsonGet(mmjson.entity_src_nat, "common_name")).concat(rdbHelper.mmjsonGet(mmjson.entity_src_nat, "pdbx_organism_scientific")).concat(rdbHelper.mmjsonGet(mmjson.pdbx_entity_src_syn, "organism_common_name")).concat(rdbHelper.mmjsonGet(mmjson.pdbx_entity_src_syn, "organism_scientific"))).join(" ") || null];
  
  
  tbl.host_species = [rdbHelper.mmjsonGet(mmjson.entity_src_gen, "pdbx_host_org_scientific_name", 0)];  
  tbl.db_ec_number = [rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.entity, "pdbx_ec"))];
  
  tbl.db_goid = [rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.gene_ontology_pdbmlplus, "goid"))];
  tbl.db_uniprot = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "UNP").concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "UNP")).concat(rdbHelper.mmjsonAt(mmjson.struct_ref_pdbmlplus, "pdbx_db_accession", "db_name", "SIFTS_UNP")).concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "UNP")))];
  
  
  tbl.db_genbank = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "GB").concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "GB")))];
  tbl.db_embl = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "EMBL").concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "EMBL")))];
  tbl.db_pir = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "PIR").concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "PIR")))];
  
  tbl.db_emdb = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.pdbx_database_related, "db_id", "db_name", "EMDB"))];
  tbl.pdb_related = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.pdbx_database_related, "db_id", "db_name", "PDB"))];
  
  tbl.aaseq = [sequences.join('')];
  tbl.update_date = [null];
  tbl.db_pfam = [rdbHelper.cleanArray(rdbHelper.mmjsonAt(mmjson.struct_ref_pdbmlplus, "pdbx_db_accession", "db_name", "Pfam"))];

  tbl.group_id = [mmjson.pdbx_deposit_group && mmjson.pdbx_deposit_group.group_id ? mmjson.pdbx_deposit_group.group_id[0] : null];
}

export async function load_data(payload, config) {
  const mmjson = JSON.parse((await general.gunzip(await fsp.readFile(payload.path))).toString());
  if (payload.pathPlus) Object.assign(mmjson, JSON.parse((await general.gunzip(await fsp.readFile(payload.pathPlus))).toString()));
  return mmjson;
}

