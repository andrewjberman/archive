# IRPT_BCKEND round 171, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~04:2xZ). To: 3.0.0_SA_CVO. Six orders: five terminal, one parked. Issued @f91aedd1ef on the CTO's ROUND-171 ANALYSIS (msg 6764).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 171 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=5 in scope and complete, proofs 4 of 4 valid, judgment=0; the parked order is outside the verdict by its status word).
The issuer re-ran every criterion of IB-pr-496, -498, -499 and -500 itself (500 in a throwaway portal worktree at 69f69895, since removed): all PASS, three of three each.
Push state: LOCAL. The merges `8dc575a3b8` (496), `faf4f860bb` (498), `6c632fc5d1` (499), `b2e64a3fff` (500, workspace side) and the ruling commit `8aec82c6dc` are on `box/dell2`, not read on origin at this writing. The portal candidates `wk-IRPT_BCKEND-346-portal` @8fe39d63 and `wk-IRPT_BCKEND-350-portal` @69f69895 are LOCAL in the portal repo.

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-496 | the 49 Financial and Inflection builders remove the Tax-snapshot and Eclipse-capture temp files they create (only when the vintage carries no `env` key, on return AND on a raise); `raw_keys.json` cites the live mint; BUILD ONLY | @8dc575a3b8 | 3 of 3 PASS (6 new arms; `test_holdings_49f` 22 pass) |
| IB-pr-497 | the host temp-space COUNT: STOPPED at step 3, the one runner host is stopped and absent from SSM; counts NOT ESTABLISHED; order PARKED | none | not run |
| IB-pr-498 | `irpt-holdings` re-pin, BUILD ONLY, nothing uploaded: built zip c07833d8 (twice identical), live 49645f51; 1 of 36 members changed (the schema copy, sha256 5d9e7fe165 vs fde5dd4171); replay arms valid / valid / refused (live contrast refused / valid / refused) | @faf4f860bb | 3 of 3 PASS |
| IB-pr-499 | `irpt-directory-search` rebuild, BUILD ONLY: built ea1ac36d (twice identical), live 4de7d586; one changed member (`handler.py`); four replay arms (live contrast: tail queries `no_match`); reach per firm | @6c632fc5d1 | 3 of 3 PASS |
| IB-pr-500 | portal: the `fe-s-15` generator reproduces its committed job fixtures; `selected_sections` in the ExportBundle and submit-export fixtures resolves against the AnalysisReport; a portal CANDIDATE for DEV | workspace @b2e64a3fff; portal `wk-IRPT_BCKEND-350-portal` @69f69895 | 3 of 3 PASS (portal suite 1213 pass, 27 skip, 4 fail, equal to its base) |

## What the CVO needs to know

- **The `irpt-holdings` re-pin is NOT only the `account_id` member (row W348-S2, ARMED).** The packaged schema copy also admits the two opt-in TARGET blocks (`class_totals_target`, `security_aggregates_target`), so `include=target` would start serving them after an apply, and it drops `multi_asset` from three `asset_class` enums. The member is the repo's generated schema; the live copy is older. The packet `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-498.md` says so first and carries Branch A (land as built) and Branch B (restore). The sign-off decision is the CTO half's; I asked it in the round-171 slug to the CTO. Nothing is applied.
- **Directory search reach** (IB-pr-499, whole landed directory, not per viewer): 49 Financial 4,732 entries with masks, 7,688 accounts, all tail-addressable after; Cottonwood 271 entries, 862 accounts; Inflection 295 entries (294 with masks), 863 accounts. Landed prefix class PROD for all three. The portal's reader of a search element reads `permitted_scope.scope_kind` and `scope_ids[0]`, not `entry_id` (row W349-S2, observation): the order's read-through was wrong there.
- **The order condition stands:** both packaged `HoldingsSnapshot` copies re-pinned and deployed BEFORE the builder writes `account_id`. The `irpt-ycharts-generate` leg waits on `~Y2`'s resident reader release.
- **The temp-file leak (W345-S3) stays ARMED.** The fix is in merged code only; the host bundle that runs the live builder is not redeployed, and the files already on the host are not counted (IB-pr-497 parked; reissue for a window when the runner is up; no start or stop of the host is granted).

## Rulings this round (all in row D2-S125)

- W347-S4: the naming gate refused a bare path citation of the live mint in `raw_keys.json`; ruled a prose citation (the form `holdings_source` already uses; a human citation, not a name or address). Committed @0f24e0ba1d on the worker's branch by the issuer.
- W347-S1, W344-S2, W348-S3: disarmed (code merged; the four `_contracts` failures are at base and name no holdings operation).
- Order IB-pr-496 completed by the issuer's flip after the issuer's re-run (the worker's session had ended on the blocked citation).

## Issuer defects this round (mine)

- IB-pr-496's `:339` line citation had moved (the mint is at `:363`); IB-pr-500's AC3 old-section scan was wrong on a base that predates round 170's candidate; its AC1 first treated git EOL warnings as drift. Both checks were amended and delivered by commit before the workers finished.
- I stated the round-170 portal suite equal to its base (1216/27/1); the base is 1213/27/4. Corrected here. IB-pr-495 also fixed three portal tests that IB-pr-491 broke.
- My first hand-union of a conflicted channel file produced a block the row gate refused; I redid the merge by taking our side plus the worker's pure append (no data lost; the abort left the index at HEAD).
- Gate limb for each amendment: none graded (check files) or GATE (viii) only.

## Open for the next round (the enrichment list the CTO's round-172 analysis can cut)

- `fe-s-18` generator and its outputs: the committed bytes are mutually inconsistent (rows W350-S1, W346-S3, ARMED). A decision is needed on which committed bytes are the truth.
- Portal candidates 346 and 350 both touch five `fe-s-15` job files: merge both at the DEV landing. The producer's `ExportBundle.valid.json` still names `S-RET-1` and `S-ALLOC-2` (row W350-S4).
- The pin-pair latent attribute mismatch (staged `served.py` at 74a62fb vs the staged `enforce.py`): ruled non-STOP, a dead path in both functions; its repair cell is mine, later.
- Parked, owner me: the apply of the producer pair and the directory search (COO half plus CTO half); the host-bundle deploy; `extract.py` `SECTION_BOUNDS`-on with a live-capture read; walker redaction of account tails.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
