"""Release readiness: one version everywhere, a self-check the release workflow runs on the packaged app, and a
release workflow that only publishes from a matching tag, from a job that runs no build code."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

from app import __version__
from app import main as entry
from app_web.context import app_version


def test_one_version_everywhere() -> None:
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    newest = re.search(r"^## (\d+\.\d+\.\d+)", Path("CHANGELOG.md").read_text(encoding="utf-8"), re.M).group(1)
    assert __version__ == project == newest
    assert app_version() in {__version__, project}


def test_self_check_passes_from_source(capsys) -> None:  # type: ignore[no-untyped-def]
    assert entry.main(["--self-check"]) == 0
    assert f"NOBAD File Bridge {__version__}" in capsys.readouterr().out


def test_release_workflow_publishes_only_from_tags_with_pinned_tools() -> None:
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert 'tags: ["v*"]' in text and "if: startsWith(github.ref, 'refs/tags/v')" in text
    assert "permissions:\n  contents: read" in text                         # read-only by default
    assert text.count("contents: write") == 1                               # only the publish job writes
    assert "pyinstaller==6.22.3" in text and "uv sync --locked" in text
    assert text.count("--self-check") == 3                  # both packaged apps, and the app the installer installed
    assert all(re.search(r"@[0-9a-f]{40}", line) for line in text.splitlines() if "uses:" in line)


def test_windows_checksum_file_uses_lf() -> None:
    # Out-File writes CRLF, which `sha256sum -c` rejects; the checksum file is written with "`n" and no BOM.
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "Out-File" not in text
    assert "[IO.File]::WriteAllText($sum, \"$h  $name`n\", [Text.UTF8Encoding]::new($false))" in text


def test_windows_release_is_an_installer() -> None:
    text = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "choco install innosetup --version 6.7.1" in text                 # pinned, like NOBAD VPN's
    assert "packaging\\windows\\installer.iss" in text and "Compress-Archive" not in text
    assert "dist/*.exe" in text                                              # the installer is attested
    iss = Path("packaging/windows/installer.iss").read_text(encoding="utf-8")
    assert "OutputBaseFilename=NobadFileBridge-Setup-{#MyAppVersion}" in iss
    assert "PrivilegesRequired=lowest" in iss                                # no admin prompt by default
    assert "MB_DEFBUTTON2" in iss                                            # deleting your data defaults to No
    assert "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" in iss                   # the WebView2 runtime check
    # Every file the script reads (paths are relative to packaging/windows) exists in the repository.
    for rel in ("resources/branding/nobad-file-bridge.ico", "LICENSE", "THIRD-PARTY-NOTICES.md"):
        assert "..\\..\\" + rel.replace("/", "\\") in iss and Path(rel).exists(), rel
