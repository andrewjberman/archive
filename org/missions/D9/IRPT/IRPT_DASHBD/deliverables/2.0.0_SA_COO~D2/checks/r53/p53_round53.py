"""IRPT_DASHBD round 53 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 18 item 1 (msg 3598, @a25a7e1ea5): ONE more no-write dry run on
live oNgy4rnr, on the HEAVIEST lots day of the last 90 days, chosen by the largest lot-row count, printed with its denominator. Over the 85% line
on that day means a pair (producer fix preferred, or a memory change with its own before/after).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB53-1-AC1  ~82/R44_HEAVY_DAY_DRYRUN.json: selection.window_days == 90; selection.days_read is a positive count (the denominator) and
              selection.chosen_day carries the maximum lot_rows of selection.top (each entry {day, lot_rows}); codesha256 == oNgy4rnr; the event
              is a dry_run population backfill of exactly chosen_day; duration_ms, max_memory_mb, timeout_s, memory_mb present; verdict UNDER
              iff duration < 0.85*timeout*1000 and memory < 0.85*memory_mb, else OVER; written_objects == 0.
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~82/R44_HEAVY_DAY_DRYRUN.json"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB53"))
        sys.exit(1)

    if cid != "DB53-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    sel = r.get("selection") or {}
    top = sel.get("top") or []
    if sel.get("window_days") != 90 or not isinstance(sel.get("days_read"), int) or sel["days_read"] <= 0 or not top:
        fail("selection %r" % {k: sel.get(k) for k in ("window_days", "days_read")})
    best = max(top, key=lambda x: x.get("lot_rows", -1))
    day = sel.get("chosen_day")
    if day != best.get("day"):
        fail("chosen_day %r is not the max lot_rows day %r" % (day, best.get("day")))
    ev = r.get("event") or {}
    if r.get("codesha256") != LIVE or ev.get("dry_run") is not True or ev.get("accounts") != "population" \
            or ev.get("backfill") != {"start": day, "end": day}:
        fail("codesha256 %r / event %r" % (r.get("codesha256"), ev))
    try:
        dur, mem, to, ms = float(r["duration_ms"]), float(r["max_memory_mb"]), float(r["timeout_s"]), float(r["memory_mb"])
    except (KeyError, TypeError, ValueError):
        fail("sizing fields missing")
    under = dur < 0.85 * to * 1000 and mem < 0.85 * ms
    if r.get("verdict") != ("UNDER" if under else "OVER"):
        fail("verdict %r but measured %s" % (r.get("verdict"), "UNDER" if under else "OVER"))
    if r.get("written_objects") != 0:
        fail("written_objects %r" % r.get("written_objects"))
    print("OK: %s on %s (%d lot rows; %d days read) -- %.1f s, %d MB" % (r["verdict"], day, best["lot_rows"], sel["days_read"], dur / 1000, mem))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
