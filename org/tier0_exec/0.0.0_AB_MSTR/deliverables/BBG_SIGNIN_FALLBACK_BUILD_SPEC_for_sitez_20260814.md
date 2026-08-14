# Bloomberg Terminal Sign-In Fallback -- BUILD SPEC (site-Z fabric builds)

**Authored by** `0.0.0_AB_MSTR` (laptop) **for** `0.0.0_AB_MSTR~Z` (site-Z) to route into the
site-Z fabric. Laptop MSTR stays the comms line to Andrew; site-Z fabric owns the build.

## Authorization (moratorium exception -- he explicitly asked, twice)

Andrew-direct 2026-08-14, verbatim: *"that needs to be a dedicated fall back if port 8194 bbg is not
open"* and, refining the design, *"the terminal upload skill should have a check if the blpapi is
active/available if the port is working, and if not then it runs this."* The build commit carries an
inline `# andrew-asked: 2026-08-14 "terminal upload skill checks blpapi/8194, runs the sign-in if
not open"` marker (sanctioned moratorium exception).

## Purpose

Close the mid-session-Terminal-logout gap today's incident exposed (Terminal logged out overnight,
no agent to re-login, 07:00 pull failed, dashboard stale). This is DISTINCT from the reboot-recovery
gap (no reboot fires, so no logon trigger). The durable-est fix is keeping `0.0.3_BG_BBGTerminal`
alive; this fallback is the mechanism that self-heals the login regardless.

## Design (Andrew-specified integration point)

**Integrate the fallback INTO the terminal upload skill itself** -- NOT a standing separate monitor:
1. **At the upload skill's start, CHECK blpapi/DAPI availability (port 8194 open + a real
   `bloomberg_health` probe).** Use the incident's discriminator, not just a port ping: bbcomm can be
   "up but loopback-only" while the entitlement is dead -- the **8194 listener + a `//blp/refdata`
   health call** is the true test.
2. **If available -> proceed with the upload normally.**
3. **If NOT available -> run the sign-in (`C:\opal-elev\bbg_signin.ps1`, the PROVEN typer from
   today's recovery @9ec85e4f6e), then re-check availability, then proceed with the upload.**

## The action = the proven typer, made UNSUPERVISED-safe

The sign-in mechanism is the phased typer proven in today's recovery: fill + foreground-verify +
click-not-tab + SendKeys-escaped + screenshot-before-submit. **For the unsupervised fallback it must
be made STRICTER and headless-capable than today's human-supervised run:**

- **C1 -- FIRE-ONCE-THEN-ESCALATE, NEVER A RETRY-LOOP.** Bloomberg **locks the account on repeated
  failures.** Exactly ONE sign-in attempt per trigger; on failure, ESCALATE to a human via a
  sanctioned channel and STOP. A persistent attempt-guard (lock/counter with state, the existing
  1-per-6h ledger) blocks a second automated attempt until a human clears it. *(Today's supervised
  run had Andrew's explicit 2-attempt allowance; the UNSUPERVISED fallback does NOT -- one attempt.)*
- **C2 -- AGENT-INDEPENDENT.** Today's root cause WAS a dead agent. The fallback lives in the upload
  skill's own execution path (Task-Scheduler-driven), so it fires with no agent alive.
- **C3 -- AUTOMATE THE SCREENSHOT-VERIFY.** Today a human read the 5x-zoom screenshot (username
  correct + 9 masked dots) BEFORE submit -- that gate is what let the submit be confident and kept
  typing errors at ZERO Bloomberg attempts. Unsupervised, there is no human: the verify must be
  **programmatic** (OCR/image-check the username field + count the masked dots) and must **abort
  before submit** if it does not verify -- preserving the zero-attempt-typing-error property. This is
  the one genuinely new engineering piece.
- **C4 -- P0 CHEAP-REMEDY GATE first** (the runbook's: confirm transport truly down, not a network
  fault, cheap remedies eliminated) BEFORE any sign-in, so the fallback never fires on a transient.
- **C5 -- CREDENTIALS** from AWS Secrets Manager env-injection, never logged/printed/written.

## Acceptance (confirm to laptop MSTR with evidence)

1. Upload skill checks availability (8194 + health) at start; on down, runs the sign-in then
   proceeds; on up, proceeds directly.
2. The fire-once + escalate-on-failure + automated-screenshot-verify guards are demonstrated (a
   second trigger inside the window does NOT fire a second sign-in; a mistyped field aborts pre-submit
   at zero Bloomberg cost).
3. On a real down->sign-in->up, the pull publishes T-1 and the served object advances (content-
   verified + `.ST` content check, per today's runbook).

## Test-plan constraint

Exercise trigger + guards **without risking the account** (stub the submit to test guard logic;
exercise the real sign-in only in a path with Andrew's explicit go). **Never loop the real sign-in.**

## Ownership + flow

Site-Z fabric builds it (MSTR~Z routes). Laptop MSTR is the comms line. **Confirm to laptop MSTR when
done, with acceptance evidence; I relay to Andrew.** Today's recovery already proved the sign-in half
end-to-end (1/2 attempts, account safe); the remaining new work is the **availability-check
integration + the automated screenshot-verify + the fire-once-then-escalate hardening.**
