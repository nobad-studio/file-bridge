from __future__ import annotations

import mimetypes
import stat
from pathlib import Path

from file_ops.base import FileItem, FileKind, local_time


def local_file_item(path: str | Path) -> FileItem:
    item = Path(path)
    info = item.lstat()
    if stat.S_ISDIR(info.st_mode):
        kind = FileKind.DIRECTORY
    elif stat.S_ISLNK(info.st_mode):
        kind = FileKind.SYMLINK
    elif stat.S_ISREG(info.st_mode):
        kind = FileKind.FILE
    else:
        kind = FileKind.OTHER
    return FileItem(
        name=item.name,
        path=str(item),
        kind=kind,
        size=info.st_size if kind == FileKind.FILE else None,
        modified_at=local_time(info.st_mtime),
        permissions=stat.filemode(info.st_mode),
        mime_type=mimetypes.guess_type(item.name)[0],
    )

