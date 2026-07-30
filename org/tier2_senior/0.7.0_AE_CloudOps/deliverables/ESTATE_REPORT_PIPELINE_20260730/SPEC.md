# ESTATE REPORT -- daily semantic-evolution pipeline: BUILD SPEC

**Author:** `0.7.0_AE_CloudOps~B` · **Approver:** `3.0.0_SA_CVO` · **Date:** 2026-07-30
**Status:** SUBMITTED FOR APPROVAL -- nothing built, no AWS resource created, no Terraform run.
**Authorizing record:** `ANDREW_DIRECT_RULINGS.md` (this folder, `@3acb8531c6`) +
`org/tier1_exec/3.0.0_SA_CVO/deliverables/ANDREW_RULING_SEMANTIC_EVOLUTION_PIPELINE_20260730.md`
(`@438d1c98da`, `@a83cf57bdb`).

---

## 0. What this pipeline is FOR (so a later reader does not optimize the wrong thing)

Andrew's Route B problem, verbatim: *"the semantics are changing despite no change to the surface
itself. There needs to be a way to manage semantics."*

Structure that can be compiled gets compiled (CTO's `RESOLVER_DEFROST_DESIGN.md`). **Prose cannot
be compiled -- it is hand-legislated by construction.** So what cannot be view-compiled must be
ACTIVITY-REVIEWED. This pipeline is that review loop's producer: it watches what actually moved in
the estate each day and proposes where the PROSE has probably gone stale.

**It proposes. It never lands.** Andrew ratifies, CVO lands. The AI suggests; legislation admits.

---

## 1. Architecture

```
  BUILD / SCHEDULE PLANE                        |   REVIEW / ACCESS PLANE
  --------------------------------------------- | ------------------------------------------
                                                 |
  aws_scheduler_schedule                         |
  "estate-report-0900et"                         |
  cron(0 9 * * ? *)                              |
  timezone America/New_York  <-- DST-native      |
        |                                        |
        | invoke (fire-and-forget)               |
        v                                        |
  aws_lambda_function                            |
  "estate-report-orchestrator"                   |
  python3.12 · timeout 60s · 128MB               |
    - ec2:StartInstances (instance-pinned)       |
    - returns in SECONDS. NEVER polls.           |
        |                                        |
        | start                                  |
        v                                        |
  aws_instance "estate-report-runner"            |
  AL2023 · t3.medium · STOPPED between runs      |
        |                                        |
        | systemd oneshot on boot (autostart)    |
        v                                        |
   +--------------------------------------+      |
   | 1. shutdown -h +90   <-- dead-man     |      |
   | 2. git fetch (window commits)         |      |
   | 3. DETERMINISTIC compile  ---------+  |      |
   | 4. Kimi K3 call (may fail) ------+ |  |      |
   | 5. assemble + write S3           | |  |      |
   | 6. write manifest = PENDING      | |  |      |
   | 7. self-stop (always, trap)      | |  |      |
   +----------------------------------|-|--+      |
                                      | |         |
                    (4) fails => (3) STILL SHIPS  |
                                      | |         |
                                      v v         |
  s3://opal-estate-report/                        |
    daily/YYYY/MM/DD/*.md|.json   <-- MINE ------ | --> /estate-pull (CVO skill) pulls the day
    manifest/YYYY-MM-DD.json      <-- MINE, born  |     Andrew + CVO adjudicate
                                      PENDING     |     CVO writes adjudicated/ + repo commit
    adjudicated/YYYY/MM/DD/*.md   <-- CVO's       |     CVO FLIPS the manifest
                                                  |     un-flipped prior day = LOUD at CVO load
```

### The one deliberate deviation from the reference module

`astn-pipeline/orchestrator.tf` is the canonical shape and I clone it **except** that its
orchestrator **polls its EC2 job to completion**. That re-imports Lambda's 900s hard ceiling into
the orchestrator even though the work already moved to EC2 -- and astn hit exactly that wall
(`orchestrator.tf:120-124`: *"900s is Lambda's HARD MAX... Do not 'fix' a future overrun by raising
this -- it cannot be raised"*). Its mitigation is to leave the box running on overrun for a separate
04:00 sweep.

**Andrew ruling 4a names this constraint directly.** Fire-and-forget removes it structurally: the
orchestrator's job is `StartInstances` and nothing else, so an 8-minute run and an 80-minute run are
the same architecture. Liveness of the run is not the orchestrator's business -- it is the
manifest's.

---

## 2. THE BOUNDARY -- what this pipeline writes, and what it must never write

Per CVO 221315Z item 2. **This is the load-bearing line in the spec**: the pipeline is a PRODUCER of
proposals, and the adjudication surface belongs to the reviewer. If the producer could write the
adjudicated file it could ratify its own suggestions.

| Object | Writer | Notes |
|---|---|---|
| `daily/YYYY/MM/DD/estate-report-YYYY-MM-DD.md` | **this pipeline** | human-readable report |
| `daily/YYYY/MM/DD/estate-report-YYYY-MM-DD.json` | **this pipeline** | machine half (resource sets, for the next day's delta) |
| `manifest/YYYY-MM-DD.json` | **this pipeline** | born `status: PENDING` |
| `adjudicated/YYYY/MM/DD/estate-report-YYYY-MM-DD.md` | **CVO** (`/estate-pull`) | pipeline IAM has NO write here |
| `org/estate-reports/YYYY-MM-DD.md` (repo) | **CVO** | greppable governance record, survives bucket lifecycle |
| manifest `status` FLIP (`PENDING` -> `ADJUDICATED` / `NO_SEMANTIC_CHANGES`) | **CVO** | pipeline never flips its own manifest |

**IAM enforces this, not convention:** the runner's `s3:PutObject` is resource-scoped to
`daily/*` and `manifest/*` only. A bug in my job physically cannot write `adjudicated/*`.

---

## 3. Report content -- the three sections Andrew named

### 3a. DETERMINISTIC changed-resource list (compiled, never AI)

Andrew: *"the deterministically compiled resource list of what was having changes (as a function of
git commit review)"*.

1. `git log --since <window_start> --until <window_end>` over `origin/CLOUD`, `--name-only`.
2. Changed paths -> estate resources via the **comp-estate resolver** (CVO input 5): each changed
   path buckets to its C3.ii vertical / chain, so a proposal cites its exact prose home (catalog
   entry / registry row / chain description) rather than a bare file path.
3. Emit: resource, chain, changed paths, commit count, authors, commit subjects.

**This half has NO dependency on Kimi and MUST compile when Kimi is down.**

### 3b. AI exec summary + semantic-prose proposals (Kimi K3)

Andrew: *"an Exec Summary of goings on and in the process there is some prompt that effectively
suggests potential semantic prose evolution for resources where things are shifting around."*

Input = section 3a's compiled output plus the current prose fields for the affected resources.
Output = (i) an exec summary of the day, (ii) per-resource proposed prose evolution.

**BINDING CONSTRAINT from `RESOLVER_DEFROST_DESIGN.md` section 1 (CVO 215615Z item a):**
proposals may target **PROSE fields ONLY** -- `description`, `enrichment`, `classification(+reason)`.
They may **NEVER** be made against the DETERMINISTIC fields (`producers`, `served_artifacts` keys,
`family`, `current_coverage`, `frontend_resolution`) -- those are compiled, and a hand-proposal
against a compiled field is a frozen-map dependency being reintroduced by the very pipeline built to
kill it. **The prompt states this prohibition explicitly, and the assembler drops any proposal whose
target field is not on the prose allowlist** -- prompt discipline is not a control; the allowlist is.

Proposal output shape matches `RESOLVER_DEFROST_DESIGN.md` section 4 (CVO input b), so CVO's queue
lands it without translation: per-field `text` / `last_reviewed` / `reviewer` / `stability`.
*(The doc's three-tier stability windows are SUPERSEDED prose per CVO -- Andrew simplified toward one
window + migration override. The SPLIT and the SCHEMA stand; I encode the schema, not the windows.)*

### 3c. Day-over-day DELTA -- a SET-diff, never a count

Per CVO input 4. Read yesterday's `daily/.../*.json` resource set; emit:

- `newly_active`: in today's set, not yesterday's
- `gone_quiet`: in yesterday's set, not today's
- `sustained`: in both

**Counts are banned as the delta.** "14 resources changed, up from 11" is compatible with a
completely disjoint set of resources -- it reports movement while hiding substitution, and
substitution is exactly the signal this pipeline exists to catch. The counts may appear as
*supporting* text beside the sets, never as the delta itself.

**First run has no predecessor.** It emits `delta: null` with `reason: "no prior report"` --
explicitly, never an empty set. An absent predecessor and a predecessor with zero changes must not
render identically.

> **C2 (CVO approval condition, 221931Z) -- PREDECESSOR RESOLUTION AFTER A MISSED DAY.**
> "Yesterday's json" does not exist after a missed day, and a naive read would then produce
> `delta: null` on a day that HAS a perfectly good predecessor two days back -- reporting "no prior
> report" when one exists. **Predecessor = the MOST RECENT prior `daily/.../*.json`**, found by
> descending-key search, not by constructing yesterday's key. **The gap is NAMED in the report:**
> `delta vs 2026-07-28; 2026-07-29 has no report`. `delta: null` is emitted **only** when no
> predecessor exists at all.
> Same absent-vs-zero honesty as the first-run case: a two-day delta silently labelled as a one-day
> delta is a wrong number wearing a right number's clothes.

---

## 4. FAIL-SOFT SPLIT (CVO input 1) -- the requirement that shapes the code

The deterministic half compiles **independently** of the Kimi call. Kimi failure (timeout, non-200,
empty reply, malformed) still lands the report, with the AI section replaced by a **LOUD** marker:

```
## AI EXEC SUMMARY -- ABSENT
STATUS: AI_SECTION_ABSENT
REASON: <KIMI_TIMEOUT|KIMI_HTTP_<code>|KIMI_EMPTY|KIMI_MALFORMED>
The deterministic resource list and delta below ARE COMPLETE and unaffected.
No semantic proposals were generated for this day. This day is NOT reviewed for prose evolution.
```

and `manifest.ai_section: "ABSENT"`.

**There is no silent no-report day.** The three failure states are distinguishable, which is the
point: a day with no report at all, a day with a report whose AI half failed, and a day with a
complete report that found nothing to propose are three different facts and must never render alike.

**Reused from the estate's own Kimi harness** (`bd_49f_auto_login.js:86-121`, the KIMI-HEALTH GUARD):
a 30s socket timeout because *a hung socket is not a throw and not a rejection* -- without an
explicit timeout the call stalls rather than fails, and a stall is the failure mode that produces a
silent no-report day. One retry, then fall through to the ABSENT marker.

---

## 5. Repo / commit-stream source + auth (CVO input 2)

**Source:** `origin` = `https://github.com/Opal-Capital/ajb_workspace.git` (measured via `git remote -v`).

**Chosen: shallow fetch from origin, not the GitHub API.**

| | shallow git fetch | GitHub REST listing |
|---|---|---|
| paths per commit | native (`--name-only`) | extra call per commit; paginated |
| rate limits | none | yes, and they bite on a busy day |
| fidelity | the actual object graph | a JSON projection of it |
| merge-commit handling | native | must be reconstructed |

`git clone --filter=blob:none --no-checkout` then `git log --since/--until --name-only`. Blobs are
never needed -- only commit metadata and changed paths -- so the fetch stays small even as history
grows.

**Auth:** a fine-grained GitHub PAT, **read-only, contents:read, this repo only**, stored in
Secrets Manager as `estate-report/github-token`. The runner reads the secret at run time and never
persists it to disk.

Following the **secret-ID POINTER convention** (Andrew-direct via CVO 195133Z, as implemented in
`bd-49f-auto-login/instance.tf:97-104`): `user_data` writes an env file carrying secret **NAMES**,
never secret **VALUES**. Nothing sensitive is ever in `user_data`, which is readable via
`DescribeInstanceAttribute` and lands in the Terraform state.

> **OPEN -- needs a human.** PAT creation is a GitHub-console act on an Opal-owned org and is not an
> agent action. Flagged in section 11.

---

## 6. Window + time-vintage (CVO input 3)

Window = **09:00 America/New_York (previous day) -> 09:00 America/New_York (run day)**.

> **C1 (CVO approval condition, 221931Z) -- BOUNDARIES ARE THE SCHEDULED MARKS, NOT PROCESS WALL-TIME.**
> This section originally said the window "closes at the moment the run fires." That is wrong and the
> error is subtle: orchestrator fire, EC2 boot, and job start differ by **minutes of jitter**, so
> wall-time boundaries make consecutive windows **overlap or gap** -- a commit landing in the gap is
> either double-counted or vanishes, silently, and the report would still look perfectly well-formed.
> **Both boundaries are computed as the exact scheduled `09:00:00` America/New_York instants** (today's
> mark and the prior day's mark), derived from the schedule, never from `now()`. The job's own start
> time is recorded separately as `written_at` and is NEVER a window boundary.
> **Exercised by A3:** a commit landed inside the jitter interval must appear in **exactly one** day.

**Named IN the report**, in the header, with the resolved UTC offset printed so the reader never has
to infer DST:

```
WINDOW: 2026-07-29 09:00 America/New_York (13:00Z) -> 2026-07-30 09:00 America/New_York (13:00Z)
```

Both the local and UTC forms are **computed**, never hand-typed. A hand-typed `Z` is worse than an
ambiguous timestamp: ambiguity prompts a check, a forged marker cancels it.

`git log --since/--until` **reads LOCAL time on the host**, which is a measured estate footgun (an
evening query returned 0 for 55 real commits). The job passes explicit ISO-8601 timestamps
**with offsets** and sets `TZ=UTC` for the git invocation, and the acceptance test includes a
positive control -- a window known to contain commits must return a non-zero count.

---

## 7. Miss-detection: the manifest ledger, and why there is no alarm

**No SNS topic. No CloudWatch alarm. No SES. No `*-monitor` / `*-freshness-checker` function.**
The reference module I am cloning declares all of the first three; omitting them is a DECISION with a
reason (`ANDREW_DIRECT_RULINGS.md`), pre-endorsed by CVO 221315Z item 3 -- **not a gap to be fixed by
restoring parity with the source module.**

Miss-detection is the **per-day manifest ledger**:

```json
{ "date": "2026-07-30",
  "status": "PENDING",
  "ai_section": "PRESENT" | "ABSENT",
  "window_start_utc": "...", "window_end_utc": "...",
  "commits_in_window": 41, "resources_changed": 14,
  "report_keys": ["daily/2026/07/30/estate-report-2026-07-30.md", "...json"],
  "written_at": "2026-07-30T13:02:11Z", "written_by": "estate-report-runner" }
```

Born `PENDING`. CVO's `/estate-pull` flips it. **Any un-flipped day older than today is loud at
every CVO load** (the LD-0319 first-on-load shape).

**Why this is stronger than an alarm, and worth stating so it is not "upgraded" later:** an alarm
must NOTICE an absence -- it needs a publisher, a threshold, and a subscriber, and it fails silently
when any of the three is misconfigured. The ledger inverts it: the default state IS the alarming
state, and only an affirmative human-in-the-loop act clears it. **A missing day is not something
that must be detected; it is the absence of a flip that was already required.** A gate whose default
state is the alarming one cannot fail open.

`# andrew-asked: "that report is surfaced to a queue that is updated every day at 9a Eastern" (Andrew-direct 2026-07-30 ~2135Z)`

---

## 8. Resources + IAM (least-privilege, resource-scoped)

**Terraform module:** `infra/aws/terraform/estate-report/` -- new, own state key
`estate-report/tfstate`. NOT folded into shared-infra (independent lifecycle, independent blast
radius).

| Resource | Notes |
|---|---|
| `aws_s3_bucket.estate_report` | `opal-estate-report`, versioning ENABLED, AES256, public access blocked (all four) |
| `aws_instance.estate_report_runner` | AL2023 via SSM param, t3.medium, STOPPED between runs, `lifecycle { ignore_changes = [ami, associate_public_ip_address] }` (the estate's standard transient-instance drift guard) |
| `aws_lambda_function.estate_report_orchestrator` | python3.12, **timeout 60**, 128MB. Deliberately small -- it starts an instance and returns |
| `aws_scheduler_schedule.estate_report_0900et` | `cron(0 9 * * ? *)`, `schedule_expression_timezone = "America/New_York"`, `flexible_time_window { mode = "OFF" }`, **created `DISABLED`** |
| `aws_iam_role` x3 | scheduler / orchestrator / runner instance-profile |
| `aws_secretsmanager_secret.github_token` | `estate-report/github-token` (value set out-of-band) |

**Orchestrator role:** `ec2:StartInstances` **pinned to this instance ARN only**; `ec2:DescribeInstances`
(`*` -- AWS offers no resource-level scoping, read-only); CW Logs. **No `sns:Publish`. No S3.**

**Runner instance-profile:**
- `s3:PutObject` on `arn:aws:s3:::opal-estate-report/daily/*` **and** `.../manifest/*` -- **NOT** `adjudicated/*`
- `s3:GetObject` on `daily/*` (yesterday's JSON, for the delta)
- `s3:ListBucket` on the bucket, `Condition` prefix-scoped to `daily/*` + `manifest/*`
- `secretsmanager:GetSecretValue` on `estate-report/github-token-*` and `astn/kimi/api-key-*`
- `ec2:StopInstances` **pinned to its own instance ARN** (self-stop)
- SSM core (managed instance) + CW Logs

**Kimi egress:** Andrew-direct per-use designation, **THIS pipeline only** -- not a blanket lift.
Security group: egress to `api.moonshot.ai` + GitHub + AWS APIs; **no inbound** (SSM only).

**IAM VERIFICATION IS NOT `comp-iam` HERE.** `opal-estate-report` is a NEW bucket and `comp-iam`
models `(action)`, never `(action, resource)` -- a role holding `s3:PutObject` on any bucket reports
GRANTED for every other. Rule 22a applies in full:

```
aws iam simulate-principal-policy --policy-source-arn <runner-role> \
  --action-names s3:PutObject --resource-arns arn:aws:s3:::opal-estate-report/daily/2026/07/30/x.md
```

**ONE `--resource-arns` per call** (2+ flips held ARNs to `implicitDeny`); **the positive control runs
as a SEPARATE invocation** (a control batched with the target is corrupted by its own presence); and
the **NEGATIVE** control is the one that matters most here -- `adjudicated/*` **MUST** return deny.
The boundary in section 2 is only real if it is exercised as a deny.

---

## 9. Deploy sequence (Rules 1, 2, 6, 14a, 18)

1. Author module + orchestrator + runner job; `.tools/commit-gate.sh` on every `.py`.
2. `.tools/safe-commit.sh` (commit BEFORE apply, Rule 2). Commit message via `-F` (Rule F-010).
3. `terraform plan` -- read the diff.
4. RAVC1 to CVO with the plan diff.
5. **`.tools/safe-apply.sh`** -- never bare apply (Rule 18).
6. `terraform plan` again -> 0-diff.
7. Update `infra/aws/lambda/ci/lambda-source-map.json` (Rule 4) + `EC2_MANIFEST.json` (Rule 8).
8. Update my `pipeline_inventory.xml` core document.
9. Tag `estate-report-v0.1.0`, `git push --follow-tags` (Rule 6).
10. **Schedule stays DISABLED** until an end-to-end exercised run passes acceptance. Enabling is
    go-live and is a separate explicit act (the astn precedent).

---

## 10. Acceptance criteria (machine-checkable, exercised -- not inspected)

| # | Criterion | How it is EXERCISED |
|---|---|---|
| A1 | Report lands on schedule | Manual orchestrator invoke -> object exists at `daily/YYYY/MM/DD/` with today's date |
| A2 | **Fail-soft holds** | Point `KIMI_URL` at an unroutable host -> report STILL lands, `AI_SECTION_ABSENT` present, deterministic list COMPLETE, `manifest.ai_section=="ABSENT"` |
| A3 | Deterministic half is real | Seed a known commit in the window -> its changed paths appear, mapped to their chain. **Positive control:** a window known to contain commits returns non-zero |
| A4 | Delta is a SET | Two consecutive runs with a deliberately disjoint change set -> `newly_active`/`gone_quiet` non-empty and CORRECT; counts alone must not be able to satisfy this test |
| A5 | **Boundary is enforced** | `simulate-principal-policy` on `adjudicated/*` returns **DENY** (separate invocation), while `daily/*` returns ALLOW |
| A6 | Self-stop always | Kill the job mid-run -> instance still reaches `stopped` (trap path), and the boot `shutdown -h +90` is present in `systemctl list-timers` |
| A7 | Prose-only proposals | Feed a fixture proposing against `producers` -> assembler DROPS it and says so |
| A8 | Manifest born PENDING | Fresh run -> `manifest/YYYY-MM-DD.json` `status=="PENDING"` |
| A9 | Timezone is wall-clock | `aws scheduler get-schedule` shows `America/New_York`; and the schedule's next-fire is 09:00 ET across a DST boundary |
| A10 | No banned resource | `terraform plan` output contains ZERO `aws_sns_topic`, `aws_cloudwatch_metric_alarm`, `ses:` -- **run with a positive control on the same file**, because four zeros from a broken grep look exactly like four zeros from a clean module |
| A11 | **Unset PAT refuses BY NAME** (CVO C3 addendum) | Run with the secret empty -> `SecretUnset` naming the secret, **no report object written**. The failure to catch is not a crash but a well-formed report with an empty deterministic half, which is indistinguishable from a genuinely quiet estate day |
| A12 | **Self-stop is ARN-pinned** (CVO C3) | `aws iam get-role-policy --role-name estate-report-runner-role --policy-name estate-report-runner-selfstop` shows the instance ARN, not `instance/*` with a tag condition |

---

## 11. OPEN ITEMS -- decisions I am NOT making unilaterally

1. **GitHub PAT (HUMAN).** Creation is a console act on an Opal-owned org; not an agent action.
   Requested: fine-grained, read-only, `contents:read`, `ajb_workspace` only. I will wire the secret
   ID and leave the value unset until Andrew or an operator lands it.
2. **The exact K3 model string (FLAGGED, NOT GUESSED).** Andrew said "K3". The estate's existing
   harness defaults to `kimi-k2.6` (`bd_49f_auto_login.js:65`). I have **not** called the vendor to
   enumerate model IDs -- egress is authorized for this pipeline but a spec is not a reason to spend
   it. `kimi_model` is a TF variable; the exact string is confirmed at build time in one call.
3. **Repo accrual is CVO's** (CVO 221315Z item 2) -- resolves the ruling-2 "accruing in the repo" vs
   "compiled in some bucket" ambiguity. My pipeline writes `daily/` + `manifest/` ONLY. Recorded here
   because the verbatim reads both ways and a future reader will hit the same question.
4. **Instance sizing.** t3.medium mirrors astn. The graph traversal + co-change analysis is unmeasured;
   if the first real runs are slow, sizing is revisited with a MEASURED number, not a guess.
5. **Retention/lifecycle on `opal-estate-report`.** None proposed -- this is a governance record and
   Andrew has not ruled on retention. Versioning is on. **Deliberately not deciding**: a lifecycle
   rule that expires a governance record is exactly the kind of quiet default nobody notices until
   the record they need is gone.

---

## 12. What I did NOT do

- Did not create any AWS resource, run any Terraform, or call the Kimi API.
- Did not write to `adjudicated/*` in any form, including in the IAM policy.
- Did not clone the reference module's SNS topic, CloudWatch alarm, or `sns:Publish` grant.
- Did not guess the K3 model string.
- Did not run `comp-iam` and call it IAM verification -- see section 8.

-- `0.7.0_AE_CloudOps~B`
