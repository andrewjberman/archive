# NFRA_MCPINDEX.TO-MX-s-1 -- TrueShares holdings reach silver, and the guard counts them

Seat `0.4.0_DS_ClientPlatform~D`, worktree `/c/tmp/mx-s1-d`, branch `wk-mcpindex-s1-d`, cut at `b1b15be9f5`.
Source row `NFRA_MCPINDEX-W3-S2`; ruling R-4 of `ledger/ROUND_ANALYSIS.round1.md`; Andrew option 4.

**Headline: the feed is fixed, backfilled and proven in the repo, and it still converts nothing in production.**
AC1 PASSES. AC2 FAILS, and it cannot pass from this lane: the code that actually runs is a Lambda bundle six
weeks older than the converter, and rebuilding it is a DT/AE act.

---

## 1. THE CAUSE (step 1)

Two defects, stacked. Either alone is sufficient to produce "0 silver objects", which is why the tree read
healthy from every angle anyone had looked from.

**(a) The deployed bundle predates the converter.** `opal-assets-silver-etf` was last modified
`2026-07-15T23:24:02Z`, `CodeSha256 a14fYacwkjPlkj7P5qb7QGTKDeQ2A9GTnkM/t1rTxcs=`. I downloaded the zip and
recomputed its sha256 equal, so these are the running bytes, not a filename match (rule 22a). Its
`etf_conversion.py` hashes `623568f3...c56436` -- equal to `BUILD_MANIFEST.json`'s own `vendor_sha256` -- and
carries **0** occurrences of `_convert_trueshares_holdings` and no `kc.feed == "holdings"` dispatch. The
converter landed in the repo at `e442e30964` on **2026-08-24**; the bundle was built at `2705444350` on
**2026-07-15**. Bronze holdings deliveries begin 2026-08-24. The function that converts holdings has never
existed in production.

**(b) `expected_partitions_etf` hardcoded the silver feed.** One line, `etf_conversion.py:552`, mapped EVERY
trueshares bronze key to a `netassets_page` silver key regardless of `kc.feed`. That has two faces:

- `fact_holdings` never entered the expected set, so `set_identity` never marked a holdings partition MISSING
  and the sweep never dispatched a holdings key. The converter was reachable in code and unreachable in fact.
- The same absence is why the guard read `missing 0` over a tree short an entire table. **You cannot report a
  hole in a denominator you never built.** The live guard's "expected 72/73" equals the netassets count exactly.

It also collided both feeds of one date onto a single expected key.

Reproduced before touching anything: 2 bronze keys (one netassets, one holdings, same date) went in and **1**
expected entry came out.

The commit that added the converter, `e442e30964`, fixed `classify_key` to parse the feed and added the
dispatch -- and never touched `expected_partitions_etf`, its sibling hardcode. Its own subject line names the
defect class it half-fixed: *"the classifier hardcoded `netassets`, so the feed would have converted NOTHING
while reading perfectly healthy."*

### What this cause does NOT cover, checked rather than assumed

- **No S3 notification rule matches a holdings `.csv`.** The trueshares rules are prefix
  `trueshares/{DIVZ,IDVZ}/bronze/` suffix `.html`; `divz_holdings.csv` matches **0 of 11** rules, the netassets
  `.html` matches 1. This is **not** a third cause of the zero, because the sweep
  (`opal-assets-silver-etf-sweep-daily`, ENABLED, `cron(30 23 * * ? *)`) lists bronze directly and does not
  depend on the event rule. It is a latency gap: once the bundle is rebuilt, holdings converts on the nightly
  sweep rather than on delivery, unlike netassets. Filed as part of `Z-S4`.

## 2. THE FIX (step 2)

| commit | change |
|---|---|
| `6c6232a5d7` | `expected_partitions_etf` follows `kc.feed`: `"holdings" if kc.feed == "holdings" else "netassets_page"`. |
| `23efc28a2f` | `_to_arrow_etf`'s float64 parse-or-raise guarded by `not is_numeric_dtype(...)` instead of `dtype == object`. |

The second was **not** discretionary. pandas 3.0.3 on this interpreter infers a column of strings as the `str`
dtype, so `dtype == object` reads False and `_numeric_or_raise` is skipped for every float64-declared column --
the Rule 17 CAPTURED-BAD boundary the order requires. Without it the backfill would not have been Rule 17
STRICT. The deployed path is unaffected and that is measured, not assumed: partitions the lambdas wrote at
2026-09-25T22:00Z read back `float64`, reachable only through the `object` branch.

**Tests: 23 -> 28 passed, 3 skipped.** Five added, and **every one was falsified against the unfixed source**
before being trusted:

| test | fails on old code with |
|---|---|
| `test_expected_partitions_counts_the_trueshares_holdings_feed` | `assert 1 == 2` |
| `test_sweep_converts_a_trueshares_holdings_delivery` | the `fact_holdings` key absent from S3 |
| `test_guard_REPORTS_a_planted_missing_holdings_date` | planted date mapped to `fact_netassets_page` |
| `test_float64_parse_or_raise_fires_whatever_pandas_infers` | `ArrowInvalid`, not the converter's `VendorDriftError` |
| `test_float64_columns_round_trip_as_numbers_not_strings` | `Shares read back as str` |

The pathfinder 1->2 fan is asserted unchanged as a negative control (2 bronze -> 2 expected, both funds).

### The deploy clause is REFUSED, with its measurement

Step 2 says "Deploy through `.tools/safe-deploy.sh` as rule 13 requires." Measured, not predicted:

```
safe-deploy: 1 path(s) to deploy (1 script, 0 bundle-member)
  SKIP-NOT-MEMBER  [mdpf] data/assets/scripts/silver/etf_conversion.py
      probed s3://opal-data-mdpf/code/scripts/silver/etf_conversion.py -> 404
OK: safe-deploy gate PASS -- 0 file(s) deployed; 1 SKIPPED (first-mint, 404). NOTHING WAS DEPLOYED.
```

`safe-deploy` maps `data/assets/scripts/silver/` to `s3://opal-data-mdpf/code/scripts/silver/`, where this file
is not a member -- and **that S3 prefix is not how this converter runs anyway**. The running code is a vendored
Lambda zip. Rebuilding it is DT/AE under rule 13 and NEVER-9 (`update-function-code` is Terraform only). I did
not widen the criterion or meet it by an unnamed route. Row `Z-S4`.

## 3. THE BACKFILL (step 3)

Runner: `probes/mx_s_1_backfill.py` (`--list` | `--date` | `--all`), idempotent by construction
(`partition_exists` skips unless `--force`), no deletion of any object.

Before, measured: `DIVZ bronze=33 silver=0`, `IDVZ bronze=33 silver=0`.
A single date was converted first as a controlled write, its bytes read back and checked, then the rest.

**Result: `converted=66 skipped_idempotent=0 failed=0`.** Live re-read: `DIVZ bronze=33 silver=33`,
`IDVZ bronze=33 silver=33`, dates 2026-08-24..2026-09-25 contiguous on both funds.

Verified against the **artifacts**, not the runner's exit code -- all 66 partitions re-read from S3:

- **0 defects** across 66 partitions.
- 957 rows DIVZ + 1,410 rows IDVZ = **2,367 rows**.
- Every partition's `Account` set equals its own fund exactly (the converter's per-fund mis-delivery boundary).
- `Shares, Price, Market Value, Weightings, Net Assets` all numeric on read-back.
- Written parquet schema `.equals()` the declared arrow schema.

## 4. THE GUARD (step 4) -- code done, served state BLOCKED

The code change is the same one line as the cause: with `fact_holdings` in the expected set, a holdings gap
now appears as `missing`. `test_guard_REPORTS_a_planted_missing_holdings_date` plants a 07-16 delivery with a
drifted header that cannot heal, beside a converting 07-15 control, and asserts the guard reports it --
`backfill_complete false` and `"missing 1"` in its own detail line. It fails on the old code.

**AC2 FAILS live, and the reason is (a), not this fix:**

```
DIVZ: guard expected=73 missing=0 live silver=106 of which fact_holdings=33
IDVZ: guard expected=73 missing=0 live silver=106 of which fact_holdings=33
funds whose guard counts the holdings feed 0 of 2 -- RESULT: FAIL -- exit=1
```

`106 - 33 = 73` exactly: the served guard is still the stale bundle's netassets-only denominator.
`backfill-status.json` has exactly ONE writer, the sweep, which runs the deployed bytes. No DS act can move it.

### A consequence this order CAUSES, named loudly

Currently served (read before the next sweep): `trueshares/{DIVZ,IDVZ}` both `backfill_complete: true`,
`verdict PASS`, `expected 73 landed 73 matched 73 missing 0 alien 0`.

Simulating the next sweep with the **deployed** bytes against **live** state (read-only, no synthetic input):

```
trueshares/DIVZ  expected=73 landed=106 matched=73 missing=0 alien=33 -> FAIL
trueshares/IDVZ  expected=73 landed=106 matched=73 missing=0 alien=33 -> FAIL
```

`set_identity` is `PASS iff not missing and not alien`, so the 66 partitions just landed are ALIEN to the stale
guard and **both trees flip PASS -> FAIL at the next 23:30Z sweep.** The FAIL is the truer statement -- the
previous PASS was false, over a tree missing an entire feed -- but unannounced it reads as "DS broke the ETF
guard". It clears itself with no data act once the rebuilt bundle computes `expected=106`.

**Timing, so it can simply be avoided:** the sweep last ran 2026-09-25T23:30Z; the next fire is
**2026-09-26T23:30Z**. A bundle rebuild inside that window means the served verdict never flips. Row `Z-S5`.

## 5. ROWS FILED

Committed `b2df0b5aef` on CLOUD, in the shared tree (14b inverts for an append-only channel).

| row | class / hazard | what |
|---|---|---|
| `Z-S4` | BLOCKING / ARMED | deployed bundle predates the converter; no event rule matches holdings `.csv`; AC2 unreachable from DS |
| `Z-S5` | OBSERVATION / ARMED | this order's backfill flips the served guard PASS -> FAIL until the rebuild |
| `Z-S3` | OBSERVATION / ARMED | `mirror_conversion.py:330` carries the same `dtype == object` guard, 5 vendored copies -- NOT fixed here |
| `Z-S6` | OBSERVATION / ARMED | pre-existing: `pathfinder/{PFDE,PFOE}` already serve FAIL / `missing 2`, unowned |

`Z-S6` is off-task and was filed rather than chased, per CLAUDE.md section 2. Attribution was checked against
the served artifact's own LastModified, which predates the backfill -- it is not mine.

## 6. WHAT IS OWED, AND BY WHOM

1. **DT/AE** -- rebuild `opal-assets-silver-etf` from `BUILD_MANIFEST.json`'s `vendored_modules` list at the
   two commits below, and apply via Terraform. This is the single act that closes AC2 *and* disarms `Z-S5`.
   Ideally before 2026-09-26T23:30Z.
2. **DT/AE, smaller** -- decide whether a `.csv` notification rule for the trueshares holdings prefix is wanted,
   so the feed converts on delivery rather than on the nightly sweep.
3. **The issuer** -- route `Z-S3` (the shared framework guard) to whoever owns `mirror_conversion.py`.

## 7. COMPILER TOOLS

| tool | result |
|---|---|
| `comp-find` | used for every repo census (writers of `bd_assets.parquet`, the `dtype == object` pattern, `expected_partitions_etf`); denominators printed and carried into the rows |
| `comp-pipescript io etf_conversion.py` | **NOT-APPLICABLE, measured** -- `Unknown script in tree [all]: ETF_CONVERSION`. The `opal-data-assets` ETF pipeline is in no indexed tree, so the DS role minimum has no coverage here. Recorded as a gap, not a skipped check. |
| `comp-pipescript deployed` / `postdeps` | same gap, same reason -- the script resolves in no tree. |
| `safe-deploy.sh` | ran; `NOTHING WAS DEPLOYED`, SKIP-NOT-MEMBER 404 (section 2). |
| `safe-commit.sh` | 3 commits, gates clean; `surprise-row-gate` graded 4 new rows OK. |

**Gap worth naming:** the `data/assets` ETF silver pipeline is invisible to `comp-pipescript` in all three verbs.
A DS seat working this tree has no dependency-graph instrument at all, which is part of why a whole feed could
sit unconverted for a month with every tool reporting green.
