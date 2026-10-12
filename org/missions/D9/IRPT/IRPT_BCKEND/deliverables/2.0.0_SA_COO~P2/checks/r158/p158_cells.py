"""IRPT_BCKEND round 158 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msg 6192, NEVER-2):
  IB158-1  IB-pr-462  four deploy ledger entries left OPEN on site Z 16 to 18 days ago, inherited by this lane: for each open
                      leg, MEASURE THE ARTIFACT it names against what the leg was to produce, with a positive control; verdict
                      SUPERSEDED (world-done or overtaken, citing the measure) or NOT_DONE (what is half-landed, since when).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB158-1-AC1  the four entries were read from origin/box/sitez at a stated commit; every leg of each is listed with its
               closed state as the sentinel holds it; exactly the open legs are measured; the denominators add up.
  IB158-1-AC2  each open leg: what it was to produce, the artifact measured now with the command class and the reading, a
               positive control, and one verdict from the closed set with its claim; a NOT_DONE leg says what is half-landed
               and since when; a SUPERSEDED leg cites the measure that makes it so.
  IB158-1-AC3  the bounds: nothing re-executed, re-applied, rolled back, invoked or signed in; no sentinel edited; no value of
               an account, plan or secret in the record.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~317/"
OUT, READ = D + "IB158-1_open_ledger_legs_measured.json", D + "IB158-1_OPEN_LEDGER_LEGS_MEASURED.md"
SLUGS = ("irpt-p-live-scope-20260923", "irpt-performance-49f-engine-20260924", "irpt-performance-inf-one-use-20260925",
         "irpt-holdings-principals-dispatch-m-20260925")
LEGS = {"irpt-p-live-scope-20260923": (6, ["HTTP"]), "irpt-performance-49f-engine-20260924": (2, ["S1"]),
        "irpt-performance-inf-one-use-20260925": (5, ["S1"]), "irpt-holdings-principals-dispatch-m-20260925": (4, ["N1"])}
VERDICTS = ("SUPERSEDED_WORLD_DONE", "SUPERSEDED_OVERTAKEN", "NOT_DONE")
CLAIMS = ("measured", "inferred", "held", "absent")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB158"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    ents = a.get("entries") or {}
    if set(ents) != set(SLUGS):
        fail("entries must be keyed by exactly the four slugs")
    if cid == "IB158-1-AC1":
        if not re.match(r"^[0-9a-f]{10,40}$", str(a.get("read_from_commit") or "")) or a.get("read_from_ref") != "origin/box/sitez":
            fail("read_from_ref must be origin/box/sitez with read_from_commit")
        n_open = 0
        for s in SLUGS:
            e = ents[s]
            total, want_open = LEGS[s]
            if e.get("legs_total") != total or sorted(e.get("legs_open") or []) != sorted(want_open) or not e.get("author") or not e.get("status_in_sentinel"):
                fail("%s: legs_total %d and legs_open %s as the sentinel holds them, with author and status_in_sentinel" % (s, total, want_open))
            if sorted((e.get("measured") or {}).keys()) != sorted(want_open):
                fail("%s: exactly the open legs are measured" % s)
            n_open += len(want_open)
        if a.get("open_legs_measured") != n_open or a.get("present_on_this_box") not in (True, False):
            fail("open_legs_measured must be %d, and present_on_this_box stated" % n_open)
        print("OK: four entries read at %s; %d open leg(s) measured of %d legs" % (a["read_from_commit"][:10], n_open, sum(v[0] for v in LEGS.values())))
    elif cid == "IB158-1-AC2":
        tally = {}
        for s in SLUGS:
            for leg, m in (ents[s].get("measured") or {}).items():
                if not m.get("was_to_produce") or not isinstance(m.get("measures"), list) or not m["measures"] \
                        or any(not x.get("what") or not x.get("command_class") or "reading" not in x for x in m["measures"]):
                    fail("%s/%s: was_to_produce and measures (each: what, command_class, reading)" % (s, leg))
                pc = m.get("positive_control") or {}
                if not pc.get("what") or "reading" not in pc:
                    fail("%s/%s: a positive control with its reading" % (s, leg))
                v = m.get("verdict")
                if v not in VERDICTS or m.get("claim") not in CLAIMS or not m.get("reason"):
                    fail("%s/%s: verdict in %s, a claim and a reason" % (s, leg, VERDICTS))
                if v == "NOT_DONE" and (not m.get("half_landed") or not m.get("since")):
                    fail("%s/%s: NOT_DONE needs half_landed and since" % (s, leg))
                if v != "NOT_DONE" and not m.get("measure_cited"):
                    fail("%s/%s: a SUPERSEDED verdict cites the measure" % (s, leg))
                tally[v] = tally.get(v, 0) + 1
        if sum(tally.values()) != 4:
            fail("four open legs must each carry a verdict")
        print("OK: verdicts %s" % tally)
    elif cid == "IB158-1-AC3":
        for k in ("re_executed", "re_applied", "rolled_back", "functions_invoked", "sign_ins_made", "sentinels_edited", "aws_writes_made"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not a.get("how_the_close_is_to_be_written"):
            fail("not_established and how_the_close_is_to_be_written must be stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        both = text + rd.read_text(encoding="utf-8")
        # AMENDMENT 1 (row IRPT_BCKEND-D2-W317-S2): the four slugs end in a date; they are not account ids.
        for s in SLUGS:
            both = both.replace(s, "<slug>")
        if re.search(r"acc_[0-9a-f]{12,}", both) or re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", both):
            fail("an account token or an eight-digit token is in the outputs")
        print("OK: nothing re-executed, applied, rolled back, invoked or edited; no account or plan value written")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
