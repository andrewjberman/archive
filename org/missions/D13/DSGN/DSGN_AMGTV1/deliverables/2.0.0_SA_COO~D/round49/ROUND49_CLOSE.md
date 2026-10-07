# DSGN_AMGTV1 round 49 -- CLOSE (2.0.0_SA_COO~D, 2026-10-07 ~12:5xZ)

**Candidate: portal `b3440392`** = DEV `8ddfe409` + 5 commits (rounds 47, 48 and 49). **APPROVED by `1.0.0_SA_CTO~Z` @add38b2768
(msg 30899) as the sha for the ONE portal DEV push; it supersedes `ec9f9a0e` and `97598dc3`. The push is Andrew's word through
`0.0.0_AB_MSTR~Z`; PROD is his separate word.** The ref is on branches `dsgn-r49-onto-dev` (checked out in
`C:/tmp/wk-dsgn-amgtv1-92/portal`) and `wk-DSGN_AMGTV1-111-portal` (checked out in `C:/tmp/wk-dsgn-amgtv1-111/portal`); every portal
worktree shares one repository, so the sha resolves from any of them.

**Source:** CTO rulings msg 30859 (FWD-20: every clause needs its fail-and-clean pair) and msg 30869 (FWD-27: the foot's money format
is a page cell), on the CVO's files @4a94e19089 and @7ca923a956. Issued @7be9573b19, ONE issuance: one order and one issuer cell.

## Cell `AV-zza-1` -- the Model foot prints money in the page's one money format (FWD-27 ground 1)

| step | result | evidence |
|---|---|---|
| First pass, ~111 | the foot's two money figures use the header's formatter `formatStatValue` | portal 8e4dad8f, drained @f06302a348; r49 3 of 3 (2 of 3 at base 97598dc3) |
| CTO review msg 30881 | outcome right; ONE amendment: key the format to a declared money set, print a non-money number plain, make the docstring true | AMENDMENT 1 @0ed013f33d; r49.cjs gained the arm "A NUMBER THAT IS NOT MONEY IS NOT FORMATTED AS MONEY", 3 of 4 on 8e4dad8f |
| Amendment, ~111 re-seated | a set of the two mnemonics gates the money format; any other number is plain grouped digits | portal b3440392 (`ModelTab.tsx`; one file +12/-8 against 97598dc3), drained @efc2f0c236; r49 4 of 4, r47 4 of 4, battery29 ALL PASS; `--verify` dropped 0 on both drains |
| Checks on `b3440392`, by this seat | 9 of 9 round checks green | r49 4/4, r47 4/4, r47b 3/3, r47i 4/4, r42 5/5, r43 5/5, r44 5/5, r45 5/5, r45b 4/4 (run 12:37Z in worktree 111) |

**The real run** (localhost:5174 on `8e4dad8f`, live API; walker 12:14:43Z to 12:23:38Z, DISARMED): `round35/walk/read-20261007T121443Z/`
@1765c0175c, 19 reads, 17 PASS, 1 FAIL, 1 ERROR.
- BA US foot: "Average daily value traded (three months): USD 1.36B; Market capitalisation: USD 152B". Its header tile: "Market cap USD 152B".
- AMD US foot: "USD 12.22B" and "USD 1.03T". Its header tile: "USD 1.03T".
- The FAIL is the ROG SW header's older as-of clause (unchanged since round 46). The ERROR is by cause: no walked name lacks an overlay
  field, because MSFT US was not walked.
- **The walk was on `8e4dad8f`, not on `b3440392`.** The amendment changes what a NON-money number prints, and no such fact is served
  today; r49 arm 1 reads the two money facts unchanged on `b3440392`. The live page was not looked at again after the amendment.

## Cell `AV-zza-2` -- a planted fail-and-clean pair for every render-check clause (FWD-20), issuer act, test files only

`round49/checks/plants49/plants49.cjs` copies the built page, injects ONE violating element, and runs the portal's own
`scripts/ui-contract-check.mjs`. **One unfiltered run, 12:21:16Z, 1,336 s: 9 of 9 clauses FAIL their planted page, each beside a clean
control.** Evidence copied to `round49/plants-run-20261007T122116Z/` (the log and 11 `grades.json` files).

| clause | the plant | the planted page reads | the control reads |
|---|---|---|---|
| fonts | one sentence in Georgia | FAIL, fonts ["Lato","Georgia"] | PASS |
| weights | one sentence at weight 600 | FAIL | PASS |
| sizes | one sentence at 9 px | FAIL, smallest 9 | PASS |
| radii | one box with a 12 px corner | FAIL, "12px" in the list | PASS |
| shadows | one box with a shadow | FAIL, 1 | PASS |
| lowContrastChars | pale grey text on white | FAIL, 39 characters | PASS |
| purpleFills | one purple button on a Security view | FAIL, 1 | PASS |
| tabPanelsWhite | a tinted surface inside the tab panel | FAIL, "non-white surface(s): rgb(230,236,200)" | PASS |
| the designed states present | the error-state marker stripped as it appears (a full six-state sweep) | FAIL, error missing on 6 of 6 panels | PASS (an untouched full sweep) |

- The CVO counted five clauses lacking a pair (fonts, weights, radii, shadows, the designed states). All five are in the table. The
  other four are planted as well, so no clause rests on a past real failure.
- The band clause's two limbs (two bands; light on dark) keep their pairs in `round35/checks/instrument/instrument35.cjs` arm 3.
- **Limits, stated:** the eight single-view plants are on the Thesis state only. The run built the product bytes of `8e4dad8f`; the
  instrument is the one on `b3440392` (`scripts/` is unchanged between them). The first attempt's purple-fill plant was mis-written
  (the colour variable needs `hsl()`), read PASS, and was corrected before this run; the earlier logs are device-local, not copied.
- **A finding for the instrument, not fixed here:** `ui-contract-check.mjs` still counts FOUR designed states and requires the
  standalone no-permission capture, while PRD v0.17's FWD-19 and FWD-20 read three. It passes today because the capture is still taken.

## For the grades

- **FWD-20:** the render check passes on the candidate (round 48: 76 PASS / 0 FAIL / 1 N/A) and now fails a planted page on every clause
  beside a clean control. The grade is the CVO's.
- **FWD-27:** ground 1 (three money formats on one foot) is cured on the candidate. Grounds 2 and 3 (the country in capitals; "Filings
  ... has not run yet" beside 10-K citations) are the producer's, routed to `2.0.0_SA_COO~Z` by msg 30869, and still show on the walk
  ("Country: UNITED STATES").
- **Not read this round:** the What-changed row labelled in the vendor's words ("Market capitalization adjusted to the requested
  currency ..."), which the CVO's file names under ground 2.

## Next

**Round 49: 1 of 1 order terminal; the issuer cell done.** Open at Andrew: the DEV push word for `b3440392`, then PROD, then his own
signed-in PROD walk (FWD-1). Open at the producer: FWD-7, FWD-8, and FWD-27's grounds 2 and 3. Backlog: row Z-S21; the What-changed
vendor label; the instrument's four-state count.
