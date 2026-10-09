# Never-widen ask -- OG-tm-1, add the Tax SMA master 08403355 to the daily pull, its silver conversion and the gateway's reader roles

By: `0.9.0_WK_NFRA_OPLGTW~39` for the issuer `2.0.0_SA_COO~O`, 2026-10-09 ~00:5xZ. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-tm-1.taxsma-master-daily-add.md` at amendment A1 (@4d0222ab81).
Phase A build: @cb9358a9e0 (LOCAL on branch `wk-NFRA_OPLGTW-32-39`). Nothing is applied, uploaded or sent.
Evidence is in `deliverables/0.9.0_WK_NFRA_OPLGTW~39/`: `plans/*.txt`, `probes/*`, `data_assets_mirror.patch`,
`tm1_contract_hookup.json`, and the OG-en-1 record `g5_enumerate_record.json` (@8ba9b3d865).

**Authority.** Andrew-direct 2026-10-08 ~17:4xZ answer 1 and ~21:2xZ ("added to the daily pull and opalgateway asap");
PRD v2.0 item 5; round-31 analysis section 4a item 7. Shape ruling: `1.0.0_SA_CTO~O` msg 32147 (relayed 2026-10-09 00:08Z):
08403355 without `slm` IS "the same shape", on two conditions, answered in section 2.

**Halves owed:** `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`, both against THIS file at its commit. The applier is `0.7.0_AE_CloudOps~Z`
(ledger entry `nfra-oplgtw-og-tm-1-taxsma-master`, which that seat opens and closes). Phase B is not mine.

## 0. Open items the halves must settle (read first)

1. **BLOCKING row `NFRA_OPLGTW-Z-W39-S4`.** The silver-schwab package dir is a vendored copy of `data/assets/scripts/silver/`
   (9 shared modules, byte-identical today), which is outside my `<paths>`. The converter change must also land in the source
   with its two test edits, or the next rebuild from source ships a converter that refuses 08403355. The patch is
   `data_assets_mirror.patch` (4 files; `git apply --check` clean; 46 of 46 tests pass with it). `silver.tf`'s
   `silver_build_commit.schwab` (now `1f03a3f209`) must then name the commit where source and package are equal; I did not edit it
   because that commit does not exist yet. Leg C below does not ship until both are done.
2. **Unrelated drift in two roots (row `S5`, ARMED).** The opal-assets plan also carries `cot_rebalancer_runner_daily`
   (cron 06:00 -> 12:45) and the opal-gateway plan carries `mcportal_grant_writer` (code hash). The apply order must use the
   `-target` lists in section 1; a whole-root apply is outside this ask.
3. **The label `"Tax SMA basis"`** (new `BASIS_LABEL` entry) is my proposal. The label is the never-summed identity recorded on
   every run manifest, so the CTO half should ratify the string.
4. **The first pull lands the 30-day window, not one day.** The rule runs with the puller's default `-LookbackDays 30`, the same
   as the other two rules, and OG-en-1 measured 226 distinct files over 22 dates and 13 types. The first pull (the QA pull) lands
   those 226 objects and raises 226 `ObjectCreated` events to the converter (reserved concurrency 2). Later daily pulls land about
   one day. If the halves want one day only, the rule input would differ from its siblings (`-LookbackDays 3`), which departs from
   "exactly the same structure"; I implemented the sibling shape.
5. **Option B for the IAM replacement window** (section 3, resource 8). Decide: accept the planned replace with the timing
   mitigation, or add `lifecycle { ignore_changes = [description] }` to `silver_write_per_source` first.

## 1. The bytes and the resources (what the act may touch)

Everything below is the new master's keys and the three IAM/rule surfaces; nothing else.

| # | Root | Resource (apply `-target`) | Plan action | Change |
|---|---|---|---|---|
| 1 | canonical-schwab-ec2 | `aws_cloudwatch_event_rule.si2_daily["08403355"]` | create | `cron(45 10,22 * * ? *)`, label "Tax SMA" |
| 2 | canonical-schwab-ec2 | `aws_cloudwatch_event_target.si2_daily["08403355"]` | create | SSM `AWS-RunPowerShellScript` on `i-0f3d57a97f14727af`, the same input as the siblings with `-Master 08403355` |
| 3 | canonical-schwab-ec2 | `aws_iam_role_policy.schwab_si2_monolith_write` | in place | +`schwab/08403355/bronze/*` (list, put), `_ops/*`, `meta/pulls/*` (put). The one-time remap role in the same file is NOT extended. `iam.tf` lists no masters: unchanged |
| 4 | opal-assets | `aws_iam_role_policy.silver_read_bronze["schwab"]` | in place | +`schwab/08403355/bronze/*` read and list |
| 5 | opal-assets | `aws_s3_bucket_notification.monolith_bronze` | in place | +ONE rule `silver-schwab-08403355` (`schwab/08403355/bronze/`, `.zip`) -> `opal-assets-silver-schwab` |
| 6 | opal-assets | `aws_iam_policy.monolith_write_per_source["schwab"]` | replace | +`08403355` in both lists; `attachment_count = 0` (nothing attaches it) |
| 7 | opal-assets | `aws_iam_policy.silver_write_per_source["schwab"]` | replace | +`schwab/08403355/silver/*` and `meta/*` |
| 8 | opal-assets | `aws_iam_role_policy_attachment.silver_write["schwab:schwab"]` | replace | follows 7 |
| 9 | opal-assets | `module.silver_converter["schwab"]` (code hash) | in place, after the upload | package built from @cb9358a9e0 |
| 10 | opal-gateway | `aws_iam_role_policy.schwab_data_read_policy` | in place | +four `schwab/08403355/silver/dim_*` prefixes |
| 11 | opal-gateway | `aws_iam_role_policy.schwab_catalog_read_policy` | in place | +`schwab/08403355/meta/complete/` |
| 12 | S3 code object | `s3://opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1` | replace bytes | `ValidateSet` gains `'08403355'`, one token |
| 13 | S3 artifact | `s3://opal-313476888478-lambda-artifacts/opal-assets/opal-assets-silver-schwab.zip` | new version | 2 members differ |

Plan totals (verbatim in `plans/`): canonical-schwab-ec2 `2 to add, 1 to change, 0 to destroy`; opal-assets
`3 to add, 3 to change, 3 to destroy` (of which `cot_rebalancer_runner_daily` is unrelated, row S5); opal-gateway
`0 to add, 3 to change, 0 to destroy` (of which `mcportal_grant_writer` is unrelated). In the targeted form the new master's
net is: 2 add and 1 change (ec2); 3 add, 2 change, 3 destroy (opal-assets, the add/destroy being the replacements 6-8);
2 change (gateway).

**Code object (12).**
- Before: ETag `0017f9b549ca9f8013704f50c4327bed`, 35,842 bytes (= the repo file at @4d0222ab81, MD5 verified on the box in OG-en-1).
- After: MD5 `e49aea76a8c634c9d49e6a7cccc51bdf`, 35,853 bytes (single-part, so the S3 ETag equals the MD5). The diff is one line,
  `[ValidateSet('08242234','08335338')]` -> `[ValidateSet('08242234','08335338','08403355')]`.
- Because every scheduled pull re-pulls this object (Rule 12), the existing two masters' next pulls run the new bytes. Their
  behaviour is identical: `-Master` is validated against a set that still contains both.

**Converter artifact (13).**
- `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh opal-assets opal-assets-silver-schwab` built (no upload):
  sha256 `AzrzJS+91y57ylRdqGccFPGqWaqAGLFn/jhItkAQCzE=`, 74,839 bytes.
- Live now: sha256 `v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`, ETag `c46721a1a616713f0571e327fa273aef`, 74,535 bytes,
  VersionId `7Db1UfM3EU_Z6q4cLQiV4wM3bYaAaFMF`.
- `probes/tm1_zip_live_vs_new.txt`: 12 members each side; live equals git @4d0222ab81 member for member (12 of 12); exactly two members
  differ new-vs-live: `conversion_manifest.py` and `silver_registry.py`.
- The build embeds the working tree, so the applier rebuilds from the merged commit and compares the sha256 to the one above.

## 2. The ruling's two conditions

**Condition 1 -- the puller, the converter and every consumer run without `slm` for this master and date.**
- *Puller.* `sdd-daily-pull.ps1` is type-agnostic. The type is derived from each vendor filename (`TypeFolder`), and the only
  emptiness check is on the TOTAL (`ENUMERATED = 0` on a trading day, `Die 2`). It names `slm` only in comments. OG-en-1 ran this
  exact enumerate path for 08403355: 226 files, exit 0.
- *Converter.* The expected table set of a day derives from that day's bronze (`build_closure`, "never from a fixed cross-master list
  -- the two masters' type sets differ by construction"; `set_identity_guard.py` header: "0824 carries rlw, no fam/slm"). The only
  type a pipe delivery must carry is `RLD` (`NON_OPTIONAL`), and `slm` rides the CS channel, which the guard exempts by name.
  `slm` has no projection (`schwab_projections.py`: "FAM/SLM ... have no projections"), so no `dim_*` served table depends on it.
- *Measured on the live producer.* `08242234` (which also has no `slm`) on 2026-10-07: `status qualified`, `day_disposition DATA`,
  14 expected tables, `fact_slm` listed in `non_applicable` as `DECLARED_NO_SOURCE_PARTITION`. `08335338` on the same date:
  `qualified`, `DATA`.
- *Consumers.* The gateway serves four `dim_*` tables and the closure; `app/` has no `slm` reference, and its closure validator is
  the producer's rule ported verbatim, where `non_applicable` is only counted and hashed. The 49F accelerator is keyed to
  `schwab/08335338/meta/complete/` alone. A repo search for `fact_slm` finds only 08335338's own data, org scripts and gateway
  fixtures. I read no reader that requires an `slm` file for a master and date.
- *Limit.* This is a code and live-closure read plus a synthetic-inventory run of the changed `build_closure`
  (`probes/tm1_closure_probe.after.txt`: a 08403355 day with 13 types and no `slm` -> `qualified`, 0 findings). It is not a real
  08403355 day; that is what Phase B's QA pull proves (AC2).

**Condition 2 -- the completion record lists `slm` as an explicit NON-APPLICABLE disposition for 08403355.**
- Today's producer would already list `fact_slm` (generic `DECLARED_NO_SOURCE_PARTITION`) on any day without `slm`; that wording
  does not say the master never publishes it, and it reads the same for 08335338 on a day its `slm` is simply missing.
- *The minimum change (Leg C, producer code):* in `conversion_manifest.py`, a constant
  `MASTER_NOT_PUBLISHED = {"08403355": ("slm",)}`, used in `build_closure` only for a type absent from that day's bronze: the
  closure then carries `{"kind":"source_partition","subject":"slm","reason":"NOT_PUBLISHED_FOR_MASTER"}` and
  `{"kind":"table","subject":"fact_slm","reason":"NOT_PUBLISHED_FOR_MASTER"}` for 08403355 only. about a dozen lines in one file.
- *Both branches (probe + 2 tests in the patch):* 08403355 without `slm` -> qualified, both entries present; 08242234 without
  `slm` -> unchanged `DECLARED_NO_SOURCE_PARTITION`; 08403355 WITH an `slm` object landed -> no entry, `fact_slm` is in
  `expected_tables` and converted normally (the declaration never suppresses a real file).
- *Closure identity.* `non_applicable` is inside the closure hash, so 08403355 closures carry a hash that includes the new reason;
  producer and gateway recompute from the object's own fields, so both agree.
- Negative control: the same inputs against the HEAD converter raise `ManifestError: master '08403355' has no basis label`
  (`probes/tm1_closure_probe.before_HEAD.txt`): without Leg C's master edits the converter refuses the master.
- **Both conditions are met in the code I can read.** Leg C is a deploy leg for `0.7.0_AE_CloudOps~Z`; it is blocked on S4, not on
  the conditions.

Also changed in the package, needed for the converter to accept the master and not part of the `slm` leg: `DECLARED_SCHWAB_MASTERS`
(`silver_registry.py`, gives the sweep a third lane) and `BASIS_LABEL["08403355"] = "Tax SMA basis"` (`conversion_manifest.py`, without
which `build_manifest` and `validate_closure` refuse the master). The sweep now runs three lanes in one invocation: the function's
timeout is 600 s and its longest recorded Duration since 2026-09-25 is 159 s (CloudWatch Maximum, 14-day period).

## 3. Blast radius per S3 prefix and per resource

**Per prefix, `s3://opal-data-assets/schwab/08403355/`** (a new tree; `KeyCount = 0` today, OG-en-1 AC2):

| Prefix | Who writes after the act | Notes |
|---|---|---|
| `bronze/{type}/{YYYYMMDD}/` | the SI2 box role (`aws_iam_role.schwab_si2`, policy `quartz-si2-monolith-write`): PutObject | raw vendor zips, additive; the box has no GetObject and no Delete |
| `_ops/daily_pull/` | the same box role: PutObject | run record |
| `meta/pulls/` | the same box role: PutObject | pull manifest |
| `silver/{table}/date=/` | `opal-assets-silver-schwab-role` via policy `opal-assets-silver-write-schwab` | converter |
| `meta/conversions/` | the same converter role | run manifest |
| `meta/complete/date=*.json` | the same converter role | the closure the gateway reads |

Readers: the converter reads `bronze/` only (item 4); the two gateway roles read `silver/dim_*` and `meta/complete/`.

**Writer census (N principals, counted from the three roots and the live attachments I read):**
- N = 2 for any `schwab/08403355/` key: the SI2 box role (bronze, `_ops`, `meta/pulls`) and the schwab converter role (silver, `meta/*`).
- Not writers: `opal-assets-write-schwab` (item 6) has `attachment_count = 0`;
  `quartz`'s one-time remap role is not extended; `bd49f_convert` writes only `schwab/08335338/silver/fact_acc/*`; the consolidation
  gold runner writes `schwab/<its master>/gold` for its single configured master. I did not enumerate every IAM principal in the
  account; the census is bounded by the Terraform I read, and the Phase B read-back repeats it from IAM
  (`simulate-principal-policy` on `PutObject` under the new bronze key, both gateway roles' denies as controls).
- Other branch: any writer found beyond these two is a BLOCKING row and the act does not proceed.

**`ObjectCreated` consumers of `schwab/08403355/`** (live notification list: 11 rules; planned: 12):
- `bronze/*.zip` -> `opal-assets-silver-schwab` (new rule, item 5); `lambda:InvokeFunction` from the bucket already exists per
  family (`AllowS3InvokeFromMonolith`), so no permission is added.
- `meta/complete/*.json` -> NO notification (the 49F accelerator rule `advi-49f-silver-complete-accelerator` stays on
  `schwab/08335338/meta/complete/`). No prefix overlap with any other rule.
- The notification resource is the bucket's singleton: the apply re-PUTs the whole configuration. The plan shows the other 11 rules
  unchanged apart from list order; a post-apply read must show exactly those 11 plus the new one (12), same ids.

**Per resource:**
- 1-2 (rule, target): a new rule; the first fire is the next 10:45 or 22:45Z after creation. Gaps: 30 min after 08242234
  (10:15/22:15) and 60 min after 08335338 (09:45/21:45); the box-wide session lock refuses a contended start (exit 7). The
  puller's 50-minute deadline now runs the occupied window to about 11:35 and 23:35Z.
- 3 (box grant): adds writes on the new master's three prefixes only; no other action.
- 4, 7: grants limited to the new master's `bronze/` read and `silver/`+`meta/` write.
- 5: one new notification rule (above).
- 6-8: **a replacement window.** `description` is ForceNew and interpolates the scope list (the hazard `monolith.tf` documents).
  Item 6 is unattached, so replacing it moves nothing. Items 7+8 are attached to the live converter role: Terraform detaches,
  deletes and recreates, so for a few seconds the converter has no silver write grant. A conversion landing in that window fails
  AccessDenied, retries (async, 2 retries), then goes to the DLQ, and the 12:15Z sweep re-converts misses.
  - *Mitigation A (default):* apply 7+8 when no bronze is landing: outside [09:15,11:35) and [21:15,23:35)Z and outside
    [12:00,12:45)Z (the sweep).
  - *Option B:* add `lifecycle { ignore_changes = [description] }` to `silver_write_per_source` before the apply; the plan then reads
    an in-place policy update and there is no window. It is a one-line edit not in this commit and it departs from "exactly as the
    other masters".
- 9, 13 (converter): the same function serves 08242234 and 08335338; their conversion code paths are unchanged (12 of 12 members
  equal except two, whose diff is the master list, the label and the closure reason text). The 30-day first pull (item 4 above)
  queues 226 events behind reserved concurrency 2.
- 10-11 (gateway roles): extend the allow-lists by the new master's prefixes; the roles' explicit denies (`DenyAllNonReadActions`,
  `DenyReadsOutsideApprovedDatasets`, bronze and `fact_*` untouched) stay. No gateway code, contract or release is part of this act;
  `tm1_contract_hookup.json` holds the contract lines for the issuer.

## 4. Rollback per resource

- 1-2: delete the rule and target (`terraform` targeted destroy of the two), or `DISABLED` first. Nothing else depends on them.
- 3: re-apply the prior policy document (revert the three added resource lines); data already landed stays (bronze is additive).
- 4-5, 7-8, 10-11: revert the commit and re-apply the same `-target` list; 7+8 repeat the replacement window.
- 6: revert; no dependents.
- 12 (code object): restore the prior bytes: `git show 4d0222ab81:infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1`, upload; the ETag
  must read `0017f9b549ca9f8013704f50c4327bed` again. The bucket is versioned, so the prior version can also be restored.
- 13 / 9 (converter): re-point the function at the saved prior artifact version (`VersionId 7Db1UfM3EU_Z6q4cLQiV4wM3bYaAaFMF`, sha256
  `v2Bztqbu...`) by the same targeted apply; the bucket is versioned.
- Data: objects landed under `schwab/08403355/` are new keys. Removing them is a deletion and is not part of this rollback; if the
  halves want them removed, that is a separate signed act.

## 5. Order of legs and timing

1. **Leg C first:** the converter artifact upload (13) and the opal-assets targets 4-9, so the converter, its scope and its
   notification exist before any bronze lands. Not before S4 is closed.
2. **Leg B:** box grant (3, ec2 root), then the puller code object (12). Both outside [09:15,11:35) and [21:15,23:35)Z.
3. **Leg A last:** the rule and target (1-2). The rule must not exist before legs 1-2 are in place: its first fire would land bronze
   into a converter that refuses the master.
4. **Gateway roles (10-11):** any time after the contract hookup is decided; independent of the pull.
5. **QA pull (Phase B step 11):** after all of the above, outside [09:15,11:05) and [21:15,23:05)Z and outside the new rule's own
   hours (10:00-10:59Z and 22:00-22:59Z); I propose 13:00-20:30Z. It uses the rule's own input read back from
   `aws events list-targets-by-rule`, and lands the 30-day window (item 4).

## 6. Halves

**COO -- owed.** (the issuer signs section 3's per-resource radius, the leg order, and decides section 0 items 1, 2, 4, 5.)

**CTO -- owed.** (ratifies the label `"Tax SMA basis"`, the `slm` NOT_PUBLISHED disposition as the minimum change for condition 2,
and the shape ruling's two conditions as answered in section 2.)
