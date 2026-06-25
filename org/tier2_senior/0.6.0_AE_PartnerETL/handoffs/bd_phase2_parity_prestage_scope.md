# BD Phase-2 decommission — parity PRESTAGE scope (derived layers only; held-away EXCLUDED+RETAINED)

**Author:** 0.6.0_AE_PartnerETL · **Date:** 2026-06-25 · **For:** COO (RAVC) / CVO (held-away gate owner) / 0.4.0_DS (DATA_ANALYTICS.A1 silver-dim owner) / CTO
**Scope GO:** COO 2026-06-25 (with CVO's held-away guardrail 171138Z). **NOT** the decommission (CVO+Andrew-gated). **NOT** the held-away path. **NOT** a teardown trigger. This is the un-gated PROOF-PREP that BD's DERIVED layers can go Schwab-native.

## The load-bearing carve-out (CVO held-away gate — bake this into everything)

BD plays TWO roles for 49F; only ONE is in scope:

| BD role | Schwab-direct replacement? | Prestage disposition |
|---|---|---|
| **DERIVED / RECONSTRUCTION** (reconcile B_00, FIFO lots B_01/B_02, A_03 cube) on **Schwab-CUSTODIED** positions ($1.63B) | YES — the DATA_ANALYTICS.A1 6 silver dims (custodian-native, ← RPS/ULN/RLD/TRN) | **IN SCOPE — prove native == BD-derived within tolerance** |
| **AGGREGATION** of HELD-AWAY / non-Schwab custody (Fidelity ~$200M) | NO — no Fidelity raw feed exists; BD is the SOLE ingest path | **EXCLUDED + RETAINED.** Never parity-targeted; the AUA aggregation KEEPS BD for the held-away portion. Full-book $1.83B = $1.63B Schwab + ~$200M held-away. |

A full BD teardown would silently drop the served ~$200M held-away. So: parity proves the DERIVED layers replaceable; the held-away aggregation is a NAMED, RETAINED exclusion in every parity comparison (carve held-away rows OUT before diffing — their absence from the Schwab-direct side is BY DESIGN, not a parity failure).

## Parity pairs (Schwab-CUSTODIED subset only)

Each BD-derived GOLD artifact ↔ its A1 Schwab-direct SILVER-DIM equivalent. (A1 v0.3: FIFO is NOT fully retired — B_01 repositions to a VALIDATION lane; this prestage IS that validation lane formalized.)

| BD-derived (gold) | A1 Schwab-direct (silver dim ← raw) | Join keys (A1 v0.2 LOCKED) | Tolerance |
|---|---|---|---|
| B_00.canonical_holdings (custodian reconcile) | fact_position + dim_account (← RPS) | account_id (10-digit padded) + cusip | position MV: epsilon_usd float-noise floor (per-position); count exact on the Schwab subset |
| B_01.holdings_lots + B_02.canonical_lots (FIFO unrealized) | fact_lot_unrealized (← ULN; surrogate key REQUIRED) | lot surrogate + lot_lineage_id hash (A1 v0.3 FIFO-vs-custodian key) | unrealized G/L: epsilon; lot-count within custodian-latency band (the FIFO-vs-custodian sanity-check delta A1 expects, NOT zero) |
| B_02.canonical_lots (FIFO realized) | fact_lot_realized (← RLD; key=(close_event_id,open_event_id)) | (close_event_id, open_event_id) | realized G/L: epsilon; key-set symmetric-diff = 0 on the Schwab subset |
| A_03.positions_cube (FIFO-derived) | joins over fact_position/fact_lot_* | account_id + cusip | derived-from-the-above; inherits their tolerance |
| (fee rate / dim_fee) | dim_fee — **the one NON-custodian gap** (fees aren't Schwab-raw; now fed by the bd-49f-fees-runner REST path I built) | account_id | fees stay a BD/REST feed -> NOT a decommission candidate (note, not a parity pair) |

**Subset filter (the held-away carve-out, mechanical):** before every diff, restrict BOTH sides to Schwab-custodied rows (custodian == Schwab / account in the Schwab dim_account set); the held-away/Fidelity rows are excluded from the parity numerator+denominator. Report the held-away row/AUA count separately as the RETAINED residual (proves the carve-out is real, not silent).

## Verifier prep (what to build when the actual verifier is GO'd — NOT now)

- A `bd_phase2_parity.py`-class scorecard (mirrors the gldinc shadow/SS4c scorecard shape: key_set_symmetric_diff / row_count_delta / max_abs_diff / within_eps): per pair, on the Schwab subset, Schwab-direct vs BD-derived -> a parity scorecard to `gold/_parity/phase2_schwab_native/{date}/`.
- Piggyback the nightly (NFRA_COSTAWS: no manufactured run); emit a metric + a divergence/absence alarm (the SS4c discipline). EGRESS = the now-restored opal-critical-surface-alerts.
- Run as an EVIDENCE-ACCUMULATION lane (like the gldinc shadows): N clean nights on the Schwab subset = the evidence the derived layers CAN go native. The actual decommission stays CVO+Andrew-gated on (Fidelity-feed-exists OR Andrew-elects-the-drop).

## Boundaries (explicit)
- This doc is SCOPE + verifier PREP only. NOT the verifier build, NOT the decommission, NOT touching the held-away path.
- DS (0.4.0) owns DATA_ANALYTICS.A1 (the silver dims + the FIFO validation lane) — this parity-prestage is the AE-side decommission-evidence framing OF A1's validation lane; coordinate the join-key/tolerance specifics with DS (A1 is Andrew-direct, actively v0.4). The verifier build, when GO'd, is a joint AE(harness)/DS(lib) split like SS4c.
- CVO owns the held-away gate; this scope encodes the carve-out CVO set.
