# LGIC_CANON.CN-k-2-r2 -- result (cell CN-k-2, round 2)

**Worker:** `0.9.0_WK_LGIC_CANON~1`. **Worktree:** `.worktrees/wk-lgic-canon-2-1`, branch `wk-lgic-canon-2-1`,
cut from CLOUD at `68644b3c19`. **Commit carrying the edit + surprise rows:** `6ba9a9affd`.

## Baseline (pre-edit, this worktree at spawn)

All six mechanical criteria FAIL before any edit (checker `check_canon_r2.py`, issued by `2.0.0_SA_COO~G`):
the canon had none of the five closed axis verdicts as its own vocabulary, no `SEVERITY ORDER` passage, R20's
own block named no axis, no `DECIDING RULE` phrase, and no rule heading named `PIPELINE INSTANCE`. `--check`
already read `CHECK: FRESH` (baseline for K2-AC6, which the edit must not disturb).

## What the edit did, one item per WORKER FACE instruction

1. **Axis verdict vocabulary (A-1).** New passage in `infra/logic/02_DOCTRINE.md` §2, bold-led
   `**THE AXIS VERDICT VOCABULARY.**`, states the five closed values (`CONFORMS`, `DECLARED-EXCEPTION`,
   `DEPARTS-RECOMMENDED`, `UNDETERMINED`, `VIOLATES`) with a table of what each says, in the canon's own words.
2. **SEVERITY ORDER (A-1).** A `**SEVERITY ORDER, least severe to most severe:**` passage immediately follows,
   with the ordered code block `CONFORMS < DECLARED-EXCEPTION < DEPARTS-RECOMMENDED < UNDETERMINED < VIOLATES`
   and the two non-obvious placements argued: `DECLARED-EXCEPTION` sits just above `CONFORMS` because R20 makes
   a declared departure the pattern working, ranked above `CONFORMS` only for the obligation it carries;
   `UNDETERMINED` sits above `DEPARTS-RECOMMENDED` and below `VIOLATES` because nobody can act on a canon gap,
   and ranking it low would let a judge park every hard plane there. Matches `CN_SEVERITY.md`'s order; no
   surprise row filed on that axis because the two agree.
3. **R20 on every axis (A-2).** R20's own block (`infra/logic/02_DOCTRINE.md:532`) now opens: "R20 reaches
   every axis alike -- A1 INGESTION, A2 BUCKET STRUCTURE, A3 NAMING, A4 COMPUTE and A5 FORMAT (§2) --
   because it is the rule that decides an axis's verdict whenever a departure exists: undeclared, the axis
   reads `VIOLATES`; declared, it reads `DECLARED-EXCEPTION`." All five axis tokens are now inside R20's block
   (checked from the `**R20` heading to the next `**R21` heading).
4. **The citation rule (A-2).** New passage `**THE CITATION RULE.**` in §2: "A verdict cites the DECIDING
   RULE -- the one rule, or the small set of rules, whose test the facts met or failed on that axis, never the
   axis's whole rule list ... An `UNDETERMINED` verdict cites the rule whose test the facts could not settle."
5. **One pipeline-instance rule (A-9).** New `R22 -- A FIRM'S PIPELINE IS A PIPELINE INSTANCE OF ITS VENDOR
   FAMILY, NOT A NEW DEFINITION`, placed in `### A4 COMPUTE` (the axis ruling A-9 names) right after R13: a
   firm's pipeline for a source is an instance of that vendor family's canonical definition, inheriting the
   family's tables, partition forms, resource set, function words and directory, with scope `<LONG>` the only
   varying input. Its `authority` line cites the round-1 analysis ruling A-9 by id.

## Coherence edits within the same file, not separately criterion-tested

- §2's axis table: A1's rules column gains `R20` (the analysis text: "section 2's A1 row lists R20 beside R9
  and R18"); A4's rules column gains `R22`, since A-9 places the new rule on the compute axis.
- §7 CHANGE LOG gains a `v1.1` row summarizing the edit, matching the v1.0 row's own convention (this same
  worker's round-1 entry).

**⛔ DID NOT TOUCH** anything between `<!-- BEGIN GENERATED NAMING SECTION -->` and
`<!-- END GENERATED NAMING SECTION -->` (lines 160-293, unchanged); `render_naming_section.py --check` reads
`CHECK: FRESH -- 0 failure(s)` after the edit, same as before it (K2-AC6).

**Not touched, on purpose:** R1's census tag / the source-first vintage mark (ruling A-4). The decomp table
(round-1 analysis s.3) lists A-4 under CN-k-2's rulings, but this task order's WORKER FACE names only the five
items above and none of `K2-AC1..AC6`/`K2-J1` reads R1. R1's census line already carries a dated
SUPERSEDED/source-first marker from round 1 (changelog v1.0). Filed as `LGIC_CANON-W1-S4`, OBSERVATION, INERT
-- not this cell's grant to resolve either way.

## Deciding output, each criterion, at commit `6ba9a9affd` (clean worktree)

```
$ python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py k2-vocab
axis verdict vocabulary, denominator 5: 5 present -- ['CONFORMS', 'VIOLATES', 'DECLARED-EXCEPTION', 'DEPARTS-RECOMMENDED', 'UNDETERMINED']
absent: none
VERDICT: PASS-K2-VOCAB-CARRIED

$ python ... k2-severity
severity passage names 5 of 5 axis verdicts, in this order: ['CONFORMS', 'DECLARED-EXCEPTION', 'DEPARTS-RECOMMENDED', 'UNDETERMINED', 'VIOLATES']
every axis verdict placed in the order: True
VERDICT: PASS-K2-SEVERITY-ORDERED

$ python ... k2-r20-axes
R20's block names 5 of 5 axes: ['A1', 'A2', 'A3', 'A4', 'A5']
axes R20 does not name: none
VERDICT: PASS-K2-R20-ON-EVERY-AXIS

$ python ... k2-citation
the canon states the citation rule (names a DECIDING RULE): True
VERDICT: PASS-K2-CITATION-RULE-STATED

$ python ... k2-instance
canon rules whose heading names PIPELINE INSTANCE, denominator 1 expected: 1 ['R22']
VERDICT: PASS-K2-INSTANCE-RULE-ONCE

$ python ... k2-render-fresh
OK: stamp org/standards/NAMING_SCHEMA.json v1.9 sha256:3ade1e7b01f86862f104b8240a1a2a83b54d4f118cd9eec781c2ef22e2b6b39c equals the live file
OK: stamp infra/logic/registry/scopes.json - sha256:b2a54608f8ebbade98982de9fc8ae6a7d4e40ce83ee4f32c146f08cd69a0034b equals the live file
OK: the section's bytes equal a fresh render (134 lines, CRLF normalised)
CHECK: FRESH -- 0 failure(s)
render --check reads FRESH after the canon edit: True
VERDICT: PASS-K2-GENERATED-SECTION-UNTOUCHED
```

6 of 6 mechanical criteria PASS.

## For L9 (K2-J1)

`3.0.0_SA_CVO` grades whether the severity order's two non-obvious placements are ARGUED (not merely
asserted) and whether R22 is a rule a checklist step can actually execute. The two placements' arguments are
in §2 verbatim (above, item 2). R22 states the ONE input (the family) that CN-o-3's checklist steps 3, 7, 8
and 9 read to become mechanical (R22 says so by name, citing `10_ONBOARDING_CHECKLIST.md` STEP 3, 7, 8, 9);
CN-o-3 itself is a different cell and not this worker's to edit.

## Rows filed

- `LGIC_CANON-W1-S3` -- OBSERVATION, INERT: the WORKER FACE's round-1-analysis path
  (`org/tier1_exec/1.0.0_SA_CTO/deliverables/LGIC_CANON_ROUND1_ANALYSIS.md @26ae876d23`) never existed; the
  real file is under `org/missions/D14/LGIC/LGIC_CANON/deliverables/1.0.0_SA_CTO/`, same commit.
- `LGIC_CANON-W1-S4` -- OBSERVATION, INERT: A-4 (R1's census tag) is in the decomp table's CN-k-2 scope but
  absent from this task order's concrete edit list and criteria; left untouched by design.

Neither is blocking; both were worked around within this turn.
