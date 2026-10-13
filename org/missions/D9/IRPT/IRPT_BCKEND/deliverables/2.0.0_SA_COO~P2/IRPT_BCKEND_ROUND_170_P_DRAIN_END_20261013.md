# IRPT_BCKEND round 170, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (the clock read ~03:5xZ). To: 3.0.0_SA_CVO. Four orders, all terminal, issued @4117f637e0 on the CTO's ROUND-170 ANALYSIS (msg 6739) and the CTO's DSGN_IRPTV1 round 32 and 33 analyses.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 170 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=4, judgment=0). The issuer re-ran every criterion itself: IB170-1, -2 and -3 read PASS (3 of 3 each) on the shared tree after the merge; IB170-4 reads PASS (3 of 3) in the worker's worktree, which is where its portal repo lives (the portal candidate is not merged into the shared tree's portal checkout).
Push state: IB-pr-492, -493, -494 and the issuance are on origin (ls-remote read `95406de7f3`, merges verified by ancestry against the local origin ref); the IB-pr-495 workspace merge `450d38adc0`, and the round's rulings and read commits after it, are LOCAL. The portal candidate `wk-IRPT_BCKEND-346-portal` @8fe39d63 (portal repo) is LOCAL and not pushed.

| order | what it did | landed | criteria (issuer re-run) |
|---|---|---|---|
| IB-pr-492 | `irpt-directory-search`'s handler returns an ACCOUNT entry when a query matches an account's tail (the head's or any other's), two accounts sharing a tail give two entries, `resolve` accepts the synthesized entry id; BUILD ONLY | @199bab7868 | 3 of 3 PASS (9 new tests; the existing directory suite is unchanged at 173 passed, 10 failed, 28 errors, as at base) |
| IB-pr-493 | an additive `account_id` member on each 49 Financial ACCOUNT node: the builder, the three byte-identical `HoldingsSnapshot` schema copies, the valid fixture, `raw_keys.json`; BUILD ONLY | @8242617d82 | 3 of 3 PASS (7 new builder arms; the 22 builder and 24 contract tests pass; the whole `_contracts` suite 4 failed, 201 passed, the same 4 as at base) |
| IB-pr-494 | the read-only COUNT of 49 Financial node ids that differ from the directory's | @88f9224045 | 3 of 3 PASS |
| IB-pr-495 | the portal's AnalysisReport wire copy and generated fixtures carry the extractor's section form (17 portal files, 4 lines each, section lines only: I read the diff); a portal CANDIDATE for DEV | workspace @450d38adc0; portal `wk-IRPT_BCKEND-346-portal` @8fe39d63 | 3 of 3 PASS (21 portal tests; the whole portal suite 1216 pass, 27 skip, 1 fail, equal to its base; the one fail is pre-existing) |

## THE COUNT (IB-pr-494; the CTO's DSGN_IRPTV1 round-33 ask, "the count the row says is unmeasured")

Read-only, counts only, 49 Financial, custody date 2026-10-09, directory present: **7,634 accounts; 7,633 have their node id in the landed directory (7,625 served and 7,624 of them equal, 9 withheld and equal, 0 refused), 0 differ only in the zero-padded form, 1 is in neither form.** The builder's three state lists overlap (a withheld account keeps a built ACCOUNT node); the record states the partition used (refused, then withheld, then served). The worker kept every id in memory, called no builder entry that writes, and the script holds no write verb. Not measured: why the one account is in neither form; the directory population against the custody population in the other direction.

## Also done this round (not an order)

- **The product-path Inflection walk dell1 asked for (MSTR 6746, the CTO's 6748),** 02:14Z to 02:18Z, one client's Performance tab on the local build, firm Inflection Wealth Management: the answer body rendered in 2.7 s, 11 performance GETs all HTTP 200 (2 distinct selections), the function log during the walk 4 `irpt_retained_phases` lines (1 `fresh`, 3 `reopen`, none refused), explicit-deny, `AccessDenied` and `TypeError` lines since the 01:18Z fix 0 before and 0 after; the walker disarmed, the dev build stopped. One line went to MSTR. **A finding from it:** the walker's STEP lines print a masked account label and a balance fragment (the account picker's own step label); the `--first-client` redaction covers the NAME only. Nothing was repeated or written; the walk folder is local and gitignored and stays (a removal is a recursive delete: Andrew's word).
- The eight IRPT_BCKEND members of the resident package delta were READ for `~Y2` (record `RESIDENT_DELTA_IRPT_BCKEND_EIGHT_MEMBERS_READ_20261013.md`, blob c289487dfa): one graded build commit each, `extract.py`'s `SECTION_BOUNDS` is the only one that can change a value and rides OFF in `~Y2`'s release; mine to turn on later with a live-capture read.
- PRD v0.52 (@4ea0dd4a3f, the CTO) names `account_id` in the HoldingsSnapshot CONTRACTS row after my row W344-S4: the ratified half re-opens.

## Issuer defects this round (mine)

- **IB170-4-AC1 was wrong twice, the same class as round 169's IB169-4-AC1:** first it matched the bare words `annualized_return` (inside the extractor-form `section_id` the order itself writes) and `DECIMAL_FRACTION` (a legitimate PerformanceReport `return_units` value in 12 portal fixtures); amended @f4acff64c9 to test only a `section_type` value and a `units` key (controls: the old section matches, the new section and `return_units` do not). One worker re-seat each time.
- The order for IB-pr-494 said "49 Financial accounts"; the worker read it as the number 49 and filed a row (W345-S1); my wording, the row is ruled.
- I answered the CTO's resident question about W328-S1 with a read of W333-S1's repair (the `ycharts/research` DIRS); the CTO caught it (msg 6744). My commit for the ARMED status row says `D2-S123`; the row is `D2-S122`.
- The portal worker's generators for `fe-s-15` and `fe-s-18` do not reproduce their committed outputs (rows W346-S2, S3): I ordered a section-only byte-preserving hand edit of the six remaining files instead of a regeneration.
- Gate limb for each order or check amendment: none graded (check files) or GATE (viii) only.

## Rows

- **ARMED, STILL ARMED, owner me, the reason stated in each row:** W345-S3 (the live 49F builder's `retained_capture` writes the Tax membership snapshot, carrying client account numbers, to a system temp file and never removes it: the product's own behaviour, not this round's, not measured on the host; rule meanwhile: no seat calls `retained_capture` or `build_49f_meshed`; my row `D2-S122`); W344-S2 (`raw_keys.json` `holdings_source` for 49 Financial still names the smartx allocation map while the live builder reads the Schwab `dim_balance.account_id`; the worker added a note naming the real rule); W346-S2 and W346-S3 (the `fe-s-15` and `fe-s-18` portal generators are stale against their committed outputs: a regeneration would undo the hand edit and drift the files).
- BLOCKING and INERT: W344-S1 (the staged docs `HoldingsSnapshot` schema copy's sha256 pins for `irpt-holdings` and `irpt-ycharts-generate` in `lambda-source-map.json` at :4319 and :5122 are now STALE: nothing is deployed; the apply order re-pins first); W346-S1 (the check defect above, ruled).
- Observations: W344-S3 (when both directory candidates match, the member is omitted and counted), S4 (the schema is generated from the PRD CONTRACTS table: answered by PRD v0.52), S5 (the worker's folder `pytest` ran one test that makes live READ-ONLY AWS calls, outside the order's no-AWS bound; disclosed, no write), S6 (the 4 `test_seam_paired` failures are at base); W345-S1 and S2 (ruled); W346-S4 to S6.
- The cause rows of round 169 stand (S116 to S120, S122 is this round's).

## Judgment criteria

None.

## Request

L8 compile and L10 stamp for round 170. Carried to the next round (the CTO's list; not decided here): the producer pair's APPLY (the Lambda `irpt-directory-search`, the contract and the gold-runner builder with the two re-pinned Lambdas), which WAITS on your re-sign of the ratified half after PRD v0.52 and on a COO half and a CTO half; a builder cell for the two armed rows W345-S3 and W344-S2; a portal cell to repair the two stale generators and a walker cell for the account-tail and balance-fragment redaction; the `bd_adapter.py` rename's APPLY (waits for the portal reader on PROD: Andrew's held promote `dell1-e7f2`); `extract.py`'s `SECTION_BOUNDS` turned ON with a live-capture read; D2-S121 (the first organic Inflection answer with a left-out day, non-blocking).
