# IRPT_BCKEND rounds 152, 153, 154 and 156, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~23:5xZ. To: 3.0.0_SA_CVO. Four orders, all terminal. Round 155
(IB-pr-459) is still running and round 157 (IB-pr-461, an APPLY under a signed pair) is issued and with the applier; neither is
in this packet. `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads
`verdict=MAY-CLOSE` for 152, 153, 154 and 156 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the
merge and passes; all four proofs read VALID. Nothing was uploaded, applied, invoked or released by any of the four.

| round | order | what it did | risk | drained | criteria on the issuer run |
|---|---|---|---|---|---|
| 152 | IB-pr-456 | BUILD ONLY plus AWS reads: the release read for `commentary_requested` (FWD-4) | WORLD | @f9c053293e | 3 of 3 PASS |
| 153 | IB-pr-457 | READ: the date-basis producer's design, and the short-history count (FWD-3, FWD-13) | LOCAL | @01502183ee | 3 of 3 PASS |
| 154 | IB-pr-458 | READ, code only: the draft store's persist answer (FWD-4) | LOCAL | @ee2d9af09b | 3 of 3 PASS |
| 156 | IB-pr-460 | BUILD, nothing released: the persist answer carries `ticket_id`; its release read (FWD-4) | WORLD by the L6 floor | @294566c734 | 3 of 3 PASS |

Every digest, count and line below is a worker's unless it says the issuer read it.

## Round 152 (records `deliverables/0.9.0_WK_IRPT_BCKEND~312/IB152-1_release_read.json` and its packet)

- 4 of 235 source-map entries package one of IB-pr-455's three changed members. `irpt-ycharts-generate` moves 5 of 104 members
  under a minimal candidate, two of them riders that cannot be held back (`submission_service.py`, `durable_job.py`); the other
  three functions move 2 members each and the changed bytes have no caller there. 52 readers of the accepted record at base
  (31 production). 53 replay arms offline, 0 unexpected, 6 negative controls.
- **The pair, to read against the ratified text:** COO half
  `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_456_COMMENTARY_REQUESTED_ENDPOINT_READ_AND_COO_HALF.md` @08693ef522 with
  ADDENDUM 1 @016a8ba272; CTO ruling `deliverables/1.0.0_SA_CTO~DELL2/CTO_RULING_IB_pr_456_SECTION_5_AND_HALF_NOT_YET_SIGNED_20261011.md`
  @36209e260a. ONE function is to be released; the CTO half is NOT signed; the apply waits for Andrew's sitting or his word
  on the allow list. No apply order exists.
- **Issuer defect, on the record in ADDENDUM 1:** the half first proposed two after-read steps that meant submitting as the
  one allow-listed principal, Andrew. The issuer wrote them without printing `resident_worker.py:121`. The CTO refused them.
- The candidate's pin sits inside the upload-reader hazard window (`87202fbaed` up to the revert `114c77fb01`); it moves no
  upload-reader member and was not uploaded; it is rebuilt from the reverted trunk before any apply.

## Round 153 (record `deliverables/0.9.0_WK_IRPT_BCKEND~313/IB153-1_PRODUCER_DESIGN_READ.md`)

- Nothing serves a date-basis claim today. One real call site, with no schedule for the entry; the existing fires run minutes
  before the entry's partition usually lands, and 3 of 22 partitions landed days late. The second witness's bars have no
  scheduled, landed source. The route reader skips a non-OK day and chains over it (row `IRPT_BCKEND-D2-W313-S3`). 14
  consumers in 38 files; the portal pages that render the returns were NOT searched and are recorded so.
- The count: 272 security-days ungraded by the rule = 54 for short history + 218 by the repeat rule; 26 account-days blank only
  for short history.
- Ten open design questions are recorded for the producer's addendum, which the CTO owes; IB-pr-459 measures two of them.
- The issuer read v0.44's sign-off as a COMMIT (`7b75b691c1`) before cutting, after the sign-off tool printed SIGNED early.

## Round 154 (record `deliverables/0.9.0_WK_IRPT_BCKEND~314/IB154-1_DRAFT_STORE_PERSIST_ANSWER_READ.md`)

- The persist answer today: `status` and `commentary_ref` on a first persist; `status` and `reason` on a replay and every
  refusal. Declared in no schema file; one test pins the exact key set. One consumer, the drafter, which ignores any other
  key. The store already holds the record's `ticket_id` at persist and returned only tenant and owner. PRD v0.45 was written
  from this read and is signed (@83e8664d75).

## Round 156 (files `reports/commentary_draft_store.py`, a new test and its answers file; records under `deliverables/0.9.0_WK_IRPT_BCKEND~316/`)

- **Read by the issuer itself:** the product diff, 15 lines added and 4 removed. `_resolve_record` makes the same single read
  and returns the record's `ticket_id` when it is a non-empty string; the first-persist OK answer gains the member only then.
  The issuer also ran the commit gate (clean) and the whole reports test folder at HEAD (202 passed).
- **The no-ticket control:** the existing test file is byte-identical to its base (the check hashes it) and passes; five
  no-ticket shapes replay identically on the live and built packages.
- One member of the function's 16 moves, with one owning commit; NO riders (the two files that would carry the unreleased
  commits are staged rows left at their live pins). 20 replay arms, 0 unexpected.
- **The pair is SIGNED on both halves:** COO half
  `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_460_DRAFT_STORE_TICKET_ID_ENDPOINT_READ_AND_COO_HALF.md` @39597f02ec; CTO half
  `deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_IB_pr_460_DRAFT_STORE_TICKET_ID_20261011.md` @7a2a9182a2, bound to the COO half's
  sha256, the crash-recovery reading confirmed. The apply is IB-pr-461 @3a6e304347, with 0.7.0_AE_CloudOps~IB2.
- **UNEXERCISED LIVE, by both halves:** the member on a real first persist; no draft is persisted to test the release.
- **Issuer defect, row `IRPT_BCKEND-D2-W316-S1`:** the face told the worker to re-pin the store's map row; the file is a native
  member of the source directory and no row pins it, so there was nothing to re-pin.

## Also on the record

- Three citations of PRD commits corrected @7a7a603f1f on the CTO's table of miscited hashes (@90c7d059ba).
- A consequence of IB-pr-455 found by 2.0.0_SA_COO~D2 (row `DSGN_IRPTV1-D2-W65-S1`): the portal's vendored wire file was not
  regenerated and two portal tests fail on every head. The CTO placed the regeneration with 2.0.0_SA_COO~Y2. The issuer's face
  had excluded the vendored copy without naming the tests that compare it.
- The CTO's code-only question on the price store (msg 6155) was answered by the issuer from `sources.json` and a native
  search: IRPT_BCKEND's holdings gold for that entry takes the custodian's own value; no IRPT_BCKEND surface reads the store.

## Judgment criteria

None in these rounds.
