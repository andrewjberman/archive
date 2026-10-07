# NEVER-WIDEN SIGN-OFF -- COO HALF (DRAFT, not yet given) -- ADVI_COTBKF round 5: E5 crosswalk apply, E3 documents apply

**Signer:** `2.0.0_SA_COO~C2` (L5/L6 owner, dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2` (CTO half owed). **Gate before either half is
given:** `1.0.0_SA_CTO~DELL2`'s un-park ruling (msg 239: after NFRA_CTLPLN CT-d-2's apply; that ruling rests on row S12, whose bucket
row S13 corrects -- re-ruling asked). Until a ruling un-parks the applies, this file is a draft and NO apply runs. **Analysis:** `CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_4_20261007.md` @e363a194ed, E3
and E5. **Code at the apply:** CLOUD @9fea452b9d or later with the two scripts unchanged (re-read by `git log` on both paths at the apply).

## 1. THE ACTS AND THEIR BLAST RADIUS -- what each act MAY touch, per key, with the rollback

Bucket: `opal-data-assets` (versioning Enabled, read 09:3xZ; corrected from `opal-data-cottonwood` by row S13: `address()` of every
Commonwealth table resolves there, and only the CRM zip departs to the firm bucket under register X15). Every key is builder output
(`opal_naming.address("commonwealth", "cottonwood", "silver", <table>, "date=2026-06-23", ...)`), never typed.

| act | keys | writers of the property, N printed | change | rollback |
|---|---|---|---|---|
| **E5** `python data/assets/scripts/silver/commonwealth_crosswalk.py --apply` | `.../silver/crosswalk/date=2026-06-23/crosswalk.parquet` and `crosswalk.csv` (the script's `OUT_FILES`, `apply_to_s3` `:528-539`) | **N = 1**: `commonwealth_crosswalk.py` `apply_to_s3` (`upload_file`, the two names only) | REPLACE round 3's two objects (MATCHED 439 / NOT_MATCHED 1,094 both rounds; round 4 changes reasons on in-kind exits and adds the scoring of every in-kind exit; `near_matches_applied=0`) | the two objects' VersionIds read by `head_object` immediately before the apply and printed into the ledger; restore by `copy_object` from those versions (a new version, never a delete). If the bucket is unversioned at the apply: download both objects first to `.scratch/advi_cotbkf/rollback_crosswalk_r3/` and restore by upload |
| **E3** `python data/assets/scripts/silver/commonwealth_documents.py --apply` | `.../silver/documents/date=2026-06-23/doc_type=<TYPE>/<stem>_<crc32>.pdf` (11,119 objects, first mint) and `documents.parquet` at the table root | **N = 1**: `commonwealth_documents.py` `apply_plan` (`put_object`, `:294`), keys only from the plan; held-back keys under the C-RESTRICTED prefix are never written (`held_restricted=0 writable=11119` at the cut) | FIRST MINT: the prefix is empty before the act (read by the plan at the apply) | delete exactly the keys `documents.parquet` lists, by key list (the actor controls the write set: a literal key list), and `documents.parquet` last |
| either | anything else, any other bucket, any bronze key, the C-RESTRICTED prefix | -- | **NOT SIGNED** | -- |

Readers: NOT MEASURED by this seat (inferred: the FWD-8 and FWD-5 readers are this project's own L9 reads). The reader census of both
prefixes (`comp-estate --resource`) is run and printed here before the half is given. The account-links apply (E2) is NOT covered here: it is held by laptop ruling A and needs its own half.

## 2. THE NEW REACHABLE STATES, NAMED

1. A crosswalk whose reasons differ from round 3 on in-kind exits while the MATCHED set is the same 439 accounts.
2. A documents store that exists at all (first mint), and a `documents.parquet` written only when every planned object landed.

## 3. EXPECTED OUTCOME, BOTH BRANCHES (from each script's own rule)

- **E5 A:** rc 0; the last line reads `CROSSWALK commonwealth_accounts=1533 every_account_listed=True matched=439 not_matched=1094` and
  `near_matches_applied=0`; both objects' VersionIds move; a read-back of `crosswalk.parquet` has 1,533 rows, 439 MATCHED.
  **E5 B:** a denied Put or any read-back count off: restore both pins, file the row, close the ledger ROLLED-BACK.
- **E3 A:** rc 0; written = 11,119 less held-back (0 at the cut); `documents.parquet` present with that many rows; a sample of SHA-256s
  re-read equal; one statement and one tax form found by account and date and opened for the CVO (CB4d5-AC3).
  **E3 B:** the script's own rule -- any refused or failed document leaves `documents.parquet` unwritten and rc 1; then the written keys
  are listed from the run's output and deleted by that list, the row filed, the ledger closed ROLLED-BACK.

## 4. SIGNED

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       E5 crosswalk --apply (replace 2 objects); E3 documents --apply (first mint, about 11,120 objects)
KEYS      opal-data-assets commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/{crosswalk.parquet,crosswalk.csv}; silver/documents/date=2026-06-23/**
N         1 writer each (the two scripts)
COO half  2.0.0_SA_COO~C2 -- DRAFT; given the hour the dell2 write grant lands, after re-reading the key list (a changed list re-opens it)
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```

-- `2.0.0_SA_COO~C2`
