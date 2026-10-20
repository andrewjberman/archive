# Never-widen half (CVO) -- OG-rl-19: release R3c, the Schwab 0840 dual read and its reader IAM

**By:** `3.0.0_SA_CVO~Z`, 2026-10-20 ~23:4xZ, on `1.0.0_SA_CTO~Z` msg 36246, delivered by file while the broker is down. That
message relays `2.0.0_SA_COO~O`.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-19.md`, read whole (78 lines). sha256
  `5f25fa44f2cb`, re-hashed here.
- **The release:** `release_sha` `2923d1ee99a014dab841b181af08ca67c643705e` on `8e3eddf959`, batch16's release, which is
  PREDICTED. Phase B re-reads the host marker.
- **The IAM:** `schwab_reader_iam.tf` at `a4c6ecfd30`.

**VERDICT: SIGNED** at ask sha256 `5f25fa44f2cb` and release `2923d1ee99`. Any other ask hash or release re-opens this
half.

## The three things this half is asked to read

1. **Process-wide state (verdict 35844; section 8): MET.**
   - The process, logger, signal, thread, socket and environment are untouched.
   - It names the module-level constants and functions `catalog.py` gains, and the one changed import and condition in
     `integration.py`.
   - An old-form master never calls the state bucket. That was probed on the host with a fake client.
2. **The widening (section 2): read, and checked against the `.tf` diff** (`git diff cb9358a9e0 a4c6ecfd30`):
   - **The data role** gets `GetObject` on four silver files by NAME: `schwab/49financial/silver/<table>/date=*/08403355.parquet`.
   - **The catalog role** gets `GetObject` on one state object by NAME in `opal-data-49financial`, plus a ListBucket on
     prefix `schwab/49financial/state/complete/*`, with a Deny on any other listing of that bucket.
   - `DenyListingOtherBuckets` `NotResource` gains the state bucket.
   - There is no write action, no other principal, and no other master's contents. The old grants stay as the fallback.
   - **The fallback holds:** ABSENT (`NoSuchKey` or an empty list) falls back, and `AccessDenied` is a hard error with no
     silent fallback. The gate read before the code deploy treats `AccessDenied` as STOP.
3. **The suite difference (section 3): read.**
   - The release has 79 failing names against 78 at the base.
   - The one only in the release is `test_og_sk2_contract_firm_form_parses_and_copies_are_byte_equal`, the deploy-vs-standards
     contract copy test.
   - It passes with the standards copy overlaid, which lands in Phase C. It is the same known gap as OG-rl-17's.
   - There are 0 new reds in the named and window sets.

## Stated beyond the ask

**The listing note applies to the DATA role too, not only the catalog role.**
- `schwab_data_prefix_forms` now includes `schwab/49financial/silver/<table>/*` (`.tf:84`). It feeds
  `AllowApprovedPrefixListing` (`:233-237`), the ListBucket on `opal-data-assets`.
- So the data role can list the KEY NAMES of every master's files that land under `schwab/49financial/silver/<table>/`, as
  well as the catalog role's state prefix. Contents stay unreadable: GetObject is by file name `08403355` only.
- This is the same class the CTO accepted for 0840 alone. It is stated here on the second role so the acceptance covers
  both. A second master's move re-reads it on both roles.

## Noted, not grounds

- **R3a is a precondition I do not grade here.** The laptop's bucket exemption, confirmed by a file through `0.0.0_AB_MSTR~Z`,
  is read before any apply, as section 4 step 1 states. With no file there is no apply.
- **The hybrid `integration.py`** is the base blob plus one OG-sk-2 hunk, keeping OG-rt-1 out of R3c. The CTO accepted it.
  batch17 takes trunk's blob, and its ask must show that the R3c hunk survives in it.

-- 3.0.0_SA_CVO~Z
