# DSGN_AMGTV1 round 47 -- CLOSE (2.0.0_SA_COO~D, 2026-10-07 ~11:2xZ)

**Candidate: portal `ec9f9a0e`** (branch `dsgn-r47-onto-dev` in `C:/tmp/wk-dsgn-amgtv1-92/portal`) = DEV `8ddfe409` + 2 commits
(3 files, +11/-4; a fast-forward of DEV). **For the CTO's review from the render. The DEV push is Andrew's word through
`0.0.0_AB_MSTR~Z`; PROD is his separate word.**

**Source:** `ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md` @43d2e5eb3c, ROUND 47 items 1-4, and its CORRECTION @50e71b5b8d, item 5.
Issued @de235b1e7c (ONE issuance, 2 cells, fan-out 2 of 2) against PRD v0.17 @8730d6c042, ADMITTED.

## What was done, per list item

| item | result | evidence |
|---|---|---|
| **1. FWD-20: the Model tab's 10 px text** (`AV-zy-1`, ~108) | DONE on the candidate. The gap mark is 11 px. | Render instrument on `ec9f9a0e`: `states.model.sizes` PASS, smallest 11, 0 under 11 (`round47/instrument35-candidate-grades.json`; round 46 read FAIL, smallest 10). `r47.cjs` arm 1: 0 sizes under 11 over 242 sized nodes |
| **2. FWD-27: the Model tab's foot** (`AV-zy-1`, ~108) | DONE on the candidate. Read first, as ordered: all three lines were PAGE text. | Live walk, BA US and AMD US Model tab: no "Company short name" line; "2 of 6 kinds of input have been collected for this name."; "News: Articles we collect; last ran ... and worked." Country, Average daily value traded and Market capitalisation still print |
| **3. The instrument's FWD-18 clause** (`AV-zy-I`) | NOT CUT. It follows the hash the CTO said it would send (msg 30797). | The render instrument still reads 10 FAIL cells, all the purple-fill clause (`purpleFills` and `fwd18_controls` on thesis, exec, peers, model, posture). Tally 66 PASS / 10 FAIL / 1 N/A (round 46: 65 / 11 / 1) |
| **4. FWD-21, one read** | 10 of 10 ellipsised labels on the 30D face carry the full name on hover. Focus was not read. | `round47/FWD21_READ.md` @8a1ebcf475; re-read in this round's walk: 57 labels, 10 shortened, 10 of 10 hovers carry the full name |
| **5. An uncovered name says so once** (`AV-zy-2`, ~109) | DONE on the candidate. Read first, as ordered: the served payload has NO coverage marker, so the page rule is keyed on the served shape (no figure with a value, one reason shared by all seven). | Live walk, MSFT US header: key-figures text is "We hold no stored company data for this name yet." once, 0 tiles (round 46: 7 tiles, the sentence 7 times). `r47b.cjs` 3 of 3; ROG SW still draws 7 tiles |

## Checks on the combined candidate `ec9f9a0e`

`r47` 4 of 4, `r47b` 3 of 3, `r42` 5 of 5, `r43` 5 of 5, `r44` 5 of 5, `r45` 5 of 5, `r45b` 4 of 4; battery29 ALL PASS (0 skipped; tsc 0,
eslint 0). Log `C:/tmp/r47-candidate-checks.log` (device-local). Workers: ~108 portal 38247180, proof VALID, drained @93b4bfd987;
~109 portal d11a407b, proof VALID, drained @9a14382252; `--verify` dropped 0 on both. No surprise row, no harness line changed.

## The real run (localhost:5174 on `ec9f9a0e`, live API; walker 10:59:57Z to 11:12:49Z, DISARMED)

`round35/walk/read-20261007T105958Z/` (closewalk35.mjs): 27 reads, 26 PASS, 1 FAIL, 0 ERROR. The FAIL is the ROG SW header's older
as-of clause, unchanged from round 46 and ruled on there (the 2026-10-05 covered-names rule).

**FWD-4, 7 and 8 on COVERED names, as the CORRECTION orders** (BA US, VLO US, AMD US; MSFT US walked only for its designed state):
- **FWD-7:** BA US shows 12 officers and VLO US shows 5, both from the 10-K's Item 10. AMD US shows no officers and prints the chain tried.
  So FWD-7's gap stands on a covered name (AMD US); its cure is AMGT_RESAPP ba-22.
- **FWD-8:** on all three covered names the Price column is still headed "currency not stated". Every peer price read on BA, VLO and AMD
  is a US listing; the mixed-currency rows of round 46 were on MSFT's table. The header wording is the table's, as the CTO ruled.
- **FWD-4:** BA, VLO and AMD pass the overlay census (0 not-served strings on 19 carried fields each).

## Named for AMGT_RESAPP (`2.0.0_SA_COO~Z`), not built here

1. **The news source is served with storage words:** `harvested news (the overlay feed, gold article_security_mention)`. The page now maps
   that exact string to "Articles we collect"; if the producer changes the string, the row falls back to "source not named". A plain
   served source name would remove the page-side mapping.
2. **No coverage marker is served** for a pool name outside coverage. The page infers it from the shape of the seven header figures. A
   served marker would let the page say "not covered" in its own words instead of repeating the producer's reason.

## Not established

- Keyboard focus on an ellipsised label (FWD-21's "hover or focus": hover only).
- `round11/checks/ledger.cjs` reads 2 of 3 at the base and on the candidate (its re-run sentence arm, stale since round 45 removed the
  control); it is not in battery29 and was not repaired.
- The Model tab foot on a name whose news class has not run.

## Next

**Round 47: 2 of 2 orders terminal.** The candidate goes to the CTO's review. Open in the round: cell `AV-zy-I` (the instrument clause),
which is cut when the CTO's hash arrives; FWD-20 cannot grade REALIZED before it. Backlog: row Z-S21 (case value and currency attributes
on `ModelTab.tsx`).
