# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~30 on AMGT_RESAPP.TO-AMGT-rk-28 (checker gains a data-vacuity shape)

THE BAR FIRST: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-30-ck`; `org/` and `.tools/` both present ->
TREE-OK.

READ THE ORDER. Chain CK, a single order (`AMGT-rk-28`), sibling of `AMGT-rk-9` AC4. `.tools/criteria_quality_checker.py`
(358 ln, built by `AMGT-rk-9`) refuses five shapes; this order adds a SIXTH, `shape6_data_vacuity`, for round-12's
`rk-15` AC3 measured instance: a criterion counting occurrences of a field-name TOKEN can PASS while every counted
value is invented, missing or unverified -- the count proves PRESENCE, never VALUE.

BUILT: added `COUNT_METHOD_RE` (`.count(`, `grep -c`, `wc -l`, "occurrences of", "counts of"),
`FIELD_COUNT_EXPECT_RE` (a token followed by a comparator and a number, e.g. `points-emitted >= 6`), and
`VALUE_CHECK_RE` (equals/matches/matched against/compared to-against/source excerpt/specific value/expected
value/per-item) as new module-level regexes, following the existing pattern beside `FILE_TOKEN_RE`.
`shape6_data_vacuity(c)` flags when the invocation carries a counting method AND expect carries a bare
token-comparator-number shape, UNLESS the combined invocation+expect+verbatim text also carries a value-check
phrase. Wired into `evaluate()`'s per-criterion tuple alongside shape1/2/4/5 (shape3 stays a separate whole-set
pass, unchanged). Added ONE sealed mutant (`MUT-6`) mirroring round-12's `rk-15` AC3 shape (`.count('points_emitted')`
against raw text; expect `points-emitted >= 6`) and one clean control (`CTRL-6`, reads the field via `json.load`
and asserts a specific value "matched against the source excerpt") to `_self_test()`.

DEVIATION FROM shape1..shape5's INTERNAL CONVENTION, NOTED: shape1_zero_collected through shape5_no_timeout all
index their input dict (`c["invocation"]`, assuming `_norm()` already ran). AC1's own literal invocation calls
`cqc.shape6_data_vacuity(mutant)` DIRECTLY on a bare `{id, invocation, expect}` dict, never through `_norm()`/`_mk()`
-- indexing would raise `KeyError` on the missing `method`/`verbatim`/etc keys. `shape6_data_vacuity` was written
with `c.get(...)` throughout specifically so it survives being called both ways (through `evaluate()` post-`_norm()`,
and directly on a raw dict as AC1 does); this is the one place this cell's function deliberately does NOT
mirror shape1's exact indexing style, because shape1 is never called that way and shape6 is (by this order's own
proof clause). The RETURN SHAPE (a formatted string or `None`) and OUTER SIGNATURE (`def shapeN_x(c):`) do match
shape1 exactly, per the order's instruction.

SELF-TEST SUMMARY LOGIC GENERALIZED: the pre-existing `_self_test()` print/tally loop special-cased the single
id `"CTRL-1"` to mean "this is the clean control." With a second control (`CTRL-6`) this would have silently
mis-tallied CTRL-6 as a mutant. Changed the check to `mid.startswith("CTRL")` and made the mutant/control counts
and the printed "N of N" denominators computed from the `results` list rather than hard-coded 5/1, so the summary
is correct for any number of shape pairs without another hand-edit at the next shape. This IS the wiring/reporting
work the order asks for ("Wire it into `evaluate()`'s per-criterion loop... in the same position/order style as
the other five shapes" + "Add ONE sealed mutant + one clean control to `_self_test()`") -- no existing shape's
OWN detection function body was touched, per the order's explicit prohibition.

ITERATION NOTE: the first draft of `MUT-6`/`CTRL-6` omitted a `timeout <N>` bound in the invocation text (unlike
the existing `CTRL-1`, which carries `timeout 90`). Running `--self-test` showed `CTRL-6 -> REFUSED (WRONG)`,
and a direct `evaluate()` call on the raw dict showed the flag was `NO-TIMEOUT`, not `DATA-VACUITY` -- i.e. the
pre-existing shape5 fired on my new control, not a shape6 defect. Added `timeout 30` to both `MUT-6` and `CTRL-6`
invocations so the pair isolates shape6 specifically; MUT-6 remains REFUSED afterward (now for the intended
DATA-VACUITY reason, confirmed by removing the timeout again and reading the flags dict directly: both
NO-TIMEOUT and DATA-VACUITY fire, proving shape6 itself -- not just shape5 -- flags the mutant).

PROOF: AC1 (direct `shape6_data_vacuity` calls on the order's own literal mutant/clean dicts) and AC2
(`--self-test` tail) both run byte-for-byte as the order's literal invocations and both PASS; see
`AMGT_RESAPP.TO-AMGT-rk-28.checker-data-vacuity-shape.proof_of_spec.json` in this folder for verbatim output.

py_compile clean throughout; non-ASCII scan: 0 bytes (`len(b) - len(b.decode('utf-8')) == 0`).

NO SURPRISE ROW FILED: nothing off-task was found. The order's own narrow scope (one function, wired in, one
mutant/control pair) was fully satisfiable as written; no criterion was refused.
