# Procedural Reproducibility Artifact

This staging directory contains the reproducibility surface for the
procedural-semantics study in structured CTI.

Paper title: The Procedural Semantics Gap in ATT&CK-in-STIX: A Measurement-Driven Analysis for APT Emulation.

Suggested public repository name: `sticks-docker`.

## Public clone path

```bash
git clone https://github.com/sidneibarbieri/sticks-docker.git
cd sticks-docker
bash run_review_check.sh
```

## Reviewer entry points

Fast validation path:

```bash
bash run_review_check.sh
```

This reruns the structural measurement scripts, refreshes the frozen
Docker audit summaries, and executes the measurement unit tests.

Optional full Docker replay:

```bash
bash sticks-docker/measurement/run_full_docker_audit.sh
```

This heavier path prepares a disposable Docker runtime context, brings
up the shared-substrate lab, reruns the eight curated adversaries, and
regenerates the execution summaries consumed by the paper.

## What the reviewer can verify directly

- Retrieval: the repository is public, self-contained, and includes a `LICENSE`.
- Exercisability: `bash run_review_check.sh` recomputes the released measurement
  outputs and validates the frozen execution summaries.
- Main-result reproduction: the optional Docker path rebuilds the shared lab and
  reruns the eight curated adversaries end to end from the published artifact.

## Runtime expectations

- Python 3.11+
- A TeX environment with `latexmk`/`pdflatex` available
- `docker-compose` available on `PATH` only for the optional full replay
- Fast validation runtime: about 3 to 4 minutes on a laptop-class machine
- Full Docker replay runtime: substantially longer and dependent on Docker build cache
- No GitHub, Azure, or other external API keys are required for the reviewer paths
- For Docker Desktop on macOS, run the full Docker replay from a regular local clone
  path (for example under your home directory) rather than a transient temp directory,
  so the Caldera bind mount remains visible to the containers.

## Repository layout

- `run_review_check.sh`: root-level reviewer wrapper.
- `sticks/`: shared ATT&CK bundle required by the verifier.
- `sticks-docker/measurement/`: Paper 1 measurement scripts, tests, verifier, and latest audit outputs.
- `sticks-docker/sticks/`: frozen Stage 2/3 support code and curated adversary payloads.
- `sticks-docker/docker/`: frozen shared-substrate Docker context with runtime residue removed.

## Reproduction contract

If `bash run_review_check.sh` passes from the repository root, the staged
artifact has enough material to rerun the procedural measurements and
refresh the frozen Docker audit summaries.

The optional Docker replay remains explicitly labeled as a shared-substrate
execution audit, not isolated per-campaign historical replay.
