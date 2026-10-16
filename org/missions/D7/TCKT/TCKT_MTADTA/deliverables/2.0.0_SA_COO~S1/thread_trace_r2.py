"""TCKT_MTADTA round 2 -- the FWD-1 thread trace over the repaired code, run by the issuer at the drain (SYNTHETIC events,
in-memory clients, no network, no AWS, no Microsoft).

Hops: collector (filter + levers) -> door `put` on the COLLECTOR alias -> door `derive_silver` (called by the collector) ->
door `get_day` and `list_state`/`get_state` on the MEMBER alias -> read_day.render and first_content.report.
Negative arms: the planted-value search over every stored object; the collector alias refused a read; the member alias refused
a put; an unqualified invoke refused everything.

Run from the repository root:  python org/missions/D7/TCKT/TCKT_MTADTA/deliverables/2.0.0_SA_COO~S1/thread_trace_r2.py
"""
import gzip
import io
import json
import os
import sys
import types

ROOT = os.getcwd()
COLL = os.path.join(ROOT, "data", "m365_metadata", "scripts", "collector")
DOOR = os.path.join(ROOT, "infra", "aws", "lambda", "globgrph-trino-access")
SILV = os.path.join(ROOT, "data", "m365_metadata", "scripts", "silver")
sys.path[:0] = [COLL, DOOR, SILV]

import collect  # noqa: E402
import first_content  # noqa: E402
import handler  # noqa: E402
import read_day  # noqa: E402
import silver_builder  # noqa: E402
from access_client import AccessClient  # noqa: E402

os.environ["BUCKET"] = "opal-data-trino"
FN = "arn:aws:lambda:us-east-1:123456789012:function:globgrph-trino-access-lambda"
OUTSIDER = "outsider.person@opalinvest.com"
INTERNAL = "zed.other@opalinvest.com"
EXTERNAL_DOMAIN = "evil-example.org"
SUBJECT = "Wire instructions for ACME Fund Q3"
RAW_IP = "203.0.113.77"
GUID = "0f1e2d3c-4b5a-6978-8796-a5b4c3d2e1f0"


class FakeS3:
    def __init__(self):
        self.objs = {}

    def put_object(self, Bucket, Key, Body, **kw):
        assert kw.get("ServerSideEncryption") == "aws:kms", "a put without SSE-KMS"
        self.objs[Key] = Body if isinstance(Body, bytes) else Body.encode()
        return {}

    def get_object(self, Bucket, Key, **kw):
        return {"Body": io.BytesIO(self.objs[Key])}

    def list_objects_v2(self, Bucket, Prefix="", **kw):
        return {"Contents": [{"Key": k} for k in sorted(self.objs) if k.startswith(Prefix)], "IsTruncated": False}


class Source:
    def __init__(self, blobs):
        self.blobs = blobs

    def list_content(self, ct, start, end):
        return [{"id": i, "created": c} for (i, c, _e) in self.blobs.get(ct, [])]

    def fetch(self, ct, blob_id):
        return [e for (i, _c, e) in self.blobs[ct] if i == blob_id][0]


def ev(i, who, t, op="FileAccessed", wl="SharePoint", **kw):
    d = {"Id": i, "CreationTime": t, "Operation": op, "Workload": wl, "RecordType": 6, "ResultStatus": "Succeeded",
         "UserId": who, "ClientIP": RAW_IP, "SiteUrl": "https://synthetic.example/sites/ops",
         "SourceFileName": "recon-synthetic.xlsx", "SourceRelativeUrl": "Shared Documents/Ops",
         "ExtendedProperties": [{"Name": "x", "Value": "NOPE-EXT"}]}
    d.update(kw)
    return [d]


def main():
    s3 = FakeS3()
    logs = []

    def door(alias):
        arn = FN if alias is None else FN + ":" + alias
        ctx = types.SimpleNamespace(invoked_function_arn=arn)
        return lambda payload: handler.handle(payload, ctx, s3=s3, log=logs.append, silver_builder=silver_builder)

    access = AccessClient(door("collector"))
    member = door("member")
    cfg = json.load(open(os.path.join(ROOT, "data", "m365_metadata", "scripts", "population.json"), encoding="utf-8"))
    cfg["subject_key"] = "synthetic-trace-key"
    blobs = {
        "Audit.SharePoint": [
            ("s1", "2026-10-15T13:00:30.000Z", ev("e1", "yang@opalinvest.com", "2026-10-15T13:00:00")),
            ("s2", "2026-10-16T02:30:30.000Z", ev("e3", "yang@opalinvest.com", "2026-10-16T02:30:00")),
            ("s3", "2026-10-15T15:30:30.000Z", ev("x1", OUTSIDER, "2026-10-15T15:30:00", SourceFileName="outsider-planted.xlsx")),
            ("s4", "2026-10-15T15:45:30.000Z", ev("g1", GUID, "2026-10-15T15:45:00")),
        ],
        "Audit.Exchange": [
            ("x1", "2026-10-15T14:05:30.000Z", ev("e2", "yang@opalinvest.com", "2026-10-15T14:05:09", op="Send", wl="Exchange",
                                                   Subject=SUBJECT, Recipients=[INTERNAL, "bob@" + EXTERNAL_DOMAIN, "alyssa@opalinvest.com"])),
        ],
    }
    out = collect.run_once(Source(blobs), access, cfg, now="2026-10-16T12:00:00Z")
    results = {"collector": {"fetched": out["fetched"], "bronze_objects": out["bronze_objects"], "failed": out["failed"]}}
    rows = read_day.fetch(member, "yang@opalinvest.com", "2026-10-15")
    results["read_day_lines"] = read_day.render(rows).splitlines()
    results["first_content_report"] = first_content.report(member, "2026-10-15").splitlines()
    bad = []
    if [r.get("event_id") for r in rows] != ["e1", "e2", "e3"]:
        bad.append("yang's Eastern day should hold e1, e2, e3 in order: %r" % [r.get("event_id") for r in rows])
    if "id-only actors dropped: 1" not in results["first_content_report"]:
        bad.append("the id-only count should read 1")
    needles = [OUTSIDER, INTERNAL, EXTERNAL_DOMAIN, SUBJECT, RAW_IP, "outsider-planted", "NOPE-EXT", "Wire instructions", GUID]
    hits = []
    for k, b in s3.objs.items():
        blob = gzip.decompress(b) if k.endswith(".gz") else b
        for n in needles:
            if n.encode() in blob:
                hits.append((k.rsplit("/", 1)[-1], n))
    results["stored_objects"] = len(s3.objs)
    results["negative_arm_hits"] = hits
    cov = sorted(k.rsplit("/", 1)[-1] for k in s3.objs if "collection_coverage" in k and "date=2026-10-15" in k)
    results["coverage_objects_for_2026-10-15"] = cov
    if hits:
        bad.append("planted values found in storage: %r" % hits)
    if cov != ["coverage_20261016T120000Z.json"]:
        bad.append("coverage object for the day: %r" % cov)
    refusals = {
        "collector_get_day": door("collector")({"op": "get_day", "person": "yang@opalinvest.com", "date": "2026-10-15"}).get("ok"),
        "collector_get_coverage": door("collector")({"op": "get_state", "key": cov and [k for k in s3.objs if "collection_coverage" in k][0]}).get("ok"),
        "member_put": member({"op": "put", "dataset": "state", "key": collect.CURSOR_KEY, "body_b64": "e30="}).get("ok"),
        "unqualified_get_day": door(None)({"op": "get_day", "person": "yang@opalinvest.com", "date": "2026-10-15"}).get("ok"),
        "member_non_member_day": member({"op": "get_day", "person": OUTSIDER, "date": "2026-10-15"}).get("ok"),
        "collector_cursor_read": door("collector")({"op": "get_state", "key": collect.CURSOR_KEY}).get("ok"),
    }
    results["door_answers_ok"] = refusals
    if any(v for k, v in refusals.items() if k != "collector_cursor_read") or refusals["collector_cursor_read"] is not True:
        bad.append("a refusal was served or the cursor read was refused: %r" % refusals)
    results["calls_logged"] = len(logs)
    results["verdict"] = "THREAD-TRACE-OK" if not bad else "THREAD-TRACE-FAIL " + "; ".join(bad)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
