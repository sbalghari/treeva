from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from treeva.models import AnalysisResult

from rich.table import Table
from rich.panel import Panel

from treeva.cli.output.console import CONSOLE, COLORS
from ...utils import format_size



def analysis_result_table(analysis_result: AnalysisResult) -> None:
    """Display AnalysisResult as a Rich tables.

    Args:
        analysis_result: The AnalysisResult model instance to display.
    """
    dir_info = analysis_result.dir_info
    code_metrics = analysis_result.code_metrics
    code_quality = analysis_result.code_quality
    languages = analysis_result.languages_stats
    docs = analysis_result.documentation_info
    entities = analysis_result.entities
    scan = analysis_result.scan_metadata
    dir_structure = analysis_result.dir_structure

    # -------------------------
    # Project Overview
    # -------------------------
    overview_table = Table(show_header=False, box=None, padding=(0, 1))
    overview_table.add_row("Project Name", dir_info.dirname)
    overview_table.add_row("Project Path", str(dir_info.full_path))

    # -------------------------
    # Project Statistics
    # -------------------------
    proj_stats = Table(title="Project Statistics", expand=True)
    proj_stats.add_column("Metric", style=COLORS["mauve"], width=25)
    proj_stats.add_column("Value", justify="right", style=COLORS["text"])

    proj_stats.add_row("Total Files", f"{dir_info.files_count:,}")
    proj_stats.add_row("Total Directories", f"{dir_info.subdirectory_count:,}")
    proj_stats.add_row(
        "Total Project Size", format_size(dir_info.size_in_bytes)
    )
    proj_stats.add_row(
        "Deepest Directory", str(dir_structure.deepest_directory_depth)
    )
    proj_stats.add_row(
        "Avg Files per Directory",
        f"{dir_structure.average_files_per_directory:.2f}",
    )
    proj_stats.add_row(
        "Empty Directories", str(dir_structure.empty_directory_count)
    )

    # -------------------------
    # Code Metrics
    # -------------------------
    code_table = Table(title="Code Metrics", expand=True)
    code_table.add_column("Metric", style=COLORS["mauve"], width=25)
    code_table.add_column("Value", justify="right", style=COLORS["text"])

    code_table.add_row(
        "Total Lines of Code", f"{code_metrics.lines_of_code:,}"
    )
    code_table.add_row("Total Comments", f"{code_metrics.lines_of_comment:,}")
    code_table.add_row("Total Blank Lines", f"{code_metrics.blank_lines:,}")
    code_table.add_row(
        "Comment Density", f"{code_metrics.comment_density:.1f}%"
    )

    effective_loc = code_metrics.lines_of_code - code_metrics.lines_of_comment
    code_table.add_row("Effective LOC", f"{effective_loc:,}")

    code_table.add_row("Total Imports", f"{code_metrics.import_count:,}")
    code_table.add_row("Total Classes", f"{code_metrics.class_count:,}")
    code_table.add_row("Total Functions", f"{code_metrics.function_count:,}")
    code_table.add_row("Total Methods", f"{code_metrics.method_count:,}")
    code_table.add_row("Total Branches", f"{code_metrics.branches_count:,}")
    code_table.add_row("Total Loops", f"{code_metrics.loops_count:,}")
    code_table.add_row(
        "Max Nesting Depth", str(code_metrics.max_nesting_depth)
    )
    code_table.add_row(
        "Avg Nesting Depth", f"{code_metrics.average_nesting_depth:.2f}"
    )

    # -------------------------
    # Code Quality
    # -------------------------
    quality_table = Table(title="Code Quality", expand=True)
    quality_table.add_column("Metric", style=COLORS["mauve"], width=25)
    quality_table.add_column("Value", justify="right", style=COLORS["text"])

    quality_table.add_row(
        "Cyclomatic Complexity", f"{code_quality.cyclomatic_complexity:,}"
    )
    quality_table.add_row(
        "Maintainability Index",
        f"{code_quality.maintainability_index:.1f}/100",
    )
    documented = (
        docs.documented_functions
        + docs.documented_classes
        + docs.documented_methods
    )
    total_symbols = (
        documented
        + docs.undocumented_functions
        + docs.undocumented_classes
        + docs.undocumented_methods
    )
    doc_coverage = (documented / total_symbols * 100) if total_symbols else 0
    quality_table.add_row("Documentation Coverage", f"{doc_coverage:.1f}%")

    # -------------------------
    # Largest Entities
    # -------------------------
    entities_table = Table(title="Largest Entities", expand=True)
    entities_table.add_column("Entity", style=COLORS["mauve"], width=25)
    entities_table.add_column("Name", style=COLORS["sky"])
    entities_table.add_column(
        "Location / Size", justify="right", style=COLORS["text"]
    )

    entities_table.add_row(
        "File",
        entities.file.path.name,
        f"{format_size(entities.file.size)} ({entities.file.loc:,} LOC)",
    )
    if entities.function:
        entities_table.add_row(
            "Function",
            entities.function.name,
            f"{entities.function.loc:,} LOC",
        )
    if entities.cls:
        entities_table.add_row(
            "Class",
            entities.cls.name,
            f"{entities.cls.loc:,} LOC",
        )

    # -------------------------
    # File Distribution
    # -------------------------
    distribution_table = Table(title="File Distribution", expand=True)
    distribution_table.add_column("Language", style=COLORS["sky"])
    distribution_table.add_column(
        "Files", justify="right", style=COLORS["green"]
    )

    for lang, count in sorted(
        dir_info.source_files_count.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        distribution_table.add_row(lang, f"{count:,}")

    # -------------------------
    # Top Languages (LOC)
    # -------------------------
    lang_table = Table(title="Top Programming Languages by LOC", expand=True)
    lang_table.add_column("Language", style=COLORS["sky"], width=20)
    lang_table.add_column(
        "Lines of Code", justify="right", style=COLORS["green"]
    )
    lang_table.add_column(
        "Percentage", justify="right", style=COLORS["yellow"]
    )

    for lang, loc in languages.top_languages:
        percentage = languages.distribution.get(lang, 0)
        lang_table.add_row(lang, f"{loc:,}", f"{percentage:.1f}%")

    # -------------------------
    # Scan Metadata
    # -------------------------
    scan_table = Table(title="Scan Details", expand=True)
    scan_table.add_column("Metric", style=COLORS["mauve"], width=25)
    scan_table.add_column("Value", justify="right", style=COLORS["text"])

    scan_table.add_row("Scanned Files", f"{scan.scanned_files:,}")
    scan_table.add_row("Ignored Files", f"{scan.ignored_files:,}")
    scan_table.add_row("Failed Files", f"{scan.failed_files:,}")
    scan_table.add_row("Duration", f"{scan.duration_seconds:.2f}s")

    # -------------------------
    # Timeline
    # -------------------------
    timeline_table = Table(title="Project Timeline", expand=True)
    timeline_table.add_column("Event", style=COLORS["mauve"], width=25)
    timeline_table.add_column("Timestamp", style=COLORS["text"])

    timeline_table.add_row(
        "Created",
        dir_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
    timeline_table.add_row(
        "Modified",
        dir_info.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
    timeline_table.add_row(
        "Oldest File",
        dir_info.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if dir_info.oldest_file_date
        else "N/A",
    )
    timeline_table.add_row(
        "Newest File",
        dir_info.newest_file_date.strftime("%Y-%m-%d %H:%M:%S")
        if dir_info.newest_file_date
        else "N/A",
    )

    # Output
    CONSOLE.print(
        Panel(
            overview_table,
            title="Project Analysis",
            border_style="border.success",
            expand=False,
        )
    )

    CONSOLE.print(proj_stats)
    CONSOLE.print(code_table)
    CONSOLE.print(quality_table)
    CONSOLE.print(entities_table)
    CONSOLE.print(distribution_table)

    if languages.top_languages:
        CONSOLE.print(lang_table)

    CONSOLE.print(scan_table)
    CONSOLE.print(timeline_table)
