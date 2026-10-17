# AMGT_RESAPP round 112 -- `AMGT-bs-4`: the earnings-row read on PROD `932cea99` and the live byte tie (W491-S2), `2.0.0_SA_COO~R1`, 2026-10-17 ~19:5xZ

**Asked by** the CTO (round-111 analysis item 1, msg 7711): walk RIO LN's and ICT PM's earnings row on PROD `932cea99`, and tie the live bundles to that build by bytes with the prior build as the negative control. A read; a code cell only if it fails. **It does not fail.**

## The byte tie (done earlier this round, not repeated)

`round111/LIVE_TIE_932CEA99.md` @b39f7d6e89: run 39057551567 (head `932cea99`, success); live `index.html`, the main bundle, the CSS, four vendor bundles and the Security Analysis chunk `index-CZ3eT7d6.js` byte-equal to the run's artifact; br-3's marker `a vendor figure` in the served chunk (count 1) and in 0 chunks of the previous deploy's artifact (run 39042189942).

## The earnings row, read in a shot of the round-111 close walk

The close walk (`round111/PROD_CLOSE_WALK.md`, walker on a local build of PROD `932cea99`, evidence `C:/dev/ui-walk-evidence/r111-close/`, shots under `tmp/ui-walk/20261017T182727Z/shots/`) walked RIO LN's Model-tab version selects. The state `Earlier version October 14th, 2026, 9:12a ET` against `Later version October 17th, 2026, 9:08a ET` lists **48 changed** figures, and the earnings row is among them (shot `016-RIO-LN-Model-select-0-October-14th-2026-9-12.png`, read by the issuer in a crop, `crop_oct14_end.png`): the figure **"Earnings announcement dates and the fiscal period each covers (BULK field: Bloomberg returns a list of rows; each row's announcement date is a DATE; rows kept in Bloomberg's own order)"** reads, before `2026-10-13 (2026:Q3), 135 entries` and after `2026-10-13 (2026:Q3), 136 entries`, change `--`, change % `--` (the round-109 list reading, unchanged), no braces, no brackets, no `[object Object]`, no `undefined`.

**The instrument, on the same pair.** Round 109's walk of the candidate `d060d119` reported three `raw-code` findings quoting `[{"announcement_date":...` on this pair's states with the row's `Full figures` closed (`W491-S2`: the raw text sat in the closed `details > p`, so the walker's text check sees closed details). The close walk of PROD `932cea99` reports **no `raw-code` finding on any RIO LN or ICT PM state**. A check that fired on the old code over closed details, silent on the same pair now, reads: the row's detail text carries no raw list JSON.

## Reading and its limits

**W491-S2 reads as fixed on PROD `932cea99`:** the row's visible cells are plain text (shot) and the instrument that caught the raw text in its detail is silent (walker). **Not verified, stated:** the row's own `Full figures` detail was not OPENED in that state (the walker opens details only in the default pair, where the earnings row is absent); the detail text `<date> (<period>); ...; <n> entries in all` is graded by the round-111 harness `CHANGED OBJECT CELLS HARNESS` O3/O4 on the fixture and by round 110's `bq-1` harness L10, not read on the live page. ICT PM's earnings row was not looked for in a shot (RIO LN's was).

**A by-product finding:** the walker's `format:dates` finding (`2026-09-22 | September 22nd, 2026`) fires in exactly these older-pair states: the earnings row's text prints the served ISO `announcement_date` while the page's other dates read long form. Filed in `round112/WALK_FINDINGS_TRIAGE.md` as a class, not a defect of this read.
