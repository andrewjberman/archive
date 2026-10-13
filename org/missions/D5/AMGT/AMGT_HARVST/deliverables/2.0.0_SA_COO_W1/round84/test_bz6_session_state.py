"""HVST-bz-6 instrument: it prints state and mints once, and it never prints a secret-bearing field. No network, no browser."""
import datetime as dt
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bz6", str(Path(__file__).with_name("bz6_session_state.py")))
bz6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bz6)

NOW = dt.datetime(2026, 10, 13, 12, 0, tzinfo=dt.timezone.utc)
SECRET_BEARING = {"bundle": {"all_cookies": [{"name": "djcs_auth", "value": "COOKIE-VALUE-123"}], "user_agent": "UA-STRING"},
                  "auth_evidence": {"subscriber": True, "visible_status": "USERNAME-ABC logged in", "username": "USERNAME-ABC"},
                  "network_auth_corroborated": True, "captured_at": "2026-10-12T12:00:00+00:00"}


class Vault:
    def __init__(self, envelope, raises=None):
        self.envelope, self.raises = envelope, raises

    def __call__(self, root):
        return self

    def load(self, publisher):
        if self.raises:
            raise self.raises
        return self.envelope


class Manager:
    calls = []

    def __init__(self, envelope=None, raises=None):
        self.envelope, self.raises = envelope, raises

    def __call__(self, root, record):
        record({"event": "reauth_started", "publisher": "wsj", "cookie": "SHOULD-NOT-SURVIVE"})
        return self

    def refresh(self, publisher):
        Manager.calls.append(publisher)
        if self.raises:
            raise self.raises
        return self.envelope


def run(capsys, argv, vault, manager=None):
    Manager.calls = []
    rc = bz6.main(["wsj", "--runtime-root", "x"] + argv, vault_factory=vault, manager_factory=manager, now=NOW)
    return rc, capsys.readouterr().out


def test_state_is_read_only_and_prints_no_secret(capsys):
    rc, out = run(capsys, [], Vault(SECRET_BEARING))
    assert rc == 0 and "present=True subscriber=True network_auth_corroborated=True" in out and "age_days=1.0" in out
    for token in ("COOKIE-VALUE-123", "UA-STRING", "USERNAME-ABC", "djcs_auth"):
        assert token not in out
    assert Manager.calls == []


def test_absent_session_without_mint_makes_no_sign_in(capsys):
    rc, out = run(capsys, [], Vault(None))
    assert rc == 0 and "present=False" in out and "VALID=False" in out and Manager.calls == []


def test_mint_is_skipped_when_the_saved_session_is_valid(capsys):
    rc, out = run(capsys, ["--mint"], Vault(SECRET_BEARING), Manager(SECRET_BEARING))
    assert rc == 0 and "SKIPPED" in out and Manager.calls == []


def test_mint_signs_in_once_when_absent_and_prints_no_secret(capsys):
    rc, out = run(capsys, ["--mint"], Vault(None), Manager(SECRET_BEARING))
    assert rc == 0 and Manager.calls == ["wsj"] and "MINT wsj DONE present=True subscriber=True" in out
    for token in ("COOKIE-VALUE-123", "UA-STRING", "USERNAME-ABC", "SHOULD-NOT-SURVIVE"):
        assert token not in out


def test_a_refused_mint_names_the_class_only_and_is_not_retried(capsys):
    rc, out = run(capsys, ["--mint"], Vault(None), Manager(raises=RuntimeError("password=HUNTER2 rejected")))
    assert rc == 3 and "MINT wsj REFUSED: RuntimeError" in out and "HUNTER2" not in out and Manager.calls == ["wsj"]


def test_an_unreadable_vault_names_the_class_only(capsys):
    rc, out = run(capsys, [], Vault(None, raises=ValueError("token=ABCDEF")))
    assert rc == 0 and "unreadable=ValueError" in out and "ABCDEF" not in out
