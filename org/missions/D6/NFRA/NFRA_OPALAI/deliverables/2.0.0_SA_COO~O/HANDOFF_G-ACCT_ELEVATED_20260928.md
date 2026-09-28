# HANDOFF -- G-ACCT: provision the Opal_Agent account (for `2.0.0_SA_COO~O elevated`)

**From:** `2.0.0_SA_COO~O` (site Z), 2026-09-28 ~15:3xZ. **On:** Andrew-direct 2026-09-28: "write a text handoff to an
agent who would do it in the elevated shell". **You run in:** an ADMINISTRATOR PowerShell on this site-Z machine, as the
operator user (`Opal Bloomberg`, elevated). The source of these steps is the CTO's runbook
`org/missions/D6/NFRA/NFRA_OPALAI/deliverables/1.0.0_SA_CTO~O/ANDREW_SWITCHOVER_RUNBOOK.md`, Parts A and B step 3a.

## Already done and measured by `2.0.0_SA_COO~O` (do not redo)

- `C:\opal_runtime\runtime.config.json` exists, with keys `checkout_dir` `C:\opal_runtime\opal_ai`, `state_dir`
  `C:\opal_runtime\state`, `workspace_probe_file` (the workspace CLAUDE.md) and `prod_ref` `PROD`.
- `C:\opal_runtime\opal_ai` is cloned at PROD `fd8ab8a` (== origin/DEV), runbook step 0.
- The account `Opal_Agent` does NOT exist yet (`Get-LocalUser` returned nothing).
- The dry run printed exactly these eight acts and changed nothing:
  ```
  PLAN: CREATE-USER Opal_Agent
  PLAN: ASSERT-NOT-MEMBER Administrators
  PLAN: ASSERT-NOT-MEMBER CodexSandboxUsers
  PLAN: MKDIR checkout_dir (C:\opal_runtime\opal_ai)
  PLAN: MKDIR state_dir (C:\opal_runtime\state)
  PLAN: ACL checkout_dir Opal_Agent:RX
  PLAN: ACL state_dir Opal_Agent:M
  PLAN: SECRET DPAPI operator
  ```

## Your steps, in order. Stop at the first surprise and report it.

1. **Re-run the dry run** and confirm it prints the same eight lines:
   `powershell -ExecutionPolicy Bypass -File C:\opal_runtime\opal_ai\opal\runtime\provision\provision-account.ps1 -Config C:\opal_runtime\runtime.config.json -Plan`
2. **Real run (elevated):** the same command WITHOUT `-Plan`.
   - Expect one `OK:` line per act, ending `OK: provisioning complete for Opal_Agent`, exit 0.
   - The password is generated and stored DPAPI-protected at `%USERPROFILE%\.opal_runtime\opal_agent_cred.xml`
     (the operator's profile). NEVER print it, copy it or put it in any repo.
   - REFUSE and report if it prints any act other than the eight, or `ELEVATION REQUIRED` (exit 3).
3. **Boundary check:**
   `powershell -ExecutionPolicy Bypass -File C:\opal_runtime\opal_ai\opal\runtime\provision\verify-boundary.ps1 -Config C:\opal_runtime\runtime.config.json`
   It must print `BOUNDARY: DENIED-OK` with exit 0: Opal_Agent is DENIED the workspace probe file and ALLOWED its own
   state_dir. Any other verdict (e.g. `NOT-PROVISIONED` exit 4, or a read that SUCCEEDS): stop and report.
4. **One-time setup AS Opal_Agent** (runbook 3a). Start a PowerShell as Opal_Agent with the stored credential,
   `Start-Process powershell -Credential (Import-Clixml "$env:USERPROFILE\.opal_runtime\opal_agent_cred.xml") -LoadUserProfile`,
   and in THAT session:
   - install Claude Code for this account with the standard installer, run as Opal_Agent (NOT the operator's copy at
     `C:\Users\Opal Bloomberg\.local\bin\claude.exe`, which Opal_Agent cannot read);
   - `claude mcp add --transport http --scope user opal-gateway-bbg https://mcp.opalinvest.dev/mcp`, the ONE server the
     runtime may use;
   - `[Environment]::SetEnvironmentVariable('OPAL_RUNTIME_CONFIG','C:\opal_runtime\runtime.config.json','User')`.
   - Confirm with `claude --version` and `claude mcp list` (one server, `opal-gateway-bbg`).

## Do NOT

- Do not sign in. That is G-AUTH (runbook steps 4-5: the Claude sign-in and the gateway's Microsoft sign-in). It waits
  on Andrew's decision about the service-account path, which `2.0.0_SA_COO~O` is taking to him separately.
- Do not run `launcher.ps1`, add Opal_Agent to any group, or touch the workspace repo, AWS or the gateway.

## Report (one message to `2.0.0_SA_COO~O`, file inbox `org/mcp/inbox/2.0.0_SA_COO/~O/`)

The exit code and the `OK:`/`BOUNDARY:` lines of steps 2 and 3, `claude --version` and `claude mcp list` as Opal_Agent,
and any refusal with its full text. No password and no token in the report. Rollback if needed: `Remove-LocalUser
Opal_Agent`, delete `C:\opal_runtime\state` and the credential file, and say so in the report.
