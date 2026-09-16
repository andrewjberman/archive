# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~27 on AMGT_RESAPP.TO-AMGT-rk-9 (criteria repair at the issuer)

THE BAR FIRST: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-27`; `org/` and `.tools/` both present ->
TREE-OK. Worktree cut from SITEZ @6e4327f77f.

READ THE ORDER. Chain E, a single order (`AMGT-rk-9`). The DELIVER list names FIVE shapes a checker must refuse
(zero-collected denominator; a piped runner whose rc is swallowed; a pre/post census pair at different grains;
a capture asserted by an inexact filename; a criterion with no staged/cold timeout bound), plus a mandatory
sealed planted mutant per shape and a clean control, all counted and printed (AC2), and a run of the checker
over this round's own text (AC3), plus a JUDGMENT (AC4) on whether the checker would have refused round 11's
two actual criteria-that-could-not-fail.

BUILT: `.tools/criteria_quality_checker.py` (358 lines). Five REGEX-based shape detectors operating on a common
normalized criterion dict (id, method, invocation, expect, verbatim, output_evidence, denominator), readable
from either a PROOF-OF-SPEC instance (`acceptance[]` rows, post-execution) or a TASK-ORDER `.md` file's
`<proof_of_spec>` block (`<criterion>` elements, pre-execution). A `--self-test` mode runs five sealed planted
mutants (synthetic, embedded in the file) plus one clean control and prints the discrimination count.

ITERATION 1: built, compiled, self-test discriminated 5/5 + 1/1 on the first pass.

ITERATION 2 (precision fix, found while running AC3 over the round's own orders): the INEXACT-CAPTURE detector's
context regex `captur\w*` matched Python's `capture_output=True` subprocess.run() kwarg -- unrelated boilerplate
present in this order's own AC2/AC3 invocations, which locate the checker via a wildcard glob. Fixed with a
negative lookahead (`captur(?!e_output)\w*`) so the real "captured"/"capturing" language still matches while
the kwarg does not. Re-verified: rk-9's own AC2/AC3 no longer false-flag; rk-8 AC4's genuine "captured" match
(a route set saved to a wildcarded path) still fires. Self-test re-run, still 5/5 + 1/1.

ITERATION 3 (RUNNER_RE widening, found while building AC4's real-specimen evidence): the actual round-11
zero-collected defect (row `AMGT_RESAPP-Z-W18-S1`, grounded at commit `10c74d0efb`) used
`python -m unittest discover`, which the checker's RUNNER_RE did not recognize (it only knew pytest/bun
test/jest/etc.), so the checker would NOT have caught the real historical defect it exists to catch. Widened
RUNNER_RE to include `python -m unittest` / `unittest discover`. Re-verified against the real W18-S1 invocation
and output (quoted verbatim from the investigation row) -> REFUSED, matching `\bran\s+0\s+test`. Self-test
re-run again, still 5/5 + 1/1 (the widening did not change the self-test's synthetic pytest-shaped mutant).

AC1: `checker-files 1`, `.tools/criteria_quality_checker.py`, 358 lines. Met.

AC2: self-test run, rc 0, five refusals + one admission, DENOMINATOR line printed, DISCRIMINATES. Run twice,
byte-identical (determinism). Met.

AC3: the LITERAL invocation was run byte-for-byte: rc 0, orders-scanned 40, verdicts printed. Investigating the
scanned set (a re-grounding this worker ran because the criterion's own `<expect>` names "this round's own
sixteen orders"): `sorted(os.listdir(t))[:40]` takes the first 40 files alphabetically from the WHOLE 80-file
task-orders directory, stopping at `rj-13` -- 0 of the round's 16 `rk-*` orders are in that slice. This is filed
as row `AMGT_RESAPP-Z-W27-S1`. The literal invocation's own bar (nonzero denominator, per-file verdicts printed)
is still met, so AC3 is not FAILED by this; a SUPPLEMENTARY run of the same tool directly against the 16 rk-*
orders was executed and recorded alongside the literal run so the round's actual population is examined and
reported: 16 of 16 orders flagged, overwhelmingly NO-TIMEOUT (53 of 56 criteria), one genuine INEXACT-CAPTURE
(rk-8 AC4), and one likely FALSE POSITIVE (rk-5 AC3's ZERO-COLLECTED flag, which fired on the criterion's own
prohibitive prose about round 11's defect rather than on evidence of an actual zero-collected run) -- disclosed
honestly rather than patched away, per the instruction not to soften the checker to make this round's orders
pass.

AC4 (JUDGMENT, no self-graded verdict): literal invocation run; three discrimination arms added as evidence --
(1) the REAL round-11 zero-collected suite (W18-S1) -> REFUSED; (2) the REAL round-11 verbatim-gate vacuous
pass (W20-S5, a data/business-rule defect on live filing text carrying no quotation marks) -> ADMITTED and
disclosed as OUTSIDE the five named textual shapes, never claimed as covered; (3) one honest control -> ADMITTED
unchanged. Evidence recorded; verdict left to `3.0.0_SA_CVO~Z` at L9.

MID-TASK ISSUER AMENDMENT (2.0.0_SA_COO~Z, ~2026-09-16 07:0xZ): every round-12 order's `<paths>` omitted its own
file, found by `0.9.0_WK_AMGT_RESAPP~28` on `AMGT-rk-10` (row `AMGT_RESAPP-Z-W28-S1`, already filed and ruled --
not re-filed here). Fixed at `6f433fc2a8`, drained `f94429b776`. Directed: `git merge --ff-only` the main tree's
HEAD before the final commit. The merge initially refused (`error: Your local changes to
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md would be overwritten`)
because this worker's own uncommitted splice of row S1 and the amendment's drain both touched the tail of the
same append-only fenced JSON array with GENUINELY DIFFERENT bytes (this worker's S1 vs the sibling's W28-S1) --
a real conflict, not a same-bytes false one. Resolved by: (1) snapshotting this worker's dirty copy to
`.scratch/`; (2) restoring the file to this worker's own HEAD via `git show HEAD:<path> > <path>` (never
`git checkout --`); (3) running the now-unblocked `git merge --ff-only`, which fast-forwarded cleanly and landed
`AMGT_RESAPP-Z-W28-S1` at the tail; (4) re-splicing this worker's own row (S1) after it by the same textual-splice
method used originally. Verified at each step: the fenced JSON array parses, pure LF throughout (0 CRLF bytes),
both rows present in the final file. rk-9's own `<paths>` now names its own file (confirmed by reading the
order at the new HEAD) and the criteria text (AC1-AC4) is unchanged, as the amendment states.

ROUND-13 CANDIDATE (per the issuer's explicit bound, not built here): the amendment names a genuine SIXTH shape
this cell's five do not cover -- an order whose mandated final write (the status flip) is outside its own
`<paths>` grant. The issuer's own message: "do not let it displace your five named shapes ... if adding it would
push you past your criteria as written, file a row naming it for round 13 instead." Measured the named
before/after specimen directly (0 of 16 round-12 orders name their own file at commit `2726497094`; 16 of 16 do
at HEAD) and filed it as row `AMGT_RESAPP-Z-W27-S2` with a proposed detection recipe, without adding a sixth arm
to the shipped checker.

PUSH STATE: LOCAL only. This worker never pushes; the branch is `wk-amgt_resapp-12-27`.
