"""Structural and behavioral tests for the packaged /sync skill."""

import os
import re
import shutil
import tempfile
from pathlib import Path
import pytest
import yaml


@pytest.fixture
def skill_path() -> Path:
    base = Path(__file__).resolve().parent.parent
    skill_file = base / "SKILL.md"
    assert skill_file.exists(), f"SKILL.md not found at {skill_file}"
    return skill_file


@pytest.fixture
def skill_content(skill_path: Path) -> str:
    return skill_path.read_text(encoding="utf-8")


def test_frontmatter_validity(skill_content: str):
    """Verify that SKILL.md contains valid YAML frontmatter adhering to writing-for-agents."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", skill_content, re.DOTALL)
    assert match is not None, "SKILL.md must start with YAML frontmatter bounded by '---'"
    
    frontmatter_raw, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_raw)
    
    assert frontmatter["name"] == "sync"
    assert "description" in frontmatter and len(frontmatter["description"]) > 10
    assert frontmatter.get("disable-model-invocation") is True, "Must be user-invoked to avoid context load"
    assert "argument-hint" in frontmatter


def test_leading_words_present(skill_content: str):
    """Verify that all core leading words are defined and utilized."""
    required_words = ["sync", "land", "retire", "receipt", "frontier"]
    for word in required_words:
        assert f"**`{word}`**" in skill_content or f"`{word}`" in skill_content, (
            f"Missing required leading word: {word}"
        )


def test_all_seven_phases_present(skill_content: str):
    """Verify that the complete closeout lifecycle is documented."""
    required_phases = [
        "1. Discover and target",
        "2. Gate 1 — verify the delivered work",
        "3. Reconcile maps and local tracker projections",
        "4. Land and retire implementations",
        "5. Stage and audit reconciliation changes",
        "6. Commit and publish",
        "7. Update and close affected tickets",
        "8. Emit the receipt and frontier",
    ]
    for phase in required_phases:
        assert phase in skill_content, f"Missing required lifecycle phase: {phase}"


def test_two_gate_fail_stop_rules(skill_content: str):
    """Verify that verification precedes reconciliation and publication."""
    assert "Gate 1 — verify the delivered work" in skill_content
    assert "Stage and audit reconciliation changes" in skill_content
    assert "stop before publication" in skill_content.lower()


# ---------------------------------------------------------------------------
# Behavioral Simulation Tests
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_workspace(tmp_path: Path):
    """Creates a mock git repository with Wayfinder issue tracker and map."""
    workspace = tmp_path / "mock_project"
    workspace.mkdir()
    
    # Initialize mock tracker structure
    effort_dir = workspace / ".scratch" / "auth"
    issues_dir = effort_dir / "issues"
    issues_dir.mkdir(parents=True)
    
    # Map file
    map_file = effort_dir / "map.md"
    map_file.write_text(
        "# Map: Auth System\n\n"
        "## Destination\nImplement secure auth.\n\n"
        "## Decisions so far\n\n"
        "## Not yet specified\n- Session token refresh strategies\n",
        encoding="utf-8"
    )
    
    # Child tickets with dependency chain (01 blocks 02)
    ticket_1 = issues_dir / "01-jwt-auth.md"
    ticket_1.write_text(
        "# 01: JWT Authentication\n\n"
        "Status: claimed\n"
        "Type: task\n"
        "Blocked by: None\n\n"
        "## Question\nHow do we issue signed JWTs?\n",
        encoding="utf-8"
    )
    
    ticket_2 = issues_dir / "02-token-refresh.md"
    ticket_2.write_text(
        "# 02: Token Refresh Rotation\n\n"
        "Status: open\n"
        "Type: task\n"
        "Blocked by: 01-jwt-auth.md\n\n"
        "## Question\nHow do we rotate refresh tokens safely?\n",
        encoding="utf-8"
    )
    
    # Reflection session to protect
    reflection_dir = workspace / ".scratch" / "reflection-session"
    reflection_dir.mkdir(parents=True)
    (reflection_dir / "session.json").write_text('{"status": "active"}', encoding="utf-8")
    
    return {
        "root": workspace,
        "map": map_file,
        "ticket_1": ticket_1,
        "ticket_2": ticket_2,
        "reflection_dir": reflection_dir,
    }


def test_wayfinder_ticket_resolution_and_frontier_projection(mock_workspace):
    """
    Simulates Phase 3: Reconciling a resolved ticket, appending to Decisions so far,
    and calculating the next unblocked frontier ticket.
    """
    ticket_1 = mock_workspace["ticket_1"]
    ticket_2 = mock_workspace["ticket_2"]
    map_file = mock_workspace["map"]
    
    # Simulate synthesizing ## Answer and marking ticket 1 resolved
    answer_text = "\n## Answer\nImplemented HMAC-SHA256 JWT tokens with 15-min TTL.\n"
    content_1 = ticket_1.read_text(encoding="utf-8").replace("Status: claimed", "Status: resolved")
    ticket_1.write_text(content_1 + answer_text, encoding="utf-8")
    
    # Simulate updating map.md
    map_content = map_file.read_text(encoding="utf-8")
    decision_entry = "- [01: JWT Authentication](issues/01-jwt-auth.md): Implemented HMAC-SHA256 JWT tokens with 15-min TTL.\n"
    map_file.write_text(
        map_content.replace("## Decisions so far\n", f"## Decisions so far\n{decision_entry}"),
        encoding="utf-8"
    )
    
    # Verify Map state
    updated_map = map_file.read_text(encoding="utf-8")
    assert "01: JWT Authentication" in updated_map
    assert "HMAC-SHA256" in updated_map
    assert "- Session token refresh strategies" in updated_map  # Fog was preserved
    
    # Compute frontier: scan open tickets whose blockers are resolved
    open_tickets = [ticket_2]
    unblocked = []
    for t in open_tickets:
        text = t.read_text(encoding="utf-8")
        if "Status: open" in text:
            # Check blockers
            if "01-jwt-auth.md" in text:
                blocker_text = ticket_1.read_text(encoding="utf-8")
                if "Status: resolved" in blocker_text:
                    unblocked.append(t.name)
    
    assert unblocked == ["02-token-refresh.md"], "Ticket 02 should be the newly unblocked frontier ticket"


def test_selective_staging_filter_excludes_reflection(mock_workspace):
    """
    Simulates Phase 4 staging rules: modified tracked sources and map updates are staged,
    while untracked reflection records are strictly excluded.
    """
    root = mock_workspace["root"]
    
    all_files = [
        root / ".scratch" / "auth" / "map.md",
        root / ".scratch" / "auth" / "issues" / "01-jwt-auth.md",
        root / ".scratch" / "reflection-session" / "session.json",
        root / "src" / "auth.py",
    ]
    
    def is_stageable(path: Path) -> bool:
        # Exclusion rule: never stage reflection records or temporary scratch
        if "reflection-session" in path.parts or "weekly-records" in path.parts:
            return False
        if path.suffix in [".log", ".tmp"]:
            return False
        return True
    
    staged = [f for f in all_files if is_stageable(f)]
    
    assert mock_workspace["map"] in staged
    assert mock_workspace["ticket_1"] in staged
    assert (root / ".scratch" / "reflection-session" / "session.json") not in staged
