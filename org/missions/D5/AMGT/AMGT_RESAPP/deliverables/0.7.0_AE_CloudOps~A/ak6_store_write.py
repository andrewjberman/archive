"""AMGT-ak-6 act (A) -- the stored-field rewrite of the three FROZEN plans.

Per key: GET, assert every planned entry's `before`, set `after`, PUT the WHOLE object back at
the SAME key in the versioned bucket. All entries for one key are applied in ONE put.

TWO PHASES ON PURPOSE. The order and both halves say a differing `before` is "a STOP for the
whole act, with nothing more written". Asserting as you go satisfies "nothing MORE", but leaves
whatever was already written in place -- a partial write that, as the COO half itself warns, can
still pass AC1-AC3 because those grade only BA and VLO. So this asserts ALL 1,188 entries over
ALL 251 keys FIRST, and only then writes. A mismatch anywhere means ZERO objects were touched.

Phase 1 also checks each key's live VersionId against the base appendix. The appendix VersionId
is the documented rollback; if an object has moved since signing, rolling back would revert
somebody else's write too, so drift is a STOP rather than a warning.

The field path helpers are IMPORTED from the issuer's own ak6_verify.py, not reimplemented --
one path implementation means the writer and the grader cannot disagree about what a
`store_field` addresses.

  --out <json>   write the receipt (key, prior VersionId, new VersionId, fields set)
  --dry-run      phase 1 only: assert and report, write nothing
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
from collections import defaultdict

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
VERIFY = ROOT + "/2.0.0_SA_COO~Z/round61/checks/ak6_verify.py"
BASE = ROOT + "/2.0.0_SA_COO~Z/round61/AK6_BASE_VERSIONS.json"
BUCKET = "opal-data-harvest"
REGION = "us-east-1"

PLANS = [
    ("B2", "C:/tmp/ak6_b2_plan.json",
     "d373d0615deef8019619079d6df9b803b4aac82e75890c25e8469c53ce4629c4"),
    ("B3", ROOT + "/0.9.0_WK_AMGT_RESAPP~202/m1_officer_plan.json",
     "11518fd5924c880614adfeff0acf92d7464bc1f546d21e4075f0874d21188424"),
    ("B4", ROOT + "/0.9.0_WK_AMGT_RESAPP~203/posture_claim_plan.json",
     "0e77bc0c349b5675555af120ce2d26c8ebf0f27c2aba672322975e1c0193d684"),
]


def _load_verify():
    spec = importlib.util.spec_from_file_location("ak6_verify", VERIFY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    v = _load_verify()
    get, set_ = v._get, v._set

    # ---- condition 1, re-hashed here so the writer never trusts a prior check -------------
    print("CONDITION 1 -- plan sha256 at write time")
    by_key = defaultdict(list)
    for cell, path, exp in PLANS:
        raw = open(path, "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        if got != exp:
            print("  %s STOP  %s != %s" % (cell, got, exp))
            return 2
        print("  %s MATCH %s" % (cell, got))
        for e in json.loads(raw.decode("utf-8")).get("entries") or []:
            by_key[e["store_key"]].append(e)

    base = {r["store_key"]: r for r in json.load(io.open(BASE, encoding="utf-8"))["rows"]}
    keys = sorted(by_key)
    n_ent = sum(len(v2) for v2 in by_key.values())
    print("WRITE SET: %d distinct key(s), %d entr(ies)" % (len(keys), n_ent))

    s3 = boto3.client("s3", region_name=REGION)

    # ---- PHASE 1: assert everything, write nothing ----------------------------------------
    print()
    print("PHASE 1 -- GET every key, assert every `before`, check the rollback pin. NO WRITES.")
    staged, bad_before, drifted, missing = {}, [], [], []
    for i, key in enumerate(keys, 1):
        if key not in base:
            missing.append(key)
            continue
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        body = obj["Body"].read()
        doc = json.loads(body.decode("utf-8"))
        live_ver = obj.get("VersionId")
        if live_ver != base[key]["version_id"]:
            drifted.append((key, base[key]["version_id"], live_ver))
        for e in by_key[key]:
            try:
                cur = get(doc, e["store_field"])
            except (KeyError, IndexError, TypeError) as err:
                bad_before.append((key, e["store_field"], "unlocatable: %s" % err))
                continue
            if cur != e.get("before"):
                bad_before.append((key, e["store_field"], "before differs"))
        staged[key] = {"doc": doc, "version_id": live_ver,
                       "content_type": obj.get("ContentType"),
                       "metadata": obj.get("Metadata") or {},
                       "bytes": len(body),
                       "nonascii": sum(1 for ch in body.decode("utf-8") if ord(ch) > 127)}
        if i % 50 == 0:
            print("  ... asserted %d of %d keys" % (i, len(keys)))

    print("  keys GET: %d of %d ; entries asserted: %d of %d"
          % (len(staged), len(keys), n_ent - len(bad_before), n_ent))
    print("  before-mismatches : %d %s" % (len(bad_before), bad_before[:5]))
    print("  rollback-pin drift: %d %s" % (len(drifted), drifted[:5]))
    print("  missing from base : %d %s" % (len(missing), missing[:5]))
    if bad_before or drifted or missing:
        print("STOP -- phase 1 found a blocker. NOTHING WAS WRITTEN. "
              "A before-mismatch means the plan is stale against the store; pin drift means the "
              "appendix VersionId is no longer the rollback.")
        return 3
    print("  PHASE 1 CLEAN: all %d entries match their `before` and all %d keys still sit on "
          "their appendix VersionId." % (n_ent, len(keys)))

    if a.dry_run:
        print("DRY RUN -- stopping before any write.")
        return 0

    # ---- PHASE 2: one PUT per key --------------------------------------------------------
    print()
    print("PHASE 2 -- one whole-object PUT per key, all entries for a key in ONE put.")
    rows, failed = [], []
    for i, key in enumerate(keys, 1):
        st = staged[key]
        doc = st["doc"]
        fields = []
        for e in by_key[key]:
            set_(doc, e["store_field"], e["after"])
            fields.append(e["store_field"])
        # ensure_ascii=True: the stored body stays pure ASCII (CLAUDE.md "no non-ASCII in
        # production code/logs/AWS"). This can re-escape non-ASCII in fields the plan does not
        # name -- the BYTES of those fields change while the PARSED value does not, which is why
        # the verifier's C3 compares parsed objects. prior_nonascii below makes that visible
        # rather than silent.
        payload = json.dumps(doc, ensure_ascii=True, indent=1).encode("utf-8")
        kw = {"Bucket": BUCKET, "Key": key, "Body": payload}
        if st["content_type"]:
            kw["ContentType"] = st["content_type"]
        if st["metadata"]:
            kw["Metadata"] = st["metadata"]
        try:
            put = s3.put_object(**kw)
        except Exception as err:                                  # noqa: BLE001
            failed.append((key, str(err)))
            print("  PUT FAILED %s: %s" % (key, err))
            break
        rows.append({"store_key": key, "prior_version_id": st["version_id"],
                     "new_version_id": put.get("VersionId"), "fields_set": fields,
                     "entries": len(fields), "prior_bytes": st["bytes"],
                     "new_bytes": len(payload), "prior_nonascii": st["nonascii"]})
        if i % 50 == 0:
            print("  ... wrote %d of %d keys" % (i, len(keys)))

    receipt = {
        "act": "AMGT-ak-6 (A) stored-field rewrite",
        "bucket": BUCKET,
        "keys_planned": len(keys),
        "keys_written": len(rows),
        "entries_planned": n_ent,
        "entries_written": sum(r["entries"] for r in rows),
        "plan_sha256": {c: e for c, _p, e in PLANS},
        "failed": failed,
        "rows": rows,
    }
    json.dump(receipt, io.open(a.out, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("  keys written: %d of %d ; entries: %d of %d ; receipt %s"
          % (len(rows), len(keys), receipt["entries_written"], n_ent, a.out))
    if failed:
        print("STOP -- a PUT failed. The act is PARTIAL: %d key(s) written. Roll back each "
              "written key to its prior_version_id in the receipt, or complete the act." % len(rows))
        return 4
    moved = sum(1 for r in rows if r["new_version_id"] != r["prior_version_id"])
    print("  every key moved off its prior VersionId: %d of %d" % (moved, len(rows)))
    print("AK6 ACT (A) WRITE COMPLETE: %s" % ("YES" if len(rows) == len(keys) else "NO"))
    return 0 if len(rows) == len(keys) else 5


if __name__ == "__main__":
    raise SystemExit(main())
