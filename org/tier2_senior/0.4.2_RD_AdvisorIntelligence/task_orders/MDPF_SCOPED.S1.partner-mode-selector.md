# MDPF_SCOPED.S1 — Partner-mode selector (mirror Advisor Intelligence) (RD~B)

**Project:** [MDPF_SCOPED](../../../projects/MDPF_SCOPED.json)
**PRD:** `docs/architecture/MDPF_SCOPED.md` v0.1 §3 S1 + §4 + §8 Q1 (commit 486da0470)
**Pod:** 0.4.2_RD_AdvisorIntelligence~B
**Lane:** RD_AdvisorIntelligence ~B (MDPF tilde-lane; parallel to ADVI F2 on RD base)
**Issued to:** 0.4.2_RD_AdvisorIntelligence~B
**Author:** 2.0.0_SA_COO 2026-05-28T~20:00Z (/drive — CTO MDPF_SCOPED NOVEL_PRD_READY 19:54Z)
**Sizing:** scaffold ~60-90min against Global; per-firm wiring as S3 artifacts land
**Authority anchor:** CTO PRD v0.1 486da0470 + Andrew direct 2026-05-28

<status>pending</status>

## Objective

Add a **`Select Partner:` dropdown** to Model Portfolios — same canonical upper-right placement + styling as Advisor Intelligence — driving **3 modes: Global (default), 49 Financial, Inflection Wealth Management.**

## Pattern to mirror (verified)

`portal/src/pages/AdvisorIntelligence/index.tsx` — top-level dispatcher with `ALL_PARTNER_FIRMS` + `selectedFirmId` useState + `PARTNER_VIEWS` record (firmId → `_partners/{firm}/index.tsx`), sharing `_shared/`; `Select Partner:` dropdown upper-right (`allFirms` / `onFirmChange`). Replicate exact placement + styling on Model Portfolios.

## Modes (3) — note the default difference vs AI

- **Global (DEFAULT)** — today's Model Portfolios (all cohorts aggregated). **AI defaults to a firm (49financial); MDPF defaults to Global (the aggregate, NOT a firm).** Dropdown = `[Global (default), 49 Financial, Inflection Wealth Management]`.
- **49 Financial** — Model Portfolios today **without Cohort 2**.
- **Inflection Wealth Management** — **Cohort 2a + 2b** only.

Switching modes re-scopes the entire page (metrics, donut, trend analysis, distribution) to that mode's cohort composition.

## Acceptance criteria

- **AC1.** `Select Partner:` dropdown in the same canonical upper-right position + styling as Advisor Intelligence, `[Global (default), 49 Financial, Inflection]`. Switching re-scopes the whole page: Global = all; 49F = all − Cohort 2; Inflection = Cohort 2a+2b.
- **AC1-Q1.** Flag to COO/Andrew: for internal Opal admins, default Global or a specific firm? (External users firm-locked by firmAccess.ts; non-blocking on scaffold.)

## Dependencies

- **Reads S3's per-firm artifacts** (49F / Inflection) for the non-Global modes. **Scaffold in parallel** against the Global artifact (current behavior) now; wire per-firm modes as S3 artifacts land. Coordinate with MDPF_SCOPED.S3 (DS~B) on artifact shape + firm-id keys.
- **ADVI_INFMVP shared primitive:** firmAccess.ts + partner-view pattern are shared with ADVI F2 (RD base). **Use the canonical firmAccess.ts L1 firm-id namespace** (Global/49financial/inflection) AI already uses — do NOT fork it. Sequence/coordinate any firmAccess.ts touch with the ADVI F2 lane (F2 lands first per that TO).

## Sequencing

1. ~20min: read AdvisorIntelligence/index.tsx dispatcher + the Model Portfolios page structure
2. ~40min: scaffold the dropdown + dispatcher against the Global artifact (default mode working end-to-end)
3. wire 49F + Inflection modes as S3 artifacts land (coordinate DS~B)
4. RAVC2 (scaffold milestone acceptable as interim; full per-firm wiring on S3 completion)

## RAVC2 deliverable

`[RAVC2-Request] MDPF_SCOPED.S1 — partner-mode selector` to ws COO. CC ws CTO. Body: dropdown placement/styling parity evidence vs AI + Global-mode working + per-firm wiring status (gated on S3) + Q1 ask.

## Compiler tools mandate

- `comp-transform schema-check ModelPortfolios` before/after the dispatcher wiring.
- Portal stays on DEV (Rule 19).

## Cross-domain coordination

`<scoped/>` — Model Portfolios FE + shared partner-view primitives. Two coordination points: (1) S3 (DS~B) for per-firm artifact shape; (2) ADVI F2 (RD base) for the shared firmAccess.ts namespace — don't double-edit.

— ws COO /drive 2026-05-28T~20:00Z
