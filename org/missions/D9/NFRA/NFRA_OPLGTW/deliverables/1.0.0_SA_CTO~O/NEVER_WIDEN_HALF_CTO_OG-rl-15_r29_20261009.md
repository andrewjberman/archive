# Never-widen half (CTO) -- OG-rl-15, the r29 gateway release, Half 1 (the code that runs)

By: `1.0.0_SA_CTO~O`, 2026-10-09 ~07:2xZ (after the site Z reboot at 06:58Z).
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/ANNOUNCE_OG-rl-15.md` @368e48e533
(worker branch `wk-NFRA_OPLGTW-32-43`, tip read 368e48e533; no later edit of the ask), section 13 Half 1.
Pinned to: release sha `91811b648ab119e73e22f8d401dd09f45b8ab19b` (`rel-nfra-oplgtw-r29`), ONE commit on live
`aa75078e1b` (r28). Diff read here: 19 files, +1378/-58, equal to the ask's count.
Beside: the COO half `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-15_r29_20261009.md` @40b39ad88d.

## What this seat read at the sha (not from the ask's prose)

`git diff aa75078e1b 91811b648a` over `destructive_ops.py`, `oauth_as.py`, `server.py`, `data_entitlement.py`,
`admin_grants.py`, plus every reader of the rolling window in `app/` at the sha (`git grep` of `ROLLING_WINDOW_DAYS`,
`window_first`, `_allowed_dates`, `calendar_months`).

## SIGNED: Half 1, on the ask's terms

1. **`opal_asker_query` becomes SAFE (R54).** One name is added to `SAFE_TOOLS`, and the two maps are unchanged.
   `classify` still fails closed on any other unlisted tool. The tool is a read, so this seat accepts the change.
2. **Token grants answer once sent (R50).** `SendGate.mark_sent()` sits immediately before `transact_runtime` in both
   `exchange_code` and `exchange_refresh`. `abandon()` takes the same lock, so exactly one side wins:
   - **Abandoned first:** the work raises 503 at `mark_sent` and the consuming transaction is never sent. The client's
     retry presents an unconsumed token, which is the R49 fix.
   - **Sent first:** the handler awaits the same future with no second budget and answers its result.
   No token, family or scope is added. A reuse revocation before the gate is unchanged behaviour.
3. **`calendar_months` 1-13 (PRD v2.0 item 4).**
   - `parse_rolling_window` is the one rule. The READ parser, the operator CLI and the admin door all call it.
   - It refuses: both fields at once, a bool, a fraction, a non-finite Decimal, 0, 14, and `calendar_days` other than 30.
   - A grant with neither field keeps the 30-day window. An explicit `calendar_days: 30` is the same window, not a widening.
   - `months_before` clamps to the month's last day.
   - The catalog's availability read uses the same `window_first`, so the check and the listing agree.
   - The grant-writer Lambda still refuses the field until it is rebuilt. That path fails closed (409).
4. **Rollback per key.** Redeploying `aa75078e1b` would make the older parser refuse a stored `calendar_months` grant.
   So Phase C's grant is reverted BEFORE any gateway rollback, never after, as the COO half also orders. This seat
   signs on that order.

## Observations (not conditions)

- **Window boundary.** `window_first` gives the same calendar day 13 months earlier, and both ends are inclusive. A
  13-month grant therefore reads 13 months plus one day. This seat accepts that as the meaning of "13 months". The
  30-day window counts the anchor day the same way.
- **Per-call span.** `schwab_list_files` keeps its per-call span limit of `ROLLING_WINDOW_DAYS` (30). That limit
  predates r29 (live `integration.py:473`). A 13-month reach is listed in pages of 30 days or less. This narrows, it
  does not widen. Whether it should follow `calendar_months` is a later enrichment, not an r29 condition.

## Not covered by this half

- Half 3 (CVO~Z): the mail-domain widening and the second bearer holder.
- Andrew's own 13-month reach: a separate question that does not hold r29 (A7 D3).

-- 1.0.0_SA_CTO~O
