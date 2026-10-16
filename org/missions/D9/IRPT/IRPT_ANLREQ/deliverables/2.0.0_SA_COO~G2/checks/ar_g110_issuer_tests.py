"""IRPT_ANLREQ AR-g-110 issuer tests (2.0.0_SA_COO~G2): the upload door's resolver is built with the yfinance checker (C-SWAP step 2).

Run by ar_g110_checks.py with AR110_ROOT = the investor-reporting folder to grade. Offline: the vendor transport child is stubbed, the
yfinance history port is a fake. ASCII only.
"""
import base64
import json
import os
import sys
from pathlib import Path


ROOT = Path(os.environ["AR110_ROOT"])
for rel in ("ycharts/session", "ycharts/generate", "intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/extract", "_scope", "_ids", "lib"):
    if (ROOT / rel).is_dir():
        sys.path.insert(0, str(ROOT / rel))

from resident_session import ResidentSession  # noqa: E402
import deadline_transport  # noqa: E402
import yfinance_check  # noqa: E402
from transport import ReplayTransport  # noqa: E402


class Conditional(Exception):
    response = {"Error": {"Code": "ConditionalCheckFailedException"}}


class Dynamo:
    def __init__(self):
        self.row = None

    def get_item(self, **kw):
        return {} if self.row is None else {"Item": dict(self.row)}

    def update_item(self, **kw):
        values = kw["ExpressionAttributeValues"]
        if kw["ConditionExpression"] == "attribute_not_exists(#job)":
            if self.row is not None:
                raise Conditional()
        elif self.row is None or self.row["operation_version"] != values[":expected"]:
            raise Conditional()
        self.row = {**kw["Key"], "operation_row": values[":row"], "operation_version": values[":version"]}


def runtime(monkeypatch, known):
    """A ResidentSession whose provider lookup answers FOUND for the symbols in `known` and an empty list for any other."""
    bundle = ReplayTransport({}).bundle
    bundle["fence"] = 1

    class Secrets:
        def get_secret_value(self, **kw):
            return {"SecretString": json.dumps(bundle), "VersionId": "fixture-version"}

    def child(command, frame, deadline, **kw):
        wanted = frame["path"].split("securities=", 1)[1].replace("%2C", ",").split(",")
        rows = [{"id": s, "security_id": s, "securitylist_security_id": "S:" + s, "security_name": "fixture",
                 "detailed_security_type": "stock", "features_needed": []} for s in wanted if s in known]
        body = json.dumps(rows).encode()
        return {"body": base64.b64encode(body).decode(), "cookies": frame["bundle"]["cookies"],
                "info": {"method": "GET", "path": "/securities/securities_info", "status": 200,
                         "final_url_path": "/securities/securities_info", "body_complete": True,
                         "content_type": "application/json", "bytes": len(body), "login_destination": False}}
    monkeypatch.setattr(deadline_transport, "_run_child", child)
    return ResidentSession(secrets_client=Secrets(), dynamo_client=Dynamo(), jobs_table="irpt-jobs",
                           enrolled_user_id=bundle["identity"]["user_id"], clock=lambda: 100.25)


def fake_history(table, seen):
    def history(symbol):
        seen.append(symbol)
        value = table.get(symbol)
        if isinstance(value, Exception):
            raise value
        return value or []
    return history


def test_a_symbol_yfinance_knows_and_the_provider_omits_is_kept_with_no_replace_or_no(monkeypatch):
    seen = []
    monkeypatch.setattr(yfinance_check, "default_history", fake_history({"ZZQX": [("2026-10-01", 10.0), ("2026-10-02", 11.5)]}, seen))
    monkeypatch.setattr(yfinance_check.time, "sleep", lambda s: None)
    result = runtime(monkeypatch, {"AAPL"}).template_resolver(identity=lambda *a: None, source_revision="fixture")({}, {}, ["AAPL", "ZZQX"])
    assert result["AAPL"]["state"] == "FOUND"
    kept = result["ZZQX"]
    assert kept["state"] == "KEPT" and kept["resolution_action"] == "NONE" and kept["price_source"] == "yfinance"
    assert kept["checker"] == {"rows": 2, "last_close": 11.5}
    assert seen == ["ZZQX"]  # the found symbol is never sent to the checker


def test_a_symbol_neither_knows_stays_not_found(monkeypatch):
    monkeypatch.setattr(yfinance_check, "default_history", fake_history({}, []))
    result = runtime(monkeypatch, set()).template_resolver(identity=lambda *a: None, source_revision="fixture")({}, {}, ["NOPE"])
    assert result["NOPE"]["state"] == "NOT_FOUND"


def test_a_missing_yfinance_library_is_a_failed_check_never_a_clean_absence(monkeypatch):
    monkeypatch.setattr(yfinance_check, "default_history", fake_history({"ZZQX": yfinance_check.CheckerUnavailable("CHECKER_UNAVAILABLE")}, []))
    result = runtime(monkeypatch, set()).template_resolver(identity=lambda *a: None, source_revision="fixture")({}, {}, ["ZZQX"])
    assert result["ZZQX"]["state"] == "UNAVAILABLE" and result["ZZQX"]["reason"] == "YFINANCE_CHECK_FAILED"


def test_a_pushback_is_a_failed_check_not_an_absence(monkeypatch):
    monkeypatch.setattr(yfinance_check, "default_history", fake_history({"ZZQX": RuntimeError("HTTP Error 429: Too Many Requests")}, []))
    result = runtime(monkeypatch, set()).template_resolver(identity=lambda *a: None, source_revision="fixture")({}, {}, ["ZZQX"])
    assert result["ZZQX"]["state"] == "UNAVAILABLE" and result["ZZQX"]["check_failed"] == "PUSHBACK"


def test_an_injected_checker_wins_over_the_default(monkeypatch):
    class Mine:
        def check(self, symbols):
            return {s: {"state": "KEPT", "rows": 3, "last_close": 9.0, "reason": "HISTORY_ROWS"} for s in symbols}
    monkeypatch.setattr(yfinance_check, "default_history", lambda s: (_ for _ in ()).throw(AssertionError("default used")))
    result = runtime(monkeypatch, set()).template_resolver(identity=lambda *a: None, source_revision="fixture", checker=Mine())({}, {}, ["ZZQX"])
    assert result["ZZQX"]["state"] == "KEPT"
