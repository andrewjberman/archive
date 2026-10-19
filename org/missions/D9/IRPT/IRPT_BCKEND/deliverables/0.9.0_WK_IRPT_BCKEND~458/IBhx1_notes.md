# IB-hx-1 notes (0.9.0_WK_IRPT_BCKEND~458, read only)

Base: HEAD 2d46c0f6f1 (branch wk-IRPT_BCKEND-458). Read date 2026-10-19. Firm 49financial (the builder build_49f_meshed).
Candidate day 2026-10-16, prior day 2026-10-15 (tcal.prev_trading_day), served day 2026-10-12.
Accounts appear here only as the first 12 hex of sha256 of the account id string as the producer holds it.

## 1. The order in which an account is tested (file data/assets/scripts/gold/investor_reporting/holdings_snapshot.py at HEAD)

1. Lines 3407-3408: have = candidate scope account ids plus ACCOUNT nodes; gone = served account ids minus have.
2. Lines 3409-3413: if gone, closed = closed_accounts() and gone (3410, listed, not refused); lost = gone minus closed (3413).
3. Lines 3415-3419: if lost and the provider is set, absent_at_source_exempt(lost, evidence()) (3416); exempt ids are removed from lost (3419).
4. Lines 3033-3063, absent_at_source_exempt, tables in order positions then balance (3049): both days must be dicts with integer counts (3055-3057); n_prior <= 0 or n_cand * 100 < n_prior * 95 returns the empty set (3058-3059); present |= accounts_with_positions of candidate and prior (3060-3061); exempt = lost minus present (3062).
5. Lines 3421-3425: if lost, marks_no_closures() true lists it not refused (3422-3423); otherwise add account_lost (3425).

Evidence reader: 3157-3180 (_absent_evidence, partitions read per day at 3164-3169, walk at 3170-3179); census 3121-3132; row presence 3101-3118; 49F spec 3183-3195 (positions and balance both null_present True). Closed set 2990-2999 (TERMINATED directory entries); marks 3014-3021.

## 2. Replay (read only, nothing written outside scratch)

- The copied harness IB233-1_49f_transplant_reread_harness.py (unmodified, copied into a scratch directory outside the repository) ran rc=0. Pins: transplant sha256 equal to the IB-pr-595 record (2 of 2); imported modules are the scratch transplant files; cusip_port_present True; one_date_bypass_absent True. Anatomy and DELTA harnesses rc=0.
- The harness needs GIT_DIR set because it runs git rev-parse in its own directory, which lies outside a checkout. GIT_DIR was set to the worktree's git directory.
- The scratch tree is a git archive of HEAD for the gold, silver, lib, registry and contract paths, with the two transplant files in place. The transplant holdings_snapshot.py differs from HEAD in cusip, classify, SmartX blocks (diff hunks at 180, 853, 943-985, 1028, 3248-3294); the gate and exemption lines 3024-3083 and 3371-3440 are identical.
- A second read-only probe (my own script, scratch only) rebuilt the candidate once, reproduced the refusal (outcome REFUSED, condition account_lost count 1), and counted rows per account.
- Read calls: get_object, head_object, list_objects_v2 and list_object_versions only. Writes: 0. Refused calls: 0.

## 3. Counts

- Served accounts 7640; candidate carries 7690; gone 3; gone and closed 0; lost 3; exempt 2 (both listed); gone and not exempt 1.
- Gone and not exempt, h12 eba4f45e3963: closed_marker false. positions candidate 0 rows, prior 18 rows; balance candidate 0 rows, prior 1 row (rows counted as the evidence function counts them; raw rows equal).
- Exempt, h12 3f628765e287 and h12 8d3bc7db8361: 0 rows in both tables on both days; closed_marker false.
- Partitions: positions candidate 6454 of prior 6444 = 100 percent; balance candidate 7690 of prior 7675 = 100 percent. Prior partitions are 100 by construction (6444 and 7675). The 95 percent floor is met in all four.
- Refusal object versions (four, one per refusing fire; the dates are the refused_at dates, which match the LastModified dates):
  - 2026-10-14: account_lost 1, listed absent_at_source 0 (candidate 2026-10-13).
  - 2026-10-15: account_lost 2, listed 0 (candidate 2026-10-14).
  - 2026-10-16: account_lost 2, listed 0 (candidate 2026-10-15).
  - 2026-10-19: account_lost 1, listed 2 (candidate 2026-10-16).

## 4. Each exemption test for the gone and not exempt account

- No positions in positions on both days: FAILS (prior day 18 rows).
- No positions in balance on both days: FAILS (prior day 1 row).
- All four partitions at least 95 percent of prior: PASSES (100, 100, 100, 100).
- Closed marker: absent (the account is not in the 80 account ids under TERMINATED directory entries).

The account has no source rows on the candidate day in either table, and the candidate build carries none, so no candidate-day row was dropped by the build. Its prior-day holdings make it fail the same no-positions tests the two listed accounts pass on both days.

## 5. Premise check (cell text)

The cell text says the lost account refuses because 49 Financial marks no closures. The live flag is the opposite: directory_marks_no_closures returned False (80 account ids under TERMINATED directory entries), so the refusal comes from the else branch at 3424-3425. With the flag True the account would have been listed not refused (3422-3423). Filed as a surprise row (IRPT_BCKEND-D2-W458-S1).

## 6. Verdict

- why_not_exempt: HAS_POSITIONS_IN_A_SOURCE_TABLE (the prior day holds positions in both tables).
- verdict: SOURCE_ABSENT_BUT_EXEMPTION_TESTS_FAIL. The source is absent on the candidate day and the exemption's both-day test fails. It is not BUILD_FAULT_ACCOUNT_HAS_SOURCE_POSITIONS, because the candidate day holds no source rows for the account.
- decision line: holdings_snapshot.py line 3062, exempt = lost - present.
- The CTO rule (extend only when absent by the same tests) is for the issuer; this read does not rule on it.

## 7. Not measured

- Whether the account closed or was liquidated at the custodian; the tables and the directory were the only sources read.
- The refusal object bodies beyond the counts above; the served publication beyond its account ids.
