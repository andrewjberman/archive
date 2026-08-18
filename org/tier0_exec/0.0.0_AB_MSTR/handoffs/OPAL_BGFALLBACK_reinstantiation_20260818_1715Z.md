# REINSTANTIATION — 0.0.0_AB_MSTR~Z · OPAL_BGFALLBACK · 2026-08-18 ~1715Z

**WHO/WHERE:** site-Z MSTR~Z, the Bloomberg Terminal box. Driving OPAL_BGFALLBACK directly (CTO~Z would
not instantiate — new-session API issues). Startup: /watcher, /agentbus (sitez consumer), then work.

**READ FIRST** (all on origin/SITEZ):
- Brief:   `org/tier0_exec/0.0.0_AB_MSTR/deliverables/OPAL_BGFALLBACK_BRIEF_20260818.md` @caac7b3138
- Project: `org/projects/OPAL_BGFALLBACK.json`
- Code:    `integrations/bloomberg/auth/{bbg_fallback.ps1,bbg_signin.ps1,bbg_verify.ps1,dapi_check.py}`
           + `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` (fallback wired at start)
- Runbook: `org/tier0_utility/0.0.3_BG_BBGTerminal/deliverables/BLOOMBERG_TERMINAL_SIGNIN_RECOVERY.md`

**SHIPPED (pushed):**
- `caac7b3138` brief + project registered.
- `197e41df7d` WS-1 fill hardening: bbg_signin.ps1 `-Fresh` relaunch + 3s input-ready settle;
  bbg_fallback.ps1 fill-RETRY loop (re-fill until verify passes; re-fill NEVER submits = zero Bloomberg
  attempts; submit stays FIRE-ONCE).
- `75d44454fd` WS-1b: (a) `-Fresh` now kills the FULL Bloomberg UI tree (wintrv+blpsmarthost+blpwtk2) —
  the zombie 'BLOOMBERG: Login' dialog is owned by a blpwtk2 subproc, so a wintrv-only kill left it and
  the next fill re-targeted the dead dialog (the `dots:1/user:''` root cause); (b) dapi_check sends a
  real data request (SPX), not just openService.

**CORRECTED DIAGNOSIS (measured 2026-08-18, Andrew present):**
- The 08-16/17 07:00 failures = bbcomm session fully expired ("failed to start session"); dapi_check
  correctly read DOWN and the fallback FIRED. The bug was the FILL; root cause = the ZOMBIE leftover
  login window (fix = `-Fresh` full-tree-kill + settle + retry, shipped).
- The entitlement SURVIVES a GUI logout+exit: after Andrew signed off + exited wintrv, bbcomm STILL
  serves SPX AND the login-scoped `.ST` (PX_LAST=113.09). So RIGHT NOW is state A (entitled, live) —
  NOT a testable down-state. The genuine down-state (session.start fails) is TIME-dependent: bbcomm's
  session must expire (overnight → ~07:00). Cannot force it cleanly on demand without care.
- dapi_check REFINEMENT (open): SPX rides bbcomm across a logout, so SPX can read UP while the
  login-scoped entitlement is dead ("entitlement dead" mode, cf. runbook 08-11 12.5h). Stricter
  discriminator = `.ST`. Consider switching dapi_check's probe SPX→.ST. Not urgent (the primary
  08-16/17 mode is session.start-fails, already caught).

**CURRENT STATE (~1715Z):** wintrv=0 (Andrew exited), 8194 listening, SPX+.ST BOTH resolve = entitlement
LIVE. Dashboard served `data_as_of 2026-08-17` (correct Tue T+1). Fire-once ledger last entry
`2026-08-14T15:43:59Z` (>6h → clear). Box up 5d, zero crashes.

**NEXT STEPS:**
1. **THE TEST** (needs a genuine down-state): wait for the next real 07:00 down IF the Terminal is
   logged out overnight, OR — with Andrew present — force a down-state (kill bbcomm while logged out and
   confirm session.start then fails / `.ST` dies), then run the full fallback:
   ```
   python integrations/bloomberg/auth/bbg_credentials.py -- powershell -NoProfile -ExecutionPolicy Bypass -File integrations/bloomberg/auth/bbg_fallback.ps1
   ```
   Watch: DAPI DOWN → P0 → fire-once → fill (full-tree-kill `-Fresh`, settle, retry ≤3) → verify →
   submit ONCE → recheck. SUBMIT is authorized on a real down + Andrew's go; NEVER loop the real submit.
   On success: run `scheduled_daily_pull.cmd` to refresh the dashboard, verify at the served object.
2. Then WS-2/WS-3 (restart auto-recovery + Tailscale, staged `C:\opal-elev\`) — gated on ONE elevated
   console session (WS-4); Andrew is helping with the human parts (Splashtop client on his laptop).

**SAFETY:** the programmatic verify aborts a bad fill at ZERO Bloomberg attempts (proven 08-16/17).
Fire-once on submit (Bloomberg locks on repeats). NEVER log out a WORKING Terminal to test. Creds via
bbg_credentials.py (AWS secret `bloomberg/terminal/login` — never printed). Ledger: `~/.bbg_signin_attempts.json`.
