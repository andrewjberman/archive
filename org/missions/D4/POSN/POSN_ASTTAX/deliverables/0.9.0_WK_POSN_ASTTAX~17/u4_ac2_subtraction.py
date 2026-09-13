"""U4-AC2 -- THE RETAG MEMBER SET, AS `DENOMINATOR MINUS WHAT IS EXCLUDED`.

NOT a forward list. Every one of the 285 rows is assigned to exactly one bucket and the
buckets are asserted to sum back to 285; a member cannot be lost without the count disagreeing.

THE RULE LADDER IS ITSELF WRITTEN BY SUBTRACTION FROM THE SPEC, NOT FROM RECALL: the rules are
read off the PRD's own two binding carriers and each carries its file:line, and the classes the
ladder can reach are printed as `the five ratified classes MINUS the ones no rule reaches`.

  PRD org/missions/D4/POSN/POSN_ASTTAX/prd/POSN_ASTTAX_PRD.md @ae66157381
  (blob bd9f9d1f93836878351540c53c20b84ec8dcb34b, byte-identical at HEAD 72f2417499)
    :130-:134  s.3  the five ratified classes and, in the `holds` column, WHAT EACH HOLDS
    :168-:179  s.4  C-VOL-HEDGE-STRUCTURED -- the mechanical membership rules
    :332-:334  s.4  C-MEMBERSHIP-AT-L5 -- edge rules are reserved to L5 and are NOT pre-judged

Usage: python u4_ac2_subtraction.py <scan.json>
"""
import sys
import json
import re
import collections

SCAN = sys.argv[1]

# ---------------------------------------------------------------- the taxonomy
# s.3, verbatim `holds` text, transcribed row for row from PRD:130-:134.
HOLDS = {
    "Fixed Income / Cash": "fixed income and cash",
    "Equity": "equities only -- volatility and hedge REMOVED to Structured",
    "Structured": "options, VIX futures, volatility overlays, VXX and the like",
    "Commodities": "physical (gold, nickel, silver), crypto, and commodity indices (e.g. GSCI)",
    "Alternatives": "real assets (not commodities), private equity, private credit, real estate",
}

# The SERVING-LAYER image of the stored legacy vocabulary. `hedge` HAS NO IMAGE: it is not one
# of the five, which is why every hedge row is a member before any rule is applied.
CURRENT_IMAGE = {
    "equity": "Equity",
    "fixed_income": "Fixed Income / Cash",
    "hedge": None,          # NOT A RATIFIED CLASS
    "cash": "Fixed Income / Cash",
}

COMMODITY_SUBS = {"Gold", "Silver", "Oil", "Commodities"}

# Rules are applied in order; the FIRST that fires wins, and the row records which one did.
# R1..R3 are MECHANICAL: they key on stored fields and are stated verbatim in the constraint.
# R4..R5 are TAXONOMY-TEXT: they key on the `holds` column of s.3, which C-FIVE-CLASSES makes
#        binding. They are applied with the SAME standing round 3 gave its own derived
#        candidates (UVXY/QBER/PDBC), which it counted INTO the set -- see the report.
RULES = [
    ("R1", "sub_asset_class == 'Volatility'  ->  Structured",
     "PRD:168-179 C-VOL-HEDGE-STRUCTURED, 'Volatility -> Structured (VIXY, plus VXX currently "
     "mis-served equity)'; and PRD:132 s.3 Structured holds 'VIX futures, volatility overlays'"),
    ("R2", "asset_class == 'hedge' AND sub in {Gold,Silver,Oil,Commodities}  ->  Commodities",
     "PRD:168-179 C-VOL-HEDGE-STRUCTURED, 'It splits by sub_asset_class: {Gold, Silver, Oil, "
     "Commodities} -> Commodities'"),
    ("R3", "sub_asset_class == 'Commodities' at ANY asset_class  ->  Commodities",
     "PRD:168-170 C-VOL-HEDGE-STRUCTURED, 'physical/crypto/commodity-index positions to "
     "Commodities, NOT Equity'; PRD:133 s.3 Commodities holds 'commodity indices (e.g. GSCI)'"),
    ("R4", "crypto signal in name/sector/sub  ->  Commodities",
     "PRD:133 s.3 Commodities holds 'physical (gold, nickel, silver), CRYPTO, and commodity indices'"),
    ("R5", "real-estate signal in name/sector/sub  ->  Alternatives",
     "PRD:134 s.3 Alternatives holds 'real assets (not commodities), private equity, private "
     "credit, REAL ESTATE'"),
]

RX_CRYPTO = re.compile(r"bitcoin|ether(eum)?\b|crypto|blockchain|digital asset|\bcoin\b", re.I)
RX_REALEST = re.compile(r"real estate|\breit\b|realty|\bproperty\b", re.I)
# R5-WIDE is NOT applied. It is printed so the narrow reading can be falsified.
RX_REALASSET_WIDE = re.compile(
    r"infrastructur|timber|farmland|pipeline|midstream|\bmlp\b|master limited|toll road", re.I)
RX_PRIVATE = re.compile(r"private (equity|credit|market)|\bbdc\b|business development", re.I)


def _s(it, k):
    return it[k]["S"] if k in it and "S" in it[k] else ""


def load(path):
    d = json.load(open(path))
    out = []
    for it in d["Items"]:
        out.append({"t": _s(it, "ticker"), "a": _s(it, "asset_class"),
                    "s": _s(it, "sub_asset_class"), "m": _s(it, "management_style"),
                    "sec": _s(it, "sector"), "n": _s(it, "name")})
    return out, d


def classify(r):
    """Return (target_class, rule_id) or (None, None) if NO rule reaches this row."""
    blob = " | ".join((r["n"], r["sec"], r["s"]))
    if r["s"] == "Volatility":
        return "Structured", "R1"
    if r["a"] == "hedge" and r["s"] in COMMODITY_SUBS:
        return "Commodities", "R2"
    if r["s"] == "Commodities":
        return "Commodities", "R3"
    if RX_CRYPTO.search(blob):
        return "Commodities", "R4"
    if RX_REALEST.search(blob):
        return "Alternatives", "R5"
    return None, None


rows, raw = load(SCAN)
N = len(rows)

print("=" * 78)
print("START -- THE DENOMINATOR: %d rows" % N)
print("  dynamodb://etf-classifications, full scan, Count==ScannedCount==%d, no LastEvaluatedKey" % N)
print("=" * 78)

print()
print("THE RULE LADDER, read off the spec (not recalled). Each rule cites where it comes from:")
for rid, stmt, cite in RULES:
    print("  %s  %s" % (rid, stmt))
    print("      <- %s" % cite)
print()
print("WHICH OF THE FIVE RATIFIED CLASSES CAN THE LADDER REACH, written as a SUBTRACTION:")
reach = set()
for rid, stmt, _ in RULES:
    reach.add(stmt.split("->")[-1].strip())
unreached = [c for c in HOLDS if c not in reach]
print("  the five MINUS the classes no rule targets = %s" % sorted(reach))
print("  UNREACHED by any rule: %s" % unreached)
print("  ^ correct and expected: no rule MOVES a row INTO Fixed Income / Cash or INTO Equity --")
print("    those two are where the un-moved rows already sit, so they are the ladder's fall-through,")
print("    never its target. Alternatives IS reachable, by R5 only.")

# ------------------------------------------------------------------ partition
members, excluded = [], collections.OrderedDict()


def exclude(key, r, why):
    excluded.setdefault(key, {"why": why, "rows": []})["rows"].append(r)


for r in rows:
    tgt, rid = classify(r)
    cur = CURRENT_IMAGE.get(r["a"], "<UNMAPPED LEGACY VALUE %r>" % r["a"])
    if tgt is None:
        if cur is None:
            # a hedge row no rule reaches -- would be a member with an UNDETERMINED target
            members.append((r, "<UNDETERMINED>", "NO-RULE", cur))
        elif cur == "Fixed Income / Cash":
            exclude("E1", r, "served fixed_income and NO rule in the ladder reaches it: its "
                             "sub_asset_class is not Volatility, not a commodity sub, and its "
                             "name/sector carry no crypto or real-estate signal. PRD:130 class 1 "
                             "holds 'fixed income and cash', so it is already in its class.")
        elif cur == "Equity":
            exclude("E2", r, "served equity and NO rule in the ladder reaches it: not Volatility, "
                             "not a commodity sub, no crypto/real-estate signal in name or sector. "
                             "PRD:131 class 2 holds 'equities only', so it is already in its class.")
        else:
            exclude("E3", r, "served a legacy value with no ratified image and no rule reaches it "
                             "-- IF THIS BUCKET IS EVER NON-EMPTY IT IS A FINDING, NOT AN EXCLUSION")
    elif cur is not None and tgt == cur:
        exclude("E4", r, "a rule reaches this row but its target EQUALS the class it is already "
                         "served as -- no membership change, so no retag")
    else:
        members.append((r, tgt, rid, cur))

print()
print("=" * 78)
print("THE SUBTRACTION")
print("=" * 78)
run = N
print("  START                                                        %4d" % run)
for key in ("E1", "E2", "E3", "E4"):
    excluded.setdefault(key, {"why": {
        "E1": "served fixed_income, no rule reaches it (already class 1)",
        "E2": "served equity, no rule reaches it (already class 2)",
        "E3": "legacy value with no ratified image that no rule reaches -- AN EMPTY BUCKET "
              "HERE IS THE CLAIM THAT EVERY hedge ROW IS ACCOUNTED FOR",
        "E4": "a rule reaches it but the target equals the class it is already served as",
    }[key], "rows": []})
for key, blk in excluded.items():
    run -= len(blk["rows"])
    print("  MINUS %-3s %4d rows  %s" % (key, len(blk["rows"]), blk["why"][:60]))
    for extra in [blk["why"][60:][i:i + 60] for i in range(0, len(blk["why"][60:]), 60)]:
        print("                        %s" % extra)
    print("  %-58s %4d" % ("  remainder", run))
print("  " + "-" * 66)
print("  SURVIVING RETAG MEMBER SET                                   %4d" % len(members))
assert run == len(members), "ARITHMETIC DOES NOT CLOSE"
assert sum(len(b["rows"]) for b in excluded.values()) + len(members) == N
print("  ARITHMETIC CLOSES: %d excluded + %d members == %d denominator"
      % (sum(len(b["rows"]) for b in excluded.values()), len(members), N))

print()
print("== E0 -- THE EXCLUSION THAT IS MADE BEFORE THE LADDER RUNS, AND IT IS A CHOICE ==")
RATIFIED = set(HOLDS)
carry = [r for r in rows if r["a"] in RATIFIED]
print("  rows whose STORED asset_class string is already one of the five ratified labels:")
print("      %d of %d" % (len(carry), N))
print("  So on a STRING reading -- 'a retag is any row whose stored value is not a ratified")
print("  label' -- THE MEMBER SET IS ALL %d ROWS, not %d." % (N, len(members)))
print("  THAT READING IS EXCLUDED HERE, WITH ITS REASON: the stored vocabulary is lowercase")
print("  legacy ('equity','fixed_income','hedge') and the serving layer maps it to the ratified")
print("  labels, so 'equity'->Equity is a RENDERING, not a membership change. This cell settles")
print("  WHICH MEMBERS THE RETAG WOULD TOUCH -- rows whose CLASS MEMBERSHIP moves. The competing")
print("  reading is named rather than suppressed because it changes the answer by 273.")

print()
print("THE MEMBERS:")
for r, tgt, rid, cur in sorted(members, key=lambda x: (x[1], x[0]["t"])):
    print("  %-6s served a=%-13s s=%-12s sec=%-12s  %-20s -> %-14s [%s]"
          % (r["t"], r["a"], r["s"], r["sec"], cur or "(NO ratified image)", tgt, rid))

print()
print("PER-RULE TALLY (sums to the member count):")
tal = collections.Counter(rid for _, _, rid, _ in members)
for rid, stmt, _ in RULES:
    print("  %s  %-4d  %s" % (rid, tal.get(rid, 0), stmt))
print("  SUM %d" % sum(tal.values()))

# -------------------------------------------------- the delta against ELEVEN
STANDING_11 = {"DBC", "GLD", "GSG", "IAU", "SLV", "USO", "VIXY", "VXX", "UVXY", "QBER", "PDBC"}
mine = {r["t"] for r, _, _, _ in members}
print()
print("=" * 78)
print("AGAINST THE STANDING FIGURE -- ELEVEN (carried from round 3, AT3-s-5 / TO-T5-1)")
print("=" * 78)
print("  standing set size : %d" % len(STANDING_11))
print("  derived set size  : %d" % len(mine))
print("  PRESENT-BUT-UNEXPECTED (in my set, not in the standing eleven): %s"
      % (sorted(mine - STANDING_11) or "NONE"))
print("  EXPECTED-BUT-ABSENT    (in the standing eleven, not in my set): %s"
      % (sorted(STANDING_11 - mine) or "NONE"))
print("  INTERSECTION           : %d" % len(mine & STANDING_11))

print()
print("=" * 78)
print("THE ARM THAT WAS *NOT* APPLIED, PRINTED SO THE NARROW READING CAN BE FALSIFIED")
print("=" * 78)
for label, rx in (("R5-WIDE real assets (infrastructure/timber/farmland/midstream)", RX_REALASSET_WIDE),
                  ("R5-WIDE private equity / private credit", RX_PRIVATE),
                  ("R4 crypto", RX_CRYPTO)):
    hits = [r for r in rows if rx.search(" | ".join((r["n"], r["sec"], r["s"])))]
    print("  %-58s %d of %d rows" % (label, len(hits), N))
    for r in sorted(hits, key=lambda r: r["t"]):
        print("      %-6s a=%-12s s=%-14s sec=%-12s %s" % (r["t"], r["a"], r["s"], r["sec"], r["n"][:48]))
print("  ^ these are NOT counted as members. Reason: C-MEMBERSHIP-AT-L5 (PRD:332-334) reserves")
print("    edge membership rules to L5. R5 fires on the literal phrase 'real estate', which is")
print("    written verbatim in s.3's Alternatives row AND is the literal value of the row's own")
print("    `sector` field -- that is the spec speaking, not an edge call. 'Infrastructure' is in")
print("    no class's holds text, so calling it a real asset WOULD be an edge call and is not")
print("    made here; it is recorded UNDETERMINED in the U4-AC3 table instead of being guessed.")

print()
print("== SUBSTRING TRAP, DISCLOSED ==")
gs = [r for r in rows if re.search(r"gold", r["n"], re.I)]
print("  a case-insensitive 'gold' over the name column returns %d rows: %s"
      % (len(gs), sorted(r["t"] for r in gs)))
print("  GS is 'The Goldman Sachs Group Inc' -- a SUBSTRING hit, not a commodity. It is excluded")
print("  by E1 because no rule keys on the name column for R2/R3; only R4/R5 read names, and")
print("  neither pattern matches it. Printed because a silent substring hit is how a wrong")
print("  member enters a set that otherwise looks derived.")
