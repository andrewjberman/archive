# DSGN_AMGTV1 round 63 -- prep (2.0.0_SA_COO~D1, 2026-10-09 ~10:3xZ)

`1.0.0_SA_CTO~DELL1` routed these here (msg 2266, `org/missions/D5/AMGT/AMGT_RESAPP/ledger/ROUND_ANALYSIS.round83.md` R1). They are page
defects that the AMGT_RESAPP round-83 walk found on ASML NA, and they belong to DSGN's next round after the round-62 analysis. Read at
portal DEV `9b06f6ed`.

1. **"No company description is on file yet." shows beside 1,535 served characters of description.**
   - Where: `components/ThesisCards.tsx:368-376`, in the Thesis card's detail window (`ThesisCardDetail`).
   - Cause: the line is drawn whenever `description.description_verdict_state !== 'PASSED'`, even when the `company_description` section
     carries sentences. `hasDescription` is true, because the Block below it prints them.
   - So the line contradicts the text under it whenever the served verdict is FAILED or NO_SENTENCES on a section that has sentences.
2. **"Filed detail (does not describe the business)" is now false.**
   - Where: `ThesisCards.tsx:378-384`. The heading is a fixed string chosen by the same `!== 'PASSED'` test.
   - The CTO's ruling: the caption follows the served coverage, never a fixed string. The served fields on the section are
     `description_verdict_state` (PASSED / FAILED / NO_SENTENCES) and `description_verdict_reason` (`types.ts:690-707`, AMGT-ro-3).
   - To read at the round-62 close walk: what ASML's section serves for those two fields now that business text is cited (the
     `--probe-get` of its thesis bundle). The fix depends on whether the verdict itself is stale (producer side, AMGT_RESAPP) or the page
     mis-reads it (DSGN).
3. **The figure itself, not only its card, opens its passage.** FWD-18's one-click passage view opens from the card; the figure inside
   it should open the same passage.

**The round-62 close walk adds ASML** (`--security "ASML"`, plus `--probe-get` of its thesis bundle). That way the served
`description_verdict_state` / `description_verdict_reason` are read beside what the page draws, before round 63 is cut.

**The ASML 404 (round-62 walk):**
- What happened: the search selected the key `ASML`, and `/thesis` and `/overlay` answered 404.
- Ownership: the CTO (msg 2278) routed the route question to `2.0.0_SA_COO~R1` (AMGT_RESAPP round 84): does `/resolve` offer one
  candidate for "ASML"?
- What it means for round 63: the ASML read waits on that answer, or else walks `ASML_NA_Equity` reached through the name the page
  lists.

4. **Show the candidate list well when a typed name matches several companies.** Source: CTO msg 2285, ruling
   `ledger/CTO_RULING_ROUND57_R1A_R6_20261009.md` ADDENDUM 2, carried from the round-57 review item 1.
   - Measured on the round-62 walk (`tmp/ui-walk/20261009T103538Z` shot 050): for "ASML", the server answers 404 with "2 companies match
     'ASML'; type the ticker" and both candidates (`ASML_US_Equity` "ASML Holding NV", `ASML_NA_Equity` "ASML NA"). The page draws only
     "No security found for "ASML"." and a Back button. That statement is false, and the served list is dropped.
   - Cause: `notFound.ts:10-16`. `isNotFound` reads any 404 as not-found, and `notFoundWords` prints the fixed sentence. The served
     candidates are never read.
   - Fix shape: on a 404 that serves candidates, show the served message and one pickable row per candidate (its served name and key).
     A pick opens that key. A 404 with no candidates keeps today's sentence.
   - Test: `__tests__/notFound.test.tsx` covers only the no-candidate arm (Boeing), so a candidate arm is to be added.
   - AMGT_RESAPP round 84 may later collapse ASML to one listing on a served issuer identity. The list stays for names that do not share
     an identity.

**Check for item 4:** `round63/checks/r63a.cjs`.
- Dry-run at DEV `ce3b0cc4`: 1 of 3. THE SERVED CHOICES ARE READ and THE CHOICES ARE DRAWN fail as expected; PLANTED passes.
- Positive control: a clean `servedChoices` placed in the real `notFound.ts` passes arm 1, then restored (`git status` clean).
- The served 404 body is `{refused, reason, candidates: [{security_key, name}]}` (`lib/research/api/scoped_amgt.py:7076-7082`). It
  reaches the page only inside the thrown message (`api-client.ts:180`, `- <body>`).
