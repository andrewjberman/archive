# IRPT_BCKEND rounds 127 (AMENDMENT 2), 129, 130, 132, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~14:5xZ. To: 3.0.0_SA_CVO. Four orders, all terminal.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for each of 127,
129, 130, 132 (orders=1, judgment=0 each; read at 14:5xZ). No judgment criterion. Every criterion below was re-run by the
issuer at box HEAD 231219c1f4 after the merges; every proof reads VALID. NOTHING IS APPLIED OR SERVED by any of the four.

| round | order | what it did | drained | criteria on the issuer run |
|---|---|---|---|---|
| 127 | IB-pr-429, AMENDMENTS 2 and 3 | the date-basis claim re-counted under PRD ADDENDUM v0.35, with v0.36's names; read only | @f795f94f2f | 6 of 6 PASS (three of the first count, three of the re-count) |
| 129 | IB-pr-431 (0.7.0_AE_CloudOps~IB2) | why the YCharts host's session capture failed to sign in; the last READY; read only by SSM | @ce3ccbf3a7 | 3 of 3 PASS |
| 130 | IB-pr-432 | the sections response schema admits the Opal-made report form beside the vendor form | @8aa28be2a8 | 3 of 3 PASS |
| 132 | IB-pr-434 | BUILD ONLY: the capture persists its sign-in receipt, names the after-submit case, keeps stderr per run | @231219c1f4 | 3 of 3 PASS |

## What each found

- **127, the re-count (FWD-3, Cottonwood).** 76,796 account-days: UNGRADEABLE 42,967; ACCT_OWN_DATE 20,138; NOTHING_TO_GRADE
  13,636; ACCT_PRIOR_DATE 55. 25,109 days moved from own-date to UNGRADEABLE and 370 from prior. Served 32,341 of 75,796 eligible;
  57.3 percent blank; 382 of 999 accounts never served. OUTSIDE_ANCHOR is on 34,437 account-days. The CTO ruled the rule stands
  (msg 5082) and, on the next read, that the custodian's own mark is not the anchor (msg 5157). Why an amendment and not a new
  order: the L6 gate, LIMB 6, refused a new order on the ratified-text half then reading REFUSED at v0.34; the CTO had ruled in
  advance (msg 4998) that such a refusal stands and the count runs as an amendment. v0.35 was signed by this reviewer afterwards.
- **129, the host read (FWD-4).** The sign-in was not rejected: the form was submitted at step 0, steps 1 to 7 read
  CH-AUTHENTICATED, the probe never passed, MAX_STEPS ran out. Claim `inferred`: `login_submission` and `probe_pair` persist
  nowhere. Measured: no session bundle written since 2026-10-05T10:04Z; 11 capture refusals in 14 days, 10 with a sign-in; one
  refresh per job. The vendor path is stopped for every seat by the CTO (msg 4916) until a resident release (st32) carries
  round 132's build, and the first sign-in after it is one request on the CTO's word.
- **130, the contract (FWD-4 / PRD ADDENDUM v0.28 item 29).** `data` is an `anyOf` of two closed forms; the Opal form's members
  are `$ref`s into the v2 report schema, which is neither copied nor inlined. The contract test's registry gained that one schema
  by a bounded edit with a control (another non-v1 id still does not resolve). One existing test,
  `ops/tests/test_owned_report.py::test_sections_projection_matches_existing_closed_response_schema`, turned red on the new shape
  (ARMED row D2-W290-S2): repaired by the issuer on the branch before the merge @168a3a1400 -- it now selects the vendor form
  and asserts it closed; its assertions on the projection are unchanged; 35 passed.
- **132, the build (FWD-4).** New reason code `SIGNED_OUT_APP_CHROME_AFTER_SUBMIT`, with its four-postulate record and token
  census in the record; fires at the first probe after ONE submission, no retry. The receipt is persisted by a named whitelist
  (43 closed leaves in the sample; 0 of 4 planted secrets). stderr kept for 16 runs at 64 KiB. The new `ycharts_session.js` is
  sha256 a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841; the host pins the library by hash, so nothing running
  moves until a release whose bindings carry it. Session tests 127 passed; the offline suite exits 0 under the netguard preload.

## Rows filed by these rounds

- IRPT_BCKEND-D2-W288-S2 (one non-cash row with units zero and value positive: a sixth reason; the CTO ruled it a refusal of the
  stamp until a kind is added by addendum).
- IRPT_BCKEND-D2-S85 (the receipt is not persisted and the diagnosis is gated on no submission), -S86 (an empty SSM send returned
  Success), -S87 (the two false positives of the issuer's check), -S88 (kms:Decrypt denied on the lease rows), all by ~IB2.
- IRPT_BCKEND-D2-W290-S1 (the test registry loads only v1; ruled by AMENDMENT 1), -S2 (the ARMED one above; disarmed by the
  repair, disarm owner this seat).
- IRPT_BCKEND-D2-W292-S1 (`probe_pair` is null in exactly the case the new code names; a pair there would cost a second vendor
  request, which the order forbids).
- IRPT_BCKEND-D2-S84 (this seat): IRPT_BCKEND is named expiry owner of a transitional directory row by dell1's ADVI_FIRMBKTS; parked.

## Issuer defects this stretch (for the round-N analysis)

1. IB-pr-431's AC3 held two false-positive patterns (a `sha256sum` of the runner files; `>/I` inside a sed text). AMENDMENT 1.
2. IB-pr-431's face named a row-id form the proof gate cannot resolve; the applier renumbered on the issuer's word.
3. IB-pr-430's AMENDMENT 1 named a synthetic firm id the naming gate resolves to a real firm (reported in the earlier packet).
The applier and the workers left each failing criterion failing and did not edit a check.

## Open in the workstream, not part of this packet

IB-pr-435 (round 133: the securities the anchor does not carry; complete on its branch @497c7628fd, drain in progress) and
IB-pr-436 (round 134: nine funds' independent NAV against the custodian's mark; worker running). IB-pr-426: both halves signed,
no apply order until the CTO's word after st32. IB-pr-413 L4 and IB-pr-404 L6 wait on Monday 2026-10-12 14:15Z.
