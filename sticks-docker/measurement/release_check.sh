#!/usr/bin/env bash
set -euo pipefail

MEASUREMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${MEASUREMENT_DIR}/../.." && pwd)"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paper1-release-check.XXXXXX")"
RUNTIME_CONTEXT="${TEMP_DIR}/docker-context"
API_OVERLAY="${TEMP_DIR}/curated-api"
export PYTHONDONTWRITEBYTECODE=1

cleanup() {
  rm -rf "${TEMP_DIR}"
}

trap cleanup EXIT

cd "${ROOT_DIR}"

python3 sticks-docker/measurement/scripts/analyze_campaigns.py \
  --bundle sticks/data/stix/enterprise-attack.json
python3 sticks-docker/measurement/scripts/sync_paper1_values.py
python3 sticks-docker/measurement/scripts/analyze_identifiability.py
python3 sticks-docker/measurement/scripts/analyze_paper1_robustness.py
python3 sticks-docker/measurement/scripts/analyze_paper1_appendix.py
python3 sticks-docker/measurement/scripts/prepare_docker_runtime_context.py \
  --output-dir "${RUNTIME_CONTEXT}" \
  --api-overlay-dir "${API_OVERLAY}"
python3 sticks-docker/measurement/scripts/summarize_docker_findings.py
python3 sticks/scripts/build_manuscript.py --paper-dir "${ROOT_DIR}/ACM CCS - Paper 1"
python3 sticks/scripts/check_paper_hygiene.py --paper paper1

(
  cd sticks-docker/measurement
  PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
)

echo "PASS: paper1 measurement + manuscript + frozen docker audit are consistent"
