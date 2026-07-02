# ADVI_ETLFIX Phase-1 TO-pack -- WS-2/3/4 durable TOs (AUTHORED, dispatch-HELD until the un-freeze lands)

**Authored:** 2.0.0_SA_COO 2026-07-02, per CTO handoff (author-now-lock-the-shape) + Andrew drive-to-completion. **Dispatch discipline (CTO-directed):** DO NOT dispatch the AE/DS durable TOs until the un-freeze LANDS (don't split 0.6.1/DS~A/0.6.0/0.6.2 mid-firefight). WS-1 = fold-as-record (inline firefight guards). WS-5 = CTO-authored post-un-freeze (once defer_guard_read_bronze concretizes). All arch-gates RULED (CTO 150959Z); each converter/design RAVCs CTO on commit per GATE-1.

**Leash (every TO):** degrade LOUD not catastrophic not silent | never-widen + single-writer + parity-to-cent + no-clobber | ground on SERVED/deployed not self-report (Rule 22) | freshness-SLA-is-a-GATE | firm-separation | don't over-build a sunset source | comp-tools mandate (comp-freshness/comp-pipescript io+deployed/comp-iam/comp-blast) + machine-checkable ACs.

---

## WS-1 -- Inflection ETL robustness (FOLD-AS-RECORD; inline in firefight)
Record-only (no new dispatch): txn-pull ext-fix (6aaa395f5) + txn converter DEFER-guard + CTO-policy detection-limb (b7dc964db) + perf-silver DEFER-guard (c6332e5dd, inline mirror). REMAINING Phase-1 (post-un-freeze, DS~A):
- **positions_mv guard = DEFER-with-HONEST-VINTAGE (CTO arch-sharpening 161646Z -- the load-bearing precision):** positions_mv feeds the SERVED AUA (headline number), so NEITHER blind-DEFER (carry-forward + stamp fresh-today = WRONG-FRESH silent AUA, BAD) NOR block-on-stale (one dim freezes the whole page, BAD). CORRECT: DEFER carry-forward (chain completes, page refreshes -- no whole-page-freeze) BUT the served AUA data_as_of HONESTLY reflects the carried-forward positions vintage (never claims fresher than actual positions -> HONEST-STALE-visible, not WRONG-FRESH-silent) + WS-4 content-oracle catches the non-advancing data_as_of (WS-1<->WS-4 PAIRED) + ChainStepDegraded fires + N=1 ceiling BLOCKs if >1 trading day. Load-bearing req = HONEST VINTAGE. (NOTE: this is the DURABLE guard; the CURRENT un-freeze bar stays fresh-positions per 0.6.1 -- today WANTS fresh, not honest-stale.)
- the DRY shared-helper refactor (defer_guard_read_bronze in _orion_api_silver_lib.py -- multi-homed, post-un-freeze, coordinate the txn guard); the full 63-step de-convert CLASS-B audit (class=4 dims + cron-backing UNRESOLVED per DS~A). + per-INF freshness-SLA (folds into WS-4). CTO GATE-1 (robustness contract) applies.

## WS-2 -- 49F source resilience durable [DISPATCH-HELD]
### WS-2a BD-auth-durable -> 0.7.0_AE~A (lead) + 0.6.0_AE + 0.6.2_AE
Scope: (1) FEED-REPOINT -- productionize 0.6.0's manual cookie-REST path (feeds off the dead runner.ts UI-export -> the working .bd.identity cookie-REST pull) = ADVI_BDAPIMIG.P1 (0.6.0 P1.ae-productionize-runner + 0.6.2 P1-DURABLE, both pending TOs -> activate). (2) 0.7.0~A kill-cookie resilience VERIFY-GATE (deliberately kill the cookie -> prove re-auth-at-ETL re-mints+ingests) -- POST-0.6.0-backfill-clear, coordinated. (3) 0.6.2 Kimi-guard box-rollout (5d9cc4649) -- post-bd-P0-clear, COO-GO'd S3->box pull.
AC: the scheduled bd feeds pull daily WITHOUT a manual re-auth (durable autologin proven on N nightlies); a source-freeze fires a loud per-partner alarm (WS-4). Arch-gate: CTO (already ruled; RAVC on commit).

### WS-2b Schwab-ingest-durable -> 0.6.2_AE (lead) + 0.4.0_DS~A
Scope (CTO 4 decisions RULED): C1 = isolated-retireable EB converter-chain (D-A: dedicated instance mirroring canonical-schwab-runner, NOT folded into SI2/canonical, independently retireable at the SSOTMG cutover). C2 = SI2->01_raw repoint, single-source-NO-permanent-fork (D-B: prefer wait-for-N=5; timeboxed-tracked interim only if durability outranks, un-fork committed -- the wait-vs-expedite is Andrew's Caution-B call, 0.6.2 lane). C3 = TRN-A -> S3 01_raw/ (D-C APPROVED, DS~A rule-13, scoped edit + parity-reverify silver byte-unchanged). D-D = BUILD-THE-BRIDGE (done: SI2 sync-race root-fix v1.1.0), do NOT accelerate SSOTMG. + DS~A multi-prefix-deploy hardening for the PULL scripts (orphan-removal, 8 multi-homed scripts -> single-home; silver converters stay single-homed code/silver per DS~A's correction).
AC: Schwab raw ingest lands daily (SI2 same-cycle post-v1.1.0); C3 headless TRN daily; the repoint is a tracked un-fork not a permanent divergence. Arch-gate: CTO (ruled).

## WS-3 -- 49F-MDPF custody + aggregate durable [DISPATCH-HELD] -> 0.5.0_AE + CVO + CTO co-sign
Scope: (1) confirm schwab-native custody advances DAILY (gated on WS-2b Schwab-ingest health -- the flip made it load-bearing). (2) CVO post-flip per-field parity (custody/model_aua/non_model_aua, no-unexpected-widen, 06-25 freeze-clear) on the FIRST post-un-freeze mdpf fire -> CLOSE the MDPF flip deploy-completion ledger (20260702T1405Z). (3) generalize the leg-2 protection-gate pattern (fresh-but-wrong can't replace known-stale) to future custody-basis moves.
AC: custody advances daily; CVO per-field parity GREEN; MDPF flip ledger CLOSED; leg-2 gate proven on N nightlies. Arch-gate: never-widen standing (CTO GATE-3).

## WS-4 -- Predictable Portal refresh (SLA-as-gate) [DISPATCH-HELD] -> 0.4.0_DE (lead) + AE (alarm infra) + CVO
Scope (DE design ed595f90e/6ae9fc727/f55df6cfb, CTO GATE-4 RULED): (1) per-partner per-served-key freshness-SLA + fail-LOUD alarm keyed on SERVED-CONTENT data_as_of (NOT chain-completion, NOT mtime) -> a degrade CANNOT silence it (outcome-keyed, per-DIMENSION per CVO C1). (2) BUILD the comp-freshness CONTENT-vintage dimension INSIDE WS-4 (CTO routing ruling; reusable/parameterized -> WS-5 inherits; R1 pre-req = content-vintage field audit, a key without one falls back to mtime = the trap). (3) single-writer + no-clobber byte-size/shape FLOOR across served keys (ADVI_BREAKS stub-clobber; coordinate the LIVE freeze-monitor + TO-6b, don't duplicate). (4) post-fix re-publish/CF-invalidate path + optional served-staleness UI.
AC: every anchor-partner served key has a daily SLA + a degrade-unsilenceable alarm; content-vintage oracle live; single-writer+no-clobber verified; re-publish proven. Arch-gate: CTO (SLA-as-gate ruled; the 6 ADs on the firmed TO).

## WS-5 -- cross-cutting contract STANDARD [CTO-AUTHORED post-un-freeze]
CTO authors the parameterized robustness/SLA/validation STANDARD (NFRA_INTEGRATIONS_STANDARD pattern) once the shared defer_guard_read_bronze helper concretizes; COO per-partner rollout; CVO validation gates. Not a COO-dispatch TO.

---

## Dispatch plan (on the un-freeze LANDS)
1. Un-freeze lands (inf L1-GREEN + CVO parity + bd served-advance) -> COO collects the 3-way tri-attestation (0.6.1+DS~A+CVO) + holds registry-flip -> CTO closes INFREF+MDPF ledgers.
2. THEN dispatch WS-2a (0.7.0~A/0.6.0/0.6.2), WS-2b (0.6.2/DS~A), WS-3 (0.5.0), WS-4 (DE/AE) durable TOs -> each RAVCs CTO on commit for the arch-gate.
3. Register ADVI_ETLFIX threads (WS-1..5) in org/projects/ADVI_ETLFIX.json on dispatch.
**HELD until the un-freeze -- do not split firefight focus (CTO-directed).**
