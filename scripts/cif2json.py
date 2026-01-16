#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "gemmi>=0.7.4",
#     "tqdm>=4.66",
# ]
# ///

"""
Convert CIF files to mmJSON format using gemmi.
Supports parallel processing and gzip compression.
"""

import argparse
import gzip
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import gemmi
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def convert_file(args: tuple[str, str]) -> tuple[str, bool, str]:
    """
    Convert a single CIF file to JSON.gz

    Args:
        args: Tuple of (cif_path, output_dir)

    Returns:
        Tuple of (cif_path, success, error_message)
    """
    cif_path, output_dir = args

    try:
        # gemmi can read gzip files directly
        doc = gemmi.cif.read(cif_path) # type: ignore

        # Convert to mmJSON format
        json_str = doc.as_json(mmjson=True)

        # Generate output filename: xxxx_validation.cif.gz -> xxxx_validation.json.gz
        cif_filename = Path(cif_path).name
        json_filename = cif_filename.replace(".cif.gz", ".json.gz").replace(".cif", ".json")
        output_path = os.path.join(output_dir, json_filename)

        # Write gzipped JSON
        with gzip.open(output_path, "wt", encoding="utf-8") as f:
            f.write(json_str)

        return (cif_path, True, "")
    except Exception as e:
        return (cif_path, False, str(e))


def main():
    parser = argparse.ArgumentParser(description="Convert CIF files to mmJSON format using gemmi")
    parser.add_argument(
        "input_dir", help="Input directory containing CIF files (*.cif.gz or *.cif)"
    )
    parser.add_argument("output_dir", help="Output directory for JSON.gz files")
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=os.cpu_count(),
        help=f"Number of parallel jobs (default: {os.cpu_count()})",
    )
    parser.add_argument(
        "--pattern", default="**/*.cif.gz", help="File pattern to match (default: **/*.cif.gz)"
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Find all CIF files
    input_path = Path(args.input_dir)
    cif_files = list(input_path.glob(args.pattern))

    if not cif_files:
        logger.warning(f"No files found matching pattern '{args.pattern}' in {args.input_dir}")
        return

    logger.info(f"Found {len(cif_files)} files to convert")
    logger.info(f"Using {args.jobs} parallel workers")

    # Prepare arguments for parallel processing
    convert_args = [(str(f), args.output_dir) for f in cif_files]

    # Process files in parallel with progress bar
    success_count = 0
    error_count = 0
    errors: list[tuple[str, str]] = []

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(convert_file, arg) for arg in tqdm(convert_args, desc="Preparing", unit="file")]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting", unit="file"):
            cif_path, success, error_msg = future.result()
            if success:
                success_count += 1
            else:
                error_count += 1
                errors.append((cif_path, error_msg))

    # Report errors
    for cif_path, error_msg in errors:
        logger.error(f"Error processing {cif_path}: {error_msg}")

    logger.info("Conversion complete:")
    logger.info(f"  Success: {success_count}")
    if error_count > 0:
        logger.warning(f"  Errors: {error_count}")


if __name__ == "__main__":
    main()
