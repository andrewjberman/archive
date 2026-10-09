# TO18 leg C closure

Issuer GO 107414 after X1 at 22:27Z. Plain no-var, no-target locked root plan and saved safe-apply: 0 add / 1 change / 0 destroy, aws_iam_policy.dell2_ssm policy only. Live policy equals canonical closed policy. UpdateDate 2026-10-08T22:34:24Z; readback 22:34:46Z.

ssm:SendCommand on AWS-RunShellScript: explicitDeny, cloudops-dell2-agent-ssm-policy, Sid DenyShellDocuments. F1 instance alone remains allowed by standing per-user policy; the shell-document plus F1 request is denied by the explicit document deny. No SSM command sent.

AC1 sendcmd_ok=34/34 shellwin_ok=18/18 all_ok=True. AC2 default full-root replan no changes, exit=0. Evidence: AC1.txt, plan.json, apply.txt, live-policy.json, live-simulations.json, replan.txt in this directory.

Leg A previously applied 20:29:25Z (2fd495e5c1); leg B opened 20:49:58Z (260879f234). Leg C is now closed. The 2026-10-09T06:00Z hard-close deadline and 05:55Z reminder are retired; no future closure apply is needed.

Ledger org/critical_paths/change_management/20261008T2232Z_d2-legc-close-laptop-20261008_deploy_completion.md CLOSED, C1/V1 proven, sentinel removed; open commit 703be341f3. No policy source edits. Measured origin/CLOUD 709d093fa95f5f33bd8d8ea1937dcb6666542bf7; no push by this seat. Final closure commit supplied in issuer message.
