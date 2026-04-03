#!/usr/bin/env bash
set -euo pipefail

MEASUREMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${MEASUREMENT_DIR}/../.." && pwd)"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paper1-release-check.XXXXXX")"
RUNTIME_CONTEXT="${TEMP_DIR}/docker-context"
API_OVERLAY="${TEMP_DIR}/curated-api"
export PYTHONDONTWRITEBYTECODE=1

resolve_python_bin() {
  local candidate
  for candidate in /opt/homebrew/bin/python3 python3 python3.14 python; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      if "${candidate}" -c 'import pytest, sys; print(sys.executable)' >/tmp/paper1-python-bin 2>/dev/null; then
        cat /tmp/paper1-python-bin
        rm -f /tmp/paper1-python-bin
        return 0
      fi
    fi
  done

  echo "release_check.sh could not find a Python interpreter with pytest installed" >&2
  return 1
}

PYTHON_BIN="$(resolve_python_bin)"

cleanup() {
  rm -rf "${TEMP_DIR}"
}

trap cleanup EXIT

cd "${ROOT_DIR}"

"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_campaigns.py \
  --bundle sticks/data/stix/enterprise-attack.json
"${PYTHON_BIN}" sticks-docker/measurement/scripts/sync_paper1_values.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_identifiability.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_paper1_robustness.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_paper1_appendix.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/prepare_docker_runtime_context.py \
  --output-dir "${RUNTIME_CONTEXT}" \
  --api-overlay-dir "${API_OVERLAY}"
"${PYTHON_BIN}" sticks-docker/measurement/scripts/summarize_docker_findings.py
"${PYTHON_BIN}" sticks/scripts/build_manuscript.py --paper-dir "${ROOT_DIR}/ACM CCS - Paper 1"
"${PYTHON_BIN}" sticks/scripts/check_paper_hygiene.py --paper paper1

(
  cd sticks-docker/measurement
  PYTHONDONTWRITEBYTECODE=1 "${PYTHON_BIN}" -m pytest -q -p no:cacheprovider
)

echo "PASS: paper1 measurement + manuscript + frozen docker audit are consistent"
