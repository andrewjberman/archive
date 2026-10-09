"""DB8-1-AC2 -- CTO batch 193: the equity basis re-measured over ALL 14 like-day pairs, the population figure and the guard; S22
re-read; no vendor call.

Reads two records in deliverables/0.9.0_WK_IRPT_DASHBD~2/:
  TIEOUT_49F_BLACKDIAMOND_R8.json
    {"tolerance": 0.0035, "vendor_calls": 0, "method_version": <int > 1>,
     "pairs": [{"account", "start", "end", "abs_diff_r4", "abs_diff_now", "bd_accrual", "within": bool, "reason"}],
     "s22": {"account": "acct#89d0916a", "start": "2026-06-25", "residual": <number>, "disposition": "DISARMED" | "RESTATED",
             "reason"}}
  POPULATION_EQUITY_R8.json
    {"day": "2026-10-01", "accounts": 7570, "positive_before": 6685, "positive_after": <int>,
     "guard_state_before": {state: count}, "guard_state_after": {state: count},
     "zero_margin_accounts": <int > 0>, "zero_margin_rows_changed": 0, "null_margin_balance_rows": <int>}
Grades:
  - tolerance 0.0035; vendor_calls 0; method_version an int above 1;
  - the pairs are exactly round 4's 14, keyed (account, start) from deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.json;
  - every pair has numeric abs_diff_now and bd_accrual, and within == (abs_diff_now <= 0.0035);
  - every pair not within carries a non-empty reason;
  - s22 names the acct#89d0916a 2026-06-25 pair, its residual equals that pair's abs_diff_now, its disposition is DISARMED exactly
    when the residual is within the tolerance and RESTATED otherwise, and a RESTATED disposition carries a reason;
  - the population record: day 2026-10-01, accounts 7570, positive_before 6685, positive_after an int; both guard_state maps
    are non-empty and sum to the same row count; zero_margin_accounts above 0; zero_margin_rows_changed 0;
    null_margin_balance_rows declared as an int.
Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R8 = D + "0.9.0_WK_IRPT_DASHBD~2/TIEOUT_49F_BLACKDIAMOND_R8.json"
POP = D + "0.9.0_WK_IRPT_DASHBD~2/POPULATION_EQUITY_R8.json"
R4 = D + "0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.json"
TOL = 0.0035
def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


S22 = (_REAL("acct#89d0916a"), "2026-06-25")


def fail(msg):
    print("FAIL: " + msg)
    print("DB8-1-AC2 FAIL")
    sys.exit(1)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    for rel in (R8, POP, R4):
        if not (root / rel).is_file():
            fail("no record at %s" % rel)
    r = json.loads((root / R8).read_text(encoding="utf-8"))
    pop = json.loads((root / POP).read_text(encoding="utf-8"))
    r4 = json.loads((root / R4).read_text(encoding="utf-8"))
    if r.get("tolerance") != TOL:
        fail("tolerance is %r, not 0.0035" % r.get("tolerance"))
    if r.get("vendor_calls") != 0:
        fail("vendor_calls is %r, not 0" % r.get("vendor_calls"))
    mv = r.get("method_version")
    if not isinstance(mv, int) or isinstance(mv, bool) or mv <= 1:
        fail("method_version is %r, not an int above 1" % mv)
    want = {(p["account"], p["start"]) for p in r4["pairs"]}
    pairs = r.get("pairs") or []
    got = {(p.get("account"), p.get("start")) for p in pairs}
    if len(want) != 14 or got != want or len(pairs) != 14:
        fail("the pairs are not round 4's 14: missing %s, extra %s" % (sorted(want - got), sorted(got - want)))
    by = {}
    for p in pairs:
        k = (p["account"], p["start"])
        d, acc = num(p.get("abs_diff_now")), num(p.get("bd_accrual"))
        if d is None or acc is None:
            fail("%s %s lacks a numeric abs_diff_now or bd_accrual" % k)
        if p.get("within") is not (d <= TOL):
            fail("%s %s: within is %r but abs_diff_now is %s" % (k[0], k[1], p.get("within"), d))
        if not p["within"] and not str(p.get("reason") or "").strip():
            fail("%s %s is beyond the tolerance with no reason" % k)
        by[k] = d
    s = r.get("s22") or {}
    if (s.get("account"), s.get("start")) != S22:
        fail("s22 does not name the acct#89d0916a 2026-06-25 pair")
    res = num(s.get("residual"))
    if res is None or abs(res - by[S22]) > 1e-12:
        fail("s22 residual %r is not that pair's abs_diff_now %r" % (s.get("residual"), by[S22]))
    expect = "DISARMED" if res <= TOL else "RESTATED"
    if s.get("disposition") != expect:
        fail("s22 disposition is %r; residual %s calls for %s" % (s.get("disposition"), res, expect))
    if expect == "RESTATED" and not str(s.get("reason") or "").strip():
        fail("s22 is RESTATED with no reason")
    if pop.get("day") != "2026-10-01" or pop.get("accounts") != 7570 or pop.get("positive_before") != 6685:
        fail("population record day/accounts/positive_before are %r/%r/%r" % (pop.get("day"), pop.get("accounts"),
                                                                              pop.get("positive_before")))
    if not isinstance(pop.get("positive_after"), int):
        fail("positive_after is not an int")
    gb, ga = pop.get("guard_state_before") or {}, pop.get("guard_state_after") or {}
    if not gb or not ga or sum(gb.values()) != sum(ga.values()):
        fail("guard_state maps are empty or count different rows: %s vs %s" % (gb, ga))
    if not isinstance(pop.get("zero_margin_accounts"), int) or pop["zero_margin_accounts"] <= 0:
        fail("zero_margin_accounts is %r" % pop.get("zero_margin_accounts"))
    if pop.get("zero_margin_rows_changed") != 0:
        fail("zero_margin_rows_changed is %r, not 0: the one rule moved an account with no margin"
             % pop.get("zero_margin_rows_changed"))
    if not isinstance(pop.get("null_margin_balance_rows"), int):
        fail("null_margin_balance_rows is not declared as an int")
    beyond = sorted(k for k, d in by.items() if d > TOL)
    print("OK: 14 of 14 pairs at method_version %d; %d beyond 0.35 pp %s; s22 %s at %.6f; population positive %d -> %d; "
          "guard rows %d; zero-margin accounts %d unchanged" % (mv, len(beyond), beyond, expect, res, pop["positive_before"],
                                                                pop["positive_after"], sum(ga.values()),
                                                                pop["zero_margin_accounts"]))
    print("DB8-1-AC2 PASS")


if __name__ == "__main__":
    main()
