# NFRA_MCPORTAL -- evidence the project holds for FWD-1, FWD-2, FWD-15, FWD-16, FWD-17 (for the CVO's L9 grade)

**Compiled by:** `2.0.0_SA_COO~MP`, 2026-10-19 ~17:3xZ. **Does not grade.** Ruling: `1.0.0_SA_CTO~Z` msg 36018 ("compile the evidence ... as one file ... do not grade it yourself, and do not re-cut a replacement human act").
**Why now:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_163xZ_SIX_HANGING_OPEN_CALLS_RESOLVED.md` closed calls f0d2, 8ed7, def4 ("no longer owed by Andrew"). It grades no FWD; "its CVO grades it on whatever evidence the project holds". MP-q-1, MP-v-2 and MP-c-2 are CANCELLED citing it (their ACs read files the human halves would have written).

**Claim levels used.** RECORDED = quoted from a committed record, not re-run by this seat for this file. MEASURED-NOW = read by this seat on 2026-10-19 and the read is stated. ABSENT = no artifact exists; "absent" is a finding, never a zero.

## FWD-1 -- Andrew changes one colleague's access from the dashboard; the colleague's next question reflects it

DONE WHEN: EXERCISED -- one real change followed to the colleague's next answer (PRD :91-97).

| item | level | where |
|---|---|---|
| owner gate, serving, grant writer build, handlers, Entitlements pages | RECORDED, orders `complete` | `task-orders/NFRA_MCPORTAL.TO-MP-t-1`, `-t-2`, `-t-4`, `-t-5`, `-w-1`, `-b-1`, `-b-2`, `-b-3` |
| grant writer applied live; the join deploy | RECORDED, `-a-2` `complete`; `-t-3` and `-t-6` `superseded` by CTO ruling R-1 | `TO-MP-a-2`, `TO-MP-t-3`, `TO-MP-t-6` |
| writer's data-grant write path live, AC1-AC3 PASS | RECORDED | `TO-MP-k-2`, and msg 32656 (CloudOps~MP, 2026-10-09) |
| negative arms of the writer (no owner header -> REFUSED NO-OWNER-HEADER; direct sts:AssumeRole -> AccessDenied) | RECORDED, `round3/checks/c1.AC2.sh` expectation line reads PASS exit=0 | `TO-MP-c-1`, line 73 (this seat did not re-run it for this file) |
| `opal_asker_query` live for the colleague's question path | RECORDED | `drive_log_20261014T02Z_opal_bloomberg.md` ("R54 measured LIVE at ad2acc0a93") |
| the real change: narrow one colleague, the colleague asks, widen, the colleague asks; both writes in Recent Changes with before and after | **ABSENT** | `TO-MP-c-1` `superseded` (HELD, never spawned); `TO-MP-c-2` `cancelled`. The sitting with the colleague was Andrew's call def4 ("postponed" 2026-10-16, relay msg 34811, record @92df615fc6), now closed as no longer owed. |

## FWD-2 -- nobody but Andrew can open the dashboard or change anything; any Opal colleague can still read the daily report

DONE WHEN: EXERCISED -- a signed-in colleague tries every page and every change (PRD :99-103).

| item | level | where |
|---|---|---|
| server-side owner gate on every page and handler | RECORDED, `TO-MP-t-1` `complete` | `TO-MP-t-1` |
| route census: `admin_api.py` carries 12 admin routes (the check's denominator) | RECORDED, pre-check 2026-10-17 ~04:4xZ | `drive_log_20261017T04Z_opal_bloomberg.md` |
| deny guard pre-read | RECORDED: `None, None, 403` | same log |
| live window 2026-10-17: opened 04:52:43Z, a sign-in completed 04:55:48Z; `GET /` answered 200; the worker stopped at 1 of 13 requests | RECORDED | same log; worker `0.9.0_WK_NFRA_MCPORTAL~3` |
| what that window proved about the signed-in identity | RECORDED, issuer read-only `GET /api/admin/whoami`: status 200, the email IS the dashboard owner | same log. **The window signed in as the owner, not as a non-owner.** AC1 read FAIL (refused 0 of 13, admitted 1) because of that, not because a non-owner got in. Rows Z-W3-S4 and Z-W3-S5 adjudicated by Z-S74 @68b0364acd (S4's premise, a non-owner session, was false; S5 a non-defect). |
| `/sprint` served to the signed-in account (the daily-report half) | RECORDED: AC2 PASS, 200 on 2 of 2 | same log |
| a signed-in NON-owner refused on every page and every change, on the live host | **ABSENT** | `TO-MP-v-1` `superseded` (HELD, never spawned); `TO-MP-v-2` `cancelled`. The second window as Opal Bloomberg (call f0d2) never ran. |

## FWD-15 / FWD-16 / FWD-17 -- the Control Plane panels: overlaps, git state, open calls

DONE WHEN: EXERCISED -- one real overlap read on the page and checked against the store (15); one box whose work is not on the trunk seen as such the same day (16); one real call closed from the page (17) (PRD :173-188).

| item | level | where |
|---|---|---|
| handlers built: overlap (FWD-15), git state (FWD-16), open-calls read and close-request write (FWD-17), and their write grant | RECORDED, all `complete` | `TO-MP-o-1`, `TO-MP-g-1.fabric-gitstate-handler`, `TO-MP-k-1`, `TO-MP-k-2`, `TO-MP-p-2` (panels) |
| CP2 gateway release serving all three | RECORDED, `TO-MP-r-2` `complete`, CP2 release live @2a5966dfbd, AC1-AC3 PASS | msg 33076 (CloudOps~MP, 2026-10-10 23:32Z) |
| FWD-16 bounded read: cold read 1.3 s on the host, 2.2 s from site Z, against the 5 s bar | RECORDED, graded REALIZED for C17 (round 2) | `ledger/ROUND_ANALYSIS.c17-round2.md` section 1 |
| FWD-16 refusal field shows three states (G1): laptop reads "refused: false", sitez reads "not recorded" | RECORDED, graded REALIZED | `ledger/ROUND_ANALYSIS.pc-round1.md` section 1 |
| the Control Plane page displayed cleanly to Andrew (FWD-14, not 15-17) | RECORDED, his words 2026-10-16 ~18:5xZ | `org/tier1_exec/2.0.0_SA_COO~MP/deliverables/ANDREW_DIRECT_20261016_185xZ_CLOSE_21C5_21D9_44EB_GATEWAY_READS_WELL.md` |
| Andrew read one overlap, one box's git state, and closed one call FROM THE PAGE | **ABSENT** | `TO-MP-q-1` `cancelled`; `q1_seen.json` was never written. His closes of 21c5, 21d9, 44eb on 2026-10-16 were spoken to a seat, and the 2026-10-19 rows were closed by `1.0.0_SA_CTO~Z` citing his record (`closed.ruled_by: andrew`); neither is shown to have gone through the page. |
| close-request results on the box's S3 list | MEASURED-NOW: `aws s3 ls .../fabric/open-calls/v1/box=sitez/request_results/` and `.../requests/` both print no rows, 2026-10-19 ~17:2xZ. Positive control: the parent `box=sitez/` lists `open_calls.json`, `open_deploys.json`, `scan.json`. | An empty prefix does not show that no page close ever happened: whether results are retained after the box applies them is not read here. |

## Not in this file, stated so nothing is assumed

- `TO-MP-x-5` (FWD-14 close run) and `TO-MP-z-6` (FWD-20 close run) are still `staged`. Their calls (21c5 and 21d9) were closed by Andrew's own words on 2026-10-16 with a live read, so they are a different case from the three cancelled here. The CTO's ruling named FWD-1, 2, 15, 16, 17 only; the issuer carries x-5 and z-6 as its own open item.
- No grade is given or implied. `3.0.0_SA_CVO~Z` grades at L9.
