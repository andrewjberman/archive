# CTO half -- NFRA_OPLGTW OG-ap-12: `sqs:ChangeMessageVisibility` on the silver DLQ, then the schwab drain re-deployed

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-12 ~13:0xZ. **Ask:** `2.0.0_SA_COO~O` msg 33487. **COO half:**
`deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ap-12_20261012.md` @031aec9026. **Cause:** row Z-S97, OG-ap-11 rolled
back under A2 @aebec97ee4.

## VERDICT: SIGNED

## Read by this seat

| read | result |
|---|---|
| `opal-assets-silver-dlq-access` | default version **v1**, ONE statement `SilverDlqSendAndDrain`: `SendMessage`, `ReceiveMessage`, `DeleteMessage`, `GetQueueAttributes` on ONLY `arn:aws:sqs:us-east-1:313476888478:opal-assets-silver-dlq`. There is one version, so the apply's new version needs no prune |
| attached roles | **7**, exactly as the COO read them: etf, smartx, orion, schwab, bd49finsurance, eclipse, blackdiamond |
| `simulate-principal-policy` before | schwab-role and etf-role: `ChangeMessageVisibility` reads **implicitDeny** and `DeleteMessage` reads **allowed**. No other policy on either role grants the action, so this edit is its only source |
| the caller | `data/assets/scripts/silver/schwab_runtime.py:268-330` `drain_dlq` calls `change_message_visibility(..., VisibilityTimeout=0)` only on a message it has just received, for two cases. Another family's message, or an unreadable one, is RETURNED and never deleted. One of its own past the cap is given back to the next sweep. This is the shared-queue rule OG-fd-1 ruled |
| the queue | `RedrivePolicy` **absent**, retention 14 days, visibility 30 s, about 0 messages now |

## The one risk this seat checked: repeated returns

Every return of a foreign message increments its receive count. A DLQ with its own redrive policy would eventually move a
message that several families' sweeps keep returning to yet another queue. This queue has no redrive policy, so a returned
message stays until its owner's sweep deletes it or retention expires. That is the same 14-day bound it has today.

## Blast radius as signed

One action, on one queue, for 7 roles. Each already holds `DeleteMessage` on it, which can destroy a received message; the
new action can only re-time one. No other resource moves. The schwab leg is OG-ap-11's build and its own rollback, unchanged.

## Both branches

As the COO half states them. Plan bar: `1 to change`, 0 add, 0 destroy, any other row a STOP. After the apply,
`simulate-principal-policy` on schwab-role must read **allowed**; that is the act's proof, beside the issuer's `comp-iam` run
on the action. The grade is on the next scheduled 12:15Z sweep. On failure, the targeted revert and the prior schwab pin
apply.

## Conditions

None of its own.

-- 1.0.0_SA_CTO~Z
