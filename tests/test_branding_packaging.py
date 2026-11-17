from __future__ import annotations

from pathlib import Path

from app_web import window

BRANDING = Path("resources/branding")


def test_branding_is_the_blue_nobad_mark_and_the_old_icon_is_gone() -> None:
    for size in (16, 24, 32, 48, 64, 128, 256, 512):
        assert (BRANDING / f"nobad-file-bridge-{size}.png").is_file()
    assert (BRANDING / "nobad-file-bridge.ico").is_file()
    assert not list(BRANDING.glob("remote-file-manager*"))          # the old green/blue terminal icon


def test_icon_files_are_real_multi_size_icons() -> None:
    for ico in (BRANDING / "nobad-file-bridge.ico", Path("app_web/ui/brand/favicon.ico")):
        data = ico.read_bytes()
        assert data[:4] == b"\x00\x00\x01\x00"                       # ICO header
        assert int.from_bytes(data[4:6], "little") >= 6              # 16 ... 256 px
    png = (BRANDING / "nobad-file-bridge-256.png").read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert int.from_bytes(png[16:20], "big") == int.from_bytes(png[20:24], "big") == 256


def test_window_uses_the_app_icon() -> None:
    path = window.window_icon()
    assert path and Path(path).is_file() and Path(path).parent == window.BRANDING
    assert "icon=window_icon()" in Path("app_web/window.py").read_text(encoding="utf-8")


def test_pyinstaller_spec_includes_resources_and_app_icon() -> None:
    source = Path("build.spec").read_text(encoding="utf-8")

    assert '"nobad-file-bridge.ico"' in source
    assert 'globals().get("SPECPATH", ".")' in source
    assert "icon=str(APP_ICON)" in source
    assert '(str(RESOURCES_DIR), "resources")' in source
    assert '"credentials"' in source
    assert '"deployment"' in source
    assert '"keyring.backends"' in source
    assert '"argon2-cffi"' in source
    assert "exclude_binaries=True" in source


def test_installer_uses_the_app_icon() -> None:
    assert "SetupIconFile=..\\..\\resources\\branding\\nobad-file-bridge.ico" in Path(
        "packaging/windows/installer.iss").read_text(encoding="utf-8")


def test_linux_deb_packaging_metadata_uses_launcher_icon() -> None:
    desktop = Path("packaging/linux/nobad-file-bridge.desktop").read_text(encoding="utf-8")
    build_script = Path("packaging/linux/build-deb.sh").read_text(encoding="utf-8")

    assert "Icon=nobad-file-bridge" in desktop
    assert "Exec=nobad-file-bridge" in desktop
    assert 'BIN_DIR="${PACKAGE_ROOT}/usr/bin"' in build_script
    assert "QT_QPA_PLATFORM" in build_script
    assert "QTWEBENGINE_CHROMIUM_FLAGS" in build_script
    assert "resources/branding/nobad-file-bridge-256.png" in build_script
    assert "libxcb-cursor0" in build_script
    assert "libxkbcommon-x11-0" in build_script
    assert "libasound2t64 | libasound2" in build_script
    assert "dpkg-deb --build" in build_script
