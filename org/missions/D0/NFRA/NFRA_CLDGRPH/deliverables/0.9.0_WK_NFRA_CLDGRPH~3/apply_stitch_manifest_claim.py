#!/usr/bin/env python3
"""CG-s-20 deliverable 3 -- put the S53 CLAIM FIELDS on the stitch store's
manifest in the MAIN WORKSPACE. Run once; idempotent; prints the file before
and after; opens no store with any engine and changes no store's bytes.

kuzu_stitch_db._build_manifest.json is EDITED IN PLACE: two keys ADDED, nothing
else touched (the script asserts the pre-existing key/value set is identical
after the write).

  edge_count_claim = merge_attempts   -- kuzu_stitch_load.py stamps `written`,
      which increments once per MERGE EXECUTED; MERGE is idempotent, so the
      number is an UPPER BOUND on the edges in the artifact.
  artifact_claim   = interim_local_projection -- CG-s-20 decided the stitch
      surface's HOME is JOIN_PROJECTION, so this store is an interim local
      projection of a cloud-produced graph, never the graph itself.

WHAT THE CLAIM DOES NOT FIX, stated because a field that looks complete is
worse than an absent one: the manifest's built_at (2026-07-07T15:46:38Z) does
NOT describe the bytes on disk. The store's Modify AND Change times are both
2026-08-27 02:32:00 local -- a content write 51 days after the build, with no
manifest rewritten beside it. node_count and edge_count are therefore claims
about the 2026-07-07 bytes. That is recorded in CG-s-20's record and in the
surprise row, and is NOT papered over here.

USAGE: python apply_stitch_manifest_claim.py [--check]
"""
from __future__ import annotations

import json
import os
import sys

W = r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph"
STITCH_MANIFEST = os.path.join(W, "kuzu_stitch_db._build_manifest.json")
STORE = os.path.join(W, "kuzu_stitch_db")


def show(path: str, label: str) -> None:
    print("--- %s: %s ---" % (label, path))
    if not os.path.exists(path):
        print("  (absent)")
        return
    with open(path, encoding="utf-8") as fh:
        print("".join("  " + ln for ln in fh.readlines()))


def main() -> int:
    check = "--check" in sys.argv[1:]
    st = os.stat(STORE)
    print("STORE BEFORE: %s bytes=%d mtime_epoch=%d" % (STORE, st.st_size, st.st_mtime))
    show(STITCH_MANIFEST, "BEFORE")

    with open(STITCH_MANIFEST, encoding="utf-8") as fh:
        before = json.load(fh)
    after = dict(before)
    after["edge_count_claim"] = "merge_attempts"
    after["artifact_claim"] = "interim_local_projection"
    untouched_before = {k: v for k, v in before.items()
                        if k not in ("edge_count_claim", "artifact_claim")}
    untouched_after = {k: v for k, v in after.items()
                       if k not in ("edge_count_claim", "artifact_claim")}
    assert untouched_before == untouched_after, "a pre-existing key changed"
    if not check:
        tmp = STITCH_MANIFEST + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(after, fh, indent=2, sort_keys=True)
        os.replace(tmp, STITCH_MANIFEST)

    show(STITCH_MANIFEST, "AFTER")
    st2 = os.stat(STORE)
    print("STORE AFTER:  %s bytes=%d mtime_epoch=%d" % (STORE, st2.st_size, st2.st_mtime))
    print("STORE_UNTOUCHED=%s" % ((st.st_size, st.st_mtime) == (st2.st_size, st2.st_mtime)))
    print("PRE_EXISTING_KEYS_UNCHANGED=%d of %d" % (len(untouched_before), len(before)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
