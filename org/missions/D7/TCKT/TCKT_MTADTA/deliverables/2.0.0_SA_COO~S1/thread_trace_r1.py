"""TCKT_MTADTA round 1 -- the FWD-1 thread trace, run by the issuer at the drain (decomposition: release act 4's code path,
driven end to end with SYNTHETIC events and in-memory clients; no network, no AWS, no Microsoft).

Hops: collector (filter + levers) -> access door `put` -> door `derive_silver` -> door `get_day` -> read_day.render.
Negative arm: events of someone outside the eight, an internal recipient outside the eight, an external recipient, a
subject and an IP are planted; after the run EVERY stored byte (bronze gz, silver parquet, state, coverage) is searched.

Run from the repository root:  python org/missions/D7/TCKT/TCKT_MTADTA/deliverables/2.0.0_SA_COO~S1/thread_trace_r1.py
"""
import gzip
import io
import json
import os
import sys

ROOT = os.getcwd()
COLL = os.path.join(ROOT, "data", "m365_metadata", "scripts", "collector")
DOOR = os.path.join(ROOT, "infra", "aws", "lambda", "globgrph-trino-access")
SILV = os.path.join(ROOT, "data", "m365_metadata", "scripts", "silver")
sys.path[:0] = [COLL, DOOR, SILV]

import collect  # noqa: E402
import handler  # noqa: E402
import read_day  # noqa: E402
import silver_builder  # noqa: E402

BUCKET = "opal-data-trino"
os.environ["BUCKET"] = BUCKET

OUTSIDER = "outsider.person@opalinvest.com"
INTERNAL = "zed.other@opalinvest.com"
EXTERNAL_DOMAIN = "evil-example.org"
SUBJECT = "Wire instructions for ACME Fund Q3"
RAW_IP = "203.0.113.77"
SECRET_FILE = "synthetic-planted.xlsx"


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
    def __init__(self, evs):
        self.evs = evs

    def list_content(self, ct, start, end):
        return ["%s-0" % ct] if ct == "Audit.SharePoint" or ct == "Audit.Exchange" else []

    def fetch(self, ct, blob):
        w = "SharePoint" if ct == "Audit.SharePoint" else "Exchange"
        return [e for e in self.evs if e["Workload"] == w]


def ev(i, who, t, op="FileAccessed", wl="SharePoint", **kw):
    d = {"Id": i, "CreationTime": t, "Operation": op, "Workload": wl, "RecordType": 6, "ResultStatus": "Succeeded",
         "UserId": who, "ClientIP": RAW_IP, "SiteUrl": "https://synthetic.example/sites/ops",
         "SourceFileName": "recon-synthetic.xlsx", "SourceRelativeUrl": "Shared Documents/Ops",
         "ObjectId": "https://synthetic.example/recon-synthetic.xlsx", "ExtendedProperties": [{"Name": "x", "Value": "NOPE-EXT"}]}
    d.update(kw)
    return d


def main():
    s3 = FakeS3()
    logs = []

    def invoke(payload):
        return handler.handle(payload, None, s3=s3, log=logs.append, silver_builder=silver_builder)

    from access_client import AccessClient
    access = AccessClient(invoke)
    cfg = json.load(open(os.path.join(ROOT, "data", "m365_metadata", "scripts", "population.json"), encoding="utf-8"))
    cfg["subject_key"] = "synthetic-trace-key"
    evs = [
        ev("e1", "yang@opalinvest.com", "2026-10-15T13:00:00"),
        ev("e2", "yang@opalinvest.com", "2026-10-15T14:05:09", op="Send", wl="Exchange", Subject=SUBJECT,
           Recipients=[INTERNAL, "bob@" + EXTERNAL_DOMAIN, "alyssa@opalinvest.com"]),
        ev("e3", "yang@opalinvest.com", "2026-10-16T02:30:00"),
        ev("e4", "bobby@opalinvest.com", "2026-10-15T15:00:00"),
        ev("x1", OUTSIDER, "2026-10-15T15:30:00", SourceFileName=SECRET_FILE),
    ]
    out = collect.run_once(Source(evs), access, cfg, now="2026-10-16T12:00:00Z")
    results = {"collector": {"fetched": out["fetched"], "bronze_objects": out["bronze_objects"]}}
    r = invoke({"op": "derive_silver", "date": "2026-10-15"})
    results["derive_silver"] = r
    rows = read_day.fetch(invoke, "yang@opalinvest.com", "2026-10-15")
    text = read_day.render(rows)
    results["read_day_lines"] = text.splitlines()
    bad = []
    if len(rows) != 3:
        bad.append("yang's 2026-10-15 Eastern day should hold e1, e2, e3; got %d" % len(rows))
    order = [x.get("event_id") for x in rows]
    if order != ["e1", "e2", "e3"]:
        bad.append("order %r" % order)
    # Negative arm: search every stored byte, decompressing gz and reading parquet as text-bearing bytes.
    needles = [OUTSIDER, INTERNAL, EXTERNAL_DOMAIN, SUBJECT, RAW_IP, SECRET_FILE, "NOPE-EXT", "Wire instructions"]
    hits = []
    for k, b in s3.objs.items():
        blob = gzip.decompress(b) if k.endswith(".gz") else b
        for n in needles:
            if n.encode() in blob:
                hits.append((k.rsplit("/", 1)[-1], n))
    results["stored_objects"] = sorted(k.replace("m365-metadata/trino/", "") for k in s3.objs)
    results["negative_arm_hits"] = hits
    if hits:
        bad.append("planted values found in storage: %r" % hits)
    # The door refuses a non-member and never returns bronze.
    nm = invoke({"op": "get_day", "person": OUTSIDER, "date": "2026-10-15"})
    gb = invoke({"op": "get", "dataset": "bronze", "key": [k for k in s3.objs if "/bronze/" in k][0]})
    results["door_refusals"] = {"non_member": nm.get("ok"), "get_bronze": gb.get("ok")}
    if nm.get("ok") or gb.get("ok"):
        bad.append("the door answered a non-member or returned bronze")
    results["calls_logged"] = len(logs)
    results["verdict"] = "THREAD-TRACE-OK" if not bad else "THREAD-TRACE-FAIL " + "; ".join(bad)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
