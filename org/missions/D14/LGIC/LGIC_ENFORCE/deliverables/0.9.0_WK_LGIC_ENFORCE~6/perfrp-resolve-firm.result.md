# LGIC_ENFORCE.TO-EN-v-5 -- result (0.9.0_WK_LGIC_ENFORCE~6)

Branch `wk-lgic-enforce-1-6`, base `b02fdaa849`. Cell `EN-v-5`: the generated view of `resolve_firm`.

## What landed

`data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py` is now the generator's output at its existing path:

    python lib/opal_naming.py generate --out . --target data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py
    WROTE data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py (7086 bytes)
    GENERATE: 1 written, 0 skipped, into . at registry@50e4fabd1cb6a150

The diff is exactly two added lines, the begin and END marks of the `FIRM_TREES` block. `lib/opal_naming.py` VIEWS
names only `FIRM_TREES` for this carrier. The `FIRM_TREES` body the registry renders is byte-identical to the
pre-image, and so is every other line (`resolve_firm`, `FOREIGN_FIRM_BUCKETS`, `assert_path_belongs`,
`path_census`, `main`). The file is rendered to `.scratch/gen` first and diffed before it is written in place.

## Criteria

| id | invocation | deciding output | denominator | status |
|---|---|---|---|---|
| V5-AC1 | `check_en.py v5-header` | `VERDICT: PASS-GENERATED-HEADER` rc 0 | 1 of 1 file carries the mark at registry@50e4fabd1cb6a150 | PASS |
| V5-AC2 | `check_en.py v5-delta0` | `BASE: b02fdaa849  FILES: 1  EXPORTS EQUAL: 1  DIFFER: []` / `VERDICT: PASS-DELTA0` rc 0 | 1 of 1 file exports equal | PASS |

## Controls

- Mutant pair, each arm through `check_en.py`:
  - An export mutated (`gold_root` gold/advi -> gold/advX): `FAIL-DELTA-NONZERO` rc 1 while the header check still PASSes.
  - The mark's hash mutated: `FAIL-HEADER` rc 1 while the DELTA=0 check still PASSes.
  - The file was then restored by regenerating, and `cmp` reads it byte-identical to the untouched scratch render.
- Determinism: both invocations ran twice, and the outputs are identical (6 lines, 2 of 2 PASS).
- `py_compile` rc 0, `ruff --target-version py39` clean, `ds-precommit-check` rc 0, 0 non-ASCII bytes.

## Not claimed

- No consumer was repointed; that is ADVI_FIRMBKTS FWD-3's.
- Nothing was deployed and nothing live was read.
- No consumer test exists for this carrier, so V5-AC2 is its check.

## Row and commits

- `LGIC_ENFORCE-W6-S1` (OBSERVATION, INERT): before staging, proof-of-spec-check refuses a PENDING-THIS-COMMIT row
  on a modified tracked carrier, and Rule 14a forbids pre-staging.
- The carrier was therefore committed alone at `efacdee1e0`. The instance pins it there with the introduces
  token `END GENERATED [FIRM_TREES]`.
- The instance, this file, the row and the `complete` flip ride a second commit.
