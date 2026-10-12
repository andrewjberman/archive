"""IRPT_BCKEND round 164 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msgs 6414, 6420;
PRD v0.48 C-CHAINCLAIM): the read before the cell.
  IB164-1  IB-pr-470  the closed status set with counts; the NON-POSITIVE-BASE days by whether the account held any position
                      the prior day; the producer's assignment order; the accounts whose claim moves.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB164-1-AC1  the status tokens the producer can write, each with a cite that exists; per entry the count of each token over
               the served gold summing to the rows read; tokens met in the gold and not in the code listed.
  IB164-1-AC2  per entry and window the interior NON-POSITIVE-BASE days reproduce IB-pr-467's, and every NON-POSITIVE-BASE
               day is placed by whether the account held a position row the prior day, summing with no remainder.
  IB164-1-AC3  the assignment order with its verdict and lines; the accounts whose claim moves per entry and window under
               both readings; the bounds.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~325/"
OUT, READ = D + "IB164-1_status_set_and_base.json", D + "IB164-1_STATUS_SET_AND_BASE_READ.md"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~322/IB161-1_excluded_day_base.json"
HELD = ("held_none", "held_included_only_or_mixed", "held_only_excluded", "held_only_negative", "held_other", "not_determinable")
NPB = "NON-POSITIVE-BASE"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB164"))
        sys.exit(1)

    def cite_ok(c):
        m = re.match(r"^(.+?):(\d+)", str(c))
        if not m or not (root / m.group(1)).is_file():
            return False
        return int(m.group(2)) <= len((root / m.group(1)).read_text(encoding="utf-8", errors="replace").splitlines())

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    cells = a.get("per_entry_and_window")
    if cid == "IB164-1-AC1":
        code = a.get("status_tokens_in_code")
        if not isinstance(code, list) or not code:
            fail("status_tokens_in_code is empty")
        for t in code:
            if not t.get("token") or not cite_ok(t.get("defined_at")) or not cite_ok(t.get("assigned_at")) or not t.get("condition_in_words"):
                fail("each token: token, defined_at and assigned_at that exist, condition_in_words (%r)" % (t.get("token"),))
        names = {t["token"] for t in code}
        g = a.get("status_counts_over_the_served_gold")
        if not isinstance(g, dict) or len(g) != 2:
            fail("status_counts_over_the_served_gold must carry the two entries")
        for e, v in g.items():
            if not isinstance(v.get("by_token"), dict) or sum(v["by_token"].values()) != v.get("rows_read") or not isinstance(v.get("partitions_read"), int):
                fail("%s: by_token must sum to rows_read, with partitions_read" % e)
            extra = sorted(set(v["by_token"]) - names)
            if extra != sorted(v.get("tokens_in_the_gold_not_in_the_code", [])):
                fail("%s: tokens_in_the_gold_not_in_the_code must list exactly %s" % (e, extra))
        print("OK: %d token(s) in code; " % len(code) + "; ".join("%s: %d rows over %d partitions" % (e, v["rows_read"], v["partitions_read"]) for e, v in g.items()))
    elif cid == "IB164-1-AC2":
        if not isinstance(cells, list) or not cells:
            fail("per_entry_and_window is empty")
        prior = {(c["entry"], c["window"]): c for c in json.loads((root / PRIOR).read_text(encoding="utf-8"))["per_entry_and_window"]}
        if {(c.get("entry"), c.get("window")) for c in cells} != set(prior):
            fail("the cells must be IB-pr-467's eight entry-window pairs")
        for c in cells:
            k = (c["entry"], c["window"])
            want = sum((prior[k]["interior_by_status_and_prior_value"].get(NPB) or {}).values())
            n = c.get("non_positive_base_days")
            if not isinstance(n, dict) or n.get("interior") != want:
                fail("%s/%s: interior NON-POSITIVE-BASE days %r, IB-pr-467 read %d" % (k[0], k[1], (n or {}).get("interior"), want))
            for part in ("interior", "all_positions"):
                h = c.get("non_positive_base_%s_by_prior_day_holdings" % part)
                if not isinstance(h, dict) or set(h) != set(HELD) or sum(h.values()) != n.get(part):
                    fail("%s/%s: the %s table must carry exactly %s and sum to its days" % (k[0], k[1], part, HELD))
        if not a.get("prior_day_holdings_rule_in_words"):
            fail("prior_day_holdings_rule_in_words")
        print("OK: 8 cells reproduce IB-pr-467's interior NON-POSITIVE-BASE days; " + "; ".join("%s %s: %d of %d held a position" % (c["entry"], c["window"], c["non_positive_base_days"]["interior"] - c["non_positive_base_interior_by_prior_day_holdings"]["held_none"] - c["non_positive_base_interior_by_prior_day_holdings"]["not_determinable"], c["non_positive_base_days"]["interior"]) for c in cells))
    elif cid == "IB164-1-AC3":
        o = a.get("assignment_order")
        if not isinstance(o, dict) or o.get("only_excluded_holdings_can_be_stamped_non_positive_base") not in ("YES", "NO") or not o.get("in_words") or not all(cite_ok(c) for c in (o.get("cites") or [None])):
            fail("assignment_order {only_excluded_holdings_can_be_stamped_non_positive_base YES|NO, in_words, cites that exist}")
        for c in cells or [None]:
            m = (c or {}).get("accounts_whose_claim_moves")
            if not isinstance(m, dict) or not all(isinstance(m.get(x), int) for x in ("accounts_with_a_figure_saying_measured", "under_the_contract_as_written", "if_non_positive_base_with_a_prior_position_also_moves")):
                fail("accounts_whose_claim_moves needs its three integers in every cell")
            if not m["under_the_contract_as_written"] <= m["if_non_positive_base_with_a_prior_position_also_moves"] <= m["accounts_with_a_figure_saying_measured"]:
                fail("%s/%s: the claim-move counts are not ordered" % (c["entry"], c["window"]))
        for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "values_written", "product_files_edited"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not (a.get("control") or {}).get("what") or not (root / READ).is_file() or not a.get("base_commit"):
            fail("not_established, a control, base_commit and the read file")
        print("OK: order verdict %s; claim moves counted in %d cells; nothing invoked, no account and no value written" % (o["only_excluded_holdings_can_be_stamped_non_positive_base"], len(cells)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
