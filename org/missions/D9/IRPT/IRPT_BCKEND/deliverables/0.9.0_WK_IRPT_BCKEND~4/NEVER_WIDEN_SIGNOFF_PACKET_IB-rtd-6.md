# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtd-6: the directory write grant, all three firms

**For:** the two sign-off halves required before `IB-rtd-7` (the actual move cell) applies (CLAUDE.md:
never-widen sign-off is CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`. **Prepared by:**
`0.9.0_WK_IRPT_BCKEND~4` (`IRPT_BCKEND.TO-IB-rtd-6`). **Ruling carried:** R-44 @57bc083d45 (the same ruling
that shaped `IB-rtc-6`'s read-grant packet, applied here to a write grant). **NOTHING HERE IS APPLIED. Plans
only.** A half signs the **blast radius** of the act below: what each key may touch, and the rollback for
each key. It does not sign an intention. The halves themselves are written by the two seats, not by this
seat. A half that names fewer keys than this packet is `IB-rtd-7`'s stop condition.

---

## The act, in one paragraph

For **49 Financial only** (the leg that can port today -- see "the provisioning gap" below): a new IAM role,
**`irpt-49f-directory-write-role`** (builder output: `name('irpt', '49financial', 'directory-write', 'role')`),
assumable ONLY by `mdpf-daily-runner-ec2-role`, carrying `s3:PutObject` on
`opal-data-49financial/irpt/49financial/gold/directory/*` and nothing else. The host role gains ONE
statement, `sts:AssumeRole` on that role. The runner's 49 Financial destination write moves through the
assumed session. Inflection and Cottonwood are named but NOT ACTED ON by this packet -- their FIRM buckets
do not exist yet (measured live, below), so there is no fence for a write-principal to be admitted through.
**No read grant changes. No object is copied, moved or deleted. No legacy prefix is touched.**

---

## The keys (a half names every one)

| key | root / file | resource | change | plan line |
|---|---|---|---|---|
| **K1** | `investor-reporting/directory/principal_49f_write.tf` (new file, alongside `principal_49f.tf`) | `aws_iam_role.irpt_49f_directory_write` -> `irpt-49f-directory-write-role` | **create** | `+ create` |
| **K2** | same | `aws_iam_role_policy.irpt_49f_directory_write` -> `irpt-49f-directory-write-policy` | **create** | `+ create` |
| **K3** | `mdpf-pipeline/iam.tf` | `aws_iam_role_policy.mdpf_runner` (`mdpf-runner-scoped` on `mdpf-daily-runner-ec2-role`) | **+1 statement** | `~ update in-place` |
| **K4** | `investor-reporting/directory/schedule.tf` (or the runner's own dispatch env) | the runner/refresh Lambda's environment | **+1 env key** carrying the write-principal's ARN for the 49 Financial build only | `~ update in-place` |
| **K5** | code | `directory_runner.py` (destination repoint to `lib/opal_naming.py address()`, assuming the write session for the PutObject call) | behaviour, no IAM | not a Terraform resource |

### K1 -- the role and its trust

```
Trust (assume_role_policy), 1 statement, 1 principal:
  Sid AssumedOnlyByTheDailyRunnerHost  Allow  sts:AssumeRole
  Principal AWS = arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role
```

- **Name:** `name("irpt", "49financial", "directory-write", "role")` = `irpt-49f-directory-write-role`
  (`lib/opal_naming.py:1589-1608` @6c87bd0968). Not typed anywhere.
- **Fence admit check (live, measured this cell):** `opal-data-49financial`'s bucket policy
  `DenyForeignFirmPrincipals` admits `arn:aws:iam::313476888478:role/*-49f-*` (+ 16 named exemptions). The
  new role's name carries `-49f-` -> **matches the admit pattern**, same shape as `irpt-49f-directory-read-role`
  (`IB-rtc-6`'s K1).
  - `mdpf-daily-runner-ec2-role` itself: **does NOT match** `role/*-49f-*` -> stays DENIED for `s3:PutObject`
    on this bucket, exactly as it is denied for `s3:GetObject` today (measured live,
    `battery_ib_rtd_6.py` part_d output, `IB-rtd-6_R46-AC1_battery_output.txt` lines 245-249). This is WHY
    K1 exists: same-account trust cannot bypass a RESOURCE-policy Deny on the target bucket, and there is no
    other way to give the host a working PutObject there.
- **Before:** the role does not exist (no `principal_49f_write.tf` file exists yet in this tree).
- **Blast radius:** every process that runs as `mdpf-daily-runner-ec2-role` becomes ABLE to assume this
  role. Only the host role can; no other principal, user or service can. Same shape and same caveat as
  `IB-rtc-6`'s K1: the trust is as narrow as a principal ARN allows, but that principal is a shared host
  role -- the same host that also already holds `irpt-49f-directory-read-role`'s trust.
- **Rollback:** remove K1/K2 from the new `.tf` file (revert the declaring commit), then
  `.tools/safe-apply.sh -chdir=infra/aws/terraform/investor-reporting/directory apply`. Plans **2 to
  destroy** and nothing else -- no prior state to restore around it.

### K2 -- what the role may do

```
Sid WriteThe49FinancialLgicDirectoryOnly   Allow s3:PutObject
  arn:aws:s3:::opal-data-49financial/irpt/49financial/gold/directory/*
```

- **1** PutObject prefix; **0** GetObject/ListBucket (this is a WRITE-ONLY principal -- the read side stays
  on `irpt-49f-directory-read-role`, a DIFFERENT role, never widened); **0** statements on any other bucket;
  **0** actions on Inflection's or Cottonwood's buckets (they do not exist -- see below).
- **Address:** `lib/opal_naming.py address('irpt', '49financial', 'gold', 'directory', <as_of>,
  object=...)` -- nothing typed (part a of the result).
- **KMS:** none needed; `opal-data-49financial` is SSE-S3 (unverified this cell -- a live re-check is
  `IB-rtd-7`'s, same as `IB-rtc-6` re-checked `get-bucket-encryption` at its own apply time).
- **Blast radius:** whoever assumes K1 can write ONLY under `irpt/49financial/gold/directory/`. The host
  role itself still cannot: the fence denies it (K1's note).
- **Rollback:** as K1 -- the inline policy is deleted with the role's destroy.

### K3 -- the one statement on the host role

```
+ Sid IrptDirectory49fAssumeWritePrincipal  Allow  sts:AssumeRole
    Resource arn:aws:iam::313476888478:role/irpt-49f-directory-write-role
```

- **Before:** `mdpf-runner-scoped` -- **34 statements** as of `IB-rtc-7`'s apply (the K3 that grant added,
  32 -> 33, plus one grant this order did not track between rtc-7 and today; `IB-rtd-7`'s own re-plan reads
  the true BEFORE count immediately before applying, per bound (d)'s "re-plan immediately before" discipline
  IB-rtc-6 already established). This packet does NOT assert a specific before-count; `IB-rtd-7` captures it
  live, the same way `IB-rtc-6_host_policy_before.json` was captured.
- **Blast radius:** no new data access by itself; it names K1, and K1+K2 already describe the whole of it.
- **Rollback:** revert the statement, then apply the targeted command (`-target=aws_iam_role_policy.mdpf_runner`).

### K4 -- the runner's environment / dispatch

- An env key (or an equivalent dispatch-time export, mirroring `IB-rtc-6`'s K4/K5 shape for the READ side)
  hands the write-principal's ARN to the 49 Financial destination write only. The other two firms' builds
  are unchanged (they still write the LEGACY destination, since their write-principals do not exist).
- **Blast radius:** the 49 Financial build's shell only.
- **Rollback:** revert the env/dispatch line, then re-apply the directory root.

### K5 -- the code that uses it (no IAM, neutral until K1-K4 exist)

- `directory_runner.py`'s 49 Financial destination write is repointed to the LGIC address AND to an assumed
  session using the write-principal, mirroring `refresh.py`'s existing pattern for Firm49F's SOURCE reads.
  **Without K1-K4, this code path is not built by this order** (READ-ONLY bound) -- named here as the shape
  `IB-rtd-7` builds, not committed by `IB-rtd-6`.
- **Rollback:** revert the edit; the runner reverts to writing the legacy prefix.

---

## The plans (NOT applied), with their identities (R-40)

Baseline `terraform plan` on both roots this order's `<paths>` grants, re-run live by `battery_ib_rtd_6.py`
(`IB-rtd-6_R46-AC1_battery_output.txt` lines 261-281), each root freshly `init`ed with the vendored
`.tools/terraform.exe` v1.9.8:

| root | result |
|---|---|
| `investor-reporting/directory` | **No changes.** Matches the configuration -- this order adds no K1-K5 `.tf` text. |
| `mdpf-pipeline` | **0 to add, 1 to change** -- the SAME pre-existing `aws_s3_object.mdpf_route_bindings` CRLF drift `IB-rtc-6` found and excluded (`content-sha256`/`source_hash`/`version_id` only; not this act's, and still unapplied). |

Both baselines are consistent with "nothing applied, nothing planned but the pre-existing drift IB-rtc-6
already named" -- **the K1-K5 resources above do not exist in the tree yet and are not planned by this
run**; they are the SHAPE `IB-rtd-7` will add and plan for real, immediately before its own apply.

---

## The provisioning gap (measured live) -- why Inflection and Cottonwood are named, not acted on

```
opal-data-inflection: An error occurred (NoSuchBucket) when calling the GetBucketPolicy operation
opal-data-cottonwood: An error occurred (NoSuchBucket) when calling the GetBucketPolicy operation
```

Neither bucket exists. `infra/logic/registry/scopes.json` (`:119-156`, `:157-202` @22e86e55f5) carries
`bucket_provisioned: false` for both -- consistent with the live measurement. There is no fence to admit a
write-principal through on a bucket that does not exist, so this packet's K1-K5 are 49-Financial-only.
**Provisioning `opal-data-inflection`/`opal-data-cottonwood` (bucket + `DenyForeignFirmPrincipals` fence,
shaped like 49 Financial's) is a PREREQUISITE this packet does not authorize and this order does not
perform.** `IB-rtd-7` or a successor cell either performs it under its own never-widen packet (a NEW bucket
+ NEW bucket-policy act, a materially different blast radius from an IAM-role-only grant) or the two firms'
directories stay on their legacy destinations until it does.

---

## The writer census, before (R-44)

`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/writer_census_ib_rtc_6.py`
@474bdf1dc2, re-run live this cell (`IB-rtd-6_R46-AC1_battery_output.txt` lines 163-181), subject
`s3:PutObject` on `opal-data-bd/investor-reporting/directory/2099-01-01/directory.json` (the 49 Financial
LEGACY destination, unaffected by this packet -- it is not touched until `IB-rtd-7` retires it):

- RESOURCE plane: 2 bucket-policy statements, 0 allow a write, 0 Deny.
- IDENTITY plane: **263** principals simulated, 0 unsimulated, 0 UNKNOWN.
- **WRITERS: 12 of 263** -- unchanged from `IB-rtc-6`'s own count (12 of 262; the 263rd principal is
  `irpt-49f-directory-read-role`, itself NOT a writer).

This is the BEFORE state `IB-rtd-7` re-reads AFTER its apply and must find **unchanged** on the LEGACY
destination (the new write-principal is scoped to the NEW address only, so it cannot move this count), and
the same instrument, pointed at `opal-data-49financial` post-apply, must read the new write-principal as
the ONLY new writer of the LGIC address.

---

## The negative control, designed (not executed -- nothing is applied)

| # | attempt | expected | why it discriminates |
|---|---|---|---|
| NC1 | the host (`mdpf-daily-runner-ec2-role`), NOT assuming K1, attempts `s3:PutObject` on a 49 Financial LGIC key | **AccessDenied** | the fence (measured live, this packet): the host's ARN never matched the admit pattern |
| NC2 | the host, assuming K1 (the 49 Financial write-principal), attempts `s3:PutObject` on an INFLECTION or COTTONWOOD key (probed against a bucket that DOES exist, e.g. `opal-data-inf`, the LEGACY alias, as a stand-in since the LGIC buckets do not exist) | **AccessDenied** | K2 names only `opal-data-49financial/irpt/49financial/...`; no cross-firm write is granted |
| NC3 | the EXISTING 49f READ principal (`irpt-49f-directory-read-role`, already live per `IB-rtc-7`) attempts `s3:PutObject` anywhere | **AccessDenied** | it carries `GetObject`/`ListBucket` only; the write principal (K1) is a SEPARATE role, never a widened read role |
| NC4 (positive control) | the host, assuming K1, `PutObject`s a real key under `irpt/49financial/gold/directory/` | **allowed** | without this, every Deny above is uninformative (mirrors `IB-rtc-6`'s P1) |
| NC5 | as `IB-rtc-6`'s N3: the SAME PutObject probed with a deliberately wrong `Content-MD5` | **AccessDenied vs BadDigest** discriminates unauthorized (writes nothing) from authorized-but-malformed (would be a FAIL of the control if it fired on a supposedly-denied path) |

Proof shape (R-40): each NC bound to its SSM command id and the error code read AT THE EVENT, exactly as
`IB-rtc-6`'s N1-N5 were -- `IB-rtd-7`'s to run, not this packet's.

---

## What this packet does not decide

Whether Inflection's and Cottonwood's LGIC buckets should be provisioned as part of this project or as
D14's own full-name-migration scope (R46-AC2 records the facts for `3.0.0_SA_CVO`, no verdict here); and
whether the legacy destination retires in the SAME window as the 49 Financial leg's write grant, or waits
for all three firms to be ready together (a NEVER-shadow-pipeline question for `IB-rtd-7`'s own packet, not
this one's).
