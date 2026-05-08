#!/usr/bin/env python3
"""Assign Orthohantavirus genome segments and write curated metadata."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

# Maps NCBI dataformat TSV human-readable column headers to our internal schema.
# Internal field names pass through unchanged, so this handles both raw NCBI
# output and already-normalized input.
NCBI_FIELD_MAP: dict[str, str] = {
    # Exact column headers produced by: dataformat tsv virus-genome
    "Accession": "accession",
    "Isolate Lineage": "strain",
    "Geographic Region": "_geo_region",  # continent-level fallback
    "Geographic Location": "_geo_location",  # parsed below
    "Isolate Collection date": "date",
    "Release date": "date_released",
    "Update date": "date_updated",
    "Length": "length",
    "Host Name": "host",
    "Submitter Names": "authors",
    "Source database": "sourcedb",
    "BioSample accession": "biosample_acc",
    "Submitter Affiliation": "submitter_affiliation",
    "Submitter Country": "submitter_country",
    "Isolate Lineage source": "isolate_lineage_source",
    "SRA Accessions": "sra_accs",
}


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    """Rename NCBI dataformat column headers to internal schema names."""
    out: dict[str, str] = {}
    for key, value in row.items():
        mapped = NCBI_FIELD_MAP.get(key, key)
        out[mapped] = value

    # NCBI Geographic Location format is "Country", "Country: Division",
    # or "Country: Division: Location". Parse country from this field; fall
    # back to Geographic Region (continent) only when Geographic Location is
    # absent.
    geo = out.pop("_geo_location", "").strip()
    geo_region = out.pop("_geo_region", "").strip()
    if geo:
        parts = [p.strip() for p in geo.split(":", 2)]
        out.setdefault("country", parts[0])
        out.setdefault("division", parts[1] if len(parts) > 1 else "")
        out.setdefault("location", parts[2] if len(parts) > 2 else "")
    else:
        out.setdefault("country", geo_region)
        out.setdefault("division", "")
        out.setdefault("location", "")

    # Normalize date separators (NCBI occasionally uses slashes)
    if "date" in out:
        out["date"] = out["date"].replace("/", "-")

    return out

SEGMENT_RANGES = {
    "s": (1200, 2300),
    "m": (3200, 4200),
    "l": (6000, 7000),
}

OUTPUT_COLUMNS = [
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


def date_precision(value: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return "day"
    if re.fullmatch(r"\d{4}-\d{2}", value):
        return "month"
    if re.fullmatch(r"\d{4}", value):
        return "year"
    if "XX" in value:
        parts = value.split("-")
        if len(parts) == 3 and parts[2] == "XX":
            return "month"
        if len(parts) >= 2 and parts[1] == "XX":
            return "year"
    return "unknown"


def assign_segment(row: dict[str, str]) -> tuple[str, str, str]:
    explicit = row.get("segment", "").strip().lower()
    if explicit in SEGMENT_RANGES:
        return explicit, "metadata", ""

    title = row.get("title", "")
    title_match = re.search(r"\bsegment\s+([sml])\b", title, flags=re.IGNORECASE)
    if title_match:
        return title_match.group(1).lower(), "title", ""

    try:
        length = int(row.get("length", ""))
    except ValueError:
        return "", "unassigned", "missing_or_invalid_length"

    matches = [
        segment
        for segment, (minimum, maximum) in SEGMENT_RANGES.items()
        if minimum <= length <= maximum
    ]
    if len(matches) == 1:
        return matches[0], "length", "segment_assigned_by_length"
    if len(matches) > 1:
        return "", "unassigned", "ambiguous_length"
    return "", "unassigned", "length_outside_expected_segment_ranges"


def curate_rows(rows: list[dict[str, str]], filter_segment: str | None) -> list[dict[str, str]]:
    curated = []
    for row in rows:
        segment, method, note = assign_segment(row)
        precision = date_precision(row.get("date", ""))
        qc_notes = [note] if note else []

        qc_status = "pass"
        if method == "length":
            qc_status = "warn"
        if method == "unassigned" or precision == "unknown":
            qc_status = "fail"
        if precision == "unknown":
            qc_notes.append("unknown_date_precision")

        output = {
            "accession": row.get("accession", ""),
            "strain": row.get("strain") or row.get("isolate") or row.get("accession", ""),
            "date": row.get("date", ""),
            "country": row.get("country", ""),
            "division": row.get("division", ""),
            "location": row.get("location", ""),
            "host": row.get("host", ""),
            "segment": segment,
            "length": row.get("length", ""),
            "authors": row.get("authors", ""),
            "date_released": row.get("date_released", ""),
            "date_updated": row.get("date_updated", ""),
            "segment_assignment_method": method,
            "date_precision": precision,
            "qc_status": qc_status,
            "qc_notes": ";".join(qc_notes) if qc_notes else ".",
        }

        if filter_segment and output["segment"] != filter_segment:
            continue
        curated.append(output)
    return curated


def read_metadata(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [normalize_row(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_metadata(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=OUTPUT_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--sequences", required=True, type=Path)
    parser.add_argument("--output-metadata", required=True, type=Path)
    parser.add_argument("--output-sequences", required=True, type=Path)
    parser.add_argument("--filter-segment", choices=sorted(SEGMENT_RANGES))
    args = parser.parse_args()

    rows = read_metadata(args.metadata)
    sequences = read_fasta(args.sequences)
    curated = curate_rows(rows, args.filter_segment)
    selected_ids = {row["accession"] for row in curated}
    selected_sequences = {name: seq for name, seq in sequences.items() if name in selected_ids}

    missing_sequences = selected_ids - set(selected_sequences)
    if missing_sequences:
        missing = ", ".join(sorted(missing_sequences))
        raise SystemExit(f"Missing FASTA records for metadata accessions: {missing}")

    write_metadata(curated, args.output_metadata)
    args.output_sequences.parent.mkdir(parents=True, exist_ok=True)
    write_fasta(selected_sequences, args.output_sequences)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
