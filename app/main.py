"""Start NOBAD File Bridge.

    nobad-file-bridge              # the app window
    nobad-file-bridge --browser    # the same app in your web browser
    nobad-file-bridge --self-check # check a (packaged) build without opening a window

``python -m app.main`` does the same."""
from __future__ import annotations

import sys

CLASSIC_REMOVED = ("The classic Qt window was removed; File Bridge's window now has every screen it had. "
                   "Start it without --classic.")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--classic" in args:
        print(CLASSIC_REMOVED, file=sys.stderr)
        return 2
    if "--self-check" in args:
        return self_check()
    from app.web import main as web_main

    return web_main(args)


def self_check() -> int:
    """Load what the window needs without opening it: for checking a packaged build (CI runs it on the bundle)."""
    from app import __version__
    from app_web.api import HANDLERS
    from app_web.handlers import register_all
    from app_web.server import MONACO_DIR, UI_DIR, index_ui_files

    register_all()
    files = index_ui_files(UI_DIR)
    checks = {"UI pages": "index.html" in files and len(files) > 20, "API handlers": len(HANDLERS) > 50,
              "Monaco editor": (MONACO_DIR / "vs" / "loader.js").is_file()}
    print(f"NOBAD File Bridge {__version__}: {len(files)} UI files, {len(HANDLERS)} API handlers, "
          f"Monaco {'present' if checks['Monaco editor'] else 'missing'}")
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        print("Missing: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
