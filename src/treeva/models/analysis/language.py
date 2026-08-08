from dataclasses import dataclass


@dataclass
class LanguageStatistics:
    top_languages: list[tuple[str, int]]
    distribution: dict[str, float]
    loc_per_language: dict[str, int]
