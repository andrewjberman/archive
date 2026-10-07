# L8 drain end -- IRPT_BCKEND rounds 62-63, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~11:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

**Cut from:**
- **Round 62:** the CTO round-61 analysis @aae1ed7781 (E-P8, E-P9, E-P10; E-P11 was the issuer's own row S359), plus the two preconditions
  set by the r61 directory release's CTO half @74e91285b4. Issuance @0a3c1c841d, decomposition section 55.
- **Round 63:** ruling msg 337 (W140-S1). Issuance in section 56.

## The rounds at a glance

- **Orders:** 6 of 6 terminal and merged; 6 of 6 instances VALID.
- **Judgment criteria:** 0.
- **Issuer re-runs:** every mechanical criterion, in the worktree or on CLOUD.
- **Worktrees and branches:** 0 left. Portal branches kept for landing are listed in the last section.
- **Drain hygiene** on merged CLOUD f30b548a07:
  - directory 190 passed;
  - `_ids` 43 passed;
  - reports 101 passed;
  - intake offline suite OK;
  - render host 5 of 5;
  - export 216 passed. Its 6 failures are exactly the pypdf-only tests admitted by IB-pr-336 amendment 1; none other;
  - `py_compile` OK.

**Re-seats.** Three slots were re-seated cold because their subagent had ended with the order still open:
- ~136 (round 61);
- ~138 (IB-pr-336, after amendment 2);
- ~142 (IB-pr-340, after amendment 1).

## Orders

| order | item | drain | criteria | close record |
|---|---|---|---|---|
| IB-pr-336 | E-P9: the export takes a custody report (PRD v0.29 `custody_report_ref` / `CUSTODY_REPORT`) | @5c0f5d9d42 | AC1-AC3 + G PASS under amendments 1 (pypdf) and 2 (grant + custody naming, msg 342) | submit freezes the reference (13 tests). Both ExportBundle schemas and reports KINDS carry it. The render host maps `custody-report` and REFUSES an unknown template (the hazard at `render_export.cjs:240` is closed). The manifest lists the kind. NOT released; the served release is a later packet |
| IB-pr-337 | r61 release P2: refresh stages `handler.py` from the running blob 48313e9c0e | @76a614962f | AC1 + G PASS | the census at the apply pin reads 1 changed member (`refresh.py`); the S357 rider is removed |
| IB-pr-338 | r61 release P1: reader census of the search response | @df65042c5d | AC1 + G PASS | 7 readers; 5 FAILED the over-age envelope. W140-S1 (4 portal readers) was ruled a server defect, and W140-S2 (the IRPT_CUSTDY reader) is out of population (msg 337) |
| IB-pr-339 | E-P8: the seam holds no 'None'; `ids.py` treats ''/'None'/'nan' as unmapped (IRPT_CUSTDY W5-S1) | @b43f82c155 | AC1, AC2 + G PASS | 826 of 6202 index values removed, none invented. 482 accounts are no longer refused at their next release. The writer is not in the repo (row W141-S1). `2.0.0_SA_COO~K2` was told its E1 gate is open |
| IB-pr-340 | E-P10: one fixture per gated route | @fd67584da9 | AC1 + G PASS under amendment 1 (fix the refusal the battery found) | 21 routes, 17 gated pairs green. `intake/uploads.py` refusals now declare NOT_AUTHORIZED / NOT_FOUND (W142-S1). FWD-2's full run still needs the test principal Andrew names |
| IB-pr-341 | round 63: the over-age `_status` carries only public members | @55dce54d28 | AC1, AC2 + G PASS | the 4 portal readers pass (10 of 10 bun). The worker's commit moved the `portal` gitlink to an unpushed branch commit; the issuer restored it before the merge (@17cfd9773c) |

## The r61 directory release

**It is ready, but blocked on this box.** Both halves are signed (COO @0c3d443030, CTO @74e91285b4). P1 is met on 6 of 6 readers and P2 is met.
The census at HEAD 5ee7184a42 equals the signed delta: search 3 members, refresh 1.

**dell2 has no terraform (row S364).** Ruled (b) (msg 385): terraform arrives in the bring-up kit; the laptop does not apply. When it
runs, the census is re-read at the apply pin. Row S361 is carried separately: the directory functions stage the pre-fix calendar, and
this release keeps it; the re-pin is a later cell.

## Rows filed in the rounds

| row | class | standing |
|---|---|---|
| W138-S1 | BLOCKING, INERT | resolved by amendment 1 (pypdf-only failures admitted) |
| W138-S2 | BLOCKING, INERT | resolved by PRD v0.29 + amendment 2 |
| W138-S3, W138-S4 | OBSERVATION | the manifest.ts pin in the source map is stale after the rename (issuer's re-pin, next release); no CustodyReport document schema is published |
| W140-S1 | BLOCKING, ARMED | remedied by IB-pr-341. Its disarm row is owed with the release's after-read |
| W140-S2 | BLOCKING, INERT | out of the census population (msg 337) |
| W141-S1 | OBSERVATION | the seam writer is not in the repo |
| W142-S1 | BLOCKING, INERT | resolved by IB-pr-340 amendment 1 |
| W142-S2..S6 | OBSERVATION | S2: POST /analysis QUEUED status carries internal_correlation_id. S3: GET /status reads the job id from fields an API event lacks. S4: ExportReceipt.facts names no account. S5: the export allowed arm answers its own NOT_READY. S6: two bare PermissionErrors remain in uploads.py |
| W143-S1, W143-S2 | OBSERVATION | node_modules was junctioned from a sibling worktree; the P3 test compares rows with `availability` stripped |
| S359 | DISMISSED | W127-S1 disarmed (the adapter builds) |
| S361 | OBSERVATION | the directory functions stage the pre-fix calendar |
| S364 | BLOCKING, INERT | no terraform on dell2 (ruled (b)) |

## Portal branches waiting to land on DEV (not landed by this packet)

- `wk-IRPT_BCKEND-143-portal` @5c726cf4: the four reader tests and their fixtures. Tests only. It supersedes `wk-IRPT_BCKEND-140-portal` @d53a7a0f.
- `wk-IRPT_BCKEND-138-portal` @cdda4378: `PrintEntry.tsx` names the custody-report kind. A PRODUCT file, so the CTO reviews it before DEV.
