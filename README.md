# Paper 1 Review Artifact

This staging directory contains the paper-scoped reproducibility surface
for the Paper 1 measurement manuscript on the procedural semantics gap
in structured CTI.

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

This reruns the structural measurement scripts, regenerates the
manuscript macro files, rebuilds the Paper 1 PDF, refreshes the
frozen Docker audit summaries, and executes the measurement unit tests.

Optional full Docker replay:

```bash
bash sticks-docker/measurement/run_full_docker_audit.sh
```

This heavier path prepares a disposable Docker runtime context, brings
up the shared-substrate lab, reruns the eight curated adversaries, and
regenerates the execution summaries consumed by the paper.

## Runtime expectations

- Python 3.11+
- A TeX environment with `latexmk`/`pdflatex` available
- `docker-compose` available on `PATH` only for the optional full replay
- Fast validation runtime: about 3 to 4 minutes on a laptop-class machine
- Full Docker replay runtime: substantially longer and dependent on Docker build cache
- No GitHub, Azure, or other external API keys are required for the reviewer paths

## Repository layout

- `run_review_check.sh`: root-level reviewer wrapper.
- `ACM CCS - Paper 1/`: manuscript source plus the current built PDF.
- `sticks/`: shared ATT&CK bundle plus manuscript build helpers required by the verifier.
- `sticks-docker/measurement/`: Paper 1 measurement scripts, tests, verifier, and latest audit outputs.
- `sticks-docker/sticks/`: frozen Stage 2/3 support code and curated adversary payloads.
- `sticks-docker/docker/`: frozen shared-substrate Docker context with runtime residue removed.

## Reproduction contract

If `bash run_review_check.sh` passes from the repository root, the staged
artifact has enough material to rerun the Paper 1 measurements, rebuild
the manuscript, and refresh the frozen Docker audit summaries tied to the paper.

The optional Docker replay remains explicitly labeled as a shared-substrate
execution audit, not isolated per-campaign historical replay.
