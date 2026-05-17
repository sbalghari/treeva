from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path
    from logging import Logger

from dataclasses import dataclass
from datetime import datetime
import stat

from .file_info import FileInfo
from treeva.constants import OutputFormat
from treeva.library.utils import format_size, is_hidden


@dataclass
class DirInfo:
    dirname: str
    full_path: Path
    files_count: int
    size_in_bytes: int
    language_count: dict[
        str, list[int]
    ]  # {Language name: [files count, LOC, comment lines]}, LOC and comments lines are both 0 for non code files
    is_hidden: bool
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    owner: str
    group: str
    subdirectory_count: int
    symlinks_count: int
    empty_files_count: int
    hidden_files_count: int
    total_loc: int
    total_comments: int
    comment_density: float
    largest_file: dict[str, Any]
    oldest_file_date: datetime | None
    newest_file_date: datetime | None
    executable_files_count: int
    readonly_files_count: int

    @classmethod
    def from_path(
        cls, dirpath: Path, *, logger: Logger, format: OutputFormat
    ) -> DirInfo:
        """
        Create a DirInfo instance from a directory path by walking that directory and aggregating metrics
        """
        files_count = 0
        subdirectory_count = 0
        size_in_bytes = 0
        language_count = {}
        symlinks_count = 0
        empty_files_count = 0
        hidden_files_count = 0
        total_loc = 0
        total_comments = 0
        largest_file = {"name": "", "size": 0}
        oldest_file_date = None
        newest_file_date = None
        executable_files_count = 0
        readonly_files_count = 0

        from treeva.scaners import dir_walker

        for file in dir_walker(dirpath):
            if file.is_dir():
                subdirectory_count += 1
            else:
                files_count += 1

                fileinfo = FileInfo.from_path(file, logger=logger)

                size_in_bytes += fileinfo.size_in_bytes

                # Update new metrics
                if fileinfo.is_symlink:
                    symlinks_count += 1
                if fileinfo.size_in_bytes == 0:
                    empty_files_count += 1
                if fileinfo.is_hidden:
                    hidden_files_count += 1
                if fileinfo.size_in_bytes > largest_file["size"]:
                    largest_file = {
                        "name": fileinfo.filename,
                        "size": fileinfo.size_in_bytes,
                    }

                total_loc += fileinfo.loc
                total_comments += fileinfo.comments_line

                # Track oldest/newest file dates
                if (
                    oldest_file_date is None
                    or fileinfo.modified_at < oldest_file_date
                ):
                    oldest_file_date = fileinfo.modified_at
                if (
                    newest_file_date is None
                    or fileinfo.modified_at > newest_file_date
                ):
                    newest_file_date = fileinfo.modified_at

                # Check permissions
                if (
                    "x" in fileinfo.permissions[1:]
                ):  # Skip first char (file type)
                    executable_files_count += 1
                if "w" not in fileinfo.permissions:
                    readonly_files_count += 1

                lang = fileinfo.file_type.value
                language_count[lang] = language_count.get(lang, [0, 0, 0])
                language_count[lang][0] += 1
                language_count[lang][1] += fileinfo.loc
                language_count[lang][2] += fileinfo.comments_line

        stat_info = dirpath.stat()
        owner = FileInfo._get_owner(stat_info.st_uid)
        group = FileInfo._get_group(stat_info.st_gid)
        comment_density = (
            ((total_comments / total_loc) * 100) if total_comments > 0 else 0
        )

        data = cls(
            dirname=dirpath.name,
            full_path=dirpath,
            is_hidden=is_hidden(dirpath),
            files_count=files_count,
            size_in_bytes=size_in_bytes,
            language_count=language_count,
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            accessed_at=datetime.fromtimestamp(stat_info.st_atime),
            permissions=stat.filemode(stat_info.st_mode),
            owner=owner,
            group=group,
            subdirectory_count=subdirectory_count,
            symlinks_count=symlinks_count,
            empty_files_count=empty_files_count,
            hidden_files_count=hidden_files_count,
            total_loc=total_loc,
            total_comments=total_comments,
            comment_density=comment_density,
            largest_file=largest_file,
            oldest_file_date=oldest_file_date,
            newest_file_date=newest_file_date,
            executable_files_count=executable_files_count,
            readonly_files_count=readonly_files_count,
        )

        return cls._format(data, format)

    @classmethod
    def _format(cls, data, format: OutputFormat):
        if format == "python-object":
            return data

        if format == "json":
            _dict: dict[str, Any] = {
                "Directory name": data.dirname,
                "Full path": str(data.full_path),
                "Files count": data.files_count,
                "Size": format_size(data.size_in_bytes),
                "Size in bytes": data.size_in_bytes,
                "Language count": {
                    lang: {
                        "Files count": counts[0],
                        "LOC": counts[1],
                        "Comments line": counts[2],
                    }
                    for lang, counts in data.language_count.items()
                },
                "Is hidden": data.is_hidden,
                "Created at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Modified at": data.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Accessed at": data.accessed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Permissions": data.permissions,
                "Owner": data.owner,
                "Group": data.group,
                "Subdirectory count": data.subdirectory_count,
                "Symlinks count": data.symlinks_count,
                "Empty files count": data.empty_files_count,
                "Hidden files count": data.hidden_files_count,
                "Total LOC": data.total_loc,
                "Total comments": data.total_comments,
                "Code Comment density %": f"{data.comment_density:.2f}",
                "Largest file": {
                    "name": data.largest_file["name"],
                    "size": format_size(data.largest_file["size"]),
                    "size in bytes": data.largest_file["size"],
                },
                "Oldest file date": data.oldest_file_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if data.oldest_file_date
                else None,
                "Newest file date": data.newest_file_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if data.newest_file_date
                else None,
                "Executable files count": data.executable_files_count,
                "Readonly files count": data.readonly_files_count,
            }
            return _dict

        if format == "plain-text":
            # Build language stats section
            lang_lines = []
            for lang, counts in sorted(
                data.language_count.items(),
                key=lambda x: x[1][0],
                reverse=True,
            ):
                files_count, loc, comments = counts
                lang_lines.append(
                    f"   ├─ {lang:<20} {files_count:>5} files, {loc:>7} LOC, {comments:>5} comments"
                )

            lang_section = (
                "\n".join(lang_lines) if lang_lines else "   └─ No files"
            )

            text_output = f"""
╔══════════════════════════════════════════════════════════════╗
║               DIRECTORY INFORMATION                          ║
╚══════════════════════════════════════════════════════════════╝

Directory:          {data.dirname}
Full path:          {data.full_path}
Files:              {data.files_count:,}
Subdirectories:     {data.subdirectory_count:,}
Total size:         {format_size(data.size_in_bytes)}
Size (bytes):       {data.size_in_bytes:,}
Symlinks:           {data.symlinks_count}
Empty files:        {data.empty_files_count}
Hidden files:       {data.hidden_files_count}

Programming Languages:
{lang_section}

Code Statistics:
   ├─ Total LOC:       {data.total_loc:,}
   ├─ Total comments:  {data.total_comments:,}
   ├─ Comment ratio:   {data.comment_density:.2f}%
   └─ Largest file:    {data.largest_file.get("name", "N/A")} ({format_size(data.largest_file.get("size", 0))})

Permissions:
   ├─ Executable:      {data.executable_files_count}
   └─ Read-only:       {data.readonly_files_count}

Owner/Group:        {data.owner} / {data.group}
Permissions:        {data.permissions}

Timestamps:
   ├─ Created:         {data.created_at.strftime("%Y-%m-%d %H:%M:%S")}
   ├─ Modified:        {data.modified_at.strftime("%Y-%m-%d %H:%M:%S")}
   ├─ Accessed:        {data.accessed_at.strftime("%Y-%m-%d %H:%M:%S")}
   ├─ Oldest file:     {data.oldest_file_date.strftime("%Y-%m-%d %H:%M:%S") if data.oldest_file_date else "N/A"}
   └─ Newest file:     {data.newest_file_date.strftime("%Y-%m-%d %H:%M:%S") if data.newest_file_date else "N/A"}

Hidden:             {"Yes" if data.is_hidden else "No"}
"""
            return text_output.strip()

        if format == "rich-table":
            return data
