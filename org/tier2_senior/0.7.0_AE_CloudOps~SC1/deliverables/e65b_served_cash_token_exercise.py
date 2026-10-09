"""Exercise cash_token_match() in the SERVED bytes pulled from S3.

Both arms, per the signed halves:
  LANDS   -- a NAME:: key whose name is NOT a whole cash phrase is no longer cash.
  NEGATIVE-- a NAME:: key whose WHOLE name IS a cash phrase is STILL cash;
             real ticker forms (BDCASHIN, FCASH) are unchanged.
Pure function, read-only: no writes, no AWS, no table touch.
"""
import importlib.util
import os
import sys

path = sys.argv[1]
# the served module imports its served siblings from the same prefix
sys.path.insert(0, os.path.dirname(path))
spec = importlib.util.spec_from_file_location("served_etfcs", path)
mod = importlib.util.module_from_spec(spec)
# @dataclass resolves cls.__module__ through sys.modules, so register before exec
sys.modules["served_etfcs"] = mod
spec.loader.exec_module(mod)

ctm = mod.cash_token_match

# (ticker_key, name, expected, arm, why)
CASES = [
    # --- LANDS: the fix. NAME:: key, name not a whole cash phrase -> must be False
    ("NAME::CASHMERE VALLEY BANK", "CASHMERE VALLEY BANK", False, "LANDS",
     "NAME:: key, name not a whole cash phrase"),
    ("NAME::JPMORGAN CASH RESERVES", "JPMORGAN CASH RESERVES", False, "LANDS",
     "NAME:: key, CASH is a word but not the whole phrase"),
    ("NAME::SOME CASH UNIT TRUST", "SOME CASH UNIT TRUST", False, "LANDS",
     "the S63 unit-trust shape"),

    # --- NEGATIVE ARM: must be UNCHANGED (still True)
    ("NAME::CASH", "CASH", True, "NEGATIVE", "NAME:: key whose WHOLE name IS a cash phrase"),
    ("NAME::Cash", "Cash", True, "NEGATIVE", "same, mixed case"),
    ("BDCASHIN", "BD Cash In", True, "NEGATIVE", "real ticker, CASH as a whole token"),
    ("FCASH", "Fidelity Cash", True, "NEGATIVE", "real ticker form named in the halves"),

    # --- controls: must be False either way
    ("CASHMERE", "Cashmere Valley Bank", False, "CONTROL", "CASH + unknown word"),
    ("AAPL", "Apple Inc", False, "CONTROL", "ordinary equity"),
]

print("SERVED-MODULE EXERCISE of cash_token_match()  (file: %s)" % path)
print()
fails = 0
counts = {}
for ticker, name, expected, arm, why in CASES:
    got = ctm(ticker, name)
    ok = (got == expected)
    if not ok:
        fails += 1
    counts[arm] = counts.get(arm, 0) + 1
    print("  %-5s %-9s %-28r name=%-28r -> %-5s expect=%-5s  %s"
          % ("ok" if ok else "FAIL", arm, ticker, name, got, expected, why))

print()
print("denominator: %d case(s) across %d arm(s) %s" % (len(CASES), len(counts), counts))
print("FAILURES: %d" % fails)
print("VERDICT: %s" % ("SERVED BYTES BEHAVE AS THE SIGNED HALVES DESCRIBE"
                       if fails == 0 else "*** SERVED BYTES DIVERGE FROM THE HALVES ***"))
sys.exit(1 if fails else 0)
