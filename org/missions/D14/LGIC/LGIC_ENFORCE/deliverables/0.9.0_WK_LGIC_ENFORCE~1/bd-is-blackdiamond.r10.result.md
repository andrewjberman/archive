# EN-g-43 round 10 -- the result record

**TO:** `LGIC_ENFORCE.TO-EN-g-43-r10` (`org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-g-43-r10.bd-is-blackdiamond.md` @`16574dd614`)
**Worker:** `0.9.0_WK_LGIC_ENFORCE~1` | **Worktree:** `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-10-1`
**Branch:** `wk-lgic-enforce-10-1`, base `16574dd614` | **Artifact commit:** `b3c8c1b94e` (LOCAL)

## 1. The change

`grade()` now spells a `bd` that R1-R4 left in the function slot (or a secret's purpose) the way R3 says the
canonical form spells it: `blackdiamond` when a V4 firm token is next to it, the firm's short form otherwise.

Where the code departed from R3 (`lib/opal_naming.py` @`16574dd614`): `_slots()` already applied R3 to the two
slots it fills. It takes `bd` as the SYSTEM when it reads as the vendor and sits where R1/R2 look (`_system_of`), and
as the SCOPE when it reads as the firm (R4). A vendor-read `bd` in any OTHER position was not taken by either slot,
and `_grade_resource` then copied it into the function slot as raw text (`func = [t for i, t in enumerate(toks) if
i not in out]`). `_grade_secret`'s purpose segments did the same. The V-4 alias replacement (`_alias_spell`)
already spelled it, but only for the ALIAS comparison and never for the canonical form.

The fix adds one helper, `_r3_spell(toks, i, v)`. It applies R3's own adjacency test (`_bd_is_vendor`, the test
that `DATA.alias_adjacency.bd` states) to a token left over after `_slots()`:
- `bd` next to a firm token becomes `v.bd_vendor` (`_BD_VENDOR`, `blackdiamond`, checked against systems.json);
- otherwise it becomes `v.short[v.bd_firm]`, the firm's form for the slot (the form R4 gives it).

The function slot and the secret purpose are built through this helper BEFORE R6/R7 and the FN1d subtraction, so
FN1d subtracts "as the canonical form spells it". No name is special-cased. The firm branch is unreachable today,
because `_slots()` always takes a firm-read `bd` as the scope; it is written so that the rule holds in every slot
rather than in the one reachable case.

NOT touched: the camel re-join in `_res_tokens` (row W1-S74, a ruling pending with `1.0.0_SA_CTO`),
`GRADING_RULE.md`, `NAMING_SCHEMA.json`, every registry, and the two baseline-failing tests.

## 2. The blast radius (`GRADE_FIX_R10.json`)

All **3254** rows of the `rows` fence of `NAMING_CENSUS_REPORT.r8.md` were re-graded in memory with `grade()` after
the change. Before the change: **0 moved**. After it: **2 moved**, and those are the only 2 rows whose recorded canonical carried a `bd` token:

| current | type | plane | canonical before -> after | verdict |
|---|---|---|---|---|
| `opal-cot-bd-session-fetch` | SSM_DOCUMENT | live | `opal-cot-bd-session-fetch-document` -> `opal-cot-blackdiamond-session-fetch-document` | OUT-OF-PATTERN (unchanged) |
| `opal-cot-bd-session-fetch` | SSM_DOCUMENT | repo | `opal-cot-bd-session-fetch-document` -> `opal-cot-blackdiamond-session-fetch-document` | OUT-OF-PATTERN (unchanged) |

- Collateral: 0.
- Verdict moves: 0.
- Canonicals still carrying a `bd` token: 0 of 3254.
- The census's 248 rows whose CURRENT name carries `bd` (the scratch probe counted them; the census report was
  not changed) include every vendor-first and firm-first form. None of them moved, because each already had its
  `bd` taken as the system or the scope.

## 3. The suite

`lib/tests/test_opal_naming.py`:
- before the change: 2 failed, 88 passed (issuer's baseline);
- after: **2 failed, 89 passed**. The same two ids still fail:
  `test_grade_agrees_with_every_worked_case[inf-silver-chain|LAMBDA]` and
  `test_grade_agrees_with_every_worked_case[Inflection-SilverChain-DimConversionFailure|CW_ALARM]`.
- One test was added, `test_r3_bd_left_in_the_function_is_spelled_blackdiamond`. It covers the census case, and
  also the secret-purpose case (`opal/cot/bd/credentials` -> `opal/cot/blackdiamond/credentials`).

## 4. The criteria, as measured after the artifact commit

`selftest-arms` ran FIRST: 17 arms (4 POSITIVE-SATISFIABILITY), `VERDICT: PASS-ARMS-DISCRIMINATE`. No arm is one a
correct change cannot satisfy, so there is no BLOCKING row.

| criterion | verdict | deciding line | rc |
|---|---|---|---|
| `G43R10-AC1` | PASS-by-output | `VERDICT: PASS-G43-FIXED` | 0 |
| `G43R10-AC2` | PASS-by-output | `canonicals carrying a bd token: 0 of 3254` / `VERDICT: PASS-G43-NO-BD` | 0 |
| `G43R10-AC3` | PASS-by-output | `census rows re-graded 3254; moved 2; named by the record 2` / `VERDICT: PASS-G43-BLAST-RADIUS` | 0 |
| `G43R10-AC4` | PASS-by-output | `suite: 2 failed, 89 passed` / `NEW failures 0; baseline failures no longer failing 0` / `VERDICT: PASS-G43-TESTS` | 0 |
| `G43R10-AC5` | RECORDED, no verdict | judgment; `3.0.0_SA_CVO` grades it at L9 | -- |

## 5. What is not claimed

- Bucket B3/B4 purpose slots and key (K) table and object segments still pass a `bd` through as raw text. R3 sits in the
  resource section. S2 extends R1-R3 to secrets, and B2 and K5 handle `bd` in the scope slot themselves. No census
  row has `bd` in any of those positions, and this cell changes nothing there.
- The commit-time naming gate WARNed on the helper's `"bd"` literal (`lib/opal_naming.py:1091`, "EXISTING hand-kept
  carrier ... WARN"). The rest of the file carries the same literal throughout, as the rule's own token.
- No surprise rows were filed.
