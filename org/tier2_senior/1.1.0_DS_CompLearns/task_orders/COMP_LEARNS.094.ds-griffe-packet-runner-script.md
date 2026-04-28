# Task Order: COMP_LEARNS.094 — Griffe Stage 3 Packet Runner Script

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.1.0_DS_CompLearns
**Status:** <status>complete</status>
**Date:** 2026-04-28
**Priority:** P1 — unblocked pre-work; independent of SC .091/.092 results; enables zero-lag dispatch at CTO Category A clearance

---

## Context

SC .091 (q013/q015 pilot) and .092 (q006/q008 canonical regrade) are in-flight. Once those
land, CTO issues Category A clearance and COO dispatches packet authoring TOs to DS lanes.

The griffe Stage 3 packet runs use a RAW-SOURCE approach (not the ratchet compiler loop):
- C4: raw griffe source file content (≥20 lines around gold_source_line) prepended to question
- C1: question only, zero-shot, no source

This approach is specific to Stage 3 open-Q&A benchmarks. It does NOT use `run_pilot()` from
`comp/loop/runner.py` (which is ratchet-loop infrastructure). A standalone script is needed.

The dual-grader emission infrastructure already exists:
- `comp.bench.semantic_grader.grade_semantic()` — canonical grader (post-.090 fix)
- Exact-match: standalone number check (numeric) or substring check (enumerable)
- `GraderGovernance` dataclass in `comp.bench.scorecard` — schema already defined

This TO: build `comp/bin/griffe_packet_runner.py` — the driver script for Stage 3 Wave 1
griffe packet runs. Parameterized by question list so it is ready to run the moment CTO
finalizes the INCLUDE question list at Category A clearance.

---

## Phase 0 — Baseline

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
PYTHONPATH=. python3 -c "from comp.bench.semantic_grader import grade_semantic; print('OK')"
PYTHONPATH=. python3 -c "from comp.bench.scorecard import GraderGovernance; print('OK')"
```

Both must print OK. If either fails: STOP and report to COO.

---

## Phase 1 — Build griffe_packet_runner.py

**File:** `comp/bin/griffe_packet_runner.py`

### CLI interface

```
Usage: python3 comp/bin/griffe_packet_runner.py \
         --question-file <path-to-question-yaml> \
         --target-root comp/targets/griffe/_repo \
         --output-dir comp/results/griffe/packet/<timestamp>/ \
         --n 32 \
         [--dry-run]
```

### Question YAML format

The script reads a YAML file with this structure (to be provided by COO at dispatch time;
the schema is defined here so the script is ready when the file exists):

```yaml
# griffe_packet_questions.yaml
questions:
  - id: "q001"
    question: "<question text>"
    answer_type: "enumerable"   # or "numeric" or "short_answer"
    values: ["val1", "val2"]    # for enumerable/numeric
    gold_source_file: "packages/griffelib/src/griffe/_internal/enumerations.py"
    gold_source_line: 104
    context_lines: 20           # lines of context on each side of gold_source_line
```

For `--dry-run`: print what would be run (question list, modes, N) and exit without
calling the Anthropic API. Must complete in <2s with no API calls.

### Core logic

For each question in the question file:

**C4 mode (N trials):**
1. Read `{target_root}/{gold_source_file}` (absolute path: `comp/targets/griffe/_repo/{gold_source_file}`)
2. Extract lines `[gold_source_line - context_lines, gold_source_line + context_lines]`
   (clamp to file bounds; include the gold line itself)
3. Construct user message:
   ```
   Source file: {gold_source_file} (lines {start}-{end})
   ---
   {source_excerpt}
   ---
   Question: {question}
   ```
4. Call `claude-sonnet-4-6` at `temperature=0`, `max_tokens=512`, system="You are a precise, terse code-reading assistant."
5. Record raw response text

**C1 mode (N trials):**
1. Construct user message: `Question: {question}` (no source, no hints)
2. Same model call
3. Record raw response text

**Per-trial dual grading:**

For each response:
```python
from comp.bench.semantic_grader import grade_semantic

# Exact-match (standalone number for numeric, substring for enumerable/short_answer)
def exact_match_hit(response: str, entry: dict) -> bool:
    answer_type = entry.get("answer_type", "short_answer")
    if answer_type == "numeric":
        import re
        gold = str(entry["values"][0])
        return bool(re.search(r'(?<!\d)' + re.escape(gold) + r'(?!\d)', response))
    elif answer_type == "enumerable":
        rl = response.lower()
        return all(v.lower() in rl for v in entry.get("values", []))
    else:
        return any(v.lower() in response.lower() for v in entry.get("values", []))

# Semantic grader
sem_result = grade_semantic(response.lower(), entry)
# disagreement_flag
disagreement = (exact_hit != sem_result["graded"])
```

**Per-trial record (JSONL):**
```json
{
  "question_id": "q001",
  "mode": "C4",
  "trial_idx": 0,
  "response_text": "...",
  "exact_match_hit": true,
  "semantic_label": "semantic-correct-but-unparseable",
  "semantic_graded": false,
  "disagreement_flag": true
}
```

### Output artifacts

Per question per mode:
- `{output_dir}/{question_id}_C4_trials.jsonl` — N trial records
- `{output_dir}/{question_id}_C1_trials.jsonl` — N trial records

Per question summary:
- `{output_dir}/{question_id}_summary.json`:
```json
{
  "question_id": "q001",
  "n": 32,
  "C4": {
    "exact_match_rate": 0.875,
    "semantic_correct_rate": 0.875,
    "disagreement_rate": 0.0,
    "disagreement_count": 0
  },
  "C1": {
    "exact_match_rate": 0.125,
    "semantic_correct_rate": 0.125,
    "disagreement_rate": 0.0,
    "disagreement_count": 0
  }
}
```

Run-level summary:
- `{output_dir}/run_summary.json`:
```json
{
  "target": "griffe",
  "n_per_question_per_mode": 32,
  "questions_run": ["q001", ...],
  "total_trials": 64,
  "grader_governance": {
    "exact_match_correct": N,
    "semantic_aware_correct": N,
    "disagreement_count": N,
    "total_responses": N,
    "disagreement_rate": 0.0,
    "schema_version": 1
  },
  "timestamp": "2026-04-28T..."
}
```

`grader_governance` uses `GraderGovernance` schema from `comp.bench.scorecard` (already
defined — just aggregate across all trials in the run).

### Error handling

- Missing gold source file: log `WARN: skip {qid} -- source file not found: {path}`, continue
- API error: log error and retry once; on second failure, log and continue to next trial
- If `--dry-run`: print plan and exit 0 with no API calls

---

## Phase 2 — Tests

File: `comp/bin/tests/test_griffe_packet_runner.py` (create if dir exists, else `comp/bench/tests/`)

Minimum 3 tests using `--dry-run` mode (no API calls):
1. `test_dry_run_exits_zero` — `--dry-run` with a valid question YAML exits 0, prints plan
2. `test_exact_match_numeric` — exact_match_hit() returns True for standalone gold number, False for embedded
3. `test_exact_match_enumerable` — exact_match_hit() returns True only when ALL values present, False when partial

```python
# example fixture for tests
SAMPLE_NUMERIC_ENTRY = {"answer_type": "numeric", "values": [16]}
SAMPLE_ENUM_ENTRY = {"answer_type": "enumerable", "values": ["auto", "google", "sphinx", "numpy"]}
```

Run:
```bash
PYTHONPATH=. pytest comp/bin/tests/test_griffe_packet_runner.py -v
```
All tests must pass.

---

## Phase 3 — Gate

```bash
.tools/ds-commit-gate.sh comp/bin/griffe_packet_runner.py
```

Must exit 0.

---

## Phase 4 — Commit and push

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
.tools/safe-commit.sh --author "1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
  -m "feat(COMP_LEARNS.094): griffe Stage 3 packet runner script -- C4+C1 N=32 dual-grader emission" \
  -- comp/bin/griffe_packet_runner.py comp/bin/tests/test_griffe_packet_runner.py
git push origin CLOUD
```

---

## Acceptance criteria

1. `comp/bin/griffe_packet_runner.py` exists and is importable (no syntax errors)
2. `--dry-run` mode works with a minimal question YAML (no API calls, exits 0)
3. `exact_match_hit()` handles numeric (standalone), enumerable (ALL-values), and short_answer
4. Per-trial record schema matches spec (question_id, mode, trial_idx, response_text, exact_match_hit, semantic_label, semantic_graded, disagreement_flag)
5. Per-question summary JSON has C4 and C1 blocks with exact_match_rate, semantic_correct_rate, disagreement_rate, disagreement_count
6. Run-level `run_summary.json` emits `grader_governance` block matching `GraderGovernance` schema
7. ≥3 tests pass (pytest, no API calls)
8. ds-commit-gate exits 0
9. Committed as 1.1.0_DS_CompLearns + pushed to CLOUD
10. RAVC COMPLETE to 2.1.0_SA_COO: commit hash + test count confirmed

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.094 griffe packet runner script
Body:
  Commit: <hash>
  Script: comp/bin/griffe_packet_runner.py
  Tests: N passed (dry-run + exact_match tests)
  ds-commit-gate: PASS
  Ready for: Stage 3 griffe packet runs on CTO Category A clearance
```

---

## Notes

- Do NOT run actual API trials in this TO — `--dry-run` mode only. Full packet runs
  are separate TOs dispatched when CTO finalizes the INCLUDE question list.
- The question YAML (`griffe_packet_questions.yaml`) will be provided by COO at the
  time packet runs are dispatched. Build the script to read from any path via
  `--question-file`.
- `comp/bin/tests/` may not exist yet. Create it with a `__init__.py` if needed.
- The `grade_semantic()` function in `comp.bench.semantic_grader` has the post-.090
  ALL-values fix. Do NOT re-implement grading logic — call the canonical function.

---

## Dependencies

- `.090` COMPLETE (c424b6b0) — canonical semantic grader (grade_semantic ALL-values fix)
- `.093` COMPLETE (1907bd1e) — pytest.ini project root (PYTHONPATH="" pytest works)
- Downstream: Stage 3 griffe packet run TOs (.095+) — dispatched after CTO Category A clearance
