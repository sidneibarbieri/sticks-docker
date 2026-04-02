# Paper 1 Camera-Ready Audit

- Audit date: `2026-03-25`
- Manuscript: `/Users/sidneibarbieri/paper measurement/ACM CCS - Paper 1/main.tex`
- Goal: rerun the paper baseline end-to-end, compare it with the current official ATT&CK release, and confirm that every central quantitative and execution claim remains supported.

## 1. ATT&CK Release Freeze

- Official current ATT&CK release checked on `2026-03-25`: `v18.1`
- Local Enterprise bundle path: `/Users/sidneibarbieri/paper measurement/sticks/data/stix/enterprise-attack.json`
- Downloaded upstream comparison path: `/Users/sidneibarbieri/paper measurement/tmp/mitre/enterprise-attack.remote.json`
- Local SHA-256: `f857d8f78f2f0c0b7db321a711a39fba98546c1e3076a657684850c83d0962fb`
- Remote SHA-256: `f857d8f78f2f0c0b7db321a711a39fba98546c1e3076a657684850c83d0962fb`
- Result: exact byte-for-byte match

Implication: the camera-ready rerun is simultaneously an exact-paper reproduction and a latest-official drift check for the ATT&CK Enterprise bundle.

Supporting file:
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/PAPER1_MITRE_DRIFT_CHECK_20260325.md`

## 2. Quantitative Measurement Rerun

Rerun commands completed successfully:
- `analyze_campaigns.py`
- `analyze_identifiability.py`
- `sync_paper1_values.py`

Confirmed bundle-level values:
- campaigns with techniques: `51`
- intrusion sets: `172`
- active attack-pattern objects: `691`
- campaign coverage: `43.0%`
- platform-agnostic techniques: `32`
- translatable techniques: `659`
- silhouette score: `0.05`
- LCS mean / median / max: `2.8 / 2.0 / 29`

Confirmed identifiability values:
- campaigns distinguishable: `51/51`
- intrusion sets distinguishable: `145/168`

Supporting files:
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/PAPER1_VALUES_PROVENANCE.md`
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/PAPER1_IDENTIFIABILITY_PROVENANCE.md`

## 3. Manuscript Value Sync

- `values.tex` already matched the measurement pipeline output.
- No manuscript macro drift was found.

Supporting file:
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/PAPER1_MANUSCRIPT_VALUES_SYNC.md`

## 4. Docker / Caldera Execution Rerun

Fresh rerun completed successfully after rebuilding the prepared runtime context.

Runtime context findings:
- script repairs: `29`
- generated runtime config files: `2`
- host architecture patches: `2`
- curated API overlay patches: `6`

Execution findings:
- operations with progress: `8/8`
- total successful links: `109`
- total failed links: `0`
- total pending links: `0`
- explicit end markers reached: `8/8`
- quiescent plateau reached: `True`
- poll timeout reached: `False`
- shared substrate model: `True`

Per-workflow successful links:
- `OP001 / APT41 DUST`: `24`
- `OP002 / C0010`: `10`
- `OP003 / C0026`: `7`
- `OP004 / CostaRicto`: `11`
- `OP005 / Operation MidnightEclipse`: `18`
- `OP006 / Outer Space`: `9`
- `OP007 / Salesforce Data Exfiltration`: `19`
- `OP008 / ShadowRay`: `11`

Derived summary:
- median successful links per workflow: `11`
- range: `7--24`

Supporting files:
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/DOCKER_RUNTIME_CONTEXT_LATEST.md`
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/DOCKER_CALDERA_EXECUTION_LATEST.md`
- `/Users/sidneibarbieri/paper measurement/sticks-docker/measurement/results/DOCKER_EXECUTION_FINDINGS_LATEST.md`

## 5. Runtime Nuance Confirmed by Rerun

The rerun reconfirmed an important procedural point already reflected in the manuscript:

- container-level health was not sufficient by itself;
- service-level readiness still required waiting for campaign bootstrap completion and a stable trusted `red` agent beacon;
- the legacy Docker path therefore demonstrates controlled shared-substrate enactment, not push-button isolated replay.

This strengthened the trustworthiness of the existing manuscript wording rather than requiring a new claim.

## 6. Camera-Ready Verdict

- No central quantitative claim drifted.
- No Docker execution claim drifted.
- No ATT&CK release drift affected the paper baseline.
- No manuscript number update was required after the rerun.

Final judgment:

The current manuscript remains factually aligned with the regenerated artifacts. At this stage, further paper edits would add risk without a corresponding increase in scientific accuracy or clarity.
