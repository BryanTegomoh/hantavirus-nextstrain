#!/usr/bin/env python3
"""Check staged repository content for common data-governance mistakes."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

BLOCKED_PATH_PARTS = {
    "data/raw",
    "data/private",
    "ingest/results",
    "ingest/data",
    "phylogenetic/results",
    "phylogenetic/auspice",
    "auspice",
}

BLOCKED_SUFFIXES = {
    ".zip",
    ".zst",
    ".gb",
    ".gbk",
}

SENSITIVE_MARKERS = [
    "patient" + "_name",
    "date" + "_of" + "_birth",
    "medical" + "_record" + "_number",
    "m" + "rn",
    "api" + "_key",
    "sec" + "ret",
    "token" + "=",
]


def git_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    return [root / line for line in result.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    problems: list[str] = []

    for path in git_files(root):
        rel = path.relative_to(root).as_posix()
        if any(rel == part or rel.startswith(f"{part}/") for part in BLOCKED_PATH_PARTS):
            problems.append(f"blocked tracked path: {rel}")
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            problems.append(f"blocked tracked file type: {rel}")
        if path.is_file() and path.stat().st_size < 1_000_000:
            text = path.read_text(errors="ignore").lower()
            for marker in SENSITIVE_MARKERS:
                if marker in text:
                    problems.append(f"sensitive marker '{marker}' in {rel}")

    if problems:
        raise SystemExit("\n".join(problems))

    print("Repository safety check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
