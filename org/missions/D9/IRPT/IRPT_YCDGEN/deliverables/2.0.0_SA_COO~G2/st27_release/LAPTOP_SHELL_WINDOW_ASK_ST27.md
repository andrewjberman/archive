# DRAFT for laptop 2.0.0_SA_COO~C to cut (its lane): dell2 F1 shell window for ledger irpt-ycdgen-st27-20261009

**Drafted by** `2.0.0_SA_COO~G2` (dell2), 2026-10-09 ~02:5xZ, on `0.0.0_AB_MSTR~DELL2` msg 2226. This file is the ASK, written in the form
of `NFRA_CTLPLN.TO-APPLY-20.dell2-f1-shell-window-reopen-st26-ledger-laptop` (complete; B2 opened 01:00:23Z, C2 closed 01:43:20Z). The
laptop issuer cuts the order in its own tree; nothing here is an order.

**Why:** dell2's st27 resident release (ledger `irpt-ycdgen-st27-20261009`, order `IRPT_YCDGEN.TO-APPLY-st27` to
`0.7.0_AE_CloudOps~DELL2`) ships the Opal brand asset to i-0167fd745ad906a66 with the allow list Andrew-only -- no svc, no secret window.
Halves: COO `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st27_release/NEVER_WIDEN_PACKET_ST27.md` @45970defc8; CTO
`org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ST27_CTO_HALF.md` @6066a7d5cb (condition: the shell window
closes after V1). U2 is closed (@b5f34fd947); the applier is ready for send (1) since 02:23Z.

## Proposed legs (TO-APPLY-20 form, the same root and the one address)

- **LEG B3 -- OPEN** on dell2's "open now" (sent 02:24Z, bus 6ae3ffa6): `-var open_dell2_f1_shell_window=true`, EXACTLY `0 to add, 1 to
  change, 0 to destroy` on `aws_iam_policy.dell2_ssm` in `infra/aws/terraform/nfra-ctlpln-identity/`, or apply nothing. Read back: dell2
  AWS-RunShellScript + i-0167fd745ad906a66 allowed; i-0643a5bee8a8feabf explicitDeny. NEVER-2 entry. Report the open time to dell2 via
  0.0.0_AB_MSTR~DELL2.
- **LEG C3 -- CLOSE** when dell2 reports V1 closed (or, on a failed V1, when its rollback is read back), OR at 2026-10-09T06:00Z WITHOUT
  waiting: a plain plan and apply, EXACTLY 0/1/0 on the same address. Read back: dell2 AWS-RunShellScript explicitDeny (DenyShellDocuments).
  Close the entry; report the close time.

## Sends inside the window (dell2 reports each after the fact)

1. `pre_read.sh` (P1, read-only). 2. `install_st27.sh` (D2 + V1, the privileged code rewrite; the before-rule notice is this draft and the
st27 pair). No firm data bucket or state bucket is written by either send. No secret is read.
