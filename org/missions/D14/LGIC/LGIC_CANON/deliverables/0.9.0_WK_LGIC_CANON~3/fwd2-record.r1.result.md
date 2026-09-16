# RESULT -- LGIC_CANON.TO-CN-r-1 (FWD-2 graded from the record), cell CN-r-1

**Worker:** 0.9.0_WK_LGIC_CANON~3 · **Branch:** wk-lgic-canon-1-3, cut from CLOUD @f95470f384 · **Issuer:**
2.0.0_SA_COO~G · **Grades nothing:** R1-J1 is 3.0.0_SA_CVO's at L9.

## 1. PREMISES RE-GROUNDED AT HEAD (f95470f384)

| premise the order states | read | result |
|---|---|---|
| nine-calls record @c6be748be7, card 3 "defaults", rows 17 and 18 by his word | `git log -- <record>` shows c6be748be7 as its only commit; card 3 at :34, card 8 at :39, card 9 at :40 | HOLDS |
| the table @6dab0d76a7 reads v0.2 TICKED, "Nothing on this table is open" | title :1 "v0.2 (TICKED)"; :70; `git diff --stat 6dab0d76a7 HEAD` on the file prints nothing | HOLDS (unchanged to HEAD) |
| rows 14 to 16 pre-filled from his 2026-08-25 word | v0.1 @54a764cb28 :59-61 "✓ ruled" before the sitting, :66; the 08-25 record @554dd55682 :37-38 | HOLDS |
| PRD DEC-3 | `org/missions/D14/LGIC/LGIC_CANON/prd/LGIC_CANON_PRD.md` :179-185 | HOLDS, same content as the order's cell text |

No premise failed. The one row filed (LGIC_CANON-W3-S1) is about the checker's decoding, not about a premise.

## 2. WHAT WAS WRITTEN

`org/missions/D14/LGIC/LGIC_CANON/deliverables/FWD2_FROM_RECORD.md`:
- a quoted section for the table's v0.2 TICKED state (@6dab0d76a7 :1 and :69-70)
- reading notes, not a grade: the ticks were given against v0.1 @54a764cb28, and the counts of rows ticked at their
  defaults are printed on different bases in the record (:34 "the 16 defaults"), v0.1 (:66 "Sixteen rows want a tick")
  and v0.2 (:69 "rows 1-13 ticked at their defaults")
- exactly three lines, `CLAUSE 1:`, `CLAUSE 2:` and `CLAUSE 3:`, each carrying its evidence as `path@commit :line`:

| clause | evidence cited |
|---|---|
| 1 one sitting | the nine-calls record @c6be748be7 :15-18, :34, :39, :40; the ticklist @6dab0d76a7 :14-16, :69-70 |
| 2 enough beside every row | the ticklist @54a764cb28 :7-11 and :44 (the table as put to him); @6dab0d76a7 :47; the nine-calls record @c6be748be7 :15-16 |
| 3 pre-decided rows pre-filled | the ticklist @54a764cb28 :59-61, :66; the 08-25 record @554dd55682 :37-38; the ticklist @6dab0d76a7 :62-64, :69 |

## 3. CRITERIA

**R1-AC1** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py r1-clauses`
```
CLAUSES: 3  EACH BESIDE RESOLVABLE EVIDENCE: 3
VERDICT: PASS-R1-CLAUSES-EVIDENCED
rc=0
```
Denominator: 3 of 3 clauses. Expect `VERDICT: PASS-R1-CLAUSES-EVIDENCED`: matched. **PASS-by-output.**

**R1-AC2** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py r1-ticked`
```
[stderr: 3 x UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 2743, Thread-11/-23/-35 _readerthread -- row LGIC_CANON-W3-S1]
QUOTES 'Nothing on this table is open': True  CITES infra/logic/04_SCOPE_TICKLIST.md@<commit> WHERE THAT TEXT AND v0.2 STAND: 4
VERDICT: PASS-R1-TICKED-QUOTED
rc=0
```
Denominator: 4 ticklist citations at @6dab0d76a7 stand. The @54a764cb28 citations are the ones that tracebacked, and
they do not carry the line. Expect `VERDICT: PASS-R1-TICKED-QUOTED`: matched. **PASS-by-output.**

**R1-J1** -- judgment. RECORDED; NO VERDICT. The evidence per clause is the table in section 2; 3.0.0_SA_CVO grades it
at L9.

## 4. CONTROLS

- **Mutants:** three of them, each built on a scratch copy under `.scratch/mut/<name>/` by `.scratch/mut/run_mutants.py`,
  never on the tracked file. 3 of 3 fired as expected:
  - M1 (CLAUSE 2's commits replaced by @0000000000): `EACH BESIDE RESOLVABLE EVIDENCE: 2 | VERDICT: FAIL-R1-CLAUSE-UNEVIDENCED`
  - M2 (every ticklist citation moved to v0.1 @54a764cb28): `STAND: 0 | VERDICT: FAIL-R1-TICKED-UNQUOTED`
  - M3 (the phrase not quoted): `QUOTES ...: False ... STAND: 4 | VERDICT: FAIL-R1-TICKED-UNQUOTED`
- **Determinism:** both criteria were run twice on the same file. The same verdicts and the same denominators came
  back (3 of 3; 4).

## 5. ROWS

- `LGIC_CANON-W3-S1` -- OBSERVATION, INERT. check_canon_r1.py's git() decodes in cp1252. A cited commit whose bytes
  cp1252 cannot decode prints a traceback and reads as not resolving. The direction is a false FAIL, never a false
  PASS, and this order's verdict is unaffected.

## 6. DECLARED LIMITS

- No grade on whether the evidence *supports* each clause: that is R1-J1, at L9.
- The PRD was read at the worktree's HEAD, where its last commit is 5b2336a5e4 (v1.3), the pin the order cites.
  DEC-3's text is as the order quotes it.
- Nothing live was touched (PRD DEC-9). Nothing was written outside the order's `<paths>` and this deliverables folder.
