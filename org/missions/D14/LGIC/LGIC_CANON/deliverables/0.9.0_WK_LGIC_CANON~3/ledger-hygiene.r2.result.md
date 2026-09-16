# RESULT -- LGIC_CANON.CN-l-2-r2 (ledger hygiene), round 2 cell CN-l-2

**Worker:** 0.9.0_WK_LGIC_CANON~3 · **Branch:** wk-lgic-canon-2-3, cut from CLOUD @68644b3c19 · **Issuer:**
2.0.0_SA_COO~G · **Grades nothing:** L2-J1 is 3.0.0_SA_CVO's at L9.

## 1. PREMISES RE-GROUNDED AT HEAD

| premise the order states | read | result |
|---|---|---|
| X8 already landed in the ledger at afb2a631b7 (v1.0 -> v1.1, register 7 -> 8, GRANTED 5 -> 6, plane counts unchanged) | `git merge-base --is-ancestor afb2a631b7 HEAD` on this worktree: true; `infra/logic/06_CONFORMANCE_LEDGER.md` title read v1.1 at start, register carried X8 (line 139), §7 read 8 register entries / 6 GRANTED / 2 OWED | HOLDS -- my base already carries X8 |
| X6's exception line names more than one axis, unclear which it excepts | `re.search(r"^.*\bX6\b.*$", ...)` on the file at start of work matched the FIRST X6-bearing line (section 2's `opal-data-demo/platinum/` row, not the register row), which named ZERO axis tokens, not several; the register row's own axis cell read the non-canonical word "tenancy" | PARTIALLY HOLDS -- ambiguous, not multiple; both occurrences were fixed to name exactly A2 |
| `ledger_recount.py` opens files in the platform default | line 136 (pre-edit) was `path.read_text(encoding="utf-8")` -- already utf-8, but via no literal `open(`, so `l2-utf8`'s `opens > 0` bar (which counts `\bopen\s*\(`) could never pass | PARTIALLY HOLDS -- not platform-default, but not the literal `open()` the checker requires either; converted to `open(path, "r", encoding="utf-8")` |
| §7's header cell reads `disposition class` as a round-1 workaround | line 165 (pre-edit): `| disposition class | rows | note |` | HOLDS |

Two premises read as directionally true but not literally as stated (see PARTIALLY HOLDS above); neither blocked the
work, both are recorded here rather than silently reconciled. A third measurement -- the recount script's SECTION/TOTAL
print format vs. `check_canon_r2.py`'s parser -- surfaced as a genuine fixed-input defect and is filed as row
`LGIC_CANON-W3-S2` (BLOCKING, INERT); see section 5.

## 2. WHAT WAS WRITTEN

`infra/logic/06_CONFORMANCE_LEDGER.md` (v1.1 -> v1.2):
- X6's axis: the register row (line 137) and the §2 cross-reference (line 94, the FIRST line in the document that
  names X6, per the checker's own `re.search`) both now read **A2**, replacing the non-canonical word "tenancy",
  per round-1 analysis ruling A-5 (row W1-S2): *"a tenancy departure is a bucket-structure departure, A2, unless the
  cell measures otherwise and says which axis and why"* -- no measurement to the contrary was found, so A2 stands.
- §7's header cell reverts from `disposition class` to `disposition`.
- A v1.2 changelog entry (§9) records all three fixes and the surprise row; no plane's disposition and no count changed.

`org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~2/ledger_recount.py`:
- The ledger read now uses a literal `open(path, "r", encoding="utf-8")` instead of `Path.read_text(encoding="utf-8")`,
  so every `open()` call in the script carries `encoding='utf-8'` explicitly (A-12).
- Plane-table selection is scoped by SECTION (`PLANE_SECTIONS = {"§1".."§5"}`, matched via the existing
  `sec_tag()` helper) rather than by the header cell's wording alone, so reverting the header text does not cause
  section 7's own count table to be miscounted as a sixth plane table. Confirmed by mutant M4 (section 4): without
  this fix, reverting the header alone produces `RECOUNT: MISMATCH 14` (plane rows 68 -> 77, RETIRE 13 -> 14, etc.).
  With the fix, `RECOUNT: OK`, 68 plane rows in 5 plane tables, 8 register entries, matching the ledger exactly.

`org/missions/D14/LGIC/LGIC_CANON/surprise-channel/investigations/INVESTIGATION_v1.md`:
- One row appended, `LGIC_CANON-W3-S2` (BLOCKING, INERT), inside the one JSON fence (re-read immediately before
  writing; last id in the corpus at read time was `LGIC_CANON-W3-S1`, so `-S2` is the next unused coordinate for W3).

## 3. CRITERIA

**L2-AC1** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py l2-x6-axis`
```
X6's line: | `opal-data-demo/platinum/` | 22,414 | 06-05 | R6 §1 | **CONFORMANT-as-DEMO-TENANT** (X6 GRANTED, axis A2, ~01:3xZ 09-13: ...
axes named on X6's line, denominator 5: ['A2']
VERDICT: PASS-L2-X6-ON-ITS-AXIS
rc=0
```
Denominator: 5 (the AXES domain A1-A5); exactly 1 named. Expect `VERDICT: PASS-L2-X6-ON-ITS-AXIS`: matched. **PASS-by-output.**

**L2-AC2** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py l2-utf8`
```
recount script: org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~2/ledger_recount.py
open() calls, denominator 1; encoding='utf-8' occurrences: 1
VERDICT: PASS-L2-RECOUNT-READS-UTF8
rc=0
```
Denominator: 1 `open()` call in the script; 1 carries `encoding='utf-8'`. Expect `VERDICT: PASS-L2-RECOUNT-READS-UTF8`: matched. **PASS-by-output.**

**L2-AC3** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py l2-header`
```
section 7 header cell reads 'disposition class' (the workaround): False
section 7 header cell reads 'disposition'       (reverted)      : True
the ledger must not be shaped to fit the checker; the checker scopes by section instead
VERDICT: PASS-L2-HEADER-REVERTED
rc=0
```
Expect `VERDICT: PASS-L2-HEADER-REVERTED`: matched. **PASS-by-output.**

**L2-AC4** -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py l2-recount`
```
recount script: org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~2/ledger_recount.py
SECTION lines: 0 ; TOTAL lines: 6
TOTAL rows the ledger's own table does not carry at the counted value, denominator 6: 6 ['CONFORMANT:', 'RETIRE:', 'GRANTED:', 'OWED:', 'DECIDED:']
VERDICT: FAIL-L2-COUNTS-REPRODUCED
rc=0
```
Expect `VERDICT: PASS-L2-COUNTS-REPRODUCED`: NOT matched. **FAIL-by-output**, and the FAIL is the checker's own
instrument defect, not a wrong count: `check_canon_r2.py:550-551` parses `SECTION`/`TOTAL` lines with `\S+`-only
regexes that (a) cannot capture a multi-word label (`MIGRATE (home)`, `AWAITING a word`, `PLANE ROWS (the
denominator)`, ...) and (b) glue a trailing colon onto every single-word label it does capture (`CONFORMANT:` vs.
the ledger's own cell `CONFORMANT`), so the mismatch check in `l2_recount()` fails on all 6 labels it manages to
capture and never even sees the other 8. Round 1's own checker, `check_canon_r1.py:781-782`, parses the SAME
script's SAME output correctly with a non-greedy `.+?:` regex and PASSES (`l1-recount`: `VERDICT:
PASS-L1-RECOUNT-AGREES`, rc=0, unaffected by anything in this round). Filed as row `LGIC_CANON-W3-S2`, class
BLOCKING (it blocks this criterion), hazard_standing INERT (nothing propagates the defect elsewhere). Per BOUNDS,
`check_canon_r2.py` is read-only and I did not edit it, nor did I collapse `ledger_recount.py`'s section-7 labels to
single tokens (which would regress round 1's already-PASSING `l1-recount` and misstate the ledger's own multi-word
class names). The ledger's own counts are independently confirmed correct: `ledger_recount.py` run directly prints
`RECOUNT: OK`, 68 plane rows in 5 plane tables, 8 register entries, and all 14 of section 7's totals AGREE.

**L2-J1** -- judgment. RECORDED; NO VERDICT. The axis reasoning (A2, per A-5) and the header revert's effect on the
checker are recorded in sections 1-3 above; 3.0.0_SA_CVO grades both at L9.

## 4. CONTROLS

- **Mutants:** four, each applied to the TRACKED file in this isolated worktree, checked, then restored via
  `git checkout 45f5930e32 -- <path>` (confirmed clean by `git diff --stat` after each). 4 of 4 fired as expected:
  - M1 (X6's axis note removed from the §2 line): `axes named ... denominator 5: [] | VERDICT: FAIL-L2-X6-ON-ITS-AXIS`
  - M2 (header reverted back to the round-1 workaround): `reads 'disposition class' ...: True | VERDICT: FAIL-L2-HEADER-REVERTED`
  - M3 (`encoding="utf-8"` stripped from the script's `open()`): `encoding='utf-8' occurrences: 0 | VERDICT: FAIL-L2-RECOUNT-READS-UTF8`
  - M4 (the `PLANE_SECTIONS` scoping fix reverted, header left correctly reverted): `ledger_recount.py` itself prints
    `RECOUNT: MISMATCH 14` (68 plane rows misread as 77, RETIRE 13 -> 14, DECLARED EXCEPTION 1 -> 2, etc.) -- proves
    the section-scoping fix is load-bearing, not cosmetic.
- **Determinism:** all four criteria run 3 times on the same committed bytes (@45f5930e32); identical verdicts and
  denominators every run (`PASS-L2-X6-ON-ITS-AXIS` / `PASS-L2-RECOUNT-READS-UTF8` / `PASS-L2-HEADER-REVERTED` /
  `FAIL-L2-COUNTS-REPRODUCED`, unchanged).

## 5. ROWS

- `LGIC_CANON-W3-S2` -- BLOCKING, INERT. `check_canon_r2.py`'s `l2_recount()` cannot parse `ledger_recount.py`'s
  established, round-1-validated multi-word SECTION/TOTAL output; L2-AC4 reads FAIL by that instrument's own defect,
  not by any wrong count. Not disarmed here: the remedy (a repaired regex or a re-cut criterion) is outside CN-l-2's
  grant (`check_canon_r2.py` is a read-only fixed input) and is for 3.0.0_SA_CVO at L9 / 2.0.0_SA_COO~G's recut.

## 6. DECLARED LIMITS

- No grade on whether X6 is truly on the axis it excepts, or whether the header revert leaves the checker correctly
  scoped in every future case: that is L2-J1, at L9.
- L2-AC4 is recorded FAIL, honestly, and is not papered over by editing the fixed checker or by degrading the
  ledger's own multi-word class names to fit a `\S+` regex.
- Nothing live was touched. Nothing was written outside the order's `<paths>` and this deliverables folder.
