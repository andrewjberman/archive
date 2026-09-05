# NFRA_OUTSET.TO-OS-s-6 -- RESULT: who can call the federated transport

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-6` · **outcome_ref:** FWD-2
**Verb:** audit -- MEASURE and RECORD. No principal, policy or resource was created or changed.
**Written at:** 2026-09-04 ~21:4xZ · **Repo vintage:** HEAD `14f26b5eff` on `CLOUD`
**Push state (MEASURED, `git ls-remote origin CLOUD`):** LOCAL @`14f26b5eff`; origin/CLOUD @`fa82d6b93c`.

---

## 0. WHAT THE TRANSPORT IS -- the object this audit is about

Read at source from `.tools/_trino_fed.py` (the engine `comp-heat federated` imports; `.tools/comp-heat:350`
names it). Constants at `:31-36`, the requirement stated by the producer itself at `:84`:

```
CLUSTER   = "opal-globgrph"
TASK_DEF  = "globgrph-trino"
LOG_GROUP = "/ecs/globgrph/trino"
REGION    = "us-east-1"
:84  "Requires boto3 + AWS creds with ecs:RunTask on the globgrph-trino task-def + logs:GetLogEvents."
```

The APPLIED identity of the task definition, read live (read-only):

```
$ .tools/aws ecs describe-task-definition --task-definition globgrph-trino --region us-east-1
  arn      : arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-trino:6
  family   : globgrph-trino   rev: 6
  taskRole : arn:aws:iam::313476888478:role/opal-globgrph-trino-task
  execRole : arn:aws:iam::313476888478:role/opal-globgrph-trino-execution
```

⚠ **GRAIN NOTE, load-bearing for every count below.** `ecs:RunTask` is authorized against the
**task-definition** ARN (`.../globgrph-trino:6`). `logs:GetLogEvents` is authorized against the
**log-group** ARN (`.../log-group:/ecs/globgrph/trino`). These are two different resource grains and
mixing them is the false-deny this audit measured (row `NFRA_OUTSET-S3`, §4).

---

## 1. CRITERION O6-AC1 -- MECHANICAL -- **FAIL AS WRITTEN (CUT DEFECT, row `NFRA_OUTSET-S1`)**

The face names `<invocation>python .tools/comp-iam --help</invocation>` with `<expect>usage</expect>`.

```
$ timeout 120 python .tools/comp-iam --help
  File "C:\Users\AndrewBerman\Desktop\ajb_workspace\.tools\comp-iam", line 4
    WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
                     ^
SyntaxError: invalid syntax
RC = 1        matches for "usage" = 0        (denominator: 1 invocation, 1 expect clause)
```

**Why:** `.tools/comp-iam` is not a Python file.

```
$ head -1 .tools/comp-iam      -> #!/bin/bash
$ file .tools/comp-iam         -> Bourne-Again shell script, ASCII text executable
```

It is a bash forwarder onto `org/modules/graph/iam_cli.py` (`.tools/comp-iam:5`). The instrument the
estate actually runs satisfies the criterion's INTENT exactly:

```
$ timeout 120 comp-iam --help
RC = 0        matches for "usage" = 1
usage: comp-iam [-h]
                {gaps,roles,services,service,role,stats,reconcile,attach-census,resource-sweep,
                 gaps-filtered,simulate,simulate-self-test,refresh-census,census-self-test,live,
                 investigate-candidates,investigate-candidates-self-test} ...
```

**Recorded, not worked around.** A mechanical criterion's pass "is decided by the MATCH and never by
your opinion", so I do not substitute the working invocation on my own authority. `O6-AC1` is
**FAIL** and `TO-OS-s-6` is **NOT flipped to complete** -- the proof_of_spec guard requires every
MECHANICAL criterion to PASS. The fix is the issuer's (amend the `<invocation>` to `comp-iam --help`),
per the GO: "If something in a face is wrong or missing, that is a CUT DEFECT and it is mine."

**⚠ Self-correction carried because it is the instructive part.** My first read of this printed
`RC=0`. That rc was `head`'s, not python's -- the rc of a pipeline is its LAST stage. Re-measured with
the rc captured before any pipe, the true value is `RC=1`. The defect verdict is unchanged; the first
number was wrong and would have been wrong in the *exonerating* direction.

---

## 2. CRITERION O6-AC2 -- JUDGMENT -- THE HOLDERS, MEASURED. NO VERDICT.

### 2.1 The APPLIED plane read and its vintage

```
$ timeout 120 comp-iam refresh-census          RC = 0
OK: APPLIED census written -> docs/briefs/cmpaws-iam-census-20260904.json
  generated_utc : 2026-09-04T21:18:31Z     account: 313476888478
  api           : iam:GetAccountAuthorizationDetails
  roles: 224 | groups: 1 | users: 7
```

Refreshed **before** use, per the 24h-TTL trap (this census has been measured 27 days stale in the past).
**Vintage: 2026-09-04T21:18:31Z. Age at read: minutes.**

### 2.2 Holders -- ROLE plane (denominator: 224 roles)

Matched wildcard-aware (`fnmatch` over action and resource, so `ecs:*` and `*` are caught), effect
respected, condition recorded.

| action | holder | grant | resource | conditioned |
|---|---|---|---|---|
| `ecs:RunTask` | `lambda-execution-role` | inline `FargateTriggerPermissions` | `*` | no |
| `logs:GetLogEvents` | `infrastructure-ops-lambda-role` | inline `LogsRead` | `*` | no |
| `logs:GetLogEvents` | `opal-portal-lambda-role` | inline `MonitorReadLambdaLogs` | `arn:aws:logs:us-east-1:313476888478:log-group:*` | no |
| `logs:GetLogEvents` | `workspace-sync-lambda-role` | inline `CloudWatchLogsRead` | `*` | no |

**Explicit Deny found (1):** `opal-drift-producer-codebuild-role`, sid `DenySensitiveDataReads`, on
`logs:GetLogEvents`. Recorded because an explicit Deny is not the absence of a grant.

**These are counts over the INLINE plane only. They are a FLOOR, not the answer** -- see §3.

### 2.3 Holders -- the USER plane, and the answer to the cell's real question

The census counts **7 users and 1 group** and **enumerates none of them** -- it has exactly three
top-level keys (`_meta`, `summary`, `roles`). Any user- or group-held grant is therefore invisible to
§2.2. I read that plane directly:

```
$ .tools/aws sts get-caller-identity
  Arn : arn:aws:iam::313476888478:user/Andrew_Berman        Account: 313476888478

$ .tools/aws iam list-attached-user-policies --user-name Andrew_Berman
  OpalSecretsReader | ycharts-credentials-read | inf-andrew-otp-write | IAMUserChangePassword
$ .tools/aws iam list-user-policies --user-name Andrew_Berman        -> []   (no inline)
$ .tools/aws iam list-groups-for-user --user-name Andrew_Berman      -> ["AdministratorAccessOpalCapital"]
$ .tools/aws iam list-attached-group-policies --group-name AdministratorAccessOpalCapital
  AdministratorAccess  (arn:aws:iam::aws:policy/AdministratorAccess)
$ .tools/aws iam list-group-policies --group-name AdministratorAccessOpalCapital  -> []
```

**`user/Andrew_Berman` holds both actions, via group -> `AdministratorAccess` (`Action:*`,`Resource:*`).**
Not via any of its four directly-attached policies, none of which grants either action.

### 2.4 Discrimination -- APPLIED simulate, ONE `--resource-arns` per call

The multi-ARN poisoning trap was respected: every call below carries exactly one resource ARN.

```
principal arn:aws:iam::313476888478:user/Andrew_Berman
  ecs:RunTask       @ arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-trino:6   -> allowed
  logs:GetLogEvents @ arn:aws:logs:...:log-group:/ecs/globgrph/trino                        -> allowed
  logs:GetLogEvents @ arn:aws:logs:...:log-group:/ecs/globgrph/trino:*                      -> allowed
  logs:GetLogEvents @ *                                                                     -> allowed
```

Controls run so the instrument is not taken on trust:

```
NEGATIVE CONTROL  role/advi-49f-floor-scheduler-role  ecs:RunTask @ globgrph-trino:6   -> implicitDeny  (fires)
POSITIVE CONTROL  role/advi-49f-floor-scheduler-role  lambda:InvokeFunction @ its own function -> allowed (fires)
```

Both controls discriminate, so an `allowed` above is not the simulator saying yes to everything.

### 2.5 CAN A WORKER SUBAGENT CALL IT? -- the question this cell exists to settle

**A worker subagent holds no cloud identity of its own, and it does not need one.** It is a subprocess
on this box; it inherits the box's ambient AWS credentials. Those credentials resolve to
`user/Andrew_Berman` (§2.3), which is in `AdministratorAccessOpalCapital`, which carries
`AdministratorAccess`.

So the measured answer is: **yes -- a worker subagent can call the federated transport, and it does so
holding `Action:*` on `Resource:*`, not a scoped transport identity.** There is no separate worker
principal to scope, because there is no worker principal at all. Every seat, every lane and every
worker subagent on this device is the same IAM user with full administrative rights.

Recorded without a verdict, as the criterion requires. I note only that the "who can call it" question
and the "what else can the caller do" question have the same answer here, and `3.0.0_SA_CVO` may wish
to grade that at L9.

### 2.6 CAN THE REPORT HOST CALL IT? -- **UNREADABLE**

**UNREADABLE, reason:** the report host is a PRD-§3 design object, not a provisioned resource I could
find on the APPLIED plane. The PRD describes it as "a minimal, self-parking box working from a blobless
clone" (`NFRA_OUTSET_PRD.md:180-183`) and the consumption seam it belongs to is what `OS-s-10` is cut to
settle. No instance, instance profile or role bearing a report-host identity was resolvable at this
vintage. **Not asserted as none** -- asserted as not-yet-existing-to-measure. Its caller contract is
answerable only once the seam lands.

---

## 3. CRITERION O6-AC3 -- JUDGMENT -- WHAT I COULD NOT RESOLVE. NO VERDICT.

**UNREADABLE-1 -- attached-managed policy statements: 137 of 224 roles (61.2%).**
The census discloses this itself: `managed_policies_resolved: false`, and its own note --
"attached-managed policies are RECORDED, not resolved -- their statements are marked UNRESOLVED. A
reconcile treats them as uncovered, never as absent." So §2.2's counts cannot be read as complete.

I bounded that overhang rather than leaving it open. Across the census there are **35 distinct managed
policy ARNs**; by name and AWS-published content, exactly one could bear on either target action:

| policy | roles | bearing |
|---|---|---|
| `arn:aws:iam::aws:policy/ReadOnlyAccess` | 1 | grants `logs:GetLogEvents`; does **not** grant `ecs:RunTask` |
| `service-role/AmazonECSTaskExecutionRolePolicy` | 5 | image pull + log **write** for the task; **not** `ecs:RunTask` |
| `service-role/AWSLambdaBasicExecutionRole` | 96 | log group/stream create + `PutLogEvents`; **not** `GetLogEvents`, not `RunTask` |
| the remaining 32 (SSM core, S3/asset fences, service-linked, DynamoDB, ECR, RDS monitoring, DLM) | -- | no bearing on either action |

**Residual after bounding: at most 1 additional `logs:GetLogEvents` holder, and 0 additional
`ecs:RunTask` holders, could be hiding in the unresolved managed plane.** This is an argument from
policy names and published AWS content, **not** a resolution of the 137 documents -- I did not call
`iam get-policy-version` on each. It is `inferred`, and §2.2 remains `measured`.

**UNREADABLE-2 -- the user and group planes are absent from the census artifact.** 7 users and 1 group
are counted in `summary` and enumerated nowhere. I resolved the one user that mattered (the local
caller, §2.3) and its one group directly from the live API. **The other 6 users were not swept** --
their grants on these two actions are UNREADABLE at this vintage. Reason: the cell's question is the
caller contract of the transport, and the caller I could observe is the one that runs it; a 6-user
sweep is a defensible next cut but was not this order's clause.

**UNREADABLE-3 -- resource-policy and permissions-boundary planes not traversed.** No boundary is set on
the measured user; boundaries on the 224 roles were read as a field (`permissions_boundary`) but not
evaluated as constraints against these two actions.

### The false-deny traps -- both bound here, and a THIRD one measured

1. **CONDITIONED-grant false deny.** Respected. Every holder in §2.2 is recorded with its `condition`
   field; all four matching grants are unconditioned, so no verdict here rests on a simulate result over
   a conditioned grant.
2. **Multi-ARN poisoning.** Respected -- one `--resource-arns` per call, every call (§2.4).
3. **NEW, measured this session (row `NFRA_OUTSET-S3`): a WRONG-GRAIN resource ARN is a third false-deny
   mode.** `logs:GetLogEvents` simulated against the **log-stream**-grain ARN
   `...:log-group:/ecs/globgrph/trino:log-stream:*` returns **`implicitDeny`** for a principal holding
   `AdministratorAccess` -- a decision that is impossible on the world and is purely the instrument.
   The same action against the three **log-group**-grain forms returns `allowed` (§2.4). I caught it only
   because `*`/`*` makes a deny self-evidently false; **on a narrowly-scoped principal this mode is
   invisible and reads as a true negative.**

---

## 4. ROWS FILED

`org/missions/D11/NFRA/NFRA_OUTSET/surprise-channel/investigations/INVESTIGATION_v1.md` (this seat mints
the file; both my orders name it in `<paths>`):

| row | class | one line |
|---|---|---|
| `NFRA_OUTSET-S1` | **BLOCKING** | `O6-AC1`'s invocation runs a bash script under `python`; cannot pass as written |
| `NFRA_OUTSET-S2` | OBSERVATION (ARMED) | `comp-find` content mode returns rc=124 with empty stdout -- a timeout that reads as a zero |
| `NFRA_OUTSET-S3` | OBSERVATION (ARMED) | wrong-grain resource ARN is a third `simulate-principal-policy` false-deny mode |
| `NFRA_OUTSET-S4` | **BLOCKING** | 16 of 17 faces in this issuance name their proof instance by a stem `to-pipeline-gate.py` does not search |

⚠ **`NFRA_OUTSET-S4` also changes where this order's own proof instance lives.** The face's
`<proof_of_spec>` block names
`.../deliverables/0.7.0_AE_CloudOps~W/NFRA_OUTSET.TO-OS-s-6.proof_of_spec.json`, but
`.tools/to-pipeline-gate.py:1261-1270` globs the **full face stem**, so the instance is written at
`.../NFRA_OUTSET.TO-OS-s-6.federated-transport-caller-contract-iam.proof_of_spec.json` instead -- the same
granted folder, a different filename. The mechanism was obeyed over the prose, and the divergence is
recorded here rather than left for the next reader to rediscover.

## 5. WHAT I CHANGED

**On AWS: nothing.** Every call was `describe-*`, `list-*`, `get-caller-identity`,
`simulate-principal-policy` or `s3api list-objects-v2`. No principal, policy, resource, task or log was
created, modified or deleted. `comp-iam refresh-census` wrote one local artifact
(`docs/briefs/cmpaws-iam-census-20260904.json`) and made no AWS mutation.

**In the repo:** only the two paths in my `<paths>` grant, plus the census artifact the instrument writes
by its own design.
