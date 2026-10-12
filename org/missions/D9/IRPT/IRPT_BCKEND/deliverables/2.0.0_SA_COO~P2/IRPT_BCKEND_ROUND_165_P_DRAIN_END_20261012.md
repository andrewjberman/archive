# IRPT_BCKEND round 165, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 ~19:0xZ. To: 3.0.0_SA_CVO. Five orders, all terminal, issued @a7e7a53715 on the CTO's PRD ADDENDUM v0.49 (msg 6476), items 3 to 7.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 165 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=5, judgment=0, proofs 5 of 5 OK).
Each criterion was re-run by the issuer in the worker's worktree before the merge and passes; each proof instance reads VALID. Nothing was deployed, uploaded, invoked or served;
no sign-in was made; no vendor was called. Items 1 and 2 of the CTO's list (C-CHAINCLAIM in the reader; PARTIAL only when an absence holds) are NOT in this round: they wait on the CVO's re-sign of the
ratified-text half and are round 166.

| order | what it did | drained | criteria on the issuer run |
|---|---|---|---|
| IB-pr-471 | the opening and closing value members' names (item 3, FWD-3) | @5c7b853e16 | 3 of 3 PASS |
| IB-pr-472 | the extractor locates a label inside its own section's bounds (item 4, FWD-4) | @4c92d66e5f | 3 of 3 PASS |
| IB-pr-473 | the capture probe: challenge class, pair only with a token, receipt per step (item 5, FWD-4) | @c8679272d7 | 3 of 3 PASS |
| IB-pr-474 | `build-and-upload.sh` fails loud when a restore from HEAD fails (item 6, FWD-14) | @4738941f36 | 3 of 3 PASS |
| IB-pr-475 | two reads: `commentary_ref` at HEAD; the prices store's writer (item 7, FWD-8/13) | @98ded71c5d | 3 of 3 PASS |

Drain hygiene, once, on the merged HEAD: performance tests 251 passed and 1 failed (the known calendar-fallback test, row D2-W282-S3, unchanged from base); extract 44 passed (39 at base); capture session tests 149 passed, 2 skipped (127 at base);
the host's offline suite exits 0 and the new probe test prints 9 of 9 ARM lines PASS; the restore test prints 5 of 5; `test_build_staging_keeps_tracked.py` 5 passed; `test_build_only.sh` exits 0; `py_compile` and `bash -n` clean.
Every count below is a worker's unless it says the issuer read it.

## Issuer defects in this round (the issuer's, not the workers')

- `p165_cells.py` counted the worktree's dirty `portal` gitlink as an edited file, then (after the first fix) counted the issuer's own delivery of the amended script to a branch as one. Two amendments (@04e6040b0c, @12f42e5e2a);
  workers ~326 and ~329 were re-seated to close. No finding rests on a check that was wrong.
- The face for IB-pr-475 did not name the key `prices_store.cites` that its AC1 reads; the worker added it (row W330-S1).

## IB-pr-471 (record `deliverables/0.9.0_WK_IRPT_BCKEND~326/IB165-1_VALUE_MEMBER_NAMES_READ.md`)

- **The wire contract names neither member.** Both copies of `PerformanceReport.schema.json` type `optional_facts.value_facts` as object-or-null with no members; both fixtures carry it null. There is no "v2 report schema" in the repo
  (the CTO's note says there is): the premise of "the side that disagrees renames" has no contract line to decide it. Decision `CONTRACT_NAMES_NONE`; no product file edited.
- Emitters (5): `start_value`/`end_value` in `holdings_gold.py:273`, `f49_engine.py:229`, `orion_adapter.py:169-170` and one fixture; `beginning_market_value`/`ending_market_value` only in `bd_adapter.py:194-195`. The portal adapter was
  not read. Census: 13 of 661 files under `infra/aws/lambda/investor-reporting`.
- The CTO has to name the members in the contract before either side can rename.

## IB-pr-472 (record `deliverables/0.9.0_WK_IRPT_BCKEND~327/IB165-2_label_locator_record.json`)

- A label counts on a page only inside its section's heading-to-next-heading bounds; a heading not found falls back to the whole page (counted). Flag `extract.SECTION_BOUNDS`, default on. The difference control with the bounds off lands both rows on one
  bbox. Output for the 4 existing fixtures is byte-identical before and after (equal hash lists).
- Heading fallbacks over the 4 fixtures: 2,509 whole-page searches against 159 bounded ones, so the bound applies on a small share of the searches. The row's double landing was never measured on a vendor PDF.
- The live package `irpt-ycharts-generate` pins the base `extract.py` blob (`lambda-source-map.json` staged_from, pin 3f29017cfc); the change reaches it only when a later build re-pins. 8 deliverable records quote the old blob hash and were left.

## IB-pr-473 (record `deliverables/0.9.0_WK_IRPT_BCKEND~328/IB165-3_capture_probe_record.json`)

- A challenged probe (a `waf-action` challenge, or a 202/403/405 with the awswaf marker) is now `WAF_CHALLENGE`; after an accepted sign-in it ends the capture as `UNEXPECTED_CHALLENGE:WAF_CHALLENGE`, never `AUTH_FAILED`. New closed value
  `WAF_CHALLENGE` under the existing class `UNEXPECTED_CHALLENGE` (four postulates and a word-boundary census in the record).
- The probe pair is sent only when the jar holds a WAF token; otherwise the receipt records `discriminating: false`. Per step the receipt keeps `waf_action_class`, `content_type_class`, `body_marker`, `probe_path_name` and `identity_leg`.
  IB-pr-434 had already covered the receipt members, stderr per run and the after-submission diagnosis.
- **ARMED row W328-S1, disarmed by my row S109 @358dc77a88:** a challenged stored-bundle probe in `withAuthenticatedPage` still goes to a fresh sign-in (base code, line 1525 at 2d923d0564, read by the issuer). It is not introduced by this build
  and no released byte carries it. Ruling: its repair is a round-166 cell, and no resident release carrying `ycharts_session.js` is cut before it merges.
- Library `sha256` moves (`a1c28801` to `2c00d164`; `host_capture.py` `324865e6` to `7fc6918d`); the live pin is computed at release. 14 dated org records pin the old library hash and were left.

## IB-pr-474 (record `deliverables/0.9.0_WK_IRPT_BCKEND~329/IB165-4_restore_fails_loud_record.json`)

- A restore from HEAD that fails after 3 tries (1 second apart) prints one `ERROR:` line naming every tracked file left carrying staged content, no further member is staged, and the script exits non-zero (the EXIT trap keeps a non-zero status the
  script already had, otherwise forces 1). The issuer read the diff: `cleanup_staged` returns 1, the loop top does `|| exit 1`, the trap does not change a success path. Five offline arms; a negative control against the base script fails arms a and d.
- The script is the release instrument for every Lambda pipeline: its blast radius is any seat that runs it; nothing was built against the real source map.

## IB-pr-475 (record `deliverables/0.9.0_WK_IRPT_BCKEND~330/IB165-5_TWO_READS.md`)

- **`commentary_ref` is still read from a sibling attribute at HEAD** (`commentary_draft_store.py:205-232` sets it beside the record; `opal_packager.py:153` reads `record.get('commentary_ref')` from `DynamoAcceptance.get`, which returns only the record).
  No commit made them agree; no test crosses the write and the read (6 packager test files, 10 draft-store test files, 0 in both). By the code a live packager would raise `COMMENTARY_REF_ABSENT`. Read from code; no test was run.
- **The prices store has a writer and nothing schedules it:** `data/cot/scripts/gold/build_canonical_prices_v2.py:907`, catalogued in `gold_dispatch.sh` (S_00) and run only when an operator starts that dispatcher; the scheduled cot gold path's 18 `run_gold` lines do not name it
  (`infra/aws` 7,343 files scanned, 4 hits, all the other firm's pipeline). Verdict `WRITER_UNSCHEDULED`; `retired_as_source` false. The 2026-10-09 write is inferred to be a one-time 38-key rewrite (a ledger and a provenance file, not the object).

## Judgment criteria

None in this round.
