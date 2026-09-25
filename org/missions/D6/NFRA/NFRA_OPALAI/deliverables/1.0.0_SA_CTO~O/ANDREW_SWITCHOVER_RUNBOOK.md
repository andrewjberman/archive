# Andrew's switchover sitting -- about 20 minutes at the terminal box

**For:** Andrew. **Prepared by:** `1.0.0_SA_CTO~O` on option 1 of the 2026-09-25 /next-steps ("i like all four",
record @bda25438c8). **Unblocks:** NFRA_OPALAI FWD-1 (the Analyst answers a colleague in Teams from its own account)
and NFRA_MCPORTAL FWD-1 (you change a colleague's access from the dashboard).

**Before you sit down, `2.0.0_SA_COO~O` confirms in one message that:**
- (a) the round-1 code is merged into `opal_ai` DEV and PROD;
- (b) `runtime.config.json` is written, outside every repo;
- (c) NFRA_MCPORTAL's gateway release is live;
- (d) the upload-permission precondition (row Z-S19) is met.

It fills in the exact paths below. Nothing here asks you to type a password or a secret.

## Part A -- the Opal_Agent account (needs an Administrator PowerShell)

1. **Dry run first:** `provision-account.ps1 -Config <runtime.config.json> -Plan`. It prints eight planned acts and
   changes nothing.
2. **Real run, elevated:** the same command without `-Plan`. It creates the local account `Opal_Agent` (not an admin),
   makes its folders, sets their permissions, and stores a generated password encrypted in the operator profile. Refuse
   it if it prints anything other than the eight acts.
3. **Boundary check:** `verify-boundary.ps1 -Config <runtime.config.json>`. It must show that `Opal_Agent` is DENIED a
   read of a workspace file. If that read succeeds, stop and tell the COO.

## Part B -- two sign-ins as Opal_Agent

4. **Claude sign-in:** the COO starts a session as `Opal_Agent` and a browser sign-in opens. Sign in with the Claude
   account you choose for the Analyst.
5. **Gateway sign-in:** in that same session, the gateway (`opal-gateway-bbg`) asks for a Microsoft sign-in as
   **Opal Bloomberg**. The MFA code comes to your phone. The Analyst's first act then checks `whoami` = Opal Bloomberg.

## Part C -- the test colleague

6. **Name the colleague and what they may see.** The COO writes their permissions through the existing operator path,
   and nothing new is built. Then the colleague asks the Analyst one real question in Teams, about a figure the portal
   shows. A second, un-admitted person asks too, and must be refused.

## Part D -- the dashboard page load (NFRA_MCPORTAL)

7. **Open `https://mcp.opalinvest.dev/sprint`** in your browser, signed in as yourself. That one request lets the
   gateway record which identity claims your sign-in carries, as names only and no values. The grant writer's
   configuration is set from it.
8. **Later, the live test:** from the dashboard's Entitlements tab, narrow one colleague's data access, see their next
   question answered within the new limit, then widen it back.

## If anything looks wrong

Stop at that step and tell the COO. Each part has a rollback: the account can be deleted, the sign-ins revoked, and the
grant reverted. The gateway release has its own automatic 90-second rollback.
