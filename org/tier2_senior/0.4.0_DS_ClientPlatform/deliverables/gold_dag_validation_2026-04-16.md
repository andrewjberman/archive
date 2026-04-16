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
| A_00 | accounts_dimension (external/silver) | accounts_dimension → A_01, A_04, B_00, B_01, B_02, C_00–C_03, C_05–C_07 |
| A_01 | accounts_dimension (A_00) | advisor_assignments_history → C_08, D_00c, D_02 |
| A_02 | (none) | fee_rate_history → C_08, D_00c, D_02 |
| A_03 | (none) | positions_cube/{*}.parquet → B_00 (implicit — see below) |
| A_04 | accounts_dimension (A_00) | client_dimension → D scripts only |

### Group B

| Script | Reads | Writes |
|--------|-------|--------|
| B_00 | accounts_dimension (A_00), positions_cube/ (A_03), canonical_prices (silver), schwab_bd_mapping, canonical_holdings/{*} (prior run) | canonical_holdings/{*} → B_02, B_03, C_02, C_06; canonical_holdings_gaps/{*}; watermarks.json |
| B_01 | accounts_dimension (A_00) | holdings_lots/{*}, holdings_lots_shadow/{*}, holdings_lots_backfill/{*} → C_05 (via prefix) |
| B_01b | holdings_lots/ (B_01), classify_watermark | classify_watermark |
| B_02 | canonical_holdings/{*} (B_00), schwab ULN/ULT/RLD prefixes, canonical_prices, canonical_lots_realized/{*} (prior), canonical_lots_unrealized/{*} (prior) | **canonical_lots_unrealized/{*} → B_03, C_05; canonical_lots_realized/{*} → B_03** (comp WRITES: none detected — gap, verified L617–624) |
| B_03 | canonical_holdings/{*} (B_00), canonical_lots_realized/ (B_02), canonical_lots_unrealized/ (B_02) | canonical_account_gains/{*} → C_00, C_01, C_02 |

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

*~C owns Group D + cross-group boundary edges. Merge into combined deliverable before 04:00 UTC.*

*Delivered by 0.4.0_DS_ClientPlatform~B | 2026-04-16*
