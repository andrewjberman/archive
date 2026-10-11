# TCKT_VNEXT -- row dispositions for the round-1 L10 slug and workstream F10 (issuer `2.0.0_SA_COO~V2`, 2026-10-09 ~02:1xZ)

**Purpose:** every row in `surprise-channel/investigations/INVESTIGATION_v1.md` is dispositioned before the slug. The slug then goes to
`1.0.0_SA_CTO~DELL2` the moment TV-r-1 (Alyssa's own filing) is traced. **Census:** 16 rows (regex over the channel, `"id": "TCKT_VNEXT-...`);
2 BLOCKING, 1 ARMED, 13 OBSERVATION/INERT.

| row | class / hazard | disposition | carrier |
|---|---|---|---|
| D2-S1 carriers say laptop | OBS / INERT | OPEN -> SLUG: `project.json` still reads `"fabric": "laptop"` beside `"placement": "DELL2"` | CTO (L3 carriers) |
| D2-W1-S1 fee default unruled | OBS / INERT | PARTLY RESOLVED: the invented 1.0 was removed (`None`) @da43155418. The VALUE is unruled -> SLUG | CTO / Andrew |
| D2-W1-S2 order wording, two readings | OBS / INERT | RESOLVED in the build (round-1 drain @23759c51d2; 13/13 tests) | -- |
| D2-W1-S3 matrix pin 7 | OBS / INERT | RESOLVED in round 1 (the pin moved with REPORT; it moved again in F10, 8 -> 9, row W3-S3) | -- |
| D2-W1-S4 tests call real SES | OBS / **ARMED** | DISARMED BY PROCEDURE (D2-S2: every issuer run used invalid AWS keys). The standing fix (stub SES in the pre-existing tests) -> SLUG as a cell | next round |
| D2-W2-S1 submit envelope shape | OBS / INERT | RESOLVED in the build (the page reads the adapted view) | -- |
| D2-S2 disarm record | OBS / INERT | RECORD ONLY | -- |
| D2-S3 firm answer is free text | OBS / INERT | OPEN -> SLUG: a firm pick-list (enrichment); IRPT_ANLREQ's form design may own it | CTO / IRPT_ANLREQ |
| D2-S4 report opens through IRPT's owned read | OBS / INERT | OPEN -> SLUG: a second reader of a filed report (the assignee is not the uploader) | CTO / IRPT_ANLREQ |
| D2-S5 one-account check | OBS / INERT | OPEN -> SLUG: FWD-3 cell | next round |
| D2-S6 draft not on the same ticket | OBS / INERT | CLOSED by CTO msg 1893 ("D2-S6 is already closed by generated_at"). C-PACKAGE (F10-l-3) puts the package on the same open ticket | -- |
| D2-W3-S1 sub vs email | OBS / INERT | ANSWERED FROM CODE: the authorizer sets context `email: decoded.sub` (`portal-authorizer/index.mjs:398`). Live confirmation = mint leg M step 4 | F10 leg M |
| D2-S7 build script always uploads | OBS / INERT | IN FLIGHT: TO-F10-l4 (round 4, @1676d6c23d) | F10 round 4 |
| D2-W3-S2 PACKAGE vs the pinned matrix test | **BLOCKING** / INERT | RESOLVED by D2-W3-S3 (AMENDMENT 1 @6751522799; drained @da0471b901, 118 passed) | -- |
| D2-W3-S3 resolves W3-S2 | OBS / INERT | RECORD ONLY | -- |
| D2-S8 mint pair names no reader | **BLOCKING** / INERT | IN FLIGHT: both halves amended (@b70dd6fbad, CTO 1.2). The laptop adds the one ARN (ETA ~02:0xZ), then CloudOps~DELL2 runs steps 3-7 and closes RED ledger `tckt-vnext-f10-d1-mint-20261009` | F10 leg M |

**What gates the round-1 slug:** only TV-r-1 (Alyssa, open call `dell2-20261008T211740Z-3cb1`). The two BLOCKING rows belong to workstream
F10 and gate F10's close, not round 1's.

**The slug's enrichment list, as drafted:**
1. stub SES in the pre-existing ticket_center tests (W1-S4);
2. the fee default value (W1-S1);
3. a firm pick-list (S3);
4. a second reader of a filed report (S4);
5. the one-account check, FWD-3 (S5);
6. the `fabric` carrier (S1);
7. adding the commentary secret ARN to the rotation owner's runbook (S8 aftermath).

Items 3 and 4 are named as candidates to move into IRPT_ANLREQ under Andrew's consolidation word (@2b21a349d1).
