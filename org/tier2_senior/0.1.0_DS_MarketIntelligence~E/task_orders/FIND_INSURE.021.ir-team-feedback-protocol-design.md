# FIND_INSURE.021 — IR-team feedback protocol design + schema + calibration reference impl

| | |
|---|---|
| **Project** | FIND_INSURE (Phase 3 pre-authoring) |
| **Owner** | 0.1.0_DS_MarketIntelligence~E |
| **Authored** | 2026-05-27T~21:15Z (2.0.0_SA_COO /drive cycle #188) |
| **GO** | YES — dispatch_held=false |
| **Status** | complete (AC-A1+A2+A3 shipped 2026-05-28T~04:0XZ work-cycle:0002; AC-A4 = ws CTO scope (PRD §7 AC5 fold) — decision-tree text supplied in protocol §D, CTO folds at IR-team-named-individual landing) |
| **Authority** | Brief `b67ad03ec` (docs/briefs/find-insure-phase3-ir-feedback-and-lambda-skeleton-20260527.md) + Andrew sovereign 2026-05-27T~19:50Z pace-pickup + ws COO greenlight 20:03Z |
| **Sequencing** | Fully parallel to Phase 1 + Phase 2A critical paths (substrate-ready when upstream gates clear) |

## Scope

Brief b67ad03ec Thread A — author canonical AC5 RAVC2 mechanism per PRD v0.6 §7 AC5.

## Acceptance criteria (Thread A from brief §3)

- **AC-A1**: Ship `docs/briefs/find-insure-ir-team-feedback-protocol.md` with §A-§D substantive content (feedback elicitation methodology + capture schema + empirical-tuning loop scoring-weights v0.1 → v0.2 + RAVC2-Accept decision tree)
- **AC-A2**: Feedback capture schema (per-IMO + per-session) formalized as JSON Schema at `data/find/imo/scripts/serving/schemas/ir_feedback_schema.json`
- **AC-A3**: Calibration delta calculation methodology documented + reference impl `data/find/imo/scripts/serving/calibrate_weights.py` against fixture v0.1 + fixture IR-team-feedback JSON
- **AC-A4**: RAVC2-Accept decision tree (§D) cross-referenced into PRD v0.7 candidate §7 AC5 (CTO authors v0.7 amendment post-Brief #3 RAVC2 if IR-team-named-individual identification lands separately)

## Brief reference

Full scope at `docs/briefs/find-insure-phase3-ir-feedback-and-lambda-skeleton-20260527.md` §2.1 + §3 Thread A ACs. Author against the brief verbatim; brief is the spec.

## Non-scope (v0.1)

- NO live IR-team session scheduling (Andrew + Phase 3-RAVC2-Accept window concern)
- NO IR-team-named-individual identification (ADDITIVE-1 standing per PRD §11; pre-Phase-3-RAVC2-Accept gate; brief mentions surfacing in §A)
- NO production-fixture data; all AC pass against synthetic fixture JSON

## Sister-coord

CC DS~A + DS~B + DS~C on calibration delta methodology — they consume `calibrate_weights.py` output if v0.1 → v0.2 weight-amendment fires. AC-A4 PRD v0.7 amendment is CTO scope (your ship contains decision-tree text; CTO folds into PRD amendment cycle).

## CC Andrew

AC5 ADDITIVE-1 IR-team-named-individual identification routing question surfaces in §A of your protocol design. NON-URGENT (pre-Phase-3-RAVC2-Accept gate). Brief #3 AC-A1 ships without resolution; question is surfaced in the doc, not gated by the answer.

## RAVC2-expected window

~2-4h wall (documentation-class + reference impl + JSON schema; no live data dependency). RAVC2-Request to ws COO with AC-A1..A4 self-attestation table.

## Sequencing companion

`FIND_INSURE.022` (Thread B Phase 3 Lambda skeleton trio) shipped same cycle as same-dispatch sister TO. Author in parallel OR sequentially per your discretion; brief allows bundled or split execution (§5 routing).

— 2.0.0_SA_COO /drive cycle #188 same-cycle dispatch
