# NFRA_TRNSPT round 20 -- close record: the Teams pull is live, the old silver is clean, the gateway admits no meeting yet (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `051003d7af` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R20.md`, CTO ADDENDUM 9-11). `round-close-check --round 20`
MAY-CLOSE (2 orders, 2 proofs ok); drain on the merged tree `data/transcripts/scripts/tests/` 415 passed (test_eod_voice.py ignored,
LDO-001's import error).

| cell | merged / act | what exists |
|---|---|---|
| TR-t-20 (D2-S10, ADDENDUM 9) | 488c840f48, AMEND 1+2 a9039b8d62 | Teams `GatewayTransport` on the headless /hx/transcripts route; `pull.tf` reads `gateway/transcripts/bearer` by data source. Wall-clock interim (ADDENDUM 11): content VTT only, `wallclock_basis` 'absent', never derived; research_fold carries the row's own basis (W2-S7 disarmed) |
| TR-w-20 (W1-S7, served) | TO-RUN-w20 complete c4e1506b73 | 30 Teams silver keys re-wiped in place under the pair (COO 051003d7af + CTO 7a2e7199ed) by 0.7.0_AE_CloudOps~TR2 @f012dd44d8; issuer read-back `R20_REWIPE_READBACK.json` @16d945f3e0: 30/30 new VersionIds, rows 8873 unchanged, residual 7887 names + 20 ids -> 0, planted control discriminates. **W1-S7 existing-object half CLOSED** |
| TR-x-20 / TR-f-20 (FWD-4, FWD-9 exercises) | e18849b58c | `R20_EXERCISES_FWD4_FWD9.json`: FWD-4 reaches `never_recorded`; FWD-9 203 securities (meetings 1462, mail 17, commentary 0) |
| TR-s-18 carried (FWD-2) | TO-APPLY-p18 complete 2257f25213 | Teams pull APPLIED by ~TR2 @8d87f6a93f: 9 added, outlook pull CodeSha256 unmoved, invoke 200 listed 0 refused 4. Issuer read of the served state: Lambda Active/Successful, rule ENABLED `cron(0 13-22 ? * MON-FRI *)`. Wipe-on-landing is now the live writer of Teams silver |
| TR-d-20 (FWD-6) | queued for Andrew | a real market-update deck; intake built in r19 |

**Rows:** D2-S11 BLOCKING (@fb94b3075c) -- the gateway HOST allowlist answers 403 meeting_not_allowed on 4 of 4 meetings (401 control
discriminates); FWD-2's first landing waits on NFRA_OPLGTW at site Z, relayed via 0.0.0_AB_MSTR~DELL2 (msg 3189, CTO copied 3190); site Z CTO TAKES it (msg 3207, ruling @261e2c42a0): an env-only release cell after r29, ids read from meeting_allowlist under a pair; expect 3 of 4 (research_meeting also needs its organizer's grant).
D2-S12 OBSERVATION (@8d87f6a93f) -- no `lambda-source-map.json` entry and no `transcripts-v*` tag for the transcripts root's Lambdas
(deployment rules 4 and 6): next round's repair cell.

**Carried / open:** D2-S11 (site Z); TR-d-20 deck (Andrew); TO-APPLY-a18 (FWD-8 second reader) at the laptop; the research_meeting
invite (Graph 3003, Andrew); site Z's /hx/transcripts metadata route (ruling @7f58eb8f77) for wall-clock.
