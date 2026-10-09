# Never-widen sign-off packet -- the platinum publisher goes on its schedule (IRPT_DASHBD DB-b-8; round-2 analysis E2)

Author `2.0.0_SA_COO~P`, 2026-10-02 ~13:2xZ. Cell: `DB-b-8` (decomposition section 3), the issuer's served act. Halves owed:
`1.0.0_SA_CTO` and `2.0.0_SA_COO~P`. Acceptance (the cell's): on the next trading morning the page reads "Data through" the new T-1
date, and no seat starts either run.

## The act

ONE targeted `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish/` from a saved plan. The plan was read at
~13:0xZ; the root's files are unchanged since dd3d644cd6: **7 to add, 0 to change, 0 to destroy.** It adds:
- the function `irpt-49f-reporting-publish-lambda` (artifact `investor-reporting/irpt-reporting-publish-lambda.zip`, S3 version
  `qnGujQo2HF4N3sAKb.wbB5mIYO9DtCOo`, `source_code_hash` `gZM/pgyLqFICfadTwYF5VkNQDwhoFJbR2YGmjsmbzis=`) and its log group;
- its role and policy: List on the bucket; Get on `gold/account_return_daily/*` and `gold/dim_return_method/*`; Put on
  `platinum/reporting/*` only; its own log group;
- the schedule `cron(15 8 ? * MON-FRI *)`, America/New_York, ENABLED, with its scheduler role and policy.

The S263 policy-selector defect does not reach this root. It selects with `one(distinct(...))` over its own source rows, not over
`reporting_policies.json`, and the plan runs clean. The artifact is DB-b-2's build. Downloaded at that version, it hashes to the
plan's `source_code_hash`. Of its 10 staged pins, 9 equal HEAD. The tenth is `org/standards/NAMING_SCHEMA.json`, and HEAD differs
from it only by the cadence token "1min" (`aa2b5a42ff`), which no platinum address uses.

## Blast radius, by the producer's own rule

**What the act may touch.** The apply writes no data. Each fire, and any manual invoke, writes exactly two keys per account through
the naming builder:
- `s3://opal-data-49financial/irpt/49financial/platinum/reporting/account=<id>/series.json.gz`
- `s3://opal-data-49financial/irpt/49financial/platinum/reporting/account=<id>/manifest.json`

The series is written first. The account set is every `account_id` in the NEWEST gold partition, 6 accounts today. The IAM policy
admits no other write.

**Writers of the property, counted.** ONE rule writes `platinum/reporting/`: `handler.py` + `publisher.py`. It has reached that prefix
through two invocation paths:
1. DB-b-2's QA run, which wrote today's 12 objects at 02:30Z (`built_at` 2026-10-02T02:30:01Z, `publisher_version` 0.1.0,
   `as_of` 2026-09-28);
2. this schedule.
Both run the same code. The manual path of the deployed function is the Lambda event, covered below.

**The outcome, read from the rule at signing.** The publisher lists every gold partition present and rebuilds each account's WHOLE
series from them. It is idempotent and has no date override.
MEASURED on the exact artifact: version `qnGujQo2` was downloaded, its hash matched, and its own `handler.py --local` ran without
`--upload`, writing nothing. It read 562 gold partitions, 2024-07-08..2026-10-01, for 6 accounts: acct#08137b81 (562 days),
acct#89d0916a (138), acct#f08ffd13 (131), acct#6b914f88 (61), acct#ffa615d2 (136) and acct#d0cf6c92 (95).
- **Branch A, the expected one.** The reporting gold's own schedule fires Monday 2026-10-05 at 07:41 ET. It took 20 s today and
  landed 3 days. It lands 2026-10-02, and the 08:15 fire publishes the 6 accounts `as_of` 2026-10-02.
- **Branch B.** If that partition is not there at 08:15, the fire publishes `as_of` 2026-10-01: today's measured run. The next fire
  catches up.
Neither branch moves "Data through" backward. Gold partitions only accumulate and the series is rebuilt whole. An account missing
from the newest partition is not republished, so its old objects stay as they are.
The foreign-tax change deployed today (ledger `irpt-dashbd-foreign-tax-leg-a-20261002`) is output-neutral by its own measurement. It
moves no published value.

**The manual path.** A Lambda invoke can carry `accounts` (a named subset; same two keys per named account, same rule) or `dry_run`
(writes nothing). Neither creates a state the schedule cannot reach. No date or month override exists.

## Rollback, per key

The bucket is versioned (`Enabled`). Each of the 12 live objects has one version, all written 02:30Z by DB-b-2. To roll back, restore
that version: `copy-object` from the version id onto the key.

| key under `platinum/reporting/` | live version (pre-act) |
|---|---|
| account=acct#08137b81/manifest.json | EWsHox5mi6qll4ek.mEpT71YeLHZ81lV |
| account=acct#08137b81/series.json.gz | OSPEMKS19HstKiUS2_5WXXsq654A4ght |
| account=acct#89d0916a/manifest.json | tHJwqXHbhvGZOtcg7P3OyzQYyd1B09jx |
| account=acct#89d0916a/series.json.gz | .5GmBiQ_yH3LAXrn_fNPP9l2t.ObD29E |
| account=acct#f08ffd13/manifest.json | 9FVAKupuTsqLMr5mx2Cxi0pe6fJAqjou |
| account=acct#f08ffd13/series.json.gz | T7pTUtM4jN.shppkZ0p.BeAzM2Kn_Bkh |
| account=acct#6b914f88/manifest.json | oihjnf2njlacAGNQIiEOFWTQXkPFR1Zz |
| account=acct#6b914f88/series.json.gz | KQJh0PDMQBJRoiwFZUSTorWWIKcDTNGW |
| account=acct#ffa615d2/manifest.json | AETUKZdtorpl48WotwXiA_pRQxpUDzDz |
| account=acct#ffa615d2/series.json.gz | n2WBOkrubH_Y6p.Wf3k6Wk0jPvktc.Dr |
| account=acct#d0cf6c92/manifest.json | sv540CJSYROo_KS3kvMOV5jg_IoUdr8u |
| account=acct#d0cf6c92/series.json.gz | GgejpxNBbKQVG1QxT96o47KDM6D2eK8q |

To stop further fires: a targeted destroy of the schedule, or `state = DISABLED` through the same root.

## Ledger and verification

A ledger opens at the apply with these legs:
- P1: plan 7/0/0;
- D1: safe-apply;
- V1: function config, schedule ENABLED, and a re-plan with No changes;
- A1: the first scheduled fire on Monday 2026-10-05 08:15 ET, with no seat starting it. 12 keys are written with `as_of` equal to
  T-1, and the page reads "Data through" that date.
A1 is a genuinely essential wait: the cell's acceptance IS the organic fire. An ad-hoc invoke is permitted for QA, but it would write
the same served keys, so it is not run.

## COO half -- 2.0.0_SA_COO~P

SIGNED, 2026-10-02 ~13:2xZ, on this packet's bytes at the commit that carries it.
- The write set is 12 named keys plus any account that newly appears in the newest gold partition, by one rule.
- Both branches are read from the rule and measured on the exact artifact.
- The writers are counted (one rule, two paths).
- The manual path is covered.
- The rollback is per key with version ids.

## CTO half

OWED.

## AMENDMENT 1 (2026-10-02 ~13:4xZ, 2.0.0_SA_COO~P) -- the read-back permission (row IRPT_DASHBD-S21)

**What happened.** P1, D1 and V1 closed: apply 7/0/0 at 13:32Z, CodeSha256 equal to the artifact, schedule ENABLED, re-plan No
changes. Q1, the CTO's QA invoke at 13:35:40Z, wrote `account=acct#08137b81/{series.json.gz,manifest.json}` (`as_of` 2026-10-01), then
`handler.py:158` called `head_object` on the series key and got 403. The role has PutObject and no GetObject on
`platinum/reporting/*`, so the run aborted after the first account. **Rolled back per the signed half:** each of the two keys was
copied back from its recorded version (`OSPEMKS19...`, `EWsHox5mi...`). The new current versions are `qvtMQgRd...` and `S4JjNhUe...`,
with ETags equal to the 02:30Z versions, and the manifest reads `as_of` 2026-09-28. The other 10 keys never moved.

**The amendment.** `iam.tf` gains one statement, `ReadBackThePlatinumReportingPrefixOnly`: `s3:GetObject` on the same ARNs the role
writes (`platinum/reporting/*`), and nothing wider. Plan at ~13:4xZ: **0 to add, 1 to change (the role policy), 0 to destroy.** The
write set, the keys, the rule, the branches and the rollback above do not change. The role gains read on the prefix it already
writes: platinum series of the same firm, and no other firm's prefix.

**Then:** the targeted apply of the saved plan, then Q1 again: one invoke with no arguments, expecting 12 new versions `as_of`
2026-10-01. Anything else rolls the 12 keys back from the version ids that are current at that moment. **If the amendment is not
applied before Monday 2026-10-05 07:00 ET, the schedule goes DISABLED** (the stop path above), so a fire cannot half-publish.

**COO half on amendment 1:** SIGNED, ~13:4xZ, on these bytes.

**CTO half on amendment 1:** OWED.
