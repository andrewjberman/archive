# NFRA_PYFIELD TO-1 — `PyFieldRecognizer` coverage report

**`0.8.0_AE_CloudComp` · 2026-08-07 · TO `NFRA_PYFIELD.TO-1.pyfieldrecognizer` @f6418f78e7**
Module: `org/modules/graph/comp_recognizers_pyfield.py` · Battery:
`org/modules/graph/tests/test_comp_recognizers_pyfield.py` (43/43 PASS, incl. 6 mutant controls)

---

## §0 — THE HEADLINE, STATED THE ONLY WAY IT CAN HONESTLY BE STATED

> **resolver=`pyfield-flowlocal/v2` · marker_set=`STRICT_DERIVED`@pandas-2.3.3 (n=227) ·
> vintage 2026-08-07T183904Z · SWEPT `data/inf/scripts/gold` + `data/assets/scripts/gold` ·
> UNSWEPT `bd`, `cot`, `mdpf`, the assets monolith, and EVERY silver tree:
> the recognizer resolved 2,295 of 4,413 attemptable name-based string-literal Subscript NODES
> (52.0%), by axis binding=1,555 / usage=478 / iterrows=262, leaving 2,118 unresolved and 491
> UNATTEMPTABLE by construction, and emitted 408 field-grain `FLOWS_TO` edges across 124 files with
> 0 parse failures.**

⛔ **The sentence "the recognizer resolves N% of columns" does not appear in this document and must
not be quoted from it.** It is not true or false — it is underspecified, and §1 measures exactly how
much room that leaves.

**GRAIN: AST Subscript NODES, never lines.** A `comp-find` count is LINES (4,336 on this corpus vs
4,897 nodes) — a grain difference, not a disagreement, and never a denominator here.

---

## §1 — CRITERION 1: BOTH PINS MOVE THE ANSWER. MEASURED, NOT ARGUED.

One identical corpus, one identical run, both pins swept. **Coverage ranges 20.3% → 52.1% — a 2.6x
spread — without a single line of the corpus changing.**

| resolver | marker set | resolved | of 4,413 | binding | usage | iterrows |
|---|---|---|---|---|---|---|
| v1 | MINIMAL | 895 | **20.3%** | 434 | 199 | 262 |
| v1 | STRICT_DERIVED | 1,600 | 36.3% | 434 | 904 | 262 |
| v1 | WIDE | 1,605 | 36.4% | 434 | 909 | 262 |
| v2 | MINIMAL | 1,898 | 43.0% | 1,555 | 81 | 262 |
| **v2** | **STRICT_DERIVED** | **2,295** | **52.0%** | 1,555 | 478 | 262 |
| v2 | WIDE | 2,298 | **52.1%** | 1,555 | 481 | 262 |

Both pins are re-derivable at any time: `python org/modules/graph/comp_recognizers_pyfield.py
data/inf/scripts/gold data/assets/scripts/gold --resolver <v1|v2> --marker-set <SET>`.

**`format_coverage()` RAISES rather than render a figure without a `Pins`.** Criterion 1 is enforced
by construction, not by an author remembering it. The mutant control for this is in the battery.

### The resolver delta, and a finding that nearly hid it

Binding-side moves **434 → 1,555 (3.6x)** from v1 to v2 — reproducing the TO's 9.9% → 35.3% exactly
on the same population. **But total resolution is a bad instrument for that delta.** On the test
fixture v1 and v2 both resolved 13 sites: v2 proved the annotated param by *binding*, and v1 fell
through and proved the *same site* by the *usage* marker. **A resolver delta scored on the total
would have read "v2 adds nothing."** The axes overlap — exactly the independence the PRD measured
(only 34.6% of binding hits are also usage hits) — so the delta must be read per axis. The battery
now asserts this explicitly so the trap cannot silently return.

---

## §2 — CRITERION 3: ZERO UNRESOLVED WOULD BE A FAILURE. IT IS NOT ZERO.

| channel | count | meaning |
|---|---|---|
| attemptable (denominator) | **4,413** | name-based string-literal Subscript nodes |
| resolved | 2,295 | an axis PROVED the base is a DataFrame |
| **unresolved** | **2,118** | attempted, no axis proved it — enumerated with `(locus, reason)` |
| **UNATTEMPTABLE** | **491** | `<expr>` bases — **never scored as misses** |
| total string-literal subscripts | 4,904 | 4,413 + 491 |

The **491** (`txns.groupby.()['transDate']`, `accounts.set_index.()['representative_name']`, …) are
unreachable by construction: a name-keyed mechanism structurally cannot attempt them. They live in
their **own channel**, are enumerated with reasons, and are **excluded from the denominator** — a bar
that counted them would be unpassable by construction. My independent count of 491 matches the TO's
figure exactly.

**About the 2,118 unresolved: much of it is CORRECTLY unresolved.** TO-0 established that only ~62.3%
of this population was ever a column at all; the rest are dicts, records, and API responses that were
never columns. A recognizer that never touches them is not failing.

---

## §3 — CRITERION 4: `.iterrows()`, AND THE TUPLE POSITION THAT MAKES IT WRONG

`for idx, row in df.iterrows()` yields **`(index, Series)`**. **Only element [1] is the row.**

- **Bound:** a 2-tuple target's second element. `row['col']` **IS** a column access — 262 sites.
- **NOT bound:** element [0] (`idx` is the index — `idx['x']` is not a column).
- **NOT bound:** a single-target `for r in df.iterrows()`, where `r` is the whole **tuple**.
- **NOT bound through a shadow:** a function parameter named `row` does not inherit a module-level
  iterrows row.

### Four instruments, four numbers — and this is the TO's own thesis landing on my own work

| number | instrument | verdict |
|---|---|---|
| 237 | my first recon: for-loops only | **WRONG — undercount.** It missed `ast.comprehension` iterrows entirely. |
| 257 | the TO's stated figure | a fourth instrument's read |
| 287 | flat file-wide name match | **overcount** — scope-blind |
| **262** | **the recognizer** (scope-aware, elts[1] only) | **the defensible one** |

The 287 → 262 gap is fully attributed: 25 sites where a flat name match sees an iterrows row that is
bound in a **sibling scope** the lexical walk correctly never reaches.

**What exposed the bug: a stricter rule produced a BIGGER number (262 > 237), which is backwards.**
That prompted the shadow probe, which found a real defect — a module-level iterrows row leaking into
every function taking a `row` parameter, silently mis-calling `row["Records"]` as a column.

⚠ **HONEST SCOPE OF THAT FIX, because it would be easy to sell it as a catch:** an ablation on this
corpus measured **262 with the shadow check and 262 without it — it removes ZERO false positives
here.** It is a correctness guard against a real shape this corpus does not happen to contain. My
first attribution script labelled 24 sites "shadowing"; the ablation falsified that, and those are
sibling-scope cases an upward walk never reaches either way. Recorded rather than sold.

---

## §4 — CRITERIA 2, 5, 6: SCHEMA, EXCLUSION SET, AXES

**Criterion 2 — the seven keys.** Every emitted edge carries exactly `srcField`, `dstField`, `kind`,
`rename`, `condition`, `via`, `resolution`, in the portal `{src, dst, props}` shape. Verified against
the **live portal artifact** (`tsgraph_spike/out/live_flowsto.json`, 961 edges) rather than against my
own constant — otherwise the test only proves the module agrees with itself. A key-set drift **raises**
(a hard `ValueError`, not an `assert`: `python -O` strips asserts, and a control a flag can disable is
not a control). Refs use the governed `field:` prefix → `Entity.FIELD`. All three governed EdgeKinds
are exercised; `condition` is populated on guarded flows (portal defect #3, 4.8% populated, not
inherited).

**Criterion 5 — exclusion set DERIVED, never lifted.** Marker sets are computed at runtime from the
installed pandas API (`dir(DataFrame) | dir(Series)` = **240**, pandas **2.3.3**, pinned into every
figure). `_DF_METHODS` was **not** lifted: 71 hand-drawn names against a real universe of 240 (missing
170 = 70.8%), one member (`concat`) that can never fire, unpinned. The battery asserts the derived set
is not 71 members and that `concat` is correctly absent.

**Criterion 6 — all axes from the start.** binding (1,555) · usage (478) · iterrows (262) — all three
live in the shipped default, not staged behind a follow-on.

---

## §5 — CRITERION 7: THE MUTANT CONTROLS

*A test suite that has never failed has never been tested.* Six mutations that **should** break the
emitter, each asserted to demonstrably do so:

| mutant | expected | result |
|---|---|---|
| empty constructor set + v1 | binding axis goes **DARK** | fires |
| empty marker set | usage axis goes **DARK** | fires |
| `_iterrows_base` neutered | iterrows axis goes **DARK** | fires |
| **all three** neutered | **zero edges** emitted | fires |
| props key drifted | **raises** | fires |
| `Pins` removed | `format_coverage` **refuses** | fires |

**The battery caught two real defects in its own first run** — a fixture where the usage axis could
never fire (binding always won the only marker site), and a resolver-delta assertion scored on the
wrong quantity (§1). Both are now fixed and locked.

---

## §6 — BOUNDS, and what is NOT claimed

- **SWEPT:** `data/inf/scripts/gold`, `data/assets/scripts/gold` (124 files, 0 parse failures).
  **UNSWEPT:** `bd`, `cot`, `mdpf`, the assets monolith, **and every silver tree.** Every figure above
  is scoped to the swept trees, stated in the same sentence per requirement 4.
- **408 FLOWS_TO edges emitted, NOT YET LOADED INTO THE GRAPH.** This TO builds the producer; the
  graph-load leg is not in its scope and is not claimed. The Phase-3 `comp-kuzu` census therefore
  reports the *current* graph state (field grain still 100% portal) — see the session log.
- **Corpus drift, reconciled:** I count **4,904** string-literal subscripts where the PRD says 4,896.
  CRO's own probe, re-run at my seat on today's tree, **also reports 4,904** — two independently
  written instruments agreeing, so the delta is corpus movement since the PRD's read, not an
  instrument disagreement. 491 expr-base matches the TO exactly.
- **Not type inference.** mypy/pyright/pytype/jedi are all absent (rung 5 re-confirmed); **no
  dependency was added.** Cross-file resolution is NOT claimed — this is a LEXICAL_AST-tier recognizer
  and honest-degrades under capability per LAW-1.
- **The hand-audited TO-0 sample was NOT used to tune anything.** It measures the procedure; it is not
  training data (Andrew-direct 2026-08-06, no overfitting a scorer to its own eval cases).
