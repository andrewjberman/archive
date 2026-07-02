# CVO Attestation — MDPF WS-E CUSTODY_SOURCE flip (bd -> schwab)

**Pre-parity + never-widen readiness.** Author: `3.0.0_SA_CVO`. Date: 2026-07-02 (~1319Z).
Change: MDPF WS-E 49F `partner_custody_total` basis switch, `bd` -> `schwab-native straight-RPS`,
via atomic SSM flip of `/mdpf/custody_source`. Clears the 6-day served-freeze
(`aggregate_aua_timeseries.json` frozen 2026-06-25 16:42:42 UTC).

## Verdict (this pass)

- **Pre-parity: CONFIRMED to the cent** (semantic axis, grounded on live silver RPS — NOT self-report).
- **Never-widen SCOPE: CLEARED** (Schwab-only, no account-set / Fidelity widen).
- **Never-widen served-delta: CAPTURED** (same-date 06-25 before/after; direction DOWN on every field).
- **PENDING (not yet GO):** DS~A leg-2 deploy+wire -> CVO live gate-PASS -> 3-way never-widen co-sign -> SSM flip -> CVO post-flip parity.

## Grounding (all live-artifact, citable)

### 1. Pre-parity anchor @06-24 — TIES TO THE CENT
Source: `s3://opal-data-bd/schwab/silver/rps/date=20260624/data.parquet` (independent CVO sum).
- gross market_value = **$1,591,227,965.20**
- literal-CASH (1 row, `.str.strip()=='CASH'`) = **$17,346.45**
- custody (CASH-excluded) = **$1,591,210,618.75** == locked design **to the cent**
- 91,200 rows / 5,892 accounts

Flip-date candidates pre-computed (DS~A expected-value now OFF critical path):
- 06-29: $1,604,444,361.43 (91,201 rows / 5,896 accts)
- 06-30 (latest partition): $1,608,080,123.25 (91,287 rows / 5,904 accts)

### 2. Cash rule — one rule / three call-sites, coherent
- WS-E feeder `data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py:590-591` — `.astype(str).str.strip().str.upper()` then `.isin({"CASH"})`
- leg-2 gate `data/mdpf/scripts/gold/validate_schwab_native_custody.py:82` — `.astype(str).str.strip() != "CASH"`
- CVO parity (this attestation) — `.astype(str).str.strip() == "CASH"` exclusion
- **Empirical strip-vs-upper delta = $0.00 on 06-24 / 06-29 / 06-30.** The feeder strips+uppercases; gate/CVO strip only. Coincident on live data (single uppercase `"CASH "` row); only a lowercase-cash ticker would separate them, and none exists. **Cosmetic drift note, NOT a flip-blocker.**

### 3. Leg-2 gate bands PASS on current latest (06-30)
positions 91,287 in [85k,96k] / accounts 5,904 in [5.6k,6.2k] / custody $1.608B in [$1.4B,$1.8B] /
RPS-to-RPS DoD 06-29->06-30 = +0.23% <= 1.6%. No false-DEFER on current data.

### 4. Flip mechanism — LIVE, dormant
`aws ssm get-parameter /mdpf/custody_source` = **`bd`** (version 1) — correct pre-flip. Flip = set `schwab`; rollback = `bd`.
(NB: a bare Git-Bash `get-parameter --name /mdpf/...` returns a FALSE `ParameterNotFound` — MSYS mangles the
leading `/`; read via PowerShell or confirm existence via `describe-parameters`. The param is NOT phantom.)

### 5. Never-widen served-delta — same-date 06-25 (before/after)
Served-before (bd-basis, frozen as_of 2026-06-25), from `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json` partner `49financial`:
- custody = $1,649,983,326.71 ; model_aua = $1,387,314,939.61 ; non_model_aua = $262,668,387.10

Served-after (schwab-native straight-RPS):
- custody @06-25 = **$1,597,168,491.42** -> basis-step **-3.20%** / **-$52,814,835.29** (DOWN)
- non_model_aua (design @06-24 dry-run) = $180,524,950.02 -> **-$82,143,437.08 / -31.3%** vs bd (DOWN)

**Scope:** Schwab-only 49F (reads only `schwab/silver/rps`; 5,886 accts @06-25). NO account-set widen,
NO Fidelity/full-book re-add — coheres ratified PRD v0.9 = Andrew Mandate Change 3.
**Direction:** every served field moves DOWN -> the flip structurally CANNOT be a "widen"; it is a
deliberate re-basis + freeze-clear. This is the never-widen limb for the CTO+COO+CVO sign-off.

## Open items to complete the co-sign
1. **DS~A** (rule-13 lane): deploy `validate_schwab_native_custody.py` (currently `MISSING_ON_S3` per `comp-pipescript deployed --firm mdpf`) + chain-wire post-WS-E / pre-rollup.
2. **CVO:** confirm live gate-PASS on the deployed+wired gate.
3. **3-way never-widen co-sign** (CTO + COO + CVO).
4. **0.5.0_AE:** single SSM `put-parameter` `bd -> schwab` (rollback `bd`).
5. **CVO post-flip parity** on the first post-flip nightly — append served-after same-date delta here; confirm freeze cleared.

## Non-actionable notes (Rule 22 — hypothesis, not proof)
- non_model_aua residual reconciliation (`custody - model - sma`) to be re-verified against the ACTUAL
  deployed feeder output on the ACTUAL flip date; the $180.5M figure is a 06-24 dry-run, not the flip-date served value.
