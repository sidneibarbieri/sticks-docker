# Procedural Measurement Scripts

Place migrated or newly written procedural measurement scripts here.

Rules:

- Inputs should come from `sticks-docker/`, an optional private manuscript tree,
  or data copied into this measurement boundary for procedural-study purposes.
- New measurements should not depend on `sticks/` execution paths at
  runtime.
- Keep each script single-purpose and make the output path explicit.

Planned early migrations:

- macro generation for `manuscript/paper1/results/values.tex`
- procedural provenance generation
- Docker-backed execution measurement collectors
- frozen Caldera Stage 3 execution audits driven from `sticks-docker/sticks/`
- temporary Docker runtime context preparation for the frozen artifact
- consolidated findings reports spanning architecture, runtime, and execution
