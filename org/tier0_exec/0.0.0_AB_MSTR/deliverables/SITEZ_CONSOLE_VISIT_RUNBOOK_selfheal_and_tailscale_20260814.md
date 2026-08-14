# SITE Z CONSOLE-VISIT RUNBOOK -- make the Bloomberg box self-heal + private-reachable

**One elevated console session closes everything.** Written 2026-08-14 from the outage/crash
investigation (LD-0409) + the auto-recovery design. Executable by anyone who holds an elevated
console on that box -- Andrew in person, or a session he directs. **Nothing here needs the internet
or this conversation; everything referenced is staged on the box.**

## WHY THIS EXISTS (one paragraph)

The box crashes unpredictably (~13 stops in 24.7d, a class that leaves no dump and cannot be
diagnosed after the fact -- LD-0409). We cannot prevent the crashes. **This makes RECOVERY
automatic** so a crash costs minutes, not the 18h it cost 2026-08-12. Every step below is an
**owner administering his own standalone box** -- there is no external dependency and no MSP
channel involved (the box is workgroup-joined to nothing; its only remote access is the MSP's,
which is exactly why a private path is being added).

## PRECONDITION: get an elevated console

The box is a standalone workgroup machine, NAT'd (172.16.200.184), no Azure AD / Intune / WinRM.
**Every headless elevation path was proven closed** (UAC secure desktop; Task Scheduler can't be an
elevation source; Splashtop/N-able/AMT are all the MSP's). So elevation = **a human at the console**
(physically, or the MSP grants a session / AMT credentials). Once you have an admin PowerShell, the
rest is two pastes.

> **Deliberately NOT used:** a UAC auto-elevation bypass. It would work (owner + admin account) but
> trips the MSP's active EDR, defeating the *private* intent. Quiet-in-person is the chosen path
> (Andrew, 2026-08-14). A future session must not "helpfully" reach for the bypass.

## STEP 1 -- TAILSCALE (private remote access)  [staged: C:\opal-elev\install-tailscale.ps1]

```
C:\opal-elev\install-tailscale.ps1
```
- Installs the signature-pinned MSI, runs `tailscale up`, **prints a login URL to
  `C:\opal-elev\install-transcript.txt`, and stops.** It does NOT authenticate.
- **Open the URL in a browser and approve the node into `goldengate.dev`** (Andrew's identity -- this
  is what keeps the box on his tailnet and no one else's).
- Confirm from the laptop: `tailscale status` shows the box as a peer. **Two-sided, or not done.**

## STEP 2 -- SELF-HEAL ON RESTART  [staged: C:\opal-elev\setup-autorecovery.ps1]

```
C:\opal-elev\setup-autorecovery.ps1
```
Sets up the two layers that turn a reboot into an unattended recovery:
- **Auto-login** (Sysinternals Autologon / LSA-secret preferred over plaintext `AutoAdminLogon`) ->
  the interactive desktop the pull + agents require exists on boot. The script **verifies the
  auto-login user is the same profile** that holds the persisted Claude auth token + the two
  prompt-suppression flags (`skipDangerousModePermissionPrompt`, `hasTrustDialogAccepted`) -- a
  profile mismatch is a silent stall.
- **Logon launcher** -> a logon task runs `ajb -Headless <serial>` for `0.0.0_AB_MSTR~Z` and the BG
  Bloomberg serial. `-Headless` **drops the bypass-permissions fork and disallows the strand-tools**,
  so the agents come up authenticated and autonomous with nobody typing.
- Idempotent, before-state captured, and carries an explicit **teardown/OFF** path (auto-login is a
  security-posture change -- physical access becomes an unlocked session -- so it must be undoable).

**⛔ Does NOT wire in the Bloomberg AWS-secrets sign-in.** The Bloomberg entitlement survives a reboot
(proven 2026-08-13); that sign-in is a fragile GUI-coordinate **emergency** remedy whose failure mode
is a **locked Bloomberg account**. It stays human-supervised, out of the boot chain.

## STEP 3 -- BIOS / firmware, while you are at the box (one trip, four answers)

1. **AC Recovery / "Restore on AC Power Loss" -> ON.** Auto-login + auto-launch only help once the box
   BOOTS; this makes it auto-boot after a power loss. Together = true self-heal.
2. **Read the Dell BIOS event log** -- firmware-level, survives power loss; the only instrument that
   can see a thermal/power trip the OS never witnessed (the both-zero crash class).
3. **AC-recovery answers the OFF-vs-power-loss discriminator too**; and check **whether the 08-13
   17:37 boot** was a remote AMT/WoL wake (would be positive evidence for power-loss) vs physical.
4. **Physical:** vents/dust/enclosure/fan -- a Micro-form box in a closed cabinet is a thermal story
   on sight.

## STEP 4 -- UPS (the one hardware buy; do it regardless of anything above)

The box has **no UPS, no battery** -- a building/circuit power event is unopposed on the sole
Bloomberg terminal + sole dashboard producer. **Buy a MONITORED UPS** (network card, or USB +
monitoring software) -- **NOT a bare battery backup.** The output-load reading is what makes the next
crash decidable (off draws ~0W, hung still draws power); a dumb UPS prevents the power cause but
**diagnoses nothing.** Spec detail in LD-0409.

## AFTER (acceptance)

- Tailscale: Andrew completes a real off-site session **with the box's agents dark** (that is the
  point -- if it only works with a live Claude session on the box, nothing was built).
- Self-heal: the next reboot brings agents back unattended in minutes. A future 07:00 miss caused by
  a reboot then self-heals.
- **The SSH leg** (optional, second sitting): OpenSSH Server is a *second* install and its port-22
  rule must be **scoped to the tailnet (100.64.0.0/10) in the same sitting**; PowerShell there is 5.1.

## OPEN, AT ANDREW (not blockers to the above)

- **AMT (Intel vPro)** is provisioned on the box and is the MSP's. It is the *ideal* instrument for
  the crash class (force a dump / KVM / power-read on a dark box, below OS + UAC). Obtaining the AMT
  credentials from Little Dog Tech would solve diagnosis AND elevation -- **an MSP conversation, not
  an action we take.**

## Source records
LD-0409 (crash + fix design) - LD-0408 (agentbus fix) - the 08-13/08-14 session logs - staged
artifacts under `C:\opal-elev\` on the box.
