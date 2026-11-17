from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum


class FileKind(StrEnum):
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class FileItem:
    name: str
    path: str
    kind: FileKind
    size: int | None = None
    modified_at: datetime | None = None
    permissions: str | None = None
    owner: str | None = None
    group: str | None = None
    mime_type: str | None = None
    checksum: str | None = None

    @property
    def is_dir(self) -> bool:
        return self.kind == FileKind.DIRECTORY

    @property
    def is_file(self) -> bool:
        return self.kind == FileKind.FILE


def human_size(size: int | None) -> str:
    if size is None:
        return ""
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def local_time(timestamp: float | int | None) -> datetime | None:
    """A file time as an aware local datetime, or None when there is none or it can't be shown.

    ``datetime.fromtimestamp(ts).astimezone()`` converts a naive time through ``mktime``; east of UTC a time just after
    1970 becomes negative there, which Windows rejects (``OSError: [Errno 22]``) and one such file made a whole server
    listing fail. Starting from an aware UTC time avoids ``mktime``; times outside what the platform can show (before
    1970 on Windows, far future) are reported as unknown instead of failing."""
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(float(timestamp), timezone.utc).astimezone()
    except (OverflowError, OSError, ValueError):
        return None
