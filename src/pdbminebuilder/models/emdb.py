"""SQLAlchemy schema definition for emdb."""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData(schema="emdb")
metadata.info = {"entry_pk": "emdb_id"}


brief_summary = Table(
    "brief_summary",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("docid", BigInteger, nullable=True),
    Column("deposition_date", Date, nullable=True),
    Column("header_release_date", Date, nullable=True),
    Column("map_release_date", Date, nullable=True),
    Column("modification_date", Date, nullable=True),
    Column("update_date", DateTime, nullable=True),
    Column("content", JSONB, nullable=True),
    Column("keywords", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("emdb_id"),
)

audit_conform = Table(
    "audit_conform",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("dict_location", Text, nullable=True, comment="A file name or uniform resource locator (URL) for the dictionary to which the current data block conforms."),
    Column("dict_name", Text, nullable=True, comment="The string identifying the highest-level dictionary defining data names used in this file."),
    Column("dict_version", Text, nullable=True, comment="The version number of the dictionary to which the current data block conforms."),
    PrimaryKeyConstraint("emdb_id", "dict_name", "dict_version"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["dict_location", "dict_name", "dict_version"]},
)

chem_comp = Table(
    "chem_comp",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("formula", Text, nullable=True, comment="The formula for the chemical component. Formulae are written according to the following rules: (1) Only recognized element symbols may be used. (2) Each element symbol is followed by a 'count' number. A count of '1' may be omitted. (3) A space or parenthesis must separate each cluster of (element symbol + count), but in general parentheses are not used. (4) The order of elements depends on whether carbon is present or not. If carbon is present, the order should be: C, then H, then the other elements in alphabetical order of their symbol. If carbon is not present, the elements are listed purely in alphabetic order of their symbol. This is the 'Hill' system used by Chemical Abstracts."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the chemical component."),
    Column("id", Text, nullable=True, comment="The value of _chem_comp.id must uniquely identify each item in the CHEM_COMP list. For protein polymer entities, this is the three-letter code for the amino acid. For nucleic acid polymer entities, this is the one-letter code for the base."),
    Column("mon_nstd_flag", Text, nullable=True, comment="'yes' indicates that this is a 'standard' monomer, 'no' indicates that it is 'nonstandard'. Nonstandard monomers should be described in more detail using the _chem_comp.mon_nstd_parent, _chem_comp.mon_nstd_class and _chem_comp.mon_nstd_details data items."),
    Column("name", Text, nullable=True, comment="The full name of the component."),
    Column("type", Text, nullable=True, comment="For standard polymer components, the type of the monomer. Note that monomers that will form polymers are of three types: linking monomers, monomers with some type of N-terminal (or 5') cap and monomers with some type of C-terminal (or 3') cap."),
    Column("pdbx_synonyms", Text, nullable=True, comment="Synonym list for the component."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "formula",
            "model_details",
            "model_erf",
            "model_source",
            "mon_nstd_class",
            "mon_nstd_details",
            "name",
            "pdbx_synonyms",
            "pdbx_modification_details",
            "pdbx_subcomponent_list",
            "pdbx_model_coordinates_details",
            "pdbx_model_coordinates_db_code",
            "pdbx_ideal_coordinates_details",
            "pdbx_class_1",
            "pdbx_class_2",
            "pdbx_reserved_name",
            "pdbx_casnum",
            "pdbx_smiles",
        ]
    },
)

citation = Table(
    "citation",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("country", Text, nullable=True, comment="The country/region of publication; relevant for books and book chapters."),
    Column("id", Text, nullable=True, comment="The value of _citation.id must uniquely identify a record in the CITATION list. The _citation.id 'primary' should be used to indicate the citation that the author(s) consider to be the most pertinent to the contents of the data block. Note that this item need not be a number; it can be any unique identifier."),
    Column("journal_abbrev", Text, nullable=True, comment="Abbreviated name of the cited journal as given in the Chemical Abstracts Service Source Index."),
    Column("journal_id_ASTM", Text, nullable=True, comment="The American Society for Testing and Materials (ASTM) code assigned to the journal cited (also referred to as the CODEN designator of the Chemical Abstracts Service); relevant for journal articles."),
    Column("journal_id_CSD", Text, nullable=True, comment="The Cambridge Structural Database (CSD) code assigned to the journal cited; relevant for journal articles. This is also the system used at the Protein Data Bank (PDB)."),
    Column("journal_id_ISSN", Text, nullable=True, comment="The International Standard Serial Number (ISSN) code assigned to the journal cited; relevant for journal articles."),
    Column("journal_volume", Text, nullable=True, comment="Volume number of the journal cited; relevant for journal articles."),
    Column("page_first", Text, nullable=True, comment="The first page of the citation; relevant for journal articles, books and book chapters."),
    Column("page_last", Text, nullable=True, comment="The last page of the citation; relevant for journal articles, books and book chapters."),
    Column("title", Text, nullable=True, comment="The title of the citation; relevant for journal articles, books and book chapters."),
    Column("year", Integer, nullable=True, comment="The year of the citation; relevant for journal articles, books and book chapters."),
    Column("database_id_CSD", Text, nullable=True, comment="Identifier ('refcode') of the database record in the Cambridge Structural Database that contains details of the cited structure."),
    Column("pdbx_database_id_DOI", Text, nullable=True, comment="Document Object Identifier used by doi.org to uniquely specify bibliographic entry."),
    Column("pdbx_database_id_PubMed", Integer, nullable=True, comment="Ascession number used by PubMed to categorize a specific bibliographic entry."),
    Column("unpublished_flag", Text, nullable=True, comment="Flag to indicate that this citation will not be published."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "abstract",
            "abstract_id_CAS",
            "book_id_ISBN",
            "book_publisher",
            "book_publisher_city",
            "book_title",
            "country",
            "details",
            "journal_abbrev",
            "journal_id_ASTM",
            "journal_id_CSD",
            "journal_id_ISSN",
            "journal_full",
            "journal_issue",
            "journal_volume",
            "language",
            "page_first",
            "page_last",
            "title",
            "pdbx_database_id_patent",
        ]
    },
)

citation_author = Table(
    "citation_author",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("citation_id", Text, nullable=True, comment="This data item is a pointer to _citation.id in the CITATION category."),
    Column("name", Text, nullable=True, comment="Name of an author of the citation; relevant for journal articles, books and book chapters. The family name(s), followed by a comma and including any dynastic components, precedes the first name(s) or initial(s)."),
    Column("ordinal", Integer, nullable=True, comment="This data item defines the order of the author's name in the list of authors of a citation."),
    Column("identifier_ORCID", Text, nullable=True, comment="The Open Researcher and Contributor ID (ORCID)."),
    PrimaryKeyConstraint("emdb_id", "citation_id", "name", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, citation_id) -> citation(emdb_id, id)
    info={"keywords": ["name", "identifier_ORCID"]},
)

database_2 = Table(
    "database_2",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("database_id", Text, nullable=True, comment="An abbreviation that identifies the database."),
    Column("database_code", Text, nullable=True, comment="The code assigned by the database identified in _database_2.database_id."),
    Column("pdbx_database_accession", Text, nullable=True, comment="Extended accession code issued for for _database_2.database_code assigned by the database identified in _database_2.database_id."),
    Column("pdbx_DOI", Text, nullable=True, comment="Document Object Identifier (DOI) for this entry registered with http://crossref.org."),
    PrimaryKeyConstraint("emdb_id", "database_id", "database_code"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["database_code", "pdbx_DOI"]},
)

entity = Table(
    "entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="A description of special aspects of the entity."),
    Column("formula_weight", Double, nullable=True, comment="Formula mass in daltons of the entity."),
    Column("id", Text, nullable=True, comment="The value of _entity.id must uniquely identify a record in the ENTITY list. Note that this item need not be a number; it can be any unique identifier."),
    Column("src_method", Text, nullable=True, comment="The method by which the sample for the entity was produced. Entities isolated directly from natural sources (tissues, soil samples etc.) are expected to have further information in the ENTITY_SRC_NAT category. Entities isolated from genetically manipulated sources are expected to have further information in the ENTITY_SRC_GEN category."),
    Column("type", Text, nullable=True, comment="Defines the type of the entity. Polymer entities are expected to have corresponding ENTITY_POLY and associated entries. Non-polymer entities are expected to have corresponding CHEM_COMP and associated entries. Water entities are not expected to have corresponding entries in the ENTITY category."),
    Column("pdbx_description", Text, nullable=True, comment="A description of the entity. Corresponds to the compound name in the PDB format."),
    Column("pdbx_number_of_molecules", Integer, nullable=True, comment="A place holder for the number of molecules of the entity in the entry."),
    Column("pdbx_mutation", Text, nullable=True, comment="Details about any entity mutation(s)."),
    Column("pdbx_fragment", Text, nullable=True, comment="Entity fragment description(s)."),
    Column("pdbx_ec", Text, nullable=True, comment="Enzyme Commission (EC) number(s)"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "details",
            "pdbx_description",
            "pdbx_mutation",
            "pdbx_fragment",
            "pdbx_modification",
        ]
    },
)

entity_poly = Table(
    "entity_poly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("type", Text, nullable=True, comment="The type of the polymer."),
    Column("pdbx_seq_one_letter_code", Text, nullable=True, comment="Sequence of protein or nucleic acid polymer in standard one-letter codes of amino acids or nucleotides. Non-standard amino acids/nucleotides are represented by their Chemical Component Dictionary (CCD) codes in parenthesis. Deoxynucleotides are represented by the specially-assigned 2-letter CCD codes in parenthesis, with 'D' prefix added to their ribonucleotide counterparts. For hybrid polymer, each residue is represented by the code of its individual type. A cyclic polymer is represented in linear sequence from the chosen start to end. A for Alanine or Adenosine-5'-monophosphate C for Cysteine or Cytidine-5'-monophosphate D for Aspartic acid E for Glutamic acid F for Phenylalanine G for Glycine or Guanosine-5'-monophosphate H for Histidine I for Isoleucine or Inosinic Acid L for Leucine K for Lysine M for Methionine N for Asparagine or Unknown ribonucleotide O for Pyrrolysine P for Proline Q for Glutamine R for Arginine S for Serine T for Threonine U for Selenocysteine or Uridine-5'-monophosphate V for Valine W for Tryptophan Y for Tyrosine (DA) for 2'-deoxyadenosine-5'-monophosphate (DC) for 2'-deoxycytidine-5'-monophosphate (DG) for 2'-deoxyguanosine-5'-monophosphate (DT) for Thymidine-5'-monophosphate (MSE) for Selenomethionine (SEP) for Phosphoserine (TPO) for Phosphothreonine (PTR) for Phosphotyrosine (PCA) for Pyroglutamic acid (UNK) for Unknown amino acid (ACE) for Acetylation cap (NH2) for Amidation cap"),
    PrimaryKeyConstraint("emdb_id", "entity_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "type_details",
            "pdbx_strand_id",
            "pdbx_seq_one_letter_code",
            "pdbx_seq_one_letter_code_can",
            "pdbx_target_identifier",
            "pdbx_seq_one_letter_code_sample",
            "pdbx_N_terminal_seq_one_letter_code",
            "pdbx_C_terminal_seq_one_letter_code",
            "pdbx_seq_three_letter_code",
            "pdbx_seq_db_id",
        ]
    },
)

entry = Table(
    "entry",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="The value of _entry.id identifies the data block. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

exptl = Table(
    "exptl",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("method", Text, nullable=True, comment="The method used in the experiment."),
    PrimaryKeyConstraint("emdb_id", "entry_id", "method"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["absorpt_process_details", "details", "method_details"]},
)

struct_keywords = Table(
    "struct_keywords",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("text", Text, nullable=True, comment="Keywords describing this structure."),
    Column("pdbx_keywords", Text, nullable=True, comment="Terms characterizing the macromolecular structure."),
    Column("pdbx_details", Text, nullable=True, comment="Keywords describing this structure. This is constructed by the PROGRAM for the PDB KEYWRD record."),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["text", "pdbx_keywords", "pdbx_details"]},
)

struct_ref = Table(
    "struct_ref",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_code", Text, nullable=True, comment="The code for this entity or biological unit or for a closely related entity or biological unit in the named database."),
    Column("db_name", Text, nullable=True, comment="The name of the database containing reference information about this entity or biological unit."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("id", Text, nullable=True, comment="The value of _struct_ref.id must uniquely identify a record in the STRUCT_REF list. Note that this item need not be a number; it can be any unique identifier."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "biol_id",
            "db_code",
            "db_name",
            "details",
            "pdbx_seq_one_letter_code",
        ]
    },
)

pdbx_database_related = Table(
    "pdbx_database_related",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_name", Text, nullable=True, comment="The name of the database containing the related entry."),
    Column("details", Text, nullable=True, comment="A description of the related entry."),
    Column("db_id", Text, nullable=True, comment="The identifying code in the related database."),
    Column("content_type", Text, nullable=True, comment="The identifying content type of the related entry."),
    PrimaryKeyConstraint("emdb_id", "db_name", "db_id", "content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "db_id"]},
)

pdbx_entity_nonpoly = Table(
    "pdbx_entity_nonpoly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("comp_id", Text, nullable=True, comment="This data item is a pointer to _chem_comp.id in the CHEM_COMP category."),
    Column("name", Text, nullable=True, comment="A name for the non-polymer entity"),
    PrimaryKeyConstraint("emdb_id", "entity_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={"keywords": ["name"]},
)

entity_src_nat = Table(
    "entity_src_nat",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("common_name", Text, nullable=True, comment="The common name of the organism from which the entity was isolated."),
    Column("details", Text, nullable=True, comment="A description of special aspects of the organism from which the entity was isolated."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("genus", Text, nullable=True, comment="The genus of the organism from which the entity was isolated."),
    Column("strain", Text, nullable=True, comment="The strain of the organism from which the entity was isolated."),
    Column("tissue", Text, nullable=True, comment="The tissue of the organism from which the entity was isolated."),
    Column("pdbx_organism_scientific", Text, nullable=True, comment="Scientific name of the organism of the natural source."),
    Column("pdbx_variant", Text, nullable=True, comment="Identifies the variant."),
    Column("pdbx_cell_line", Text, nullable=True, comment="The specific line of cells."),
    Column("pdbx_atcc", Text, nullable=True, comment="Americal Tissue Culture Collection number."),
    Column("pdbx_cellular_location", Text, nullable=True, comment="Identifies the location inside (or outside) the cell."),
    Column("pdbx_organ", Text, nullable=True, comment="Organized group of tissues that carries on a specialized function."),
    Column("pdbx_cell", Text, nullable=True, comment="A particular cell type."),
    Column("pdbx_plasmid_details", Text, nullable=True, comment="Details about the plasmid."),
    Column("pdbx_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for entity_src_nat data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "common_name",
            "details",
            "genus",
            "species",
            "strain",
            "tissue",
            "tissue_fraction",
            "pdbx_organism_scientific",
            "pdbx_secretion",
            "pdbx_fragment",
            "pdbx_variant",
            "pdbx_cell_line",
            "pdbx_atcc",
            "pdbx_cellular_location",
            "pdbx_organ",
            "pdbx_organelle",
            "pdbx_cell",
            "pdbx_plasmid_name",
            "pdbx_plasmid_details",
            "pdbx_ncbi_taxonomy_id",
            "pdbx_culture_collection",
        ]
    },
)

entity_src_gen = Table(
    "entity_src_gen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("gene_src_common_name", Text, nullable=True, comment="The common name of the natural organism from which the gene was obtained."),
    Column("gene_src_details", Text, nullable=True, comment="A description of special aspects of the natural organism from which the gene was obtained."),
    Column("gene_src_genus", Text, nullable=True, comment="The genus of the natural organism from which the gene was obtained."),
    Column("gene_src_species", Text, nullable=True, comment="The species of the natural organism from which the gene was obtained."),
    Column("gene_src_strain", Text, nullable=True, comment="The strain of the natural organism from which the gene was obtained, if relevant."),
    Column("gene_src_tissue", Text, nullable=True, comment="The tissue of the natural organism from which the gene was obtained."),
    Column("pdbx_gene_src_gene", Text, nullable=True, comment="Identifies the gene."),
    Column("pdbx_gene_src_scientific_name", Text, nullable=True, comment="Scientific name of the organism."),
    Column("pdbx_gene_src_variant", Text, nullable=True, comment="Identifies the variant."),
    Column("pdbx_gene_src_cell_line", Text, nullable=True, comment="The specific line of cells."),
    Column("pdbx_gene_src_atcc", Text, nullable=True, comment="American Type Culture Collection tissue culture number."),
    Column("pdbx_gene_src_organ", Text, nullable=True, comment="Organized group of tissues that carries on a specialized function."),
    Column("pdbx_gene_src_cell", Text, nullable=True, comment="Cell type."),
    Column("pdbx_host_org_organ", Text, nullable=True, comment="Specific organ which expressed the molecule."),
    Column("pdbx_host_org_organelle", Text, nullable=True, comment="Specific organelle which expressed the molecule."),
    Column("pdbx_host_org_cellular_location", Text, nullable=True, comment="Identifies the location inside (or outside) the cell which expressed the molecule."),
    Column("pdbx_host_org_strain", Text, nullable=True, comment="The strain of the organism in which the entity was expressed."),
    Column("pdbx_description", Text, nullable=True, comment="Information on the source which is not given elsewhere."),
    Column("host_org_common_name", Text, nullable=True, comment="The common name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item be derived from _entity_src_gen_express.host_org_common_name or via _entity_src_gen_express.host_org_tax_id"),
    Column("host_org_details", Text, nullable=True, comment="A description of special aspects of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would derived from _entity_src_gen_express.host_org_details"),
    Column("plasmid_details", Text, nullable=True, comment="A description of special aspects of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.details of the construct pointed to from _entity_src_gen_express.plasmid_id."),
    Column("plasmid_name", Text, nullable=True, comment="The name of the plasmid that produced the entity in the host organism. Where full details of the protein production are available it would be expected that this item would be derived from _pdbx_construct.name of the construct pointed to from _entity_src_gen_express.plasmid_id."),
    Column("pdbx_host_org_variant", Text, nullable=True, comment="Variant of the organism used as the expression system. Where full details of the protein production are available it would be expected that this item be derived from entity_src_gen_express.host_org_variant or via _entity_src_gen_express.host_org_tax_id"),
    Column("pdbx_host_org_cell_line", Text, nullable=True, comment="A specific line of cells used as the expression system. Where full details of the protein production are available it would be expected that this item would be derived from entity_src_gen_express.host_org_cell_line"),
    Column("pdbx_host_org_atcc", Text, nullable=True, comment="Americal Tissue Culture Collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_culture_collection"),
    Column("pdbx_host_org_culture_collection", Text, nullable=True, comment="Culture collection of the expression system. Where full details of the protein production are available it would be expected that this item would be derived somehwere, but exactly where is not clear."),
    Column("pdbx_host_org_cell", Text, nullable=True, comment="Cell type from which the gene is derived. Where entity.target_id is provided this should be derived from details of the target."),
    Column("pdbx_host_org_scientific_name", Text, nullable=True, comment="The scientific name of the organism that served as host for the production of the entity. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_scientific_name or via _entity_src_gen_express.host_org_tax_id"),
    Column("pdbx_host_org_tissue", Text, nullable=True, comment="The specific tissue which expressed the molecule. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.host_org_tissue"),
    Column("pdbx_host_org_vector", Text, nullable=True, comment="Identifies the vector used. Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_clone.vector_name."),
    Column("pdbx_host_org_vector_type", Text, nullable=True, comment="Identifies the type of vector used (plasmid, virus, or cosmid). Where full details of the protein production are available it would be expected that this item would be derived from _entity_src_gen_express.vector_type."),
    Column("pdbx_gene_src_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the gene source organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_host_org_ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier for the expression system organism. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for entity_src_gen data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_seq_type", Text, nullable=True, comment="This data item povides additional information about the sequence type."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "gene_src_common_name",
            "gene_src_details",
            "gene_src_genus",
            "gene_src_species",
            "gene_src_strain",
            "gene_src_tissue",
            "gene_src_tissue_fraction",
            "host_org_genus",
            "host_org_species",
            "pdbx_gene_src_fragment",
            "pdbx_gene_src_gene",
            "pdbx_gene_src_scientific_name",
            "pdbx_gene_src_variant",
            "pdbx_gene_src_cell_line",
            "pdbx_gene_src_atcc",
            "pdbx_gene_src_organ",
            "pdbx_gene_src_organelle",
            "pdbx_gene_src_plasmid",
            "pdbx_gene_src_plasmid_name",
            "pdbx_gene_src_cell",
            "pdbx_gene_src_cellular_location",
            "pdbx_host_org_gene",
            "pdbx_host_org_organ",
            "pdbx_host_org_organelle",
            "pdbx_host_org_cellular_location",
            "pdbx_host_org_strain",
            "pdbx_host_org_tissue_fraction",
            "pdbx_description",
            "host_org_common_name",
            "host_org_details",
            "host_org_strain",
            "plasmid_details",
            "plasmid_name",
            "pdbx_host_org_variant",
            "pdbx_host_org_cell_line",
            "pdbx_host_org_atcc",
            "pdbx_host_org_culture_collection",
            "pdbx_host_org_cell",
            "pdbx_host_org_scientific_name",
            "pdbx_host_org_tissue",
            "pdbx_host_org_vector",
            "pdbx_host_org_vector_type",
            "gene_src_dev_stage",
            "pdbx_gene_src_ncbi_taxonomy_id",
            "pdbx_host_org_ncbi_taxonomy_id",
            "pdbx_gene_src_culture_collection",
        ]
    },
)

pdbx_entity_src_syn = Table(
    "pdbx_entity_src_syn",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="A description of special aspects of the source for the synthetic entity."),
    Column("organism_scientific", Text, nullable=True, comment="The scientific name of the organism from which the sequence of the synthetic entity was derived."),
    Column("organism_common_name", Text, nullable=True, comment="The common name of the organism from which the sequence of the synthetic entity was derived."),
    Column("strain", Text, nullable=True, comment="The strain of the organism from which the sequence of the synthetic entity was derived."),
    Column("ncbi_taxonomy_id", Text, nullable=True, comment="NCBI Taxonomy identifier of the organism from which the sequence of the synthetic entity was derived. Reference: Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Schuler GD, Tatusova TA, Rapp BA (2000). Database resources of the National Center for Biotechnology Information. Nucleic Acids Res 2000 Jan 1;28(1):10-4 Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA, Wheeler DL (2000). GenBank. Nucleic Acids Res 2000 Jan 1;28(1):15-18."),
    Column("entity_id", Text, nullable=True, comment="This data item is a pointer to _entity.id in the ENTITY category."),
    Column("pdbx_src_id", Integer, nullable=True, comment="This data item is an ordinal identifier for pdbx_entity_src_syn data records."),
    Column("pdbx_alt_source_flag", Text, nullable=True, comment="This data item identifies cases in which an alternative source modeled."),
    Column("pdbx_beg_seq_num", Integer, nullable=True, comment="The beginning polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    Column("pdbx_end_seq_num", Integer, nullable=True, comment="The ending polymer sequence position for the polymer section corresponding to this source. A reference to the sequence position in the entity_poly category."),
    PrimaryKeyConstraint("emdb_id", "entity_id", "pdbx_src_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_id) -> entity(emdb_id, id)
    info={
        "keywords": [
            "details",
            "organism_scientific",
            "organism_common_name",
            "strain",
            "ncbi_taxonomy_id",
        ]
    },
)

em_entity_assembly = Table(
    "em_entity_assembly",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("parent_id", Integer, nullable=True, comment="The parent of this assembly. This data item is an internal category pointer to _em_entity_assembly.id. By convention, the full assembly (top of hierarchy) is assigned parent id 0 (zero)."),
    Column("source", Text, nullable=True, comment="The type of source (e.g., natural source) for the component (sample or sample subcomponent)"),
    Column("type", Text, nullable=True, comment="The general type of the sample or sample subcomponent."),
    Column("name", Text, nullable=True, comment="The name of the sample or sample subcomponent."),
    Column("details", Text, nullable=True, comment="Additional details about the sample or sample subcomponent."),
    Column("synonym", Text, nullable=True, comment="Alternative name of the component."),
    Column("entity_id_list", Text, nullable=True, comment="macromolecules associated with this component, if defined as comma separated list of entity ids (integers)."),
    Column("chimera", Text, nullable=True, comment="An indication if an assembly is contains a chimeric polymer"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "type",
            "name",
            "details",
            "go_id",
            "ipr_id",
            "synonym",
            "oligomeric_details",
            "entity_id_list",
            "ebi_organism_scientific",
            "ebi_organism_common",
            "ebi_strain",
            "ebi_tissue",
            "ebi_cell",
            "ebi_organelle",
            "ebi_cellular_location",
            "ebi_expression_system",
            "ebi_expression_system_plasmid",
        ]
    },
)

em_virus_entity = Table(
    "em_virus_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("virus_type", Text, nullable=True, comment="The type of virus."),
    Column("virus_isolate", Text, nullable=True, comment="The isolate from which the virus was obtained."),
    Column("entity_assembly_id", Text, nullable=True, comment="This data item is a pointer to _em_virus_entity.id in the ENTITY_ASSEMBLY category."),
    Column("enveloped", Text, nullable=True, comment="Flag to indicate if the virus is enveloped or not."),
    Column("empty", Text, nullable=True, comment="Flag to indicate if the virus is empty or not."),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={
        "keywords": [
            "virus_host_category",
            "virus_host_species",
            "virus_host_growth_cell",
            "ictvdb_id",
            "details",
        ]
    },
)

em_sample_support = Table(
    "em_sample_support",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("film_material", Text, nullable=True, comment="The support material covering the em grid."),
    Column("grid_material", Text, nullable=True, comment="The name of the material from which the grid is made."),
    Column("grid_mesh_size", Integer, nullable=True, comment="The value of the mesh size (divisions per inch) of the em grid."),
    Column("grid_type", Text, nullable=True, comment="A description of the grid type."),
    Column("pretreatment", Text, nullable=True, comment="A description of the grid plus support film pretreatment."),
    Column("details", Text, nullable=True, comment="Any additional details concerning the sample support."),
    Column("specimen_id", Text, nullable=True, comment="This data item is a pointer to _em_sample_preparation.id in the EM_SPECIMEN category."),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["method", "grid_type", "pretreatment", "details"]},
)

em_buffer = Table(
    "em_buffer",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("specimen_id", Text, nullable=True, comment="pointer to _em_specimen.id"),
    Column("name", Text, nullable=True, comment="The name of the buffer."),
    Column("details", Text, nullable=True, comment="Additional details about the buffer."),
    Column("pH", Double, nullable=True, comment="The pH of the sample buffer."),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["name", "details"]},
)

em_vitrification = Table(
    "em_vitrification",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("specimen_id", Text, nullable=True, comment="This data item is a pointer to _em_specimen.id"),
    Column("cryogen_name", Text, nullable=True, comment="This is the name of the cryogen."),
    Column("humidity", Double, nullable=True, comment="Relative humidity (%) of air surrounding the specimen just prior to vitrification."),
    Column("temp", Double, nullable=True, comment="The vitrification temperature (in kelvin), e.g., temperature of the plunge instrument cryogen bath."),
    Column("chamber_temperature", Double, nullable=True, comment="The temperature (in kelvin) of the sample just prior to vitrification."),
    Column("instrument", Text, nullable=True, comment="The type of instrument used in the vitrification process."),
    Column("details", Text, nullable=True, comment="Any additional details relating to vitrification."),
    PrimaryKeyConstraint("emdb_id", "id", "specimen_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["method", "time_resolved_state", "details"]},
)

em_imaging = Table(
    "em_imaging",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("residual_tilt", Double, nullable=True, comment="Residual tilt of the electron beam (in miliradians)"),
    Column("sample_support_id", Text, nullable=True, comment="This data item is a pointer to _em_sample_support.id in the EM_SAMPLE_SUPPORT category."),
    Column("detector_id", Text, nullable=True, comment="The value of _em_imaging.detector_id must uniquely identify the type of detector used in the experiment."),
    Column("scans_id", Text, nullable=True, comment="The value of _em_imaging.scans_id must uniquely identify the image_scans used in the experiment."),
    Column("microscope_id", Text, nullable=True, comment="This data item is a pointer to _em_microscope.id in the EM_MICROSCOPE category."),
    Column("microscope_model", Text, nullable=True, comment="The name of the model of microscope."),
    Column("specimen_holder_model", Text, nullable=True, comment="The name of the model of specimen holder used during imaging."),
    Column("details", Text, nullable=True, comment="Any additional imaging details."),
    Column("date", Date, nullable=True, comment="Date (YYYY-MM-DD) of imaging experiment or the date at which a series of experiments began."),
    Column("accelerating_voltage", Integer, nullable=True, comment="A value of accelerating voltage (in kV) used for imaging."),
    Column("illumination_mode", Text, nullable=True, comment="The mode of illumination."),
    Column("mode", Text, nullable=True, comment="The mode of imaging."),
    Column("nominal_cs", Double, nullable=True, comment="The spherical aberration coefficient (Cs) in millimeters, of the objective lens."),
    Column("nominal_defocus_min", Double, nullable=True, comment="The minimum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("nominal_defocus_max", Double, nullable=True, comment="The maximum defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("calibrated_defocus_min", Double, nullable=True, comment="The minimum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("calibrated_defocus_max", Double, nullable=True, comment="The maximum calibrated defocus value of the objective lens (in nanometers) used to obtain the recorded images. Negative values refer to overfocus."),
    Column("nominal_magnification", Integer, nullable=True, comment="The magnification indicated by the microscope readout."),
    Column("calibrated_magnification", Integer, nullable=True, comment="The magnification value obtained for a known standard just prior to, during or just after the imaging experiment."),
    Column("electron_source", Text, nullable=True, comment="The source of electrons. The electron gun."),
    Column("recording_temperature_minimum", Double, nullable=True, comment="The specimen temperature minimum (kelvin) for the duration of imaging."),
    Column("recording_temperature_maximum", Double, nullable=True, comment="The specimen temperature maximum (kelvin) for the duration of imaging."),
    Column("alignment_procedure", Text, nullable=True, comment="The type of procedure used to align the microscope electron beam."),
    Column("c2_aperture_diameter", Double, nullable=True, comment="The open diameter of the c2 condenser lens, in microns."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key to the EM_SPECIMEN category"),
    Column("cryogen", Text, nullable=True, comment="Cryogen type used to maintain the specimen stage temperature during imaging in the microscope."),
    PrimaryKeyConstraint("emdb_id", "entry_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={
        "keywords": [
            "astigmatism",
            "electron_beam_tilt_params",
            "specimen_holder_type",
            "details",
            "electron_source",
            "energy_filter",
            "energy_window",
            "microscope_serial_number",
            "microscope_version",
        ]
    },
)

em_image_scans = Table(
    "em_image_scans",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="The value of _em_image_scans.id must uniquely identify the images scanned."),
    Column("scanner_model", Text, nullable=True, comment="The scanner model."),
    Column("sampling_size", Double, nullable=True, comment="The sampling step size (microns) set on the scanner."),
    Column("dimension_height", Integer, nullable=True, comment="Height of scanned image, in pixels"),
    Column("dimension_width", Integer, nullable=True, comment="Width of scanned image, in pixels"),
    Column("frames_per_image", Integer, nullable=True, comment="Total number of time-slice (movie) frames taken per image."),
    Column("image_recording_id", Text, nullable=True, comment="foreign key linked to _em_image_recording"),
    Column("used_frames_per_image", Text, nullable=True, comment="Range of time-slice (movie) frames used for the reconstruction."),
    PrimaryKeyConstraint("emdb_id", "id", "image_recording_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["details"]},
)

em_3d_reconstruction = Table(
    "em_3d_reconstruction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("method", Text, nullable=True, comment="The algorithm method used for the 3d-reconstruction."),
    Column("algorithm", Text, nullable=True, comment="The reconstruction algorithm/technique used to generate the map."),
    Column("details", Text, nullable=True, comment="Any additional details used in the 3d reconstruction."),
    Column("resolution", Double, nullable=True, comment="The final resolution (in angstroms) of the 3D reconstruction."),
    Column("resolution_method", Text, nullable=True, comment="The method used to determine the final resolution of the 3d reconstruction. The Fourier Shell Correlation criterion as a measure of resolution is based on the concept of splitting the (2D) data set into two halves; averaging each and comparing them using the Fourier Ring Correlation (FRC) technique."),
    Column("nominal_pixel_size", Double, nullable=True, comment="The nominal pixel size of the projection set of images in Angstroms."),
    Column("actual_pixel_size", Double, nullable=True, comment="The actual pixel size of the projection set of images in Angstroms."),
    Column("num_particles", Integer, nullable=True, comment="The number of 2D projections or 3D subtomograms used in the 3d reconstruction"),
    Column("num_class_averages", Integer, nullable=True, comment="The number of classes used in the final 3d reconstruction"),
    Column("fsc_type", Text, nullable=True, comment="Half-set refinement protocol (semi-independent or gold standard)"),
    Column("refinement_type", Text, nullable=True, comment="Indicates details on how the half-map used for resolution determination (usually by FSC) have been generated."),
    Column("image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("symmetry_type", Text, nullable=True, comment="The type of symmetry applied to the reconstruction"),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={
        "keywords": [
            "method",
            "algorithm",
            "details",
            "resolution_method",
            "magnification_calibration",
            "ctf_correction_method",
            "euler_angles_details",
            "software",
        ]
    },
)

em_3d_fitting = Table(
    "em_3d_fitting",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="The value of _em_3d_fitting.id must uniquely identify a fitting procedure of atomic coordinates into 3dem reconstructed map volume."),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry_id in the ENTRY category."),
    Column("method", Text, nullable=True, comment="The method used to fit atomic coordinates into the 3dem reconstructed map."),
    Column("target_criteria", Text, nullable=True, comment="The measure used to assess quality of fit of the atomic coordinates in the 3DEM map volume."),
    Column("details", Text, nullable=True, comment="Any additional details regarding fitting of atomic coordinates into the 3DEM volume, including data and considerations from other methods used in computation of the model."),
    Column("overall_b_value", Double, nullable=True, comment="The overall B (temperature factor) value for the 3d-em volume."),
    Column("ref_space", Text, nullable=True, comment="A flag to indicate whether fitting was carried out in real or reciprocal refinement space."),
    Column("ref_protocol", Text, nullable=True, comment="The refinement protocol used."),
    PrimaryKeyConstraint("emdb_id", "id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["method", "target_criteria", "software_name", "details"]},
)

em_3d_fitting_list = Table(
    "em_3d_fitting_list",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("3d_fitting_id", Text, nullable=True, comment="The value of _em_3d_fitting_list.3d_fitting_id is a pointer to _em_3d_fitting.id in the 3d_fitting category"),
    Column("pdb_entry_id", Text, nullable=True, comment="The PDB code for the entry used in fitting."),
    Column("pdb_chain_id", Text, nullable=True, comment="The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank."),
    Column("pdb_chain_residue_range", Text, nullable=True, comment="Residue range for the identified chain."),
    Column("details", Text, nullable=True, comment="Details about the model used in fitting."),
    Column("chain_id", Text, nullable=True, comment="The ID of the biopolymer chain used for fitting, e.g., A. Please note that only one chain can be specified per instance. If all chains of a particular structure have been used for fitting, this field can be left blank."),
    Column("chain_residue_range", Text, nullable=True, comment="The residue ranges of the initial model used in this fitting."),
    Column("source_name", Text, nullable=True, comment="This item identifies the resource of initial model used for refinement"),
    Column("type", Text, nullable=True, comment="This item describes the type of the initial model was generated"),
    Column("accession_code", Text, nullable=True, comment="This item identifies an accession code of the resource where the initial model is used"),
    Column("initial_refinement_model_id", Integer, nullable=True, comment="The value of _em_3d_fitting.initial_refinement_model_id itentifies the id in the _pdbx_initial_refinement_model"),
    PrimaryKeyConstraint("emdb_id", "id", "3d_fitting_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "accession_code"]},
)

em_helical_entity = Table(
    "em_helical_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("entity_assembly_id", Text, nullable=True, comment="The value of _em_helical_entity.entity_assembly_id identifies a particular assembly component. This data item is a pointer to _em_entity_assembly.id in the EM_ENTITY_ASSEMBLY category."),
    Column("image_processing_id", Text, nullable=True, comment="This data item is a pointer to _em_image_processing.id."),
    Column("details", Text, nullable=True, comment="Any other details regarding the helical assembly"),
    Column("axial_symmetry", Text, nullable=True, comment="Symmetry of the helical axis, either cyclic (Cn) or dihedral (Dn), where n>=1."),
    Column("angular_rotation_per_subunit", Double, nullable=True, comment="The angular rotation per helical subunit in degrees. Negative values indicate left-handed helices; positive values indicate right handed helices."),
    Column("axial_rise_per_subunit", Double, nullable=True, comment="The axial rise per subunit in the helical assembly."),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "hand"]},
)

em_experiment = Table(
    "em_experiment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("reconstruction_method", Text, nullable=True, comment="The reconstruction method used in the EM experiment."),
    Column("aggregation_state", Text, nullable=True, comment="The aggregation/assembly state of the imaged specimen."),
    Column("entity_assembly_id", Text, nullable=True, comment="Foreign key to the EM_ENTITY_ASSEMBLY category"),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["specimen_type"]},
)

em_single_particle_entity = Table(
    "em_single_particle_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id in the ENTRY category."),
    Column("id", Integer, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id."),
    Column("point_symmetry", Text, nullable=True, comment="Point symmetry symbol, either Cn, Dn, T, O, or I"),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_admin = Table(
    "em_admin",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("current_status", Text, nullable=True, comment="This data item indicates the current status of the EMDB entry."),
    Column("deposition_date", Date, nullable=True, comment="date of the entry deposition"),
    Column("deposition_site", Text, nullable=True, comment="entry deposition site"),
    Column("details", Text, nullable=True, comment="EMDB administration details"),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to _entry.id."),
    Column("last_update", Date, nullable=True, comment="date of last update to the file"),
    Column("map_release_date", Date, nullable=True, comment="date of map release for this entry"),
    Column("header_release_date", Date, nullable=True, comment="date of header information release for this entry"),
    Column("title", Text, nullable=True, comment="Title for the EMDB entry."),
    Column("process_site", Text, nullable=True, comment="The site where the file was deposited."),
    Column("composite_map", Text, nullable=True, comment="Indicates whether the authors have declared that this is a composite map deposition"),
    PrimaryKeyConstraint("emdb_id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["details", "title"]},
)

em_author_list = Table(
    "em_author_list",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("author", Text, nullable=True, comment="Author of the EMDB entry in PDB format: Taylor, T.J."),
    Column("identifier_ORCID", Text, nullable=True, comment="The Open Researcher and Contributor ID (ORCID)."),
    Column("ordinal", Integer, nullable=True, comment="ID 1 corresponds to the main author of the entry"),
    PrimaryKeyConstraint("emdb_id", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["author", "identifier_ORCID"]},
)

em_db_reference = Table(
    "em_db_reference",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("access_code", Text, nullable=True, comment="Unique identifier for a provided link."),
    Column("db_name", Text, nullable=True, comment="The name of the database containing the related entry."),
    Column("details", Text, nullable=True, comment="A description of the related entry."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("relationship", Text, nullable=True, comment="Indicates relationship of this entry with other entries in PDB and EMDB."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_db_reference_auxiliary = Table(
    "em_db_reference_auxiliary",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("link_type", Text, nullable=True, comment="Type of auxiliary data stored at the indicated link."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_obsolete = Table(
    "em_obsolete",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("date", Date, nullable=True, comment="Dated when the entry made obsolete the other entry"),
    Column("details", Text, nullable=True, comment="Description of the reason(s) for entry obsoletion"),
    Column("entry", Text, nullable=True, comment="Entry made obsolete"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "entry"]},
)

em_supersede = Table(
    "em_supersede",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entry", Text, nullable=True, comment="Newer entry that replaces this entry"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "entry"]},
)

em_entity_assembly_molwt = Table(
    "em_entity_assembly_molwt",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True, comment="A reference to em_entity_assembly.id which uniquely identifies one sample or sample subcomponent of the imaged specimen."),
    Column("experimental_flag", Text, nullable=True, comment="Identifies whether the given molecular weight was derived experimentally."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("units", Text, nullable=True, comment="Molecular weight units."),
    Column("value", Double, nullable=True, comment="The molecular weight of the sample or sample subcomponent"),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["method"]},
)

em_entity_assembly_naturalsource = Table(
    "em_entity_assembly_naturalsource",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cell", Text, nullable=True, comment="The cell type from which the component was obtained."),
    Column("cellular_location", Text, nullable=True, comment="The cellular location of the component."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to the assembly component defined in the EM ENTITY ASSEMBLY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id for the natural organism source of the component."),
    Column("organism", Text, nullable=True, comment="The scientific name of the source organism for the component"),
    Column("organelle", Text, nullable=True, comment="The organelle from which the component was obtained."),
    Column("organ", Text, nullable=True, comment="The organ of the organism from which the component was obtained."),
    Column("strain", Text, nullable=True, comment="The strain of the natural organism from which the component was obtained, if relevant."),
    Column("tissue", Text, nullable=True, comment="The tissue of the natural organism from which the component was obtained."),
    Column("details", Text, nullable=True, comment="Additional details describing this natural source."),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={
        "keywords": [
            "cell",
            "cellular_location",
            "organism",
            "organelle",
            "organ",
            "strain",
            "tissue",
            "details",
        ]
    },
)

em_entity_assembly_recombinant = Table(
    "em_entity_assembly_recombinant",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cell", Text, nullable=True, comment="The cell of the host organism from which the expressed component was obtained, if relevant."),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to the expressed component described in the EM ENTITY ASSEMBLY category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id of the expression host used to produce the component."),
    Column("organism", Text, nullable=True, comment="Expression system host organism used to produce the component."),
    Column("plasmid", Text, nullable=True, comment="The plasmid used to produce the component in the expression system."),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the expresed component was obtained, if relevant."),
    PrimaryKeyConstraint("emdb_id", "id", "entity_assembly_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["cell", "organism", "plasmid", "strain"]},
)

em_virus_natural_host = Table(
    "em_virus_natural_host",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to _em_entity_assembly.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy id for the natural host organism of the virus"),
    Column("organism", Text, nullable=True, comment="The host organism from which the virus was isolated."),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the virus was obtained, if relevant."),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_synthetic = Table(
    "em_virus_synthetic",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("entity_assembly_id", Text, nullable=True, comment="Pointer to _em_entity_assembly.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("organism", Text, nullable=True, comment="The host organism from which the virus was isolated."),
    Column("ncbi_tax_id", Integer, nullable=True, comment="The NCBI taxonomy ID of the host species from which the virus was isolated"),
    Column("strain", Text, nullable=True, comment="The strain of the host organism from which the virus was obtained, if relevant."),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["organism", "strain"]},
)

em_virus_shell = Table(
    "em_virus_shell",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("diameter", Double, nullable=True, comment="The value of the diameter (in angstroms) for this virus shell."),
    Column("entity_assembly_id", Text, nullable=True, comment="The value of _em_virus_shell.entity_assembly_id is a pointer to _em_entity_assembly.id category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("name", Text, nullable=True, comment="The name for this virus shell."),
    Column("triangulation", Integer, nullable=True, comment="The triangulation number, T, describes the organization of subunits within an icosahedron. T is defined as T= h^2 + h*k + k^2, where h and k are positive integers that define the position of the five-fold vertex on the original hexagonal net."),
    PrimaryKeyConstraint("emdb_id", "entity_assembly_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entity_assembly_id) -> em_entity_assembly(emdb_id, id)
    info={"keywords": ["name"]},
)

em_specimen = Table(
    "em_specimen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("concentration", Double, nullable=True, comment="The concentration (in milligrams per milliliter, mg/ml) of the complex in the sample."),
    Column("details", Text, nullable=True, comment="A description of any additional details of the specimen preparation."),
    Column("embedding_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been embedded."),
    Column("experiment_id", Text, nullable=True, comment="Pointer to _em_experiment.id."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("shadowing_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been shadowed."),
    Column("staining_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen has been stained."),
    Column("vitrification_applied", Boolean, nullable=True, comment="'YES' indicates that the specimen was vitrified by cryopreservation."),
    PrimaryKeyConstraint("emdb_id", "id", "experiment_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_embedding = Table(
    "em_embedding",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Staining procedure used in the specimen preparation."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("material", Text, nullable=True, comment="The embedding material."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM SPECIMEN category"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "material"]},
)

em_fiducial_markers = Table(
    "em_fiducial_markers",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("diameter", Double, nullable=True, comment="Diameter of the fiducial markers"),
    Column("em_tomography_specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM TOMOGRAPHY SPECIMEN category"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("manufacturer", Text, nullable=True, comment="Manufacturer source for the fiducial markers"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["manufacturer"]},
)

em_focused_ion_beam = Table(
    "em_focused_ion_beam",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("current", Double, nullable=True, comment="Current of the ion beam, in nanoamperes (nA)"),
    Column("details", Text, nullable=True, comment="Additional details about FIB milling"),
    Column("duration", Double, nullable=True, comment="Milling time in seconds"),
    Column("em_tomography_specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM TOMOGRAPHY SPECIMEN category"),
    Column("final_thickness", Integer, nullable=True, comment="Final sample thickness"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("initial_thickness", Integer, nullable=True, comment="Initial sample thickness"),
    Column("instrument", Text, nullable=True, comment="The instrument used for focused ion beam sectioning"),
    Column("ion", Text, nullable=True, comment="The ion source used to ablate the specimen"),
    Column("temperature", Integer, nullable=True, comment="Temperature of the sample during milling, in kelvins"),
    Column("voltage", Integer, nullable=True, comment="Voltage applied to the ion source, in kilovolts"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument", "ion"]},
)

em_grid_pretreatment = Table(
    "em_grid_pretreatment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("atmosphere", Text, nullable=True, comment="The atmosphere used for glow discharge of the em grid."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("pressure", Double, nullable=True, comment="Pressure of the glow discharge chamber, in pascals"),
    Column("sample_support_id", Text, nullable=True, comment="Pointer to EM SAMPLE SUPPORT"),
    Column("time", Integer, nullable=True, comment="Time period for glow discharge of the em grid, in seconds"),
    Column("type", Text, nullable=True, comment="Type of grid pretreatment"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["atmosphere"]},
)

em_ultramicrotomy = Table(
    "em_ultramicrotomy",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Additional details about the ultramicrotomy sample preparation"),
    Column("em_tomography_specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM TOMOGRAPHY SPECIMEN category"),
    Column("final_thickness", Integer, nullable=True, comment="Final thickness of the sectioned sample, in nanometers"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("instrument", Text, nullable=True, comment="Ultramicrotome instrument used for sectioning"),
    Column("temperature", Integer, nullable=True, comment="Temperature of the sample during microtome sectioning, in kelvins"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument"]},
)

em_high_pressure_freezing = Table(
    "em_high_pressure_freezing",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Additional details about high pressure freezing."),
    Column("em_tomography_specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM TOMOGRAPHY SPECIMEN category"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("instrument", Text, nullable=True, comment="The instrument used for high pressure freezing."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, em_tomography_specimen_id) -> em_tomography_specimen(emdb_id, id)
    info={"keywords": ["details", "instrument"]},
)

em_tomography_specimen = Table(
    "em_tomography_specimen",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("cryo_protectant", Text, nullable=True, comment="The type of cryo-protectant used during specimen preparation."),
    Column("details", Text, nullable=True, comment="Any additional details about specimen preparation."),
    Column("fiducial_markers", Text, nullable=True, comment="'YES' indicates that fiducial markers were used in the specimen preparation"),
    Column("high_pressure_freezing", Text, nullable=True, comment="'YES' indicates that high pressure freezing was used in the specimen preparation"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("sectioning", Text, nullable=True, comment="The type of sectioning performed during specimen preparation."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM SPECIMEN category"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["cryo_protectant", "details"]},
)

em_crystal_formation = Table(
    "em_crystal_formation",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("atmosphere", Text, nullable=True, comment="The type of atmosphere in which crystals were grown"),
    Column("details", Text, nullable=True, comment="Description of growth of a 2D, 3D, or helical crystal array."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("instrument", Text, nullable=True, comment="Instrument used to prepare the crystalline array"),
    Column("lipid_mixture", Text, nullable=True, comment="Description of the lipid mixture used for crystallization"),
    Column("lipid_protein_ratio", Double, nullable=True, comment="The molar ratio of lipid to protein in the crystallized sample"),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the em_specimen category"),
    Column("temperature", Integer, nullable=True, comment="The value of the temperature in kelvin used for growing the crystals."),
    Column("time", Integer, nullable=True, comment="Time period for array crystallization, in time unit indicated (min, hr, day, month, year)"),
    Column("time_unit", Text, nullable=True, comment="Time unit for array crystallization"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["atmosphere", "details", "instrument", "lipid_mixture"]},
)

em_staining = Table(
    "em_staining",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Staining procedure used in the specimen preparation."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("material", Text, nullable=True, comment="The staining material."),
    Column("specimen_id", Text, nullable=True, comment="Foreign key relationship to the EM SPECIMEN category"),
    Column("type", Text, nullable=True, comment="type of staining"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "material"]},
)

em_support_film = Table(
    "em_support_film",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("material", Text, nullable=True, comment="The support material covering the em grid."),
    Column("sample_support_id", Text, nullable=True, comment="Pointer to EM SAMPLE SUPPORT"),
    Column("thickness", Double, nullable=True, comment="Thickness of the support film, in angstroms"),
    Column("topology", Text, nullable=True, comment="The topology of the material from which the grid is made."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_buffer_component = Table(
    "em_buffer_component",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("buffer_id", Text, nullable=True, comment="Foreign key to the entry category."),
    Column("concentration", Double, nullable=True, comment="The concentration of the sample (arbitrary units)."),
    Column("concentration_units", Text, nullable=True, comment="Units for the sample concentration value."),
    Column("formula", Text, nullable=True, comment="formula for buffer component"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("name", Text, nullable=True, comment="name of the buffer component"),
    PrimaryKeyConstraint("emdb_id", "id", "buffer_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["concentration_units", "name"]},
)

em_diffraction = Table(
    "em_diffraction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("camera_length", Double, nullable=True, comment="The camera length (in millimeters). The camera length is the product of the objective focal length and the combined magnification of the intermediate and projector lenses when the microscope is operated in the diffraction mode."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="Foreign key to the EM_IMAGING category"),
    Column("tilt_angle_list", Text, nullable=True, comment="Comma-separated list of tilt angles (in degrees) used in the electron diffraction experiment."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["tilt_angle_list"]},
)

em_diffraction_shell = Table(
    "em_diffraction_shell",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("em_diffraction_stats_id", Text, nullable=True, comment="Pointer to EM CRYSTALLOGRAPHY STATS"),
    Column("fourier_space_coverage", Double, nullable=True, comment="Completeness of the structure factor data within this resolution shell, in percent"),
    Column("high_resolution", Double, nullable=True, comment="High resolution limit for this shell (angstroms)"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("low_resolution", Double, nullable=True, comment="Low resolution limit for this shell (angstroms)"),
    Column("multiplicity", Double, nullable=True, comment="Multiplicity (average number of measurements) for the structure factors in this resolution shell"),
    Column("num_structure_factors", Integer, nullable=True, comment="Number of measured structure factors in this resolution shell"),
    Column("phase_residual", Double, nullable=True, comment="Phase residual for this resolution shell, in degrees"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_diffraction_stats = Table(
    "em_diffraction_stats",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Any addition details about the structure factor measurements"),
    Column("fourier_space_coverage", Double, nullable=True, comment="Completeness of the structure factor data within the defined space group at the reported resolution (percent)."),
    Column("high_resolution", Double, nullable=True, comment="High resolution limit of the structure factor data, in angstroms"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="Pointer to _em_image_processing.id"),
    Column("num_intensities_measured", Integer, nullable=True, comment="Total number of diffraction intensities measured (before averaging)"),
    Column("num_structure_factors", Integer, nullable=True, comment="Number of structure factors obtained (merged amplitudes + phases)"),
    Column("overall_phase_error", Double, nullable=True, comment="Overall phase error in degrees"),
    Column("overall_phase_residual", Double, nullable=True, comment="Overall phase residual in degrees"),
    Column("phase_error_rejection_criteria", Text, nullable=True, comment="Criteria used to reject phases"),
    Column("r_merge", Double, nullable=True, comment="Rmerge value (percent)"),
    Column("r_sym", Double, nullable=True, comment="Rsym value (percent)"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "phase_error_rejection_criteria"]},
)

em_tomography = Table(
    "em_tomography",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("axis1_angle_increment", Double, nullable=True, comment="The angle increment of specimen tilting to obtain the recorded images (axis 1)."),
    Column("axis1_max_angle", Double, nullable=True, comment="The maximum angle at which the specimen was tilted to obtain recorded images (axis 1)."),
    Column("axis1_min_angle", Double, nullable=True, comment="The minimum angle at which the specimen was tilted to obtain recorded images (axis 1)."),
    Column("axis2_angle_increment", Double, nullable=True, comment="The angle increment of specimen tilting to obtain the recorded images (axis 2)."),
    Column("axis2_max_angle", Double, nullable=True, comment="The maximum angle at which the specimen was tilted to obtain recorded images (axis 2)."),
    Column("axis2_min_angle", Double, nullable=True, comment="The minimum angle at which the specimen was tilted to obtain recorded images (axis 2)."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="Foreign key to the EM IMAGING category"),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_image_recording = Table(
    "em_image_recording",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("average_exposure_time", Double, nullable=True, comment="The average exposure time for each image."),
    Column("avg_electron_dose_per_subtomogram", Double, nullable=True, comment="The average total electron dose received by the specimen for each subtomogram (electrons per square angstrom)."),
    Column("avg_electron_dose_per_image", Double, nullable=True, comment="The electron dose received by the specimen per image (electrons per square angstrom)."),
    Column("details", Text, nullable=True, comment="Any additional details about image recording."),
    Column("detector_mode", Text, nullable=True, comment="The detector mode used during image recording."),
    Column("film_or_detector_model", Text, nullable=True, comment="The detector type used for recording images. Usually film , CCD camera or direct electron detector."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="This data item the id of the microscopy settings used in the imaging."),
    Column("num_diffraction_images", Integer, nullable=True, comment="The number of diffraction images collected."),
    Column("num_grids_imaged", Integer, nullable=True, comment="Number of grids in the microscopy session"),
    Column("num_real_images", Integer, nullable=True, comment="The number of micrograph images collected."),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "film_or_detector_model"]},
)

em_imaging_optics = Table(
    "em_imaging_optics",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("chr_aberration_corrector", Text, nullable=True, comment="Chromatic aberration corrector information"),
    Column("energyfilter_lower", Text, nullable=True, comment="The energy filter range lower value in electron volts (eV) set by spectrometer."),
    Column("energyfilter_slit_width", Double, nullable=True, comment="The energy filter range slit width in electron volts (eV)."),
    Column("energyfilter_name", Text, nullable=True, comment="The type of energy filter spectrometer"),
    Column("energyfilter_upper", Text, nullable=True, comment="The energy filter range upper value in electron volts (eV) set by spectrometer."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("imaging_id", Text, nullable=True, comment="Foreign key to the EM IMAGING category"),
    Column("phase_plate", Text, nullable=True, comment="Phase plate information"),
    Column("sph_aberration_corrector", Text, nullable=True, comment="Spherical aberration corrector information"),
    Column("details", Text, nullable=True, comment="Details on the use of the phase plate"),
    PrimaryKeyConstraint("emdb_id", "id", "imaging_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": [
            "chr_aberration_corrector",
            "energyfilter_lower",
            "energyfilter_name",
            "energyfilter_upper",
            "phase_plate",
            "sph_aberration_corrector",
            "details",
        ]
    },
)

em_final_classification = Table(
    "em_final_classification",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("avg_num_images_per_class", Integer, nullable=True, comment="The average number of images per class in the final 2D/3D classification"),
    Column("details", Text, nullable=True, comment="Additional details about the final 2D/3D classification"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("num_classes", Integer, nullable=True, comment="The number of classes used in the final 2D/3D classification"),
    Column("type", Text, nullable=True, comment="Space (2D/3D) for the classification."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_start_model = Table(
    "em_start_model",
    metadata,
    Column("emdb_id", Text, nullable=True, comment="EMDB id of the map used as the startup model"),
    Column("details", Text, nullable=True, comment="Any additional details about generating the startup model"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("insilico_model", Text, nullable=True, comment="Description of the \"in silico\" model used to generate the startup model"),
    Column("orthogonal_tilt_angle1", Double, nullable=True, comment="Tilt angle for the 1st image set of the orthogonal tilt pairs"),
    Column("orthogonal_tilt_angle2", Double, nullable=True, comment="Tilt angle for the 2nd image set of the orthogonal tilt pairs"),
    Column("orthogonal_tilt_num_images", Integer, nullable=True, comment="number of images used to generate the orthogonal tilt startup model"),
    Column("other", Text, nullable=True, comment="Description of other method/source used to generate the startup model"),
    Column("pdb_id", Text, nullable=True, comment="PDB id of the model coordinates used to generate the startup model"),
    Column("random_conical_tilt_angle", Double, nullable=True, comment="Angular difference between the conical tilt images used to generate the startup model"),
    Column("random_conical_tilt_num_images", Integer, nullable=True, comment="number of images used to generate the random conical tilt startup model"),
    Column("type", Text, nullable=True, comment="Type of startup model (map density) used to initiate the reconstruction"),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={
        "keywords": ["details", "insilico_model", "other", "pdb_id"],
        "pkout": True,
    },
)

em_software = Table(
    "em_software",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("category", Text, nullable=True, comment="The purpose of the software."),
    Column("details", Text, nullable=True, comment="Details about the software used."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("fitting_id", Text, nullable=True, comment="pointer to _em_3d_fitting.id in the EM_3D_FITTING category."),
    Column("imaging_id", Text, nullable=True, comment="pointer to _em_imaging.id in the EM_IMAGING category."),
    Column("name", Text, nullable=True, comment="The name of the software package used, e.g., RELION. Depositors are strongly encouraged to provide a value in this field."),
    Column("version", Text, nullable=True, comment="The version of the software."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "name", "version"]},
)

em_euler_angle_assignment = Table(
    "em_euler_angle_assignment",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Any additional details about euler angle assignment"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("order", Text, nullable=True, comment="Stage of the reconstruction in which the angle assignments were made."),
    Column("proj_matching_angular_sampling", Double, nullable=True, comment="Angular sampling of projection matching"),
    Column("proj_matching_merit_function", Text, nullable=True, comment="Overall figure of merit for projection matching"),
    Column("proj_matching_num_projections", Integer, nullable=True, comment="Number of reference projections used for euler angle assignment"),
    Column("type", Text, nullable=True, comment="The procedure used to assigned euler angles."),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "proj_matching_merit_function"]},
)

em_ctf_correction = Table(
    "em_ctf_correction",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Any additional details about CTF correction"),
    Column("em_image_processing_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_PROCESSING category"),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("type", Text, nullable=True, comment="Type of CTF correction applied"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "type"]},
)

em_volume_selection = Table(
    "em_volume_selection",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Any additional details used for selecting volumes."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="The value of _em_volume_selection.image_processing_id points to the EM_IMAGE_PROCESSING category."),
    Column("method", Text, nullable=True, comment="The method used for selecting volumes."),
    Column("num_tomograms", Integer, nullable=True, comment="The number of tomograms used in the extraction/selection"),
    Column("num_volumes_extracted", Integer, nullable=True, comment="The number of volumes selected from the projection set of images."),
    Column("reference_model", Text, nullable=True, comment="Description of reference model used for volume selection"),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_3d_crystal_entity = Table(
    "em_3d_crystal_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("angle_alpha", Double, nullable=True, comment="Unit-cell angle alpha in degrees."),
    Column("angle_beta", Double, nullable=True, comment="Unit-cell angle beta in degrees."),
    Column("angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma in degrees."),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("length_a", Double, nullable=True, comment="Unit-cell length a in angstroms."),
    Column("length_b", Double, nullable=True, comment="Unit-cell length b in angstroms."),
    Column("length_c", Double, nullable=True, comment="Unit-cell length c in angstroms."),
    Column("space_group_name", Text, nullable=True, comment="Space group name."),
    Column("space_group_num", Integer, nullable=True, comment="Space group number."),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["space_group_name"]},
)

em_2d_crystal_entity = Table(
    "em_2d_crystal_entity",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("angle_gamma", Double, nullable=True, comment="Unit-cell angle gamma in degrees."),
    Column("c_sampling_length", Double, nullable=True, comment="Length used to sample the reciprocal lattice lines in the c-direction."),
    Column("image_processing_id", Text, nullable=True, comment="pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("entity_assembly_id", Text, nullable=True, comment="Corresponding key in _em_entity_assembly category."),
    Column("length_a", Double, nullable=True, comment="Unit-cell length a in angstroms."),
    Column("length_b", Double, nullable=True, comment="Unit-cell length b in angstroms."),
    Column("length_c", Double, nullable=True, comment="Thickness of 2D crystal"),
    Column("space_group_name_H-M", Text, nullable=True),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

em_image_processing = Table(
    "em_image_processing",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Method details."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_recording_id", Text, nullable=True, comment="Foreign key to the EM_IMAGE_RECORDING"),
    PrimaryKeyConstraint("emdb_id", "image_recording_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details"]},
)

em_particle_selection = Table(
    "em_particle_selection",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("details", Text, nullable=True, comment="Additional detail such as description of filters used, if selection was manual or automated, and/or template details."),
    Column("id", Text, nullable=True, comment="PRIMARY KEY"),
    Column("image_processing_id", Text, nullable=True, comment="The value of _em_particle_selection.image_processing_id points to the EM_IMAGE_PROCESSING category."),
    Column("num_particles_selected", BigInteger, nullable=True, comment="The number of particles selected from the projection set of images."),
    PrimaryKeyConstraint("emdb_id", "id", "image_processing_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["details", "method", "reference_model"]},
)

em_map = Table(
    "em_map",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("annotation_details", Text, nullable=True, comment="map annotation details"),
    Column("axis_order_fast", Text, nullable=True, comment="The map axis that corresponds to Columns. (CCP4 HEADER WORD 17 MAPC 1=x, 2=y, 3=z)"),
    Column("axis_order_medium", Text, nullable=True, comment="The map axis that corresponds to Rows. (CCP4 map header word 18 MAPR 1=x, 2=y, 3=z)"),
    Column("axis_order_slow", Text, nullable=True, comment="The map axis that corresponds to Sections. (CCP4 map header word 19 MAPS 1=x, 2=y, 3=z)"),
    Column("cell_a", Double, nullable=True, comment="Map unit cell length parameter a. (CCP4 map header word 11)"),
    Column("cell_b", Double, nullable=True, comment="Map unit cell length parameter b. (CCP4 map header word 12)"),
    Column("cell_c", Double, nullable=True, comment="Map unit cell length parameter c. (CCP4 map header word 13)"),
    Column("cell_alpha", Double, nullable=True, comment="Value of map unit cell angle parameter alpha in degrees. (CCP4 map header word 14)"),
    Column("cell_beta", Double, nullable=True, comment="Value of map unit cell angle parameter beta in degrees. (CCP4 map header word 15)"),
    Column("cell_gamma", Double, nullable=True, comment="Value of map unit cell angle parameter gamma in degrees. (CCP4 map header word 16)"),
    Column("contour_level", Double, nullable=True, comment="recommended contour level for viewing the map"),
    Column("contour_level_source", Text, nullable=True, comment="source of the recommended contour level"),
    Column("data_type", Text, nullable=True, comment="The map data_type describes the data structure of the map voxels. (CCP4 map header word 4 MODE) EMDB currently holds MODE=0,1,and 2 maps; the majority are MODE=2. MAPS with MODES other than 2 and 0 may not work in CCP4 programs. MODE = 0: 8 bits, density stored as a signed byte (-128 to 127, ISO/IEC 10967) MODE = 1: 16 bits, density stored as a signed integer (-32768 to 32767, ISO/IEC 10967) MODE = 2: 32 bits, density stored as a floating point number (IEEE 754)"),
    Column("dimensions_col", Integer, nullable=True, comment="The number of columns in the map. (CCP4 map header word 1 NC)"),
    Column("dimensions_row", Integer, nullable=True, comment="The number of rows in the map. (CCP4 map header word 2 NR)"),
    Column("dimensions_sec", Integer, nullable=True, comment="The number of sections in the map. (CCP4 map header word 3 NS)"),
    Column("endian_type", Text, nullable=True, comment="map file endian type"),
    Column("file", Text, nullable=True, comment="Map file name."),
    Column("format", Text, nullable=True, comment="map format"),
    Column("id", Integer, nullable=True, comment="PRIMARY KEY"),
    Column("partition", Integer, nullable=True, comment="Identifies the archive file partition number of any map file"),
    Column("entry_id", Text, nullable=True, comment="This data item is a pointer to the ENTRY category."),
    Column("label", Text, nullable=True, comment="text stored in the label field of the CCP4 map header (WORDS 57-256)"),
    Column("limit_col", Integer, nullable=True, comment="The final column position of the map relative to the Cartesian coordinate origin in voxel grid units. (derived = .origin_col + .dimensions_col -1)"),
    Column("limit_row", Integer, nullable=True, comment="The final row position of the map relative to the Cartesian coordinate origin in voxel grid units. (derived = .origin_row + .dimensions_row -1)"),
    Column("limit_sec", Integer, nullable=True, comment="The final section position of the map relative to the Cartesian coordinate origin in voxel grid units. (derived -- .origin_sec + .dimensions_sec -1)"),
    Column("origin_col", Integer, nullable=True, comment="The position of the first column of the map relative to the Cartesian coordinate origin in voxel grid units. (CCP4 map header word 5 NCSTART)"),
    Column("origin_row", Integer, nullable=True, comment="The position of the first row of the map relative to the Cartesian coordinate origin in voxel grid units. (CCP4 map header word 6 NRSTART)"),
    Column("origin_sec", Integer, nullable=True, comment="The position of the first section of the map relative to the Cartesian coordinate origin in voxel grid units. (CCP4 map header word 7 NSSTART)"),
    Column("pixel_spacing_x", Double, nullable=True, comment="The length in angstroms of one voxel along the X axis."),
    Column("pixel_spacing_y", Double, nullable=True, comment="The length in angstroms of one voxel along the Y axis."),
    Column("pixel_spacing_z", Double, nullable=True, comment="The length in angstroms of one voxel along the Z axis."),
    Column("size_kb", BigInteger, nullable=True, comment="map storage size in Kilobytes (before compression)"),
    Column("spacing_x", Integer, nullable=True, comment="The number of intervals per cell repeat in X. (CCP4 map header word 8 NX)"),
    Column("spacing_y", Integer, nullable=True, comment="The number of intervals per cell repeat in Y. (CCP4 map header word 9 NY)"),
    Column("spacing_z", Integer, nullable=True, comment="The number of intervals per cell repeat in Z. (CCP4 map header word 10 NZ)"),
    Column("statistics_average", Double, nullable=True, comment="Mean (average) density value of the map."),
    Column("statistics_maximum", Double, nullable=True, comment="Maximum density value of the map."),
    Column("statistics_minimum", Double, nullable=True, comment="Minimum density value of the map."),
    Column("statistics_std", Double, nullable=True, comment="The standard deviation of the map density values."),
    Column("symmetry_space_group", Integer, nullable=True, comment="The space group number for the map. The value is 1 unless the sample is crystalline. (CCP4 map header word 23 ISPG)"),
    Column("type", Text, nullable=True, comment="Map type"),
    PrimaryKeyConstraint("emdb_id", "id", "entry_id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, entry_id) -> entry(emdb_id, id)
    info={"keywords": ["annotation_details", "file", "original_file", "label"]},
)

pdbx_audit_revision_history = Table(
    "pdbx_audit_revision_history",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_history record."),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("major_revision", Integer, nullable=True, comment="The major version number of deposition release."),
    Column("minor_revision", Integer, nullable=True, comment="The minor version number of deposition release."),
    Column("revision_date", Date, nullable=True, comment="The release date of the revision"),
    Column("part_number", Integer, nullable=True, comment="The part number of the content_type file correspondng to this milestone file"),
    PrimaryKeyConstraint("emdb_id", "ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
)

pdbx_audit_revision_group = Table(
    "pdbx_audit_revision_group",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_group record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("group", Text, nullable=True, comment="The collection of categories updated with this revision."),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_revision_category = Table(
    "pdbx_audit_revision_category",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_category record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("category", Text, nullable=True, comment="The category updated in the pdbx_audit_revision_category record."),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_revision_details = Table(
    "pdbx_audit_revision_details",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_details record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("provider", Text, nullable=True, comment="The provider of the revision."),
    Column("type", Text, nullable=True, comment="A type classification of the revision"),
    Column("description", Text, nullable=True, comment="Additional details describing the revision."),
    Column("details", Text, nullable=True, comment="Further details describing the revision."),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
    info={"keywords": ["description", "details"]},
)

pdbx_audit_revision_item = Table(
    "pdbx_audit_revision_item",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("ordinal", Integer, nullable=True, comment="A unique identifier for the pdbx_audit_revision_item record."),
    Column("revision_ordinal", Integer, nullable=True, comment="A pointer to _pdbx_audit_revision_history.ordinal"),
    Column("data_content_type", Text, nullable=True, comment="The type of file that the pdbx_audit_revision_history record refers to."),
    Column("item", Text, nullable=True, comment="A high level explanation the author has provided for submitting a revision."),
    PrimaryKeyConstraint("emdb_id", "ordinal", "revision_ordinal", "data_content_type"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    # FK: (emdb_id, data_content_type, revision_ordinal) -> pdbx_audit_revision_history(emdb_id, data_content_type, ordinal)
)

pdbx_audit_support = Table(
    "pdbx_audit_support",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("funding_organization", Text, nullable=True, comment="The name of the organization providing funding support for the entry."),
    Column("country", Text, nullable=True, comment="The country/region providing the funding support for the entry."),
    Column("grant_number", Text, nullable=True, comment="The grant number associated with this source of support."),
    Column("details", Text, nullable=True, comment="Additional details regarding the funding of this entry"),
    Column("ordinal", Integer, nullable=True, comment="A unique sequential integer identifier for each source of support for this entry."),
    PrimaryKeyConstraint("emdb_id", "ordinal"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["funding_organization", "country", "grant_number", "details"]},
)

pdbx_initial_refinement_model = Table(
    "pdbx_initial_refinement_model",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("id", Integer, nullable=True, comment="A unique identifier for the starting model record."),
    Column("type", Text, nullable=True, comment="This item describes the type of the initial model was generated"),
    Column("source_name", Text, nullable=True, comment="This item identifies the resource of initial model used for refinement"),
    Column("accession_code", Text, nullable=True, comment="This item identifies an accession code of the resource where the initial model is used"),
    Column("details", Text, nullable=True, comment="A description of special aspects of the initial model"),
    PrimaryKeyConstraint("emdb_id", "id"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["accession_code", "details"]},
)

link_entry_pdbjplus = Table(
    "link_entry_pdbjplus",
    metadata,
    Column("emdb_id", Text, nullable=True),
    Column("db_name", Text, nullable=True),
    Column("db_accession", ARRAY(Text), nullable=True),
    PrimaryKeyConstraint("emdb_id", "db_name"),
    # FK: (emdb_id) -> brief_summary(emdb_id)
    info={"keywords": ["db_name"]},
)
