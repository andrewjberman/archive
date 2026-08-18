# OPAL_BGFALLBACK — Program Brief (site-Z device autonomy)

**From:** `0.0.0_AB_MSTR~Z` (site Z) · **To:** `1.0.0_SA_CTO~Z` (register + drive) · **Date:** 2026-08-18
**Andrew-direct 2026-08-18, verbatim intent:** *"fix the autonomous fallback in both cases restart and
mid-session, then proceed through the rest … register this project as OPAL_BGFALLBACK … we will also
structure additional work orthogonally to that."*

CTO~Z: **register `OPAL_BGFALLBACK`** (project record + PRD/TO scaffolding), then drive the workstreams
below in priority order. Andrew checks in as it proceeds. Orthogonal work is structured separately later.

---

## The problem, grounded (why this project exists)

The site-Z box is the **sole producer** of the client-facing OPAL_BBGTML model-portfolio dashboard and
the **only Bloomberg Terminal**. The daily 07:00 ET scheduled pull needs a **logged-in Terminal** (DAPI
on 127.0.0.1:8194). The Terminal drops out and nothing autonomously recovers it → the dashboard goes
stale until a human intervenes. **There are TWO independent trigger modes, and they take DIFFERENT
remedies (Rule 24(iv) state-coherence — one fix does not move both):**

- **MODE A — MID-SESSION LOGOUT.** The Bloomberg *session* logs out while the OS stays up. **Measured
  2026-08-14…18:** the box ran continuously 4d18h (uptime since the 08-13 boot, ZERO restart/crash
  events), yet the Terminal logged out over the weekend and the 08-15/16/17 pulls all failed on
  DAPI-down. Confirmed independently in the Yang Liu / Alyssa Teams thread (Alyssa signed Bloomberg back
  in 2026-08-17 17:43:36Z; the manual pull followed ~53s later). **A restart-oriented fix does NOT cover
  this — no restart means no logon trigger.**
- **MODE B — DEVICE RESTART.** MS/LDT overnight updates (or a crash) restart the box; Windows sits at a
  locked login (`AutoAdminLogon` unset), so no desktop, no agents, no Terminal, no pull. This IS the
  reboot-recovery gap.

**Current state of the fix:** an in-pull DAPI-check + sign-in fallback shipped @072ff64bcb (in
`scheduled_daily_pull.cmd`). It fires correctly on Mode A and its **safety half is proven** (the
programmatic screenshot-verify aborts a bad fill at ZERO Bloomberg attempts — 2-for-2 on the 08-16 and
08-17 firings, no lockout). **But its self-heal half is broken:** the unattended FILL fails (login window
already up → keystrokes do not populate the fields), so it aborts safely without signing in. **Guardrail
works; self-heal does not.** Mode B is staged but not executed (needs elevation).

---

## Workstreams (priority order)

### WS-1 — MID-SESSION SELF-HEAL: fix the fallback fill  [P0 — NO ELEVATION, START NOW]
The highest-value item: it fixes the *actual recurring failure*, needs no elevation, and can begin
immediately.
- **Files:** `integrations/bloomberg/auth/bbg_fallback.ps1` (orchestrator), `bbg_signin.ps1` (fill/submit),
  `bbg_verify.ps1` (C3 programmatic verify — proven), `dapi_check.py` (DAPI probe — proven).
- **Defect:** unattended `-Phase fill` leaves the fields empty (verify reads `dots:1, user:''`). Works
  supervised (Fri 08-14), fails unattended (08-16, 08-17). Likely focus/timing: `SetForegroundWindow`
  returns matched but the window is not truly input-ready when the login dialog is *already up* from a
  prior state, so the clicks/SendKeys land nowhere.
- **Fix approach (proposed — CTO to design):** after focus, **per-field**: click, `^a`+DEL, type, then
  **re-screenshot + programmatically verify that field populated**, and **retry the FILL** (not the
  submit) up to a small bound until the verify passes — THEN submit ONCE. Keep FIRE-ONCE on the SUBMIT
  (the lockout guard is on submissions; a fill-retry never submits). Consider: relaunch wintrv fresh if
  the found login window is stale; add settle delays; confirm the field has caret/focus before typing.
- **Acceptance:** a real unattended down→fill→verify→submit→up cycle self-heals and the pull publishes
  T-1. Test-plan constraint (standing): exercise fill/guards freely; **exercise the real SUBMIT only on a
  real down or Andrew's explicit go, and NEVER loop the real submit** (stub it for guard tests).

### WS-2 — RESTART SELF-HEAL: auto-login + auto-launch  [P1 — BLOCKED ON ELEVATION (WS-4)]
- **Staged:** `C:\opal-elev\AUTORECOVERY_DESIGN.md` + `setup-autorecovery.ps1` (+`-Teardown`) +
  `autolaunch-agents.ps1`. Auto-login via **Sysinternals Autologon (LSA secret, not plaintext)** + a
  logon-triggered Scheduled Task that launches the two agents (`0.0.0_AB_MSTR~Z`, `0.0.3_BG_BBGTerminal`)
  headless. The headless-launch flags (`skipDangerousModePermissionPrompt`, `hasTrustDialogAccepted`) +
  the persisted Claude auth token are verified present for the Opal Bloomberg user; the setup script
  hard-gates same-user before enabling.
- **Blocked on:** one elevated in-person console session (WS-4). Prep is done; execution is one paste.
- **Interplay:** WS-2 covers Mode B; WS-1 covers Mode A. Once WS-2 lands, an auto-launched BG agent also
  becomes a seat that *can* re-run the sign-in on a mid-session drop — but do NOT make BG a standing
  monitor (moratorium); the in-pull fallback remains the agent-independent Mode-A path.

### WS-3 — PRIVATE REMOTE-IN: Tailscale  [P1 — BLOCKED ON ELEVATION (WS-4)]
- **Staged:** `C:\opal-elev\install-tailscale.ps1` + signature-verified MSI (`tailscale-setup-1.102.2`).
  Hard-stops at the login URL (Andrew authenticates the node in his own browser; an agent never enrols
  the machine). Gives Andrew private reach to the box any time — the capability whose absence cost hours
  on the 08-13 diagnosis.
- **Note:** the box's only current remote access is the MSP's (Splashtop Streamer + N-able Take Control +
  Intel AMT, all LDT-owned). Tailscale is the first Andrew-owned channel.

### WS-4 — THE ELEVATION ENABLER  [P1 — the common blocker; needs Andrew]
WS-2, WS-3, and auto-login all require ONE elevated console session. Self-elevation from an agent is
impossible here (measured: UAC `ConsentPromptBehaviorAdmin=5` + secure desktop; SYSTEM/Highest scheduled
task registration denied; no Andrew-owned remote channel). **Routes:** the **Splashtop Business client on
Andrew's laptop** (the host Streamer is already running on the box), or physical at the console. Once
reached: run `install-tailscale.ps1`, then `setup-autorecovery.ps1`, then Autologon for the password.
Two pastes + a password, then one test reboot.

### WS-5 — FREEZE / HARDWARE HARDENING  [P2 — box stable 4d, but the instruments matter for #12]
The 08-12 freeze (#11) cause is unresolved (both-zero class, no dump). Open items:
- **OFF-vs-frozen at 17:37 on 08-13** — one human answer settles hang-vs-power-loss.
- **A MONITORED UPS** (network card / USB + software) — its output-load reading is the instrument that
  distinguishes powered-off from hung remotely; the sole-producer box currently has NO power protection.
- **Intel AMT credentials from LDT** — hardware OOB KVM + dump + power-read on a dark box (an MSP
  conversation; would solve both freeze-diagnosis and elevation).

### WS-6 — CROSS-FABRIC PARITY  [P3 — adjacent, non-urgent]
site-Z is ~266 commits behind origin/CLOUD (10 ahead). An `/integrate` when convenient; the fabrics work
separate projects so this is hygiene, not a blocker.

---

## Sequencing summary for CTO~Z
1. Register `OPAL_BGFALLBACK`; scaffold the PRD/TOs.
2. **Drive WS-1 now** (no elevation) — root-cause + fix the fill; it is the actual recurring failure.
3. Hold WS-2/WS-3 ready for the moment WS-4 (elevation) is unblocked by Andrew; the prep is complete.
4. Name WS-4 to Andrew as the single gate on WS-2/WS-3.
5. WS-5/WS-6 as capacity allows.

**Andrew will structure additional orthogonal work separately** — keep OPAL_BGFALLBACK scoped to device
autonomy (the two self-heal modes + their enablers).

## Pointers
- Shipped fallback + guard evidence: commit @072ff64bcb; recovery record
  `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260814_BLOOMBERG_SIGNIN_RECOVERY_EXECUTED.md`.
- Fallback spec (laptop-authored): `.../BBG_SIGNIN_FALLBACK_BUILD_SPEC_for_sitez_20260814.md` @c4eedad9a3 (LD-0413).
- Restart auto-recovery + Tailscale: `C:\opal-elev\AUTORECOVERY_DESIGN.md` + the staged scripts (out of repo).
- Exercised sign-in runbook: `org/tier0_utility/0.0.3_BG_BBGTerminal/deliverables/BLOOMBERG_TERMINAL_SIGNIN_RECOVERY.md`.
- Freeze investigation (outside repo): `Desktop\OPAL_BLOOMBERG_freeze_investigation_2026-07-30\`.
