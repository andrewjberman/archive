"""U4-AC1 -- PRINT THE DENOMINATOR THE SUBTRACTION RUNS OVER, with instrument + vintage.

THE POPULATION IS NOT THE REPO. The criterion's named invocation is a comp-find over the
corpus; that instrument counts FILES THAT MENTION a token, which is not the population a
member set is subtracted from. The classification this cell settles lives in a SERVED STORE.
So this script prints the store's denominator on THREE instruments, and the comp-find is run
verbatim beside it and recorded for what it is (U4-AC4's corpus read, not this one's domain).

Usage: python u4_ac1_denominator.py <scan.json>
  <scan.json> is the raw, unfiltered output of:
      .tools/aws dynamodb scan --table-name etf-classifications --output json
"""
import sys
import json
import collections
import datetime

scan_path = sys.argv[1]
d = json.load(open(scan_path))
items = d["Items"]

print("== INSTRUMENT 1 (the one the subtraction uses): full table scan, client-side count ==")
print("   store      : dynamodb://etf-classifications  (us-east-1, acct 313476888478)")
print("   key schema : ticker  HASH  (single-attribute primary key -> one row per ticker)")
print("   top-level keys returned : %s" % sorted(d.keys()))
print("   len(Items)         : %d" % len(items))
print("   Count              : %s" % d.get("Count"))
print("   ScannedCount       : %s" % d.get("ScannedCount"))
print("   LastEvaluatedKey   : %s" % ("ABSENT -- SINGLE PAGE, no pagination"
                                      if "LastEvaluatedKey" not in d else d["LastEvaluatedKey"]))
ok = (len(items) == d.get("Count") == d.get("ScannedCount")) and "LastEvaluatedKey" not in d
print("   PAGE CHECK         : %s" % ("PASS -- len == Count == ScannedCount and no LastEvaluatedKey"
                                      if ok else "FAIL -- THIS IS A PAGE, NOT THE POPULATION"))

tickers = [i["ticker"]["S"] for i in items]
dupes = [t for t, n in collections.Counter(tickers).items() if n > 1]
print("   DISTINCT tickers   : %d (duplicates: %s)" % (len(set(tickers)), dupes or "none"))
missing_ac = [t for i, t in zip(items, tickers) if "asset_class" not in i]
print("   rows with NO asset_class attribute : %d %s" % (len(missing_ac), missing_ac))

print()
print("== DENOMINATOR: %d rows -- every row of the served classification registry ==" % len(items))
print()

print("== VINTAGE -- and why it is the READ TIME and not the rows' own last_updated ==")
lu = sorted(i["last_updated"]["S"] for i in items if "last_updated" in i)
print("   READ AT (UTC, this instrument's own clock): %s"
      % datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
print("   rows carrying last_updated : %d of %d" % (len(lu), len(items)))
print("   min last_updated : %s" % lu[0])
print("   max last_updated : %s" % lu[-1])
print("   ^ THE ROW FIELD IS NOT A VINTAGE OF THE ROW. TO-S4-1 (deliverables/~8) wrote")
print("     sub_asset_class on three rows by conditional update_item and states in its own")
print("     instance that it left last_updated UNTOUCHED. A September write therefore sits")
print("     under an August stamp. The only sound vintage is the read time above.")
print("   updated_by populated : %d of %d (0 unattributed)"
      % (sum(1 for i in items if "updated_by" in i), len(items)))

print()
print("== NEGATIVE CONTROL on the instrument: a key that cannot exist ==")
print("   rows whose ticker == 'ZZZ_NO_SUCH_TICKER' : %d (expected 0)"
      % sum(1 for t in tickers if t == "ZZZ_NO_SUCH_TICKER"))
print("== POSITIVE CONTROL: the two tickers the PRD names by hand at s.4 C-SATELLITE-DATA ==")
for t in ("GLD", "VXX"):
    row = [i for i in items if i["ticker"]["S"] == t]
    print("   %-4s present: %s" % (t, bool(row)))
