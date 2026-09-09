# NFRA_OUTSET.TO-OS-s-16 -- RESULT: the archive-candidate answer

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** `8c231d47bf`
**Cell:** `OS-s-16` · **outcome_ref:** FWD-8 · **verb:** build · **depends_on:** `OS-s-15`

---

## 0. THE GATE OPENED, AND THE CELL IS A WIRE

`OS-s-15` is `complete` and its decision, read at HEAD from the TO's own `<status>`: *"none of
O2/O3/O4 is a RETIRE-CANDIDATE, so `OS-s-16` is NOT struck by this ruling -- and it is a WIRE, not a
build."* So `O16-AC2`'s stop condition does **not** fire, and the work is connecting legs that
already exist rather than writing a fourth.

| leg | already existed | what was missing |
|---|---|---|
| O1 `object_freshness.build_budgeted` | per-path heat, path-scoped + budgeted (OS-s-1/2) | — |
| O2 `object_locality.aggregate_tree` + `maximal_cold_subtrees` | rolls heat **up the directory tree**; returns the **highest** wholly-cold dir, never its children too | **no caller** |
| O3 `object_recommend.assess` | **verify BEFORE recommend** — any inbound reference is a HOLD | **no caller** |

**What I added is a caller**, `comp-heat archive`, plus one parameter (`timeout_s`) so O3's git pass
takes its bound from Rule T's `clock.remaining()` instead of a constant. No new analytic.

## 1. `NFRA_OUTSET-W3-S4` DISARMED, WITH THE MEASUREMENT IT DEFERRED TO THIS CELL

W3-S4 said `freshness` labels a flat `os.path.dirname` grouping as `cold SUBTREES`, and explicitly
left open: *"how many real cold subtrees in this estate the flat grouper misses ... is OS-s-16's
measurement to make."* Made, both runs at `--budget 90` on the same worktree:

| | count |
|---|---|
| `freshness --json` → `cold_subtrees` (flat, immediate-parent) | **1,412** |
| `archive --json` → maximal cold subtrees (O2 roll-up) | **364** |
| **maximal roots the flat list NEVER contains** | **50 of 364** |
| roll-up coverage (O2's own disclosure) | **30,704 of 30,704** — no path silently unplaced |

The 50 include `org/tier3_junior`, `tools`, `data/black_diamond`,
`org/tier2_senior/0.4.0_DS_ClientPlatform/logs` — whole dead trees the flat grouping cannot see,
because no ancestor ever accumulates a count.

**Both halves of the row are closed.** The roll-up is real (battery arm B reproduces slot 3's own
synthetic shape through the CLI: flat → `[]`, O2 → `['dead']`, `comp-heat archive` → `['dead']`), and
the false label is gone — `freshness` now prints *"cold LEAF DIRS (immediate-parent grouping…) — NOT
a subtree roll-up"* and names `comp-heat archive`. The JSON key `cold_subtrees` is **unchanged** (a
rename breaks consumers); a `cold_subtrees_basis` object is added beside it.

**The residue, named:** `freshness`'s *computation* is unchanged. That is now a correctly-labelled
answer to a different question, one subcommand away from the roll-up. Changing what it computes
would alter a drained cell's output shape for every consumer.

## 2. THE ANSWER, AND WHY EACH LINE IS DISPUTABLE

Every candidate carries the numbers that produced it and an explicit **DISPUTE IT BY** clause:

- **RECOMMEND_ARCHIVE** → *"DISPUTE IT BY: naming any file outside this subtree that references it
  — the name-vs-edge pass found none. THEN RUN THE MANDATORY GRAPH GATE, which this tool does NOT
  run: `comp-blast <dir> --direction up --check-consumers`"*
- **HOLD_REFERENCED** → *"DISPUTE IT BY: showing these references are stale — HELD because N file(s)
  outside it reference it: …"*

A denominator rides every answer: *"364 maximal cold subtree(s) found across 4,165 directory(ies)
rolled up from 30,702 scored path(s); 5 assessed, 359 UNASSESSED."* **UNASSESSED is printed as
`NOT cleared, just not examined`** — an unassessed candidate is not a cleared one, and dropping the
tail silently would have been the same class of lie as an omitted stratum.

## 3. NEVER-AUTO-DELETE — ENFORCED, NOT ASSERTED

The tool removes nothing, moves nothing, and writes nothing outside a `--json` file the caller
names. **That is checked**: battery arm C snapshots every file in a throwaway tree (relative path +
sha256) before and after a real run and requires them byte-identical.

And arm D exists because **an integrity check that has never caught anything is a promise, not a
control**: the RED mutant is a copy of `comp-heat` with `shutil.rmtree` spliced in after the
candidate list is computed. It removed 8 files from its own tree and arm C's snapshot saw it.

**Every mutant run is pointed at a `tempfile.mkdtemp()` repository, never the real one.** That is
why `archive` takes `--root` at all — a mutant that deletes must not be able to reach the estate, and
"we were careful" is not a mechanism.

## 4. ACCEPTANCE

### O16-AC1 -- PASS-by-output
`<invocation>` `python .tools/tests/test_os16_archive_answer.py` · `<expect>` `PASS`

```
[PASS] A-ANSWER-RANKS-WITH-A-DISPUTABLE-REASON-PER-LINE -- rc=0 ; 1 ranked candidate line(s), 1 REASON line(s), 1 DISPUTE line(s) -- one each, and the header says the tool removes nothing | 1. RECOMMEND_ARCHIVE  dead/
[PASS] B-ROLLUP-IS-REAL-FLAT-GROUPING-MISSES-THE-DEAD-ROOT -- same 8-of-8-cold tree across 4 leaf dirs: flat immediate-parent grouping -> [] (0 candidates) ; O2 roll-up -> ['dead'] ; and `comp-heat archive` reports ['dead'] -- the wire makes the grouping real
[PASS] C-PRODUCTION-RUN-REMOVES-AND-MOVES-NOTHING -- snapshotted 39 file(s) by relative path + sha256 before and after a real `archive` run; identical=True ; added=[] removed=[]
[PASS] D-RED-MUTANT-THAT-DELETES-FAILS-THE-INTEGRITY-ARM -- the mutant removed 8 file(s) from its THROWAWAY tree (['dead/a/f1.py', 'dead/a/f2.py']...) and arm C's snapshot detects it: identical=False. Production on its own tree: identical=True. The integrity check is therefore a control, not a promise
[PASS] E-MUTATION-ANCHOR-UNIQUE
[PASS] F-DENOMINATOR-AND-COVERAGE-ARE-PUBLISHED -- {"scope": "(whole estate)", "scored_paths": 9, "rollup_clustered_n": 9, "rollup_total_n": 9, "directories_rolled_up": 6, "maximal_cold_subtrees_found": 1, "assessed": 1, "unassessed": 0, "claim": "measured"}
[PASS] G-BEYOND-TOP-READS-UNASSESSED-NOT-CLEARED -- with --top 1 and 2 candidate(s) found, 1 assessed and 1 carried as UNASSESSED, and the render says 'NOT cleared, just not examined'
[PASS] H-VERIFY-BEFORE-RECOMMEND-HOLDS-A-REFERENCED-SUBTREE -- an OUTSIDE file mentioning the subtree path -> HOLD_REFERENCED with evidence ['live/uses.py'] ; a name-clean subtree -> RECOMMEND_ARCHIVE carrying the MANDATORY gate 'comp-blast dead --direction up --check-consumers' (which this tool does NOT run)
[PASS] I-A-CUT-BUDGET-CLAIMS-NO-CANDIDATE-LIST -- rc=3 ; a subtree that looks wholly cold in a partial scan may not be, so the answer is refused rather than truncated
[PASS] J-FRESHNESS-NO-LONGER-CLAIMS-A-ROLLUP-IT-DOES-NOT-DO -- {"grouping": "IMMEDIATE-PARENT (os.path.dirname), not a directory roll-up", ...}
OS16-ARCHIVE-ANSWER BATTERY: 10/10 PASS (denominator 10; every mutant run confined to a tempfile repo, 0 files removed from this estate)
```
**rc=0. 10 of 10 arms PASS**, stable across 2 direct runs; pytest `1 passed in 17.55s`.

### O16-AC2 -- JUDGMENT (`judgment="true"`) -- RECORDED, NO VERDICT

**The gate:** `OS-s-15` decided **BUILD**, not RETIRE (s.0). So this criterion's stop condition does
not apply and no row was filed against it.

**One real ranked answer, whole estate, `--budget 90 --top 5`, rc=0 in 21.8 s:**

```
=== comp-heat archive  scope=(whole estate)  ADVISORY-ONLY -- NOTHING IS REMOVED ===
budget: 90 s (flag)
WITHIN BUDGET: scanned 30702 of 30702 files; budget: 90 s (flag), used 20.765 s
  denominator: 364 maximal cold subtree(s) found across 4165 directory(ies) rolled up from 30702 scored path(s) under (whole estate); 5 assessed, 359 UNASSESSED
  basis: a candidate is a MAXIMAL cold subtree -- the highest directory whose whole subtree is >= 90% cold with >= 5 files, whose parent does not itself qualify. cold = age > 30d (hot<=7d, warm<=30d); score = exp(-ln2*age/30d half-life).
  verdicts: 0 RECOMMEND_ARCHIVE / 5 HOLD_REFERENCED / 359 UNASSESSED (beyond --top 5)
      1. HOLD_REFERENCED    infra/
         REASON: 7468 of 7920 files in this subtree are cold (cold_frac=0.9429), oldest write 291 days ago, mean heat 0.1427, depth 1.
         DISPUTE IT BY: showing these references are stale -- HELD because 5 file(s) outside it reference it: .claude/settings.json, ...
      2. HOLD_REFERENCED    org/tier2_senior/0.4.0_DS_ClientPlatform/logs/
         REASON: 850 of 906 files in this subtree are cold (cold_frac=0.9382), oldest write 187 days ago, mean heat 0.1660, depth 4.
      ...
    ---. UNASSESSED        deck_generation/  (194 of 194 cold) -- beyond --top; NOT cleared, just not examined
  REMINDER: ADVISORY ONLY. This tool removes nothing, moves nothing and writes nothing outside its own --json.
```

**Denominator:** 364 of 4,165 directories qualified, from 30,702 scored paths; 5 assessed, 359
unassessed; roll-up coverage 30,704 of 30,704.

**What this answer is not.** **0 of the 5 top-ranked reached RECOMMEND** — every one came back
HOLD_REFERENCED. Nothing in this estate is being proposed for archive today, and every RECOMMEND
anywhere still carries a graph gate this tool does not run.

## 5. A PROPERTY OF THE ANSWER I MEASURED AND DID NOT FIX -- `NFRA_OUTSET-W1-S23`

O3's inbound check matches a candidate's path as a **bare substring**. Measured:
`referenced_index('.', ['tools'])` returns `.claude/settings.json` and five others; and
`docs/architecture/ADHC_BASHFIX.md` carries **5 substring hits for `tools`** while an anchored search
for the real `tools/` path in that file returns **nothing** — every hit is `.tools/`, a *different*
directory.

So a shallow candidate can essentially never reach RECOMMEND, whatever its true reference count, and
a person disputing a HOLD is handed file names that may not reference the subtree at all.

**Direction: over-HOLD** — conservative. R-5 is not breached and nothing is wrongly recommended.

**I did not fix it, and the reason is the rule rather than the grant.**
`object_recommend.py` **is** in my `<paths>`. Anchoring the pattern would move candidates from HOLD
to RECOMMEND on an *archive recommender* — a reduction in conservatism on the exact axis R-5 governs.
That is a ruling first and a measured change second, not a worker's mid-cell judgement.

## 6. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os16_archive_answer.py` | `10/10 PASS`, rc=0 (x2) |
| `python -m pytest -q .tools/tests/test_os16_archive_answer.py` | `1 passed in 17.55s`, rc=0 |
| `test_os1_budget_battery.py` | `21/21 PASS`, rc=0 |
| `test_os2_path_grain.py` | `10/10 PASS`, rc=0 |
| `test_os4_federated_vintage.py` | `9/9 PASS`, rc=0 |
| `test_os5_sql_bound.py` | `10/10 PASS`, rc=0 |
| `test_os10_seam.py` | `12/12 PASS`, rc=0 |
| `test_comp_heat_battery.py` | `Ran 2 tests ... OK`, rc=0 |
| `bash .tools/commit-gate.sh` on the 3 touched files | `OK: pre-commit gate clean for 3 of 3 file(s)`, rc=0 |

One gate block, fixed rather than worked around: ruff F401 on an unused `uuid` import.

**A fixture bug worth recording, because it failed one layer from its cause.** `git commit` refuses
a relative date (`fatal: invalid date format: 400 days ago`) even though `git log --since` accepts
one; the commit then failed and the *next* call died on *"does not have any commits yet"*. Fixed with
an absolute ISO stamp **and** an explicit rc check on the fixture commit, so a future failure names
itself.

## 7. DECLARED NON-APPLICATION

- **Nothing was removed, moved or renamed** anywhere, in the estate or in any temp tree by a
  production run. R-5 is absolute and arm C+D are how it is enforced here.
- **`freshness`'s computation is untouched** — only its label and an additive JSON basis (s.1).
- **O3's substring matching is untouched** — `W1-S23`, s.5.
- **No fourth engine.** `OS-s-15` ruled the legs stay; this cell is their caller.
- **O4 (`object_report.py`) is not wired here.** `OS-s-16`'s accept is the ranked answer with a
  reason per line, which O2+O3 deliver; a report surface is not this cell's accept.
- **No alarm, monitor or freshness-checker; no new dependency; nothing pushed.**

## 8. PUSH STATE

**LOCAL.** Measured with `git ls-remote` at report time — see the WORKER REPORT.
