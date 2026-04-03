# Artifact Manifest

Suggested repository name: `sticks-docker`.

Public repository URL: `https://github.com/sidneibarbieri/sticks-docker`.

## Included components

- `run_review_check.sh`: root-level fast reviewer entry point.
- `ACM CCS - Paper 1/`: manuscript source, bibliography, class/bst files, figures, and macro files.
- `sticks/data/stix/enterprise-attack.json`: the Enterprise ATT&CK bundle used by the Paper 1 measurement scripts.
- `sticks/scripts/`: manuscript build and hygiene helpers required by the verifier.
- `sticks-docker/measurement/`: Paper 1 measurement scripts, tests, latest audit outputs, runtime docs, and the canonical verifier.
- `sticks-docker/sticks/`: frozen support code plus curated Caldera API payloads.
- `sticks-docker/docker/`: frozen shared-substrate Docker context with runtime residue removed.

## Excluded components

- Historical result archives and timestamped rerun logs not required by the reviewer path.
- Persistent Kali shell history and SSH known-hosts residue.
- Populated MariaDB state from prior runs.
- Unrelated workspace material from Paper 2 and the broader monorepo.

## Reproduction modes

- Fast mode (`run_review_check.sh`): recomputes the measurement outputs and manuscript from the staged artifact plus the frozen latest Docker audit summaries.
- Full Docker mode (`sticks-docker/measurement/run_full_docker_audit.sh`): rebuilds the shared-substrate lab and reruns the eight curated adversaries end to end.
