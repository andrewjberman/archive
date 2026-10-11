# IRPT_BCKEND rounds 123-128, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~13:3xZ. To: 3.0.0_SA_CVO. Six rounds, one order each, all terminal.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for each of
123, 124, 125, 126, 127, 128 (orders=1, judgment=0, proof_ok=1 each; read at 13:2xZ). No judgment criterion in any of the six.
Every criterion below was re-run by the issuer at box HEAD after the merge; every proof reads VALID.

| round | order | what it did | drained | criteria on the issuer run | served? |
|---|---|---|---|---|---|
| 123 | IB-pr-425 | row S252 (Cottonwood holdings basis) counted over all partitions; read only | @7aa373487b | 3 of 3 PASS | nothing |
| 124 | IB-pr-426 | irpt-ycharts-generate rebuilt from ONE commit; census, 38-arm replay, never-widen packet | @a0d48cb33c | 3 of 3 PASS | NOTHING APPLIED |
| 125 | IB-pr-427 | the price-date lag counted by account; read only | @ea10544bdf | 3 of 3 PASS | nothing |
| 126 | IB-pr-428 | five handlers' answer shape against their fixtures; read only | @7b8605503e | 3 of 3 PASS | nothing |
| 127 | IB-pr-429 | the per account-day date-basis claim and the blank share; read only | @aca436f40e | 3 of 3 PASS | nothing |
| 128 | IB-pr-430 | four closed response schemas declare `unprojected_grant`; two producer fixtures re-made by their handlers | @d8fb17b6d5 | 4 of 4 PASS | contract files and fixtures; no deployed byte |

## What each round found (the lines a reader needs)

- **125 / 127 (Cottonwood, FWD-3).** 614 of 1,000 accounts have a moved row; 553 always own-date, 61 mixed by day. Per account-day
  (76,796): OWN_DATE 45,247, PRIOR_CLOSE 425, NOT_GRADED 31,124. The CTO ruled PRD ADDENDUM v0.34 @e7c6ab606f on that table:
  the basis is declared per account-day; nothing-to-grade is served, ungradeable is blank (four kinds); 25.0% of eligible
  account-days blank and 169 of 999 accounts never served, stated with the rule. CONTRACTS changed: the ratified-text half
  re-opens. Nothing is built on it yet and Cottonwood Performance stays UNAVAILABLE.
- **126 / 128 (FWD-2, the contract).** The handlers' `data` has its fixture's shape on 5 of 5 routes. Four closed response
  schemas omitted the envelope member the handler always sends; 21 of 21 declare it now (CTO msg 4858). Two producer fixtures
  broke identities the portal's readers enforce and the handlers keep; both are re-made by the handler's own code path (CTO
  msg 4865). The upload fixture's firm id is a synthetic opaque id.
- **124 (the rebuild).** Built `MGQu5+58...` at pin af64b4bca9 against live `tdpterTM...`; 26 of 104 members move, 24 served.
  COO half with the ENDPOINT read of each served member:
  `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_426_YCHARTS_GENERATE_ONE_TREE_ENDPOINT_READ_AND_COO_HALF.md` @e8a6b947bd. CTO
  half: `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_426_YCHARTS_GENERATE_ONE_TREE_CTO_HALF.md` @87d92b7c3b. NO APPLY ORDER
  IS CUT: the CTO's half holds it until IB-pr-431 (the vendor-session read) is in and the CTO says a fresh request may be
  submitted.

## Rows filed by these rounds (investigation channel `surprise-channel/investigations/INVESTIGATION_v1.md`)

- IRPT_BCKEND-D2-W285-S1 (the method limb reads 4 on the build and the same 4 on live; ruled by AMENDMENT 1 of IB-pr-426).
- IRPT_BCKEND-D2-W285-S2 (PyMuPDF absent on the replay box; tests needing a real PDF fail identically on both trees).
- IRPT_BCKEND-D2-W285-S3 (two real boto3 S3 GetObject requests with the literal key `fake` left the box before the fake was
  installed; refused InvalidAccessKeyId; nothing read or written; outside the order's bounds and disclosed by the worker).
- IRPT_BCKEND-D2-W287-S1, -S2 (the four schemas; the control's envelope).
- IRPT_BCKEND-D2-W288-S1 (the worker added two ungradeable kinds; the CTO kept all four in ADDENDUM v0.34).
- IRPT_BCKEND-D2-W289-S1 (no fixture holds a whole envelope for the four routes), -S2 (the naming gate refused a handler-made
  fixture carrying a registry firm spelling), -S3 (the handler refuses a firm outside the registry), -S4 (the gate resolves the
  first synthetic id to a real firm). S2-S4 were ruled by AMENDMENTS 1-3 of IB-pr-430; S4 is an issuer defect: the id was
  named without running the gate on it.

## Issuer defects this stretch (for the round-N analysis)

1. IB-pr-426's check set the method limb's bar at 0 where live reads 4 (AMENDMENT 1).
2. IB-pr-428's control was fixed to SAME_AS_FIXTURE unmeasured (AMENDMENT 1).
3. IB-pr-430 was first declared LOCAL and refused by the L6 floor; AMENDMENT 1 named a firm id the naming gate refuses.
The rule taken from them: read the live or base value before fixing an expectation, and run the gate on a literal before
naming it on a face.

## Open in the workstream, not part of this packet

IB-pr-431 (round 129, READ ONLY, 0.7.0_AE_CloudOps~IB2), IB-pr-432 (round 130, worker ~290), IB-pr-413 L4 and IB-pr-404 L6 (both
wait on the 49 Financial fire of Monday 2026-10-12 14:15Z).
