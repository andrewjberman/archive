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
