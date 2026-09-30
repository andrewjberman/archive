"""AMGT_RESAPP round 50, AMGT-yy-7 -- THE POOL UNION SITS IN THE CHOKE POINT: every crosswalk/v1 write keeps a served record, whichever
writer makes it (CTO round-49 analysis cell 5 follow-up @1b2294bbd6; AMGT_CORPUS row Z-S66).

A fake S3 (in memory; no AWS write) is seeded with the REAL latest served crosswalk PLUS a planted record `ZZPLANTED_US_Equity` (the
pinned-side append). Then each of the two crosswalk/v1 writers runs a CLOUD-side write through that fake:
  (A) add_security's own pool mint: `add_security._mint_pool(as_of, rows, reg_path, universe, universe_source, client=fake)`;
  (B) the crosswalk CLI's path: `build_crosswalk(...)` with NO served= argument, then `crosswalk.write_pool(key, payload,
      document=doc, client=fake)`.
PASS when the object each writer leaves in the fake bucket still carries the planted record (and every served record).
usage: python <this>   (from the repo root; reads the real served pool read-only, writes nothing to AWS)"""
import copy
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from botocore.exceptions import ClientError  # noqa: E402

from lib.research.identity import add_security  # noqa: E402
from lib.research.identity import crosswalk as cw  # noqa: E402

PLANT = "ZZPLANTED_US_Equity"


class FakeS3:
    def __init__(self):
        self.objects = {}

    def seed(self, key, body):
        self.objects[key] = {"Body": body, "Metadata": {"document-sha256": hashlib.sha256(body).hexdigest(),
                                                        "schema-version": str(cw.SCHEMA_VERSION)}, "ETag": '"seed"'}

    def head_object(self, Bucket, Key):
        if Key not in self.objects:
            raise ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "HeadObject")
        o = self.objects[Key]
        return {"Metadata": dict(o["Metadata"]), "ETag": o["ETag"], "ContentLength": len(o["Body"])}

    def put_object(self, Bucket, Key, Body, Metadata=None, **kw):
        body = Body if isinstance(Body, bytes) else Body.encode("utf-8")
        self.objects[Key] = {"Body": body, "Metadata": dict(Metadata or {}), "ETag": '"%s"' % hashlib.md5(body).hexdigest()}
        return {"ETag": self.objects[Key]["ETag"]}

    def get_object(self, Bucket, Key):
        return {"Body": io.BytesIO(self.objects[Key]["Body"])}

    def get_paginator(self, name):
        store = self

        class _P:
            def paginate(self, Bucket, Prefix):
                return [{"Contents": [{"Key": k} for k in sorted(store.objects) if k.startswith(Prefix)]}]
        return _P()


def keys_of(body):
    return {r.get("security_key") for r in json.loads(body.decode("utf-8")).get("records") or []}


def seeded(served, key):
    doc = copy.deepcopy(served)
    planted = copy.deepcopy(doc["records"][0])
    planted["security_key"] = PLANT
    doc["records"].append(planted)
    fake = FakeS3()
    fake.seed(key, cw.serialise(doc))
    return fake


def main():
    served, served_key = cw._read_pool_latest()
    as_of = served["as_of"]
    key = "%s%s.json" % (cw.CROSSWALK_PREFIX, as_of)
    want = {r.get("security_key") for r in served["records"]} | {PLANT}
    universe, usrc = cw.load_identity_universe(None)
    rows, reg_path = cw.load_registrations()
    results = {}
    fake = seeded(served, key)
    try:
        add_security._mint_pool(as_of, rows, reg_path, universe, usrc, client=fake)
        got = keys_of(fake.objects[key]["Body"])
        results["A add_security._mint_pool"] = (PLANT in got, len(want - got))
    except Exception as exc:  # noqa: BLE001 -- a refusal is a result
        results["A add_security._mint_pool"] = (False, "%s: %s" % (type(exc).__name__, str(exc)[:120]))
    fake = seeded(served, key)
    try:
        rf, rr = cw._research_folders_for_disclosure()
        doc = cw.build_crosswalk(as_of, identity_universe=universe, identity_source=usrc, research_folders=rf, research_root=rr)
        cw.write_pool(key, cw.serialise(doc), document=doc, client=fake)
        got = keys_of(fake.objects[key]["Body"])
        results["B crosswalk build + write_pool"] = (PLANT in got, len(want - got))
    except Exception as exc:  # noqa: BLE001
        results["B crosswalk build + write_pool"] = (False, "%s: %s" % (type(exc).__name__, str(exc)[:120]))
    print("served %s: %d records + planted %s (the pinned-side append)" % (served_key, len(served["records"]), PLANT))
    for name, (kept, lost) in results.items():
        print("  %-32s planted kept: %s; served+planted records dropped: %s" % (name, kept, lost))
    ok = all(kept and lost == 0 for kept, lost in results.values())
    print("EVERY CROSSWALK WRITER KEEPS A SERVED RECORD: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
