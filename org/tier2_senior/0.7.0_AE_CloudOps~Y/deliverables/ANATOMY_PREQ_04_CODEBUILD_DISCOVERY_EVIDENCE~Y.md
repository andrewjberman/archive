# ANATOMY.TO-PREQ-04-CODEBUILD-DISCOVERY~Y — immutable evidence packet

**Task order:** `ANATOMY.TO-PREQ-04-CODEBUILD-DISCOVERY~Y`
(`org/tier2_senior/0.7.0_AE_CloudOps~Y/task_orders/ANATOMY.TO-PREQ-04-CODEBUILD-DISCOVERY~Y.md`,
5117 bytes, SHA256 `b47b75c524c6b048a57ec64dd37a067f3b5e78fb3d8d9f60b18deece9d1f941f`
— matches `4.0.0_SA_CRO~Y`'s independent measurement)
**Controlling carrier:** `C:/Users/AndrewBerman/Downloads/docs_abcdeg/fabric/PHASE_3_P3_TO_05_PREQ_04_CLOUDOPS_READ_ONLY_DISCOVERY_TASK_ORDER_20260905.md`,
3677 bytes, SHA256 `0f1321f3ba21f962ae36b320cc960811dce1328f183a9b9cf352aa23d7011fdc` — **MATCHES claimed**
**Issuing commit:** `1d1b5b327a` (author `1.0.0_SA_CTO`, "governance: issue CloudOps PREQ-04 discovery", 1 file / 62 insertions)
**Executed by:** `0.7.0_AE_CloudOps~Y`, registered PID 41524
**Window:** 2026-09-05T20:22:37Z — 2026-09-05T20:28:41Z
**Disposition:** COMPLETE. No refusal, no denial, no ambiguity, no partial.

---

## Compliance summary

| Criterion | Verdict | Basis |
|---|---|---|
| C1 ACK before first AWS call | PASS | ACK sent 20260905T~2019Z (ids 94438/94439); first AWS call 20:22:37Z. Both seats validated the ACK. |
| C2 only the three permitted actions | PASS | Exactly 3 distinct AWS API actions invoked, 3 calls total. Enumerated below. |
| C3 caller + region complete or ABSENT | PASS | Both resolved with named evidence source. Neither is ABSENT. |
| C4 all projects inventoried, pagination handled, denominators stated | PASS | 4 of 4 live projects, single page confirmed by absent `nextToken`, client-side count. |
| C5 four local TF declarations authenticated, no mutation | PASS | Bytes + worktree SHA256 + git blob @HEAD for each. Read-only. |
| C6 commands, timestamps, exit codes, errors, non-claims | PASS | This document. |
| C7 no prohibited effect | PASS | See "Prohibited effects" below. |
| C8 handback names path/bytes/SHA256/disposition | PASS | Handback message to CTO and CRO. |

---

## Every AWS action taken (C2) — complete denominator: 3 calls, 3 distinct actions

| # | Action | Exact command | UTC start | UTC end | Exit |
|---|---|---|---|---|---|
| 1 | `sts:GetCallerIdentity` | `.tools/aws sts get-caller-identity --output json` | 2026-09-05T20:22:37Z | 2026-09-05T20:22:41Z | 0 |
| 2 | `codebuild:ListProjects` | `.tools/aws codebuild list-projects --output json` | 2026-09-05T20:24:21Z | 2026-09-05T20:24:23Z | 0 |
| 3 | `codebuild:BatchGetProjects` | `.tools/aws codebuild batch-get-projects --names opal-stitch-produce opal-drift-producer globgrph-derive-build semantic-clustering-lambda-build --output json` | 2026-09-05T20:26:04Z | 2026-09-05T20:26:08Z | 0 |

**stderr on all three: empty.** No other AWS API action was invoked at any point in this session.

---

## Step 1 — caller identity (`sts:GetCallerIdentity`)

```json
{
    "UserId": "AIDAUR7FNW6PEXHN2JIOH",
    "Account": "313476888478",
    "Arn": "arn:aws:iam::313476888478:user/Andrew_Berman"
}
```

| Field | Value | Note |
|---|---|---|
| Account | `313476888478` | |
| ARN | `arn:aws:iam::313476888478:user/Andrew_Berman` | |
| User ID | `AIDAUR7FNW6PEXHN2JIOH` | Not credential material; an IAM unique-id. |
| Partition | `aws` | Read from ARN field 2. **Derived from the ARN, not separately returned by the API.** |

**No credential material was read or printed.** No access key, secret, session token or key material
appears in this packet or in any file it references.

⚠ **FINDING WORTH THE CTO's AND CRO's ATTENTION — the caller is a HUMAN IAM USER, not a role.**
The operating principal for this discovery is `user/Andrew_Berman`, a long-lived IAM user, not an
assumed role and not a service principal. This is reported, not acted on. It bears directly on
intake group C (service-role ARN, session principal/session-name law, credential delivery
mechanism, and the requirement that test processes and descendants cannot read credentials): a
long-lived human user is the credential shape that section exists to eliminate. Naming it is
within this order; changing anything about it is not, and I did not.

## Step 2 — effective region

| Evidence source | Result |
|---|---|
| A. `AWS_REGION` environment variable | **UNSET** |
| B. `AWS_DEFAULT_REGION` environment variable | **UNSET** |
| C. `aws configure get region` (exit 0, stderr empty) | **`us-east-1`** |
| D. Config file presence | `~/.aws/config` exists, 33 bytes, mode `-rwx------+` |

**Effective region: `us-east-1`.** Evidence source: the CLI-resolved configured default (C),
backed by the config file (D). Not ABSENT; no region was chosen by me. Corroborated independently
by a repo artifact predating this order: `arn:aws:logs:us-east-1:313476888478:log-group:/aws/codebuild/*`
in `docs/briefs/cmpaws-iam-axis-census-20260603.json:1613`.

## Step 3 — live CodeBuild inventory

**Pagination handled (C4):** `list-projects` returned **no `nextToken`** → single page, list is
complete. Count taken **client-side** from the array, not from `--query length()` (which would
have returned the page count).
**DENOMINATOR: 4 live projects.**
`batch-get-projects` requested 4, returned 4, **`projectsNotFound: []`** — the empty array is
stated explicitly because an unknown name returns there rather than erroring.

| field | opal-stitch-produce | opal-drift-producer | globgrph-derive-build | semantic-clustering-lambda-build |
|---|---|---|---|---|
| ARN | `arn:aws:codebuild:us-east-1:313476888478:project/opal-stitch-produce` | `…:project/opal-drift-producer` | `…:project/globgrph-derive-build` | `…:project/semantic-clustering-lambda-build` |
| **environment.type** | **LINUX_CONTAINER** | **LINUX_CONTAINER** | **LINUX_CONTAINER** | **LINUX_CONTAINER** |
| environment.image | `aws/codebuild/amazonlinux2-x86_64-standard:5.0` | `aws/codebuild/amazonlinux2-x86_64-standard:5.0` | `aws/codebuild/standard:7.0` | `aws/codebuild/standard:7.0` |
| computeType | BUILD_GENERAL1_SMALL | BUILD_GENERAL1_SMALL | BUILD_GENERAL1_MEDIUM | BUILD_GENERAL1_MEDIUM |
| privilegedMode | false | false | true | true |
| serviceRole | `…:role/opal-stitch-produce-codebuild-role` | `…:role/opal-drift-producer-codebuild-role` | `…:role/globgrph-derive-build-role` | `…:role/codebuild-semantic-clustering-role` |
| source.type / location | S3 `opal-313476888478-globgrph/stitch-source/source.zip` | S3 `opal-313476888478-lambda-artifacts/drift-producer/source.zip` | S3 `opal-313476888478-globgrph/build-source/derive-runner-source.zip` | S3 `opal-data-news-v2/codebuild/semantic-clustering-source.zip` |
| artifacts.type | NO_ARTIFACTS | NO_ARTIFACTS | NO_ARTIFACTS | NO_ARTIFACTS |
| **vpcConfig** | **ABSENT (no VPC)** | **ABSENT (no VPC)** | **ABSENT (no VPC)** | **ABSENT (no VPC)** |
| logs | ENABLED `/aws/codebuild/opal-stitch-produce` | ENABLED `/aws/codebuild/opal-drift-producer` | ENABLED `/aws/codebuild/globgrph-derive-build` | ENABLED `/aws/codebuild/semantic-clustering-lambda-build` |
| timeoutInMinutes | 30 | 60 | 60 | 30 |
| queuedTimeoutInMinutes | 480 | 480 | 480 | 480 |
| concurrentBuildLimit | `null` (unset) | `null` (unset) | `null` (unset) | `null` (unset) |
| webhook | ABSENT (none) | ABSENT (none) | ABSENT (none) | ABSENT (none) |

**Windows environments among live projects: 0 of 4.**
**Projects with a VPC configuration: 0 of 4** — every live project runs outside a VPC. Bears on
intake group E (four disjoint traffic classes, routes, NAT path): there is no existing VPC-attached
CodeBuild precedent in this account to inherit from.
**Projects with a concurrency limit set: 0 of 4** — `concurrentBuildLimit` is unset on all four.
Bears on intake group B's "project concurrency, exactly one" requirement: no existing project
demonstrates that control here.

## Step 4 — local Terraform declarations, authenticated

| path | bytes | SHA256 (worktree bytes) | git blob @HEAD | LINUX_CONTAINER | WINDOWS |
|---|---|---|---|---|---|
| `infra/aws/terraform/globgrph/derive-build.tf` | 3540 | `9aa90c68e3dc66256c9799fa795eb899333b3ce549f25ceebbbc65a6d6811df7` | `dd4cf454fef12d9f047c2a64d387684351c38a1c` | 1 | 0 |
| `infra/aws/terraform/globgrph/stitch-produce.tf` | 10421 | `27924630333a0ba33090059836fec388c9659f0e4dcfbad3baaa2ee561b4c343` | `66ac869a957a9fee9f5ce669f10ab57262c45c7d` | 1 | 0 |
| `infra/aws/terraform/shared-infra/drift-producer.tf` | 11323 | `14e652354f09e70fbdac410a836b5bd28fc142229d9f6b12ac5945e490842a35` | `df4a79d0417802a8bbb15410f619b443662ba255` | 1 | 0 |
| `infra/aws/terraform/c3materialize-b4/main.tf` | 11855 | `ca20761395f428134cd93d872cbeb154f8c723b056ecb78f7dfcba5d16d48743` | `95d57a3c90204435bb6201410b5c35a030a33719` | 1 | 0 |

⚠ **GRAIN QUALIFIER ON THESE DIGESTS.** The SHA256 column hashes the **worktree checkout** on an
`autocrlf` box, which is not necessarily the committed record. The `git blob @HEAD` column is
supplied alongside precisely so the record-plane identity is available and the two planes are not
conflated. Use the blob id for any claim about the committed bytes.

**Windows environment declarations across all four files: 0.**

### Declared-vs-live correlation (step 4's "relationship or non-relationship")

| project | declared at | live? | class |
|---|---|---|---|
| `globgrph-derive-build` | `derive-build.tf:66` | YES | **MATCHED** |
| `opal-stitch-produce` | `stitch-produce.tf:130` | YES | **MATCHED** |
| `opal-drift-producer` | `drift-producer.tf:173` | YES | **MATCHED** |
| `opal-c3materialize-b4-sbm` | `c3materialize-b4/main.tf:211` (`local.name` @ `:77`) | **NO** | **DECLARED-no-LIVE** |
| `semantic-clustering-lambda-build` | — none found — | YES | **LIVE-no-DECLARED** |

**Denominators: 4 declared, 4 live, union 5, intersection 3.**

- `opal-c3materialize-b4-sbm` being absent from AWS is **consistent with its own declaration**,
  which describes it as "One-shot; torn down after the measurement is read." Reported as an
  observation, **not** asserted as drift — I did not measure whether it ever existed.
- `semantic-clustering-lambda-build` is live with **no Terraform declaration found** in this repo.
  A pre-existing repo artifact corroborates it independently: `codebuild-semantic-clustering-role`
  appears in `docs/briefs/cmpaws-iam-axis-census-20260603.json`. Reported; no action taken.

---

## Prohibited effects (C7) — none occurred

No create, update, start, stop, retry, delete, import, export, tag, or any other AWS mutation. No
IAM change and no role assumption. No credential or secret value read or printed. No arbitrary
endpoint contact. No final-project selection. No product/source copy. **No CodeBuild run.** No
mutation of `scratchpad_tmp`, `docs_abcdeg`, deployment state, or any customer estate. No push.
The three calls in the table above are the complete set of AWS interactions.

Files written by this order, both inside the CloudOps deliverables directory and both new:
this packet and its proof JSON. No pre-existing file was modified.

---

## Explicit non-claims (C6)

1. **No permission sufficiency is claimed.** `sts:GetCallerIdentity` answers *who I am*, never *who
   is permitted*. Nothing here establishes that this or any principal may provision, invoke, or tear
   down anything.
2. **No statement that a Windows CodeBuild environment is unavailable in AWS.** The measured claim is
   narrower and exact: **zero of four projects live in account 313476888478 are Windows, and zero of
   four local declarations declare Windows.** Whether `WINDOWS_SERVER_*_CONTAINER` is offered in
   `us-east-1`, at what compute types, and whether it can satisfy the group-D capability list is
   **UNMEASURED** — those questions were not in scope and no API in the permitted set answers them.
3. **No final project selection**, no recommendation of a project for PREQ-04 reuse, and no claim
   that any existing project is suitable.
4. **`concurrentBuildLimit: null`** is reported as returned. I did not test whether account- or
   project-level concurrency behaves as "exactly one"; that requires an action outside this ceiling.
5. **No claim about `opal-c3materialize-b4-sbm`'s history.** Absent from the live list is all that
   was measured; whether it was created and torn down, or never created, is unmeasured.
6. **No claim that the LIVE-no-DECLARED project is unmanaged.** It may be declared in another repo,
   fabric, or state file not searched under this order.
7. **The four SHA256 values hash the worktree, not the record** — see the GRAIN qualifier above.
8. **Vintage.** Every AWS value is as-of the 20:22:37Z–20:26:08Z window and perishable; the live
   plane may have changed since.
