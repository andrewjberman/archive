# [Template] CTO to CVO Report — Wave Gate / Project Close / PRD Ship / Stage Gate

Copy this file to `../inbox/{YYYYMMDDTHHMMSSZ}_from_{your_serial}_{subject_slug}.md` and
fill in every section. Delete template commentary (italic notes) before committing.

---

## Frontmatter

```yaml
---
from: 1.0.0_SA_CTO                       # or "1.0.0_SA_CTO + 2.0.0_SA_COO" for joint sign
to: 3.0.0_SA_CVO
trigger: wave_gate                        # wave_gate | project_close | prd_ship | stage_transition | surprising_result | cross_project_dep | periodic
phase: ADHC_WAVPLN Wave 1                 # current phase/wave/project identifier
gate_reference: ADHC_WAVPLN.WAVE1        # primary TO or project code this report is closing or gating
prd_authority: docs/architecture/{PRD}.md @ {commit} (rev{N})
report_date: {YYYY-MM-DD}
ask_shape: mechanism-specific            # mechanism-specific | go-no-go | advisory-only
---
```

---

## §0 — Why you are reading this

*One short paragraph. Frame the report in terms of the Opal Capital delivery purpose.
Why does this wave / close / gate matter for the organization's data pipeline, client
platform, or infrastructure — not just the immediate project step?*

---

## §1 — Exec summary

*3-5 sentences. What happened. What was surprising (if anything). The single sentence
that if the reviewer read only one line, they would still have the point.*

---

## §2 — Gate or wave outcomes (table)

*For a wave gate: every project or TO in this wave, one row per item.*
*For a project close: milestone-level outcomes, one row per phase.*
*For a PRD ship: diff summary — what changed from prior version.*
*For a stage gate: criteria matrix — each criterion and pass/fail verdict.*

| Project / Item | Status | Shipped artifact / commit | Blocking issues | Evidence |
|----------------|--------|--------------------------|-----------------|----------|
| ADVI_HISTBF Wave B | COMPLETE | `org/.../session_wave_b.md:12` | None | `org/projects/ADVI_HISTBF.json` |
| ADVI_JWTRES Option A | LIVE | `81a7a5684` | Option B TBD | `org/projects/ADVI_JWTRES.json:11` |

*Add quantitative deltas in a supporting table if available.*

---

## §3 — What shipped / what improved

*Structural gains vs the prior wave or baseline. Not hype. If this gate improved
over-and-above prior, say what improved and point to evidence. If this gate did
NOT improve on an axis, surface that explicitly — do not hide it.*

- ...

---

## §4 — Failures / integrity findings / surprising results

*Everything that did not go as expected. Silent failures, unconfirmed dispatches,
IAM gaps, stuck DT agents, stale REGISTRY rows. Name the failure mode at mechanism
level — not "something went wrong" but "AE 0.6.1 Wave B GO sent 18h+ with no EC2
start confirmation because no sentinel file and no session continuity."*

- ...

---

## §5 — Non-findings (what you explicitly did NOT evaluate)

*If the gate excluded something deliberately, name it. Prevents CVO from pointing
out gaps you already scoped out.*

- Example: "TRSB_PATHFIX DT spawn decision — deferred to Andrew; outside CVO scope."

---

## §6 — Open questions — per driver

*Structured. Every question MUST be tagged with its addressed driver
(CTO / COO / DS / AE / DT). Cross-cutting questions CAN be tagged with multiple drivers
but must name each.*

### For CTO

**Q1.** [Grounded in a specific file:line observable] ... [specific enough that
CVO can give a mechanism-level answer, not a generic one].

**Q2.** ...

### For COO

**Q3.** ...

### For DS

**Q4.** ...

### For AE

**Q5.** ...

### For DT

**Q6.** ...

*Aim for 3-9 questions total across all drivers. More than 9 means the questions
are too broad or you are batching what should be two reports.*

---

## §7 — Evidence paths

*Every file/line the reviewer would need to reproduce the analysis. Group by purpose.*

### Project and PRD framing

- `org/projects/REGISTRY.md` — active project registry
- `org/projects/{PROJECT_CODE}.json` — project state JSON
- `docs/architecture/{PRD}.md` — relevant PRD

### Execution artifacts (primary evidence)

- `org/tier2_senior/{agent_serial}/logs/{date}/{session_log}.md:NN` — key session log entry
- `org/tier2_senior/{agent_serial}/task_orders/{TO_code}.md` — TO being closed or gated
- `infra/aws/lambda/ci/lambda-source-map.json` — Lambda source truth (if Lambda changes in scope)
- `infra/aws/ec2/EC2_MANIFEST.json` — EC2 service truth (if EC2 work in scope)

### Git evidence

- `git log --oneline --author={agent_serial} --since={date}` — recent commits by agent
- `{commit_hash}` — specific commit or tag (e.g., `inf-pipeline-v1.7.9`)

### COO / CTO session logs

- `org/tier1_exec/1.0.0_SA_CTO/logs/{date}/{session_log}.md` — CTO session narrative
- `org/tier1_exec/2.0.0_SA_COO/logs/{date}/{session_log}.md` — COO session narrative

---

## §8 — Scope of what you are asking for

**In scope:**
- Mechanism-specific critique grounded in enumerated evidence
- Priority-ranked recommendations per driver
- Unknown-unknowns — what we did not know to ask
- Sharp "this is the wrong design" calls

**Out of scope (we will not act on):**
- Generic "monitor more" recommendations — we already do
- Recommendations requiring data not in evidence paths (flag as P2 if worth future work)
- Re-litigating Andrew rulings already locked in project JSONs or session logs
- Scope expansion beyond what the current wave/gate authorized

---

## §9 — What happens after your response

*Commit to how the CVO feedback will be processed.*

- CTO + COO dyad reads each recommendation and attributes it to: PRD amendment, TO amendment, follow-on TO, or explicit deferral
- Each adopted recommendation cites the CVO response filename in the commit message
- Deferrals are captured in the gate decision record with explicit rationale
- CVO response archives to `archives/{gate_ref}/` after the synthesis commit lands

---

## §10 — One-line summary if you only read this

*One sentence. What happened. What is the single most important question you are asking.*

---

*End of report.*
