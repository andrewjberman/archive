# Task Order: COMP_LEARNS.088 — hishel v1.2.1 LOC Verify + Conditional Vendor + Question Pool

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.3.0_DS_CompLearns
**Status:** <status>complete</status>
**Completion commit:** <completion_commit>7609c631</completion_commit>
**Completion date:** <completion_date>2026-04-28</completion_date>
**Date:** 2026-04-28
**Priority:** P1 — conditional; LOC gate must pass before authoring proceeds

---

## Context

hishel is a conditional candidate from the .084 survey (22d4ddee). REQUIRED criterion 8 (≥ 10k
Python LOC) and question diversity (≥ 12) are both flagged as UNCERTAIN. This TO has a hard
LOC gate: clone → cloc → if Python LOC ≥ 10k proceed to vendor + question pool; if < 10k
STOP and MCP COO + CTO with the LOC report.

Do NOT skip Phase 0. Do NOT proceed to authoring without confirming LOC ≥ 10k.

---

## Phase 0 — LOC gate (REQUIRED before any authoring)

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git clone --depth 1 --branch v1.2.1 https://github.com/karpetrosyan/hishel /tmp/hishel_loc_check
pip install cloc 2>/dev/null || true
# Use cloc or count manually:
find /tmp/hishel_loc_check -name "*.py" | xargs wc -l | tail -1
```

**Gate:** If Python LOC < 10,000 → STOP. Write a brief LOC report to
`comp/results/path_b_candidates/hishel_loc_check.md` and MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
with the count. Do NOT proceed to vendoring or authoring.

If Python LOC ≥ 10,000 → proceed to Phase 1.

---

## Phase 1 — Vendor and pin (only if LOC gate passes)

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git clone --depth 1 --branch v1.2.1 https://github.com/karpetrosyan/hishel comp/targets/hishel/_repo
cd comp/targets/hishel/_repo
git rev-parse HEAD > ../repo_pin.txt
echo "tag: v1.2.1" >> ../repo_pin.txt
echo "date: 2026-04-27" >> ../repo_pin.txt
```

**Architecture (from .084 survey):**
- `hishel/_controller.py` — RFC 9111 freshness + re-validation logic
- `hishel/_storages.py` (or `_storages/`) — FileSystem, Redis, SQLite, InMemory backends
- `hishel/_serializers.py` — Pickle, MsgPack, YAML serializers
- `hishel/_transports.py` (sync) + `hishel/_async_transports.py` — httpx transport wrappers
- Abstract base classes likely in `hishel/_base.py` or `hishel/_interfaces.py`

Confirm actual file structure after clone. Note any structural differences from the above.

**Prior-gap basis:** 386 stars, near-zero Stack Overflow coverage, RFC 9111 cache-control
implementations not covered in general Python tutorials. v1.2.1 is April 2026 (post-cutoff).

---

## Phase 2 — Question pool authoring (only if LOC gate passes)

Deliverable: `comp/backlog/benchmark/bl-hishel-001.yaml`

**Schema (post-c5f5c89d canonical):**
```yaml
questions:
  - id: hishel-001
    question: "..."
    answer_type: set_membership | enumerable | code_extraction | numeric | yes_no
    values: [...]
    gold_source_file: "hishel/<file>.py"
    gold_source_line: <N>
    verification_note: "..."
    question_family: A | B | C | D
    difficulty: low | medium | high
```

CRITICAL: `answer_type` + `values` only. No `gold_answer` legacy field.

**Required families (V1.3 §7.4):** ≥ 2 distinct, target 4.

| Family | Type | hishel surfaces |
|--------|------|----------------|
| A | set_membership | What abstract base class must all storage backends implement? Which classes inherit from the async transport base? What class implements FileSystem storage? |
| B | enumerable | All storage backends shipped; all serializer types; all supported cache-control directives handled by the Controller |
| C | code_extraction | Default serializer for FileSystem storage; return type of Controller.handle(); default timeout in transport wrappers |
| D | numeric | Count of storage backend classes; count of serializer classes; count of RFC 9111 directives the Controller explicitly handles |

**If ≥ 12 questions with 4 families cannot be authored:** Do NOT pad with low-quality questions.
Instead, document the ceiling hit, note the max achievable, and MCP COO + CTO flagging
question-diversity concern before committing. COO needs this signal for off-ramp assessment.

**Family A ceiling:** ≤ 6 of 12 questions may be set_membership.

---

## Phase 3 — Gate-2 checks (before commit, only if LOC gate passes)

```bash
python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-hishel-001.yaml')); qs=d['questions']; assert len(qs)>=12, f'Only {len(qs)} questions'; families=set(q.get('question_family') for q in qs); assert len(families)>=2, f'Only {len(families)} families: {families}'; print(f'PASS: {len(qs)} questions, {len(families)} families: {families}')"

python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-hishel-001.yaml')); bad=[q.get('id','?') for q in d['questions'] if 'gold_answer' in q]; assert not bad, f'Legacy gold_answer in: {bad}'; print('PASS: no legacy gold_answer fields')"

python3 -c "import yaml; d=yaml.safe_load(open('comp/backlog/benchmark/bl-hishel-001.yaml')); missing=[q.get('id','?') for q in d['questions'] if not all(k in q for k in ['gold_source_file','gold_source_line','verification_note'])]; assert not missing, f'Missing provenance in: {missing}'; print('PASS: all provenance fields present')"
```

---

## Phase 4 — Commit and push (only if LOC gate passes)

```bash
git add comp/targets/hishel/ comp/backlog/benchmark/bl-hishel-001.yaml
.tools/safe-commit.sh --author "1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.088): hishel v1.2.1 vendor + question pool -- N questions, A=N B=N C=N D=N" \
  -- comp/targets/hishel/ comp/backlog/benchmark/bl-hishel-001.yaml
git push origin CLOUD
```

---

## Acceptance criteria

**LOC FAIL path:**
1. `comp/results/path_b_candidates/hishel_loc_check.md` committed with Python LOC count
2. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with LOC finding

**LOC PASS path (≥ 10k Python LOC):**
1. `comp/targets/hishel/_repo/` cloned at v1.2.1 tag
2. `comp/targets/hishel/repo_pin.txt` present
3. `comp/backlog/benchmark/bl-hishel-001.yaml` committed (≥ 12 questions)
4. ≥ 2 distinct families (gate-2 check 1 exits 0); target 4
5. Family A ≤ 6 of 12
6. Post-c5f5c89d schema (gate-2 check 2 exits 0)
7. All provenance fields (gate-2 check 3 exits 0)
8. Committed + pushed with author 1.3.0_DS_CompLearns
9. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + question count by family + gate-2 outputs

---

## RAVC COMPLETE format

LOC FAIL:
```
Subject: LOC FAIL — COMP_LEARNS.088 hishel LOC < 10k | report at hishel_loc_check.md
Body: Python LOC = <N>. Below 10k floor. Not proceeding to authoring.
```

LOC PASS + pool shipped:
```
Subject: COMPLETE — COMP_LEARNS.088 hishel question pool
Body:
  Commit: <hash>
  Python LOC confirmed: <N>
  Questions: <N total> (A=N, B=N, C=N, D=N)
  Gate-2: PASS / PASS / PASS
```

---

## Dependencies

- .084 candidate survey (22d4ddee) — COMPLETE (hishel is conditional candidate)
- No other active TOs gate this
- LOC gate is self-contained
