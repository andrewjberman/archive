# IRPT_BCKEND round 1, workstream ~PC (the S158 READ: why Cottonwood's holdings are stale) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~11:2xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @1713c505c1 on the CTO's msg 8020 and row D2-S158: IB-pr-569 `complete` (merged @f7ae7ad352). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PC"` reads `MAY-CLOSE`. I re-ran IB209-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: nothing was published, bypassed, re-run or written to AWS. The lost account is described by class only; no id is in any tracked file.**

## What the CVO needs to know

- **My order's premise was wrong, and the worker's stop found it.** Row S158 and my order said every refusal names ONE lost account. The worker read all three refusal record versions: the first candidate (2026-10-09) names `account_lost` with count **9** (8 of them closed accounts the guard lists as not refused), the next two (2026-10-12, 2026-10-13) name count 1. My STOP clause was too tight; I amended the order (record every candidate's count, only the latest must read 1), and the sparse worktree lacked `data/` (a local, uncommitted sparse add fixed it). Cottonwood is served at 2026-10-08, four trading days behind.
- **The cause (claim `inferred`, not measured): the account is NOT closed and NOT missing from the source.** It is listed in the custodian `fact_holdings` partition on 2026-10-08, 2026-10-12 and 2026-10-13, has no directory entry (the directory holds 271 entries: 2 terminated, 269 unknown), and is dropped between the source and the candidate by the **COT account screen** (`cot_screen_accounts`, `holdings_snapshot.py` lines 2266 to 2294, which refuses an account that fails `validate_cot_actual_positions`). The failing validator condition is not measured: its reason is kept only in screen evidence.
- **The acceptance path, read in the code:** the guard is line 3058; the closed-account exclusion (line 3051) cannot apply (no directory mark); the one-date bypass waives `source_frontier_older` only and does NOT clear `account_lost` (line 3191), so it is the wrong tool. The path is a custodian-confirmed closure that sets a TERMINATED mark, or a decision of the owner to change the screen. The code names the owner only in the gate docstring (an Andrew-direct ruling, PRD v0.31 and v0.32); row S158 names the CTO.
- **Other firms:** 49 Financial is served at 2026-10-12 and DOES have a refusal record (row S158 said no firm besides Cottonwood was blocked); Inflection is served at 2026-10-13 with none. Disposition follows in the next channel row.
- **Next read (the CTO's to order or I propose):** run `validate_cot_actual_positions` offline, read-only, on the account's source rows to name the failing condition; that measures the cause.

## Judgment criteria

None this round (judgment=0).
