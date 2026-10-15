# IRPT_DASHBD round 111 (the CTO's round-110 L10 answer, msg 7858), workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~22:3xZ)

**Three orders, all drained; nothing served moved, nothing written to AWS, nothing deployed; counts, hashes and words only in the repo; the client silver, the sample, the household table and every render stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @332465706b. Drained: `DB-b-226` (~181, @edaefd57d3), `DB-b-225` (~180, @abeabca47c) and `DB-b-224` (~179, @432f218d18). On the landed tree `DB111-1-AC1`, `DB111-2-AC1` and `DB111-3-AC1` PASS, and so do all five round-110 criteria and the 14 earlier live criteria. `round-close-check` reads **REFUSED for one reason: `DB111-2-J1` is ungraded and is the CVO's** (3 orders complete, 2 of 3 proof rows accepted). Push state: `332465706b`, `edaefd57d3` and my amendments are ON origin box/dell2 (fetch read, origin @70f82239a8); the merges `abeabca47c` and `432f218d18` and this packet are LOCAL until the box-sync takes them. The portal label work is LOCAL on `wk-IRPT_DASHBD-180-portal` (not on origin).

## What the cells found

- **`DB-b-224` (the 49 Financial household daily return):** a new sibling contract `IRPT_DASHBD_HOUSEHOLD_RETURN_DAILY_CONTRACT.json` (schema hash recomputed by the stated basis), a firm-neutral pure function `compute_household_returns` and a private dry run over 570 partitions of the firm's account return gold (2024-07-08 to 2026-10-13; 4013 households, 1742 with more than one account, 6616 accounts; 207 crosswalk households dropped for having no account in the gold). **The method (amended on `W179-S1`, my error): the household's daily return is the prior-day-value weighted combination of its accounts' own `total_return_daily`**; my first cut chained summed values and flows in the endpoint form and did not reproduce the account series' linked return on carried large-flow days (4 of 5701 one-account window comparisons differed). Now **every one-account household equals its account (2176 households, 5701 window comparisons, max gap 0.0).** The range tie-out, with no tolerance assumed: QTD 3807 of 3814 compared within the range of the accounts' returns (7 outside, none at 100 bp or more); YTD 1966 of 2027 (61 outside, 14 at 100 bp or more); last 12 months 1700 of 1765 (65 outside, 16 at 100 bp or more); since inception 1297 of 1449 (152 outside, 57 at 100 bp or more; claim inferred, the read takes at most the newest 900 partitions). **NOT comparable: 199 (QTD), 1986 (YTD), 2248 (last 12 months) and 2564 (since inception) of 4013 households**: a single null account return, or an account that has no row the day after its last, makes that household day None and the product over the window None.
- **`DB-b-225` (the label rule):** the Inflection sample relabelled (a new file; every value, date and window status unchanged, every `last4` null) and the render rule (one label function, keyed by the account entry): "Account ending NNNN" only for a last four of at least 4 digits, otherwise "Account <n> of <N>"; a test feeds a word, letters and digits and a short digit run, and "ending" never precedes them. All 5 accounts read "Account 1 of 5" to "Account 5 of 5" in headers, tables, notes and footers; suite 1300 pass, the 20 failures identical to the base (this worktree's base reads 20 against round 110's 5, row `W180-S3`); lint and typecheck 0 errors.
- **`DB-b-226` (the account-number field read):** of 217 string columns over 8 silver tables and 20 partitions, 3 qualify as the custodian account number (a digit run of 4 or more on 95 percent or more of accounts, stable across sampled partitions, unique): Orion `fact_positions.accountNumber` (980 distinct values over the 980 accounts), Orion `fact_assets.accountNumber` and Eclipse `fact_portfolios_simple.accountNumber` (753 keys). The value is an identifier that holds a digit run AND other characters: the round-109 and round-110 labels were its last four characters, which for some accounts are letters. Row `W181-S1` disarmed in `D2-S45`.

## What this seat read for itself

I re-ran every criterion in each worker's tree and on the landed tree, re-validated each proof instance, scanned the changed files for identifier-length digit runs (hashes, a private path and a commit pin only), and parsed the merged channel. **I read all 20 pages of the final label render as images.** Every label is "Account <n> of 5", in the page header, the page footer, every table row and every note; there is no "ending" anywhere; every other count of round 110 holds (the gain/loss Ending Values equal the overview's, the not-spanned words, the split sentence once). Two accounts still end at $0, now "Account 1 of 5" and "Account 4 of 5". **Not a grade; `DB111-2-J1` is the CVO's.**

## Issuer errors this round (mine, disclosed)

The household method (the endpoint form, caught by the one-account clause on the real data, `D2-S46`). Everything else of this round held at the first cut.

## Rows held (owners named)

`W179-S1` (BLOCKING, ruled in `D2-S46`), `W181-S1` (ARMED, mine, disarmed in `D2-S45`). Observations only otherwise; no ARMED row has a dark owner.

## What goes to the CTO (one ask, in the slug)

The household chain is None for about half of the households in the longer windows because one unmeasurable account day nulls the whole window: may a household day whose only gap is an account with no measured return that day take the weighted return of its remaining accounts (that account outside the day's base, as a joining account is), so that those households become comparable, or must the day stay None? Carried as data facts, not asks: the account-number field above (the label can take the last four digits of the longest digit run of `fact_positions.accountNumber` next round, the CTO's own switch); the outside-range counts of the household tie-out for the CTO's ruling; the household table is private and nothing sources the report contract from it yet.

## What this does to the FWD outcomes

Inputs to `FWD-2` and `FWD-21`: neither is met. The household return now exists for 49 Financial as a measured private table with a stated method and a tie-out, one-account households equal their account, and the Inflection labels no longer claim an account number; the report contract's household return members for 49 Financial stay ABSENT until the household table is accepted and sourced. Grading is the CTO's and CVO's at L10.

## Open

**Andrew:** the as-of approval row `dell2-20261014T195533Z-90a9` (client-facing) and call a252 (the 49 Financial disclosure file). **This seat:** `DB-b-183` L3, the first scheduled D_04 run after the 12:08:39Z upload (about 23:00Z; no timer is set).

-- 2.0.0_SA_COO~D2
