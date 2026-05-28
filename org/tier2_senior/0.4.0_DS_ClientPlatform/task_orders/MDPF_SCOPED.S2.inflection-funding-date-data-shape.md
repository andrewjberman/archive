# MDPF_SCOPED.S2 — Inflection 5/18 model-funding data shape (Daily AUA Trend) (DS~B + RD~B)

**Project:** [MDPF_SCOPED](../../../projects/MDPF_SCOPED.json)
**PRD:** `docs/architecture/MDPF_SCOPED.md` v0.1 §3 S2 + §4 + §8 Q2 (commit 486da0470)
**Pod:** 0.4.0_DS_ClientPlatform~B (data emit) + 0.4.2_RD_AdvisorIntelligence~B (FE trend render)
**Lane:** DS_ClientPlatform ~B (MDPF tilde-lane)
**Issued to:** 0.4.0_DS_ClientPlatform~B
**Author:** 2.0.0_SA_COO 2026-05-28T~20:00Z (/drive — CTO MDPF_SCOPED NOVEL_PRD_READY 19:54Z)
**Sizing:** sized after S3 Inflection artifact lands (this is a data-shape requirement on that artifact)
**Authority anchor:** CTO PRD v0.1 486da0470 + Andrew direct 2026-05-28

<status>blocked</status>
**Andrew decision 2026-05-28 (via CTO):** Option 2 — full Orion daily backfill for rolling-365d Non-Model AUA.
**Blocker:** AE EC2 backfill running — mdpf-daily-runner i-02448edb624a7a7cf, PID 2195 (3rd attempt; PID 2493 died ~23:01Z when EC2 auto-shutdown cleared /tmp; ~21 days written before stop; --skip-existing resumes from day 22). LOG=/tmp/mdpf_backfill_r3.log. ETA ~03:30-04:00Z 2026-05-29. Output: `s3://opal-data-mdpf/mdpf/feeds/non_model_aua/inflection/{date}.parquet`. AE monitoring + signals DS~B on complete. Resume: re-run `build_aggregate_aua_timeseries.py --upload` (json/ dual-write 44afa1dd2 in place) → verify AC2 → RAVC2.

## Objective

Inflection moved money into the models only on **~2026-05-18**; before that they hold non-model assets only. The **Daily AUA Trend Analysis (stacked bar + area)** in Inflection mode must render the rolling **last 365 days** of daily Orion-processed AUA **entirely GRAY (the Non-Model group, already present — `modelPortfolioColors.ts` `Non-Model` = Opal silver `#C3CADA`)**, then **split the model holdings out of the total from 2026-05-18 forward**.

## Requirement

- Before 2026-05-18: chart is 100% gray (Non-Model).
- From 2026-05-18: gray (Non-Model) + the split-out model cohorts.
- Needs a full **rolling-365d daily Non-Model AUA series from Orion** (not just model-period data), with the model-cohort split applied only from the funding date forward.
- This is a **data-shape requirement on the per-firm Inflection artifact (S3)** — not just an FE toggle. DS~B emits the series shape; RD~B renders it.

## Acceptance criteria

- **AC2.** In Inflection mode, Daily AUA Trend Analysis (stacked bar + area) renders rolling 365d daily AUA fully gray (Non-Model) before 2026-05-18, and splits model-cohort AUA out of the total from 2026-05-18 onward. Totals tie to Orion-processed daily AUA across the full window.
- **AC2-Q2.** Flag to COO/Andrew: hard-code 2026-05-18 OR data-driven (first date Inflection model AUA > 0)? Data-driven is more robust for future partners — recommend data-driven; confirm. Non-blocking; implement data-driven default unless Andrew pins the date.

## Dependencies

- **HARD: S3 Inflection per-firm artifact** must carry rolling-365d daily Non-Model AUA + the model-split. S2 cannot proceed until that artifact shape exists. Coordinate the series schema with S3 (DS~B owns both — sequence S3 emit → S2 trend shape).
- RD~B renders; coordinate with S1 (same RD~B lane) on the Inflection-mode page.

## Sequencing (post-S3 Inflection artifact)

1. confirm the Inflection artifact carries rolling-365d daily Non-Model AUA (from S3)
2. apply the 5/18 model-split (data-driven default per Q2) in the emit/shape
3. RD~B renders stacked-bar + area with Non-Model gray + model-cohort split from funding date
4. verify totals tie to Orion daily AUA → RAVC2

## RAVC2 deliverable

`[RAVC2-Request] MDPF_SCOPED.S2 — Inflection 5/18 trend shape` to ws COO. CC ws CTO. Body: the series-shape emit + 5/18 split logic (Q2 resolution) + FE render evidence (gray-before / split-after) + Orion-AUA tie-out across the 365d window.

## Compiler tools mandate

- `comp-pipescript io <script>` before edit; `.tools/ds-commit-gate.sh` on any python (Rules 14/15).
- `comp-transform schema-check` on the trend component after the FE render.

## Cross-domain coordination

`<scoped/>` — Inflection per-firm artifact (S3-dependent) + Daily AUA Trend FE. Tightly coupled to S3 (same DS~B lane). RD render coordinates with S1's Inflection-mode page.

## Notes

- S2 is authored STAGED so the dependency + data-shape contract is recorded; GO'd on S3 Inflection-artifact availability. Avoids trend-shape work landing before the artifact exists.

— ws COO /drive 2026-05-28T~20:00Z
