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
