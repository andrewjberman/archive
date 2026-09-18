# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtc-6: the 49 Financial source principal

**For:** the two sign-off halves required before IB-rtc-7 applies (CLAUDE.md: never-widen sign-off is
CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`. **Prepared by:** `0.4.0_DS_ClientPlatform~X`
(IRPT_BCKEND.TO-IB-rtc-6). **Ruling:** R-44 @57bc083d45. **Nothing here is applied.** Plans only.

A half signs the **blast radius** of the act below: what each key may touch, and the rollback for each
key. It does not sign an intention. The halves themselves are written by the two seats, not by this seat.
A half that names fewer keys than this packet is IB-rtc-7's stop condition.

---

## The act, in one paragraph

A new IAM role, **`irpt-49f-directory-read-role`**, whose name is builder output, may be assumed ONLY by
`mdpf-daily-runner-ec2-role`. It may read the FIVE 49 Financial dimension tables in the firm's own bucket
and list exactly those five prefixes, and nothing else. The host role gains ONE statement, `sts:AssumeRole`
on that role. The refresh Lambda gains ONE env key that hands the role's ARN to the 49 Financial build
only. The runner's 49 Financial source set reads its five tables through the assumed session. Inflection
and Cottonwood are unchanged. **No write is granted anywhere.**

---

## The keys (a half names every one)

| key | root / file | resource | change | plan line |
|---|---|---|---|---|
| **K1** | `investor-reporting/directory/principal_49f.tf` | `aws_iam_role.irpt_49f_directory_read` -> `irpt-49f-directory-read-role` | **create** | `+ create` |
| **K2** | same | `aws_iam_role_policy.irpt_49f_directory_read` -> `irpt-49f-directory-read-policy` | **create** | `+ create` |
| **K3** | `mdpf-pipeline/iam.tf` | `aws_iam_role_policy.mdpf_runner` (`mdpf-runner-scoped` on `mdpf-daily-runner-ec2-role`) | **+1 statement** (32 -> 33) | `~ update in-place` |
| **K4** | `investor-reporting/directory/schedule.tf` | `module.irpt_directory_refresh.aws_lambda_function.this` (`irpt-directory-refresh`) | **+1 env key** (4 unchanged) | `~ update in-place` |
| **K5** | code | `refresh.py` (hand-off, via the Lambda artifact) and `directory_runner.py` (Firm49F, via the `investor_reporting` bundle) | behaviour, no IAM | not a Terraform resource |

### K1 -- the role and its trust

```
Trust (assume_role_policy), 1 statement, 1 principal:
  Sid AssumedOnlyByTheDailyRunnerHost  Allow  sts:AssumeRole
  Principal AWS = arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role
```

- **Name:** `name("irpt", "49financial", "directory-read", "role")` = `irpt-49f-directory-read-role`
  (`lib/opal_naming.py`; Terraform: `module.opal_name` with the same four arguments). Not typed anywhere.
- **Name-prefix checks:**
  - Against the four prefixes the face lists as the old Deny (`role/cot-*`, `role/inf-*`, `role/mdpf-*`,
    `role/opal-assets-mdpf-*`): matches **0 of 4**.
  - Against the LIVE fence on `opal-data-49financial` (`DenyForeignFirmPrincipals`, `ArnNotLike
    [role/*-49f-*, 16 exemptions]`, LGIC_ENFORCE EN-f-1): **matches the admit pattern `role/*-49f-*`**.
  - The second check is what makes the grant work: the fence admits this role and still denies the host
    role, which carries no scope slot (row `IRPT_BCKEND-S66`).
- **Host role ARN:** derived from `infra/aws/ec2/EC2_MANIFEST.json` (`services["mdpf-daily-runner"].iam_role`),
  the same way `schedule.tf` derives the instance id.
- **Before:** the role does not exist (`iam get-role` -> `NoSuchEntity`, 2026-09-18 ~05:4xZ).
- **Blast radius:** **every process that runs as `mdpf-daily-runner-ec2-role`** (the whole mdpf daily chain on
  `i-02448edb624a7a7cf`, the accrual bridge's SSM runs, the IRPT dispatch's builds) becomes ABLE to assume
  this role. Only the host role can; no other principal, user or service can. This is the honest radius
  of K1 + K3: the trust is as narrow as a principal ARN allows, but that principal is a shared host role.
- **Rollback:** remove K1 and K2 from `principal_49f.tf` (revert the declaring commit), then
  `.tools/safe-apply.sh -chdir=infra/aws/terraform/investor-reporting/directory apply`. That plans
  **2 to destroy** (the role and its inline policy) and nothing else. There is no state before K1, so
  destroying it restores the prior state exactly.

### K2 -- what the role may do

```
Sid ReadTheFiveDimensionTablesOnly   Allow s3:GetObject
  arn:aws:s3:::opal-data-49financial/gold/advi/dimensions/dim_account/*
  arn:aws:s3:::opal-data-49financial/gold/advi/dimensions/dim_relationship/*
  arn:aws:s3:::opal-data-49financial/gold/advi/dimensions/dim_identity_crosswalk/*
  arn:aws:s3:::opal-data-49financial/gold/advi/dimensions/dim_portfolio_group/*
  arn:aws:s3:::opal-data-49financial/gold/advi/dimensions/bridge_group_account/*
Sid ListExactlyThoseFivePrefixes     Allow s3:ListBucket  on arn:aws:s3:::opal-data-49financial
  Condition StringLike s3:prefix = [the same five, each "<prefix>/*"]
```

- **5** GetObject prefixes; **1** ListBucket, prefix-conditioned to those **5** (never bucket-wide, so the
  negative control below can DISCRIMINATE); **0** statements on any other bucket; **0** write actions.
- **Addresses:** the bucket is `module.opal_name.scope_bucket[<the firm whose scope slot the name carries>]`,
  and the root is read from the producer's own `runner_common.OUT_ROOT` (`gold/advi`), the constant
  `directory_runner` reads. Nothing is typed (row `IRPT_BCKEND-S67`).
- **KMS:** none needed. The bucket is SSE-S3 (`AES256`, `get-bucket-encryption`).
- **Blast radius:** whoever assumes K1 can list and read those five tables. The host role itself still
  cannot: the fence denies it, and it is given no S3 grant on this bucket (the `:592-621` note in
  `mdpf-pipeline/iam.tf` stays true).
- **Rollback:** as K1. The inline policy is deleted with the role's destroy.

### K3 -- the one statement on the host role

```
+ Sid IrptDirectory49fAssumeSourcePrincipal  Allow  sts:AssumeRole
    Resource arn:aws:iam::313476888478:role/irpt-49f-directory-read-role
```

- **Before:** `mdpf-runner-scoped`, 32 statements, 6,686 minified characters, captured verbatim as
  `IB-rtc-6_host_policy_before.json` (sha256 `b1d8027fe940c6a13a340dd271387b65ca2c372cfa56905f768166811fdce939`).
- **After:** 33 statements, about 6,850 characters of the 10,240 aggregate inline limit.
- **Why declare it when same-account trust may already suffice:** IAM's same-account evaluation lets a
  resource policy (here, K1's trust) that names the principal's ARN grant on its own. K3 is declared
  because the face requires it, and because it puts the capability on the host role's own document, where
  anyone reading that role's permissions will find it.
- **Blast radius:** no new data access by itself. It names K1, and the grant K1 + K2 already describe is
  the whole of it.
- **Rollback:** revert the statement, then apply the targeted command below. The policy returns to the
  `before` document byte for byte (the other 32 statements are unchanged in the plan).

### K4 -- the Lambda's environment

```
+ IRPT_DIRECTORY_SOURCE_ROLE_MAP = jsonencode({"49financial" = "arn:aws:iam::313476888478:role/irpt-49f-directory-read-role"})
  (4 unchanged: IRPT_DIRECTORY_BUCKET_MAP, IRPT_DIRECTORY_BUNDLE_URI, IRPT_DIRECTORY_PREFIX, IRPT_DIRECTORY_RUNNER_INSTANCE_ID)
```

- The ARN is BUILT at plan time (account + builder name) rather than read back from K1. Read back, the
  plan would print the whole environment as "known after apply" and hide this one key.
- **Blast radius:** `refresh.py` exports the ARN into the 49 Financial build's shell only (it keeps only a
  value shaped like a role ARN; anything else is dropped). The other two firms' builds are unchanged.
- **Rollback:** revert the `schedule.tf` line, then apply the directory root. The environment returns to its
  4 keys.

### K5 -- the code that uses it (no IAM, and neutral until K1-K4 exist)

- `refresh.py` `dispatch()`: prepends `export IRPT_SOURCE_READ_ROLE_ARN='<arn>'` for a firm listed in the
  map. It **reaches the Lambda only through a rebuilt artifact** (`investor-reporting/irpt-directory-refresh.zip`);
  IB-rtc-7's directory apply must carry a rebuild that includes this edit.
- `directory_runner.py` `Firm49F`: the five dimension reads go through a lazily assumed session
  (`sts:AssumeRole`, session `irpt-directory-source-read`), and the BD xref stays on the host session.
  It is a member of the `investor_reporting` bundle, so it reaches the host through a bundle mint
  (Rule 13, DS lane). **Without the env variable it behaves exactly as today**: host session, refused by
  the fence, with a WARN note.
- **Rollback:** revert the two edits; the next rebuild and mint restore the prior behaviour.

---

## The plans (NOT applied), with their identities (R-40)

| root | result | text artifact | sha256 (text) | sha256 (binary plan, kept local) |
|---|---|---|---|---|
| `investor-reporting/directory` | **2 to add, 1 to change, 0 to destroy** | `IB-rtc-6_plan_directory.txt` | `b844c72c198c8f23101ee30eb30f002ae0004116a84b5c06979f502f1e02943a` | `3e09c20388cfa435f2afc735920b3cea161733f4af0083d7e65d570d8a18b241` |
| `mdpf-pipeline` | **0 to add, 2 to change, 0 to destroy** | `IB-rtc-6_plan_mdpf-pipeline.txt` | `0d586c2e31be6375b05b46a404a81c4693467dcfcccb33d1fd1d23bebb598c74` | `e10a4c53415a6c71a8ca23730e61731f47bbd58220e427c38fe7d307a16697a5` |

Vendored `.tools/terraform.exe` v1.9.8, each root `init`ed fresh. The directory plan was re-run at 05:41:30Z,
after IB-rtc-3's Lambda deploy (05:23:55Z), and read identically. The planned documents are extracted to
`IB-rtc-6_plan_iam_extract.json`.

**The second change in `mdpf-pipeline` is NOT part of this act.** `aws_s3_object.mdpf_route_bindings` has a
deployed hash (`56a03a14...`) that matches neither the committed blob (`650f893a...`, LF) nor a Windows
checkout's CRLF rendering (`f94e8e4c...`). It is someone's unapplied change, and from this box it would
upload CRLF bytes (row `IRPT_BCKEND-S68`). **So IB-rtc-7 applies that root TARGETED** (below).

---

## How IB-rtc-7 applies it (the act this packet covers, and nothing more)

1. Both halves at HEAD naming **K1-K5**. Ledger entry OPEN with its sentinel committed first. Per CLAUDE.md
   NEVER-2's new clause, anyone auditing it reads every live worktree, not only CLOUD.
2. Re-plan both roots **immediately before** each apply. The directory plan must be exactly K1, K2 and K4
   (+ the rebuilt artifact for K5), with **0 to destroy**; anything else is a stop.
3. `.tools/safe-apply.sh -chdir=infra/aws/terraform/investor-reporting/directory apply` (the role first).
4. `.tools/safe-apply.sh -chdir=infra/aws/terraform/mdpf-pipeline apply -target=aws_iam_role_policy.mdpf_runner`
   (**targeted**: K3 only).
5. Mint the `investor_reporting` bundle through `.tools/safe-deploy.sh --mint-bundle investor_reporting` so the
   host runs the K5 runner (a DS-lane act).
6. Close the ledger before the grading reads; then run the negative control.

**Sequencing condition until then (row `IRPT_BCKEND-S65`, ARMED, owner `2.0.0_SA_COO~B`):** once this
branch merges, ANY apply of either root from a tree carrying it performs this act unsigned. The directory
root is the refresh Lambda's deploy root. Hold such applies, or make IB-rtc-7 the next one.

---

## The writer census of the 49 Financial directory prefix (R-44)

`writer_census_ib_rtc_6.py`, 2026-09-18 ~05:3xZ, subject `s3:PutObject` on
`arn:aws:s3:::opal-data-bd/investor-reporting/directory/2099-01-01/directory.json`. The destination is
**`opal-data-bd`**, the LEGACY 49 Financial bucket per `data/firm_registry.json`, until D14 moves it.

- **RESOURCE plane:** the bucket policy has 2 statements, both CloudFront `GetObject`; **0** allow a write;
  **0** Deny.
- **IDENTITY plane:** **262** principals simulated (255 roles, 7 users), 0 unsimulated.
  - 64 conditioned principals needed only context keys that cannot occur in a PutObject request (their
    decision stands).
  - 2 were re-simulated with the request's true context (this account, this region, the bucket's tags).
  - 4 were settled by reading their documents (0 Allow statements match the action and key).
  - **0 UNKNOWN.**
- **WRITERS: 12 of 262.** Eight roles (`bd-allocation-processor-role`, `bd-daily-trigger-lambda-role`,
  `bd-exporter-ec2-role`, `bd-gold-detail-generator-role`, `bd-gold-layer-lambda-role`,
  `bd-merge-daily-lambda-role`, `bd-pipeline-task-role`, `bd-processor-lambda-role`), plus
  `mdpf-daily-runner-ec2-role` (its existing destination write), plus users `Andrew_Berman`,
  `Andrew_Berman_Console` and `Opal_Terminal`.
- **The new principal is NOT a writer:** its planned policy simulates `implicitDeny` on the same key.
  IB-rtc-7 re-censuses after the apply and must read 12, unchanged.

---

## The negative control IB-rtc-7 runs (from the host, by the host, as the assumed role)

A read-only SSM command on `i-02448edb624a7a7cf`. It assumes K1 from the host session, then runs:

| # | attempt | expected | why it discriminates |
|---|---|---|---|
| P1 | list + get a `manifest.json` under `gold/advi/dimensions/dim_relationship/` | **allowed** | the positive control: without it every Deny below is uninformative |
| N1 | read `opal-data-inf/silver/api_dims/representatives/` | **AccessDenied** | another firm's source, no grant |
| N2 | read `opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/` | **AccessDenied** | another firm's source in the shared bucket |
| N3 | write `opal-data-bd/investor-reporting/directory/_negative_control_probe` **with a deliberately wrong `Content-MD5`** | **AccessDenied** | the 49 Financial DESTINATION. A bad digest means an AUTHORIZED write fails with `BadDigest` and writes nothing, so the probe cannot land an object: `AccessDenied` = not authorized, `BadDigest` = authorized (a FAIL of the control) |
| N4 | list `opal-data-49financial` at `gold/advi/` (outside the five) and get an object outside them | **AccessDenied** | the ListBucket condition and the GetObject scope bite |
| N5 | the SAME five reads on the HOST session, not assumed | **AccessDenied** | the host role itself gained nothing; the fence still refuses it |

**N3's probe shape is proved before it is trusted.** The wrong-digest write depends on S3 authorizing a
request before it checks the body. IB-rtc-7 first sends the SAME probe as the HOST session. The host is
a known writer of this prefix (the census above), so it must come back `BadDigest` with no object at the
key (a `head-object` 404 after). Only then does an `AccessDenied` for the assumed role mean "not
authorized" rather than "a probe that cannot tell".

---

## What this packet does not decide

Whether the destination should leave the legacy `opal-data-bd` before D14, and whether FWD-7's DONE WHEN
requires the directory in the firm's own bucket (R36-AC2 records the facts for `3.0.0_SA_CVO`).
