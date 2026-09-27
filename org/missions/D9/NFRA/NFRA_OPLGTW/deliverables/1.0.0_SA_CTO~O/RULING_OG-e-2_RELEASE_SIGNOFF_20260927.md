# OG-e-2 -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-27 ~16:3xZ)

**Act:** the opal-gateway narrow release in `NFRA_OPLGTW.TO-OG-e-2.email-deny-release` (issued @17f7d7b477). It is cut
at the LIVE `110d93fb73` plus only OG-e-1's gateway commits `06eff3b73f` and `744e4468e1`. Deployer
`0.9.0_WK_NFRA_OPLGTW~8`, issuer `2.0.0_SA_COO~O`.
**Authority for this half:** Andrew's self-drive arming term, "Served output still moves only under a never-widen
sign-off (CTO half + a second, non-acting half)" (`ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_O_FABRIC.md` @56050d290d).
**Second half owed:** `3.0.0_SA_CVO~O`, a non-acting seat. The issuer and the deployer are acting seats.
**Design ruled at:** `RULING_R2-k_FIVE_CALLS_20260927.md` @2ae58221ab (call 2 fail closed, call 4 live base only).

## What the served code changes (read from `git show 06eff3b73f -- app/`; 744e4468e1 touches no `app/` file)

1. **`server.py` GuardMiddleware**, the branch `path == "/login" or sprint_view.is_sprint_path(path)` only. After
   `enforce(email)`, one `_email_denied(email)` returns 403, 503 or None. The `/mcp` branch and every other path are
   untouched.
2. **`server.py` legacy `/callback`:** the same check on the state's declared email, before `redeem_consent` runs.
3. **`token_broker.redeem_consent`:** a second check on the VALIDATED principal's email, before either cache write
   (the account-picker case).
4. **`data_entitlement.email_denial`:** one strongly-consistent `GetItem` on `POLICY#EMAILDENY#<sha256hex>` / `email_deny`.
   A present record returns 403. `DependencyUnavailable` or `AccessStateRefused` returns 503.
5. **`access_state`:** the key function, and `operator_transact` relaxed to admit `email_deny` puts. The operator path
   uses it; the runtime never calls it. Runtime writes to `POLICY#` stay refused by code and by IAM `LeadingKeys`.

**Live base check:** every name the change uses exists at `110d93fb73`: `_NO_STORE`, `_within_budget`, `import html`,
`is_sprint_path`, `OAuthError`, `acs.store`, `oauth_as.AUTH_ENDPOINT_SECONDS = 10`. `git show` read, 16:3xZ. There is no
import cycle, because `data_entitlement` imports only `access_state` and `context`.

## Writers of the named property (NEVER-1: count them)

The named property is the answer on `/login`, `/sprint`, `/sprint/`, `/sprint/archive`, `/sprint/{day}` and the legacy
`/callback`. **N = 4**:
1. **The served code** -- this act.
2. **`email_deny` records.** Their writers are the operator role only: `ops/schwab_entitlement_admin.py` restricted
   `activate` and `deny-backfill`, and, after R2-k step 3, the dashboard grant-writer Lambda. **MEASURED 16:2xZ:
   `gateway-access-state-table`, 162 items scanned (consistent scan, every page), `POLICY#EMAILDENY#` = 0** (the other
   `POLICY#` items = 10).
3. **The table's readability by `opal-gateway-role`.** Read with `iam get-role-policy` at 16:2xZ, APPLIED:
   `AccessStateStrongRead` = `dynamodb:GetItem` on the table ARN, with NO condition. So an `EMAILDENY#` key is readable,
   and the success branch does not fall into 503.
4. **The host `.env` and the dashboard bundle**, which every deploy rewrites (`deploy-to-ec2.sh` near :196 and :80-92).
   These are the same two writers MX-r-3's half named. The order's steps 5, 7, 9 and 11 carry both guards.

## Both branches, read from the producer's rule

- **Table readable and 0 deny records (the measured state at GO):** every caller of the 6 paths gets the same answer as
  today. **DELTA = 0**, and the MCP tool list stays 46 = 46. The one live change is latency: a single `GetItem` per
  request inside the existing 10 s budget.
- **Table unreadable, or the `GetItem` exceeds 10 s:** the 6 paths answer **503** with `Retry-After: 5`, where today
  they serve. This is a NEW dependency of the 5 browser routes on the access-state table. It is signed deliberately, as
  ruled (R2-k call 2): the lesser harm than a leak. `/mcp` is unaffected, because it already fails closed on the same
  store.
- **Deny record present:** 403 on the 6 paths. **This half does NOT sign any deny record.** No deny record exists, and
  the order writes none (bound 1). The first one is written by R2-k step 2, the Alyssa backfill, which waits on Andrew,
  or by a later restricted `activate`. Each is a separate act. Note for the operator: after this release, a restricted
  `activate` run from CLOUD's `ops/` script writes a deny record for that principal's email in the same transaction.

## Rollback, per key

- **Code:** redeploy `110d93fb73`'s prebuilt artifact through the same wrapper, with the 90-second health rollback. The
  order proves that build before the act (step 6). The manifest record reverts with it.
- **Data:** none written by this act.

## Guards required at GO (all are already in the order; this half makes them conditions)

- Host md5 of the 4 app files equals `110d93fb73`'s bytes BEFORE the act (step 1).
- The release census names only OG-e-1's gateway files (step 3).
- The 5 test modules pass on the release tree (step 4).
- `mcportal` HEAD equals the manifest pin before the upload (steps 5, 11).
- The live `ENABLED_INTEGRATIONS` is exactly `ycharts opal_portal globgrph` (step 9), else STOP.
- **Added condition:** at GO, the deployer re-reads `POLICY#EMAILDENY#` = 0 with the same full consistent scan. If it
  is non-zero, STOP: this half's DELTA = 0 no longer holds.
- After: on-host `/health` 200, md5 equals the release commit, tool list 46 = 46, `ENABLED_INTEGRATIONS` unchanged.
- NEVER-2 ledger `nfra-oplgtw-email-deny-release`, opened before and closed after.
- Off-hours GO, announced through `0.0.0_AB_MSTR~Z` and the agentbus.

**CTO half: SIGNED**, for the act above as bounded here, by `1.0.0_SA_CTO~O`.
