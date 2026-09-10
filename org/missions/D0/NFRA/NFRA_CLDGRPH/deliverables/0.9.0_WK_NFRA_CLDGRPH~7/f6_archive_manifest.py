#!/usr/bin/env python3
"""TO-CG-F-6 step 2a -- WRITE THE ARCHIVE MANIFEST that travels with the bytes.

The three payload files are hashed HERE, before any upload, and the hashes this
file records are the ones f6_archive.sh compares against S3's own computed
ChecksumSHA256 and the ones the tombstone quotes. One hashing act, one recorded
value, three consumers -- so a mismatch anywhere is a real mismatch and not two
independent reads of the same disk drifting apart.

Fields the criterion requires by name: sha256 (per artifact), builder_last_hash,
bytes_vs_manifest (W3-S11 -- the bytes are 51 days YOUNGER than the manifest
that claims them, and no manifest describes what is on disk).

usage: f6_archive_manifest.py <out.json>
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys

W = "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph"
BUCKET = "opal-313476888478-globgrph"
PFX = "archive/NFRA_CLDGRPH.CG-s-26"
PAYLOADS = ["kuzu_stitch_db", "kuzu_stitch_db._build_manifest.json", "stitch_graph.json"]
BUILDER = "infra/aws/globgrph/kuzu_stitch_load.py"


def sha256_hex(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          check=False).stdout.strip()


def main() -> int:
    out = sys.argv[1]
    artifacts = []
    for name in PAYLOADS:
        p = os.path.join(W, name).replace("\\", "/")
        st = os.stat(p)
        artifacts.append({
            "name": name,
            "archive_key": "%s/%s" % (PFX, name),
            "size_bytes": st.st_size,
            "sha256": sha256_hex(p),
            "mtime_local": _dt.datetime.fromtimestamp(st.st_mtime).isoformat(),
            "mtime_utc": _dt.datetime.fromtimestamp(
                st.st_mtime, tz=_dt.timezone.utc).isoformat(),
            "source_path": p,
            "claim": "measured",
        })

    manifest_doc = json.loads(
        open(os.path.join(W, "kuzu_stitch_db._build_manifest.json"),
             encoding="utf-8").read())

    doc = {
        "archive_manifest_version": 1,
        "written_by": "0.9.0_WK_NFRA_CLDGRPH~7",
        "written_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task_order": "NFRA_CLDGRPH.TO-CG-F-6",
        "cell": "CG-s-26",
        "prd_row": "S26 (PRD v0.6 s.7, addendum @30027295be)",
        "bucket": BUCKET,
        "prefix": PFX,
        "artifacts": artifacts,
        "sha256": {a["name"]: a["sha256"] for a in artifacts},
        "sizes": {a["name"]: a["size_bytes"] for a in artifacts},
        "mtimes_local": {a["name"]: a["mtime_local"] for a in artifacts},
        "build_manifest_content": manifest_doc,
        "bytes_vs_manifest": (
            "bytes 2026-08-27 newer than built_at 2026-07-07; undescribed by any "
            "manifest (W3-S11)"),
        "bytes_vs_manifest_detail": {
            "store_mtime_local": next(a["mtime_local"] for a in artifacts
                                      if a["name"] == "kuzu_stitch_db"),
            "manifest_built_at": manifest_doc.get("built_at"),
            "gap_days": 51,
            "node_count_claim": manifest_doc.get("node_count"),
            "edge_count_claim": manifest_doc.get("edge_count"),
            "edge_count_semantics": manifest_doc.get("edge_count_claim"),
            "reading": (
                "the counts are claims about the JULY bytes; the bytes archived here "
                "are the AUGUST ones. The named capable mutator was INFERRED as the "
                "deleted kuzu_cost_enrich.py. No manifest describes what was on disk, "
                "so these bytes are archived UNDESCRIBED and must never be quoted as "
                "a counted graph."),
            "claim": "measured for the timestamps, inferred for the mutator",
        },
        "builder_last_hash": git("log", "-1", "--format=%H", "--full-history",
                                 "--", BUILDER),
        "builder": {
            "path": BUILDER,
            "disposition": "RETIRE (git rm) under this order",
            "blob_sha1_at_head": git("rev-parse", "HEAD:" + BUILDER),
            "recover_with": "git show <builder_last_hash>:" + BUILDER,
        },
        "served_source": {
            "bucket": BUCKET,
            "key": "stitch/stitch_graph.json",
            "note": ("the cloud-produced stitch, folded into the derive since CG-s-24 "
                     "and read through comp-kuzu against the SERVED projection. This "
                     "is the source now; the archived stitch_graph.json is a July "
                     "hand-run scratch and is not it."),
        },
        "recovery": (
            "aws s3api get-object --bucket %s --key %s/<name> <dest>; the store is a "
            "Kuzu file -- opening it CREATES an absent one, so verify by sha256 "
            "before any engine touches it." % (BUCKET, PFX)),
    }
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("WROTE %s (%d B)" % (out, os.path.getsize(out)))
    for a in artifacts:
        print("  %s size=%d sha256=%s" % (a["name"], a["size_bytes"], a["sha256"]))
    print("  builder_last_hash=%s" % doc["builder_last_hash"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
