# Gold Chain DAG Validation — Groups A, B, C
**Agent:** 0.4.0_DS_ClientPlatform~B  
**Date:** 2026-04-16  
**Scope:** Groups A (A_00–A_04), B (B_00–B_03), C (C_00–C_08)  
**Method:** comp-pipescript io on all 19 scripts + direct code verification for comp gaps  
**References:** 5f8d5c88 (original bottleneck audit + phase map)  

Group D + cross-group boundary edges: owned by ~C.

---

## Summary

Original phase map in 5f8d5c88 contained **one race condition** (B_02 || B_03) caused by a
comp tool write-detection gap. Additionally, two implicit dependencies not in the declared
dep graph were identified. Revised phase map below is safe.

---

## Full I/O Matrix — Groups A, B, C

### Group A

| Script | Reads | Writes |
|--------|-------|--------|
| A_00 | accounts_dimension (external/silver) | accounts_dimension → A_01, A_04, B_00, B_01, B_02, C_00–C_03, C_05–C_07, D_00, D_00b, D_01 |
| A_01 | accounts_dimension (A_00) | advisor_assignments_history → C_08, D_00c, D_02 |
| A_02 | (none) | fee_rate_history → C_08, D_00c, D_02 |
| A_03 | (none) | positions_cube/{*}.parquet → B_00 (implicit — see below) |
| A_04 | accounts_dimension (A_00) | client_dimension → D_00, D_00b, D_00c, D_01, D_02, D_03, D_04 |

### Group B

| Script | Reads | Writes |
|--------|-------|--------|
| B_00 | accounts_dimension (A_00), positions_cube/ (A_03), canonical_prices (silver), schwab_bd_mapping, canonical_holdings/{*} (prior run) | canonical_holdings/{*} → B_02, B_03, C_02, C_06; canonical_holdings_gaps/{*}; watermarks.json |
| B_01 | accounts_dimension (A_00) | holdings_lots/{*}, holdings_lots_shadow/{*}, holdings_lots_backfill/{*} → C_05 (via prefix) |
| B_01b | holdings_lots/ (B_01), classify_watermark | classify_watermark |
| B_02 | canonical_holdings/{*} (B_00), schwab ULN/ULT/RLD prefixes, canonical_prices, canonical_lots_realized/{*} (prior), canonical_lots_unrealized/{*} (prior) | **canonical_lots_unrealized/{*} → B_03, C_05; canonical_lots_realized/{*} → B_03** (comp WRITES: none detected — gap, verified L617–624) |
| B_03 | canonical_holdings/{*} (B_00), canonical_lots_realized/ (B_02), canonical_lots_unrealized/ (B_02) | canonical_account_gains/{*} → C_00, C_01, C_02, C_03 |

### Group C

| Script | Reads | Writes |
|--------|-------|--------|
| C_00 | accounts_dimension (A_00), canonical_account_gains/ (B_03) | canonical_performance/{*} → C_02 |
| C_01 | accounts_dimension (A_00), canonical_account_gains/ (B_03), client_performance (prior run C_02), nna_atomic/{*} (external), nna_validation/{*} (external) | canonical_nna/{*} → terminal |
| C_02 | accounts_dimension (A_00), canonical_account_gains/ (B_03), canonical_holdings/ (B_00), canonical_performance/ (C_00) | client_performance.parquet → C_01(next run), C_03, C_06, D_00, D_00b, D_01, D_03; aua_certification/{*} → D_00, D_00b, D_01 |
| C_03 | accounts_dimension (A_00), canonical_account_gains/ (B_03), client_performance (C_02) | account_performance.parquet → C_01b, C_06, C_07, D_00, D_00b, D_00c, D_01, D_02, D_03, D_04 |
| C_04 | aua_validation_{*}.json (S3-dynamic, written during chain) | aua_validation_{*}.json → terminal |
| C_05 | accounts_dimension (A_00), canonical_lots_unrealized/ **(B_02)**, holdings_lots/ (B_01) | client_tax_liability.parquet → D_00, D_02 |
| C_06 | accounts_dimension (A_00), account_performance (C_03), canonical_holdings/ (B_00), client_performance (C_02), rel_architect_lookup (C_07), client_timeseries/{*} (prior), mix_daily_summary (prior) | mix_daily_summary → D_03, D_04; client_timeseries/{*} → D_04 |
| C_07 | accounts_dimension (A_00), account_performance (C_03) | account_team → C_01b, C_08, D_00, D_00b, D_00c, D_01, D_02, D_04; relationship_team; rel_architect_lookup → C_06, D_00, D_00b, D_00c, D_01, D_02, D_03 |
| C_08 | account_team (C_07), advisor_assignments (A_01), fee_rate_history (A_02), nna_atomic/ (external), role_aua/ (external), advisor_fee_detail/ (prior) | advisor_fee_efficiency.json → D_04; advisor_fee_detail/{*} |

---

## Findings

### FINDING 1 — RACE CONDITION IN ORIGINAL PHASE MAP (B_02 || B_03)

**Severity: HIGH — would corrupt B_03 output on first run.**

Original audit proposed PHASE_B2: `B_02 || B_03`.

**Reality:** B_02 writes `gold/canonical/lots_unrealized/{date}.parquet` and `gold/canonical/lots_realized/{date}.parquet` (B_02.canonical_lots.py L617–624 — `_s3.put_object(..., Key=canonical_lots_unrealized_key(date_str))` and `Key=canonical_lots_realized_key(date_str)`).

B_03 reads both prefixes (`CANONICAL_LOTS_REALIZED_PREFIX`, `CANONICAL_LOTS_UNREALIZED_PREFIX`) — these are the same S3 paths B_02 writes.

**Comp tool gap:** `comp-pipescript io B_02` reports `WRITES: (none detected)`. The tool misses puts that use helper-function keys (`canonical_lots_unrealized_key`, `canonical_lots_realized_key`). This is a known gap in the FUNC-key writer detection path.

**Fix:** B_02 must complete before B_03 starts. They cannot be in the same phase.

---

### FINDING 2 — IMPLICIT DEPENDENCY: A_03 → B_00 (not in comp manifest)

**Severity: MEDIUM — preserved by A-before-B phase ordering, but undeclared.**

B_00 reads `POSITIONS_CUBE_PREFIX: gold/timeseries/positions_cube/ [PREFIX]` — declared as `(external/silver)` in comp manifest.

A_03 writes `positions_cube_key: gold/timeseries/positions_cube/{*}.parquet [FUNC]` — declared as `-> (terminal)` (no downstream consumers listed).

These are the same S3 path. The comp tool lost the edge because B_00 uses a PREFIX read and A_03 uses a FUNC write — the cross-reference logic does not match them.

**Risk:** If A_03 were ever moved or excluded from the full chain, B_00 would run on stale positions_cube data with no declared gate. This caused the Easter 2026-04-03 incident (stale pricing).

**Fix:** No change to phase map needed — A group runs before B group by design. However, the dependency should be declared explicitly in `gold_pipeline_deps.yaml` as a precondition for B_00.

---

### FINDING 3 — IMPLICIT DEPENDENCY: B_02 → C_05

**Severity: LOW — preserved by phase ordering in revised map.**

C_05 reads `CANONICAL_LOTS_UNREALIZED_PREFIX: gold/canonical/lots_unrealized/ [PREFIX]` — declared as `(external/silver)`.

This is the same path B_02 writes (FINDING 1). C_05 therefore depends on B_02, not just B_01. The comp manifest does not declare this edge.

In the revised phase map below, B_02 completes before C_05 starts. Preserved, but should be added to `gold_pipeline_deps.yaml`.

---

### FINDING 4 — C_01 reads CLIENT_PERFORMANCE from prior run (by design, not a bug)

**Severity: INFO — confirms C_00 || C_01 is safe.**

C_01's comp manifest shows `CLIENT_PERFORMANCE: gold/timeseries/client_performance.parquet <- C_02`. C_01 runs before C_02 in chain order. Confirmed by inspection: C_01 uses client_performance only for legacy NNA cross-validation (optional reference to prior run's output). It does NOT require the current run's C_02 output.

**Implication:** C_00 and C_01 can safely run in parallel — neither produces output the other reads.

---

## Validated Phase Map (Groups A, B, C)

```
PHASE_A1:  A_00 || A_02 || A_03          A_02 and A_03 have zero reads; safe with A_00
PHASE_A2:  A_01 || A_04                  both read accounts_dimension (A_00 done)

PHASE_B1:  B_00 || B_01                  B_00: needs A_03 done (PHASE_A1); B_01: needs A_00 done
PHASE_B2:  B_01b || B_02                 B_01b: needs B_01 done; B_02: needs B_00 done
PHASE_B3:  B_03 || C_05                  B_03: needs B_02 done; C_05: needs B_02 + B_01 done
                                          (C_05 pulled earlier than original audit — does NOT need B_03)

PHASE_C1:  C_00 || C_01                  both need B_03 done; neither reads the other's output
PHASE_C2:  C_02                          needs C_00 done (canonical_performance)
PHASE_C3:  C_03                          needs C_02 done (client_performance)
PHASE_C4:  C_04 || C_07                  C_04: needs C_02 done; C_07: needs C_03 done
PHASE_C5:  C_06 || C_08                  both need C_07 done; no shared writes
```

---

## Race Condition Check — All Phases

| Phase | Scripts | Shared write? | Verdict |
|-------|---------|---------------|---------|
| PHASE_A1 | A_00, A_02, A_03 | A_00 writes accounts_dimension; A_02/A_03 don't read it | SAFE |
| PHASE_A2 | A_01, A_04 | Both read accounts_dimension (read-only); A_01 writes advisor_assignments, A_04 writes client_dimension — no overlap | SAFE |
| PHASE_B1 | B_00, B_01 | B_00 writes canonical_holdings; B_01 writes holdings_lots — no overlap; both read accounts_dimension (read-only) | SAFE |
| PHASE_B2 | B_01b, B_02 | B_01b writes classify_watermark; B_02 writes canonical_lots — no overlap; neither reads the other | SAFE |
| PHASE_B3 | B_03, C_05 | B_03 writes canonical_account_gains; C_05 writes client_tax_liability — no overlap; C_05 reads canonical_lots_unrealized (B_02 done) | SAFE |
| PHASE_C1 | C_00, C_01 | C_00 writes canonical_performance; C_01 writes canonical_nna — no overlap | SAFE |
| PHASE_C4 | C_04, C_07 | C_04 writes aua_validation; C_07 writes account_team, rel_architect_lookup — no overlap | SAFE |
| PHASE_C5 | C_06, C_08 | C_06 writes mix_daily_summary, client_timeseries; C_08 writes advisor_fee_efficiency, advisor_fee_detail — no overlap | SAFE |

---

## Comp Tool Gaps (recommend fixing in comp-tools.yaml)

| Gap | Affected scripts | Impact |
|-----|-----------------|--------|
| FUNC-key write detection misses `put_object` calls using helper functions | B_02 (lots_realized, lots_unrealized) | Caused race condition proposal in 5f8d5c88 |
| PREFIX read vs FUNC write cross-reference | A_03 → B_00 (positions_cube), B_02 → B_03/C_05 (lots) | Implicit deps not surfaced in io manifest |

---

## gold_pipeline_deps.yaml additions recommended

```yaml
preconditions:
  B_00.canonical_holdings.py:
    - artifact_s3: "gold/timeseries/positions_cube/"
      check: exists
      reason: "B_00 reads all positions_cube partitions written by A_03; A_03 must run first"
      blocking: true

  B_03.account_gains.py:
    - artifact_s3: "gold/canonical/lots_realized/"
      check: exists
      reason: "B_03 reads canonical lots written by B_02; B_02 must complete first"
      blocking: true

  C_05.client_tax_liability.py:
    - artifact_s3: "gold/canonical/lots_unrealized/"
      check: exists
      reason: "C_05 reads canonical_lots_unrealized written by B_02; B_02 must complete first"
      blocking: true
```

---

*Delivered by 0.4.0_DS_ClientPlatform~B | 2026-04-16*

---

## Group D — Full I/O Matrix and Wave Validation

*Delivered by 0.4.0_DS_ClientPlatform~C | 2026-04-16*
*Method: comp-pipescript io on all 7 D scripts + code inspection of apparent circulars*

### Proposed D-group wave map (from 83dae334)

```
Wave D1 (concurrent, immediate): D_00, D_00c, D_03
Wave D2 (after D_00):            D_00b, D_01
Wave D3 (after D_01):            D_02
Wave D4 (after all):             D_04
```

### D-group artifact dependency matrix

| Artifact | Written by | Read by | Wave written | Wave read | Race risk |
|----------|-----------|---------|--------------|-----------|-----------|
| `gold/artifacts/clients_tab.json` | D_00 | D_04 | D1 | D4 | NONE |
| `gold/artifacts/summary/header_metrics.json` | D_00 | D_04 | D1 | D4 | NONE |
| `gold/validation/aua_certification/{*}.json` | D_00 | D_00b, D_01 | D1 | D2 | NONE — D1 completes before D2 |
| `gold/artifacts/timeseries_chart.json` | D_00b | D_04 | D2 | D4 | NONE |
| `gold/artifacts/employee_leaderboard.json` | D_00c | D_04 | D1 | D4 | NONE |
| `gold/canonical/role_aua/{*}.parquet` | D_01 (updates) | D_02 | D2 | D3 | NONE — D2 completes before D3 |
| `gold/artifacts/partner_analytics/header_metrics_{*}.json` | D_01 | D_04 | D2 | D4 | NONE |
| `gold/entities/clients/{*}/detail.json` | D_02 | D_04 | D3 | D4 | NONE |
| `gold/artifacts/firm_mix_views.json` | D_03 | D_04 | D1 | D4 | NONE |
| `gold/entities/advisors/{*}/mix.json` | D_03 | D_04 | D1 | D4 | NONE |
| `platinum/*` (21 outputs) | D_04 | terminal | D4 | — | NONE |

**Result: Zero race conditions in D-group wave map. All artifact writes complete before reads at every wave boundary.**

---

### Wave gate validation

**Gate D1 → D2: D_00 must complete before D_00b + D_01 start**

Gate artifact: `gold/validation/aua_certification/{*}.json`
- D_00 WRITES aua_certification → D_00b, D_01
- D_00b READS aua_certification ← C_02 (primary), D_00, D_01 (supplement)
- D_01 READS aua_certification ← C_02 (primary), D_00

CONFIRMED hard gate. C_02's cert is always present as primary; D_00's cert entry is what D2 scripts wait for.

Note: D_00b also lists D_01 as a cert source, but D_01 is in the same wave. C_02 satisfies D_00b's primary cert read — D_01's entry is a supplemental cross-check from prior run. No functional dep on D_01's current-run cert. D_00b and D_01 safe to run concurrently in D2.

**Gate D2 → D3: D_01 must complete before D_02 starts**

Gate artifact: `gold/canonical/role_aua/{*}.parquet`
- D_01 WRITES canonical_role_aua updates → D_02
- D_02 READS canonical_role_aua ← C_01b (primary), D_01 (updates)

CONFIRMED hard gate. D_01 updates canonical_role_aua partitions during its partner analytics run; D_02 must read the updated versions for timeseries accuracy.

**Gate D3 → D4: all D1/D2/D3 must complete before D_04 starts**

D_04 reads: clients_tab (D_00/D1), header_metrics (D_00/D1), timeseries_chart (D_00b/D2), employee_leaderboard (D_00c/D1), partner_analytics (D_01/D2), client_detail (D_02/D3), firm_mix_views (D_03/D1), advisor_mix (D_03/D1). All gates confirmed.

---

### Apparent circulars — resolved

| Pair | Shared artifact | Resolution |
|------|----------------|------------|
| D_00 ↔ D_01 | aua_certification | D_00 reads D_01's cert as prior-run supplement; C_02 is current-run primary. D_00 in D1, D_01 in D2 — no same-wave race. SAFE. |
| D_01 ↔ D_02 | canonical_role_aua | C_01b is current-run primary writer. D_01 reads C_01b partitions (not D_02's). D_02 reads D_01's updates after D2 gate. Serial — SAFE. |
| D_01 ↔ D_04 | partner_analytics | D_01 reads prior-run D_04 output (rolling-window delta for period-over-period). Not a runtime circular — temporal pattern. SAFE. |

---

## Cross-Group Boundary Edges

### A → B (validated against ~B's I/O matrix)

| Artifact | A writer | B reader | Safe? |
|----------|----------|---------|-------|
| `accounts_dimension_latest.parquet` | A_00 | B_00, B_01, B_02 | YES — A completes before B |
| `positions_cube/{*}.parquet` | A_03 | B_00 (implicit — not in comp manifest, see FINDING 2) | YES — A completes before B. **Recommend: add to gold_pipeline_deps.yaml** |

A_01, A_02, A_04 write no B-consumed artifacts. Only A_00 and A_03 gate B start.

### A → C (cross-group skip, bypasses B)

| Artifact | A writer | C reader | Safe? |
|----------|----------|---------|-------|
| `accounts_dimension_latest.parquet` | A_00 | C_00, C_01, C_02, C_03, C_05, C_06, C_07 | YES — A completes before C (by full-phase gate) |
| `advisor_assignments_history.parquet` | A_01 | C_08 | YES |
| `fee_rate_history.parquet` | A_02 | C_08 | YES |

C_04 and C_08-via-A_00 are not A→C direct; C_04 reads only aua_validation (S3-dynamic). A_03 and A_04 write no C-consumed artifacts.

### B → C (validated against ~B's I/O matrix, with C_03 correction)

| Artifact | B writer | C reader | Safe? |
|----------|----------|---------|-------|
| `canonical_holdings/{*}.parquet` | B_00 | C_02, C_06 | YES — B completes before C |
| `canonical_account_gains/{*}.parquet` | B_03 | C_00, C_01, C_02, **C_03** | YES — C_03 read verified at C_03.account_performance.py L69/L114 (CANONICAL_ACCOUNT_GAINS_PREFIX import + `_list_prefix` call) |
| `holdings_lots/{*}.parquet` | B_01 | C_05 (HOLDINGS_LOTS_PREFIX) | YES |
| `canonical_lots_unrealized/{*}.parquet` | B_02 | C_05, B_03 | YES — PHASE_B2 ensures B_02 before B_03/C_05 |
| `canonical_lots_realized/{*}.parquet` | B_02 | B_03 | YES — PHASE_B2 serial |

C_05 pulled into PHASE_B3 by ~B (correct — C_05 doesn't need B_03, only B_02 + B_01). No race with B_03.

**Correction to ~B's Group B row 40 I/O matrix:** `canonical_account_gains/{*} → C_00, C_01, C_02, C_03` (original row listed only C_00–C_02; C_03 row 49 confirms the read).

### A → D (cross-group skip, bypasses B and C)

| Artifact | A writer | D reader | Safe? |
|----------|----------|---------|-------|
| `accounts_dimension_latest.parquet` | A_00 | D_00, D_00b, D_01 (direct imports `ACCOUNTS_DIMENSION`) | YES — full-phase gate |
| `client_dimension.parquet` | A_04 | **ALL 7 D scripts** (D_00, D_00b, D_00c, D_01, D_02, D_03, D_04 — direct imports `CLIENT_DIMENSION`) | YES |
| `advisor_assignments_history.parquet` | A_01 | D_00c, D_02 | YES |
| `fee_rate_history.parquet` | A_02 | D_00c, D_02 | YES |

**Correction to ~B's Group A row 26 I/O matrix:** `accounts_dimension → A_01, A_04, B_00, B_01, B_02, C_00–C_03, C_05–C_07, D_00, D_00b, D_01` (original row missed D_00/D_00b/D_01; verified via direct `ACCOUNTS_DIMENSION` imports in D_00 L49, D_00b L39, D_01 L74).

A_04's client_dimension reaches every D script directly — this was the broadest A→D fan-out and was under-specified in ~B's row 30 ("D scripts only"). Enumerated above.

### C → D (full boundary matrix)

| Artifact | C writer | D readers | D wave | Safe? |
|----------|----------|-----------|--------|-------|
| `client_performance.parquet` | C_02 | D_00, D_00b, D_01, D_03 | D1, D2 | YES |
| `aua_certification/{*}.json` | C_02 | D_00, D_00b, D_01 | D1, D2 | YES |
| `account_performance.parquet` | C_03 | ALL D scripts | D1–D4 | YES — broadest gate; C_03 must complete |
| `client_tax_liability.parquet` | C_05 | D_00, D_02 | D1, D3 | YES |
| `mix_daily_summary.json` | C_06 | D_03, D_04 | D1, D4 | YES |
| `client_timeseries/{*}.json` | C_06 | D_04 | D4 | YES |
| `account_team.parquet` | C_07 | D_00, D_00b, D_00c, D_01, D_02, D_04 | D1–D4 | YES |
| `rel_architect_lookup.parquet` | C_07 | D_00, D_00b, D_00c, D_01, D_02, D_03 | D1–D3 | YES |
| `advisor_fee_efficiency.json` | C_08 | D_04 | D4 | YES |
| `advisor_fee_detail/{*}.parquet` | C_08 | D_00c, D_02 | D1, D3 | YES |
| `canonical_role_aua/{*}.parquet` | C_01b | D_01, D_02 | D2, D3 | YES |

**C→D is a hard boundary. `account_performance` (C_03) is consumed by every D script — C_03 is the most critical C→D gate. No D script can start before all C completes.**

---

## Combined Validated Wave Map (Full Chain)

```
PHASE_A1:  A_00 || A_02 || A_03
PHASE_A2:  A_01 || A_04

PHASE_B1:  B_00 || B_01
PHASE_B2:  B_01b || B_02
PHASE_B3:  B_03 || C_05               (C_05 pulled forward — no B_03 dep)

PHASE_C1:  C_00 || C_01
PHASE_C2:  C_02
PHASE_C3:  C_03
PHASE_C4:  C_04 || C_07
PHASE_C5:  C_06 || C_08

PHASE_D1:  D_00 || D_00c || D_03
PHASE_D2:  D_00b || D_01              (after D_00)
PHASE_D3:  D_02                       (after D_01)
PHASE_D4:  D_04                       (after all D1–D3)
```

**Total phases: 13. Current sequential execution: 31 scripts in series.**
**Critical path: A_00 → B_00 → B_02 → B_03/C_05 → C_02 → C_03 → C_07 → C_08 → D_00 → D_01 → D_02 → D_04**

---

## Dispatcher Gate Requirements

| Gate | Condition | Unblocks |
|------|-----------|---------|
| A_00 complete | accounts_dimension written | A_01, A_04, B_00, B_01 |
| PHASE_A1 complete | A_00 + A_02 + A_03 all exit 0 | B_00 (needs A_03) |
| B_00 complete | canonical_holdings written | B_02, B_03 |
| B_01 complete | holdings_lots written | B_01b, C_05 |
| B_02 complete | canonical_lots_unrealized/realized written | B_03, C_05 |
| PHASE_B3 complete | B_03 + C_05 exit 0 | C_00, C_01 |
| C_00 complete | canonical_performance written | C_02 |
| C_02 complete | client_performance + aua_certification written | C_03, C_04 |
| C_03 complete | account_performance written | C_07 (and all D via C group gate) |
| C_07 complete | account_team + rel_architect_lookup written | C_06, C_08 |
| All C complete | All C exits 0 | D_00, D_00c, D_03 (PHASE_D1) |
| D_00 complete | aua_certification (D gate) written | D_00b, D_01 (PHASE_D2) |
| D_01 complete | canonical_role_aua updated | D_02 (PHASE_D3) |
| PHASE_D1–D3 complete | All exit 0 | D_04 (PHASE_D4) |

---

## Outstanding Comp Tool Gaps (combined, recommend fixing)

| Gap | Scripts affected | Impact |
|-----|-----------------|--------|
| FUNC-key write detection misses `put_object` via helper functions | B_02 (lots_realized, lots_unrealized) | Caused race condition in 5f8d5c88 |
| PREFIX read vs FUNC write cross-reference | A_03→B_00 (positions_cube), B_02→B_03/C_05 (lots) | Implicit deps not surfaced |
| D_01 partner_analytics prior-run read not flagged as rolling-window | D_01←D_04 | Could be misread as circular dep |

*Full deliverable: 0.4.0_DS_ClientPlatform~B (Groups A/B/C) + 0.4.0_DS_ClientPlatform~C (Group D + cross-group) | 2026-04-16*
