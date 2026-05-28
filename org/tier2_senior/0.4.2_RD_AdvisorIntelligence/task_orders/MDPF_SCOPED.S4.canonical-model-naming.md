# MDPF_SCOPED.S4 — Canonical model-portfolio naming (comprehensive FE rename, audit-first) (RD~B)

**Project:** [MDPF_SCOPED](../../../projects/MDPF_SCOPED.json)
**PRD:** `docs/architecture/MDPF_SCOPED.md` v0.1 §3 S4 + §8 Q3 (commit 486da0470)
**Pod:** 0.4.2_RD_AdvisorIntelligence (base)
**Lane:** RD_AdvisorIntelligence **base** (RE-ROUTED from ~B 2026-05-28T~20:06Z /drive pace-pickup: F2 shipped, base lane is warm + idle; S4 is independent + does NOT touch firmAccess.ts, so it parallelizes with RD~B's S1 cleanly). RD~B keeps S1.
**Issued to:** 0.4.2_RD_AdvisorIntelligence
**Author:** 2.0.0_SA_COO 2026-05-28T~20:00Z (/drive — CTO MDPF_SCOPED NOVEL_PRD_READY 19:54Z); re-routed to base ~20:06Z
**Sizing:** Audit ~30-45min; rename sized after audit (30 files match the grep anchor)
**Authority anchor:** CTO PRD v0.1 486da0470 + Andrew direct 2026-05-28

<status>complete</status>

## Objective

Apply Andrew's canonical model-portfolio naming **comprehensively** across Model Portfolios, Attribution, Positioning, and Factor Tilts (+ shared libs). **Audit-first — do NOT blind find-replace** (LTC/LTA may be data keys, not just display strings).

## Canonical convention (Andrew direct)

| Current | Legacy abbrev | Canonical name | Canonical abbrev | Rule |
|---|---|---|---|---|
| Ultra Short-Term | — | **Ultra-Short Term** | (unchanged) | hyphen in "Ultra-Short", space before "Term" |
| Short-Term | — | **Short Term** | — | **no hyphen** |
| Intermediate | — | **Intermediate Term** | — | add "Term" |
| Long-Term Conservative | **LTC** | **Long Term** | **LT** | rename LTC → LT |
| Long-Term Aggressive | **LTA** | **Ultra-Long Term** | **ULT** | rename LTA → ULT |

Long-end remap reframes Conservative/Aggressive as duration tiers: LTC → Long Term (LT); LTA → Ultra-Long Term (ULT).

## CRITICAL — audit-first (do this BEFORE any rename)

Audit whether old names/abbreviations (esp. `LTC`/`LTA`) are **data keys** the backend artifacts emit + the FE joins on, vs display-only strings:
- **If data keys** → rename must go through a **display-mapping layer** (canonical display name ← raw data key) so charts/colors/joins don't break; a data-key rename requires coordinated DS artifact changes (surface to COO → DS coordination if so).
- **If display-only** → safe FE rename.
Decide display-only-mapping vs full data-key-rename in Phase-0 and **document**. Coordinate with MDPF_SCOPED.S3 (DS~B) if the rename touches per-firm artifact data keys.

## Scope (comprehensive — grep anchor: 30 files match `LTC|LTA|Short-Term|Ultra-Short|Intermediate Term|Cohort 2`)

`ModelPortfolios.tsx` + `ModelPortfolios/tabs/*`; `pages/Attribution/**` (tabs + constants/ + README); `pages/Positioning/**` (tabs/panels + constants/); `pages/FactorTilts/**` (tabs/panels + constants.ts + types.ts); shared libs `lib/modelPortfolioColors.ts` + `lib/tickerRegistry.ts`.

## Acceptance criteria

- **AC4.** The 5 canonical names + LT/ULT abbreviations render consistently everywhere across the 4 pages (+ tabs). No "Short-Term" hyphen; "Long Term"/"Ultra-Long Term" replace LTC/LTA. Color-map, ticker-registry, chart joins remain correct (mapping layer if data keys retain legacy values). No orphaned legacy strings in the 4 pages' UI.
- **AC4-Q3.** Confirm with COO/Andrew whether LT/ULT are the canonical short forms for compact UI (legends/axes/headers) + whether the short end needs canonical abbreviations or only the long end — non-blocking on the audit; flag at audit completion.

## Dependencies

- Largely independent (FE rename + mapping). Coordinate with **S3 (DS~B)** if the audit finds the rename touches data keys the per-firm artifacts emit.
- **ADVI_INFMVP coordination:** none (different surface). RD base lane is on ADVI F2; this is RD~B — parallel.

## Sequencing

1. ~30min: grep the 30 files; audit LTC/LTA + name strings for data-key-vs-display (the critical gate)
2. **decision + document:** display-mapping-layer vs data-key-rename; if data-key, COO-surface for DS coordination
3. apply rename/mapping across the 4 pages + shared libs
4. verify color-map + ticker-registry + chart joins intact (DEV; Rule 19) → RAVC2

## RAVC2 deliverable

`[RAVC2-Request] MDPF_SCOPED.S4 — canonical naming` to ws COO. CC ws CTO. Body: audit finding (data-key vs display) + approach taken (mapping layer or rename) + the 4-page consistency evidence + Q3 confirmation ask + no-broken-joins verification.

## Compiler tools mandate

- `comp-transform schema-check ModelPortfolios` (+ Attribution/Positioning/FactorTilts) before/after — MISSING = runtime undefined; verify no join breaks.
- Portal stays on DEV (Rule 19).

## Cross-domain coordination

`<scoped/>` — 4 portal pages + 2 shared libs. The audit gate is the real coordination point: if LTC/LTA are data keys, this becomes a cross-domain DS+RD effort — surface to COO immediately.

## Notes

- The audit-first caution is the whole ballgame — a blind find-replace on data keys breaks color/chart joins silently. Do the audit, document the verdict, then rename.

— ws COO /drive 2026-05-28T~20:00Z
