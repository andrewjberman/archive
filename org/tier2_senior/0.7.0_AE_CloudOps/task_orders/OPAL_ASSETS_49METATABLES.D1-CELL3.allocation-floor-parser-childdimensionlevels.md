# D1 cell-3: bd49f allocation column-floor parser -- childDimensionLevels envelope (INERT CONTROL fix)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>1.0.0_SA_CTO (131908Z, DS D1 co-read finding 131819Z routed)</issued_by>
<date>2026-07-15</date>
<status>staged-fix-authored -- SWAP GATES ON TONIGHT 22:00Z CLEAN VERDICTS (CTO 163603Z)</status>
<!-- PROGRESS 2026-07-15 ~16:4xZ (0.7.0): AC1+AC2 MET. Fix authored + committed 459ded842 (_selected_dim_floor now walks levels + parentDimensionLevels + childDimensionLevels, family-agnostic; collision-safe max). EXERCISED on the REAL probe bodies: allocation_390224 floor 0->70 (census {Relationship:7, Portfolio Group:2, Portfolio:26, Account:70}); fees_435407 unchanged 21 (census {Transactions:3, Relationship:1, Account:21, Holding:4}) -- NO regression. commit-gate clean. Artifact STAGED: build-verified sha tj4T5e1B, source-map 8c39c7fcc, plan bd49f-cell3-swap.tfplan = 0/1/0 (source_code_hash only). SWAP HELD: live sha still Ir0PmpFI (unchanged) -- apply gated on tonight's 22:00Z ETF/0833 verdicts reading clean per CTO; 02:30Z fire = natural runtime-confirm (AC3) post-swap. AC4 swap+session-log on apply. -->
<priority>BEHIND everything parity-critical (delta-7, ES-1, Amendment-2, any 0833/orion/etf work). TRACKED, not dropped. No ledger urgency -- normal fix once the parity push clears.</priority>
<project>OPAL_ASSETS_49METATABLES (D1 Apply B, opal-assets-bd49f-daily-pull)</project>

## THE GAP (inert control, verification law 4 -- a guard nothing enforces is no guard)
`_selected_dim_floor()` in `infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py`
iterates ONLY `full.get("levels")` with `dim.get("isSelected")`. That is the fees_435407 (queryType
Transactions) envelope shape -- correct there: sidecar shows selected_dim_floor=21 + full census
{Transactions:3,Relationship:1,Account:21,Holding:4}.

But allocation_390224 (queryType Allocation) uses a DIFFERENT envelope: `parentDimensionLevels` +
`childDimensionLevels` (parent/child), each carrying `dimensions[].isSelected`. It has NO flat `levels`
array, so the parser returns selected_dim_floor=0 + level_selected_census={} -- the column-floor
assertion for the allocation feed runs against a floor of 0 and trivially passes anything.

## WHY IT DID NOT BITE (07-15 02:30Z first fire)
column_extent=92 landed, exceeding DS's measured 70-col floor -- export complete, NOTHING BAD LANDED.
This is NOT a data defect and NOT a cert blocker. It is a control that is decorative for exactly the
feed whose columns matter most (the D1 fee substrate): a future 390224 export silently dropping its
advisor/fee columns would NOT be caught by a floor of 0.

## THE FIX (scoped, DS-evidenced)
Extend `_selected_dim_floor` (and the census it returns) to ALSO read the childDimensionLevels shape:
`parentDimensionLevels` + `childDimensionLevels`, each `dimensions[].isSelected`, the same way it reads
`levels[].dimensions[]`. Keep the flat `levels` path for the Transactions shape (both must work -- the
parser is family-agnostic). Expected allocation floor after fix: 70 (the Account childDimensionLevel's
selected count; portfolio parent level = 26).

## <acceptance_criteria>
1. `_selected_dim_floor` returns floor=70, census populated (Account 70 / portfolio-parent 26) for the
   390224 Allocation body; STILL returns 21 + full census for the 435407 Transactions body (no regression).
2. Exercised on the REAL landed probe body `blackdiamond/49f/_ops/probe/20260714T171101_template_390224.json`
   (childDimensionLevels[1] = Account level, 70 selected) -- not just a synthetic.
3. Next scheduled 02:30Z fire's allocation sidecar shows selected_dim_floor=70 (was 0), census non-empty.
4. commit-gate clean; artifact-swap through the standard vehicle (CTO gate); session-log Compiler Tools.
</acceptance_criteria>

## Evidence pointers
- DS finding 131819Z; CTO priority ruling 131908Z (names it in the parity cert as a residual, 0.7.0 owner).
- Template structure: `blackdiamond/49f/_ops/probe/20260714T171101_template_390224.json` (childDimensionLevels).
- Sidecar contrast: 390224 (floor 0, census {}) vs 435407 (floor 21, full census) on the 07-15 02:30Z fire.
