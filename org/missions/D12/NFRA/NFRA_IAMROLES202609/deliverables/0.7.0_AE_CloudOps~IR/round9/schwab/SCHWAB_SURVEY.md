# IAM-z-2 PHASE A -- opal-data-schwab: the reader is gone, the grant is next

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-2` - **Risk:** WORLD
**Read time:** 2026-10-12 03:5xZ - 04:1xZ. Every live value below was measured in that window.
**Standing (Z-S40):** this survey names its read time; the act re-reads its baseline before it applies.
**PHASE A committed:** this survey + the rollback. **No edit to any Terraform file** -- see section 3.

---

## 1. THE REFS LINE (step 1)

```
REFS: bd-exporter-ec2-role opal-data-schwab: env=0 code=11
```

**`env=0` with its cause named:** `bd-exporter-ec2-role` carries **14 EC2 instances** and **0 Lambdas**
(`bd-allocations`, `bd-assets`, `bd-fees`, `bd-gold-layer-runner`, `bd-gold-qa-runner`,
`bd-transactions`, and 6+ `historical-prices-fetcher`; graph bands `EC2_INSTANCE=14 IAM_POLICY=17
IAM_ROLE=1 INSTANCE_PROFILE=1` over 2926 nodes). An EC2 instance has **no API-visible environment**, so
this `env=0` means *the instrument cannot read this plane*, not *there is no reference*. The 0 Lambdas is
a real measurement: the same `comp-kuzu` query shape returns `opal-smartx-ingestion-pipeline` for a role
that has one, so it is not a wrong-pattern artifact.

**Positive control, as the cell requires -- one live bucket the role really uses:** over the same 174
files, `opal-data-bd` appears **189** times and `opal-data-assets` **12**. So a count of 11 for a 404
bucket sits beside a 189-count for a working one, read by the same pass.

**The grant, live:**

| | |
|---|---|
| policy | `schwab-bucket-access` (1 of **17** inline policies on the role) |
| Sid | `SchwabBucketReadWrite` |
| actions | `s3:GetObject`, `s3:PutObject`, `s3:ListBucket`, `s3:GetObjectVersion` |
| ARNs | `arn:aws:s3:::opal-data-schwab` **and** `arn:aws:s3:::opal-data-schwab/*` -- **2 of 2 dead** |
| TF address | **none** -- see section 3 |

**The name, re-read live:** `get-bucket-location opal-data-schwab` -> **rc=254, `NoSuchBucket`**; control
`opal-data-bd` -> **rc=0** in the same run.

**Rollback:** `.../schwab/ROLLBACK_schwab-bucket-access.json` -- 1 statement, 2 ARNs, in **document**
shape (not the wrapped API envelope; see section 6).

---

## 2. THE ROLE IS HOT, WHICH MAKES THIS THE ONLY ACT OF THE ROUND WITH A LIVE CONSUMER

```
aws iam get-role --role-name bd-exporter-ec2-role --query Role.RoleLastUsed.LastUsedDate
  -> 2026-10-12T02:30:42+00:00
```

**That is roughly one hour before this read.** Every other role this round touched was cold or
never-assumed: `workspace-sync` 2025-12-30, `infrastructure-ops` **null**, `smartx-exporter`
2026-06-01, `smartx-ingestion` 2026-08-14, `market-data-generator` **null**. This one is in daily use by
the bd pipeline, so it is the single act of round 9 where branch B -- a run that succeeded before the
change failing after it -- is a live possibility rather than a formality. The pair should know that
before it signs, and PHASE B should read a real bd run afterwards, which for this role is actually
available.

**What makes the narrowing safe anyway** is section 4: nothing that runs touches the dead bucket.

---

## 3. STEP 2 AS WRITTEN IS NOT PERFORMABLE: THERE IS NO DECLARATION TO EDIT

The cell's step 2 says *"In YOUR OWN worktree: edit the declaration; plan with -target on that address;
record `PLAN: bd-pipeline: <targeted plan summary, verbatim>` and the untargeted plan beside it."*
**`schwab-bucket-access` is not Terraform-declared, so there is no address to target and no plan to
record.**

| probe | result |
|---|---|
| `grep -c 'schwab-bucket-access'` in `infra/aws/terraform/bd-pipeline/iam.tf` | **0** |
| `grep -c 'opal-data-schwab'` in the same file | **0** |
| **positive control** -- `aws_iam_role_policy` blocks declared in that file | **29** |
| file size | 51,044 bytes |
| the role itself | declared there at `:341` (`resource "aws_iam_role" "bd_exporter"`, `name = "bd-exporter-ec2-role"`) |

So the ROLE is Terraform-managed and this POLICY is not -- a console/CLI-created inline policy on a
declared role. The cell's own framing anticipates this shape elsewhere (for `FredIngestionLambdaRole` it
says *"may be a console inline policy: then it is an IAM-API act"*), and it is the same re-route round 7
made for x-2's smartx act.

**Therefore ACT z-2(b) is an IAM-API act**, and because **2 of its 2 ARNs are dead**, narrowing would
leave an empty `Statement` list -- which is not a valid policy. **So the act is
`aws iam delete-role-policy --role-name bd-exporter-ec2-role --policy-name schwab-bucket-access`**, the
same shape as z-1's ACT 4, not `put-role-policy`.

In place of the two plans, the before/after document diff:

```
statements 1 -> 0    dropped-as-EMPTY: ['SchwabBucketReadWrite']
ARNs 2 -> 0, removed 2:
  - [SchwabBucketReadWrite] arn:aws:s3:::opal-data-schwab
  - [SchwabBucketReadWrite] arn:aws:s3:::opal-data-schwab/*
```

No after-document is written: there is nothing valid to write. The other **16** inline policies on the
role are untouched.

---

## 4. THE 11 CODE REFERENCES, CLASSIFIED -- AND ALL THREE LIVE ONES ARE RETIRED PATHS

Of 11 hits over 174 files, **3 are assignments that are actually used** and 8 are prose, docstrings or
dated historical notes (`"source was opal-data-schwab/01_raw/ (deprecating)"` in four converters, plus a
`gold_freshness_config.yaml` note). Each of the three was checked for USE, not just assignment:

| script | constant | used? | status |
|---|---|---|---|
| `bronze/convert_schwab_uln_to_silver.py:74` | `SRC_BUCKET` | **yes** -- `paginate(Bucket=)` `:135`, `get_object(Bucket=)` `:180`, print `:258` | **self-declared `*** DEPRECATED 2026-06-24 -- DO NOT USE ***`**, superseded by `convert_schwab_lots_to_silver.py uln`, "NOT in the recurring /49-schwab-conv skill" |
| `bronze/rps_ingestion.py:35` | `SCHWAB_BUCKET` | **yes** -- `paginate(Bucket=)` `:78`, upload `:115` | **0 references in the skill**; last touched 2026-05-18; a manual operator utility (`Author: 0.7.0_AE_CloudOps` -- this seat) |
| `bronze/sync_schwab_onedrive_to_s3.py:34` | `BUCKET` | **yes** -- `paginate(Bucket=)` `:47`, upload `:75`, print `:95` | the skill's **"Retired Step 1 (do not run)"** |

**So no scheduled producer touches the dead bucket.** All three are hand-run paths that are deprecated,
unreferenced or explicitly retired. The narrowing therefore breaks nothing that runs; what it changes is
that if a human ran one of these three by hand, it would fail `AccessDenied` instead of `NoSuchBucket` --
the same break with a less informative error. Filed as row **Z-S52**, naming all three.

> **A claim I nearly made and the classification stopped.** `convert_schwab_uln_to_silver.py` does NOT
> read monolith bronze (0 hits) while the skill states *"ALL SEVEN converters read this via
> `_monolith_bronze.py`; none reads local or `01_raw`."* I was one step from reporting the skill's claim
> false. It is **true**: the seven are invoked as `convert_schwab_lots_to_silver.py uln ult rld`, and
> that file **is** the monolith reader (4 hits) whose single `opal-data-schwab` mention is its own
> deprecation note. The file I had found is the retired predecessor, which says so in its own header.
> Counting a deprecated script as a converter would have produced a confident, wrong finding about a
> document that was right.

**One weakness in my own instrument, recorded:** my classifier labelled all three real assignments
`UNCLASSIFIED` rather than `S3`, because its regex tested `[Bb]ucket` and the constants are
`SRC_BUCKET` / `SCHWAB_BUCKET` / `BUCKET` -- all caps. The three most important hits in the census were
the ones it classified worst. The counts are right because every hit is printed and I read them; a
reader who had trusted the class labels alone would have concluded the opposite.

---

## 5. STEP 3 DONE: `.claude/skills/49-schwab-conv/SKILL.md` CORRECTED (LOCAL, no pair)

Line 3's description named `s3://opal-data-schwab` as the sync target. **Two** facts in that one sentence
were wrong, and the file's own body is what establishes both:

| was | now | why, from the skill's own body |
|---|---|---|
| "sync the new Schwab CRS files from OneDrive to **s3://opal-data-schwab**" | "forward from **MONOLITH BRONZE** (`s3://opal-data-assets/schwab/08242234/bronze/`) ... The OneDrive -> s3://opal-data-schwab sync is RETIRED (see Retired Step 1) and that bucket is DELETED: it returns NoSuchBucket, so anyone could claim the name" | line 26: *"SOURCE OF RECORD (2026-07-17 onward): s3://opal-data-assets/schwab/08242234/bronze/... ALL SEVEN converters read this"*; line 29 marks `s3://opal-data-schwab/01_raw/` **DEAD**; line 27 records the local OneDrive folder stopped delivering after `CRS20260715` |
| "all **six** silver tables (ACC, RPS, TRN, TRN_NNA, ULN, RLD)" | "all **seven** silver tables (ACC, RPS, TRN, TRN_NNA, ULN, **ULT**, RLD)" | line 30 lists seven `{acc,rps,trn,trn_nna,uln,ult,rld}`; line 93 invokes `uln ult rld`; line 95 says **"RUN ULT EVERY TIME"** and records that ult being un-invoked once froze `silver/ult` for 85 days |

I also corrected **line 29**, whose warning had been retired by this project's own act: it read
*"BUT `build_canonical_daily.py:154-156` **STILL ENUMERATES IT**"*. That read was removed by
`TO-IAM-z-5` @`7411ca0892`; `grep -c 'Bucket=SRC_BUCKET'` on that file now reads **0** at HEAD and in the
working tree. Leaving a warning that this round had just falsified seemed worse than the small scope
stretch, and the line now cites the commit that retired it.

**Diff: 2 files changed is 1 file, 2 lines -- 2 insertions, 2 deletions.** Byte hygiene: 0 CR; the file's
pre-existing non-ASCII count went **62 -> 61** (I replaced one em-dash with `--` in the line I rewrote and
introduced none; the remaining two non-ASCII characters on that line, `U+2014` and `U+26A0`, are from the
part I did not touch).

**The correction is already live where it is read:** the skill listing now shows the new description.

---

## 6. THE ROLLBACK WAS NOT RESTORABLE UNTIL THIS TURN

A shape audit of round 9's rollback documents found **2 of 13** written in the **WRAPPED**
`get-role-policy` response form (`{RoleName, PolicyName, PolicyDocument}`) rather than the policy
document -- and **one of them was this act's**. `put-role-policy --policy-document` takes the document;
handed the envelope it fails, so the artifact whose entire job is to restore this grant could not have
restored it.

The control I had run on those files proved each **equal to a fresh re-fetch** (7 of 7, canonical
`sort_keys`) -- which the wrapped form satisfies perfectly, because it is exactly what the API returns.
**It validated the file against its producer instead of its consumer.** Re-captured with
`--query PolicyDocument`; the re-audit reads **14 files, 0 WRAPPED, 14 DOCUMENT**. Both the cell's name
(`ROLLBACK_schwab-bucket-access.json`) and the older role-prefixed name now hold the same restorable
document, so nothing citing either breaks.

---

## 7. PHASE B'S PRECONDITION IS ALREADY MET

The cell gates PHASE B on act (a) -- the canonical builder's dead read -- landing first, measured not
reported:

```
grep -c 'Bucket=SRC_BUCKET' data/canonical/schwab/build_canonical_daily.py
  -> 0 in the working tree, 0 at HEAD
```

That is **AC1**, and it passes. `TO-IAM-z-5` landed it (@`7411ca0892`, drained; the COO recorded it
complete at `55962b72f9`). Reading the file at HEAD, `latest_rps_date()` now paginates
`Bucket=MONOLITH_BUCKET` and carries the comment *"opal-data-schwab bucket is deleted (its name is
claimable by any account): never read it."*

So the ORDER the cell insists on -- reader out before grant narrowed -- is satisfied, and narrowing now
cannot turn a silent dead read into a loud `AccessDenied` in the builder, because the builder no longer
reads it.

---

## 8. WHAT PHASE A DID AND DID NOT DO

**Did:** the classified reference census with a 189-hit positive control and a per-constant USE check;
the consumer census (14 EC2 instances, 0 Lambdas, with a validated graph control); the live
`NoSuchBucket` re-read with a live control; the grant decomposed per Sid and per ARN; the rollback
re-captured in restorable shape; the before/after document diff that stands in for the impossible plan;
`RoleLastUsed` read, which is the fact that most distinguishes this act from the round's others; and the
SKILL.md correction (step 3, LOCAL, no pair).

**Did NOT:** call `delete-role-policy` or `put-role-policy`, apply anything, open a NEVER-2 entry, touch
`build_canonical_daily.py` (its owner's, and already done by z-5), or touch any of the role's other 16
inline policies. No AWS write of any kind.

**For the pair:** the blast radius is one inline policy, `schwab-bucket-access`, deleted in full from
`bd-exporter-ec2-role`; 2 ARNs, both the 404 name; 16 sibling policies and the role itself untouched.
**Branch A** -- the delete lands, `list-role-policies` drops from 17 to 16 with `schwab-bucket-access`
absent and `get-role-policy` on it returning `NoSuchEntity`, and a real bd run after the change succeeds
(this role is hot, so one is actually readable). **Branch B** -- a bd run that succeeded before fails
after: restore with `put-role-policy` from the rollback document, then file a row. Section 4 is the
reason branch B is unlikely: no scheduled producer references the bucket at all.
