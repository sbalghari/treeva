from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from subprocess import run, CalledProcessError

from treeva.models.git import GitInfo, GitChurn

if TYPE_CHECKING:
    from logging import Logger


def _git_log_numstat(repo_path: Path, logger: Logger) -> str:
    """Run git log --numstat and return raw output, or '' on failure.

    Args:
        repo_path: Path to the git repository.
        logger: Logger instance for warnings.

    Returns:
        Raw git log output string, or empty string on failure.

    Notes:
        Uses a 30-second timeout. Returns empty string for any failure
        (missing git binary, non-repo path, git errors, etc.).
    """
    try:
        result = run(
            ["git", "log", "--all", "--numstat", "--pretty=%H %ai %an"],
            capture_output=True,
            text=True,
            cwd=repo_path,
            timeout=30,
        )
        result.check_returncode()
        return result.stdout
    except CalledProcessError as e:
        logger.warning("git log failed: %s", e.stderr)
        return ""
    except FileNotFoundError:
        logger.warning("git not found")
        return ""
    except Exception as e:
        logger.warning("git analysis failed: %s", e)
        return ""


def analyze_git(repo_path: Path, *, logger: Logger) -> GitInfo | None:
    """Return git-churn and hotspot data for repo_path.

    Args:
        repo_path: Path to the git repository.
        logger: Logger instance for warnings.

    Returns:
        A GitAnalysis instance, or None if git analysis fails.

    Notes:
        Hotspots are defined as the top 20 most-churned files by
        total additions + deletions.
    """
    raw = _git_log_numstat(repo_path, logger)
    if not raw:
        return None

    commits: set[str] = set()
    authors: set[str] = set()
    file_churn: dict[str, dict] = {}

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line[0].isdigit() or line[0] == "-":
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            add_str, del_str, filepath = parts
            add = int(add_str) if add_str != "-" else 0
            d = int(del_str) if del_str != "-" else 0
            if filepath not in file_churn:
                file_churn[filepath] = {
                    "additions": 0,
                    "deletions": 0,
                    "commits": 0,
                    "authors": set(),
                }
            file_churn[filepath]["additions"] += add
            file_churn[filepath]["deletions"] += d
            file_churn[filepath]["commits"] += 1
        else:
            parts = line.split(" ", 2)
            if len(parts) == 3:
                commit_hash, _, author = parts
                commits.add(commit_hash)
                authors.add(author)

    churn: list[GitChurn] = []
    for filepath, data in file_churn.items():
        churn.append(
            GitChurn(
                filepath=filepath,
                additions=data["additions"],
                deletions=data["deletions"],
                commits=data["commits"],
                authors=data["authors"],
            )
        )
    churn.sort(key=lambda x: x.additions + x.deletions, reverse=True)

    hotspots = sorted(
        churn,
        key=lambda x: x.additions + x.deletions,
        reverse=True,
    )[:20]  # Top 20 most-churned files = hotspots

    return GitInfo(
        total_commits=len(commits),
        total_authors=len(authors),
        churn=churn,
        hotspots=hotspots,
    )
