from __future__ import annotations

from functools import lru_cache
import importlib.util
import sys
from pathlib import Path


MEASUREMENT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = MEASUREMENT_ROOT.parent.parent
SYNC_SCRIPT_PATH = MEASUREMENT_ROOT / "scripts" / "sync_paper1_values.py"
ANALYZE_SCRIPT_PATH = MEASUREMENT_ROOT / "scripts" / "analyze_campaigns.py"
PAPER1_VALUES = WORKSPACE_ROOT / "ACM CCS - Paper 1" / "results" / "values.tex"


@lru_cache(maxsize=1)
def _load_sync_module():
    spec = importlib.util.spec_from_file_location("paper1_sync_values", SYNC_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _load_analyze_module():
    spec = importlib.util.spec_from_file_location("paper1_docker_measurement_sync", ANALYZE_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_sync_writes_current_values_to_alternate_target(tmp_path: Path) -> None:
    sync_module = _load_sync_module()
    analyze_module = _load_analyze_module()

    target_path = tmp_path / "values.tex"
    target_path.write_text(PAPER1_VALUES.read_text(encoding="utf-8"), encoding="utf-8")

    result = sync_module.sync_values(manuscript_values_path=target_path, dry_run=False)
    expected_values = analyze_module.render_values_tex(
        analyze_module.compute_paper1_values(analyze_module.DEFAULT_BUNDLE)
    )

    assert result.status in {"current", "updated"}
    assert result.macros_written == 40
    assert target_path.read_text(encoding="utf-8") == expected_values


def test_sync_dry_run_does_not_modify_target(tmp_path: Path) -> None:
    sync_module = _load_sync_module()

    target_path = tmp_path / "values.tex"
    original_text = PAPER1_VALUES.read_text(encoding="utf-8")
    target_path.write_text(original_text, encoding="utf-8")

    result = sync_module.sync_values(manuscript_values_path=target_path, dry_run=True)

    assert result.status == "dry_run"
    assert target_path.read_text(encoding="utf-8") == original_text
