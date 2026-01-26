"""Tests for SIFTS pipeline."""

import gzip
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mine2.pipelines.sifts import TTL_FILES, parse_ttl_file, load_ttl_file, run


class TestParseTtlFile:
    """Tests for parse_ttl_file function."""

    def test_parse_pfam(self, tmp_path: Path) -> None:
        """Parse Pfam TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
<https://rdf.wwpdb.org/pdb/102L/entity/1> rdfs:seeAlso pfam:PF00959 .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_pfam.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("101M", "1", "PF00042")
        assert results[1] == ("102L", "1", "PF00959")

    def test_parse_go(self, tmp_path: Path) -> None:
        """Parse GO TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix GO: <http://identifiers.org/go/GO:> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso GO:0004601 .
<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso GO:0005344 .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_go.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("101M", "1", "0004601")
        assert results[1] == ("101M", "1", "0005344")

    def test_parse_enzyme(self, tmp_path: Path) -> None:
        """Parse enzyme (EC) TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://rdf.wwpdb.org/pdb/1A2U/entity/1> rdfs:seeAlso <http://identifiers.org/ec-code/3.1.31.1> .
<https://rdf.wwpdb.org/pdb/9P4K/entity/1> rdfs:seeAlso <http://identifiers.org/ec-code/3.1.-.-> .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_enzyme.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("1A2U", "1", "3.1.31.1")
        assert results[1] == ("9P4K", "1", "3.1.-.-")

    def test_parse_taxonomy(self, tmp_path: Path) -> None:
        """Parse taxonomy TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tax: <http://identifiers.org/taxonomy/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso tax:9755 .
<https://rdf.wwpdb.org/pdb/10GS/entity/1> rdfs:seeAlso tax:9606 .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_taxonomy.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("101M", "1", "9755")
        assert results[1] == ("10GS", "1", "9606")

    def test_parse_uniprot_short(self, tmp_path: Path) -> None:
        """Parse UniProt short TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix up: <http://identifiers.org/uniprot/> .

<https://rdf.wwpdb.org/pdb/101M/entity_poly/1> rdfs:seeAlso up:P02185 .
<https://rdf.wwpdb.org/pdb/102L/entity_poly/1> rdfs:seeAlso up:P00720 .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_uniprot_short.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("101M", "1", "P02185")
        assert results[1] == ("102L", "1", "P00720")

    def test_parse_uniprot_segments(self, tmp_path: Path) -> None:
        """Parse UniProt full TTL content with residue ranges."""
        ttl_content = b"""@prefix sifts: <https://pdbj.org/schema/sifts.owl#> .

<https://rdf.wwpdb.org/pdb/101m/entity_poly/1#1,154> sifts:region_match <https://purl.uniprot.org/uniprot/P02185#1,154> .
<https://rdf.wwpdb.org/pdb/102l/entity_poly/1#1,40> sifts:region_match <https://purl.uniprot.org/uniprot/P00720#1,40> .
<https://rdf.wwpdb.org/pdb/102l/entity_poly/1#42,165> sifts:region_match <https://purl.uniprot.org/uniprot/P00720#41,164> .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_uniprot.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 3
        # (pdbid, entity_id, pdb_start, pdb_end, uniprot_id, uniprot_start, uniprot_end)
        assert results[0] == ("101m", "1", "1", "154", "P02185", "1", "154")
        assert results[1] == ("102l", "1", "1", "40", "P00720", "1", "40")
        assert results[2] == ("102l", "1", "42", "165", "P00720", "41", "164")

    def test_parse_pubmed(self, tmp_path: Path) -> None:
        """Parse PubMed TTL content."""
        ttl_content = b"""@prefix pdbr: <https://rdf.wwpdb.org/pdb/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix pubmed: <http://identifiers.org/pubmed/> .

pdbr:100D dcterms:references pubmed:7816639 .
pdbr:101D dcterms:references pubmed:7711020 .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_pubmed.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("100D", "7816639")
        assert results[1] == ("101D", "7711020")

    def test_parse_interpro(self, tmp_path: Path) -> None:
        """Parse InterPro TTL content."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso <http://identifiers.org/interpro/IPR000971> .
<https://rdf.wwpdb.org/pdb/102L/entity/1> rdfs:seeAlso <http://identifiers.org/interpro/IPR002196> .
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_interpro.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 2
        assert results[0] == ("101M", "1", "IPR000971")
        assert results[1] == ("102L", "1", "IPR002196")

    def test_parse_skips_non_matching_lines(self, tmp_path: Path) -> None:
        """Non-matching lines are skipped."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

# This is a comment
<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
# Another comment
"""
        filepath = tmp_path / "test.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        pattern = TTL_FILES["pdb_chain_pfam.ttl.gz"]["pattern"]
        results = list(parse_ttl_file(filepath, pattern))

        assert len(results) == 1
        assert results[0] == ("101M", "1", "PF00042")


class TestLoadTtlFile:
    """Tests for load_ttl_file function."""

    def test_load_pfam_file(self, tmp_path: Path) -> None:
        """Load Pfam TTL file into database."""
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
<https://rdf.wwpdb.org/pdb/102L/entity/1> rdfs:seeAlso pfam:PF00959 .
"""
        filepath = tmp_path / "pdb_chain_pfam.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        config = TTL_FILES["pdb_chain_pfam.ttl.gz"]

        with patch("mine2.pipelines.sifts.bulk_upsert") as mock_upsert:
            mock_upsert.return_value = (2, 0)

            inserted, updated = load_ttl_file(
                filepath, config, "sifts", "conninfo", batch_size=10
            )

            assert inserted == 2
            assert updated == 0
            mock_upsert.assert_called_once()

            # Verify the data passed to bulk_upsert
            call_args = mock_upsert.call_args
            assert call_args[0][0] == "conninfo"  # conninfo
            assert call_args[0][1] == "sifts"  # schema_name
            assert call_args[0][2] == "pdb_pfam"  # table
            assert call_args[0][3] == ["pdbid", "entity_id", "pfam_id"]  # columns

            # Check the data tuples
            data = call_args[0][4]
            assert len(data) == 2
            assert data[0] == ("101m", 1, "PF00042")  # pdbid lowercase, entity_id int
            assert data[1] == ("102l", 1, "PF00959")

    def test_load_pubmed_file(self, tmp_path: Path) -> None:
        """Load PubMed TTL file (different schema - no entity_id)."""
        ttl_content = b"""@prefix pdbr: <https://rdf.wwpdb.org/pdb/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix pubmed: <http://identifiers.org/pubmed/> .

pdbr:100D dcterms:references pubmed:7816639 .
pdbr:101D dcterms:references pubmed:7711020 .
"""
        filepath = tmp_path / "pdb_pubmed.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        config = TTL_FILES["pdb_pubmed.ttl.gz"]

        with patch("mine2.pipelines.sifts.bulk_upsert") as mock_upsert:
            mock_upsert.return_value = (2, 0)

            inserted, updated = load_ttl_file(
                filepath, config, "sifts", "conninfo", batch_size=10
            )

            assert inserted == 2
            call_args = mock_upsert.call_args
            data = call_args[0][4]
            assert data[0] == ("100d", 7816639)  # pubmed_id is int
            assert data[1] == ("101d", 7711020)

    def test_batching(self, tmp_path: Path) -> None:
        """Test that large files are processed in batches."""
        # Create TTL with 25 entries
        lines = [
            b"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n",
            b"@prefix pfam: <http://identifiers.org/pfam/> .\n\n",
        ]
        for i in range(25):
            pdbid = f"{i:04d}"
            lines.append(
                f"<https://rdf.wwpdb.org/pdb/{pdbid}/entity/1> rdfs:seeAlso pfam:PF{i:05d} .\n".encode()
            )

        filepath = tmp_path / "pdb_chain_pfam.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.writelines(lines)

        config = TTL_FILES["pdb_chain_pfam.ttl.gz"]

        with patch("mine2.pipelines.sifts.bulk_upsert") as mock_upsert:
            mock_upsert.return_value = (10, 0)

            inserted, updated = load_ttl_file(
                filepath, config, "sifts", "conninfo", batch_size=10
            )

            # Should be called 3 times: 10 + 10 + 5
            assert mock_upsert.call_count == 3
            assert inserted == 30  # 10 * 3


class TestTtlFilesConfig:
    """Tests for TTL_FILES configuration."""

    def test_all_files_have_required_keys(self) -> None:
        """All TTL file configs have required keys."""
        required_keys = {"table", "pattern", "columns", "pk"}

        for filename, config in TTL_FILES.items():
            assert required_keys <= set(config.keys()), f"{filename} missing keys"

    def test_pk_columns_subset_of_columns(self) -> None:
        """Primary key columns must be in columns list."""
        for filename, config in TTL_FILES.items():
            pk_set = set(config["pk"])
            col_set = set(config["columns"])
            assert pk_set <= col_set, (
                f"{filename}: pk {pk_set} not in columns {col_set}"
            )

    def test_patterns_are_valid_regex(self) -> None:
        """All patterns are valid regex."""
        import re

        for filename, config in TTL_FILES.items():
            try:
                re.compile(config["pattern"])
            except re.error as e:
                pytest.fail(f"{filename}: invalid regex - {e}")


class TestRun:
    """Tests for run function."""

    def test_run_with_missing_directory(self) -> None:
        """Run handles missing data directory."""
        mock_settings = MagicMock()
        mock_config = MagicMock()
        mock_config.data = "/nonexistent/path"
        mock_schema_def = MagicMock()
        mock_schema_def.schema_name = "sifts"

        results = run(mock_settings, mock_config, mock_schema_def)

        assert results == []

    def test_run_with_missing_file(self, tmp_path: Path) -> None:
        """Run handles missing TTL file gracefully."""
        mock_settings = MagicMock()
        mock_config = MagicMock()
        mock_config.data = str(tmp_path)
        mock_schema_def = MagicMock()
        mock_schema_def.schema_name = "sifts"

        results = run(mock_settings, mock_config, mock_schema_def)

        # All files should fail (not found)
        assert len(results) == len(TTL_FILES)
        assert all(not r.success for r in results)
        assert all("not found" in r.error for r in results)

    def test_run_processes_files(self, tmp_path: Path) -> None:
        """Run processes available TTL files."""
        # Create one valid TTL file
        ttl_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
"""
        filepath = tmp_path / "pdb_chain_pfam.ttl.gz"
        with gzip.open(filepath, "wb") as f:
            f.write(ttl_content)

        mock_settings = MagicMock()
        mock_settings.rdb.constring = "test_conninfo"
        mock_config = MagicMock()
        mock_config.data = str(tmp_path)
        mock_schema_def = MagicMock()
        mock_schema_def.schema_name = "sifts"

        with patch("mine2.pipelines.sifts.bulk_upsert") as mock_upsert:
            mock_upsert.return_value = (1, 0)

            results = run(mock_settings, mock_config, mock_schema_def)

        # One success, rest failures (not found)
        success_results = [r for r in results if r.success]
        assert len(success_results) == 1
        assert success_results[0].entry_id == "pdb_chain_pfam.ttl.gz"
        assert success_results[0].rows_inserted == 1

    def test_run_with_tables_filter(self, tmp_path: Path) -> None:
        """Run processes only specified tables."""
        # Create two valid TTL files
        pfam_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix pfam: <http://identifiers.org/pfam/> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso pfam:PF00042 .
"""
        go_content = b"""@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix GO: <http://identifiers.org/go/GO:> .

<https://rdf.wwpdb.org/pdb/101M/entity/1> rdfs:seeAlso GO:0004601 .
"""
        with gzip.open(tmp_path / "pdb_chain_pfam.ttl.gz", "wb") as f:
            f.write(pfam_content)
        with gzip.open(tmp_path / "pdb_chain_go.ttl.gz", "wb") as f:
            f.write(go_content)

        mock_settings = MagicMock()
        mock_settings.rdb.constring = "test_conninfo"
        mock_config = MagicMock()
        mock_config.data = str(tmp_path)
        mock_schema_def = MagicMock()
        mock_schema_def.schema_name = "sifts"

        with patch("mine2.pipelines.sifts.bulk_upsert") as mock_upsert:
            mock_upsert.return_value = (1, 0)

            # Only process pdb_pfam table
            results = run(
                mock_settings, mock_config, mock_schema_def, tables=["pdb_pfam"]
            )

        # Should only process 1 file (pdb_pfam), not all 10
        assert len(results) == 1
        assert results[0].entry_id == "pdb_chain_pfam.ttl.gz"
        assert results[0].success

    def test_run_with_invalid_table_filter(self, tmp_path: Path) -> None:
        """Run returns empty when no tables match filter."""
        mock_settings = MagicMock()
        mock_config = MagicMock()
        mock_config.data = str(tmp_path)
        mock_schema_def = MagicMock()
        mock_schema_def.schema_name = "sifts"

        results = run(
            mock_settings, mock_config, mock_schema_def, tables=["nonexistent_table"]
        )

        assert results == []
