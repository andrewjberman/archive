# Task Order: COMP_LEARNS.089 — cattrs Targeted Prior Assessment

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.2.0_DS_CompLearns
**Status:** <status>complete</status>
**Date:** 2026-04-28
**Priority:** P1 — gates CTO prior ruling on cattrs as Wave 2 candidate

---

## Context

cattrs (python-attrs/cattrs) was rated BORDERLINE in the .084 survey (22d4ddee) with the note
"surface to CTO for prior ruling." The specific concern: cattrs has 967 stars and is
well-documented in Python tutorials, but its internal implementation structure may be
low-prior even if the API surface is known. CTO has not yet issued a prior ruling.

This TO is remote-only (WebSearch + WebFetch). No cloning. No COMP_LEARNS harness compute.
Goal: produce enough evidence for CTO to issue a definitive PASS or REJECT on the prior criterion.

---

## Objective

Author `comp/results/path_b_candidates/cattrs_prior_assessment.md` — a structured prior
assessment that answers the key question: could a 16-question pool from cattrs source contain
≥ 5 INCLUDE-class questions under V1.2 dual-grader governance?

---

## Phase 1 — Prior surface assessment (WebSearch/WebFetch only)

Investigate the following surfaces and document findings:

### 1a — API surface prior (what pre-cutoff models likely know)
- Search for cattrs tutorials, Real Python articles, blog posts from 2023–2025
- What converter patterns, structuring/unstructuring mechanics, and hook registration
  patterns are prominently documented?
- What parts of the API are in the README, quickstart docs, official tutorial?

### 1b — Internal implementation prior (what models likely don't know)
- What is the actual class hierarchy inside `src/cattrs/`? Is there a disambiguator,
  converter base, or hook registry implementation that is NOT in top-level tutorials?
- cattrs v24.x–v25.x (post-cutoff) changelog — what structural changes landed in 2025?
  These would be genuine knowledge gaps for Aug 2025 cutoff models.
- GitHub: `python-attrs/cattrs` releases page — what shipped after Aug 2025?

### 1c — Question pool viability check
Sketch 8 candidate questions from internal implementation surfaces (not API surface):
- Must be answerable only by reading `src/cattrs/` Python source
- Must NOT be answerable from the public API docs / README / top-level tutorials
- If ≥ 8 such questions can be sketched, the pool likely has INCLUDE headroom

---

## Phase 2 — Deliverable

File: `comp/results/path_b_candidates/cattrs_prior_assessment.md`

Structure:
```markdown
# cattrs Prior Assessment — COMP_LEARNS Stage 3 Wave 2 Candidacy

**Author:** 1.2.0_DS_CompLearns
**Date:** 2026-04-28
**Target:** cattrs (python-attrs/cattrs), candidate release: v25.x (latest stable post-cutoff)

## §1 — Prior surface summary
[What pre-cutoff models know from tutorials/docs]

## §2 — Internal implementation gap
[What is NOT in tutorials — internal class hierarchy, hook registry, disambiguator mechanics]
[Post-cutoff structural changes (v24.x/v25.x) that create genuine knowledge gaps]

## §3 — Candidate question sketches (≥ 6, target 8)
[Questions answerable only from src/cattrs/ source — not from API docs]
[Include question_family tag for each: A/B/C/D]

## §4 — COO assessment
PASS — internal implementation gap is large enough; pool likely yields ≥ 5 INCLUDE post-triage
  OR
BORDERLINE — prior surface is moderate; pool might reach INCLUDE ≥ 5 but risk is non-trivial
  OR
REJECT — prior too high; even internal questions would be dominated by model knowledge of the API

## §5 — CTO ruling request
[Single sentence: what ruling is needed from CTO to proceed or drop]
```

---

## Phase 3 — Commit and push

```bash
git add comp/results/path_b_candidates/cattrs_prior_assessment.md
.tools/safe-commit.sh --author "1.2.0_DS_CompLearns <1.2.0_DS_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.089): cattrs prior assessment -- [PASS|BORDERLINE|REJECT]" \
  -- comp/results/path_b_candidates/cattrs_prior_assessment.md
git push origin CLOUD
```

---

## Acceptance criteria

1. `comp/results/path_b_candidates/cattrs_prior_assessment.md` committed + pushed
2. §1–§4 all authored (prior surface, implementation gap, ≥ 6 candidate questions sketched, COO assessment)
3. §5 specifies the CTO ruling ask explicitly
4. RAVC COMPLETE MCP to 2.1.0_SA_COO with: commit hash + COO assessment verdict (PASS/BORDERLINE/REJECT) + one-sentence rationale

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.089 cattrs prior assessment | [PASS|BORDERLINE|REJECT]
Body:
  Commit: <hash>
  Assessment: PASS / BORDERLINE / REJECT
  Rationale: <one sentence>
  CTO ruling request: <what ruling is needed>
  Full report: comp/results/path_b_candidates/cattrs_prior_assessment.md
```

---

## Dependencies

- .084 candidate survey (22d4ddee) — COMPLETE (cattrs listed as BORDERLINE)
- No other TOs gate this
- Downstream: CTO prior ruling on cattrs candidacy (gates Wave 2 TO if PASS/BORDERLINE)
