# FWD27 laptop-side read (TO NFRA_CTLPLN.TO-CT-ai-4, worker 0.9.0_WK_NFRA_CTLPLN~109)

Read by key from the laptop, run from the worktree root C:/Users/AndrewBerman/Desktop/ajb_wk/ctlpln-109 at
2026-10-15T13:09:13Z (start) to 2026-10-15T13:09:27Z (end), by `python .tools/tests/test_round19_fwd27_laptop_side.py`
on the test bytes of commit b265d96511 and its per-box login map. Read only: `hostname` by key and the tool's
no-password probe. No password was sent, no write was made on any box, nothing was run elevated.

Logins: the per-box map is the one recorded in the CT-ab-7 order,
`org/missions/D0/NFRA/NFRA_CTLPLN/task-orders/NFRA_CTLPLN.TO-CT-ab-7.ssh-tools-kbdint-and-replan.md` line 30:
sitez as `Opal Bloomberg`, dell1 and dell2 as `Test`. The identity is the tool's default
(`%USERPROFILE%\.ssh\id_ed25519`). Earlier runs at 12:41:50Z and 12:46:52Z used the client default login from
`ssh -G` (`AzureAD+AndrewBerman`); those were refused on all three boxes and are superseded by this run.

## Printed tool lines (verbatim)

```
BOX sitez 100.99.180.19 port22=OPEN key=ANSWERED:Opal_Bloomberg password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
BOX dell1 100.79.95.44 port22=OPEN key=ANSWERED:DESKTOP-HK1UU7N password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
BOX dell2 100.104.84.87 port22=OPEN key=ANSWERED:DESKTOP-N8RJV0A password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
SSH-VERIFY boxes=3 done=3 not_done=-
FWD27-LAPTOP-SIDE boxes=3 key_ok=3 password_refused=3 ok=True
```

Test exit code 0. `key_ok=3` of 3 boxes. The password arm is measured as `KBDINT-NO-PROMPT` on all three boxes
(keyboard-interactive is offered, no prompt is sent), which the tool counts as refused, so `password_refused=3`.
The tool's own verdict is `done=3` (port22 OPEN, key ANSWERED, password arm refused).

## FWD-27 arms this cell did NOT drive

| Arm | Why not driven | Owner |
|---|---|---|
| Key login from rc and from muse (Andrew's devices) | Not this laptop; the cell reads from the laptop only | Andrew |
| The laptop as a target (`hostname` by key to the laptop itself) | The laptop's only account is an Entra account sshd cannot resolve; a local administrator account on the laptop is needed first | Andrew (one line) |
| A login refused from an address outside the tailnet | Needs an off-tailnet address; the tool cannot source one (reads NOT-DRIVEN) | 0.0.0_AB_MSTR |
| Password login off on each box (PasswordAuthentication no) | Changing sshd is elevated; the tool sends no password and changes nothing. The read above shows the password arm refused by the tool's rule, not sshd configuration | Andrew (elevated line per box) |
