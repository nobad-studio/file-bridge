"""Pruning old deployment backups runs the real command in a real shell: names with spaces are kept whole (issue #5)."""
from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from core.result import OperationResult
from deployment.backup_manager import BackupManager

BASH = shutil.which("bash")


def _shell_path(path: Path) -> str:
    text = str(path).replace("\\", "/")
    if os.name == "nt" and len(text) > 1 and text[1] == ":":      # Git Bash: C:/x -> /c/x
        text = "/" + text[0].lower() + text[2:]
    return text


class ShellConnection:
    async def run_command(self, command: str, *, cwd: str | None = None) -> OperationResult:
        done = subprocess.run([BASH, "-c", command], capture_output=True, text=True, timeout=30)
        return OperationResult.success("ok", data={"stdout": done.stdout, "stderr": done.stderr, "exit_status": done.returncode})


@pytest.mark.skipif(BASH is None or subprocess.run([BASH, "-c", "find --version"], capture_output=True).returncode != 0,
                    reason="needs bash and GNU find")
def test_prune_keeps_the_newest_and_handles_spaces(tmp_path: Path) -> None:
    folder = tmp_path / "my site" / ".rfm-backups"
    folder.mkdir(parents=True)
    (tmp_path / "my").mkdir()                                     # a decoy that a space-split path would hit
    decoy = tmp_path / "my" / "keep.tar.gz"
    decoy.write_text("not a backup of this site")
    names = [f"site backup {n}.tar.gz" for n in range(5)]
    for n, name in enumerate(names):
        path = folder / name
        path.write_text(str(n))
        stamp = time.time() - (100 - n * 10)                         # later n = newer
        os.utime(path, (stamp, stamp))

    result = asyncio.run(BackupManager().prune_backups(ShellConnection(), _shell_path(folder), retention=2))

    assert result.ok, result
    assert sorted(p.name for p in folder.iterdir()) == ["site backup 3.tar.gz", "site backup 4.tar.gz"]
    assert decoy.exists()
