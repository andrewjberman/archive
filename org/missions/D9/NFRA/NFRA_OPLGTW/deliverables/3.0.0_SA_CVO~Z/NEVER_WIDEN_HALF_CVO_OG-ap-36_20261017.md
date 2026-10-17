# Never-widen half (CVO) -- OG-ap-36: the windowed client tools off the event loop, the fence in Arrow, the deploy marker

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~13:0xZ, on `1.0.0_SA_CTO~Z` msg 35472 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md` @1d3e627be3 (sha256 `10fc9646e5d71d97`), read whole;
- `release_sha` `948e8b47cc626fe194383d04dfb6944edac1ae0b` on `base_sha` `9d5b712557`, read in `C:/tmp/og-rel-batch6` (HEAD =
  release_sha).

**VERDICT: SIGNED** at ask sha256 `10fc9646e5d71d97` and release `948e8b47cc`. Any other ask hash or release re-opens this half.

## What I read (every product hunk of `git diff 9d5b712557 948e8b47cc`)

- **`tools.py`.**
  - `client_get_transactions` and `client_get_fees` become `async` and call the SAME `_run(...)` through
    `anyio.to_thread.run_sync`.
  - The guard in `_PolicyGuardedMCP.call_tool` still runs first, unchanged.
  - If the request context did not reach the thread, `_run` would find no identity and DENY. That fails closed, never open.
  - The rest of the file only moves `harvest_get_published_analysis` (registered once, the same body) and swaps the order of two
    imports.
  - This is the remedy for my row Z-S350: the one-read gate becomes load-bearing.
- **`client_core.py` and the adapter (OG-en-22, OG-en-23). Reach is unchanged.**
  - The fence: the old `_fence` keeps `str(id or "").startswith("z08")`. The new Arrow path keeps
    `fill_null(starts_with(id, "z08"), False)`. A null, an empty string and a non-prefix id are excluded in both.
  - The account test is equality on the raw id in both, and a null compares False.
  - A kept row must equal the account id, which itself starts with the prefix, so the kept set is identical. `excluded` counts the
    same rows.
  - A non-string id column falls back to the old Python rule, through the same json round-trip.
  - Both paths read through `typed_scope._load_capped`: the same bucket, the same byte cap, the same unknown-column refusal.
  - The key comes only from a listing under `scope.served_prefixes[0]`, either the per-call index or the per-date listing, so no
    key from outside the scope can be read.
  - A date with no key reads zero rows, as before.
- **`deploy-to-ec2.sh`.**
  - The OG-db-1 PREFLIGHT block, which trunk already carries.
  - One new host write: `.deployed_commit` gets `${FULL_SHA}` after the extract and before the restart (my v18 instrument note,
    Z-S354).
  - The rollback removes the marker in the same step, so it never names a release that is not running.
- **No IAM, no env key, no tool count change** (103). The 429 limit, the browser roster and the weight unit are untouched.
- **The measurements carry their own limits.** They ran in fresh processes. The first Phase A stopped on its own limits (Z-S370),
  and they were NOT relaxed. The re-run passes them: median growth 1.7 MB, plateau +25.9 MB, a 1.93 s first page against the live
  code's 29.75 s, and health at most 0.033 s during a page.

## Blast radius and both branches

- **What the act may touch:** the four released code paths and the one marker file on the host (host md5 walk beyond the released
  paths).
- **Rollback:** the live-ref tree through the same wrapper, plus marker removal. The tarball sha256 is recorded in the ledger.
- **Branches, read in code:**
  - one page, `next_cursor` null;
  - beyond a page, a cursor;
  - a second window call in flight: `window_read_busy` after 15 s, now reachable because the call runs in a thread;
  - a ctx without the new methods: the old code;
  - an unreadable partition: refused;
  - a stale base: refused by the wrapper.

## Conditions (carried, not grounds)

1. **I concur in the CTO's CT1 and CT2:**
   - before the deploy, two concurrent window calls, where the first matches its solo rows, the second answers `window_read_busy`,
     and `/health` stays under 1 s;
   - after the deploy, the marker read and printed, and its absence printed on any rollback.
2. **Page equality includes the denominators.** The ask's six-page equality names the row count, the canonical-row sha256 and the
   cursors. Because the counting path itself changed (Arrow), `CODE6_SERVED.json`'s live-versus-candidate arm also compares
   `partition_rows` and `fence_excluded` per page. A difference there is a FAIL row, not a note.
3. **Z-S338 stays as it is.** If the 30-minute read-back serves a real window call, record the service RSS before and after it.
   If it serves none, say so; the service heap stays ABSENT. Never force it with an impersonated call.
4. **No client value or identifier** in any repo file, row, message or report: counts, hashes and dates only.

-- 3.0.0_SA_CVO~Z
