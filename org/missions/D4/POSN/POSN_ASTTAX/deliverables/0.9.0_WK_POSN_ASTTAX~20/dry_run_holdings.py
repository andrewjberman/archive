#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V2-1 V2-AC4 -- the holdings artifact EXERCISED LOCALLY, before any deploy.

Runs the REAL builder (data/assets/scripts/gold/build_satellites_registry.py, the same
functions the Lambda calls) against the LIVE bronze partition and the LIVE served
etf-classifications table, and WRITES NOTHING. Every assertion below is a clause of V2-AC4
and each one prints its own measured value beside the expectation, so a failure names the
figure rather than just failing.

THE LABEL CHECK USES A SECOND INSTRUMENT ON PURPOSE. The builder reads the table through
`boto3.resource("dynamodb").Table(...).get_item` (the shared ETFClassifier); this script
re-reads every labelled ticker through the LOW-LEVEL `boto3.client("dynamodb").get_item`
and compares. Re-running the builder's own read would be repetition, not corroboration --
it would agree with itself about a wrong table name, a wrong region or a stale cache.

The MEMORY/TIMEOUT re-measure the cell requires (the .tf comment forbids inherited numbers)
is the wall clock and tracemalloc peak printed at the foot.

ASCII only. Run from the repo root:
    python org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~20/dry_run_holdings.py
    [--as-of YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import decimal
import json
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(REPO_ROOT / "data" / "assets" / "scripts" / "gold"))

import boto3  # noqa: E402
import build_satellites_registry as producer  # noqa: E402

FAILURES: list[str] = []


def check(label: str, got, want) -> None:
    ok = got == want
    print("  %-7s %-58s got=%r want=%r" % ("PASS" if ok else "FAIL", label, got, want))
    if not ok:
        FAILURES.append("%s: got=%r want=%r" % (label, got, want))


def row(satellites: dict, code: str, ticker: str) -> dict:
    hits = [h for h in satellites[code]["holdings"] if h["ticker"] == ticker]
    if len(hits) != 1:
        FAILURES.append("%s / %s: %d row(s), expected exactly 1" % (code, ticker, len(hits)))
        return {}
    return hits[0]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--as-of", default=None)
    args = ap.parse_args(argv)

    tracemalloc.start()
    t0 = time.time()

    s3 = boto3.client("s3")
    as_of = producer.resolve_as_of(args.as_of)
    print("OK: as_of=%s   roster=s3://%s/%s"
          % (as_of, producer.ASSETS_BUCKET, producer.ROSTER_KEY % as_of))

    roster = producer._get_json(s3, producer.ASSETS_BUCKET, producer.ROSTER_KEY % as_of)
    rows = roster.get("pagedResults") or []
    members = producer.derive_members(rows)
    print("OK: %d member(s) derived of %d roster row(s)   <- DENOMINATOR"
          % (len(members), len(rows)))

    details = producer.load_details(s3, members, as_of)
    classifier = producer.load_classifier()
    satellites = producer.build_holdings(details, classifier)

    wall = time.time() - t0
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n" + producer.format_coverage(satellites))

    print("\nTHE PAYLOAD AS IT WOULD BE PUBLISHED (nothing is written by this script):")
    block = producer.build_holdings_payload(satellites, as_of)
    body = json.dumps(block, indent=2, sort_keys=False).encode("utf-8")
    print("  s3://%s/%s  %d bytes  %d satellite(s)"
          % (producer.REGISTRY_BUCKET, producer.HOLDINGS_KEY, len(body), len(block["satellites"])))
    print("  top-level keys: %s" % (sorted(block),))

    print("\nV2-AC4 CLAUSES")
    check("nine satellites", len(satellites), 9)

    gld15 = row(satellites, "Opal Satellite 15", "GLD")
    check("Sat 15 GLD weight", gld15.get("weight"), 8.34)
    check("Sat 15 GLD sleeves", gld15.get("sleeves"), [{"book": "ST", "weight": 8.34}])

    gld30 = row(satellites, "Opal Satellite 30", "GLD")
    check("Sat 30 GLD weight", gld30.get("weight"), 7.25)
    check("Sat 30 GLD sleeves",
          sorted((s["book"], s["weight"]) for s in gld30.get("sleeves", [])),
          [("INT", 1.0), ("ST", 6.26)])

    # EVERY TICKER ONCE PER SATELLITE -- asserted over the whole set, denominator printed.
    dupes = []
    total_rows = 0
    for code in sorted(satellites):
        tickers = [h["ticker"] for h in satellites[code]["holdings"]]
        total_rows += len(tickers)
        if len(tickers) != len(set(tickers)):
            dupes.append(code)
    check("no ticker twice in a satellite (over %d rows / 9 satellites)" % total_rows,
          dupes, [])

    # coverage.labelled + coverage.unlabelled == the row count, PER SATELLITE.
    bad = [code for code in satellites
           if satellites[code]["coverage"]["labelled"] + satellites[code]["coverage"]["unlabelled"]
           != len(satellites[code]["holdings"])]
    check("coverage sums to the row count on all 9", bad, [])

    # ---------------------------------------------------------------- labels, 2nd instrument
    print("\nLABELS RE-READ ON A SECOND INSTRUMENT (low-level dynamodb client vs the "
          "builder's resource-level ETFClassifier)")
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    served: dict[str, tuple] = {}
    distinct = sorted({h["ticker"] for code in satellites for h in satellites[code]["holdings"]})
    for ticker in distinct:
        item = ddb.get_item(TableName=producer.CLASSIFICATIONS_TABLE,
                            Key={"ticker": {"S": ticker}}).get("Item")
        if not item:
            served[ticker] = (None, None)
        else:
            ac = item.get("asset_class", {}).get("S")
            sac = item.get("sub_asset_class", {}).get("S")
            served[ticker] = (ac, sac)
    mism = []
    for code in sorted(satellites):
        for h in satellites[code]["holdings"]:
            if (h["asset_class"], h["sub_asset_class"]) != served[h["ticker"]]:
                mism.append((code, h["ticker"], (h["asset_class"], h["sub_asset_class"]),
                             served[h["ticker"]]))
    check("every label equals the table's CURRENT served value (%d distinct tickers)"
          % len(distinct), mism, [])
    print("  distinct tickers: %d   served-with-a-class: %d   NOT in the table: %d"
          % (len(distinct),
             sum(1 for t in distinct if served[t][0] is not None),
             sum(1 for t in distinct if served[t][0] is None)))
    print("  unlabelled tickers: %s"
          % ([t for t in distinct if served[t][0] is None],))
    for t in ("GLD", "VXX"):
        if t in served:
            print("  %-5s served now: asset_class=%r sub_asset_class=%r"
                  % (t, served[t][0], served[t][1]))

    # ---------------------------------------------------------------- the exact sums
    print("\nEXACT PER-SATELLITE SUM OF absoluteAllocation (a disclosure, not a gate --"
          " the published weights are quantized at 2 dp and a 20+ row set drifts by up to"
          " half a cent per row)")
    for code in sorted(details):
        exact = sum((producer.to_pct(c.get("absoluteAllocation"))
                     for sleeve in (details[code]["hierarchy"].get("children") or [])
                     for c in producer._components_of(sleeve)), decimal.Decimal(0))
        printed = sum(decimal.Decimal(repr(h["weight"])) for h in satellites[code]["holdings"])
        print("  %-20s exact=%s   sum of published 2dp weights=%s" % (code, exact, printed))

    # ---------------------------------------------------------------- the unlabelled arm
    # THE LIVE TABLE LABELS 25 OF 25 TODAY, so the `asset_class: null` + coverage.unlabelled
    # path is NOT exercised by the run above -- and an unexercised branch that only ever
    # reports zero is indistinguishable from one that cannot fire. This arm WITHHOLDS one
    # ticker at the classifier, which is exactly what the module does on a table miss
    # (get_classification returns None), and reads the difference.
    print("\nUNLABELLED-PATH CONTROL (one ticker withheld at the classifier -- the same"
          " None the real client returns on a table miss)")

    class _WithholdOne:
        def __init__(self, inner, ticker):
            self.inner = inner
            self.ticker = ticker

        def get_classification(self, ticker):
            return None if ticker == self.ticker else self.inner.get_classification(ticker)

    probe = producer.build_holdings({"Opal Satellite 15": details["Opal Satellite 15"]},
                                    _WithholdOne(classifier, "GLD"))
    probe_row = [h for h in probe["Opal Satellite 15"]["holdings"] if h["ticker"] == "GLD"][0]
    base_cov = satellites["Opal Satellite 15"]["coverage"]
    probe_cov = probe["Opal Satellite 15"]["coverage"]
    print("  withheld GLD -> row: %s" % json.dumps(probe_row))
    print("  coverage      live %r  ->  withheld %r" % (base_cov, probe_cov))
    check("withheld ticker carries null/null",
          (probe_row["asset_class"], probe_row["sub_asset_class"]), (None, None))
    check("withheld ticker is COUNTED, not dropped",
          (probe_cov["labelled"], probe_cov["unlabelled"], len(probe["Opal Satellite 15"]["holdings"])),
          (base_cov["labelled"] - 1, base_cov["unlabelled"] + 1,
           len(satellites["Opal Satellite 15"]["holdings"])))
    check("withheld ticker keeps its WEIGHT", probe_row["weight"],
          row(satellites, "Opal Satellite 15", "GLD")["weight"])

    print("\nRUNTIME MEASUREMENT for the .tf memory_size / timeout (never inherited)")
    print("  wall                %.2f s   (%d S3 GETs + %d DynamoDB GetItems, all sequential)"
          % (wall, 1 + len(members), len(distinct)))
    print("  traced allocation   %.2f MiB peak (python objects; the interpreter and boto3"
          " baseline are NOT in tracemalloc)" % (peak / 1048576.0))
    print("  current at exit     %.2f MiB" % (cur / 1048576.0))

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
                          capture_output=True, text=True)
    print("\nVINTAGE: worktree HEAD %s   builder %s"
          % (head.stdout.strip(), producer.__file__))

    if FAILURES:
        print("\nFAIL: %d clause(s)" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        return 1
    print("\nOK: every V2-AC4 clause passed on the live partition.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
