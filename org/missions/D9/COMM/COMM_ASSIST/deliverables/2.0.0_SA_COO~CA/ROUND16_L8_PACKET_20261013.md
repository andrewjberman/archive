# COMM_ASSIST round 16 -- L8 packet, PART 1 (issuer 2.0.0_SA_COO~CA, laptop, 2026-10-13 ~19:0xZ)

**Reader:** `3.0.0_SA_CVO~L`. Round 16 = the muse thread, cut on `ledger/ROUND_ANALYSIS.round15.md` @15fdb72f21 over PRD v0.6,
issued @3477d67af5 (`fanout: 1 of 2 chains, cap 8`), decomposition `decompositions/COMM_ASSIST_DECOMP.round16.md`.
`round-close-check --round 16` at this write: REFUSED. The two reasons: CAh3-AC2 is ungraded (yours), and CA-h-2 is not yet cut.
This is part 1; part 2 follows when CA-h-2 is terminal.

## What you are asked to grade now: CAh3-AC2 (judgment, no verdict recorded by the worker)

Document: `deliverables/0.9.0_WK_COMM_ASSIST~8/MUSE_ANSWER_PATH_DESIGN.md` (133 lines, six sections, merged @35feed35c8).
Criterion text: the design makes a forged answer from the dell2 agents' account refuse, names the weaker case plainly, settles the
stale-version rule from the real code, and names the write entry and its grant. The issuer's reading, for you to confirm or refuse:

- Section 1 chooses a signature (`ssh-keygen -Y verify`) over a path rule and states the weaker case: the trust anchor is as strong as
  who can rewrite `allowed_signers` on dell2; both that and the key's location are "not measured".
- Section 4 reads `unseen()` and `on_sms_reply` (tenant.py:131-147, :497-500) and finds a real gap, row W8-S6: the edit branch
  (:527-530) has no version check, so a stale edit answer applies to the newer draft. The fix is in tenant.py, outside this cell.
- Section 5 names entry `sms.reply`, the payload with `version`, and the write statement `sqs:SendMessage` on the LDO mailbox. It
  says the Dell admin-group membership covers it on the declared state, that the group's policy is not in the repo, and that the
  applied membership is CA-h-2's precondition.
- Section 6 gives the two inputs, the control that the refused arm refuses for SIGNATURE alone, and a stated limit.

## CA-h-1 (mechanical, LOCAL): all three PASS, instance VALID, merged @bfaa09da63

`CAh1-AC1 H1-FAILURE-SHAPE ok=True`; `CAh1-AC2 H1-LIVE ok=True unreadable=0 of 4`; `CAh1-AC3 H1-CENSUS files=6 hits=0 ok=True`. The
issuer re-ran all three from the worker worktree. The issuer's one real run of the CLI, 2026-10-13T18:59:10Z, committed as
`deliverables/2.0.0_SA_COO~CA/r16/real_run/` (INDEX.json and README.txt only; the data files hold Andrew's draft text and open calls and
are not committed): `MUSE-REFRESH ok=2 absent=2 unreadable=0`. drafts ok (4 pending), open_calls ok (14 open), eod_today absent (no
`eod:2026-10-13` row yet), sprint_today absent (nothing under today's prefix). FWD-10's clause holds: absent is not shown as empty.

## Rows this round (worker 0.9.0_WK_COMM_ASSIST~8): S1 to S9, all OBSERVATION and INERT, armed 0

S6 (stale edit applies to the newer draft), S7 (muse's public key is not in `org/devices/` or `.tools/`), S8 (drafts.json carries no object
id), S9 (the reader folder has no `answers/` location) are the enrichment items for CA-h-2 and the round-17 analysis. S1 to S5 are CA-h-1's.

## Not exercised

FWD-6 (muse reads the folder over SSH) and FWD-11's off-tailnet refusal need CA-h-2 on dell2 (lane `0.7.0_AE_CloudOps~CA2`, after the
NFRA_CTLPLN round-12 cell-1 read-back). Nothing in this packet claims either.

## PART 2 (appended ~21:4xZ, before CA-h-2 is terminal): the CVO's grade and the state of the slug

- **CAh3-AC2: FAIL**, graded by `3.0.0_SA_CVO~L` at L9 (row `COMM_ASSIST-C-S1`, commit 6d9d2b697d, `surprise-channel/adjudications/ADJUDICATION_v1.md`).
  Clauses 3 and 4 MET; clauses 1 and 2 NOT MET: the dell2 agents' own AWS identity can send an `sms.reply` straight to the queue, so the
  forwarder-side signature check is bypassed and `on_sms_reply` checks no origin (tenant.py:494-557 @38ac43222d). The design omitted that
  weaker case. The CVO's named repair: verify at the receiver against a key pinned in the assistant's deployed config, name the CloudTrail
  residual, add a direct-send arm to section 6's forged input. Whether the residual falls short of FWD-7's "nothing else" is an ENDPOINT
  question for the CTO. The worker did not self-grade; the issuer holds no verdict on this row.
- **CA-h-2:** cut @3ab6cc6281 as workstream `DELL2HOST` (the L6 gate admits a second order into an issued round only that way), crossbox
  ORDER `XB-20261013T210323Z-78b0` committed @96354c3a29 and delivered to `0.7.0_AE_CloudOps~CA2` on dell2 at 21:20Z; its ack is pending.
- **Round-17 candidates for the CTO's enrichment list** (this seat's reading; the CTO writes the list): (1) the receiver-side check and
  direct-send arm (C-S1); (2) the edit-branch stale-version gap in tenant.py (W8-S6); (3) the `answers/` location and the object-id lookup
  the forwarder needs (W8-S8, W8-S9); (4) muse's public key is in no repo file, and round 12 does not read it back (W8-S7, S3);
  (5) FWD-12, the efficacy cell, after FWD-6 is exercised.
- **The slug waits on CA-h-2 terminal** and on the issuer's two reads (muse's key against AC3's fingerprints; the off-tailnet refusal).

## PART 3 (~21:5xZ): CA-h-2 terminal, the issuer's reads, and the round's state for the slug

**CA-h-2 (workstream DELL2HOST, `0.7.0_AE_CloudOps~CA2` on dell2): complete @161b3cf8b7.** AC1 `H2-IDENTITY ok=True user=cloudops-dell2-agent-user
in_group=True`; AC2 `H2-SCHEDULED ok=True task=found last_result=0 ok=4 absent=0 unreadable=0`; AC3 `H2-SSH ok=True listening=True keys=3`. The
instance validates VALID in this tree. Report: `deliverables/0.7.0_AE_CloudOps~CA2/REPORT_TO-CA-h-2.md`. No row filed by the seat. The folder is
`C:\Users\Test\muse-reader`, task `MuseReaderRefresh` every 15 minutes (S4U), rollback in the report. No answers folder, forwarder or SQS send.

**The issuer's reads (2026-10-13 ~21:5xZ, all read-only, from the laptop):**

- **Folder over SSH (FWD-6's path, from the laptop; muse itself was not used).** `ssh Test@100.104.84.87` by the laptop's key (fingerprint
  `SHA256:Ysgq86UGf/...`, one of AC3's) read the folder: six files, `INDEX.json` run_at `2026-10-13T21:41:24Z`, all four sources `ok`
  (the End of Day row and the sprint page now exist). The 21:41 fire was the task's, per the seat's AC2 line.
- **muse's key is on dell2 (row S3).** AC3's second fingerprint `SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ` is muse's, named in
  0.0.0_AB_MSTR msg 108706 (Andrew passing muse's key) and in the laptop's enable receipt (`org/devices/state/laptop/ssh_enable_20261013T004127270Z.json`,
  "keys added ssh-ed25519 muse"). It appears on two lines of the key file (one distinct key). A login BY muse was not run: that is Andrew's.
- **FWD-11's off-tailnet refusal.** dell2's port-22 rules: `OpenSSH SSH Server (sshd)` Enabled=False; `OpenSSH Server (Tailscale only)` Enabled=True,
  remote `100.64.0.0/255.192.0.0`. Control and test from the laptop, which sits on dell2's own subnet (source 172.16.200.67, dell2 172.16.200.236):
  the tailnet address answers; `Test-NetConnection 172.16.200.236 -Port 22` -> `TcpTestSucceeded=False`, `ssh` -> "Connection timed out". A drop,
  not a reset, which is what a Windows firewall does to a source outside the rule.
- **Limit, stated plainly:** the ssh host key could not be saved here (`HOME` is `/home/AndrewBerman`, which does not exist), so each laptop-to-dell2
  call accepted the key without recording it; the read is not a host-identity proof. FWD-7 and the receiver-side check are untouched (round 17).

**Round 16 state:** 3 of 3 orders terminal (CA-h-1, CA-h-3, CA-h-2); judgment 1 of 1 graded (CAh3-AC2 FAIL); `round-close-check` MAY-CLOSE.
Rows: this round W8-S1..S9 and S3, all OBSERVATION; carried and unchanged: Z-S1 and Z-S3 (BLOCKING, UNDER_INVESTIGATION, CA-d-2 deploy, site Z
origin), Z-S6, Z-S9, Z-S10 (no disposition). Armed: 0. Not exercised: muse itself reading the folder, and any answer from muse.
