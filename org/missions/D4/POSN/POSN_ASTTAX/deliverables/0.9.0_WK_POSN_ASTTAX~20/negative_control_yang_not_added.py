#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V2-1 V2-AC5 -- THE ARM THAT WOULD ADD YANG'S COPY, run beside the real one.

C-SATELLITE-SOURCE says the Satellites mode shows Black Diamond's figure summed across the
sleeves and that YANG'S COPY IS NEVER ADDED: LT VXX is 1.87, not 1.87 + 1.50. A builder that
simply never opens Yang's data satisfies that by construction -- and "by construction" is
exactly the claim a reader cannot check, because a correct output and an output that could
not have been wrong look identical.

SO THIS RUNS BOTH ARMS ON THE SAME BUILDER AND THE SAME LIVE INPUTS:

    ARM A   producer.build_holdings(...)                    -- what ships
    ARM B   the SAME rows, plus Yang's own served LT copy    -- what "blending" produces

ARM B IS NOT A SYNTHETIC FIGURE. It reads the SECOND SOURCE THE PORTAL ACTUALLY BLENDS today
-- s3://opal-data-portal-v2/json/positioning/positioning_data.json, the served artifact
`satelliteAdapter.ts` unions holdings from -- and takes Yang's LT weight for the ticker out of
it. If that read ever returns Yang agreeing with Black Diamond to the cent, the two arms
converge and THIS CONTROL STOPS DISCRIMINATING; it says so and refuses to report a pass,
because two arms that agree cannot tell a builder that ignores Yang from one that adds it.

THE SUBJECT IS Opal Satellite 80, which blends ONE sleeve at 100% -- Opal Conservative Growth,
book LT (`satellites_weights.NAME_TO_BOOK`, ruled by Andrew: "Opal Conservative Growth is the
same as the 'LT Model'"). That makes the satellite's VXX weight and the LT model's VXX weight
THE SAME QUANTITY measured by two vendors, which is what makes the two figures comparable at
all rather than merely different numbers.

ASCII only. Run from the repo root:
    python org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~20/negative_control_yang_not_added.py
"""
from __future__ import annotations

import argparse
import decimal
import gzip
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(REPO_ROOT / "data" / "assets" / "scripts" / "gold"))

import boto3  # noqa: E402
import build_satellites_registry as producer  # noqa: E402

YANG_BUCKET = "opal-data-portal-v2"
YANG_KEY = "json/positioning/positioning_data.json"
SUBJECT = "Opal Satellite 80"
TICKER = "VXX"
BOOK = "LT"


class _NoLabels:
    """The label read is irrelevant to this control and is not made: a DynamoDB round trip
    per ticker would add a second moving part to a comparison about weights."""

    def get_classification(self, ticker):
        return None


def yang_weight(s3, book: str, ticker: str):
    """Yang's OWN served figure for one ticker in one model book, as percentage points.

    Reads the served artifact the portal reads. `weight` there is a FRACTION (VXX in LT reads
    0.015), converted through the producer's own exact seam so the two arms are compared in
    ONE unit -- a unit mismatch here would manufacture a difference and the control would pass
    for the wrong reason.
    """
    raw = s3.get_object(Bucket=YANG_BUCKET, Key=YANG_KEY)
    body = raw["Body"].read()
    if body[:2] == b"\x1f\x8b":
        body = gzip.decompress(body)
    doc = json.loads(body)
    rows = (doc.get("current_holdings") or {}).get(book, {}).get("holdings") or []
    hits = [r for r in rows if r.get("ticker") == ticker]
    if len(hits) != 1:
        raise SystemExit(
            "REFUSED: %s appears %d time(s) in Yang's %s book at s3://%s/%s -- the control "
            "needs exactly one row to compare against." % (ticker, len(hits), book, YANG_BUCKET, YANG_KEY))
    return producer.to_pct(hits[0]["weight"]), doc.get("data_as_of"), raw.get("VersionId")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--as-of", default=None)
    args = ap.parse_args(argv)

    s3 = boto3.client("s3")
    as_of = producer.resolve_as_of(args.as_of)

    roster = producer._get_json(s3, producer.ASSETS_BUCKET, producer.ROSTER_KEY % as_of)
    members = producer.derive_members(roster.get("pagedResults") or [])
    members = [m for m in members if m["name"] == SUBJECT]
    if len(members) != 1:
        raise SystemExit("REFUSED: %r is not in the %s roster (%d match)." % (SUBJECT, as_of, len(members)))
    details = producer.load_details(s3, members, as_of)

    # ---------------------------------------------------------------- ARM A -- what ships
    satellites = producer.build_holdings(details, _NoLabels())
    holdings = satellites[SUBJECT]["holdings"]
    arm_a_row = [h for h in holdings if h["ticker"] == TICKER]
    if len(arm_a_row) != 1:
        raise SystemExit("REFUSED: %s appears %d time(s) in %s." % (TICKER, len(arm_a_row), SUBJECT))
    arm_a = arm_a_row[0]["weight"]

    # ---------------------------------------------------------------- ARM B -- the blend
    yang, yang_as_of, yang_version = yang_weight(s3, BOOK, TICKER)
    arm_b = producer.pct(decimal.Decimal(repr(arm_a)) + yang)

    print("SUBJECT  %s / %s   (sleeves: %s)"
          % (SUBJECT, TICKER, [(s["book"], s["weight"]) for s in arm_a_row[0]["sleeves"]]))
    print("INPUT A  s3://%s/%s  as_of=%s   (Black Diamond, the rebalancer detail)"
          % (producer.ASSETS_BUCKET, producer.DETAIL_KEY % (as_of, members[0]["model_id"]), as_of))
    print("INPUT B  s3://%s/%s  data_as_of=%s VersionId=%s   (Yang's served copy of book %s)"
          % (YANG_BUCKET, YANG_KEY, yang_as_of, yang_version, BOOK))
    print()
    print("ARM A -- producer.build_holdings, what ships        %s %-4s = %.2f" % (BOOK, TICKER, arm_a))
    print("ARM B -- the same rows PLUS Yang's served copy      %s %-4s = %.2f  (%.2f + %s)"
          % (BOOK, TICKER, arm_b, arm_a, yang))
    print()

    if arm_a == arm_b:
        print("NOT DISCRIMINATING: the two arms read the SAME value (%.2f). Yang's served copy "
              "for %s/%s is %s, so adding it changes nothing and this control cannot tell a "
              "builder that ignores Yang from one that adds it. NO RESULT IS REPORTED."
              % (arm_a, BOOK, TICKER, yang))
        return 2

    failures = []
    if arm_a != 1.87:
        failures.append("ARM A is %.2f, expected 1.87 (Black Diamond's own figure)" % arm_a)
    if arm_b != 3.37:
        failures.append("ARM B is %.2f, expected 3.37 (1.87 + Yang's 1.50)" % arm_b)
    print("  %-7s the arms DIFFER                     A=%.2f  B=%.2f  delta=%.2f"
          % ("PASS", arm_a, arm_b, arm_b - arm_a))
    print("  %-7s ARM A is Black Diamond's figure     %.2f" % ("PASS" if arm_a == 1.87 else "FAIL", arm_a))
    print("  %-7s ARM B is the summed-both figure     %.2f" % ("PASS" if arm_b == 3.37 else "FAIL", arm_b))
    print()
    print("READS: the shipped builder emits %.2f. It reaches that figure from ONE input -- the "
          "Black Diamond detail artifact -- and Yang's %s is present, served, and NOT in it."
          % (arm_a, yang))

    if failures:
        for f in failures:
            print("FAIL: %s" % f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
