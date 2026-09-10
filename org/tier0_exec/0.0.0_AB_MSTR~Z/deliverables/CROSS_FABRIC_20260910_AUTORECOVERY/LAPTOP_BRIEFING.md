# AUTO-RECOVERY FOR THE LAPTOP FABRIC — briefing for `0.0.0_AB_MSTR` (base)

**From:** `0.0.0_AB_MSTR~Z` (site Z) · **2026-09-10** · **Andrew-direct**, verbatim:

> *"Whatever the script is that we set up that autoloads MSTR~Z at startup on sitez box, i want a
> briefing and all relevant scripts etc in a zip issued to MSTR on laptop box, as I need that
> function on laptop, a restart should trigger a load of that agent."*

**This is a WORKING mechanism, not a design.** It fired on site Z at **06:18:56Z today** and launched
the `0.0.0_AB_MSTR~Z` session that wrote this briefing. Three fires are in its log
(`2026-09-05T00:37`, `2026-09-09T08:29`, `2026-09-10T02:18` local).

⛔ **AND TODAY IS THE CASE FOR INSTALLING IT ON THE LAPTOP.** At 06:35:24Z your RMM (`winagent.exe`)
initiated a restart; a Windows OS upgrade followed; every seat on that device died at 06:43:35Z and
**the laptop fabric stayed dark for five hours** until Andrew relaunched by hand at ~11:50Z. Site Z
took no such outage — but when site Z *has* been restarted, this chain brought it back unattended.
That five-hour window is exactly what this closes.

---

## 1. THE MECHANISM — three layers, only one of which needs elevation

| layer | what it does | needs elevation | on the laptop |
|---|---|---|---|
| **1 — auto-login** | Windows logs the user in on boot (`AutoAdminLogon` + LSA secret) | **YES** | **decide deliberately — see §4** |
| **2 — auto-launch** | a **logon** Scheduled Task runs `ajb -Headless <serial>` per agent | no | the part you want |
| **3 — Bloomberg pull** | 07:00 task, entitlement survives reboot | no | **site-Z only. Not applicable.** |

**Layer 2 is the whole answer to Andrew's ask**, and it works because `ajb -Headless` is purpose-built
for human-free launch: it drops the dev-channel Y/N prompt and passes
`--disallowedTools AskUserQuestion EnterPlanMode ExitPlanMode`, so a session can never strand on a
prompt nobody is there to answer.

## 2. ⛔ THE ONE THING THAT WILL CATCH YOU: IT IS A **LOGON** TRIGGER, NOT A **BOOT** TRIGGER

`MSFT_TaskLogonTrigger`, 30-second delay. **It fires when a user logs on — not when the machine
boots.** So:

- Laptop reboots and **Andrew logs in** → the task fires, agents come up. ✅ *This alone satisfies
  "a restart should trigger a load of that agent" whenever a human is present.*
- Laptop reboots and **nobody logs in** → Windows sits at the lock screen, **no logon event, nothing
  fires, the box is dark indefinitely.** ❌

**That gap is precisely why layer 1 exists.** Unattended recovery = layers 1 **and** 2. Layer 2 alone
= recovery that waits for a human to log in. Both are legitimate; they are different products, and
Andrew should choose knowingly rather than discover the difference after the next RMM restart.

## 3. ⛔ FOUR DEVICE-SPECIFIC VALUES YOU **MUST** CHANGE — every one fails differently

These scripts are site-Z originals, byte-identical, deliberately **not** pre-edited for the laptop —
a guessed path is worse than an obvious blank. Change all four:

**`autolaunch-agents.ps1`**
1. **`$serials`** — currently `@('0.0.0_AB_MSTR~Z','0.0.3_BG_BBGTerminal')`. Site-Z roster. The laptop
   wants `0.0.0_AB_MSTR` (**no `~Z` suffix**) plus whatever else Andrew names. A wrong serial here
   launches a session that registers under an identity nobody expects.
2. **`$root` fallback** — hardcodes `C:\Users\Opal Bloomberg\Desktop\ajb_workspace`. **The script
   already honours `$env:OPAL_WS_ROOT` first**, which is the clean fix; set that machine-wide and the
   fallback never runs. The script's own comment says *"NEVER hardcode the laptop path"* — honour it.

**`setup-autorecovery.ps1`**
3. **`$targetUser = 'Opal Bloomberg'`** — the laptop's interactive user is different. This value feeds
   the auto-login registry write *and* the profile gate below; wrong here and the gate checks the
   wrong profile.
4. **`$root`** — same path issue, and it is used to build the trust-dialog lookup key.
   ⚠ **That key is FORWARD-SLASHED** inside `.claude.json`:
   `projects['C:/Users/.../ajb_workspace'].hasTrustDialogAccepted`. Backslashes there read as absent
   and the gate fails for a reason that looks like a missing flag.

## 4. THE PROFILE GATE — read this before enabling auto-login

`setup-autorecovery.ps1` **hard-verifies three things and aborts** rather than enabling auto-login into
a stall:

```
~/.claude/settings.json     skipDangerousModePermissionPrompt = true
~/.claude.json              projects['<root, forward slashes>'].hasTrustDialogAccepted = true
~/.claude/.credentials.json present
```

⛔ **These are PER-USER-PROFILE.** If auto-login signs in as a user whose `~/.claude` lacks them, the
headless launch prompts anyway and the box auto-logs-in to a Claude prompt nobody can answer — strictly
worse than staying at the lock screen, because it *looks* recovered. Verify against **the laptop's
actual auto-login user**, not whichever profile you happen to be running as.

## 5. WHAT IS IN THE ZIP, AND WHAT IS NOT

| file | role | sha256 (site-Z original) |
|---|---|---|
| `autolaunch-agents.ps1` | layer-2 launcher the logon task calls | `949ae210ec113fcb…c584ef7d5` |
| `setup-autorecovery.ps1` | elevated one-paste install + `-Teardown` | `6277a43e5c45351a…059b7de2` |
| `install-tailscale.ps1` | the Tailscale bridge, included for §6 only | `1a93e6c97c1f2eac…a0543177` |
| `AUTORECOVERY_DESIGN.md` | the original design record, unedited | `4b70cf8ba44a6c37…a1609082` |
| `LAPTOP_BRIEFING.md` | this file | — |

**Excluded deliberately, so you know the denominator rather than wondering:**
`tailscale-setup-*.msi` (38 MB — the laptop is already on the tailnet and needs no installer);
`AutoLogon.zip` (Sysinternals — download from source, safer than a ferried binary);
`winlogon_before.reg` (site-Z's **own** restore point — useless and actively misleading elsewhere);
screenshots and runtime logs.

⚠ **`install-tailscale.ps1` is included for reference only.** Do **not** run it on the laptop — that
node is already enrolled. It is here because §6 quotes its design intent.

## 6. THE SECOND SITTING THAT NEVER HAPPENED — relevant to Andrew's other ask

`install-tailscale.ps1` says, in its own header:

> *"No sshd here (that is the second sitting, with a tailnet-only firewall rule, after the node is
> approved)."*

**That second sitting was never held on either box.** Measured today:

```
site Z    sshd service NOT PRESENT · nothing listening on :22 · tailscale RunSSH=false
laptop    :22 OPEN (a real OpenSSH server) · :3389 · :445 · :135 · tailscale RunSSH=false
```

So the two devices are **asymmetric**: the laptop exposes a conventional OpenSSH server over the
tailnet, site Z exposes nothing. Neither has **Tailscale SSH** enabled. That is with Andrew as a
separate decision; nothing in this package changes it.

⭐ **AND THE PRINCIPLE IN THAT SCRIPT SHOULD SURVIVE THE COPY:** *"An agent never enrols a machine onto
the owner's private mesh — and neither does this script."* It stops at the login URL by design and
lets Andrew approve under his own identity. **Whatever remote-access posture gets chosen, an agent
should not be the thing that opens it.**

## 7. WHAT TO DO, IN ORDER

1. **Read** `AUTORECOVERY_DESIGN.md` — it carries the reasoning, including why the Bloomberg sign-in
   is *deliberately* excluded from any unattended boot chain (GUI-coordinate automation, unexercised,
   and Bloomberg locks accounts on repeated failure).
2. **Edit the four values in §3.** Do not run anything unedited.
3. **Decide layer 1 with Andrew** (§2). Layer 2 alone gets you login-triggered recovery, which may be
   all the laptop needs if he is normally at it.
4. **Run `setup-autorecovery.ps1` from an ELEVATED PowerShell.** It captures a restore point first and
   the profile gate aborts on mismatch. **`-Teardown` reverses it.**
5. **Test with one real reboot** and confirm on artifacts: `autolaunch.log` gains a fire, and the
   seats register on the broker. A task that *ran* is not a task that *worked*.

⛔ **NOT AUTHORIZED BY THIS PACKAGE:** auto-login is a **standing posture change** — anyone with
physical access gets a logged-in desktop. Site Z accepted that on Andrew's explicit directive for that
box. **That acceptance does not transfer to the laptop**, which is a different machine in a different
place. It is Andrew's call, separately, and this briefing does not make it.

## 8. A FRAGILITY WORTH FIXING WHILE YOU ARE HERE

⛔ **NONE OF THIS IS IN THE REPOSITORY.** Measured: `comp-find --name 'setup-autorecovery*'` and
`--name '*autorecovery*'` both return **0 hits across 55,554 files**. The entire auto-recovery chain
lives only in `C:\opal-elev\` on the site-Z box — untracked, unversioned, and **lost with the
machine**. It is also precisely why the laptop never had it: there was nothing to pull.

**Recommendation (not an act — this is base's call for its own tree, and a shared-surface decision
either way):** land these under version control so the mechanism survives its device and both fabrics
can diverge visibly rather than silently. Site Z has not done this unilaterally because the natural
home is a shared path and the two devices genuinely need different values in it — which is a design
question, not a copy.
