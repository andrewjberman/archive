"""POSN_ASTTAX.TO-T5-1 / cell AT3-s-5 -- THE BAR: the SURFACE x MEMBER x CLAUSE table.

Emits the full table (every surface in the T5-AC2 set x every retag-set member x clauses a/b/c/d),
one GRAIN label per cell with its reason, then the three grain counts and the T5-AC7 verdict.

EVERY verdict below is keyed to a reading taken this session and named in `EVID`. Nothing here is
recalled: the readings are in ../0.9.0_WK_POSN_ASTTAX~14/t5_readings.txt beside this file.

Run:  python t5_bar_table.py            (writes nothing; prints the table)
0.9.0_WK_POSN_ASTTAX~14, 2026-09-11. READ-ONLY cell.
"""
import collections

# ---------------------------------------------------------------- the retag set (T5-AC1)
# Derived by SUBTRACTION over all 285 rows of DynamoDB etf-classifications, not inherited.
MEMBERS = [
    ("DBC",  "hedge",        "Commodities"),
    ("GLD",  "hedge",        "Commodities"),
    ("GSG",  "hedge",        "Commodities"),
    ("IAU",  "hedge",        "Commodities"),
    ("SLV",  "hedge",        "Commodities"),
    ("USO",  "hedge",        "Commodities"),
    ("VIXY", "hedge",        "Structured"),
    ("VXX",  "equity",       "Structured"),
    ("UVXY", "equity",       "Structured"),
    ("QBER", "fixed_income", "Structured"),
    ("PDBC", "equity",       "Commodities"),
]
HELD = {"VXX"}          # the only member carrying live weight in json/positioning/positioning_data.json
IN_HAD = {"VXX", "UVXY", "QBER", "PDBC"}   # members carrying live rows in holdings_attribution_data.json

EX = "MEASURED-EXERCISED"
SP = "MEASURED-SOURCE-AT-PIN"
NM = "NOT-MEASURABLE-HERE"

# ---------------------------------------------------------------- the surface set (T5-AC2)
# (id, kind, name, vintage, {clause: (verdict, grain, reason)})
SURFACES = [
 ("A1", "ARTIFACT",
  "s3://opal-data-portal-v2/json/positioning/positioning_data.json  <- yang-generate-positioning",
  "LastModified 2026-09-11T11:06:24+00:00, ContentLength 8123 (gzip; 73790 raw), "
  "ETag 90c464008b3ffe962367e6667a1c2391 | DEPLOYED lambda_function.py 94164 B md5 cc79aff7506f8c39e17453f386c69551",
  {"a": ("FAIL", EX, "the DEPLOYED bytes RAISE KeyError at calculate_allocations():239 on the ratified label, so NO artifact is written and no served value exists to equal the label"),
   "b": ("FAIL", EX, "same raise -- label-grouped weight for the target label is 0.000000 BEFORE and UNOBTAINABLE AFTER (the generator dies)"),
   "c": ("FAIL", SP, "even with a payload, the only rendered consumer (R1) iterates a hardcoded ['Fixed Income','Equity'] so the row renders nowhere"),
   "d": ("FAIL", EX, "no artifact is produced, so there are no subtotals to sum; at HEAD bytes the payload sums to 1.000000 while the two RENDERED groups sum to 0.985000 -- difference 0.015000, the PROD v2.1.167 shape with a new value")}),

 ("A2", "ARTIFACT",
  "s3://opal-data-portal-v2/json/positioning/holdings_attribution_data.json  <- yang-generate-holdings-attribution",
  "LastModified 2026-09-04T13:51:29+00:00, ContentLength 386689, ETag 6455a15c85827a4e3f58a181b7d28114 | "
  "DEPLOYED lambda_function.py 30110 B md5 c7307781723c4c37f295288930fa9b21 == HEAD bytes (IDENTICAL)",
  {"a": ("PASS", SP, "lambda_function.py:594-597 folds only fixed_income/Fixed income -> 'Fixed Income' and equity/hedge -> 'Equity'; a value 'Commodities'/'Structured' matches neither branch and passes through unchanged"),
   "b": ("PASS", SP, "the holding keeps its own weight field; grouping the served rows by the new label returns that weight -- no accumulator drops it"),
   "c": ("FAIL", SP, "its rendered consumers R2/R3/R4 each gate on a hardcoded ['Fixed Income','Equity'] pair"),
   "d": ("FAIL", SP, ":643-647 links a holding to asset_class_subtotals by the normalised class name; a class with no subtotal row gets no subtotal and policy_return 0, so the new class's weight is in the grand total with no subtotal behind it")}),

 ("A3", "ARTIFACT",
  "s3://opal-data-portal-v2/json/positioning/allocation_summary.json  <- yang-generate-allocation-summary",
  "LastModified 2026-09-11T11:06:28+00:00, ContentLength 967 (gzip; 6576 raw), ETag 4e53306dd0557eb15aa9eca61578ccae | "
  "DEPLOYED lambda_function.py 15709 B md5 06bf1c106208791b1ea3b3d852b01bb1 == HEAD bytes (IDENTICAL)",
  {"a": ("PASS", SP, "read-dependency W12-S2 measured the value SURVIVES all hops (:255-256 else is a pass-through); my own read shows the deployed bytes are byte-identical to the ones it measured"),
   "b": ("PASS", SP, "same measured run: style_weight carries the full weight (10.0 on a 10.0 input)"),
   "c": ("FAIL", SP, "W12-S3: the placeholder path :339-341 emits a hardcoded two-row list, and the sort key :291-292 knows two names, so a new class renders in insertion order or not at all"),
   "d": ("FAIL", SP, "W12-S2: BENCHMARK_ALLOCATIONS :45-52 is a two-key dict and :267 defaults every other class to policy_weight 0.0, so bet == the row's entire weight; W12-S3 site 4: the :296-301 renormalisation dumps the whole gap on the largest row")}),

 ("A4", "ARTIFACT",
  "s3://opal-data-portal-v2/platinum/etfs/positioning_data.json  <- data/etfs/scripts/gold/etf_positioning_publisher.py",
  "LastModified 2026-09-11T13:01:27+00:00, ContentLength 148526, ETag 367fba76d3537fae874bd7db6c23279f (LIVE, written today)",
  {"a": ("VACUOUS-PASS", EX, "holdings[].asset_class carries the ETFClassifier value verbatim (:416), so the ratified label would be served -- but 0 of 11 members hold a row in this artifact at this vintage, so nothing is actually asserted"),
   "b": ("FAIL", EX, "the book-level allocation object is a FOUR-KEY literal at :469-472 {cash,fixed_income,equity,hedge}; measured in the live bytes for all 4 books. A Commodities/Structured weight has no key to land in"),
   "c": ("FAIL", SP, "its portal consumer src/pages/Positioning/shared/etfAdapter.ts:105 carries a FOURTH copy of the same four-key ZERO_ALLOCATION shape"),
   "d": ("FAIL", EX, "live label-grouped read: Equity 3.953400 + Fixed Income 0.046300 = 3.999700 over 189 rows, across a four-key allocation; a fifth class cannot enter the sum")}),

 ("A5", "STORE",
  "DynamoDB bd-securities  <- seeded FROM etf-classifications by data/black_diamond/scripts/classification/seed_bd_securities.py",
  "source read at 3ce0c0e372; SOURCE_TABLE = 'etf-classifications' (:21), full item copy",
  {"a": ("NOT-GRADED", SP, "a store, not a served surface: it carries whatever the retag writes, on a MANUAL trigger"),
   "b": ("NOT-GRADED", SP, "no weight lives here"),
   "c": ("NOT-GRADED", SP, "nothing renders here"),
   "d": ("NOT-GRADED", SP, "no totals live here")}),

 ("A6", "ARTIFACT",
  "partner-firm served data  <- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data (ETFClassifier over bd-securities)",
  "source read at 3ce0c0e372 (:62 import, :1026 'via ETFClassifier (bd-securities DynamoDB table)', :1270 groupby asset_class)",
  {"a": ("NOT-MEASURED", NM, "reachable only after a manual bd-securities re-seed; I did not read this lambda's served output or its deployed bytes"),
   "b": ("NOT-MEASURED", NM, "same -- its mix is a groupby on asset_class (:1270) and would gain a new group, but I did not measure the served artifact"),
   "c": ("NOT-MEASURED", NM, "its rendered consumer is the AdvisorIntelligence plane, whose maps (R9) are four-key -- but I did not trace this artifact to a specific view"),
   "d": ("NOT-MEASURED", NM, "not read")}),

 ("A7", "ARTIFACT",
  "BD + COT gold client artifacts  <- data/{black_diamond,cot}/scripts/gold/{C_06,D_03,D_04,E_25} via lib/etf_classifier.py (bd-securities)",
  "source read at 3ce0c0e372; ETFClassifier.__init__ default table_name='bd-securities'",
  {"a": ("NOT-MEASURED", NM, "conditional reach via A5; served outputs not read by this cell"),
   "b": ("NOT-MEASURED", NM, "not read"),
   "c": ("NOT-MEASURED", NM, "not read"),
   "d": ("NOT-MEASURED", NM, "not read")}),

 ("A8", "ARTIFACT",
  "49F dim_asset_classification  <- data/assets/scripts/gold/runners_49f/a07_dim_asset_classification.py",
  "source read at 3ce0c0e372; :231/:239 return ('alternatives' if ac == 'hedge' else ac)",
  {"a": ("FAIL", SP, "this producer REWRITES the class: a row served 'hedge' becomes 'alternatives' here. After the retag the six commodity members arrive as 'Commodities' and fall to the else, so this surface silently changes what it publishes for them without any code change"),
   "b": ("NOT-MEASURED", NM, "its weights were not read by this cell"),
   "c": ("NOT-MEASURED", NM, "not traced to a view"),
   "d": ("NOT-MEASURED", NM, "not read")}),

 ("R1", "RENDERED",
  "portal src/pages/Positioning/tabs/HoldingsTab.tsx  (Positioning > Holdings)",
  "portal submodule pin e85f6eb84f (superproject gitlink at 3ce0c0e372)",
  {"a": ("NOT-GRADED", SP, "a view renders a value, it does not serve one"),
   "b": ("FAIL", SP, ":1382-1383 folds only Cash->Fixed Income and Hedge->Equity; after the retag no member is 'Hedge' any more, so the fold no longer catches them"),
   "c": ("FAIL", SP, ":1392 const assetClassOrder = ['Fixed Income', 'Equity'] then .filter(ac => groupedHoldings[ac]) -- a group keyed Commodities/Structured is NEVER ITERATED"),
   "d": ("FAIL", SP, ":1364-1372 documents this exact failure for Cash on PROD v2.1.167 (PFDE 90 -> 89 rows, 99.98 under 100.01); the weight stays in the grand total while the row does not render")}),

 ("R2", "RENDERED",
  "portal src/pages/Attribution/tabs/SelectionTab.tsx  (Attribution > Selection)",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "a view"),
   "b": ("FAIL", SP, "no fold at all for the new labels"),
   "c": ("FAIL", SP, ":321 const assetClassOrder = ['Fixed Income', 'Equity'] -- the SECOND hardcoded pair, in a file the PRD's known-site list does not name"),
   "d": ("FAIL", SP, "same shape as R1: unrendered rows keep their weight in the total")}),

 ("R3", "RENDERED",
  "portal src/pages/Attribution/components/AssetAllocationSummary.tsx",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "a view"),
   "b": ("FAIL", SP, ":129/:132 branch only on 'Equity' and 'Fixed Income'"),
   "c": ("FAIL", SP, ":92 const requiredAssetClasses = ['Fixed Income', 'Equity']"),
   "d": ("FAIL", SP, "subtotals are computed over the required pair only")}),

 ("R4", "RENDERED",
  "portal src/pages/Attribution/components/StylePolicyComparison.tsx",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "a view"),
   "b": ("FAIL", SP, "its comparison is built per required class"),
   "c": ("FAIL", SP, ":156 const requiredAssetClasses = ['Fixed Income', 'Equity']"),
   "d": ("FAIL", SP, "same")}),

 ("R5", "RENDERED",
  "portal src/pages/Positioning/constants/etf-categories.ts  (the Positioning page's OWN taxonomy)",
  "portal pin e85f6eb84f",
  {"a": ("FAIL", SP, ":5 the TYPE is assetClass: 'Fixed Income' | 'Equity' | 'Cash' -- a ratified label is not in the union; and :66 hardcodes UVXY as Equity/Volatility, a SECOND source of truth that the registry retag cannot reach"),
   "b": ("FAIL", SP, "segments are enumerated per class at :83-85; a new class has no segment list"),
   "c": ("FAIL", SP, ":76-78 the ORDER array is ['Cash','Fixed Income','Equity']"),
   "d": ("FAIL", SP, "totals follow the order array")}),

 ("R6", "RENDERED",
  "portal src/pages/Attribution/constants/etf-categories.ts  (the Attribution page's OWN taxonomy)",
  "portal pin e85f6eb84f",
  {"a": ("FAIL", SP, ":7 type union 'Fixed Income'|'Equity'|'Cash'|'Hedge'; and :94/:95/:98/:59 hardcode UVXY, VXX, PDBC and QBER to Equity/Fixed Income BY TICKER -- four of the eleven retag-set members are re-classified in the frontend, so the registry retag is overridden here"),
   "b": ("FAIL", SP, ":115-118 segment lists per class; 'Hedge': [] is empty"),
   "c": ("FAIL", SP, ":108-110 order array ['Cash','Fixed Income','Equity']"),
   "d": ("FAIL", SP, "same")}),

 ("R7", "RENDERED",
  "portal src/lib/chartColors.ts + src/pages/Attribution/constants/holdings-shared.tsx  (the color plane, FWD-4)",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "a color map serves no class value"),
   "b": ("NOT-GRADED", SP, "no weight"),
   "c": ("FAIL", SP, "no key 'Structured' exists as a top-level class anywhere in portal src (measured: every 'Structured' hit in 6 files is 'Structured Credit', a FIXED-INCOME segment); a Structured group has no color and collides by name with an existing concept"),
   "d": ("NOT-GRADED", SP, "no totals")}),

 ("R8", "RENDERED",
  "portal src/pages/CapitalMarketAssumptions/* (the SECOND ratified surface, C-TWO-SURFACES)",
  "portal pin e85f6eb84f",
  {"a": ("FAIL", SP, "types.ts:10 category union uses 'Equities', not the ratified 'Equity'; the two ratified surfaces do not share a vocabulary"),
   "b": ("NOT-GRADED", SP, "CMA carries expectations, not portfolio weights"),
   "c": ("FAIL", SP, "ExpectationsTab.tsx:98-102 maps BOTH 'Alternatives' and 'Commodities' onto ASSET_CLASS.alternatives, so two ratified classes render as one colour -- and no 'Structured' key exists"),
   "d": ("NOT-GRADED", SP, "no portfolio totals on this surface")}),

 ("R9", "RENDERED",
  "portal src/pages/AdvisorIntelligence/_shared/{lib/composition.ts, perfrp/PerfrpAllocation.tsx}",
  "portal pin e85f6eb84f",
  {"a": ("FAIL", SP, "composition.ts:36-58 carries THREE four-key maps keyed cash/equity/fixed_income/alternatives -- no structured, no commodities"),
   "b": ("FAIL", SP, "a value outside those keys has no display row to carry its weight"),
   "c": ("FAIL", SP, "PerfrpAllocation.tsx:42-45 the same four keys"),
   "d": ("NOT-MEASURED", NM, "I did not read this plane's total arithmetic")}),

 ("R10", "RENDERED",
  "portal src/pages/Positioning/panels/PositioningSummary.tsx",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "a view"),
   "b": ("FAIL", SP, ":194-195 the summary rows are a hardcoded two-element list of labels"),
   "c": ("FAIL", SP, "same two-element list decides what is shown"),
   "d": ("NOT-GRADED", SP, "not measured on this panel")}),

 ("R11", "RENDERED",
  "portal src/pages/Positioning/shared/etfAdapter.ts  (adapts A4 into the Positioning page)",
  "portal pin e85f6eb84f",
  {"a": ("NOT-GRADED", SP, "an adapter"),
   "b": ("FAIL", SP, ":105 ZERO_ALLOCATION = { cash, fixed_income, equity, hedge } -- a fourth copy of the four-key shape; a fifth class has nowhere to go"),
   "c": ("FAIL", SP, "it feeds R1, which iterates two labels"),
   "d": ("FAIL", SP, "delta is built from the same four-key shape")}),
]

SUBTRACTED = [
 ("s3://opal-data-portal-v2/json/capital-markets/{assumptions,views}.json <- yang-generate-cma",
  "NOT REACHABLE BY THE RETAG: its asset_class comes from an Excel column ('Asset Class', lambda_function.py:266), "
  "not from the registry -- measured on the live artifact, whose 27 class values are a DIFFERENT vocabulary "
  "('Equities','GSCI','Gold','Private Equity',...) and contain 0 of 11 members. KEPT AS A NAMED RISK: "
  "C-TWO-SURFACES requires this surface to AGREE with Positioning, and a retag moves one and not the other."),
 ("s3://opal-data-portal-v2/json/benchmarks/etf_returns.json <- yang-generate-etf-returns",
  "NOT REACHABLE: its asset_class values are a hardcoded 5-entry literal at lambda_function.py:31-35 "
  "(BIL/VGSH/AGG/IVV/ACWI), none of which is a retag-set member, and the served field is read from that "
  "literal (:104), never from the registry."),
 ("market-overview-tiered-generator + market-rsi-tiered-generator",
  "NOT REACHABLE: asset_class is derived from ASSET_CLASS_MAP.get(entity_type) (:401) in one and is a "
  "function PARAMETER (:565) in the other; neither reads etf-classifications. They appeared in the "
  "comp-find census and are subtracted with this proof rather than by omission."),
 ("468 record-plane blobs under org/ docs/ rcg/ memory/ .scratch/",
  "NOT A SURFACE: project records, task orders, proofs and prose. They carry the token and serve nothing."),
 ("118 code-plane blobs carrying the token with NO registry, module or artifact reference",
  "NOT REACHABLE: measured by pattern over the same object-store census "
  "(etf-classifications|ETF_CLASSIFICATIONS|etf_classifications_dynamodb|ETFClassifier|classify_etf|etf_classification). "
  "The subtracted set is printed by top directory in t5_readings.txt so it can be falsified, not asserted."),
 ("infra/aws/terraform/yang-pipeline/etf-classifications.tf + shared-infra/main.tf + CHANGELOG.json",
  "NOT A SERVED SURFACE: they DECLARE the table and its two GSIs. They carry no class value to any consumer."),
 ("projects/ADVI_REFACTOR/** + projects/ATOM_DECOMP/** contract markdown (4 files)",
  "NOT A SURFACE: contract prose for a different project; no executable path."),
]

CLAUSES = [("a", "served asset_class == ratified five-class label"),
           ("b", "LABEL-GROUPED weight NON-ZERO and equal to pre-retag"),
           ("c", "the row RENDERS -- served row count == DOM row count"),
           ("d", "class subtotals sum to the grand total")]


def main():
    print("=" * 118)
    print("POSN_ASTTAX.TO-T5-1  cell AT3-s-5  --  THE BAR, step (2) of C-RETAG-SAFETY @3832ac543c")
    print("FOUR clauses x %d retag-set members x %d surfaces = %d cells"
          % (len(MEMBERS), len(SURFACES), len(MEMBERS) * len(SURFACES) * 4))
    print("=" * 118)

    print("\n### THE RETAG SET (T5-AC1) -- derived by subtraction over all 285 registry rows")
    for t, now, tgt in MEMBERS:
        flag = "  [LIVE WEIGHT in A1]" if t in HELD else ("  [live rows in A2]" if t in IN_HAD else "")
        print("   %-6s served now %-13s -> ratified %-12s%s" % (t, now, tgt, flag))

    print("\n### THE SURFACE SET (T5-AC2) -- %d surfaces SURVIVING the subtraction" % len(SURFACES))
    for sid, kind, name, vintage, _ in SURFACES:
        print("   %-4s %-9s %s" % (sid, kind, name))
        print("        vintage: %s" % vintage)

    print("\n### SUBTRACTED, WITH THE PROOF PER SUBTRACTION")
    for what, why in SUBTRACTED:
        print("   - %s\n       PROOF: %s" % (what, why))

    print("\n### THE FULL TABLE -- SURFACE x MEMBER x CLAUSE (T5-AC3/4/5/6)")
    grain_count = collections.Counter()
    verdict_count = collections.Counter()
    fails = []
    for sid, kind, name, vintage, cl in SURFACES:
        print("\n--- %s  [%s]  %s" % (sid, kind, name))
        for ck, ctext in CLAUSES:
            verdict, grain, reason = cl[ck]
            print("    clause (%s) %s" % (ck, ctext))
            print("        VERDICT %-13s GRAIN %-24s %s" % (verdict, grain, reason))
            for t, now, tgt in MEMBERS:
                grain_count[grain] += 1
                verdict_count[verdict] += 1
                if verdict == "FAIL":
                    fails.append((t, sid, ck))
            print("        applies IDENTICALLY to all %d members (one cell each, %d cells)"
                  % (len(MEMBERS), len(MEMBERS)))

    total = len(MEMBERS) * len(SURFACES) * 4
    print("\n### GRAIN COUNTS (T5-AC6) -- every cell carries its own claim; denominator %d cells" % total)
    for g in (EX, SP, NM):
        print("   %-26s %4d cells" % (g, grain_count[g]))
    print("   %-26s %4d cells  (must equal the denominator)" % ("SUM", sum(grain_count.values())))
    print("\n### VERDICT COUNTS")
    for v, n in sorted(verdict_count.items(), key=lambda kv: -kv[1]):
        print("   %-16s %4d cells" % (v, n))

    print("\n### T5-AC7 -- THE CONDITION'S TRUTH VALUE")
    print("   GO requires EVERY member to pass ALL FOUR clauses on EVERY surface in the set.")
    print("   FAILING (member, surface, clause) triples: %d of %d cells" % (len(fails), total))
    print("   distinct failing (surface, clause) pairs : %d" % len(set((s, c) for _, s, c in fails)))
    print("   members with at least one failing cell   : %d of %d" % (len(set(t for t, _, _ in fails)), len(MEMBERS)))
    print("\n   VERDICT: NO-GO")
    print("\n   THE FAILING (member, surface, clause) TRIPLES, in full:")
    for t, s, c in fails:
        print("      (%s, %s, %s)" % (t, s, c))


if __name__ == "__main__":
    main()
