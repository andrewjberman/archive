# ADVI_BREAKS — COO Decomposition (P0 Andrew-sovereign gate)

**Source PRD:** docs/architecture/ADVI_BREAKS_PRD.md (CTO d2cae58f9)
**Decomposed by:** 2.0.0_SA_COO 2026-06-30T12:52Z
**Gate:** DATA_ANALYTICS + DATA_SSOTMG HELD until all 3 pipelines GREEN (§4 axes A-F) + CVO confirm (TO-5) + prevention alarm live (TO-6).
**Lane map (Andrew-direct):** base `0.4.0_DS` -> Cottonwood · `~A 0.4.0_DS~A` -> Inflection · `~B 0.4.0_DS~B` -> 49F.

## Sequencing principle (methodical, Andrew-direct)
Two-stage per pipeline: **(1) DIAGNOSE (read-only, dispatch now)** -> **(2) FIX (gated on diagnosis + CTO/COO coordination; §8 — no fix may re-introduce a 2nd writer or path divergence).** No prod write fires before its diagnosis grounds the mechanism (Rule 22) and CTO+COO coordinate it. inf (TO-1->TO-2) is the FIRST critical path (it's the proven RED + the worst — schema regression + freeze on the live partner header).

## TO map (owner = Andrew lane + AE infra pair)

| TO | Pipeline | Stage | Owner(s) | Status | Gate / dep |
|---|---|---|---|---|---|
| **TO-1** | inf | DIAGNOSE | `~A` (DS inf) + AE | READY — pending ~A live | none; FIRST |
| **TO-2** | inf | FIX | `~A` + AE | HELD | gates on TO-1 source-confirm + CTO/COO coord |
| **TO-3** | 49F | DIAGNOSE (full §4 sweep) | `~B` (DS) + AE | **DISPATCH NOW** | ~B live + held for GO |
| **TO-4** | COT | DIAGNOSE (finish as_of-resolution trace) | `base` (DS) + AE | **DISPATCH NOW** | base live + half-done; read-only |
| **TO-4b** | COT | FIX (as_of-pin) | `base` + AE | HELD | gates on TO-4 mechanism-pin + coord |
| **TO-5** | all 3 | independent freshness+parity verdict (gate release) | CVO `3.0.0` | **DISPATCH NOW** (baseline) | runs continuously; final verdict gates on TO-2/3/4 GREEN |
| **TO-6** | prevention | served-key single-writer + parity alarm (COMPDIFF freeze-monitor generalized) | `0.8.0_AE~B` + AE | spawn-req'd | parallel; gate-close requires it live |

## Capacity needed (spawn-req to MSTR)
- `~A 0.4.0_DS~A` — Andrew bringing on; inf TO-1 ready the moment it registers (verify via broker, not marker — Andrew-launched = marker-less per MSTR 124840Z).
- **AE pair**: `0.7.0_AE_CloudOps` (S3 producer-race / trigger / EventBridge infra — TO-1/2/3/4 infra legs) + `0.8.0_AE_CloudComp~B` (canonical-format trace + TO-6 alarm; built the freeze-monitor). Neither live — spawn-req this turn.

## Per-pipeline diagnosis scope (§4 A-F, bind to LIVE/SERVED)
- **inf (TO-1):** source-confirm the 132-byte stub producer + its trigger of `opal-data-inf/platinum/firm/header_metrics.json`; why introduced (canonical convergence?); should it write this key at all. Axes B (single-writer) + F (trigger) + E (schema) are the RED ones.
- **49F (TO-3):** full A-F on the 49F served chain (Schwab custodian-native; served = `platinum/firm/header_metrics_fresh.json` total_aua per 49f_parity_config.yaml). Hypothesis: inf-class (shared-canonical 2nd-writer/path/trigger) — confirm or refute with S3 version/size forensic + chain map.
- **COT (TO-4):** finish the read-only producer as_of-RESOLUTION trace (where data_as_of pins 06-26 vs fresh 06-29 silver — the DATEMODE-B holdings-leg seam, `org/seams/cottonwood-bronze-silver-gold-platinum-aua-freeze.md`). Already half-done (base grounded: 728B one-writer, NOT a clobber). Pin the exact code mechanism.

## Exit
All 3 GREEN on A-F + CVO TO-5 verdict + TO-6 alarm live -> ADVI_BREAKS closes -> DATA_ANALYTICS + DATA_SSOTMG unblock.
