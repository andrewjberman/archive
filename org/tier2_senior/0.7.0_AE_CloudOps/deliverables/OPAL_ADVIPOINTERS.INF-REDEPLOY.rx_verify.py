#!/usr/bin/env python3
"""RX leg-table verifier -- INF-REDEPLOY.

Asserts each of the eight legs' source-map row carries the PACKAGE-RESOLVED vintage
the face's leg table names. Takes the map path as argv[1] so the same instrument runs
against the real record and against a planted mutant.

Prints the denominator. rc=0 all legs match, rc=1 any mismatch.
"""
import json
import sys

# (leg id, function, vintage the FACE's leg table names, class)
EXPECTED = [
    ("R1", "inf-api-assets-v2",             "927b9cd4f3", "(b) REAL DRIFT"),
    ("R2", "inf-api-txn",                   "67f6a4d7ea", "(b) REAL DRIFT -- D1, single-valued per ruling 88329"),
    ("R3", "inf-unified-account-dim-daily", "bc4759ad00", "(b) REAL DRIFT"),
    ("R4", "inf-tax-daily",                 "444e4f9792", "(b) REAL DRIFT"),
    ("R5", "inf-billing-daily",             "7021cddab0", "(b) REAL DRIFT"),
    ("R6", "inf-performance-daily",         "7021cddab0", "(b) REAL DRIFT"),
    ("R7", "inf-etf-ownership-daily",       "af4f123e2c", "(d) UNDEPLOYED CHANGE -- record was ALREADY correct"),
    ("R8", "inf-portal-advisor-publisher",  "c42c5e6ed0", "(b) on a SINGLE UNCONTROLLED comparison"),
]

FALSE_SWEEP = "46d0b98aef"  # the 2026-06-11 provenance-sweep value, false on six rows


def main() -> int:
    path = sys.argv[1]
    fns = json.load(open(path, encoding="utf-8"))["functions"]
    ok = 0
    fails = []
    for leg, fn, want, klass in EXPECTED:
        row = fns.get(fn)
        if row is None:
            fails.append(f"{leg} {fn}: ROW ABSENT")
            continue
        got = str(row.get("last_deployed_commit") or "")
        if got.startswith(want):
            ok += 1
            print(f"OK:    {leg} {fn:<32} {got[:10]}  {klass}")
        else:
            fails.append(f"{leg} {fn}: recorded {got[:10]}, face names {want}")
            print(f"ERROR: {leg} {fn:<32} {got[:10]} != {want}")

    # Negative control: the false sweep value must survive on NO leg.
    residual = [fn for _, fn, _, _ in EXPECTED
                if str(fns.get(fn, {}).get("last_deployed_commit") or "").startswith(FALSE_SWEEP)]
    print(f"\nDENOMINATOR: {ok} of {len(EXPECTED)} legs match the face; "
          f"{len(fns)} rows in the map total.")
    print(f"NEGATIVE CONTROL: legs still carrying the false sweep value {FALSE_SWEEP}: "
          f"{len(residual)} {residual}")

    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
