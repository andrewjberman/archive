"""AMGT_RESAPP round 78 -- AMGT-bb-21, the segment table's period and currency labels, tied to stored revenue.

  python r78_bb21.py --crit AC1|AC2 --where local

The rule (CTO ruling msg 31077): a period column of the stored segment table is labelled with a fiscal year only where the sum
of its level-1 rows equals a stored fiscal year's revenue. The probe of 2026-10-07 measured that tie on AMD (34,639).

AC1 (build) the pure function `lib/research/api/segment_period.py` `label_periods(period_sums, revenue_by_year, currency)`:
  C1 a period whose sum equals a stored year within 0.5 percent is labelled with that year, and the currency is stated;
  C2 a period whose sum equals no stored year is NOT labelled and carries a plain reason (AMD's Period 2: 16,136 against 25,785);
  C3 a period with no sum (no level-1 row present) is not labelled;
  C4 no stored revenue at all labels nothing and says why; no year is ever guessed from a neighbouring column;
  C5 one stored year is never given to two periods;
  C6 no served sentence uses a system word.
AC2 (build, the real neighbour) AMD US from the store: Period 1 of the newest stored segment table that carries revenue rows,
  against the newest stored revenue figures, reads fiscal year 2025 in USD.
Verdict: R78 BB21 <crit> SERVED: YES|NO (exit 0|1). AC2 reads the store; nothing is written.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

WORDS = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
         "input ledger", "bronze")
AMD_REVENUE = {"2025": 34639.0, "2024": 25785.0, "2023": 22680.0}


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _load(results, crit):
    try:
        from lib.research.api import segment_period
        return segment_period
    except Exception as exc:  # noqa: BLE001 -- the build check reports any import failure as its first clause
        results.append(False)
        print("FAIL C0 lib.research.api.segment_period imports %s" % str(exc)[:160])
        print("R78 BB21 %s SERVED: NO" % crit)
        return None


def _clause(results, name, cond, detail=""):
    results.append(bool(cond))
    print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))


def _by_period(out):
    return {p.get("period"): p for p in (out.get("periods") or [])}


def ac1():
    results = []
    sp = _load(results, "AC1")
    if sp is None:
        return 1
    out = sp.label_periods({1: 34639.0, 2: 16136.0, 3: None}, AMD_REVENUE, "USD")
    per = _by_period(out)
    _clause(results, "C1 a period that ties is labelled with its fiscal year and the currency is stated",
            per.get(1, {}).get("fiscal_year") == "2025" and out.get("currency") == "USD", str(per.get(1))[:120])
    _clause(results, "C2 a period that ties to no stored year is not labelled and says why",
            per.get(2, {}).get("fiscal_year") is None and bool(per.get(2, {}).get("reason")), str(per.get(2))[:120])
    _clause(results, "C3 a period with no sum is not labelled", per.get(3, {}).get("fiscal_year") is None, str(per.get(3))[:120])
    none = sp.label_periods({1: 34639.0, 2: 25785.0}, {}, None)
    _clause(results, "C4 with no stored revenue nothing is labelled and the currency is not stated",
            all(p.get("fiscal_year") is None for p in none.get("periods") or [{}]) and none.get("currency") is None
            and bool(none.get("reason")), str(none)[:140])
    twice = sp.label_periods({1: 100.0, 2: 100.2}, {"2025": 100.0}, "EUR")
    labelled = [p for p in twice.get("periods") or [] if p.get("fiscal_year") == "2025"]
    _clause(results, "C5 one stored year is given to one period only", len(labelled) == 1 and labelled[0].get("period") == 1,
            str([(p.get("period"), p.get("fiscal_year")) for p in twice.get("periods") or []]))
    text = json.dumps([out, none, twice]).lower()
    used = [w for w in WORDS if w in text]
    _clause(results, "C6 no served sentence uses a system word", not used, str(used))
    ok = all(results)
    print("R78 BB21 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac2():
    results = []
    sp = _load(results, "AC2")
    if sp is None:
        return 1
    import boto3

    from lib.research.api import scoped_amgt
    from lib.research.harvest import store

    client = boto3.client("s3", region_name="us-east-1")
    keys = sorted(store.fetch_key_exists("bloomberg", "segments", store.entity_partition("security_key", "AMD_US_Equity"),
                                         client=client))
    rows = []
    for key in reversed(keys):
        body = json.loads(client.get_object(Bucket="opal-data-harvest", Key=key)["Body"].read())
        rows = (body.get("response") or {}).get("PG_REVENUE") or []
        if rows:
            break
    sums = {}
    for n in range(1, 6):
        vals = [r.get("Period %d Value" % n) for r in rows if r.get("Product Geographic Hierarchy Level") == 1]
        vals = [v for v in vals if isinstance(v, (int, float)) and abs(v) > 1e-6]
        sums[n] = sum(vals) if vals else None
    block = scoped_amgt._read_model_block_pool("AMD_US_Equity")
    block = block[0] if isinstance(block, tuple) else block
    figures = (block or {}).get("figures") or []
    revenue = {str(f.get("fiscal_year")): f.get("value") for f in figures
               if f.get("scope") == "fiscal_year_line_item" and f.get("mnemonic") == "SALES_REV_TURN" and f.get("value") is not None}
    currency = next((f.get("value") for f in figures if f.get("mnemonic") == "EQY_FUND_CRNCY"), None)
    out = sp.label_periods(sums, revenue, currency)
    p1 = _by_period(out).get(1, {})
    _clause(results, "S1 AMD's Period 1 reads fiscal year 2025 in USD from stored figures",
            p1.get("fiscal_year") == "2025" and out.get("currency") == "USD",
            "sum %s; stored years %d; label %r; currency %r" % (sums.get(1), len(revenue), p1.get("fiscal_year"), out.get("currency")))
    ok = all(results)
    print("R78 BB21 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    sys.path.insert(0, _root())
    return ac1() if a.crit == "AC1" else ac2()


if __name__ == "__main__":
    sys.exit(main())
