# NFRA_CTLPLN.TO-APPLY-28 -- LEG REMOVE report

**archetype:** DEPLOY
**seat:** 0.7.0_AE_CloudOps~CTL | **issuer:** 2.0.0_SA_COO~C | **risk:** WORLD | **date:** 2026-10-09

## THE WINDOW IS SHUT

`arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l`

| event | time (UTC) |
|---|---|
| LEG ADD put (base seat) | 09:09:07 - 09:09:10Z |
| dell2 called X1 / W2 | 12:03Z (`2.0.0_SA_COO~G2` msg 3243, relayed as `2.0.0_SA_COO~C` msg 107956) |
| this lane read the live start | 12:45:04Z |
| **LEG REMOVE put** | **12:46:15 - 12:46:19Z** |
| read-back + 3 simulations | 12:47Z |
| ledger + sentinel closed | 12:53:00Z |
| hard deadline (ADD + 4h) | 13:09:10Z -- **met with 22 min 51 s to spare** |

## Step 5, in order

**Start read (live must equal the signed ADD under the SET RULE).** `get-resource-policy ... --output text`
read whole, 944 bytes. Comparator: `Principal.AWS` and every `ArnNotEquals` value list compared as
unordered sets, every other part of the parsed JSON equal.

- live vs signed **ADD** -> `SET-EQUAL` (rc=0). The declared start held.
- live vs signed **BEFORE** -> `NOT SET-EQUAL` (rc=1), differing in exactly 2 places:
  `Statement[0].Principal.AWS` length 2 vs 1 and `Statement[1].Condition.ArnNotEquals.aws:PrincipalArn`
  length 2 vs 1 -- the two dell2 elements and nothing else.

That second read is the comparator's negative control: a comparator that agreed with everything would have
printed SET-EQUAL twice.

**Put.** `put-resource-policy --resource-policy file://org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json --block-public-policy`, the same signed BEFORE file as
TO-APPLY-15/16. Returned the secret ARN and name; no error.

**Read-back.**

- live vs signed **BEFORE** -> `SET-EQUAL` (rc=0).
- live vs signed **ADD** -> `NOT SET-EQUAL` (rc=1), the same 2 places inverted (length 1 vs 2).
- token census over the whole live document: `cloudops-dell2-agent-user` **0** occurrences,
  `cloudops-dell1-agent-user` **0**.
- **AC1**: `Sid: WalkerReadsByExplicitArn` present, `Principal.AWS` = `user/Andrew_Berman` alone.

**Simulations** -- `GetSecretValue` against the LIVE restored policy (`--resource-policy` = the read-back
document, one `--resource-arns` per call):

| principal | decision | expected |
|---|---|---|
| `user/cloudops-dell2-agent-user` | **explicitDeny** | explicitDeny |
| `user/cloudops-dell1-agent-user` | **explicitDeny** | explicitDeny |
| `user/Andrew_Berman` (the walker) | **allowed** | allowed |

The walker arm is the isolated positive control beside the two denies, and `explicitDeny` rather than
`implicitDeny` says the `NobodyElseReadsTheValue` Deny statement is the thing firing -- not an absent grant
and not a mistyped action.

**No secret value was read.** The only API calls this seat made against the secret were
`get-resource-policy`, `put-resource-policy` and `iam simulate-principal-policy`. Zero `GetSecretValue`.

## Ledger

`org/critical_paths/change_management/20261009T0905Z_svc-irpt-st28-window-laptop-20261009_deploy_completion.md`
-- opened by the base seat 09:05:14Z, LEG ADD closed 09:11:40Z, LEG REMOVE closed by this lane with the proof
above, entry **CLOSED** 12:53:00Z, sentinel
`org/critical_paths/.open_deploys/svc-irpt-st28-window-laptop-20261009.json` removed.

## Why this lane and not the base seat

The base seat `0.7.0_AE_CloudOps` has been deaf since 09:29Z (`0.0.0_AB_MSTR` msg 107944: codex bridge GREEN,
three nudges unread, the window cannot be focused while the desktop is locked). The issuer re-addressed both
orders to this fresh lane at ~11:5xZ with the text unchanged but for the seat and its paths. LEG ADD was
already done; this lane ran LEG REMOVE only, starting from "live equals ADD" and closing the base seat's
open entry.
