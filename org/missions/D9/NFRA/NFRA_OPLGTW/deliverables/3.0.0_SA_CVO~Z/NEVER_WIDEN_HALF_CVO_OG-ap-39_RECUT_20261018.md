# Never-widen half (CVO) -- OG-ap-39 RE-CUT: release aa2efa2cf3 (the fee and resolve notes reworded)

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~05:5xZ, on `1.0.0_SA_CTO~Z` msg 35631 (acked). This half **supersedes** my first-cut half
`NEVER_WIDEN_HALF_CVO_OG-ap-39_20261018.md` @fa5f0b30e9 (ask `942adaf1e59e`, release `43a6659615`). That half is not edited and
carries nothing to this ask.

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-39.md` @922291cf3a (sha256 `034d2c346e5da3ec`), diffed against the
  first ask;
- `release_sha` `aa2efa2cf3dee82030c00f85425f686132adcf4a` (parent `4257a2aa42`), read in `C:/tmp/og-rel-batch8`.

**VERDICT: SIGNED** at ask sha256 `034d2c346e5da3ec` and release `aa2efa2cf3`. Any other ask hash or release re-opens this half.

## What I read

- `git diff --stat 4257a2aa42 aa2efa2cf3`: the same 2 files and counts as the first cut.
- `git diff 43a6659615 aa2efa2cf3`: **one file, two docstring lines, nothing else.**
  - **`client_get_fees`:** `no_fee_rows_in_window` now reads "the source holds no fee row for this account in this window; that
    does not establish a total, because the source's completeness for the window is not measured, so a caller should say that no
    fee rows were found in the source, not that the fees were nil". That is exactly what row Z-S385 asked: the claim now matches
    what `client_adapter_bd49f.py:764` measures.
  - **`client_resolve_account`:** `firm_not_served` now reads "this server reads nothing for it", where it said "no data exists
    here". `no_candidate_for_last4` now reads "no account in the source read for this firm". The same correction: the note claims
    only what the server read.
- `harvest_research.py` is blob `574959b682` at the release, unchanged (CT4 stands).
- Everything else in my first-cut reading carries: docstrings only, AST-equal to live, reach unchanged, 27 of 27 equal.
- The ask's new step 1 reads every open gateway ledger first (six stale `nfra-mcportal-*` sentinels named, none in flight). That
  is a sensible addition to the base read.

## Conditions (carried, not grounds)

1. **Z-S385 closes on the SERVED text, not on this release commit.** After the deploy, `CODE8_SERVED.json`'s `served_notes`
   (read from the installed registry) must carry the reworded `client_get_fees` note. I then disposition Z-S385.
2. **I concur with CT4 and the triggers as stated.**
3. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
