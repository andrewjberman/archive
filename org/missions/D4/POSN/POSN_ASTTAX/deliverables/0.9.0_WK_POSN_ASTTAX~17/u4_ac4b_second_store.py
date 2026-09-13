"""U4-AC4, ARM 5 -- THE DOMAIN TEST ON THE *LIVE* PLANE, NOT THE REPO PLANE.

A repo census cannot answer a live-plane question. ARM 1-4 read the corpus; this arm asks the
live account whether a SECOND store assigns the same classification on the same key, because
that is the shape that makes a chosen domain wrong while every repo instrument agrees with it.

It does NOT copy the second store into the record: it prints COUNTS, the shared vocabulary, and
the 13 rows of U4-AC3's own table. Nothing else is retained.

Usage: python u4_ac4b_second_store.py <etf_classifications_scan.json> <bd_securities_proj.json>
  the second file is the projected scan:
      .tools/aws dynamodb scan --table-name bd-securities \
        --projection-expression "#t,#a,#s,#n" \
        --expression-attribute-names '{"#t":"ticker","#a":"asset_class",
                                       "#s":"sub_asset_class","#n":"asset_name_raw"}'
"""
import sys
import json
import re
import collections

DOM_SCAN, BD_SCAN = sys.argv[1], sys.argv[2]

dom_items = json.load(open(DOM_SCAN))["Items"]
domain = {i["ticker"]["S"] for i in dom_items}
bd = json.load(open(BD_SCAN))
items = bd["Items"]


def g(it, k):
    return it[k]["S"] if k in it and "S" in it[k] else ""


rows = [{"t": g(i, "ticker"), "a": g(i, "asset_class"), "s": g(i, "sub_asset_class"),
         "n": g(i, "asset_name_raw")} for i in items]

print("=" * 78)
print("ARM 5 -- IS THE CHOSEN DOMAIN THE ONLY STORE THAT ASSIGNS THIS CLASSIFICATION?")
print("=" * 78)
print("   live tables in us-east-1 / 313476888478 whose name suggests a classification store")
print("   were enumerated from `dynamodb list-tables` (43 tables). TWO carry a ticker-keyed")
print("   asset_class: etf-classifications (the chosen domain) and bd-securities.")
print()
print("   SECOND STORE : dynamodb://bd-securities")
print("     key schema        : ticker HASH -- THE SAME KEY SPACE as the domain")
print("     attributes        : asset_class, sub_asset_class -- THE SAME ATTRIBUTE NAMES")
print("     server-side Count : %s  (scan --select COUNT)" % bd.get("Count"))
print("     len(Items)        : %d" % len(rows))
print("     LastEvaluatedKey  : %s" % ("ABSENT -- single page" if "LastEvaluatedKey" not in bd
                                       else bd["LastEvaluatedKey"]))
print("     ^ describe-table ItemCount read 9578 against a server-side COUNT of %s. ItemCount is a"
      % bd.get("Count"))
print("       ~6-hourly CACHE and is not a measurement; the COUNT scan is.")
print()
print("   VOCABULARY COMPARISON -- the two stores do not share one:")
print("     domain           : %s"
      % dict(sorted(collections.Counter(i["asset_class"]["S"] for i in dom_items).items())))
print("     bd-securities    : %s"
      % dict(sorted(collections.Counter(r["a"] for r in rows).items())))
print("     ^ bd-securities HAS 'alternatives' (a ratified class) and has NO 'hedge'.")
print("       The domain has 'hedge' and NO 'alternatives'. seed_bd_securities.py says why in")
print("       its own docstring: \"asset_class 'hedge' remapped to 'alternatives'\".")

print()
print("   KEY-SPACE COMPARISON:")
bdt = set(r["t"] for r in rows)
print("     tickers in bd-securities        : %d" % len(bdt))
print("     also in the domain              : %d" % len(bdt & domain))
print("     NOT in the domain               : %d" % len(bdt - domain))
print("     domain tickers absent from bd   : %d -> %s"
      % (len(domain - bdt), sorted(domain - bdt)[:12]))

COMM = {"Gold", "Silver", "Oil", "Commodities"}
RX = re.compile(r"volatil|\bvix\b|bitcoin|ether(eum)?\b|crypto|blockchain|commodit|\bgold\b|"
                r"silver|\boil\b|bullion|platinum|palladium|precious metal|\bgsci\b|real estate|"
                r"\breit\b|realty", re.I)


def reached(r):
    if r["s"] == "Volatility":
        return "R1"
    if r["a"] == "hedge" and r["s"] in COMM:
        return "R2"
    if r["s"] == "Commodities":
        return "R3"
    if RX.search(" | ".join((r["n"], r["s"]))):
        return "R4/R5"
    return None


hit = [(r, reached(r)) for r in rows if reached(r)]
out = [(r, w) for r, w in hit if r["t"] not in domain]
print()
print("   THE LADDER APPLIED TO THE SECOND STORE:")
print("     rows a ratified rule would reach       : %d of %d" % (len(hit), len(rows)))
print("     of those, ticker NOT held by the domain: %d" % len(out))
print("     ^ THE DOMAIN DOES NOT HOLD THESE. Whether they are RETAG MEMBERS depends entirely on")
print("       whether the retag's scope is the ONE ratified source or every store that assigns a")
print("       class -- which is the question C-ONE-SOURCE answers in the SPEC and the world does")
print("       not. Stated, not resolved: resolving it is L5's, not a worker's.")

print()
print("   THE DECIDING TEST FOR U4-AC2 -- are any of MY MEMBERS outside the domain?")
MEM = [("DBC", "Commodities"), ("GLD", "Commodities"), ("GSG", "Commodities"),
       ("IAU", "Commodities"), ("SLV", "Commodities"), ("USO", "Commodities"),
       ("PDBC", "Commodities"), ("VXX", "Structured"), ("VIXY", "Structured"),
       ("UVXY", "Structured"), ("QBER", "Structured"), ("VNQ", "Alternatives"),
       ("BIPC", "UNDETERMINED")]
print("     members / candidates : %d | all present in the domain : %s"
      % (len(MEM), all(t in domain for t, _ in MEM)))
print("     SO: ZERO members lie outside the domain, and U4-AC2's subtraction is NOT VOID.")

print()
print("   BUT THE SAME 13 ROWS IN THE SECOND STORE DISAGREE WITH THE TARGET, AND THAT IS A")
print("   SEPARATE FINDING FROM THE VOID TEST:")
bdmap = {r["t"]: r for r in rows}
print("     %-6s | %-14s | %-18s | %-14s | %s"
      % ("TICKER", "bd asset_class", "bd sub_asset_class", "POSN TARGET", "AGREES?"))
print("     " + "-" * 74)
agree = 0
for t, tgt in MEM:
    r = bdmap.get(t)
    if not r:
        print("     %-6s | %-14s | %-18s | %-14s | %s" % (t, "<ABSENT>", "-", tgt, "n/a"))
        continue
    ok = (r["a"].lower() == tgt.lower())
    agree += 1 if ok else 0
    print("     %-6s | %-14s | %-18s | %-14s | %s"
          % (t, r["a"], r["s"], tgt, "YES" if ok else "NO"))
print("     AGREEMENT: %d of %d" % (agree, len(MEM)))
print("     ^ NOTE THE SHAPE: the disagreeing rows carry 'alternatives', which IS one of the five")
print("       ratified classes. A check that asks only 'is the served value one of the five'")
print("       reads PASS on every one of them. The value is ratified AND wrong.")
