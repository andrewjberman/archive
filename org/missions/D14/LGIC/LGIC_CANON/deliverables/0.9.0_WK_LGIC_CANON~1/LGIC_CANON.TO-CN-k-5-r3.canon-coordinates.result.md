# LGIC_CANON.TO-CN-k-5-r3 -- result (cell CN-k-5, round 3)

**Worker:** `0.9.0_WK_LGIC_CANON~1` · **Worktree:** `wk-lgic-canon-3-1` · **Base:** CLOUD @`3da3b4204f`
(carries this slot's earlier order CN-k-4, merged).

## What the cell did

Four edits to `infra/logic/02_DOCTRINE.md` and one to `infra/logic/10_ONBOARDING_CHECKLIST.md`, per
ruling R-9 (`SELF_DRIVE_LGIC_RULINGS_20260916.md:304-334`) and the round-2 analysis's rulings A-19 and
A-6 RESTATED (`LGIC_CANON_ROUND2_ANALYSIS.md` s.2).

### 1. The four `resolves R-9(iii) C<k>:` coordinate lines

Each is ONE line, inside its named rule block, reading the answer FROM the canon's own already-ruled
text (never inventing a new ruling):

- **C1, in R10, naming R9** (`infra/logic/02_DOCTRINE.md:433`): R9's "Monolith bronze CONFORMANT" clearance
  rests on a stated MECHANISM -- a bucket-policy deny that blocks a non-raw write at ingest, scoped to the
  whole monolith bucket. R10 carries no equivalent write-time deny, and R10's own test is CONTENT (dedup,
  dtype, completeness, event-trigger), which a deny mechanism does not reach. So R9's clearance does not
  extend to SILVER by analogy: `orion/inflection/silver/` and `eclipse/inflection/silver/` read UNDETERMINED
  on A5 for want of plane-specific evidence, never CONFORMS by borrowing R9's bronze finding. This is the
  reading judge C already applied and stated its reasoning for
  (`deliverables/0.9.0_WK_LGIC_CANON~4/judge-c.r2.result.md:64-70`), now written into the rule itself so a
  later reader does not have to re-derive it from a judge's private method note. Traced split:
  `judge-compare-r2.md` D1, D3.
- **C2, in R1, naming its own census** (`infra/logic/02_DOCTRINE.md:175`): R1's GRAMMAR binds the KEY (the
  full `{source}/{scope}/{tier}/{table}/{partition}` string); its own `census` tag ("53 of 53 ... monolith
  PLANES CONFORMANT") is a PLANE-level sweep, never a per-key audit. A plane-level clearance therefore does
  not clear a departure found by grading one KEY beneath that plane -- a bare date occupying the `{table}`
  slot reads OUT-OF-PATTERN against the grammar on its own terms, whatever the plane's census tag says.
  Traced split: `judge-compare-r2.md` D2.
- **C3, in R6, naming R5** (`infra/logic/02_DOCTRINE.md:399`): the canon already RULED this, in its own §6
  (`:612-614` at HEAD, card 2, ~01:3xZ 2026-09-13): the spelled-out LONG-form buckets become THE firm
  buckets, and the legacy short-form three -- `opal-data-inf` included -- RETIRE after migration. So
  `opal-data-inf/platinum/` and `opal-data-inf/gold/` sit on the RETIRING legacy plane, not the ruled firm
  bucket that R5 names; R6's own CONFORMANT count on `inf` is a CURRENT-STATE reading under R19's in-flight
  migration, not a settled A2 clearance that the legacy short-form bucket equals "the firm's bucket." Traced
  split: `judge-compare-r2.md` D4, D5 (one identity reached twice, on platinum and gold).
- **C4, in R19, naming R18** (`infra/logic/02_DOCTRINE.md:557`): R19 assigns a migrating plane no separate
  IN-FLIGHT status -- it stays graded by R18's ordinary test. R18 states no duration threshold (its 31-day
  census example is a measured instance, not a floor); its only carve-out is a same-window rollback copy
  named in a never-widen sign-off, and R19 itself REQUIRES that sign-off on every served key that moves. So a
  migration mid-cutover with that sign-off on file reads DECLARED-EXCEPTION; one without it reads VIOLATES
  under R20's ordinary undeclared-departure default -- never UNDETERMINED for want of a "standing" test
  neither rule names. Traced split: `judge-compare-r2.md` D6.

None of the four needed a sovereign call outside the record: C1 and C2 are read from the cited rules' own
stated mechanism and grain; C3 is read from an EXISTING Andrew-ruled disposition (§6 card 2) the canon
already carries but had not connected to R5/R6's split; C4 is read from R18's and R19's own text (the
sign-off requirement plus R20's default). No BLOCKING row was filed on this criterion.

### 2. Title and census recount (A-19)

Line 1: `v1.0` -> `v1.1` (the content changes round 2's CN-k-2 cell landed were already logged in section 7
as a "v1.1" changelog entry, but the title heading itself was never bumped -- this cell's own cut defect,
named and fixed). Section 0's line: recounted by rule block (22 blocks total, all 22 carrying
`authority:`/`census:`/`non-application:`) -- `21 of 21` -> `22 of 22`.

### 3. R1's census vintage (A-4, re-scoped by A-19)

`01_CENSUS.md @d35653da5e` commits 2026-09-12 12:53:33 -0400 (`git show -s --format='%H %ci %s' d35653da5e`),
which PREDATES the SOURCE-FIRST ruling (~03:2xZ 2026-09-13). R1's `census:` line now reads "as of
`01_CENSUS.md` @d35653da5e (2026-09-12) -- predating the SOURCE-FIRST ruling ..., so the 53-of-53 sweep was
measured under this rule's PRIOR (collapsed, tier-first-in-a-scoped-bucket) reading, never re-measured
against the text above."

### 4. A-6 restated in the checklist's INPUTS words

`infra/logic/10_ONBOARDING_CHECKLIST.md`'s SHORT-form row: mark `**SOVEREIGN** where Andrew gives one, else
**DERIVED**` -> `**SOVEREIGN**`. Its who-gives cell: "supplied ONCE on the identity row -- by Andrew, or by
the CRO in the registry on his word -- and READ thereafter by every builder: `name()` looks the short form UP
on that row ... and `validate()` refuses a FIRM row without one; no derivation is built." The count sentence
recounted: "Nine rows: five SOVEREIGN, four GIVEN, and none the person running the checklist decides" (was
"five SOVEREIGN (one of them SOVEREIGN-or-DERIVED), four GIVEN"). `validate()`'s own text confirms `short` is
required on every scope row (`lib/opal_naming.py:326`, the `for f in ("key", "class", "long", "short",
"tenancy", "bucket")` refusal loop), consistent with the restated claim.

### 5. Change log

One new row added under `v1.1` (2026-09-17), naming the title bump, the census recount, the four
coordinates and the R1 vintage, so section 7 states what landed and when, without inventing a new version
number the checker does not ask for.

## Mechanical criteria, run at this commit (before pinning)

```
$ timeout 300 python .../fixed_inputs/r3/check_canon_r3.py k5-census
title line: '# 02 -- THE PLATFORM LOGIC CANON (the doctrine) -- v1.1' -> carries v1.1: True
RULE BLOCKS RECOUNTED -- DENOMINATOR 22 block(s); carrying all three parts: 22
blocks missing a part: []
section 0 types: 22 of 22
VERDICT: PASS-K5-CENSUS-RECOUNTED

$ timeout 300 python .../fixed_inputs/r3/check_canon_r3.py k5-coordinates
COORDINATES -- DENOMINATOR 4 (R-9 iii)
  C1 in R10: 1 line(s), naming \bR9\b: 1
  C2 in R1: 1 line(s), naming \bcensus\b: 1
  C3 in R6: 1 line(s), naming \bR5\b: 1
  C4 in R19: 1 line(s), naming \bR18\b: 1
coordinates carried: 4 of 4
VERDICT: PASS-K5-FOUR-COORDINATES

$ timeout 300 python .../fixed_inputs/r3/check_canon_r3.py k5-r1-vintage
R1 block census line(s), denominator 1: ["census: 53 of 53 ... CONFORMANT, as of `01_CENSUS.md` @d35653da5e (2026-09-"]
carrying a vintage ('as of' + @hash or a date): 1
VERDICT: PASS-K5-R1-CENSUS-VINTAGED

$ timeout 300 python .../fixed_inputs/r3/check_canon_r3.py k5-short-sovereign
INPUT ROWS -- DENOMINATOR 9; marks SOVEREIGN 5, GIVEN 4, other []
SHORT row(s): 1; its mark: 'SOVEREIGN'
the prose count reads (rows, SOVEREIGN, GIVEN): (9, 5, 4)
VERDICT: PASS-K5-SHORT-SOVEREIGN-READ

$ timeout 300 python .../fixed_inputs/r3/check_canon_r3.py o3-sovereign
THE INPUTS section -- DENOMINATOR 14 input row(s); MARKED SOVEREIGN: 6
VERDICT: PASS-O3-SOVEREIGN-ROWS-COUNTED

$ timeout 300 python .../fixed_inputs/r2/check_canon_r2.py k4-fresh
the section stamps the schema: True ; render --check FRESH: True
VERDICT: PASS-K4-RERENDERED-AT-SCHEMA
```

## K5R3-AC7 (judgment, for `3.0.0_SA_CVO` at L9)

Each coordinate line answers the split it names from a ruling that already exists in the record (R9's own
stated deny mechanism; R1's own stated grain; the canon's own §6 card-2 disposition; R18's/R19's own
sign-off/default text) -- none required Andrew's sovereign call, so no BLOCKING row was filed. The R1 vintage
is TRUE, measured (`git show -s d35653da5e`, predating the SOURCE-FIRST ruling). A-6's restated words match
`name()` (`lib/opal_naming.py:1552`, `_long_scope(...)["short"]`, reads the row) and `validate()`
(`lib/opal_naming.py:326`, `short` required on every scope row). This is presented for L9 judgment, not
self-graded.

## Provenance

```
GROUNDED ON: SELF_DRIVE_LGIC_RULINGS_20260916.md:304-334 (R-9); LGIC_CANON_ROUND2_ANALYSIS.md s.2 (A-4, A-6
             RESTATED, A-19); judge-compare-r2.md s.1 (D1-D6) and s.0; infra/logic/02_DOCTRINE.md :1, :28,
             R1/R5/R6/R9/R10/R18/R19/section-6 at this commit's pre-edit HEAD (3da3b4204f); lib/opal_naming.py
             :285-323 (validate), :1530-1610 (name, _long_scope); git show -s d35653da5e
NOT READ:    the other nine round-3 cells' outputs (not yet cut/drained at this worker's spawn); the judges'
             CN-j-8/9/10 orders (this cell runs BEFORE the judges per the decomposition's `depends on: nothing;
             before the judges`)
PUSH STATE:  LOCAL on wk-lgic-canon-3-1 at write; not pushed
```
