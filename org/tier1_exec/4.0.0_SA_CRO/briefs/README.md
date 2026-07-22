# `4.0.0_SA_CRO` — Briefs

Master briefings and the index to every competitive-research source in the Opal corpus.

**Start with a master briefing.** Each consolidates *all* corpus analysis on its target — architecture,
endpoints, methodologies, auth, limits, open items — and points at canonical sources rather than copying them.

| Briefing | Target | Covers |
|---|---|---|
| [`MASTER_BLACK_DIAMOND_ANALYSIS.md`](MASTER_BLACK_DIAMOND_ANALYSIS.md) | Black Diamond (SS&C/Advent) | Two separate API surfaces (DataMining vs the product APIs), the star schema, snapshot-vs-lots-FIFO doctrine, the method contract, the affect vector |
| [`MASTER_ORION_ECLIPSE_ANALYSIS.md`](MASTER_ORION_ECLIPSE_ANALYSIS.md) | Orion Advisor Solutions + Eclipse | Three surfaces, the 9 daily production pulls, the performance method contract, `Reporting/Scope` as a calculation graph, the Orion↔Eclipse join and the ~3.4% lag |
| [`MASTER_SMARTX_ANALYSIS.md`](MASTER_SMARTX_ANALYSIS.md) | SmartX (TAMP) | **A partner, not a displacement target.** Five surfaces, the build-vs-buy seam, the dependency tradeoff, the two-axis account-of-record ruling, and the three-vendor comparison |

**Determinism (Cottonwood current membership):** [`COTTONWOOD_MEMBERSHIP_DETERMINISM_20260722.md`](COTTONWOOD_MEMBERSHIP_DETERMINISM_20260722.md) -- 100% deterministic current model membership via two cross-validated assignment endpoints (17/17, 296==296), vs the ~97% holdings-fit. Read, not fit.

**Appended daily series (Cottonwood model snapshot):** [`COTTONWOOD_DAILY_MODEL_SNAPSHOT_APPEND_SPEC_20260722.md`](COTTONWOOD_DAILY_MODEL_SNAPSHOT_APPEND_SPEC_20260722.md) -- Andrew-commissioned spec: the per-model daily count+value already lands in gold `dim_model_portfolio` per-day partitions but is unqueryable as a series; specs an append-only `fact_model_portfolio_daily` + one-object query surface, FAIL-LOUD identities per append, backfill-compatible by key.

**Verification:** [`SURFACE_RECONCILIATION_TEST_20260722.md`](SURFACE_RECONCILIATION_TEST_20260722.md) — do a
vendor's two surfaces agree on value? **Orion: PASS, exact to the cent. BD: inconclusive, and the $0==$0
"agreement" is explicitly not scored as a pass.** Also names two consumption hazards (Orion's mixed units;
our own `factor` field's semantics).

**Cross-platform synthesis** — the seven invariants both vendors arrived at independently, and what they say
we should build: [`../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md)

**Engagement index (authoritative):** [`../RECON_REGISTER.md`](../RECON_REGISTER.md)

---

## Why these reference rather than copy

Andrew's instruction allowed either: *"brought into your folder or otherwise summarized and pointed to in
paths/references."* **Reference was the right call**, for the reason this agent's own charter exists to guard:
a duplicated 250-line spec is a second copy that a later correction may not reach, and the corpus already
demonstrates the hazard *and* the cure —

- D2's "the BD session is IP-bound" claim was **falsified off-box** and corrected **in place** (2026-07-08).
- D3's "Orion and Eclipse publish no API catalog" was **falsified for Eclipse** and amended **in place**, with
  its scope explicitly bounded to the product actually verified (2026-07-16).

Both corrections landed because there was **one** authoritative copy to correct. The master briefings restate
findings *with attribution and evidence grade*, so a reader can always go to the source — and if the source
changes, the pointer still resolves.

**What is NOT in these briefings, deliberately:** Opal infrastructure economics (BD gold rightsizing, S3 bloat,
memory diagnostics) — real work, not platform analysis. And the **SmartX** corpus, which is the *partner*
candidate for the trade layer rather than an Orion surface; it deserves its own briefing if we do a TAMP
comparison.

## Conventions

Every briefing labels its evidence: **[HAR]** captured response bodies · **[PROD]** code we run in production ·
**[LIVE]** verified against the live vendor · **[DOC]** vendor documentation · **[SPEC]** the vendor's own
OpenAPI · **[INFERENCE]** explicitly fenced. **`[UNOBSERVED]` means our captures never exercised it — it is
never scored as absence.**
