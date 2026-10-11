# XB-0c52 term 5 -- the one class read on REQ-4b5155ac2ea9467ab771b414's owner

From `0.7.0_AE_CloudOps~ANL` (laptop), 2026-10-11 ~11:1x ET. Follows `XB_0c52_EIGHT_RECONCILING_WRITES_RETURN_STOPPED_AT_STATUS7_20261011.md`.
Read-only. Authority: order XB-20261011T145549Z-0c52 step 6; CTO message 108338 (the read is not conditioned on the writes).

## Answer (a class, never an address)

**YES: the principal is an internal profile on `opal-users-v2`, `userType` = `service`, `status` = `active`.** One PROFILE row.
Attribute names on the row: `PK SK allowedFirmIds email firmId name status userType`. No value other than `userType` and `status` left the laptop.

## How it was read

The owner `principal_id` of the request's `irpt-requests` record (`analysis#REQ-4b5155ac2ea9467ab771b414#1`, tenant 49financial,
consistent get-item), matched case-insensitively to `email` over a consistent scan of `opal-users-v2`: **86 items scanned, 1 matched.**
The principal contains `@`; it does not begin `svc`. Denominator printed; no other row matches.

## What it does and does not say

- Resolves "OTHER" in the owners file: the principal is a registered service-type profile, not an unknown outsider. It is not
  established which service, nor why its address is neither at opalinvest.com nor the `SERVICE:` subject form of requests 2, 3 and 7.
- `userType` `service` is the table's own class; this seat did not check that the profile's `allowedFirmIds` covers 49financial
  (not asked, and a different question).

Nothing written. Push state: LOCAL on `box/laptop` (ls-remote not read).
