# DEAD_BUCKET_SWEEP -- NFRA_IAMROLES202609.TO-IAM-y-2 (round-7 analysis E2; row Z-S39 generalised)

**Cell:** IAM-y-2, **READ-ONLY** -- nothing applied, edited or deleted, and no bucket was ever created to
"test" a name. **Executed by:** `0.7.0_AE_CloudOps~IR`. **GO:** the round-8 issuance @`e27d52cb19`.
**Measured:** 2026-10-11 ~16:3xZ-16:5xZ. **No deploy ledger** -- there is no act to bound.

---

## 1. THE HEADLINE

**Seven bucket names in live identity grants do not exist. SIX OF THE SEVEN HAVE NO TOMBSTONE** -- no record
that anyone decided they should be gone -- **and FIVE of those six carry WRITE.** An S3 name is global, so each
is claimable by any AWS account, and a claimant would inherit whatever our grant allows.

Round 7 closed six ARNs on ONE role. This sweep is the account-wide question nobody had asked, and the answer
is that the class is wider than the role: **0 of these seven names were reachable only through the role x-5
narrowed.**

## 2. THE REQUIRED LINES

```
BUCKET: ajb-workflow class=ABSENT grants=1 write=yes
BUCKET: opal-313476888478-globgrph class=OURS grants=16 write=yes
BUCKET: opal-313476888478-lambda-artifacts class=OURS grants=11 write=yes
BUCKET: opal-313476888478-terraform-state class=OURS grants=1 write=no
BUCKET: opal-313476888478-yang-qa-scratch class=OURS grants=2 write=yes
BUCKET: opal-data-49financial class=OURS grants=16 write=yes
BUCKET: opal-data-assets class=OURS grants=62 write=yes
BUCKET: opal-data-astn class=OURS grants=2 write=yes
BUCKET: opal-data-bd class=OURS grants=38 write=yes
BUCKET: opal-data-cot class=OURS grants=20 write=yes
BUCKET: opal-data-cottonwood class=OURS grants=10 write=yes
BUCKET: opal-data-demo class=OURS grants=1 write=yes
BUCKET: opal-data-etfs class=OURS grants=22 write=yes
BUCKET: opal-data-harvest class=OURS grants=6 write=yes
BUCKET: opal-data-imo class=OURS grants=1 write=yes
BUCKET: opal-data-inf class=OURS grants=41 write=yes
BUCKET: opal-data-inflection class=OURS grants=11 write=yes
BUCKET: opal-data-irpt class=OURS grants=7 write=yes
BUCKET: opal-data-mdpf class=OURS grants=6 write=yes
BUCKET: opal-data-news-av class=OURS grants=6 write=yes
BUCKET: opal-data-news-v2 class=OURS grants=6 write=yes
BUCKET: opal-data-pm class=OURS grants=2 write=yes
BUCKET: opal-data-portal-s3 class=ABSENT grants=1 write=yes
BUCKET: opal-data-portal-v2 class=OURS grants=38 write=yes
BUCKET: opal-data-portfolio class=OURS grants=3 write=yes
BUCKET: opal-data-schwab class=ABSENT grants=1 write=yes
BUCKET: opal-data-security class=OURS grants=1 write=yes
BUCKET: opal-data-smartx class=ABSENT grants=1 write=no
BUCKET: opal-data-smartx-v2 class=ABSENT grants=3 write=yes
BUCKET: opal-data-trade-submissions class=OURS grants=1 write=yes
BUCKET: opal-data-transcripts class=OURS grants=6 write=yes
BUCKET: opal-data-ycharts class=OURS grants=11 write=yes
BUCKET: opal-estate-report class=OURS grants=5 write=yes
BUCKET: opal-infrastructure-snapshots class=OURS grants=2 write=yes
BUCKET: opal-market-data-v2 class=ABSENT grants=1 write=yes
BUCKET: opal-market-update class=ABSENT grants=1 write=yes
BUCKET: opal-mcp-audit class=OURS grants=2 write=yes
BUCKET: opal-runner-shared class=OURS grants=2 write=no
BUCKET: opal-security-evidence class=OURS grants=1 write=yes
BUCKET: opal-website-backups class=OURS grants=2 write=yes
BUCKET: opalinvest-portal class=OURS grants=1 write=yes
DENOMINATOR: principals=393 documents=651 names=41 wildcard_skipped=3
```

**Totals: 41 distinct concrete names -- 7 ABSENT, 34 OURS, 0 FOREIGN, 0 UNRESOLVED.**

## 3. WHAT WAS SWEPT, AND WHAT WAS DELIBERATELY NOT COUNTED

| | count |
|---|---|
| principals read (roles + users + groups + customer-managed policies) | **393** |
| -- roles / users / groups / managed policies (default versions) | 303 / 9 / 2 / 79 (79) |
| policy documents read | **651** |
| statements read | **1666** |
| distinct concrete bucket names in an **Allow** | **41** |
| wildcard names SKIPPED (counted, not classified) | **3** distinct, 9 occurrences |
| names appearing ONLY in a Deny / NotResource | **2** (not grants) |

**ONLY `Effect: Allow` COUNTS AS A GRANT.** A Deny naming a bucket is a guardrail, not an exposure, and
counting it would inflate every number here. The 2 Deny-only names are tallied above and excluded below, so
the choice is visible rather than silent.

**The wildcard names skipped are `opal*`, `opal-*`, `opal-data-*`** -- each would match many buckets and cannot be
classified by a `head-bucket` call, so they are counted and left for a different instrument. **A wildcard is
not evidence of safety:** `opal-data-*` grants on every future `opal-data-` bucket, including a name an
attacker creates. That is outside this cell's question and is named here rather than dropped.

## 4. THE SEVEN ABSENT NAMES, CROSS-REFERENCED AGAINST THE TOMBSTONE LIST

This is the cross-reference the cell did not ask for and it is the sweep's sharpest output. A tombstoned
absence is a **decision** with its debt tracked; an untombstoned absence is **nobody's decision**.

| bucket | write | tombstoned | what that means |
|---|---|---|---|
| `ajb-workflow` | **YES** | -- | **no record that anyone decided this should be gone** |
| `opal-data-portal-s3` | **YES** | -- | **no record that anyone decided this should be gone** |
| `opal-data-schwab` | **YES** | -- | **no record that anyone decided this should be gone** |
| `opal-data-smartx` | no | -- | **no record that anyone decided this should be gone** |
| `opal-data-smartx-v2` | **YES** | -- | **no record that anyone decided this should be gone** |
| `opal-market-data-v2` | **YES** | **YES** | ruled DELETE 2026-07-30; `declaration_removed: NOT YET -- TF-debt A7, OPEN` |
| `opal-market-update` | **YES** | -- | **no record that anyone decided this should be gone** |

- tombstoned (a ruled deletion, debt tracked): **1 of 7**
- **UNEXPLAINED absences: 6 of 7**
- of those six, carrying WRITE: **5**

**AND THE REVERSE CHECK, which is what makes the first number mean something.** Of the six tombstoned S3
buckets, only `opal-market-data-v2` is still named in any live Allow; the other five had their grants cleaned
up. **So the cleanup pattern exists and was followed 5 times out of 6** -- the outlier is not the rule, and
the six untombstoned names are not "how it is always done".

## 5. THE CONTROLS, AND THE ONE CLASS THAT HAS NONE

| class | control |
|---|---|
| **ABSENT (404)** | `opal-data-smartx`, which round 7 independently proved absent, is in the swept set and classified ABSENT by this run. |
| **OURS (200)** | all 34 names classified OURS appear in this account's own `list-buckets` (40 buckets). |
| **FOREIGN (403)** | **none, because the class is EMPTY.** |

**A class with no members has no control, and that is a fact about the account rather than a gap in the
sweep** -- but it is also the one verdict here I cannot corroborate. If a 403 had appeared it would have been
the URGENT finding (a name that already belongs to someone else, with our grant reaching it). None did.

**TWO CROSS-CHECKS, both clean:**

- names classified **OURS** that are NOT in our own bucket list: **0**. A 200 on a bucket we do not own would
  mean cross-account read access and would be a finding in itself.
- names classified **ABSENT** that ARE in our bucket list: **0**. That would be a flat contradiction between
  two reads and would void the sweep.

**ON THE INSTRUMENT:** `head-bucket` is the right tool *here* and the wrong one elsewhere. It is a HEAD
request, so it returns no error body -- which is why round 7's x-2 recorded `(404)` where an error CODE was
asked for and its AC1 failed. But this sweep needs exactly what a HEAD gives: the **status**, because 403 and
404 are the discrimination. The cell says `404 / NoSuchBucket` for that reason.

## 6. `market_data_v2` -- IT WAS NOT DELETED OUT OF BAND. ANDREW RULED IT.

The cell describes this bucket as "deleted out of band", and **my own x-1 survey said the same**. Both are
wrong, and the record was there to be read:

```json
// infra/aws/terraform/tombstones.json
{ "name": "opal-market-data-v2", "type": "aws_s3_bucket",
  "deleted": "2026-07-30", "verified_absent": "2026-07-30 (HeadBucket 404)",
  "declaration_removed": "NOT YET -- TF-debt A7, OPEN",
  "why": "Frozen-at-creation-day estate; Andrew ruled DELETE (semantic note 18)." }
```

`RULINGS_LEDGER.jsonl` carries the act itself, and the gate it passed is more thorough than anything this
project has run:

> DELETE executed. Gate: **0/192 lambda env refs + 0 portal two-hop + 0 refs in DEPLOYED code** of the 2
> portal-critical modeled readers (market-overview-tiered-generator, portal-data-proxy -- **zips pulled and
> grepped**) + frozen at creation day 7.2mo. **474 objects archived local-only, 474 versions purged,
> head_bucket 404, positive control 200, buckets 35->34**

**SO THE `4 to add` DRIFT IN `market-overview` IS NOT A BUCKET GOING MISSING -- IT IS TERRAFORM TRYING TO
RESURRECT A BUCKET ANDREW RULED DELETED.** That inverts the risk: x-1's pair treated `-target` as protecting
against recreating something lost, when it is protecting a ruling.

**AND THE RECREATE IS ALREADY GATED, WHICH NOBODY IN ROUND 7 NAMED.** `safe-apply`'s tombstone-gate checks
every planned create against this list; on my own x-6 apply it printed `checked 0 create(s) in this plan
against 7 tombstone(s)`. An untargeted `market-overview` apply would plan a create of a tombstoned bucket and
**the gate would refuse it.** `-target` was still correct -- a gate you did not know you were relying on is
not a control you can cite -- but the hazard was never as open as round 7's records imply.

**The declaration removal is a KNOWN, TRACKED, OPEN debt item: `TF-debt A7`.** `RULINGS_LEDGER` line 115
records that `0.7.0_AE_CloudOps` -- this seat, in July -- found A6/A7 (the `opal-data-aaii-v2` and
`opal-market-data-v2` declaration removals) in its own sweep and **DISOWNED them as NOT-AUTHORIZED**, on the
ground that they read as an obvious continuation of a thread Andrew had opened but were not inside his
approval. So the debt is open by a deliberate choice of this lane's own making, not by neglect.

### 6a. ITS CONSUMERS

| kind | count | detail |
|---|---|---|
| live IAM grants | **1** | `role/market-data-generator-lambda-role`, inline `market-data-generator-permissions`, **write=yes** |
| environment variables | **0** | checked live on `market-data-generator`, `opal-market-overview-tiered-generator`, `opal-portal-data-proxy` |
| deployed code | **0** | the July gate pulled and grepped the zips of both portal-critical readers; nothing has referenced it since |

**AND THE ONE GRANT IS HELD BY AN ORPHAN.** `market-data-generator-lambda-role` reads
**`RoleLastUsed: null`** -- never assumed in its existence -- and the served graph carries an `IAM_ROLE` and an
`IAM_POLICY` node for it but **NO `LAMBDA` node**: there is no function on this role at all. So the bucket's
only reference is a write grant that nothing can exercise.

The repo also holds three `opal-portal-lambda-role.inline.opal-portal-s3-read.json` copies naming the bucket,
under `v2_portal/{01_market_overview,02_model_portfolios,07_macroeconomics}/iam/`. **Those are stale repo
artifacts, not consumers:** x-5 removed that ARN from the LIVE policy, and the live document is the authority.
They are named because a future sweep of the repo will hit them and should not count them twice.

```
MARKET_DATA_V2_CONSUMERS: 1
```

## 7. WHAT THIS SWEEP HANDS TO ROUND 9, AND WHAT IT DOES NOT DECIDE

**The narrowing candidates -- ABSENT with write=yes, six of them:**

- `ajb-workflow` -- 1 principal(s): role/workspace-sync-lambda-role
- `opal-data-portal-s3` -- 1 principal(s): role/workspace-sync-lambda-role
- `opal-data-schwab` -- 1 principal(s): role/bd-exporter-ec2-role
- `opal-data-smartx-v2` -- 3 principal(s): role/infrastructure-ops-lambda-role, role/smartx-exporter-role-20251218220948293500000001, role/smartx-ingestion-lambda-role
- `opal-market-data-v2` -- 1 principal(s): role/market-data-generator-lambda-role
- `opal-market-update` -- 1 principal(s): role/FredIngestionLambdaRole

**NOTHING IS URGENT IN THE FOREIGN SENSE: that class is empty.** The cell says each FOREIGN name would be
urgent; none exists, so the urgency the sweep was cut to find is absent, and saying so plainly is the result.

**WHAT I DO NOT DECIDE, and why each is someone else's:**

- **Whether any of the six should be narrowed or RECREATED.** `opal-market-data-v2` is the proof that
  "absent" does not imply "should be absent" in reverse: for a tombstoned name the answer is narrow the
  grant, but for an untombstoned one, nobody has established whether the bucket or the grant is the mistake.
  Six names may not share one answer -- the same shape as x-5's six.
- **`TF-debt A7`.** Known, open, and disowned as unauthorized by this lane in July. Re-authorizing it is
  Andrew's or the CTO's, and I am not reopening a scope question this seat already closed against itself.
- **The three wildcard grants.** `opal-data-*`, `opal-*` and `opal*` cannot be swept by name and are a
  different question with a different instrument.
- **Anything about the 34 OURS names.** They exist and are ours; this cell asked whether grants point at
  nothing, not whether live grants are right-sized.

**READ-ONLY. No AWS write, no policy edit, no bucket created, no ledger opened. Every classification is a live
`head-bucket` read, every count is printed beside its denominator, and the 41 `BUCKET:` lines above were
GENERATED from the measured data rather than transcribed.**
