/*
  Copyright (C) 2021 Gert-Jan Bekker
  Pipeline to load mmjson-plus-noatom data into the rdb
*/

import yaml from "js-yaml";
import * as fs from "fs";
import dateformat from "dateformat";

import * as rdbHelper from "../modules/rdb-helper.js";
import * as general from "../modules/general.js";
import * as rdbLoader from "../modules/rdb-loader.js";
import { setScandone } from "../modules/rdb-loader.js";
import type { Config, PipelineMemObj } from "../types/index.js";
import type { JobPayload } from "../modules/rdb-loader.js";

const fsp = fs.promises;

// loading from scratch (excluding schema): ~ 50-60 minutes
// update: ~ 12-15 minutes

const chain_type_mapping: Record<string, number> = {
  "polypeptide(D)": 1,
  "polypeptide(L)": 2,
  "polydeoxyribonucleotide": 3,
  "polyribonucleotide": 4,
  "polysaccharide(D)": 5,
  "polysaccharide(L)": 6,
  "polydeoxyribonucleotide/polyribonucleotide hybrid": 7,
  "cyclic-pseudo-peptide": 8,
  "other": 9,
  "peptide nucleic acid": 10,
};

const exptl_method_mapping: Record<string, number> = {
  "X-RAY DIFFRACTION": 1,
  "NEUTRON DIFFRACTION": 2,
  "FIBER DIFFRACTION": 3,
  "ELECTRON CRYSTALLOGRAPHY": 4,
  "ELECTRON MICROSCOPY": 5,
  "SOLUTION NMR": 6,
  "SOLID-STATE NMR": 7,
  "SOLUTION SCATTERING": 8,
  "POWDER DIFFRACTION": 9,
  "INFRARED SPECTROSCOPY": 10,
  "EPR": 11,
  "FLUORESCENCE TRANSFER": 12,
  "THEORETICAL MODEL": 13,
  "HYBRID": 14,
  "THEORETICAL MODEL (obsolete)": 15,
};

// mmJSON category types - use Record for flexibility with dynamic data
/* eslint-disable @typescript-eslint/no-explicit-any */
type AnyCategory = Record<string, any[]>;

interface BriefSummaryCategory {
  [key: string]: unknown[];
}

interface PDBJPayload extends JobPayload {
  path: string;
  pathPlus?: string;
}

// Pipeline-specific mmJSON type
type PDBJMMJson = Record<string, AnyCategory>;

export async function pipeline_exec(config: Config): Promise<void> {
  const rdb_def = yaml.load(
    await fsp.readFile(general.expandPath(config.pipelines.pdb.deffile as string), "utf8")
  ) as rdbLoader.RdbDef;
  const jm = await rdbLoader.init(config, rdb_def);

  let dir = general.expandPath(config.pipelines.pdb.data as string);
  if (!dir.endsWith("/")) dir += "/";

  let dir_plus = general.expandPath(config.pipelines.pdb["data-plus"] as string);
  if (!dir_plus.endsWith("/")) dir_plus += "/";

  const plusFiles = Object.fromEntries(
    (await fsp.readdir(dir_plus)).map((x) => [
      x.split("-")[0].split(".")[0],
      dir_plus + x,
    ])
  );

  // Get limit from argv (--limit N)
  const argv = config.argv as Record<string, unknown>;
  const limit = typeof argv.limit === "number" ? argv.limit : undefined;

  let files = await fsp.readdir(dir);
  if (limit) {
    files = files.slice(0, limit);
    console.log(`Processing ${files.length} entries (limited)`);
  }

  files.forEach((x) =>
    jm.jobs.push({
      path: dir + x,
      pathPlus: plusFiles[x.split("-")[0].split(".")[0]],
      entryId: x.split("-")[0],
    })
  );

  setScandone(jm);
  await jm.waiter.promise;

  const dbconnect = new rdbHelper.NativePSQLPool(config.rdb.constring, 1);
  const result = (await dbconnect.query(
    "select max(release_date) as rdate from brief_summary"
  )) as { rdate: (Date | null)[] };
  const update_date = dateformat(result.rdate[0] || new Date(), "yyyy-mm-dd");
  await dbconnect.query(
    `CREATE OR REPLACE FUNCTION UPDATE_DATE() RETURNS date LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$SELECT TO_DATE('${update_date}', 'YYYY-MM-DD')$$`
  );
  dbconnect.end();
}

export function brief_summary(
  memObj: PipelineMemObj,
  __primaryKey__: string
): void {
  const mmjson = memObj.mmjson as unknown as PDBJMMJson;

  if (mmjson.pdbx_struct_assembly_gen) {
    const tbl = mmjson.pdbx_struct_assembly_gen;
    tbl._hash_asym_id_list = tbl.asym_id_list.map((x) => rdbHelper.hex_sha256(x));
  }

  const tbl: BriefSummaryCategory = (mmjson.brief_summary = {});

  let sequences: string[];
  if (mmjson.entity_poly) sequences = mmjson.entity_poly.pdbx_seq_one_letter_code_can;
  else sequences = [];

  tbl[__primaryKey__] = [memObj.entryId];

  tbl.docid = [rdbHelper.gen_docid(memObj.entryId)];

  tbl.deposition_date = [
    mmjson.pdbx_database_status?.recvd_initial_deposition_date
      ? mmjson.pdbx_database_status.recvd_initial_deposition_date[0]
      : null,
  ];

  tbl.release_date = [
    mmjson.pdbx_audit_revision_history?.revision_date
      ? mmjson.pdbx_audit_revision_history.revision_date[0]
      : null,
  ];
  tbl.modification_date = [
    mmjson.pdbx_audit_revision_history?.revision_date
      ? mmjson.pdbx_audit_revision_history.revision_date[
          mmjson.pdbx_audit_revision_history.revision_date.length - 1
        ]
      : null,
  ];

  tbl.deposit_author = [mmjson.audit_author?.name || []];
  if (mmjson.citation_author) {
    tbl.citation_author = [mmjson.citation_author.name];
    tbl.citation_author_pri = [
      rdbHelper.mmjsonAt(mmjson.citation_author, "name", "citation_id", "primary"),
    ];
  } else {
    tbl.citation_author = [[]];
    tbl.citation_author_pri = [[]];
  }

  if (mmjson.citation) {
    tbl.citation_title = [rdbHelper.removeNull(mmjson.citation.title)];

    tbl.citation_journal = [rdbHelper.removeNull(mmjson.citation.journal_abbrev)];
    tbl.citation_year = [rdbHelper.removeNull(mmjson.citation.year)];

    tbl.citation_volume = [rdbHelper.removeNull(mmjson.citation.journal_volume)];
    tbl.citation_title_pri = rdbHelper.mmjsonAt(
      mmjson.citation,
      "title",
      "id",
      "primary"
    );
    tbl.citation_journal_pri = rdbHelper.mmjsonAt(
      mmjson.citation,
      "journal_abbrev",
      "id",
      "primary"
    );
    tbl.citation_year_pri = rdbHelper.mmjsonAt(
      mmjson.citation,
      "year",
      "id",
      "primary"
    );
    tbl.citation_volume_pri = rdbHelper.mmjsonAt(
      mmjson.citation,
      "journal_volume",
      "id",
      "primary"
    );

    if ((tbl.citation_title_pri as unknown[]).length === 0) {
      tbl.citation_title_pri = [null];
      tbl.citation_journal_pri = [null];
      tbl.citation_year_pri = [null];
      tbl.citation_volume_pri = [null];
    }

    tbl.db_pubmed = [
      rdbHelper
        .removeNull(mmjson.citation.pdbx_database_id_PubMed)
        .map((x) => x + ""),
    ];
    tbl.db_doi = [rdbHelper.removeNull(mmjson.citation.pdbx_database_id_DOI)];
  } else {
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

  let tmp: unknown[];
  if (mmjson.entity_poly) tmp = rdbHelper.cleanArray(mmjson.entity_poly.type);
  else tmp = [];
  tbl.chain_type = [tmp];
  tbl.chain_type_ids = [
    rdbHelper.cleanArray((tmp as string[]).map((x) => chain_type_mapping[x])),
  ];

  tmp = rdbHelper.mmjsonAt(mmjson.entity, "pdbx_number_of_molecules", "type", "polymer");
  if (tmp.length === 0) tbl.chain_number = [0];
  else tbl.chain_number = [(tmp as number[]).reduce((a, b) => a + b)];
  tbl.chain_length = [sequences.map((x) => x.replace(/\n/g, "").length)];

  tbl.pdbx_descriptor = [
    rdbHelper
      .cleanArray((mmjson.entity?.pdbx_description || []).unique())
      .join(", "),
  ];

  tbl.struct_title = [mmjson.struct?.title[0] || null];

  const chemCompType = mmjson.chem_comp?.type || [];
  tmp = chemCompType
    .map((x, i) =>
      x === "peptide linking" ||
      x === "L-peptide linking" ||
      x === "DNA linking" ||
      x === "RNA linking"
        ? -1
        : i
    )
    .filter((x) => x !== -1);
  tbl.ligand = [
    rdbHelper.cleanArray(
      (tmp as number[])
        .map((x) => mmjson.chem_comp?.name[x])
        .concat((tmp as number[]).map((x) => mmjson.chem_comp?.pdbx_synonyms[x]))
        .concat((tmp as number[]).map((x) => mmjson.chem_comp?.id[x]))
    ),
  ];

  tmp = rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.exptl, "method") as string[]);
  if (tmp.length > 1) tmp.push("HYBRID");
  tbl.exptl_method = [tmp];
  tbl.exptl_method_ids = [
    rdbHelper.cleanArray((tmp as string[]).map((x) => exptl_method_mapping[x])),
  ];

  tbl.resolution = [
    (rdbHelper.mmjsonGet(mmjson.refine, "ls_d_res_high", 0) as number | null) ||
      (rdbHelper.mmjsonGet(mmjson.em_3d_reconstruction, "resolution", 0) as number | null),
  ];

  tbl.biol_species = [
    rdbHelper
      .cleanArray(
        (rdbHelper.mmjsonGet(mmjson.entity_src_gen, "pdbx_gene_src_scientific_name") as string[])
          .concat(rdbHelper.mmjsonGet(mmjson.entity_src_gen, "gene_src_common_name") as string[])
          .concat(rdbHelper.mmjsonGet(mmjson.entity_src_nat, "common_name") as string[])
          .concat(rdbHelper.mmjsonGet(mmjson.entity_src_nat, "pdbx_organism_scientific") as string[])
          .concat(rdbHelper.mmjsonGet(mmjson.pdbx_entity_src_syn, "organism_common_name") as string[])
          .concat(rdbHelper.mmjsonGet(mmjson.pdbx_entity_src_syn, "organism_scientific") as string[])
      )
      .join(" ") || null,
  ];

  tbl.host_species = [
    rdbHelper.mmjsonGet(
      mmjson.entity_src_gen,
      "pdbx_host_org_scientific_name",
      0
    ) as string | null,
  ];
  tbl.db_ec_number = [
    rdbHelper.cleanArray(rdbHelper.mmjsonGet(mmjson.entity, "pdbx_ec") as string[]),
  ];

  tbl.db_goid = [
    rdbHelper.cleanArray(
      rdbHelper.mmjsonGet(mmjson.gene_ontology_pdbmlplus, "goid") as string[]
    ),
  ];
  tbl.db_uniprot = [
    rdbHelper.cleanArray(
      rdbHelper
        .mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "UNP")
        .concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "UNP"))
        .concat(
          rdbHelper.mmjsonAt(
            mmjson.struct_ref_pdbmlplus,
            "pdbx_db_accession",
            "db_name",
            "SIFTS_UNP"
          )
        )
        .concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "UNP"))
    ),
  ];

  tbl.db_genbank = [
    rdbHelper.cleanArray(
      rdbHelper
        .mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "GB")
        .concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "GB"))
    ),
  ];
  tbl.db_embl = [
    rdbHelper.cleanArray(
      rdbHelper
        .mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "EMBL")
        .concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "EMBL"))
    ),
  ];
  tbl.db_pir = [
    rdbHelper.cleanArray(
      rdbHelper
        .mmjsonAt(mmjson.struct_ref, "db_code", "db_name", "PIR")
        .concat(rdbHelper.mmjsonAt(mmjson.struct_ref, "pdbx_db_accession", "db_name", "PIR"))
    ),
  ];

  tbl.db_emdb = [
    rdbHelper.cleanArray(
      rdbHelper.mmjsonAt(mmjson.pdbx_database_related, "db_id", "db_name", "EMDB")
    ),
  ];
  tbl.pdb_related = [
    rdbHelper.cleanArray(
      rdbHelper.mmjsonAt(mmjson.pdbx_database_related, "db_id", "db_name", "PDB")
    ),
  ];

  tbl.aaseq = [sequences.join("")];
  tbl.update_date = [null];
  tbl.db_pfam = [
    rdbHelper.cleanArray(
      rdbHelper.mmjsonAt(
        mmjson.struct_ref_pdbmlplus,
        "pdbx_db_accession",
        "db_name",
        "Pfam"
      )
    ),
  ];

  tbl.group_id = [
    mmjson.pdbx_deposit_group && mmjson.pdbx_deposit_group.group_id
      ? mmjson.pdbx_deposit_group.group_id[0]
      : null,
  ];

  tbl.plus_fields = [{}];
  (tbl.plus_fields[0] as Record<string, number>).bu_mw = calculateMW4BU(mmjson);

  tbl.keywords = ["pdb_" + memObj.entryId.rjust(8, "0")];

  // patches
  if (
    memObj.entryId === "7ed1" &&
    mmjson.chem_comp?.id.indexOf("MET") === -1
  ) {
    patch(mmjson.chem_comp!, {
      id: "MET",
      type: "L-peptide linking",
      mon_nstd_flag: "y",
      name: "METHIONINE",
      formula: "C5 H11 N O2 S",
      formula_weight: 149.211,
    });
  }
}

function patch(
  category: Record<string, unknown[]>,
  data: Record<string, unknown>
): void {
  for (const k of Object.keys(category))
    category[k].push(data[k] !== undefined ? data[k] : null);
}

interface BUAssembly {
  [assemblyId: string]: [string[], string[]][];
}

function calculateMW4BU(pdbxData: PDBJMMJson): number {
  // Cast categories to any for flexible access
  const BUassemblies: BUAssembly = {};
  let length: number;
  try {
    length = pdbxData.pdbx_struct_assembly_gen!.assembly_id.length;
  } catch {
    length = 0;
  }

  let tmp: string[];
  let tmp1: string[][];
  let tmp2: (string | number)[];
  let j: number;
  let k: number;
  let mats: (string | number)[];

  const xpnd = function (inp: string): (string | number)[] {
    tmp2 = [];
    const parts = inp.split(",");
    for (j = 0; j < parts.length; j++) {
      if (parts[j].indexOf("-") !== -1) {
        const range = parts[j].replace("(", "").replace(")", "").split("-");
        for (k = parseInt(range[0]); k < parseInt(range[1]) + 1; k++) tmp2.push(k);
      } else tmp2.push(parts[j].replace("(", "").replace(")", ""));
    }
    return tmp2;
  };

  for (let i = 0; i < length; i++) {
    if (
      !Object.prototype.hasOwnProperty.call(
        BUassemblies,
        pdbxData.pdbx_struct_assembly_gen!.assembly_id[i]
      )
    )
      BUassemblies[pdbxData.pdbx_struct_assembly_gen!.assembly_id[i]] = [];

    mats = [];
    if (pdbxData.pdbx_struct_assembly_gen!.oper_expression[i].indexOf(")(") !== -1) {
      tmp1 = pdbxData.pdbx_struct_assembly_gen!.oper_expression[i].split(")(") as unknown as string[][];
      tmp = (tmp1[0] as unknown as string).slice(1) as unknown as string[];
      tmp1[0] = xpnd(tmp as unknown as string) as unknown as string[];
      tmp = (tmp1[1] as unknown as string).slice(0, (tmp1[1] as unknown as string).length - 1) as unknown as string[];
      tmp1[1] = xpnd(tmp as unknown as string) as unknown as string[];
      for (j = 0; j < tmp1[0].length; j++)
        for (k = 0; k < tmp1[1].length; k++) mats.push(tmp1[0][j] + "-" + tmp1[1][k]);
    } else mats = xpnd(pdbxData.pdbx_struct_assembly_gen!.oper_expression[i]);
    BUassemblies[pdbxData.pdbx_struct_assembly_gen!.assembly_id[i]].push([
      mats as string[],
      pdbxData.pdbx_struct_assembly_gen!.asym_id_list[i].split(","),
    ]);
  }

  let assembly_id: string | null = null;

  if (pdbxData.pdbx_struct_assembly) {
    const tst = pdbxData.pdbx_struct_assembly || { details: [] as string[] };
    for (let i = 0; i < tst.details.length; i++) {
      if (tst.details[i].substring(0, 19) === "author_and_software") {
        assembly_id = tst.id[i];
        break;
      }
    }
    if (assembly_id === null) {
      for (let i = 0; i < tst.details.length; i++) {
        if (tst.details[i].substring(0, 6) === "author") {
          assembly_id = tst.id[i];
          break;
        }
      }
    }
    if (assembly_id === null) {
      for (let i = 0; i < tst.details.length; i++) {
        if (tst.details[i].substring(0, 8) === "software") {
          assembly_id = tst.id[i];
          break;
        }
      }
    }
  }

  if (assembly_id === null) {
    const sinfo: Record<string, number> = {};
    const norInfo: Record<string, number> = {};
    if (pdbxData.entity_poly && pdbxData.entity_poly.entity_id) {
      for (let i = 0; i < pdbxData.entity_poly.entity_id.length; i++)
        sinfo[pdbxData.entity_poly.entity_id[i]] = pdbxData.entity_poly.pdbx_seq_one_letter_code_can[i]
          .replace(/\s/g, "").length;
    }
    if (pdbxData.struct_asym) {
      for (let i = 0; i < pdbxData.struct_asym.id.length; i++)
        norInfo[pdbxData.struct_asym.id[i]] =
          sinfo[pdbxData.struct_asym.entity_id[i]] || 0;
    }

    const largest: [string | null, number] = [null, 0];

    for (const aid in BUassemblies) {
      let sz = 0;
      if (isNaN(parseInt(aid, 10))) continue;
      for (let i = 0; i < BUassemblies[aid].length; i++) {
        let nor = 0;
        for (let j2 = 0; j2 < BUassemblies[aid][i][1].length; j2++)
          nor += norInfo[BUassemblies[aid][i][1][j2]] || 0;
        sz += BUassemblies[aid][i][0].length * nor;
      }
      if (sz > largest[1]) {
        largest[0] = aid;
        largest[1] = sz;
      }
    }
    if (largest[0] !== null) assembly_id = largest[0];
  }

  if (assembly_id === null) return 0.0;

  const poly_asym_ids: string[] = [];
  if (pdbxData.entity_poly && pdbxData.struct_asym) {
    const poly = pdbxData.entity_poly.entity_id;
    for (let i = 0; i < pdbxData.struct_asym.id.length; i++) {
      if (poly.indexOf(pdbxData.struct_asym.entity_id[i]) !== -1)
        poly_asym_ids.push(pdbxData.struct_asym.id[i]);
    }
  }

  const asym2mw: Record<string, number> = {};
  if (pdbxData.struct_asym && pdbxData.entity) {
    for (let c = 0; c < pdbxData.struct_asym.entity_id.length; c++)
      asym2mw[pdbxData.struct_asym.id[c]] =
        pdbxData.entity.formula_weight[
          pdbxData.entity.id.indexOf(pdbxData.struct_asym.entity_id[c])
        ];
  }

  let MW = 0;
  for (let i = 0; i < BUassemblies[assembly_id].length; i++) {
    let tmp3 = 0;
    let tmp4 = 0;
    for (let c = 0; c < BUassemblies[assembly_id][i][1].length; c++) {
      if (poly_asym_ids.indexOf(BUassemblies[assembly_id][i][1][c]) !== -1) tmp3++;
      tmp4 += asym2mw[BUassemblies[assembly_id][i][1][c]] || 0;
    }
    MW += tmp4 * BUassemblies[assembly_id][i][0].length;
  }

  if (assembly_id === "-1" && pdbxData.entry)
    console.log(pdbxData.entry.pdbid, MW);

  return MW;
}

export async function load_data(
  payload: PDBJPayload,
  _config: Config
): Promise<PDBJMMJson> {
  const mmjson = JSON.parse(
    (await general.gunzip(await fsp.readFile(payload.path))).toString()
  ) as PDBJMMJson;
  if (payload.pathPlus)
    Object.assign(
      mmjson,
      JSON.parse(
        (await general.gunzip(await fsp.readFile(payload.pathPlus))).toString()
      )
    );
  return mmjson;
}
