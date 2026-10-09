"""IB-pr-391 replay: the deployed composition of the surface, end to end through the PACKAGED modules (replay_preload.py).

The composition the Lambda runs is compose_ports(): the packaged registry's irpt-x10-v1 policy (ACTIVE) and the packaged
reporting_destination, over the retained ArtifactRepository, plus the real DynamoAcceptance over a dynamodb client. Here every
client is an offline fake. Synthetic bytes, zero network. ASCII only.
"""
import json

import pytest

import commentary_composition as cc
import composition
import opal_naming
import test_retention
from test_repository import S3, Table as ReportTable
from test_svc_commentary import COMPOSITION, COMPOSITION_BYTES, REQUEST_ID  # noqa: F401
from test_svc_commentary import retention_world, world  # noqa: F401  (fixtures)

TENANT = "49financial"


class FakeDynamo:
    """dynamodb client get_item for the acceptance read (analysis#<id>#1 in the tenant partition)."""

    def __init__(self, records):
        self.records = records
        self.calls = []

    def get_item(self, TableName, Key, ConsistentRead):
        assert ConsistentRead is True
        self.calls.append((TableName, Key["tenant"]["S"], Key["request_revision"]["S"]))
        rec = self.records.get((Key["tenant"]["S"], Key["request_revision"]["S"]))
        return {"Item": {"record": {"S": json.dumps(rec)}}} if rec else {}


@pytest.fixture
def deployed(world):  # noqa: F811  (the imported fixture is the argument)
    """The same composition as the Lambda: packaged policy + packaged destination. A permissive writer puts one composition."""
    table = test_retention.Table()
    table.queries = []
    table.roundtrip = ReportTable.roundtrip
    table.query = ReportTable.query.__get__(table)
    s3 = S3()
    w = world
    writer = composition.build_retained_repositories(
        table, s3, w.policy.authorize, lambda kind, value: None,
        reporting_policy=opal_naming.reporting_policy, reporting_destination=opal_naming.reporting_destination,
        clock=lambda: w.state.now)
    ref = writer.artifacts.put(w.principal, w.owner, "REQUEST_COMPOSITION", REQUEST_ID + "-sha", COMPOSITION_BYTES,
                               "application/json")
    record = {"identity": {"tenant_firm_id": TENANT, "request_id": REQUEST_ID, "revision": 1, "immutable": True},
              "owner": w.owner, "composition_ref": ref, "accepted_at": 1}
    dynamo = FakeDynamo({(TENANT, "analysis#" + REQUEST_ID + "#1"): record})
    ports = cc.compose_ports(clients={"dynamodb": dynamo, "table": table, "s3": s3}, clock=lambda: w.state.now,
                             environ={})
    return type("D", (), dict(ports=ports, ref=ref, s3=s3, dynamo=dynamo, world=w))


def test_deployed_composition_own_tenant_read_is_ok_sha_equal_owner_stripped(deployed):
    ans = cc.handle(deployed.ports["requests"], deployed.ports["artifacts"], {"tenant": TENANT, "request_ref": REQUEST_ID})
    assert ans["status"] == "OK"
    assert ans["sha256"] == deployed.ref["sha256"]
    text = json.dumps(ans)
    assert "owner" not in text and "advisor" not in text and "acc-a" not in text
    assert ans["redacted_count"] == 2
    assert ans["composition"]["resolved"]["profile"] == COMPOSITION["resolved"]["profile"]
    assert deployed.dynamo.calls == [("irpt-requests", TENANT, "analysis#" + REQUEST_ID + "#1")]


def test_deployed_composition_another_tenant_is_refused(deployed):
    for tenant in ("cottonwood", "inflection", "global", "opal-capital"):
        ans = cc.handle(deployed.ports["requests"], deployed.ports["artifacts"], {"tenant": tenant, "request_ref": REQUEST_ID})
        assert ans["status"] == "REFUSED", (tenant, ans)
        assert "composition" not in ans and "sha256" not in ans


def test_deployed_composition_tampered_blob_is_refused(deployed):
    (key, (body, version)), = [(k, v) for k, v in deployed.s3.objects.items()]
    deployed.s3.objects[key] = (body.replace(b"Quarterly", b"Tampered"), version)
    ans = cc.handle(deployed.ports["requests"], deployed.ports["artifacts"], {"tenant": TENANT, "request_ref": REQUEST_ID})
    assert ans["status"] == "REFUSED" and "composition" not in ans, ans


def test_handler_entry_is_named_in_the_packaged_module():
    assert callable(cc.lambda_handler)
    assert opal_naming.reporting_policy("irpt-x10-v1")["state"] == "ACTIVE"
