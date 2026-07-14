"""OPAL_ASSETS C2 follow-on: reap the 2,269 flat/type-collapsed orion orphan keys.

AUTHORITY (recorded): Andrew verbatim GO ("Go for sure on 1.)", ~05:5xZ ET 2026-07-14, relayed COO
060839Z) + CTO grant-gate PASS at his source read of 2d2b13705 + COO re-confirm 075027Z + CTO
no-objection 075236Z. Key list pinned at git blob f5ead206452c237a9d07713eaacfa0a8e50bc33f
(conversion-invariant; @ commit 2cc0f8fee).

DISCIPLINE:
  - Denominators enumerated AT RUN TIME (ruling 13b), never quoted from a document.
  - SET IDENTITY asserted before any delete: live flat-class keys == pinned list, symmetric
    difference EMPTY. A live flat key NOT on the list (mirror regression) or a listed key already
    gone (concurrent actor) is a STOP, not a skip.
  - Partition completeness asserted: flat + typed == total, zero unclassified keys.
  - Per-batch result verification: every response key checked against Deleted[] / Errors[].
  - Post-delete re-enumeration: flat class == 0 AND typed count UNCHANGED from the snapshot.
  - The bucket is versioned-without-expiry (ruling 17): deletes write MARKERS; the corrupt bytes
    persist as noncurrent versions BY DESIGN. The guard reads current listings; 0 = success.

The IAM grant (opal-c2-orphan-reap-role, bronze/20* scoping + belt Denies) makes a scripting bug
structurally unable to delete a good key; this script's checks are the second, independent layer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-assets"
PREFIX = "orion/inflection/bronze/"
ROLE_ARN = "arn:aws:iam::313476888478:role/opal-c2-orphan-reap-role"
ORPHAN_RE = re.compile(r"^orion/inflection/bronze/\d{4}-\d{2}-\d{2}\.jsonl\.gz$")
TYPED_RE = re.compile(r"^orion/inflection/bronze/[A-Za-z][^/]*/[^/]+$")


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {msg}", flush=True)


def enumerate_classes(s3) -> tuple[set[str], set[str], int]:
    flat: set[str] = set()
    typed: set[str] = set()
    total = 0
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            total += 1
            if ORPHAN_RE.fullmatch(key):
                flat.add(key)
            elif TYPED_RE.fullmatch(key):
                typed.add(key)
            else:
                raise SystemExit(f"STOP: UNCLASSIFIED KEY (partition incomplete): {key!r}")
    return flat, typed, total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-file", required=True, help="pinned orphan key list (blob f5ead2064)")
    ap.add_argument("--execute", action="store_true", help="actually delete (default: dry-run)")
    args = ap.parse_args()

    with open(args.list_file, encoding="ascii") as f:
        pinned = {ln.strip() for ln in f if ln.strip() and not ln.startswith("#")}
    log(f"pinned list: {len(pinned)} keys")
    bad = [k for k in pinned if not ORPHAN_RE.fullmatch(k)]
    if bad:
        raise SystemExit(f"STOP: {len(bad)} pinned keys fail the orphan class regex, e.g. {bad[:3]}")

    sts = boto3.client("sts")
    creds = sts.assume_role(RoleArn=ROLE_ARN, RoleSessionName="c2-orphan-reap-0-6-2")["Credentials"]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )
    log(f"assumed {ROLE_ARN}")

    flat, typed, total = enumerate_classes(s3)
    log(f"SNAPSHOT (run-time enumerated): total={total} flat={len(flat)} typed={len(typed)}")
    if len(flat) + len(typed) != total:
        raise SystemExit("STOP: partition incomplete (flat + typed != total)")

    only_live = sorted(flat - pinned)
    only_pinned = sorted(pinned - flat)
    if only_live or only_pinned:
        log(f"STOP: SET IDENTITY FAILED: live-not-pinned={len(only_live)} {only_live[:5]}")
        log(f"      pinned-not-live={len(only_pinned)} {only_pinned[:5]}")
        raise SystemExit("STOP: the live flat class is not the pinned list -- escalate, do not delete")
    log(f"SET IDENTITY HOLDS: live flat class == pinned list ({len(pinned)} keys, symmetric diff empty)")

    if not args.execute:
        log("DRY-RUN complete (no deletes issued). Re-run with --execute.")
        return 0

    targets = sorted(pinned)
    deleted: list[str] = []
    errors: list[dict] = []
    for i in range(0, len(targets), 1000):
        batch = targets[i : i + 1000]
        resp = s3.delete_objects(
            Bucket=BUCKET,
            Delete={"Objects": [{"Key": k} for k in batch], "Quiet": False},
        )
        got = {d["Key"] for d in resp.get("Deleted", [])}
        errs = resp.get("Errors", [])
        errors.extend(errs)
        missing = [k for k in batch if k not in got and k not in {e["Key"] for e in errs}]
        if missing:
            raise SystemExit(f"STOP: {len(missing)} keys in neither Deleted nor Errors, e.g. {missing[:3]}")
        markers = sum(1 for d in resp.get("Deleted", []) if d.get("DeleteMarker"))
        deleted.extend(sorted(got))
        log(f"batch {i // 1000 + 1}: requested={len(batch)} deleted={len(got)} markers={markers} errors={len(errs)}")

    log(f"TALLY: deleted={len(deleted)} errors={len(errors)}")
    for e in errors[:10]:
        log(f"  ERROR: {e}")

    flat2, typed2, total2 = enumerate_classes(s3)
    log(f"POST-STATE: total={total2} flat={len(flat2)} typed={len(typed2)}")
    ok = not errors and len(deleted) == len(pinned) and len(flat2) == 0 and typed2 == typed
    verdict = "REAP COMPLETE" if ok else "REAP FAILED"
    log(f"{verdict}: deleted {len(deleted)}/{len(pinned)}; post flat={len(flat2)} (expect 0); "
        f"typed unchanged={typed2 == typed} ({len(typed)} -> {len(typed2)})")
    print(json.dumps({
        "verdict": verdict,
        "pinned": len(pinned),
        "snapshot": {"total": total, "flat": len(flat), "typed": len(typed)},
        "deleted": len(deleted),
        "errors": len(errors),
        "post": {"total": total2, "flat": len(flat2), "typed": len(typed2)},
        "typed_set_unchanged": typed2 == typed,
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
