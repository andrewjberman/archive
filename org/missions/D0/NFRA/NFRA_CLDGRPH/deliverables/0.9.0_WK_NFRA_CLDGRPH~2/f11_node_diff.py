#!/usr/bin/env python3
"""The CTO's discriminator for the CG-s-31 image act: a BEFORE/AFTER node diff of the SERVED graph.

The sign covers ONE change on the served plane -- the fold no longer writes
`vocabulary=stitch-v1` -- so the diff must read exactly `{PORTAL_BUNDLE: -vocabulary}` for the
props of a node that exists on both sides, and every other difference must be attributable and
named. A claim that "only the stamp changed" is worth nothing unless the instrument could have
seen a second change: this one reads EVERY node's id, type and props, not the stamp's own query.

  snapshot <file>   read the served graph now and write the snapshot
  diff <before> <after>

Run from the repository root.
"""
import collections
import hashlib
import json
import os
import subprocess
import sys

BASH = os.environ.get("BASH_BIN") or "bash"
Q = ("MATCH (n:CloudNode) RETURN n.node_id AS id, n.node_type AS t, n.props AS p "
     "ORDER BY id SKIP %d LIMIT %d")
PAGE = 6000


def _rows():
    out, skip = [], 0
    while True:
        p = subprocess.run([BASH, ".tools/comp-kuzu", "--json", Q % (skip, PAGE)],
                           capture_output=True, text=True)
        try:
            batch = json.loads(p.stdout)
        except Exception:  # noqa: BLE001
            raise SystemExit("BLOCKED: the served read did not return JSON at skip=%d: %s"
                             % (skip, (p.stderr or "")[:200]))
        out.extend(batch)
        if len(batch) < PAGE:
            return out
        skip += PAGE


def snapshot(path):
    rows = _rows()
    snap = {r["id"]: [r.get("t"), r.get("p") or ""] for r in rows}
    json.dump({"count": len(rows), "distinct_ids": len(snap), "nodes": snap},
              open(path, "w", encoding="utf-8"))
    print("SNAPSHOT rows=%d distinct_ids=%d -> %s" % (len(rows), len(snap), path))


def _props(s):
    try:
        return json.loads(s) if s else {}
    except Exception:  # noqa: BLE001
        return {"__unparseable__": s}


def diff(before_path, after_path):
    b = json.load(open(before_path, encoding="utf-8"))
    a = json.load(open(after_path, encoding="utf-8"))
    B, A = b["nodes"], a["nodes"]
    added = sorted(set(A) - set(B))
    removed = sorted(set(B) - set(A))
    type_changed, prop_changed = [], []
    key_delta = collections.Counter()
    for nid in set(A) & set(B):
        bt, bp = B[nid]
        at, ap = A[nid]
        if bt != at:
            type_changed.append((nid, bt, at))
        if bp != ap:
            pb, pa = _props(bp), _props(ap)
            gone = sorted(set(pb) - set(pa))
            new = sorted(set(pa) - set(pb))
            moved = sorted(k for k in set(pa) & set(pb) if pa[k] != pb[k])
            prop_changed.append((nid, at, gone, new, moved))
            for k in gone:
                key_delta["-" + k] += 1
            for k in new:
                key_delta["+" + k] += 1
            for k in moved:
                key_delta["~" + k] += 1
    print("NODE_DIFF before=%d after=%d" % (len(B), len(A)))
    print("NODES_ADDED=%d NODES_REMOVED=%d TYPE_CHANGED=%d PROPS_CHANGED=%d"
          % (len(added), len(removed), len(type_changed), len(prop_changed)))
    print("PROPS_KEY_DELTA=%s" % dict(key_delta))
    print()
    print("  -- every props change, by node type and key --")
    per_type = collections.Counter()
    for nid, t, gone, new, moved in prop_changed:
        per_type[(t, tuple("-" + k for k in gone) + tuple("+" + k for k in new)
                  + tuple("~" + k for k in moved))] += 1
    for (t, keys), c in sorted(per_type.items(), key=lambda kv: -kv[1]):
        print("     %-18s %-28s %d node(s)" % (t, ",".join(keys) or "(value-only)", c))
    for nid, t, gone, new, moved in prop_changed[:8]:
        print("       e.g. %s [%s] -%s +%s ~%s" % (nid[:60], t, gone, new, moved))
    print()
    print("  -- added / removed node ids, by type --")
    print("     added   : %s" % dict(collections.Counter(A[i][0] for i in added)))
    print("     removed : %s" % dict(collections.Counter(B[i][0] for i in removed)))
    for i in added[:6]:
        print("       + %s [%s]" % (i[:70], A[i][0]))
    for i in removed[:6]:
        print("       - %s [%s]" % (i[:70], B[i][0]))
    print()
    stamp_only = (list(key_delta) == ["-vocabulary"])
    print("PROPS_DELTA_IS_STAMP_ONLY=%s" % str(stamp_only).lower())
    print("DENOMINATOR: %d node(s) on the before side and %d on the after side, every one read "
          "with its id, type and props -- not a query scoped to the stamp, so a SECOND props "
          "change would appear on the PROPS_KEY_DELTA line above." % (len(B), len(A)))
    print("SNAPSHOT_SHA256 before=%s after=%s"
          % (hashlib.sha256(open(before_path, 'rb').read()).hexdigest()[:16],
             hashlib.sha256(open(after_path, 'rb').read()).hexdigest()[:16]))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "snapshot":
        snapshot(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "diff":
        diff(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
