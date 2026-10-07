# RENDER_ZW2 -- DSGN_AMGTV1 AV-zw-2 (0.9.0_WK_DSGN_AMGTV1~107)

The page's rendered text of the driver chart and the segment breakdown, from the deployed /thesis bytes of
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_groupB_fixture.json`, by walking the actual
`ThesisDriverChart.tsx`, `PassageTable.tsx` and `SegmentBreakdown.tsx` as a React tree (portal branch wk-DSGN_AMGTV1-107-portal).
The header line `| 737 | 747 ...` leads with an empty corner cell. AMENDMENT 1: a row whose figure count differs from the column labels (BA's 5-figure and 8-figure rows against 6 labels) is NOT in the table body; it is its own line beneath the table, the label then every figure in served order, so BA's table body is empty and both rows are lines. A row with exactly as many figures as labels would be a `label | figure | ...` table row. In the
segment breakdown each "Source" line and the cite beneath it sit in a CLOSED disclosure on the page; this text dump prints
closed disclosure content because it does not model the fold. The chart line itself is a recharts drawing and is not text.

## BA (table passages, three different ids)

### Driver chart at rest

```text
Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model
2023: 528 -- show the filing passage
2024: 348 -- show the filing passage
2025: 600 -- show the filing passage
3 fiscal year(s) from the filing
```

### Driver chart after one press on the first point

```text
Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model
2023: 528 -- show the filing passage
2023
| 737 | 747 | 767 | 777 | 787 | Total |
Cumulative deliveries 8,528 1,573 1,303 1,727 1,110
Deliveries 396 (9) 1 32 (14) 26 73 528
Some rows list a different number of figures than there are columns, because the filing's blank cells and footnote marks are not kept; those rows give their figures in the order printed and may not line up with the columns.
From the filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2023
2024: 348 -- show the filing passage
2025: 600 -- show the filing passage
3 fiscal year(s) from the filing
```

Y axis ticks for the served values (528, 348, 600): 528, 348, 600

### After pressing the second point next (the first closes)

```text
Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model
2023: 528 -- show the filing passage
2024: 348 -- show the filing passage
2024
| 737 | 747 | 767 | 777 | 787 | Total |
Cumulative deliveries 8,793 1,573 1,321 1,741 1,161
Deliveries 265 (5) 18 (8) 14 51 348
Some rows list a different number of figures than there are columns, because the filing's blank cells and footnote marks are not kept; those rows give their figures in the order printed and may not line up with the columns.
From the filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2024
2025: 600 -- show the filing passage
3 fiscal year(s) from the filing
```

### Segment breakdown

```text
Business segments -- from the filing
Commercial Airplanes
Commercial Airplanes revenue was $41,494 million in 2025, versus $22,861 million in 2024 and $33,901 million in 2023.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Total $89,463 $66,517 $77,794 / paragraph 18 (passage P0111)
BCA recorded a loss from operations of $7,079 million in 2025, an operating margin of (17.1)%.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Revenues / paragraph 71 (passage P0164)
BCA backlog was $567,290 million at December 31, 2025 versus $435,175 million a year earlier, within total backlog of $682,207 million.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Total Backlog $682,207 $521,336 / paragraph 56 (passage P0149)
BCA 2025 deliveries totaled 600 aircraft, including 447 737s and 88 787s, versus 348 total in 2024.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Table of Contents / paragraph 73 (passages P0166, P0167)
Defense, Space & Security
Defense, Space & Security revenue was $27,234 million in 2025, up from $23,918 million in 2024.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Total $89,463 $66,517 $77,794 / paragraph 18 (passage P0111)
BDS loss from operations narrowed to $128 million in 2025, a (0.5)% operating margin, from $5,413 million in 2024.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Operating margins (0.5) % (22.6) % (7.1) % / paragraph 105 (passage P0198)
BDS backlog was $84,786 million at December 31, 2025 compared with $64,023 million at December 31, 2024.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Backlog / paragraph 113 (passage P0206)
Global Services
Global Services revenue was $20,923 million in 2025, up $969 million on higher government and commercial services revenue.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Revenues / paragraph 121 (passage P0214)
BGS earnings from operations were $13,474 million in 2025, a 64.4% operating margin.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Revenues / paragraph 121 (passage P0214)
BGS earnings rose $9,856 million in 2025 "primarily due to a 2025 gain on the Digital Aviation Solutions Divestiture of $9,566 million."
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Earnings From Operations / paragraph 123 (passage P0216)
BGS total backlog of $29,720 million at December 31, 2025 increased 39% from $21,403 million.
Source
10-K filed 2026-01-30, ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / Backlog / paragraph 125 (passage P0218)
From the 10-K filed January 30th, 2026.
```

## ASML NA (three points, one shared id)

### Driver chart at rest

```text
Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization -- from the filing, not the model
2023: 393421721 -- show the filing passage
2024: 393283720 -- show the filing passage
2025: 385417665 -- show the filing passage
3 fiscal year(s) from the filing
```

### Driver chart after one press on the first point

```text
Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization -- from the filing, not the model
2023: 393421721 -- show the filing passage
2023 2024 2025 Issued ordinary shares with nominal value of €0.09 393,421,721 393,283,720 385,417,665
From the filing: TABLE / period 2023
2024: 393283720 -- show the filing passage
2025: 385417665 -- show the filing passage
3 fiscal year(s) from the filing
```

Y axis ticks for the served values (393421721, 393283720, 385417665): 393.4M, 393.3M, 385.4M

### After pressing the second point next (the first closes)

```text
Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization -- from the filing, not the model
2023: 393421721 -- show the filing passage
2024: 393283720 -- show the filing passage
2023 2024 2025 Issued ordinary shares with nominal value of €0.09 393,421,721 393,283,720 385,417,665
From the filing: TABLE / period 2023
2025: 385417665 -- show the filing passage
3 fiscal year(s) from the filing
```

### Segment breakdown

```text
Business segments -- from the filing
Authorized share capital
Authorized share capital: total EUR126.0 million, split into 700,000,000 cumulative preference shares and 700,000,000 ordinary shares of EUR0.09 nominal value each, one vote per share.
Source
20-F filed 2026-02-25, ITEM 3.D. RISK FACTORS / General Meeting. / paragraph 60 (passages P0059, P0060)
Other
No single segment can be named from the stored filing text for this finding.
Issued ordinary shares with EUR0.09 nominal value: 393,421,721 (2023), 393,283,720 (2024) and 385,417,665 (2025).
Source
20-F filed 2026-02-25, ITEM 3.D. RISK FACTORS / General Meeting. / paragraph 60 (passages P0059, P0060)
Treasury shares
Treasury shares: 6,162,857 (2023), 546,972 (2024) and 2,730,009 (2025) issued ordinary treasury shares of EUR0.09.
Source
20-F filed 2026-02-25, ITEM 3.D. RISK FACTORS / General Meeting. / paragraph 60 (passages P0059, P0060)
Major holders
Major holders: BlackRock, Inc. 26,325,103 shares or 6.83% and Capital Research and Management Company 19,612,223 shares or 5.09%.
Source
20-F filed 2026-02-25, ITEM 3.D. RISK FACTORS / 5.09% / paragraph 65 (passages P0064, P0065)
Board holdings
Board holdings: members of ASML's current Board of Management and Supervisory Board (8 persons) held 51,095.11 shares, or 0.01%.
Source
20-F filed 2026-02-25, ITEM 3.D. RISK FACTORS / 5.09% / paragraph 65 (passages P0064, P0065)
From the 20-F filed February 25th, 2026.
```

