# NFRA_OPLGTW.TO-OG-v-6 -- result: sealed question set v2

**Worker:** `0.9.0_WK_NFRA_OPLGTW~10` | **Branch:** `wk-NFRA_OPLGTW-10` (worktree `C:/tmp/wk-oplgtw-10`) | **Spec:** PRD
v1.1 C3, contract v1.3 | **Cell:** `OG-v-6` (decomposition addendum R2-E, item E4). Contains no customer value: counts,
hashes, VersionIds, dates and booleans only.

## 1. Dates (step 1)

`D_NEW` = **2026-09-25**, the newest date whose closure marker has `closure.status == "qualified"` in both masters
(markers exist through 2026-09-25 in both). `D_PREV` = **2026-09-24**, the qualified date immediately before it in both
masters. Each marker's VersionId, LastModified and closure id are in `GRAIN_DECLARATION.json` under `markers`, and again
in `SEALED_EXPECTED_V2.json`. Each date's marker has 10 versions; the recorded one is the `IsLatest` version at the run
(row `NFRA_OPLGTW-Z-W10-S4`). Both dates are literal in every question (ruling R-OG-12).

## 2. Grains, measured (step 2)

Declared grain (source column names, inlined by the order): `dim_position` = (account_id, cusip, l_s); `dim_balance` =
(account_id); `dim_asset` = (cusip). 12 of 12 snapshots read by VersionId (the VersionIds come from each marker's
`closure.tables[<dataset>].object`).

| dataset | snapshots | HOLDS | COLLIDES | colliding keys per snapshot | extra rows per snapshot |
|---|---|---|---|---|---|
| dim_position | 4 | 0 | 4 | 10 | 13 |
| dim_balance | 4 | 4 | 0 | 0 | 0 |
| dim_asset | 4 | 0 | 4 | 1 | 22 (SmartX), 24 (BlackDiamond) |

Each snapshot's row count equals the row count its own marker declares. For every COLLIDES snapshot the smallest
superset of contract columns unique on it is recorded as a CANDIDATE (one extra column suffices on 8 of 8; no key value
is recorded). Adopting a grain is a spec decision for `1.0.0_SA_CTO~O`. Rows `Z-W10-S1` and `Z-W10-S2`.

## 3. Questions (step 3) -- `WALKTHROUGH_PROTOCOL.md` section 4, RQ2-1 to RQ2-7

| kind | ids | dataset | sealed as |
|---|---|---|---|
| units | RQ2-1 | dim_position (BlackDiamond, D_NEW) | C3 refusal `duplicate_source_grain`, plus the described decimal scales |
| units | RQ2-2 | dim_balance (BlackDiamond, D_NEW) | values: sums, sign of each sum, negative-account counts, scale, of `mkt_value_long` and `mkt_value_short` |
| balance_overlap | RQ2-3 | dim_balance (BlackDiamond, D_NEW) | three sums reported separately, no total (round 1's RQ3 at D_NEW) |
| between_dates | RQ2-4 (SmartX), RQ2-5 (BlackDiamond) | dim_balance (D_PREV and D_NEW) | two snapshot sums and an exact decimal delta of one field |
| between_masters | RQ2-6 | dim_balance (D_NEW) | two snapshot sums, no combined total |
| paged_read | RQ2-7 | dim_position (BlackDiamond, D_NEW) | C3 refusal `paging_refused_no_unique_grain` |

The units question the order describes (quantity against value for one (cusip, l_s) group, sign on a short group) sits on
`dim_position`, which COLLIDES on every measured snapshot, so the C3 rule makes RQ2-1's expected answer a refusal. Value
units (sign, scale) are exercised with real values on `dim_balance` in RQ2-2 (BlackDiamond holds a negative
`mkt_value_short`; SmartX holds none). Row `Z-W10-S1`. Protocol edits: section 4 paragraph and table, A7 step 2 (:107)
and the seal and date at :111, nothing else (the stale references elsewhere in the file were row `Z-W10-S3`; see section 9).

## 4. Seal (steps 4 and 5)

`compute_expected_v2.py` was run once (`OK: sealed 7 of 7 questions`). Instrument: pyarrow Parquet decode only, exact
`decimal.Decimal` arithmetic, `sha256(salt || canonical_json(answer))`, a fresh `secrets.token_hex(32)` salt; it does not
read or import `app/integrations/schwab/`. Pre-seal absence record, taken by the sealer as its first act at commit
`d292b6c0b9`: G-D record `git cat-file -e HEAD:<path>` rc 128 = ABSENT (also ABSENT at the `CLOUD` tip
`b75c94aa8e`); G-C record rc 128 = ABSENT at that HEAD (the order allows either); positive control (a path known present)
rc 0. The seal commit is `0f88790148`, a descendant.

## 5. Copy of record in SSM (step 6)

`/opal/nfra_oplgtw/ogv6/seal_v2_20260928/{RQ2-1..RQ2-7, SALT}`, 8 of 8 SecureString, each read back with decryption and
its sha256 equal to the local bytes (`SSM_COPY_RECORD.json`: names, byte lengths, booleans). Values reached the CLI via a
short-lived file under the worktree `.scratch/` (a path with no space), removed immediately.

**Retention.** The local salt and plaintext answers stay in `%LOCALAPPDATA%/opal/og-salt/v2/expected/` (with the
Parquet work cache in `.../v2/work/`, which holds customer bytes). `OG-v-7` reads `expected/` at grading, and its drain
removes the whole `%LOCALAPPDATA%/opal/og-salt/v2/` directory. The SSM copy is the second copy, so a lost local salt
(row S42) is recoverable.

## 6. Criteria

| id | invocation (from the worktree root) | deciding line | denominator |
|---|---|---|---|
| OGV6-AC1 | `timeout 110 .venv-og/Scripts/python <cell>/probes/og_v6.py AC1` | `VERDICT: PASS-OGV6-AC1` (rc 0) | 12 of 12 snapshots re-read by VersionId and equal to the file |
| OGV6-AC2 | `... AC2` | `VERDICT: PASS-OGV6-AC2` (rc 0) | 7 protocol rows = 7 sealed ids; kinds units=2, between_dates=2, between_masters=1, balance_overlap=1, paged_read=1; 2 of 2 colliding questions sealed as a C3 refusal |
| OGV6-AC3 | `... AC3` | `VERDICT: PASS-OGV6-AC3` (rc 0) | 7 of 7 digests re-derived from SSM; pre-seal commit is an ancestor of the seal commit; 0 values found in 10 files against 18 SSM-held values |
| OGV6-J1 | none (judgment) | RECORDED, no verdict | graded at L9 by `3.0.0_SA_CVO~O` |

**Control.** A planted copy of one sealed answer in the cell directory turned AC3 to `VERDICT: FAIL-OGV6-AC3 value found
in a committed file` (3 values found in 11 files); the file was removed and AC3 re-passed.

**OGV6-J1, the record (no verdict).** Date alignment: RQ2-4 and RQ2-5 answer two real qualified dates in each master as
two separate snapshots and an exact delta (neither is `NONE_QUALIFIED`). Units: RQ2-2 asks sign, scale and per-field
sums for a value field beside a signed one on real values; RQ2-1 asks quantity against value and is sealed as the
refusal the C3 rule requires (row `Z-W10-S1`). Balance-field overlap: RQ2-3 reports three fields separately. Between
masters: RQ2-6.

## 7. Rows filed

`NFRA_OPLGTW-Z-W10-S1` (units question on a colliding grain), `-S2` (collision structure and candidate supersets),
`-S3` (stale OG-v-3, OG-v-4 and `C:/tmp` references left in the protocol, ARMED; disarmed by amendment A1, section 9), `-S4` (marker enumeration by version listing,
marker VersionId churn). Disarm owner `2.0.0_SA_COO~O`.

## 8. Declared exclusions

No Gateway call, sign-in or vendor API; no AWS write other than SSM PutParameter under `/opal/nfra_oplgtw/ogv6/`; no
read of the Gateway's engine; the grain of the code and the contract not changed; no live exercise of FWD-2 (that is
`OG-v-7`).

## 9. Amendment A1 (row `Z-W10-S3` disarmed)

The issuer reopened the order (commit `518cf9a3d0`) to correct five protocol lines and nothing else in
`WALKTHROUGH_PROTOCOL.md`: `:38` and `:242` the answer path is now `%LOCALAPPDATA%/opal/og-salt/actual_v2/`; `:39` and
`:111` the grader is now `OG-v-7`; `:208` the sealer is now `OG-v-6`. The seal, the SSM copy and
`SEALED_EXPECTED_V2.json` did not move. `OGV6-AC1`, `AC2` and `AC3` were re-run as written and all three print
`VERDICT: PASS-OGV6-AC<n>` (AC3: 0 values in 12 files). The commit that lands this correction disarms row
`NFRA_OPLGTW-Z-W10-S3`.
