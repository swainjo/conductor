"""Unit tests for setup resume — tracker files stay optional."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import resume  # noqa: E402

_TRACKER_FILES = ("linear.md", "github.md")
_REQUIRED_CHAIN = (
    "product.md",
    "product-guidelines.md",
    "tech-stack.md",
    "code_styleguides",
    "workflow.md",
)


def test_determine_resumption_does_not_require_tracker_files(tmp_path, monkeypatch):
    conductor = tmp_path / "conductor"
    conductor.mkdir()
    (conductor / "product.md").write_text("x")
    (conductor / "product-guidelines.md").write_text("x")
    (conductor / "tech-stack.md").write_text("x")
    (conductor / "code_styleguides").mkdir()
    (conductor / "workflow.md").write_text("x")
    (conductor / "index.md").write_text("x")
    monkeypatch.chdir(tmp_path)

    result = resume.determine_resumption()

    assert result["setup_complete"] is True
    assert result["next_step"] is None
    for name in _TRACKER_FILES:
        assert name not in result["checklist"]
        assert not (conductor / name).exists()


def test_required_chain_does_not_include_tracker_files():
    source = Path(resume.__file__).read_text()
    for name in _TRACKER_FILES:
        assert f'"{name}"' not in source
        assert f"'{name}'" not in source
    for name in _REQUIRED_CHAIN:
        assert name in source
