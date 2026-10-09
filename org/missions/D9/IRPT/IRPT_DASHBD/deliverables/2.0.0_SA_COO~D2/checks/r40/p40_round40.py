"""IRPT_DASHBD round 40 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-39 ADDENDUM 8 (CVO slug msg 2951). RULING W53-S2: the inferred
billing flag is ACCEPTED, and a consumer must show its basis. The supervised and billed slices read `inferred: from fee amount and schedule`;
wherever Orion's IncludedInBilling is readable for an account it wins and that account reads `measured` (a value carries its claim).

Cell: DB-b-83, the fee slices re-printed with a per-account basis. E1 (the 11:41Z fire's A1-A7 and REPORT duration) is the issuer's read.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB40-1-AC1  ~60/INF_FEE_SLICES_R40.json: billed and unbilled each carry basis_counts {measured int, inferred int} summing to their
              denominator, and a basis string that contains "inferred: from fee amount and schedule" whenever inferred > 0 and "measured"
              whenever measured > 0; orion_overrides is an int >= 0 (accounts where Orion's readable flag changed the inferred state).
  DB40-1-AC2  supervised and unsupervised each carry a basis string containing "inferred" (the managed flag is not an Orion supervision
              field), and every slice row carries value, readable, denominator and status, with status "PARTIAL" iff readable < denominator.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~60/INF_FEE_SLICES_R40.json"
INF = "inferred: from fee amount and schedule"
ALL = ["supervised", "unsupervised", "supervision_total", "billed", "unbilled", "billing_total"]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB40"))
        sys.exit(1)

    p = root / D
    if not p.is_file():
        fail("no %s" % D)
    r = json.loads(p.read_bytes().decode("utf-8"))
    sl = r.get("slices") or {}
    if cid == "DB40-1-AC1":
        for k in ("billed", "unbilled"):
            x = sl.get(k) or {}
            bc = x.get("basis_counts") or {}
            m, i, n = bc.get("measured"), bc.get("inferred"), x.get("denominator")
            if not isinstance(m, int) or not isinstance(i, int) or not isinstance(n, int) or m + i != n:
                fail("%s basis_counts %r vs denominator %r" % (k, bc, n))
            b = str(x.get("basis") or "")
            if (i > 0 and INF not in b) or (m > 0 and "measured" not in b):
                fail("%s basis %r does not state its claim (measured %d, inferred %d)" % (k, b, m, i))
        if not isinstance(r.get("orion_overrides"), int) or r["orion_overrides"] < 0:
            fail("orion_overrides %r" % r.get("orion_overrides"))
        b = sl["billed"]["basis_counts"]
        print("OK: billed/unbilled basis stated: %d measured, %d inferred; Orion overrode %d" % (b["measured"], b["inferred"], r["orion_overrides"]))
    elif cid == "DB40-1-AC2":
        for k in ("supervised", "unsupervised"):
            if "inferred" not in str((sl.get(k) or {}).get("basis") or ""):
                fail("%s basis %r must state inferred" % (k, (sl.get(k) or {}).get("basis")))
        bad = []
        for k in ALL:
            x = sl.get(k) or {}
            if not num(x.get("value")) or not isinstance(x.get("readable"), int) or not isinstance(x.get("denominator"), int) \
                    or x.get("status") != ("PARTIAL" if x["readable"] < x["denominator"] else "COMPLETE"):
                bad.append(k)
        if bad:
            fail("slices without value/readable/denominator/status by rule: %r" % bad)
        print("OK: supervision slices state inferred; 6 slices carry status by rule")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
