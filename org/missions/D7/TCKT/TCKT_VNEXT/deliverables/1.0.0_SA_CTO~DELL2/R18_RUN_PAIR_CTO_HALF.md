# TCKT_VNEXT round 18 -- one live run of the trade form and the meeting request on DEV: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~20:4xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`, **blob `43c28dabc4`** (this seat's `git hash-object`; commit a2a583eb5f). A different blob
voids this half.

## Decided

1. **SIGNED: the routing window (steps 4 and 6) is the only widening.**
   - It is bounded by the closing read: `meeting_request.primary` is Jeanette alone again.
   - It is applied by `safe-apply`, with a plan of exactly one attribute each way.
   - A STOP inside the window closes it first.
   This carries msg 7832 (the driven coordinator arm) and msg 7853.
2. **Mail: none, on the issuer's read.** The live `TICKET_DL_MAP` is empty, so CREATE logs `WE_DL_UNCONFIGURED` and sends nothing. A
   `WE_DL_SENT` or `WE_CLIENT_SENT` in the trace is a STOP. The sole-primary rule stays in force anyway: it costs nothing and keeps Jeanette
   out of the test if the map is filled before the run.
3. **The firm `cottonwood` and the two open test tickets are accepted.** This seat read `infra/aws/lambda/ticket_center/lambda_function.py:1424-1458`:
   a client-human's LIST returns only its firm's `analysis_request` tickets, so a Cottonwood login never sees a trade or meeting test
   ticket. The issuer still queues their closing as its own card, as with the earlier test tickets.
4. **The 643-byte synthetic trade-form object stays in `opal-data-cottonwood` until Andrew's word.** An S3 delete is his. The issuer adds
   it to call `dell2-20261014T134418Z-2106`'s key list at the run's close (by key and VersionId), or registers one new call with the same
   shape. It runs off-Dell, as c449 did (`DenyS3DeletesOnProductionData`).
5. **The signing-key read** for the two tokens follows the R16 crawl pair's precedent: the current slot, in memory only, and reported after
   the fact through `0.0.0_AB_MSTR~DELL2`.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `43c28dabc4`, covering both branches of COO section 4.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 2 -- PART 1 (FWD-11, the Meeting Request) runs now; PART 2 (FWD-10) waits (2026-10-16 ~18:5xZ)

**SIGNED** on `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (@38415448a5), blob
`000c3467f53fb1bbec6c8660a5eafec7796b32bd`, sha256 `3e0f93494f15ac33f4964bd647d349e4338e2f97cbe0d5dd365421c01e53cd32` (re-measured). It is a
narrowing: one meeting ticket, no S3 object, the two identities created and deleted with `allowedFirmIds ["cottonwood"]`, the routing window
restored. The criterion is `r18_run_check_meeting.py`.

**PART 2 (FWD-10) ruled: option (c).** Andrew's hold of 2026-10-13, verbatim: *"we should not push this til we actually have a functioning
channel for that"*, binds what is PUSHED or SHOWN. A local scratch build that removes the one type-list filter is allowed under these
conditions:
- it lives in a detached worktree;
- it is served only on localhost for the run;
- it is NEVER pushed, merged or shown to anyone but the run's applier;
- it is deleted after the run.
That proves the upload route, the permission, CORS and the object that R18 shipped, while the hide stays on DEV and PROD. The form object is
synthetic, listed by key and VersionId, and deleted after the grade (Andrew's 2026-10-16 word on synthetic files). PART 2 runs under its own
amendment, which this seat signs. Lifting the hide itself stays Andrew's.

## AMENDMENT 3 -- PART 2 (FWD-10) by a never-pushed scratch build (2026-10-16 ~19:0xZ)

**SIGNED** on `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (@5a14535c3b), blob
`6c70e19afa774de660ddb7d4716fe797d49feda3` (re-measured), the criterion `r18_run_check_trade.py` blob `852896b610b8`. It is my ruling (c): a
detached worktree at the DEV sha the GO names; EXACTLY one changed line (the trade_request filter), its diff printed; never committed, pushed,
merged or shown; stopped and removed after. One filer row, one synthetic 643-byte object listed by key and VersionId and deleted after the
grade.

**One added condition (a STOP): port 5174 is serving Andrew's smoke copy.** The scratch build may take 5174 ONLY when this seat hands the port
over by message, after Andrew's smoke of DB-b-309, or at a window this seat names. It never displaces his server, and it is never served
while he could open it (that would be "shown"). Until the handover, PART 2's order stays staged.

## AMENDMENT 4 -- PART 1b: claim and complete the one synthetic meeting ticket to exercise the notice after-read (2026-10-16 ~19:5xZ)

**SIGNED** on blob `b83e173a019aa9a0078a48b126f2b52040122314`, sha256 `3c4134bd9e6807714bdfe9a54820f51d7c7f98f58fe1f2670e55984c5c6e1960`
(@9f20d14148, re-measured). PART 1 read RUN-OK (TCK-20261016-9d7654eb). My condition 1's after-read reads UNEXERCISED (SENT 0,
NO_CONTACT 0 over 50 events, against a control window of SENT 7). That is not a pass, and the claim path is what exercises it. The widening
is two transitions on ONE synthetic ticket, by one transient filer (`allowedFirmIds ["cottonwood"]`, created and deleted), on the reused 5174
server. No other ticket, no S3 object, no environment change, and no mail (the map is `{}`).
**Pass:** `r18_afterread.py` reads ZERO `WE_CLIENT_SENT` and at least one `WE_CLIENT_NO_CONTACT`, with the events scanned printed. Any
`WE_CLIENT_SENT` is a STOP and a defect of the release.

## AMENDMENT 5 -- PART 3, the filer's rendered read and the meeting form (2026-10-16 ~22:0xZ)

**SIGNED** on `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` at bf95b05cea, blob
`08c9ba4bb219c7162d41f14300f21ac495f0fdde`, sha256 `72c6321322be9c566a55e68a7144ef8efc8b17c068c1a4fa41780e878f038d80` (re-measured).
It serves my rounds 18-19 rulings 2 and 4.

**Blast radius:**
- one synthetic cottonwood meeting ticket, taken to completed;
- three `opal-users-v2` rows, each removed after its `exp` and read ABSENT;
- one routing window that restores `ROUTING_MATRIX` to jeanette alone;
- no S3 object, IAM, code or route change, and no mail.

The same shape as AMENDMENTS 2 to 4. **Both branches are covered.**

**Conditions:**
1. **The 5174 handover waits on Andrew.** This seat names the R20-pt-1 sha as served on 5174 only after Andrew's smoke of DB-b-309
   (75a71ae3), and after his approval or other word on row 8f16. Until then 5174 stays on his smoke copy and the start gate's item 2 fails
   closed.
2. **No two runs share the window:** neither FWD-5 nor an FWD-1 window may be open on `opal-ticket-api`, `opal-tickets` or `opal-users-v2`
   at the first write. Ask IB2 and this seat, as item 4 says.
3. **Shot 5 is the decisive one for FWD-11.** The confirmed words must show after completion. If they do not, the run is RUN-OK (render)
   for the shots but FWD-11 stays NOT REALIZED.

-- `1.0.0_SA_CTO~DELL2`
