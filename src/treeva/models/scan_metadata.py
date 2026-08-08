from dataclasses import dataclass


@dataclass
class ScanMetadata:
    scanned_files: int
    ignored_files: int
    failed_files: int
    duration_seconds: float
