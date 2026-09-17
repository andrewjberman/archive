# LGIC_ENFORCE.TO-EN-s-6-r3 -- the census, run to the end (round 3, cell EN-s-6): AMENDMENT 1 result and session log

Worker `0.9.0_WK_LGIC_ENFORCE~4`, worktree `.worktrees/wk-lgic-enforce-3-4`, branch `wk-lgic-enforce-3-4`,
cut from CLOUD @`b54636545d`. Everything here is LOCAL on that branch (never pushed). This supersedes this
worker's PRE-AMENDMENT result on this order (commits `4f1370701c`/`824e5da109`), which read THE CELL before
AMENDMENT 1 landed.

## The bar

- `git rev-parse --abbrev-ref HEAD` -> `wk-lgic-enforce-3-4`; `test -d org && test -d .tools` -> `TREE-OK`.
- Grant: `<paths>` -- `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`,
  `infra/logic/registry/systems.json`, `infra/logic/registry/resources.json`, `lib/opal_naming.py` -- plus
  `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/` and this order's own file.
  `check_en_r3.py` is read-only.

## What AMENDMENT 1 added and what this worker did with it

THE CELL item 4 (AMENDMENT 1, issuer `2.0.0_SA_COO~G`, 2026-09-17 ~14:5xZ, CTO ruling R-29): extend
`lib/opal_naming.py census` with `--not-judged <json file>` (a list of `{name, plane, card}`); mint a
registry row ONLY where a RAISE's owner is MEASURED from a declared source; card NOT-JUDGED where it is
not; stop at a 25-distinct-RAISE timebox and file the full list as one row.

1. **Built `--not-judged`** in `lib/opal_naming.py`: `census_judge()` now carries a `not_judged` index
   (plane, current); a matching item is CARDED -- never passed to `grade()`, never a row, never a stop -- and
   `census()` writes `carded_live`/`carded_repo` into the report's `denominators` (0 when none) and a
   top-level `not_judged` list copied verbatim from the file. Any RAISE on a name NOT in the file still
   stops the run (verified: the run below stops on `astn-wsjft-orchestrator-errors`, which is not in
   `NOT_JUDGED_S6.r3.json`).
2. **Minted ONE registry row**, the only RAISE with a measurable owner: `infra/logic/registry/resources.json`
   `{"name": "inf-otp-relay-api", "type": "API_GW", "system": "advi", "evidence": "infra/aws/terraform/inf-pipeline/api-gateway.tf:24-38 @422a3c724c, resource aws_apigatewayv2_api.inf_otp_relay ..."}` --
   measured from a declared Terraform source, the same `advi`/inf-pipeline standard every neighboring row in
   that file already carries. `python lib/opal_naming.py validate` -> `VALIDATE: OK 25 system row(s), 9
   scope row(s), 17 warning(s) at registry@26623a452ff8583d`.
3. **Carded 2 further RAISEs NOT-JUDGED** (owner unmeasurable from any declared source):
   `sentiment-query-api` (a token absent from EVERY registry carrier, not merely unresolved -- no `tf_file`,
   no Terraform tree, `DIRECTIVES.yaml` 0 hits) and `trade-submission-api` (the token `trade`, already
   MEASURED unresolved by `EN-r-5-r3` on the same registry commit). Cards: `OWNER_CARDS_S6.r3.md`. Carrier:
   `NOT_JUDGED_S6.r3.json`.
4. **Re-ran; hit a THIRD RAISE**, `astn-wsjft-orchestrator-errors` (CW_ALARM), on the token `astn` -- also
   already MEASURED unresolved by `EN-r-5-r3`.
5. **Measured the timebox before minting further.** A direct-library sweep (`census_live()`+`census_repo()`
   items, `grade()` called on every one without stopping at the first `RaiseDefect` -- the SAME function
   `census_judge()` calls, run without its stop-on-first-RAISE behavior) at registry@`26623a452ff8583d`
   finds **462 RAISE occurrences, 351 distinct (plane, type, name) triples, 248 distinct names** still ahead
   -- `RAISE_POPULATION_S6.r3.md`, token breakdown + full list. **462 > 25 by more than an order of
   magnitude**, on the FIRST re-run past the original stop. Per THE CELL's own clause: minting/carding stops
   here; filed as row `LGIC_ENFORCE-W4-S6`; FWD-5 goes to round 4 on the full list.

## What was built (final artifacts)

1. **`NAMING_CENSUS_REPORT.r3.md`** -- re-run with `--not-judged NOT_JUDGED_S6.r3.json`. rc=3 (stopped on
   `astn-wsjft-orchestrator-errors`). `judged_live` 21, `carded_live` 2, `live_nameable` 1828; `judged_repo`
   0, `carded_repo` 0, `repo` 1878.
2. **`NAMING_CENSUS_COMPARISON.r3.md`** -- recomputed against the new report: N2 (45) -- 3 names compared, 3
   agree (`opal-portal-data-proxy-api`, `opal-stitch-produce`, `Inflection-SilverChain-DimConversionFailure`);
   N6 (88) -- 6 names compared, 2 agree, 4 disagree (`inf-otp-relay-api` and `ExecIncrParityFailure` differ
   only in CANONICAL FORM -- N6 pre-dates this cell's registry mint / a tokeniser hyphen difference;
   `estate-report-seam-freshness-publisher` and `semantic-clustering-lambda-build` differ in VERDICT -- N6
   RAISEd on tokens (`estate`, `semantic`) the current registry now resolves). Same fenced-json shape as
   round 2's/the pre-amendment comparison (`census`, `against.N2`, `against.N6`, plus `disagreements`).

Filed row `LGIC_ENFORCE-W4-S6`: the timebox measurement above, with the full RAISE list as evidence.

## Criteria

| id | subcommand | rc | verdict |
|---|---|---|---|
| S6R3-AC1 | s6-live-complete (on the report) | 1 | FAIL-S6-LIVE-STOPPED-ON-RAISE |
| S6R3-AC2 | s6-repo-complete (on the report) | 1 | FAIL-S6-REPO-STOPPED-ON-RAISE |
| S6R3-AC3 | s6-no-placeholder (on the report) | 1 | FAIL-S6-PLACEHOLDER-IN-REPORT |
| S6R3-AC4 | s6-comparison-arithmetic (on the comparison) | 1 | FAIL-S6-COMPARISON-NOT-OVER-REAL-POPULATION |
| S6R3-AC5 | (JUDGMENT, `3.0.0_SA_CVO`) | n/a | `UNVERIFIABLE-BY-INSTRUMENT`; see comparison sections 5-6 |

**0 of 4 mechanical criteria PASS**, exactly the outcome THE CELL's own ACCEPTANCE text states in advance
("All four arms read RED at the cut"). The run now judges 21 names + cards 2 (up from 3 pre-amendment) and
resolves `inf-otp-relay-api`'s placeholder, but still stops (now on `astn`, a token the AMENDMENT's own
timebox says this cell cannot mint its way past), still carries 8 OTHER `{system}` placeholders (unresolved
tokens `inf`/`opsec`/`exec`/`portfolio`/`semantic`), and the comparison's embedded census is therefore still
incomplete.

## Controls

- **Positive control (discrimination):** `check_en_r3.py`'s own `selftest-arms` corroborates cell 6's arms
  independently (synthesized COMPLETE fixtures PASS all four subcommands; round-2-numbers fixtures FAIL as
  designed) -- 10 of 10 cell-6 sub-checks OK, confirming the FAILs above are driven by THIS run's real state,
  not a checker that always fails.
- **Mechanism control:** the `--not-judged` file deliberately excludes `astn-wsjft-orchestrator-errors`;
  the run RAISEs and stops on it exactly as `census_judge()`'s docstring states ("a RAISE on any OTHER name
  still stops the run") -- a negative control on the new code path, not just the positive fixtures.
  Separately, `python lib/opal_naming.py validate` reads OK after the mint (no schema refusal), and a
  registry validate re-run with `sentiment-query-api`/`trade-submission-api` still absent from every
  registry carrier confirms the two cards were not silently minted as rows.
- **Determinism:** all four real invocations re-run a second time (pre- and post-commit `6c87bd0968`);
  4 of 4 identical verdicts both times. The census run itself is not re-run for determinism (its live plane
  is a fresh `comp-find --corpus aws` pull whose vintage/node count move with the estate; this round's two
  live pulls, 13:49:55 UTC pre-mint and 14:41:29 UTC post-mint, differ by exactly 1 node -- 2191 -> 2190 --
  unrelated to this cell's own writes).

## Rows filed

`LGIC_ENFORCE-W4-S6` (OBSERVATION, INERT) -- the timebox measurement: 462 RAISE occurrences / 351 distinct
triples / 248 distinct names ahead of the third stop, dominated by the same three already-unresolved tokens
(`news` 114, `trade` 50, `astn` 35) plus unrelated S3-key path segments; minting/carding stops here per THE
CELL's own clause; `RAISE_POPULATION_S6.r3.md` is the full list. (Row `LGIC_ENFORCE-W4-S5`, filed by this
worker's pre-amendment spawn, stands unchanged -- it recorded the original `sentiment-query-api`/
`inf-otp-relay-api` stop, now superseded in FACT by this commit's mint+card but not retracted, per the
channel's append-only rule.)

## Limits

- No further registry edit was attempted past the timebox: `infra/logic/registry/systems.json` and further
  `resources.json` rows for the 248 distinct RAISE-hitting names are round 4's, per THE CELL's own clause.
- The comparison's "uncompared" reason is uniform across the 124 hand rows the census never reached (plus the
  1 carded name N6 also grades, `trade-submission-api`) rather than per-row; `S6R3-AC5` leaves the adequacy
  of a uniform reason to `3.0.0_SA_CVO`.
- IV7 is included in the comparison for shape parity with round 2's document but is not required by
  `check_en_r3.py`'s `s6-comparison-arithmetic` and is not named in this order's `<expected_criteria>`.

## Commits (LOCAL on wk-lgic-enforce-3-4)

- `lib/opal_naming.py` (`--not-judged`), `infra/logic/registry/resources.json` (the `inf-otp-relay-api`
  mint), `NAMING_CENSUS_REPORT.r3.md`, `NAMING_CENSUS_COMPARISON.r3.md`, `OWNER_CARDS_S6.r3.md`,
  `NOT_JUDGED_S6.r3.json`, `RAISE_POPULATION_S6.r3.md` and the surprise row (`INVESTIGATION_v1.md`),
  committed at `6c87bd0968`.
- This file and the proof instance (pinning the artifacts' commit hash) -- committed second. No `<status>`
  flip: four of five criteria are FAIL or judgment, none PASS.
