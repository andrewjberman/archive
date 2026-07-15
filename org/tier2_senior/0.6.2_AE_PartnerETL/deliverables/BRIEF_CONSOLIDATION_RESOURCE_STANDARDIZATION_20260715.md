# BRIEF -- CONSOLIDATION resource standardization: ingestion coverage verdict + the patterns/nomenclature/repo-documentation program

**To:** 1.0.0_SA_CTO (CONSOLIDATION owner) | **CC:** 2.0.0_SA_COO | **From:** 0.6.2_AE_PartnerETL
**Date:** 2026-07-15 ~18:4x-19:0xZ | **Authority:** Andrew-direct, MY terminal, two messages ~18:4xZ
**Basis:** live two-service trigger census + 10-tree bronze frontier sweep (all read-only, run-time
denominators) + repo doc-surface scan. Everything cited was measured this window unless marked prior-art.

## 0. THE MANDATE, VERBATIM (recorded + broadcast same turn per fabric law)

Message 1: "Make sure that all buckets with only up to 7-10 data have function eventbridge-triggered
daily ingestion lambdas, we also need to establish a clean and clear pattern of how those triggers are
named and documented. A big part of what we're doing here with the consolidation is not only
standardizing all of these resources and our data flows, we also want to standardize the patterns for
eventbridge, lambdas (and the chunking/parallelization function), EC2s (and thier autoshutdown),
terraform protocol, etc. anda all associated nomenclature and taxonomy."

Message 2: "That means we use medallion infrastructure every single time, we have raw bronze with the
same type of ingestion trigger lambdas every single time, when we use ec2s, we install them with our
telemetry analysis so we can keep an eye on them with a protocol for right sizing, all of this stuff
needs to be standardized. [...] start scanning resources and repo documentatiobn on the architecutre of
these resources and their interactions and develop a briefing on how we can achieve this and issue that
brief to CTO. This should cover not only the cloud, but how this information is stored and documented
inside the local repo and local repo directory structure/maintenance."

## 1. ASK-1 ANSWERED -- ingestion coverage of the <=07-10 frontier class

**Every monolith bronze tree has live, verified ingestion wiring. The <=07-10 class is exactly the two
held INF channels, and their ingestion is proven working** (FRONTIER_0710_INGESTION_CHECK_20260715.md @
195653e85, CTO-accepted into the cert): frontier = the upstream raw producer dead UNDER THE STANDING
HOLD; re-wiring or restarting it is Door 5, Andrew-by-name. **No unwired bucket exists to fix.**

| Tree (10/10, run-time enumerated) | n | frontier | ingestion unit | trigger (service / state) |
|---|---|---|---|---|
| orion/inflection/bronze | 4,640 | **07-10** | opal-assets-ingest-mirror | rule ingest-mirror-inf-daily 14:15Z ENABLED, fired-clean today |
| eclipse/inflection/bronze | 624 | **07-10** | opal-assets-ingest-mirror | same rule -- same verdict |
| blackdiamond/cottonwood/bronze | 313 | 07-15 | opal-assets-ingest-mirror | rule ingest-mirror-cot-daily 03:30Z ENABLED |
| blackdiamond/49f/bronze | 6 | 07-14 (T-1 healthy) | opal-assets-bd49f-daily-pull | rules ...-pull-daily 02:30Z + ...-reattempt-daily 04:30Z ENABLED |
| schwab/08242234/bronze | 6,246 | 07-14 (T-1 healthy) | EC2 si2 box pull | rule canonical-schwab-si2-08242234-daily-pull 10:15/22:15Z ENABLED |
| schwab/08335338/bronze | 6,959 | 07-14 (T-1 healthy) | EC2 si2 box pull | rule canonical-schwab-si2-08335338-daily-pull 09:45/21:45Z ENABLED |
| smartx/platform/bronze | 3 | 07-15 | smartx-assets-daily-pull | **SCHEDULER** smartx-assets-daily-pull-daily ENABLED |
| trueshares/DIVZ + /IDVZ | 1+1 | 07-15 | etfs-netassets-daily | rule etfs-netassets-daily 22:00Z ENABLED |
| pathfinder/filepoint/bronze | 2 | 07-15 | **OPEN CELL -- feeder not identified in this sweep** | -- |

Frontier discipline: schwab/bd 07-14 keys are TODAY'S pulls of yesterday's business date (T-1, NEVER#1)
-- current, not stale. Trading-day math per lib/trading_calendar throughout.

## 2. MEASURED CURRENT STATE -- the heterogeneity the standard has to close

**(a) TWO scheduling services live simultaneously.** Classic EventBridge RULES carry mirror / bd49f /
etf / emitter / schwab-si2 / inf-api; **EventBridge SCHEDULER** carries 8 schedules (smartx x4, etf
reports x2, astn-wsjft x2). Consequence measured live: `list-rule-names-by-target` returns EMPTY for
smartx -- a rules-only census reads a wired channel as unwired. Any coverage instrument must sweep BOTH
services or it lies by omission.

**(b) Five trigger-naming patterns in live use** (exhibits): `opal-assets-ingest-mirror-{tree}-daily` /
`opal-assets-bd49f-daily-pull-pull-daily` (the unit name already ends in -daily-pull, so the rule
stutters) / bare `etfs-netassets-daily` (rule name == lambda name, function invisible) /
`canonical-schwab-si2-{master}-daily-pull` (EC2 family, different root) /
`smartx-assets-daily-pull-daily` (Scheduler). An absence-check twin EXISTS as a nascent convention
(etfs-reports-monthly-absence-check, astn-wsjft-4am-absence-check) but is applied to 2 units only;
bd49f has a reattempt twin instead; mirror/schwab/etf-netassets have neither.

**(c) Sizing/registry drift is a live class, caught twice TODAY:** lambda-source-map said schwab
memory 3008 while TF+live said 10240 (fixed @ 6bfea3fdf); the schwab BUILD_MANIFEST `memory_mb: 3008`
still reads as a TARGET with no field semantics saying so. The registries record desired state with no
instrument tying them to applied state.

**(d) Chunking/parallelization: the standard already exists and is one leg from CANONICAL.**
lib/stream_parquet (delta-6): memory-bounded atomic fan-out writer, n=2 formally reviewed across two
vendor grammars (orion jsonl.gz + schwab CRS), measured 3.17GB->786MB on the OOM-basis unit. The
chunking-arch doc stamps CANONICAL on my AC-1 runtime number tonight. The standard needs NAMING as law
("any partition-scale write rides ChunkedParquetWriter"), not invention.

**(e) EC2s:** EC2_MANIFEST.json exists (rule 8) and safe-ec2-deploy/S3-artifact law is strong (rules
7-12), but telemetry-at-provision, a right-sizing protocol, and autoshutdown are NOT standardized --
the si2 box runs 24/7 with no recorded sizing review; prior art ADHC_TRIGMRK documents how fragile the
EC2<->trigger contract gets without a standard (the phantom-consumer marker incident family).

**(f) Repo documentation:** machine-readable registries EXIST but are PLURAL and unevenly gated --
lambda-source-map.json (CI drift-check), EC2_MANIFEST.json, per-lambda BUILD_MANIFEST.json,
lambda-layer-map.json, shared-infra-resource-map.json -- and **there is NO trigger registry at all**:
rules/schedules live only in TF source. docs/architecture is codename-keyed (40+ ADHC_*/NFRA_* files,
no resource-type index); deployment law is split across CLAUDE.md + docs/deployment/*. Prior art:
ADHC_LAMBDADOC (deployment-doc gap incidents: flat-vendoring, layer-ARN drift) is the incident record
arguing for exactly this consolidation.

## 3. PROPOSED TARGET STANDARDS (per axis -- concrete, gate-enforced, for your ratification)

**A. THE MEDALLION LAW (per source tree).** Every source lands as
`{source}/{scope}/{bronze|silver|gold}/...` in the monolith with, ALWAYS: raw-only bronze (17a; the
mirror's COERCED_SUFFIXES exclusion generalized), exactly ONE registered ingestion unit, silver
`fact_*` conversion (T1-class control where the vendor ships one), manifest emission per run, and a
registry row. "The same type of ingestion trigger lambda every single time" = one blessed ingestion
unit shape: schedule + absence-check + manifest + registry, whether the puller is a Lambda or an EC2.

**B. TRIGGER STANDARD.** (i) ONE scheduling service for cron-class triggers -- recommend EventBridge
SCHEDULER for all new cron work (flexible windows, native retry policy; rules stay ONLY for
event-PATTERN triggers like S3-event and bronze-complete) -- your call, but ONE, and the census
instrument sweeps both regardless. (ii) Naming grammar:
`{unit}-{function}-{cadence}` where `unit` = the target's exact name, `function` in
{run, reattempt, absence-check}, cadence in {daily, monthly, ...}; the bd49f stutter and the bare
etf name both fall out. (iii) **Absence-check twin REQUIRED for every daily producer** -- the
etfs/astn pattern generalized; a fire that lands nothing must alarm (silence is never success).
(iv) **A trigger registry**: `infra/aws/lambda/ci/trigger-map.json` (or a `triggers[]` block per
source-map entry) carrying rule/schedule name, service, cron, target, absence-twin -- with a CI
drift check against live, same class as the source-map check. I can author the two-service census
script that builds + checks it (I have it half-written from today's sweep).

**C. LAMBDA STANDARD.** Naming `opal-assets-{stage}-{source}` (the dominant family: silver converters
already conform; legacy names rename on natural touches, never big-bang). BUILD_MANIFEST.json REQUIRED
per lambda with `sizing_basis` = a MEASURED acceptance (the delta-6 3-dim form: RSS/wall//tmp on the
heaviest real unit) and field semantics fixed (memory_mb = TF-desired, stamped with the TF motion).
Chunking law: partition-scale writes ride lib/stream_parquet (canonical at n=2 tonight). A CI
instrument reconciles source-map/BUILD_MANIFEST/TF/live sizing -- the drift class I hit twice today
dies as a class.

**D. EC2 STANDARD.** EC2_MANIFEST row + safe-ec2-deploy (existing law) PLUS: telemetry agent installed
AT PROVISION (CW agent: mem/CPU/disk into the estate telemetry), a QUARTERLY-or-on-incident
right-sizing review recorded next to the manifest (the Lambda sizing_basis discipline ported), and
autoshutdown DEFAULT for any box without a 24/7 duty cycle (the si2 box's cron windows are 4 fixed
times/day -- exhibit A for schedule-scoped uptime). Exceptions declared in the manifest, never implicit.

**E. TERRAFORM PROTOCOL.** The law already exists and held twice today (commit-before-apply, plan-shape
0/1/0 gates, safe-apply/HALTGT, 0-diff, tag `{pipeline}-v{X.Y.Z}`, one-motion rulings) -- it is
scattered across CLAUDE.md + docs/deployment. Consolidate VERBATIM into one
`docs/deployment/TERRAFORM_PROTOCOL.md`, referenced from CLAUDE.md (law stays in CLAUDE.md; the
mechanism moves to the doc per the where-things-go table).

**F. REPO DOCUMENTATION + DIRECTORY STANDARD.** (i) One REGISTRY surface: formalize
`infra/aws/lambda/ci/` (or `infra/aws/registry/`) as THE machine-readable home -- source-map,
trigger-map (new), layer-map, EC2_MANIFEST, shared-infra-map -- every registry with a CI drift gate
(gates teach at violation time; prose taxes every session). (ii) `docs/architecture/INDEX.md` keyed by
RESOURCE TYPE (lambda/trigger/EC2/TF/bucket) mapping codenames to subjects, so the 40+ ADHC_*/NFRA_*
corpus becomes navigable by what a reader owns rather than by what an incident was called. (iii)
Per-resource docs live WITH the resource (the BUILD_MANIFEST pattern), estate-wide docs in docs/,
decision records in org/tier0/ledger -- already the CLAUDE.md table; the INDEX makes it findable.
(iv) Maintenance = instruments, not cadence: every registry gets a drift check; no scheduled prose
reviews.

## 4. GAPS FOUND BY THIS SWEEP (actionable, none urgent tonight)

1. **pathfinder/filepoint feeder unidentified** (n=2, frontier current) -- open cell; needs an owner claim.
2. `smartx-model-monthly-pull-daily` Scheduler entry DISABLED -- verify intended (monthly-vs-daily name smell too).
3. No absence-check twin on: ingest-mirror (both rows), bd49f, schwab-si2, etfs-netassets -- the B(iii) rollout list.
4. BUILD_MANIFEST field-semantics ambiguity (schwab memory_mb 3008-as-target vs live 10240) -- C's fix.
5. Trigger registry does not exist -- B(iv); trigger knowledge currently lives only in TF + tribal memory.

## 5. EXECUTION SHAPE (yours to decompose under CONSOLIDATION)

Phase the standard behind ratification, not renames: (1) you ratify grammars + registry schemas (this
brief's B-F); (2) trigger-map census script built + first map committed (I volunteer -- half-written);
(3) absence-check rollout on the 4-unit gap list; (4) renames ride natural touches only; (5) EC2
telemetry/right-sizing doc + si2 as the pilot; (6) TERRAFORM_PROTOCOL consolidation; (7) INDEX.md.
Each phase gate-enforced per the CLAUDE.md rule-shape (imperative + gate + pointer). My lane can carry
the schwab/trigger-map/chunking-adjacent pieces without disturbing tonight's binding legs (AC-1 number,
box-guard first fire).
