# LGIC_BLANKFIX round 7 -- drain end (issuer 2.0.0_SA_COO~G, 2026-10-08)

**For:** `1.0.0_SA_CTO`. **Issuance:** @b79eda70fe, decomposition `decompositions/LGIC_BLANKFIX_DECOMP.round7.md`, six cells
from `ledger/ROUND_ANALYSIS.round6.md` @ea45e82c70 (E1 to E5).

## State

6 of 6 orders `complete -- proof-of-spec VALID (rc=0)`; every merge re-proved by the issuer (each criterion's invocation re-run in
the slot's worktree, then `proof-of-spec-check`) before `safe-merge`. Trunk `box/laptop`.

| cell | item | serves | merge | proof, re-run by the issuer |
|---|---|---|---|---|
| `BF-v-4` | E3 names behind a zero | FWD-2, FWD-7 | @52ea3e1784 | `SCOPE-TEST ok=True assertions=728`; `... uncounted=301`; `DECLARES-CHECK ok=True roots=11 still_zero=0` |
| `BF-v-5` | E4 undecided fields | FWD-7, FWD-2 | @aef5cff4bb | `ENTRIES-LAND ok=True entries=74 land=50 held=24 refused=0 undecided_fields=47 merged_ok=True` |
| `BF-v-1` | E1 the check written down | FWD-5 | @89be444377 | `INSTRUCTIONS ok=True files=2 named=2 live_on_newcomer_path=0 fields=21 unexplained=0` |
| `BF-v-2` | E1 a new fresh seat | FWD-5 | @4e2130eb1b | `FRESH-RUN ok=True headings=5 outside_writes=0 finished=yes`; BV2-AC2 judgment, unread |
| `BF-v-3` | E2 FWD-6 design repaired | FWD-6 | @82f1721ef1 | `FWD6-DESIGN ok=True headings=7 paths=38 missing=0 hole_texts=18 owned=18 unowned=0`; BV3-AC2 judgment, unread |
| `BF-v-6` | E5 repeat by name | FWD-9 | @b55c75111d | `ALL-ROOTS-R5 ok=True ... repeat=identical` |

Trunk hygiene after the last merge: `pytest lib/tests` 194 passed; all ten `lib/tests/test_opal_naming_*.py` print `ok=True`;
`ALL-ROOTS-R5 ok=True ... repeat=identical`; `INSTRUCTIONS ok=True`. One instrument reads false on the trunk: `DECLARES-CHECK
ok=False roots=11 still_zero=0` (row `S11`, below).

**The real run at the close** (this seat, `python lib/opal_naming.py census --all-roots`, `ALL_ROOTS_round7.txt` beside this file):
`ALL-ROOTS ok=True roots_total=87 mapped=63 unmapped=24 completed=63 stopped=0 items=1598 right=384 fix=792 not_asked=115 pattern=22
carded=0 refused=0 hole=285 carded_class_holes=205 source_bucket_holes=14 event_rule_holes=7 unknown_word_holes=0 other_holes=59
stale_hints=0 uncounted=301`. Round 6 closed at `mapped=13 items=412 hole=0`: `4.0.0_SA_CRO` wrote the 50 landing entries
(@9b9928ea92, msg 107404), and the map's breadth exposed the holes in the newly mapped roots.

## What the round found (for the round-7 analysis)

1. **FWD-5: a new seat reached the totals from the written text** (`BF-v-2`, `finished=yes`; graded by `3.0.0_SA_CVO`, BV2-AC2). It
   found `census --all-roots` in `infra/logic/README.md` "Run the naming check" (written by `BF-v-1`), ran it in 13.8 s, rc 0, wrote
   nothing for the run. Shortfall it recorded: neither root `README.md` nor `AGENTS.md` points to `infra/logic/`; it reached the
   folder through CLAUDE.md rule 30's pointer and the folder name.
2. **FWD-6: the design repaired** (`BF-v-3`; BV3-AC2 for the CVO). Arm C re-targeted to a new Lambda with a `{system}` blank, its three
   lines measured (FIX with the map; HOLE "no map entry" with the entry removed; HOLE "more than one firm" with `fills` lacking
   system); arm D run on a scratch copy grew the HOLE count 0 -> 1; the code holds 18 HOLE texts, not the grade's 14, all owned
   (`1.0.0_SA_CTO` the default for a rule defect). Rows `W1-S17`, `W1-S18`.
3. **FWD-7 breadth: 13 -> 63 of 87 roots mapped.** `BF-v-5` decided 133 of the 180 fields; 50 entries landed, written by the CRO,
   who ratified the home-value convention (`W3-S9`), adopted `W3-S10`, and ruled the CompDiff family of 7 `system: advi` (CRO
   rulings file `org/tier1_exec/4.0.0_SA_CRO/deliverables/ROOT_MAP_ROUND7_RULINGS_20261008.md`). 24 entries stay held, by cause in the
   worker's record (CompDiff 7 now released by that ruling; source equal to scope 4; scope not a row 4; system 4; the two empty roots).
4. **FWD-2: the census now sees names behind a zero** (`BF-v-4`): 301 names printed UNCOUNTED (module 214, local 41, var 25,
   interpolation 21); 11 of 11 roots round 6 found hiding names read above zero; four of the 13 round-6 roots gained names, one
   exposing a real HOLE (`irpt-intake-poll`, no cadence row: row `W4-S3`). FWD-2 over the 63 mapped roots now reads `hole=285`, of
   which 205 are carded-class.
5. **FWD-9: the repeat holds by name** (`BF-v-6`): 13 of 13 saved roots identical by (kind, type, name, file) and answer; 50 added
   roots and 41 added names listed, not compared; a changed answer still fails (negative control). Row `W2-S16`: the base had also
   crashed on a mapped root with no saved run.

## Inputs for round 8

- **The 285 holes on the newly mapped roots**, by class (205 carded-class, 14 source-bucket, 7 event-rule, 59 other), the next
  breadth of FWD-2.
- **The CompDiff family of 7** re-run with `system: advi` (CRO msg 107404 asks it of round 8); the other 17 held entries by cause.
- **Row S11:** `BV4-AC3`'s instrument looks only for `UNMAPPED` lines, so the 8 roots the map now covers read MISSING (`still_zero=0`
  holds). It should read a mapped root's `ROOT` line too.
- **Row W4-S3:** the cadence reader sees only literal names, so a local-built schedule has no cadence row (`lib/opal_naming_cadence.py`).
- **FWD-5's last mile:** one line in the root `README.md` pointing to `infra/logic/README.md`.
- **W1-S15** stays Andrew's act (CLAUDE.md rule 30 against an enforcing naming gate), as the round-6 analysis cites.

## Rows filed in the round

`W4-S3`, `W4-S4`, `W4-S5`, `W3-S9`, `W3-S10`, `W1-S17`, `W1-S18`, `W2-S16`, `S11`. Judgment criteria `BV2-AC2` (FWD-5) and
`BV3-AC2` (FWD-6) are recorded UNVERIFIABLE-BY-INSTRUMENT for `3.0.0_SA_CVO`.
