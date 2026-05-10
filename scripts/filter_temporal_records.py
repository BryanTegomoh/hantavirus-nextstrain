#!/usr/bin/env python3
"""Filter curated metadata and FASTA records for temporal analyses."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_fasta(path: Path) -> dict[str, str]:
    records: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text().splitlines():
        if not line:
            continue
        if line.startswith(">"):
            current = line[1:].split()[0]
            records[current] = []
            continue
        if current is None:
            raise ValueError(f"Sequence line before FASTA header in {path}")
        records[current].append(line.strip())
    return {name: "".join(parts) for name, parts in records.items()}


def write_fasta(records: dict[str, str], path: Path) -> None:
    with path.open("w") as handle:
        for name, sequence in records.items():
            handle.write(f">{name}\n")
            for start in range(0, len(sequence), 80):
                handle.write(f"{sequence[start:start + 80]}\n")


def year_from_date(value: str) -> int | None:
    if len(value) < 4:
        return None
    year = value[:4]
    if not year.isdigit():
        return None
    return int(year)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--sequences", required=True, type=Path)
    parser.add_argument("--output-metadata", required=True, type=Path)
    parser.add_argument("--output-sequences", required=True, type=Path)
    parser.add_argument(
        "--date-precisions",
        default="day,month,year",
        help="Comma-separated date_precision values to keep.",
    )
    parser.add_argument("--min-year", type=int)
    parser.add_argument("--max-year", type=int)
    args = parser.parse_args()

    allowed_precisions = {
        precision.strip()
        for precision in args.date_precisions.split(",")
        if precision.strip()
    }
    sequences = read_fasta(args.sequences)

    with args.metadata.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    selected = []
    for row in rows:
        precision = row.get("date_precision", "")
        date = row.get("date", "")
        if precision not in allowed_precisions or not date:
            continue
        year = year_from_date(date)
        if year is None:
            continue
        if args.min_year is not None and year < args.min_year:
            continue
        if args.max_year is not None and year > args.max_year:
            continue
        selected.append(row)

    if not selected:
        raise SystemExit("No records passed temporal filtering")

    selected_ids = {row["accession"] for row in selected}
    selected_sequences = {
        name: sequence
        for name, sequence in sequences.items()
        if name in selected_ids
    }
    missing_sequences = selected_ids - set(selected_sequences)
    if missing_sequences:
        missing = ", ".join(sorted(missing_sequences))
        raise SystemExit(f"Missing FASTA records for metadata accessions: {missing}")

    args.output_metadata.parent.mkdir(parents=True, exist_ok=True)
    with args.output_metadata.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(selected)

    args.output_sequences.parent.mkdir(parents=True, exist_ok=True)
    write_fasta(selected_sequences, args.output_sequences)
    print(
        "Retained "
        f"{len(selected)} of {len(rows)} records with date_precision in "
        f"{','.join(sorted(allowed_precisions))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
