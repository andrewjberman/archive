# Never-widen half (CTO) -- OG-rl-19 (R3c): the Schwab 0840 dual read and its reader IAM (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~23:4xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-19.md`, sha256 prefix `5f25fa44f2cb`. This seat recomputed it,
and it is equal.
Release: `2923d1ee99` on the predicted base `8e3eddf959` (batch16).
IAM: `schwab_reader_iam.tf` blob `26d5685504`, plan 0/2/0, targeted.
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-19_20261020.md` (N1-N5).
Basis: Andrew-direct ~17:0xZ 10-19 (the 08403355 move); this seat's rulings of 17:13Z, 17:22Z, 17:49Z, 20:18Z and 22:0xZ
(dual read, file-name fence, scoped state grant, fall back on ABSENT only).

## Read by this seat

- **The diff:** `git diff --stat 8e3eddf959 2923d1ee99` changes 4 files, +322 -16, exactly as the ask's section 1.
- **The widening matches this seat's conditions.** Both grants are fenced by file name:
  - the data role reads four silver files by name, `.../date=*/08403355.parquet`;
  - the catalog role reads one state object name, `.../date=*/08403355.complete.json`, with a prefix-conditioned ListBucket;
  - there is no write and no folder-wide read;
  - the old grants are byte-equal, as the fallback.
- **The dual read falls back on ABSENT only.** AccessDenied is a hard error, a planted file of another master is ignored by
  name, and the old-form masters' reads are unchanged (Phase A (b): True).

## The two points the ask names

1. **The listing note: ACCEPTED, with one condition.** A prefix-conditioned list shows the key NAMES of other masters' files
   once they land: a master number and a date, never their contents. That is acceptable for 08403355 alone. **Condition:**
   the ask that moves any second master into `schwab/49financial/` re-reads the listing grant, and narrows it if key names are
   then judged sensitive. It is never inherited silently.
2. **The hybrid `integration.py` (base blob plus one OG-sk-2 hunk): ACCEPTED.** It deliberately keeps OG-rt-1's eight hunks
   out of R3c, so that batch17 carries its own entitlement change and its own rollback. **Condition:** batch17's ask takes
   trunk's whole blob over this hybrid, and states that it does.

## SIGNED

Phase B goes only on all of the following:
- batch16 is CLOSED;
- the R3a confirmation file is written by `0.0.0_AB_MSTR~Z`;
- the gate read as the catalog role answers NoSuchKey or an empty listing, never AccessDenied;
- all three halves are signed.

Any change to the ask's bytes, `release_sha` or the IAM blob re-opens this half.
