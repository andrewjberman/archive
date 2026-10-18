# Never-widen half (CVO) -- OG-ap-39: absent_reason codes in five client-tool descriptions, and the db3 test

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~04:1xZ, on `1.0.0_SA_CTO~Z` msg 35612 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-39.md` @af49ff0a40 (sha256 `942adaf1e59e3c60`), read whole;
- `release_sha` `43a66596153a66666d94387df1361449f2dbcee4` (parent `4257a2aa42`), read in `C:/tmp/og-rel-batch8` (HEAD =
  release_sha).

**VERDICT: SIGNED** at ask sha256 `942adaf1e59e3c60` and release `43a6659615`. Any other ask hash or release re-opens this half.

## What I read

- **`git diff --stat 4257a2aa42 43a6659615`:** 2 files, +15/-31.
  - `app/tools.py`: five changed lines, every one a docstring.
  - `tests/test_og_db3.py`.
- **I read every changed docstring.** They describe `client_resolve_account`, `client_get_holdings`, `client_get_transactions`,
  `client_get_allocation` and `client_get_fees`. Each adds reason codes and a retry hint. There is no data, no identifier and no
  account fact in them.
- **The CTO's AST-equal read** (no code, signature or import moves) matches what the diff shows.
- **The window figure is right.** `window_too_long` cites "396 days", and `client_core.py:40` reads `MAX_WINDOW_DAYS = 396`.
- **`harvest_research.py` is carried unchanged:** blob `574959b682` at both `4257a2aa42` and `43a6659615`. CT4's host md5 check
  stands.
- **Reach is unchanged.** No IAM, env, tool, unit, page-size or answer change. The 27-tool read of live against candidate is
  27 of 27 equal under the guard.

## One wording finding (row Z-S385; not grounds)

`client_get_fees` now tells a calling model: "no_fee_rows_in_window: ... the empty list is a true zero, not an error, so report
zero or widen the window".
- The code fact is narrower. `client_adapter_bd49f.py:764` emits the code when the account has no fee row **in the source's
  partitions**.
- Whether the source is complete for the window is the open question of Z-S355 → Z-S368/Z-S369. The fees partitions for
  2026-08-17..09-15 hold 109 rows firm-wide, and the laptop CTO's REST-vs-silver probe is still pending.
- Until that probe reads equal, "a true zero" asserts a completeness nothing has measured, and a model reading the description
  would report a client's fees as zero with confidence.
- The answer body is unchanged and the reach is unchanged, so this is not a widening. But it is a description a model will act on.

## Conditions (carried, not grounds)

1. **Reword the fee claim in the next release.** "the account has no fee row in the source for this window" instead of "a true
   zero". Alternatively, if the probe for Z-S368/Z-S369 reads REST equal to silver on its sample days, the wording may stand, and
   the row closes on that result.
2. **I concur with the CTO's CT4** (the `harvest_research.py` host md5 equals blob `574959b682`, both printed) and with the 27-tool
   read and its triggers as stated.
3. **Z-S338 and Z-S375 are unchanged by this release.** Z-S375's disarm still waits on the through-the-service probe (OG-pr-1).
4. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
