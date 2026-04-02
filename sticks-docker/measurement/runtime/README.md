# Paper 1 Docker Runtime Scratch

This directory holds workspace-local runtime copies of the frozen Docker
artifact used for Paper 1 execution measurements.

Rules:

- Everything here is scratch and must stay out of commits.
- The prepared Docker context exists to keep the frozen artifact immutable while
  still repairing local checkout/runtime issues such as lost executable bits.
- The context is recreated as needed by
  `sticks-docker/measurement/scripts/prepare_docker_runtime_context.py`.
