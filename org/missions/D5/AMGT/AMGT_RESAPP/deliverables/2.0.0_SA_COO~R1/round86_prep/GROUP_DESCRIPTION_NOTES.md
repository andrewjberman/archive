# AMGT_RESAPP round-86 PREP -- company_description drawn from the business item only (CTO~DELL1 round-85 analysis R5)

Read-only grounding (no store write, no model call), 2026-10-09 ~14:3xZ. Check: `checks/r86_description.py`.

## 1. The producer, and why NU's lines are Item 5

- `lib/research/filings/drafting_build.py:66-67` `SECTION_SOURCES["company_description"] = ("segments", "commentary")` -- the section
  is filled from the analysis's ITEM CLASSES `segments` and `commentary`, not from any filing ITEM. `Drafter.draft` (`:289-327`) walks
  those classes in order and keeps up to `SECTION_LIMIT = 10` items (`:75`), with no check of where an item's evidence sits in the filing.
- A `segments` finding is typically a revenue or segment figure, and the filing states those in Item 5 (20-F OFR) -- so NU's 10 lines are
  8 Item 5, 1 Item 3.D, 1 Item 4.B.
- The served route passes the stored section through (`scoped_amgt.py` `drafted_sections`); `company_description_verdict`
  (`scoped_amgt.py:4266`) already marks NU's section FAILED ("no served D-1 company_description sentence passing the describes-the-
  business test"), so the page shows a verdict, not an empty state.

## 2. Measured on the live function (HZoC2x, 2026-10-09 ~14:3xZ) -- sentences per cited item label

| name | form | sentences | business-cited | item mix |
|---|---|---|---|---|
| ASML_NA_Equity | 20-F | 5 | 0 | 3.D 1, 5 4 |
| BABA_US_Equity | 20-F | 1 | 0 | 5 1 |
| NU_US_Equity | 20-F | 10 | 1 | 3.D 1, 4.B 1, 5 8 |
| PBR_US_Equity | 20-F | 4 | 0 | 5 4 |
| SAP_GY_Equity | 20-F | 5 | 0 | 5 5 |
| AMD_US_Equity | 10-K | 0 | 0 | -- (already empty) |
| NVDA_US_Equity | 10-K | 0 | 0 | -- (already empty) |

24 of 25 served company_description sentences cite a banned item. `r86_description --crit AC1` reads **NO** (D1 24 of 25 not business,
D2 24 of 25 banned, D3 four 20-F names non-empty without a business line).

## 3. The repair -- producer-time, two halves

1. **Code (future drafts):** in `drafting_build.Drafter.draft`, for `company_description` only, keep an item only when EVERY evidence
   passage it cites locates in the business item (20-F Item 4 / 4.B; 10-K Item 1, not 1A/1B/1C) -- the passage map already carries each
   passage's item. No business-cited item -> the section is EMPTY (the page's empty state shows, and the verdict reads absent, not
   FAILED). Tests: an Item 5 segment finding is dropped; an Item 4.B finding is kept; a filing with no business item yields an empty
   section.
2. **Store (the served objects):** the five 20-F names' `drafting/v1/<KEY>.json` must change -- the served route reads the stored draft.
   **HAZARD:** do NOT rebuild NU's draft from its stored analysis with `drafting_build` -- NU's analysis items still carry the pre-round-85
   glued text, so a rebuild would undo jj-2's in-place repair. The store act is a SECTION-LOCAL in-place edit, all five names alike: in
   each stored draft, keep only the `company_description` sentences whose evidence is all business-located (NU keeps 1; ASML, BABA, PBR,
   SAP become EMPTY); every other section byte-equal. Five keys, no fetch, no model call -- one pair (like jj-2's ADDENDUM 2, widened
   to five names). The 10-K names already serve an empty section: no write.
3. **Not serve-time:** a redeploy alone changes nothing; the bytes are in the stored drafts.

## 4. The check

`r86_description.py --crit AC1 [--where deployed|local] [--keys ...]` (default keys: the five 20-F names + AMD, NVDA): D1 every
non-empty sentence business-cited; D2 0 banned-item sentences; D3 a name with no business-cited sentence serves an empty section. Base:
NO. After the five in-place edits it reads YES on the live function (NU 1 sentence, Item 4.B; the other four empty).
