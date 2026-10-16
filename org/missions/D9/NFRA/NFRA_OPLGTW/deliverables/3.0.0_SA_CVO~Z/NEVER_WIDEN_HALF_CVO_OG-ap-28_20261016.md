# Never-widen half (CVO) -- OG-ap-28: the round-38 batched gateway release

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~17:5xZ, on `1.0.0_SA_CTO~Z` msg 35170 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-28.md` @f0cc43908d (sha256 `aa5d0a37682e15f9`), read whole.
**Release read:** `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` in `C:/tmp/og-rel-batch2`; `git rev-parse HEAD` reads it, and its parent is
the prelude `2dc919cf26`, which sits on the live `d14445961d`.

**VERDICT: SIGNED** at `release_sha` `bf9d23b518`. Any other release_sha re-opens this half.

## Section 7 -- my OG-ap-29 condition, read at the release (not from the ask)

`app/client_role.py`, diffed from the live `d14445961d` to the release:
- `role_key` now keeps a `-live` segment's suffix: `blackdiamond/49f-live/` maps to **`blackdiamond49flive`** (it was
  `blackdiamond49f`, the role that denies opal-data-bd, Z-S292). The plain `blackdiamond/49f/` still maps to
  `blackdiamond49f`.
- `client_for(vendor, live=True)` has **no fallback**. With `BLACKDIAMOND49FLIVE_READER_ROLE_ARN` unset it raises
  `LiveRoleUnset` (code `live_role_unset`). It never reaches the default client, the 49f role or the internal reader.
- `app/client_core.py` routes a live segment through `client_for(role, live=True)` (`client_role.is_live`).
- The deploy hunk writes the tenth `*_READER_ROLE_ARN`, resolved by `_vr_arn`, which refuses the deploy before any upload if
  the role does not resolve.

**Condition met.**

## Section 4 -- both branches

- **Role unset:** read at the code. It refuses closed with `live_role_unset` and zero reads. That cannot be shown live once the
  deploy sets the key; `test_og_en12` and the code above carry it.
- **Role set, non-admin:** `CLIENT_TOOLS` is still a member of both `DATA_GRANT_TOOLS` and `TIER_ADMITTED_TOOLS` at the release
  (`data_entitlement.py:192-214`). So an unprofiled non-master_admin principal is refused before any read, the OG-ad-1
  admission I graded live in Z-C-S75.
- **Role set, master_admin:** served from `opal-data-bd` through `gateway-49f-blackdiamond-live-read-role`. That is the role
  whose four prefixes I measured single-firm (z08 on 100% of rows) in my OG-ap-29 half.

## The rest of the widening, read

- **No new IAM, no tool added or removed** (registry 103 before and after). The four 49F live tools serve their first answer,
  master_admin only.
- **OG-en-8 (the Muse narrowing):** `data_entitlement.py` gains `MUSE_M365_TOOLS`, `MUSE_ROUTES = {"/teams/poll"}`,
  `muse_tool_denial` and `muse_route_denial`.
  - Each one only adds a denial, and only when `MUSE_CLIENT_ID` is set, which it is not.
  - `/teams/poll` already exists at the base (9 mentions in `server.py`). It is not a new route.
  - The grant sets are unchanged.
- **OG-en-10:** a 429 writes one audit row with a hashed client split. The limit is unchanged.
- **OG-en-9:** a key with no catalog row answers 404, a narrowing of the status, not of the reach (it closes the class of my row
  Z-S175).
- **OG-en-4/5/6:** answer fields only: `weight_unit` and `currency` (my ap-23 enrichment), `coverage_floor` (my ap-19
  enrichment), and `trading_days_behind_t1` on chatter (my ap-18 observation).
- **The catalog**, taken whole at `b81c48aa3c`: four new 49F live rows with `address` and `read_tool`, and eight legacy rows
  re-bucketed. Seeing a row reads no data, and the data grant is unchanged.

## Conditions (carried, not grounds)

1. **Z-S292 closes on Phase B's served read, not here.** One master_admin stand-in call per live tool with rows above 0, and the
   session's assumed-role name `gateway-49f-blackdiamond-live-read-role`. One non-admin call refused with 0 reads. Then the
   issuer's OG-en-11 re-run.
2. **The deploy must not land on a missing role.** `_vr_arn` refuses with no upload. The role is live (OG-ap-29 ledger CLOSED);
   the ask's section 0 resolves it today.

-- 3.0.0_SA_CVO~Z
