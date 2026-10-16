# Never-widen half (CVO) -- OG-ap-23: the code batch release (27 READ tools, six vendor reader keys)

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~06:5xZ, on `2.0.0_SA_COO~O` msg 34785 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md` @6fea51c310 (sha256 `a4c90d32c29f...`), read whole.
**Release read:** `56c0f8ce1d602b309abaf3f25dd28974c7736d39` in `C:/tmp/og-rel-code`; HEAD read by `git rev-parse` at signing.

## VERDICT: REFUSED

**The reason, in one line:** the release admits every Opal principal to client account-level data. Ratified PRD v3.1
Ruling 2 forbids exactly that, and because the deploy writes the six reader keys, the widening is live at the deploy.

### What the ratified text says

`org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md:1144-1146`, v3.1 addendum, ratified text this seat signed:

> **Ruling 2 -- admission for client data is the DATA-GRANT class.** Every `client_*` tool goes in `DATA_GRANT_TOOLS`,
> never `NATIVE_TOOLS`. A principal reads a firm only with that firm's data grant (as `schwab_*` today). Being an Opal
> user is not enough for client data.

v3.12 item 7 (`:1478-1479`) repeats it as the done-by bar: "each group answers one driven call by a real Opal principal
**under its grant**". No later addendum (v3.4 through v3.13 read by heading, and a token census of `DATA_GRANT|Ruling 2`
over the PRD: 4 hits, none superseding) changes Ruling 2.

### What the release does (read at `56c0f8ce1d`)

- `app/data_entitlement.py:158-162`: `client_resolve_account`, `client_get_holdings`, `client_get_transactions`,
  `client_get_allocation` and `client_get_fees` are in **`NATIVE_TOOLS`**, commented "read class, legacy: Opal
  principals only".
- `:205` `DATA_GRANT_TOOLS = frozenset(SCHWAB_TOOLS) | {"blackdiamond_list_fees"}`, and `:209`
  `TIER_ADMITTED_TOOLS = {"blackdiamond_list_fees"}`. No `client_*` tool is in either set.
- `decide()` (`:669-698`) lets an unprofiled principal through on every tool outside the Schwab class and
  `TIER_ADMITTED_TOOLS`.
- `app/client_core.py:66` and `:342`: the client tools' own admission is `typed_scope.admit_scope`, which "checks the
  principal only". `typed_scope.py:70`: `tools._is_opal_user(principal.email)`.
- There is no per-firm grant check anywhere in the client path (searched: `client_core.py`, `client_role.py`, the
  `tools.py` registrations).
- The ask itself (section 3) states the result: "the gateway can now return client account-level data (holdings,
  transactions, fees, allocation) to named Opal principals". The release is not dormant (section 0), because the deploy
  writes the six `*_READER_ROLE_ARN` keys.

### Why this is a widening a never-widen half must refuse

1. **Every Opal login, not named grant holders.** The firm fence (one firm per call, prefix-conditioned roles, the
   SmartX row filter) limits WHICH firm a call reads. It does not limit WHO may call. Any Opal principal may read any
   of the three firms' client accounts.
2. **It bypasses two existing gates on the same data.**
   - `blackdiamond_list_fees` (Black Diamond fees) is in the data-grant family and tier-admitted: master_admin or a
     grant only, which OG-bd-2 made Andrew's rule. Ruling 1 says `client_get_fees` wraps it.
   - The `schwab_*` tools need an active data entitlement. `client_adapter_schwab` serves Schwab accounts for firm
     `49financial` through `client_*` with no entitlement read.
   - The release therefore opens the data those gates hold to everyone the gates refuse.
3. **The loss is traceable.** None of the six G2 build orders (`TO-OG-cl-1` to `cl-6`) names the admission class: 0 of
   6 mention `DATA_GRANT` or `NATIVE_TOOLS`. Ruling 2 never reached the decomposition, and the hookup placed the tools
   by the default ("legacy").

## What this half does NOT refuse (read and found sound)

- **The 22 non-client tools** (rival funds 10, silver etfs 3, portfolio 1, json-served 7, classification 1) read Opal or
  fund data through the internal reader role, for Opal principals only. That is the read class Ruling 2 keeps for
  them. The classification tool's path is the one OG-ap-26 moved (my half @f2cf55e41e).
- **The six reader keys' resolution** (`iam get-role`, compare, refuse on mismatch, no value printed) is sound as a
  mechanism.
- **C1 and C2** (section 8) are well placed in Phase B and would be met as written. They test the firm fence. They do
  not test admission, so they cannot cure this.

## The smallest change I would sign (the remedy is the issuer's; the design is the CTO's)

1. Admit the five `client_*` tools as the data-grant class Ruling 2 names. Moving them into `DATA_GRANT_TOOLS` alone is
   NOT enough. `DATA_GRANT_TOOLS` confines only principals WITH a profile (`decide()` `:685-690`), and an unprofiled
   Opal principal still passes (`:694-698`). They must also take the unprofiled-deny branch, as `blackdiamond_list_fees`
   does through `TIER_ADMITTED_TOOLS`. With today's grant model (`allowed_tools` `:487-492`, Schwab tools only), that
   means master_admin only until a per-firm grant shape exists. That is a CTO design call, not mine.
2. Or carry the client tools out of this batch and ship the other 22. The ruling "nothing ships dormant" is the issuer's
   to re-weigh against this.
3. Either way, the served read adds the negative arm this half needs: an Opal principal WITHOUT a grant (and not
   master_admin) calls `client_get_holdings` and is refused with 0 reads. A grant holder, or master_admin, is served.

A re-cut naming a new `release_sha` re-opens this half; I will read it on receipt.

-- 3.0.0_SA_CVO~Z
