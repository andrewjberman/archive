# FWD-18 on ASML NA -- what the deployed function serves (a read for the round-79 walk)

**For the walker, in one line:** on ASML NA's Thesis tab, read the driver-chart place (it should draw NO chart and say
"The filing text kept here counts the company's own shares or describes its share capital, so no driver chart is
shown."), then press the figure in the company-description sentence "... (8 persons) held 51,095.11 shares, or 0.01%."
and read that it opens the filing passage "Members of ASML's current Board of Management and Supervisory Board (8
persons) 3" (20-F filed 2026-02-25, Item 3.D, paragraph 65).

Read by a drafting subagent for `2.0.0_SA_COO~Z`. ONE GET-shaped direct invoke of `opal-amgt-scoped-api`, read-only, at
2026-10-08T10:20:23Z: `/api/scoped/amgt/security/ASML_NA_Equity/thesis`, header `x-firm-id: opal`, modelled on
`round78/checks/r78_bb18_issuer_hand_reads.py`. Status 200, no FunctionError. Live CodeSha256
`+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=`, last modified 2026-10-08T07:19:32Z (the bb-18 deploy). No page was
opened and nothing was written.

## 1. The outcome being graded

`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`, lines 676 to 688:

```
676:   FWD-18 The company's own filings are read for the analyst, and the one
677:          chart that matters is drawn from them
678:          DONE WHEN  EXERCISED -- (v0.40) a seat clicks, on demand, a
679:                     filing-derived figure on a covered company the grading seat
680:                     names, through to the passage it came from. An analyst's
681:                     own click stays the ACCEPT
682:          ACCEPT     The Thesis tab says, in the company's own words and with
683:                     each sentence linked to the passage in the filing it came
684:                     from, what the company is doing now, its biggest
685:                     challenges and its biggest bets; and it shows one chart,
686:                     chosen for that company, of the thing it lives or dies
687:                     on. The Model tab's figures are the plain financial
688:                     model, built the same way for every company.
```

The DONE WHEN is a click from a filing-derived figure to its passage. The chart is in the ACCEPT.

## 2. The served `thesis_driver` (the raw driver the drafted notes name)

```
series             Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization
unit               number of shares
resolution         cited
source_passage_id  P0059
why                The count shows ASML's authorized repurchase of up to 10% of issued capital converting into a
                   shrinking share base, the one quantified trend in this governance excerpt.
points             2023  393421721  passage P0086  span [49888, 49899]      <- first
                   2024  393283720  passage P0086  span [49900, 49911]
                   2025  385417665  passage P0086  span [49912, 49923]      <- last
absent_reason      null
held_uncited       []
```

It cites two passages by id, P0059 (the series) and P0086 (all three points). **Neither passage's text is in the
response**: `P0086` occurs 3 times in the body and `P0059` once, each time as an id inside `thesis_driver` and nowhere
else. So the driver's own figures cannot be followed to a passage from what is served.

## 3. The served `thesis_driver_chart` (what the page draws)

```
status              ABSENT
refused             true
driver_series       Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization
driver_unit         number of shares
reason              The filing text kept here counts the company's own shares or describes its share capital, so no
                    driver chart is shown.
plain_reason        (the same sentence)
points              []
points_count        0
held_uncited_count  0
series_translated   null      unit_translated null      why_translated null
```

The chart is REFUSED (the round-76 ruling 7 refusal, `lib/research/filings/table_class.py driver_refusal`, as the round-78 GROUP_C notes name it; not re-read here). The label and
the unit are served; no point is. The three share counts of section 2 are served on `thesis_driver` and are not drawn.
So the analysis's phrase "its served `thesis_driver` is a shares-outstanding series" is true of the raw block, and the
chart beside it is refused with a plain reason.

## 4. What else on the response bears on FWD-18

- Drafted notes: `drafting_status` SERVED, source `pool`, from the 20-F filed 2026-02-25 (accession 000162828026011378),
  `as_of_date` 2026-02-25; `drafting_provenance.dropped` reads 3 (its meaning was not read).
- Sentences served, by section: company_description 1, investment_thesis 0, risks 0, ceo_bio 0, recommendation 1. Two
  sentences in all.
  - company_description: "Board holdings: members of ASML's current Board of Management and Supervisory Board (8
    persons) held 51,095.11 shares, or 0.01%." Its evidence carries the passage TEXT: P0064, "Members of ASML's current
    Board of Management and Supervisory Board (8 persons) 3", location "ITEM 3.D. RISK FACTORS / 5.09% / paragraph 65";
    and P0065, a BlackRock Schedule 13-G/A footnote.
  - recommendation: "The updated Dutch Corporate Governance Code 2025 applies to financial years starting on or after
    January 1, 2025, and to comply ASML has included a Risk Management Statement in its 2025 Annual Report based on
    EU-IFRS." Evidence P0002, "to the financial years starting on or after January 1, 2025,".
- `passage_coverage`: ONE section of the filing was read, "Item 3.D. Risk Factors", 70,000 of 1,091,017 characters
  (share 0.0642, `truncated: true`), 86 passages; "Item 5. Operating and Financial Review and Prospects could not be
  read from this filing, so no note here rests on it."
- `segment_breakdown`: 0 rows, "The filing text kept here is about the company's share capital and who holds its shares,
  so no segment breakdown is shown."
- `research_coverage`: covered, 95 covered names.

## 5. Reading it against FWD-18

- **The DONE WHEN can be pressed on this name**: one served sentence carries a filing-derived figure (51,095.11 shares,
  0.01%) with its passage text and location. Whether the page makes that figure a click that opens the passage is what
  the walk reads; this read did not open the page.
- **The ACCEPT is not met by what is served for this name**: no chart is drawn; the notes say nothing of what the company
  is doing now, its challenges or its bets (0 sentences in the thesis and risks sections); and the text kept from the
  filing is 6.4 percent of one item, cut off, which is why the notes are about share capital and governance.
- The served refusal is an honest answer and reads in plain words. A walker should grade the press, and record the chart
  as refused with its sentence, not as missing.

## 6. Not measured

- The rendered page: whether the refusal sentence shows, and whether the figure is clickable through to the passage.
- The stored drafted document and the filing text behind P0059 and P0086 were not opened (one invoke was the brief).
- Why the kept filing text is the first 70,000 characters of Item 3.D and Item 5 could not be read.
- Any other name. This is one company.
