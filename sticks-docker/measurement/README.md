# Paper 1 Measurement Boundary

This directory is the only allowed write surface for new Paper 1 measurement
code, generated measurement outputs, and migration notes.

The surrounding `sticks-docker/` tree is treated as a frozen Docker artifact.
Do not edit `sticks-docker/docker/` or `sticks-docker/sticks/` for new Paper 1
measurement work. If a Paper 1 result must be regenerated or audited, add the
new code here and make it consume the Docker artifact as an input.

## Scope

- `scripts/`: Paper 1 measurement code migrated or rewritten for the Docker
  artifact.
- `results/`: generated outputs that support Paper 1 claims.

## Source-of-Truth Rule

If a number, table, or claim supports Paper 1 and depends on the Docker-based
artifact semantics, the code that produced it should live here rather than
under `sticks/`.

## Migration Contract

The first migration targets should be:

1. Paper 1 macro generation currently implemented under `sticks/scripts/`.
2. Paper 1 provenance reports currently emitted under `sticks/results/`.
3. Any execution-side measurement collectors needed to tie Docker runs to the
   Paper 1 manuscript.

Until those migrations are complete, treat `sticks/` as a transitional source
of implementation ideas, not as the authoritative origin of new Paper 1
results.
