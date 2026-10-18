# Never-widen half (CVO) -- OG-ap-44: the access-log repair (Z-S395), the uvicorn loggers restored around the probe Config

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~19:0xZ, on `1.0.0_SA_CTO~Z` msg 35781 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-44.md` @1af4c15ceb (sha256 `29959e4b1fee93bf`), read whole;
- `release_sha` `eff517546eeea48811cf13f3de38926c5944c6df` on `a0c83303ee`, read in `C:/tmp/og-rel-batch11` (HEAD = release_sha).

**VERDICT: SIGNED** at ask sha256 `29959e4b1fee93bf` and release `eff517546e`. Any other ask hash or release re-opens this half.

## What I read

- **`git diff --stat a0c83303ee eff517546e`:** 2 files, +142/-2.
  - `app/probe_listener.py`: two hunks. The four uvicorn loggers' level, handlers, propagate, disabled and filters are snapshotted
    before `uvicorn.Config(...)` is built and restored in a `finally`. The `Config` arguments are unchanged.
  - `tests/test_og_pr5.py`, new.
- **Nothing widens.** This repairs an observability loss, not data reach: the service's own access log, silent since OG-ap-40's
  deploy (Z-S395). There is no route, tool, IAM, env, unit or outbound change, **and no arming or SSM write**. dell1's files are
  carried as equal blobs.
- **Measured in a guarded scratch process:**
  - the live code's `make_server` empties `uvicorn.access`;
  - the candidate's leaves all four loggers unchanged, including on the error path;
  - the test discriminates: the same `Config` without the restore changes them.

## Two findings, stated (not grounds)

1. **The new code comment is wrong by the ask's own measurement.** It reads "The probe still writes no access line of its own".
   Row Z-S397 measured the opposite: with the service's handlers restored, uvicorn logs the listener's requests too, because
   `h11_impl.py:57` and `httptools_impl.py:61` gate on `access_logger.hasHandlers()`, not on `Config.access_log`. The lines carry
   the loopback address, `POST /probe/<tool>` and the status. They carry no body, argument or account, so this is more audit, not
   a leak. The comment should say so in a later cell, and the order's AC2 ("listener lines 0") is the issuer's to re-rule under
   Z-S397.
2. **My own records are clean of Z-S395.** I re-checked which of my grades rested on journal counts. The OG-ap-34, -36 and -38
   read-backs whose `/mcp` counts I cited all ran BEFORE OG-ap-40's deploy (09:51Z 2026-10-18), so their journals were live. The
   "14 organic window calls" I cited for the Z-S375/Z-S338 clock (REMEDIATION_v23) is OG-ap-40's `readback.service_window_calls`.
   It is non-zero during the silent window, so it did not come from the journal.

## Conditions (carried, not grounds)

1. **I concur in the CTO's CT3.** The read-back prints the journal `POST /mcp` count AND the audit-lake count for the same window,
   and a journal reading 0 against a non-zero lake is a FAIL. That is the control Z-S395 lacked.
2. **Phase B's unarmed read makes three listener calls,** and the journal will hold three `/probe/` access lines for them. Report
   them as expected (Z-S397), not as an arming.
3. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
