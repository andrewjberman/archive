"""IRPT_DASHBD round 65 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4459: FWD-11 is unbuilt for the reporting read.

Cell: DB-b-121 one read-only cell before any build: (1) what the reporting read needs per firm, and whether Cottonwood has it; (2) whether
the page's year-to-date needs the reporting summary at all once the performance route answers; (3) what DB-b-86's hop3 run reads of the
Cottonwood returns gold minted on 2026-10-11, since a reader of it is its own never-widen pair.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB65-1-AC1  ~96/REPORTING_READ_PER_FIRM.json: per_firm_needs is a non-empty list of {need, source: {file, line}}; cottonwood_has
              covers every need by its `need` text, each with state PRESENT / ABSENT / ACCESS_DENIED / NOT_ESTABLISHED and evidence;
              ytd_needs_summary is YES / NO / NOT_ESTABLISHED with basis [{file, line}] and a plain `because`; hop3 {reads (a
              non-empty list of {what, source: {file, line}}), reads_cottonwood_returns_gold (bool), existing_readers (int)};
              every source file inside this repo exists at HEAD; a NOT_ESTABLISHED or ACCESS_DENIED answer says what would settle it.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~96/"
STATES = ("PRESENT", "ABSENT", "ACCESS_DENIED", "NOT_ESTABLISHED")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB65"))
        sys.exit(1)

    def src_ok(s, portal_ok=False):
        if not isinstance(s, dict) or not s.get("file") or not isinstance(s.get("line"), int):
            return False
        if s.get("repo") == "portal":
            return portal_ok
        return (root / str(s["file"])).is_file()

    if cid != "DB65-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (D + "REPORTING_READ_PER_FIRM.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    needs = r.get("per_firm_needs") or []
    if not needs or any(not str(n.get("need") or "").strip() or not src_ok(n.get("source")) for n in needs):
        fail("per_firm_needs is empty, or an entry lacks its need or a file-and-line source at HEAD")
    has = {str(h.get("need")): h for h in (r.get("cottonwood_has") or [])}
    for n in needs:
        h = has.get(str(n["need"]))
        if not h or h.get("state") not in STATES or not str(h.get("evidence") or "").strip():
            fail("cottonwood_has lacks %r with a state and evidence" % n["need"])
        if h["state"] in ("ACCESS_DENIED", "NOT_ESTABLISHED") and not str(h.get("what_would_settle_it") or "").strip():
            fail("%r is %s without what_would_settle_it" % (n["need"], h["state"]))
    y = r.get("ytd_needs_summary")
    if y not in ("YES", "NO", "NOT_ESTABLISHED") or not str(r.get("because") or "").strip():
        fail("ytd_needs_summary %r or its because is missing" % y)
    if not r.get("basis") or any(not src_ok(b, portal_ok=True) for b in r["basis"]):
        fail("basis lacks file-and-line entries")
    if y == "NOT_ESTABLISHED" and not str(r.get("ytd_what_would_settle_it") or "").strip():
        fail("ytd_needs_summary NOT_ESTABLISHED without ytd_what_would_settle_it")
    h3 = r.get("hop3") or {}
    if not h3.get("reads") or any(not str(x.get("what") or "").strip() or not src_ok(x.get("source")) for x in h3["reads"]) \
            or not isinstance(h3.get("reads_cottonwood_returns_gold"), bool) or not isinstance(h3.get("existing_readers"), int):
        fail("hop3 %r" % {k: h3.get(k) for k in ("reads_cottonwood_returns_gold", "existing_readers")})
    n = {s: sum(1 for h in has.values() if h.get("state") == s) for s in STATES}
    print("OK: %d per-firm need(s); Cottonwood: %r; the YTD needs the summary: %s; hop3 reads the Cottonwood returns gold: %s"
          % (len(needs), n, y, h3["reads_cottonwood_returns_gold"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
