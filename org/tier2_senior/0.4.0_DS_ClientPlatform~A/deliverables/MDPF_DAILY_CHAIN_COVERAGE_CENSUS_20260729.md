# MDPF daily-chain coverage census — Work Item 1 (CTO 044832Z), read-only

**Agent:** 0.4.0_DS_ClientPlatform~A · **Run:** 2026-07-29 ~0500-0512Z · **Scope:** canonical gold tree
`s3://opal-data-assets/portal/gold/mdpf/{scope}/{type}/{YYYY-MM-DD}.json` — for every (type × scope): does the
SCHEDULED chain write it daily, or did its dates come from hand-runs only?

**Denominators (printed per Rule 22):** canonical tree = 15 objects (full recursive ListObjectsV2, quoted below);
trigger scan = 143 EventBridge rules + 10 schedules, us-east-1 (comp-trigger); code bucket = 38 objects under
`s3://opal-data-mdpf/code/` (full recursive listing); dispatch deployed-vs-repo = byte diff of the downloaded S3
object vs `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh`.

## HEADLINE

**NO (type × scope) IN THE CANONICAL TREE HAS A SCHEDULED WRITER. ZERO. Today's 15:0xZ chain fire will accrue
NOTHING into `portal/gold/mdpf/**`.** The scheduled chain (Stage 6) writes only the *source* tree
`gold/mdpf_revamp/*` (underscore names, current-state overwrite files — no date accrual). The one bridge from
source → canonical, `data/mdpf/scripts/gold/build_portal_gold_accrual.py`, is invoked by **nothing** (not in the
dispatch — deployed OR repo copy, both grepped; no Lambda, no rule targets it) and is deployed **nowhere** (absent
from all 38 objects in `opal-data-mdpf/code/`). Every date in the tree so far came from local hand-runs
(write batches 19:49:06Z 07-28 and 00:35:16Z 07-29, rendered from `s3 ls` local-UTC-4; attribution to the two
known hand passes is INFERRED — the *no-scheduled-writer* claim is source-confirmed and does not rest on it).

The 16:15Z publisher cron (`opal-assets-mdpf-portal-publisher-daily`, cron(15 16), ENABLED) will fire daily and
re-publish the SAME latest date per (scope,type) until the accrual is scheduled. This matches CTO G6 (open gates
20260728_2140Z: "asked before P1 is scheduled") — the census confirms G6 is still fully open, and that it is
load-bearing for the entire contract, not one type.

## The table

Source producer = scheduled TODAY via dispatch Stage 6 (non-fatal, see D3), writes `gold/mdpf_revamp/…`.
Canonical accrual = `portal/gold/mdpf/…` daily date-key accrual.

| type | scope | source producer (scheduled, Stage) | canonical accrual | dates present |
|---|---|---|---|---|
| aggregate-aua-timeseries | 49financial | `dim_mdpf_aggregate_aua_timeseries.py` (6a) | **HAND-RUN ONLY** | 07-27 |
| aggregate-aua-timeseries | inflection | same (6a) | **HAND-RUN ONLY** | 07-27 |
| aggregate-aua-timeseries | global | same (6a + 6d re-stage) | **HAND-RUN ONLY** | 07-27 |
| aggregate-aua-timeseries | cottonwood | `build_cottonwood_mdpf_slice.py` (6d) | **HAND-RUN ONLY** | 07-22, 07-27 |
| account-distribution | 49financial | `dim_mdpf_account_distribution.py` (6b) | **HAND-RUN ONLY** | 07-28 |
| account-distribution | inflection | same (6b) | **HAND-RUN ONLY** | 07-27 |
| account-distribution | global | same (6b) | **HAND-RUN ONLY** | 07-28 |
| account-distribution | cottonwood | `build_cottonwood_mdpf_pair.py` (6d) | **HAND-RUN ONLY** | 07-20, 07-24 |
| aum-metrics | cottonwood | `build_cottonwood_mdpf_pair.py` (6d) | **HAND-RUN ONLY** | 07-20, 07-24 |
| aum-metrics | 49financial / inflection / global | **NO PRODUCER EXISTS** (WI-2, this lane, in flight) | n/a | none |
| account-units | cottonwood | `build_cottonwood_mdpf_pair.py` sidecar (`:500`, 6d) | **HAND-RUN ONLY** | 07-20, 07-24 |
| non-model-assets | global | `dim_mdpf_non_model_assets.py` (6c) | **HAND-RUN ONLY** | 07-27 |

Carried flag (PIN-1, unchanged): `account-units` cottonwood-only declaration is **UNVERIFIED — needs a consumer
trace** (CTO-routed, open).

## Defects, each with producer + trigger named

**D1 — THE canonical-accrual defect (all 11 existing pairs + both new ones once landed).**
Producer: `build_portal_gold_accrual.py` (repo-only, @6493257fc/@9e69057c9). Trigger: **NONE** — a production
pipeline must have a schedule; this one has neither schedule nor invoker. Two sub-blockers already on record
(F-3 / G6), census-verified still true on the live plane:
  (a) script absent from `opal-data-mdpf/code/` — and the dispatch's `s3 sync --delete` (:125) evaporates any
      hand-placed copy;
  (b) roster path mismatch: the roster IS now published (`code/scripts/gold/partner_roster.json`, 22,725 B,
      07-28 23:33Z) but the accrual reads `{workspace}/data/mdpf/config/partner_roster.json` repo-relative —
      staging the script alone still fail-closes on the runner. Fix design is a DS+AE seam; scheduling gate is
      CTO's (G6).

**D2 — The chain itself is still event-only.** Live trigger: `mdpf-daily-refresh-trigger`, event-pattern on the
INF completion marker (Door-6), ENABLED, fired 5x in the 7d window (last 07-28) — the "15:00Z family" is INF
completing ~15:00Z, not a schedule. `mdpf-scheduled-floor` (20:00Z daily incl. weekends,
`infra/aws/terraform/mdpf-pipeline/scheduled-floor.tf`) is **BUILT-NOT-LANDED**: absent from the live 143-rule
scan; its own header says apply is COO/CTO-gated. Until it lands, an INF failure = no MDPF fire at all (the
exact 07-18 six-day-freeze class NEVER#4 names). Not mine to apply; naming it because the census question "will
today's 15:00Z fire happen" is itself conditional on INF.

**D3 — Every contract type's *source* producer runs inside Stage 6, which is NON-FATAL by design.** A Stage-6
failure emits `RevampParallelFailed=1` (metric only, no alarm gate — and none should be built per the
moratorium) and the chain reports `complete`. Consequence for the contract: a silent no-fresh-source day is
structurally possible even after D1 is fixed. Remedy belongs with the accrual scheduling design (a gate/owned
blocking item, not an alert).

**D4 — Deployed dispatch lags repo.** S3 `code/mdpf-daily-dispatch.sh` md5 `6f26beac…` (07-23 vintage, 578
lines) vs repo `bf881091…` (609 lines); delta = closure-row-18 present-or-FATAL guard only (repo-newer,
functionally same stages otherwise). AE lane; noted so nobody reads the repo guard as live.

**D5 — aum-metrics × {49financial, inflection, global}: no producer.** This is WI-2, my build, dispatched.
Publisher side already confirmed ENUMERATE (AE~A 045920Z grounded at deployed CodeSha256 `WSwmCWplyR…`): the
artifacts flow to platinum automatically on landing; type grammar `[a-z0-9-]+` — `aum-metrics` passes.

## What today's fires WILL and WILL NOT heal (the question this census answers)

- **WILL:** refresh `gold/mdpf_revamp/*` source objects for all 11 source-covered pairs (if INF completes and
  Stage 6 passes); re-publish existing canonical latest-dates to platinum at 16:15Z (idempotent, no new data).
- **WILL NOT:** accrue any new `{date}.json` into `portal/gold/mdpf/**` for ANY type × scope — canonical-tree
  daily accrual does not exist as a scheduled behavior anywhere on the live plane.

Read-only throughout; zero writes to any pipeline surface, zero runs. Grounding: dispatch deployed copy
downloaded + byte-diffed; trigger claims from comp-trigger live scan (denominator above); code-bucket and
gold-tree listings full-recursive, quoted in this file's git blob's session log.
