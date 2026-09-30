"""NFRA_OPLGTW TO-OG-g-1 AMENDMENT A3 -- the per-master DISTINCT account COUNT of the sealed set.

A3 grants exactly this and nothing else: S3 GetObject BY THE PINNED VersionId on the 5 qualified silver
objects `SEALED_EXPECTED_V2.json` records (no other key, no list, no latest version), via the
`.tools/aws` shim; decode with pyarrow and count DISTINCT account identifiers per master.

WHAT THIS PRINTS: per object, its key, VersionId and ROW COUNT; per master, the DISTINCT account COUNT.
WHAT IT NEVER PRINTS, WRITES, COMMITS OR SENDS: an account identifier, a balance, a holding, or any
other customer value. The bytes land in a temp directory OUTSIDE the repository and are deleted in a
`finally`, so a crash does not leave customer data on disk.

Usage: python <this file>            (counts, for the evidence file)
       python <this file> --verify   (re-runs and compares against RECORDED_COUNTS below)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[8]
_SEAL = _REPO / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~10/SEALED_EXPECTED_V2.json"
_BUCKET = "opal-data-assets"
# The PHYSICAL source column, not the contract catalog name. The contract's `fields` lists
# `account_ref`, which is the Gateway's opaque keyed HMAC over the raw id and exists only in
# responses -- the parquet has no such column. app/integrations/schwab/datasets.json:12: "The source
# column is account_id (schwab_schemas.py:169, CORE)". Counting the raw ids and counting their refs
# give the SAME count (the HMAC is injective per master), so the count is mapping-independent.
_ACCOUNT_COLUMN = "account_id"

# Filled in from the first run; --verify re-measures and compares. A drift here means the pinned
# VersionIds no longer decode to what the seal was computed over, which would void the grant's
# accounts clause -- not a cosmetic mismatch.
RECORDED_COUNTS = {"08242234": None, "08335338": None}


def _aws(args):
    """The repo's aws shim. `.tools/aws` is a bash script that native Windows Python cannot exec, so the
    .cmd forwarder is resolved first on win32. No argument may span lines -- aws.cmd truncates a
    multi-line argv value at the first newline and still returns rc=0."""
    cands = []
    if sys.platform == "win32":
        cands.append(_REPO / ".tools" / "aws.cmd")
    cands.append(_REPO / ".tools" / "aws")
    shim = next((c for c in cands if c.exists()), None)
    if shim is None:
        raise RuntimeError("no aws shim found at %s" % ", ".join(str(c) for c in cands))
    for a in args:
        if "\n" in a:
            raise RuntimeError("refusing a multi-line argv value (aws.cmd truncates it silently)")
    p = subprocess.run([str(shim)] + args, capture_output=True, text=True, timeout=180, cwd=str(_REPO))
    if p.returncode != 0:
        raise RuntimeError("aws rc=%d: %s" % (p.returncode, (p.stderr or p.stdout).strip()[:300]))
    return p.stdout


def measure():
    seal = json.loads(_SEAL.read_text(encoding="utf-8"))
    objects = seal["qualified_objects_used"]
    print("seal: %s" % _SEAL.relative_to(_REPO))
    print("pinned objects to read (denominator): %d -- the grant is these and no others" % len(objects))
    import pyarrow.parquet as pq

    tmp = Path(tempfile.mkdtemp(prefix="og-g1-acct-"))
    per_master = {}
    per_object = []
    try:
        for o in objects:
            key, vid, master = o["key"], o["version_id"], o["master"]
            dest = tmp / (vid + ".parquet")
            _aws(["s3api", "get-object", "--bucket", _BUCKET, "--key", key,
                  "--version-id", vid, str(dest)])
            table = pq.read_table(dest, columns=[_ACCOUNT_COLUMN])
            rows = table.num_rows
            accts = {v for v in table.column(_ACCOUNT_COLUMN).to_pylist() if v is not None}
            per_master.setdefault(master, set()).update(accts)
            per_object.append({"master": master, "dataset": o["dataset"], "date": o["date"],
                               "key": key, "version_id": vid, "rows": rows,
                               "distinct_in_object": len(accts)})
            dest.unlink(missing_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print("PER OBJECT (key, VersionId and row count are recordable; no value is):")
    for r in per_object:
        print("  %-8s %-12s %s  rows=%-6d distinct_accounts_in_object=%d" %
              (r["master"], r["dataset"], r["date"], r["rows"], r["distinct_in_object"]))
        print("      key=%s" % r["key"])
        print("      VersionId=%s" % r["version_id"])
    print()
    print("PER MASTER -- DISTINCT account COUNT over the sealed set (counts only):")
    counts = {m: len(v) for m, v in sorted(per_master.items())}
    for m, n in counts.items():
        print("  master %s: %d distinct account(s)" % (m, n))
    print("total distinct across both masters: %d (masters are disjoint tenants; the sum is not a grain)"
          % sum(counts.values()))
    return counts, per_object


if __name__ == "__main__":
    verify = "--verify" in sys.argv[1:]
    counts, _ = measure()
    if verify:
        if any(v is None for v in RECORDED_COUNTS.values()):
            print("VERIFY: no recorded counts to compare against")
            raise SystemExit(2)
        ok = counts == RECORDED_COUNTS
        print("VERIFY: measured %s vs recorded %s -> %s" % (counts, RECORDED_COUNTS,
                                                            "MATCH" if ok else "DRIFT"))
        raise SystemExit(0 if ok else 1)
    raise SystemExit(0)
