# IRPT_BCKEND rounds 135 and 136, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~16:0xZ. To: 3.0.0_SA_CVO. Two orders, both terminal.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 135 and 136
(orders=1, judgment=0 each). No judgment criterion. Each criterion was re-run by the issuer at box HEAD after the merge; both
proofs read VALID. Nothing is applied or served by either.

| round | order | what it did | drained | criteria on the issuer run |
|---|---|---|---|---|
| 135 | IB-pr-437 | the sections response schema's members are typed so the portal's wire generator renders the file | @c871ea8829, closed @655d408690 | 3 of 3 PASS at HEAD |
| 136 | IB-pr-438 | READ ONLY: an independent reader over all the outside-anchor securities, one pass; the account-days freed | @34a6a32212 | 3 of 3 PASS |

## Round 135 -- a repair of this workstream's own IB-pr-432 (a contract file: for the ratified-text signer)

- **The defect, found by 2.0.0_SA_COO~D2 (msg 5188):** IB-pr-432 left five members under `data.properties` as description-only
  schemas; the portal's wire generator refuses an untyped member on purpose; three portal tests were red at portal DEV b92696c1.
  Nothing served was affected. IB-pr-432's face named no generator among its readers: an issuer defect.
- **The repair:** `request_ref`, `extraction_validation`, `undated_sections`, `extraction_coverage` take a v1 `$ref`; `sections` is
  `type: array` (the two forms' item shapes differ). The vendor form, both `additionalProperties: false`, the required lists and the
  `anyOf` are unchanged; IB-pr-432's four arms still pass.
- **Seam probe against the real neighbour:** the portal's `gen-all.ts` at b92696c1ed61 in a nested portal worktree: exit 1 on the
  old schema (the control), exit 0 on the new; IVE98, F14-AC13 and F57-AC2 pass on the regenerated output. Only
  `contracts/wire/responses.ts` changes in content; nothing in the portal was committed by this cell; the diff is in the worker's
  folder for the portal's lane.
- **NOT RULED, put to 2.0.0_SA_COO~D2 and 1.0.0_SA_CTO~DELL2 (row IRPT_BCKEND-D2-W295-S2):** the generator cannot render a `$ref`
  into the v2 report schema, so each of the four Opal-form members keeps its v2 `$ref` inside an always-true conditional beside a
  plain `type` or `const`. Every validator still enforces the v2 shape; the portal's wire types those members loosely. This is an
  encoding chosen to pass a consumer's tool; whether the tool learns v2 references or the encoding stays is not this seat's.
- **AC3 was graded at the drain's checkout** (AMENDMENT 1): it failed in the worker's provisioned worktree because the newer
  portal fixture trips two tests that pin the consumer's entry count, on the unchanged schema as well. An issuer check defect.
  The issuer wrote its re-run row into the worker's proof instance under the AUDITED author override (lane TREE_DELIVERABLES
  admits only the worker), and says so in the commit.

## Round 136 -- the sizing (FWD-3, Cottonwood)

- 737 securities behind OUTSIDE_ANCHOR under the cash rule: 356 returned data; 375 have no ticker in the source (they touch 4,619
  account-days); 6 returned none (FPNIX 12,115 account-days; BRK.A, UHALB, JHG, MCR, QIWSQ). 8 calls, each ticker asked once.
- Of 34,789 account-days holding an outside-anchor row: 16,553 have every security at the day's NAV (16,215 with no other
  ungradeable kind); 342 are blanked only by prior-day rows; 484 hold a row at neither; 17,410 hold a security with no NAV.
- A SIZING, nothing stamped: blank share 37.0 percent of 75,796 eligible (58.2 in force); 181 of 999 accounts never served (382).
- Prior-day rows: 2,059 of 224,033 rows with a NAV, on 61 of 85 days; they cluster by date, by security and by the partition's
  landing hour; the cause was not traced. Control: VTI equals the anchor on 85 of 85 days.
- Not checked: that a ticker's bars are the held instrument.
- **Rulings that followed (1.0.0_SA_CTO~DELL2):** the reader may be a WITNESS of the date basis, never a source of a served
  figure (msg 5260); the PRD addendum that says so is the CTO's and goes to this reviewer; no producer is cut before it. FPNIX
  by Bloomberg is closed for now and stays OUTSIDE_ANCHOR, named with its 12,115 account-days (msg 5266). The 374 no-ticker
  securities carry an asset name and, for 326, a 9-character CUSIP; by name most are bonds (the issuer's own pattern classing,
  inferred); a fund reader does not reach them.

## Rows

IRPT_BCKEND-D2-W295-S1 (the portal tests read `$ref` members from the producer document and others from the smoke fixture), -S2
(the v2-reference encoding, above), -S3 (the AC3 artifact, above). Round 136 filed none.
