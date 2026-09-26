# Andrew's switchover sitting -- about 20 minutes at the terminal box

**For:** Andrew. **Prepared by:** `1.0.0_SA_CTO~O` on option 1 of the 2026-09-25 /next-steps ("i like all four",
record @bda25438c8). **Unblocks:** NFRA_OPALAI FWD-1 (the Analyst answers a colleague in Teams from its own account)
and NFRA_MCPORTAL FWD-1 (you change a colleague's access from the dashboard).

**Precondition status (`2.0.0_SA_COO~O`, 2026-09-26 ~00:3xZ):**
- (a) MET. `opal_ai` DEV and PROD are both at `fd8ab8a57f` on origin. `0.0.0_AB_MSTR~Z` pushed them (msg
  20260925T235909Z) and verified by `ls-remote`.
- (b) MET. `C:\opal_runtime\runtime.config.json` is written outside every repo (keys `checkout_dir`, `state_dir`,
  `workspace_probe_file`, `prod_ref`).
- (c) MET. NFRA_MCPORTAL's release `1f7128201a` went live at 21:25:38Z. The live gateway is now `1.0.0_SA_CTO`'s laptop
  release `0af72fb1d0` (23:01:38Z), which is built on `1f7128201a`, so the MCPORTAL code is still served.
- (d) NOT YET. Z-S19's server-side fix is cut as `OA-f-1` (build, running) and `OA-f-2` (the narrow release)
  @`0dd3492d8a`.

**Before you sit down, `2.0.0_SA_COO~O` confirms in one message that:**
- (a) the round-1 code is merged into `opal_ai` DEV and PROD;
- (b) `runtime.config.json` is written, outside every repo;
- (c) NFRA_MCPORTAL's gateway release is live;
- (d) the upload-permission precondition (row Z-S19) is met.

It fills in the exact paths below. Nothing here asks you to type a password or a secret.

**Paths and commands, filled by `2.0.0_SA_COO~O` (2026-09-25 ~22:5xZ), read from `opal_ai` DEV @fd8ab8a:**

| Item | Path or command |
|---|---|
| Runtime config (outside every repo) | `C:\opal_runtime\runtime.config.json`: `checkout_dir` `C:\opal_runtime\opal_ai`, `state_dir` `C:\opal_runtime\state`, `workspace_probe_file` `C:\Users\Opal Bloomberg\Desktop\ajb_workspace\CLAUDE.md`, `prod_ref` `PROD` (the keys of `opal/runtime/provision/runtime.config.example.json`) |
| Scripts (after the clone below) | `C:\opal_runtime\opal_ai\opal\runtime\provision\provision-account.ps1`, `...\provision\verify-boundary.ps1`, `...\opal\runtime\launcher.ps1` |
| How the Opal_Agent session starts | `powershell -ExecutionPolicy Bypass -File C:\opal_runtime\opal_ai\opal\runtime\launcher.ps1 -Config C:\opal_runtime\runtime.config.json`, run by YOU (the operator). It fast-forwards the checkout to PROD, runs the launch gate as Opal_Agent, and only on `GATE: PASS` starts `claude.exe` as Opal_Agent in `...\opal\runtime`. |

**Three gaps the scripts do not cover.** Each is a step below, and each is filed as a round-2 row:
- the checkout must be CLONED first, because the launcher only fetches into an existing clone;
- `claude.exe` sits in YOUR profile (`C:\Users\Opal Bloomberg\.local\bin\claude.exe`), which Opal_Agent cannot read, so
  Claude Code must be installed where Opal_Agent can run it;
- the launcher passes no environment, and the fence denies every write when `OPAL_RUNTIME_CONFIG` is unset. It is set
  once, as a user variable of Opal_Agent.

## Part A -- the Opal_Agent account (needs an Administrator PowerShell)

0. **Clone the checkout** (your normal PowerShell, your existing GitHub access):
   `git clone --branch PROD https://github.com/Opal-Capital/opal_ai.git C:\opal_runtime\opal_ai`
1. **Dry run first:** `provision-account.ps1 -Config C:\opal_runtime\runtime.config.json -Plan`. It prints eight
   planned acts and changes nothing.
2. **Real run, elevated:** the same command without `-Plan`. It creates the local account `Opal_Agent` (not an admin),
   makes its folders, sets their permissions, and stores a generated password encrypted in the operator profile. Refuse
   it if it prints anything other than the eight acts.
3. **Boundary check:** `verify-boundary.ps1 -Config C:\opal_runtime\runtime.config.json`. It must show that `Opal_Agent`
   is DENIED a read of a workspace file. If that read succeeds, stop and tell the COO.

## Part B -- two sign-ins as Opal_Agent

3a. **One-time setup AS Opal_Agent** (`runas /user:Opal_Agent powershell`; the password is the one step 2 stored):
   - install Claude Code for this account (the standard installer, run as Opal_Agent);
   - `claude mcp add --transport http --scope user opal-gateway-bbg https://mcp.opalinvest.dev/mcp`, the ONE server the
     runtime may use;
   - `[Environment]::SetEnvironmentVariable('OPAL_RUNTIME_CONFIG','C:\opal_runtime\runtime.config.json','User')`.
4. **Claude sign-in:** run the launcher command above. A browser sign-in opens. Sign in with the Claude account you
   choose for the Analyst.
5. **Gateway sign-in:** in that same session, the gateway (`opal-gateway-bbg`) asks for a Microsoft sign-in as
   **Opal Bloomberg**. The MFA code comes to your phone. The Analyst's first act then checks `whoami` = Opal Bloomberg.

## Part C -- the test colleague

6. **Name the colleague and what they may see.** The COO writes their permissions through the existing operator path,
   and nothing new is built. Then the colleague asks the Analyst one real question in Teams, about a figure the portal
   shows. A second, un-admitted person asks too, and must be refused.

## Part D -- the dashboard page load (NFRA_MCPORTAL)

7. **Open `https://mcp.opalinvest.dev/`** (your dashboard; CORRECTED from `/sprint`, which does not pass the owner gate
   that records the claims) in your browser, signed in as yourself. That one request lets the gateway record which
   identity claims your sign-in carries, as names only and no values. If the recorded names do NOT include `oid`, also
   open `https://mcp.opalinvest.dev/api/admin/whoami` and give the COO the `sub` value it shows you. It goes only into
   the grant writer's configuration. The writer's apply also needs your word for one pinned download from PyPI
   (G-PYPI).
8. **Later, the live test:** from the dashboard's Entitlements tab, narrow one colleague's data access, see their next
   question answered within the new limit, then widen it back.

## If anything looks wrong

Stop at that step and tell the COO. Each part has a rollback: the account can be deleted, the sign-ins revoked, and the
grant reverted. The gateway release has its own automatic 90-second rollback.
