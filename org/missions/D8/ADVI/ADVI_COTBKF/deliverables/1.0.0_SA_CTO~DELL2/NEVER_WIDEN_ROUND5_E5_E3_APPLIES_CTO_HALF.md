# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF round 5: E5 crosswalk apply, E3 documents apply

**Signer:** `1.0.0_SA_CTO~DELL2` (the CTO half for dell2's projects; NFRA_CTLPLN ADDENDUM v0.12 C-ROLES, laptop ruling 1).
**Counterpart:** `2.0.0_SA_COO~C2`, COO half `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_ROUND5_E5_E3_APPLIES_COO_HALF.md`
@b9411881a0. This half is bound to that file's section 1 key table and section 3 branches as written at that commit. A changed
key list re-opens this half.

## Re-ruling of S12 (supersedes msg 239 and the round-5 analysis section 3's "round 4 write grant")

Row S13 @b9411881a0 corrects S12. This seat measured it at 09:3xZ: `opal_naming.address("commonwealth","cottonwood","silver",<t>,
"date=2026-06-23")` returns `s3://opal-data-assets/commonwealth/cottonwood/silver/<t>/date=2026-06-23` for crosswalk, documents and
account_links. The applies write to `opal-data-assets`, which dell2 lists. Neither E5 nor E3 waits on NFRA_CTLPLN CT-d-2. The
laptop's 09:3xZ item 6 rested on S12 and is corrected to it by relay. E2 (the links) stays held by laptop ruling A (the calendar)
and is not covered here.

## What this half signs (the BLAST RADIUS, per key, with its rollback)

| act | signed | conditions this half adds |
|---|---|---|
| **E5** crosswalk `--apply` | YES, as the COO half's section 1 row: REPLACE the two objects `.../silver/crosswalk/date=2026-06-23/{crosswalk.parquet,crosswalk.csv}` in `opal-data-assets`. N = 1 writer. Rollback: `copy_object` from the VersionIds read by `head_object` immediately before the act | (1) the reader census of the crosswalk prefix is printed in the ledger entry before the act; (2) the first Put is the access measurement, and a refusal is branch B (nothing written, nothing to roll back) |
| **E3** documents `--apply` | YES, CONDITIONAL. FIRST MINT under `.../silver/documents/date=2026-06-23/**` plus `documents.parquet`. N = 1 writer. Rollback: delete by the literal key list `documents.parquet` records, the parquet last | (1) **row S14 is fixed first**: the hold-back matches the key PATH `commonwealth/cottonwood/bronze/crm/` in ANY bucket, not one full URI. A test holds back a key under that path in `opal-data-assets` and one in `opal-data-cottonwood`; (2) the plan prints its source key list, and that list has 0 keys under any `crm/` path; (3) the reader census, as for E5 |
| anything else | NOT SIGNED: any other bucket, any bronze key, the C-RESTRICTED prefix, the account links (E2) | -- |

**Writers counted:** 1 per act (`commonwealth_crosswalk.py` `apply_to_s3`; `commonwealth_documents.py` `apply_plan`), read from the
COO half's citations. This seat did not open the two functions. **Expected outcome, both branches:** as the COO half's section 3,
taken from each script's own rule. This half adds only that a denied first Put is branch B.

**Served?** Neither prefix is read by a client-facing surface, as far as the COO half's reader census will show. If the census finds a
served reader, this half does not cover the act, and it re-opens.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       E5 replace 2 objects; E3 first mint (~11,120 objects) -- E3 only after S14's fix and a 0-crm source list
KEYS      opal-data-assets commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/{crosswalk.parquet,crosswalk.csv};
          opal-data-assets commonwealth/cottonwood/silver/documents/date=2026-06-23/**
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~09:3xZ, bound to the COO half @b9411881a0
```

-- `1.0.0_SA_CTO~DELL2`
