# NFRA_OPLGTW.TO-OG-v-1 -- result: independent acceptance expectations and the walkthrough protocol

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Branch:** `wk-nfra_oplgtw-1-6` (worktree `/c/tmp/wk-oplgtw-1-6`, cut from `CLOUD`
@1f03a3f209, after OG-c-1 merged) | **Work commit:** `225f241978` (LOCAL, not pushed) | **Spec:** PRD v0.2 @f0aa50dbc0,
contract v1.0 | **Decomposition:** v1 @8768f46770, cell `OG-v-1` | **Deployed:** nothing (tests and fixtures only).

## 1. Premises, re-grounded at the cut

* The tree carries the order's paths (`TREE-OK`); `infra/aws/ec2/opal-gateway/tests/acceptance/` did not exist (new).
* OG-c-1's result file is present (`deliverables/0.9.0_WK_NFRA_OPLGTW~4/closure-contract.result.md`); its section 3 is
  the closure schema the fixtures follow.
* The certified rectangle's S3-data `source_contract.types` gives the measured types; the column lists were written out
  by hand from the silver projection pins (dim_position 25, dim_balance 34, dim_asset 24, plus 5 provenance columns;
  these equal the rectangle's footer column counts of 30, 39 and 29).
* The two walkthrough input records (`1.0.0_SA_CTO~A/G-C_...`, `G-E_...`) do not exist at the cut. The protocol states
  that a walkthrough does not start until its input lands (they are what OG-v-4/OG-v-5 are HELD on).
* `app/integrations/schwab/` was not opened. No Schwab object was read, and nothing left the machine.

## 2. What was written (all under `infra/aws/ec2/opal-gateway/tests/acceptance/` unless named)

| file | what it is |
|---|---|
| `A_ROWS.json` | A1..A20, 20 of 20 contract `acceptance_ids`; 29 halves (15 machine, 14 person), 9 rows with both; every half carries expected_result, instrument and graded_by; machine halves cite `EXPECTED.json` case ids |
| `make_fixtures.py` | the seeded, deterministic generator; `seed_universe()` (the AC9 scan's reference), `compose_marker()`, and `restamp()` for a harness whose emulated bucket mints its own VersionIds |
| `fixtures/` | 113 Parquet objects (dims typed as measured; `fact_*` stubs with matching row counts), 15 closure markers, `MANIFEST.json` (sha256 per Parquet file, upload order, variant intent) |
| `expect_independent.py`, `expected/EXPECTED.json` | 15 expected cases; instrument: PyArrow row read + stdlib `decimal` (prec 60), no DuckDB, no Gateway code |
| `WALKTHROUGH_PROTOCOL.md` | steps, expected observation and evidence for the 14 person-operated rows; RQ1..RQ6 for OG-v-3; the G-D and G-F record templates |
| `deliverables/0.9.0_WK_NFRA_OPLGTW~6/probes/og_v1.py` | the probe every criterion names |

**Fixture design:**
* Masters: 08242234 (SmartX) and 08335338 (BlackDiamond). Complete days 2026-07-09 and 2026-07-10 for both; the frozen
  expectation clock is 2026-07-13T14:00:00Z.
* Account 99000001 is in both masters.
* Balance rows satisfy `net_mv_plus_cash == net_mv_positions + cash_balance_settled_only` and
  `net_mv_positions == mkt_value_long + mkt_value_short`.
* Decimal edge values: type maxima (9999999999999.99, 9999999999.99999, 9999999999999.9999), one-scale-step values, and
  sums that exceed the source precision.
* Also carried: nulls in both datasets, negative values, and Unicode text of 20 codepoints / 29 UTF-8 bytes.
* Prompt-like security descriptions and six formula-like text cells, two of them with a leading whitespace or control
  character.
* Closure variants, all on SmartX, one business date each:
  * `missing`
  * `stored_qualified_over_missing` (a record that says qualified over a missing table)
  * `partial` (required `rld` absent)
  * `failed`
  * `unversioned` (an UNVERSIONED disposition and a PRESENT object with VersionId `null`)
  * `grain_mismatch` (projection parity broken)
  * `foreign_object` (an object under the other master)
  * `duplicate_grain` (an exact AND a conflicting duplicate in each dataset)
  * `stale_version` (a later object version at a pinned key)
  * `stale_date` (outside the 30-day window)
  * `legacy_only` (a v1 marker with no closure)
  * `absent` (silver objects with no marker)

## 3. Criteria -- run exactly as the order writes them, `<WS>` = `/c/tmp/wk-oplgtw-1-6`

Invocation for each: `cd /c/tmp/wk-oplgtw-1-6 && timeout 120 .venv-og/Scripts/python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~6/probes/og_v1.py AC<n>`

| id | deciding output | rc | denominator |
|---|---|---|---|
| OGV1-AC1 | `CENSUS: 20 of 20 contract acceptance_ids present ...` / `VERDICT: PASS-OGV1-AC1` | 0 | 20 of 20 ids; 29 halves |
| OGV1-AC2 | `SHARED: 1 numeric account ID(s) in both of 2 masters ['99000001']` / `VERDICT: PASS-OGV1-AC2` | 0 | 2 masters; 3 + 2 account IDs |
| OGV1-AC3 | overlap 47/47 rows, nulls 29/141, signs, 6 max-edge and 5 step-edge columns, 3 duplicate-grain objects / `VERDICT: PASS-OGV1-AC3` | 0 | 863 served decimal cells across 32 objects |
| OGV1-AC4 | `PROMPT-LIKE: 34 ...`, `FORMULA-LIKE: 96 text cells, 6 distinct; with leading whitespace/control 2` / `VERDICT: PASS-OGV1-AC4` | 0 | 2,620 non-null text cells |
| OGV1-AC5 | missing 2, partial 1, failed 1, stale 2, unversioned 1; the published validator agrees on 14 of 14 closures / `VERDICT: PASS-OGV1-AC5` | 0 | 15 markers, 14 with a closure |
| OGV1-AC6 | `forbidden 0 []`; `REPRODUCED: ... True (15 cases)` / `VERDICT: PASS-OGV1-AC6` | 0 | 3 python files, 36 import statements |
| OGV1-AC7 | `PROTOCOL: 14 of 14 carry steps, expected observation and the five evidence items` / `VERDICT: PASS-OGV1-AC7` | 0 | 14 person-operated rows |
| OGV1-AC8 | per master RQ1 / RQ2, RQ3; between masters RQ4; between dates RQ5, RQ6 / `VERDICT: PASS-OGV1-AC8` | 0 | 6 questions |
| OGV1-AC9 | `FOREIGN (not from the generator's seeds): 0 []` / `VERDICT: PASS-OGV1-AC9` | 0 | 129 files (113 Parquet, 16 JSON); 4,655 cells; 7,009 JSON strings |

## 4. Controls (each fired)

* **Mutants, 9 of 9 fired:** each tampers a scratch copy (`.scratch/mut/`) and runs the probe with `--acceptance-dir`:
  * M1: a non-seed account ID -> AC9 FAIL.
  * M2: the shared account removed from BlackDiamond -> AC2 FAIL.
  * M3: a `sys.path` injection into the forbidden package plus `import duckdb` -> AC6 FAIL.
  * M4: A10's evidence without `ofid_` -> AC7 FAIL.
  * M5: A20 dropped -> AC1 FAIL.
  * M6: the between-dates questions removed -> AC8 FAIL.
  * M7: the unversioned variant given a VersionId -> AC5 FAIL.
  * M8: the duplicate-grain rows removed -> AC3 FAIL.
  * M9: prompt- and formula-like text neutralised -> AC4 FAIL.
* **Published validator as a second instrument (AC5):** OG-c-1's `validate_closure` returns the built status and finding
  classes for all 14 closures. The expectations in `EXPECTED.json` were written by hand, not taken from it.
* **Second instrument for AC6:** `comp-find 'integrations.schwab|import duckdb|from duckdb'` over the authored paths
  found 4 hits across 22 text files scanned (113 binary files not searched). All 4 are prose disclaimers; there are 0
  import statements.
* **Determinism:**
  * The generator ran four times (two scratch runs, the worktree run, and a rerun after the ASCII fix below) and every
    run was byte-identical (`diff -r` clean).
  * `EXPECTED.json` was regenerated byte-identical, and the probe re-derives it in process (AC6).
  * The nine criteria ran three times.

**Two defects of my own, fixed before commit and recorded:**
* **The probe's first AC6 run FAILED.** An extra constant limb flagged the prose disclaimers as path constants. It was
  narrowed to paths handed to a call or joined with `/`, and M3 proves it still fires on a real injection.
* **The first commit-gate run WARNed about non-ASCII at `make_fixtures.py:92`.** The Unicode test string's escapes had
  been written as literal characters. The line was rewritten with `chr()`, and fixtures and expectations regenerate
  byte-identical.

## 5. Surprise rows filed (`INVESTIGATION_v1.md`, committed at 225f241978)

* `NFRA_OPLGTW-W6-S1` (OBSERVATION/INERT): `operated_by` as one value cannot express the nine rows proved in both a
  machine cell and a walkthrough, or A13's live-arm grading. Each row is written as halves.
* `NFRA_OPLGTW-W6-S2` (OBSERVATION/INERT): no carrier declares a unique grain per dataset. The duplicate-grain day
  carries exact duplicates, so it is a duplicate under any grain.
* `NFRA_OPLGTW-W6-S3` (OBSERVATION/**ARMED**, disarm owner `1.0.0_SA_CTO`): C3's "HEAD every named silver object" meets
  `fact_*` objects outside both Gateway roles' grants. A local green would certify a design that fails closed in AWS.
* `NFRA_OPLGTW-W6-S4` (OBSERVATION/INERT): `*.parquet` is gitignored (`infra/.gitignore:75`), so the fixtures land only
  by named force-add.

## 6. Declared limits

* The Gateway application was not run: the integrated local run is OG-v-2's, and the real-data sealing is OG-v-3's.
* The two record templates are in protocol section 5. Their landed homes (`deliverables/2.0.0_SA_COO~O/`) are outside
  this order's paths.
* Some expectations are an accepted set of error codes, not one code, where the PRD does not pin a code (for example
  `INCOMPLETE_SNAPSHOT` or `UNAVAILABLE` for an incomplete date). Every such case still forbids any success or partial
  total.
