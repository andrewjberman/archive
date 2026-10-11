"""AMGT_RESAPP round-92 PREP -- option C: the candidate universe's pool home follows the scanner's asOf and a rebuild writes a NEW dated key.

  PYTHONPATH=<repo root> python r92_universe_home.py            (no network, no AWS: a fake S3 client stands in for boto3)

Round 91's pp-3 stopped on this: `universe.refresh_candidate_universe` writes ONE fixed address, `.../candidate_universe/date=2026-08-06/
candidate_universe.json` (`CURRENT_VINTAGE`, a constant), which exists, so a refresh at scanner vintage 2026-10-02 would OVERWRITE it and
put 2026-10-02 content under a 2026-08-06 key. The act ran under option B (a local cache, no pool put) and left the pool object stale.

    H1 a refresh of a document whose own `vintage` is 2026-10-02 lands at `.../date=2026-10-02/candidate_universe.json`, a NEW key.
    H2 the existing `date=2026-08-06` object is byte-equal afterwards (nothing overwritten).
    H3 the same refresh again is idempotent (no error, no second put); a DIFFERENT document at the SAME vintage is REFUSED, nothing
       written (a same-key put with other bytes is a STOP).
    H4 the loader reads the LATEST dated key: with `date=2026-08-06` and `date=2026-10-02` both present it returns the 2026-10-02 document.
    H5 control: with only `date=2026-08-06` present the loader returns that document, unchanged.
Verdict: R92 UNIVERSE HOME: YES|NO (exit 0|1). At the base (2026-10-11) H1, H2 and H4 FAIL, H5 PASSes.
"""
import copy
import io
import json
import os
import shutil
import sys
import tempfile

import boto3
from botocore.exceptions import ClientError

from lib.research.peers import universe

BUCKET = "opal-data-harvest"
PREFIX = "amgt/harvest/gold/candidate_universe/"
NAME = "candidate_universe.json"


class FakeS3:
    def __init__(self):
        self.objects = {}
        self.puts = []

    @staticmethod
    def _missing(op):
        return ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, op)

    def head_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            raise self._missing("HeadObject")
        body, meta = self.objects[(Bucket, Key)]
        return {"ETag": '"e%d"' % len(body), "Metadata": dict(meta), "ContentLength": len(body)}

    def put_object(self, Bucket, Key, Body, ContentType=None, Metadata=None, IfMatch=None, IfNoneMatch=None):
        if IfNoneMatch == "*" and (Bucket, Key) in self.objects:
            raise ClientError({"Error": {"Code": "PreconditionFailed", "Message": "exists"}}, "PutObject")
        self.objects[(Bucket, Key)] = (bytes(Body), dict(Metadata or {}))
        self.puts.append(Key)
        return {}

    def get_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            raise ClientError({"Error": {"Code": "NoSuchKey", "Message": "missing"}}, "GetObject")
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)][0])}

    def list_objects_v2(self, Bucket, Prefix="", **kw):
        keys = sorted(k for (b, k) in self.objects if b == Bucket and k.startswith(Prefix))
        return {"Contents": [{"Key": k, "Size": len(self.objects[(Bucket, k)][0])} for k in keys], "KeyCount": len(keys), "IsTruncated": False}


def doc(vintage, extra=None):
    d = {"vintage": vintage, "csc_member_codes": ["price", "ev", "ey"], "preset_value_codes": ["price", "ev", "ey"],
         "rows": [], "row_value_codes": [], "read_at": "2026-10-11T00:00:00Z"}
    if extra:
        d.update(extra)
    return d


def key(vintage):
    return "%sdate=%s/%s" % (PREFIX, vintage, NAME)


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    results = []
    scratch = tempfile.mkdtemp(prefix="r92_uh_")
    real_client, real_tmp, real_build = boto3.client, tempfile.gettempdir, universe.build_candidate_universe
    old = json.dumps(doc("2026-08-06"), sort_keys=True).encode("utf-8")
    fake = FakeS3()
    fake.objects[(BUCKET, key("2026-08-06"))] = (old, {"document-sha256": "x"})
    boto3.client = lambda *a, **k: fake
    os.environ.pop(universe.ENV_CACHE, None)
    universe._MEMO.clear()

    def fresh_tmp():
        d = tempfile.mkdtemp(dir=scratch)
        tempfile.gettempdir = lambda d=d: d
        universe._MEMO.clear()

    try:
        # H1, H2
        fresh_tmp()
        universe.build_candidate_universe = lambda *a, **k: copy.deepcopy(doc("2026-10-02"))
        err = None
        try:
            universe.refresh_candidate_universe()
        except Exception as exc:  # noqa: BLE001 -- recorded as the FAIL detail
            err = "%s: %s" % (type(exc).__name__, exc)
        new_key = key("2026-10-02")
        results.append(say((BUCKET, new_key) in fake.objects, "H1 the refresh lands at a NEW key dated by the document's own vintage",
                           err or "puts: %s" % fake.puts))
        results.append(say(fake.objects[(BUCKET, key("2026-08-06"))][0] == old,
                           "H2 the existing date=2026-08-06 object is byte-equal afterwards"))
        # H3
        n_puts = len(fake.puts)
        universe._MEMO.clear()
        again = None
        try:
            universe.refresh_candidate_universe()
        except Exception as exc:  # noqa: BLE001
            again = "%s: %s" % (type(exc).__name__, exc)
        results.append(say(again is None and len(fake.puts) == n_puts,
                           "H3a the same refresh again is idempotent (no error, no second put)", again or "puts %d -> %d" % (n_puts, len(fake.puts))))
        before = fake.objects.get((BUCKET, new_key))
        universe.build_candidate_universe = lambda *a, **k: copy.deepcopy(doc("2026-10-02", {"rows": [{"ticker": "X"}]}))
        fresh_tmp()
        refused = None
        try:
            universe.refresh_candidate_universe()
        except Exception as exc:  # noqa: BLE001
            refused = "%s" % type(exc).__name__
        results.append(say(refused is not None and fake.objects.get((BUCKET, new_key)) == before,
                           "H3b a different document at the same vintage is refused and nothing is written", refused or "NOT refused"))
        # H4: the loader reads the latest dated key (the store is set explicitly: both dated keys, the older one untouched)
        new_bytes = json.dumps(doc("2026-10-02"), sort_keys=True).encode("utf-8")
        fake.objects = {(BUCKET, key("2026-08-06")): (old, {"document-sha256": "x"}),
                        (BUCKET, key("2026-10-02")): (new_bytes, {"document-sha256": "y"})}
        fresh_tmp()
        got = None
        try:
            got = universe.load_candidate_universe()
        except Exception as exc:  # noqa: BLE001
            got = {"error": "%s: %s" % (type(exc).__name__, exc)}
        results.append(say(isinstance(got, dict) and got.get("vintage") == "2026-10-02",
                           "H4 the loader returns the LATEST dated key's document", "vintage %s" % (got or {}).get("vintage", got)))
        # H5: control, only the old key
        fake.objects = {(BUCKET, key("2026-08-06")): (old, {"document-sha256": "x"})}
        fresh_tmp()
        got = None
        try:
            got = universe.load_candidate_universe()
        except Exception as exc:  # noqa: BLE001
            got = {"error": "%s: %s" % (type(exc).__name__, exc)}
        results.append(say(isinstance(got, dict) and got.get("vintage") == "2026-08-06",
                           "H5 control: with only date=2026-08-06 present the loader returns it", "vintage %s" % (got or {}).get("vintage", got)))
    finally:
        boto3.client, tempfile.gettempdir, universe.build_candidate_universe = real_client, real_tmp, real_build
        shutil.rmtree(scratch, ignore_errors=True)

    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R92 UNIVERSE HOME: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
