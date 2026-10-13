# IRPT_BCKEND round 173, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~06:0xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued @ca2f4a6d3a on the CTO's ROUND-173 ANALYSIS (msg 6798); IB-pr-504 amended once @5a8d46331a (the issuer's grant omitted four fixtures).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 173 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). The issuer re-ran every criterion itself: IB173-1 AC1-AC3 PASS on the merged tree; IB173-2 AC1-AC3 PASS in the worker's worktree at portal `c8c668c0` (its portal repo lives there).
Push state: LOCAL. Merges `317311364d` (IB-pr-503) and `69394053a4` (IB-pr-504, workspace side) are on `box/dell2`, not read on origin at this writing. The portal candidate `wk-IRPT_BCKEND-355-portal` @c8c668c0 (on top of `-353-portal` @e1cd356e2f) is LOCAL and not pushed.

| order | what it did | landed | criteria (issuer re-run) |
|---|---|---|---|
| IB-pr-503 | OFFLINE replay of the packaged `irpt-holdings` serve path (36 members re-hashed to the source map's pins) on a synthetic snapshot: a node with `account_id`, without it, and with an unknown member | @317311364d | 3 of 3 PASS (the check re-runs the worker's script) |
| IB-pr-504 | the frozen export envelope carries `facts.covered_account_ids` (the wire's synthetic list), validated against the v1 `ExportReceipt` schema; the generator reproduces it, and so do the four fixtures that clone the envelope (three holdings maps, the fe-s-32 no-answer map) | workspace @69394053a4; portal `wk-IRPT_BCKEND-355-portal` @c8c668c0 | 3 of 3 PASS (six consuming tests 28 pass, 8 skip, 0 fail) |

## What the CVO needs to know

- **The `irpt-holdings` serve path passes a node carrying `account_id` through unchanged** (and passes an unknown member through too): `project()` copies each kept node whole (pinned `snapshot.py:356`, which I read) and nothing between load and response filters node keys; the one validator has no serve caller (round 172). Together with round 172's finding, **nothing on the Lambda side blocks the builder's `account_id`**: no packaged copy validates, and the serve path carries the member. What remains before the builder first writes it: its host bundle (which also carries the 49F temp-file fix) and its never-widen pair, once the host is next Online. The `irpt-directory-search` apply (round 171's signed pair) is separate.
- **A finding I filed in row S127, for the CTO:** the portal test `IVE48-AC1` now fails because the v1 contract enum regained `multi_asset` (dell1's TO-SC-e100, `7d49d6cc6d`, reached this branch at ~05:1Z) while the portal's wire fixtures carry no `multi_asset`. The full portal folder reads 1212 pass, 27 skip, 5 fail against the earlier 1213/27/4; the fifth failure is that test, which also fails alone at the worker's portal HEAD, so IB-pr-504 did not cause it. The fix (the wire union and its type move together, or the test names the producer's six) is a portal-owned decision, asked of the CTO.
- **Portal candidates awaiting the DEV review lane:** `-346-portal` @8fe39d63, `-350-portal` @69f69895, `-353-portal` @e1cd356e2f and `-355-portal` @c8c668c0 (355 contains 353). 346 and 350 both touch five `fe-s-15` job files (merge both at the landing).

## Rows

- **STILL ARMED, owner me:** W345-S3 (the fix is in merged code; the host bundle is not redeployed; the host is stopped, so no new file is written; IB-pr-497 is parked), W348-S2 (the `irpt-holdings` schema at HEAD also enables `include=target` and narrows three enums: not re-pinned), W346-S2, W346-S3 and W350-S1 (the portal generators drift at DEV until the candidates land). Row `D2-S127` carries the reasons.
- **Disarmed:** W354-S2 (the serve path validates nothing: the repo schema admits the optional `account_id`, so the line serves no invalid bytes). Closed: W355-S1. Observations: W354-S1, W355-S2 to S5.

## Issuer defects this round (mine)

- IB-pr-503's order named `snapshot.project(snapshot, scope, include=())`; the packaged `project()` takes no `include` argument (row W354-S1). IB-pr-504's grant omitted four fixtures the generator also writes (row W355-S1). Gate limb for the 504 amendment: none graded (order text only; placeholders NONE).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
