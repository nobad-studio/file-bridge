# NOBAD File Bridge: instructions for AI coding assistants

This is the repository `nobad-studio/file-bridge` (split from `nobad-studio/Nobad-VPN` with its full history on
2026-11-17). NOBAD-wide rules and project memory live in [`nobad-studio/Nobad-VPN`](https://github.com/nobad-studio/Nobad-VPN)
(`AGENTS.md`, `docs/ai/memory.md`); read them too.

NOBAD File Bridge is a desktop file manager for remote servers (SSH/SFTP, FTP/FTPS, transfers, sync, remote editing,
terminals, an encrypted credential vault, deployments). Python 3.12 + PySide6. Author and code owner:
@harshRaj1601. Part of NOBAD: *software with a point of view*.

## Commands (from the repository root)
- Install: `pip install -e ".[dev]"` (CI should move to `uv sync --locked`, see #33)
- Tests: `python -m pytest -q tests` (Qt offscreen: `QT_QPA_PLATFORM=offscreen`). CI: `.github/workflows/tests.yml`.
- Run: `python -m app.main` (classic Qt UI) · `python -m app.web` (new web UI, in development; see `docs/WEB-UI.md`)
- Web UI screenshots (temporary database, never commit them): `python -I scripts/ui_screenshots.py <folder> [screen ...]`

## Before the first NOBAD File Bridge release: fix these (open issues)
| Issue | Severity | What |
|---|---|---|
| [#29](https://github.com/nobad-studio/Nobad-VPN/issues/29) | high | Remote file names can make downloads write outside the target folder (`file_ops/sftp_ops.py`, `transfers/transfer_manager.py`, `file_ops/ftp_ops.py`). Validate names; always use `safety.safe_destination`. |
| [#30](https://github.com/nobad-studio/Nobad-VPN/issues/30) | high | Monaco loaded from cdnjs/unpkg without integrity, in a page with a Python bridge. Bundle it locally. |
| [#31](https://github.com/nobad-studio/Nobad-VPN/issues/31) | medium | Data folder 0700, database 0600; no shared `/tmp` fallback. |
| [#32](https://github.com/nobad-studio/Nobad-VPN/issues/32) | medium | Don't auto-type the sudo password on server-controlled output (`sudo -S -p <nonce>`). |
| [#33](https://github.com/nobad-studio/Nobad-VPN/issues/33) | low | Green test suite plus smaller hardening (quoting, Argon2 limits, auto-lock, export permissions, `xargs -0`). |

Close an issue in the PR that fixes it (`Fixes #29`), with a test that would have caught it.

## Rules for this project
- **Remote servers are untrusted.** Every name, path, listing or output from a server is attacker-controlled: never
  join it into a local path without `safe_destination`, never splice it into a shell command without `shlex.quote`,
  never treat it as a prompt to answer with a secret.
- **Secrets:** vault keys stay in memory only while unlocked; nothing secret in logs, exports or the database in
  plaintext; files that hold secrets are 0600.
- **No new outbound connections** (CDNs, telemetry, update checks) without a setting and documentation.
- **Verification on by default:** SSH host keys (unknown host = ask, changed key = refuse by default) and TLS
  certificates. Disabling either is opt-in and shows a warning.
- Every change comes with tests; `python -m pytest -q tests` must pass.

## How changes land
Branch → pull request against `main`; the `file-bridge-tests` check runs this suite on every PR. The
`file-bridge` team (@harshRaj1601) maintains this repository; workflows (`.github/`) stay with @AryanGupta-234. Copilot reviews every PR automatically; treat its comments as advice.
Releases of NOBAD File Bridge will get their own tag pattern and workflow when it's ready: ask the maintainer first.

## Shared memory (all NOBAD repos)
Decisions, open items and ideas shared by every contributor and AI assistant live in
[`nobad-studio/memory`](https://github.com/nobad-studio/memory). Read its `INDEX.md` first (one line per fact; Claude
Code loads it automatically at session start through `.claude/settings.json`), open a fact only when it matters, and
check who else is working on what with `python tools/mem.py status` there. Record new decisions as a PR to that repo
(its `AGENTS.md`, or the `nobad-memory` skill), never secrets.
