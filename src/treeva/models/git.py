from dataclasses import dataclass, field


@dataclass
class GitChurn:
    """Per-file change statistics from git history."""

    filepath: str
    additions: int
    deletions: int
    commits: int
    authors: set[str] = field(default_factory=set)


@dataclass
class GitInfo:
    """Aggregate git analysis with churn and top hotspots."""

    total_commits: int
    total_authors: int
    churn: list[GitChurn]
    hotspots: list[GitChurn]
