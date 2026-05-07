#!/usr/bin/env python3
"""Validate curated metadata and FASTA concordance."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED_COLUMNS = [
    "accession",
    "strain",
    "date",
    "country",
    "division",
    "location",
    "host",
    "segment",
    "length",
    "authors",
    "date_released",
    "date_updated",
    "segment_assignment_method",
    "date_precision",
    "qc_status",
    "qc_notes",
]

VALID_SEGMENTS = {"s", "m", "l"}
VALID_QC_STATUS = {"pass", "warn", "fail"}


def read_fasta_ids(path: Path) -> set[str]:
    ids = set()
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            ids.add(line[1:].split()[0])
    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--sequences", type=Path)
    args = parser.parse_args()

    with args.metadata.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing:
            raise SystemExit(f"Missing required metadata columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise SystemExit("Metadata has no records")

    accessions = []
    for index, row in enumerate(rows, start=2):
        accession = row["accession"].strip()
        if not accession:
            raise SystemExit(f"Missing accession at metadata line {index}")
        accessions.append(accession)

        if row["segment"] not in VALID_SEGMENTS:
            raise SystemExit(f"Invalid segment for {accession}: {row['segment']}")
        if row["qc_status"] not in VALID_QC_STATUS:
            raise SystemExit(f"Invalid qc_status for {accession}: {row['qc_status']}")
        try:
            if int(row["length"]) <= 0:
                raise ValueError
        except ValueError:
            raise SystemExit(f"Invalid length for {accession}: {row['length']}") from None

    duplicates = sorted({accession for accession in accessions if accessions.count(accession) > 1})
    if duplicates:
        raise SystemExit(f"Duplicate accessions in metadata: {', '.join(duplicates)}")

    if args.sequences:
        fasta_ids = read_fasta_ids(args.sequences)
        metadata_ids = set(accessions)
        if fasta_ids != metadata_ids:
            missing_fasta = sorted(metadata_ids - fasta_ids)
            missing_metadata = sorted(fasta_ids - metadata_ids)
            details = []
            if missing_fasta:
                details.append(f"missing FASTA: {', '.join(missing_fasta)}")
            if missing_metadata:
                details.append(f"missing metadata: {', '.join(missing_metadata)}")
            raise SystemExit("; ".join(details))

    print(f"Validated {len(rows)} metadata records from {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
