# AMGT_RESAPP round 120 -- the issuer's interim reads (`2.0.0_SA_COO~R1`, 2026-10-18 ~14:2xZ)

Push state of every commit named: LOCAL on box/dell1, unread. This file records reads taken between merges; the round's own packet (`round120/DRAIN_END_PACKET.md`) restates what survives to the end.

## 1. The merged tree after `ca-3` (`dda778e2f8`) and `ca-1` (`a1eb3b86ce`)

`python -m pytest lib/research/print/tests lib/research/api/tests lib/research/management/tests -q` in the full tree (shared checkout, head `41cfc89d0a`): **`9 failed, 1603 passed, 13 subtests passed` in 288.7 s**. The nine FAILED lines are the same nine as every round since 116 (the print folder's `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` and eight api tests: `test_feed_and_names_an3`, two in `test_fiscal_scope_contract`, `test_11` and `test_15` of `test_generation_and_pool_routes`, `test_price_windows_route`, two in `test_r82_reason_and_mentions`). The management folder (added to the run this round, because `ca-1` re-scoped readers it tests) adds no failure. Output: `C:/dev/ui-walk-evidence/r120-merged13-tests.txt` (client data stays local; none here).

## 2. The live base of the source census (`AMGT-ca-2`, row `W519-S5`; the CTO's grade: a census of every source line across the 101 names, with any `?` listed)

`python round120_prep/checks/r120_source_census.py live` over the pool, BEFORE any round-120 code is deployed (the live function at `VQ9zM6r4..`): **101 of 101 names read, 0 error; 0 question-mark sources in the PDF appendix, 0 `source not stated` lines, 0 question-mark sources in the rich exports.** The distinct appendix source words are `Bloomberg` (68,231 lines) and period-ending date tails the parser reads as a source when a line carries no further segment (a limitation of the instrument, named: a date tail is not a source). Positive control of the parser on synthetic lines: `Short interest ratio: 2.1 - ?` reads `?`; `Net debt: USD 5 million - source not stated` reads `source not stated`; a `Bloomberg` line with a date tail reads `Bloomberg`. So `W519-S5` is INERT on the live pool at the base: the live appendix does not print the figures that carry no source (the four names the `bz-3` worker found are fixture figures the live header omits). `ca-2` guards the synthetic case; the after-merge census over the candidate handler is the second read.

## 3. What is still open at this time

Worker `~521` (`ca-2`) has not reported (38 minutes; its receipt, proof instance and five test files are staged in its worktree, no commit yet). Merge `ca-2`, re-run the merged-tree folders, the census over the candidate, the three-state fixtures and the cross-surface read; then a release pin from the live pin `2771164d0d` with `render_pack.py` and `scoped_amgt.py`, the COO half, and `ca-5`.
