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
  Chrome through the extension, not through a screen, so an agent needs no viewer. At the time of Part 1 no VNC server was installed (x11vnc,
  Xvnc, vncserver, tigervncserver all absent), so no human could SEE a display; Part 1b below installed one (display :1, localhost only).

needs=andrew_claude_ai_login_for_claude_code_on_the_box; andrew_signin_of_the_extension_to_the_same_account_and_org; viewable_display_for_that_one_time_extension_signin; ruling_on_a_standing_claude_ai_credential_on_the_box; ruling_on_a_machine_wide_extension_policy_vs_the_puller; ruling_on_the_documented_login_page_pause
  1. Andrew act, Claude Code: run /login on the box (a URL to open and a code to paste back; it needs an interactive SSM session). Free, uses his
     existing plan, no new spend.
  2. Andrew act, extension: sign in to the extension inside the Chrome profile. That needs a display a human can see; the box has none.
     DONE in Part 1b: a VNC server (dnf, no spend) on display :1, localhost only, reached by SSM port forwarding (see vnc= below).
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

## Part 1b (CTO rulings 8724): a VNC display for a human, localhost only

vnc=installed
  Reason (M): tigervnc-server-minimal 1.14.1-3.amzn2023.0.6 provides /usr/bin/Xvnc, run by the systemd unit fidelity-vnc.service
  (enabled and active): `Xvnc :1 -geometry 1440x900 -depth 24 -rfbport 5901 -localhost -SecurityTypes None -AlwaysShared`. Measured with ss -ltn:
  it listens on 127.0.0.1:5901 and [::1]:5901 only; the RFB banner (RFB 003.008) is readable from loopback and a connection to the box's own
  network address is refused. The security group fidelity-alongside-uploader-sg has 0 inbound rules (describe-security-groups), so the
  port is reachable only through an SSM port forward. The same box lists sshd on 0.0.0.0:22 (the Amazon Linux default, not changed here);
  it is likewise unreachable because of the 0 inbound rules.
  No password was set, none printed, none stored: the VNC leg uses SecurityTypes None because access is gated by the SSM StartSession
  permission on the instance, and anyone holding it can already run root commands through SSM. If the CTO prefers a VNC password, it is one
  dnf-free edit of the unit plus a root-only password file; say so and I add it.
  The display is :1, separate from the Xvfb displays the puller's checks use. The agent's Chrome is meant to run on DISPLAY=:1 with its
  own profile /opt/fidelity-uploader/profile-agent (ruling 2); this seat created neither the profile nor any extension policy.

The exact port-forward command Andrew runs from a machine that has the AWS CLI and the Session Manager plugin and his own AWS credentials with
ssm:StartSession on this instance, then points a VNC viewer at localhost:5901:

  aws ssm start-session --region us-east-1 --target i-028e830f7226cc685 --document-name AWS-StartPortForwardingSession --parameters "portNumber=5901,localPortNumber=5901"

Not tested end to end: the Session Manager plugin is not installed on this seat's machine, so the forward itself was not run here; the
box side (bind, banner, refusal on the NIC) was measured on the box. The instance role carries AmazonSSMManagedInstanceCore, which includes
the session channel permissions.

## CDP (TO-FU-s-11 re-cut, CTO ruling 8750): a Chrome a dell1 agent can attach to, not started

The plugin plan above (Claude account, Claude Code login, extension policy) is WITHDRAWN; its lines stay as a record. The browser stays on the box,
the controller is a dell1 agent that attaches by Playwright connect_over_cdp through an SSM port forward, the way the VNC screen is reached.

cdp_unit=installed_not_started
  Reason (M): /etc/systemd/system/fidelity-agent-chrome.service is on the box (md5 bef9f0bfd0cc6d7e57057f3a62830ed5). systemctl reads it
  is-active=inactive and is-enabled=static (the unit has no [Install] section, so it cannot be enabled at boot at all; it starts only by
  name). Nothing listens on 9222 and no Chrome runs on the agent profile. /opt/fidelity-uploader/profile-agent does not exist yet; the unit's
  ExecStartPre creates it at the first START. The puller's /opt/fidelity-uploader/profile is never named by this unit. No extension policy,
  no credential, no password anywhere. The unit text, verbatim:

    [Unit]
    Description=Fidelity agent Chrome (headful on display :1, CDP on 127.0.0.1:9222 only, own profile). Started only on the issuer's START.
    After=network.target fidelity-vnc.service
    Wants=fidelity-vnc.service

    [Service]
    Type=simple
    Environment=DISPLAY=:1
    ExecStartPre=/usr/bin/mkdir -p /opt/fidelity-uploader/profile-agent
    ExecStart=/opt/google/chrome/chrome --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir=/opt/fidelity-uploader/profile-agent --no-sandbox --no-first-run --no-default-browser-check
    Restart=no

  Display :1 is the VNC screen, so a person can watch. Wants=fidelity-vnc.service starts the VNC unit if it is not running and does nothing if it
  is; unlike Requires= it does not tie the two lifetimes together. Note the consequence: if the VNC unit is stopped, Chrome loses its display and
  exits on its own.

The exact commands (nothing has been run; the issuer's START and STOP gate them):

  start the unit, from any machine with the AWS CLI and credentials that may call ssm:SendCommand:
    aws ssm send-command --region us-east-1 --instance-ids i-028e830f7226cc685 --document-name AWS-RunShellScript --parameters 'commands=["systemctl start fidelity-agent-chrome.service"]'

  the SSM port forward of the CDP port (the same shape as the VNC one; leave it open while the agent drives; ssm:StartSession permission):
    aws ssm start-session --region us-east-1 --target i-028e830f7226cc685 --document-name AWS-StartPortForwardingSession --parameters "portNumber=9222,localPortNumber=9222"

  then the agent attaches to http://127.0.0.1:9222 on the forwarding machine (Playwright connect_over_cdp). To stop (on the issuer's STOP):
    aws ssm send-command --region us-east-1 --instance-ids i-028e830f7226cc685 --document-name AWS-RunShellScript --parameters 'commands=["systemctl stop fidelity-agent-chrome.service"]'

Risks to read before START (not measured, because the unit has not been started):
  - A CDP endpoint gives full control of a signed-in browser. The unit asks for 127.0.0.1 only and the security group has 0 inbound rules, but
    whether this Chrome build (155) honors --remote-debugging-address for a headful run is verified only at START by FU11-AC1 (it checks the bind).
  - Anyone with ssm:StartSession on the instance can open the forward and drive the browser; that permission is the whole access control.
  - The unit runs Chrome as root with --no-sandbox, as the order specifies, on a box that holds a Quo key and a Wealthscape secret grant.
  - The Claude Code CLI (2.1.197) and nodejs installed in Part 1 are still on the box, unused, no login. Not removed: the re-cut does not order it.

## Reachability from the box (HTTP status only, curl)

chromewebstore.google.com 200; clients2.google.com/service/update2/crx 200; registry.npmjs.org 200; dl.google.com 302; api.anthropic.com 404
(reachable); bridge.claudeusercontent.com 426 (reachable; upgrade required, the websocket bridge host the extension uses); claude.ai 403 to curl
(a bot challenge, expected for curl, not a block of the box).

## What this seat changed on the box in Part 1 (all free, all ASCII)

- Installed: nodejs 18.20.8 and npm 10.8.2 (dnf), @anthropic-ai/claude-code 2.1.197 (npm -g). Nothing else; no config, no login.
- Installed earlier under TO-FU-s-10: xorg-x11-server-Xvfb 21.1.13 and google-chrome-stable 155.0.8059.84.
- Installed in Part 1b: tigervnc-server-minimal 1.14.1 and the unit /etc/systemd/system/fidelity-vnc.service (localhost only, see above).
- Temporary and removed: one managed policy file and one scratch Chrome profile (probe above).
- Unchanged: /opt/fidelity-uploader (code, config.json, profile, work, venv, bridge symlinks), the instance state, the Wealthscape secret.

## Verdict

Part 1 is complete. The plugin CAN be installed and Claude Code CAN be installed, but a Claude session CANNOT run until Andrew supplies the claude.ai login
(needs 1 and 2), and the vendor's login-page pause (needs 5) may stop Part 2. Part 2 should wait for the issuer's GO and Andrew's acts; the CTO rules
needs 3 and 4 first.
