# NEVER-WIDEN SIGN-OFF -- COO HALF -- ADVI_COTBKF E2: the account links applied on the covering calendar

**Signer:** `2.0.0_SA_COO~C2` (dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2` (CTO half owed). **Un-park:** laptop `1.0.0_SA_CTO` 106145
(hold A lifted for 2010-2027; `lib/trading_calendar.py` @83ab7192ee merged to dell2 CLOUD @0a73ed06a0), `1.0.0_SA_CTO~DELL2` msg 321.
**Analysis:** `CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_4_20261007.md` @e363a194ed, E2 (1)-(3); round-5 analysis @21843491cd section 3.

## 0. Preconditions, measured before this half (dell2, 10:1xZ)

- `calendar_source()` = `NYSE/hardcoded-fallback-2010-2027` (170 closures); the transactions run 2013 onward, so CB-e-1's guard admits.
- **E2 (1):** `commonwealth_account_links.py --out .scratch/advi_cotbkf/account_links_e2` -> `ACCOUNT-LINKS ended_accounts=1450
  every_ended_account_listed=True linked=212 not_linked=1238 ambiguous=14 chains=11 lines_reaching_open_account=12`; compared with
  `deliverables/0.9.0_WK_ADVI_COTBKF~13/account_links_r4.csv` (laptop, pmc 5.4.0) keyed on `old_account`: **0 of 1,450 differ on
  (status, new_account), 0 of 1,450 differ on any column.**
- **E2 (3):** the census re-run on the same calendar (`deliverables/2.0.0_SA_COO~C2/census_e2/`): `security_days_needed=9388961`
  (round 2: 9,388,961 -- equal), `security_days_covered=1297651` (round 2: 2,090,953; the drop is the BARRED bd/inf price files, ruling 1).
- **Reader census:** `comp-estate --resource 'commonwealth/cottonwood/silver/account_links'` -> SUBJECT_ABSENT_FROM_CORPUS, 0 of 135
  chains; repo search outside `org/` -> the script and its test only. No served reader.

## 1. THE ACT AND ITS BLAST RADIUS

| act | keys (bucket `opal-data-assets`, builder output) | writers, N | change | rollback |
|---|---|---|---|---|
| `python data/assets/scripts/silver/commonwealth_account_links.py --out .scratch/advi_cotbkf/account_links_e2_apply --apply` | `commonwealth/cottonwood/silver/account_links/date=2026-06-23/{account_links.parquet,account_links.csv}` (the script's `OUT_FILES`) | **N = 1**: `commonwealth_account_links.py` `--apply` | REPLACE round 3's table (459 old accounts) with round 4's (1,450 ended accounts, 212 LINKED) | pins read 10:1xZ by head-object: `account_links.parquet` VersionId `ogf8Q2zk2PMPIX5DjxD_az7x67Q76k0n` (99,934 B), `account_links.csv` `JqEXeGJYaqLcF1qXg064dCA9DE7ogaCw` (697,488 B); restore by `copy_object` (versioning Enabled) |
| anything else | any other key, bucket or table | -- | **NOT SIGNED** | -- |

## 2. NEW REACHABLE STATE

A links table covering every ended account (1,450) where round 3's covered 459; the 212 LINKED rows include the two links S9 named
(acct#b777d6dc -> acct#e5077da3, acct#6c5d660c -> acct#03cd2494); cv0QF879185 reads NOT_LINKED (ambiguous, two candidates at score 1.0).

## 3. EXPECTED OUTCOME, BOTH BRANCHES

- **A:** rc 0; both VersionIds move off the pins; a read-back of `account_links.parquet` has 1,450 rows, 212 LINKED, and equals the
  laptop deliverable on (status, new_account) 1,450 of 1,450 -- **S9's disarm condition**.
- **B:** a refused Put, rc != 0, or any read-back count off: restore both pins by `copy_object`, file the row, close the ledger
  ROLLED-BACK. S9 stays ARMED.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       E2: account links --apply (replace 2 objects)
KEYS      opal-data-assets commonwealth/cottonwood/silver/account_links/date=2026-06-23/{account_links.parquet,account_links.csv}
N         1 writer
COO half  2.0.0_SA_COO~C2 -- GIVEN 2026-10-07 ~10:2xZ
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```

-- `2.0.0_SA_COO~C2`
