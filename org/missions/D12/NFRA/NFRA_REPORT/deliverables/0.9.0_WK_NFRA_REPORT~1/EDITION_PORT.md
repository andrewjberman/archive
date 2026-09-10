# EDITION_PORT.md -- porting the edition engine into the Lambda (cell RP-s-21, round 4)

**Cell:** `NFRA_REPORT.TO-RP-s-21` -- lift the LOGIC out of the round-3 specimen
`org/missions/D12/NFRA/NFRA_REPORT/deliverables/0.9.0_WK_NFRA_REPORT~1/compose_edition.py` and leave the
FACTS (`ROW_FACTS`) and the wiring (`main()`) behind. **New file:**
`infra/aws/lambda/infrastructure_monitor/edition.py`.

## WHAT MOVED

Six functions, ported ONE FOR ONE from the specimen at HEAD (`20327a663f652cde867f0962206f346b2e6d3a60`),
bodies unchanged, docstrings carried:

| function | specimen lines | port lines |
|---|---|---|
| `compute_delta` | `:334-371` | `edition.py:46-83` |
| `compute_delta_watch` | `:374-385` | `edition.py:86-97` |
| `compute_verdict` | `:388-396` | `edition.py:100-108` |
| `fmt_state` | `:399-408` | `edition.py:111-120` |
| `gen_sentence` | `:411-417` | `edition.py:123-129` |
| `render_markdown` | `:420-545` | `edition.py:132-257` |

Also moved: `RANK = {"OK": 0, "DEGRADED": 1, "BREACH": 2}` (specimen `:70`), the small module-level constant
`compute_delta()` closes over -- not a fact table, three entries, referenced by name inside the ported
logic, so it travels with the function that needs it (AC3's `BIG_UPPERCASE_DATA_LITERALS` threshold is
`>400` chars of `ast.dump`; `RANK` is nowhere near it and is not a "frozen fact", it is part of the rule).

The port was built by slicing the exact named line ranges out of the specimen file programmatically
(`.scratch/build_port.py`, a scratch script, not committed) rather than re-typing them, to remove
transcription risk from the criterion the cell calls out as *the* cell (AC2).

## WHAT DID NOT MOVE, AND WHY

- **`ROW_FACTS`** -- the hard-coded, hand-transcribed round-1 fact table. Cell instruction: "`ROW_FACTS`
  DOES NOT TRAVEL." Not present in `edition.py` anywhere (AC3 confirms: 0 big uppercase data literals).
- **`main()`** -- the wiring that read `ROW_FACTS`, ran the delta-annotation loop over it, called
  `compute_verdict`/`render_markdown` and wrote `EDITION_SPECIMEN.md` to disk. Cell instruction: "`main()`
  DOES NOT TRAVEL." Not present in `edition.py`.
- **The `import datetime`** the specimen used only inside `main()` to stamp `vintage` -- unneeded here
  since `render_markdown(rows, needs_andrew, breach_rows, worse_rows, vintage)` already takes `vintage`
  as a caller-supplied argument in the ported signature.
- **The delta-attach loop itself** (specimen `main()` `:549-555`) -- see CALLER CONTRACT below. It is
  `main()`'s content and does not travel into `edition.py`; per issuer ruling `NFRA_REPORT-Z-S20`, it
  belongs to the CALLER (`RP-s-23`'s wiring cell, now amended to carry it), not to this pure-function
  module.
- **No AWS call, no HTTP call, no file read, no new dependency** -- confirmed by AC5 (0 non-stdlib
  imports) and by inspection: none of the six ported functions performs I/O; they are pure functions over
  the arguments their caller supplies, exactly as the cell requires.

## THE ROW SHAPE

Unchanged. `render_markdown`/`fmt_state`/`gen_sentence`/`compute_verdict` accept exactly the row dicts
`ROW_FACTS` entries already are (`property`, `attribution`, `family`, `prev`, `curr`, `citation`,
`evidence`, optional `illustrative`) plus the two fields `main()`'s excluded loop used to attach
(`delta`, `rule_note` -- see CALLER CONTRACT below). Nothing in this cell's diff touches that shape; the
cell's own bound forbids it, and this worker did not.

## CALLER CONTRACT (read this before wiring RP-s-23 or reusing RP-s-22's mapper)

`compute_verdict()` and `render_markdown()` both read `r["delta"]` off every row. In the specimen that key
was populated ONLY by `main()`'s own loop (specimen `:549-555`), run once, before either function was ever
called:

```python
for r in rows:
    if r["family"] == "watch":
        delta, note = compute_delta_watch(r["prev"], r["curr"])
    else:
        delta, note = compute_delta(r["prev"], r["curr"])
    r["delta"] = delta
    r["rule_note"] = "(%s)" % note
```

That loop is `main()`'s content, so it does not travel into `edition.py`. **The caller is responsible for
running the equivalent of it and attaching `delta` (and, optionally, `rule_note`) to every row dict BEFORE
calling `compute_verdict()` or `render_markdown()`.** A row handed to either function without a `delta`
key already set raises `KeyError: 'delta'`. Per issuer ruling `NFRA_REPORT-Z-S20`, that caller is
`RP-s-23`'s wiring cell (amended in the same ruling to carry the loop); `edition.py` itself stays pure
functions over arguments and this worker's scope/BOUNDS/write-surface do not change.

## SURPRISE FILED, THEN ADJUDICATED -- NFRA_REPORT-Z-W1-S7 / NFRA_REPORT-Z-S20

The task order's ORIGINAL `AC2` ("THE CELL") and `AC4` called `compute_verdict()`/`render_markdown()`
directly on `spec.ROW_FACTS` -- which never carries `delta` -- with no equivalent of `main()`'s loop run
first. Both raised `KeyError: 'delta'` on their first call. This worker reproduced the identical error
against the **unmodified specimen module itself** (`spec.compute_verdict(spec.ROW_FACTS)`, no port
involved), proving the two criteria were unsatisfiable by any implementation honouring the cell's own
"`main()` does NOT travel" bound -- not a port-fidelity gap. Filed as surprise row `NFRA_REPORT-Z-W1-S7`.

The issuer (`2.0.0_SA_COO~ZZ`) adjudicated at `NFRA_REPORT-Z-S20` (commit `95b7d4ecd2`): row **UPHELD IN
FULL**, defect the issuer's own (the RED ARM it printed for AC2 was reasoned, never run). The issuer
recut AC2 and AC4 to attach `delta` via the port's own `compute_delta`/`compute_delta_watch`, over an
independent `copy.deepcopy` per side, before rendering -- and directed this worker to amend its own copy
of the task order (`<paths>`-authorized) citing the ruling, then re-run. Done; see PROOF OF SPEC below.
The recut is strictly stronger than the original: the original AC2 never called `compute_delta` or
`compute_delta_watch` at all, so two of the six ported functions were unexercised by the criterion that
names itself THE CELL. The recut exercises all six.

## PROOF OF SPEC -- MEASURED, NOT ASSUMED

All six invocations were run verbatim from the (AC2/AC4: issuer-amended, `NFRA_REPORT-Z-S20`)
`<proof_of_spec>`, substituting this worktree (`C:/tmp/wk-report-4-1`) for the main checkout path the
invocations name (the task order's own instruction: the files under test are this worker's and
uncommitted).

| id | result | what decided it |
|---|---|---|
| AC1 | **PASS** | `DEFINED=6 of 6 MISSING=[]` |
| AC2 ("THE CELL", recut per `Z-S20`) | **PASS** | `SPEC_TABLE_LINES=35 PORT_TABLE_LINES=35 IDENTICAL=True` |
| AC3 | **PASS** | `MODULE_LEVEL_DEFS=8 BIG_UPPERCASE_DATA_LITERALS=0 NAMES=[]` |
| AC4 (recut per `Z-S20`) | **PASS** | `BASE_ROWS=26 MUT_ROWS=1 OUTPUTS_DIFFER=True` |
| AC5 | **PASS** | `IMPORTS=0 NON_STDLIB=0 NAMES=[]` |
| AC6 | **PASS** | `LINES=258 NON_ASCII_LINES=0 FIRST=[]` |

All six criteria PASS. `<status>` on this task order is flipped to `complete`.

## MUTANT AND DETERMINISM CONTROLS

- **Mutant:** the port file was temporarily moved aside (`mv edition.py .scratch/edition.py.bak`,
  restored immediately after) to reproduce the task order's own RED ARM independently rather than trust
  its printed numbers. With the file absent, `open()`/`ast.parse()` raised `FileNotFoundError` on every
  criterion, matching the RED ARM's "file absent" shape. File restored and re-verified (`py_compile` +
  `ruff check --target-version py39`, both clean) before continuing.
- **Determinism:** every one of the six criteria (AC2/AC4 in their recut form) was run twice in
  succession against the final file bytes -- identical output both times, including the two originally
  KeyError-ing criteria now PASS-ing identically twice.
