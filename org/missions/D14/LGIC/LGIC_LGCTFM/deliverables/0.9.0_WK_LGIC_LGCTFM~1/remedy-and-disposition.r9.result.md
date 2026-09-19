# LGIC_LGCTFM.TO-LT-m-1-r9 -- execute what is executable, disposition all seven: result

Assignee: `0.9.0_WK_LGIC_LGCTFM~1`. Worktree: `wk-lgic-lgctfm-9-1`. Branch base (base_sha, every verdict
line): `155b3bf938fbbb6e3194f8162c4459fba0a007a3`.

## Instrument confirmation

`python org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r9/check_lt_r9.py
selftest-arms` -> `VERDICT: PASS-ARMS-DISCRIMINATE`, rc=0, 19 arms driven (3 POSITIVE, 3 WIRING, 13
mutant/other), run BEFORE any record was written or any code touched.

## Population, re-derived (not inherited)

Read `ROUTED_ROW_LIVENESS_R8.json`'s `liveness.rows` (23 rows) and took every row whose `verdict ==
"STILL-LIVE"`: `S18, W1-S21, S26, W1-S30, S33, W2-S36, S41` -- 7 of 23, matching the record's own
`still_live: 7` tally. This is byte-for-byte the same set R9_BASE.json's framing table names, but it was
re-derived from the tree per the order's instruction, not copied.

## The collision (the round's own finding, re-confirmed)

Reading all seven `next_act` fields verbatim from `REMEDIATION_ROUTE_R7.json` (`0.9.0_WK_LGIC_LGCTFM~3`'s
deliverable) at base_sha showed they are not seven of the same thing:

| id | class | why |
|---|---|---|
| `S18` | UNEXECUTABLE-AS-ROUTED | routes to an arm inside `check_lt_r1.py`, round 1's PINNED fixed input of a CLOSED round |
| `W1-S21` | UNEXECUTABLE-AS-ROUTED | routes to documentation inside that SAME pinned checker's own carrier |
| `S26` | THE-ISSUERS-OWN-ACT | routed_act names `2.0.0_SA_COO~G` by serial as the verifying/disarming actor |
| `W1-S30` | EXECUTED | a one-line rendering fix on a LIVE library |
| `S33` | EXECUTED | a shortfall-naming condition fix on a LIVE library |
| `W2-S36` | NOT-A-WORKERS-ACT | a law/mechanics edit needing a same-turn broadcast this worker cannot discharge |
| `S41` | NOT-WORK-A-DECISION | routed_act's own text is "the engine's owner decides" |

## The two executed fixes

- **`W1-S30`** -- `render_plan_md()` (`lib/opal_lgctfm.py`, function at `:1953` at base_sha; the route's
  `:1762-1796` citation is stale) never rendered a package's `step_dependencies` field. Now prints
  `" (after: <ids>)"` when the field is non-empty, nothing when empty.
- **`S33`** -- `_coverage_lines()` (`lib/lgctfm_render.py`, function at `:118`) said `"-- short by N, named
  below"` whenever `involved > rows`, but the `not covered:` lines it promises are appended only per
  `not_covered` entry -- a shortfall can exist with none. Now says "named below" only when this column's
  `not_covered` list is actually non-empty, else "not itemized by the instrument".

`lib/tests/test_opal_lgctfm.py` gained one test per fix. Each was independently confirmed, OUTSIDE the
committed test module (a scratch `python -c` by-path load of the pre-fix bytes at base_sha, `.scratch/`
only, never committed), to FAIL against the OLD behaviour:

- old `render_plan_md()`: CLASSIFY's line was `"- R-1-CLASSIFY: classify it"` -- no `(after:`.
- old `_coverage_lines()`: the un-itemized case still printed `"-- short by 1, named below"`.

Whole module run: `python -m pytest lib/tests/test_opal_lgctfm.py -v` -> 4 passed, 0 failed.

## Not performed (classed, not executed)

- **`S18` / `W1-S21`** -- editing `check_lt_r1.py` would violate BOUNDS ("READ-ONLY, NOT ONE BYTE") and
  LGIC_ENFORCE round 16's additive-sibling ruling (L9/L10 upheld, `14d80144dd`, EN-m-2). Not one byte of
  that file was touched.
- **`S26`** -- no verification or disarm performed; that is `2.0.0_SA_COO~G`'s act under R-19.
- **`W2-S36`** -- no edit to CLAUDE.md or org mechanics docs; this worker has no send tool to discharge
  the law-edit broadcast surface.
- **`S41`** -- no decision taken on S3Key bucket resolution; that is the engine owner's call.

## Mechanical criteria

- `M1R9-AC1` -- `python check_lt_r9.py m1-remedy` -> `VERDICT: PASS-M1-REMEDY`, rc=0.
- `M1R9-AC2` -- `python check_lt_r9.py r9-vintage-field` -> `VERDICT: PASS-R9-VINTAGE-FIELD`, rc=0.
- `M1R9-AC3` -- `python check_lt_r9.py r9-stale-proofs` -> `VERDICT: PASS-R9-STALE-PROOFS`, rc=0 (1
  fixed-input commit since `R9_BASE.json`'s `cut_pin` `13566fbfe2`, informational only -- it is this
  round's own minting issuance `155b3bf938`; 0 proofs at risk, 0 enumerated, SET EQUALITY holds).
- `M1R9-AC4` -- judgment, recorded `UNVERIFIABLE-BY-INSTRUMENT`, routed to `3.0.0_SA_CVO` at L9, over ALL
  FIVE classes per the order's partition-quantified bar.

## Controls

- **mutant** -- backed up the committed `ROUTED_ROW_REMEDY_R9.json`, overwrote `remedy.executed` 2 -> 99
  (rows unchanged); re-run flipped `VERDICT: PASS-M1-REMEDY` -> `VERDICT: FAIL-M1-REMEDY` naming both the
  count disagreement and "the class arithmetic does not close against the rows carried"; restored the
  original committed bytes from the backup, `git status --porcelain` read clean after restore, and the
  re-run reproduced the original `VERDICT: PASS-M1-REMEDY` output exactly. FIRED-AS-EXPECTED.
- **determinism** -- two consecutive runs of each of the three commands against the unmodified committed
  record, diffed byte-for-byte: no differences on any of the three. STABLE.

## proof-of-spec-check

`python .tools/proof-of-spec-check.py org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/LGIC_LGCTFM.TO-LT-m-1-r9.remedy-and-disposition.proof_of_spec.json
M1R9-AC1,M1R9-AC2,M1R9-AC3,M1R9-AC4 --governing-order
org/missions/D14/LGIC/LGIC_LGCTFM/task-orders/LGIC_LGCTFM.TO-LT-m-1-r9.remedy-and-disposition.md` -- see
this order's `<status>` flip commit for the recorded rc.

## Not done here (BOUNDS)

No row was disarmed or dispositioned to a terminal state -- all seven remain `2.0.0_SA_COO~G`'s under
R-19, and the DISPOSITION is `3.0.0_SA_CVO`'s at L9. `check_lt_r1.py` and every pinned fixed input stayed
read-only throughout, verified by `git status --porcelain` never showing them.
