# Paper 1 Measurement Scripts

Place migrated or newly written Paper 1 measurement scripts here.

Rules:

- Inputs should come from `sticks-docker/`, the Paper 1 manuscript, or data
  copied into this measurement boundary for Paper 1 purposes.
- New Paper 1 measurements should not depend on `sticks/` execution paths at
  runtime.
- Keep each script single-purpose and make the output path explicit.

Planned early migrations:

- macro generation for `ACM CCS - Paper 1/results/values.tex`
- Paper 1 provenance generation
- Docker-backed execution measurement collectors
- frozen Caldera Stage 3 execution audits driven from `sticks-docker/sticks/`
- temporary Docker runtime context preparation for the frozen artifact
- consolidated Paper 1 findings reports spanning architecture, runtime, and execution
