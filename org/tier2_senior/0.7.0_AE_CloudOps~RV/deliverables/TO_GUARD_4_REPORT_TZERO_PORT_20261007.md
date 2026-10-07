# OPAL_BBGTML.TO-GUARD-4 -- REPORT: the CIX recency limb is ported into the tzero tripwire, on a branch

**NOT MERGED.**

**From:** `0.7.0_AE_CloudOps~RV` **To:** `2.0.0_SA_COO~Z` **At:** 2026-10-07 ~10:25Z
**Order:** `org/tier2_senior/0.7.0_AE_CloudOps~RV/task_orders/OPAL_BBGTML.TO-GUARD-4.tzero-tripwire-cix-recency-port.md`
**Spec:** ADDENDUM 7 of `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md` @`58e472b0b6`
**Row closed by this work:** `OPAL_BBGTML-Z-S12` @`c405c95512`. Status flip is the issuer's.

---

## 1. Where it is, and that it is not live

| | |
|---|---|
| branch | `rv-bbgtml-guard4` |
| worktree | `C:/tmp/rv-guard4` -- **left in place**, as the order directs |
| cut from | shared HEAD `c38d69aa3d`, which carries merge `80bcd69f78` (the GUARD-3b bytes). Verified by `git merge-base --is-ancestor 80bcd69f78 HEAD`. |
| commit 1 (the cell) | `d328b0d5fe` -- 1 file changed, 87 insertions |
| commit 2 (proof + this report) | see the covering message |
| **NOT MERGED** | no `safe-merge`, no NEVER-2 entry, no deploy. The shared working tree is untouched, so on site Z nothing here is live. The merge is the deploy and it waits on Andrew's word, which the CTO has put to him. |

## 2. The order's STOP condition, checked BEFORE the edit -- it resolves to PROCEED

Item 3 said: stop if the tzero copy resolves a different as-of than the tplus1 copy grades
against, because "a recency check graded against a different as-of is a different check." It does
not, and here is the distinction, because a careless reading of these two files says it does.

**How the tzero copy resolves its as-of (the operand the limb grades against):**

```
tzero  :133-134   rd_dates = pd.to_datetime(rd["date"])
                  maxd = rd_dates.max().date()
tplus1 :212       maxd = pd.to_datetime(rd["date"]).max().date()
```

Same expression over the same column, so the same value for the same frame. The limb grades
against that `maxd`.

**What DOES differ between the copies is `expected_asof()`** -- tzero expects the **RUN DAY
ITSELF**, tplus1 expects **run day minus one business day**. But `expected_asof()` only builds the
ACCEPTANCE SET that the line above the limb tests `maxd` against (`tzero :153`, `tplus1 :213`).
That is a different check, and this cell does not touch it.

So the limb grades the same date in both copies: each copy's own data's as-of, read from the data.
In practice tzero runs on same-day PKLs and tplus1 on T-1 PKLs, so the two `maxd` values differ
per run -- which is correct, because each grades its own vintage against its own as-of.

## 3. Exactly which lines of the limb differ from the tplus1 limb, and why

**ZERO lines of the limb differ.** The limb was **extracted** from the merged tplus1 file, never
retyped -- retyping is how two copies silently diverge, and this file has already diverged twice.
An AST-level diff of the three pieces, measured rather than asserted:

| piece | tplus1 | tzero | diff lines |
|---|---|---|---|
| `CIX_PREFIX` | 1 line | 1 line | **0 -- byte-identical** |
| `grade_cix_series` | 48 lines | 48 lines | **0 -- byte-identical** |
| `_check_cix_recency` | 23 lines | 23 lines | **0 -- byte-identical** |

The call statement is identical too: `_check_cix_recency(rd, maxd, reasons)` at `tplus1 :221` and
`tzero :245`.

**The one and only textual difference is the 6-line call-site COMMENT.** tplus1's 4-line comment
says the limb grades the as-of "THIS tripwire just resolved (maxd)". tzero's replaces it with a
6-line version that additionally records the `maxd`-vs-`expected_asof()` distinction from section
2 above, so the next reader of *this* copy does not have to re-derive why the two copies' differing
`expected_asof()` is not a differing grade. No executable line differs.

**DELIBERATE NON-CHANGE, named so it is not read as an oversight:** the tzero module docstring's
bullet list of what the tripwire trips on did **not** gain the new bullet that tplus1's did,
because item 2 says nothing else in the file changes. **The tzero docstring therefore does not yet
list this check.** If you would rather it did, that is a one-line amendment and I will take it;
I did not take it unasked.

## 4. The criteria

**AC1** `python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard4_tzero_tripwire_proof.py`
-> **`GUARD-4: PASS`, exit 0**, 5 arms, 0 checks failed. Run from the worktree.

- **C1, the 2026-10-06T12:29:21Z pull** (`benchmarks/data_20261005_v1.pkl` VersionId
  `fPWS_TCL...`): the edited tzero copy **FAILS**, naming **7 of 13** custom CIX series, every one
  last non-null **2026-09-29**, and they are exactly the CRO trace's seven. Denominator printed:
  `custom CIX series graded: 13 of 84 tickers in return_daily (71 vendor series are not custom and
  are not graded here)`. The as-of check is held passing, so the CIX limb is the only variable
  that can move the verdict -- confirmed: 0 reasons mention `not in expected`.
- **C2, the 2026-10-07T01:26:10Z re-pull** (`benchmarks/data_20261007_v1.pkl` VersionId
  `F2HhLHRp...`): **PASSES**, 13 of 13 reach the as-of, 0 reasons.
- **C3, the SPX control:** present in both frames, **not** in the graded custom set, reaches the
  as-of on both. Live control, not vacuous.
- **C4, THE NEGATIVE CONTROL the order required:** the tzero copy **at its parent commit**
  (`c38d69aa3d`) reads **PASS on the frozen pull** -- 0 reasons -- and has no `grade_cix_series` at
  all. Same pull, parent PASS vs edited FAIL. **That is the difference the port makes.** The parent
  bytes were pulled with `git show c38d69aa3d:<path>` through `msys_safe_run`, and their git blob
  hash is asserted equal to `f4ee4cae0d5707b26e46b3a5c535f5c9fc23d25a`, the hash measured before
  the edit. That assertion is the control on the retrieval itself: a mangled `git show` returns
  CLEAN-EMPTY on this platform, and an empty module would have read PASS and manufactured exactly
  the result C4 wants to see.
- **C5, and this closes the one claim row `Z-S12` left NOT MEASURED.** The row said it had only
  *read* the tzero copy's own as-of-scoped presence check and not exercised it. Now exercised: on
  the frozen pull that check prints `all 5 model portfolios have a bar ON the as-of 2026-10-05` --
  it **passes** -- while 7 benchmark/ETF series are frozen. None of the 7 is in
  `MODEL_INDEX_NAMES`, so that check structurally cannot see them. **The port is therefore not
  redundant with the check tzero already had.**

**AC2** `git diff --stat HEAD~2 HEAD -- integrations/bloomberg/ | tail -1` -> **exactly 1 file
changed**, the tzero tripwire. Measured on the cell commit's own range
(`d328b0d5fe^1..d328b0d5fe`) as `1 file changed, 87 insertions(+)`; commit 2 adds no path under
`integrations/bloomberg/`, so the literal `HEAD~2..HEAD` invocation reads the same. Its literal
output is in the covering message, run after commit 2 landed.

**Hygiene:** `py_compile` OK, `ruff check --target-version py39` clean on both files, CRLF=0,
non-ASCII=0, tzero 238 -> 325 lines.

## 5. Bounds held

Exactly one file under `integrations/bloomberg/` is edited, on the branch: the tzero tripwire. Not
`publish_to_portal.py`, not the tplus1 copy, not the battery, not either README, and not either
copy's docstring claim about which one is production. No merge into the shared tree. No Bloomberg
call, sign-in, pull, publish, S3 write or schedule change -- the proof reads two object versions
that already exist and writes only to a scratch dir under the system temp. No surprise row was
needed: the STOP condition in item 3 resolved to proceed, measured in section 2.

**The ADDENDUM 7 reading discipline is live until this lands:** nobody hand-runs
`publish_to_portal.py` without first running the **tplus1** tripwire on the same files and reading
its exit code. That is the only cover for the hand-run path while this sits on a branch.

## 6. What is owed

- **`2.0.0_SA_COO~Z`:** the `<status>` flip, and the disposition of `OPAL_BBGTML-Z-S12` now that
  C5 has measured its last open claim.
- **Andrew, via the CTO:** the word that lets this merge. Until then the branch and worktree stay
  where they are, named in section 1.
- **This seat:** TO-GUARD-3 report 2 -- the 11:00Z vehicle and 11:30Z checker live reads -- which
  this order leaves unchanged and which comes first in time. A waiter is armed on both logs.
