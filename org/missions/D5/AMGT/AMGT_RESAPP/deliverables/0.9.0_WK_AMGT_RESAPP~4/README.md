# AMGT-s-8 -- THE PEER SET: comparable to THIS company, or absent with a stated reason

Worker: `0.9.0_WK_AMGT_RESAPP~4` | Task order:
`org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-s-8.peer-set-comparable-or-absent-with-a-reason.md`

FWD-8's bar: "The comparison block is about the company on the page. DONE WHEN
EXERCISED -- an analyst who distrusted it has stopped. ACCEPT: The list of comparable
companies is genuinely about the company being shown. Where a sensible comparison
cannot be worked out, the page says so rather than showing another company's list."

## (a) F6 re-measured first

Re-ran AMGT-s-12's own instrument (not a third implementation):

```
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/f6_remeasure.py
```

This worker's run (2026-09-11T00:05Z):

```
F6 RE-MEASURED: stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks; vintage 2026-09-11T00:05Z
F6 CITED (brief @19ce7d5b4d, CRO method): stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks -- agreement: {'stale_set': True, 'own_set': True, 'no_csc': True, 'denominator': True}
```

AMGT-s-12's own committed run, recorded verbatim at
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/identity-layer-the-root.result.md:72`:

```
AC3: F6 RE-MEASURED: stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks; vintage 2026-09-10T23:20Z (unaffected -- CSC-sheet scoring never touched bloomberg_ticker)
```

**Verdict: AGREE.** Both runs partition the identical 54-workbook denominator identically
(stale-set 48 / own-set 4 / no-CSC 2); only the vintage stamp differs (this run is the
third read of the same instrument -- AMGT-s-11's distribution run and AMGT-s-12's own
run precede it -- and it reproduces the same partition both times, which is what makes
it corroboration rather than a fresh, independent measurement).

**Side effect, filed as a row (`AMGT_RESAPP-Z-W4-S1`):** re-running the script as AC1
requires overwrites `0.9.0_WK_AMGT_RESAPP~3`'s already-committed `f6_remeasure.json` in
place (its `OUTPUT_PATH` is hardcoded beside the script itself, not into the calling
worker's own deliverables). This worker did **not** commit that mutated file -- it is
left uncommitted in this worktree, outside this worker's own `deliverables/0.9.0_WK_AMGT_RESAPP~4/`
output, so the shared branch state is undisturbed by this run.

## (b) The peer engine

`lib/research/peers/engine.py` -- `peers(security_key, model_block_dir=..., analyst_override=None,
candidate_universe=None) -> peer_set dict`:

```
{security_key, basis: "analyst"|"derived"|"absent", test: "<the comparability test, stated>",
 members: [...], reason: "<why absent, or how derived>", vintage}
```

**The test** (stated in code -- `engine.TEST_STATEMENT` -- and in `SPEC_SECTION_peers.md`):
comparable = same Bloomberg industry classification AND a market-cap band within
0.2x-5.0x of the subject. The finest classification field AMGT-s-1's landed record
actually carries is `GICS_SECTOR_NAME` (measured: `model_block_{BABA_US,BA_US,SAP_GY}_Equity.json`
and `field_map.json`'s `fields` array carry `GICS_SECTOR_NAME` for all three securities
and no finer GICS/BICS subgroup-level mnemonic for any of them) -- the engine's `test`
string names this field explicitly rather than silently promising subgroup-level
precision it does not have.

The subject's classification and market cap are read ONLY from the record AMGT-s-1
already landed (`model_block_<security_key>.json`'s header figures) -- no new
Bloomberg call, no new security (F2/G-24).

## (c) Why every peer set at this cut reads `absent`

A `derived` set additionally needs a **candidate universe** classified by the same
field. Classifying the covered names (up to 89) is itself a quota decision the brief
flags directly (F2: "the binding constraint is UNIQUE SECURITIES TOUCHED"; "the limit
itself is unmeasured") and this cell does not spend it. `build_peer_sets.py` (this
folder) calls `engine.peers()` once for each of the three securities AMGT-s-1 landed,
with no `candidate_universe` supplied -- the honest state today -- and every call
returns `basis: "absent"`, reason naming the F2 quota decision by name. This is FWD-8's
own bar made literal: "where a sensible comparison cannot be worked out, the page says
so rather than showing another company's list."

| security_key | basis | reason (abridged) |
|---|---|---|
| `BABA_US_Equity` | absent | candidate universe not classified; F2 quota decision precedes derivation (subject's own GICS_SECTOR_NAME='Consumer Discretionary' is known) |
| `BA_US_Equity` | absent | candidate universe not classified; F2 quota decision precedes derivation (subject's own GICS_SECTOR_NAME='Industrials' is known) |
| `SAP_GY_Equity` | absent | candidate universe not classified; F2 quota decision precedes derivation (subject's own GICS_SECTOR_NAME='Information Technology' is known) |

None of the three real securities carries "subject classification not in the landed
record" as its reason -- all three DO carry a `GICS_SECTOR_NAME` value in AMGT-s-1's
landed record. That distinct reason string (and its own test, AC2 test 4) is exercised
against a synthetic fixture instead (see (d)), since it does not occur on the real,
current corpus.

An `analyst` basis is also supported (`analyst_override={"members": [...], "reason": ...}`)
-- the path for a set a person enters directly; marked as such and never subjected to
the engine's own comparability test (AC2 test 3).

## (d) The unscoped pass -- C-SHARED-DEFECT

`lib/research/peers/shared_defect.py`'s `check(peer_sets, subgroup_of)` runs over
**every** `peer_set` a run has emitted (any basis) -- never per-name -- and REFUSEs if
any two subjects in DIFFERENT classifications carry the identical, non-empty member
set (the F6 shape). It ADMITs the legitimate twin: two subjects of the SAME
classification (e.g. two telecoms) genuinely sharing a set is not a defect.

Fixtures (AC2 tests 1-2, run for real in `lib/research/peers/tests/test_peers.py`):
- Two non-telecoms (ASML, semiconductors; AstraZeneca, pharma) both carrying the
  unmodified 12-ticker KPN telecom set -> **REFUSE**, naming the pair.
- Two genuine telecoms (KPN, Telefonica) both carrying the same set -> **ADMIT**.

## (e) The corpus is never a source

Neither `engine.py` nor `shared_defect.py` opens a workbook, a CSC sheet, or any
`*.xlsx`/`*ONE PAGER*` file -- AC5 (a structural, negative grep) confirms.
`f6_remeasure.py` -- the ONLY code path that reads the corpus in this cell's whole
chain -- is AMGT-s-12's, re-run rather than re-implemented (a).

## What is here

| File | What it is |
|---|---|
| `lib/research/peers/engine.py` | (b) the peer engine -- `peers()`. |
| `lib/research/peers/shared_defect.py` | (d) the unscoped C-SHARED-DEFECT pass -- `check()`. |
| `lib/research/peers/__init__.py` | package docstring. |
| `lib/research/peers/tests/test_peers.py` | the four AC2 tests. |
| `build_peer_sets.py` (this folder) | driver: calls `engine.peers()` for each of the three securities AMGT-s-1 landed; writes `peer_set_<security_key>.json` beside itself. |
| `peer_set_BABA_US_Equity.json`, `peer_set_BA_US_Equity.json`, `peer_set_SAP_GY_Equity.json` (this folder) | (c) the three real peer_set outputs, all `basis: "absent"` at this cut. |
| `SPEC_SECTION_peers.md` (this folder) | for AMGT-s-5 -- the Peer Comparison panel section. |
| `peer-set-comparable-or-absent-with-a-reason.result.md` (this folder) | session log: controls (two mutants, determinism), raw command outputs. |

## Bounds respected

- No new Bloomberg call, no new security (F2/G-24): the subject's classification is
  read only from AMGT-s-1's landed `model_block_<security_key>.json`; classifying a
  candidate universe is left to whichever cell spends that quota decision.
- The corpus is never a source of peers (e): re-measured only via AMGT-s-12's script.
- C-SHARED-DEFECT is unscoped and not per-name (d).
- C-IDENTITY-RESOLVED: members are named by Bloomberg ticker strings (the identity
  layer's key), never a bare company name.
- A VALUE MUST CARRY ITS CLAIM: `basis` is always in `{analyst, derived, absent}`.
- C-DESIGN-SPEC-FIRST: no `.tsx` written; `SPEC_SECTION_peers.md` delivered instead.

## Declared exclusion

Classifying a candidate universe by `GICS_SECTOR_NAME` (or a finer field) for the
other covered names is NOT this order's to spend (F2's quota decision; see (c)) --
the engine's `derived` code path is written and exercised only via a synthetic
`candidate_universe` fixture inside the mutant control (see the result log), never
against the real corpus at this cut.
