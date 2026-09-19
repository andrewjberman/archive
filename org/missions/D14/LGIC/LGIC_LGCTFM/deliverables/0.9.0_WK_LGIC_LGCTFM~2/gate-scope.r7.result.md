# LGIC_LGCTFM.TO-LT-g-1-r7 -- gate-scope -- result (0.9.0_WK_LGIC_LGCTFM~2)

Cell `LT-g-1`, round 7. Re-measures `LGIC_LGCTFM-W2-S1` (round 2, ARMED and BLOCKING, disarm_owner
`1.0.0_SA_CTO`): "DEC-9's MARK COMMIT AND THE ENGINE'S OWN RUN ARTIFACTS ARE NOT COMMITTABLE AT DEC-12's
RUN HOME" -- `.tools/naming-gate.py` in ENFORCE mode refusing `contract.json`, `plan.json`, `PLANT.json`,
`PLANT_UNTYPEABLE.json` and `MARK.json` wholesale.

## The finding

The gate no longer refuses these paths. `1.0.0_SA_CTO`'s R-35 fix (commit `5fd4251792`,
2026-09-17T18:40:15-04:00) added `RUN_ARTIFACT_RE` (`naming-gate.py:96`, matched through
`_is_record_tree`/`_is_run_artifact` at `:719-725`), exempting any path shaped like
`workflows/<engine>/<subject>/<8-digit>T<6-digit>Z-<7..40 hex>/...` from grading before any literal is
ever read. That fix is an ANCESTOR of this round's `cut_pin` `ed073a4d48` (verified with
`git merge-base --is-ancestor 5fd4251792 ed073a4d48`) -- it landed before the round-7 cut, so the
round-2 refusal this cell was asked to re-measure was already closed at issuance time.

Live invocation against the real DEC-9 mark commit's five added files (the diff of `3ea3fec204`'s
`MARK.json`, `contract.json`, `plan.json`, `PLANT.json`, `PLANT_UNTYPEABLE.json` under
`workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/`):

```
python .tools/naming-gate.py --diff .scratch/mark_commit_diff.patch --enforce
DENOMINATOR: 5 path(s) in this diff; declaration-tree domain = 5 MINUS EXCLUDED(org/, docs/, run-artifact
dirs ^workflows/[^/]+/[^/]+/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40}/) 5 = 0 path(s) [of the excluded, 5 are run
artifacts and 0 are org//docs/]
COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set
and not .gitattributes); 0 seen
NAMING-GATE: PASS 0 graded
rc=0
```

Corroborated independently: commit `3ea3fec204` (this same worker, made AFTER the R-35 fix) landed these
exact 5 files at HEAD through `bash .tools/safe-commit.sh` (which calls this same `naming-gate.py
--enforce`) with zero naming-gate lines; `git status --porcelain` on them is clean and `git ls-files`
finds all 5 tracked. All 6 run directories under `workflows/legacy_transform/blackdiamond-49financial/`
follow the same timestamp-hash shape and are committed clean.

**Scoping control** (proves the exemption is a scoped run-directory carve-out, not the gate going silent
on the whole tree): a synthetic hand-authored file placed one directory level OUTSIDE the run-id shape
(`workflows/legacy_transform/blackdiamond-49financial/scratch-probe.json`, not committed), carrying the
same legacy literal the round-2 row named (`opal-data-bd`), still REFUSES:

```
NAMING REFUSE workflows/legacy_transform/blackdiamond-49financial/scratch-probe.json:2 opal-data-bd -> opal-data-49financial
  why: NEW and ALIAS as S3_BUCKET: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial')
NAMING-GATE: REFUSE 1 graded
rc=1
```

So where a refusal DOES occur in this tree, the basis is CONTENT (the string value inside the file), not
FILENAME or PATH alone -- it is the run-id-shaped DIRECTORY that now stops the literal from ever being
read under DEC-12's actual run home.

## The record

`GATE_SCOPE_R7.json`: `gate_scope.refused = []`, `refused_denominator = 5`, the gate's own verbatim
aggregate output line, the R-35 exclusion predicate named at `file:line`, `refusal_basis = ""` (no
refusal to classify), an admitting control (the same invocation's exclusion of `MARK.json`, corroborated
by commit `3ea3fec204`), a `scoping_control` (canonical field: `{path, verdict, refused: true}`) proving
the guard still refuses a hand-authored path in the same tree, and `gate_pin = 5fd4251792`.

## RE-GRADE: the arm is repaired (`13bbe12343`)

The first cut's `core_gate_scope` required a NON-EMPTY `refused` set, so a genuinely-empty one -- the
true measurement above -- could not be satisfied by any correct artifact. `0.9.0_WK_LGIC_LGCTFM~2`
measured 0 of 5 refused, filed `LGIC_LGCTFM-W2-S45` BLOCKING rather than manufacturing a refusal, and did
not flip its order; that finding stands and its row stays open. `1.0.0_SA_CTO` repaired the arm at
`13bbe12343` to admit a second branch: **(B) the gate no longer refuses** -- an EMPTY refused set is
admissible when the record carries `why_zero`, the excluding predicate at `file:line`, and a
`scoping_control` proving the gate still refuses something in the same tree. The evidence in this
record was already exactly that shape (the scoping-control probe was produced unprompted at the first
cut); this pass only lifted it into the arm's canonical field name (`gate_scope.scoping_control`,
`check_lt_r7.py:136`), keeping the prior descriptive key alongside it. **No measurement was re-run or
changed.**

## Criteria

Every invocation below ran from `<WS>` =
`/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-lgctfm-7-2b` against the checker at
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r7/check_lt_r7.py`.

- **G1R7-AC1** (`g1-scope`): **PASS-G1-SCOPE**, rc=0 (re-run after the arm repair; was FAIL-G1-SCOPE at
  the first cut, on the arm's own structural defect, not a record defect). Branch (B): `refused paths: 0
  (denominator 5)`, `why zero` and `scoping control (still REFUSED, so the guard is live)` both present
  and read clean. `LGIC_LGCTFM-W2-S45` (filed against the first cut's defect) stays open; disposition is
  `3.0.0_SA_CVO`'s.
- **G1R7-AC2** (`r7-vintage-field`): PASS-R7-VINTAGE-FIELD, rc=0. 3 records present in this checkout
  (`LT-n-3`, `LT-g-1`, `LT-r-3` -- this worktree branches off `13bbe12343`, the round-7 drain, so all
  three cells' records are present, per S106's checkout-scoped population), 6 of 6 fixed inputs named and
  resolvable.
- **G1R7-AC3** (`r7-stale-proofs`): PASS-R7-STALE-PROOFS, rc=0. 2 commits since `cut_pin` touched the
  watched path (informational: the r7 issuance commit and the arm repair `13bbe12343`); proofs-at-risk =
  0 for all three cells, each record's `proofs_re_run` = 0 -- set equality holds.
- **G1R7-AC4**: judgment, no self-graded verdict. Recorded in the proof instance for `3.0.0_SA_CVO` at
  L9: what is checkable (the gate output is literal and re-runnable at the stated pin; the predicate is
  the line that actually short-circuits grading; the admitting control ran through the same invocation)
  and what is not (an old-gate negative control timed out at the 120s bound and was not retried past one
  timeout, so it is INCOMPLETE evidence, not a fired negative control -- the R-35 commit's own message and
  the current source's absence of `RUN_ARTIFACT_RE` at the prior pin corroborate the same mechanism
  independently).

## Row filed

`LGIC_LGCTFM-W2-S45`, BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~G`, spliced into
`org/missions/D14/LGIC/LGIC_LGCTFM/surprise-channel/investigations/INVESTIGATION_v1.md` (id one above the
highest `S<k>` at write time, `S44`; coordinate `W2` matches this worker's own slot `~2`, per
`surprise-row-gate`'s refusal on the first attempt naming `W7`). Unchanged by this re-grade -- its
disposition is `3.0.0_SA_CVO`'s.
