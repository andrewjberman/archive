"""Positive control and negatives for p198_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control198.py <real_repo_root>
Builds a temp root with synthetic records and packets in the shapes the order asks for, runs every criterion in-process expecting PASS, then applies
each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r198"))
import p198_cells as P  # noqa: E402

P6 = P.P6
P1, P2 = P.PIN1, P.PIN2


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")


def firm_rec(total):
    return {"total_changed_nodes": total}


def recs():
    r196 = {"firms": {"49financial": firm_rec(32), "cottonwood": firm_rec(485), "inflection": firm_rec(841)}}
    r197 = {"firms": {"49financial": firm_rec(119), "cottonwood": firm_rec(255), "inflection": firm_rec(841)}}
    rec = {"notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    v2 = "# v2\n" + ("v2 line\n" * 100)
    v3 = v2 + ("\n## v3\nA per-firm pin table, a temporary fork closed by the CUSIP port's own release (%s) for reconvergence; opal_unidentified in the closure; "
               "the built bundle, the cash rule, same served state, Branch A, Branch B, manifest anchor, business date, moved member, signed scope.\n"
               "| firm | pin | moved by | changed nodes |\n|---|---|---|---|\n"
               "| 49financial | %s | the cash rule | 32 |\n| cottonwood | %s | the cash rule | 255 |\n| inflection | %s | the cash rule | 841 |\n"
               "49financial at pin 2 measured 119 changed nodes (87 outside the rule), which is why it stays on the closure-fix pin.\n"
               "COO half UNSIGNED. CTO half UNSIGNED.\n" % (P.CUSIP_PORT, P1, P2, P2)) + ("padding line\n" * 400)
    return r196, r197, rec, v2, v3


def put(root, r196, r197, rec, v2, v3):
    wt(root, P.R196_2, json.dumps(r196))
    wt(root, P.R197_2, json.dumps(r197))
    wt(root, P.R_REC, json.dumps(rec))
    wt(root, P6.V2, v2)
    wt(root, P.V3, v3)


def run(root, cid):
    P6.ROOT, P6.CID = root, cid
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            P.CHECKS[cid]()
        return cid + " PASS"
    except SystemExit:
        return cid + " FAIL"
    except Exception as e:  # noqa: BLE001 -- a crash is not a verdict
        return cid + " CRASH " + type(e).__name__ + ": " + str(e)[:120]


bad = 0
root = Path(tempfile.mkdtemp(prefix="c198_"))
base = recs()
put(root, *base)
for cid in P.CHECKS:
    r = run(root, cid)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))


def neg(label, cid, v3=None, rec=None, r196=None, r197=None):
    global bad
    rr = list(base)
    if v3 is not None:
        rr[4] = v3
    if rec is not None:
        rr[2] = rec
    if r196 is not None:
        rr[0] = r196
    if r197 is not None:
        rr[1] = r197
    put(root, *rr)
    r = run(root, cid)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-52s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))


v3 = base[4]
neg("v3 is v2 plus little", "IB198-1-AC1", v3="# v2\n" + ("v2 line\n" * 100) + "x\n")
neg("v3 without the closure-fix pin", "IB198-1-AC1", v3=v3.replace(P1, "0" * 40))
neg("v3 without pin 2", "IB198-1-AC1", v3=v3.replace(P2, "0" * 40))
neg("v3 without the CUSIP port", "IB198-1-AC1", v3=v3.replace(P.CUSIP_PORT, "abc"))
neg("v3 without the temporary fork", "IB198-1-AC1", v3=v3.replace("temporary fork", "split"))
neg("49financial on pin 2", "IB198-1-AC2", v3=v3.replace("| 49financial | %s" % P1, "| 49financial | %s" % P2))
neg("cottonwood on the closure-fix pin", "IB198-1-AC2", v3=v3.replace("| cottonwood | %s" % P2, "| cottonwood | %s" % P1))
neg("inflection without its total", "IB198-1-AC2", v3=v3.replace("| 841 |\n49financial at pin 2", "| x |\n49financial at pin 2"))
neg("no 119 for 49financial at pin 2", "IB198-1-AC2", v3=v3.replace("119", "many"))
neg("one half signed", "IB198-1-AC2", v3=v3.replace("CTO half UNSIGNED.", "CTO half signed."))
neg("the record reads 49financial 31", "IB198-1-AC2", r196={"firms": {"49financial": firm_rec(31)}})
neg("the record reads cottonwood 485", "IB198-1-AC2", r197={"firms": {"49financial": firm_rec(119), "cottonwood": firm_rec(485), "inflection": firm_rec(841)}})
neg("a long digit run", "IB198-1-AC3", v3=v3 + "\nacct 123456789012\n")
neg("a counter above 0", "IB198-1-AC3", rec={"notes": ["synthetic"], **{k: 0 for k in P6.BOUND}, "aws_writes_made": 1})
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
