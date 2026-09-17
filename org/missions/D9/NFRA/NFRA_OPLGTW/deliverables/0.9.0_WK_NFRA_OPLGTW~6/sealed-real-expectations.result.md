# NFRA_OPLGTW.TO-OG-v-3 -- result: real-data expected answers, sealed by hash

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Branch:** `wk-nfra_oplgtw-6e` (worktree `C:/tmp/wk-oplgtw-6e`, cut from `CLOUD`
@4c179f1826) | **Spec:** PRD v0.2 @f0aa50dbc0 (C3), contract v1.0 | **Decomposition:** v1 @8768f46770, cell `OG-v-3` |
**Deployed:** nothing. No write, copy or delete in AWS; three GetObject-by-VersionId reads only.

## 1. Premises, re-grounded at the cut

* The tree carries the order's paths (`TREE-OK`).
* A prior hand-off (2026-09-16) ended with the fabric's close and left no commit. It left files outside the repo
  (`C:/tmp/nfra-oplgtw-sealed/expected/`, `C:/tmp/nfra-oplgtw-sealed/work/`) and an uncommitted script set at
  `C:/tmp/nfra-oplgtw-handoff/og-v-3-partial/scripts/`. **Nothing there was trusted as-is.** Every VersionId, every
  parquet byte and every computed value was re-derived independently before use (section 2).
* `OG-c-2`'s result file (`deliverables/0.9.0_WK_NFRA_OPLGTW~4/producer-deploy-replay.result.md` section 1) names the
  replayed business date `D_r = 2026-09-15` for both masters and the two closure-record VersionIds; its
  `replay/silver_versions_after.json` names the 29 versioned silver objects, of which this cell's six questions need
  exactly three (08242234 dim_balance, 08335338 dim_balance, 08335338 dim_position).
* `app/integrations/schwab/` was not opened, read or imported.

## 2. Independent re-derivation of the inherited hand-off (nothing reused unverified)

1. **VersionIds.** The three VersionIds the inherited `QUALIFIED_VERSIONS.json` cited were cross-checked against
   `OG-c-2`'s own result-file table and `replay/silver_versions_after.json` (the authoritative source `OG-c-2`
   produced): all three matched verbatim.
2. **Object bytes.** Each of the three objects was re-fetched fresh by `.tools/aws s3api get-object` with its exact
   VersionId into `C:/tmp/nfra-oplgtw-sealed/work/verify_*.parquet`. SHA-256 of each freshly-fetched file equals the
   SHA-256 of the inherited cached file at the same path (3 of 3 pairs, both directions of the comparison run once):
   `08242234_dim_balance` `ee784340482202fc...`, `08335338_dim_balance` `97ccf504a88b8bcc...`, `08335338_dim_position`
   `6dc1dbbb8291f9b7...` -- all equal.
3. **Computed values (this section deliberately states no raw value -- every number below is a customer value and
   stays outside the repository per the order's bound).** A from-scratch script
   (`.scratch/independent_check.py`, not committed, and not under this worktree's tracked paths) recomputed all six
   questions with pyarrow + `decimal.Decimal` directly against the freshly-fetched bytes, independently of the
   inherited `compute_expected.py`. Every one of the 10 distinct numeric leaves across RQ1-RQ6 (the same 10 `AC3`
   counts below) matched the inherited plaintext files exactly, value for value, with zero discrepancies. The
   inherited RQ2 note's prose ("10 keys collide across 13 rows") was re-derived independently and found to describe
   the SAME fact this cell measured under a different, ambiguous phrasing (not a discrepancy) -- this cell's own
   committed script never hardcodes that count (section 4, and the fix noted there).
4. **Previous qualified date (RQ5/RQ6).** The inherited claim that no previous qualified date exists for either
   master was re-checked live: `schwab/08242234/meta/complete/date=2026-09-14.json` (re-fetched, `VersionId
   Tsx9ccaDlBPOk_NxcXTLNw4EbQudxl_H`) still carries the pre-`OG-c-1` legacy `opal.silver.complete/v1` schema, no
   `closure`/`status` key, `written_tables=[dim_asset, fact_sec]` only -- reproducing the inherited finding exactly.
   PRD C3 (`@f0aa50dbc0:159`): "Legacy markers are nonqualifying until a controlled producer replay or metadata
   backfill reconciles against original inputs and exact current output versions." `OG-c-2` is the only producer
   replay recorded for either master, and it replayed only 2026-09-15. **Own the result: nothing in the inherited work
   was accepted without this re-derivation; the re-derivation happens to agree with it in full, except one thing it
   missed (section 3).**

**Own instrument, not the inherited one.** `compute_expected.py` (committed beside this file) is this worker's own
authorship: pyarrow.parquet decode + stdlib `decimal.Decimal` summation/grouping, no pandas float aggregation, no
DuckDB, no import from `app/integrations/schwab/`. It hardcodes the three VersionIds cited in section 1 (traceable to
`OG-c-2`'s result file, never re-derived from a live "latest" read at seal time -- see section 3) and writes the
plaintext answers and salt to `C:/tmp/nfra-oplgtw-sealed/expected/` (overwriting the inherited files) and the salted
hashes to `SEALED_EXPECTED.json` beside this file.

## 3. Surprise filed: a newer qualified closure exists live in AWS (not used here)

While re-deriving the "no previous qualified date" premise, this cell's own AWS reads found that
`schwab/{08242234,08335338}/meta/complete/date=2026-09-16.json` now exist (`LastModified` 2026-09-17, i.e. AFTER the
prior hand-off's 2026-09-16 16:20 local seal), each `status: "qualified"`, `findings: []`, produced independently of
`OG-c-2` by the live production Schwab pipeline. `date=2026-09-17.json` is absent (404) for both masters as of this
row's timestamp, so 2026-09-16 is now the true latest qualified business date, not 2026-09-15.

**This cell does NOT use the 2026-09-16 closure.** The order's worker face is explicit: "compute the expected answer
from the qualified silver objects `OG-c-2` produced" and "The qualified object keys and VersionIds are in `OG-c-2`'s
result file" -- `OG-c-2` replayed and closed only 2026-09-15. Following that instruction literally (spec frozen; a
criterion is refused, never widened, when it cannot be met as written) means these sealed hashes are pinned to
2026-09-15 even though a newer qualified date now exists. Filed as `NFRA_OPLGTW-W6-S5` (OBSERVATION, **ARMED**,
disarm owner `2.0.0_SA_COO~O`): if the Gateway's catalog reports 2026-09-16 as "latest" by the time `OG-v-4` runs A7,
the real answers will not hash-match these sealed values, and RQ5/RQ6 would gain a real previous-qualified-date
(2026-09-15) instead of `NONE_QUALIFIED`. Disarm is the issuer's call (re-seal before A7, or fix 2026-09-15 as A7's
authorized business date).

## 4. A defect of my own, fixed before commit

The first draft of `compute_expected.py`'s RQ2 comment hardcoded the real collision counts (10 keys / 23 rows / 13
extra rows) as prose in a comment -- a real-data-derived value that would have been committed to the repository. It
was rewritten to describe the check generically with no literal count; the exact counts are computed at runtime and
written only to the outside-repository plaintext note (`AC3`'s scan below covers exactly this class of leak and
passed after the fix, having failed against the pre-fix draft during authoring).

## 5. Where the values live (bound, `<paths>` and BOUNDS)

**Location:** `C:/tmp/nfra-oplgtw-sealed/expected/` (outside the repository) -- `RQ1.txt` .. `RQ6.txt` (the plaintext
canonical-JSON answer per question) and `SALT.txt` (the random salt). The parquet cache the instrument reads from is
`C:/tmp/nfra-oplgtw-sealed/work/`.

**Retention:** kept until `OG-v-4` has graded the controlled walkthrough's A7 row, then removed by the COO at that
drain. This is the same statement the task order names; no separate deletion job or schedule is created by this cell
(the standing moratorium on new monitors/schedulers applies, and none was needed).

## 6. Criteria, run as the order writes them (`<WS>` = `C:/tmp/wk-oplgtw-6e`, HEAD 4c179f1826 at run time)

| id | deciding output | rc | denominator |
|---|---|---|---|
| OGV3-AC1 | `VERSIONIDS: 3 object(s) used; 3 of 3 found verbatim ...`; `RERUN: rc=0; 6 of 6 answer file(s) byte-identical across two runs`; `VERDICT: PASS-OGV3-AC1` | 0 | 3 of 3 VersionIds traced to OG-c-2; 9 import statements parsed, 0 forbidden; 6 of 6 answer files reproduced |
| OGV3-AC2 | `SEALED_EXPECTED.json: 6 question(s), 3 qualified object(s); top-level extra keys set(); per-row problems 0`; `VERDICT: PASS-OGV3-AC2` | 0 | 6 questions + 3 qualified-object rows checked against an exact key whitelist |
| OGV3-AC3 | `DENOMINATOR: 10 sealed-answer value(s) scanned across 5 committed cell file(s)`; `HITS: 0 []`; `VERDICT: PASS-OGV3-AC3` | 0 | 10 distinct real-data values x 5 committed files (including this proof-of-spec instance) = 50 checks, 0 hits |
| OGV3-AC4 | `RESULT FILE: sealed-real-expectations.result.md exists=True; states outside-repo location=True; states a bound retention policy (kept until OG-v-4 grades, then removed)=True`; `VERDICT: PASS-OGV3-AC4` | 0 | 1 result file; 2 stated facts (location, retention) |
| OGV3-J1 | judgment -- graded at L9 by `3.0.0_SA_CVO`. RQ1/RQ4 exercise date alignment (each question names its own business date, never mixed); RQ2/RQ3 exercise balance-field overlap (`net_mv_plus_cash`, `net_mv_positions`, `cash_balance_settled_only` reported separately, never summed together, per PRD C3); RQ4 exercises a between-masters comparison as two separate snapshot answers; RQ5/RQ6 exercise a between-dates comparison, correctly reporting `NONE_QUALIFIED` rather than fabricating a delta -- see section 3 for why that reading may be superseded by the time `OG-v-4` runs A7. RECORD; NO VERDICT. | N/A | N/A -- judgment row |

## 7. Controls

**Mutants, 5 of 5 fired (each on a scratch copy in `.scratch/mut/m<n>/`, run with `--cell-dir`):**
* M1: `import duckdb` injected into the scratch `compute_expected.py` -> `AC1` FAIL (forbidden import).
* M2: the SmartX dim_balance VersionId in the scratch `SEALED_EXPECTED.json` changed to a value not in `OG-c-2`'s
  deliverables -> `AC1` FAIL (VersionId not found).
* M3: an extra key (`"raw_note": "leaked"`) added to the scratch `SEALED_EXPECTED.json` top level -> `AC2` FAIL
  (extra top-level key).
* M4: RQ1's exact sealed sum value appended as a comment to the scratch `compute_expected.py` -> `AC3` FAIL (customer
  value found in a committed file).
* M5: the `**Retention:**` prose sentence removed from a scratch copy of this result file (the AC4 check's own
  probe-echoed table cell, which necessarily contains similar words, was proven NOT to satisfy the check by a second
  drift-simulation mutant that removed the bold prose sentence but left the table cell in place) -> `AC4` FAIL
  (retention policy not stated).

**Determinism:** `compute_expected.py` was run twice against the same three pinned VersionIds; all six plaintext
answer files (`RQ1.txt` .. `RQ6.txt`) were byte-identical across both runs (only `SALT.txt` and the resulting hashes
differed, as expected from a fresh random salt per run) -- see `AC1`'s own rerun check, which asserts this on every
grading run.

## 8. Declared exclusions

* Nothing under `app/integrations/schwab/` was read or imported (order bound: Independence).
* No AWS write, copy or delete was performed; three GetObject-by-VersionId reads only.
* The 2026-09-16 qualified closure and its silver objects were read only far enough to establish that they exist and
  are qualified (head-object and one get-object of the closure record itself, for the surprise row's grounding); none
  of their silver data objects were read or used in any sealed answer.

## 9. Surprise rows filed (`INVESTIGATION_v1.md`)

* `NFRA_OPLGTW-W6-S5` (OBSERVATION, **ARMED**, disarm owner `2.0.0_SA_COO~O`): a newer qualified closure
  (date=2026-09-16) now exists in AWS, produced independently of `OG-c-2`, after the prior hand-off's premise ("no
  previous qualified date exists / 2026-09-15 is the only qualified closure") was written. This cell seals against
  2026-09-15 only, per the order's explicit instruction; section 3 above.
