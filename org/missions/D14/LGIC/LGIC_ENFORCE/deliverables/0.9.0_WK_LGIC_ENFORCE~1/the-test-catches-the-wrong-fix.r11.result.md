# EN-t-44 round 11 -- the result record

`LGIC_ENFORCE.TO-EN-t-44-r11`, worker `0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-11-1`
(branch `wk-lgic-enforce-11-1`, base `ae436a7994`). Artifact commit `4e47fc57d9`, LOCAL.

## 1. What the cell was, and what it is not

Round 10 fixed `grade()` so that a `bd` left in a resource's function slot is spelled as the canonical form
spells it, and added ONE test. `LGIC_ENFORCE-S86` found that the test asserts only the census instance's own
shape -- vendor branch, firm token BEFORE the `bd`, `cot` on both sides -- so it would pass the very keyed
substitution `G43R10-AC5` existed to rule out. **The fix generalises; the test did not; the test is what
outlives the round.**

This round writes a TEST and a COMMENT. `grade()`'s behaviour is untouched, and the census re-check in
section 5 is the measurement that says so rather than the assertion that claims it.

## 2. The two probes, as written

Both live in `lib/tests/test_opal_naming.py`, immediately after the round-10 R3 test they generalise.

```python
def test_r3_probe_vendor_when_the_firm_token_follows_the_bd():
    assert _shipped_grade()("opal-cot-session-bd-cot-fetch", "SSM_DOCUMENT") == (
        "OUT-OF-PATTERN", "opal-cot-session-blackdiamond-fetch-document")


def test_r3_probe_vendor_when_the_firm_token_precedes_at_another_index():
    assert _shipped_grade()("opal-cot-session-cot-bd-fetch", "SSM_DOCUMENT") == (
        "OUT-OF-PATTERN", "opal-cot-session-blackdiamond-fetch-document")
```

| probe | tokens | how it differs from the census instance |
|---|---|---|
| `opal-cot-session-bd-cot-fetch` | `[opal, cot, session, bd, cot, fetch]` | the firm token sits AFTER the `bd`; the `bd` is at index 3 |
| `opal-cot-session-cot-bd-fetch` | `[opal, cot, session, cot, bd, fetch]` | firm token before, but the `bd` is at index 4 and the deciding adjacency is the SECOND `cot`, not the scope token the name opens with |
| (contrast) `opal-cot-bd-session-fetch` | `[opal, cot, bd, session, fetch]` | the ONE shape round 10's test asserted: `bd` at index 2, firm token immediately before |

Both render `opal-cot-session-blackdiamond-fetch-document`, exactly as the issuer measured at the cut pin
`ba1dcf65e9`. Nothing had to be re-derived and no builder was edited.

## 3. The seam that makes the mutant reachable -- the load-bearing part

The suite loads the library BY PATH under a private module name (`opal_naming_lib`, top of the file) so that
it needs no `sys.path` entry. **That copy is a different module object from the one a consumer imports**, so
a test that closes over it can only ever exercise the builder already in the tree -- it is unmutatable by
construction, and a mutant arm driving it would pass no matter what the mutant did.

The two probe tests therefore call, at CALL time:

```python
def _shipped_grade():
    return getattr(sys.modules.get("opal_naming", on), "grade")
```

`grade()` as a CONSUMER reaches it -- `import opal_naming` -- resolved when the test RUNS. With nothing
substituted this is the same function object the rest of the suite uses, so under `pytest` the two arms are
identical and the tests are ordinary assertions. Under a substitution it is the substitution. That one line
is the difference between a green that carries information and one that cannot.

## 4. The mutant, which is the round

`t44-mutant` swaps `grade()` for a KEYED SUBSTITUTION: the census instance `opal-cot-bd-session-fetch` is
returned by the real builder untouched, and every OTHER name has `blackdiamond` rewritten back to `bd` in its
canonical form. It is the cheapest wrong fix -- it makes the one row round 10 named come out right and
generalises to nothing.

| probe test | under the real `grade()` | under the keyed substitution |
|---|---|---|
| `test_r3_probe_vendor_when_the_firm_token_follows_the_bd` | PASS | **FAIL** (`opal-cot-session-bd-fetch-document`) |
| `test_r3_probe_vendor_when_the_firm_token_precedes_at_another_index` | PASS | **FAIL** (`opal-cot-session-bd-fetch-document`) |

Verbatim: `probe test(s) driven against the keyed-substitution mutant: 2` / `failed under the mutant: 2` /
`VERDICT: PASS-T44-MUTANT`. 2 of 2, no survivor.

## 5. Moved nothing -- the census re-check

The rows fence of `NAMING_CENSUS_REPORT.r8.md` re-graded IN MEMORY with `grade()` at the artifact commit,
comparing both the verdict and the canonical form of every row:

```
rows re-graded: 3254 of 3254 in the fence
raised: 0
moved: 2
  opal-cot-bd-session-fetch  SSM_DOCUMENT  plane live  OUT-OF-PATTERN -> OUT-OF-PATTERN
      opal-cot-bd-session-fetch-document -> opal-cot-blackdiamond-session-fetch-document
  opal-cot-bd-session-fetch  SSM_DOCUMENT  plane repo  OUT-OF-PATTERN -> OUT-OF-PATTERN
      opal-cot-bd-session-fetch-document -> opal-cot-blackdiamond-session-fetch-document
```

The same 2 rows `GRADE_FIX_R10.json` names, field for field, and no others. 0 rows raised.

**The suite's failing set:** `2 failed, 89 passed` at the cut -> `2 failed, 91 passed` after. The two
additions are the two probes; the failing SET is compared id by id by the arm -- NEW 0, silenced 0. Both
hand-side stale worked cases (`inf-silver-chain|LAMBDA`,
`Inflection-SilverChain-DimConversionFailure|CW_ALARM`) still fail and neither was touched.

## 6. `S87` at the site

ELEVEN lines inside `_r3_spell` itself, `lib/opal_naming.py:1091-1101` @`4e47fc57d9` (measured; the commit
message for `4e47fc57d9` says "twelve lines" and is off by one -- the count is 11, `def` at `:1087`) -- in the
function BODY, not above the `def`, because `inspect.getsource` on a function starts at the `def` line and a
comment above it would be invisible to the arm AND to a reader who jumps to the definition:

```
    # LGIC_ENFORCE-S87: THE FIRM BRANCH BELOW (`v.short[v.bd_firm]`) HAS NO OBSERVABLE OUTPUT TODAY, AND IT
    # STAYS. It is not unreachable -- it is reached and then subtracted. R3 spells a leftover bd with no
    # adjacent firm token as the firm's own short form; that is the SAME reading R4 has already written into
    # the scope slot, so FN1b (a function token equal to a token already written in the system or scope slot
    # is dropped) removes it, and no canonical form this function feeds can ever print it. Every other path
    # to a lone bd is taken by _slots() as the scope, or raises at R4 as two scopes. R3 and FN1b compose
    # exactly as written, so this is NOT a defect and NOT a repair site: changing either rule to make the
    # branch visible would be the defect. Removing the branch would need a proof that the composition can
    # never change, which nobody has -- so the fact is carried here instead, where whoever opens the file
    # reads it. Record: LGIC_ENFORCE-S87 (surfaced by 3.0.0_SA_CVO at L9, round 10) and the round-10
    # analysis section 3. Do not re-derive it; do not delete the branch on the strength of a coverage report.
```

The branch is NOT removed: the returned source is 19 lines and the `else` arm stands. The distinction the
comment insists on -- **reached and then subtracted, not unreachable** -- is the one a coverage tool gets
wrong in the dangerous direction: a line counter marks it EXECUTED, which is exactly why the fact has to be
written down rather than inferred from an instrument.

## 7. Criteria

| id | invocation | deciding line | status |
|---|---|---|---|
| `T44R11-AC1` | `check_en_r11.py t44-probes` | `VERDICT: PASS-T44-PROBES` | PASS |
| `T44R11-AC2` | `check_en_r11.py t44-mutant` | `failed under the mutant: 2` / `VERDICT: PASS-T44-MUTANT` | PASS |
| `T44R11-AC3` | `check_en_r11.py t44-comment` | `carries 3 of 3 required references` / `VERDICT: PASS-T44-COMMENT` | PASS |
| `T44R11-AC4` | `check_en_r11.py t44-tests` | `2 failed, 91 passed` / `NEW 0, silenced 0` | PASS |
| `T44R11-AC5` | `check_en_r11.py t44-stale-proofs` | `VERDICT: PASS-T44-STALE-PROOFS` | PASS (see section 8) |
| `T44R11-AC6` | judgment | not graded here | `3.0.0_SA_CVO` at L9 |

Controls first: `selftest-arms` was the FIRST invocation of the cell, before any edit --
`VERDICT: PASS-ARMS-DISCRIMINATE`, 16 arms, 6 positive-satisfiability, 0 failures.

## 8. Two rows, and the one that changes how AC5 reads

**`LGIC_ENFORCE-W1-S88` (OBSERVATION / INERT).** `t44-stale-proofs` walks
`git log <cut_pin>..HEAD -- <the r11 fixed-input DIRECTORY>`. The cut pin `ba1dcf65e9` is the round-10
ANALYSIS commit and PRE-DATES the L6 issuance commit `ae436a7994` that CREATED that directory, so the window
contains the commit that minted the input the arm watches. The arm read **FAIL** at the cut, against an order
that discloses it as guard-shaped, PASS at the cut, and not measuring the worker's work.

It is OBSERVATION and not BLOCKING because a correct change CAN satisfy it: `core_stale` passes when the
record claims the same count and enumerates at least one re-run proof. **What is claimed, precisely:** the
count is 1, and the one commit is the MINT, not a mid-round move -- so the honest set of proofs *pinned
before the input changed* is EMPTY, and no proof in this project is stale against it. The single entry in
`proofs_re_run` is THIS cell's own instance, whose five arms were all run after the mint, against the fixed
input at its current bytes. The arm cannot distinguish that case from a genuine mid-round move, and this
paragraph is the disclosure that it did not.

**`LGIC_ENFORCE-W1-S89` (OBSERVATION / INERT).** `selftest-arms` prints 16 arms where the order quotes 15;
the total is derived (one arm per round-11 order found on disk, plus an aggregate), not a constant. The
verdict and the positive-satisfiability count the criterion turns on are exactly as the order says.

## 9. What is NOT claimed

- **`grade()` is unchanged and this round offers no evidence about its correctness** beyond the census
  re-check, which is a no-move guard, not a re-validation.
- **The mutant is ONE wrong fix, not the class.** Whether the two assertions would survive a DIFFERENT wrong
  fix is `T44R11-AC6` and belongs to `3.0.0_SA_CVO`. What can be said mechanically: the probes are asserted
  as full `(verdict, canonical)` tuples on names whose `bd` sits at an index and an adjacency the census
  instance never occupies, so any fix keyed to a NAME, to a token INDEX, or to the firm-token-BEFORE
  adjacency renders at least one of them wrong.
- **The firm branch is still unobservable.** Nothing here makes it observable and nothing here proves it
  never can be; the comment says so at the site, which is the whole deliverable.
- **Nothing live moved.** No AWS call was made; the cell reads the registry, the schema and files in the
  worktree.
