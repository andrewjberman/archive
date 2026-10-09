# RERUN_COMPARISON -- round 4 permission-cold run beside round 3

Produced by 0.9.0_WK_NFRA_IAMROLES202609~11 for NFRA_IAMROLES202609.TO-IAM-u-2. Every figure below is printed
by `compare-runs.py` over two committed bundles (no cloud call); the "why" column is from reading the two
bundles' rows and the run's own `list-roles.json` (CreateDate), and says "not determinable" where it is.

- Run A (round 3): `deliverables/0.9.0_WK_NFRA_IAMROLES202609~8/permission-cold-raw-bundle.json`, run_date_utc 2026-09-10.
- Run B (round 4): `deliverables/0.9.0_WK_NFRA_IAMROLES202609~11/permission-cold-raw-bundle.round4.json`, run_date_utc 2026-10-09.
- `COMPARABLE: yes` -- lookback_days 90 and 90, population_rule equal (service-linked count masked, 10 and 10),
  instrument_blobs equal (`.tools/comp-iam-usage` 5c7f03ba37..., `org/modules/graph/comp_iam_usage.py` 8670fc5025...).
  Same instrument bytes, same rule, same lookback: a difference is the ESTATE or the CALENDAR, not the method.
- 29 days apart (2026-09-10 -> 2026-10-09).

## 1. The population change, named

| | Round 3 | Round 4 |
|---|---|---|
| roles at Path "/" (the population) | 219 | **280** |
| service-linked roles at /aws-service-role/ (excluded, named) | 10 | 10 |
| `list-roles` total | 229 | 290 |
| attempted / returned rc0 / in results | 219 / 219 / 219 | 280 / 280 / 280 |
| rc != 0 roles (counted apart, never read as clean) | none | none |

- INTERSECTION roles=219: every round-3 role is still present. ROLES REMOVED = 0. ROLES ADDED = **61**
  (219 + 61 = 280).
- The figure of record for this run is the run's own `list-roles` read: 280 (+10 service-linked = 290). The live
  role graph read 283 IAM_ROLE nodes on 2026-10-09 (graph vintage 03:31Z, a different instrument that also
  counts service-linked roles). 283 vs 290 is NOT reconciled here: the graph is an earlier snapshot and a
  different population rule; this report does not explain the 7.
- The 61 added roles: CreateDate in `list-roles.json` runs 2026-09-10 to 2026-10-06; 55 of 61 were created
  after 2026-09-10. The other 6 (`irpt-core-firm-49financial`, `-cottonwood`, `-inflection`, `irpt-core-quarantine`,
  `irpt-directory-role`, `irpt-performance-adapter-role`) are dated 2026-09-10 itself, the day round 3 ran, so they
  appeared after round 3's `list-roles` read the same day (the creation time of day was not compared). Name
  families: irpt 32, gateway 5, mdpf 4, amgt 3, etfs 3, rivalfunds 3, opal 3, firmsep 2, teams 2, and one each of
  cot, daily, mcportal, outlook. Named in full in the compare output ("ROLES ADDED").

## 2. What moved, by how much

Totals (granted permissions = used + never-used + unobservable):

| | granted | used | never-used | unobservable |
|---|---|---|---|---|
| Round 3, 219 roles | 5494 | 421 | 1437 | 3636 |
| Round 4, 280 roles (all) | 5994 | 479 | 1486 | 4029 |
| Round 4, intersection (219 roles) | 5609 | 402 | 1448 | 3759 |

Reconciliation of the +500 on all roles (5994 - 5494):

- +385 granted from the 61 added roles: used 77, never-used 38, unobservable 270.
- +115 granted on the 219 shared roles: used -19, never-used +11, unobservable +123.

Observable share (used + never-used, over granted): round 3 1858 of 5494 = 33.8 percent; round 4 1965 of 5994
= 32.8 percent (intersection 1850 of 5609 = 33.0 percent). Used over observable: 421 of 1858 = 22.7 percent ->
479 of 1965 = 24.4 percent (intersection 402 of 1850 = 21.7 percent). The unobservable two-thirds did not shrink:
66.2 percent -> 67.2 percent (intersection 67.0 percent).

## 3. Transitions on the 219 shared roles, with the why

5328 permission rows are unchanged. 25 of 219 roles changed at all; 194 are identical. 166 row changes in total:

| transition | count | why |
|---|---|---|
| (absent) -> unobservable | 97 | **Grant added.** The permission was not granted in round 3 and is now. 82 are on `opal-drift-producer-codebuild-role`, 7 on `opal-gateway-role`, and 8 across `advi-49f-gold-dispatch-role` (2), `cot-exporter-ec2-role` (2), `cot-satellites-registry-producer-role` (2), `inf-ec2-launch-monitor-lambda-role` (1), `opalinvest-auth-lambda-role` (1). The rows carry reason "service 's3' / 'dynamodb' has no action-level tracking in Access Advisor", so a new grant on those services lands unobservable by construction. WHAT added the grant (a Terraform apply, a console edit) is not determinable from these bundles. |
| used -> never-used | 23 | **Aging out of the 90-day window, not a change in behaviour.** In all 23 the `last_used` date is identical in both runs (e.g. 2026-06-12 for `codebuild-semantic-clustering-role` ecr:*, 6 rows; 2026-07-02 for `agentbus-sim01-fleet-alpha/beta-role` kms:*, 4 rows) and `age_days` grew by the 28 to 29 days between runs, crossing 90 (reason now "last use is Nd ago, outside the 90d lookback"). 13 of the 23 are a single `logs:CreateLogGroup`, `logs:CreateLogStream` or `secretsmanager:GetSecretValue` row on its own role. |
| never-used -> unobservable | 26 | **Instrument-side change in what Access Advisor returns, one role.** All 26 are `opal-drift-producer-codebuild-role` iotevents:* and evidently:* actions; round 3 read them never-used, round 4 reads "service not present in Access Advisor response". The grant is unchanged (the permission is in both runs); the Advisor response for that role no longer lists those services. The cause inside AWS is not determinable here; the instrument is byte-identical. |
| (absent) -> never-used | 16 | **Grant added**, `opal-drift-producer-codebuild-role` only (directconnect, appconfig, inspector2 read actions); Advisor lists the service, no use recorded. |
| (absent) -> used | 2 | **Grant added and already used**: `sts:AssumeRole` on `mdpf-daily-runner-ec2-role` and `mdpf-gold-lambda-role`, last used 2026-10-08. |
| never-used -> used | 2 | **Newly exercised**: `opal-gateway-role` sts:AssumeRole (last used 2026-10-09) and `opal-globgrph-derive-runner-execution` ecr:BatchCheckLayerAvailability (last used 2026-09-29). |

No transition is a grant removed: `-revoked` is 0 on every role. The single largest mover is
`opal-drift-producer-codebuild-role`: 125 of the 166 row changes (+98 granted: 82 + 16, and 26 + 1 re-read
rows), a codebuild role; round 3's posture rollup reports a TOTALS-EXCL-CODEBUILD line that sets the codebuild role out
of the headline (granted 5494 -> 2576). The next, `opal-gateway-role`, has 8 changes (7 added grants, 1 newly used).

## 4. What this does and does not say

- The 23 used -> never-used rows are a calendar effect and will recur every quarter: a permission used once in
  months 3 to 4 reads "used" or "never-used" depending only on the run date. A reader who treats them as
  "the permission fell out of use" over-reads them; the last-use date did not move.
- The 61 added roles carry 385 granted permissions of which 270 (70 percent) are unobservable, S3 (115 rows) and DynamoDB (63) the
  largest reasons, services Access Advisor does not track per action. Population growth, not a posture change, is why the
  unobservable absolute count rose by 393 (3636 -> 4029).
- Naming an unused permission is not removing it. Nothing in AWS was changed by this run; no Access Analyzer was
  called.
- To repeat next quarter, by hand from the checkout:
  `bash org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.9.0_WK_NFRA_IAMROLES202609~11/rerun-population.sh --dry-run`
  (reads the plan), then the same script with `--out <bundle.json> --workdir <dir>` in chunks (`--offset N
  --limit M`; a finished role is skipped on resume; about 5 s per role), then
  `python .../compare-runs.py <this-bundle.json> <next-bundle.json>`.
  This run took 280 roles at 0 failures; the first 65 were done in an earlier sitting and resumed from the
  workdir.
