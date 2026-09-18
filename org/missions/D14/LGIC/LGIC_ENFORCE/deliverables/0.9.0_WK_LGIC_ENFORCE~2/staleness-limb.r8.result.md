# LGIC_ENFORCE.TO-EN-k-38-r8 -- staleness-limb -- result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Branch:** `wk-lgic-enforce-8-2b` | **Cut from CLOUD at** `8689484c69`

## What landed

`.tools/surprise-row-gate.py` gained a SECOND limb over the rowlessness one EN-g-37 built: `_stale_open_row`
(pure) / `_stale_open_row_violations` (wrapper), wired into `check_file()`'s existing L10 precondition block,
REMEDIATION-plane only. It refuses a NEW remediation row (the slug) when an EXISTING remediation row under
the project is `remediation.state == "OPEN"`, carries a non-empty `remediation.owner`, and its own
`remediation.round` sits `STALE_OPEN_ROW_N_ROUNDS` (= 2) or more rounds behind the slug's own round.

Commits: `4450391b96` (gate), `5798b991f9` (record).

## N = 2 rounds

Measured against two things, not one:
- **This project's own cadence:** round 1 (2026-09-15T02:20Z) through round 8's cut census
  (2026-09-18 ~05:42 UTC) is ~75.5 hours across 7 round-to-round gaps, ~10.8h/round.
- **W7-S1's own numbers, as a check rather than a target:** opened `remediation.round=v1`, OPEN, owned by
  `1.0.0_SA_CTO`; first caught at round 8 -- a 7-round, 67-hour gap. N=2 would have caught it at round v3
  (2026-09-17T14:12Z), ~40 hours sooner -- i.e. N=2 was not tuned to land exactly on round 8's discovery, it
  would have fired earlier, which is the discriminator against "picked to make W7-S1 fire".

## The three verdicts of `k38-distinct`

On the SAME planted mutant (a GRADUATED item carrying its OWN remediation row, OPEN, owned, 7 rounds old),
run through the REAL `check_file()` twice -- once through EN-g-37's rowlessness function, once through
this limb's staleness function, same commit, same file:

| fact | value |
|---|---|
| `mutant_row_exists` | `true` -- the row is present in the remediation channel |
| `rowlessness_limb_verdict` | `PASS` -- EN-g-37's limb returns 0 violations for it |
| `staleness_limb_verdict` | `REFUSED` -- this limb's own violation is the ONLY entry in that run |

Had `rowlessness_limb_verdict` also read `REFUSED`, the round would have built one limb twice; it did not.

## Criteria

| id | invocation | verdict |
|---|---|---|
| K38R8-AC1 | `check_en_r8.py k38-limb-present` | `PASS-K38-LIMB-PRESENT` |
| K38R8-AC2 | `check_en_r8.py k38-controls` | `PASS-K38-CONTROLS` |
| K38R8-AC3 | `check_en_r8.py k38-distinct` | `PASS-K38-DISTINCT` |
| K38R8-AC4 | judgment, `3.0.0_SA_CVO` at L9 | `UNVERIFIABLE-BY-INSTRUMENT` (no worker verdict) |

Gate's own `--self-test`: 171 of 171 arms pass, rc=0 (156 pre-existing + 15 new, 0 regressed).
`selftest-arms`: 31 arms, 13 positive-satisfiability, 0 failures.

## Corrections made mid-flight

1. The staleness limb's own docstrings originally named `_graduated_without_row`/
   `_graduated_without_row_violations` literally in prose; the gate's own negative-control arm (checking
   that neither limb's source names the other's function) caught this on the first `--self-test` run.
   Reworded to describe the sibling limb without the literal token; re-ran clean.
2. `.scratch/k38_e2e_test.py`'s first run failed with "schema unreadable" -- the isolated scratch git repo
   had no `org/surprise_channel/schemas/` directory, so `_schema()` (which reads the STAGED INDEX, never the
   real repo) could not find `remediation_row.schema.json`. Added a copy-in step for both schema files;
   re-ran clean.

## Bounds honoured

`EN-g-37`'s limb was read (to match its pattern) and never edited. Nothing live moved. No AWS, no deploy.
The gate change is additive only (200 insertions, 0 deletions) per `git show --stat 4450391b96`.
