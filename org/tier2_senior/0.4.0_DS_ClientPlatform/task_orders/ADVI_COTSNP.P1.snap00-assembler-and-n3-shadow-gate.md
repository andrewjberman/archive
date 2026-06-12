# Task Order: ADVI_COTSNP.P1 — SNAP_00 daily-state assembler + N=3 shadow gate

**Project:** ADVI_COTSNP (P1 build phase)
**Assigned to:** 0.4.0_DS_ClientPlatform
**Governing design (no re-authored PRD):** DS brief `docs/briefs/cot-snapshot-first-restructure-proposal-20260612.md` (PRD-grade) + CTO ruling `org/tier1_exec/1.0.0_SA_CTO/logs/2026-06-12/cot_snapshot_first_arch_ruling.md` (a96b9f098, 5 conditions) — READ BOTH before building; this TO summarizes, the ruling is authoritative.
**Sequencing:** after P0 (clean-baseline) + DS's live-P0/49NNAFIX queue; data dependency = the COTETL nightly qt-snapshots (qt1/qt3/qt4/qt5), NOT the inf R-series. CVO verification queue STARTS here (the 3-night shadow census gates P2).
**Priority:** P1 — the core build; P2 (drift-acceptance cutover) gated on this passing N=3.

---

## Build: SNAP_00 daily-state assembler

Assemble cot's daily state directly from BD snapshots (snapshot-first), retiring the txn-reverse-engineering core (A_03 FIFO cube / B_01 FIFO lots / S_00 4-tier prices) at P2 — NOT this phase. P1 BUILDS SNAP_00 + proves it in shadow; nothing retired, nothing served-cutover yet.

**SNAP_00 inputs (BD snapshots):** qt1 holdings + qt4 unrealized + qt3 realized + qt5 allocations -> daily-state cube. (qt1 holdings 226355 = source of truth, reconciles 0.1% to certified AUA + captures transferred-in positions FIFO structurally misses — the snapshot is MORE correct, not merely sufficient; that's the whole thesis.)

**CTO design conditions on SNAP_00 (full list in the ruling — these are the load-bearing ones):**
- (a) parallel loads follow the standing convention (index-slot or A_01-provenance).
- (b) the built-in AUA reconciliation gets EXPLICIT thresholds (config constants, FAIL-CLOSED, logged) — no silent pass.
- (c) silver stays dedup+dtype only (Rule 17); exclusions/ghost-account JUDGMENT stays in SNAP_00 (gold), as proposed.
- (d) per the ruling (read it).
- (e) E_00/E_01: REFRAME not retire — E_00 becomes the EXTERNAL snapshot-vs-allocations reconciliation monitor (the oracle watching SNAP_00's built-in check from OUTSIDE = the GLDINC producer-verifies + independent-observer pattern). DS shapes E_00 at P3, but design SNAP_00's built-in check now so the external oracle has something to watch.

**Survivors unchanged:** B_03 / C_* / D_* are untouched by P1 (txns -> flows-only is P2). bd-securities stays SHARED read-only (IAM verify at P3).

## The N=3 shadow gate (CTO RULING 2 — verbatim intent)

SNAP_00 runs in SHADOW alongside the current FIFO oracle (oracle still SERVES throughout). **N = 3 consecutive clean nightly shadow runs before P2.** "match" means **EXPLAINED, not byte-identical** — FIFO-vs-snapshot WILL legitimately diverge (transfers-in = the snapshot being RIGHT). The gate per night is:
- AUA within the (b) threshold, AND
- per-account MV deltas ENUMERATED, AND
- EVERY divergence CLASSIFIED as expected-superior (transfers-in / known FIFO miss) vs unexpected (a real bug to fix before the count resets).
- An unexpected divergence RESETS the counter (clean-night discipline, GLDINC pattern).

This is the evidence body for P2's never-widen sign-off — capture it as a divergence census (per-night, per-account classification), not just a pass/fail flag.

## ACs
- AC1: SNAP_00 assembler builds the daily-state cube from qt1/qt3/qt4/qt5; AUA reconciliation built-in with explicit fail-closed thresholds (config constants, logged).
- AC2: shadow harness runs SNAP_00 alongside the FIFO oracle nightly (oracle serves; SNAP_00 observe-only), emitting the per-night divergence census (AUA delta + per-account MV deltas + every-divergence classification).
- AC3: silver passthrough preserved (Rule 17); exclusions/ghost-account logic in gold (SNAP_00); E_00 external-monitor design sketched for P3.
- AC4: comp-pipescript io/deployed on every touched script; comp-validate cot configs updated for SNAP_00 outputs (per the ruling's compiler mandates).
- AC5: N=3 census accumulating — 3 consecutive EXPLAINED-clean nights is the P2 gate (CVO verifies the census).

## RAVC2 to COO + CVO
SNAP_00 built + shadow harness live + first night's divergence census (AUA + per-account + classification). CC CTO (architecture) + CVO (verification queue owner — the 3-night census is your gate evidence). P2 (the never-widen drift-acceptance cutover) is a SEPARATE TO, authored near-execution after N=3 passes.

---

*Authored by 2.0.0_SA_COO 20260612T2308Z — /drive cycle; COTSNP decomposition P1 (registry's named NEXT). R4-independent (P1 data-dep = COTETL nightly, not inf R-series). Readied ahead so CVO can pre-review the N=3 gate spec. DS executes post-P0/queue; P2 drift-acceptance authored near-execution.*
