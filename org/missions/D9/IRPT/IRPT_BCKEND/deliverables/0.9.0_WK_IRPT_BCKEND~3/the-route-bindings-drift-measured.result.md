# IB-rtd-4 -- THE ROUTE-BINDINGS DRIFT MEASURED AND ITS SIGN-OFF PACKET: result

**TO:** `IRPT_BCKEND.TO-IB-rtd-4` | **serial:** `0.9.0_WK_IRPT_BCKEND~3` |
**branch:** `wk-irpt_bckend-4-3` | **worktree:** `/c/tmp/wk-irpt-4-3` | **cut:** `e4623a5872`
**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rtd_4.py`
**Ruling executed:** R-44 @57bc083d45; round-3 analysis @5c59f68d70 s.6/s.9 item 5.

**READ-ONLY throughout.** Nothing applied, put, or edited under `data/mdpf/config/`. Two `terraform plan`
runs only (untargeted, and targeted to `aws_s3_object.mdpf_route_bindings`).

---

## ARM A -- the three-way content difference (by CONTENT, not hash alone)

| rendering | bytes | md5 | sha256 |
|---|---|---|---|
| committed (`git show HEAD:...`) | 13,516 | `650f893a7b9594404ce1d6f067b5b078` | `98f5e9c5...328d923` |
| worktree (this box, CRLF) | 13,701 | `f94e8e4c5d7c56d93f6ab16af227721d` | `37eb8451...96e21c2` |
| served (`s3://opal-data-assets/config/mdpf/route_bindings.yaml`) | 12,008 | `56a03a1410848f88b006f1f98b69dced` | `c9e54ce2...c834b971fcd` |

- **EOL-normalised:** committed == worktree: **True** (CRLF is the worktree's ONLY difference from
  committed -- confirmed by a SECOND instrument, `yaml.safe_load(committed) == yaml.safe_load(worktree)`
  -> **True**, corroborating the byte-level normalised compare rather than repeating it). committed ==
  served: **False** -- served differs in CONTENT.
- **Semantic diff** (denominator: 218 committed leaf keys, 215 served leaf keys): confined to ONE sub-tree,
  `firms.49financial.custody_leg.*` -- 7 added (only in committed), 4 removed (only in served), 5 changed.
  The served object still names the DELETED DynamoDB table `opal-assets-daily-aua`
  (`DDB_AUA_TABLE`/`ddb-cohort`); the committed content points at `fact_rps_s2`/`SCHWAB_SILVER`
  (`s3-monolith-silver`).
- **Last commit touching the file:** `f999fb25f6` 2026-08-07T16:19:35-04:00 "repoint the 49F custody
  binding off the deleted DDB table" (MDPF_REMED.W1-1).
- **Last write of the object:** `list-object-versions` shows exactly **1** version -- the object was
  first-minted 2026-08-07T00:13:10Z and never re-applied since (VersionId `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz`).
  `cloudtrail lookup-events` on this ResourceName returned rc=0, 0 events -- a management-event lookup, not
  evidence of a data-event trail; the object's own version history is the authoritative last-write evidence.
- **Bucket versioning:** `Enabled` (rollback is possible).
- **`eol=lf` finding:** `git check-attr eol -- data/mdpf/config/route_bindings.yaml` -> `unspecified`. A row
  (`IRPT_BCKEND-S68`, already filed by `0.4.0_DS_ClientPlatform~X`), not an edit -- BOUNDS.
- **INSTRUMENT TRAP surfaced and handled:** a plain `git hash-object` on the worktree file returns
  `73924ab7...`, IDENTICAL to the committed blob's oid, because `core.autocrlf=true` re-applies the clean
  filter before hashing -- it hides the exact CRLF divergence this cell measures. Every worktree-identity
  claim in this cell's outputs uses `git hash-object --no-filters` or the raw sha256/md5, never a filtered
  `git hash-object`.

## ARM B -- consumers and writers

**Consumers, 4 of 4 candidates resolved and read** (`comp-estate --resource route_bindings`:
`SUBJECT_ABSENT_FROM_CORPUS`, 135 of 135 chains scanned; `comp-pipescript io` on the deployed gold
consolidator: `READS: (none detected)`; `graph-call-manifest.yaml`: 0 hits):

| consumer | reads the S3 object? | CRLF-tolerant if it did |
|---|---|---|
| `mdpf-gold-lambda` (role `mdpf-gold-lambda-role`, the ONE IAM grant on this exact key, `infra/aws/terraform/mdpf-pipeline/iam.tf:766-769 @8d18193bcc`) | **NO** -- `data/mdpf/scripts/gold/mdpf_gold_consolidator.py:304-323 @1465fd3f7d` reads a package-adjacent/repo copy (bundled by `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:158 @ec8206c1b1` FROM the repo file at build time); its own docstring: "NEVER an S3-read leg here" | N/A -- unexercised grant |
| `build_mdpf_spine.py` (ad-hoc QA, not deployed) | NO -- `data/mdpf/scripts/gold/build_mdpf_spine.py:53-54,63-65 @bf74d031c1` reads the local repo file | YES (text-mode + `yaml.safe_load`) |
| `route_bindings_tieout.py` (W-1 validator, read-only) | NO -- `data/mdpf/config/route_bindings_tieout.py:31-34,132-134 @8058f55233` reads the local repo file | YES |
| `mdpf-daily-dispatch.sh` (EC2 runner) | NO -- `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:130,136-140 @cf838e54d5` syncs `s3://opal-data-mdpf/code/config/`, a DIFFERENT bucket/prefix than this cell's subject | N/A -- different artifact |

**Live re-run of the W-1 tie-out validator against the committed content, this run:** `34 tie rows checked
... 34 TIE / 0 FAIL` -- corroborates that the COMMITTED content is what the live code constants agree with
today; the served object's custody row would fail this same validator.

**IAM census (R-44's instrument, adapted for this key), both live this run:**
- **Writers (`s3:PutObject`): 3 of 263** principals -- `Andrew_Berman`, `Andrew_Berman_Console`,
  `Opal_Terminal` only. 0 Lambda/EC2/ECS role can write it (0 UNKNOWN, 0 unsimulated).
- **Readers-by-grant (`s3:GetObject`): 6 of 263** -- the 3 human/terminal identities, plus
  `mdpf-gold-lambda-role` (the intentional, unexercised grant), plus TWO INCIDENTAL roles whose S3 access
  is not specific to this key: `opal-news-lambda-role` (AWS-managed `AmazonS3ReadOnlyAccess`,
  account-wide) and `partners-lambda-role` (inline `Sid ReadPartnerBuckets`,
  `arn:aws:s3:::opal-data-*/*`). Neither names `route_bindings` anywhere in its own code (checked).

**So the practical blast radius of the served bytes today is ZERO code paths.** The drift is real and the
object should be brought current, but no live consumer's runtime behaviour changes because it changes.

## The untargeted root's full plan (not applied)

`terraform plan` on `infra/aws/terraform/mdpf-pipeline`: **0 to add, 1 to change, 0 to destroy** -- the
ONLY drifted resource in the entire root is `aws_s3_object.mdpf_route_bindings`
(`source_hash` `56a03a14... -> f94e8e4c...`, the CRLF render's own hash). A targeted plan of the object
alone plans the BYTE-IDENTICAL diff block (confirmed by hashing the diff block separately from the
`Refreshing state...` preamble, which differs between the two runs by construction and is not evidence of
a different act).

## R44-AC2 -- judgment, for `3.0.0_SA_CVO` (no verdict)

- **Which of the three renderings is the intended one:** the **COMMITTED content** (`git show
  HEAD:data/mdpf/config/route_bindings.yaml @e4623a5872`). It is what the live W-1 tie-out validator
  (`data/mdpf/config/route_bindings_tieout.py @8058f55233`) ties 34/34 against today, and what
  `dim_mdpf_aggregate_aua_timeseries.py`'s live constants (`SCHWAB_SILVER`, `fact_rps_s2`) already agree
  with per `data/mdpf/scripts/gold/build_mdpf_spine.py:81-93 @bf74d031c1`. Neither the served bytes (a
  stale pre-repoint snapshot naming a table Andrew deleted) nor a hypothetical "committed is wrong" reading
  is supported by any live evidence found.
- **Is the drift a rider of some other project's unapplied change:** **YES.** The served object's staleness
  traces to commit `f999fb25f6dd5127d06ebb9f23fecaa217352e4e` (`MDPF_REMED.W1-1`, "repoint the 49F custody
  binding off the deleted DDB table", 2026-08-07T16:19:35-04:00 @`f999fb25f6`), landed ~20 hours AFTER the
  object's sole apply (2026-08-07T00:13:10Z). `MDPF_REMED` is a separate project from `IRPT_BCKEND`; this
  cell's own project (`IRPT_BCKEND`) never touched `data/mdpf/config/route_bindings.yaml` or
  `config_objects.tf` before `IB-rtc-6`/`IB-rtc-7` (`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
  0.4.0_DS_ClientPlatform~X/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtc-6.md:145-148 @474bdf1dc2`), which
  observed the drift already present and routed AROUND it with a targeted apply.
- **Whose act the fix belongs to:** the APPLY belongs to MDPF's owner (`1.0.0_SA_CTO`, per the endpoint's
  own framing in this order's `<status>` line and the round-3 analysis item 5), as a SEPARATE act from
  IRPT_BCKEND's own cells -- `infra/aws/terraform/mdpf-pipeline/` is in this order's `<paths>` grant for
  MEASUREMENT only (BOUNDS: read-only, plan-only); IRPT_BCKEND's own scope is the 49 Financial directory
  and IRPT dispatch, not MDPF's route-bindings config object. `IRPT_BCKEND.TO-IB-rtd-5` (already cut, gated
  on both never-widen halves) is the vehicle for the apply act itself.

## Rows

No new row filed. `IRPT_BCKEND-S68` (ARMED, owner `2.0.0_SA_COO~B`, filed by
`0.4.0_DS_ClientPlatform~X`) is the row this cell measures; nothing surfaced here contradicts its
grounding or requires a second row at this coordinate. The IAM readers-by-grant finding (`opal-news-lambda-role`,
`partners-lambda-role` holding an incidental, unexercised `GetObject` grant on this key) is carried in the
packet as a finding, not filed separately -- it changes no premise of this task order and is not a
capability gap, a wrong path, or an invocation that failed to produce its named result.
