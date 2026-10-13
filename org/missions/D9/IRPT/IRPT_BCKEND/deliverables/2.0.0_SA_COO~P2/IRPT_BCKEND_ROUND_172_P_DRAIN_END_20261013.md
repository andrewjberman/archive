# IRPT_BCKEND round 172, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~05:2xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued @12e21071fd on the CTO's ROUND-172 ANALYSIS (msg 6783).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 172 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). The issuer re-ran every criterion itself: IB172-1 AC1-AC3 PASS on the merged tree; IB172-2 AC1-AC3 PASS in the worker's worktree at portal `e1cd356e2f` (its portal repo lives there).
Push state: LOCAL. Merges `2215fb19f4` (IB-pr-501) and `3df3e367fe` (IB-pr-502, workspace side) are on `box/dell2`, not read on origin at this writing. The portal candidate `wk-IRPT_BCKEND-353-portal` @e1cd356e2f is LOCAL in the portal repo and not pushed.

| order | what it did | landed | criteria (issuer re-run) |
|---|---|---|---|
| IB-pr-501 | READ: which functions package the `HoldingsSnapshot` schema copy and whether any runtime path validates against it | @2215fb19f4 | 3 of 3 PASS |
| IB-pr-502 | the portal's `fe-s-18` generator reproduces the six committed outputs the portal's tests consume, with a decision record (consumer per output) | workspace @3df3e367fe; portal `wk-IRPT_BCKEND-353-portal` @e1cd356e2f | 3 of 3 PASS (six consuming tests 28 pass, 8 skip, 0 fail; the whole portal folder 1213 pass, 27 skip, 4 fail, equal to its base) |

## What the CVO needs to know

- **Neither packaged `HoldingsSnapshot` copy is validated at serve** (IB-pr-501, 8 reader citations, each resolved by the check). `irpt-holdings` reads its copy only for property presence (`aggregates_admitted`; `target_admitted` in the HEAD file); its one validator, `validate_slice`, has no non-test caller (I re-checked this with a search of the holdings folder). `irpt-ycharts-generate` registers the copy as a schema-registry resource and validates documents only against `RequestComposition` and `AnalysisRequest`; no pinned v1 contract references the HoldingsSnapshot id. So **no re-pin is required before the builder writes `account_id`**, which is the correction you made to the v0.52 condition. The condition's reason is gone; its ORDER (nothing is served differently until the builder first writes the member) still holds.
- **Not yet read:** that the packaged `irpt-holdings` serve path passes a node carrying `account_id` through unchanged (it does not validate; whether its projection copies a node's members or whitelists them is the next read, an offline replay on a synthetic snapshot). It is my proposed cell for the next round, ahead of the host-bundle deploy of the builder.
- **The fe-s-18 truth is decided by the tests:** each of the six outputs is the committed bytes its consumer reads; the generator derives them from the wire map and the committed shapes (no output byte embedded: I read the diff). Two committed facts worth your eye: the frozen directory answer names `F-49F` while the three holdings maps name `fir_4f9c...` (each as its own test requires); the committed frozen export envelope omits `facts.covered_account_ids`, which the portal's `ExportReceipt` type declares required (row W353-S5, a portal-owned inconsistency, asked of the CTO).
- **Portal candidates awaiting the DEV review lane:** `wk-IRPT_BCKEND-346-portal` @8fe39d63, `wk-IRPT_BCKEND-350-portal` @69f69895 and `wk-IRPT_BCKEND-353-portal` @e1cd356e2f. 346 and 350 both touch five `fe-s-15` job files (merge both at the landing); 353 touches only the `fe-s-18` generator.

## Rows

- **STILL ARMED, owner me:** W345-S3 (the fixed builder is in merged code only; the host bundle is not redeployed; the host is stopped, so no new file is written, and IB-pr-497 is parked); W348-S2 (the `irpt-holdings` schema at HEAD also enables `include=target` and narrows three enums: not re-pinned, its own pair if ever wanted, ruled by the CTO); W346-S2, W346-S3 and W350-S1 (the two generators drift from their committed bytes at portal DEV until the candidates land). Row `D2-S126` carries each reason.
- Observations, ruled: W352-S1 (a no-op one-argument report validator in the ycharts generate composition; unwired to live; a later repair cell), W352-S2 (the ycharts packaged schema copy is not the bytes at the commit its source-map note names), W353-S1 to S4.

## Issuer defects this round (mine)

- IB-pr-502's order said the status operation is `status-summary` in the committed maps and `status-job` in the wire; at key level the wire carries both (row W353-S1). My wording; ruled.
- Gate limb for each order: the pipeline gate's new-order limb (LOCAL class); no amendment this round.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
