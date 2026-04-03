#!/usr/bin/env bash
set -euo pipefail

MEASUREMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${MEASUREMENT_DIR}/../.." && pwd)"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paper1-release-check.XXXXXX")"
RUNTIME_CONTEXT="${TEMP_DIR}/docker-context"
API_OVERLAY="${TEMP_DIR}/curated-api"
export PYTHONDONTWRITEBYTECODE=1

find_paper_dir() {
  local root="$1"
  local pattern
  for pattern in "*Paper 1*" "*paper1*" "paper1-manuscript"; do
    local match
    while IFS= read -r match; do
      if [[ -f "$match/main.tex" ]]; then
        printf '%s\n' "$match"
        return 0
      fi
    done < <(find "$root" -maxdepth 1 -type d -name "$pattern" 2>/dev/null | sort)
  done
  return 1
}

PAPER_DIR="${ROOT_DIR}/paper1-manuscript"
if found_paper_dir="$(find_paper_dir "${ROOT_DIR}")"; then
  PAPER_DIR="${found_paper_dir}"
fi
HAS_MANUSCRIPT_DIR=0
if [[ -f "${PAPER_DIR}/main.tex" ]]; then
  HAS_MANUSCRIPT_DIR=1
fi
export PAPER_DIR
export HAS_MANUSCRIPT_DIR

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
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_identifiability.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_paper1_robustness.py
"${PYTHON_BIN}" sticks-docker/measurement/scripts/analyze_paper1_appendix.py
if [[ "${HAS_MANUSCRIPT_DIR}" == "1" ]]; then
  "${PYTHON_BIN}" sticks-docker/measurement/scripts/sync_paper1_values.py
fi
"${PYTHON_BIN}" sticks-docker/measurement/scripts/prepare_docker_runtime_context.py \
  --output-dir "${RUNTIME_CONTEXT}" \
  --api-overlay-dir "${API_OVERLAY}"
"${PYTHON_BIN}" sticks-docker/measurement/scripts/summarize_docker_findings.py
if [[ "${HAS_MANUSCRIPT_DIR}" == "1" ]]; then
  "${PYTHON_BIN}" sticks/scripts/build_manuscript.py --paper-dir "${PAPER_DIR}"
  "${PYTHON_BIN}" sticks/scripts/check_paper_hygiene.py --paper paper1
fi

(
  cd sticks-docker/measurement
  PYTHONDONTWRITEBYTECODE=1 "${PYTHON_BIN}" -m pytest -q -p no:cacheprovider
)

if [[ "${HAS_MANUSCRIPT_DIR}" == "1" ]]; then
  echo "PASS: procedural measurement + manuscript + frozen docker audit are consistent"
else
  echo "PASS: procedural measurement + frozen docker audit are consistent"
fi
