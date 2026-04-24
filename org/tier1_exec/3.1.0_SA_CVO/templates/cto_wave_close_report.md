# [Template] CTO → CVO Report — Wave Close / PRD Ship / Stage Gate

Copy this file to `../inbox/{YYYYMMDDTHHMMSSZ}_from_{your_serial}_{subject_slug}.md` and
fill in every section. Delete template commentary (italic notes) before committing.

---

## Frontmatter

```yaml
---
from: 1.1.0_SA_CTO                       # or "1.1.0_SA_CTO + 2.1.0_SA_COO" for joint sign
to: 3.1.0_SA_CVO
trigger: wave_close                      # wave_close | prd_ship | stage_transition | surprising_result | plateau | periodic
phase: Wave 3a                           # current phase/wave identifier
wave_reference: COMP_LEARNS.051          # primary TO or commit this report is closing
prd_authority: docs/architecture/COMP_LEARNS_WAVE3_V1.md @ bd84ef10 (rev5)
report_date: 2026-04-24
ask_shape: mechanism-specific-chokepoints  # mechanism-specific-chokepoints | go-no-go | advisory-only
---
```

---

## §0 — Why you're reading this

*One short paragraph. Frame the report in terms of the COMP_LEARNS program purpose
(`docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md`). Why does this wave / ship / gate
matter for the end-state comparative-eval program, not just the immediate project step?*

---

## §1 — Exec summary

*3-5 sentences. What happened. What was surprising (if anything). The single
sentence that if the reviewer read only one line, they'd still have the point.*

---

## §2 — Wave outcomes (table)

*Every wave has objectively-scored outcomes. Lay them out in a table. One row per
case/condition/run. If PRD ship: replace this with "diff summary." If stage gate:
replace with "criteria matrix."*

| Case | Condition | Verdict | Primary metric | Wall-clock | Tokens | Δ vs baseline | Evidence |
|------|-----------|---------|----------------|------------|--------|----------------|----------|
| case-003-sphinx | aided (condition_b, 1.3.0_DS) | PASS | — | 195s | 15200 | — | `comp/results/wave-3a/verdicts/case-003-ds-1.3.0-condition_b-run-1.json` |
| case-003-sphinx | unaided (condition_a, 1.4.0_DS) | PASS | — | 105s | 4400 | — | `comp/results/wave-3a/verdicts/case-003-ds-1.4.0-condition_a-run-1.json` |

*Add every quantitative delta in a supporting table if helpful. Metric audit JSON
files go in the evidence path section.*

---

## §3 — Improvements over prior wave

*Structural gains vs the prior wave (or baseline if first wave). Not hype. If this
wave improved over-and-above prior, say what improved and point to evidence. If
this wave did NOT improve on an axis, surface that explicitly — do not hide it.*

- ...

---

## §4 — Failures / integrity findings / surprising results

*Everything that did not go as expected. Integrity findings, measurement
invalidations, counter-directional results, aborted sub-experiments. Name the
failure mode at mechanism level — "self-scoring bundle" not "lane A didn't work."*

- ...

---

## §5 — Non-findings (what you explicitly did NOT measure)

*If the wave design excluded something deliberately, name it. Prevents CVO from
pointing out gaps you already scoped out. Keeps the critique on real gaps.*

- Example: "Cross-model DS comparison — PRD §9 explicitly defers to Wave 4; not in this wave's scope."

---

## §6 — Open questions — chokepoints, per driver

*Structured. Every question MUST be tagged with its addressed driver
(CTO / COO / SC / DS). Cross-cutting questions CAN be tagged with multiple drivers
but must name each.*

### For CTO

**Q1.** [Grounded in a specific observable] ... [question specific enough that
Codex can give a mechanism-level answer, not a generic one].

**Q2.** ...

### For COO

**Q3.** ...

### For SC

**Q4.** ...

### For DS

**Q5.** ...

*Aim for 3-9 questions total across all drivers. More than 9 means the questions
are too broad or you're batching what should be two reports. Fewer than 3 means
the wave probably didn't actually need CVO review.*

---

## §7 — Evidence paths

*Every file/line the reviewer would need to reproduce the analysis. Group by purpose.*

### PRD / architectural framing

- `docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md` — program purpose
- `docs/architecture/COMP_LEARNS_WAVE3_V1.md` — wave PRD, current rev
- `docs/architecture/COMP_LEARNS_ARCHITECTURE.md` — structural reference

### Case artifacts (primary evidence)

- `comp/tasks/{case}/packet.yaml` — task definition
- `comp/tasks/{case}/bundles/{agent}/reasoning.md` — agent narrative
- `comp/tasks/{case}/bundles/{agent}/nav_log.jsonl` — per-file-open trail
- `comp/tasks/{case}/bundles/{agent}/changes.patch` — fix applied

### Scoring + metric audit

- `comp/results/{wave}/verdicts/{case}-{agent}-run-1.json` — Phase 1 frozen verdict
- `comp/results/{wave}/metric_audit/{case}-efficiency-delta.json` — Phase 2 metric audit

### Decision records

- `comp/results/{wave}/coo-review-memo.md` — COO review memo
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.{NN}.{decision}.md` — CTO decision record
- `org/tier1_exec/1.1.0_SA_CTO/logs/{date}/{session_log}.md` — narrative session log

---

## §8 — Scope of what you're asking for

**In scope:**
- Mechanism-specific critique grounded in enumerated evidence
- Priority-ranked recommendations per driver
- Unknown-unknowns — what we didn't know to ask
- Sharp "this is the wrong design" calls

**Out of scope (we will not act on):**
- Generic "collect more data" recommendations — we already are
- Recommendations that require data we don't have (flag as P2 if worth future work)
- Re-litigating scope honesty caveats (already captured in our PRD §X.Y)
- Scope expansion beyond what the wave PRD authorized

*Be explicit about what is NOT useful. The ask-shape is the strongest signal of
what kind of reviewer attention you want.*

---

## §9 — What happens after your response

*Commit to how the CVO feedback will be processed. Builds trust that effort spent
is not wasted.*

- CTO + COO dyad reads each recommendation and attributes it to: PRD amendment (before next wave), TO amendment (current wave's TOs), follow-on TO (Wave N+1), or explicit deferral
- Each adopted recommendation cites the CVO response filename in the commit message
- Deferrals are captured in the wave-close synthesis with explicit rationale
- CVO response archives to `archives/wave_{ref}/` after the synthesis commit lands

---

## §10 — One-line summary if you only read this

*One sentence. What happened. What's the single most important question you're asking.*

---

*End of report.*
