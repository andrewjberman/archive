# L8 drain end -- ADVI_COTBKF round 5

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~09:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 5 was cut as one issuance (@407326a599, `fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-4 analysis @e363a194ed,
under laptop `1.0.0_SA_CTO`'s ruling A (08:5xZ): no dell2 production dated before 2024 through `lib/trading_calendar.py` until ruling
B's fix lands. E2 was not cut (gated on that fix). Decomposition: `decompositions/ADVI_COTBKF_DECOMP.round5.md`.

Every order of the round is terminal and merged:
- 3 of 3 orders `complete`;
- `proof-of-spec-check.py` VALID rc 0 on 3 of 3 instances;
- 0 JUDGMENT criteria in this round;
- 0 unmerged worker branches and 0 linked worktrees for this project on dell2.

## Orders

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-e-1 calendar readers refuse an uncovering calendar | ~17 | @9014a21b22 | VALID: AC1 PASS, AC2 6 passed (difference control: the same 2013-2026 span refused under the fallback stub, admitted under the package stub) | `CALENDAR-REFUSAL refused=3 of 3 calendar=NYSE/hardcoded-fallback-2024-2027`; each script rc 2, `CALENDAR-UNCOVERED 2013..2023`; outputs in a deleted temp directory |
| CB-e-3 documents plan holds back the C-RESTRICTED prefix | ~18 | @9fea452b9d | VALID: AC1 4 passed, AC2 PASS | `DOCUMENTS-PLAN unique=11119 every_document_once=True sources_verified=11119 refused=0 keys_unique=True bytes=1795905639 held_restricted=0 writable=11119`; prefix from `opal_naming.address(..., "bronze", "crm", ...)`, never typed |
| CB-e-4 the C-RESTRICTED apply write-in | ~19 | @ece9baad7a | VALID: AC1 PASS | request `org/devices/role_requests/dell2/dell2-20261007T085711Z-7b15.json` (12 permissions, each tied to its `s3-lgic-firm-buckets.tf` line), one bus line sent by the writer; note `deliverables/0.9.0_WK_ADVI_COTBKF~19/C_RESTRICTED_WRITE_IN.md` |

Drain hygiene: `py_compile` and ruff (py39) clean on every changed `.py`; the silver suites 30 passed, the analysis census suite 15 passed
(run separately: run together, the two test folders collide on a module name at collection, which predates this round).

## Issuer acts NOT done, and why

| act | state | carrier |
|---|---|---|
| E5 crosswalk `--apply` | NOT RUN | row S12 (BLOCKING, ARMED): the Cottonwood bucket explicitly denies dell2 List and GetBucketPolicy; no apply from dell2 until `1.0.0_SA_CTO~DELL2` rules where it runs |
| E3 documents `--apply` | NOT RUN | row S12, same |
| E4 send of the request path to `1.0.0_SA_CTO~DELL2` | sent with this packet's commit (msg in this seat's sent log) | -- |
| E2 links + census on a covering calendar | NOT CUT | ruling A/B; rows S9, W12-S1 stay ARMED |

## Rows filed in the round

| row | class | standing | note |
|---|---|---|---|
| S10 | OBSERVATION | INERT | S9's cause measured by its disarm owner: 1,450 of 1,450 rows equal under a pre-2024-complete calendar |
| S11 | OBSERVATION | INERT | ruling C list: the round-4 census day figures (committed) and the scratch links run; none served, landed or graded REALIZED |
| W19-S1 | OBSERVATION | INERT | the role-request writer admits only a service as the assuming principal; the break-glass trust is a user, carried in the note |
| S12 | BLOCKING | ARMED (this seat) | the applies vs the Cottonwood bucket fence (above) |

Carried ARMED: S9, W12-S1 (E2). Open relay: W12-S2 listing script @27b47e8ef1 sent for the laptop (msgs 225-226).
