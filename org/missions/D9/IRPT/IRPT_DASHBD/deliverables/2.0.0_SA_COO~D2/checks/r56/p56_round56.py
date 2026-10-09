"""IRPT_DASHBD round 56 (issuer 2.0.0_SA_COO~D2) -- the memory-step pair (COO half @ca40177794, CTO half NEVER_WIDEN_MEMSTEP_CTO_HALF.md,
msg 3789): apply memory_size 2048 -> 3008 on the gold Lambda, the setting only, then the 10-08 dry run under 3008 as the after-proof.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB56-1-AC1  ~87/MEMSTEP_APPLY_RECORD.json: before {codesha256 == oNgy4rnr, memory_mb == 2048}; plan == {add 0, change 1, destroy 0} with
              plan_changes == ["memory_size"]; after {codesha256 == oNgy4rnr, memory_mb == 3008}; replan_no_changes true; dry_run {duration_ms,
              max_memory_mb, written_objects == 0}; verdict UNDER iff duration < 0.85*900*1000 and memory < 0.85*3008, else OVER with
              rollback.memory_mb_after == 2048; ledger_entry names a file at HEAD.
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~87/MEMSTEP_APPLY_RECORD.json"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB56"))
        sys.exit(1)

    if cid != "DB56-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    b, a = r.get("before") or {}, r.get("after") or {}
    if b.get("codesha256") != LIVE or b.get("memory_mb") != 2048:
        fail("before %r" % b)
    if r.get("plan") != {"add": 0, "change": 1, "destroy": 0} or r.get("plan_changes") != ["memory_size"]:
        fail("plan %r / changes %r" % (r.get("plan"), r.get("plan_changes")))
    if a.get("codesha256") != LIVE or a.get("memory_mb") != 3008 or r.get("replan_no_changes") is not True:
        fail("after %r / replan %r" % (a, r.get("replan_no_changes")))
    d = r.get("dry_run") or {}
    try:
        dur, mem = float(d["duration_ms"]), float(d["max_memory_mb"])
    except (KeyError, TypeError, ValueError):
        fail("dry_run %r" % d)
    if d.get("written_objects") != 0:
        fail("written_objects %r" % d.get("written_objects"))
    under = dur < 0.85 * 900 * 1000 and mem < 0.85 * 3008
    if r.get("verdict") != ("UNDER" if under else "OVER"):
        fail("verdict %r but measured %s" % (r.get("verdict"), "UNDER" if under else "OVER"))
    if not under and (r.get("rollback") or {}).get("memory_mb_after") != 2048:
        fail("OVER without a recorded rollback to 2048")
    if not r.get("ledger_entry") or not (root / r["ledger_entry"]).is_file():
        fail("ledger_entry %r" % r.get("ledger_entry"))
    print("OK: memory 2048 -> 3008, code unchanged; dry run %s (%.1f s, %d MB)" % (r["verdict"], dur / 1000, mem))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
