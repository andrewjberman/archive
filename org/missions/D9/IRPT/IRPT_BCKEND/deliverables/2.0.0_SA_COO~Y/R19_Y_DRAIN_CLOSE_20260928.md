# IRPT_BCKEND round 19, workstream ~Y -- drain close (2026-09-28 ~21:3xZ)

Issuer `2.0.0_SA_COO~Y`. Issuance `ecbb08548f` (2 of 2 chains). Both orders are terminal, drained, and their worktrees
and branches removed.

| order | worker | criteria (worker's proof, VALID) | drain merge |
|---|---|---|---|
| `TO-IB-yr-2` (item 8: the lookup-capture test runs from pinned fixtures in the test tree) | `~64` | Y19-2-AC1 `24 passed`; Y19-2-AC2 `COPIES-IDENTICAL 3/3` | `7b99390ae3` |
| `TO-IB-yr-1` (item 6: a saved portfolio type other than `fixed` refuses a tolerated setting before generation) | `~63` | Y19-1-AC1 `1 passed`; Y19-1-AC2 `2 passed` | `ec8f69f718` (append-only channel conflict resolved keeping both sides' rows, +25/-0) |

## Drain checks, run once by the issuer on merged CLOUD

- `env -u IRPT_LOOKUP_FIXTURE_ROOT pytest infra/aws/lambda/investor-reporting/intake/tests`: 249 passed, 1 skipped.
- `pytest infra/aws/lambda/investor-reporting/ycharts/generate/tests`: 290 passed, 30 skipped.
- `pytest org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/R19_CHECKS/test_r19_y1_pregen_static.py`: 3 passed.
- `ruff check --target-version py39` on `recipe.py`, `resident_worker.py`, `test_security_resolution.py`: clean.
  `py_compile` on `recipe.py` and `resident_worker.py`: OK.

## The real run of the outcome

- **IB-yr-1 changes resident behaviour.** The resident is served only through 2.0.0_SA_COO~P's next resident and
  generate build, under its own halves and ledger. Its real run is the first live window on that build. The run
  exercises the `fixed` arm (every portfolio the recipe creates goes through `/model_portfolios/fixed/`), and the
  deciding check is unchanged until a non-fixed type appears.
- The close record for the non-fixed refusal is the entry-point harness run above (`resident_worker` `execute` with
  replayed vendor fixtures).
- **IB-yr-2 is suite hygiene;** the drain's suite run above is its real run.

## Rows

- `IRPT_BCKEND-W63-S1` (OBSERVATION, INERT, disarmed by the worker). The issuer's own face named the proof instance by
  the `<to_id>` stem, not by the order file's basename that the gate's complete-flip search globs. It is the same class
  as W21-S1, W41-S3 and S167. The issuer's correction applies to every later ~Y order: name the instance
  `<order file basename>.proof_of_spec.json`.
