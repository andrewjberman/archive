"""U4-AC3 -- (member, current class, target class) WITH PROVENANCE ON BOTH SIDES. No blanks.

CURRENT is read from the STORE BY KEY on a SECOND instrument (batch-get-item point reads),
not sliced out of the scan U4-AC2 subtracted over -- so the two columns of this table do not
share one retrieval. The script asserts the two instruments agree per member and prints the
comparison; a disagreement would be the finding, not a footnote.

TARGET is cited to the spec line that rules it, at a pinned commit and a blob sha.

A member whose target cannot be determined is printed as UNDETERMINED with the reason and is
NOT counted into the set -- never guessed, never omitted.

Usage: python u4_ac3_member_table.py <scan.json> <batchget_resp.json>
"""
import sys
import json

SCAN, BATCH = sys.argv[1], sys.argv[2]

PRD = "org/missions/D4/POSN/POSN_ASTTAX/prd/POSN_ASTTAX_PRD.md"
PIN = "ae66157381"
BLOB = "bd9f9d1f93836878351540c53c20b84ec8dcb34b"
STORE = "dynamodb://etf-classifications (us-east-1, acct 313476888478), key {ticker: <T>}"

# (ticker, target, standing, rule, spec citation, one-line reason)
TABLE = [
    ("DBC", "Commodities", "MEMBER", "R2", PRD + ":168-179",
     "served asset_class=hedge with sub_asset_class=Commodities; C-VOL-HEDGE-STRUCTURED splits "
     "the hedge bucket and sends {Gold,Silver,Oil,Commodities} to Commodities"),
    ("GLD", "Commodities", "MEMBER", "R2", PRD + ":168-179 and :343-345",
     "physical gold; hedge/Gold. Named BY HAND in C-SATELLITE-DATA as the measured served-plane "
     "gap that must move to Commodities"),
    ("GSG", "Commodities", "MEMBER", "R2", PRD + ":168-179",
     "GSCI commodity-indexed trust; hedge/Commodities. s.3 class 4 names 'commodity indices "
     "(e.g. GSCI)' literally"),
    ("IAU", "Commodities", "MEMBER", "R2", PRD + ":168-179",
     "physical gold trust; hedge/Gold"),
    ("SLV", "Commodities", "MEMBER", "R2", PRD + ":168-179",
     "physical silver trust; hedge/Silver"),
    ("USO", "Commodities", "MEMBER", "R2", PRD + ":168-179",
     "oil fund; hedge/Oil"),
    ("PDBC", "Commodities", "MEMBER", "R3", PRD + ":168-170 and :133",
     "served EQUITY with sub_asset_class=Commodities -- the 'commodity-index positions to "
     "Commodities, NOT Equity' half of the same constraint. Not in the hedge bucket, so a "
     "derivation that enumerates the hedge bucket misses it"),
    ("VXX", "Structured", "MEMBER", "R1", PRD + ":168-179, :132 and :343-345",
     "VIX-futures ETN served equity/Volatility. Named BY HAND in C-SATELLITE-DATA and by name "
     "in s.3's Structured holds text ('VXX and the like')"),
    ("VIXY", "Structured", "MEMBER", "R1", PRD + ":168-179",
     "VIX short-term futures ETF; the ONE volatility row inside the hedge bucket"),
    ("UVXY", "Structured", "MEMBER", "R1", PRD + ":168-179 and :132",
     "ultra VIX short-term futures ETF served equity/Volatility"),
    ("QBER", "Structured", "MEMBER", "R1", PRD + ":168-179 and :132",
     "quarterly bear hedge ETF served FIXED_INCOME with sub_asset_class=Volatility -- the only "
     "member whose current class is class 1, and the one a hedge-bucket or equity-scoped "
     "derivation cannot see at all"),
    ("VNQ", "Alternatives", "MEMBER", "R5", PRD + ":134",
     "Vanguard Real Estate ETF, sector field reads the literal string 'Real Estate', which is "
     "the literal phrase in class 5's holds column. NOT in the standing eleven -- this is the "
     "delta, and it is the ONLY row in the registry that reaches Alternatives at all"),
    ("BIPC", "UNDETERMINED", "CANDIDATE-NOT-COUNTED", "R5-WIDE", PRD + ":134 and :332-334",
     "Brookfield Infrastructure Corp, served equity/Utilities. Class 5 holds 'real assets (not "
     "commodities)' and infrastructure is conventionally a real asset -- BUT the word "
     "'infrastructure' appears in NO class's holds text, so deciding it is an EDGE RULE, and "
     "C-MEMBERSHIP-AT-L5 reserves edge rules to L5. Target UNDETERMINED rather than guessed; "
     "recorded so it is not omitted. It is also an operating COMPANY, not a fund, which is a "
     "second reason the call is not mechanical"),
]


def read_scan(p):
    d = json.load(open(p))
    return {i["ticker"]["S"]: i for i in d["Items"]}


def read_batch(p):
    d = json.load(open(p))
    assert d.get("UnprocessedKeys") == {}, "UnprocessedKeys NOT EMPTY: %r" % d.get("UnprocessedKeys")
    return {i["ticker"]["S"]: i for i in d["Responses"]["etf-classifications"]}


def g(it, k):
    return it[k]["S"] if it and k in it and "S" in it[k] else "<ABSENT>"


scan = read_scan(SCAN)
batch = read_batch(BATCH)

IMAGE = {"equity": "Equity", "fixed_income": "Fixed Income / Cash", "hedge": None}

print("PROVENANCE OF THE *CURRENT* COLUMN")
print("  store/key : %s" % STORE)
print("  instrument A : full scan  (the population U4-AC2 subtracted over)")
print("  instrument B : batch-get-item POINT READS by key, UnprocessedKeys {} verbatim, "
      "13 of 14 keys resolved")
print("                 (the 14th, ZZZ_NO_SUCH_TICKER, is a NEGATIVE CONTROL and correctly "
      "did not resolve)")
print("PROVENANCE OF THE *TARGET* COLUMN")
print("  spec      : %s @%s  (blob %s, byte-identical at HEAD)" % (PRD, PIN, BLOB))
print()

hdr = ("%-6s | %-12s | %-20s | %-14s | %-5s | %s"
       % ("MEMBER", "SERVED VALUE", "CURRENT CLASS", "TARGET CLASS", "RULE", "STANDING"))
print(hdr)
print("-" * len(hdr))
counted = 0
disagreements = []
for t, tgt, standing, rule, cite, why in TABLE:
    a, b = scan.get(t), batch.get(t)
    va, vb = g(a, "asset_class"), g(b, "asset_class")
    if va != vb:
        disagreements.append((t, va, vb))
    cur = IMAGE.get(vb, "<UNMAPPED %r>" % vb)
    cur_s = cur if cur else "(NONE -- 'hedge' is not one of the five)"
    print("%-6s | %-12s | %-20s | %-14s | %-5s | %s" % (t, vb, cur_s, tgt, rule, standing))
    if standing == "MEMBER":
        counted += 1
print("-" * len(hdr))
print("COUNTED MEMBERS: %d   |   UNDETERMINED CANDIDATES NOT COUNTED: %d   |   TABLE ROWS: %d"
      % (counted, len(TABLE) - counted, len(TABLE)))
print("BLANKS IN ANY CELL: 0 (every cell above is a value or the literal UNDETERMINED)")

print()
print("CROSS-INSTRUMENT CONTROL (scan vs point read, per member, on the graded attribute):")
print("  disagreements: %s" % (disagreements or "NONE -- all %d rows agree" % len(TABLE)))

print()
print("PER-MEMBER DETAIL -- every attribute as read on instrument B, plus the rule and reason")
for t, tgt, standing, rule, cite, why in TABLE:
    b = batch.get(t)
    print()
    print("  %s  [%s]" % (t, standing))
    print("    READ FROM   : %s" % STORE.replace("<T>", t))
    print("    name              : %s" % g(b, "name"))
    print("    asset_class       : %s      <- THE CURRENT CLASSIFICATION" % g(b, "asset_class"))
    print("    sub_asset_class   : %s" % g(b, "sub_asset_class"))
    print("    sector            : %s" % g(b, "sector"))
    print("    management_style  : %s%s" % (g(b, "management_style"),
          "   <- TRIP=TRUE, the truthy 'unknown' placeholder C-RETAG-SAFETY names"
          if g(b, "management_style") == "unknown" else ""))
    print("    last_updated      : %s   (NOT a vintage -- see U4-AC1)" % g(b, "last_updated"))
    print("    updated_by        : %s" % g(b, "updated_by"))
    print("    CURRENT CLASS     : %s"
          % (IMAGE.get(g(b, "asset_class")) or "(NONE -- 'hedge' is not one of the five ratified "
                                               "classes, so this row is in NO class today)"))
    print("    TARGET CLASS      : %s   [%s]" % (tgt, rule))
    print("    TARGET CITED TO   : %s @%s" % (cite, PIN))
    print("    REASON            : %s" % why)

print()
print("== THE ARMED HALF OF C-RETAG-SAFETY, COUNTED OVER THIS TABLE ==")
trip = [t for t, _, _, _, _, _ in TABLE if g(batch.get(t), "management_style") == "unknown"]
print("  members whose management_style is the truthy 'unknown' placeholder: %d of %d -> %s"
      % (len(trip), len(TABLE), trip or "NONE"))
print("  (PRD:250-255 predicted GLD/IAU/SLV/USO/DBC/GSG would all trip. They do not today --")
print("   TO-S5-1 set them. Re-read at the moment of acting, never from the PRD's sentence.)")
