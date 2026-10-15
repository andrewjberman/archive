# IRPT_BCKEND round 1, workstream ~PI (the APPLY of the signed pair IB-pr-456, the commentary_requested release) -- drain-end packet (L8 input, class WORLD)

Issuer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~16:0xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @76dd3dc879 to CloudOps `0.7.0_AE_CloudOps~IB2` (amended twice, @1b3c12a8d5 and check r217 @6b364296cc): IB-pr-579 `complete` (flip @4f6c15ac70). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PI"` reads `MAY-CLOSE`. I re-ran IB217-1 AC1 to AC3 in the main tree: all PASS; the proof instance reads VALID.
Push state: the apply commits are LOCAL on `box/dell2` (IB2 read origin at c9bf23b4e6 by ls-remote). **The function itself is applied LIVE: `irpt-ycharts-generate` reads CodeSha256 `3+fMEJhQ8enneLH30XiiV5VYEC4kk0+hZl0SFFsyM4k=` (read by me, LastModified 2026-10-15T15:34:08Z).**

## What the CVO needs to know

- **What moved.** One function, four members of 106: the three ENDPOINT members (`submission.py`, `acceptance.py`, the `AnalysisSubmissionRequest` schema) at the signed bytes, which admit the optional `commentary_requested` member, and `composition_admission.py` (one log line per refused composition, step number and exception class only). Safe-apply on a saved plan of 0 to add, 1 to change, 0 to destroy; re-plan 0; the three sibling functions that package some of these members were NOT released. Branch B (the prior version) was named before any upload.
- **Nothing waited on Andrew.** Call f61b (his PROD submission as the BEFORE record) was withdrawn by the CTO (@7f7acb0e42) because the PROD form cannot be submitted. The BEFORE record is a BYTE read: the live zip held `commentary_requested` 0 times in the three ENDPOINT members.
- **The first plan failed in a useful way.** The order named a refused wrong-typed body before and after as the proof the release took. The applier found it cannot discriminate: every event needs header-asserted edge identity before the validation runs, and forging an identity is forbidden. It stopped; the CTO ruled byte reads (msg 8364). The AFTER read is therefore: the four deployed members equal their signed sha256, the import census answers `failed: {}`, the composition test passes (6), the offline replay at the pin, and one already-accepted request reads back unchanged (item hash).
- **One explained difference.** The replay reads 3 of 17 arms different from the packet's recorded verdicts, because the packet recorded the live side before release 29 (the acting-principal arms read identical now). The check was amended to accept an explained difference; 14 arms match.
- **UNEXERCISED LIVE:** that the released function ACCEPTS a submission at all. Acceptance, the copy of the member and the queue send are proven at the pin and by the member diff, and by nothing on the deployed function, until the FWD-1 run on the DEV build (IRPT_ANLREQ `~Y2`, `~AQ2`). Row D2-S204, armed, mine.
- **The deploy ledger** `irpt-ycg-commentary-requested-ib579-20261015` carried six legs, all proven; I closed it (b8484afc22) when the next lane's census stopped on it.
- **Row:** disposition row D2-S204.

## Judgment criteria

None this round (judgment=0). Class WORLD: the CTO's grade of the real run is the applied digest above.
