# Task Order: COMP_LEARNS.087 — awkward-array v2.9.0 Vendor + Question Pool

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.1.0_DS_CompLearns
**Status:** <status>complete</status>
**Date:** 2026-04-28
**Priority:** P0 — Wave 1 fallback preparation; parallel with .086 SC pre-screen

---

## Context

.086 SC pre-screen is executing on griffe (Wave 1 primary). awkward-array is the established
Wave 1 fallback target per Path B sub-PRD V1 ACCEPTED (ef8da939). Survey data is at
`comp/results/path_b_candidates/candidate_survey.md` (.084, 22d4ddee). G1 (survey → select)
was satisfied by .084 + Path B sub-PRD ACK — no fresh CTO ACK gate required before vendoring.

This TO runs in parallel with .086. Do NOT wait for .086 result.

---

## Objective

Vendor awkward-array v2.9.0 under `comp/targets/awkward_array/` and author a question pool
at `comp/backlog/benchmark/bl-awkward-array-001.yaml` per V1.3 §7.4 guardrail.

---

## Phase 0 — Vendor and pin

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git clone --depth 1 --branch v2.9.0 https://github.com/scikit-hep/awkward comp/targets/awkward_array/_repo
cd comp/targets/awkward_array/_repo
git rev-parse HEAD > ../repo_pin.txt
echo "tag: v2.9.0" >> ../repo_pin.txt
echo "date: 2026-02-08" >> ../repo_pin.txt
```

Verify source path after clone. The Python layer is expected at `src/awkward/` (modern packaging
layout). Confirm the actual path and note it in your session log. All gold_source_file values
must use the confirmed path prefix.

**Prior-gap basis (from .084 survey):** 957 stars, niche particle-physics domain (scikit-hep),
v2.9.0 is Feb 2026 (post-cutoff). Content-type hierarchy and reducer machinery are not covered
in general Python tutorials. Pre-cutoff models have conceptual awareness but not implementation
specifics.

---

## Phase 1 — Question pool authoring

Deliverable: `comp/backlog/benchmark/bl-awkward-array-001.yaml`

**Schema (post-c5f5c89d canonical):**
```yaml
questions:
  - id: awkward-array-001
    question: "..."
    answer_type: set_membership | enumerable | code_extraction | numeric | yes_no
    values: [...]
    gold_source_file: "src/awkward/<path>/<file>.py"
    gold_source_line: <N>
    verification_note: "..."
    question_family: A | B | C | D
    difficulty: low | medium | high
```

CRITICAL: `answer_type` + `values` only. No `gold_answer` legacy field.

**Required families (V1.3 §7.4):** ≥ 2 distinct, target all 4.

| Family | Type | awkward-array surfaces |
|--------|------|----------------------|
| A | set_membership | Which content class handles variable-length lists? Which classes directly inherit from Content? What mixin does RecordArray use for field access? |
| B | enumerable | All direct subclasses of Content in contents/; valid behavior registration methods; reducer strategy names |
| C | code_extraction | Default parameter value of axis= in reduce operations; return type of layout() call; default value of check_valid |
| D | numeric | Count of direct Content subclasses; number of registered builtin behaviors; count of parameters in ArrayBuilder.__init__ |

**Gold key strategy:**
- Primary: class hierarchy in `src/awkward/contents/` — each content type is a file; which class inherits what, which methods are abstract. Low prior, mechanically verifiable.
- Supplementary: reducer dispatch mechanics in `src/awkward/_reducers.py` or `_reducers/`; behaviors registration in `src/awkward/behaviors/`.
- Avoid: top-level `ak.*` function signatures that are documented prominently in the README/quickstart (those have high prior).

**Family A ceiling:** ≤ 6 of 12 questions may be set_membership.

---

## Phase 2 — Gate-2 checks (before commit)

```bash
python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-awkward-array-001.yaml')); qs=d['questions']; assert len(qs)>=12, f'Only {len(qs)} questions'; families=set(q.get('question_family') for q in qs); assert len(families)>=2, f'Only {len(families)} families: {families}'; print(f'PASS: {len(qs)} questions, {len(families)} families: {families}')"

python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-awkward-array-001.yaml')); bad=[q.get('id','?') for q in d['questions'] if 'gold_answer' in q]; assert not bad, f'Legacy gold_answer in: {bad}'; print('PASS: no legacy gold_answer fields')"

python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-awkward-array-001.yaml')); missing=[q.get('id','?') for q in d['questions'] if not all(k in q for k in ['gold_source_file','gold_source_line','verification_note'])]; assert not missing, f'Missing provenance in: {missing}'; print('PASS: all provenance fields present')"
```

All 3 must exit 0.

---

## Phase 3 — Commit and push

```bash
git add comp/targets/awkward_array/ comp/backlog/benchmark/bl-awkward-array-001.yaml
.tools/safe-commit.sh --author "1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.087): awkward-array v2.9.0 vendor + question pool -- N questions, A=N B=N C=N D=N" \
  -- comp/targets/awkward_array/ comp/backlog/benchmark/bl-awkward-array-001.yaml
git push origin CLOUD
```

Replace N with actual counts.

---

## Acceptance criteria

1. `comp/targets/awkward_array/_repo/` cloned at v2.9.0 tag
2. `comp/targets/awkward_array/repo_pin.txt` present (commit hash + tag + date)
3. `comp/backlog/benchmark/bl-awkward-array-001.yaml` committed
4. ≥ 12 candidate questions
5. ≥ 2 distinct families (gate-2 check 1 exits 0); target 4
6. Family A ≤ 6 of 12 (≤ 50%)
7. Post-c5f5c89d schema throughout (gate-2 check 2 exits 0)
8. All provenance fields present (gate-2 check 3 exits 0)
9. All gold_source_file paths reference the actual v2.9.0 source (confirmed on clone)
10. Committed with author 1.1.0_DS_CompLearns, pushed to CLOUD
11. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + question count by family + gate-2 outputs

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.087 awkward-array question pool
Body:
  Commit: <hash>
  File: comp/backlog/benchmark/bl-awkward-array-001.yaml
  Vendor: comp/targets/awkward_array/_repo/ @ v2.9.0 (<commit hash>)
  Questions: <N total> (A=N, B=N, C=N, D=N)
  Gate-2: PASS / PASS / PASS
  Source path confirmed: <actual path found on clone>
```

---

## Dependencies

- .084 candidate survey (22d4ddee) — COMPLETE
- Path B sub-PRD V1 ACCEPTED (ef8da939) — COMPLETE; awkward-array is the established fallback target
- No other active TOs gate this

**Downstream blocked on this TO:**
- COO CTO G2 pool review (per INTAKE_WAVE §4 — CTO reviews pool after delivery)
- SC pre-screen for awkward-array (only if griffe fails .086 off-ramp OR as Wave 2 target)
