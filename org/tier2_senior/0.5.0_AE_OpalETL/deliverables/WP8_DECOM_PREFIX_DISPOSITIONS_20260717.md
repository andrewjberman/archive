# WP8-DECOM -- opal-data-schwab prefix dispositions (the ~20:30Z batch)

**Owner:** 0.5.0_AE_OpalETL (WP8-DECOM lead, Andrew-approved 6024e85ed).
**Grounding:** my 4-cell census/liveness pass (185103Z, step-1 ledger @ 519584d15) -- structure + liveness, zero P2 reads, D4 window respected.
**Ruling:** 1.0.0_SA_CTO SIX-PREFIX BATCH RULING (203910Z). This doc ledgers his dispositions "that way" per his instruction.

## Cell dispositions

| Cell | Prefixes | Disposition | Sequence / gate |
|---|---|---|---|
| **CELL 1** | `03_silver/` (TRN, TRN_NNA, account_xref, scripts) | **RETIRE** | Dead: consumers repointed (account_xref -> opal-data-bd 2026-06-29 build_dim_account.py:51; TRN_NNA retire ruled 182433Z; TRN superseded by monolith fact_trn), frozen 2026-04-20/21. Rides the normal **D5 read-only -> D6 Andrew-delete-word** sequence. No special handling. |
| **CELL 2** | `02_anonymized/` + `03_mappings/` (the ANONYMIZER cell) | **HOLD -- do NOT batch-retire** | (a) producer DORMANT (0 invocations/7d) but "dormant" != "confirmed-superseded" -- confirm nothing in the monolith path still needs anonymization; (b) **`03_mappings` = the CLIENT RE-IDENTIFICATION KEY** (cross-firm-bucket-read-deny.tf:45), security-sensitive. Retiring it is a **SECURE-DELETE (crypto-erase / verified object deletion) needing EXPLICIT Andrew sign-off + a security disposition**, separate from the D-series copy batch. CTO surfacing CELL 2 to Andrew as its own security cell. **I leave 02_anonymized / 03_mappings untouched: do not copy, do not open, do not retire.** |
| **CELL 3** | `_archive/` | **RETIRE** | Dead-archive, no producer/consumer. Rides the D5 -> D6 sequence. |
| **CELL 4** | `backfill/` + `01_raw_quartz_validation/` + `quartz/` (QUARTZ SI2 spike) | **HOLD -- CANNOT retire (LIVE)** | LIVE EC2 `i-0f3d57a97f14727af` (running 18d, quartz-si2-spike-role, writing `backfill/08335338/`). A LIVE-INSTANCE disposition, not a prefix-retire. Sequences: (1) 0.6.2 cell-3 code re-home lands (CTO approved; box pulls code from the monolith, not the dying bucket) -> (2) **0.7.0_AE_CloudOps** assesses + stops/repoints the running spike -> (3) THEN D5. **Routed to 0.7.0** (running-instance owner). CTO flagging the 18-day unmanaged spike to Andrew as a cost/ownership item. Its activity is D4-window attributable (quartz-si2-spike-role, enumerable) -- **EXCLUDE from any zero-reader verdict.** |

## NET
- **RETIRE on the D-sequence:** CELL 1 + CELL 3 (D5 read-only -> D6 Andrew delete word).
- **HELD (security, Andrew):** CELL 2 anonymizer -- secure-delete cell, CTO->Andrew.
- **HELD (live, 0.7.0):** CELL 4 quartz spike -- 0.7.0 stop/repoint after the 0.6.2 code re-home, then D5.

## Cross-refs
- Related dead-UI-channel retirement (`canonical-schwab-si2-download-schedule` EventBridge, ENABLED, drives frozen GUI channel): my cell-3 PART-2, source-grounded 195615Z; retires with the D5 battery (separable from the live monolith REST pull -- `monolith-daily-schedule`).
- 0.6.2 cell-3 SI2 code re-home: additive IAM grant GO=(A) decoupled prep (214213Z); literal-flips + cutover HELD to D1 GO.
- D1 two clean cycles (~07-18 date=2026-07-17 + ~07-21 date=2026-07-20, pending CTO date-ratify) gate the cutover + my SI2 re-home GO.
