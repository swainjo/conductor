"""Offline checks for the GitHub-first setup template."""

from __future__ import annotations

from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "github.md"

_REQUIRED_PLACEHOLDERS = (
    "{{OWNER}}",
    "{{REPO}}",
    "{{SURFACE_EXAMPLE_NAME}}",
    "{{SURFACE_EXAMPLE_PATH}}",
)

_REQUIRED_SECTIONS = (
    "github-issues",
    "github-review",
    "github-handoff",
    "github-label-review",
    "Class",
    "Surface",
    "in-progress",
    "in-review",
    "blocked",
    "GitHub MCP",
    "`gh`",
)


def test_github_template_exists():
    assert TEMPLATE.is_file(), f"missing template: {TEMPLATE}"


def test_github_template_has_required_placeholders():
    text = TEMPLATE.read_text()
    missing = [token for token in _REQUIRED_PLACEHOLDERS if token not in text]
    assert not missing, f"missing placeholders: {missing}"


def test_github_template_documents_taxonomy_and_transport():
    text = TEMPLATE.read_text()
    missing = [token for token in _REQUIRED_SECTIONS if token not in text]
    assert not missing, f"missing sections: {missing}"


def test_github_template_does_not_contain_secrets():
    text = TEMPLATE.read_text()
    assert "ghp_" not in text
    assert "GITHUB_TOKEN=" not in text
    assert "lin_api_" not in text
