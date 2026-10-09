# NFRA_GATSCP round 2 -- the close's real runs (issuer 2.0.0_SA_COO~N1, 2026-10-09 10:4xZ-12:3xZ)

## 1. FWD-2, FWD-3, FWD-4, FWD-6 -- real safe-commit acts on the never-pushed QA branch `qa/gatscp-r2` (ruling J)

Base: box/dell1 1cd1871f4a (round 2's five dell1 orders landed @50a354da0c). Placed on QA only by plumbing @ce7a46746e:
IRPT_FNTEND row W1-S15 `surfaced_at` non-UTC; IRPT_FNTEND `project.json` dep_stage EXECUTING->DECOMP without its index.
Driver: `qa2_acts.py` (issuer scratch), each act a real `.tools/safe-commit.sh` run as 2.0.0_SA_COO~N1 in the QA worktree; a
refused act's working file restored after it. Result: `QA2-ACTS ok=True passed=6/6`. The QA branch is kept on dell1, never pushed
(ls-remote `refs/heads/qa/*`: 0).

| act | outcome | commit |
|---|---|---|
| A1_own_row_lands | FWD-2 land: own valid channel row beside IRPT_FNTEND's placed error | 0fb79191f5 |
| A2_own_bad_row_refused | FWD-2 own: own INVALID row refused | refused, nothing committed |
| A3_baseline_reset_refused | FWD-2 reset: dropping a baseline tuple refused | refused, nothing committed |
| A4_own_row_lands_with_index | FWD-3 land + FWD-4: own row dep_stage change staged ALONE; the commit carries org/projects/NFRA_GATSCP.json | 3c0ba4cb79 |
| A5_own_index_drift_refused | FWD-3 own: hand-drifted own index entry refused | refused, nothing committed |
| A6_unsaved_edit_not_graded | FWD-6: another seat's UNSAVED edit (LGIC_BLANKFIX row, working tree only) not graded; own commit lands | 559d17648d |

A4's commit carries both `org/missions/D0/NFRA/NFRA_GATSCP/project.json` and `org/projects/NFRA_GATSCP.json` with no derive run by
hand (FWD-4). A3 refuses with every finding in-act (the bystander's placed failure included): a deliberate `--write-baseline`
re-baseline captures it instead. A6's output never names LGIC_BLANKFIX.

### Key lines per act (line-ending warnings removed)

#### A1_own_row_lands

```
STANDING IRPT_FNTEND surprise-corpus org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md IRPT_FNTEND-W1-S15 /surfaced_at
[surprise-corpus] SCOPE: act_documents=1 in-act findings=0 (new=0 malformed=0) STANDING=1 (new=1 malformed_docs=0) resolved=0
[surprise-corpus] OK: the act's documents are clean against the baseline (4 known, 1 STANDING outside the act, 0 resolved).
STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json dep_stage: index='EXECUTING' tree='DECOMP'
OK: missions-tree-check -- 1 tree/register path(s) staged; RESULT: 0 violation(s) in the act's projects, 1 STANDING  (denominators on the first line)
  [msg-verify] committed 0fb79191f5  subject: qa(A1): own valid channel row beside IRPT_FNTEND's placed error
  STANDING IRPT_FNTEND surprise-corpus org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md IRPT_FNTEND-W1-S15 /surfaced_at
  [surprise-corpus] SCOPE: act_documents=1 in-act findings=0 (new=0 malformed=0) STANDING=1 (new=1 malformed_docs=0) resolved=0
  [surprise-corpus] OK: the act's documents are clean against the baseline (4 known, 1 STANDING outside the act, 0 resolved).
```

#### A2_own_bad_row_refused

```
ERROR: BLOCKED -- surprise-channel row gate (steps 7/10). Commit aborted.
  [surprise-corpus] REFUSED: 1 NEW failure(s), 0 RESOLVED baseline tuple(s). The set moved.
  [surprise-row-gate] BLOCKED -- 2 violation(s) on NEW rows:
      NFRA_GATSCP-D1-S91: schema violation at /surfaced_at -- 'not-a-utc-time' does not match '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?Z$'
      standing corpus pass REFUSED -- see the [surprise-corpus] lines above
    NEW      org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md  NFRA_GATSCP-D1-S91  /surfaced_at  71eefb651595
  STANDING IRPT_FNTEND surprise-corpus org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md IRPT_FNTEND-W1-S15 /surfaced_at
  [surprise-corpus] SCOPE: act_documents=1 in-act findings=1 (new=1 malformed=0) STANDING=1 (new=1 malformed_docs=0) resolved=0
```

#### A3_baseline_reset_refused

```
[surprise-corpus] REFUSED: 2 NEW failure(s), 0 RESOLVED baseline tuple(s). The set moved.
[surprise-row-gate] BLOCKED -- 1 violation(s) on NEW rows:
    standing corpus pass REFUSED -- see the [surprise-corpus] lines above
  NEW      org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md  IRPT_FNTEND-W1-S15  /surfaced_at  71eefb651595
  NEW      org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md  D1_CATVIEWS-S8  /disposition  99a9efd23c0e
[surprise-corpus] SCOPE: act_documents=1 in-act findings=2 (new=2 malformed=0) STANDING=0 (new=0 malformed_docs=0) resolved=0
```

#### A4_own_row_lands_with_index

```
STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json dep_stage: index='EXECUTING' tree='DECOMP'
OK: missions-tree-check -- 2 tree/register path(s) staged; RESULT: 0 violation(s) in the act's projects, 1 STANDING  (denominators on the first line)
  [msg-verify] committed 3c0ba4cb79  subject: qa(A4): own tree row dep_stage EXECUTING->DECOMP, staged alone
```

#### A5_own_index_drift_refused

```
BLOCKED: missions-tree-check -- the project tree's validator REFUSES this commit (staged: org/projects/NFRA_GATSCP.json )
  ACT SCOPE: in-act=1 STANDING=1 (act projects: NFRA_GATSCP)
STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json dep_stage: index='EXECUTING' tree='DECOMP'
  [INDEX-DRIFT] org/projects/NFRA_GATSCP.json: dep_stage: index='EXECUTING' tree='DECOMP'
RESULT: 1 violation(s) in the act's projects, 1 STANDING  (denominators on the first line)
  remedy: fix the state the violation names (R5 = the register's members list, 0.0.0_AB_MSTR's lane); never bypass.
```

#### A6_unsaved_edit_not_graded

```
STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json dep_stage: index='EXECUTING' tree='DECOMP'
OK: missions-tree-check -- 1 tree/register path(s) staged; RESULT: 0 violation(s) in the act's projects, 1 STANDING  (denominators on the first line)
  [msg-verify] committed 559d17648d  subject: qa(A6): own deliverable beside another seat's unsaved edit
```

## 2. FWD-7 -- one real order to a site-Z Codex lane, no seat-home copy, no hand relay

| step | act | evidence |
|---|---|---|
| open | `crossbox-call.py issue --order <GS-e-2 order>` (GS-e-3) resolved `~ZG` to sitez by lane letter | `XBOX-ISSUE opened XB-20261009T105156Z-1c53 sitez 0.7.0_AE_CloudOps~ZG` (10:51:56Z) |
| commit | the crossbox file committed by 0.0.0_AB_MSTR~DELL1 (lane DEVICES_CROSSBOX refuses a COO) | msg 2307 |
| send | `crossbox-call.py send-pending` by the manager: candidates=1 sent=1 held=0 | SENT 10:53:35Z, bus 77379c81 (msg 2307) |
| receive | site Z took CLOUD 276e94b50c; the file present in its tree | 11:09:44-45Z (msg 2331) |
| ACK | READ by 0.7.0_AE_CloudOps~ZG | 11:11:38Z, bus 9267a044 (msg 2334) |
| execute | GE2-AC1 on site Z's tree: `GS-E2-SITEZ ok=True arms=3 failed=0`; "ran from the mission tree with no seat-home copy: yes" | 79e603bf34, `deliverables/0.7.0_AE_CloudOps~ZG/SITEZ_READ_round2.md` |

Gaps seen on the way (row NFRA_GATSCP-D1-S10, beside the lane's own row Z-S1): the issuing COO cannot commit the crossbox file it
opens, and the receiving lane cannot commit its ACK (DEVICES_CROSSBOX admits managers only); box/sitez's integrate HELD at
11:35Z on the crossbox record (`bus_message_id` on one side, null on the other) and on this project's channel (an append union),
both resolved by 0.0.0_AB_MSTR~Z at 12:1xZ, so the completion reached box/dell1 at 12:2xZ (@77d960385f).

## 3. FWD-5 -- the sync's standing line, on real box-sync code

`box-sync.sh grade` on site Z's tree printed `box-sync: 0 standing` (GS-e-2's report); the QA syncs of round 1 printed nothing.
The organic sync line on box/dell1 is read at the next scheduled pass.

## 4. FWD-4 and FWD-6 on box/dell1

The ROUND_CLOSE commit of round 2 stages `project.json` alone, through safe-commit, with no derive run by hand; its commit must
carry `org/projects/NFRA_GATSCP.json`, and its close gate grades round-close-check `--staged`. Recorded in that commit's message.
