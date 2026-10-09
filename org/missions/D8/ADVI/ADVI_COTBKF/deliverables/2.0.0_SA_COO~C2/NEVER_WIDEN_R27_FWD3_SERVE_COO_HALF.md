# NEVER-WIDEN SIGN-OFF -- COO HALF (DRAFT, not yet given) -- ADVI_COTBKF: mint the three FWD-3 silver tables (CB-aa-4)

**Signer:** `2.0.0_SA_COO~C2` (dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2`. **Applier:** `0.7.0_AE_CloudOps~CB2` (MSTR msg 2264).
**Given when:** CB-aa-3 (round 27) is drained VALID with `FWD3-SERVE mode=dry ... keys=3 addresses_from_builder=True`, and the dry
run's three addresses equal the keys in section 1. Until then this file is a DRAFT and nothing is written. **ADDED 2026-10-09 ~04:1xZ (disarm of rows D2-W50-S1, S2, S3):** the half is ALSO not given while the build carries days whose value is known wrong -- split days valued with split-adjusted closes against as-traded quantities (S1), in-kind `li` flows understated (S2), `dvr` close steps (S3). It is given only once those days are repaired, or blanked with their reason (FWD-3: "a day that cannot be worked out says so and is never filled in"), by a ruled cell. **Code at the apply:** the
drained `data/assets/scripts/silver/commonwealth_fwd3_serve.py`, unchanged since the drain commit.

## 1. THE ACT AND ITS BLAST RADIUS

Bucket `opal-data-assets`. The addresses are the builder's output, measured 2026-10-09 ~03:2xZ with
`lib/opal_naming.address("commonwealth", <cottonwood scope>, "silver", <table>, "date=2026-06-23")`:

| act | prefix | writers, N | change | rollback |
|---|---|---|---|---|
| `commonwealth_fwd3_serve.py --apply` | `s3://opal-data-assets/commonwealth/cottonwood/silver/daily_returns/date=2026-06-23/` | N = 1 (the builder's apply) | MINT: 0 objects today | delete what the act wrote under this prefix |
| the same run | `s3://opal-data-assets/commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/` | N = 1 | MINT: 0 objects today | delete what the act wrote |
| the same run | `s3://opal-data-assets/commonwealth/cottonwood/silver/month_grades/date=2026-06-23/` | N = 1 | MINT: 0 objects today | delete what the act wrote |
| anything else | -- | -- | NOT SIGNED | -- |

**Measured before the draft:** a `get_file_info` listing of each prefix returned 0 objects for all three targets; the positive control
(`.../silver/transactions/date=2026-06-23/`) returned 14, so a zero is a real absence. No existing served object is moved or
overwritten. **Readers:** `comp-estate --resource` on each of the three prefixes reads "absent from 135 measured estate chains", 0
readers. No consumer page reads these tables yet.

## 2. EXPECTED OUTCOME, BOTH BRANCHES

- **A:** rc 0; `--verify` prints `FWD3-VERIFY tables=3 match=True`; the three prefixes hold the built tables, with row counts and content
  hashes equal to the dry run's.
- **B:** a refused Put, a partial write, or `match=False`: delete everything the act wrote under the three prefixes (they were empty),
  file a row, and close the ledger ROLLED-BACK.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       commonwealth_fwd3_serve.py --apply (MINT 3 new prefixes; 0 existing objects moved)
N         1 writer
COO half  2.0.0_SA_COO~C2 -- DRAFT (given on CB-aa-3's VALID drain + address equality)
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```
