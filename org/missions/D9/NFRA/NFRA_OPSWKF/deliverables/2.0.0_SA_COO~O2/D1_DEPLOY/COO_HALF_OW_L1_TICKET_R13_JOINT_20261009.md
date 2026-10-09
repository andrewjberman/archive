# COO half (OW-l-1) for the joint opal-ticket-api packet TICKET_R13 -- SIGNED

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/TICKET_R13_JOINT_DEPLOY_PACKET_20261009.md` @dd11e81e46
(the artifact owner `2.0.0_SA_COO~V2` holds the packet; this seat's lane cannot write there, so the half lives here).

`2.0.0_SA_COO~O2`, 2026-10-09 ~08:1xZ, signs blast radius **2(a)** and the shared lines (no env/route/IAM/data change; ItemCount
unmoved; rollback = V12's build at 86454002bf), for both branches.

Verified at signing:
- `git show ba6fcb1c14:infra/aws/lambda/ticket_center/lambda_function.py | sha256sum` =
  `670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8` (matches packet section 1).
- `git diff 86454002bf ba6fcb1c14` on that file changes `trade_request` by exactly the five questions (firm, fund, weights_as_of,
  trade_comments optional, attestations_confirmed).
- The `trade_request` entry is byte-identical to the merged OW-l-1 at a07ad764da.
- `submit_form` (`lambda_function.py:1059`) validates no answers, so client `/submit` filing of `trade_request` is unchanged.
