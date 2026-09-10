# RP-s-5 -- The COMPUTE MANIFEST as a reporting substrate (EC2 + ECS)

**Cell:** `RP-s-5` (manifest row S5, outcome FWD-9) · **Worker:** `0.9.0_WK_NFRA_REPORT~2` · **TO:**
`NFRA_REPORT.TO-RP-s-5.compute-manifest-substrate-ec2-and-ecs.md` · **Worktree HEAD at start:**
`7ea739b7b5` · **Vintage of every live AWS read below:** `2026-09-09T20:10Z` (`aws sts get-caller-identity`
confirms account `313476888478`, principal `arn:aws:iam::313476888478:user/Andrew_Berman`).

**ACT restated:** one record answering "what compute do we run, and what shuts itself down", spanning
BOTH kinds of compute (EC2 and ECS), each unit's duty cycle and autoshutdown state, and the always-on
set named BY GROUP (Dashboard, Website, Graph per Andrew's ruling 15b). PORT verb: `sync-ec2-manifest.sh`
reused, not rebuilt, not edited (it is outside this cell's `<paths>`).

---

## 1. Premises re-grounded against live state, before building anything

The TO carries four measurements from the L1 brief (F8) "rather than re-derived". Each is re-checked here.

| Carried premise | Re-grounded finding |
|---|---|
| 27 declared services | **CONFIRMED.** `infra/aws/ec2/EC2_MANIFEST.json` `.services` has exactly 27 keys. |
| 18 of 27 rows carry a LIFECYCLE WORD (`persistent`\|`transient`\|`ephemeral`) where a MACHINE TYPE belongs | **CONFIRMED EXACTLY.** Enumerated below (s.3a). |
| Two services share an id | **CONFIRMED, AND FURTHER CHARACTERIZED.** `bd-allocations` and `bd-price-runner` both carry `instance_id: i-0800437d1dbb0b5cc`. This is **NOT a data-integrity defect**: `bd-price-runner`'s own `_trigger`/`_replaces` fields (pre-existing in the file) document it as a script co-located on the `bd-allocations` host, invoked at the end of the `opal-bd-allocation-download` SSM sequence (~21:51 UTC weekdays). Confirmed live: the shared id resolves to one running box (`t3.medium`, Name=`bd-allocations`, state `stopped` at read time). |
| The manifest is EC2-ONLY, ECS absent entirely | **CONFIRMED for the manifest file; FALSE for the AWS account.** `aws ecs list-clusters --region us-east-1` returns **1 of 1** live cluster: `opal-globgrph` (ACTIVE, FARGATE, 3 of 3 services running). See s.4 -- this is the single largest finding of this cell. |
| "the manifest is itself 2014.2h old" | **STALE AS A CITATION, NOT AS A DEFECT** -- see s.6 / row `NFRA_REPORT-Z-W2-S3`. The manifest's own `_last_updated` reads `2026-09-09T19:08:11Z`, ~62 minutes before this read (`git log -1` on the file: commit `9f76655b9f`, an `opal-gateway` deploy, landed after the L1 brief's `@37ff80867a` vintage). The brief's number was correct **at its own vintage**; an intervening operational deploy touched the same file before this cell started. Carried as a STATE-axis finding, not acted on (the manifest's freshness does not change this cell's ACT). |

---

## 2. Live EC2 reconciliation (32 of 32 live instances swept, `us-east-1`)

`aws ec2 describe-instances --region us-east-1` (no instance-id filter, so no instance could be silently
excluded by a stale id list) returns **32 of 32 Reservations/Instances**, denominator printed by the
call itself (`length(Reservations[])` cross-checked separately in `us-east-2` and `us-west-2`: **0 of 0**
in each, consistent with every reviewed script/terraform file in this repo hardcoding
`REGION=us-east-1`; a full 17-commercial-region sweep was **not** performed -- 3 of ~17 regions checked,
denominator stated, not hidden).

- **25 of 27** declared rows carried a non-null `instance_id` before this cell's edit (2 null: `bd-exporter`,
  `bd-gold-detail-generator`); those 25 values covered **24 of 25** distinct ids (the by-design duplicate
  above).
- Of those 24 unique declared ids, **22 of 24** resolved to a live instance; **2 of 24** did not
  (`InvalidInstanceID.NotFound`): `orion-crawl-harness` (`i-010f195f1798b40ad`) and `estate-report-runner`
  (`i-0512bd3cbaf602b7f`).
- **10 of 32** live instances were not referenced by any manifest row at all.

**This cell's edit to `EC2_MANIFEST.json` resolved 2 of those 10, by live Name-tag lookup (the same
method `sync-ec2-manifest.sh` already uses):**
- `bd-gold-detail-generator` had never carried an `instance_id`; the live sweep found exactly one instance
  named `bd-gold-detail-generator` (`i-074bfc40ee049dc62`, `r6i.xlarge`, stopped) -- backfilled.
- `estate-report-runner`'s recorded id (`i-0512bd3cbaf602b7f`) does not exist live. This row **already
  carries its own documented id-churn history** (`_instance_id_note` 2026-08-04, `_instance_id_churn_2026-08-25`
  -- three prior corrections, by design: `user_data_replace_on_change=true` on this Terraform resource means
  every `user_data` edit replaces the instance). This is the **fourth** churn, undetected until this
  re-grounding, because (per the row's own `_deployed_record_note`) "nothing reads instance_id back
  against TF." Corrected here to the live match `i-0584e17d283fa7ef4` (`t3.medium`, stopped), with a new
  `_instance_id_churn_2026-09-09` note continuing the row's own established pattern. **Not** re-derived
  from the Terraform output `estate_report_runner_instance_id` (out of this cell's scope) -- the row's own
  note instructs a future sync to re-verify against TF, which still applies.

**8 of 32 live instances remain undeclared, carried as a finding (not fabricated into rows -- no evidence
tells which one, if any, is the "canonical" box for its name):**

| Name tag | Extra live instance ids (not in any manifest row) | Count |
|---|---|---|
| `historical-prices-fetcher` | `i-0416edf7e4b901380`, `i-094c504a4384f9c47`, `i-025cba31603a6c8a6`, `i-032fa1babe1abe48a`, `i-0ec91038b9a2c73a6`, `i-088e7fa9323bac1b9`, `i-03c397afaa967d978` | 7 |
| `seeking-alpha-scraper` | `i-07ebae29a16e43ed1` | 1 |

All 8 are `stopped`. The manifest's own note on `historical-prices-fetcher` ("Managed by
historical-prices-scheduler Lambda. Starts on daily schedule, runs yfinance fetch, stops.") is consistent
with a scheduler that **launches a fresh instance per run** rather than starting a fixed one -- 8 distinct
ids under one Name tag, all stopped, is the shape that mechanism would produce. This is exactly the kind
of box-grain fact `RP-s-9`'s cost-anomaly detector (conditioned on this cell, PRD `D3`) needs and could not
see before this cell landed. Not resolved further here -- filed as row `NFRA_REPORT-Z-W2-S1` (s.6).

---

## 3. The schema fix: separating MACHINE TYPE from LIFECYCLE

`infra/aws/ec2/EC2_MANIFEST.json` bumped `_schema_version` `1.0` -> `1.1`. **`instance_type` itself is left
UNCHANGED on every row** -- `sync-ec2-manifest.sh` (outside this cell's `<paths>`, PORT-not-rebuild) selects
which services to sync with `select(.value.instance_type == "persistent")`; overwriting that field with a
real machine type on the 18 conflated rows would silently drop them out of the sync loop's coverage
forever (this is, in fact, the mechanism that appears to have orphaned `estate-report-runner`'s id -- see
s.2 -- once its `instance_type` held a real machine class instead of a lifecycle word, it left the set
`sync-ec2-manifest.sh` ever looks at). Both new fields below are **additive**.

### 3a. `machine_type` added to the 18 of 27 rows that carried a lifecycle word

Backfilled by live `describe-instances` (Name/id match), `2026-09-09T20:10Z`:

| Service | `instance_type` (unchanged) | `machine_type` (new) |
|---|---|---|
| orion-crawl-harness | transient | **UNRESOLVED** -- declared id not live, no live replacement found |
| astn-wsjft-scraper | transient | t3.medium |
| bd-49f-auto-login | transient | t3.medium |
| etfs-reports-reporter | transient | t3.medium |
| smartx-exporter | persistent | t3.small |
| seeking-alpha-scraper | persistent | t3.medium |
| bd-gold-layer-runner | persistent | r6i.4xlarge |
| bd-gold-qa-runner | persistent | c6i.16xlarge (cross-checked against the row's own pre-existing `_deploy_note`, "same instance type as production (c6i.16xlarge)" -- agrees) |
| bd-exporter | persistent | **UNRESOLVED** -- no id ever recorded, no live instance named `bd-exporter` found |
| bd-allocations | persistent | t3.medium |
| bd-transactions | persistent | t3.medium |
| bd-fees | persistent | t3.medium |
| bd-assets | persistent | t3.medium |
| bd-price-runner | persistent | t3.medium (co-located box, see s.1) |
| bd-gold-detail-generator | ephemeral | r6i.xlarge (newly resolved, s.2) |
| historical-prices-fetcher | ephemeral | t3.xlarge |
| opal-gateway | persistent | t4g.nano |
| opal-website-wp | persistent | t3.small |

**18 of 18** conflated rows now carry an explicit `machine_type`; **16 of 18** resolved to a real value,
**2 of 18** (`orion-crawl-harness`, `bd-exporter`) are recorded `UNRESOLVED` rather than guessed.

### 3b. `lifecycle` added to the 9 of 27 rows that carried a machine type but no lifecycle information

These 9 rows (`consolidation-gold-runner`, `inf-gold-layer-runner`, `inf-gold-qa-runner`, `inf-exporter`,
`inf-bronze-runner`, `mdpf-daily-runner`, `canonical-schwab-si2`, `cot-exporter`, `estate-report-runner`)
already carry a real EC2 instance type in `instance_type`, but **none of the other 8** had ever been given
a lifecycle classification -- the inverse of the 18-row defect. `estate-report-runner` is the **one
exception and the precedent this fix follows**: it already carries a free-text `lifecycle` field
("TRANSIENT -- STOPPED between runs... NOT always-on; NOT exempt from the auto-shutdown enforcer"),
so the fix below **extends that existing convention to the other 8** rather than inventing a new shape
(build-ladder rung 2).

| Service | Live state (2026-09-09T20:10Z) | `lifecycle` (new, or pre-existing for estate-report-runner) | Evidence |
|---|---|---|---|
| consolidation-gold-runner | stopped | SCHEDULED-BURST, currently DISABLED | row's own `duty_cycle`/`autoshutdown` fields |
| inf-gold-layer-runner | **running** | TRIGGERED, not always-on | `infra/aws/terraform/inf-pipeline/inf-assets-trigger.tf`: "Starts inf-gold-layer-runner EC2 (if stopped) then dispatches" |
| inf-gold-qa-runner | stopped | ON-DEMAND, not always-on | row's own `notes`: "Manual SSM dispatch only" |
| inf-exporter | stopped | TRIGGERED, not always-on | `infra/aws/terraform/inf-pipeline/ssm-inf-exporter.tf`, `ssm-inf-jwt-fetch.tf` |
| inf-bronze-runner | stopped | SCHEDULED, not always-on | row's own `cron_schedule`: daily 08:30 ET |
| mdpf-daily-runner | stopped | EVENT-DRIVEN, not always-on | row's own `cron_schedule`/`notes`: S3-sentinel trigger, self-stops |
| canonical-schwab-si2 | **running** | **PERSISTENT / ALWAYS-ON** | row's own `instance_type_class`: "persistent"; `managed_by`: "not TF lifecycle-managed" -- a continuously-running Windows box with internal Scheduled Tasks, not an EC2 start/stop cycle |
| cot-exporter | stopped | SCHEDULED, not always-on | row's own `purpose`: "Stopped between runs... cron(0 2) chain" |
| estate-report-runner | stopped | TRANSIENT (pre-existing, unchanged) | row's own `lifecycle` field, the precedent for this whole fix |

**9 of 9** rows now carry a lifecycle classification; **8 of 9** newly added, **1 of 9** pre-existing and
left untouched. **One of the 9, `canonical-schwab-si2`, is ALWAYS-ON** and is carried into s.5 alongside
`opal-gateway` as a box the Dashboard/Website/Graph naming scheme does not capture.

---

## 4. ECS enumeration -- the manifest's other blind spot, and what it resolves

`aws ecs list-clusters --region us-east-1` -> **1 of 1** cluster: `opal-globgrph` (ACTIVE, capacity
provider FARGATE). `describe-clusters`: `runningTasksCount: 3`, `activeServicesCount: 3`. `list-services`
-> **3 of 3**: `globgrph-nessie`, `globgrph-trino`, `globgrph-serving`. `describe-services` on all three:
`desiredCount: 1`, `runningCount: 1`, `launchType: FARGATE`, `status: ACTIVE` for each, created
`2026-06-09`, `2026-06-29` and `2026-09-03` respectively. `aws application-autoscaling
describe-scheduled-actions --service-namespace ecs` -> **0 of 0** scheduled actions anywhere in the
account. **No autoshutdown mechanism exists for any of the 3 services -- they are ALWAYS-ON by the
absence of a schedule**, not by an explicit flag (there is no ECS equivalent of `AutoShutdown=false` in
this account; the absence of a scheduled-scaling action is the evidence).

**This directly resolves ruling 15b's own open sub-item.** The ruling states: *"no graph-ops box appears
in the 27-service manifest, and the security sweep reports 7 unused `opal-globgrph-*` security groups...
The Graph group may therefore be EMPTY."* That reasoning was sound over its own evidence (an EC2-only
manifest cannot see ECS), but the conclusion is **false**: `opal-globgrph` is a live, ACTIVE, 3-service
Fargate cluster. **The Graph group is NOT empty.** `EC2_MANIFEST.json`'s new `ecs_clusters.opal-globgrph`
section carries this with `always_on_group: "Graph"` on each of the 3 services.

### 4a. The open naming question this does NOT resolve: "Gateway" vs "Graph"

Andrew's own verbatim words (batch 6, `ANDREW_DIRECT_20260909_1458Z_INFRA_REPORT_FIVE_RULINGS.md:313,365`):
*"should be named separately id say by group (Dashboard, Website, Graph)."* This TO's own text quotes the
same three names. But **two other canonical artifacts of this same project independently render the third
name as "Gateway", not "Graph"**:

- `org/missions/D12/NFRA/NFRA_REPORT/prd/NFRA_REPORT_PRD.md` s.6: *"the three properties are Dashboard...
  Website, **Gateway** (the opal-gateway MCP server)."*
- `org/projects/NFRA_REPORT.json` (the registered project record, `generated_at: 2026-09-09T19:35:31Z`):
  *"...across three properties (Dashboard, Website, **Gateway**)."*

These are **not the same referent**. "Gateway" (per the PRD's own parenthetical) means the `opal-gateway`
EC2 box (`t4g.nano`, confirmed running live, systemd `opal-gateway.service` behind an ALB). "Graph" (per
ruling 15b's own surrounding text, which discusses "graph-ops box" and "`opal-globgrph-*` security
groups") means the graph-database infrastructure -- now confirmed to be the `opal-globgrph` ECS cluster
found in s.4. **Both are real, both are plausibly always-on, and they are different compute.** This looks
like a downstream paraphrase (PRD, project register) silently "correcting" Andrew's verbatim word into a
name the authors already recognized (`opal-gateway`), while the ruling's own interpretive prose -- and now
this cell's live ECS finding -- confirms the verbatim word meant something else. **Filed as row
`NFRA_REPORT-Z-W2-S2` (s.6); not resolved here** -- this cell's bounds say the always-on set is named
BY GROUP per ruling 15b, and this cell follows that literally (Dashboard/Website/Graph) in s.5, while
flagging that `opal-gateway` -- a real, running, persistent EC2 box -- does not fit any of the three
literal names under that reading.

---

## 5. The always-on set, named BY GROUP (Andrew's ruling 15b)

| Group | Compute | Kind | Evidence |
|---|---|---|---|
| **Website** | `opal-website-wp` | EC2 (`t3.small`) | row's own `_status`: `AutoShutdown=false (exempt from the auto-shutdown reaper)` -- explicit |
| **Graph** | `globgrph-nessie`, `globgrph-trino`, `globgrph-serving` | ECS Fargate (3 services, 1 cluster) | s.4 -- no schedule, `desiredCount` fixed at 1 since each service's creation |
| **Dashboard** | *(none found)* | -- | "the entire serverless system feeding opalinvest.dev" (PRD s.6) is serverless (Lambda/API Gateway/CloudFront-class), which has no EC2 or ECS unit to be "always-on" in this cell's sense -- **empty by construction, not a gap.** Out of this cell's EC2/ECS enumeration scope by definition. |
| **NOT NAMED BY ANY OF THE THREE, CARRIED OPEN** | `opal-gateway` (EC2, `t4g.nano`, running, systemd-managed behind an ALB, no explicit stop path found in its own extensive `_status` history) and `canonical-schwab-si2` (EC2, `t3.large`, running, `instance_type_class: persistent`, "not TF lifecycle-managed") | EC2 | Both are real, currently-running, apparently-standing boxes that the literal Dashboard/Website/Graph vocabulary does not capture. `opal-gateway` is the direct casualty of the Gateway-vs-Graph naming split in s.4a. `canonical-schwab-si2` is a separate, independent gap: it is a Schwab raw-ingestion box, not a website, not the graph DB, and not part of a "serverless system feeding opalinvest.dev." |

Per this cell's own BOUNDS ("An empty group is a legitimate finding -- record it, do not manufacture a
member"), the Graph and Dashboard rows above are recorded as measured, not inferred, and the two ungrouped
boxes are carried open rather than force-fit into a name that does not describe them. **This is the
substance of judgment criterion AC6** and is left for `3.0.0_SA_CVO~Z` at L9.

---

## 6. Surprises filed (`org/missions/D12/NFRA/NFRA_REPORT/surprise-channel/investigations/INVESTIGATION_v1.md`)

- **`NFRA_REPORT-Z-W2-S1`** -- live EC2 fleet (32 instances) exceeds the declared manifest (27 rows) by
  10 undeclared instances (8 remain undeclared after this cell's two backfills); the manifest undercounts
  live compute. OBSERVATION, INERT.
- **`NFRA_REPORT-Z-W2-S2`** -- the PRD (s.6) and the registered project record (`org/projects/NFRA_REPORT.json`)
  both name the third always-on property "Gateway", while Andrew's own verbatim ruling 15b and this TO
  name it "Graph" -- two different real compute surfaces, only one of which (`opal-globgrph`, ECS) this
  cell's enumeration confirms live. OBSERVATION, ARMED (a future reader building the always-on report off
  the PRD's "Gateway" wording would silently drop the Graph/globgrph ECS cluster this cell just found, or
  vice-versa) -- disarm owner `1.0.0_SA_CTO~Z` (governs the PRD text) at L9/L10.
- **`NFRA_REPORT-Z-W2-S3`** -- the TO's carried premise "the manifest is itself 2014.2h old" (from L1 brief
  `@37ff80867a`) is stale as of this cell's re-grounding: the manifest's own `_last_updated` reads
  `2026-09-09T19:08:11Z`, ~62 minutes before this read, because an intervening `opal-gateway` deploy
  (commit `9f76655b9f`) touched the file after the brief's vintage. OBSERVATION, INERT (does not change
  this cell's ACT).

---

## 7. Declared exclusions

- **Editing `sync-ec2-manifest.sh`** to select on the new `lifecycle` field instead of the literal string
  `"persistent"` in `instance_type` -- the script is not in this cell's `<paths>`; the schema fix is
  additive specifically so the script's existing (if narrow) coverage is not broken by this cell.
- **Resolving which of the 8 undeclared `historical-prices-fetcher`/`seeking-alpha-scraper` instances (if
  any) is canonical**, or terminating any of them -- no evidence names a canonical one; recorded as a
  finding (s.2, row S1), not remediated.
- **Resolving the Gateway-vs-Graph naming split** (s.4a) -- carried open per this cell's own BOUNDS
  ("OPEN SUB-ITEM, carried not resolved"); filed as row S2 for CTO/CVO disposition.
- **Any alarm, monitor or notification** -- this cell's BOUNDS explicitly forbid it; none created.
- **Any IAM grant** -- every AWS call in this cell was a read (`describe-instances`, `list-clusters`,
  `describe-clusters`, `list-services`, `describe-services`, `describe-scheduled-actions`) under the
  existing operator credential; nothing was created, changed, or required.
