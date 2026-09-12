#!/usr/bin/env python3
"""IB-rt-11 mutant control -- a passing assertion never mutated has never been tested.

    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/
        IB-rt-11_mutant_control.py

TWO CLAIMS, EACH MUTATED BY MONKEYPATCH IN A PROCESS THAT EDITS NO PRODUCTION FILE. The
specific risk this addresses is that a parser's controls, written by the parser's author, agree
with the parser: an arm that would pass whether or not the mechanism worked is a decoration.

  M1  AGAINST "never infer a currency from a symbol". `determine_currency` is replaced by one
      that reads a `$` as USD -- the single most natural wrong thing to do, and what almost
      every spreadsheet tool does. The multi-sheet specimen's AMBIGUOUS_CURRENCY quarantine
      must BREAK, and the money rows must start claiming a USD unit they cannot justify.

  M2  AGAINST "a subtotal is never summed". `_is_subtotal_label` is replaced by one that always
      returns False -- round 1's behaviour. The subtotal specimen's computed total must
      double-count its groups, and the ROW-COUNT reconciliation must still balance, which is the
      point: the count leg cannot see it.

Prints a JSON record. Exit 0 only when BOTH mutants FIRE.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                      text=True, check=True).stdout.strip()
INTAKE = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "intake")
FIX = os.path.join(INTAKE, "fixtures", "holdings")
sys.path.insert(0, INTAKE)
import parse  # noqa: E402

MAPPING = parse.load_mapping(os.path.join(FIX, "security_mapping.json"))


def run(name, **kw):
    with open(os.path.join(FIX, name), "rb") as fh:
        data = fh.read()
    return parse.parse_holdings(data, name, "att", mapping=MAPPING, **kw)


def predicate_m1(result):
    """Arm (a)'s claim: every money row on this specimen is AMBIGUOUS and claims no unit."""
    return (bool(result.money_rows)
            and all(m["state"] == "AMBIGUOUS" for m in result.money_rows)
            and all(h["quantity"]["units"] is None for h in result.normalized_holdings))


def predicate_m2(result):
    """Arm (a)'s claim: the subtotal is excluded, so the computed total equals the stated one."""
    return (result.totals["computed"].get("USD") == 700000.0
            and result.totals.get("matches") is True)


def main():
    out = {"cell": "IB-rt-11", "mutants": {}}

    base_m1 = run("holdings_multi_sheet.xlsx")
    out["mutants"]["M1_infer_currency_from_a_symbol"] = {
        "claim": "never infer a currency from a symbol -- a bare $ is USD, CAD, AUD, NZD, HKD, "
                 "SGD, MXN and more, so it establishes nothing",
        "baseline_predicate_holds": predicate_m1(base_m1),
        "baseline_states": sorted({m["state"] for m in base_m1.money_rows}),
    }
    real_determine = parse.determine_currency

    def mutant_determine(signals, controls):
        for s in signals:
            for sym in s.get("symbols", []):
                candidates = controls["ambiguous_symbols"].get(sym, [])
                if candidates:
                    return {"state": "ESTABLISHED", "currency": candidates[0],
                            "candidates": candidates, "evidence": signals,
                            "why": "MUTANT: read the symbol as its first candidate"}
        return real_determine(signals, controls)

    parse.determine_currency = mutant_determine
    try:
        mutated_m1 = run("holdings_multi_sheet.xlsx")
        out["mutants"]["M1_infer_currency_from_a_symbol"].update(
            mutated_predicate_holds=predicate_m1(mutated_m1),
            mutated_states=sorted({m["state"] for m in mutated_m1.money_rows}),
            mutated_units=sorted({str(h["quantity"]["units"])
                                  for h in mutated_m1.normalized_holdings}),
            mutated_findings=sorted({f["code"] for f in mutated_m1.findings}))
    finally:
        parse.determine_currency = real_determine

    base_m2 = run("holdings_subtotals.csv")
    out["mutants"]["M2_a_subtotal_is_a_holding"] = {
        "claim": "a subtotal row is excluded from the computed total; including it counts its "
                 "group twice",
        "baseline_predicate_holds": predicate_m2(base_m2),
        "baseline_computed": base_m2.totals["computed"],
    }
    real_is_subtotal = parse._is_subtotal_label
    parse._is_subtotal_label = lambda text: False
    try:
        mutated_m2 = run("holdings_subtotals.csv")
        out["mutants"]["M2_a_subtotal_is_a_holding"].update(
            mutated_predicate_holds=predicate_m2(mutated_m2),
            mutated_computed=mutated_m2.totals["computed"],
            mutated_row_count_still_balances=mutated_m2.reconcile()["balances"])
    finally:
        parse._is_subtotal_label = real_is_subtotal

    # DETERMINISM: the same bytes twice, in this process and again in a fresh one.
    a = run("holdings_non_usd.csv").digest()
    b = run("holdings_non_usd.csv").digest()
    prog = ("import sys, os\nsys.path.insert(0, %r)\nimport parse\n"
            "m = parse.load_mapping(os.path.join(%r, 'security_mapping.json'))\n"
            "d = open(os.path.join(%r, 'holdings_non_usd.csv'), 'rb').read()\n"
            "print(parse.parse_holdings(d, 'holdings_non_usd.csv', 'att', mapping=m).digest())\n"
            ) % (INTAKE, FIX, FIX)
    fresh = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True,
                           cwd=REPO).stdout.strip()
    out["determinism"] = {"in_process_run_1": a[:16], "in_process_run_2": b[:16],
                          "fresh_interpreter": fresh[:16],
                          "stable": a == b == fresh}

    m1 = out["mutants"]["M1_infer_currency_from_a_symbol"]
    m2 = out["mutants"]["M2_a_subtotal_is_a_holding"]
    fired = (m1["baseline_predicate_holds"] and not m1["mutated_predicate_holds"]
             and m2["baseline_predicate_holds"] and not m2["mutated_predicate_holds"])
    out["status"] = "FIRED-AS-EXPECTED" if fired else "DID-NOT-FIRE (deliverable INVALID)"
    out["determinism_status"] = "STABLE" if out["determinism"]["stable"] else "UNSTABLE"
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if fired and out["determinism"]["stable"] else 1


if __name__ == "__main__":
    sys.exit(main())
