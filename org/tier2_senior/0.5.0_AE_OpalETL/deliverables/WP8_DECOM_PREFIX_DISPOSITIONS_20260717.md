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

## D-sequence tracked item -- step-5 PRODUCER retirement (routed to me, CTO 214039Z via DS~A)

- **WHAT:** retire the producer `convert_schwab_trn_to_nna_silver.py` (step 5 of `/49-schwab-conv`, AE-owned). **I (pod AE) execute the skill edit** when gated -- not a DS action; not a prefix-retire.
- **WHY UNBLOCKED:** WP8 trn_nna option-b D1 landed + CTO-accepted; C_01 re-derives NNA gold-side from monolith `fact_trn` (37bd2fee1). AC1 parity = 26,504 (account,date) cells / 0 mismatch over 495 dates (2024-07-08..2026-07-15), output-identical -> monolith path fully replaces the legacy converter for the ONLY prod reader (C_01).
- **HARD CONSTRAINT 1 -- PRESERVE, do NOT secure-delete:** the frozen legacy `opal-data-bd/schwab/silver/trn_nna/` partitions STAY (reachable via `SCHWAB_FLOW_SOURCE=legacy` env override) as the historical-rebuild fallback for pre-2024-07-08 (57 days / +$18.07M, accepted immaterial but preserved). Retire the PRODUCER, keep the ARTIFACTS. (Distinct from CELL 1's `opal-data-schwab/03_silver/TRN_NNA` retire -- different bucket.)
- **HARD CONSTRAINT 2 -- GATED ON FLIP EVIDENCE:** the `/49-schwab-conv` retirement arc (L5b monolith re-point eac5476c1 + the bd gold re-key/flip evidence) must land + be CTO-accepted FIRST. Flip evidence still unread at CTO's gate -> **step-5 removal HELD until that clears.** Retiring the producer before the flip is proven is premature.
- **Grounding:** `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/WP8_TRN_NNA_OPTIONB_PARITY_20260717.md`.

## Cross-refs
- Related dead-UI-channel retirement (`canonical-schwab-si2-download-schedule` EventBridge, ENABLED, drives frozen GUI channel): my cell-3 PART-2, source-grounded 195615Z; retires with the D5 battery (separable from the live monolith REST pull -- `monolith-daily-schedule`).
- 0.6.2 cell-3 SI2 code re-home: additive IAM grant GO=(A) landed + independently validated + RAVC-closed (221511Z; new home has all 9 artifacts, box-read 35842B rc=0, my simulate=allowed, never-widen controls). **Literal-flips/cutover GO'd NOW (222210Z, Andrew-prompted)** -- REVERSING my earlier "held to D1" bundling: the code-read flip is ORTHOGONAL to the D1 parity clock (it changes only WHERE the box reads its byte-identical code, not what the pull writes or the silver/parity path). Guardrails: byte-identity (repo==old==new, 35842B) + prove-on-fire (landed bytes from the new-home read) BEFORE any grant retire. **STILL D5-gated (NOT pulled forward):** the old SchwabOpsCodeRead grant retirement on opal-data-schwab + the opal-data-schwab DATA decommission (those keep the D1 + full-sequence gate).
- D1 two clean cycles (~07-18 date=2026-07-17 + ~07-21 date=2026-07-20, pending CTO date-ratify) gate the cutover + my SI2 re-home GO.
