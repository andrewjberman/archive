"""Issuer scenarios for IB-cw-2 (2.0.0_SA_COO~P2, 2026-10-19): a failed command carried on a COMPLETED record, and the 09:30/09:40 same-date retry slots. NOT a repo test: copy it next to tests/test_refresh_failed_command_redispatch.py (it imports that module) and run it against the NEW refresh.py before the Lambda release. Both passed on the merged code."""
from test_refresh_failed_command_redispatch import FakeS3, FakeSSM, _fire, _artifact_key, _sends_on, refresh


def _seed_completed_carrying_a_failed_command():
    s3, ssm = FakeS3(), FakeSSM()
    s3.seed_manifest("2026-10-13", "REFRESH_COMPLETED",
                     {"directory_key": _artifact_key("2026-10-13"), "ssm_command_id": "cmd-1", "dispatched_for": "2026-10-13"},
                     revision="rev-1013")
    s3.land("2026-10-13", "rev-1013")
    ssm.sent.append("cmd-1")
    ssm.status["cmd-1"] = "Failed"
    return s3, ssm


def test_completed_carried_failed_command_is_reported_then_redispatched_once(monkeypatch):
    s3, ssm = _seed_completed_carrying_a_failed_command()
    before = len(ssm.sent)
    _fire(monkeypatch, s3, ssm, "2026-10-14")
    m = s3.objects[refresh.manifest_key("2026-10-14")]
    assert m["reason_code"] == "REFRESH_FAILED", m["reason_code"]
    assert m["delta"].get("failed_command_id") == "cmd-1", m["delta"]
    assert _sends_on(ssm, before) == [], ssm.sent
    before = len(ssm.sent)
    _fire(monkeypatch, s3, ssm, "2026-10-15")
    assert _sends_on(ssm, before) == ["cmd-2"], ssm.sent
    m2 = s3.objects[refresh.manifest_key("2026-10-15")]
    assert m2["reason_code"] == "REFRESH_DISPATCHED" and m2["delta"]["ssm_command_id"] == "cmd-2", m2


def test_same_date_retry_fire_redispatches_after_the_observing_fire(monkeypatch):
    """The 09:30 fire observes and reports; the 09:40 retry of the SAME date re-dispatches once (the real cottonwood case)."""
    s3, ssm = FakeS3(), FakeSSM()
    s3.seed_manifest("2026-10-13", "REFRESH_COMPLETED", {"directory_key": _artifact_key("2026-10-13")}, revision="rev-1013")
    s3.land("2026-10-13", "rev-1013")
    _fire(monkeypatch, s3, ssm, "2026-10-14")          # dispatches cmd-1
    ssm.end("cmd-1", "Failed")
    before = len(ssm.sent)
    _fire(monkeypatch, s3, ssm, "2026-10-15")          # fire 1 of the date: observes, reports
    assert _sends_on(ssm, before) == []
    _fire(monkeypatch, s3, ssm, "2026-10-15")          # fire 2 of the SAME date (the retry slot): re-dispatches once
    assert _sends_on(ssm, before) == ["cmd-2"], ssm.sent
    _fire(monkeypatch, s3, ssm, "2026-10-15")          # a third same-date fire: cmd-2 is in flight, no second send
    assert _sends_on(ssm, before) == ["cmd-2"], ssm.sent
