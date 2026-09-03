# comp-dataflow `gate` under FWD-10 -- NFRA_COMPEFFICACY per-cell result (PRD v0.5 s.4.4 verdict-bearing row)

Schema: `org/missions/D11/NFRA/NFRA_COMPEFFICACY/prd/NFRA_COMPEFFICACY_PRD.md` v0.5 @`5bbdab5ec7`
(FWD-10 appended; s.4.4 gains the `verdict-bearing` row). Row: T-7 (manifest s.7 :608), the SAME
tool as CE-t-7's own round-4 audit -- this is a NEW, focused deliverable for CE-t-25, not a
replacement; `comp-dataflow.result.md` @`803539f490` stands as the round-4 record and is READ, not
restated. Cell: CE-t-25 (decomp v0.2.3 @`dcf07b4799`, ADDED), STAGE (round 5). Measured by
`0.8.0_AE_CloudComp~A`, 2026-09-03T09:27Z-12:04Z, read-vintage HEAD @`72e7846ca7`, engine
@`72e7846ca7`. **This cell is the S14 disarm** (`org/missions/D11/NFRA/NFRA_COMPEFFICACY/surprise-channel/investigations/INVESTIGATION_v1.md`
row `NFRA_COMPEFFICACY-S14`, disarm reported at row `NFRA_COMPEFFICACY-S16@72e7846ca7`, disposition
left for `3.0.0_SA_CVO`'s own L9 adjudication per the TO's own words).

## THE BAR, QUOTED (PRD v0.5 @`5bbdab5ec7`, not restated in my own words)

> **FWD-10** A tool whose exit code is its verdict never returns the clean verdict from a partial
> run: at budget expiry it says so in its own voice and exits in a way no reader can mistake for
> clean, and it tells the reader where to resume.
> **DONE WHEN** EXERCISED -- a budget-cut sweep of a verdict-bearing tool has been read by an
> rc-only consumer (a hook, a script, an `&&`) as NOT clean, and its resume cursor has been
> followed to completion.
> **ACCEPT** for every marquis tool whose rc carries a verdict (a gate, a deny-test, a check): at
> BUDGET REACHED the line prints as Rule T requires AND the rc is a non-clean value distinct from
> both the clean verdict and the failing one, carrying the PARTIAL_OR_BLIND state in the tool's
> voice (`NOT-DECIDABLE`); a consumer that reads only the rc cannot read a prefix as CLEAN; the
> cursor resumes as in s.4.4.
> **s.4.4 `verdict-bearing` row:** a tool whose rc IS its verdict -- a gate, a deny-test, a check --
> prints the BUDGET REACHED line exactly as above and returns a NON-CLEAN rc distinct from both the
> clean verdict and the failing one, carrying PARTIAL_OR_BLIND in its own voice ("NOT-DECIDABLE",
> the enum's tool-voice token; `iam_cli.py` returns it as rc 2 today); the "rc stays 0" clause above
> governs every NON-verdict tool and nothing else; the cursor is unchanged. A verdict-bearing tool
> that returns its clean rc at expiry FAILS Rule T whatever its line says.

## THE RC VOCABULARY (`comp-dataflow gate`, `--help`'s own epilog, quoted)

```
RC VOCABULARY (VERDICT-BEARING, PRD v0.5 s.4.4 / FWD-10, NFRA_COMPEFFICACY CE-t-25):
  0  clean     -- a COMPLETE sweep, zero findings
  1  findings  -- a COMPLETE sweep, >=1 finding
  2  usage     -- a CLI usage error (a malformed --budget value)
  3  refused   -- the pathspec resolved to zero producer files (input-resolution)
  4  not-decidable -- a PARTIAL (budget-limited) sweep; ALWAYS this value at BUDGET
        REACHED, regardless of whether the units reached carried a finding -- never
        the clean rc and never the findings rc (a prefix carries no verdict). The
        family precedent: org/modules/graph/iam_cli.py:50 STATE_NOT_DECIDABLE
        returns rc=2 for this same enum state; this tool adopts rc=4 instead only
        because its own rc=2 was already occupied (usage) before this cell.
```
**Why rc=4, not the family's rc=2:** `iam_cli.py`'s `STATE_NOT_DECIDABLE` is a fresh vocabulary
with rc=2 open; `comp-dataflow gate` already occupied rc=2 for a CLI usage error at CE-t-7, before
this cell existed. Colliding two meanings on one rc would make an rc-only consumer unable to tell
"malformed flag" from "partial coverage." The TO's own words anticipated this exactly ("adopt the
same value unless cmd_gate's existing rc vocabulary already occupies 2, in which case pick the next
unoccupied value") -- rc=4 is that next value (0/1/2/3 all occupied).

## EXERCISED (T25-AC2, the FWD-10 DONE WHEN) -- both runs, quoted verbatim

**Run 1 -- a real rc-only consumer bails on a budget-cut sweep:**
```
$ python org/modules/graph/comp_dataflow.py gate data/ --budget 0.001 > /dev/null 2>/dev/null && echo "PROCEEDED (WRONG)" || echo "CORRECTLY DID NOT PROCEED (rc=$?)"
CORRECTLY DID NOT PROCEED (rc=4)
```
The `&&` short-circuited on the non-zero rc -- exactly the consumer FWD-10's DONE WHEN names ("a
hook, a script, an `&&`"). The tool's own text, quoted from the same run:
```
comp-dataflow GATE (layer-grammar / PSTMRT item-9): 0 finding(s)
  DENOMINATOR: 1 producer files swept, 3 reads scanned, 1 unresolved-dynamic (blind) [...], 0 exempt
  BUDGET REACHED: 0.001 s (flag); scanned 1 of 532 producer_file; results are a PREFIX, not the
  answer; resume: comp-dataflow gate data/ --budget 0.001 --cursor
  data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py
  STATE: NOT-DECIDABLE  (rc=4, distinct from clean rc=0 and findings rc=1 -- a PREFIX carries no verdict)
  DEFERRED: 531 of 532 producer_file(s) did not return -- each names its reason below
```

**Run 2 -- the cursor is followed to a REAL completion; the rc becomes the true verdict:**
```
$ python org/modules/graph/comp_dataflow.py gate data/ --budget 30 --cursor "data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py"
... rc=1 ...
  DENOMINATOR: 531 producer files swept, 1033 reads scanned, 603 unresolved-dynamic (blind) [...], 0 exempt
  WITHIN BUDGET: scanned 531 of 531 producer_file; budget: 30 s (flag), used 6.72 s
  DEFERRED: 0 of 531 producer_file(s) did not return -- each names its reason below

$ python org/modules/graph/comp_dataflow.py gate data/ --budget 30 --cursor "data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py" > /dev/null 2>/dev/null && echo "PROCEEDED" || echo "DID NOT PROCEED (rc=$?)"
DID NOT PROCEED (rc=1)
```
rc=1 is the TRUE verdict for this population (the swept subtree genuinely carries a served-origin
finding, per the round-4 audit's own item-9 semantics, unchanged) -- distinguishable from rc=4 by
value alone, and NEVER rc=0. The DONE WHEN is met: an rc-only consumer correctly refused a partial
run, and following its own printed cursor to completion produced a real, distinguishable verdict.

## THE BUG FOUND WHILE EXERCISING THE ABOVE (not asked for; required to build it)

The FIRST attempt at Run 2 (following the printed cursor with an AMPLE budget, `--budget 30`)
**did not produce a true verdict** -- it read `rc=4` again, with `WITHIN BUDGET` nowhere and
`BUDGET REACHED: ...; scanned 531 of 532 producer_file; ... DEFERRED: 0 of 532`. Zero units were
actually deferred, yet the run still reported PARTIAL. Root cause, found by reading the exact
line: `total_units = len(units)` was measured **before** the `--cursor` filter reassigned `units`,
so `N` stayed pinned at the pre-cursor population size (532) forever, while `n` (units this
invocation actually completed) could only ever reach 531 -- `n < N` by construction, no matter how
generous the budget. **A cursor-resumed sweep could never reach a true verdict.** This directly
contradicts FWD-10's own DONE WHEN ("its resume cursor has been followed to completion") -- the
mechanism this cell exists to build would have been unsatisfiable by its own acceptance test.

Fixed in the same commit: `total_units` is now measured **after** the cursor filter, matching
`comp-find`'s own established precedent for the identical shape (CE-t-1's own `_search_aws`
resolves its unit-count post-cursor too). Re-verified: the identical Run 2 sequence now returns
`rc=1`, quoted above.

## Non-application stated (T25-AC3)

- **`origin`'s rc semantics: ZERO diff.** `git diff` confirms no hunk touches `cmd_origin`'s body --
  the function is byte-for-byte unchanged by this commit. `origin` traces exactly one file, never a
  sweep, and was never in scope for a verdict-bearing rc (CE-t-7's own non-application finding
  stands unmodified).
- **The round-4 cursor SKIP mechanism (which files get processed) was already exact and remains
  exact** -- confirmed by this cell's own exercise (Run 2 processed exactly the 531 files after the
  named cursor, none repeated, none missed). What was broken, and is now fixed, is the
  **denominator/verdict determination** after a resume, a narrower and more specific defect than
  "the cursor is wrong."
- **Item-9 semantics (served-origin flagging, exemptions): untouched.** `_served_findings()`,
  `classify_layer()`, `trace_file()`'s classification logic carry zero diff lines; re-verified live
  against the RF-7 charter specimen (unchanged, still 5 SERVED-ORIGIN flags).

## Battery (T25-AC4)

`.tools/tests/test_comp_dataflow_battery.py`: **11 of 11 PASS** (the 8 round-4 arms unaffected +
3 new), direct and under `pytest -q`.

New arms:
- **VERDICT-RC-CONSUMER**: a real `subprocess.run` rc check (the same signal a shell `&&` reads)
  does not proceed on a budget-cut sweep; the same pathspec at an ample budget completes with a
  true verdict rc (never usage/refused/not-decidable).
- **VERDICT-RC-VOCABULARY**: three real `gate` invocations (a genuinely clean subtree, a genuinely
  findings-bearing subtree, a budget-cut full-tree sweep) produce three **pairwise distinct** rc
  values on the real binary -- 0, 1, 4 -- no shared value across any pair. No mutant needed; this is
  the real production binary end to end.
- **MUTANT-VERDICT-RC** (RED-first): a planted build where `if partial: return RC_NOT_DECIDABLE`
  is replaced with `return RC_CLEAN` reproduces the EXACT FWD-10 violation on demand (`rc=0` from a
  budget-cut sweep) -- built in a scratch mirror matching `comp_dataflow.py`'s own `_WS`-resolution
  depth (the CE-t-7 precedent), proving arm 7's rc=4 is produced by real compliance, not an
  identity that would pass regardless.

All 8 round-4 arms (`NEVER-GUESS-*`, `REASON-CLASS`/`MUTANT-REASON`, `REASON-CONSERVATION`,
`ITEM-9-UNCHANGED`, `BUDGET-CARRIER`/`MUTANT-BUDGET`) re-confirmed green, unaffected by this cell's
edits -- direct proof that CE-t-25's changes are additive to CE-t-7's, not a rework of them.

Directory grain: `pytest --collect-only .tools/tests/` still `INTERNALERROR` / `SystemExit` at
`test_fabric_check_classify.py:76` (CTO's F6, unchanged); 36 tests collected before the abort (up
from 35 at CE-t-7's own read, +1 for this file's growth) -- not this cell's, carried.

## A finding routed up, not landed here (BOUNDS)

`_compbudget.py` is consumed, not edited under this order. If the verdict-bearing expiry-rc shape
(a distinct rc for a partial run, on top of the shared module's existing `WITHIN BUDGET`/
`BUDGET REACHED` text) belongs in the shared module itself -- so the NEXT verdict-bearing marquis
tool (a deny-test, a check) inherits the mechanism instead of re-deriving its own rc vocabulary from
scratch, as this cell did -- that is a proposal for the L4 owner (`1.0.0_SA_CTO`) and the sequencer
to place, not a change this one-tool cell may land. Proposed shape (not built): `_compbudget.py`
could export a small `verdict_reached_rc(clean_rc, findings_rc, not_decidable_rc=None)` helper that
returns the vocabulary's occupied set given a tool's own clean/findings values, so each verdict-
bearing tool only states its two existing values and receives the next-free NOT-DECIDABLE rc rather
than hand-picking it (as this cell did, reading its own `return N` statements to find rc=4 was free).

## Captures and controls

Every quoted run above is a direct execution captured in this session, including the ONE run that
demonstrated the bug BEFORE the fix (not selectively omitted). Production sha256:
`org/modules/graph/comp_dataflow.py` was
`7724e1a44ebe183a843d0775ae3350477a1d99ce16dc25d189a2aab9b69ace03` at HEAD `8fdc3d0602` (CE-t-7's
own landed state, before this cell), `422d81bfdfab06749428c23fca6c0df8aa359e0985b2fec7fd56c5d0e57413b7`
at HEAD `72e7846ca7` (after this cell's fix) -- two MEASURED points. `git status` at write time shows
only this deliverable + its proof-of-spec instance + the S16 surprise-row append pending beyond the
already-landed code commit. Push state, MEASURED (ls-remote + is-ancestor), reported in the commit
report per T25-AC5, not asserted here.
