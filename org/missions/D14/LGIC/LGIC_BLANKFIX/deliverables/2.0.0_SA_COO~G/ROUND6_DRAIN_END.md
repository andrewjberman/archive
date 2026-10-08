# LGIC_BLANKFIX round 6 -- drain end (issuer 2.0.0_SA_COO~G, 2026-10-08)

**For:** `1.0.0_SA_CTO`. **Issuance:** @6ded8fd5d9, decomposition `decompositions/LGIC_BLANKFIX_DECOMP.round6.md`, seven cells
from `ledger/ROUND_ANALYSIS.round5.md` @34ba4c1c90 amended @cbdf36254c (E1 to E6).

## State

7 of 7 orders `complete -- proof-of-spec VALID (rc=0)`; every merge re-proved by the issuer (each criterion's invocation re-run in
the slot's worktree, then `proof-of-spec-check`) before `safe-merge`.

| cell | item | serves | merge | proof, re-run by the issuer |
|---|---|---|---|---|
| `BF-u-1` | E1 sort + drafts | FWD-7, FWD-2 | @c6cf182bb2 | `UNMAPPED-SORTED ok=True ... names_zero=24 no_stored_name=14 to_map=36 sections=74 declares_names=11` |
| `BF-u-6` | E5 design | FWD-6 | @a763bb7029 | `FWD6-DESIGN ok=True headings=7 paths=30 missing=0`; BU6-AC2 judgment, unread |
| `BF-u-4` | E3 red test | the gate | @6037eb086c | `KEYFILL-TEST ok=True cases=86` |
| `BF-u-5` | E4 repeat | FWD-9 | @90b5e06676 | `ALL-ROOTS-R5 ok=True ... repeat=identical` |
| `BF-u-7` | E6 fresh copy | FWD-5 | @7b56a00893 | `FRESH-RUN ok=True headings=5 outside_writes=0 finished=no`; BU7-AC2 judgment, unread |
| `BF-u-3` | E2 rulings move | FWD-2 | @93514b64f0 | `ROOTCHECK-TEST ok=True cases=209`; `stale_hints=0`; `repeat=identical` |
| `BF-u-2` | E1 reader | FWD-7, FWD-9 | @93514b64f0 | `ROOTMAP-TEST ok=True assertions=46`; `ALL-ROOTS ok=True ... hole=0` |

Trunk hygiene after the last merge: `pytest lib/tests` 194 passed; all ten `lib/tests/test_opal_naming_*.py` print `ok=True`.

**The real run at the close** (this seat, `python lib/opal_naming.py census --all-roots`, `ALL_ROOTS_round6.txt` beside this file):
`ALL-ROOTS ok=True roots_total=87 mapped=13 unmapped=74 completed=13 stopped=0 items=412 right=124 fix=248 not_asked=32 pattern=8
carded=0 refused=0 hole=0 ... stale_hints=0`. The root map did not change in the round, so the mapped totals equal round 5's.

## What the round found (for the round-6 analysis)

1. **FWD-7 / FWD-2 breadth did not move.** `4.0.0_SA_CRO` drafted all 74 entries from `BF-u-1`'s file; only `inf-pipeline` loads
   (notes @6091606dd8: 180 UNDECIDED fields; with it, `mapped=14 items=776 hole=69`). Row `S10` parks the measurement of the 180
   to round 7 (owner this lane). The 13 `names: none` entries can now load (`BF-u-2` merged).
2. **The census misses names** (row `W1-S14`, ARMED, disarm owner `1.0.0_SA_CTO`): 11 of the 24 roots that read `names=0` declare
   names built in locals, through modules, or in a `.json` file.
3. **FWD-5 exercised and did not finish** (`BF-u-7`; graded by `3.0.0_SA_CVO`, BU7-AC2). A first-time seat on a fresh copy found the
   written commands only in `infra/logic/10_ONBOARDING_CHECKLIST.md` STEP 13 and the brief, both requiring `--live`; on the repository
   plane `census --repo` stops at the first RAISE with every repo-held skip list; `--all-roots` (found only in the help text) finishes
   over 13 of 87 roots. Nothing was written for the run.
4. **FWD-6 has a design** (`BF-u-6`; BU6-AC2 for the CVO): `place()` extracted from the root check, called by the commit gate and the
   apply gate; FIX and HOLE refused with what is owed; a live per-root hole ratchet. It measured that today's naming gate refuses a
   wrong schedule name but prints the blank unfilled and says nothing owed. Row `W1-S15`: the naming gate is ENFORCE on this box
   (`org/mcp/naming-gate.enforce`), not WARN as CLAUDE.md rule 30 says.
5. **An issuer error, caught and repaired in the round.** `BF-u-3` item 1 matched a ruling on the key alone; on the trunk that re-paired
   `bd-49f-freshness-probe`'s `bronze/` (it reads `opal-data-bd`) to the `opal-data-inf` row, and AMENDMENT 1 wrongly accepted the
   resulting stale hint as true. `4.0.0_SA_CRO` named the cause (msg 107136); AMENDMENT 2 (@a9830667e3) required bucket agreement
   and `repeat=identical`; the line is back to `-> blackdiamond/49financial/bronze/` and `stale_hints=0`. Row `W4-S2` (BLOCKING) is
   resolved by that amendment and waits for its disposition.

## Inputs for round 7

- The 180 UNDECIDED fields (row `S10`); the CRO's recommendation to retire the two empty roots (`canonical-schwab-si2-schedule`,
  `opal-assets-absence`) as dead Terraform rather than add a third `why`.
- The scope's blind spot for names in locals, modules and `.json` (row `W1-S14`).
- FWD-5's gaps: a written repository-plane command; one run that passes without a skip list the repository does not hold.
- `lines_check` on a `names: none` root reports FAIL (unchanged by `BF-u-2`; its report says so).
- Two keyfill cases still type paths (`lambda_function.py`, `handler.py` are not unique base names).

## Rows filed in the round

`S9` (E5 label, answered before the cut), `S10` (parked), `W1-S14` (ARMED), `W1-S15`, `W1-S16`, `W4-S2` (BLOCKING, resolved by
AMENDMENT 2). Judgment criteria `BU6-AC2` and `BU7-AC2` are recorded UNVERIFIABLE-BY-INSTRUMENT for `3.0.0_SA_CVO`.
