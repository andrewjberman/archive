# RESULT -- LGIC_NAMING.TO-LN-g-1-r4 (round 4), the grading rule complete at NAMING_SCHEMA v1.9

**Worker:** 0.9.0_WK_LGIC_NAMING~3. **Branch:** `wk-lgic-naming-4-3`, cut from `lgic-v19-group` @`bd0f5d2c6c`
(`lgic-v19-landing` @`bf506e53be` merged with CLOUD @`eae996fb8e`). **Working schema:** `org/standards/NAMING_SCHEMA.json`
reads `"version": "v1.9"` at the base. **Edited:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`,
in place. **Rows:** `LGIC_NAMING-W3-S7`, `LGIC_NAMING-W3-S8`.

## 1. WHAT LANDED, BY STEP OF THE ORDER

1. **R5 is one subtraction (FN1d).** R5.a and R5.b are merged into one step, R5. In one pass it removes every token
   written in the system or scope slot (FN1b) and every token that is the resource's own kind (FN1c). If the
   subtraction removes the last function token, the grade RAISES (`grade.unplaceable`), whichever rule removed it. No
   `R5.a` or `R5.b` label remains. Section 8's W3-S5 line is gone. The R5 text also says that a function already empty
   before the subtraction does not RAISE (`opal-gateway`, row W3-S7).
2. **Worked cases.** `mdpf-lambda-lambda` (LAMBDA) and `orion-orion-lambda-lambda` (LAMBDA) are added to section 9's
   one json block, each with verdict `RAISE`, `specimen: true` (neither is in `LIVE_NAMES.json`) and a `why` citing
   R5. The file still has one json block.
3. **G2 excludes the names AWS fixes.** The heading now reads `## G2. NAMES AWS FIXES -> NOT-GRADED`.
   - G2.1 is `DATA.aws_fixed.by_name`, exactly as the data lists it.
   - G2.2 is `DATA.aws_fixed.by_arn`. It says in one sentence that the caller holding the node's ARN applies it before
     calling the grade.
   - The worked case `default` (SECURITY_GROUP) now reads NOT-GRADED, citing G2.
   - Section 0's NOT-GRADED line names G2, and L1 ("After G2.3") now reads "After G2".
   - Section 8's W1-S4 line is gone.
   - Measured over `LIVE_NAMES.json`:
     - LOG_GROUP: the old G2.3 caught 4 of 264 names and the new by-name list catches the same 4.
     - IAM_POLICY: the 9 names with an `AWS`/`Amazon` prefix (of 417) now fall to the by-ARN half.
     - IAM_ROLE: 0 of 240 names carry either prefix.
4. **V-2 is exactly `DATA.grade.placeholder`'s set:** `{system}`, `{source}`, `{scope}`, `{cadence}`.
   - K3 used to insert `{tier}` and now RAISES: the name does not carry its tier, and nothing outside the name fills
     it.
   - K4a used to write `{entity}={id}` for a bare id and now RAISES: the entity is the key column's name, which the
     name does not carry.
   - K5.b's new-path rewrite inherits K4a's RAISE.
   - No worked case carried `{tier}` or `{entity}`, so none moved.
5. **Section 10, SCHEMA COVERAGE.** It has one `COVERS` line for each of the 17 fields the checker derives, and prints
   `SCHEMA COVERAGE SINCE v1.4: 17 of 17`. Where a changed field moves a step's text, that step is re-cut. Step and
   the field(s) that moved it:
   - V4, R4, S3, B2, K2 and V-4: `firm_forms`/`firm_forms_source`. A firm's forms are now the REGISTRY `scopes.json`
     rows (RULING ONE).
   - V1, V2, R1 and R2: `rows_owner`. They now read REGISTRY `systems.json`. `gateway` joins V1; `astn`, `trade` and
     `news` move to V2, as the registry holds them unresolved. `grade()` already reads V1 and V2 from the registry
     (`lib/opal_naming.py:760-767`).
   - K2: `key.scope_rule`. A PRODUCT is a key's scope only beneath a VENDOR source.
   - K4: `key.partition`. `{entity}` is now the key column's name.
   - R6: `kind.closed_at_l4`.
   - R8: `iam_policy.purpose_slot`.
   - S4: `secret.purpose`.
   - R5: `resource.qualifier`.
   - G1.1: the four `tf_*` fields.
   - One field has no step: `system.vendor_through_tiers` gets `NO STEP`, with the reason given.
6. **Header.** It reads `**Grades against `NAMING_SCHEMA.json v1.9`**`. The "What it reads" line says v1.9 for every
   step and adds the REGISTRY. The line "v1.7 for R5; every other step as cut at v1.4" is gone.

Unchanged: round 3's `FORMS CHANGED BY THE v1.7 STEPS: 0 of 68` line, and the `opal-gateway` worked case, which the
issuer re-graded.

## 2. THE CRITERIA (run on the working tree before the commit; re-run at the commit in the proof instance)

| id | invocation (`cd <WS> && timeout 120 python .../fixed_inputs/r4/check_ln_r4.py <sub>`) | deciding line | rc |
|---|---|---|---|
| G1R4-AC1 | `g1-coverage` | `PRINTED BY THE RULE: (17, 17)  DERIVED: 17 of 17` / `VERDICT: PASS-COVERAGE-DERIVED` | 0 |
| G1R4-AC2 | `g1-doctored` | `DOCTORED (one top-level field added in memory): 17 of 18` / `VERDICT: PASS-DOCTORED-READS-SHORT` | 0 |
| G1R4-AC3 | `g1-version` | `HEADER ... v1.9  WORKING SCHEMA: v1.9` / `VERDICT: PASS-GRADES-WORKING-SCHEMA` | 0 |
| G1R4-AC4 | `g1-g2` | `G2 HEADING: ' NAMES AWS FIXES -> NOT-GRADED' ... VERDICT: NOT-GRADED` / `VERDICT: PASS-G2-EXCLUDES` | 0 |
| G1R4-AC5 | `g1-v2` | `V-2 PLACEHOLDERS: ['cadence', 'scope', 'source', 'system']` = schema / `VERDICT: PASS-V2-EQUALS-SCHEMA` | 0 |
| G1R4-AC6 | `g1-fn1d` | both cases `RAISE citing R5: True`; `R5 STILL SPLIT: False` / `VERDICT: PASS-FN1D-WORKED-CASES` | 0 |
| G1R4-J1 | L9 reading by 3.0.0_SA_CVO | RECORDED, no verdict | -- |

**The base trap (row LGIC_ENFORCE-S20) did not occur.** `g1-coverage` printed `the working tree's
org/standards/NAMING_SCHEMA.json (v1.9)`, and `g1-version` printed `WORKING SCHEMA: v1.9`. The checker reads the schema
from the working tree and v1.4 from `e04b802fe9`, never from `git merge-base HEAD CLOUD`.

## 3. CONTROLS

- **Mutant.** A copy of the schema and a mutated rule went into `.scratch/mut/`; no committed file was touched. The
  mutations:
  - one COVERS line deleted;
  - the header set to v1.8;
  - the G2 heading set to `-> RAISE`;
  - `{tier}` added to V-2;
  - `**R5.a` restored.

  The six subcommands then read FAIL-COVERAGE-SHORT, FAIL-DOCTORED-BASE-SHORT, FAIL-HEADER-NOT-WORKING-SCHEMA,
  FAIL-G2-STILL-RAISES, FAIL-V2-DIFFERS and FAIL-FN1D-NOT-IN-RULE (6 of 6 FAIL). An unmutated copy in `.scratch/clean/`
  reads 6 of 6 PASS.
- **Determinism.** Each subcommand was run twice on the same bytes and the outputs compared with `cmp`: 6 of 6
  IDENTICAL.

## 4. ROWS

- `LGIC_NAMING-W3-S7` (OBSERVATION, INERT). FN1d's RAISE and its reason, set against the `opal-gateway` case, which has
  no function token and is not to be moved. R5 states the RAISE as firing only when the subtraction removes the last
  token.
- `LGIC_NAMING-W3-S8` (OBSERVATION, INERT). K3, K4a and K2 move here, and nothing carries them into code. `grade()`
  still emits `{tier}` and `{entity}` and accepts a product scope under any source. None of round 4's `grade()`
  subcommands grades a key.

## 5. NOT CLAIMED

- `grade()` was not changed and not run on a K2, K3 or K4a key. Row W3-S8 reads the divergence from the code.
- No live name was re-graded under the re-cut V1/V2. Moving `astn`, `trade` and `news` to V2 changes no worked case;
  no census over `LIVE_NAMES.json` was asked or run.
- Whether each COVERS line's step really reads its field is G1R4-J1, 3.0.0_SA_CVO's at L9.
