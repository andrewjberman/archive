# Never-widen half (COO) -- OG-tl-1, the 4 NFRA_TRNSPT meetings onto TRANSCRIPT_MEETING_ALLOWLIST

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~12:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~48/NEVER_WIDEN_ASK_OG-tl-1.md` (drained
@0f5e74909f), release `78afad428389a4665aed267ac7f44e76533be59a` on `rel-nfra-oplgtw-tl1` (parent: stage commit
`4514246d65`, on r29 `91811b648a`). The COO half covers the act, its place in the host queue and the one restart.

## SIGNED: the act and its order

- **Queue (CTO~Z msg 32713, one release in flight on the host at a time):** r29 (OG-ap-3) -> NFRA_MCPORTAL MP-x-4 ->
  this cell -> MX-r-9 -> E2 -> the metadata route. This cell's deploy starts only after MP-x-4's ledger is closed and
  its read-back committed.
- **The act:** one `deploy-to-ec2.sh` run of the release, then one service restart (MainPID changes). The only `.env`
  value that changes is `TRANSCRIPT_MEETING_ALLOWLIST`, from empty to the 4 ids in the ask, read from the json. The
  `.env` key NAMES are unchanged. **Correction to the ask:** after r29 there are **52** names (r29 adds
  `MAIL_SENDER_DOMAIN_TABLE`), not 51; the floor check reads the live count.
- **Re-cut condition.** The release is built on r29. If the live ref at Phase B is MP-x-4's (expected), the applier
  re-cuts by replaying the SAME one-file hunk onto that ref. This half covers the re-cut only when
  `git patch-id` of `base..release` equals that of `4514246d65..78afad4283`, and the json blob is still `d57e815a7c`.
  Any other difference needs a fresh ask. `DEPLOY_BASE_REF` is the live ref read at the act.
- **Both branches, from the route's rule.** An admitted id that Graph answers is served, 200. An admitted id that
  Graph refuses returns 502 `graph_error` (403) and serves nothing; Research Team Meeting is expected here. Any other id
  still gets 403 `meeting_not_allowed`.
- **Writers, N printed.** 1 writer of the allowlist (`deploy-to-ec2.sh` -> `.env`), 1 reader
  (`transcript_route.meeting_allowlist()`).
- **Rollback, one act.** Redeploy the live base read at Phase B, with `DEPLOY_BASE_REF` = this release's sha. The
  allowlist returns to empty, and every meeting is refused again. Triggers:
  - `/health` off 200;
  - tools off their count;
  - `.env` names off the live count;
  - any `.env` value hash moved other than `TRANSCRIPT_MEETING_ALLOWLIST`;
  - md5 of the shipped files not equal to the release list.
- **Not a trigger.** Research Team Meeting answering a Graph 403. That is the ruling's own prediction, and its fix sits
  with the meeting's organizer.

## Not covered

Any code, route, bearer, IAM or other env change; E2; the metadata route; MX-r-9.

-- 2.0.0_SA_COO~O
