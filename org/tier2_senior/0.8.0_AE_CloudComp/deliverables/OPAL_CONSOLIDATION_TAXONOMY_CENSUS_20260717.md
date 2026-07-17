# OPAL_CONSOLIDATION Taxonomy CONFORMANCE CENSUS (v0.1)

**Author:** 0.8.0_AE_CloudComp~C, 2026-07-17 ~18:1xZ. **TO:** OPAL_CONSOLIDATION.P3-CENSUS
(issued 2.0.0_SA_COO; Andrew-ratified standing allocation, CTO relay 171739Z).
**Measured against:** `docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md` **@HEAD `cf4938c07`**
(v0.1 + the 3-row SS-D amendment: scheduler naming / absence-twin / telemetry-at-provision, landed
this hour on this census's own cite-a-clause mandate find). Every census column below cites a standard
clause; no measured-but-unstandardized column exists (mandate Phase-1 step 2 satisfied).
**READ-ONLY. Zero remediation. Zero writes to any measured resource. Zero opal-data-schwab live calls**
(WP8 D4 zero-reader window LIVE through 2026-07-24T17:21:29Z; 0.5.0 window-owner ruled STAY-OUT
20260717T175310Z — schwab rows carry pre-window measured evidence per that ruling).

**Location note:** the TO's directed output path `docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_CENSUS.md`
is CTO-lane-owned by the `owned-paths` pre-commit gate (`lane=ANY_CTO`, architecture docs); an AE lane
cannot land there. This census is committed to the ~C deliverables lane and the canonical placement
(alongside the STANDARD) is requested of CTO — surfaced, not forced.
**Companion column:** base session's `DECOMMISSION_TOOLING_ASSESSMENT_20260717.md` (`@61a3efdcc`) supplies
the "unused-by-heat" column that pairs with this doc's "deviation-from-standard" column (CTO's
two-columns-of-one-resource-table frame). Phase-1 enumeration below is the shared groundwork (built once,
consumed by both). Base note: S3/DDB/EC2 have NO heat coverage today (comp-debris is Lambda-only), so an
"unused" verdict for the monolith surface would need CloudTrail/last-modified, not an existing tool.

## Method & evidence grades

One row per (resource, axis). Verdict ∈ CONFORM / CONFORM-AS-LEGACY / CONFORM-BY-AMENDMENT / DEVIATE /
CANDIDATE (deviation suspected, one sub-fact unverified — named as such, never laundered to CONFORM).
Every DEVIATE row NAMES the deviation exactly (quotable into a gate spec) + cites evidence.

| Grade | Meaning |
|---|---|
| `LIVE-20260717` | my own live `aws`/comp read this session (~18:0x–18:1xZ), APPLIED truth |
| `GRAPH@8829022918628754404` | comp-kuzu canonical DB, built 2026-07-17T18:06:54Z, Nessie HEAD current (age 0.0h) |
| `MEASURED-20260716-PREWINDOW` | opal-data-schwab structure measured by 0.5.0 pre-window (commits `ee59022d1`, `2be42054a`); cited per the D4 window-owner's ruling — stronger than TF DESIRED, zero live calls |
| `TF-DESIRED@<path>` | Terraform source = DESIRED (cannot tell landed from planned; flagged where it matters) |

**Denominators enumerated at run time** (verification law 6 — a census whose denominator is not
enumerated is the axis-error class):

| Axis | Standard clause | N enumerated | Enumeration source |
|---|---|---|---|
| A — bucket + prefix grammar | SS-A | 8 buckets + 5 monolith grammar-substructure rows | GRAPH (38 buckets total → 8 consolidation-associated) + LIVE key-sample (4,000 keys of opal-data-assets) |
| B — repo `data/` tree | SS-B | 3 tree rows | `find data/ -maxdepth 4` |
| C — EC2 runner structure + specs | SS-C | 4 runners | GRAPH (33 EC2 total → 4 consolidation-associated) + `describe-instances` |
| D — implementation patterns | SS-D (8 canon rows incl. 3 amended) | 24 schedule/rule names + 11 scheduled producers + 5 pattern rows | `scheduler list-schedules` + `events list-rules` + TF |
| E — device OS + IAM | SS-E | 4 OS + 32 IAM roles | `describe-instances`/`describe-images` + GRAPH IAM_ROLE |

---

## Axis A — Bucket structure + prefix grammar (SS-A)

Grammar law (SS-A): `s3://opal-data-assets/{source}/{scope}/{layer}/{type|feed}/{date}`, `{layer} ∈
bronze|silver|gold|meta`; legacy per-pipeline buckets are MIGRATION SOURCES/serving surfaces, not
templates; telemetry buckets dedicated + named for subject+lifecycle, never in a data bucket.

### A.1 — Buckets

| Resource | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| `opal-data-assets` (monolith) | **CONFORM** (reference) | — canonical grammar paths present (`orion/inflection/bronze/assets/2020-04-28.jsonl.gz` = source/scope/layer/type/date); us-east-1; PAB+SSE+versioning+lifecycle+policy all present | LIVE-20260717 (4k-key sample) + TF-DESIRED@`infra/aws/terraform/opal-assets/main.tf` |
| `opal-schwab-d4-access-logs-313476888478` (telemetry) | **CONFORM-BY-AMENDMENT** (SS-A telemetry clause) | — dedicated, named `{subject=schwab-d4-access-logs}-{acct}`, dies with D4 phase; PAB all-4-true; never in a data bucket | LIVE-20260717 `get-public-access-block` → `{Block/Ignore/Restrict/BlockPolicy=true}`; us-east-2 |
| `opal-data-schwab` (migration source) | **CONFORM-AS-LEGACY** (SS-A legacy clause) | — legacy per-pipeline bucket, migration source; not held to monolith grammar; us-east-2 | MEASURED-20260716-PREWINDOW (`ee59022d1`: 38,392 obj / 12 prefixes; `2be42054a`: 01_raw 7,222 obj / 195.21GB) |
| `opal-data-bd` (migration source / bd serving) | **CONFORM-AS-LEGACY** | — legacy per-pipeline bucket; us-east-1 | GRAPH + LIVE-20260717 region |
| `opal-data-cot` (migration source) | **CONFORM-AS-LEGACY** | — legacy per-pipeline bucket; firm-separated from bd (never mirrored); us-east-1 | GRAPH + LIVE-20260717 region |
| `opal-data-inf` (migration source) | **CONFORM-AS-LEGACY** | — legacy per-pipeline bucket; us-east-1 | GRAPH + LIVE-20260717 region |
| `opal-data-etfs` (ETF feeder source) | **CONFORM-AS-LEGACY** | — legacy per-pipeline bucket | GRAPH |
| `opal-data-smartx-v2` (smartx feeder source) | **CONFORM-AS-LEGACY** | — legacy per-pipeline bucket | GRAPH |

### A.2 — Monolith intra-bucket grammar (opal-data-assets sub-structure)

The reference bucket is CONFORM at the canonical path, but the key-space carries five NAMED grammar
deviations — each quotable into a prefix-lint gate:

| Sub-structure | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| `code/consolidation-gold/*` root | **DEVIATE** | non-grammar root `code/` — EC2 runner shell scripts (`run-gold.sh`, `setup-instance.sh`, `watchdog-shutdown.sh`) stored in the DATA monolith; root token is not a `{source}` and payload is code, not a `{layer}`. A dedicated `opal-runner-shared` bucket exists for runner code. | LIVE-20260717 (3 keys under `code/`) |
| `blackdiamond/49f/_ops/*` | **DEVIATE** | non-canonical layer token `_ops` in the `{layer}` slot (`_ops ∉ {bronze,silver,gold,meta}`); carries `probe/*.json` + `pull_state.json` operational artifacts the grammar routes to `meta/`. | LIVE-20260717 (5 keys) |
| `_probe/{source}/{scope}/{layer}/{type}/{date}/grammar.probe` root | **DEVIATE** | grammar-validation probe scaffolding under a non-source `_probe/` root (22 objects); likely intentional test scaffolding but unstandardized — no SS-A clause blesses a `_probe/` root. | LIVE-20260717 (22 keys) |
| eclipse bronze `{layer}/{date}/...` | **DEVIATE** | eclipse OMITS the `{type|feed}` grammar segment: partitions `eclipse/inflection/bronze/2026-05-15/model_composition_NN.json` (date directly under layer, type encoded in filename), whereas orion carries `bronze/assets/{date}.gz` and blackdiamond `bronze/{type}/{date}/data.xlsx`. Per-feed grammar drift within one layer. | LIVE-20260717 (side-by-side key samples) |
| inline `.../{date}/_meta/pull_complete.json` | **DEVIATE** | pull-provenance written INLINE at `{source}/{scope}/{layer}/{type}/{date}/_meta/` (eclipse + blackdiamond) rather than the SS-D-canonical `meta/pulls/{YYYYMMDD}/`. Cross-references SS-D "Pull provenance" row. | LIVE-20260717 |

---

## Axis B — Local repo `data/` structure (SS-B)

Mirror the estate `data/{pipeline}/scripts/{bronze|silver|gold}/*.py`; shared libs in a named
`lib/`/`canonical/`; vendored canonical copies carry a build-verified sha tie.

| Resource | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| `data/assets/scripts/{gold,silver,lib,analysis}` | **CONFORM** (layer split + named `lib/`) with **1 DEVIATE sub-row** | layer split present (gold/silver/lib); no `bronze/` scripts is correct (bronze is raw-as-delivered). **DEVIATE:** a non-data `org/mcp/` + `org/mcp/agent_telemetry/` subtree lives under `data/assets/` and `data/assets/scripts/` — fabric agent-comms scaffolding inside the data code tree, which SS-B says should mirror the estate. | LIVE-20260717 `find data/assets -maxdepth 3 -type d` |
| schwab silver/canonical code | **DEVIATE** | schwab converter code exists under TWO parallel homes — `data/canonical/schwab/` AND `data/schwab/` — not a single mirror-the-estate location (SS-B "Mirror the estate"). | LIVE-20260717 `find data -iname '*schwab*'` |
| `landing_guard.py` vendored copies | **CANDIDATE** | vendored in ≥2 Lambda dirs (`etfs-netassets-daily/`, `smartx_assets_pull/`); SS-B requires a sha-tie to the canonical file verified MECHANICALLY at build. **sha-tie presence UNVERIFIED in this census** — named as the exact input to the SS-B build-manifest gate (the bd49f BUILD_MANIFEST lesson SS-B cites). | LIVE-20260717 `find -iname landing_guard*.py` |

---

## Axis C — EC2 runner structure + specs (SS-C)

Structure invariant: registered in `EC2_MANIFEST.json`; code Local→S3→pull→execute; TF owns infra not
code. Size MAY vary (not a deviation); OS/telemetry/autostart/log-shipping/stamp-pair uniform.

| Runner | Type | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|---|
| `consolidation-gold-runner` | r6i.xlarge | **CONFORM** (structure) | registered in `infra/aws/ec2/EC2_MANIFEST.json`; autostart via `consolidation-gold-runner-scheduled-start` + `schedule_absence` alarm; size per-workload (allowed). *(OS deviation → Axis E.)* | LIVE-20260717 `describe-instances` + manifest grep (4 hits) |
| `canonical-schwab-runner` | r6i.xlarge | **CONFORM** (structure) | registered; SSM-driven (`opal-schwab-archive-01raw`, `opal-schwab-rps-convert`); `sentinel_absence`/`si2_schedule_absence` alarms present. *(OS deviation → Axis E.)* | LIVE-20260717 + manifest (4 hits) |
| `bd-49f-auto-login` | t3.medium | **CONFORM** | registered; SG `bd-49f-auto-login-sg`; AL2023. | LIVE-20260717 + manifest (6 hits) |
| `bd-assets` | t3.medium | **CONFORM** | registered; SSM `opal-bd-asset-dim-download`; AL2023. | LIVE-20260717 + manifest (2 hits) |

**Smell-pass (not a scored deviation — no SS-C region clause):** `canonical-schwab-runner` is us-east-1
while its data bucket `opal-data-schwab` is us-east-2 — a cross-region runner→bucket hop. Flagged for the
ruling batch as a possible SS-C addition (region co-location), not scored DEVIATE against the current doc.

---

## Axis D — Implementation patterns (SS-D, 8 canon rows incl. the 3 amended)

### D.1 — Scheduler naming `{unit}-{function}-{cadence}` (SS-D amended row; OPAL_STNDRD origin)

24 consolidation-associated schedule/rule names enumerated. **CONFORM: 14. DEVIATE: 10.**

CONFORM (14): `opal-assets-bd49f-dim-convert-daily`, `opal-assets-bd49f-dim-convert-absence-check-daily`,
`opal-assets-ingest-mirror-cot-daily`, `opal-assets-ingest-mirror-inf-daily`,
`opal-assets-ingest-mirror-cot-absence-check-daily`, `opal-assets-ingest-mirror-inf-absence-check-daily`,
`opal-assets-silver-{blackdiamond,eclipse,etf,orion,schwab}-sweep-daily` (5),
`bd-49f-runner-daily`, `bd-49f-session-daily`, `bd-49f-fees-runner-daily`, `bd-49f-fees-session-daily`,
`etfs-netassets-daily`, `inf-api-assets-v2-daily`.

| Rule/schedule | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| `opal-assets-bd49f-daily-pull-pull-daily` | **DEVIATE** | cadence-stutter: `daily` ×2 + `pull` ×2 (`...daily-pull-pull-daily`); the cadence token is embedded in the function name AND appended. | LIVE-20260717 `events list-rules` cron(30 2 * * ? *) |
| `opal-assets-bd49f-daily-pull-reattempt-daily` | **DEVIATE** | cadence token `daily` embedded in function (`daily-pull-reattempt`) then re-appended. | LIVE cron(30 4 * * ? *) |
| `opal-assets-bd49f-daily-pull-absence-check-daily` | **DEVIATE** | same embedded-cadence function stem (`daily-pull`) as its producer. | LIVE (scheduler) |
| `opal-assets-daily-emitter-daily` | **DEVIATE** | cadence-stutter `daily` ×2 (`daily-emitter-daily`). | LIVE cron(15 17 * * ? *) |
| `smartx-assets-daily-pull-daily` | **DEVIATE** | cadence-stutter `daily` ×2 (`daily-pull-daily`). | LIVE (scheduler) |
| `consolidation-gold-runner-scheduled-start` | **DEVIATE** | NO cadence token — ends `-scheduled-start` (a function); fires MON-FRI with no `{cadence}` suffix. | LIVE cron(30 6 ? * MON-FRI *) |
| `canonical-schwab-si2-08242234-daily-pull` | **DEVIATE** | no trailing `{cadence}` + misleading: function says `daily` while cron fires TWICE daily. | LIVE cron(15 10,22 * * ? *) |
| `canonical-schwab-si2-08335338-daily-pull` | **DEVIATE** | same: no cadence suffix + twice-daily cron under a `daily` function stem. | LIVE cron(45 9,21 * * ? *) |
| `canonical-schwab-si2-download-schedule` | **DEVIATE** | suffix `-schedule` is not a `{cadence}` token; twice-daily cron. | LIVE cron(35 8,20 * * ? *) |
| `bd-49f-freshness-sched` / `bd-49f-keepalive-sched` | **DEVIATE** | suffix `-sched` is not a `{cadence}`; `rate(1 hour)`/`rate(15 minutes)` → should read `-hourly`/`-15min`. | LIVE list-rules |

### D.2 — Absence twin (SS-D amended row: every scheduled producer pairs with an absence-detection twin)

11 scheduled producers enumerated. **PAIRED: 8. UNPAIRED (DEVIATE): 1. CANDIDATE: 2 classes.**

| Producer | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| `opal-assets-bd49f-daily-pull` | **CONFORM** | twin `...-absence-check-daily` (`aws_scheduler_schedule.bd49f_pull_absence_twin`). | TF-DESIRED@`opal-assets/*.tf` + LIVE scheduler |
| `opal-assets-bd49f-dim-convert` | **CONFORM** | twin `...-absence-check-daily` (`bd49f_dims_absence_twin`). | TF + LIVE |
| `opal-assets-ingest-mirror-cot` | **CONFORM** | twin `mirror_cot_absence_twin`. | TF + LIVE |
| `opal-assets-ingest-mirror-inf` | **CONFORM** | twin `mirror_inf_absence_twin`. | TF + LIVE |
| `consolidation-gold-runner` | **CONFORM** (twin = alarm) | `aws_cloudwatch_metric_alarm.schedule_absence`. | TF-DESIRED@`consolidation-gold-runner/*.tf` |
| `canonical-schwab-runner` / si2 | **CONFORM** (twin = alarm) | `sentinel_absence` + `si2_schedule_absence` alarms. | TF-DESIRED@`canonical-schwab-*/*.tf` |
| `bd-49f-runner` | **CONFORM** (twin = probe) | `bd-49f-freshness-probe` lambda + `bd-49f-freshness-sched`. | GRAPH + LIVE |
| **`smartx-assets-daily-pull`** | **DEVIATE** | scheduled producer with **NO absence-detection twin** — no `*-absence-check` schedule/alarm in `smartx-pipeline/assets-pull-*.tf` (the only `twin`/`absence` hits are unrelated comments at `assets-pull-iam.tf:154`, `assets-pull-lambda.tf:147`). | LIVE grep + `scheduler list-schedules` (no smartx absence twin) |
| `opal-assets-daily-emitter` | **CANDIDATE** | no `*-absence-check` twin found for the emitter itself; the emitter WRITES the downstream completion signal (`gold/meta/pipeline-complete.json`) but its own firing is untwinned. Verify whether an emitter-absence signal exists elsewhere before scoring. | LIVE grep (no emitter absence twin in opal-assets TF) |
| `opal-assets-silver-{firm}-sweep` (5) | **CANDIDATE** | the 5 scheduled silver sweeps have no `*-absence-check` twin; they are S3-event-primary (scheduled sweep is a backstop), so SS-D's twin duty may be satisfied by the event path — needs a ruling on whether an event-primary producer needs a scheduled-cadence twin. | LIVE grep (no silver-sweep absence twin) |

### D.3 — Other SS-D pattern rows

| Pattern (SS-D row) | Verdict | Note | Evidence |
|---|---|---|---|
| Pull provenance → `meta/pulls/{YYYYMMDD}/` | **DEVIATE** | provenance written inline at `.../{date}/_meta/pull_complete.json` (eclipse + blackdiamond), not the canonical `meta/pulls/`. (Same fact as Axis A.2 inline-`_meta` row; cross-listed.) | LIVE-20260717 |
| Landing verification (listing-based guard) | **CONFORM** (present) | `landing_guard.py` present in feeder Lambda dirs (etfs-netassets, smartx-assets-pull). Content-parity to canonical = the Axis-B sha-tie CANDIDATE. | LIVE find |
| lambda_chunking / retry-client / telemetry-at-provision | **NOT-MEASURED (scoped-out)** | per-lambda source-pattern conformance (chunking on large workloads, Retry session, telemetry-at-provision) is a deeper source audit than this structural census; named here as the next census slice, not scored. | — |

---

## Axis E — Device OS + IAM baseline (SS-E)

OS: Amazon Linux 2023 for new runners (existing AL2 migrate at rebuild). IAM: one role per
runner/Lambda, `{resource}-role`, scope-exact grants.

### E.1 — OS

| Runner | AMI | OS | Verdict | Deviation NAMED |
|---|---|---|---|---|
| `bd-49f-auto-login` | ami-00948338a4aeec604 | `al2023-ami-2023.12.20260622.0` | **CONFORM** | — AL2023 |
| `bd-assets` | ami-07ff62358b87c7116 | `al2023-ami-2023.10.20260105.0` | **CONFORM** | — AL2023 |
| `consolidation-gold-runner` | ami-0c7217cdde317cfec | `ubuntu-jammy-22.04-amd64-server-20231207` | **DEVIATE** | net-new consolidation runner on **Ubuntu 22.04**, not the SS-E AL2023 baseline. |
| `canonical-schwab-runner` | ami-0c7217cdde317cfec | `ubuntu-jammy-22.04-amd64-server-20231207` | **DEVIATE** | net-new consolidation runner on **Ubuntu 22.04**, not AL2023. (Same AMI as gold-runner.) |

### E.2 — IAM role naming

32 consolidation IAM roles enumerated (GRAPH). Naming `{resource}-role`: **CONFORM: 31. DEVIATE: 1.**

| Role | Verdict | Deviation NAMED | Evidence |
|---|---|---|---|
| 31 roles (`opal-assets-*-role`, `consolidation-gold-runner*-role`, `canonical-schwab-*-role`, `bd-49f-*-role`, `smartx-assets-pull*-role`, `opal-schwab-monolith-remap-role`) | **CONFORM** | `{resource}-role` (helper roles `{resource}-{automation-start,events-invoke-ssm,scheduler}-role` are named-consistent purpose roles, not a "one-role" violation). | GRAPH@8829022918628754404 |
| `schwab-anonymizer-lambda-role` | **DEVIATE** | extra `-lambda-` infix → `{resource}-lambda-role` instead of `{resource}-role` (only role carrying `-lambda-role`). | GRAPH |

**Scope-exactness (SS-E "scope-exact grants, measured by simulate-principal-policy"):** NOT measured
per-role in this structural census (the per-(action,resource) simulate-principal-policy audit with
isolated positive controls is a distinct deep pass — Rule 22a). Named here as the SS-E APPLIED-truth
follow-on; this census measures DESIRED naming + one-role-per-resource structure only.

---

## Phase-2 controls (reproduced — mandate gate)

| Control | Expected | Observed | Pass/Fail |
|---|---|---|---|
| **Conform control** — opal-data-assets canonical grammar path | CONFORM | `orion/inflection/bronze/assets/2020-04-28.jsonl.gz` measured = source/scope/layer/type/date → **CONFORM** (Axis A.1 row 1) | **PASS** |
| **Currency control** — us-east-2 telemetry bucket vs SS-A amended clause @HEAD | CONFORM-BY-AMENDMENT citing SS-A | `opal-schwab-d4-access-logs-313476888478` PAB all-4-true, dedicated, subject+acct named → **CONFORM-BY-AMENDMENT (SS-A telemetry clause)** (Axis A.1 row 2) | **PASS** |

Both controls discriminated (a conform resource read CONFORM; the telemetry bucket read
CONFORM-BY-AMENDMENT, NOT DEVIATE — proving the instrument read the standard at HEAD `cf4938c07`, not a
cached draft). The instrument can fail and did not.

---

## Deviation-class rollup (the input to CTO's gate design — SS-F step 2/3)

Per-axis denominators + named deviation classes, each quotable into a lint:

| # | Deviation class | Axis | Instances | Gate candidate |
|---|---|---|---|---|
| DC-1 | Non-grammar / non-`{source}` root in the monolith (`code/`, `_probe/`) | A | 2 roots (25 obj) | prefix-lint: deny root ∉ enumerated `{source}` set ∪ `{meta}` on `opal-data-assets` PutObject |
| DC-2 | Non-canonical `{layer}` token (`_ops`) | A | 1 (`blackdiamond/49f/_ops`, 5 obj) | prefix-lint: `{layer}` segment ∈ `{bronze,silver,gold,meta}` |
| DC-3 | Per-feed grammar drift — `{type|feed}` segment omitted (eclipse) | A | 1 feed | prefix-lint: bronze key depth == 5 (`{type}` present) |
| DC-4 | Pull-provenance written inline (`{date}/_meta/`) not `meta/pulls/{YYYYMMDD}/` | A/D | 2 feeds (eclipse, blackdiamond) | provenance-path lint |
| DC-5 | Non-data subtree in repo data tree (`data/assets/**/org/mcp/`) | B | 1 | commit-gate path lint: no `org/` under `data/*/` |
| DC-6 | Dual code home (`data/canonical/schwab` + `data/schwab`) | B | 1 | structural: single mirror-the-estate home |
| DC-7 | Vendored canonical copy without verified sha-tie (`landing_guard.py`) | B | ≥2 dirs (UNVERIFIED) | build-manifest sha-tie assertion (SS-B references the bd49f BUILD_MANIFEST) |
| DC-8 | Scheduler-name cadence-stutter (`daily...daily`) | D | 3 (`bd49f-daily-pull-pull-daily`, `daily-emitter-daily`, `smartx...daily-pull-daily`) | name-lint: `{cadence}` token appears once, as suffix only |
| DC-9 | Scheduler-name missing/`non-cadence` suffix (`-scheduled-start`, `-schedule`, `-sched`) | D | 5 | name-lint: suffix ∈ `{daily,hourly,weekdays,15min,...}` |
| DC-10 | Scheduler-name cadence embedded in function (`daily-pull*`) | D | 4 | name-lint (same as DC-8/9 family) |
| DC-11 | Misleading cadence — function says `daily`, cron fires twice-daily (schwab si2) | D | 2 | name-vs-cron cross-check lint |
| DC-12 | Scheduled producer without absence twin (`smartx-assets-daily-pull`) | D | 1 confirmed (+2 CANDIDATE classes: emitter, 5 silver sweeps) | provisioning gate: every `aws_scheduler_schedule`/`aws_cloudwatch_event_rule` with a cron pairs with an absence alarm/twin |
| DC-13 | New consolidation runner not on AL2023 (`consolidation-gold-runner`, `canonical-schwab-runner` on Ubuntu 22.04) | E | 2 | provisioning lint: new `aws_instance` AMI is an AL2023 owner-alias |
| DC-14 | IAM role naming infix (`schwab-anonymizer-lambda-role`) | E | 1 | name-lint: role matches `{resource}-role` (+ blessed helper suffixes) |

**Named UNVERIFIED (honest residuals, not scored CONFORM):** landing_guard sha-tie (DC-7); emitter +
silver-sweep absence twins (DC-12 CANDIDATEs); per-role scope-exactness (SS-E simulate-principal-policy
deep pass); per-lambda chunking/retry/telemetry-at-provision source patterns (D.3 scoped-out). Each is a
place to look, not a verdict laundered to CONFORM.

**Coverage denominator printed:** 8 buckets + 5 grammar sub-rows + 3 repo trees + 4 runners + 24
schedule names + 11 producers + 4 OS + 32 roles measured. opal-data-schwab measured pre-window (0.5.0
ruling); no live schwab call made.
