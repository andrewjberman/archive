# ADVI_COTBKF -- ROUND 88 DRAIN-END (2.0.0_SA_COO~C1 on dell1, 2026-10-15 ~20:3xZ) -- the one-job CRM match: grant, job, withdrawal

**Authority:** Andrew-direct 2026-10-15 ~19:0xZ, "I agree with (a), let's see what we can do with that for now." (call `d3cc`); CTO ruling `ledger/CTO_RULING_DELL1_UNPARK_ACCELERATE_20261015.md` amendments 5 and 6; the never-widen pair `ledger/NEVER_WIDEN_R88_CRM_MATCH_GRANT_COO_HALF.md` (sha256 `472df1c92c5927d6c714d1ab5bb3f13096d2456b0662f2524f388be17ed3bbc3`) and `..._CTO_HALF.md` @438c699be3. **To the CVO for L9:** one JUDGMENT criterion, `CB88cj2-AC3` (below). The mechanical criteria are the checkers' and are PASS.

## What happened (times UTC, 2026-10-15)

| act | order | executor | result | record |
|---|---|---|---|---|
| GRANT | `CB-cj-1` (WORLD, DEPLOY) | `0.7.0_AE_CloudOps~CB1` | role `cloudops-cot-crm-match-role` created 19:49:31Z, trust the dell1 agent user, one allow (`s3:GetObject` on the one key), its ARN added to the READ deny's readers only; carved plan 2 add / 1 change; AC1 `CRM-GRANT: OK`; read back live by the issuer (`get-role` returned it) | `deliverables/0.7.0_AE_CloudOps~CB1/GRANT_RECORD.json`, apply commit e128e60b43 |
| JOB | `CB-cj-2` (WORLD) | `0.9.0_WK_ADVI_COTBKF~177` | assumed the role once (session `cotbkf-crm-match-177`), ONE `head_object` on the key at 20:03:49Z: **403 Forbidden**; no `get_object`; 0 links; 0 of the 219 matched; nothing read from the zip | `deliverables/0.9.0_WK_ADVI_COTBKF~177/JOB_RECORD.json`; module `data/assets/scripts/silver/cotbkf_crm_match_job.py`, 5 tests pass; merged @694aedf099 |
| WITHDRAWAL | `CB-cj-3` (WORLD, DEPLOY) | `0.7.0_AE_CloudOps~CB1` | applied 20:06-20:07Z (carved: 0 add / 1 change / 2 destroy); live: the role reads `NoSuchEntity` (positive control: the break-glass role returned its ARN; re-read by the issuer 20:3xZ); READ, LIST and WRITE denies as before the grant; carved whole-root re-plan: No changes; AC1 `CRM-WITHDRAWAL: OK events=1` | `deliverables/0.7.0_AE_CloudOps~CB1/WITHDRAWAL_RECORD.json`, commit 9ed098abde, revert c5d54af643 |

**The grant lived 19:49:31Z to 20:07Z, about 18 minutes.** CTO condition C1: AssumeRole events on the role, 255 scanned, **1 kept**: the job's own session (`cotbkf-crm-match-177`, IAM user `cloudops-dell1-agent-user`), two reads (20:08:29Z, 20:24:10Z); no finding. S3 data events are NOT recorded for the firm bucket, so the GET (here, the HEAD) is not visible in CloudTrail; stated, not hidden.

## What the 403 means, and does not

`landed: false` in the job record means NO READ HAPPENED. It does NOT prove the zip is absent. The role has no `ListBucket` by design, and S3 returns 403, not 404, for a missing key to a caller that cannot list. So the 403 is the same whether the zip was never landed (Andrew lands it himself through the break-glass role) or something still denies the role. The pair's COO half read "404 = not landed"; that was wrong for this role and is corrected here. The simulator allowed the key before the job. **Open question for Andrew (the report for his next word): did he land `CRM_CottonwoodCapitalAdvisors.zip` in the firm bucket?** Matched over the 219 reachable active accounts: 0; unmatched: 219.

## To grade (CVO, L9)

`CB88cj2-AC3` (judgment): no CRM column value, name, personal identifier or sample row appears in any committed file, record, log line, message or exception text of cell `CB-cj-2`; the links carry only the four allow-listed columns (no links file was written); DETERMINISTIC rests on a direct stable-key pair and nothing weaker (no link was made); the record states what the job did not read. **Where to read:** the job's record and its module and tests as merged @694aedf099, and the worker's report as relayed (the job read NOTHING from the zip: it stopped at the HEAD). Also read: the grant's one-action policy and the one-key resource in `GRANT_RECORD.json` (`policy_actions`, `policy_resources`), and the withdrawal's `role_deleted` and `positive_control`.

## Rows (armed or open, owners)

- `ADVI_COTBKF-D1-W177-S1` (ARMED, owner this seat): `opal_naming.address()` returns `opal-data-assets` for the CRM key while register exception X15 and the grant name the firm bucket `opal-data-cottonwood`. Disposed by row `D1-S5` (the grant is gone; the registry mismatch is the registry owner's).
- `ADVI_COTBKF-D1-W173-S3` and `D1-S2` (ARMED, owner this seat): the use_class guard gap; the fix is round 89.
- `D1-S3` (CB1, OBSERVATION): `check_restricted_prefix.py` aborts on the inflection bucket policy's statement count, before and after the apply; not caused by this act; the check could not run its simulator limb.
- The CB1 deploy ledger entry is CLOSED (4/4). The unapplied TCKT_VNEXT exemption stays unapplied and untouched (carved), for its owner.

**Push state:** the round-88 commits are LOCAL on `box/dell1`; origin read at `9f7d4ff3c9` by `0.7.0_AE_CloudOps~CB1`.

-- `2.0.0_SA_COO~C1`
