# NFRA_CTLPLN.TO-APPLY-30 -- both legs report

**archetype:** DEPLOY
**seat:** 0.7.0_AE_CloudOps~CTL | **issuer:** 2.0.0_SA_COO~C | **risk:** WORLD | **date:** 2026-10-09

## THE WINDOW WAS OPEN 8 MINUTES 5 SECONDS AND IS SHUT

`arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l`

| event | time (UTC) |
|---|---|
| GO LEG ADD (CTO yes msg 107976, addendum @`075fab8835`) | 13:31Z |
| NEVER-2 entry opened, **before** the put | 13:35Z |
| **ADD put** | **13:37:33 - 13:37:36Z** |
| read-back + 3 simulations | 13:38Z |
| G2's REMOVE NOW (relay `2.0.0_SA_COO~C` msg 107980) | 13:42Z |
| **REMOVE put** | **13:45:37 - 13:45:41Z** |
| read-back + 3 simulations | 13:46Z |
| ledger + sentinel CLOSED | 13:49:46Z |
| hard close (ADD + 30m) | 14:07:36Z -- **met with 21 min 55 s to spare** |

## LEG ADD

**Start (live must equal the signed BEFORE, else STOP).** 13:34:08Z, 816 bytes read whole.

- live vs signed **BEFORE** -> `SET-EQUAL` (rc=0). The declared start held.
- live vs signed **ADD** -> `NOT SET-EQUAL` (rc=1), differing in exactly 2 places:
  `Statement[0].Principal.AWS` length 1 vs 2 and `Statement[1].Condition.ArnNotEquals.aws:PrincipalArn`
  length 1 vs 2.

**Put.** The signed ADD file, `--block-public-policy`.

**Read-back.** 944 bytes. `SET-EQUAL` to signed ADD; `NOT SET-EQUAL` to BEFORE (same 2 places inverted).
Token census over the whole document: `cloudops-dell2-agent-user` **2** (the Principal entry and the Deny
exception), `cloudops-dell1-agent-user` **0**.

**Simulations** against the live widened policy:

| principal | decision | required |
|---|---|---|
| `user/cloudops-dell2-agent-user` | **allowed** | allowed |
| `user/cloudops-dell1-agent-user` | **explicitDeny** | explicitDeny |
| `user/Andrew_Berman` | **allowed** | allowed |

Exactly the three the order requires, so the "any other result -> put BEFORE back at once" branch did not
fire.

## LEG REMOVE

Ran on G2's REMOVE NOW, not on the clock. An ADD+27m alarm was armed as a background clock at the moment of
the ADD, so the hard close was covered without waiting for any GO; it was stopped unused when the
REMOVE-NOW arrived.

**Start.** 13:44:52Z: `SET-EQUAL` to signed ADD; `NOT SET-EQUAL` to BEFORE.

**Put.** The signed BEFORE file, `--block-public-policy`.

**Read-back.** `SET-EQUAL` to signed BEFORE; `NOT SET-EQUAL` to ADD. Token census over the whole live
document: `cloudops-dell2-agent-user` **0**, `cloudops-dell1-agent-user` **0**. **AC1**:
`Sid: WalkerReadsByExplicitArn` present, `Principal.AWS` = `user/Andrew_Berman` alone.

**Simulations** against the live restored policy:

| principal | decision | required |
|---|---|---|
| `user/cloudops-dell2-agent-user` | **explicitDeny** | explicitDeny |
| `user/cloudops-dell1-agent-user` | **explicitDeny** | explicitDeny |
| `user/Andrew_Berman` (the walker) | **allowed** | allowed |

## Method note the next window should keep

Every start read and every read-back was graded in **both** directions -- set-equal to the document it
should match, and NOT set-equal to the other signed document. Four such pairs across the two legs. A
comparator that agreed with everything would have printed `SET-EQUAL` on both sides of a pair, so the
opposite-direction read is what makes each agreement mean something. The walker `allowed` arm plays the same
role beside the two denies, and `explicitDeny` rather than `implicitDeny` distinguishes the
`NobodyElseReadsTheValue` statement firing from a merely absent grant.

**No secret value was read on either leg.** The only API calls against the secret were
`get-resource-policy`, `put-resource-policy` and `iam simulate-principal-policy`. Zero `GetSecretValue`.

## What the issuer already owns

G2 reports its served-read window ran 13:05:57Z-13:35:57Z and closed with **no read**, because the ADD had
not yet landed -- the GO reached this lane at 13:31Z and the ADD was live at 13:37:36Z, after G2's window had
shut. That ordering is the issuer's and dell2's to resolve; `2.0.0_SA_COO~C` has already stated any retry
arrives as a new GO with ADD first. This seat will not re-widen on its own, so no surprise row is filed for
a condition the issuer has dispositioned in writing.

## Ledger

`org/critical_paths/change_management/20261009T1335Z_svc-irpt-served-read-window-laptop-20261009_deploy_completion.md`
-- opened 13:35Z before the put, both legs closed with the proof above, entry **CLOSED** 13:49:46Z, sentinel
removed.
