# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtd-4: the route-bindings S3 object drift (row S68)

**For:** `1.0.0_SA_CTO` (MDPF's owner) and `2.0.0_SA_COO~B`. **Prepared by:** `0.9.0_WK_IRPT_BCKEND~3` (IRPT_BCKEND.TO-IB-rtd-4), measured 2026-09-18T13:35:20Z. **Ruling:** R-44 @57bc083d45; the round-3 analysis @5c59f68d70 s.6/s.9 item 5. **NOTHING IS APPLIED HERE. Plans only.**

A half signs the **blast radius** of the act below: what each key may touch and the rollback for each key. The halves themselves are written by the two seats, not by this seat.

---

## The act recommended, in one paragraph

`aws_s3_object.mdpf_route_bindings` (`infra/aws/terraform/mdpf-pipeline/config_objects.tf`) is served at a byte sequence that is NEITHER the committed blob NOR any CRLF rendering of it -- it is a DIFFERENT, EARLIER content (12,008 bytes, sha256 `c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd`), created once on 2026-08-07T00:13:10Z (the object's only version) and never re-applied since. `git log -1` on the committed file shows its LAST touching commit landed the SAME DAY at 16:19:35-04:00 (`f999fb25f6`, 'repoint the 49F custody binding off the deleted DDB table', MDPF_REMED.W1-1) -- roughly 20 hours AFTER the object was last applied. The semantic diff (committed vs served, 218 committed / 215 served leaf keys) is confined to ONE sub-tree, `firms.49financial.custody_leg.*`: the served object still names the DELETED DynamoDB table `opal-assets-daily-aua` (symbol `DDB_AUA_TABLE`), which Andrew deleted on 2026-08-07 ('too late got rid of both and dont care'); the committed content correctly points at `fact_rps_s2` / `SCHWAB_SILVER`. Re-running the W-1 tie-out validator live against the committed content: **DENOMINATOR: 34 tie rows checked (code-literal=13, computed=2, computed-expr=1, const=16, const-dict=1, const-tuple=1); 34 TIE / 0 FAIL**. **RECOMMENDATION: a TARGETED apply of `aws_s3_object.mdpf_route_bindings` alone, from a checkout with `eol=lf` enforced (or via `git show HEAD:... > tmp && terraform apply` sourced from the LF bytes, never this Windows box's CRLF worktree render) -- never an untargeted apply from this box (below), and never the reverse claim ('the committed file is wrong') -- the committed content is the one the live tie-out validates and the deleted table is not a viable revert target.**

---

## The three-way content difference (ARM A, by CONTENT not hash alone)

| rendering | bytes | md5 | sha256 | identity note |
|---|---|---|---|---|
| committed (`git show HEAD:...`) | 13516 | `650f893a7b9594404ce1d6f067b5b078` | `98f5e9c51d016d5283562e525b53088292576d86752c6cf0449865fbf328d923` | git blob oid `73924ab7efbf8eb3808bd9994bbf7a95ed1f3e2e` |
| worktree (this box, CRLF render) | 13701 | `f94e8e4c5d7c56d93f6ab16af227721d` | `37eb845123b155ef8993babdda60d918b119331d9ad83c4b725ca081096e21c2` | raw on-disk (`--no-filters`) git oid `96bc8bd7581ffc0d4930d7634de101833bfee15f`; WARN: a plain `git hash-object` on this file returns `73924ab7efbf8eb3808bd9994bbf7a95ed1f3e2e`, IDENTICAL to the committed oid, because `core.autocrlf=true` re-applies the clean filter before hashing -- **never cite a filtered `git hash-object` as this file's on-disk identity** |
| served (S3 `s3://opal-data-assets/config/mdpf/route_bindings.yaml`) | 12008 | `56a03a1410848f88b006f1f98b69dced` | `c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd` | ETag `56a03a1410848f88b006f1f98b69dced`, VersionId `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz`, LastModified `2026-08-07T00:13:10+00:00`, object metadata `content-sha256`=`c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd` (self-consistent: equals the served bytes' own sha256) |

**EOL-normalised verdict:** committed == worktree after CRLF->LF normalisation: **True** (the worktree's ONLY difference from committed is EOL rendering). committed == served after normalisation: **False** (served differs from committed in CONTENT, not merely EOL).

**Semantic diff, committed vs served** (denominator: 218 committed leaf keys, 215 served leaf keys, union 7):

- **Added in committed, absent in served (7):** firms.49financial.custody_leg.source.fact, firms.49financial.custody_leg.source.field, firms.49financial.custody_leg.source.prefix, firms.49financial.custody_leg.tie[1].contains, firms.49financial.custody_leg.tie[2].contains, firms.49financial.custody_leg.tie[2].file, firms.49financial.custody_leg.tie[2].kind
- **Removed (present in served, absent in committed) (4):** firms.49financial.custody_leg.source.cohort, firms.49financial.custody_leg.source.table, firms.49financial.custody_leg.tie[1].expect, firms.49financial.custody_leg.tie[1].symbol
- **Changed (5):** `firms.49financial.custody_leg.authority`: served='ANDREW-CANONICAL (his 141545Z expansion + 140458Z source map), carried VERBATIM per F-1 ruling / C-1 PRESERVED-BY-BINDING: "whatever the aua content of the schwab 08242234 account serves", per-date; SUPERSEDES the fact_rps_s2 envelope as the served custody series. ETFS-CANON may later re-bind THIS ROW ONLY -- zero route change (ratified boundary, rulings F-1).' -> committed='SUPERSEDED BY MEASUREMENT 2026-08-07 (MDPF_REMED.W1-1). The 49F custody series is SUM(fact_rps_s2.net_mv_plus_cash) -- positions + full cash leg. Re-derived at the 0.4.0_DS seat against served platinum/mdpf/49financial/aggregate-aua-timeseries.json (meta.basis "schwab-rps"): EXACT to the cent on 9 of 9 post-7/23 dates, while the net_mv_positions negative control misses on 9 of 9 by $24,768,500.61..$32,146,081.74. The negative limb failing every date is what makes the positive limb evidence rather than coincidence. BOUND: the tie covers the 9 post-7/23 dates where both series exist; PRE-7/23 IS UNTESTED. ETFS-CANON may later re-bind THIS ROW ONLY -- zero route change (ratified boundary, rulings F-1). ~~SUPERSEDED 2026-08-07, PRESERVED FOR PROVENANCE (CTO-ruled: strike, never delete -- deleting a false claim removes the evidence it was ever believed, so the next reader cannot tell whether the basis was decided or never considered): "ANDREW-CANONICAL (his 141545Z expansion + 140458Z source map), carried VERBATIM per F-1 ruling / C-1 PRESERVED-BY-BINDING: \'whatever the aua content of the schwab 08242234 account serves\', per-date; SUPERSEDES the fact_rps_s2 envelope as the served custody series."~~ The struck sentence\'s "SUPERSEDES the fact_rps_s2 envelope" clause is the FALSE half -- contradicted by the served artifact the producer itself emits. The backing table `opal-assets-daily-aua` was deleted by Andrew 2026-08-07 ("too late got rid of both and dont care"); the F-1/C-1 citation is retained visible here so an Andrew-named ruling is VISIBLY superseded rather than silently vanishing from the record.'; `firms.49financial.custody_leg.source.type`: served='ddb-cohort' -> committed='s3-monolith-silver'; `firms.49financial.custody_leg.tie[0].expect`: served='opal-assets-daily-aua' -> committed='schwab/08242234/silver'; `firms.49financial.custody_leg.tie[0].symbol`: served='DDB_AUA_TABLE' -> committed='SCHWAB_SILVER'; `firms.49financial.custody_leg.tie[1].kind`: served='const' -> committed='code-literal'

**Last commit touching the committed file:** `f999fb25f6dd5127d06ebb9f23fecaa217352e4e 2026-08-07T16:19:35-04:00 fix(MDPF_REMED.W1-1): repoint the 49F custody binding off the deleted DDB table -- ATOMIC across 4 files, because deleting the constants alone would have MANUFACTURED the outage this TO was chasing`

**Last write of the served object:** `list-object-versions` shows exactly **1** version(s) total (the object was FIRST-MINTED, never re-applied since); LastModified `2026-08-07T00:13:10+00:00`, VersionId `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz`. `cloudtrail lookup-events` on `ResourceName=config/mdpf/route_bindings.yaml`: rc=0, 0 event(s) -- a management-event lookup, not a data-event trail; the object's own version history above is the authoritative 'last write' evidence here.

**Bucket versioning:** `Enabled` (confirmed via `get-bucket-versioning`; rollback below is possible).

**`eol=lf` finding (a `.gitattributes` question, not this order's act):** `git check-attr eol -- data/mdpf/config/route_bindings.yaml` reports `data/mdpf/config/route_bindings.yaml: eol: unspecified` -- no `eol` attribute is set on this file, which is why this Windows box's checkout renders it CRLF and a naive apply from here would upload CRLF bytes. Row, not an edit (BOUNDS).

---

## The consumers (ARM B)

Denominator: **4 of 4** candidate consumers identified and read (comp-estate --resource route_bindings: `ONTOLOGY BOUNDARY: this is a generated C3.ii naming snapshot, not locked C(N). C(N) is RELIES-ON NFRA_C3MATERIALIZE; unresolved C(N) names are CARRIED there, never guessed here.`; comp-pipescript io on the gold consolidator: 0 S3 reads detected; graph-call-manifest.yaml: 0 hits for 'route_bindings'/'config/mdpf').

| consumer | IAM grant | CRLF tolerance | parsed-content-change meaning |
|---|---|---|---|
| mdpf_gold_lambda (deployed mdpf-gold-lambda function, role mdpf-gold-lambda-role) | infra/aws/terraform/mdpf-pipeline/iam.tf:766-769 @8d18193bcc Sid ConfigRouteBind... | N/A -- never reads the S3 object at all (0 GetObject calls o... | nothing today (no read path); if wired to read S3 in future, an untargeted apply... |
| build_mdpf_spine.py (Model-B ad-hoc QA driver, run manually, not deployed) | none named for this script; runs under the operator's own AWS identity when invo... | YES -- text-mode open() + yaml.safe_load tolerate CRLF (Pyth... | not applicable -- never reads the served object. |
| route_bindings_tieout.py (W-1 read-only tie-out validator) | none named; read-only, no AWS calls (docstring: 'Read-only by construction: no S... | YES -- text-mode + yaml.safe_load; reads the LOCAL REPO FILE... | not applicable -- never reads the served object. (Battery re-runs this validator... |
| mdpf-daily-runner EC2 dispatch (mdpf-daily-dispatch.sh, on i-02448edb624a7a7cf) | reads via `aws s3 sync s3://opal-data-mdpf/code/config/ .../config/` -- a DIFFER... | N/A to THIS object -- the runner never reads config/mdpf/rou... | not applicable -- different artifact entirely. |

### mdpf_gold_lambda (deployed mdpf-gold-lambda function, role mdpf-gold-lambda-role)

- **IAM grant:** infra/aws/terraform/mdpf-pipeline/iam.tf:766-769 @8d18193bcc Sid ConfigRouteBindingsRead, s3:GetObject on this exact key -- the ONLY grant in mdpf-pipeline/iam.tf that names config/mdpf/route_bindings.yaml
- **Code reader:** data/mdpf/scripts/gold/mdpf_gold_consolidator.py:304-323 @1465fd3f7d load_bindings() -- reads an adjacent-packaged copy first (os.path.join(_HERE, 'route_bindings.yaml'), bundled into the Lambda zip by infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:158 @ec8206c1b1 FROM THE REPO FILE at build time), repo-relative second; opens 'rb', yaml.safe_load(raw). Docstring, verbatim: 'NEVER an S3-read leg here: the TF-managed S3 object is P2-1's config axis, not this loader's.'
- **CRLF tolerance:** N/A -- never reads the S3 object at all (0 GetObject calls on this key in deployed code); the IAM grant is unexercised. yaml.safe_load in bytes mode WOULD tolerate CRLF if it ever did read S3 bytes (PyYAML treats \r\n as a line break).
- **What the parsed-content change means for it:** nothing today (no read path); if wired to read S3 in future, an untargeted apply would hand it the CURRENT (post-C-1-repoint) bindings instead of the stale pre-repoint ones it is NOT reading now.

### build_mdpf_spine.py (Model-B ad-hoc QA driver, run manually, not deployed)

- **IAM grant:** none named for this script; runs under the operator's own AWS identity when invoked
- **Code reader:** data/mdpf/scripts/gold/build_mdpf_spine.py:53-54,63-65 @bf74d031c1 BINDINGS_PATH = repo-local data/mdpf/config/route_bindings.yaml; load_bindings() opens with encoding='utf-8' (text mode), yaml.safe_load(fh)
- **CRLF tolerance:** YES -- text-mode open() + yaml.safe_load tolerate CRLF (Python universal newlines in text mode, and YAML's own line-break handling); reads the LOCAL REPO FILE, never the S3 object, so this cell's drift does not reach it at all.
- **What the parsed-content change means for it:** not applicable -- never reads the served object.

### route_bindings_tieout.py (W-1 read-only tie-out validator)

- **IAM grant:** none named; read-only, no AWS calls (docstring: 'Read-only by construction: no S3, no writes')
- **Code reader:** data/mdpf/config/route_bindings_tieout.py:31-34,132-134 @8058f55233 BINDINGS = HERE/route_bindings.yaml (repo-local); open(BINDINGS, encoding='utf-8'), yaml.safe_load(fh)
- **CRLF tolerance:** YES -- text-mode + yaml.safe_load; reads the LOCAL REPO FILE only.
- **What the parsed-content change means for it:** not applicable -- never reads the served object. (Battery re-runs this validator live against the committed content as a corroborating instrument; see ARM B output for its own denominator/verdict.)

### mdpf-daily-runner EC2 dispatch (mdpf-daily-dispatch.sh, on i-02448edb624a7a7cf)

- **IAM grant:** reads via `aws s3 sync s3://opal-data-mdpf/code/config/ .../config/` -- a DIFFERENT bucket (opal-data-mdpf) and prefix than the TF-managed object (opal-data-assets/config/mdpf/); its grant, if any, is on that separate key, not this cell's subject
- **Code reader:** infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:130,136-140 @cf838e54d5 -- syncs config/ from a separate 'runner bundle' S3 location distinct from this cell's S3 object; then the chain scripts (yaml-parsing, CRLF-tolerant by the same argument as build_mdpf_spine.py) read the synced local file
- **CRLF tolerance:** N/A to THIS object -- the runner never reads config/mdpf/route_bindings.yaml on opal-data-assets; it reads a same-named file synced from a different bucket/prefix maintained by a separate mint mechanism, out of this cell's scope.
- **What the parsed-content change means for it:** not applicable -- different artifact entirely.

**The live W-1 tie-out re-run** (`route_bindings_tieout.py`, this run): `DENOMINATOR: 34 tie rows checked (code-literal=13, computed=2, computed-expr=1, const=16, const-dict=1, const-tuple=1); 34 TIE / 0 FAIL` -- corroborates that the COMMITTED content is what the live code constants actually agree with today; the served object's custody_leg row would FAIL this same validator (it still names the deleted `DDB_AUA_TABLE` / `opal-assets-daily-aua`, which no longer resolves).

---

## The writers (IAM census, R-44's instrument, adapted for this key)

```
subject: s3:PutObject on arn:aws:s3:::opal-data-assets/config/mdpf/route_bindings.yaml
RESOURCE plane: bucket policy 2 statement(s); allowing a write: 0 []; Deny: 1 ['DenyParquetUnderBronze17a']
IDENTITY plane: 263 principal(s) simulated (256 roles, 7 users); 0 could not be simulated []
  conditioned: 109 with only keys that cannot occur in a s3:PutObject request (decision stands); 4 re-simulated with the request's true context; 2 settled by statement reading (0 Allow statements match the action and key) [('role', 'AWSServiceRoleForAPIGateway'), ('role', 'AWSServiceRoleForECS')]; 0 UNKNOWN []
PRINCIPALS: 3 of 263 may s3:PutObject arn:aws:s3:::opal-data-assets/config/mdpf/route_bindings.yaml:
  user Andrew_Berman
  user Andrew_Berman_Console
  user Opal_Terminal
```

**3 of 263** principals may `s3:PutObject` this key -- the three human/terminal identities (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`); **0** Lambda/EC2/ECS role can write it. Only a `terraform apply` run as one of those three identities is a writer, which is exactly how the object was minted (config_objects.tf).

## The readers-by-IAM-grant (a wider net than the code-level consumers above)

```
subject: s3:GetObject on arn:aws:s3:::opal-data-assets/config/mdpf/route_bindings.yaml
RESOURCE plane: bucket policy 2 statement(s); allowing a write: 1 ['AllowMdpfPortalCloudFrontOACRead']; Deny: 1 ['DenyParquetUnderBronze17a']
IDENTITY plane: 263 principal(s) simulated (256 roles, 7 users); 0 could not be simulated []
  conditioned: 106 with only keys that cannot occur in a s3:GetObject request (decision stands); 4 re-simulated with the request's true context; 2 settled by statement reading (0 Allow statements match the action and key) [('role', 'AWSServiceRoleForAPIGateway'), ('role', 'AWSServiceRoleForECS')]; 0 UNKNOWN []
PRINCIPALS: 6 of 263 may s3:GetObject arn:aws:s3:::opal-data-assets/config/mdpf/route_bindings.yaml:
  role mdpf-gold-lambda-role
  role opal-news-lambda-role
  role partners-lambda-role
  user Andrew_Berman
  user Andrew_Berman_Console
  user Opal_Terminal
```

**6 of 263** principals hold an IAM grant that would allow `s3:GetObject` on this key: the 3 human/terminal identities, `mdpf-gold-lambda-role` (the ONE intentional grant, `Sid ConfigRouteBindingsRead` -- but its code never exercises it, per ARM B above), and TWO INCIDENTAL roles whose grant is not specific to this key: `opal-news-lambda-role` (AWS-managed `AmazonS3ReadOnlyAccess`, account-wide) and `partners-lambda-role` (inline `Sid ReadPartnerBuckets`, `arn:aws:s3:::opal-data-*/*`). Neither's deployed code names `route_bindings` anywhere in this repo (full-corpus search, 0 hits in their lambda directories). **So the practical blast radius of the served bytes today is ZERO code paths** -- the drift is real and the object should be brought current, but no live consumer's behaviour changes today because it changes.

---

## Rollback

The object has exactly **1** version(s) (`list-object-versions`); the current/only version is `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz`. **There is no PRIOR version to roll back to** -- the object was first-minted on 2026-08-07 and has never been re-applied since, so any apply that changes it creates version #2, and rollback of THAT act is `s3api put-object` (or a re-apply) restoring version `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz`'s bytes, OR `s3api delete-object --version-id <new>` to remove the new version and let `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz` become current again (bucket versioning confirmed `Enabled`, so a version delete is non-destructive to the prior version).

---

## The untargeted root's FULL plan (NOT applied)

Vendored `.tools/terraform.exe` v1.9.8, root `init`ed fresh this run. Untargeted `terraform plan` on `infra/aws/terraform/mdpf-pipeline` (sha256 of the plan text `32b52e5df0d4b85f38b220e70017cd8e32aa85214a30ad35ec482799c4311684`):

```
module.mdpf_accrual_trigger.aws_lambda_function.this: Refreshing state... [id=mdpf-accrual-trigger]
aws_iam_role_policy.mdpf_accrual_scheduler: Refreshing state... [id=mdpf-accrual-scheduler-role:invoke-the-accrual-trigger]
aws_iam_role_policy.mdpf_feeder_scheduler: Refreshing state... [id=mdpf-feeder-scheduler-role:invoke-the-feeder-trigger-plus-dlq]
aws_lambda_permission.eventbridge_mdpf_feeder_trigger: Refreshing state... [id=AllowExecutionFromEventBridge]
aws_scheduler_schedule.mdpf_accrual_bridge_daily: Refreshing state... [id=default/mdpf-accrual-bridge-daily]
aws_cloudwatch_event_target.mdpf_feeder_accelerator: Refreshing state... [id=mdpf-feeder-accelerator-MdpfFeederTrigger]
aws_scheduler_schedule.mdpf_feeder_backstop: Refreshing state... [id=default/mdpf-feeder-backstop-daily]
aws_lambda_permission.scheduler_mdpf_accrual_bridge_daily: Refreshing state... [id=SchedulerMdpfAccrualBridgeDaily]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_s3_object.mdpf_route_bindings will be updated in-place
  ~ resource "aws_s3_object" "mdpf_route_bindings" {
        id                            = "config/mdpf/route_bindings.yaml"
      ~ metadata                      = {
          ~ "content-sha256"   = "c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd" -> "37eb845123b155ef8993babdda60d918b119331d9ad83c4b725ca081096e21c2"
            # (1 unchanged element hidden)
        }
      ~ source_hash                   = "56a03a1410848f88b006f1f98b69dced" -> "f94e8e4c5d7c56d93f6ab16af227721d"
        tags                          = {
            "Name"   = "mdpf-route-bindings-config"
            "System" = "MDPFPipeline"
        }
      ~ version_id                    = "iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz" -> (known after apply)
        # (24 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Changes to Outputs:
  ~ mdpf_route_bindings_sha256 = "c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd" -> "37eb845123b155ef8993babdda60d918b119331d9ad83c4b725ca081096e21c2"

─────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't
guarantee to take exactly these actions if you run "terraform apply" now.
```

**Plan: 0 to add, 1 to change, 0 to destroy -- the ONLY drifted resource in the ENTIRE root is `aws_s3_object.mdpf_route_bindings`.** IB-rtc-7's targeted apply (of `aws_iam_role_policy.mdpf_runner` only) correctly left this alone; nothing else in the root has since drifted.

A TARGETED plan of the object alone (full-text sha256 `b55db0ca3f830d2e284bf28fd139708bbc2de1eff518ec4c05445043daf75579`) differs from the untargeted plan's full text (sha256 `32b52e5df0d4b85f38b220e70017cd8e32aa85214a30ad35ec482799c4311684`) ONLY in the `Refreshing state...` preamble (untargeted refreshes every resource tracked in the root's state before planning; targeted refreshes only the target) -- **the substantive `# aws_s3_object.mdpf_route_bindings will be updated in-place` diff block is BYTE-IDENTICAL between the two runs (diff-block sha256 `c30da24307e204a37949ef8d5c67528d94e91f565367105dacdae8daded83aa7` both), confirmed=True**: because this is the only drifted resource, targeted and untargeted currently plan the same act. A targeted apply is still the SAFER choice going forward: it bounds the blast radius by declaration, not by accident of today's drift being singular.

---

## What this packet does not decide

Whether the S3-object mechanism (Phase 2's TF-managed-object design, `config_objects.tf` comment) should gain a real consumer wired to read it, given that its ONE intentional grant-holder (`mdpf-gold-lambda-role`) documents in its own code that it deliberately never reads it. That is a design question for MDPF's owner, not a drift-measurement act.

