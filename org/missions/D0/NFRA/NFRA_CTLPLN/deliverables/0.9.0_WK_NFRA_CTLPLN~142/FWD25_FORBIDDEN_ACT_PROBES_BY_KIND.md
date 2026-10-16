# FWD-25 forbidden-act probes by seat kind (CT-bd-1, round 29)

Source: `python .tools/seat-rules-check.py exercise` run in the worktree `0.9.0_WK_NFRA_CTLPLN~142` (branch `wk-NFRA_CTLPLN-142`), output saved to the worker scratch and transcribed by a scratch script that reads the tool's own `PROBE` lines and classifies each serial with the tool's `kind_of_local`. Detail column truncated to 120 characters.

Probe lines per kind (every kind printed, zero included):

| kind | probe lines | PASS | FAIL | UNREAD | PENDING |
|---|---|---|---|---|---|
| CTO | 11 | 11 | 0 | 0 | 0 |
| COO | 5 | 5 | 0 | 0 | 0 |
| CVO | 7 | 7 | 0 | 0 | 0 |
| CRO | 5 | 5 | 0 | 0 | 0 |
| CLOUDOPS | 4 | 4 | 0 | 0 | 0 |
| TIER2 | 5 | 5 | 0 | 0 | 0 |
| WORKER | 5 | 5 | 0 | 0 | 0 |
| MSTR | 9 | 9 | 0 | 0 | 0 |
| NO-SERIAL | 9 | 9 | 0 | 0 | 0 |
| UNKNOWN | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 60 | 60 | 0 | 0 | 0 |

NO-SERIAL: probes that name no serial (`stands_for_all_kinds`, one run each). Their rule's kinds are in the last column of their row. A kind whose count above is zero has no probe line in this run at all.

## CTO (11 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-1 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (CLAUDE.md NEVER#7): rebas |
| R-GITOPS-2 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (shared-worktree blast rul |
| R-GITOPS-3 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (CLAUDE.md Git / LD-0276): |
| R-GITOPS-4 | PASS | 1.0.0_SA_CTO | CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (LD-0367 rule 2 / LD-0368  |
| R-GITOPS-6 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-1 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (CLAUDE.md NEVER#3): bare  |
| R-AWSDEVOPS-2 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=1.0.0_SA_CTO kind=CTO root=opal-assets verdict=REFUSED reason=a CTO does n |
| R-WORKFLOW-4 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: RESULT: "SEND REFUSED (LD-0529, Andrew-direct 2026-09-03: a Tier-2 seat acts only on a tas |
| R-WORKFLOW-7 | PASS | 1.0.0_SA_CTO | CTO | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/signoff/CVO_RATIFIED_v1.json -- lane=TREE_PRD_SIGNOFF (Project |
| R-WORKFLOW-8 | PASS | 1.0.0_SA_CTO | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: der '1.0.0_SA_CTO'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |
| R-WORKFLOW-9 | PASS | 1.0.0_SA_CTO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: _SA_CTO</issued_to> names a TIER-1 seat. L7 workers are TIER-2 ONLY (Andrew-direct 2026-09-03, @716 |

## COO (5 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-6 | PASS | 2.0.0_SA_COO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-2 | PASS | 2.0.0_SA_COO | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=2.0.0_SA_COO kind=COO root=opal-assets verdict=REFUSED reason=a COO does n |
| R-WORKFLOW-4 | PASS | 2.0.0_SA_COO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: RESULT: "SEND REFUSED (LD-0529, Andrew-direct 2026-09-03: a Tier-2 seat acts only on a tas |
| R-WORKFLOW-6 | PASS | 2.0.0_SA_COO | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-9 | PASS | 2.0.0_SA_COO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: _SA_COO</issued_to> names a TIER-1 seat. L7 workers are TIER-2 ONLY (Andrew-direct 2026-09-03, @716 |

## CVO (7 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-6 | PASS | 3.0.0_SA_CVO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-2 | PASS | 3.0.0_SA_CVO | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=3.0.0_SA_CVO kind=CVO root=opal-assets verdict=REFUSED reason=a CVO does n |
| R-WORKFLOW-3 | PASS | 3.0.0_SA_CVO | CVO | rc=0 saw: RESULT: "SEND REFUSED (spine v3.1 L8: the CVO's one send of a round i |
| R-WORKFLOW-4 | PASS | 3.0.0_SA_CVO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: RESULT: "SEND REFUSED (LD-0529, Andrew-direct 2026-09-03: a Tier-2 seat acts only on a tas |
| R-WORKFLOW-6 | PASS | 3.0.0_SA_CVO | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-8 | PASS | 3.0.0_SA_CVO | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: der '3.0.0_SA_CVO'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |
| R-WORKFLOW-9 | PASS | 3.0.0_SA_CVO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: _SA_CVO</issued_to> names a TIER-1 seat. L7 workers are TIER-2 ONLY (Andrew-direct 2026-09-03, @716 |

## CRO (5 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-6 | PASS | 4.0.0_SA_CRO | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-2 | PASS | 4.0.0_SA_CRO | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=4.0.0_SA_CRO kind=CRO root=opal-assets verdict=REFUSED reason=a CRO does n |
| R-WORKFLOW-4 | PASS | 4.0.0_SA_CRO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: RESULT: "SEND REFUSED (LD-0529, Andrew-direct 2026-09-03: a Tier-2 seat acts only on a tas |
| R-WORKFLOW-8 | PASS | 4.0.0_SA_CRO | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: der '4.0.0_SA_CRO'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |
| R-WORKFLOW-9 | PASS | 4.0.0_SA_CRO | MSTR,CTO,COO,CVO,CRO | rc=0 saw: _SA_CRO</issued_to> names a TIER-1 seat. L7 workers are TIER-2 ONLY (Andrew-direct 2026-09-03, @716 |

## CLOUDOPS (4 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-6 | PASS | 0.7.0_AE_CloudOps~S | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-3 | PASS | 0.7.0_AE_CloudOps~S | CLOUDOPS,TIER2 | rc=1 saw: t open_deploy=clear verdict=STOP |
| R-WORKFLOW-6 | PASS | 0.7.0_AE_CloudOps~S | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-8 | PASS | 0.7.0_AE_CloudOps~S | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: 7.0_AE_CloudOps~S'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |

## TIER2 (5 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-4 | PASS | 0.4.0_DS_ClientPlatform~A | CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (LD-0367 rule 2 / LD-0368  |
| R-GITOPS-6 | PASS | 0.4.0_DS_ClientPlatform~A | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-3 | PASS | 0.4.0_DS_ClientPlatform~A | CLOUDOPS,TIER2 | rc=1 saw: t open_deploy=clear verdict=STOP |
| R-WORKFLOW-6 | PASS | 0.4.0_DS_ClientPlatform~A | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-8 | PASS | 0.4.0_DS_ClientPlatform~A | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: _ClientPlatform~A'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |

## WORKER (5 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-6 | PASS | 0.9.0_WK_NFRA_CTLPLN~8 | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-GITOPS-7 | PASS | 0.9.0_WK_NFRA_CTLPLN~8 | WORKER | rc=1 saw: VIOLATION: infra/aws/terraform/opal-assets/main.tf -- lane=CLOUD_OPS_OR_ETL (Any AE agent ? infra/aws, pipelin |
| R-AWSDEVOPS-2 | PASS | 0.9.0_WK_NFRA_CTLPLN~8 | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=0.9.0_WK_NFRA_CTLPLN~8 kind=WORKER root=opal-assets verdict=REFUSED reason |
| R-WORKFLOW-6 | PASS | 0.9.0_WK_NFRA_CTLPLN~8 | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-8 | PASS | 0.9.0_WK_NFRA_CTLPLN~8 | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: _WK_NFRA_CTLPLN~8'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |

## MSTR (9 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-GITOPS-5 | PASS | 0.0.0_AB_MSTR~DELL1 | MSTR | rc=0 saw: |
| R-GITOPS-6 | PASS | 0.0.0_AB_MSTR | MSTR,CTO,COO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/tier0/STAKES_MATRIX.md -- lane=TIER0_LAW (Tier-0 governance law -- Constitution, S |
| R-AWSDEVOPS-2 | PASS | 0.0.0_AB_MSTR | MSTR,CTO,COO,CVO,CRO,WORKER | rc=1 saw: EVOPS-4; targets=0 APPLY-WHO serial=0.0.0_AB_MSTR kind=MSTR root=opal-assets verdict=REFUSED reason=a MSTR doe |
| R-WORKFLOW-1 | PASS | 0.0.0_AB_MSTR | MSTR | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-2 | PASS | 0.0.0_AB_MSTR | MSTR | rc=0 saw: tName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED (mstr-no-tier2-writes) --  |
| R-WORKFLOW-4 | PASS | 0.0.0_AB_MSTR | MSTR,CTO,COO,CVO,CRO | rc=0 saw: RESULT: "SEND REFUSED (LD-0529, Andrew-direct 2026-09-03: a Tier-2 seat acts only on a tas |
| R-WORKFLOW-6 | PASS | 0.0.0_AB_MSTR | MSTR,COO,CVO,CLOUDOPS,TIER2,WORKER | rc=1 saw: VIOLATION: org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md -- lane=ANY_CTO (Any CTO (base, ~B C-suite, |
| R-WORKFLOW-8 | PASS | 0.0.0_AB_MSTR | MSTR,CTO,CVO,CRO,CLOUDOPS,TIER2,WORKER | rc=0 saw: er '0.0.0_AB_MSTR'. COO is the only agent that does task orders (LD-0521 A3): a new file under org/missions/*/ |
| R-WORKFLOW-9 | PASS | 0.0.0_AB_MSTR | MSTR,CTO,COO,CVO,CRO | rc=0 saw: AB_MSTR</issued_to> names a TIER-0 seat. L7 workers are TIER-2 ONLY (Andrew-direct 2026-09-03, @716 |

## NO-SERIAL (9 probe lines)

| rule | status | serial | rule kinds | detail |
|---|---|---|---|---|
| R-AWSDEVOPS-7 | PASS | - | CLOUDOPS,TIER2 | rc=0 saw: POLICY-DENY sid=DenyCloudTrailWrites action=cloudtrail:DeleteTrail effect=Deny (declared in the |
| R-AWSDEVOPS-7 | PASS | - | CLOUDOPS,TIER2 | rc=0 saw: POLICY-DENY sid=DenyS3DeletesOnProductionData action=s3:DeleteObject* effect=Deny (declared in the file; |
| R-AWSDEVOPS-7 | PASS | - | CLOUDOPS,TIER2 | rc=0 saw: POLICY-DENY sid=DenyTableAndDatabaseDeletes action=dynamodb:DeleteTable effect=Deny (declared in the fi |
| R-WORKFLOW-5 | PASS | - | WORKER | rc=0 saw: ion 9) -- a crit PASS J judgment=true with status PASS -> 1 violation (no verdict on a judgment criterion) (vi |
| R-WORKFLOW-18 | PASS | - | CTO | rc=0 saw: eads ON, never off CALL-SCOPE-SELFTEST cases=36/36 ok=True |
| R-WORKFLOW-19 | PASS | - | CTO,MSTR | rc=0 saw: and-writes-nothing CROSSBOX-SELFTEST cases=40/40 ok=True |
| R-WORKFLOW-20 | PASS | - | MSTR | rc=0 saw: the run is not ok MSTR-RECORD-SELFTEST cases=16/16 ok=True |
| R-WORKFLOW-21 | PASS | - | CVO,COO | rc=0 saw: verdict=MAY-CLOSE ROUND-CLOSE-SELFTEST cases=30/30 ok=True |
| R-WORKFLOW-22 | PASS | - | CRO,CTO | rc=0 saw: aught, not applied RESEARCH-OWED-SELFTEST cases=16/16 ok=True |

## UNKNOWN (0 probe lines)

No probe line of this kind in this run.

## Last line of the tool (verbatim)

```
SEAT-RULES rules=47 gate=25 skill=11 launcher=11 pairs_covered=24/24 probes_pass=60 probes_pending=0 probes_fail=0 probes_unread=0 needs_andrew=2 ok=True
```

