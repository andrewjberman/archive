# IRPT_BCKEND round 174, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~07:0xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued @6e3cbe050a on the CTO's ROUND-174 ANALYSIS (msg 6812). IB-pr-506 was amended twice (@8207e46109: the optional `account_id` node member; @e06aa7cb6a: the six-class direction after the CTO's amendment @cbcc4a88b8).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 174 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). `python .tools/prd-signoff.py status IRPT_BCKEND`: v0.53 ADMITTED; the ratified-text half shows SIGNED at the earlier hash and "text CHANGED since signed" (the v0.53 contract line), so the CVO's re-sign of that half is open.
The issuer re-ran every criterion itself: IB174-1 AC1-AC3 PASS on the merged tree; IB174-2 AC1-AC3 PASS in the worker's worktree at portal `63b31b0c` (its portal repo lives there).
Push state: LOCAL. Merges `50fc1010d5` (IB-pr-505) and `7c14d46b59` (IB-pr-506, workspace side) are on `box/dell2`, not read on origin at this writing. The portal candidate `wk-IRPT_BCKEND-357-portal` @63b31b0c is LOCAL and not pushed.

| order | what it did | landed | criteria (issuer re-run) |
|---|---|---|---|
| IB-pr-505 | READ: the builder validates its own snapshot against the repository's v1 schema before any write (`run_firm` calls `validate_snapshot`, then raises `REFUSED`; `land`'s hook and `publication.py:232` validate again before the first put); a new 5-arm test plants an unknown ACCOUNT-node member and the build refuses with zero puts. No product edit | @50fc1010d5 | 3 of 3 PASS |
| IB-pr-506 | the portal keeps SIX classes: the wire generator subtracts the retired set `{multi_asset}`; `IVE48-AC1` asserts wire == contract enum minus `{multi_asset}`; the adapter shows a served `multi_asset` as unclassified and logs it; `iv-e-148` untouched | workspace @7c14d46b59; portal `wk-IRPT_BCKEND-357-portal` @63b31b0c | 3 of 3 PASS (whole folder 1219 pass, 2 fail; tsc 0 errors) |

## What the CVO needs to know

- **A conflict with Andrew's word was caught and not decided by me.** The CTO first ruled (RE 6807) that the portal wire follows the contract's enum with `multi_asset`; regenerating failed the portal test `iv-e-148`, whose header quotes Andrew-direct 2026-10-07 ("there should be no multi-asset class. There are 6 classes"). I stopped, put the contradiction to the CTO, and the CTO withdrew the ruling (RE 6818): six classes in the product, the contract's bytes unchanged (v1 keeps `multi_asset` only as a retired member). Nothing went to Andrew.
- **The builder side of "enforced at build, not at serve" is now proven by a test.** The account_id line has nothing left on the Lambda side: no packaged copy validates (round 172), the serve path passes the member through (round 173), the builder validates before it writes and refuses a stray member (this round). What remains before the builder first writes `account_id`: its host bundle (which also carries the 49F temp-file fix) and the never-widen pair, once the host is next Online.
- **Portal candidates awaiting the DEV review lane:** `-346-portal` @8fe39d63, `-350-portal` @69f69895, `-353-portal` @e1cd356e2f, `-355-portal` @c8c668c0 (contains 353) and `-357-portal` @63b31b0c. 346 and 350 both touch five `fe-s-15` job files.

## Rows

- **STILL ARMED, owner me:** W345-S3, W348-S2, W346-S2, W346-S3, W350-S1, as in rows `D2-S126` and `D2-S127`. Row `D2-S128` closes W357-S4 and S5 (superseded) and records the observations: W356-S1 to S3 (the validation call is in `run_firm`; `land` writes a local file before its hook when called directly, not S3; a pre-existing import-order defect in `test_runner_jsonschema_tolerance.py` stops a combined pytest at collection) and W357-S6 to S8.

## Issuer defects this round (mine)

- IB-pr-506's refusal clause named `multi_asset` alone, but the regeneration also adds the contract's optional `account_id` node member (row W357-S1): amended. I named the validation call "in main"; it is in `run_firm`, which `main` calls (W356-S1).
- Gate limb for the amendments: none graded (order text and check files; placeholders NONE).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
