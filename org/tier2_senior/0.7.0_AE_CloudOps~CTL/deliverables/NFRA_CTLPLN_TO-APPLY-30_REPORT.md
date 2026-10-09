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

---

# AMENDMENT 1 -- the retry (pair 2)

The issuer reopened the order at ~14:1xZ for ONE retry of the same ledger
`irpt-ycdgen-served-read-20261009` under the same CTO consent (msg 107976) and the same dell2 CTO half
@`da885deef2`, for a served read of `REQ-5e4149d2`. Same two signed documents, same set rule, a NEW
NEVER-2 entry as the amendment requires. Pair 1 above stays closed as recorded.

## THE RETRY WINDOW WAS OPEN 15 MINUTES 19 SECONDS AND IS SHUT -- AND THIS TIME THE READ LANDED

| event | time (UTC) |
|---|---|
| GO ADD (AMENDMENT 1, msg 107989) | 14:14Z |
| start read (live = signed BEFORE) | 14:17:11Z |
| new NEVER-2 entry opened, **before** the put | 14:18Z |
| **ADD put** | **14:19:47 - 14:19:50Z** |
| read-back + 3 simulations | 14:20Z |
| put time relayed to G2 via `0.0.0_AB_MSTR` for W1 | 14:23:02Z |
| **G2's svc secret read (its act, in memory only)** | **~14:26:12Z** |
| G2 called R DONE | 14:26:19Z |
| **REMOVE put** | **14:35:05 - 14:35:09Z** |
| read-back + 3 simulations | 14:36Z |
| ledger + sentinel CLOSED | 14:38:23Z |
| hard close (ADD + 30m) | 14:49:50Z -- **met with 14 min 41 s to spare** |

## LEG ADD (retry)

Start 14:17:11Z, 816 bytes read whole: `SET-EQUAL` to signed **BEFORE**; `NOT SET-EQUAL` to ADD (rc=1,
exactly the two dell2 elements). That start read does double duty -- it is also the independent confirmation
that pair 1's REMOVE had fully landed, measured on the live document rather than inferred from pair 1's own
read-back.

Read-back 944 bytes: `SET-EQUAL` to signed **ADD**; `NOT SET-EQUAL` to BEFORE. Token census over the whole
document: `cloudops-dell2-agent-user` **2**, `cloudops-dell1-agent-user` **0**.

| principal | decision | required |
|---|---|---|
| `user/cloudops-dell2-agent-user` | **allowed** | allowed |
| `user/cloudops-dell1-agent-user` | **explicitDeny** | explicitDeny |
| `user/Andrew_Berman` | **allowed** | allowed |

## LEG REMOVE (retry)

Ran on G2's R DONE, not on the clock. An ADD+27m alarm was armed at the moment of the ADD and stopped unused
-- as in pair 1, the clock was carried independently of the message so the hard close was covered either
way.

Start 14:34:14Z: `SET-EQUAL` to ADD; `NOT SET-EQUAL` to BEFORE. Read-back: `SET-EQUAL` to signed BEFORE;
`NOT SET-EQUAL` to ADD. Token census: `cloudops-dell2-agent-user` **0**, `cloudops-dell1-agent-user` **0**.
**AC1**: `Sid: WalkerReadsByExplicitArn` present, `Principal.AWS` = `user/Andrew_Berman` alone.

| principal | decision | required |
|---|---|---|
| `user/cloudops-dell2-agent-user` | **explicitDeny** | explicitDeny |
| `user/cloudops-dell1-agent-user` | **explicitDeny** | explicitDeny |
| `user/Andrew_Berman` (the walker) | **allowed** | allowed |

## Both pairs together

Four legs, four start reads, four read-backs, **eight** negative controls and **twelve** simulated
decisions. Total open window across both pairs: **23 minutes 24 seconds**. Two NEVER-2 entries, both CLOSED,
both sentinels removed. **Zero `GetSecretValue` calls by this seat** on any leg -- dell2's read at
~14:26:12Z is G2's act under its own ledger.

## Ledger (retry)

`org/critical_paths/change_management/20261009T1418Z_svc-irpt-served-read-retry-laptop-20261009_deploy_completion.md`
-- opened 14:18Z before the put, both legs closed with the proof above, entry **CLOSED** 14:38:23Z, sentinel
removed.
