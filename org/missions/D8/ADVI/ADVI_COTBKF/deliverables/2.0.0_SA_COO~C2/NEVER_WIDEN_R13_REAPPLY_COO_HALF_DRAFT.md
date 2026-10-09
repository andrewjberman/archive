# NEVER-WIDEN SIGN-OFF -- COO HALF (DRAFT, not yet given) -- ADVI_COTBKF: re-apply the crosswalk and the account links on the one signing table

**Signer:** `2.0.0_SA_COO~C2` (dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2`. **Given when:** the CTO's round-13 answer cuts the re-apply (or
says apply). Until then this file is a draft and nothing is applied. **Code at the apply:** CLOUD @79e9c35429 or later with
`commonwealth_signs.py`, `commonwealth_crosswalk.py` and `commonwealth_account_links.py` unchanged since.

## 1. THE ACTS AND THEIR BLAST RADIUS

Bucket `opal-data-assets`; keys are builder output (`opal_naming.address("commonwealth", "cottonwood", "silver", <table>, "date=2026-06-23")`).

| act | keys | writers, N | change (measured by CB-m-2's diff) | rollback pin (head-object, 15:5xZ) |
|---|---|---|---|---|
| crosswalk `--apply` | `.../silver/crosswalk/date=2026-06-23/{crosswalk.parquet,crosswalk.csv}` | N = 1 (`apply_to_s3`) | 65 rows change: 32 NOT_MATCHED -> MATCHED (439 -> 471), 33 score changes, 0 matches lost | parquet `fatOX6x0HfXRV_O7TKPNmuGBrL5wuoG1` (141,226 B); csv `RGQHH1zievrDXGUvGO.S9TDdQCNk8faA` (692,831 B) |
| account links `--apply` | `.../silver/account_links/date=2026-06-23/{account_links.parquet,account_links.csv}` | N = 1 (the script's `--apply`) | 2 status/link rows (one gained, one lost; 212 LINKED unchanged) + 52 reason texts | parquet `OQ9YHJ3hrm7PUOJ9r64TBt8ec3.4rxqS` (145,925 B); csv `JY3f29AVoi57DaE75trdGa_.mZcWUKjc` (885,566 B) |
| either | anything else | -- | NOT SIGNED | -- |

Readers: re-run the reader census before the half is given (`comp-estate --resource` on both prefixes; 0 of 135 chains at the previous
applies). Restore is `copy_object` from the pins (versioning Enabled).

## 2. EXPECTED OUTCOME, BOTH BRANCHES

- **A:** both scripts rc 0; VersionIds move off the pins; read-back of `crosswalk.parquet`: 1,533 rows, 471 MATCHED; of `account_links.parquet`:
  1,450 rows, 212 LINKED, with acct#e1e2dacb -> acct#f6464238 LINKED and acct#d6187d4b NOT_LINKED (LEFT_COMMONWEALTH); and the CB-m-2 diff re-run
  against the NEW applied tables reads 0 changed.
- **B:** a refused Put or any count off: restore all four pins, file the row, close the ledger ROLLED-BACK.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       crosswalk + account_links --apply on the one signing table (replace 4 objects)
N         1 writer per table
COO half  2.0.0_SA_COO~C2 -- DRAFT
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```

## 3. GIVEN -- 2026-10-07 ~16:0xZ (the key table above unchanged)

CTO half: `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ADVI_COTBKF_R13_REAPPLY_CTO_HALF_20261007.md` @d9877f9754 (msg 812). Its conditions,
met here: **reader census printed** -- `comp-estate --resource` on `commonwealth/cottonwood/silver/crosswalk` and `.../account_links`:
SUBJECT_ABSENT_FROM_CORPUS, 0 of 135 chains each; a repo search outside `org/` finds only this project's scripts and tests (the three silver
scripts, the signs module, and three read-only analysis readers), no served consumer. **Pins re-read at the apply** -- identical to section 1
(crosswalk.parquet fatOX6x0..., crosswalk.csv RGQHH1zi..., account_links.parquet OQ9YHJ3h..., account_links.csv JY3f29AV...). **Code**
unchanged since @42f647fa77 (git log on the three scripts). **The ledger opens before any write.**

```
COO half  2.0.0_SA_COO~C2 -- GIVEN 2026-10-07 ~16:0xZ
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN @d9877f9754
```
