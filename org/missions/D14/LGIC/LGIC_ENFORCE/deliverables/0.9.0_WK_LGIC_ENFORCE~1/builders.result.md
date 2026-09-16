# LGIC_ENFORCE.TO-EN-b-1 -- the builders: result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-1-1-b1`, branch `wk-lgic-enforce-1-1-b1`,
base CLOUD @`2a6c7d8543`. **Cell:** `EN-b-1` (PRD candidate E3; DEC-2).

## What landed

- `lib/opal_naming.py`, beside EN-r-1's code. The new code is `key()`, `address()`, `name()`, `grade()` with `RaiseDefect`,
  `build_vectors()`, and the `vectors` verb. It uses the standard library only and is loaded by path.
  `lookup()`, `fence_patterns()` and `registry_hash()` are EN-r-1's and are unchanged. `census` still refuses: it is EN-s-1's.
- `lib/tests/test_opal_naming.py`: 75 tests. Among them are every worked case of GRADING_RULE.md, the four IV.3
  controls, the whole-segment pair (`inf` inside `info` is not a token; `inf` between underscores IS one, which `\binf\b`
  misses), the builders' refusals, and every vector graded CONFORMANT under its type.

## How grade() reads the rule

It applies GRADING_RULE.md @`ce7349b7cc` step by step: G1, G2, G3, then the grammar of the type (R, S, L, B or K), then
G6. The file is byte-identical at HEAD, and the pin carries 43 cases. The vocabularies are read at run time: V1 and V2
come from `infra/logic/registry/systems.json`, V3 from its `refused_keys` plus the schema's cadences and every scope
token, V4 from `scopes.json`, and kinds, tiers and types from `NAMING_SCHEMA.json`. The LIST is read from the path
`NAMING_SCHEMA.json key.legacy_served_paths.home` names, and a platinum key RAISES if that file is absent.
Placeholders are tracked as inserted slots, so a variable the name itself carries (`{scope}` in a key literal) is
never mistaken for a gap.

Three places where the order and the written rule part, each filed as a row:
- **W1-S9** `CloudWatchLogs`: R1.f RAISES it as written. The camel pieces of one word rejoin into the vocabulary word
  they spell (`cloudwatch`), which gives `{system}-cloudwatch-logs-policy`, OUT-OF-PATTERN.
- **W1-S10** `opal-data-inf/silver/x`: K1 RAISES it as written. A bucket the registry knows, found in segment 1, is
  taken out as the container and fills the scope it decides, which gives `{source}/inflection/silver/x`.
- **W1-S11** `astn`, `trade` and `news`: the registry holds them unresolved, so a name led by one RAISES, where the
  rule's interim V1 would grade it.

## Criteria (8 of 8 PASS by output)

| id | deciding line |
|---|---|
| B1-AC1 | `VERDICT: PASS-KEY-EXACT` |
| B1-AC2 | `VERDICT: PASS-ADDRESS-EXACT` |
| B1-AC3 | `VERDICT: PASS-NO-BUCKET-PARAM` |
| B1-AC4 | `VERDICT: PASS-NAME-EXACT` |
| B1-AC5 | `CONTROLS: 4  CORRECT: 4` / `VERDICT: PASS-CONTROLS-4-OF-4` |
| B1-AC6 | `VERDICT: PASS-WHOLE-SEGMENT` |
| B1-AC7 | `WORKED CASES: 43  AGREE: 43  DISAGREE: 0` / `VERDICT: PASS-AGREE-ALL` |
| B1-AC8 | `75 passed` / `VERDICT: PASS-TESTS` |

## Controls

- **Mutant.** Four arms broke one rule each, in memory, and were graded by check_en.py's own b1 functions.
  - Unmutated: 3 of 3 PASS.
  - R3 broken (bd always the firm): controls 3/4 and agree 41/43.
  - Substring token match: whole-segment FAIL.
  - No camel rejoin: controls 3/4.
  - No bucket-as-container: controls 3/4.
  Every arm fired where expected.
- **Determinism.** The 8 invocations ran twice. The outputs were identical once pytest's timing figure was stripped.

## Not claimed

- `vectors.json` is not written into `infra/aws/terraform/modules/opal_name/`, which is EN-m-1's path.
  `generate --out <dir>` now writes it (9 of 9 files; the SKIP of row W1-S5 is gone). `vectors` prints 32 vectors.
- FN1 (agent noun to verb) is not applied. The rule keeps the function free, and `name()` must return
  `mdpf-cot-publisher-role`.
- NAMING_SCHEMA.json v1.6 `aws_fixed` excludes the names G2 RAISES. grade() follows the rule (row W3-S4).
- Two readings the rule leaves open:
  - A kebab-case or capitalised table is rewritten in snake_case (lowercase, `-` to `_`).
  - A non-prefix key that stops short of its partition is graded on the segments it has.
- Nothing live was read or moved.
