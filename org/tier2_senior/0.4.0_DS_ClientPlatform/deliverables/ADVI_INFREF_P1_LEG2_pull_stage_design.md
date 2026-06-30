# ADVI_INFREF P1 LEG-2 Step-1 -- PULL-STAGE MODULE DESIGN (for CTO arch-gate + 0.6.1_AE co-design)

**Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-06-30 | **TO:** ADVI_INFREF.P1 LEG-2
**Gate:** CTO arch-gates THIS design BEFORE the shell edit (3 checks below); 0.6.1_AE co-designs + supplies EC2/IAM/trigger.
**Scope:** Step-1 ONLY = the front-of-chain single PULL stage (CSV-dims land RAW as-is -- already CSV, NO de-convert).
The 4-dim JSON DE-CONVERT (positions/assets/perf/txn -> raw JSON + silver-read repoint) is the LATER atomic-per-dim
LEG-2 step (higher-risk, byte-parity-gated, positions_mv LAST) -- NOT this design.
**Inputs:** dim-list ef1c8e5fb (the pull surface) + timeout-tolerate 9ea447b3a (already live in run_script).

## 1. The MODULE -- clean PULL[I/O,can-hang] / COMPUTE[silver+A/B/C/D] boundary (CTO check #1)
In `data/inf/scripts/gold/orion-gold-dispatch.sh`, a separately-invocable PULL stage:
- `CHAIN_PULL` = the ingestion ids ONLY (all `INF_API_PULL_*` dims + their `INF_API_SILVER_*` converters), front-of-chain.
- New dispatch mode `--stage pull` (runs CHAIN_PULL then writes a `gold/meta/pull-complete.json` sentinel + exits) and
  `--stage compute` (asserts pull-complete sentinel for the run-date, then runs A/B/C/D). `--chain full` = pull-stage
  THEN compute-stage (the boundary is the sentinel). Keeps today's one-runner/one-script; the boundary is explicit.
- Every PULL step keeps the deployed `timeout -k 30 ${PULL_STEP_TIMEOUT:-600}` + tolerate (9ea447b3a, run_script
  INF_API_PULL_* branch) -- the PULL stage is the I/O/can-hang half; COMPUTE steps stay hard-fail under set -e.
- Rationale: this alone collapses the duplicate-pull hang class (the 2-layer overlap) -- the inline pulls become THE
  single pull layer; the 9 cron-Lambda pulls decommission (0.6.1 lane, SPEC-1 R1).

## 2. The PULL LIST (one-script-per-dim, two-domain, cataloged surface) (CTO check #2 + #3)
ORION domain -> `bronze/orion-api/{date}/` (Session-JWT; runner role covered):
- MOVE-ONTO-EC2 (today cron-only, 3): tax (tax_unrealized+tax_realized), billing, unified_account_dim.
- ALREADY-INLINE (6, keep as the single layer): representatives+household_rep_mapping, accounts_v2/new_portfolio,
  assets_v2(->positions/assets), transactions, performance, positions_daily.
- ONE SCRIPT PER DIM (retire dups in data/inf/manual_api/): txn = ONE (retire transactions.py + _v2.py, keep the
  Custom-Report-28198 _rest); performance = ONE (retire performance_dim.py, keep _rest). (the dup-retirement is the
  SPEC-1 §2 cleanup, folded here.)
- NEW cataloged (SPEC-1 §59 -- SCOPE for CTO, #10-12 from dim-list): Trading/Models + Models/{id} (139 models),
  Custom Reports per-txn (already = transactions), per-client Assets snapshot (= positions/assets, already), aux
  (Authorization/User+Privileges, Homepage/Action/DataSources). PROPOSE: pull Trading/Models in P1 (it's a real
  silver/gold-useful dim); per-account Assets (#11) + aux (#12) = DEFER (per-client covers v1; aux is observe-only).
ECLIPSE domain -> `bronze/eclipse-api/{date}/` (SEPARATE; orion->eclipse JWT exchange, likely zero IAM add):
- portfolios_simple, portfolios_full, models, model_composition_{id}x9 (pull_eclipse_portfolios.py, move onto EC2).
- TWO DOMAINS NEVER SHARE A PREFIX (SPEC-1 Principle 6); eclipse pulled raw, join only at gold.

## 3. Migration / parity (never-widen)
- PARALLEL-RUN: the new pull-stage runs the full surface alongside the existing inline pulls until the bronze output
  is parity-confirmed (same dims land, same content), THEN the 9 cron Lambdas decommission (0.6.1) + the inline-
  interleave is replaced by the front-of-chain stage. NO cron-decommission before the pull-stage is parity-proven.
- The CSV-dims land RAW unchanged (this step does NOT touch the parquet-at-bronze 4-dim double-write -- that's the
  later de-convert step). So Step-1 is bronze-additive/parity-neutral on existing silver: silver reads are unchanged.

## 4. The 3 CTO arch-gate checks (pre-answered)
1. BOUNDARY: explicit `--stage pull` (CHAIN_PULL + pull-complete sentinel) vs `--stage compute`; PULL=timeout-guarded
   I/O, COMPUTE=hard-fail. Separately-invocable. (your front-of-chain ruling to 0.6.1.)
2. SURFACE: the full DATA_PLATFORM-cataloged surface from dim-list ef1c8e5fb (9 prod + 3 cron-onto-EC2 + Trading/
   Models; per-account+aux DEFERRED) -- NOT vendor-exhaustive-guess; crawler-frontier (DC1/DC2) ingests as confirmed.
   YOUR CALL: confirm Trading/Models IN-P1 + per-account/aux DEFER.
3. ONE-SCRIPT-PER-DIM + TWO-DOMAIN: dup pull scripts retired (txn/perf), orion-api + eclipse-api distinct prefixes.

## 5. Lane split + next
- DS (me): authors CHAIN_PULL + the `--stage` modes + the sentinel + the one-script-per-dim consolidation in
  orion-gold-dispatch.sh (+ the dim pull scripts moved off manual_api into the chain).
- 0.6.1_AE: the EC2 run-mode wiring, the EventBridge two-flow (Leg-1 landed), the 9-cron decommission (post-parity),
  IAM (zero adds expected; eclipse-SM verdict at the eclipse step).
- ON CTO ARCH-GATE: I author the shell module (bash -n + a dry-run `--stage pull --dry-run` parity check), RAVC CTO
  the diff, 0.6.1 wires the EC2 mode, parallel-run parity, then cut over. RAVC CTO + 0.6.1 + CVO at parity.
