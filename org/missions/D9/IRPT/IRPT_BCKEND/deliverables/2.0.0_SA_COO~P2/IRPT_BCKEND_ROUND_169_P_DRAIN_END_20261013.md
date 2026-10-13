# IRPT_BCKEND round 169, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (the clock read 01:4xZ). To: 3.0.0_SA_CVO. Four orders, all terminal, issued @410abe2d57 on the CTO's ROUND-169 ANALYSIS (msg 6660) and amended several times (below).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 169 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=4, judgment=0). The issuer re-ran every criterion itself after each worker or executor report. On the final shared tree ten of the twelve read PASS; the other two, IB169-1-AC3 and IB169-4-AC3, are the "nothing outside the grant changed" checks, which read FAIL in the shared tree only because other seats' uncommitted files fill its dirty list. I verified the boundary directly instead: `git diff --name-only 410abe2d57 <worker branch>` for both branches lists only each order's grant paths, the issuer's own delivered check file, the investigation file and the order and proof files (worker 341: the two ui-walk files and its deliverables; worker 342: the two fixtures and its deliverables).
Push state: `IB-pr-490`'s commits (84f7bce350, b86e6e8f9d) and my check amendment 569e06a9f3 are LOCAL; origin/box/dell2 read @8cf145cf49 (ls-remote at 01:4xZ), carrying the other three orders' merges.

| order | what it did | landed | criteria (issuer re-run) |
|---|---|---|---|
| IB-pr-488 | the `/ui-walk` engine: `--firm "<label>"` (selects the header Firm control by its visible label; `FIRM_OPTION_ABSENT` if the label is not an option) and `--first-client` | @6bee5842ba | 3 of 3 PASS |
| IB-pr-489 | ONE Inflection walk kept its selection references (two: the performance paths of one client carried two distinct references) outside any git tree, left the walker disarmed; the walker gained a single-letter probe for the empty client search and a redaction of the first client's name in log, shot name and step label | @66439bd6a8 | 3 of 3 PASS |
| IB-pr-490 | the LIVE READ of the changed claim path: two windows of one Inflection reference, observed claim and counts against the offline prediction (closes the CTO's D2-S114, with the limit below) | b86e6e8f9d | 3 of 3 PASS |
| IB-pr-491 | the producer's two `AnalysisReport` contract fixtures send the extractor's section form (`section_id` `2.annualized_return.c1`, `section_type` `2`, `value` 7.12, `units` `pct`) instead of `annualized_return` / `DECIMAL_FRACTION` (row DSGN_IRPTV1-D2-W63-S1) | @be628bd919 | 3 of 3 PASS |

## The live read of the changed path (IB-pr-490)

The deployed `irpt-performance-adapter` (`abep4h7R...`, live since 2026-10-12T22:35:06Z) was invoked directly (the function's own role) with the Inflection references: two invokes were REFUSED before the laptop's fence fix (below), two COMPUTED after it (01:31Z and 01:32Z, log path `fresh`, HTTP 200, `PERFORMANCE_PARTIAL`, a retained reference present). Windows YTD (191 days) and 1Y (249 days): the observed claim equals the offline prediction in both (`measured` / `measured`); `days_without_base` and `days_with_return_left_out` are present as integers (0 and 0); the sha256 of the figure equals the predicted one. 4 invokes, 2 retained revisions persisted, 0 `AccessDenied`, 0 `TypeError` since 01:18Z (my own log read, after a retry for an aws CLI crash).
**THE LIMIT, stated and not hedged: the account that computed had 0 excluded days in both windows, so the rule predicted `measured` and the LEFT-OUT branch (claim `inferred`, `days_with_return_left_out` > 0), the branch this release changed, is STILL UNEXERCISED LIVE.** The counts-present and measured-stays-measured behaviour is exercised live. The second reference was not re-invoked after the fix. An on-demand act exists (another walk with a different first letter picks another client; whether its account has excluded days is unknown beforehand): offered to the CTO, not run.

## The Inflection incident (not this project's, but it blocked the read)

Inflection Performance answers were refused for ANY caller from the first call at 2026-10-13T00:04:48Z (the walk of this round) until the laptop's fence fix FB-f-21 landed 01:17Z to 01:18Z. Cause (the CTO's read, the laptop cluster lead's ruling at msg 108710 and the CTO ruling `CTO_RULING_INFLECTION_PERFORMANCE_DENY_OWNER_APPLIER_AND_PAIR_20261013` @af61c60689): ADVI_FIRMBKTS act 4 (dell1, 10-12 14:03Z to 14:13Z) moved the adapter's Inflection reads onto `opal-data-inflection`'s bucket-policy fence (an explicit deny on `s3:ListBucket` for principals outside `role/*-inf-*` and a named list); one `exemptions.json` row plus a `safe-apply` by laptop `0.7.0_AE_CloudOps~FBL` cured it. **dell1's CTO recommended, through MSTR (msg 6708), a ROLLBACK of IB-pr-487; CTO~DELL2 declined it with evidence:** the pins' diff (31+/7-, all claim logic, no S3/bucket/listing line) and the bucket policy unchanged since 10-11 (CloudTrail: 0 `PutBucketPolicy` on `opal-data-inflection`); a rollback restores kMB8xCI9, act 4's own build, so it would have restored the same denied call. Whether real client logins saw the refusal is NOT measured: no Inflection traffic ran between 10-12 14:13Z and 22:35Z, and the log's only denials before the fix are this round's walk and invokes (6 explicit-deny lines, 18 `AccessDenied`, all 10-13 00:04Z to 00:27Z). Rows: S116 (IB2, located the failure at the index read; corrected by its own S118), S117 (my cause record), S119 (my disposition of S116 to S118), S120 (IB2's AC2 FAIL, which was my check defect).

## Issuer defects this round (mine)

- IB169-4-AC1 substring-matched the section_id my own order tells the worker to write (check amended @faf155cc10; worker re-seated to close its proof).
- The `--firm` label was a guess (`Inflection`; the control's option reads `Inflection Wealth Management`): order amendment 1, three worker re-seats before the walk ran.
- The empty client search lists nothing; I did not read the page first: amendment 2 (letter probe).
- The walk produced two references, my order said one: amendment 3, and I wrote the two references myself from the walk's net log.
- IB169-3-AC2 read a paginated `--query length()` as one count (@569e06a9f3), the same trap CLAUDE.md names in 22a.
- The gate refused the first issuance for absolute `C:\` paths in `<paths>` (fixed to repo-relative); my path-fixing script's glob also rewrote orders 480 to 487 in the working tree: all eight restored from HEAD with `git show` before any commit; none reached a commit.
- The worker's proof instance for IB-pr-491 still carries one stale `compiler_tools.result` string reading "AC1 row status FAIL"; its acceptance row reads PASS (the lane gate bars me from editing the worker's folder; I did not use the audited author override).
- Gate limb for each order amendment: GATE (viii) on a modify only; it found none.

## Rows

BLOCKING, INERT and resolved by an amendment or a ruling: W342-S1 (the AC1 defect), W341-S4 (the firm label), W341-S5 (the empty search), W341-S6 (two references; the detector's 45 s ceiling disagrees with the network measure, which rules), S116 to S120 as above. ARMED: W341-S7 (the screenshot slug printed a name fragment on one worker's terminal) DISARMED by my S115 @4e678b4363; the redaction is by code read plus the worker's three IB169-1 criteria, NOT exercised on a live page, and the row says so. Observations: W341-S1 to S3, W342-S2 (4 `test_seam_paired` failures in `_contracts`, identical on the base and on the worker branch: 4 failed, 201 passed on both; round 167's "2 known" is stale).
A worker disarmed an orphaned walker arm (process not running) in its last session; the walker reads `disabled`, `armed=no`.

## Drain hygiene (once, on the merged HEAD)

`node --check` of `walk.mjs` OK; `_contracts` suite 4 failed, 201 passed at the base and on the branch of IB-pr-491 (no new failure); the other suites were not run (only the walker and two fixtures changed). No thread trace this round (the round's cells are not a hop of the FWD-1 thread). The two worker worktrees are removed and the scratch reference file is deleted.

## Judgment criteria

None.

## Request

L8 compile and L10 stamp for round 169. MAY-CLOSE is read on the strength of four terminal orders, one live read that matched its prediction on the measured branch, and the stated limit above.
Carried to the next round (the CTO's list; not decided here): the DSGN_IRPTV1 `D2-S28` producer pair (a last-four search returns the ACCOUNT entry, plus an `account_id` member on each ACCOUNT node, with a packet count of 49F accounts whose node id differs from the directory id), the portal-copy follow-up to the fixture cell, and the `bd_adapter.py` rename's APPLY, which waits for Andrew's PROD promote of the portal reader (`dell1-e7f2`).
