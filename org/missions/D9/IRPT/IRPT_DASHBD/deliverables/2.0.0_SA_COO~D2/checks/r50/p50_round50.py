"""IRPT_DASHBD round 50 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's R44 CTO half AMENDMENT 1 (msg 3550, @b758031ba2): ONE dry-run
backfill of 2026-10-08 on live oNgy4rnr, no writes; under 85% of the timeout AND the memory closes ledger leg S1 with the read, over either is
Branch B to yIAQjspL now. Monday 2026-10-12 07:41 ET stays the acceptance.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB50-1-AC1  ~78/R44_SIZING_DRYRUN.json: codesha256 == oNgy4rnr; event.dry_run is true with backfill 2026-10-08..2026-10-08 and accounts
              "population"; accounts >= 7000 and lots_rows > 0 (the run sized the lots stage); duration_ms, max_memory_mb, timeout_s,
              memory_mb present; verdict == UNDER iff duration_ms < 0.85 * timeout_s * 1000 and max_memory_mb < 0.85 * memory_mb; on UNDER
              ledger_leg_closed is true; on OVER rollback.live_codesha256_after == yIAQjspL; written_objects == 0.
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~78/R44_SIZING_DRYRUN.json"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="
BASE = "yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB50"))
        sys.exit(1)

    if cid != "DB50-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    ev = r.get("event") or {}
    if r.get("codesha256") != LIVE:
        fail("codesha256 %r" % r.get("codesha256"))
    if ev.get("dry_run") is not True or ev.get("backfill") != {"start": "2026-10-08", "end": "2026-10-08"} or ev.get("accounts") != "population":
        fail("event %r" % ev)
    if not isinstance(r.get("accounts"), int) or r["accounts"] < 7000 or not isinstance(r.get("lots_rows"), int) or r["lots_rows"] <= 0:
        fail("accounts %r / lots_rows %r: the run did not size the lots stage" % (r.get("accounts"), r.get("lots_rows")))
    try:
        dur, mem, to, ms = float(r["duration_ms"]), float(r["max_memory_mb"]), float(r["timeout_s"]), float(r["memory_mb"])
    except (KeyError, TypeError, ValueError):
        fail("sizing fields missing")
    under = dur < 0.85 * to * 1000 and mem < 0.85 * ms
    if r.get("verdict") != ("UNDER" if under else "OVER"):
        fail("verdict %r but measured %s" % (r.get("verdict"), "UNDER" if under else "OVER"))
    if under and r.get("ledger_leg_closed") is not True:
        fail("UNDER but ledger leg S1 not closed")
    if not under and (r.get("rollback") or {}).get("live_codesha256_after") != BASE:
        fail("OVER but no rollback to yIAQjspL recorded")
    if r.get("written_objects") != 0:
        fail("written_objects %r (a dry run writes nothing)" % r.get("written_objects"))
    print("OK: %s -- %.1f s of %d s, %d MB of %d MB" % (r["verdict"], dur / 1000, to, mem, ms))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
