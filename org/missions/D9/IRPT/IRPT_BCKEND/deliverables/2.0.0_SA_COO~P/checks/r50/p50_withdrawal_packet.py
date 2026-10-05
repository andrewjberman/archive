"""IRPT_BCKEND round 50 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the W100-S2 never-widen withdrawal packet (CTO batch 251). A
read-only cell: the packet is a record; the CTO signs it and the S3 delete is Andrew's.

Usage: python <this file> <repo_root> <criterion_id>
  IB50-1-AC1  the packet (PACKET) carries the six parts batch 251 names:
              - `versioning`, a non-empty value read from get_bucket_versioning;
              - `perfrp_keys`, a non-empty list where each entry has key, etag, size, last_modified, writer and
                carries_20250110, plus `perfrp_keys_denominator` equal to its length;
              - `withdrawal_set`, a non-empty subset of those keys that includes the 49F account leaf, every member
                measured carries_20250110 true;
              - `rollback`, one entry per withdrawal key;
              - `stop_rule`, naming the ETag;
              - `after_read`, naming PROD and a 49F login.
              Base: FAIL (no packet).
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import sys
from pathlib import Path

PACKET = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~122/W100S2_WITHDRAWAL_PACKET.json"
LEAF = "platinum/advi/49financial/perfrp_performance_account.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB50-1"))
        sys.exit(1)

    if cid != "IB50-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / PACKET
    if not p.is_file():
        fail("no %s" % PACKET)
    c = json.loads(p.read_bytes().decode("utf-8"))
    for k in ("versioning", "perfrp_keys", "perfrp_keys_denominator", "withdrawal_set", "rollback", "stop_rule", "after_read"):
        if not c.get(k):
            fail("packet lacks %r" % k)
    keys = c["perfrp_keys"]
    if c["perfrp_keys_denominator"] != len(keys):
        fail("denominator %r != %d keys listed" % (c["perfrp_keys_denominator"], len(keys)))
    for e in keys:
        miss = [f for f in ("key", "etag", "size", "last_modified", "writer", "carries_20250110") if f not in e]
        if miss:
            fail("key entry %r lacks %s" % (e.get("key"), miss))
    by_key = {e["key"]: e for e in keys}
    ws = c["withdrawal_set"]
    ws_keys = [w if isinstance(w, str) else w.get("key") for w in ws]
    if not any(k and k.endswith(LEAF) for k in ws_keys):
        fail("the 49F account leaf is not in the withdrawal set")
    for k in ws_keys:
        if k not in by_key:
            fail("withdrawal key %r is not among the listed perfrp keys" % k)
        if by_key[k]["carries_20250110"] is not True:
            fail("withdrawal key %r is not measured to carry 2025-01-10" % k)
    rb = c["rollback"]
    rb_keys = set(rb) if isinstance(rb, dict) else {r.get("key") for r in rb}
    if set(ws_keys) - rb_keys:
        fail("no rollback for %s" % sorted(set(ws_keys) - rb_keys))
    if "etag" not in json.dumps(c["stop_rule"]).lower():
        fail("stop_rule does not name the ETag")
    ar = json.dumps(c["after_read"]).lower()
    if "prod" not in ar or "49" not in ar:
        fail("after_read does not name PROD and a 49F login")
    print("OK: versioning %r; %d perfrp keys; withdrawal set %d; rollback %d" % (c["versioning"], len(keys), len(ws_keys), len(rb_keys)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
