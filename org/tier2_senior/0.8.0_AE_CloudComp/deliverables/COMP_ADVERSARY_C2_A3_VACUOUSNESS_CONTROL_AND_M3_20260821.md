# comp-adversary control 2 -- A3 vacuousness control + mutant M3

**Seat:** `0.8.0_AE_CloudComp~A` (repair lane, Andrew-direct via MSTR 64164/64161)
**Companion records:** base `0.8.0_AE_CloudComp`'s `COMP_ADVERSARY_C2_ACCEPTANCE_20260821.md`,
`COMP_ADVERSARY_C2_ACCEPTANCE_A4_TRANSCRIPT.txt` (A4-M1), `COMP_ADVERSARY_C2_A3_LOOP.txt` (A3 loop).
**Subject:** `.tools/comp-adversary` @`f5bbfaf66e` (the landed fix), read at sha256
`37a555aeeb2323e5dbc264ec0e7d496f6e9aaec7ecde2bafaf735d16b42fe459`.
**Division of labour (coordination 64165/64166/64167):** base built the fix and ran A4-M1; this
seat ran the two arms base's evidence lacked -- the A3 **vacuousness control** and mutant **M3**.

---

## 1. THE MEASUREMENT THAT REFRAMES A3 -- the defect's window is ~205 ms, not ~16.5 s

The defect lives in the gap between `self_test`'s HEAD read (`:260`) and `compose()`'s OWN HEAD read
(`:171`). Measured directly, by timestamping both `rev-parse HEAD` calls in a live run:

| run | 1 | 2 | 3 | 4 | 5 | **median** |
|---|---|---|---|---|---|---|
| setup -> compose window (ms) | 205.2 | 234.4 | 364.2 | 55.6 | 55.0 | **205.2** |

A full `--self-test` run is **~16,500 ms**. **The window a HEAD-before/after-the-run oracle measures
is ~80x wider than the window the defect occupies.** A "MOVED-MID-RUN" iteration therefore does not
establish that the advance fell in the gap; it establishes only that it fell somewhere in a span 80x
larger. *(Base named this limitation themselves in 64167 before it was measured -- this quantifies it.)*

### Consequence: ambient churn CANNOT discharge A3

Measured, cell 5 below: a background committer landed **10 commits in ~62 s** (~1 per 6.2 s) while
4 self-test iterations ran. HEAD advanced between **every** iteration -- churn was unambiguously live
-- and the window was crossed **0 / 4 times**. At a 205 ms window and a 6.2 s inter-commit interval,
P(cross) per iteration is roughly **3%** (order-of-magnitude, not a precise rate).

**So "run it while commits are landing" is not a test -- it is a lottery ticket with a ~3% payout,
and a green from it is indistinguishable from never having entered the condition.** The only sound
forms are (i) measure the crossing DIRECTLY, and (ii) FORCE it.

---

## 2. THE ORACLE -- setup_head != compose_head, read off compose's own header

Every iteration compares the sha `self_test` read at setup against the sha `compose` stamped into its
own `read-vintage: HEAD @...` line. Those are exactly the two reads the defect sits between, so a
disagreement is a **direct measurement** of the crossing, not an inference from it.

Both predicates are then evaluated **on the same composed output**, so the verdicts are strictly comparable:

- **OLD** (pre-fix, verbatim @`0d48f454f6`): `c2 = (head in out)`
- **NEW** (landed, verbatim @`f5bbfaf66e`): the `VERIFIED` line for the planted sha, AND the
  `(2 attempted / 1 verified / 1 UNVERIFIABLE)` denominator, AND that sha absent from `UNVERIFIABLE`.

Harness: `COMP_ADVERSARY_C2_A3_HARNESS_A.py` (beside this record). Executed in an **isolated linked
worktree** on throwaway branch `scratch/adv-a3-023918` -- never CLOUD, never pushed, torn down at the
end. Churn commits are `--allow-empty` scaffolding inside that worktree only.

---

## 3. THE EVIDENCE MATRIX -- 2 tools x 2 window states x 2 predicates

`M3` = the landed tool with **only** the pre-fix printing guard restored, byte-faithful to
@`0d48f454f6`. **The verifier itself is untouched** -- M3 breaks the *observability* of the
verification path, not its correctness. That is precisely the pre-fix state.

| # | tool | window | crossings | OLD c2 | NEW c2 | VERIFIED line |
|---|---|---|---|---|---|---|
| 1 | FIXED | quiet | 0/1 | PASS | **PASS** | present |
| 2 | FIXED | **CROSSED (injected)** | **3/3** | PASS | **PASS** | present |
| 3 | **M3** (pre-fix printing) | quiet | 0/2 | **PASS** | **FAIL** | absent |
| 4 | **M3** (pre-fix printing) | **CROSSED (injected)** | **2/2** | **FAIL** | **FAIL** | absent |
| 5 | FIXED | concurrent ambient churn | **0/4** (10 commits landed) | PASS | **PASS** | present |

### What each row establishes

- **Rows 1+2 -- A2 and A3.** The landed control passes with the window **provably crossed**, 3/3, by
  direct measurement. Row 5 adds the condition injection does not reproduce: **genuine concurrent git
  processes and real lock contention**. No false FAIL in any of them.
- **Row 3 is the load-bearing one -- A4/M3, and it is the original defect (a).** Verifier CORRECT,
  VERIFIED lines suppressed. **OLD says PASS. NEW says FAIL. Same output, same run.** That is a
  measured demonstration that the rewritten control discriminates exactly where the old one could
  not: the old form could not tell "verification path healthy" from "verification path invisible."
- **Row 4 -- defect (b), reproduced deterministically for the first time.** Under the pre-fix output
  shape with the window crossed, OLD **FAILS**. This is MSTR's 02:07Z false-FAIL, now reproducible on
  demand rather than by luck. It is also what gives the whole matrix teeth: **the old predicate is
  demonstrably capable of failing under my test condition, so the FIXED greens in rows 1/2/5 are not
  vacuous.**

---

## 4. FINDING -- THE SPECIFIED POSITIVE CONTROL WOULD ITSELF HAVE BEEN VACUOUS

The control assigned to this seat (64166/64167) was: *evaluate the OLD predicate on the fixed tool
under spanning runs; if old-c2 FAILS where new-c2 PASSES, the window was crossed.*

**That control can never fire on the fixed tool.** Row 2 shows why: with the window crossed 3/3, the
OLD predicate still reads **PASS**. The A5 half of the fix -- printing verified pins -- puts the real
sha into the output on the VERIFIED line, so `head in out` is now satisfied by the verification path
itself, no longer only by the `read-vintage` header. **A5 incidentally repaired the old predicate's
symptom while leaving its blindness intact.**

So an A3 run using that control would have concluded "churn never reached the gap" on every run,
forever, and the seat would have kept looping for a failure that cannot occur -- **an acceptance test
that could not have said otherwise, inside the acceptance of a finding about instruments that cannot
say otherwise.** The direct header-sha oracle is what actually works, and M3 (row 4) is where the old
predicate is given a fair chance to fail -- and does.

*This is surfaced, not adjudicated: it is a defect in the specified control, not in the landed fix.*

---

## 5. ACCEPTANCE BAR -- STATUS

| | bar | verdict | evidence |
|---|---|---|---|
| **A1** | c2 asserts the verification path (pin ABSENT from UNVERIFIABLE; source 1 = 2/1/1) | **MET** | landed @`f5bbfaf66e`; independently re-derived here -- rows 3+4 prove it fails when that path regresses |
| **A2** | indifferent to HEAD motion | **MET** | source-grounded (`verify_commits` rides `git cat-file -t`, HEAD-independent) + rows 2/5 exercised |
| **A3** | exercised across a LIVE COMMIT WINDOW | **MET, non-vacuously** | rows 2+5; crossing measured DIRECTLY 3/3; teeth proven by row 4 |
| **A4** | negative control -- break verification, confirm c2 FAILS | **MET** | M1 (verifier always fails) at base, transcript @`9f8a09c051`; **M3 (this seat), rows 3+4** |
| **A5** | print verified pins | **MET** | landed @`f5bbfaf66e`; VERIFIED line present rows 1/2/5, absent 3/4 |

**Restore proof (A4):** the shared `.tools/comp-adversary` is byte-identical to its pre-exercise
baseline -- sha256 `37a555aeeb...fe459` before and after, `git status --porcelain` empty. **No mutant
was ever written to the shared working tree**: M3 ran as a scratchpad copy with cwd set to the scratch
worktree, so `repo_root()` resolved identically while the shared tree stayed clean. This was deliberate
-- ~8 seats live in this worktree, and a transiently-broken `.tools/comp-adversary` could be picked up
by another seat's run or swept into an unrelated `safe-commit` pathspec (the @`6d14f2d15` "test subject"
class). Base independently ran M1 by in-memory monkeypatch, which has the same property.

---

## 6. SURFACED, NOT ABSORBED (scope fence held -- one control, not a rewrite)

1. **The specified positive control is vacuous on the fixed tool** (section 4). Recommend the direct
   header-sha oracle wherever this bar is re-run.
2. **A HEAD-before/after-the-run oracle understates the window by ~80x** (section 1). Any future
   HEAD-churn test in the estate should measure the gap it actually cares about.
3. **No defect found in the landed fix.** The compose path, declaration output, L0a family shape,
   five stages and declared-exclusions contract were not in scope and were not touched.

**Nothing in this record authorizes packaging.** Phases 2 and 3 (skill + design home + comp-which
vocabulary; Workflow orchestration) remain sequenced behind the full A1-A5 close per Andrew's word.
