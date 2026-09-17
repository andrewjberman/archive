# LGIC_ENFORCE.TO-EN-s-6-r3 -- the census, run to the end (round 3, cell EN-s-6): result and session log

Worker `0.9.0_WK_LGIC_ENFORCE~4`, worktree `.worktrees/wk-lgic-enforce-3-4`, branch `wk-lgic-enforce-3-4`,
cut from CLOUD @`b54636545d`. Everything here is LOCAL on that branch (never pushed).

## The bar

- `git rev-parse --abbrev-ref HEAD` -> `wk-lgic-enforce-3-4`; `test -d org && test -d .tools` -> `TREE-OK`.
- Grant: `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md` (the
  `<paths>` block), plus `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/` and this
  order's own file. `check_en_r3.py` and the registry files are read-only.

## Premise re-grounded

The order states round 2 STOPPED on `sentiment-query-api` (R1.f) with `judged_live 3 of live_nameable 1821`,
`judged_repo 0 of repo 1878`, and a `{system}` placeholder. Running the ordered command fresh at this round's
HEAD reproduces the SAME stop, at the same name and step, with the estate's live count moved (1821 -> 1829
nameable; 1878 repo unchanged):

```
CENSUS LIVE: 2191 node(s) at VINTAGE Built from the estate as of 2026-09-17 13:49:55 UTC ... manifest: 0dd53f50b7da; 346 of NOT GRADED types, 16 aws_fixed; 1829 to judge
CENSUS REPO: 1878 name(s) from 473 .tf file(s) and 468 source file(s); 2864 vendored file(s) excluded
CENSUS RAISE live API_GW sentiment-query-api -- R1.f: 'sentiment' is in no vocabulary; no registry row resolves it
CENSUS: STOPPED on the first RAISE after 3 judged: live API_GW 'sentiment-query-api'
```

Direct registry reads confirm the cause is unchanged: `infra/logic/registry/systems.json@23980d3fbe` carries
`sentiment` in NONE of `systems`, `refused_keys` (workstream_code/generic_noun/purpose_word/retired) or
`unresolved` (which holds only `astn`, `trade`, `news`); `infra/logic/registry/resources.json@b15ed01ee6`
carries no `(name='inf-otp-relay-api', type='API_GW')` row, so `grade()` fills `{system}-inf-otp-relay-api`
verbatim, the same defect row `LGIC_ENFORCE-W2-S10` first recorded in round 2.

## What was built

Two documents, run to the end of what the estate allows -- no registry edit (outside `<paths>`, BOUNDS
forbids it):

1. **`NAMING_CENSUS_REPORT.r3.md`** -- `python lib/opal_naming.py census --live --repo --report <path>`, run
   verbatim, unchanged, instrument untouched. rc=3 (stopped on the RAISE above).
2. **`NAMING_CENSUS_COMPARISON.r3.md`** -- the census's totals set beside LGIC_NAMING's N2 worked cases (45,
   measured fresh from `GRADING_RULE.md@7c1e9ffb26`'s section-9 json, re-counting the verdict mix rather than
   carrying round 2's table forward -- OUT-OF-PATTERN/RAISE moved 18/4 -> 20/2 since the file was re-cut) and
   N6 grader rows (88, `n6-grader-a.tsv@388b07f486`, unchanged). Census block copied verbatim from this
   round's own report. Same fenced-json shape as round 2's comparison (`census`, `against.N2`, `against.N6`,
   each with `hand_population`, `compared`, `uncompared_hand_rows`), plus IV7 for shape parity.

Filed row `LGIC_ENFORCE-W4-S5`: the RAISE and the placeholder both persist unresolved across three rounds;
no registry edit made here (outside this cell's grant).

## Criteria

| id | subcommand | rc | verdict |
|---|---|---|---|
| S6R3-AC1 | s6-live-complete (on the report) | 1 | FAIL-S6-LIVE-STOPPED-ON-RAISE |
| S6R3-AC2 | s6-repo-complete (on the report) | 1 | FAIL-S6-REPO-STOPPED-ON-RAISE |
| S6R3-AC3 | s6-no-placeholder (on the report) | 1 | FAIL-S6-PLACEHOLDER-IN-REPORT |
| S6R3-AC4 | s6-comparison-arithmetic (on the comparison) | 1 | FAIL-S6-COMPARISON-NOT-OVER-REAL-POPULATION |
| S6R3-AC5 | (JUDGMENT, `3.0.0_SA_CVO`) | n/a | `UNVERIFIABLE-BY-INSTRUMENT`; see comparison section 5-6 |

**0 of 4 mechanical criteria PASS.** This is the outcome the order's own ACCEPTANCE text states in advance
("All four arms read RED at the cut"): the run stops on the same RAISE round 1 and round 2 hit, and the
report's one non-CONFORMANT row still carries the `{system}` placeholder. The comparison's arithmetic closes
against both real hand populations (N2 1+44=45, N6 2+86=88) but the checker also requires the embedded census
to be COMPLETE on both planes, which this stopped run cannot satisfy.

## Controls

- **Positive control (discrimination):** synthesized complete fixtures (`.scratch/mutant/`, not committed) --
  a report with `stopped=null`, `judged_live==live_nameable`, `judged_repo==repo`, no placeholder; a
  comparison whose embedded census is complete and whose N2/N6 arithmetic closes against 45/88. All four
  subcommands PASS against these fixtures (`PASS-S6-LIVE-COMPLETE`, `PASS-S6-REPO-COMPLETE`,
  `PASS-S6-NO-PLACEHOLDER`, `PASS-S6-COMPARISON-ARITHMETIC`), confirming the FAILs above are driven by the
  real report's state, not by a checker that always fails.
- **Corroboration:** the fixed input's own `selftest-arms` prints the cell-6 arms' 10 of 10 sub-checks OK
  (4 RED-on-round-2-numbers, 4 GREEN-on-synthesized-complete, 2 traps -- arithmetic-open,
  closes-but-census-incomplete); overall `SELFTEST-ARMS: 69 of 74` (unrelated cells' arms are not this
  worker's concern).
- **Determinism:** all four real invocations re-run a second time against the committed artifacts; 4 of 4
  identical verdicts both times. The census run itself is deliberately not re-run (its live plane is a fresh
  `comp-find --corpus aws` pull whose vintage and node count move with the estate).

## Rows filed

`LGIC_ENFORCE-W4-S5` (OBSERVATION, INERT) -- round 3's fresh reproduction of the same RAISE (`sentiment`,
R1.f) and the same `{system}` placeholder (`inf-otp-relay-api`), with round-3 denominators, citing
`LGIC_ENFORCE-W7-S1` (round 1's original) and `LGIC_ENFORCE-W2-S10` (the placeholder's origin) as still
unresolved two rounds later.

## Limits

- No registry edit was made or attempted; `infra/logic/registry/systems.json` and `resources.json` are
  outside this order's `<paths>` and BOUNDS forbids editing them here.
- The comparison's "uncompared" reason is uniform across all 130 rows (the run stopped before reaching any
  of them) rather than per-row; `S6R3-AC5` leaves the adequacy of a uniform reason to `3.0.0_SA_CVO`.
- IV7 is included in the comparison for shape parity with round 2's document but is not required by
  `check_en_r3.py`'s `s6-comparison-arithmetic` and is not named in this order's `<expected_criteria>`.

## Commits (LOCAL on wk-lgic-enforce-3-4)

- `NAMING_CENSUS_REPORT.r3.md`, `NAMING_CENSUS_COMPARISON.r3.md` and the surprise row
  (`INVESTIGATION_v1.md`), committed first, at `4f1370701c`.
- This file, the proof instance (pinning the artifacts' commit hash) -- committed second. No `<status>` flip:
  four of five criteria are FAIL or judgment, none PASS.
