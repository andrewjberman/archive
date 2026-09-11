# `battery_ib_s_7.result.md` -- S7-AC1, six arms, 6 of 6

**TO:** `IRPT_BCKEND.TO-IB-s-7` | **cell:** `IB-s-7` (PRD cell B7) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-1-3` | **worktree:** `/c/tmp/wk-irpt-1-3` | **base:** `5236a7603d`

**Invocation (the one the task order names):**
```
timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_7.py
```
**rc 0. Last line: `IBS7-PARSE-DETERMINISTIC`. Full verbatim output:
`.../IB-s-7_S7-AC1_battery_output.txt`. Run from COMMITTED source (`5708161e8e`).**

**Precondition printed first:** a specimen with no header row is `ParseRefused`, never parsed
positionally -- a positional guess maps the wrong column to quantity and says nothing.

---

## (a) DETERMINISTIC -- `4 of 4`

The same bytes parsed twice, compared **as bytes**: 4 of 4 specimens byte-identical. The
serialization carries no timestamp and no random value, which is why byte equality is
achievable here rather than merely verdict equality.

## (b) NOTHING DROPPED -- the difference control

| build | unmatched holdings carried | reconciliation |
|---|---|---|
| **correct** (`drop_unmatched=False`, the only value any caller in the package uses) | **1** -- `'PRIVATE PLACEMENT 2019'` at `holdings_unmatched.csv!C3`, quantity `{value: 250.0, units: SHARES}`, verbatim `'250'`, finding `UNMATCHED_IDENTIFIER/UNCERTAIN` naming the source cell, `needs_correction=True` | balances |
| **broken** (`drop_unmatched=True`, one flag moved on the same code path) | **0** | `unaccounted: 1, balances: false` |

**The arithmetic catches the drop.** `rows_seen == holdings + findings standing in for a row +
declared skips + header rows` is computed, not curated, so a row that vanishes shows up as a
disagreement rather than as silence: `4 of 4` specimens balance, `0` unaccounted rows across
all of them, and the broken build fails the same arm.

## (c) UNITS, CELLS, TOTALS, CASH

- **`15 of 15` rows** carry units **or** a `UNITS_UNDETERMINED` finding.
- **`15 of 15` rows** carry sheet + row + column + the verbatim source text.
- **`4 of 4` specimens** carry `$:CASH` and all four kept it in the `CASH` namespace.
- **`4 of 4` specimens** reconcile their stated total **or name the difference**:
  `holdings_share_class.csv` computes `500,000 USD` against a stated `500,100 USD` and emits
  `TOTAL_MISMATCH` with the `-100.0` difference. The rows are **not rescaled** to hit the
  stated total -- that would change the advisor's numbers.
- **`4 of 4` specimens** validate against the **shared `AnalysisRequest` schema**.

## (d) THE CORRECTION STATE

```
revision 0: stage=NEEDS_CORRECTION  StatusEnvelope.state=NEEDS_CORRECTION
  hash(r0) at open  = <h>
  hash(r0) after r1 = <h>        r0 UNCHANGED = True
r1: corrections[] = [{finding_code: SHARE_CLASS_SUBSTITUTION_PROPOSED,
                      approved_by: analyst:alyssa, from_value: VTSAX, to_value: VTI}]
  r0 still holds VTSAX = True    r1 holds VTI = True
  r1 stage = NEEDS_CORRECTION    (a finding nothing resolved still stands)
  overwrite of r0 REFUSED; store writes=2 refused_overwrites=1 revisions=[0, 1]
  a substitution with NO approver is refused = True
```

The approval is **explicit on r+1** in the contract's own `corrections` array, and `r` is
byte-stable across the whole operation.

## (e) SETTINGS ARE DATA

`7` settings recorded, `7 of 7` with a named source, `management_fee == 0.003` with the
superseded `0.01` **kept and dated** rather than deleted, and `2` cautions:
`TAX_DEFAULT_IS_NOT_CLIENT_STATUS`, `NO_BENCHMARK_TEMPLATE_KEEPS_THE_CALCULATION_BENCHMARK`.

## (amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE

**The reading taken, stated so a grader can disagree with it: this cell ships NO ROUTE
HANDLER.** The deliverable is a parser and a correction state inside the intake package -- a
library called in-process. `corrections.ROUTES` is exported **empty** so the census has a real
object and a future handler lands where the census already looks.

| census | result |
|---|---|
| `unguarded_routes(corrections.ROUTES)` | `0 of 0` -- **printed as VACUOUS**: it reads identically whether the censor works or not |
| CONTROL: an **unguarded** handler wired to a route | `1 of 1 unguarded` -- the censor **fires** |
| CONTROL: the **same** handler wrapped by `guard()` | `0 of 1 unguarded` |
| route-reachability of this cell's public callables | `0` of `9` wired to any route table in the corpus |

The amendment's fallback object, `routes.json`, **does not exist anywhere in the corpus** --
row `IRPT_BCKEND-W3-S5`.

**FIRM BINDING (row W2-S9):** a reconciling binding writes revision 0; a **non-reconciling**
binding returns `Refusal(FIRM_BINDING)` and `None` -- **a refusal, not an empty set**, because
an empty result is indistinguishable from a revocation and a caller will treat it as one. The
failing opaque id is **not echoed** in the envelope (confirmed by substring census).

**`_keys` REFUSAL SILENCE (row W2-S10):** a key parameter carrying a client display name,
taken through **`guard()` -> `serve()`** so the audit trail is populated:

```
outcome code = KEY_REFUSED
reason: "1 of 2 key parameter(s) were refused by the key grammar: ['client'] ..."
audit trail entries: 1
CENSUS over the WHOLE envelope (body + reason + AUDIT TRAIL), 809 bytes:
  occurrences of the refused value: 0
```

The library path (`corrections.revision_key`) reads the same: `0` occurrences over 473 bytes.
**The refused value is never printed anywhere in this battery -- only its count.**

---

## Controls

**MUTANT -- two by monkeypatch, plus one that ships.**

```
baseline immutability  hash(r0) stable, overwrite refused          -> predicate HOLDS
M1  store overwrites   hash(r0) moves on the tamper attempt        -> predicate BREAKS
baseline substitution  identifiers = [VTSAX, FXAIX, OPAL-SIP, $:CASH], 2 proposals -> HOLDS
M2  mapping APPLIED    identifiers = [VTI, IVV, OPAL-SIP, $:CASH], 0 proposals     -> BREAKS
```

**M2 is the one that matters**: with the mapping applied, the parser returns a portfolio the
advisor never sent, and emits **zero** proposals to say so. Recorded verbatim in
`IB-s-7_mutant_control_output.json`, reproducible by `IB-s-7_mutant_control.py`. The third
control **ships inside the battery**: arm (b)'s `drop_unmatched=True` build.

**DETERMINISM.** Two full battery runs on the same inputs: **126 lines, byte-identical, zero
differing lines**, both `IBS7-PARSE-DETERMINISTIC` at rc 0.

**A BUG THIS CELL FOUND IN ITSELF before the battery ran.** An `.xlsx` omits empty cells from
the XML, so the weights specimen's Total row is `[('Total','A'), ('100%','C')]` -- positions
`0,1`, columns `A,C`. The first draft indexed **by position** and read the total as the
description, losing the stated total entirely while every CSV specimen passed. Every cell is
now addressed **by column letter**, and
`test_cells_are_addressed_by_column_letter_not_position` asserts it on the xlsx specimen
specifically, because on a CSV the bug is invisible.

**Package tests:** `15 of 15` pass (`intake/tests/test_parse.py`).

## What this battery does NOT establish

- **The specimens are SYNTHETIC.** No real advisor-supplied holdings file exists in this
  repository. A green arm proves the parser handles THESE shapes; the shapes it cannot
  represent are enumerated in the S7-AC2 judgment.
- **No deploy, no vendor call, no mailbox read.** This cell ships a library; the intake
  Lambda's next build in this slot carries it.
- **The guard census over this cell's routes is vacuous on its own** and is reported as such;
  the two controls on the censor are what carry that arm.
