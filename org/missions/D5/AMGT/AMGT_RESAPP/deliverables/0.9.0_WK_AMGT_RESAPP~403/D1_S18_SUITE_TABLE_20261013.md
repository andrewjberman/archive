# D1-S18 suite table

SUITE-BEFORE: files 462 | pass 1386 | fail 6 | skip 27
SUITE-AFTER: files 462 | pass 1392 | fail 0 | skip 27

Measured with `bun test` from the portal root. BEFORE: DEV 0a06280a, the run taken by the first seat of this slot (6 fail). AFTER: portal commit c26e0c68 (the five edits), run by this seat (`Ran 1419 tests across 462 files`, 0 fail). The AC1 seven-file run reads 23 pass, 0 fail.

### iv-e-46.class-readers.test.ts
CAUSE: measured the two NAMED citations at DEV 0a06280a: _shared/perfrp/PerfrpAllocation.tsx line 44 and _shared/types.ts line 1561 no longer carry the word alternatives (it sits at :46 and :1565); the reason-text cite :1608 had moved to :1612. Edited to match; the file passes after the edit.
CLASS: STALE-CITATION

### iv-e-115.vendor-section-names-units.test.tsx
CAUSE: measured the pinned census docs/briefs/sources/YCHARTS_COMPARISON_REPORT_FIELD_SCRAPE_20260909.json, which changed at commit a1b500eb1f (TO-IV-e-118), while CENSUS_PIN and CENSUS_SHA256 in contracts/vendorSectionNames.ts still held the old values. Both moved to the a1b500eb1f census; the test passes after.
CLASS: PIN-DRIFT

### producer-fixtures.test.ts
CAUSE: measured the portal copy fixtures/wire/HoldingsSnapshot.valid.json at DEV 0a06280a lacked the account_id line that the infra source carries on a consumed node field. Copied the source over byte-identical; the test passes after.
CLASS: GENERATED-DRIFT

### iv-e-26.wire-regen.test.ts
CAUSE: measured the committed wire folder was not gen-wire.ts output: the regeneration differed from the committed HoldingsSnapshot.ts by 7 lines added and 6 removed, because the frozen v1 schema carries multi_asset. Regenerated with gen-all.ts (commit c26e0c68); the test passes after.
CLASS: CONTRACT-ENUM

### iv-e-48.new-classes.test.tsx
CAUSE: measured at DEV 0a06280a the wire union lacked multi_asset, which the contract enum carries (VERDICT NEW-CLASSES-FAIL). The regenerated HoldingsSnapshot.ts adds multi_asset to the wire union; the test passes after.
CLASS: CONTRACT-ENUM

### iv-e-98.generators-drift.test.ts
CAUSE: measured the same one-file generator drift at DEV 0a06280a (HoldingsSnapshot.ts, 1 of 28 files). Regenerating the wire folder with gen-all.ts removes it; the test passes after.
CLASS: GENERATED-DRIFT

## DECISION
RULED by CTO~DELL1 msg 4899 (2026-10-13): regenerate the wire folder, and relax arm (d) of iv-e-148.
Regenerating turned green iv-e-26, iv-e-48 and iv-e-98 (the three wire-contract reds).
Unrelaxed, it would have turned iv-e-148 arm (d) red, because the frozen v1 wire type carries multi_asset (MDPF_SECCLASS restored it at 506096fc9a).
Relaxed arm (d), now titled "the frozen v1 wire type may carry the retired token only inside a class enum": the token may appear only inside a class enum, so it is counted against the enum lines, not required to be absent.
Every reader still maps the token to unclassified (arm a); the colour registry and the lists stay six (arms b, c, e); SECCLASS's producer test proves no row emits it.
Andrew's 2026-10-07 word ("no multi-asset class, 6 classes") is about classes and is kept by arms (a), (b), (c), (e).
Relaxed arm (d) is in commit c26e0c68; gen-wire.ts, gen-consumed.ts and the iv-e-26, iv-e-48, iv-e-98 tests are untouched.
