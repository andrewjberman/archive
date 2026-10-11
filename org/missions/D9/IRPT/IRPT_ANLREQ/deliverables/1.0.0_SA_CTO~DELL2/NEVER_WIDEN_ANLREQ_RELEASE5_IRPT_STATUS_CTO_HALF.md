# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ release 5: irpt-status from ONE tree (pin ee3fd7c5e5), build Iw3FADFr

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~09:5xZ** | **Against:** the pair file
`deliverables/2.0.0_SA_COO~Y2/release5/NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_IRPT_STATUS.md`, blob `1b310f3c2a` (`git hash-object`,
this seat), and the build `Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0=`. A build that prints another digest is an ABORT, not
a re-sign.

## 1. The act and its blast radius

One function's code, `irpt-status`, revision 6 (`6idtFvAm...`) to the build above. No role, policy, environment variable,
route or schedule. 14 of 49 members move: 3 change a served answer and 11 are censused inert. The radius, both branches and
the rollback (the S3 object version recorded at R0, digest `6idtFvAm...`) are as the COO half states them.

## 2. What this seat read itself

- **Every hunk of `ops/owned_report.py` and `ops/prospect_dates.py`** between the old pin 361c44fa9d and ee3fd7c5e5.
  - `prospect_dates.section_dates` reads an `OPAL_ENGINE` report by its own branch: a row must state `status` VALUE or
    NOT_AVAILABLE and carry `as_of_date`; null is admitted only beside NOT_AVAILABLE; a non-ISO date, a null beside VALUE and
    any `undated_sections` row refuse. The other branch's rule is unchanged, moved into an `else`. This is the ruling of
    ADDENDUM 8.1 to the IRPT_YCDGEN round-8 analysis, as written.
  - `owned_report.sections` adds `retained_ref` to both forms, taken from the receipt `read` already checked. **It also adds
    one new refusal, `READY_REPORT_RECEIPT_REQUIRED`, when that receipt is not a dict.** `read` sets it on every path this
    seat read. R2 is the after-read that shows a READY report still answers.
- The diff's size for the three served-changing members: 88 insertions, 21 deletions.

**Taken as filed:** `owned_requests.py`'s 62 changed lines (ruled in msg 4430, not read line by line here); the census of the
eleven inert members, two of which the COO half itself marks as readings; the reach read's count of 0; the laptop's count of
0 unreadable compositions of 49.

## 3. Conditions

1. The COO half's section 4, R0 to R8, in order, and its three branches. R8 is the control for the eleven inert members and
   is not skipped: an inert member that changes an answer is a failed after-read and takes the rollback.
2. R4 recorded as ABSENT with its census if no `OPAL_ENGINE` request is readable; ABSENT is not EXERCISED and the close says
   which. `REQ-5e4149d2` is the known one (IRPT_YCDGEN row D2-S38): its read here is also that row's disarming read.
3. The building commit is read ON ORIGIN by the applier before the build.
4. The source map's stale applied-artifact fields (row D2-S33) are corrected in the record step of this apply, not left for
   a third release.

-- 1.0.0_SA_CTO~DELL2

---

## ROLLBACK RULED 2026-10-11 ~11:2xZ -- the release broke the page that consumes it; this half missed the consumer

**What is wrong.** Release 5's history answer carries a third top-level member, `unreadable_rows`. The portal's reader,
`src/pages/InvestorReporting/contracts/owned-requests.ts` `readOwnedHistory`, requires EXACTLY `items` and `next_cursor`
(`exact(value, ['items', 'next_cursor'])`, read by this seat on portal `origin/PROD`) and throws "Invalid owned request
history" on anything else. The laptop applier's R3 read `unreadable_rows` true on the live function. So from 10:25:40Z every
Investor Reporting history read on portal PROD and DEV throws. Found by 2.0.0_SA_COO~D2 (msg 4803) while probing fixtures;
inferred from three measured legs, the page itself not observed.

**Ruling (msg 4805):** the pair's rollback branch, at once: `irpt-status` back to `6idtFvAm...`, the S3 object version recorded
at R0, one ledger entry, the source map re-pinned back. After-reads: the digest, and one history read answering with exactly
the two keys.

**What this half got wrong.** It conditioned the apply on reads of the SERVICE's new members and named no read of a
CONSUMER. Every after-read in the pair asked "does the function now say the new thing"; none asked "does the page that reads
it still accept the answer". The census classed the change as "changes a served answer" and stopped there. A served answer
that gains a member is a breaking change wherever a reader checks an exact key set, and this portal's readers do.

**The order the release returns in:** the portal's readers admit the new members first (history: `unreadable_rows`; each row:
`client_id`, `client_claim`; sections: `retained_ref`), on PROD, which is Andrew's word for a client-facing page; then the
service. Each served-answer change in a pair names its consumers and one read through each.

-- 1.0.0_SA_CTO~DELL2
