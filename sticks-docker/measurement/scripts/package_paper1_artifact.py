#!/usr/bin/env python3
"""
Create a paper-scoped review artifact for ACM CCS Paper 1.

The staged artifact preserves the frozen Docker-backed execution boundary while
excluding workspace residue, historical result archives, and reviewer-irrelevant
administrative material.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MEASUREMENT_ROOT = SCRIPT_DIR.parent
STICKS_DOCKER_ROOT = MEASUREMENT_ROOT.parent
REPO_ROOT = STICKS_DOCKER_ROOT.parent
PAPER1_ROOT = REPO_ROOT / "ACM CCS - Paper 1"
DEFAULT_DEST = REPO_ROOT / "artifacts" / "paper1-review-artifact"
PUBLISHED_REPOSITORY = "https://github.com/sidneibarbieri/sticks-docker"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dest: Path) -> None:
    ensure_parent(dest)
    shutil.copy2(src, dest)


def copy_text_with_repo_relativization(src: Path, dest: Path) -> None:
    ensure_parent(dest)
    text = src.read_text(encoding="utf-8")
    repo_prefix = str(REPO_ROOT) + "/"
    text = text.replace(repo_prefix, "")
    dest.write_text(text, encoding="utf-8")


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            ".pytest_cache",
            "*.pyc",
            ".DS_Store",
        ),
    )


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def empty_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def stage_paper(dest_root: Path) -> None:
    paper_dest = dest_root / "ACM CCS - Paper 1"
    keep_files = [
        "main.tex",
        "main.pdf",
        "references.bib",
        "acmart.cls",
        "ACM-Reference-Format.bst",
        "results/values.tex",
        "appendix_values.tex",
    ]
    for relative in keep_files:
        copy_file(PAPER1_ROOT / relative, paper_dest / relative)

    copy_tree(PAPER1_ROOT / "figures", paper_dest / "figures")


def stage_shared_bundle(dest_root: Path) -> None:
    copy_file(
        REPO_ROOT / "sticks" / "data" / "stix" / "enterprise-attack.json",
        dest_root / "sticks" / "data" / "stix" / "enterprise-attack.json",
    )
    for relative in ["build_manuscript.py", "check_paper_hygiene.py"]:
        copy_file(
            REPO_ROOT / "sticks" / "scripts" / relative,
            dest_root / "sticks" / "scripts" / relative,
        )


def stage_measurement_boundary(dest_root: Path) -> None:
    measurement_dest = dest_root / "sticks-docker" / "measurement"
    for relative in [
        "README.md",
        "requirements.txt",
        "release_check.sh",
        "run_full_docker_audit.sh",
    ]:
        copy_file(MEASUREMENT_ROOT / relative, measurement_dest / relative)

    copy_file(
        MEASUREMENT_ROOT / "runtime" / "README.md",
        measurement_dest / "runtime" / "README.md",
    )

    copy_tree(MEASUREMENT_ROOT / "scripts", measurement_dest / "scripts")
    copy_tree(MEASUREMENT_ROOT / "tests", measurement_dest / "tests")

    result_files = [
        "README.md",
        "paper1_values_provenance.json",
        "PAPER1_VALUES_PROVENANCE.md",
        "paper1_identifiability_provenance.json",
        "PAPER1_IDENTIFIABILITY_PROVENANCE.md",
        "paper1_robustness_provenance.json",
        "PAPER1_ROBUSTNESS_PROVENANCE.md",
        "paper1_manuscript_values_sync.json",
        "PAPER1_MANUSCRIPT_VALUES_SYNC.md",
        "paper1_appendix_provenance.json",
        "PAPER1_APPENDIX_PROVENANCE.md",
        "docker_runtime_context_latest.json",
        "DOCKER_RUNTIME_CONTEXT_LATEST.md",
        "docker_caldera_execution_latest.json",
        "DOCKER_CALDERA_EXECUTION_LATEST.md",
        "docker_execution_findings_latest.json",
        "DOCKER_EXECUTION_FINDINGS_LATEST.md",
    ]
    for relative in result_files:
        copy_text_with_repo_relativization(
            MEASUREMENT_ROOT / "results" / relative,
            measurement_dest / "results" / relative,
        )


def stage_frozen_artifact(dest_root: Path) -> None:
    sticks_dest = dest_root / "sticks-docker" / "sticks"
    copy_tree(STICKS_DOCKER_ROOT / "sticks" / "config", sticks_dest / "config")
    copy_tree(STICKS_DOCKER_ROOT / "sticks" / "lib", sticks_dest / "lib")
    copy_tree(STICKS_DOCKER_ROOT / "sticks" / "tools", sticks_dest / "tools")
    copy_tree(STICKS_DOCKER_ROOT / "sticks" / "data" / "api", sticks_dest / "data" / "api")
    copy_tree(STICKS_DOCKER_ROOT / "sticks" / "data" / "dag", sticks_dest / "data" / "dag")
    for relative in ["main.py", "requirements.txt"]:
        copy_file(STICKS_DOCKER_ROOT / "sticks" / relative, sticks_dest / relative)

    docker_dest = dest_root / "sticks-docker" / "docker"
    copy_file(STICKS_DOCKER_ROOT / "docker" / "docker-compose.yml", docker_dest / "docker-compose.yml")
    copy_file(STICKS_DOCKER_ROOT / "architecture.png", dest_root / "sticks-docker" / "architecture.png")
    copy_tree(STICKS_DOCKER_ROOT / "docker" / ".docker" / "caldera", docker_dest / ".docker" / "caldera")
    copy_tree(STICKS_DOCKER_ROOT / "docker" / ".docker" / "nginx", docker_dest / ".docker" / "nginx")
    copy_tree(STICKS_DOCKER_ROOT / "docker" / ".docker" / "kali", docker_dest / ".docker" / "kali")
    copy_tree(STICKS_DOCKER_ROOT / "docker" / ".docker" / "db", docker_dest / ".docker" / "db")

    empty_directory(docker_dest / ".docker" / "db" / "dbdata")
    empty_directory(docker_dest / "kali-data")

    write_text(
        sticks_dest / "README.md",
        "\n".join(
            [
                "# Frozen STICKS Layer",
                "",
                "This subtree contains the frozen Paper 1 Stage 2/Stage 3 support code",
                "consumed by the measurement boundary. It is intentionally kept minimal",
                "and should be treated as read-only by reviewers.",
                "",
                "The reviewer-facing entry points are the repository-root",
                "`run_review_check.sh` wrapper and the canonical verifier at",
                "`sticks-docker/measurement/release_check.sh`.",
                "",
            ]
        ),
    )

    write_text(
        docker_dest / "README.md",
        "\n".join(
            [
                "# Frozen Docker Substrate",
                "",
                "This directory contains the frozen shared-substrate Docker context used",
                "by the Paper 1 execution audit.",
                "",
                "Reviewer paths:",
                "",
                "- Fast validation: do not enter this directory directly; run",
                "  `bash run_review_check.sh` from the repository root.",
                "- Full Docker replay: run",
                "  `bash sticks-docker/measurement/run_full_docker_audit.sh` from the",
                "  repository root if you want to rebuild the shared substrate and rerun",
                "  the eight curated adversaries end to end.",
                "",
                "The staged artifact intentionally excludes runtime residue such as",
                "persistent Kali history and populated database state.",
                "",
            ]
        ),
    )


def write_artifact_docs(dest_root: Path) -> None:
    write_text(
        dest_root / "run_review_check.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"',
                'cd "$ROOT_DIR/sticks-docker/measurement"',
                "bash release_check.sh",
                "",
            ]
        ),
    )
    (dest_root / "run_review_check.sh").chmod(0o755)
    (dest_root / "sticks-docker" / "measurement" / "release_check.sh").chmod(0o755)
    (dest_root / "sticks-docker" / "measurement" / "run_full_docker_audit.sh").chmod(0o755)

    write_text(
        dest_root / ".gitattributes",
        "\n".join(
            [
                "* text=auto eol=lf",
                "*.sh text eol=lf",
                "*.py text eol=lf",
                "*.tex text eol=lf",
                "*.yml text eol=lf",
                "*.yaml text eol=lf",
                "",
            ]
        ),
    )

    write_text(
        dest_root / ".gitignore",
        "\n".join(
            [
                ".DS_Store",
                "__pycache__/",
                "*.pyc",
                "sticks-docker/measurement/runtime/docker-context/",
                "sticks-docker/measurement/runtime/curated-api/",
                "ACM CCS - Paper 1/build_artifacts/",
                "ACM CCS - Paper 1/*.aux",
                "ACM CCS - Paper 1/*.bbl",
                "ACM CCS - Paper 1/*.blg",
                "ACM CCS - Paper 1/*.fdb_latexmk",
                "ACM CCS - Paper 1/*.fls",
                "ACM CCS - Paper 1/*.log",
                "ACM CCS - Paper 1/*.out",
                "ACM CCS - Paper 1/*.run.xml",
                "ACM CCS - Paper 1/*.synctex.gz",
                "",
            ]
        ),
    )

    write_text(
        dest_root / "README.md",
        "\n".join(
            [
                "# Paper 1 Review Artifact",
                "",
                "This staging directory contains the paper-scoped reproducibility surface",
                "for the Paper 1 measurement manuscript on the procedural semantics gap",
                "in structured CTI.",
                "",
                "Suggested public repository name: `sticks-docker`.",
                "",
                "## Public clone path",
                "",
                "```bash",
                f"git clone {PUBLISHED_REPOSITORY}.git",
                "cd sticks-docker",
                "bash run_review_check.sh",
                "```",
                "",
                "## Reviewer entry points",
                "",
                "Fast validation path:",
                "",
                "```bash",
                "bash run_review_check.sh",
                "```",
                "",
                "This reruns the structural measurement scripts, regenerates the",
                "manuscript macro files, rebuilds the Paper 1 PDF, refreshes the",
                "frozen Docker audit summaries, and executes the measurement unit tests.",
                "",
                "Optional full Docker replay:",
                "",
                "```bash",
                "bash sticks-docker/measurement/run_full_docker_audit.sh",
                "```",
                "",
                "This heavier path prepares a disposable Docker runtime context, brings",
                "up the shared-substrate lab, reruns the eight curated adversaries, and",
                "regenerates the execution summaries consumed by the paper.",
                "",
                "## Runtime expectations",
                "",
                "- Python 3.11+",
                "- A TeX environment with `latexmk`/`pdflatex` available",
                "- `docker-compose` available on `PATH` only for the optional full replay",
                "- Fast validation runtime: about 3 to 4 minutes on a laptop-class machine",
                "- Full Docker replay runtime: substantially longer and dependent on Docker build cache",
                "- No GitHub, Azure, or other external API keys are required for the reviewer paths",
                "",
                "## Repository layout",
                "",
                "- `run_review_check.sh`: root-level reviewer wrapper.",
                "- `ACM CCS - Paper 1/`: manuscript source plus the current built PDF.",
                "- `sticks/`: shared ATT&CK bundle plus manuscript build helpers required by the verifier.",
                "- `sticks-docker/measurement/`: Paper 1 measurement scripts, tests, verifier, and latest audit outputs.",
                "- `sticks-docker/sticks/`: frozen Stage 2/3 support code and curated adversary payloads.",
                "- `sticks-docker/docker/`: frozen shared-substrate Docker context with runtime residue removed.",
                "",
                "## Reproduction contract",
                "",
                "If `bash run_review_check.sh` passes from the repository root, the staged",
                "artifact has enough material to rerun the Paper 1 measurements, rebuild",
                "the manuscript, and refresh the frozen Docker audit summaries tied to the paper.",
                "",
                "The optional Docker replay remains explicitly labeled as a shared-substrate",
                "execution audit, not isolated per-campaign historical replay.",
                "",
            ]
        ),
    )

    write_text(
        dest_root / "ARTIFACT_MANIFEST.md",
        "\n".join(
            [
                "# Artifact Manifest",
                "",
                "Suggested repository name: `sticks-docker`.",
                "",
                f"Public repository URL: `{PUBLISHED_REPOSITORY}`.",
                "",
                "## Included components",
                "",
                "- `run_review_check.sh`: root-level fast reviewer entry point.",
                "- `ACM CCS - Paper 1/`: manuscript source, bibliography, class/bst files, figures, and macro files.",
                "- `sticks/data/stix/enterprise-attack.json`: the Enterprise ATT&CK bundle used by the Paper 1 measurement scripts.",
                "- `sticks/scripts/`: manuscript build and hygiene helpers required by the verifier.",
                "- `sticks-docker/measurement/`: Paper 1 measurement scripts, tests, latest audit outputs, runtime docs, and the canonical verifier.",
                "- `sticks-docker/sticks/`: frozen support code plus curated Caldera API payloads and DAG files.",
                "- `sticks-docker/docker/`: frozen shared-substrate Docker context with runtime residue removed.",
                "",
                "## Excluded components",
                "",
                "- Historical result archives and timestamped rerun logs not required by the reviewer path.",
                "- Persistent Kali shell history and SSH known-hosts residue.",
                "- Populated MariaDB state from prior runs.",
                "- Unrelated workspace material from Paper 2 and the broader monorepo.",
                "",
                "## Reproduction modes",
                "",
                "- Fast mode (`run_review_check.sh`): recomputes the measurement outputs and manuscript from the staged artifact plus the frozen latest Docker audit summaries.",
                "- Full Docker mode (`sticks-docker/measurement/run_full_docker_audit.sh`): rebuilds the shared-substrate lab and reruns the eight curated adversaries end to end.",
                "",
            ]
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="Destination directory for the staged review artifact.",
    )
    args = parser.parse_args()

    dest_root = args.dest.resolve()
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    stage_paper(dest_root)
    stage_shared_bundle(dest_root)
    stage_measurement_boundary(dest_root)
    stage_frozen_artifact(dest_root)
    write_artifact_docs(dest_root)

    print(f"Staged Paper 1 artifact at {dest_root}")


if __name__ == "__main__":
    main()
