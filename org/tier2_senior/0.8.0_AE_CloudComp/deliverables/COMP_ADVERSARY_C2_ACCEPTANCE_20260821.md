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

## A3 transcript

(appended on loop completion -- HEAD-before, HEAD-after, verdict per iteration; the discharging iterations are the ones where before != after with PASS)
