---
status: PRE-STAGED-TEMPLATE
cycle: /verify-channel Mode B COMPREHENSIVE (Phase 3 RAVC2-Accept close-cycle scaffold)
verdict: <<FILL_AT_FIRE: CORROBORATE | CORROBORATE-with-additives | CORROBORATE-with-CONCERN | COUNTER>>
project: FIND_INSURE
trigger_fires_when: ALL THREE of (1) FIND_INSURE.023 RAVC2-Accept lands (DS~E consolidated serving/scoring.json + .021 IR-team-feedback-protocol) + (2) Phase 1 universe-run completes (99/99 OR known-empty-body-tail per AC-T2 escape-valve disposition) + (3) Phase 2A AC3a + Phase 2B AC3b empirical landings on subset
authoring_basis: ws COO [PRE-POSITION-RATIFY] 2026-05-27T~23:15Z + CVO ACK 23:17Z per [[feedback_cvo_proactive_verdict_landing_pattern]] empirical anchor
pre_stage_authored: 2026-05-27T23:20Z
fill_authority: ws CVO at Phase 3 close-cycle firing moment (this CVO instance OR successor respawn-instance per LD-0029)
prior_cycle_anchors:
  - 5a48a72ed (prior CVO Mode B 21:58Z 11-axes Phase 1 Andrew mandate; verdict MISALIGNED + REPAIR-AMENDMENT (a)+(b))
  - 810211e17 (this CVO Mode B 22:55Z through-Phase-3 path-by-path; verdict MISALIGNED-AGGREGATE + 4 REPAIR-AMENDMENT triggers + Constitution-coherence GREEN)
constitution_axis: <<FILL_AT_FIRE: rerun §Constitution-drift subscan at fire-moment; today's baseline GREEN — likely persists>>
self_validation_surface: <<FILL_AT_FIRE>> -- pre-staged declaration body below applies as scaffold
---

**archetype:** VALIDATE

# /verify-channel FIND_INSURE Phase 3 close-cycle — PRE-STAGED Mode B template

Per ws COO [PRE-POSITION-RATIFY] 2026-05-27T23:15Z + CVO ACK 23:17Z. Pre-stages Mode B comprehensive verdict mechanics for the Phase 3 RAVC2-Accept moment so verdict lands same-cycle wall as `.023` RAVC2-Request fires (~15-20min compression vs cold-start). Empirical anchors are `<<FILL_AT_FIRE>>` placeholders to be filled verbatim when the trigger conditions are met.

**Andrew sovereign goal authority (2026-05-27T22:49Z):** "Drive the end-to-end completion of FIND_INSURE through the close of Phase 3."

---

## Trigger conditions (ALL THREE required for template-fire)

| # | Condition | Verification anchor |
|---|---|---|
| 1 | `FIND_INSURE.023` RAVC2-Accept | DS~E consolidated `serving/scoring.json` ranked table lands at `s3://opal-data-imo/serving/scoring.{json,parquet}` + `companies.{json,parquet}` + `employees.{json,parquet}`; matches Phase 3 close-template `docs/briefs/find-insure-phase3-close-template.md` contract |
| 2 | Phase 1 universe-run completion | `s3://opal-data-imo/corp/*` shows >= 90% of 99-IMO universe with `gold/web-scrape/{date}/score.json` (per AC2 ≥90% gate) OR known-empty-body-tail per AC-T2 escape-valve disposition (`scraping_browser1` v0.3.0 ship-pre-close OR accept-with-tail per CTO+COO RAVC2 disposition); AC-T1 telemetry emission populated at `telemetry/{lambda-name}/{date}/{run-id}.ndjson` per (b)(iv) REPAIR-AMENDMENT close-loop |
| 3 | Phase 2A AC3a + Phase 2B AC3b empirical landings on subset | Phase 2A: `s3://opal-data-imo/corp/{subset-slug}/gold/linkedin-scrape/{date}/` populated with ranked employee data + Series-license flags per AC3a; Phase 2B: `s3://opal-data-imo/corp/{subset-slug}/gold/job-posting-scrape/{date}/` populated with per-IMO hiring-pattern analytics per AC3b + HAR-feasibility manifest v0.1+ EMPIRICAL-RATIFIED at `docs/briefs/find-insure-job-board-endpoint-manifest.md` |

If any of the three conditions are not yet met at observation moment: DO NOT FIRE TEMPLATE. Continue STANDBY. Per /verify-channel SKILL.md trigger model — comprehensive Mode B is event-based; pre-stage does NOT change the fire-conditions, only the wall-time-compression at fire-moment.

---

## Self-validation surface declaration (pre-authored scaffold)

Per `[[feedback_cvo_self_validation_mitigation_pattern]]`:

- **(a) Accurate report of own prior actions:** Prior CVO Mode B instances `5a48a72ed` (11-axes 21:58Z) + `810211e17` (through-Phase-3 path-by-path 22:55Z) are CVO authoring. Phase 3 close empirically tests:
  - Whether REPAIR-AMENDMENT (a) was correctly dispatched (PRD v0.7 reconciles to actual final-state empirical reality)
  - Whether REPAIR-AMENDMENT (b)(i) W1 threshold semantics shipped + are decision-useful at universe-scale
  - Whether REPAIR-AMENDMENT (b)(iii) code/ prefix disposition was correct (either implemented OR amended-out)
  - Whether REPAIR-AMENDMENT (b)(iv) telemetry/ emission was implemented + AC-T1 mechanism fired empirically
  - Whether CVO ADDITIVE-1 (IR-team-individual identification) gate is honored at Phase 3b close
- **(b) Chartered-not-escape-hatch acceptance path:** Andrew sovereign goal 22:49Z is the explicit invocation authority for this Phase 3 close-cycle. ws COO PRE-POSITION-RATIFY 23:15Z is the operational coordination. Mode B comprehensive at Phase 3 close fires per Class-1 immediate-fire #2 [RAVC2-CLOSE] per /verify-channel SKILL.md trigger model. CVO is the chartered verifier per Constitution Art III authority distribution.
- **(c) Andrew/MSTR override backstop preserved:** Any verdict in the filled template remains subject to Andrew sovereign override OR MSTR ratify chain per /mstr-review skill body.
- **Cross-respawn-instance distinction (LD-0029):** If the firing CVO instance is different from this pre-staging instance, the firing instance VALIDATES this template scaffold independently before filling; pre-stage is scaffold-only, not a pre-committed verdict.

---

## Per-axis fill-table (placeholders)

| Axis | Today's grade (810211e17) | Target grade (Phase 3 close) | Empirical anchor to fill at fire |
|---|---|---|---|
| **C1** — 99/99 universe attestation | F (3/99=3%) | <<FILL: target ACCEPTED-CLEAN if ≥90% OR ACCEPTED-with-tail if AC-T2 escape-valve accept-with-known-empty-body-tail disposition>> | `aws s3 ls s3://opal-data-imo/corp/ | wc -l` empirical count + universe-run completion timestamp + AC-T2 escape-valve disposition per CTO+COO joint RAVC2-Accept |
| **C2** — Crawl outcome distribution | D (33% empty-body on n=3) | <<FILL: target ACCEPTED-with-empirical-distribution>> | Universe-run distribution: SUCCESS / EMPTY-BODY / BLOCKED-other / fetch-timeout / parse-error percentages |
| **B1** — Bronze field inventory | B | <<FILL: target ACCEPTED-CLEAN>> | Random sample of 5-IMO bronze .meta.json schema validation post-universe-run |
| **S1** — Silver Rule 17 check | B+ (Rule 17 fix CLOSED) | <<FILL: target ACCEPTED-CLEAN unless new field-drop regression>> | Random sample of 5-IMO silver records — Rule 17 5 bronze meta fields preserved verification |
| **G1** — Gold structured layout | B+ | <<FILL: target ACCEPTED-CLEAN>> | Random sample of 5-IMO gold score.json schema + per-match evidence trails |
| **P1** — Parsing yield on SUCCESS pages | B+ | <<FILL: target ACCEPTED-CLEAN at-universe-scale>> | Per-IMO body_text length distribution + headings + structured_blocks density |
| **P2** — Empirical TP/FP discrimination | INCOMPLETE | <<FILL: target ACCEPTED-with-IR-team-spot-review>> | IR-team 10-IMO spot-review pass per PRD §4 Phase 1 deliverable 4 + AC2 — agreement rate on top-N rankings + false-positive rate + missing-positive rate |
| **W1** — Term taxonomy criterion | C+ (threshold semantics missing) | <<FILL: target ACCEPTED-CLEAN if (b)(i) REPAIR-AMENDMENT scribed in PRD v0.7 with explicit 3-class threshold mapping>> | PRD v0.7 §4 W1 sub-section verbatim — does it state has-WM-program-class vs adjacent-class vs absent-class threshold ranges? |
| **W2** — Scoring weights traceability | C | <<FILL: target ACCEPTED-CLEAN-OR-with-CONCERN-deferred-to-Andrew-Q2>> | Per Andrew Q2 PRD §9 weighting decision; if Andrew has ratified, render CORROBORATE; if not, render CORROBORATE-with-CONCERN-deferred |
| **W3** — Ranking output | INCOMPLETE | <<FILL: target ACCEPTED-CLEAN>> | `s3://opal-data-imo/serving/scoring.json` cardinality matches 99-IMO universe + `companies.json` + `employees.json` + IR-team-readable per AC4 |
| **M1** — Noise vs signal aggregate | CONDITIONAL | <<FILL: target ACCEPTED-CLEAN-OR-CORROBORATE-with-additives>> | Step 3.5 sub-3 consumed-output meaning probe: (i) run-to-run stability of top-N rankings + (ii) discrimination at head (does rollup_score 100-cap saturate? if so, ADDITIVE-2 v0.2 ranking-refinement fires) |
| **AC-T1** — Crawl-coverage telemetry | INCOMPLETE-MECHANISM-PRESENT-DESTINATION-EMPTY | <<FILL: target ACCEPTED-CLEAN if (b)(iv) telemetry/ emission CLOSE-LOOP per PRD v0.7 scribe + Lambda impl>> | `aws s3 ls s3://opal-data-imo/telemetry/ --recursive | wc -l` populated + AC-T1 distribution (max_depth distribution + page_count_vs_max_pages_cap ratio) at universe-scale |
| **AC-T2** — Empty-body escape-valve | STAGED | <<FILL: target ACCEPTED-CLEAN-DISPOSITION-EITHER-SHIPPED-OR-ACCEPT-WITH-TAIL>> | CTO+COO joint disposition at Phase 1 RAVC2-Accept: scraping_browser1 v0.3.0 escape-valve SHIPPED (if >5-10% empty-body) OR accept-with-known-empty-body-tail count |
| **AC2a** — Bronze-tier completeness gate | NOT-YET-EMPIRICAL | <<FILL: target ACCEPTED-CLEAN if ≥90% bronze with size > threshold + content_hash NOT in suspect-cluster>> | Empirical threshold calibration at first-99-IMO universe-run per EMPIRICAL-FIRST-RUN posture |
| **AC3a** — Phase 2A LinkedIn | NOT-RUN | <<FILL: target ACCEPTED-CLEAN>> | `gold/linkedin-scrape/{subset-slug}/{date}/` populated; ranked employee data + Series-license flags surfaced; Lusha cost-burn under per-IMO + global ceilings per cost-budgets-v0.1.json |
| **AC3b** — Phase 2B Job-postings | NOT-RUN | <<FILL: target ACCEPTED-CLEAN>> | `gold/job-posting-scrape/{subset-slug}/{date}/` populated; per-IMO hiring-pattern + Series-license + investment-keyword + hiring-velocity per role-class distribution; HAR-feasibility manifest v0.1+ EMPIRICAL-RATIFIED |
| **AC4** — Phase 3 serving tables | NOT-EXISTS | <<FILL: target ACCEPTED-CLEAN>> | `s3://opal-data-imo/serving/{companies,employees,scoring}.{json,parquet}` exist + coherent target list joining Phase 1 + Phase 2A + Phase 2B signals + time-travel archive `serving/_history/{date}/scoring.json` per Q-B |
| **AC5** — IR team review | NOT-COMPLETE | <<FILL: target ACCEPTED-CLEAN-or-with-additives>> | IR-team verdict per `.021` protocol — "rankings agree with judgment" (CLOSE-COMPLETE) OR "rankings need recalibration, here is feedback" (re-open Phase 3 scoring iteration) — either verdict closes v0.1 per PRD §7 AC5 |
| **AC6** — Run protocol doc | INCOMPLETE | <<FILL: target ACCEPTED-CLEAN if `docs/operations/find-insure-run-protocol.md` lands per ws COO TO authoring>> | doc exists + cites which Lambdas + order + dispatch source + expected duration + common failure modes |

---

## ADDITIVE axes (CVO authoring; self-validation surface)

### ADDITIVE-1 — IR-team-individual identification gate

Per CVO Mode B PRE-EXECUTION verdict `a5920688c` ADDITIVE-1 — pre-Phase-3 close-gate requires an identified named IR-team-individual consumer (not abstract "IR team"). Andrew gate-3 response per PRD §9 Q5 OR equivalent. Verifier-axis:

| Fill-at-fire | Expected anchor |
|---|---|
| <<FILL: IR-team-individual identified Y/N>> | Andrew direct citation OR ws COO `.021` protocol output identifying named individual |
| <<FILL: AC5 protocol authored>> | DS~E `.021` protocol doc-of-record |
| <<FILL: gate-fire timestamp>> | Andrew utterance OR proxy-via-COO directive |

If IR-team-individual identification GATE NOT MET: verdict shape upgrades to **CORROBORATE-with-CONCERN** (per LD-0094 verification-class) — Phase 3 mechanics CORROBORATE but ADDITIVE-1 unmet means IR-team-validation step cannot fire → soft-block on full RAVC2-Accept close-out.

### ADDITIVE-2 — Rollup_score 100-cap saturation handling

Per today's Step 3.5 CONCERN-meaning surfaced at `810211e17`: avantax saturates at 100 on 3-IMO sample. At universe-scale risk:

| Fill-at-fire | Expected anchor |
|---|---|
| <<FILL: universe-scale saturation count>> | Number of IMOs in `serving/scoring.json` with `rollup_score == 100` post-universe-run |
| <<FILL: top-N discriminability>> | Top-10 IMOs unique rollup_score values (count of distinct vs all-saturated) |
| <<FILL: v0.2 ranking-refinement disposition>> | DS~B + DS~E disposition on whether to (a) remove 100-cap + use raw rollup OR (b) percentile-rank OR (c) keep cap + accept top-saturation as design |

If >5 IMOs saturate at 100: render verdict as **CORROBORATE-with-additives** including ADDITIVE-2 (v0.2 ranking-refinement candidate). If <5 IMOs saturate: ADDITIVE-2 RESOLVED-AT-EMPIRICAL (3-IMO sample concern empirically did not materialize at universe-scale). Per LD-0095 verification-class: empirical-smoke-class (universe-empirical disposition binds).

---

## Verdict-shape fork (LD-0084 §2 4-shape taxonomy)

Per joint CVO council 2026-05-25 + LD-0094 framing-lean → explicit-verdict-on-invite + LD-0095 verification-class taxonomy:

### Path A — CORROBORATE (most-positive)

**Fires if:** all 16 axes resolve to ACCEPTED-CLEAN at empirical fill AND no ADDITIVE surfaces.

**Implication:** Phase 3 close clean; IR-team review CLOSE-COMPLETE; project moves to v0.2 post-feedback-iteration phase OR project CLOSE-COMPLETE per AC5 verdict.

### Path B — CORROBORATE-with-additives (most-probable per COO + CVO joint lean)

**Fires if:** mechanism + methodology PASS at universe-scale BUT one or more axes surface additives (most-likely candidates: ADDITIVE-2 100-cap saturation, W2 weight-tuning per Andrew Q2, IR-team v0.2 nuance feedback).

**Implication:** Phase 3 close passes with explicit ADDITIVE list materializing as v0.2 candidate axes. Per LD-0025 additive-materializes-immediately — additives roll into v0.2 PRD without re-cycle gate.

### Path C — CORROBORATE-with-CONCERN (4th-shape per LD-0094)

**Fires if:** methodology sound BUT a soft-fix surfaces requiring operational adjustment without RE-CYCLE (e.g., IR-team identifies ranking re-weighting that doesn't require code change; OR ADDITIVE-1 IR-team-individual gate UNMET but mechanism is clean).

**Implication:** Phase 3 mechanics CORROBORATE + 1-2 soft-fix recommendations fold into close-out artifact at writeup-time (driver implements without re-cycle).

### Path D — COUNTER (low-probability complete-failure path)

**Fires if:** methodology empirically fails at universe-scale (e.g., ranking is structurally non-discriminating against IR-team-known-good-set; OR REPAIR-AMENDMENT (a)+(b)(i)+(b)(iii)+(b)(iv) scribe response is mechanically-untrue against post-amendment empirical state).

**Implication:** Phase 3 RE-OPEN; PRD amendment + Lambda code revision required; full re-cycle gate.

### Decision algorithm (template fill at fire-moment)

```
if any axis grade resolves to COUNTER-grade-equivalent:
    verdict = COUNTER
elif any axis grade resolves to CORROBORATE-with-CONCERN-grade-equivalent (e.g., ADDITIVE-1 unmet + mechanism clean):
    verdict = CORROBORATE-with-CONCERN
elif any ADDITIVE surfaces (ADDITIVE-1 + ADDITIVE-2 + emergent):
    verdict = CORROBORATE-with-additives
else:
    verdict = CORROBORATE
```

---

## Constitution-drift subscan (re-run at fire)

Today's baseline (810211e17) GREEN across all 10 Articles (Art I principal mandate; Art II continuous-cycle; Art III authority distribution; Art IV non-overlap; Art V three-input cascade; Art VI earned mandate authority; Art VII /ws-charter; Art VIII doctrine codification; Art IX subordination N/A ws-scope; Art X amendment mechanism).

**Fill at fire:** re-walk per-Article empirical check on Phase 3 close-cycle window; expected GREEN persistence absent unexpected COUNTER drift.

---

## §5.6 Input 0 outcome-feedback emission (re-author at fire)

Pre-stage shape (verdict + axes fill at fire):

```json
{
  "verdict": "<<FILL: CLEAN | CONCERN | MISALIGNED>>",
  "project": "FIND_INSURE",
  "artifacts_verified": ["<<FILL: ALL Phase 0+1+2A+2B+3 artifacts + s3 paths>>"],
  "tools_gating_artifacts": ["comp-pipescript deployed", "comp-validate", "comp-iam", "comp-blast", "ds-commit-gate.sh", "safe-deploy.sh", "record-terraform-deploy.sh", "halt-gate-check.sh", "safe-commit.sh", "safe-apply.sh"],
  "axis_mechanical": "<<FILL: GREEN | YELLOW | RED>>",
  "axis_intent_coverage": "<<FILL>>",
  "axis_decision_useful": "<<FILL>>",
  "axis_constitution_coherence": "<<FILL>>",
  "constitution_drift_articles": [],
  "timestamp_utc": "<<FILL: ISO8601Z at fire>>",
  "mode": "comprehensive",
  "source": "verify-channel-ws",
  "verdict_artifact": "<<FILL: org/tier1_exec/3.0.0_SA_CVO/verify-channel/verify_channel_FIND_INSURE_phase3_close_{HHMMZ}.md>>",
  "scope_note": "<<FILL: Phase 3 close-cycle verdict per ws COO PRE-POSITION-RATIFY 2026-05-27T~23:15Z + CVO PRE-STAGE 23:20Z; fired at <<trigger conditions met>>>",
  "prior_cycle_anchors": ["5a48a72ed", "810211e17"],
  "next_class1_fire_candidate": "<<FILL: post-Phase-3 IR-team v0.2 feedback-iteration cycle OR project CLOSE-COMPLETE>>"
}
```

---

## Routing pre-stage (verdict-driven; fill at fire)

| Verdict | ws CTO routing | ws COO routing | DS lanes routing | MSTR routing |
|---|---|---|---|---|
| CORROBORATE | none (clean close) | RAVC2-ACCEPT-FINAL fire-and-forget | CC informational on close | informational CC |
| CORROBORATE-with-additives | additive list per LD-0025 materializes-immediately into v0.2 spec | RAVC2-ACCEPT + v0.2 TO authoring for ADDITIVE-X items | additive items dispatch per lane | informational CC |
| CORROBORATE-with-CONCERN | soft-fix recommendation per LD-0094 verification-class | RAVC2-ACCEPT-with-CONCERN; soft-fix folds into close-out artifact | none required if soft-fix is alignment-class | informational CC |
| COUNTER | RE-OPEN PRD amendment scope | RE-OPEN TO scope | RE-OPEN lane work | ASK-MSTR-ratify on re-open scope per Art VI escalation chain |

---

## Materialization estimate (wall-time at fire)

Per [[feedback_cvo_proactive_verdict_landing_pattern]] empirical baseline:
- Cold-start Mode B comprehensive (no pre-stage): ~2-3h wall (reading PRD + commits + per-path verify + verdict authoring)
- Pre-staged Mode B at fire: ~15-30min wall (empirical anchor fills + verdict-fork decision + commit + push + MCP routing)
- Compression: ~75-90% wall-time reduction

This template is the compression mechanism. Fill at fire; do not pre-commit verdict.

---

## ws COO chain-state acknowledgment (pre-stage moment)

Per ws COO [PRE-POSITION-RATIFY] 23:15Z body:
- Phase 1 P3 leg = CLOSED via FIND_INSURE.007 `3ee6ee869` + RAVC2-ACCEPT-CLOSE 23:08Z ✓
- Phase 1 P1 leg = AE 0.7~A Stage 1 dispatching (.008 subset config `798a7dab7`)
- Phase 3 enabling = DS~E pre-staging .023 design + code
- Phase 2A LIVE-DISPATCH (DS~C) = .024 STAGED (gates .011 RAVC2 + Andrew Q1)
- Phase 2B Stage Bα (DS~D) = .025 STAGED (gates Andrew HAR supply)
- Phase 3 close-commit template = pre-authored at `docs/briefs/find-insure-phase3-close-template.md`

Chain is loaded; gates clear; CVO standby at this template fill-trigger ready posture.
