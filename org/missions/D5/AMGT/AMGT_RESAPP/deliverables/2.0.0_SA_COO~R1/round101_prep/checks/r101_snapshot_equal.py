"""AMGT_RESAPP round-101 PREP -- the stored /freshness snapshot equals the live recompute (CTO round-100 ADDENDUM 1, arm 3: "bytes equal to the live recompute").

  PYTHONPATH=<repo root> python r101_snapshot_equal.py

READ-ONLY (S3 listings and GETs through the checkout's own readers; one recompute of the whole view, about 5 s locally). Reads the stored snapshot through
`snapshot.read_freshness_snapshot` (the rule of the checkout), recomputes `scoped_amgt.read_coverage_freshness()`, and compares every key of the two views except `generated_at` and the
`snapshot` / `snapshot_fallback` annotations, with the `rows` compared row by row (by `security_key`). Verdict:
    R101 SNAPSHOT EQUAL: YES            the stored snapshot is current by the checkout's rule and equals the recompute
    R101 SNAPSHOT EQUAL: NO             current, but a row or a key differs (printed, first 10)
    R101 SNAPSHOT EQUAL: NOT CURRENT    the stored snapshot is not current by the checkout's rule: nothing compared (its reason printed)
Exit 0 on YES, 1 otherwise. A difference after a write can be a real input that landed since (a Bloomberg pull between the write and the recompute): the run prints each differing row's
keys so the cause is read, not assumed.
"""
import sys

import boto3


def main():
    from lib.research.api import scoped_amgt
    from lib.research.freshness import snapshot

    s3 = boto3.client("s3", region_name="us-east-1")
    doc, rec = snapshot.read_freshness_snapshot(s3)
    if doc is None:
        print("snapshot not current: %s" % rec.get("reason"))
        print("R101 SNAPSHOT EQUAL: NOT CURRENT")
        return 1
    live = scoped_amgt.read_coverage_freshness()
    skip = {"generated_at", "snapshot", "snapshot_fallback", "rows"}
    diffs = []
    # The snapshot is written BY the function (a Lambda: packaged files at /var/task/...); this recompute runs in the checkout (the same files at the checkout's own path). The
    # `object_key` of a PACKAGED list read is the deployed artifact's path, an environment fact and not a value: it is blanked on both sides and the note printed.
    env_notes = []

    def _blank_packaged_paths(view):
        lists = ((view.get("reads") or {}).get("lists") or {}) if isinstance(view.get("reads"), dict) else {}
        for name, entry in lists.items():
            if isinstance(entry, dict) and entry.get("source") == "packaged" and "object_key" in entry:
                env_notes.append("reads.lists.%s.object_key (packaged: %s)" % (name, str(entry["object_key"])[:50]))
                entry["object_key"] = "<packaged path>"
        return view

    doc = _blank_packaged_paths(dict(doc))
    live = _blank_packaged_paths(dict(live))
    for k in sorted(set(doc) | set(live)):
        if k in skip:
            continue
        if doc.get(k) != live.get(k):
            diffs.append("key %s: snapshot %r vs recompute %r" % (k, str(doc.get(k))[:60], str(live.get(k))[:60]))
    a = {r.get("security_key") or r.get("name"): r for r in doc.get("rows") or []}
    b = {r.get("security_key") or r.get("name"): r for r in live.get("rows") or []}
    for name in sorted(set(a) | set(b), key=str):
        if a.get(name) != b.get(name):
            ra, rb = a.get(name) or {}, b.get(name) or {}
            cols = sorted(c for c in set(ra) | set(rb) if ra.get(c) != rb.get(c))
            diffs.append("row %s: %s differ" % (name, ",".join(str(c) for c in cols)[:80]))
    for note in sorted(set(env_notes)):
        print("   environment path blanked on both sides: " + note)
    print("snapshot generated_at %s age %s h | rows: snapshot %d, recompute %d | differing: %d" % (rec.get("generated_at"), rec.get("age_hours"), len(a), len(b), len(diffs)))
    for d in diffs[:10]:
        print("   " + d)
    print("R101 SNAPSHOT EQUAL: %s" % ("YES" if not diffs else "NO"))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
