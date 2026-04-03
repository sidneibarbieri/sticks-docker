#!/usr/bin/env python3
"""
Synchronize Paper 1 values.tex from the Docker-boundary measurement pipeline.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MEASUREMENT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = MEASUREMENT_ROOT.parent.parent
PAPER1_MAIN = WORKSPACE_ROOT / "ACM CCS - Paper 1" / "main.tex"
PAPER1_VALUES = WORKSPACE_ROOT / "ACM CCS - Paper 1" / "results" / "values.tex"
ANALYSIS_CMD = [
    "python3",
    str(MEASUREMENT_ROOT / "scripts" / "analyze_campaigns.py"),
    "--bundle",
    str(WORKSPACE_ROOT / "sticks" / "data" / "stix" / "enterprise-attack.json"),
    "--output-latex",
]
OUTPUT_JSON = MEASUREMENT_ROOT / "results" / "paper1_manuscript_values_sync.json"
OUTPUT_MD = MEASUREMENT_ROOT / "results" / "PAPER1_MANUSCRIPT_VALUES_SYNC.md"


def display_path(path: Path) -> str:
    for root in (WORKSPACE_ROOT, MEASUREMENT_ROOT):
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            pass
    return path.as_posix()


@dataclass
class SyncResult:
    status: str
    details: str
    macros_written: int = 0


def extract_macros(text: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"\\newcommand\{\\([A-Za-z][A-Za-z0-9]+)\}\{([^}]*)\}",
            text,
        )
    }


def extract_used_macros(text: str) -> set[str]:
    return set(re.findall(r"\\([A-Za-z][A-Za-z0-9]+)", text))


def sync_values(
    manuscript_values_path: Path,
    dry_run: bool,
) -> SyncResult:
    completed = subprocess.run(
        ANALYSIS_CMD,
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    generated_values_text = completed.stdout
    generated_macros = extract_macros(generated_values_text)
    paper_main_text = PAPER1_MAIN.read_text(encoding="utf-8")
    current_text = manuscript_values_path.read_text(encoding="utf-8")
    current_defined_macros = set(extract_macros(current_text))
    missing_manuscript_macros = sorted(
        (extract_used_macros(paper_main_text) & current_defined_macros) - set(generated_macros)
    )
    if missing_manuscript_macros:
        return SyncResult(
            status="blocked",
            details=(
                "Paper 1 still uses macros that are absent from "
                "sticks-docker/measurement/scripts/analyze_campaigns.py output: "
                + ", ".join(missing_manuscript_macros)
            ),
            macros_written=0,
        )

    if not dry_run:
        manuscript_values_path.write_text(generated_values_text, encoding="utf-8")
        status = "updated" if current_text != generated_values_text else "current"
        details = (
            "Paper 1 values.tex replaced from the Docker-boundary analyze_campaigns.py output."
            if current_text != generated_values_text
            else "Paper 1 values.tex already matched the Docker-boundary analyze_campaigns.py output."
        )
    else:
        status = "dry_run"
        details = "Paper 1 sync checked against the Docker-boundary analyze_campaigns.py output."

    return SyncResult(
        status=status,
        details=details,
        macros_written=len(generated_macros),
    )


def write_report(result: SyncResult) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(),
        "result": result.__dict__,
        "manuscript_values_path": display_path(PAPER1_VALUES),
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Paper 1 Manuscript Values Sync",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Status: `{result.status}`",
        f"- Macros written: `{result.macros_written}`",
        f"- Details: {result.details}",
        f"- Manuscript values path: `{display_path(PAPER1_VALUES)}`",
        "",
    ]
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--manuscript-values",
        default=str(PAPER1_VALUES),
        help="Path to the Paper 1 values.tex file to update.",
    )
    args = parser.parse_args()

    result = sync_values(
        manuscript_values_path=Path(args.manuscript_values),
        dry_run=args.dry_run,
    )
    write_report(result)

    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    if result.status == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
