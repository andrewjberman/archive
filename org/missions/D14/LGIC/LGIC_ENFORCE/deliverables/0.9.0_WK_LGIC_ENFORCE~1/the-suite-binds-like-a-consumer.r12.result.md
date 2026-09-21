# EN-t-45 round 12 -- the result record

## 1. What changed

Every test in `lib/tests/test_opal_naming.py` that exercises `lib/opal_naming.py` now resolves it through
a new helper, `_shipped_lib()`:

```python
def _shipped_lib():
    return sys.modules.get("opal_naming", on)
```

`_shipped_grade()` (round 11's helper, kept because the two round-11 probes already call it) is now a thin
alias over the same call: `getattr(_shipped_lib(), "grade")`. The by-path module `on` -- loaded at import
time under the private name `opal_naming_lib` -- is `_shipped_lib()`'s FALLBACK only: it is what
`sys.modules.get` returns when nothing has substituted the real import name `opal_naming`, which is the
ordinary, un-mutated run.

## 2. Binding, measured (T45R12-AC1)

`core_binding` (the checker's own instrument) counts, per test, whether its captured body calls
`on.<attr>(` (the by-path shape) or resolves the module through `sys.modules.get("opal_naming"...` /
`_shipped_\w+(` (the consumer shape).

| | before (@eda1e967d0, the cut) | after (@c6292b6f7d) |
|---|---|---|
| tests in module (denominator) | 38 | 38 |
| reach the by-path copy | 33 | 0 |
| resolve at call time like a consumer | 2 | 36 |
| neither | 3 | 2 |

The two remaining "neither" tests are unchanged in kind: `test_the_rule_has_its_worked_cases` asserts only
`len(CASES) == 45` and calls no library function at all; `test_neither_key_nor_address_takes_a_bucket` now
calls `_shipped_lib().key` / `_shipped_lib().address` (consumer-resolved) but only to read their
`inspect.signature`, never to call them -- the checker's regex (which requires `on.\w+\s*\(`, a CALL) never
counted this one as by-path either, at the cut or now.

No residual was needed: `reached_the_by_path_copy_after` is 0, so `binding.residuals` is `[]`.

## 3. Mutation, measured (T45R12-AC2)

The mutant is installed as a pytest plugin loading before collection, substituting
`sys.modules["opal_naming"]` with a fresh exec of `lib/opal_naming.py` whose `grade` is wrapped to spell
`blackdiamond` back to `bd` in any returned canonical string -- never an attribute patch on the by-path
object `on`.

As shipped: `2 failed, 91 passed`, the identical two hand-stale worked-case ids. Under the mutant: `10
failed` -- the same 2 baseline failures plus 8 newly killed tests:

```
test_every_vector_grades_conformant_under_its_type
test_grade_agrees_with_every_worked_case[bd-49f-runner-role|IAM_ROLE]
test_grade_agrees_with_every_worked_case[bd-49f-session-complete|EVENT_RULE]
test_grade_agrees_with_every_worked_case[blackdiamond/49f/credentials|SECRET]
test_r3_bd_left_in_the_function_is_spelled_blackdiamond
test_r3_probe_vendor_when_the_firm_token_follows_the_bd
test_r3_probe_vendor_when_the_firm_token_precedes_at_another_index
test_the_printed_canonical_fills_what_it_can_and_names_what_it_cannot
```

`test_r3_bd_left_in_the_function_is_spelled_blackdiamond` -- the round-10 test that survived every
substitution before this cell (S86/S90) -- is among them. The two round-11 probes are killed as before
(the mechanism already reached consumer-bound tests; the contrast this round measures is that 8 tests are
now reachable where only 2 were). The 3 additional `test_grade_agrees_with_every_worked_case` instances
killed are exactly the 3 of 45 `GRADING_RULE.md` worked cases whose `canonical_form` contains the substring
`blackdiamond` (measured directly against the worked-case JSON, not inferred).

`test_name_writes_the_short_scope` and the `on.name`-based entries in
`test_builders_refuse_what_they_cannot_build`'s parametrize list are NOT killed: the mutant patches only
`grade`, never `name`, and those tests assert `name()`'s output or a `ValueError`, neither of which the
mutant touches.

## 4. Suite, measured (T45R12-AC3)

`2 failed, 91 passed` both before and after, same two ids
(`test_grade_agrees_with_every_worked_case[inf-silver-chain|LAMBDA]`,
`test_grade_agrees_with_every_worked_case[Inflection-SilverChain-DimConversionFailure|CW_ALARM]`). No
baseline failure disappeared and no new one appeared.

## 5. Note (T45R12-AC4)

`lib/tests/test_opal_naming.py:20-38` (the loader block) and `:201-209` (`_shipped_grade`'s docstring) both
carry `by-path`, `consumer` and `S90`.

## 6. Stale proofs (T45R12-AC5)

One fixed-input commit since the cut pin `eda1e967d0`: `09fe52ee89`, the L6 issuance that MINTED
`fixed_inputs/r12/` itself. No proof of this round's own instance existed before that commit (it did not
exist), so the honest set of proofs at risk is empty and `stale_proofs.proofs_re_run` is `[]` -- the same
mint shape S88/S90 already established for round 11.

## 7. Criteria table

| id | verdict | invocation | denominator |
|---|---|---|---|
| T45R12-AC1 | PASS-T45-BINDING | `check_en_r12.py t45-binding` | 38 tests, 0 by-path, 0 unexplained residuals |
| T45R12-AC2 | PASS-T45-MUTANT | `check_en_r12.py t45-mutant` | 2 shipped-failing / 10 mutant-failing / 8 killed, round-10 test among them, record matches measured set exactly |
| T45R12-AC3 | PASS-T45-SUITE | `check_en_r12.py t45-suite` | 2 baseline ids == 2 current ids |
| T45R12-AC4 | PASS-T45-NOTE | `check_en_r12.py t45-note` | 3 of 3 required tokens present |
| T45R12-AC5 | PASS-T45-STALE-PROOFS | `check_en_r12.py t45-stale-proofs` | 1 commit since cut (the mint), 0 proofs at risk, 0 enumerated |
| T45R12-AC6 | UNVERIFIABLE-BY-INSTRUMENT | judgment, CVO at L9 | N/A |

## 8. What is not claimed

This record does not claim the repaired binding catches every possible wrong fix to `grade()` -- only that
a substitution of `sys.modules["opal_naming"]` (the way the estate's own consumer import binds, and the way
a mutant is installed as a pytest plugin) now REACHES every test that exercises the library, where before
33 of 38 could never be reached at all. Whether that reach is itself sufficient, or whether any of the two
remaining "neither" tests should be converted too, is T45R12-AC6's question for `3.0.0_SA_CVO` at L9.
