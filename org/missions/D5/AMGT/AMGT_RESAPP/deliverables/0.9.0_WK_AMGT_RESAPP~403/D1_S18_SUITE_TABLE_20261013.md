# D1-S18 suite table

SUITE-BEFORE: files 462 | pass 1386 | fail 6 | skip 27
SUITE-AFTER: files 462 | pass 1389 | fail 3 | skip 27

Measured with `bun test` from the portal root at DEV 0a06280a (before) and at portal commit 4477deca (after). Each run took about 190 s and reported 1,419 tests across 462 files.

### iv-e-46.class-readers.test.ts
CAUSE: measured two NAMED citations pointing at lines that no longer contain the word alternatives: _shared/perfrp/PerfrpAllocation.tsx:44 (the word is at :46) and _shared/types.ts:1561 (the word is at :1565); the reason-text cite :1608 moved to :1612. Edited to match; the file passes after the edit (the AC1 targeted run reads 13 pass, 0 fail across the three files).
CLASS: STALE-CITATION

### iv-e-115.vendor-section-names-units.test.tsx
CAUSE: measured the pinned census docs/briefs/sources/YCHARTS_COMPARISON_REPORT_FIELD_SCRAPE_20260909.json, hashed at test time against CENSUS_SHA256 and pinned by CENSUS_PIN in contracts/vendorSectionNames.ts; both constants still held the pre-a1b500eb1f values. Set CENSUS_PIN to a1b500eb1f53349445dc6669672ba408cd6d49a1 and CENSUS_SHA256 to 053560a14bd5d5b2a95a25c641062c1bdcfeaca08d4d476075bd2e3891d7e831; the test passes after.
CLASS: PIN-DRIFT

### producer-fixtures.test.ts
CAUSE: measured the portal copy fixtures/wire/HoldingsSnapshot.valid.json at DEV 0a06280a (2608 bytes) lacked one line, an account_id on a node, that the infra source carries (2662 bytes). Copied the source over byte-identical (cmp returned identical); the test passes after.
CLASS: GENERATED-DRIFT

### iv-e-26.wire-regen.test.ts
CAUSE: measured the gen-wire.ts regeneration is not byte-identical to the committed HoldingsSnapshot (test diff Expected -1 / Received +3). The committed wire TypeScript has no multi_asset, while the frozen v1 schema docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json carries it at 5 lines. Not re-run here: the generators were not executed.
CLASS: CONTRACT-ENUM

### iv-e-48.new-classes.test.tsx
CAUSE: measured VERDICT NEW-CLASSES-FAIL: wire union [alternatives,cash,commodities,equity,fixed_income,other,structured,unclassified] != contract enum [alternatives,cash,commodities,equity,fixed_income,multi_asset,other,structured,unclassified]; the committed wire union lacks multi_asset.
CLASS: CONTRACT-ENUM

### iv-e-98.generators-drift.test.ts
CAUSE: measured the wire folder is not pure generator output: regeneration is not byte-identical for HoldingsSnapshot.ts, the only file the test names (the same drift as iv-e-26). Still red after this cell, as the order requires.
CLASS: GENERATED-DRIFT

## DECISION
Regenerating the wire folder (bun src/pages/InvestorReporting/__tests__/fe-s-13/gen-all.ts) is the CTO's decision, and this cell did not run it.
Per the order's analysis (not re-measured here): it turns GREEN iv-e-26.wire-regen, iv-e-48.new-classes and iv-e-98.generators-drift, the three current reds.
It turns RED dsgn-irptv1/iv-e-148.multi-asset-class-readers.test.ts arm (d), which passes today: the wire type must admit no retired token.
Both cannot hold while the frozen v1 HoldingsSnapshot schema carries multi_asset (measured at 5 lines).
Left UNTOUCHED: the wire folder, gen-wire.ts, gen-consumed.ts, and the iv-e-26, iv-e-48, iv-e-98 and iv-e-148 test files.
Still failing after this cell: iv-e-26 (IVE26-AC3), iv-e-48 (IVE48-AC1), iv-e-98 (IVE98); 3 fail.
Input to the decision: Andrew's 2026-10-07 "there should be no multi-asset class".
Decision owner: the CTO.
