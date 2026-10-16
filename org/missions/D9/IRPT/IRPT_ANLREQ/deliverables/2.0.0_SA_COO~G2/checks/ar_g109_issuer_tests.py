"""IRPT_ANLREQ AR-g-109 issuer tests (2.0.0_SA_COO~G2): the hop_failure writer, the ready-signal writer and the packager writer.

Run by ar_g109_checks.py with the environment variable AR109_ROOT = the investor-reporting folder to grade. Offline: boto3 Stubber
only, no network, no AWS call. ASCII only.
"""
import os
import re
import sys
from pathlib import Path

import boto3
import pytest
from botocore.stub import Stubber

ROOT = Path(os.environ["AR109_ROOT"])
for rel in ("ycharts/generate", "ycharts/research", "reports", "intake", "ops", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract",
            "_scope", "_ids", "lib"):
    if (ROOT / rel).is_dir():
        sys.path.insert(0, str(ROOT / rel))

import durable_job  # noqa: E402
from durable_job import DynamoGenerationStore, LeaseRefused  # noqa: E402

REQ = "REQ-" + "a" * 24
SHA = "b" * 64
AT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def make_store():
    client = boto3.client("dynamodb", region_name="us-east-1", aws_access_key_id="x", aws_secret_access_key="x")
    stub = Stubber(client)
    stub.activate()
    calls = []
    client.meta.events.register_first("before-parameter-build.dynamodb.UpdateItem", lambda params, **kw: calls.append(dict(params)))
    store = DynamoGenerationStore(client, tenant="49financial", request_id=REQ, composition_sha256=SHA, worker_id="w", now=lambda: 100)
    return store, stub, calls


def row(**extra):
    base = {"tenant": {"S": "49financial"}, "job": {"S": REQ}, "state": {"S": "READY"}, "composition_sha256": {"S": SHA}}
    base.update(extra)
    return base


def test_codes_are_closed_and_shaped():
    assert set(durable_job.HOP_FAILURE_CODES) == {"READY_SIGNAL", "COMMENTARY", "PACKAGER"}
    for hop, codes in durable_job.HOP_FAILURE_CODES.items():
        assert codes and all(re.fullmatch(r"[A-Z0-9_]+", c) for c in codes), hop
    assert durable_job.HOP_FAILURE_CODES["READY_SIGNAL"] == ("READY_SIGNAL_SEND_FAILED",)
    assert durable_job.HOP_FAILURE_CODES["COMMENTARY"] == ("COMMENTARY_DRAFT_FAILED", "COMMENTARY_DRAFT_REFUSED")
    assert durable_job.HOP_FAILURE_CODES["PACKAGER"] == ("PACKAGER_REFUSED", "PACKAGER_FAILED")


def test_first_write_is_set_once_and_touches_only_the_attribute():
    store, stub, calls = make_store()
    stub.add_response("update_item", {})
    assert store.mark_hop_failure(REQ, "PACKAGER", "PACKAGER_REFUSED", "2026-10-16T03:00:00Z") is True
    assert len(calls) == 1
    call = calls[0]
    assert call["TableName"] == "irpt-jobs" and call["Key"] == store.key
    assert call["UpdateExpression"].replace(" ", "") == "SEThop_failure=:value"
    assert "attribute_not_exists(hop_failure)" in call["ConditionExpression"]
    assert "state" not in call["UpdateExpression"].lower().replace("hop_failure", "")
    assert call["ExpressionAttributeValues"][":value"] == {"M": {"hop": {"S": "PACKAGER"}, "code": {"S": "PACKAGER_REFUSED"},
                                                                 "at": {"S": "2026-10-16T03:00:00Z"}}}
    assert set(call["ExpressionAttributeValues"]) == {":value"}


def test_second_write_is_a_noop_that_returns_false():
    store, stub, calls = make_store()
    stub.add_client_error("update_item", "ConditionalCheckFailedException")
    stub.add_response("get_item", {"Item": row(hop_failure={"M": {"hop": {"S": "PACKAGER"}, "code": {"S": "PACKAGER_FAILED"},
                                                                  "at": {"S": "2026-10-16T02:00:00Z"}}})},
                      {"TableName": "irpt-jobs", "Key": store.key, "ConsistentRead": True})
    assert store.mark_hop_failure(REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z") is False


def test_a_conditional_failure_without_a_stored_value_is_raised():
    store, stub, calls = make_store()
    stub.add_client_error("update_item", "ConditionalCheckFailedException")
    stub.add_response("get_item", {"Item": row()}, {"TableName": "irpt-jobs", "Key": store.key, "ConsistentRead": True})
    with pytest.raises(Exception):
        store.mark_hop_failure(REQ, "PACKAGER", "PACKAGER_FAILED", "2026-10-16T03:00:00Z")


@pytest.mark.parametrize("hop,code,at", [
    ("NOPE", "PACKAGER_FAILED", "2026-10-16T03:00:00Z"),
    ("PACKAGER", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z"),
    ("PACKAGER", "packager_failed", "2026-10-16T03:00:00Z"),
    ("PACKAGER", "PACKAGER_FAILED", "2026-10-16 03:00:00"),
    ("PACKAGER", "PACKAGER_FAILED", None),
    ("READY_SIGNAL", "PACKAGER_REFUSED", "2026-10-16T03:00:00Z"),
])
def test_invalid_hop_code_or_time_is_refused_before_any_call(hop, code, at):
    store, stub, calls = make_store()
    with pytest.raises(LeaseRefused) as info:
        store.mark_hop_failure(REQ, hop, code, at)
    assert str(info.value) == "HOP_FAILURE_INVALID" and calls == []


def test_a_wrong_job_id_is_refused():
    store, stub, calls = make_store()
    with pytest.raises(LeaseRefused):
        store.mark_hop_failure("REQ-" + "c" * 24, "PACKAGER", "PACKAGER_FAILED", "2026-10-16T03:00:00Z")
    assert calls == []


def test_get_state_carries_hop_failure_only_when_set():
    store, stub, calls = make_store()
    stub.add_response("get_item", {"Item": row()}, {"TableName": "irpt-jobs", "Key": store.key, "ConsistentRead": True})
    assert "hop_failure" not in store.get_state(REQ)
    stub.add_response("get_item", {"Item": row(hop_failure={"M": {"hop": {"S": "COMMENTARY"}, "code": {"S": "COMMENTARY_DRAFT_REFUSED"},
                                                                  "at": {"S": "2026-10-16T02:00:00Z"}}})},
                      {"TableName": "irpt-jobs", "Key": store.key, "ConsistentRead": True})
    state = store.get_state(REQ)
    assert state["state"] == "READY"
    assert state["hop_failure"] == {"hop": "COMMENTARY", "code": "COMMENTARY_DRAFT_REFUSED", "at": "2026-10-16T02:00:00Z"}


class FakeStore:
    tenant = "49financial"

    def __init__(self, fail_mark=False):
        self.marks, self.sent, self.fail_mark = [], [], fail_mark

    def mark_hop_failure(self, request_id, hop, code, at):
        if self.fail_mark:
            raise RuntimeError("dynamo down")
        self.marks.append((request_id, hop, code, at))
        return True

    def mark_i3_sent(self, request_id, at):
        self.sent.append(request_id)


def _worker():
    import resident_worker
    return resident_worker


def test_a_failed_ready_send_records_the_hop_once_and_does_not_raise(monkeypatch, capsys):
    rw = _worker()
    monkeypatch.setenv("IRPT_ANALYSIS_READY_QUEUE_URL", "https://sqs.invalid/q")
    store = FakeStore()

    def boom(url, body):
        raise RuntimeError("sqs down")
    assert rw.send_ready(store, boom, REQ) is None
    assert len(store.marks) == 1 and store.sent == []
    request_id, hop, code, at = store.marks[0]
    assert (request_id, hop, code) == (REQ, "READY_SIGNAL", "READY_SIGNAL_SEND_FAILED") and AT.fullmatch(at)
    assert "ANALYSIS_READY_SEND_FAILED" in capsys.readouterr().out


def test_a_failing_hop_write_is_swallowed_and_named(monkeypatch, capsys):
    rw = _worker()
    monkeypatch.setenv("IRPT_ANALYSIS_READY_QUEUE_URL", "https://sqs.invalid/q")
    store = FakeStore(fail_mark=True)

    def boom(url, body):
        raise RuntimeError("sqs down")
    assert rw.send_ready(store, boom, REQ) is None
    out = capsys.readouterr().out
    assert "HOP_FAILURE_MARK_FAILED READY_SIGNAL " + REQ in out and "dynamo down" not in out


def test_a_good_send_records_no_hop_failure(monkeypatch):
    rw = _worker()
    monkeypatch.setenv("IRPT_ANALYSIS_READY_QUEUE_URL", "https://sqs.invalid/q")
    store = FakeStore()
    rw.send_ready(store, lambda url, body: {"MessageId": "m"}, REQ)
    assert store.marks == [] and store.sent == [REQ]


def test_an_unset_queue_records_nothing(monkeypatch):
    rw = _worker()
    monkeypatch.delenv("IRPT_ANALYSIS_READY_QUEUE_URL", raising=False)
    store = FakeStore()
    rw.send_ready(store, None, REQ)
    assert store.marks == [] and store.sent == []


# --- the packager closure -------------------------------------------------------------------------------------------------------------

def _packager_world(monkeypatch, handler):
    import resident_installed as ri
    import opal_packager
    client = boto3.client("dynamodb", region_name="us-east-1", aws_access_key_id="x", aws_secret_access_key="x")
    stub = Stubber(client)
    stub.activate()
    calls = []
    client.meta.events.register_first("before-parameter-build.dynamodb.UpdateItem", lambda params, **kw: calls.append(dict(params)))

    class Acceptance:
        def get(self, tenant, request_id):
            return {"composition_ref": {"sha256": SHA}, "identity": {"tenant_firm_id": tenant, "request_id": request_id}}
    monkeypatch.setattr(opal_packager, "handle_commentary_ready", handler)
    monkeypatch.setattr(opal_packager, "live_read_job", lambda *a, **k: None)
    monkeypatch.setattr(opal_packager, "live_read_artifact", lambda *a, **k: None)
    monkeypatch.setattr(opal_packager, "live_retained_package", lambda *a, **k: None)
    packager = ri.make_packager(clients={"dynamodb": client}, acceptance=Acceptance(), artifacts=object(), opal_stores=lambda p, r: {},
                                principal_for=lambda r: {}, jobs_table="irpt-jobs", clock=lambda: 1_792_000_000)
    import keys
    body = keys.queue_message("commentary_ready", {"tenant": "49financial", "request_id": REQ})
    return packager, stub, calls, body, opal_packager


def test_a_packager_refusal_records_packager_refused_and_reraises(monkeypatch):
    import opal_packager

    def refuse(body, ports):
        raise opal_packager.PackagerRefused("COMMENTARY_REF_ABSENT")
    packager, stub, calls, body, _ = _packager_world(monkeypatch, refuse)
    stub.add_response("update_item", {})
    with pytest.raises(opal_packager.PackagerRefused):
        packager(body)
    assert len(calls) == 1
    value = calls[0]["ExpressionAttributeValues"][":value"]["M"]
    assert value["hop"] == {"S": "PACKAGER"} and value["code"] == {"S": "PACKAGER_REFUSED"} and AT.fullmatch(value["at"]["S"])


def test_any_other_packager_error_records_packager_failed_and_reraises(monkeypatch):
    def boom(body, ports):
        raise RuntimeError("attach down")
    packager, stub, calls, body, _ = _packager_world(monkeypatch, boom)
    stub.add_response("update_item", {})
    with pytest.raises(RuntimeError):
        packager(body)
    assert calls[0]["ExpressionAttributeValues"][":value"]["M"]["code"] == {"S": "PACKAGER_FAILED"}


def test_a_good_package_writes_nothing(monkeypatch):
    packager, stub, calls, body, _ = _packager_world(monkeypatch, lambda body, ports: {"outcome": "ATTACHED"})
    assert packager(body) == {"outcome": "ATTACHED"} and calls == []


def test_a_failing_hop_write_never_masks_the_packager_error(monkeypatch, capsys):
    def boom(body, ports):
        raise RuntimeError("attach down")
    packager, stub, calls, body, _ = _packager_world(monkeypatch, boom)
    stub.add_client_error("update_item", "ProvisionedThroughputExceededException")
    with pytest.raises(RuntimeError) as info:
        packager(body)
    assert str(info.value) == "attach down"
    assert "HOP_FAILURE_MARK_FAILED PACKAGER " + REQ in capsys.readouterr().out


def test_an_unreadable_message_records_nothing_and_still_reraises(monkeypatch, capsys):
    import opal_packager

    def refuse(body, ports):
        raise opal_packager.PackagerRefused("MESSAGE_NOT_JSON")
    packager, stub, calls, body, _ = _packager_world(monkeypatch, refuse)
    with pytest.raises(opal_packager.PackagerRefused):
        packager("not json")
    assert calls == [] and "HOP_FAILURE_MARK_FAILED PACKAGER" in capsys.readouterr().out


# --- the keyed form (no composition hash, UpdateItem only) --------------------------------------------------------------------------------

def keyed_client():
    client = boto3.client("dynamodb", region_name="us-east-1", aws_access_key_id="x", aws_secret_access_key="x")
    stub = Stubber(client)
    stub.activate()
    calls = []
    client.meta.events.register_first("before-parameter-build.dynamodb.UpdateItem", lambda params, **kw: calls.append(dict(params)))
    return client, stub, calls


def test_keyed_form_writes_once_with_a_key_existence_condition_and_no_read():
    client, stub, calls = keyed_client()
    stub.add_response("update_item", {})
    assert durable_job.mark_hop_failure_keyed(client, "49financial", REQ, "COMMENTARY", "COMMENTARY_DRAFT_REFUSED", "2026-10-16T03:00:00Z") is True
    call = calls[0]
    assert call["TableName"] == "irpt-jobs" and call["Key"] == {"tenant": {"S": "49financial"}, "job": {"S": REQ}}
    assert call["UpdateExpression"].replace(" ", "") == "SEThop_failure=:value"
    cond = call["ConditionExpression"]
    assert "attribute_not_exists(hop_failure)" in cond and "attribute_exists(" in cond and "composition_sha256" not in cond
    assert set(call["ExpressionAttributeValues"]) == {":value"}
    assert call["ExpressionAttributeValues"][":value"] == {"M": {"hop": {"S": "COMMENTARY"}, "code": {"S": "COMMENTARY_DRAFT_REFUSED"},
                                                                "at": {"S": "2026-10-16T03:00:00Z"}}}
    assert "ReturnValues" not in call or call["ReturnValues"] == "NONE"


def test_keyed_form_returns_false_on_a_failed_condition_without_any_read():
    client, stub, calls = keyed_client()
    stub.add_client_error("update_item", "ConditionalCheckFailedException")
    assert durable_job.mark_hop_failure_keyed(client, "49financial", REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z") is False
    stub.assert_no_pending_responses()


def test_keyed_form_propagates_other_errors():
    client, stub, calls = keyed_client()
    stub.add_client_error("update_item", "ProvisionedThroughputExceededException")
    with pytest.raises(Exception) as info:
        durable_job.mark_hop_failure_keyed(client, "49financial", REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z")
    assert "Provisioned" in str(info.value)


@pytest.mark.parametrize("tenant,job,hop,code,at", [
    ("", REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z"),
    ("49financial", "", "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z"),
    ("49financial", REQ, "PACKAGER", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z"),
    ("49financial", REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "yesterday"),
    (None, REQ, "COMMENTARY", "COMMENTARY_DRAFT_FAILED", "2026-10-16T03:00:00Z"),
])
def test_keyed_form_refuses_bad_input_before_any_call(tenant, job, hop, code, at):
    client, stub, calls = keyed_client()
    with pytest.raises(LeaseRefused) as info:
        durable_job.mark_hop_failure_keyed(client, tenant, job, hop, code, at)
    assert str(info.value) == "HOP_FAILURE_INVALID" and calls == []
