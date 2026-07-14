# OPAL_ASSETS_49METATABLES.D4 — connector census + silver-lambda verification

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-14 (~09:3x–10:3xZ measurement window)
**Dispatch:** CTO 085517Z (Andrew addendum verbatim: *"analyzing the infrastructural elements of the
connectors, making sure that the silver lambdas that set us up for this are actually done right"*).
**Bar:** every claim carries its layer — DESIRED (TF at commit) / APPLIED (live AWS primitive) /
EXERCISED (a real invocation's landed artifact) — and no config-read behavioral claims.
**Read-only:** zero fixes applied inside this census; everything routed as normal gated work
(and two items got fixed THROUGH those channels during the window — noted where they land).

---

## 1. The three feed paths (dispatch scope a + c)

### 1a. D2 — smartx daily lambda + feed-9 wiring — VERIFIED, all three layers

| Layer | Evidence |
|---|---|
| DESIRED | `infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf`: `smartx-assets-daily-pull`, own scheduler role (legacy roles untouched — new-territory), `aws_scheduler_schedule` 09:30 ET DST-stable, py3.11 (layer pin), 1024/900, fail-loud floors `EXPECT_MIN_MODELS=11`, `OPAL_FAMILY_VIEW_MIN=7`, `BUNDLE_ACCOUNTS_MIN=452`; feed-9 env `FEED9_BUNDLE_SECRET=smartx/credentials/yaliu-bundle` (deliberately NOT the global-precedence selector name — the env-precedence trap is documented in-file). |
| APPLIED | Live `get-function-configuration` == TF exactly (env, sizing, runtime; LastModified 09:30:50Z — 0.5.0 was mid-apply during measurement). Live role `smartx-assets-pull-role`: inline `smartx-assets-pull-access` CARRIES the yaliu-bundle GetSecretValue grant (exact suffixed ARN), + fence `opal-assets-one-way-fan-in-fence` attached, + basic logs. Scheduler `smartx-assets-daily-pull-daily` ENABLED cron(30 9) America/New_York. |
| EXERCISED | Real bronze landed TODAY: `smartx/account/{uuid}/bronze/allocations/20260714/allocations.json` at 08:49–08:54Z (listing-based, the 13c-sanctioned instrument). Scope grammar confirmed live: `account/{uuid}` two-segment scope — the uuid-mid-path fact that drove contract rule 10's basename design. |

**Feed-9 verdict: wiring is APPLIED (env + IAM grant both live).** Feed-9's own first EXERCISED
pull is 0.5.0's cell (rides the daily 13:30Z fire + their ligament rows tonight).

Gaps (named, §4): stale TF comment (G7), unconditioned ListBucket (G8).

### 1b. D3 — Schwab CRS silver converter — container VERIFIED; converter honestly PENDING-PACKAGING

| Layer | Evidence |
|---|---|
| DESIRED | Contract v1.2 rules 1–2 (suffix `.zip`, two masters never commingled) + `silver.tf` @ 5f6308383. |
| APPLIED | This session's V2-7 apply: notification rules `silver-schwab-08242234/-08335338` live (byte-exact vs contract), role `opal-assets-silver-schwab-role` live w/ per-master write ARNs, 22a battery 8/8 for the family (isolated positive, own-bronze-Put implicitDeny, firm-bucket + Door-6 explicitDeny, conditioned-List w/ context-entries). |
| EXERCISED | Stub level only — loud no-op proven on CloudWatch (event + sweep modes). **Converter code = honest PENDING: 0.6.2's packaging delta 4** (deps named: pandas+pyarrow, pins at packaging; upstream conversion framework 80/80 at bc4110283). Sweep 12:15Z fires the STUB today — that is AC-3 stub-behavior proof, not a conversion. |

Ingest side (C3, 0.6.2's lane, cited not re-measured): daily REST schedules live 09:45/21:45Z +
10:15/22:15Z; 0824 wide pull terminal 5,966; 0833 bronze in the monolith (his three-tier verify).

### 1c. D1 — the daily BD REST vehicle — TO-BE-BUILT; current state MEASURED

**The vehicle that exists is ALIVE; the source it points at is DEAD.** Measured this window:

- `bd-allocation-pipeline-trigger` ENABLED `cron(0 22 ? * MON-FRI *)` →
  `bd-allocation-trigger` Lambda (an EC2 starter: env `EC2_INSTANCE_ID=i-0800437d1dbb0b5cc` =
  `bd-allocations`, LastModified 2026-04-06) → SSM doc `opal-bd-allocation-download` (Command doc,
  live) → EC2 pulls scripts from `s3://opal-data-bd/scripts/src/` + runs
  `merge-daily-incremental.py` (Rule-12-compliant S3-pull shape) → Black Diamond **portal
  export** download. Sibling: `bd-transaction-pipeline-trigger` ENABLED 21:53Z →
  `bd-transactions-trigger` (i-00c7568bc510f7423).
- **The freshness-theater signature:** run logs land nightly on schedule (newest
  `logs/allocation-download-2026-07-13.log` @ 22:00:49Z) at a CONSTANT 1894 bytes across every
  observed night (07-08, 07-09, 07-10, 07-13) — a byte-identical nightly log is the same
  instrument-class as SA-1's well-formed empty manifests: **the connector reports "ran", and
  running is not landing.** Consistent with the Andrew-recorded fact that the allocations feed
  froze post-06-26 and is *replaced at source*.
- **Replacement mandate (Andrew-direct ~03:4xZ, recorded):** daily **REST** pattern for BOTH
  masters. The monolith side is ALREADY READY for it: `blackdiamond/cottonwood` write policy +
  live converter (real code as of v0.8.0), and `schwab/08335338` bronze landed by 0.6.2. What
  does not exist yet: the REST puller itself (auth, endpoint census, landing grammar, schedule).
- **Ownership:** 0.7.0 owns the vehicle (this census is its ground); DS owns the D1 dim design;
  DS opens the joint design thread today (his 085927Z). **Design inputs banked here:** the C5
  smartx-assets-daily-pull is the reference architecture (own role, own scheduler, fail-loud
  floors, fence attached, monolith-only landing) — D1's puller should clone that shape, not the
  EC2/SSM/portal-export legacy it replaces.

### 1d. Trigger-model reality per channel (dispatch scope c) — APPLIED truth, measured this session

| family | event rules (live) | schedule | sweep (live) | converter code |
|---|---|---|---|---|
| orion | 1 rule `.jsonl.gz` | — (mirror feeds it 14:15Z) | 16:00Z ENABLED | **REAL (v0.8.0)** |
| eclipse | 1 rule `.json` (belt-2 load-bearing) | — (mirror 14:15Z) | 16:00Z ENABLED | **REAL (v0.8.0)** |
| blackdiamond | 1 rule `.xlsx` | — (mirror 03:30Z) | 05:00Z ENABLED | **REAL (v0.8.0)** |
| schwab | 2 rules `.zip` (per master) | C3 REST 09:45/10:15 + 21:45/22:15Z | 12:15Z ENABLED | stub (0.6.2 packaging) |
| etf | **GATED** (ruling 26, tonight 22:00Z) | native 22:00Z landing | 23:30Z ENABLED | stub (V2-8 order 3) |
| smartx | 6 basename rules (the manifest.json event-fire question is RESOLVED: `manifest.json`/`backfill-status.json`/`*_manifest.json` match none — verified in the LIVE config) | C5 daily 13:30Z | **GATED** (C5 cadence) | stub (0.5.0 co-owns) |

## 2. Silver-lambda verification (dispatch scope b) — the V2-7/V2-8 chain

All evidence produced this session, committed: plan census 88/0/0 @ 74cc94ea6; 22a battery 48/48 @
685d64a (all three eval decisions observed — the instrument demonstrably discriminates); stub
loud-proof on CloudWatch (CTO rider 1); swap plan 0/3/0; live sha x3 MATCH; import-health smoke x3
(designed ValueError, proving layer imports resolve). Ledgers CLOSED:
20260714T0936Z (container, 4/4) + 20260714T1018Z (swap, 3/3). Tags opal-assets-v0.7.0 + v0.8.0.
CTO RAVC-4 accepted the container; swap applied on CTO AC-3 signoff 101710Z (B-COMPRESSED:
DS's pre-fire expectation reports made the natural fires prediction-then-observation).

**EXERCISED cells still open (armed, times pinned):** 14:15Z mirror walk expected ZERO-event
(dead INF raw producer — silence confirms); 16:00Z orion+eclipse sweeps = first real conversions
vs DS's 101619Z numbers + first-sweep THROUGHPUT measurement (orion backlog ~4,640 partitions;
>1wk projected clearance → V2-9 leg); bd real fire tomorrow 05:00Z; VendorDriftError on pre-2026
vintages expected = the typed boundary working.

## 3. Contract-vs-needs (dispatch scope b, "V2-7 container against V2-8 converter needs")

Two seam defects found AT AUTHORING, both fixed through the normal channel (contract v1.1,
DS-ratified 092612Z): DLQ drain actions (§5 duty vs §4 SendMessage-only — the
instrument-that-cannot-fail class) and conditioned ListBucket (set-identity is a two-sided
listing). One latent defect found AT REVIEW: no `unquote_plus` at the event boundary (S3 event
keys arrive URL-encoded) — measured 1,307 live bronze keys, ZERO encoding-significant today,
DS fixed at source same hour (8e46370bf) with a lambda_entry-path test. The seam-gap pattern to
carry forward: **every gap so far was a §5-behavior-vs-§4-grant mismatch or an event-boundary
encoding reality — check exactly those two seams first at the etf/smartx/schwab swaps.**

## 4. Named gap list with owners (dispatch scope d)

| # | Gap | Layer | Sev | Owner |
|---|---|---|---|---|
| G1 | **BD REST vehicle does not exist** (legacy vehicle alive, source dead post-06-26; nightly 1894-byte theater logs) | — | D1 BLOCKER-IN-WAITING | 0.7.0 (vehicle) + DS (dim design); joint thread opens today |
| G2 | ETF event rules 6–9 absent | DESIRED gap, deliberate (ruling 26) | gated | DS grounds suffixes on tonight's 22:00Z bytes → 0.7.0 `-target` add |
| G3 | smartx sweep schedule absent | DESIRED gap, deliberate | gated | 0.5.0 confirms C5 cadence → 0.7.0 adds |
| G4 | schwab converter code = stub | EXERCISED gap, honest | in-flight | 0.6.2 packaging delta (deps named) |
| G5 | ~~unquote at event boundary~~ | — | CLOSED @ 8e46370bf | DS (done) |
| G6 | `opal-cot-value-parity` missing from lambda-source-map (Rule 4) | DECLARATIVE | LOW | 0.7.0 queue (pre-existing find) |
| G7 | smartx TF comment "pull role does NOT get this ARN yet" is stale — the live role HAS the yaliu grant | DECLARATIVE drift | LOW | 0.5.0 next touch |
| G8 | ~~`ListMonolithSmartx` unconditioned~~ **FALSIFIED (0.5.0 live measure 11:07Z: the statement IS conditioned `s3:prefix=["smartx/*"]`, DESIRED==APPLIED since the role landed). The defect was MY READER: my policy-dump printer rendered Sid/Effect/Action/Resource and silently DROPPED Condition blocks — a conditioned statement rendered as unconditioned. An instrument that cannot display a field reports the field absent; the census's own bar caught its author.** | — | RETRACTED | 0.7.0 (corrected here, 11:1xZ) |
| G9 | orion sweep backlog ~4,640 partitions vs 600s timeout — first sweep measures; >1wk projection commissions V2-9 | EXERCISED, pending measurement | watch | 0.7.0 reports post-16:00Z → CTO rules |

**Convergence input (PRD sec-4):** the D4 half is this census; remaining = D1 joint design.
The infrastructure verdict Andrew asked for: **the silver lambdas are done right on the measured
bar** — every grant exercised through simulate with discriminating controls, every behavioral
claim either exercised or explicitly pinned to its natural-fire time, and the one place the
container and converter disagreed was caught at the seam review, not in production.
