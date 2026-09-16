# LGIC_NAMING.TO-LN-e-4-r3 -- the reader, round 3, in a clean-context seat -- result

**Worker (seat operator):** 0.9.0_WK_LGIC_NAMING~5 | **Branch:** wk-lgic-naming-3-5 | **Base:** 23864712520a3461552699a755f5fce302ac3139

This file replaces round 2's result (TO-LN-e-4-r2), which sat at the same path. The issuer has recorded that collision. Round 2's result is still in the history at this path.

**The blind party** was a `claude -p` session with no tools. `blind_seat.py run e4` ran it once, from `fixed_inputs/r3/`, and it printed:

```
SEAT: OK cell=e4 rows=18 session=c355608a-1660-486f-a2b0-b233860b64c2 base=2386471252 Q1='unknown' Q2='unknown'
```

- **Seat folder:** `C:/Users/AndrewBerman/AppData/Local/Temp/opal_blindseat_r3_e4_acxrevjt`. It was outside the workspace and in no repository. It held 0 files before and 0 after the run, and no CLAUDE.md sat up its parent chain.
- **Prompt:** sha256 `ddbf01018ae45df604519ef46ec2d265b11a0a3ea7f12e4ca15aaa39b44d0b16`, 27535 bytes. The builder made it at the base from the schema's grammar lines, `firm_forms`, the three registry row files and `n3-namer-a.tsv`.
- **Reply text:** sha256 `2d1b4389a734606097f79d4d6ac6639770ac496dda0df46bb0628e27de0461cf`. The session took 1 turn, returned rc 0 with is_error false, and ran from 2026-09-15T08:07:45Z to 08:08:04Z.

**Output:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-reader.tsv` marks all 18 of namer A's 18 round-3 names. 13 carry a firm and 5 carry `none`. The seat's five files are under `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/seats/e4.*`. No file was written or edited by hand.

## Criteria (mechanical; the checker's output grades them)

| id | invocation | deciding output | rc |
|---|---|---|---|
| E4T-AC1 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e4-seat` | `SEAT CONDITIONS: 10  HELD: 10  NOT HELD: []` / `VERDICT: PASS-CLEAN-SEAT` | 0 |
| E4T-AC2 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e4-canary` | `CANARY ANSWERS: 2 of 2  WORKSPACE-ONLY FACTS IN THE REPLY: 0 of 2` / `VERDICT: PASS-CANARY-BLIND` | 0 |
| E4T-AC3 | `timeout 120 python .../fixed_inputs/r3/check_ln_r3.py e4-marked` | `NAMES: 18  MARKED: 18  MISSING: 0 []` / `VERDICT: PASS-ALL-MARKED` | 0 |

The canary read blind, so FWD-2 can be measured on this reply. This worker does not judge whether the marks are right. The scoring cell scores them against the key.

## Surprises filed

None.
