# Never-widen half (COO) -- OG-rl-15, the r29 gateway release

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~06:1xZ.
Against: the ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/ANNOUNCE_OG-rl-15.md` at
`368e48e533` (worker branch `wk-NFRA_OPLGTW-32-43`; read it with `git show 368e48e533:<path>` until the drain lands),
section 13 Half 2 and section 14. Pinned to release sha `91811b648ab119e73e22f8d401dd09f45b8ab19b`.

## What I read before signing

- **Release sha exists** as a commit, and it is the HEAD of `C:/tmp/og-rel29`. The rollback tree `C:/tmp/og-rb29` is at
  HEAD `aa75078e1b72a28219e6148d3ec8e9bf705ea111`, the live base the ask names.
- **The Terraform act** is `98501422dc`, read as a diff. It adds one `data "aws_secretsmanager_secret"` read for
  `gateway/mail/commassist-bearer` and one ARN line in `aws_iam_role_policy.gw_gateway_read_secrets`. The rest is
  comments. The plan must show exactly one resource updated in place (the policy) and nothing created or destroyed. Any
  other plan shape stops the act.
- The Phase A tooling and the ANNOUNCE are on the worker branch only. The drain is refused by the row gate's corpus
  pass on a tuple outside this project (NFRA_MCPMSP-Z-S4, routed to `0.0.0_AB_MSTR~Z`, 06:03Z).

## SIGNED: the acts, their order, the restart (Half 2)

**Order, as section 13 lists it, by the applier `0.7.0_AE_CloudOps~Z` under an apply order this seat cuts:**
1. Create the secret `gateway/mail/commassist-bearer`. Its value is never printed or committed. The existing
   `gateway/mail/bearer` is never written.
2. Plan, then `bash .tools/safe-apply.sh` the one policy line, with its own ledger entry opened and closed. Live
   read-back: `get-role-policy` shows exactly five ARNs. `simulate-principal-policy` reads allowed on the five and
   implicitDeny on a sibling `gateway/*` secret.
3. Re-read the live host by md5. A moved live re-cuts the release; nothing deploys on a moved base.
4. NEVER-2 ledger `nfra-oplgtw-gateway-release-r29`, entry and sentinel committed before the deploy.
5. `before` reads, then the deploy from `C:/tmp/og-rel29` through `infra/aws/ec2/safe-ec2-deploy.sh` with
   `DEPLOY_BASE_REF=aa75078e1b`. The halt gate is dry-run first (rc 0).
6. The `after` reads IMMEDIATELY. The R45 bun fetch count must be 0.
7. Manifest recorded by hand on the worker branch.
8. Ledger closed.

**Window:** 11:00Z-23:00Z only.

**Writers of what moves, counted.**
- The host `.env`: ONE writer, the deploy script. It changes the values of `MAIL_BEARER` and `MAIL_BEARER_LABELS` and
  adds `MAIL_SENDER_DOMAIN_TABLE`. The `after` read refuses any other changed value hash (`--expect-changed`).
- The host role's secret reach: ONE writer, the Terraform policy above.
- The secret: ONE writer, the applier's create.
- The restart: one service restart, MainPID changes.

**Both branches, from the deploy's own rule.**
- (a) Every `after` read holds: tools 66, consent 9, `/health` 200, md5 98/98, R45 count 0, only the expected `.env`
  hashes moved. The release stands, and Phase C may follow on the issuer's continuation.
- (b) Any one fails. The applier rolls back the whole release in one act: redeploy `aa75078e1b` from
  `C:/tmp/og-rb29` with `DEPLOY_BASE_REF=91811b648a`. The ledger records the trigger and a BLOCKING row names this seat.
- The deploy itself refuses a character outside a domain list and an unreadable or empty new secret. Both are branch
  (b) before any restart.

**Rollback per key.**
- Host code: the rollback redeploy above restores all 11 host files, and the contract returns to 1.3.
- Policy line: revert `98501422dc` and `safe-apply`. The fifth ARN leaves; the four stand.
- Secret: scheduled deletion by the applier, only after the policy line is reverted and only on Andrew's word. An S3 or
  secret delete is a human-confirmation act under the autonomy rule.
- **Order constraint, binding:** if Phase C has written Alyssa's 13-month grant, that grant is rolled back (prior reach
  re-activated, revision 5) BEFORE any gateway rollback. The older parser refuses `calendar_months`, so the reverse
  order would cut her Schwab tools.

**A revoked concierge family is not a rollback trigger.** It is re-authentication (ask section 12), reported the same
hour.

## SIGNED: Phase C (section 14), conditional

The blast radius is ONE principal (Alyssa's) and ONE field (`scope.dates.calendar_months` = 13, revision 3 -> 4). The
writer is the operator CLI only (N = 2 writers; the Lambda refuses the field). Prior reach is recorded before the
write. Both branches:
- (a) The grant parses, and the 13-month read returns at least 1 qualified date per master.
- (b) A refusal at `prepare()` or at the re-read writes nothing.

Rollback is activating revision 3's scope as revision 5. Phase C runs only after branch (a) of the release, on the
issuer's continuation naming it.

## Not covered

- Any Bloomberg-account change; r29 carries none (A6).
- The OG-tg-1 and OG-pf-1 changes; they ride r30.
- Andrew's profile; he has none (D3).
- A deploy outside the window, or from any sha but `91811b648a`.

-- 2.0.0_SA_COO~O
