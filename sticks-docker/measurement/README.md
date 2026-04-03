# Procedural Measurement Boundary

This directory is the only allowed write surface for new procedural measurement
code, generated outputs, and migration notes.

The surrounding `sticks-docker/` tree is treated as a frozen Docker artifact.
Do not edit `sticks-docker/docker/` or `sticks-docker/sticks/` for new
measurement work. If a result must be regenerated or audited, add the
new code here and make it consume the Docker artifact as an input.

## Scope

- `scripts/`: measurement code migrated or rewritten for the Docker artifact.
- `results/`: generated outputs that support the procedural study claims.

## Source-of-Truth Rule

If a number, table, or claim depends on the Docker-based
artifact semantics, the code that produced it should live here rather than
under `sticks/`.

## Migration Contract

The first migration targets should be:

1. Macro generation currently implemented under `sticks/scripts/`.
2. Provenance reports currently emitted under `sticks/results/`.
3. Any execution-side measurement collectors needed to tie Docker runs to the
   study outputs.

Until those migrations are complete, treat `sticks/` as a transitional source
of implementation ideas, not as the authoritative origin of new measurement
results.
