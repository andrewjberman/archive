# `battery_ib_s_10.result.md` -- S10-AC1, seven arms, 7 of 7

**TO:** `IRPT_BCKEND.TO-IB-s-10` | **cell:** `IB-s-10` (PRD cell B10) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-1-3` | **worktree:** `/c/tmp/wk-irpt-1-3` | **base:** `7799dcfb10`

**Invocation (the one the task order names):**
```
timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_10.py
```
**rc 0. Last line: `IBS10-EXTRACTION-CERTIFIED`. Full verbatim output (166 lines):
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-s-10_S10-AC1_battery_output.txt`.**

Five lettered arms `(a)`-`(e)` from the face, `(amend)` from the IB-s-3 drain, and `(v0.11)` from
the L4 hand-off release. **Seven arms, `7 of 7`.**

---

## What this cell actually had to decide

The PRD asks for "text/table extraction certified with units, dates, page/coordinates ... no
number inferred from a visual guess". Pulling text out of a PDF is the easy half. The whole
difficulty is **refusing to emit a number the document does not say**, and almost every design
choice below is a refusal:

| refusal | what would happen without it |
|---|---|
| a chart region yields a representation, never a value | a number read off a picture |
| `--` is `MISSING_ON_PAGE`, never `0` | `0.00%` and "no data" become the same claim to a client |
| a `(cid:45)` token is not a digit | a subset-font failure silently becomes a number |
| a `list`/`table` unit has no scalar | one member of a list is served as the whole field |
| a row that IS a "Data as of:" line cannot supply a value | the day of the month becomes a measurement |
| a segment that is not id-shaped never reaches an S3 key | a client name lands in a durable key |

Four of those six were added **because something actually went wrong on a real specimen**, not
because they seemed prudent. The measurements are in the arms below.

---

## The arms

### (a) THREE VARIANTS EXTRACTED -- typed sections with units, dates and coordinates

**Section routing, by SUBTRACTION over the census's own denominator:**
`33 total - 10 CHART_ONLY - 6 DISCLOSURE = 17 TYPED`. Every one of the 33 census sections lands in
exactly one class and the three counts are asserted to re-add to 33. The routing is decided by
**the data's own shape**, not by preference: a glossary row is `term`/`definition` and carries no
unit at all, so it cannot be a typed section; a section with zero field rows has nothing to type.

| variant | located | units | page+bbox | dated | unlocated |
|---|---|---|---|---|---|
| overview | 24 | 24 of 24 | 24 of 24 | 8 | 34 (`MISSING_ON_PAGE` 14, `UNLOCATED_ON_PAGE` 20) |
| comparison | 47 | 47 of 47 | 47 of 47 | 15 | 47 (27 / 20) |
| multicomp | 70 | 70 of 70 | 70 of 70 | 22 | 60 (40 / 20) |

**Units and coordinates are `N of N` on every variant** -- not a single value is emitted without
both, which is the arm's substance.

**One row per (field, entity column),** with the column index in the `section_id`, because
`AnalysisReport.sections` rows are `additionalProperties: false` and have no entity field. Column
indices per variant: `[0]`, `[0, 1]`, `[0, 1, 2]` -- exactly the specimen's declared column count.

**An over-strong predicate of mine, caught by this battery failing.** The first cut asserted exact
`1:2:3` scaling (24 / 48 / 72). The graded run came back `24 / 47 / 70` and `arm (a): FAIL`, and
the token was withheld. The code was right and the predicate was wrong: **a field absent for one
entity and present for another yields a different number of located rows per column**, so exact
scaling was never a property of the data -- it was a property of an imagined dataset in which
every entity has every value. The predicate is now the one that holds and matters (column indices
match the declared column count; row counts rise monotonically), and the absences are carried as
`MISSING_ON_PAGE` rather than papered over.

### (b) CERTIFIED -- every number ties to the PDF text at its own coordinates

`certify.py` is a separate module that is handed **only the emitted rows and the original PDF
bytes**. It re-opens the document, crops to the recorded bbox and reads what is printed there. It
is given no access to the extractor's intermediate state, because a checker that re-derives the
answer it is grading is a tautology.

| leg | check |
|---|---|
| **L1** | the crop at `bbox` renders this value |
| **L2** | the field's own label is on the value's row, or directly above it |
| **L3** | the row carries the unit the census declares |

`24 of 24`, `47 of 47`, `70 of 70` CERTIFIED on the synthetic specimens; `{"CERTIFIED": N}` with
no other verdict present. The verdict vocabulary carries `NOT_EVALUATED` so a row that was never
checked can never be scored as a pass, and `certification_status()` claims `CERTIFIED` only when
`checked > 0` -- an empty input set returning a vacuous pass is exactly how a gate reads clean
while measuring nothing.

**L2 is the leg that is easy to leave out and it is the one that matters most.** L1 alone
certifies a mis-located value perfectly, because the number really is printed at those
coordinates; only a label tie says the number belongs to *this field*. The neighbourhood is
defined by the **document's structure** -- the value's own text row, plus a shallow band above it
for the stacked layout -- and not by a fixed box. A fixed box was tried first and failed 30 of 34
correctly-located rows, because the label-to-value gap is 260pt in the synthetic specimens and
~60pt in the measured vendor tables; a constant sized to sit between two real layouts is guessing.

### (c) THE DIFFERENCE CONTROL -- one number changed after extraction must FAIL

| variant | field | page | before -> after | verdict |
|---|---|---|---|---|
| overview | Advisory Fee | 3 | 0.3 -> 1.3 | `VALUE_NOT_AT_COORDINATES` |
| comparison | Advisory Fee | 3 | 0.3 -> 1.3 | `VALUE_NOT_AT_COORDINATES` |
| multicomp | Advisory Fee | 3 | 0.3 -> 1.3 | `VALUE_NOT_AT_COORDINATES` |

The refusal **names the field and the coordinates**, verbatim from the run:

```
page 3 at bbox [300.0, 114.86, 325.51, 123.86] renders '0.30%'; the row claims 1.3
(accepted renderings ['$1.3', '$1.30', '1.3', '1.3%', '1.30', '1.30%'])
```

Values are compared as **text**, not as floats: a float comparison would certify `0.07` against a
page printing `0.070000001`, while a reader of the PDF -- and any later dispute -- is about the
rendering.

**A second control, on the leg L1 cannot reach.** A value is left at its own correct coordinates
and attached to a *neighbour's* label. All three variants: `LABEL_NOT_IN_NEIGHBOURHOOD`. Without
L2 this passes silently, which is the whole reason L2 exists.

### (d) NO VISUAL GUESS -- a chart-only region yields a representation, never a value

`0 numeric value(s) emitted across 10 chart-only region(s)` on every variant. The ten regions are
the census's **own zero-field sections**, so the set is read off the data rather than chosen by
me. Each emits `value: null`, `units: "chart"`, a page and a bbox, with the identification in the
`section_id` and the human-readable representation on a private key:

```
S07.chart.expanded_region_exposure   value=None units=chart p4
  identified source chart: Expanded Region Exposure, page 4. NO NUMERIC VALUE IS EMITTED ...
```

`certify.py` grades a chart row **first** and fails it `CHART_REGION_EMITTED_A_VALUE` if one ever
carries a number.

### (e) SCHEMA-VALID AND LABELLED

`AnalysisReport.sections` validated `True` on all three variants (20 / 30 / 40 rows). Label census
`N of N rows carry 'synthetic'` with `other_labels_present: []` -- **the two marker strings are
never mixed**, and that is censused rather than asserted.

Two contract frictions, both resolved without inventing anything:

1. **The chart row's identity had to move into `section_id`.** The obvious shape --
   `title` + `representation` + `emitted_values` -- is refused by
   `additionalProperties: false`. So the section_id names the chart, `section_type` declares the
   row kind, and the prose rides private keys and the sidecar.
2. **`as_of_date` is REQUIRED and the documents do not always state one** -- row
   `IRPT_BCKEND-W3-S11`. `16 / 32 / 48` synthetic rows and `0 / 34 / 51` vendor rows are **held
   out and counted** rather than given a date the document does not say. The contract has no field
   in which a report-level fallback could be *declared* as a fallback, so a fabricated date would
   be indistinguishable, to every downstream consumer, from a real one.

**Fixture manifest re-derived from disk: `3 of 3` rows match, 3 PDFs on disk, 0 unlisted, census
sha matches `True`.** This is the IB-s-9 lesson (row `W3-S9`) applied *by default* rather than
after making the same mistake twice. **Generator determinism: `3 of 3` variants byte-identical
across two runs.** PyMuPDF mints a random `/ID` per run -- measured as exactly 56 differing bytes
in a 52,935-byte file, all inside the trailer -- so it is replaced by one derived from the
content, at the same length so no byte offset moves.

### (v0.11) THE THREE RETAINED VENDOR PDFs -- real YCharts output on synthetic holdings

**An Opal S3 read, never a vendor call.** Verified **before** use, `3 of 3`:

| variant | bytes | sha256 | pages | declared |
|---|---|---|---|---|
| overview | 573,677 | `abab2ffe8411a29b` | 23 | 23 |
| comparison | 820,984 | `f01cbd48a5771cb5` | 31 | 31 |
| multicomp | 854,115 | `0a67ecf76732832e` | 35 | 35 |

Page count is checked as well as sha256 -- a second, independent leg the amendment did not ask
for. A mismatch on either is a STOP.

| variant | located | certified | units | page+bbox | dated | uncensused | schema |
|---|---|---|---|---|---|---|---|
| overview | 61 | **61 of 61** | 61 of 61 | 61 of 61 | 61 | 188 | valid, 71 rows |
| comparison | 81 | **81 of 81** | 81 of 81 | 81 of 81 | 47 | 249 | valid, 57 rows |
| multicomp | 108 | **108 of 108** | 108 of 108 | 108 of 108 | 57 | 140 | valid, 67 rows |

The difference control runs on all three and fires on all three. Chart census `0` and label census
`N of N carry 'vendor_synthetic_holdings'` on all three.

**The vendor specimens state their own dates.** Every dated vendor row is `PAGE_STATED` -- the
real documents carry a per-section "Data as of:" line, which is a stronger claim than the census's
page-level hint and is preferred over it by the extractor's date priority (`PAGE_STATED` >
`CENSUS_STATED` > `NOT_STATED`, with the claim recorded so the difference is auditable).

**The uncensused list is listed, never invented into fields.** 188 / 249 / 140 label-number pairs
the documents carry that this estate's field census does not name. They are a discovery *about the
specimen*, reported as such, and none is added to `AnalysisReport.sections`.

### (amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE

**This cell ships no route handler** -- `extract.py` and `certify.py` are libraries that take
bytes and return rows. So `unguarded_routes()` reads `0 of 0` and **the census is declared
VACUOUS**, carried instead by the two controls: an unguarded handler wired to a route censuses
`1 of 1`; the same handler wrapped by `guard()` censuses `0 of 1`. The censor is proven, not an
empty set.

**The one firm-scoped act** is where `sections/report.json` lands:
`firms/49financial/generations/2332257/attempts/0/sections/report.json`. A non-reconciling binding
is refused `FIRM_BINDING` with the opaque id **not** echoed -- it is not served an empty result,
which a caller cannot tell apart from a revocation.

**`_keys` silence:** `code=KEY_REFUSED`, 1 audit entry, 1123-byte envelope,
**`OCCURRENCES OF THE REFUSED VALUE: 0`** over the whole envelope *including this cell's own
artifact refusal text*.

**And the gap that made that guard necessary, MEASURED rather than asserted** -- row
`IRPT_BCKEND-W3-S12`:

```
_keys.s3_evidence_key(client display name  ) accepted=True  firms/49financial/generations/<VALUE>/attempts/0/sections/report.json
_keys.s3_evidence_key(e-mail address       ) accepted=True  firms/49financial/generations/<VALUE>/attempts/0/sections/report.json
```

against its own docstring -- *"Each is validated by shape, so a client name cannot become a
path"* -- while `cache_key` in the same module refuses both. `_keys` is not this cell's to edit,
so this cell refuses what it would otherwise pass on, and **arm (amend) fails if the gap ever
stops being real**, so the guard cannot quietly become decorative.

---

## Controls

**MUTANTS -- four, all FIRED** (`IB-s-10_mutant_control.py`, `mutants_fired_as_expected: true`):

| | mutation | baseline | mutant |
|---|---|---|---|
| **M1** | certification stops checking the value | `VALUE_NOT_AT_COORDINATES` | `CERTIFIED` -- a changed number passes |
| **M2** | certification stops checking the label | `LABEL_NOT_IN_NEIGHBOURHOOD` | `CERTIFIED` -- a transposed column passes |
| **M3** | a chart-only region is given a number | 0 emitted, all certified | 1 emitted, `CHART_REGION_EMITTED_A_VALUE` |
| **M4** | the date-line exclusion is removed | 47 located, **0** from a date line | 64 located, **17** from a date line, 63 of them certified |

**M4 is the one worth reading twice.** It is not hypothetical: before that rule existed the
extractor located 42 values per variant instead of 26, and the extra sixteen all **CERTIFIED** --
because a date line's digits sit exactly where the extractor said they did. A control that only
mutated the *certifier* would never have found it.

**Two control defects found and fixed in the controls themselves, recorded because they are the
more instructive half:**

1. **The M4 probe shared a dependency with what it graded.** It called
   `extract._date_line_tops()` at probe time -- the exact function M4 patches out -- so it went
   blind in the one run it existed to measure and reported a clean `0` on a mutant that had just
   harvested 17 extra values. The reference set is now captured from the unmutated module at
   import time.
2. **The first M4 probe detected "date fragments" by token shape** (ends in a comma) and returned
   **4 false positives on the baseline**. Those turned out to be fragments of a `list` value
   rendered across a column boundary -- a *second, different* real defect (now `NON_SCALAR_UNITS`)
   hiding behind noise attributed to the first. The probe is now geometric: it compares the row's
   own top against the date-line tops on its page.

**DETERMINISM:** `lines 166 166 | identical: True | differing: 0`, and the **graded run is
byte-identical to both** (`graded identical to run A: True`), so the recorded output is not a
third, luckier run. All three printed `IBS10-EXTRACTION-CERTIFIED` at rc 0.

---

## What this arm set does NOT show

Stated here rather than left for a reader to find; the full version is the `S10-AC2` judgment
record, which `3.0.0_SA_CVO` grades at L9 and which carries no verdict of mine.

1. **No representative real-client specimen exists.** The vendor PDFs are real YCharts output on
   **synthetic holdings** (SPY $60,000 + AGG $40,000, two positions). A real client portfolio has
   dozens of positions, long names, footnote markers and pages this extractor has never seen.
   That gap is the PRD's own, named on FWD-4 and FWD-8, and it is not closed here.
2. **Certification proves the tie, not the arithmetic.** It says Opal's record matches the
   vendor's document at a named place. It says nothing about whether the vendor's number is right.
3. **`UNLOCATED_ON_PAGE` is 20 on every synthetic variant and is not investigated field by
   field.** Those are census fields the specimen does not render as a locatable label/value pair.
   They are counted and carried, not explained.
4. **The extractor is not deployed.** It rides IB-s-9's Lambda package at that package's next
   build, and pdfplumber is not in the python3.12 runtime -- so a deployed caller today would get
   `extraction_available=false` with the reason named. The layer question is IB-s-13's.
