"""T5-AC1 -- derive the retag set BY SUBTRACTION over the whole served registry.

Domain (declared): every row in DynamoDB table etf-classifications at this read's vintage.
Instrument: full scan (Count == ScannedCount, LastEvaluatedKey None -> not a page).
"""
import json
import collections

SCAN = ".scratch/etf_classifications_scan.json"

d = json.load(open(SCAN))
items = d["Items"]
print("DENOMINATOR: %d rows scanned (Count=%s ScannedCount=%s LastEvaluatedKey=%s)"
      % (len(items), d.get("Count"), d.get("ScannedCount"), d.get("LastEvaluatedKey")))


def g(it, k):
    v = it.get(k)
    if v is None:
        return "<ABSENT>"
    return v.get("S", json.dumps(v))


rows = [{"t": g(i, "ticker"), "a": g(i, "asset_class"), "s": g(i, "sub_asset_class"),
         "m": g(i, "management_style")} for i in items]

print("\n== FULL CROSS-TAB: served asset_class x sub_asset_class (denominator %d) ==" % len(rows))
ct = collections.Counter((r["a"], r["s"]) for r in rows)
tot = 0
for (a, s), n in sorted(ct.items()):
    print("  %-14s | %-24s | %3d" % (a, s, n))
    tot += n
print("  SUM OF CELLS: %d (must equal %d)" % (tot, len(rows)))

print("\n== served asset_class VALUE census (the stored vocabulary) ==")
for a, n in sorted(collections.Counter(r["a"] for r in rows).items()):
    print("  %-14s %3d" % (a, n))

# ---- SUBTRACTION -------------------------------------------------------
# Start from the WHOLE table; subtract rows PROVEN not to need a top-level retag.
RATIFIED = {"Fixed Income / Cash", "Equity", "Structured", "Commodities", "Alternatives"}
# The PRD's membership rules that are RATIFIED (C-VOL-HEDGE-STRUCTURED):
#   asset_class=hedge & sub in {Gold, Silver, Oil, Commodities} -> Commodities
#   sub == Volatility                                           -> Structured
COMMODITY_SUBS = {"Gold", "Silver", "Oil", "Commodities"}

survivors = []
sub_legacy_ok = []
sub_vol = []
for r in rows:
    if r["s"] == "Volatility":
        sub_vol.append(r)
        survivors.append((r, "Structured", "sub_asset_class=Volatility -> Structured (C-VOL-HEDGE-STRUCTURED)"))
    elif r["a"] == "hedge" and r["s"] in COMMODITY_SUBS:
        survivors.append((r, "Commodities", "asset_class=hedge & sub=%s -> Commodities (C-VOL-HEDGE-STRUCTURED)" % r["s"]))
    elif r["a"] == "hedge":
        survivors.append((r, "<UNRULED>", "asset_class=hedge but sub=%r is in NEITHER ratified rule" % r["s"]))
    else:
        sub_legacy_ok.append(r)

print("\n== SUBTRACTION ==")
print("  START      : %d rows (the whole table)" % len(rows))
print("  SUBTRACT   : %d rows whose served asset_class is NOT 'hedge' and whose sub_asset_class is NOT 'Volatility'" % len(sub_legacy_ok))
print("               PROOF: no ratified rule in PRD s.4 C-VOL-HEDGE-STRUCTURED moves any such row;")
print("                      C-MEMBERSHIP-AT-L5 reserves every other edge rule to L5 and none is cut.")
print("  ---------------------------------------------")
print("  SURVIVING RETAG SET: %d members" % len(survivors))
for r, tgt, why in sorted(survivors, key=lambda x: x[0]["t"]):
    print("    %-6s served a=%-8s s=%-12s m=%-8s -> TARGET %-12s | %s"
          % (r["t"], r["a"], r["s"], r["m"], tgt, why))

print("\n== CONTROL 1: is the 'hedge' bucket exactly seven? ==")
hedge = [r for r in rows if r["a"] == "hedge"]
print("  hedge rows: %d -> %s" % (len(hedge), sorted(r["t"] for r in hedge)))

print("\n== CONTROL 2: every row whose sub_asset_class is Volatility, at ANY asset_class ==")
for r in sorted(sub_vol, key=lambda r: r["t"]):
    print("  %-6s a=%-8s s=%s" % (r["t"], r["a"], r["s"]))

print("\n== CONTROL 3: rows served 'equity' whose sub_asset_class is a COMMODITY sub ==")
c3 = [r for r in rows if r["a"] != "hedge" and r["s"] in COMMODITY_SUBS]
print("  %d row(s): %s" % (len(c3), sorted(r["t"] for r in c3)))

print("\n== CONTROL 4: rows carrying a BLANK/absent sub_asset_class (the 3 the PRD names) ==")
c4 = [r for r in rows if r["s"] in ("", "<ABSENT>")]
print("  %d row(s): %s" % (len(c4), sorted((r["t"], r["a"], r["s"]) for r in c4)))

print("\n== CONTROL 5: does ANY row already carry a ratified five-class label? ==")
c5 = [r for r in rows if r["a"] in RATIFIED]
print("  %d of %d rows carry a ratified label today" % (len(c5), len(rows)))

print("\n== CONTROL 6: management_style of every retag-set member (the ARMED half of C-RETAG-SAFETY) ==")
for r, tgt, why in sorted(survivors, key=lambda x: x[0]["t"]):
    trip = "TRIP=TRUE (truthy placeholder)" if r["m"] == "unknown" else "trip=false"
    print("  %-6s m=%-10s %s" % (r["t"], r["m"], trip))
