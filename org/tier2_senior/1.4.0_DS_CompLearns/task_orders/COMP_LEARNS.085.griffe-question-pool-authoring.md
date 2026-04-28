# Task Order: COMP_LEARNS.085 — griffe v2.0.0 Question Pool Authoring

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.4.0_DS_CompLearns
**Status:** <status>pending</status>
**Date:** 2026-04-27
**Priority:** P0 — gates Stage 3 Path B pre-screen

---

## Objective

Author the question pool for griffe v2.0.0 — the Stage 3 Path B primary target. This pool feeds
the SC pre-screen (COMP_LEARNS.086), which determines whether griffe qualifies (INCLUDE ≥ 5) for
packet authoring and the 4-condition primary case dispatch.

**Target:** griffe v2.0.0 (mkdocstrings/griffe, tag v2.0.0, January 2026)
**Source path:** `packages/griffelib/src/griffe/_internal/` — v2 monorepo layout
  - NOTE: v1.x used `src/griffe/` — that path does NOT exist in v2.0. Use the monorepo path above.
**Prior-gap basis:** CTO confirmed at 20260427T223435Z — 17,417 Python LOC (49 files), post-cutoff
  monorepo restructure. Pre-cutoff models would expect v1.x flat layout, not this structure.

CTO target ruling: PRIMARY confirmed (OQ-1 RESOLVED inline, OQ-3/OQ-4 ruled, dispatch sequence
approved). Sub-PRD V1 ACCEPTED (b98c56e0 drafted, CTO ACK 20260427T223435Z).

---

## Deliverable

`comp/backlog/benchmark/bl-griffe-001.yaml` — question pool file.

- ≥ 12 candidate questions
- ≥ 2 distinct question families (target 4 per V1.3 §7.4 guardrail — see below)
- Post-c5f5c89d canonical schema (answer_type + values, NOT gold_answer legacy)
- Full provenance per question (gold_source_file, gold_source_line, verification_note)

---

## Question pool schema (post-c5f5c89d canonical)

```yaml
questions:
  - id: griffe-001
    question: "..."
    answer_type: set_membership          # set_membership | enumerable | code_extraction | numeric | yes_no
    values: [...]                         # the correct answer set or value list
    gold_source_file: "packages/griffelib/src/griffe/_internal/<file>.py"
    gold_source_line: <N>
    verification_note: "How to verify answer by reading the source"
    question_family: A                    # A | B | C | D (see families below)
    difficulty: medium                    # low | medium | high
```

CRITICAL: Do NOT use `gold_answer:` field. That is the legacy sphinx schema. Use `answer_type:` + `values:`.

---

## Required question families (V1.3 §7.4 guardrail: ≥ 2, target 4)

| Family | Type | griffe example surfaces |
|--------|------|------------------------|
| A | set_membership | Direct subclasses of DocstringSection; classes implementing a specific base in expressions.py; members of an enum |
| B | enumerable | DocstringStyle enum values; valid extension hook names from the griffe extensions API; inspector strategy names |
| C | code_extraction | Default parameter value of GriffeLoader.load(); return type of get_member() for a missing key; default value of max_bases |
| D | numeric | Number of distinct expression types extending ExprSubscript; count of built-in extension hooks; number of DocstringSection subclasses |

You must author questions from at least 2 families. Target 4 families (A+B+C+D) for margin against
the §7.4 guardrail. A pool of 12 questions all from Family A will be rejected at gate-2.

Family A ceiling rule: no more than 6 of 12 questions may be Family A (set_membership).

---

## Gold-key sourcing strategy (OQ-5 decision — COO endorsed, CTO noted sound)

**Primary source:** griffe v2.0.0 migration guide (v1.x → v2.x breaking changes).
Each breaking change documents a structural difference in the new layout — that anchors a question.
The migration guide is the richest source of facts a pre-cutoff model would NOT know.

**Supplementary (2-3 questions):** historical bug reports from mkdocstrings/griffe issue tracker.
These simulate the "hard real-world fix" framing and add variety beyond migration-anchored facts.

**Avoid:** questions whose answers are directly exposed in popular tutorials, top-level README,
or extensively documented public API in pre-cutoff docs. The prior-gap is structural, not documentary.

---

## Content discipline

- All answers must be derivable from Python source in `packages/griffelib/src/griffe/_internal/`
- Do not source answers from griffe's own docstrings if those docstrings are auto-generated from
  well-known pre-cutoff public API (those would be prior-dominated)
- Each `gold_source_file` must be a real file path in the v2.0.0 monorepo layout
- Each `gold_source_line` must be the line number in v2.0.0 where the answer is derivable
- `verification_note` must be specific enough for SC to re-verify independently
- Do NOT write questions about v1.x class names / paths that no longer exist in v2.0

---

## Compiler tools mandate

```xml
<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>cd /c/Users/AndrewBerman/Desktop/feature_clb && comp-build && pytest comp/ -v -q 2>&1 | tail -20</run>
      <expect>All existing tests PASS. Exit 0.</expect>
      <if_mismatch>STOP. Do not write until baseline is green. Surface to COO immediately.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>pytest comp/ -v -q 2>&1 | tail -20</run>
      <expect>All tests PASS. No regressions. Exit 0.</expect>
      <if_mismatch>STOP. Do not commit.</if_mismatch>
    </step>
    <step>
      <run>python -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-griffe-001.yaml')); qs=d['questions']; assert len(qs)>=12, f'Only {len(qs)} questions'; families=set(q.get('question_family') for q in qs); assert len(families)>=2, f'Only {len(families)} families: {families}'; print(f'PASS: {len(qs)} questions, {len(families)} families: {families}')"</run>
      <expect>PASS: ≥12 questions, ≥2 families listed. Exit 0.</expect>
      <if_mismatch>STOP. Add more questions or distribute across additional families.</if_mismatch>
    </step>
    <step>
      <run>python -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-griffe-001.yaml')); bad=[q.get('id','?') for q in d['questions'] if 'gold_answer' in q]; assert not bad, f'Legacy gold_answer field in: {bad}'; print('PASS: no legacy gold_answer fields')"</run>
      <expect>PASS: no legacy gold_answer fields. Exit 0.</expect>
      <if_mismatch>Replace gold_answer with answer_type + values per post-c5f5c89d canonical schema.</if_mismatch>
    </step>
    <step>
      <run>python -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-griffe-001.yaml')); missing=[q.get('id','?') for q in d['questions'] if not all(k in q for k in ['gold_source_file','gold_source_line','verification_note'])]; assert not missing, f'Missing provenance in: {missing}'; print('PASS: all questions have provenance fields')"</run>
      <expect>PASS: all questions have provenance fields. Exit 0.</expect>
      <if_mismatch>Add missing gold_source_file / gold_source_line / verification_note to flagged questions.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-build</run>
      <expect>Rebuild succeeds. No stale-cache warnings.</expect>
      <if_mismatch>Surface to COO — likely concurrent commit during your write.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>
```

---

## Acceptance criteria

1. `comp/backlog/benchmark/bl-griffe-001.yaml` committed to CLOUD from feature_clb
2. ≥ 12 candidate questions authored
3. ≥ 2 distinct question families present (gate-2 Python check exits 0)
4. Family A questions ≤ 6 of 12 (no single-family dominance)
5. Post-c5f5c89d schema throughout — `answer_type` + `values`, no `gold_answer` legacy field
6. All provenance fields present: `gold_source_file`, `gold_source_line`, `verification_note`
7. All `gold_source_file` paths reference `packages/griffelib/src/griffe/_internal/` (v2 monorepo layout)
8. Session log with Compiler Tools section (Phase 1/2/3 `<run>` outputs reproduced, pass/fail vs `<expect>`)
9. RAVC COMPLETE MCP to 2.1.0_SA_COO with commit hash + question count by family

---

## Cross-domain coordination

```xml
<cross_domain_coordination>
  <none/>
</cross_domain_coordination>
```

New YAML file under `comp/backlog/benchmark/`. No other active TOs touch this path.

---

## Evidence format (RAVC COMPLETE MCP)

```
Subject: COMPLETE — COMP_LEARNS.085 griffe question pool
Body:
  Commit: <hash>
  File: comp/backlog/benchmark/bl-griffe-001.yaml
  Questions: <N total> (A=N, B=N, C=N, D=N)
  Gate-2 outputs (3 checks): PASS / PASS / PASS
  Session log: org/tier2_senior/1.4.0_DS_CompLearns/logs/2026-04-27/<file>.md
```

---

## Dependencies

- OQ-1 resolved (CTO inline, 17,417 LOC) — COMPLETE
- Sub-PRD V1 ACCEPTED (CTO ACK 20260427T223435Z) — COMPLETE
- Post-c5f5c89d schema canonicalization (c5f5c89d) — COMPLETE

**Downstream blocked on this TO:**
- COMP_LEARNS.086 — SC pre-screen (2.1.0_SC_CompLearns) — cannot dispatch until this ships

---

## Sequence context (§6 dispatch sequence, sub-PRD)

1. OQ-1 RESOLVED (17,417 LOC) — done
2. **THIS TO** — question pool authoring → 1.4.0_DS, griffe v2.0.0
3. COMP_LEARNS.086 — pre-screen → 2.1.0_SC (after this ships)
4. CTO off-ramp ruling: INCLUDE ≥ 5 → packet authoring + 4-condition case dispatch; < 5 → fallback to awkward-array

---

## Session log

Required. Include:
- Objective
- Work completed (source files browsed, questions authored, decisions made per family)
- Compiler Tools section (Phase 1/2/3 `<run>` outputs)
- Files modified
- Current state on completion
- RAVC COMPLETE evidence
