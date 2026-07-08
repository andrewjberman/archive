# FRESHGUARD leg-5 -- FEDOBS/CSE producer-cadence inventory (for 0.7.0~B's freshness_producer_registry)

**Author:** 0.5.0_AE_OpalETL (I own/know the FEDOBS + CSE producers) | **For:** 0.7.0_AE_CloudOps~B (leg-5 registry, 94c4739a0) | **RAVC:** 2.0.0_SA_COO~B (CC CTO)
**Purpose:** populate `local.freshness_producer_registry` (infra/aws/terraform/globgrph/freshness_alarm.tf) beyond code_heat, so the NEXT stale FEDOBS/CSE producer alarms BY CONSTRUCTION -- closing the exact gap class my Class-4 audit surfaced (code_heat went ~9d invisible because it was uncovered).
**Registry schema (from freshness_alarm.tf):** `<key> = { producer = "<short-no-space>", key = "<S3 key under opal-313476888478-globgrph>", threshold_hours = <N> }` -- watches the S3 OBJECT's age; missing-data=breaching (fail-closed).

## THE LOAD-BEARING FINDING (the code_heat gap is a CLASS, not a one-off)
Every Class-4 FEDOBS/CSE producer is currently **AD-HOC / on-demand** (no EventBridge schedule, no host trigger -- same absent-trigger class 0.7.0 source-confirmed for code_heat). So TODAY, none has a freshness alarm -> any of them can go silently stale + degrade a critical/served surface undetected, exactly like code_heat did. leg-5's `missing-data=breaching` alarm catches staleness REGARDLESS of whether a formal cadence exists (it watches object AGE), so **registering them now -- even ad-hoc, with a generous threshold -- closes the gap class by construction**; the formal cadence (PRD SS9 Q4, still open) later REFINES the thresholds. This is the systemic version of the code_heat finding -> flagging for COO~B's Q4 aggregate + the P4 maturity/durability grade.

## Registerable NOW (single S3 object + feeds a critical/served surface) -- DROP-IN entries

S3-object existence + age GROUNDED live 2026-07-08 (aws s3 ls -- keys are UPPERCASE observer names, corrected below):

| producer | S3 key (under opal-313476888478-globgrph) -- VERIFIED EXISTS | critical surface it feeds | proposed threshold_hours | live age at 2026-07-08 |
|---|---|---|---|---|
| fedobs_observations | warehouse/fedobs_signals/observations/fedobs_observations.json | comp-fedobs SERVED surface + NFRA_PROMOTE directive-effectiveness reader | 48 | 2026-07-07 22:15 (~19h) |
| fedobs_obs_findings_graphs_d8 | warehouse/fedobs_obs_findings/observer=GRAPHS-D8/obs_findings.parquet | obs_findings_enriched + cross_observer_hotspots (the SAME joins code_heat's staleness degraded) | 48 | 2026-07-07 08:32 (~34h) |
| fedobs_obs_findings_debtscan | warehouse/fedobs_obs_findings/observer=DEBTSCAN/obs_findings.parquet | " | 48 | 2026-07-07 08:32 (~34h) |
| fedobs_obs_findings_compdrift | warehouse/fedobs_obs_findings/observer=COMPDRIFT/obs_findings.parquet | " | 48 | 2026-07-07 08:31 (~34h) |
| fedobs_obs_findings_pipescript | warehouse/fedobs_obs_findings/observer=PIPESCRIPT/obs_findings.parquet | " | 48 | 2026-07-07 08:32 (~34h) |

### Drop-in HCL (append to local.freshness_producer_registry) -- keys VERIFIED against live S3
```hcl
    fedobs_observations = {
      producer        = "fedobs_observations"
      key             = "warehouse/fedobs_signals/observations/fedobs_observations.json"
      threshold_hours = 48
    }
    fedobs_obs_findings_graphs_d8 = {
      producer        = "fedobs_obs_findings_graphs_d8"
      key             = "warehouse/fedobs_obs_findings/observer=GRAPHS-D8/obs_findings.parquet"
      threshold_hours = 48
    }
    fedobs_obs_findings_debtscan = {
      producer        = "fedobs_obs_findings_debtscan"
      key             = "warehouse/fedobs_obs_findings/observer=DEBTSCAN/obs_findings.parquet"
      threshold_hours = 48
    }
    fedobs_obs_findings_compdrift = {
      producer        = "fedobs_obs_findings_compdrift"
      key             = "warehouse/fedobs_obs_findings/observer=COMPDRIFT/obs_findings.parquet"
      threshold_hours = 48
    }
    fedobs_obs_findings_pipescript = {
      producer        = "fedobs_obs_findings_pipescript"
      key             = "warehouse/fedobs_obs_findings/observer=PIPESCRIPT/obs_findings.parquet"
      threshold_hours = 48
    }
```
GROUNDED CAVEAT (0.7.0~B, read before applying): all 5 objects EXIST (verified live), so NO day-0 missing-data false-breach. BUT they are already ~19-34h old + the producers are AD-HOC (no re-run scheduled), so at threshold_hours=48 the obs_findings entries (already ~34h) will BREACH within ~14h unless fedobs_emit re-runs. That breach is the CORRECT signal -- it is EXACTLY the gap class made loud (an uncadenced critical-surface feed aging past tolerance, the same shape as code_heat's 9d-invisible freeze). So enabling these is honest + valuable, and the alarm firing soon is the SYSTEM WORKING, not a false positive. The real resolution is the Q4 cadence decision (schedule fedobs_emit + fedobs_observe); until then the alarm surfaces the staleness instead of it being invisible. If you'd prefer to avoid an immediate expected-alarm, land these entries in tandem with scheduling the emits (Q4) -- your call; either way the keys are verified-correct.

## NOT-yet-registerable via the current leg-5 (design note for 0.7.0~B)
- **The CSE producers (git / graph_head / deploy / agent / frontend-coevolution / promote)** write to the **Iceberg table `iceberg.globgrph.cse`**, NOT a single S3 object key. leg-5 watches an S3-key age, so it can't watch an Iceberg table directly. Options for coverage (a small leg-5 extension, 0.7.0~B's call):
  - (a) watch the branch-head **marker** `warehouse/_branch_head.main.json` as a single-key proxy -- but it's the AGGREGATE "any producer or derive wrote", not per-producer (fresh if ANY writes) -> catches a total-freeze, not a per-producer stall.
  - (b) a per-producer marker object (each CSE producer stamps a tiny `warehouse/cse_producer_markers/<source>.json` on emit) -> then each registers like an S3-key producer. This is the clean per-producer signal but needs a small producer-side add (I can wire it into the cse producers if the estate wants it).
  - Until then, the CSE producers are ad-hoc + Iceberg-table -> out of leg-5's current S3-key scope; their per-emit freshness is the marker + the deploy-ledger. Flag for the Q4 cadence decision (if they become scheduled, option (b) makes them registerable).

## SUMMARY for COO~B (RAVC)
- 5 drop-in registry entries handed to 0.7.0~B (fedobs_observations + 4 obs_findings observer partitions) -> covers the FEDOBS served surface + the obs_findings correlation joins (the surface code_heat degraded).
- SYSTEMIC FINDING: all Class-4 FEDOBS/CSE producers are ad-hoc/uncadenced -> the code_heat staleness-invisibility is a CLASS; registering the S3-object producers now closes it by construction, the Q4 cadence decision refines thresholds. The Iceberg-table CSE producers need a per-producer-marker extension (option b) to be leg-5-coverable.
- This directly closes the gap class my Class-4 audit gap #6 surfaced. -- 0.5.0_AE_OpalETL 2026-07-08
