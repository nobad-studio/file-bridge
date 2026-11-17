# NOBAD File Bridge: instructions for AI coding assistants

This is the repository `nobad-studio/file-bridge` (split from `nobad-studio/Nobad-VPN` with its full history on
2026-11-17). NOBAD-wide rules and project memory live in [`nobad-studio/Nobad-VPN`](https://github.com/nobad-studio/Nobad-VPN)
(`AGENTS.md`, `docs/ai/memory.md`); read them too.

NOBAD File Bridge is a desktop file manager for remote servers (SSH/SFTP, FTP/FTPS, transfers, sync, remote editing,
terminals, an encrypted credential vault, deployments). Python 3.12; the window is a web UI (`app_web/`) in pywebview. Author and code owner:
@harshRaj1601. Part of NOBAD: *software with a point of view*.

## Commands (from the repository root)
- Install: `uv sync --locked --extra dev` (what CI uses; `pip install -e ".[dev]"` also works)
- Tests: `python -m pytest -q tests` (Qt offscreen: `QT_QPA_PLATFORM=offscreen`). CI: `.github/workflows/tests.yml`.
- Run: `python -m app.main` (the web UI; see `docs/WEB-UI.md`) · `--browser` opens it in a web browser
- Package: `uv run --with pyinstaller pyinstaller --clean --noconfirm build.spec` (on the target OS), then
  `packaging/linux/build-deb.sh` on Linux
- Web UI screenshots (temporary database, never commit them): `python -I scripts/ui_screenshots.py <folder> [screen ...]`

## Current work: start here
Pick up from the top. Each item says what "done" means. Update this list in the PR that finishes an item.

| # | Task | Done when |
|---|---|---|
| 1 | ~~Sign the CLA~~ | **Done** 2026-11-17 (signature recorded on the `cla-signatures` branch, which the split had left out). |
| 2 | ~~Make the test suite pass on PR #2~~ | **Done**: #2 and the rest of the web UI (#8 to #18) merged with `file-bridge-tests` green. |
| 3 | ~~[#4](https://github.com/nobad-studio/file-bridge/issues/4) private data folder~~ | **Done**: #1 merged. |
| 4 | ~~[#3](https://github.com/nobad-studio/file-bridge/issues/3) Monaco from a CDN~~ | **Done**: #9 bundles Monaco under `resources/editor/vendor/monaco/`. |
| 5 | [#5](https://github.com/nobad-studio/file-bridge/issues/5) green suite plus smaller hardening, and CI installs from `uv.lock`. | The hardening PR is merged (suite green on Windows too) and the CI PR (`uv sync --locked`, a workflow change for @AryanGupta-234) is merged. |
| 6 | **First release.** Needs a release workflow and tag pattern from the maintainer, building the Windows and Linux packages in CI, then a website PR for the File Bridge page. | A CI-built release exists and the website lists it. |

Fixed already: remote names writing outside the download folder (Nobad-VPN #29, PR #34) and the sudo password on a
server-controlled prompt (Nobad-VPN #32, PR #36). Don't release NOBAD File Bridge before item 5 is done.
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
