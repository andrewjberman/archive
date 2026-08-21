# comp-adversary self-test control 2 -- repair + acceptance record (Andrew's bar A1-A5)

**Author:** 0.8.0_AE_CloudComp, 2026-08-21 · **Finding:** 0.0.0_AB_MSTR 64159 (both anti-correlated directions measured at source) · **Sequence:** ANDREW-DIRECT via MSTR 64161 ("fix the control first" -- the packaging of comp-adversary as a slash command is HELD BY HIS WORD until this bar discharges; his rationale: a mandatory validation instrument whose discriminating control cannot fail on its own subject propagates a false green to every seat that invokes it).
**Fix commit:** @f5bbfaf66e (+ comp-system discharge) -- landed BEFORE the relay of his sequence arrived; the bar below is discharged against those bytes.

## The defect (MSTR's derivation, confirmed at source)
Old control 2 was `head in out` with HEAD read at setup (:257) and compose reading HEAD again (:260). A VERIFIED pin was COUNTED, never PRINTED -- so the only place the sha could appear was the `read-vintage:` header. Consequences, both measured: (a) a regressed verifier flagging every real commit UNVERIFIABLE would still PASS (the control could not fail on its own subject); (b) HEAD advancing mid-run -- the NORMAL state on this shared worktree -- failed the control on a healthy tool (the 02:07Z flip).

## The fix (@f5bbfaf66e)
1. compose prints EVERY pin's verdict, VERIFIED included -- the silence about successes is what made the old control reach for the header (A5).
2. control 2 asserts the VERIFICATION PATH's own printed claims: the planted real pin's `@<sha> : VERIFIED` line present, the pin ABSENT from the UNVERIFIABLE list, and the source-1 denominator `(2 attempted / 1 verified / 1 UNVERIFIABLE)` (A1).
3. HEAD-churn immunity BY CONSTRUCTION: the assertion no longer references the live-composed header at all; the planted sha remains a real commit in history regardless of later HEAD advances (A2 -- the pin-HEAD-once mechanism was offered as optional and was not needed: the dependency on HEAD equality is REMOVED, not synchronized).

## The bar, discharged

| # | Criterion | Evidence |
|---|---|---|
| A1 | c2 asserts the property it names (pin absent from UNVERIFIABLE + 2/1/1 denominator) | the predicate at `.tools/comp-adversary` control 2 @f5bbfaf66e; self-test PASS 4/4 through the verification path |
| A2 | indifferent to HEAD motion | by construction (no header reference); EXERCISED under A3's live window below |
| A3 | exercised across a LIVE COMMIT WINDOW -- the exact condition that produced the false FAIL | transcript appended below: self-test iterations with HEAD captured before/after each; iterations where HEAD MOVED MID-RUN and the verdict stayed PASS 4/4 (real commits -- this very evidence record -- landing concurrently) |
| A4 | negative control: a deliberately regressed verifier makes the NEW c2 FAIL | transcript in the A4 appendix: `verify_commits` monkeypatched to flag EVERY commit (the exact regression the finding names) -> control 2 FAIL, self-test rc=1; restored -> PASS 4/4 rc=0. The repaired control has been MADE to fail. |
| A5 | verified pins printed | compose's source-1 block @f5bbfaf66e; the discriminating re-run: a real NON-HEAD sha (@3d3ea55f52, 0 occurrences before the fix) now prints `: VERIFIED` |

Scope held per the finding: one control repaired; the compose path, the L0a family shape, the five stages, and the declared-exclusions contract untouched.

## A3 transcript (loop completed ~0234Z; full file: COMP_ADVERSARY_C2_A3_LOOP.txt)

```
iter 1 : HEAD-before 934cf14cd6 -> HEAD-after 934cf14cd6 quiet : self-test: PASS 4/4
iter 2 : HEAD-before 934cf14cd6 -> HEAD-after 934cf14cd6 quiet : self-test: PASS 4/4
iter 3 : HEAD-before 934cf14cd6 -> HEAD-after 934cf14cd6 quiet : self-test: PASS 4/4
iter 4 : HEAD-before 934cf14cd6 -> HEAD-after 934cf14cd6 quiet : self-test: PASS 4/4
iter 5 : HEAD-before 934cf14cd6 -> HEAD-after 8ff60eb580 MOVED-MID-RUN : self-test: PASS 4/4
iter 6 : HEAD-before 8ff60eb580 -> HEAD-after 9f8a09c051 MOVED-MID-RUN : self-test: PASS 4/4
iter 7 : HEAD-before 9f8a09c051 -> HEAD-after 9f8a09c051 quiet : self-test: PASS 4/4
iter 8 : HEAD-before 9f8a09c051 -> HEAD-after 9f8a09c051 quiet : self-test: PASS 4/4
```

**CORRECTED on ~A's measurement (64218 @d745b8a341) -- this loop DID NOT ESTABLISH THE CROSSING,
and the record says so rather than letting a spanning green overstate itself.** Iterations 5 and 6
spanned real HEAD advances with PASS 4/4, but ~A timestamped the actual defect window (self_test's
HEAD read to compose's own HEAD read): MEDIAN 205.2 ms of a ~16,500 ms run -- this loop's
before/after oracle measured a window ~80x WIDER than the defect occupies, and ~A's background
committer proved ambient churn crosses the true gap ~3% per iteration (0/4 under 1-commit-per-6s
churn). **A3's non-vacuous discharge therefore rests on ~A's DIRECT WINDOW ORACLE** (setup_head vs
the sha compose stamps into its own read-vintage header -- the exact two reads the defect sits
between): **crossings MEASURED 3/3 under injection with NEW PASS (A2+A3), and the old predicate's
ability to fail under the condition proven by the M3/injected row (OLD FAIL where crossing 2/2)**.

**TWO INSTRUMENT ERRORS AT BASE, owned:** (1) the loop oracle above (window 80x too wide -- named
as a limitation in my 64167 note to ~A, quantified by their measurement); (2) **the positive
control I ASSIGNED ~A (old-c2 fails where new-c2 passes) CANNOT FIRE ON THE FIXED TOOL** -- A5's
VERIFIED line puts the real sha into the output, satisfying `head in out` through the verification
path, so the old predicate's symptom is incidentally repaired while its blindness stands. Had ~A
run the control as I specified it, every run would read "churn never reached the gap" forever -- a
control that could not have said otherwise, assigned inside the acceptance of a finding about
exactly that class. ~A caught it BEFORE running it and substituted the direct oracle. Wherever
this bar re-runs, use the header-sha oracle, never the assigned form.

**A4 is TWO DIFFERENT MUTANTS, both required:** M1 (correctness regression -- verifier flags real
commits; base, in-memory monkeypatch) and ~A's M3 (OBSERVABILITY regression -- verifier correct,
VERIFIED lines suppressed = byte-faithful pre-fix state; scratch-copy + isolated linked worktree,
shared tree untouched, sha256-verified). The matrix's load-bearing row: same composed output, OLD
PASS / NEW FAIL -- the rewritten control discriminates "verification healthy" from "verification
invisible", which the old one could not.

**BAR: A1-A5 MET across both seats** (~A's matrix rows cited per criterion in their 64218; their
commit @d745b8a341 is LOCAL pending MSTR's integration window -- flagged, not assumed published).
