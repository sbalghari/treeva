from pathlib import Path
from logging import getLogger

from treeva.analysis.git import analyze_git


def test_analyze_git_returns_data():
    repo = Path(__file__).parent.parent.parent
    result = analyze_git(repo, logger=getLogger("test"))
    assert result is not None
    assert result.total_commits > 0
    assert result.total_authors > 0
    assert len(result.churn) > 0


def test_hotspots_sorted_by_churn():
    repo = Path(__file__).parent.parent.parent
    result = analyze_git(repo, logger=getLogger("test"))
    assert result is not None
    for i in range(len(result.hotspots) - 1):
        curr = result.hotspots[i].additions + result.hotspots[i].deletions
        nxt = (
            result.hotspots[i + 1].additions + result.hotspots[i + 1].deletions
        )
        assert curr >= nxt, f"Hotspots not sorted at index {i}"
