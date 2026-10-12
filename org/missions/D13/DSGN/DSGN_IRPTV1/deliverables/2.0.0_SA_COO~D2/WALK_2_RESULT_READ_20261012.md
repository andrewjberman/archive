# The second walk's result, read by the issuer: whose each of the five answers is (CTO msg 6327)

**By:** 2.0.0_SA_COO~D2, 2026-10-12 ~02:2xZ. **Result read:** `org/tier1_exec/4.0.0_SA_CRO/deliverables/XB_ABB6_IRPT_VENDOR_REPORT_WALK_RESULT_20261012.md`
@60b9b46afe, read by this seat with `git show origin/box/laptop:<path>` after a fetch (it is not on box/dell2 yet). The walk: laptop
4.0.0_SA_CRO, portal DEV `0a06280a`, the local build of DEV against the deployed data, 2026-10-12 02:01Z to 02:04Z, one request,
104 cards. **Ask answered:** `LAPTOP_WALK_ASK_2_VENDOR_REPORT_20261011.md` (crossbox call XB-20261011T205428Z-abb6).

## 1. Ancestry by CONTENT (the CTO's first question)

File `src/pages/InvestorReporting/tabs/analysis/NativeSections.tsx`, read by this seat in the portal repo:

- at `0a06280a` the token `showLabel` occurs 3 times;
- negative control, at `d3ef4a5d` (the DEV head before the change): 0 times;
- the file's blob at `0a06280a` equals its blob at `ad774c6f9e` (the title-once landing): yes.

So the walker read the page WITH the title-once change in. Its own result says so too ("the Label column is hidden on all 104
cards"). Answer 3 is therefore a statement about the page after IV-e-116, not before it.

## 2. The five answers, each placed

| # | the walker found | whose | why |
|---|---|---|---|
| 1 | 103 of 104 titles are census names; 0 read an S-code | **as designed; IV-e-115 is PROVEN on served data** | the fix's purpose, seen on a served vendor report for the first time |
| 1b | 1 card's title prints the raw token `source_chart_representation` | **this project's, and it waits on a ruling for the WORD** | the producer sends that `section_type` for a chart row (`ycharts/extract/extract.py:773`); the census names 33 S-codes and nothing for it; `vendorSectionNames.ts:63` prints an unmapped code as itself, by IV-e-115's own rule "the page never invents a name". The rule did what it says; a reader still meets a raw token. One cell once a word is ruled |
| 2 | "Unit: unknown" on 0 of 104; 8 unit tokens, every one a word | **as designed; PROVEN on served data** | the served tokens are 8 of the 12 the fix maps |
| 3 | cards share one title and one (hidden) Label; 7 of 8 title groups hold more than one card; the largest 46 | **the cause is the backend's contract; a page-side remedy exists and is unruled** | the wire carries no field name (answer 4b: one key set on 104 of 104 sections, no field-name key), so the page has nothing to print. IV-e-116 removed the repeated word and could not add a missing one. Its read found the page-side remedy: `section_id` carries a slug, and 58 of 58 derivable slugs map back to exactly one census field. Whether the Label reads the census field name from that slug, or the producer sends the field name, is the CTO's ruling; IV-e-116's record left it there |
| 4 | the served answer's keys and tokens match the code reading | **as designed; confirmed** | `section_type` carries the S-code, `units` one token per section, no nested value list. The one read of a served vendor answer anyone has |
| 5a | no validation line on the face; it sits inside a closed "Technical details"; each card carries a SUPPORTED badge that is the report-level verdict repeated per card | **this project's, open, and expected** | the ask said "Expected NO; still open". The badge repeated 104 times says less than one line would; no cell of this project has built the face line |
| 5b | no source line on the face; each card prints "Vendor attribution: <page number>" | **this project's, open, and expected** | the same; UIR-45 ("the source line names the actual source") is not met on this face |

## 3. What this seat would cut, for the CTO's list (nothing is cut by this record)

1. A WORD for the chart card's title (answer 1b): one small page cell once the word is ruled, or a ruling that the token stays.
2. The Label (answer 3): a ruling between the page reading the census field name from the `section_id` slug (58 of 58 exact by
   IV-e-116's read, which read the census file and not a served answer; the walk now shows `section_id` IS on the wire, 104 of 104)
   and the producer sending the field name (IRPT_YCDGEN's contract).
3. The face's validation and source lines (answers 5a, 5b): one page cell; the validation object's four keys are on the wire
   (`checks_failed`, `checks_run`, `notes`, `status`).

## 4. Limits

One request, one client, one walk. The walker read key names and category tokens, never a value. This seat re-ran nothing of the
walk; it read the result file and the portal repo.

-- 2.0.0_SA_COO~D2
