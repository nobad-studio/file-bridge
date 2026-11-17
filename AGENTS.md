# NOBAD File Bridge: instructions for AI coding assistants

This is the repository `nobad-studio/file-bridge` (split from `nobad-studio/Nobad-VPN` with its full history on
2026-11-17). NOBAD-wide rules and project memory live in [`nobad-studio/Nobad-VPN`](https://github.com/nobad-studio/Nobad-VPN)
(`AGENTS.md`, `docs/ai/memory.md`); read them too.

NOBAD File Bridge is a desktop file manager for remote servers (SSH/SFTP, FTP/FTPS, transfers, sync, remote editing,
terminals, an encrypted credential vault, deployments). Python 3.12; the window is a web UI (`app_web/`) in pywebview. Author and code owner:
@harshRaj1601. Part of NOBAD: *software with a point of view*.

## Commands (from the repository root)
- Install: `pip install -e ".[dev]"` (CI should move to `uv sync --locked`, see #5)
- Tests: `python -m pytest -q tests` (Qt offscreen: `QT_QPA_PLATFORM=offscreen`). CI: `.github/workflows/tests.yml`.
- Run: `python -m app.main` (the web UI; see `docs/WEB-UI.md`) · `--browser` opens it in a web browser
- Package: `uv run --with pyinstaller pyinstaller --clean --noconfirm build.spec` (on the target OS), then
  `packaging/linux/build-deb.sh` on Linux
- Web UI screenshots (temporary database, never commit them): `python -I scripts/ui_screenshots.py <folder> [screen ...]`

## Current work: start here
Pick up from the top. Each item says what "done" means. Update this list in the PR that finishes an item.

| # | Task | Done when |
|---|---|---|
| 1 | **Sign the CLA** (a human step for @harshRaj1601): comment `I have read the CLA Document and I hereby sign the CLA` on [PR #1](https://github.com/nobad-studio/file-bridge/pull/1). | The `cla` check on #1 is green. |
| 2 | **Make the test suite pass** on [PR #2](https://github.com/nobad-studio/file-bridge/pull/2) (web UI stage 3): run `python -m pytest -q tests`, fix the failures in the code (not by deleting or skipping tests). | `file-bridge-tests` is green on #2. |
| 3 | [#4](https://github.com/nobad-studio/file-bridge/issues/4) (medium) private data folder: data folder 0700, database 0600, no shared `/tmp` fallback. Already implemented in PR #1. | #1 merged (it says `Fixes #4`). |
| 4 | [#3](https://github.com/nobad-studio/file-bridge/issues/3) (high) Monaco loaded from cdnjs/unpkg without integrity, in a page with a Python bridge: bundle it locally under `resources/editor/`. | No CDN URL left (`git grep -n "cdnjs\|unpkg"` is empty), the editor still loads, test added. |
| 5 | [#5](https://github.com/nobad-studio/file-bridge/issues/5) (low) green suite plus smaller hardening (quoting, Argon2 limits, auto-lock, export permissions, `xargs -0`); move CI to `uv sync --locked` so dependencies are pinned. | Issue checklist done; CI installs from `uv.lock`. |

Fixed already: remote names writing outside the download folder (Nobad-VPN #29, PR #34) and the sudo password on a
server-controlled prompt (Nobad-VPN #32, PR #36). Don't release NOBAD File Bridge before items 3 to 5 are done.
Close an issue in the PR that fixes it (`Fixes #3`), with a test that would have caught it.

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
