# NFRA_OUTSET.TO-OS-s-18 -- THE PUBLISH: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Issuance:** `37b2a19129`
**Worked:** 2026-09-09 12:55Z -> 13:40Z (main tree, `CLOUD`). The seat was respawned 12:50:19Z after
the 2026-09-05 device crash took it mid-cell.
**Order status at this write:** `pending`. **NOT flipped to complete, and the reason is a CUT DEFECT
filed as `NFRA_OUTSET-S18` (BLOCKING).**

---

## THE ONE-PARAGRAPH ANSWER

The seam is real now. An outset tool's artifact is published at
`s3://opal-estate-report/outset/comp_heat_drift.json`, the runner's role holds `s3:GetObject` on the
prefix on the DESIRED and APPLIED planes, and **the role itself read the object** at 13:09Z -- not a
simulation, the actual principal making the actual call. A failed publish reads FAILED at every level
tested, including the rendered report text. **What did not land is the battery FILE.**
`.tools/tests/` is lane `TOOL_BATTERIES` owned by `0.8.0_AE_CloudComp`, and the `<paths>`-block-as-grant
mechanism the face's preflight relies on is implemented for WORKER serials only, so for this seat the
order's grant is inert and the criterion's own `<invocation>` path cannot exist at HEAD. That is the
issuer's to resolve; I stopped the criterion rather than overriding the lane.

---

## O18-AC1 -- MECHANICAL. Battery written, PASSES, CANNOT BE LANDED BY THIS SEAT.

**Invocation, exactly as the face cuts it:** `timeout 300 python .tools/tests/test_os18_seam_readable.py`
**Expect:** `OS18-SEAM-READABLE` · **Observed:** `OS18-SEAM-READABLE`, rc **0** (read from a
non-piped invocation -- a pipeline's rc is its last stage's, so `cmd | tail` would have reported
`tail`'s 0 regardless).
**Second required grain:** `python -m pytest -q .tools/tests/test_os18_seam_readable.py` -> `1 passed`, rc 0.

**DENOMINATOR: 13 of 13 evaluated arms PASSED, 0 NOT-EVALUATED (run at 13:10:23Z).** Verbatim:

```
  [PASS] A3-DESIRED-terraform-names-the-prefix       iam.tf occurrences of the seam resource = 1 (expected 1); reader negative control (a prefix that must not exist) = 0 (expected 0)
  [PASS] A2-APPLIED-simulate-with-both-controls      TARGET outset/comp_heat_drift.json -> allowed | NEG-CONTROL logs/<real object, Get NOT granted> -> implicitDeny | POS-CONTROL code/ -> allowed (3 separate calls, 1 resource-arn each)
  [PASS] A1-EXERCISED-by-the-role-itself             principal=arn:aws:sts::313476888478:assumed-role/estate-report-runner-role/i-0512bd3cbaf602b7f | GREEN(get outset/comp_heat_drift.json) rc=0 bytes=27060 | NEG-CONTROL(get logs/, Put-granted Get-NOT-granted) rc=254 | POS-CONTROL(head code/) rc=0
  [PASS] B1-live-seam-read-OK                        status=OK absent=False tool='comp-heat drift' age=0.11h rows=154 denominator='comp-heat drift -- tool_scalars.n=154; tool_scalars.n_modified=6; tool_scalars.n_untracked=148; budget_terminal=WITHIN B'
  [PASS] R1-broken-producer-publishes-FAILED         answer_state=FAILED published=True bytes=1028 denominators.claim=absent error='producer returned rc=2 and no parseable JSON answer'
  [PASS] R2-FAILED-publish-reads-FAILED-at-the-seam  s3 key=outset/_os18_red_arm_probe.json -> status=INSTRUMENT_FAILED absent=False rows=0 error='tool answer_state=FAILED: ...'
  [PASS] R3-the-RENDERED-report-says-FAILED          status=INSTRUMENT_FAILED row_count=None rendered contains STATUS/INSTRUMENT_FAILED/PRODUCED NO DATA = True/True/True
  [PASS] R4-never-published-reads-FAILED-and-ABSENT  status=INSTRUMENT_FAILED absent=True error='artifact ABSENT at s3://opal-estate-report/outset/_os18_never_published.json -- the publish FAILED or never ran...'
  [PASS] R5-stale-reads-FAILED-not-fresh             status=INSTRUMENT_FAILED absent=False age=999.0h error='artifact STALE ... age 999.0 h > ceiling 26.0 h'
  [PASS] R6-future-dated-is-REFUSED                  status=INSTRUMENT_FAILED error='artifact DATED IN THE FUTURE ... 48.0 h ahead of this host'
  [PASS] R7-unmapped-answer_state-is-REFUSED         status=INSTRUMENT_FAILED error="answer_state 'TOTALLY_FINE_HONEST', outside the seam's declared domain"
  [PASS] R8-OK-and-FAILED-renderings-are-NOT-byte-identical   statuses OK vs INSTRUMENT_FAILED | rendered lengths 4151 vs 1436 | 'PRODUCED NO DATA' in failed=True, in good=False
  [PASS] M-planted-mutant-is-REFUSED                 mutated FAILED->OK mapping; the consumer then read a FAILED artifact as status=OK (the arm passes by DETECTING this)
```

### The RED arm, which is what the face cut this criterion for

The face named the red arm because of `W2-S21`: 35,752 rows rendered as a confident ZERO with rc=0,
`answer_state` OK, correct vintage, correct denominators and a correct re-run recipe -- and four
batteries with 51 green arms missed it, because every fixture in the estate put rows at the top level.

So the publish was made to FAIL FOR REAL rather than hand-authored. **R1** runs the producer against a
tool path that does not exist; the producer publishes an artifact with `answer_state=FAILED`, a
`denominators.claim=absent` and the subprocess's own error -- it never publishes nothing. **R2** puts
that artifact ON the seam in S3 and reads it back through the real consumer: `INSTRUMENT_FAILED`,
`absent=False`, zero rows. **R3** takes the last step the criterion actually asks for, the RENDERED
report text, which carries `STATUS: *** INSTRUMENT_FAILED` and `THIS STRATUM PRODUCED NO DATA`.
**R8** is the arm those 51 green arms all assumed and none made: the OK rendering and the FAILED
rendering are **not byte-identical** (4151 vs 1436 bytes; the loud marker present in one, absent
from the other).

**ARM M plants a mutant**, because a declared-but-unrun falsifier is a promise and not a control. It
rewrites the one mapping the seam rests on -- `"FAILED": "INSTRUMENT_FAILED"` -> `"OK"` -- in a COPY
of the runner, and passes by DETECTING that the mutated consumer then reads a genuinely-failed
artifact as OK. The anchor's uniqueness is asserted first, so the arm refuses rather than silently
mutating nothing (`W2-S17`).

### A1 degrades to NOT-EVALUATED, and that was exercised rather than promised

The host stops itself after every run. The 13:10:23Z run caught it up (13 of 13, EXERCISED recorded).
A re-run at 13:12Z, after it self-stopped at **13:11:04Z**, recorded **12 of 12 PASSED and 1
NOT-EVALUATED**, quoting the instance state as the reason. A verdict vocabulary with no NOT-EVALUATED
value encodes non-evaluation as a verdict; this one has the value and the arm is never counted as a pass.

### Why it is not committed

`.tools/safe-commit.sh` refused: `owned-paths lane violation ... lane=TOOL_BATTERIES ... agent=0.7.0_AE_CloudOps~W
not in permitted_agents`, rc 1, with commit-gate and to-pipeline-gate passing immediately before it.
Verified against the repository and not the tool's stdout: the file is absent from `git log`. Root
cause, remedies and the override I declined are in **`NFRA_OUTSET-S18`**. The battery is complete and
sits in the working tree ready to land unchanged.

---

## O18-AC2 -- JUDGMENT. THE GRANT, on both planes. Recorded with vintage, NO VERDICT.

`3.0.0_SA_CVO` grades this at L9. What follows is measurement only.

### DESIRED (terraform)

`infra/aws/terraform/estate-report/iam.tf`, `aws_iam_role_policy.runner`, statement
`ReadPredecessorAndOwnCode`: `"${aws_s3_bucket.estate_report.arn}/outset/*"` added, `s3:GetObject`
only. Committed `54ccbdb47d`. `terraform plan` with the vendored `.tools/terraform.exe` v1.9.8:
**0 to add, 1 to change, 0 to destroy**, the single change being one element appended to one Resource
array. Applied via `.tools/safe-apply.sh` (never bare `terraform apply`) -> `Apply complete!
Resources: 0 added, 1 changed, 0 destroyed`. Unscoped re-plan afterwards: **`No changes. Your
infrastructure matches the configuration.`**

`s3:ListBucket` was deliberately NOT extended to the prefix. The consumer composes EXACT keys
(`estate_report_runner.py:1844`), so a seam reader that cannot enumerate can fetch only the keys its
own contract names. The `ListOwnPrefixes` statement stays at `daily/`, `manifest/`, `code/`.

### APPLIED (`iam:GetAccountAuthorizationDetails`, via `comp-iam refresh-census`)

Census refreshed first, as the face requires (24 h TTL, nothing refreshes it):
`docs/briefs/cmpaws-iam-census-20260909.json`, `generated_utc 2026-09-09T13:00:19Z`, account
313476888478, 224 roles / 1 group / 7 users.

`estate-report-runner-role` resolved statements, **denominator 6 resolved + 1 UNRESOLVED, all read**:

| Sid | Actions | Resources |
|---|---|---|
| WriteOwnOutputPrefixesOnly | s3:PutObject | daily/\*, manifest/\*, logs/\* |
| **ReadPredecessorAndOwnCode** | **s3:GetObject** | **daily/\*, code/\*, manifest/\*, kuzu_nessie_db, `outset/*`** |
| ListOwnPrefixes | s3:ListBucket | bucket, condition StringLike s3:prefix daily/\*, manifest/\*, code/\* |
| ReadItsTwoSecrets | secretsmanager:GetSecretValue | 2 secret ARNs |
| Logs | logs:Create\*/PutLogEvents | logs:us-east-1:313476888478:\* |
| SelfStopThisInstanceOnly | ec2:StopInstances | instance/i-0512bd3cbaf602b7f |

**`W1-S19` IS CORROBORATED, NOT CORRECTED.** It measured the role holding `s3:GetObject` on three
prefixes plus one exact key and **nothing on the globgrph bucket**. Both hold at this vintage: the
three prefixes are `daily/`, `code/`, `manifest/`, the exact key is `kuzu_nessie_db`, and no statement
in the role names any `opal-313476888478-globgrph` ARN. `outset/*` is the fifth element and is this
order's own addition.

**COVERAGE QUALIFIER, stated rather than assumed:** the seventh statement is
`managed:arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore`, recorded **UNRESOLVED** -- the census
does not fetch attached-managed statements. A reconcile treats it as uncovered, never as absent, and
so does this row. Nothing here claims that policy grants no S3 reach; it claims it was not read.

### EXERCISED -- the reading the other two planes cannot give

At 13:09Z the box was up (the daily 09:00 ET run, 13:00:45Z -> 13:11:04Z). An SSM invocation on
`i-0512bd3cbaf602b7f` produced, from `sts:GetCallerIdentity` **inside the same invocation** so the
identity cannot be mine or the agent's ambient one:

```
arn:aws:sts::313476888478:assumed-role/estate-report-runner-role/i-0512bd3cbaf602b7f
GetObject outset/comp_heat_drift.json   -> rc=0, 27060 bytes, seam=NFRA_OUTSET/OS-s-10, answer_state=OK
GetObject logs/<a REAL object>          -> rc=254 AccessDenied   (NEGATIVE CONTROL: Put granted here, Get not)
head-object code/estate_report_runner.py-> rc=0                  (POSITIVE CONTROL, separate call)
ListObjectsV2 prefix outset/            -> AccessDenied           (as designed: no ListBucket on this prefix)
```

The negative control is on an object that EXISTS, so the deny is action-level rather than the
403-because-absent an unpublished key returns.

**INSTRUMENT DISCIPLINE, since all three known `simulate-principal-policy` false-deny modes are live:**
one `--resource-arns` per call and three separate invocations (a batched call flips held resources to
implicitDeny and would have disarmed both controls); no `--context-entries` needed, and that is READ
rather than assumed -- the target statement carries `condition: null` in the census, so a deny could
not have been the conditioned-grant mode. The wrong-grain mode does not apply: the ARN is at object
grain, which is the grain `s3:GetObject` is authorized on.

### THE PUBLISH ITSELF

`python org/modules/heatmap/outset_seam.py --tool .tools/comp-heat --out-dir s3://opal-estate-report/outset`
-> `SEAM PUBLISH: 2 of 2 producer(s) published a non-FAILED artifact`.

| Key | Bytes | LastModified (s3api, UTC) |
|---|---|---|
| outset/comp_heat_drift.json | 27060 | 2026-09-09T13:03:50Z |
| outset/comp_heat_freshness_tools.json | 63822 | 2026-09-09T13:03:49Z |

**The prefix held ZERO objects before this** (`list-objects-v2` returned no `Contents` key at all).
`s3api` is used throughout rather than `aws s3 ls`, which renders local time.

---

## ROWS FILED

| Row | Class | Standing | What |
|---|---|---|---|
| `NFRA_OUTSET-S16` | OBSERVATION | ARMED | The seam is readable and published-to and **nothing configures the consumer to look**: `ESTATE_OUTSET_SEAM_PREFIX` is absent from `runtime.env` in `instance.tf` and named by neither order. Setting it is not a config edit -- `user_data_replace_on_change = true`, so it is an instance replacement. |
| `NFRA_OUTSET-S17` | OBSERVATION | ARMED | The publish has **no cadence**. Written by hand at 13:03:50Z against a 26 h ceiling, so it reads STALE from about 2026-09-10T15:03Z. The seam's steady state under the work as cut is FAILED. No schedule was built -- the moratorium reserves that to Andrew. |
| `NFRA_OUTSET-S18` | **BLOCKING** | ARMED | The cut defect above. Three granted paths unwritable by this seat; the two battery files are the `<invocation>` targets of `O18-AC1` and `O19-AC1`. |

## WHAT I DID NOT DO, AND WILL NOT UNASKED

- **Did not use `GIT_COMMIT_AUTHOR_OVERRIDE`** to force the battery into `TOOL_BATTERIES`. That lane
  is built so that gate and author are different seats, with `1.0.0_SA_CTO` gating battery work;
  collapsing that separation is not an assignee's call.
- **Did not set `ESTATE_OUTSET_SEAM_PREFIX`.** My `<paths>` DO grant `infra/aws/terraform/`, so this
  is not a cut defect and I am not claiming one -- I can reach the file and am declining, because an
  instance replacement neither criterion asks for is scope I do not hold.
- **Did not build a producer schedule.** Standing moratorium.
- **Did not start `TO-OS-s-19`.** It is sequenced behind this order, this order is not terminal, and
  its own `O19-AC1` battery file hits the identical lane refusal.
- **Did not push.** `git push` is refused under this order's BOUNDS.
