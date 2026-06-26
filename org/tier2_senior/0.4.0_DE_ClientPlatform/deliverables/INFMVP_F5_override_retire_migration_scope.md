# INFMVP.F5 Override Retirement — Migration Scope

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-06-25 (re-grounded 2026-06-26) · **For:** 2.0.0_SA_COO (RAVC; formalize → tracked TO + CVO verify-leg)
**Origin:** Preserved follow-on from ADVI_NNAATTR (closed-complete 2026-06-22, CVO #9). The FE override CVO + I flagged as load-bearing-but-latent-fragile.

> **Re-grounding note (2026-06-26):** all source anchors below re-verified against the live portal DEV tree +
> bd-gold. Three drifts from the 2026-06-25 draft were corrected: (1) `DistributionTab.tsx` moved to
> `_shared/tabs/` (the FE1 `_shared/{tabs,panels}` refactor); (2) line anchors shifted (override block now
> **2601–2638**, `canonicalNna` fetch now **925**); (3) **material**: `canonicalNna` is NOT prunable on the
> donut-retire — DistributionTab's own `heroMetrics` (1535–1550) consumes it independently of the donut
> override (§4 step-3 corrected). The override comment block (2601–2611) in the live code now itself documents
> this exact P2 migration as the known clean fix — strong corroboration the plan targets the right seam.

---

## 1. The problem in one paragraph

The Distribution-tab **ADV-NNA donut** is produced by `D_01.partner_analytics.py::build_nna_adv_view`,
which grains period NNA **by `architect`** — exactly one architect per account
(`drop_duplicates('account_id')`), so segments are **architect-scoped and ADDITIVE**: they sum to the firm
whole (`total_abs_nna = sum |period_nna|` ≈ the 102.5M additive sigma). At render time, a FE override in
`DistributionTab.tsx` (ADVI_INFMVP.F5, lines 2601–2632) **swaps every donut segment's value** for the
**all-roles canonical** per-advisor NNA from `D_00f.advisor_nna_canonical.py`
(`platinum/firm/advisor_nna_canonical.json`), which sums `nna_txn` over every account where the advisor is on
the team in **ANY** role (architect/implementor/consultant/local_ops/additional_advisor) → **NON-additive**
(~405M; 49/52 advisors diverge from architect-scope). Result: all-roles values are injected into a donut
whose declared whole is architect-additive → **parts don't sum to whole**. The override is the correct STOPGAP
(removing it reverts the donut to architect-scope and re-opens the per-advisor route divergence ADVI_NNAATTR
fixed), but the clean fix is **producer-side**: migrate the `views.nna.adv` SOURCE to emit canonical all-roles
and **decide the whole-semantics**, then retire the FE override.

---

## 2. Ground-truth map (verified this session)

| Layer | Artifact / site | Scope | Additive? |
|---|---|---|---|
| **Legacy producer** | `data/black_diamond/scripts/gold/D_01.partner_analytics.py` (bd-gold, group D order 301); ADV donut filtered to `primary_role == 'architect'` (≈ line 983 — exact fn/lines **DS to confirm**; the `build_nna_adv_view` name in the 06-25 draft is unverified) → `views.nna.adv.donut.segments` | Architect (1/account) | **YES** — segments sum to firm whole |
| **Canonical (already a D_01 INPUT)** | `D_01` already **READS** canonical NNA: `gold/canonical/nna/` (PREFIX, ← C_01) + `gold/views/nna_aua_by_advisor.parquet` (per `comp-pipescript io D_01`). FE fetches the platinum twin `D_00f.advisor_nna_canonical.py → platinum/firm/advisor_nna_canonical.json` (per-advisor × window × cohort; all-roles via `lib.advisor_nna_attribution`) | All-roles (N/account) | **NO** — multi-coverage double-counts |
| **FE override (retire target)** | `portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx` `SnapshotDistributionView`, **block 2601–2638** (`cohort==='adv'` guard; prop `canonicalNna` declared 2519, fetched 925); maps each `seg.key` → `canonicalNna.advisors[seg.key].windows[canonWindow].nna` (+ inflows/outflows), firm `metrics.aua` → `canonicalNna.firm.windows[canonWindow].nna` | — | injects all-roles onto additive donut |
| **Other `canonicalNna` consumers in DistributionTab (NOT the donut override)** | `heroMetrics` 1535–1550 (reads `firm/state/city/advisor/client.windows[W]` for hero net/inflow/outflow at every grain, cohort≠`ofc`) — independent accuracy path. Plus `AdvisorAnalytics.tsx` (204/316/323) + `AdvisorPublicProfile.tsx` (318/350) fetch canonical too | — | keeps `canonicalNna` fetch load-bearing after the donut override is gone |
| **Window vocab** | `D_00f` window build (q_current + prior quarters); FE maps `selectedPeriod`→canonical window via `PERIOD_TO_CANONICAL_WINDOW` (DistributionTab line 794) | — | — |

Both producers already exist and are CVO-grounded, and **D_01 already reads the canonical NNA as an input** — so
the migration is a **re-source WITHIN D_01** (emit canonical into `views.nna.adv`), not a new cross-script
dependency. It does not invent new aggregation — the all-roles math is the canonical's, already served + FE-consumed
today. **No new melt** is the explicit goal (eliminate the D_00c-class inline re-implementation risk CVO flagged).

---

## 3. The crux decision — donut whole-semantics (needs a ruling BEFORE build)

A donut visually asserts parts-sum-to-whole. All-roles per-advisor NNA is non-additive, so the producer must
pick a whole-semantics. Three options:

- **Option A — All-roles segments + firm-NNA center, with explicit multi-coverage disclosure.**
  Segments = canonical all-roles per-advisor (matches today's overridden render exactly); center = firm NNA
  (`D_00f.firm.window.nna`). Segments **can exceed** the center (overlap credit). Requires a FE/label change:
  donut renders as "per-advisor credited NNA" with a disclosure that segments overlap (not a strict partition).
  **Faithful to canonical; breaks the strict sum invariant by design (disclosed).** This is the truest
  representation of the all-roles reality and matches what the override already shows.

- **Option B — Primary-role additive segments.** Attribute each account's NNA to the advisor's **primary_role**
  only (one advisor per account, like architect today but using the primary-role resolution D_01 already
  computes for AUA, `advisor_role_aua`/`primary_role`). Restores strict sum-to-whole. **Loses the multi-coverage
  credit** the canonical captures — a step back from what ADVI_NNAATTR delivered. Not recommended as the donut's
  only emit.

- **Option C — Dual-emit (RECOMMENDED).** Producer emits BOTH: (1) an **additive** `views.nna.adv` donut
  (primary-role) preserving the strict visual whole, AND (2) an **all-roles** per-advisor metric block
  (`views.nna.adv.allroles` or reuse the canonical) for the leaderboard/credit surfaces. FE renders the additive
  donut as the partition and surfaces all-roles credit explicitly where the override does today. Removes the
  parts-vs-whole tension structurally and keeps both truths. **More producer work; cleanest semantics.**

**My recommendation: Option C if product wants a strict donut; Option A if product accepts a disclosed-overlap
donut (least code, exactly reproduces today's served numbers).** This is a DS/product call — flagging for COO +
CVO + (if needed) Andrew, since it's a semantics decision, not a mechanical one.

---

## 4. Migration steps (once whole-semantics is ruled)

1. **Producer (D_01, DS-lane):** in `build_nna_adv_view`, source per-advisor period NNA from the all-roles
   attribution (reuse `lib.advisor_nna_attribution` / read `advisor_nna_canonical.json` directly rather than
   re-deriving — single source of truth with D_00f). Emit per the ruled whole-semantics (A/B/C). Carry the same
   window vocabulary so per-period values tie to D_00f exactly. **No new melt** — eliminate the divergence risk
   CVO flagged (D_00c-class inline re-implementation) by reading the canonical, not re-melting.
2. **Served tie-out (the acceptance gate):** for every advisor × window, the new `views.nna.adv` segment value
   == `advisor_nna_canonical.json` `advisors[key].windows[w].nna` (and firm center == `firm.windows[w].nna`) —
   i.e. the producer now emits what the FE override currently computes. Prove **legacy-overridden render ==
   canonical-sourced render** on the served artifacts (49F + inflection partners) before the FE override comes out.
3. **FE override removal (DE-lane, mine) — SCOPED TO THE DONUT BLOCK ONLY:** delete the F5 donut-segment
   override block (`_shared/tabs/DistributionTab.tsx` **2601–2638**, the `cohort==='adv'` segment-swap). The donut
   then reads `views.nna.adv` directly and is correct. **DO NOT remove the `canonicalNna` fetch (925) or its prop
   plumbing** — it is *still load-bearing after the donut override is gone*: DistributionTab's own `heroMetrics`
   (1535–1550) reads `canonicalNna.{firm,state,city,advisor,client}.windows[W]` for hero net/inflow/outflow at
   every grain (all cohorts except `ofc`), independent of the donut. AdvisorAnalytics + AdvisorPublicProfile also
   consume it. So the donut-retire prunes ONE block, not the fetch. (Eliminating the FE canonical-fetch entirely —
   having the producer emit ALL per-grain per-window leaves heroMetrics/drilldown need — is a separate, larger
   effort, NOT in scope for "retire the F5 override.") `comp-transform schema-check SnapshotDistributionView` +
   `ternary-audit` before/after; `comp-cache collisions` to confirm the canonical query-key still has live consumers.
4. **Regression:** per-firm served diff (49F + inflection) — donut segment values, firm total, distribution
   histogram unchanged through the cut (the whole point: the cut is value-invisible to the user under A; under C
   the additive donut is the new strict-partition view).

---

## 5. Lane split (COO to formalize)

- **DS** — D_01 producer change (the real data-layer work; whole-semantics emit).
- **AE** — gold re-run / deploy of D_01 on the nightly; no ad-hoc gold run to validate (validate on scheduled artifacts).
- **DE (me)** — FE override removal + schema-check/ternary-audit + per-firm served regression; I co-author the tie-out spec.
- **CVO** — verify-leg: the served tie-out (legacy==canonical) + no per-advisor route divergence re-opens.

No external gate. Durable (no deadline). Blast radius is portal/graph + bd-gold D_01 only — no firm-pipeline
cross-reference, no cot/inf reach.

---

## 6. Open items for the ruling

1. **Whole-semantics: A, B, or C?** (Section 3 — the one real decision; everything else is mechanical.)
2. ~~Does any non-donut surface still require the FE `canonicalNna` fetch?~~ **RESOLVED (re-grounded 2026-06-26):
   YES — keep the fetch.** `heroMetrics` (DistributionTab 1535–1550) reads canonical windows at every grain,
   independent of the donut, plus AdvisorAnalytics + AdvisorPublicProfile consume it. So step-3 prunes ONLY the
   donut override block (2601–2638), not the fetch. The "retire the F5 override" scope is donut-only.
3. Confirm D_01 sourcing the donut from the canonical it **already reads** (`gold/canonical/nna/` ← C_01, +
   `nna_aua_by_advisor.parquet`) — vs re-calling the attribution lib or reading the platinum `advisor_nna_canonical.json`
   — is the preferred single-source path. My recommendation (it's already an input; no new dep), pending DS/CTO concurrence.
4. **DS to confirm the exact producer fn/lines** in `data/black_diamond/scripts/gold/D_01.partner_analytics.py`
   that emit the ADV donut (the 06-25 `build_nna_adv_view` name is unverified; live grep points at the
   `primary_role=='architect'` filter ≈ line 983). The **cot** `D_01` is a SEPARATE firm pipeline — never touch.
