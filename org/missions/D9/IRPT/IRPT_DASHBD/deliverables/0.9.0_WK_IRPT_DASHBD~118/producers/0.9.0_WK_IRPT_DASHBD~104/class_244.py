"""TO-DB-b-129: class the 244 UNEXPLAINED segments of the restated tie-out by cause. READ-ONLY on local private evidence; no AWS, no vendor call.
Usage: python -I class_244.py <repo_root>
Writes the counts-only record into the repo deliverables folder; per-segment membership stays here (private, not in the repo).
Rules are applied in this order; the first that holds takes the segment.
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

PRIV = "C:/dev/_irpt_private_evidence_20261009/"
E = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~"
REC = E + "86/RESTATED_TIEOUT.json"
REC_SHA = "1151c54c273d1c5953d275fe700e44b430e7856b6a7e501958d5a05f60e66917"
OUT_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~104/UNEXPLAINED_244.json"


def jload(p):
    return json.loads(Path(p).read_bytes().decode("utf-8"))


def key(x):
    return (x["account"], x["segment"]["start"], x["segment"]["end"])


def main():
    root = Path(sys.argv[1]).resolve()
    raw = Path(REC).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == REC_SHA
    segs = json.loads(raw.decode("utf-8"))["segments"]
    v2 = {key(x): x for x in jload(E + "35/TIEOUT_COMPOUND_V2.json")["segments"]}
    d106 = {key(x): x for x in jload(E + "81/BD_DATES_TWO_SIDED.json")["segments"]}
    assert len(segs) == 990
    U = [(i, r) for i, r in enumerate(segs) if r["reason_after"] == "UNEXPLAINED"]
    assert len(U) == 244, len(U)

    order = ["ZERO_GAIN_BOTH_SIDES_UNDER_ONE_DOLLAR", "NO_BD_TRANSACTION_ROWS_FOR_ACCOUNT", "EVENT_DATE_SETS_DIFFER",
             "EVENT_DATE_SETS_DIFFER_AND_BD_ROW_ABSENT_ON_AN_OPAL_EVENT_DAY", "BD_ROW_ABSENT_ON_AN_OPAL_EVENT_DAY",
             "DATES_AGREE_BD_DAY_COUNT_ONE_MORE_THAN_OPAL", "REMAINDER"]
    members = collections.defaultdict(list)
    for i, r in U:
        k = key(r)
        g = d106.get(k)
        v = v2[k]
        if g is None:
            assert r["reason_before"] == "UNEXPLAINED"
            c = order[0]
        else:
            codes = set(g["codes"])
            if g["verdict"] == "UNEXPLAINED":
                if "NO_BD_TXN_FOR_ACCOUNT" in codes:
                    c = order[1]
                elif "DATE_SETS_DIFFER" in codes and "BD_RECORD_ABSENT_DAY" in codes:
                    c = order[3]
                elif "DATE_SETS_DIFFER" in codes:
                    c = order[2]
                elif "BD_RECORD_ABSENT_DAY" in codes:
                    c = order[4]
                else:
                    c = "OTHER_UNEXPLAINED_CODES"
            else:
                assert g["verdict"] == "confirmed" and not codes
                c = order[5] if v["bd_days_held"] - v["opal_days"] == 1 else order[6]
        members[c].append(i)
    assert set(members) <= set(order), set(members)
    n = {c: len(members[c]) for c in order}
    assert sum(n.values()) == 244, n

    # remainder breakdown (counts only): data present per segment that does NOT name a cause
    rem = [segs[i] for i in members["REMAINDER"]]
    fee = collections.Counter((v2[key(r)]["bd_fees_reported"] or 0) != 0 for r in rem)
    gap = collections.Counter("le_2x_tol" if r["v2_abs_diff_pp"] <= 0.70 else "gt_2x_tol" for r in rem)
    rest = sum(1 for r in rem if r["restated"])
    seg_ids = {c: members[c][0] for c in order if members[c]}

    rules = {
        order[0]: "No row in DB-b-106's 475 (the segment's current reason is UNEXPLAINED, ZERO_GAIN_VENDOR_TWR in ~73 UNEXPLAINED_CLASSIFIED): ~73 evidence reads 'BD netGains and served gain are both under $1 while BD TWR is nonzero'.",
        order[1]: "DB-b-106 verdict UNEXPLAINED with code NO_BD_TXN_FOR_ACCOUNT: Black Diamond's landed transaction record holds no row for the account at all.",
        order[2]: "DB-b-106 verdict UNEXPLAINED with code DATE_SETS_DIFFER and without BD_RECORD_ABSENT_DAY or NO_BD_TXN_FOR_ACCOUNT: the set of Opal event dates (flow or income) and the set of Black Diamond event dates inside the BD record's reach are not equal.",
        order[3]: "DB-b-106 verdict UNEXPLAINED with BOTH codes DATE_SETS_DIFFER and BD_RECORD_ABSENT_DAY: the date sets differ and at least one Opal event day has no Black Diamond row on that day.",
        order[4]: "DB-b-106 verdict UNEXPLAINED with code BD_RECORD_ABSENT_DAY and NO DATE_SETS_DIFFER: every date Black Diamond holds agrees with Opal's, but at least one Opal event day has no Black Diamond row.",
        order[5]: "DB-b-106 verdict confirmed (no code: the event dates agree) AND v2 bd_days_held minus opal_days equals 1: Black Diamond counts one day more than Opal's linked series; the one-day-window test (WINDOW_ONE_DAY_SHIFT) did not close the gap.",
    }
    classes = [{"cause": c, "count": n[c], "rule": rules[c], "example_segment_ref": "row index %d in the private RESTATED_TIEOUT.json segments array (0-based)" % seg_ids[c]}
               for c in order[:6] if n[c]]
    rec = {
        "measured_by": "0.9.0_WK_IRPT_DASHBD~104",
        "task_order": "IRPT_DASHBD.TO-DB-b-129",
        "claim": "inferred",
        "denominator": 244,
        "client_figures": 0,
        "aws_calls": 0,
        "method": {
            "source": "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~86/RESTATED_TIEOUT.json (sha256 %s, the sha256 org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~86/RESTATED_TIEOUT.json records) joined on (account, start, end) to ~35/TIEOUT_COMPOUND_V2.json and ~81/BD_DATES_TWO_SIDED.json" % REC_SHA,
            "how": "READ the per-segment record in place (it exists on this box, outside the repo); counted the segments with reason_after == UNEXPLAINED: 244 of 990 (the repo record's by_reason UNEXPLAINED is 244). Of the 244: 122 carry DB-b-106 verdict UNEXPLAINED, 113 carry verdict confirmed (the ruling-1 refutations), 9 have no DB-b-106 row. None of the 244 is among the 74 restated segments, so none carries a measured convention shift (the CONVENTION count of 9 is a FLOOR, per the CTO's ruling). Each segment takes the first class whose rule holds, in the order listed; the classing script is kept outside the repo at C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~104/class_244.py.",
        },
        "classes": classes,
        "remainder": {
            "count": n["REMAINDER"],
            "why": "DB-b-106 verdict confirmed (every Opal event date appears in Black Diamond's record, so no date difference exists) AND Black Diamond's day count equals Opal's: neither a date difference nor a window-length difference is present in the segment's data, the gap is above 0.35 pp, no convention shift was measured for the segment (restated segments among them: %d), and none of the three records holds a per-segment field that names a cause." % rest,
            "breakdown_counts_only": {"bd_fees_reported_nonzero": fee[True], "bd_fees_reported_zero": fee[False],
                                      "gap_within_2x_tolerance_0.70pp": gap["le_2x_tol"], "gap_above_2x_tolerance": gap["gt_2x_tol"]},
            "next_cell_needs": "The two-sided custodian dollar read the 74 restated segments got (the ~75 W73_S1_EVIDENCE shape: per-segment Black Diamond beginning/ending value, net additions, net gains, fees and income rows against Opal's own side) for these segments: Black Diamond's landed transaction and position rows for the account over the segment window, under the firm's own 49 Financial tree (blackdiamond/49financial/silver_legacy/transactions/ and the positions/valuation tables the tie-out reader ~35 uses). This is an S3 read the present order forbids.",
        },
        "sum_check": {"classes": sum(c["count"] for c in classes), "remainder": n["REMAINDER"], "total": sum(c["count"] for c in classes) + n["REMAINDER"]},
        "convention_floor_note": "CONVENTION = 9 is a FLOOR (74 segments carry a per-segment convention shift; the CTO's round-68 ruling, section 3 row W86-S2).",
    }
    out = root / OUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({"n": n, "remainder_breakdown": rec["remainder"]["breakdown_counts_only"], "sum": rec["sum_check"], "restated_in_remainder": rest}, indent=1))
    # private membership (indices only), kept outside the repo
    Path(E + "104/membership.json").write_bytes((json.dumps({c: members[c] for c in order}) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
