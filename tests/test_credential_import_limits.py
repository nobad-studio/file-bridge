"""A crafted vault export can't make the app derive a key with absurd Argon2 parameters (issue #5)."""
from __future__ import annotations

import json

import pytest

from credentials import import_export
from credentials.crypto import KdfConfig, kdf_from_untrusted


def test_normal_settings_pass() -> None:
    assert kdf_from_untrusted(KdfConfig().to_dict()) == KdfConfig()


@pytest.mark.parametrize("change", [
    {"memory_cost": 4 * 1024 * 1024 * 1024}, {"time_cost": 100_000}, {"parallelism": 4096}, {"hash_len": 4096},
    {"name": "scrypt"}, {"memory_cost": "lots"},
])
def test_crafted_settings_are_refused(change: dict) -> None:
    with pytest.raises(ValueError):
        kdf_from_untrusted({**KdfConfig().to_dict(), **change})


def test_import_refuses_before_deriving_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    def explode(*_a, **_k):  # type: ignore[no-untyped-def]
        raise AssertionError("derive_key must not run for a crafted file")

    monkeypatch.setattr(import_export, "derive_key", explode)
    vault = type("V", (), {"is_unlocked": True})()
    service = import_export.CredentialImportExportService.__new__(import_export.CredentialImportExportService)
    service.vault = vault
    bundle = {"format": "rfm-vault", "kdf": {**KdfConfig().to_dict(), "memory_cost": 2 ** 31}, "salt": "AAAA", "payload": "x"}
    result = service.import_encrypted(json.dumps(bundle), "password")
    assert not result.ok and "safe range" in (result.technical_details or "")
