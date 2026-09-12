# `battery_ib_rt_11.py` -- RT11-AC1, FIVE ARMS, 0 CHECKS FAILED

```
timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_11.py
rc 0 | checks failed: 0 | ARMS: 5 of 5 | IBRT11-INTAKE-CONTROLLED
```

Full output: `IB-rt-11_RT11-AC1_battery_output.txt`. Mutant control:
`IB-rt-11_mutant_control.py` / `IB-rt-11_mutant_control_output.json` -- **FIRED-AS-EXPECTED**,
determinism **STABLE**.

---

## The cell's law, and how each arm is built to it

**QUARANTINE OVER RELABELING.** A value whose currency cannot be ESTABLISHED from the document
is quarantined, never relabeled to the expected one, and a quarantine is a reportable outcome
rather than a failure to handle the case.

### WHICH COORDINATE EACH CHECK READS -- the question, answered first

The adjacent cell measured what happens when nobody asks it (row `IRPT_BCKEND-W4-S28`): round 1
dated **15 of 61** overview rows and **12 of 108** multi-comparison rows from a neighbouring
block, and **every one passed all three certification legs**, because a date sits at none of the
coordinates those legs inspect. A currency is the same shape of claim, so the coordinates are
DECLARED AS DATA in `settings.json -> intake_controls` where they can be reviewed:

| coordinate | read? | can it ESTABLISH? |
|---|---|---|
| `DECLARED_CURRENCY_COLUMN` | yes | yes -- a whole-token ISO-4217 code on the same row |
| `VALUE_COLUMN_HEADER` | yes | yes -- an ISO token (`Market Value (CAD)`), never the header's vocabulary |
| `XLSX_NUMBER_FORMAT` | yes | yes -- an ISO token in the numFmt, via `xl/styles.xml` `cellXfs` |
| `VALUE_CELL_TEXT` | yes | **never** -- a symbol is ambiguous by construction |
| workbook/sheet note, header, footer, cover sheet | **no** | declared blind spot |
| CSV sidecar or filename | **no** | declared blind spot -- a filename is not a declaration |

**The number-format coordinate is the one round 1 could not see and the one that matters most.**
An Excel user who sets a cell to Currency never types a symbol into the value: the symbol lives
in the FORMAT and the stored value is bare. And the corollary that makes the policy real rather
than decorative: **`[$$-409]` is a LOCALE, not a currency declaration.** Every human looking at
that workbook sees `$` and would say USD. The document has declared nothing, so it is
quarantined.

### (a) FOUR OF FOUR -- 4 of 4 controls fired, each with its source cell

```
holdings_non_usd.csv          UNSUPPORTED_CURRENCY  source=holdings_non_usd.csv!C2          quarantined=True
holdings_subtotals.csv        SUBTOTAL_ROW_PRESENT  source=holdings_subtotals.csv!C5        quarantined=True
holdings_multi_sheet.xlsx     MULTI_SHEET_WORKBOOK  source=Holdings!(workbook)              quarantined=True
holdings_ambiguous_total.csv  AMBIGUOUS_TOTAL       source=holdings_ambiguous_total.csv!C5  quarantined=True

holdings_non_usd.csv!C2..C4   state=ESTABLISHED currency=CAD  read: DECLARED_CURRENCY_COLUMN, VALUE_COLUMN_HEADER, VALUE_CELL_TEXT
Holdings!C2..C4               state=AMBIGUOUS   currency=-    read: VALUE_COLUMN_HEADER, XLSX_NUMBER_FORMAT
```

* The CAD values are **KEPT** and carry **no unit** -- quarantine, not deletion and not
  relabeling. An unsupported position is never silently removed.
* The ambiguous total is **not resolved**: `stated=None`, 2 candidates, and no reconciliation is
  performed. Picking one of two readings is the defect; picking none and saying so is correct.
* The CAD **stated total** is also quarantined, and that is deliberate: comparing it with a USD
  sum of zero would report a portfolio-sized `TOTAL_MISMATCH` that is arithmetically true and
  says nothing -- the document and the parser are not disagreeing about a number, they are
  talking about different currencies.
* **The denominator is the declared control table**, not the findings that happened to appear.

> **SPECIMEN PROVENANCE, PRINTED ON THE ARM (B6).** Every specimen is SYNTHETIC and ADVERSARIAL
> BY CONSTRUCTION -- written to hit a named control. No real advisor-supplied workbook exists in
> this repository and none was manufactured to look like one. **This is a result about the
> controls, not a certification against real client input.**

### (b) THE DIFFERENCE CONTROL -- and the leg that passes the defect

```
CORRECT     ROW-COUNT balances=True  | CURRENCY consistent=True  violations=0
RELABELING  ROW-COUNT balances=True  | CURRENCY consistent=False violations=3
            units claimed: [USD,USD,USD] | computed total: {'USD': 210000.0}

SECOND INSTANCE, subtotal-as-holding:
CORRECT  holdings=4 computed={'USD': 700000.0}  stated=700000.0 matches=True  ROW-COUNT balances=True
DEFECT   holdings=6 computed={'USD': 1350000.0} stated=700000.0 matches=False ROW-COUNT balances=True
```

**`ROW-COUNT balances=True` in BOTH builds of BOTH defects.** That is W4-S28's lesson made
mechanical: every count is right when a CAD column is called USD, so a certification that reads
only counts passes it every time. `reconcile()` therefore has a SECOND leg that reads the
coordinate -- and the correct and defect builds are the same specimen, the same code path, ONE
FLAG apart, so the difference is the mechanism and not two different files.

### (c) PROVENANCE -- who / when / from-what, and a re-parse that cannot overwrite it

```
r+1 correction_provenance[0]:
  {"applied_on_revision": 1, "approved_at": "2026-09-12T01:45Z", "approved_by": "analyst:alyssa",
   "finding_code": "SHARE_CLASS_SUBSTITUTION_PROPOSED", "from_value": "VTSAX",
   "holdings_changed": 1, "source_cell": "holdings_share_class.csv!A2", "to_value": "VTI"}

REVISION 0 UNTOUCHED: a605b90ec31a8d29 == a605b90ec31a8d29
NEGATIVE CONTROL:     a second write to revision 0 is REFUSED
RE-PARSE:             r+2 carries 1 correction, 1 re-applied, identifier VTI present
DIFFERENCE CONTROL:   the naive re-parse loses it -- 0 corrections on r+3, identifier back to VTSAX
```

* **`approved_at` is REQUIRED**, not optional, and validated as an ISO-8601 UTC instant. An
  optional provenance field drifts to unpopulated, and a WHEN that cannot be ordered against the
  next correction is not provenance.
* **The contract's `corrections` item keeps exactly its four keys.** It is
  `additionalProperties: false` and `_contracts/` is not this order's to edit, so the WHEN
  travels in a sibling `correction_provenance` array on the revision. **Row
  `IRPT_BCKEND-W3-S35`** carries that a consumer validating `AnalysisRequest` never sees it --
  the sibling array is the honest placement available to this order, not the right long-term
  shape.
* The immutability result is paired with a negative control **because a hash that never moved
  since nothing tried to move it proves nothing.**
* `reparse_revision()` is new. A parser knows nothing about a human's decision; re-run it after
  a correction and its fresh view is the advisor's ORIGINAL. Writing that over the top erases
  the human's work with no artifact anywhere that disagrees.

### (d) ROUND 1 STILL HOLDS -- three instruments, none of them a stored hash

```
5 of 5 round-1 specimens parse byte-identically  (pinned parser at 72db64c153 vs the worktree, both in fresh interpreters)
POSITIVE CONTROL: on a NEW specimen the two parsers DISAGREE (ffd46fc90fde vs e26d554bbccc)
round-1 battery rc=0  ARMS: 6 of 6  token printed=True
intake unit tests: Ran 15 tests -- OK
```

**Both sides are re-derived every run.** A hardcoded expected digest would have been a claim
about a past run; the pinned parser is extracted from git and executed. The positive control is
what makes the 5-of-5 mean agreement rather than a comparator that cannot see a difference.

This constrained the design: the currency evidence is deliberately **not** in `row_context`,
because `row_context` is inside `to_json()` -- the round-1 contract surface. It lives in
`money_rows`, has its own `currency_evidence_digest()`, is carried into the revision's
provenance and is printed by the battery. Not hidden; just not in the contract's serialization,
where it does not belong.

### (e) WHERE THE CHECK RUNS vs WHERE THE VALUE IS CONSUMED

```
DENOMINATOR: 214 functions in lambda-source-map.json | 0 ship parse.py | 1 ships settings.json
flat /var/task run, fresh interpreter, -I, repo stripped from sys.path: 4 of 4 specimens SAME
NEGATIVE ARM, settings.json absent: 4 of 4 REFUSED
specimens byte-reproducible from their committed generator: git reports no change
FIXTURE_MANIFEST hashes re-derived from disk: 11 of 11
```

**The honest answer is printed, not implied: these controls have NO runtime yet.** `parse.py` is
packaged by 0 of 214 functions, so there is no environment in which the value is consumed, and
the arm does the closest available thing rather than claiming a deployed check (row
`IRPT_BCKEND-W3-S36`).

**The negative arm is the one that matters.** `load_intake_controls` does NOT default: with the
policy file absent the parser REFUSES by name, because a built-in "USD is supported" fallback
would relabel a non-USD value precisely when the policy failed to ship -- the one condition
under which nobody is watching. That is the runtime-only failure mode the issuer's note names,
made visible in the layout where it would happen.

---

## Mutant control -- FIRED-AS-EXPECTED

| mutant | against | baseline | mutated |
|---|---|---|---|
| M1 read a `$` as USD | "never infer a currency from a symbol" | states `[AMBIGUOUS]`, no unit claimed | states `[ESTABLISHED]`, units `[USD]`, **the `AMBIGUOUS_CURRENCY` finding disappears entirely** |
| M2 a subtotal is a holding | "a subtotal is never summed" | computed `700,000` == stated | computed `1,350,000`, and **the row count still balances** |

Determinism: the same bytes parse to `e26d554bbccc1552` twice in-process and again in a fresh
interpreter.

## What changed in the tree

| path | what |
|---|---|
| `intake/settings.json` | `intake_controls`: supported set, the three establishing coordinates, the one that never establishes, the two declared blind spots, the ambiguous-symbol table, and an ISO recogniser that fails closed. A SIBLING key, so `settings.settings`'s seven members (read by name in `irpt-ycharts-generate`) are untouched. |
| `intake/parse.py` | the coordinate readers, `determine_currency` (which picks nothing), the xlsx `numFmt` reader, six new finding codes, subtotal detection, all-candidate total collection, the currency leg of `reconcile()`, and three battery-only defect flags. |
| `intake/corrections.py` | `approved_at` required and validated; `correction_provenance`; `reparse_revision()`. |
| `intake/fixtures/holdings/` | four adversarial specimens + a deterministic generator + a re-derived manifest. |
| `intake/tests/test_parse.py`, round-1 battery and mutant control | `approved_at` added to the POSITIVE approvals only; the two negative cases (empty `approved_by`) are untouched and still assert a refusal. |

**No deploy, no Terraform root, no AWS write.** Rows filed: `W3-S34` (settings.json is a build
input of a function another cell deployed 20 minutes earlier -- INERT, the `settings` subtree is
byte-identical), `W3-S35` (the contract cannot carry the WHEN), `W3-S36` (0 of 214 functions
ship the parser).
