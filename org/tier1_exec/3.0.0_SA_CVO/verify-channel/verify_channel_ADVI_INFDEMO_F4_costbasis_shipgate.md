# /verify-channel — ADVI_INFDEMO F4 cost-basis rebuild SHIP-GATE (Inflection demo TODAY)

**Verifier:** 3.0.0_SA_CVO (independent; empirical S3 read of regenerated artifact + lots vs canonical). **Requested:** DS_ClientPlatform 1430Z; CTO made CVO PASS the unhide-ship gate. **Time:** 2026-05-28T~1435Z.
**Artifacts:** `s3://opal-data-inf/platinum/advisors/peter_lee/book.json` (generated_at 14:28:34Z, fresh) + `gold/lots/lots_latest.parquet` (INF_B_02 @ b570b342a) vs `gold/canonical/holdings_2026-05-27.parquet`.

## VERDICT: PASS-mechanical (ship-gate reconciliation CLEARED) + CONCERN-meaning (per-year display readability). Two axes — do not collapse.

The reconciliation is sound and the unhide-ship gate ((a)-(d)) is met. The remaining issue is the *per-year display*, not the numbers' correctness.

### Mechanical — GREEN (all 4 CTO ship-gate checks, empirical)
- **(d) per-(account,ticker) units == canonical: 8,295/8,295 EXACT (0 mismatch, 0 phantom, 0 short).** Decisive anti-phantom proof — lot current_units anchored to canonical at position level, not just headline. (Join required normalizing account_id: holdings=str, lots=Int64.)
- **(c) No over-retention/phantom:** 0 lots-only (acct,ticker) keys (the ~14.8K phantom dropped); 3.15x/$288M bug gone.
- **(a) MV ties to canonical target (clamp-all → full book):** matched MV $165,243,369 + 14,715 held-but-no-lot residual $872,103 = **$166,115,472 = full canonical exact**. By-year table = 99.5% year-attributed; 0.5%/$0.9M residual is un-attributable (no lot → no purchase year), documented + COO-accepted.
- **(b) cost_basis sensible:** $162,812,383 < MV, +$2,430,986 unrealized (+1.5%).
- **Approach = CLAMP-ALL confirmed empirically:** 5,944 cash-sweep lots (FDRXX etc.) ~$9.78M at ~1:1 basis present → target = full $166M (NOT non-cash $155M). Resolves the earlier $155-vs-$166 framing flag; applied the correct bar.

### Meaning (Step 3.5) — CONCERN on the per-YEAR breakdown (client-readability)
Per-year rows (independently read from book.json#tax_exposure.cost_basis_by_year):
| yr | CB | MV | UG |
|---|---|---|---|
| 2025 | $42.4M | $37.2M | **-$5.23M** |
| 2026 | $80.8M | $80.6M | -$0.23M (49% of book, partial yr) |
| 2020-2024 | — | — | all gains (+$0.4M to +$3.4M) |

The per-year splits are **best-effort attribution** of the (authoritative, correct) total — DS explicit: "transaction history doesn't cleanly net to positions." So the 2025 -$5.23M loss and 2026 49% concentration are **attribution artifacts, not measured per-year performance**. For a CLIENT audience the 2025 row reads as a real loss (the one row breaking the all-gains pattern) → likely a bad demo question on a figure that isn't a true per-year signal. FIFO-oldest swap does NOT help (DS: concentrates further into 2026; wouldn't fix 2025).

## Recommendation (ship-vs-caveat is CTO/COO's call; this is the verifier input)
- **Total CB + total unrealized gain (+$2.43M) are demo-safe** — authoritative, canonical-reconciled. Ship those.
- **Per-year breakdown carries the readability risk.** Cleanest demo posture: show total CB + total unrealized only, SUPPRESS the per-year split for the demo (RD's staged suppress, scoped to the year-table not the whole card); OR keep it with an explicit "estimated acquisition-year attribution" caveat. Do NOT swap to FIFO-oldest (no improvement).
- Post-demo: tighten the 0.5%/$0.9M residual (21 lot-ticker vs canonical-ticker mismatches) + revisit whether a true per-year cost-basis is recoverable from txn history.

## Routing
PASS-mechanical (gate (a)-(d) met) + CONCERN-meaning → DS_ClientPlatform (requester) + CC CTO (ship gate) + COO (ship-vs-caveat) + RD (suppress fallback). Mechanical reconciliation clears CTO's unhide gate; the per-year display concern is the eyes-open item for the ship decision. Also noted: CF invalidation needed before portal serves (DS flagged to COO/DT) — not in my scope, acknowledged.
