# FU-s-11 Part 1 -- Claude-in-Chrome feasibility on the Fidelity box

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-20. Box: i-028e830f7226cc685 (Amazon Linux 2023.12, t3.medium, 3.8 GB RAM, running throughout).
No Fidelity sign-in was made, the Wealthscape secret was not read, the instance was not stopped or started. No credential value
appears in this file. Every line is MEASURED on the box (M) or taken from the vendor documentation (D, URL named).

## The four facts

plugin_installable=yes
  Reason (M): the Chrome Web Store extension "Claude" (id fcoeoabgfenejglbffodgkkbkcdhcgfn, version 1.0.101, manifest v3, needs
  nativeMessaging/debugger/tabs) force-installed into Google Chrome 155.0.8059.84 on the box through the ExtensionInstallForcelist managed
  policy, in a SCRATCH profile under /tmp (the vendor documents 1.0.36 or later as the minimum). The temporary policy file and the scratch
  profile were removed in the same command (checked: policy_present=no profile_present=no leftover_procs=0). It is NOT installed into
  /opt/fidelity-uploader/profile: the policy directory is machine-wide, so a standing policy would load the extension into the scheduled
  puller's Chrome too, which is a ruling for the CTO. Branded Chrome 137+ ignores --load-extension, so the managed policy (or a human
  clicking Add in the Web Store on a viewable display) is the only install path.

claude_session_runs=no
  Reason (M, D): Claude Code 2.1.197 is installed on the box (nodejs 18.20.8 and npm from dnf, then npm install -g @anthropic-ai/claude-code;
  the vendor minimum is 2.0.73) and starts, but it has no login: /root/.claude does not exist and no credential is present. The Chrome
  integration needs a claude.ai account login with /login on a DIRECT paid plan (Pro, Max, Team or Enterprise); an API key or a
  setup-token cannot enable it (the vendor says Claude Code keeps Chrome integration off with those credentials), and Bedrock, Vertex or
  Foundry access does not count (D: https://code.claude.com/docs/en/chrome). The credential needed is therefore Andrew's claude.ai account
  login, and the same account and organization must also be signed in inside the extension. Nothing was logged in.

display=xvfb
  Reason (M): Xvfb 21.1.13 is installed and a headed Google Chrome launches under it (r1_checks fu10x is R1-FU10X-OK). The plugin drives
  Chrome through the extension, not through a screen, so an agent needs no viewer. No VNC server is installed (x11vnc, Xvnc, vncserver,
  tigervncserver all absent), so no human can SEE the display today.

needs=andrew_claude_ai_login_for_claude_code_on_the_box; andrew_signin_of_the_extension_to_the_same_account_and_org; viewable_display_for_that_one_time_extension_signin; ruling_on_a_standing_claude_ai_credential_on_the_box; ruling_on_a_machine_wide_extension_policy_vs_the_puller; ruling_on_the_documented_login_page_pause
  1. Andrew act, Claude Code: run /login on the box (a URL to open and a code to paste back; it needs an interactive SSM session). Free, uses his
     existing plan, no new spend.
  2. Andrew act, extension: sign in to the extension inside the Chrome profile. That needs a display a human can see; the box has none.
     A VNC server (dnf, no spend) reached by SSM port forwarding (the box has no inbound port) would do it. Not installed in Part 1.
  3. Ruling: a long-lived claude.ai login stored on a server is a credential-custody decision for Andrew and the CTO, not for this seat.
  4. Ruling: ExtensionInstallForcelist is machine-wide. To avoid loading the extension into the scheduled puller's Chrome, the agent-driven
     Chrome should use its own --user-data-dir only if the same profile directory is not a hard requirement; the order asks for the SAME
     profile (/opt/fidelity-uploader/profile), so the CTO must say which wins.
  5. RISK for Part 2 (D): the vendor states that "when Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually".
     Part 2 as written has the agent type the Fidelity credential at a login page and submit a text-message code. The plugin may stop at that
     page by design, which would end Part 2 at step one. This is documented behavior, not measured here (no sign-in in Part 1). Also unmeasured:
     whether Akamai Bot Manager and ThreatMetrix treat an extension-driven Chrome differently from the Playwright-driven one.
  6. First run of Claude Code with --chrome writes the native messaging host file under ~/.config/google-chrome/NativeMessagingHosts/ and
     Chrome must be restarted once to read it (D).

## Reachability from the box (HTTP status only, curl)

chromewebstore.google.com 200; clients2.google.com/service/update2/crx 200; registry.npmjs.org 200; dl.google.com 302; api.anthropic.com 404
(reachable); bridge.claudeusercontent.com 426 (reachable; upgrade required, the websocket bridge host the extension uses); claude.ai 403 to curl
(a bot challenge, expected for curl, not a block of the box).

## What this seat changed on the box in Part 1 (all free, all ASCII)

- Installed: nodejs 18.20.8 and npm 10.8.2 (dnf), @anthropic-ai/claude-code 2.1.197 (npm -g). Nothing else; no config, no login.
- Installed earlier under TO-FU-s-10: xorg-x11-server-Xvfb 21.1.13 and google-chrome-stable 155.0.8059.84.
- Temporary and removed: one managed policy file and one scratch Chrome profile (probe above).
- Unchanged: /opt/fidelity-uploader (code, config.json, profile, work, venv, bridge symlinks), the instance state, the Wealthscape secret.

## Verdict

Part 1 is complete. The plugin CAN be installed and Claude Code CAN be installed, but a Claude session CANNOT run until Andrew supplies the claude.ai login
(needs 1 and 2), and the vendor's login-page pause (needs 5) may stop Part 2. Part 2 should wait for the issuer's GO and Andrew's acts; the CTO rules
needs 3 and 4 first.
