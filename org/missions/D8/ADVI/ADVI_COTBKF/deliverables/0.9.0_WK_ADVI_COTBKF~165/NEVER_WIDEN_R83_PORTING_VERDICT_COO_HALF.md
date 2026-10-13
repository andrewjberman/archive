# NEVER-WIDEN SIGN-OFF -- COO HALF -- DRAFT, UNSIGNED -- ADVI_COTBKF round 83, CB-ce-2: porting_verdict on the three served tables

**Status:** DRAFT. Unsigned. Nothing is applied, minted, re-minted, served or uploaded by this draft.
**Signer (to sign):** `2.0.0_SA_COO~C2` (dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2` (owed). **Applier:** a CloudOps seat (to be named by the COO).
**Drafted by:** `0.9.0_WK_ADVI_COTBKF~165` (L7 worker, CB-ce-2 of the round-83 issuance). The COO half is the COO's act; this worker does not sign it.
**Form:** as `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R27_FWD3_SERVE_COO_HALF.md`.
**Evidence:** `PORTING_VERDICT_RECORD.json` in this folder; dry-run summary `.scratch/dryrun/dryrun_summary.json` (worktree, not committed).

## 1. THE ACT AND ITS BLAST RADIUS

The act re-mints the three served FWD-3 objects with ONE column appended LAST in each table (`porting_verdict`). It is the builder's guarded
apply: `commonwealth_fwd3_serve.py --build` (writes locally) then `--apply --overwrite` (one put per key). No other object is touched.
The `--index` flag names the Yahoo store index the verdict is read from (default: the builder's address).

Keys are the builder's output (`fs.target_addresses()`, read from code, not typed):

| key (prefix of part-00000.parquet) | writers, N | change | rollback |
|---|---|---|---|
| `s3://opal-data-assets/commonwealth/cottonwood/silver/daily_returns/date=2026-06-23/` | N = 1 (the serve builder's `apply`; grep of put/upload sites naming the tables) | one column appended; existing columns unchanged | the key's VersionId BEFORE the act (section 4) |
| `s3://opal-data-assets/commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/` | N = 1 (same) | one column appended; existing columns unchanged | the key's VersionId BEFORE the act |
| `s3://opal-data-assets/commonwealth/cottonwood/silver/month_grades/date=2026-06-23/` | N = 1 (same) | one column appended; existing columns unchanged | the key's VersionId BEFORE the act |
| anything else | -- | -- | NOT SIGNED |

Measured with the code, not S3: the three keys' current served content is the round-82 build (`fwd3_serve_r34/fwd3_manifest.json`, run_commit
`728d223ddca5472884c464b0482f814bfc706f41`): daily_returns 1,691,729 rows, hash `880fd12a...`; account_day_value 21,102,041 rows, hash
`121740c1...`; month_grades 82,593 rows, hash `9ea54cb2...`. Round 82 verified the served objects equal that local copy row for row.
The appended column changes every content hash; row counts do not change.

## 2. EXPECTED OUTCOME, BOTH BRANCHES OF THE INDEX RULE

The producer's rule (`commonwealth_price_need.porting_verdicts`): a Yahoo-sourced row reads its security's verdict from the index's own
`porting_verdict` column; every other row reads NOT_YAHOO. Branches: NO_COLUMN (no column), VERDICTS (each cusip reads its verdict; a missing
cusip reads UNVERIFIED), MALFORMED (no cusip column, or a value outside UNVERIFIED | PASS | FAIL | UNTESTABLE: EVERY row reads UNVERIFIED),
UNREADABLE (the index did not read: EVERY row reads UNVERIFIED).

- **Branch A -- the index carries `porting_verdict` (VERDICTS).** rc 0; the three keys hold the built tables; each Yahoo-sourced row reads
  the verdict of its cusip (UNVERIFIED where the index does not list it); the row counts equal section 3's. NOT MEASURED: the counts per verdict,
  because no verdicts file exists yet (the live index is `LastModified 2026-10-13T03:45:15Z`, VersionId `LX3q_QpJKstC.rlcnSzs29JCuYwXTzqN`,
  326 rows, NO porting_verdict column). A branch-A act needs its own dry run and count, which this draft does not supply.
- **Branch B -- no column, or MALFORMED / UNREADABLE (the state today).** rc 0; every Yahoo-sourced row reads UNVERIFIED; the counts are
  section 3's UNVERIFIED column. A PASS is never produced on a read that did not complete.
- **Failure (either branch).** A refused put, a partial write, or a verify that does not match: restore each key to its recorded prior VersionId,
  file a row, and close the ledger ROLLED-BACK. Nothing else is written.

## 3. THE COUNTS (dry run, local copies, changed code, live index with no column; counts only)

Figure rows read against the served local copies. "Existing values changed" compares every pre-existing column, row-aligned on the keys.

| table | rows | WIDE rule: UNVERIFIED | WIDE: NOT_YAHOO | NARROW rule: UNVERIFIED | NARROW: NOT_YAHOO | WIDE: existing values changed |
|---|---|---|---|---|---|---|
| account_day_value (holding-days) | 21,102,041 | 3,709,042 | 17,392,999 | 3,648,401 | 17,453,640 | 0 (keys equal) |
| daily_returns (account-days) | 1,691,729 | 669,262 | 1,022,467 | 658,642 | 1,033,087 | 0 (keys equal) |
| month_grades (account-months) | 82,593 | 33,217 | 49,376 | 32,232 | 50,361 | NOT RE-DERIVED (see section 6) |

WIDE = `yahoo_finance` and `linear_interpolation` (ruled 10-13). NARROW = `yahoo_finance` alone. A daily or monthly row reads the WORST
Yahoo label among its holdings (FAIL over UNTESTABLE over UNVERIFIED over PASS). A row with no Yahoo-priced holding reads NOT_YAHOO.
Positive controls: the changed code re-derives the round-82 values with worst absolute difference 0.0 over 1,691,729 account-days; its per-day
price table reproduces the r34 per-day file's (cusip, date, store) set exactly (2,124,908 rows).

## 4. THE ROLLBACK, PER KEY

Before the act, the CloudOps seat records the current VersionId of each of the three keys (`aws s3api list-object-versions` or
`head-object --version-id`, at the act; NOT read by this draft, because listing is outside the grant that bounded it). The rollback is a
copy of the recorded version back over the key. The act is not given until those three VersionIds are written into the ledger entry.

## 5. CONSUMERS

Two CODE readers read the served objects, both BY COLUMN NAME, so an appended column cannot move a value they read: the ARD adapter
(`commonwealth_account_return_daily.read_source`: daily_returns by eight names; account_day_value by four; month_grades by three) and the
census (`commonwealth_price_basis_census`: account, date, cusip, close, price_source). The test
`test_the_consumers_projections_read_the_same_values_with_the_column_appended` proves the projections are equal with and without the column.
NO consumer page reads these tables (round 82's read found two code readers and no page). THE ROUTE TO A PAGE IS NOT LIVE.

## 6. NOT ESTABLISHED

- **month_grades existing values were not re-derived.** Its performance input is `commonwealth_monthly_grade.performance_prefix()`, an s3
  prefix outside this worker's grant. The change to grade_table is additive (one appended column; a test proves the existing columns are equal
  with and without the map), but the dry run did not measure the month rows against the served object.
- **The per-day price values differ from the r34 file** on 37,077 security-days (34 CUSIPs). Their ratio is a split factor per CUSIP (30 CUSIPs
  have one constant ratio; 4 vary by day). The r28 split repair (`apply_splits`) takes its split history from an S3 store the dry run may not read,
  so the dry run used the r34 price values and the new source labels. Store, presence and source are exact.
- The `source` per security-day is rebuilt in the dry run from the local store caches and the as-traded price input (`r34_price_input.parquet`).
  The local r34 per-day file carries no source column; a real build re-run writes it.
- The verdict branch A counts (section 2) are not measured.

## 7. SIGNATURES

- COO half: **UNSIGNED.** (`2.0.0_SA_COO~C2`, to sign only after the CTO half and a CloudOps applier are named.)
- CTO half: **owed** (`1.0.0_SA_CTO~DELL2`).
- Nothing in this draft was applied, minted, re-minted, served, uploaded or sent.
