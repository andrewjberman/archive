# FWD27 laptop-side read (TO NFRA_CTLPLN.TO-CT-ai-4, worker 0.9.0_WK_NFRA_CTLPLN~109)

Read by key from the laptop, run from the worktree root C:/Users/AndrewBerman/Desktop/ajb_wk/ctlpln-109 at
2026-10-15T12:46:52Z (start) to 2026-10-15T12:47:09Z (end), by `python .tools/tests/test_round19_fwd27_laptop_side.py`
at commit b265d96511. Read only: `hostname` by key and the tool's no-password probe. No password was sent, no write
was made on any box, nothing was run elevated.

Logins: none is recorded in the CT-u-2 proof record or in CVO row 27 (see surprise rows NFRA_CTLPLN-W109-S1 and
NFRA_CTLPLN-W109-S2 in `org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md`). The
test passes the client default login that `ssh -G <box>` reports (`AzureAD+AndrewBerman`). A diagnostic `ssh -v` with
the same login, and a native Windows ssh with login `azuread\andrewberman`, were both refused on sitez and dell1.

## Printed tool lines (verbatim)

```
BOX sitez 100.99.180.19 port22=OPEN key=DENIED password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
BOX dell1 100.79.95.44 port22=OPEN key=DENIED password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
BOX dell2 100.104.84.87 port22=OPEN key=DENIED password_arm=KBDINT-NO-PROMPT:publickey,keyboard-interactive methods=publickey,keyboard-interactive nontailnet_arm=NOT-DRIVEN (this tool cannot source a non-tailnet connection; the firewall remote scope is read from the box's enable receipt)
SSH-VERIFY boxes=3 done=0 not_done=sitez,dell1,dell2
FWD27-LAPTOP-SIDE boxes=3 key_ok=0 password_refused=3 ok=False
```

Test exit code 1. Against the expectation `key_ok=3` the read is `key_ok=0`. The password arm is measured:
`KBDINT-NO-PROMPT` on all three boxes (keyboard-interactive is offered, no prompt is sent), which the tool counts as
refused, so `password_refused=3`.

## FWD-27 arms this cell did NOT drive

| Arm | Why not driven | Owner |
|---|---|---|
| Key login from rc and from muse (Andrew's devices) | Not this laptop; the cell reads from the laptop only | Andrew |
| The laptop as a target (`hostname` by key to the laptop itself) | The laptop's only account is an Entra account sshd cannot resolve; a local administrator account on the laptop is needed first | Andrew (one line) |
| A login refused from an address outside the tailnet | Needs an off-tailnet address; the tool cannot source one (reads NOT-DRIVEN) | 0.0.0_AB_MSTR |
| Password login off on each box (PasswordAuthentication no) | Changing sshd is elevated; the tool sends no password and changes nothing | Andrew (elevated line per box) |

The key arm itself was driven on sitez, dell1 and dell2 and read DENIED, so FWD-27's key-login arm is not met by this
read. The owner of the login name that each box accepts is Andrew; this cell cannot pick one without guessing.
