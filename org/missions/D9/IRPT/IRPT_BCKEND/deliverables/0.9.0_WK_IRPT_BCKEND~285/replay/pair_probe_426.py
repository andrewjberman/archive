"""IB-pr-426 replay: the acceptance / submission_service PAIR through one extracted tree. Run as
    python -I pair_probe426.py <extracted_zip_dir> <label> <out_json>
A REAL DynamoAcceptance over an in-memory DynamoDB client (it records the transaction it is handed) and a REAL SubmissionService over
mocked artifacts / admission / authorization (the form of the pin's test_acceptance_actor.test_submit_passes_the_verified_principal_to_accept).
One new request is submitted, then the same request again (a replay). Records: what the service call did, the keys of the record the
acceptance wrote, the value of acting_principal_id on it (a synthetic principal id), and the exception class if the pair is split.
Offline; no AWS client; synthetic ids only. ASCII only."""
import copy
import json
import socket
import sys
from unittest.mock import Mock

zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))

import acceptance as acc  # noqa: E402
from composition_admission import CompositionAdmission  # noqa: E402
from submission import compose_frozen_request  # noqa: E402
from submission_service import SubmissionService  # noqa: E402

VERIFIED = "synthetic-verified-principal"
OWNER = {"firm_id": "49financial", "principal_id": VERIFIED, "advisor_id": VERIFIED, "ownership_fingerprint": "b" * 64}
BROWSER = {"request_id": "areq-1234", "client_id": "C-one", "account_ids": ["A-one"], "snapshot_id": "SNAP-one", "variant": "overview",
           "comparison_keys": [], "report_title": None, "prepared_for": "Synthetic recipient"}


class MemoryDynamo:
    """get_item / transact_write_items / update_item over a dict; records every write."""

    def __init__(self):
        self.items, self.writes = {}, []

    def get_item(self, TableName, Key, ConsistentRead=True):
        item = self.items.get((TableName, json.dumps(Key, sort_keys=True)))
        return {"Item": item} if item else {}

    def transact_write_items(self, TransactItems):
        for w in TransactItems:
            put = w["Put"]
            key = {k: put["Item"][k] for k in put["Item"] if k in ("tenant", "request_revision", "job")}
            self.items[(put["TableName"], json.dumps({k: key[k] for k in key if k != "record"}, sort_keys=True))] = put["Item"]
            self.writes.append((put["TableName"], sorted(put["Item"])))

    def update_item(self, **kw):
        return {}


def run_once(client):
    input_ref = {"input_id": "portfolio_" + "a" * 64, "content_sha256": "a" * 64,
                 "artifact_ref": {"artifact_id": "ART-input", "family": "NORMALIZED_PORTFOLIO", "sha256": "a" * 64,
                                  "retention_ref": {"id": "ret-one"}}}
    resolved = {"owner": OWNER, "input_ref": input_ref, "source_descriptors": {},
                "client": {"client_id": "C-one", "account_ids": ["A-one"]}, "holdings": {"snapshot_id": "SNAP-one"}}
    composition = compose_frozen_request(BROWSER, resolved, recipe_version="v1", settings={"fee": 0})
    store = acc.DynamoAcceptance(client, requests_table="irpt-requests", jobs_table="irpt-jobs", now=lambda: 100)
    artifacts = Mock()
    artifacts.head.return_value = input_ref["artifact_ref"]
    artifacts.put.return_value = {"artifact_id": "ART-one", "sha256": composition["content_sha256"], "version_id": "version-one"}
    admission = Mock(spec=CompositionAdmission)
    admission.validate.return_value = b"{}"
    principal = {"principal_id": VERIFIED, "firm_id": OWNER["firm_id"]}
    service = SubmissionService(acceptance=store, artifacts=artifacts, resolve_owner=lambda *a: (principal, OWNER),
        authorize_current=lambda *a: True, resolve_inputs=lambda *a: copy.deepcopy(resolved), settings={"fee": 0}, recipe_version="v1",
        ingestion_revision="v1", destination_revision="v1", send=Mock(), queue_url="offline", admission=admission)
    try:
        service.submit(copy.deepcopy(BROWSER), None, {}, {}, None)
        outcome = "returned"
    except BaseException as exc:  # noqa: BLE001 -- recorded
        outcome = type(exc).__name__ + ":" + str(exc)[:70].replace(VERIFIED, "<principal>")
    return outcome


client = MemoryDynamo()
first = run_once(client)
rec_items = [v for (t, _), v in client.items.items() if t == "irpt-requests"]
record = json.loads(rec_items[0]["record"]["S"]) if rec_items else None
out = {"label": label, "first_submit": first, "transactions_written": len(client.writes),
       "record_keys": sorted(record) if record else None,
       "acting_principal_id_is_the_verified_principal": (record or {}).get("acting_principal_id") == VERIFIED if record else None,
       "acting_principal_id_present": "acting_principal_id" in (record or {})}
second = run_once(client)
out["replay_submit"] = second
out["transactions_after_replay"] = len(client.writes)
json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s first=%s writes=%d keys=%s" % (label, first[:40], len(client.writes), out["record_keys"]))
