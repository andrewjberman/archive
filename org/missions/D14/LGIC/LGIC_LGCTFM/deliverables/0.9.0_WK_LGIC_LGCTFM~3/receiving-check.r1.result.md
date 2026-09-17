# LGIC_LGCTFM.TO-LT-s-2-r1 -- receiving-check result (round 1)

**Cell:** LT-s-2 (the receiving checker's lgctfm-contract artifact type). **Assignee:** `0.9.0_WK_LGIC_LGCTFM~3`.
**Commit:** `4ad93b7166` on `wk-lgic-lgctfm-1-3` (LOCAL).

## What was built

- `.tools/lgctfm-contract-check.py` (new) -- the OWNING tool for the `lgctfm-contract` artifact type. Two
  passes: (1) a targeted walk of every cell-shaped field the schema requires (`trigger_denominator`'s two
  APIs, every RESOURCE/PLANE row's `current`/`desired`, every FORK row's `one_job`/`canonical_member`,
  every tension's `factors`, and `subject.vintage`), printing one line per defect naming it with one of the
  four tokens `bare-value` / `trigger-denominator` / `evidence-instrument` / `vintage`; (2) full JSON-Schema
  validation against `org/standards/LGCTFM_CONTRACT.schema.json` for anything the targeted walk does not
  name, printed as `schema: <path>: <message>`. Exit 0 with `ACCEPT lgctfm-contract: <path>` when both
  passes find nothing; exit 1 with `HAND BACK lgctfm-contract: <path>` and every defect line otherwise.
- `.tools/receiving-check.py` -- one new `ROUTES` row, labelled exactly `lgctfm-contract`, placed FIRST (no
  existing route is broader in a way that overlaps it, but the WORKER FACE's caution is honoured literally),
  matching a run's `workflows/legacy_transform/<subject>/<run-id>/contract.json` and any file ending
  `.lgctfm-contract.json`, dispatched to `lgctfm-contract-check.py` as a subprocess -- the dispatcher
  re-implements nothing. `self_test()` gained two positive classification cases (one per path shape) and one
  negative case (`workflows/legacy_transform/.../other.json` stays unclassified, confirming the pattern is
  anchored on `contract.json` and not the whole run directory).

## Acceptance (post-commit re-run, worktree HEAD `4ad93b7166`)

| id | subcommand | verdict |
|---|---|---|
| S2R1-AC1 | s2-accept-valid | PASS-S2-VALID-ACCEPTED |
| S2R1-AC2 | s2-refuse-bare | PASS-S2-BARE-VALUE-HANDED-BACK |
| S2R1-AC3 | s2-refuse-one-api | PASS-S2-ONE-API-HANDED-BACK |
| S2R1-AC4 | s2-refuse-no-instrument | PASS-S2-NO-INSTRUMENT-HANDED-BACK |
| S2R1-AC5 | s2-refuse-no-vintage | PASS-S2-NO-VINTAGE-HANDED-BACK |
| S2R1-AC6 | s2-unchecked | PASS-S2-UNKNOWN-TYPE-STAYS-UNCHECKED |
| S2R1-AC7 | s2-selftest | PASS-S2-RECEIVING-SELFTEST-GREEN |
| S2R1-AC8 | judgment | UNVERIFIABLE-BY-INSTRUMENT, for `3.0.0_SA_CVO` at L9 |

`receiving-check.py --self-test` (run directly, not through `check_lt_r1.py`) also reads `SELF-TEST: ALL
HOLD`, and `check_lt_r1.py selftest-arms` shows `s2-handback-token` and `s2-accept` PASS (the pure-core
arms driven there).

## Mutant / determinism evidence (self-supplied, beyond the fixed battery)

- Doctoring is the mutant: each of the four `s2-refuse-*` subcommands derives its input from the SAME
  `PLANTED_CONTRACT.json` `s2-accept-valid` uses, breaking exactly one field. `s2-accept-valid` is the
  positive control the four negative arms are read against.
- Re-ran `s2-accept-valid` and `s2-refuse-bare` twice each; byte-identical stdout both times (the checker
  has no non-determinism -- no timestamps, no set-ordering-dependent output beyond `sorted()` calls already
  present).

## Declared exclusions

- `lgctfm-contract-check.py` does not carry its own `--self-test`; none of S2R1-AC1..AC8 asks for one (only
  `receiving-check.py --self-test`, AC7, is named), and the WORKER FACE's "Add self-test cases for it" reads
  against the ROUTE, satisfied in `receiving-check.py`'s own `self_test()`.
- The targeted walk's generic schema pass (`schema: ...` lines) is exercised incidentally by every
  `s2-refuse-*` doctored fixture (each also breaks the schema, so a `schema:` line accompanies the named
  token line) but no acceptance criterion isolates a schema-only defect the targeted walk does NOT also
  name (e.g. a bad `node_type` enum value) -- declared, not hidden; the schema in `org/standards/` and its
  own S1R1 battery (LT-s-1, drained) already cover that surface independently.
