# DSGN_AMGTV1 round 59 -- cut plan for SAW-01..23 (prep, 2.0.0_SA_COO~D1, 2026-10-09 ~06:2xZ)

**Input:** the walk register `docs/briefs/dsgn-amgtv1-security-analysis-walk-findings-20261009.json` @5786933a9c (Andrew-direct
~05:0xZ-05:1xZ, record @1725deb826), named round 59's scope by the CTO (rulings batch @6c538a0bfd G). A read-only code map of portal
`7892d865` was taken at ~06:1xZ; its facts are below with file:line. **This is prep, not an issuance:** the round is cut from the CTO's
round-58 analysis, in one issuance.

## What the map settles

- **The spine has more served signal than it shows.**
  - Each served day carries `mention_score`, `tier_a..tier_d`, `trailing_7d_sum`, `breakout_ratio`, `z_score`, and `events[]`
    (`first_day`, `last_day`, `lead_headline`, `articles_total`). Only `articles_total` and the collection state `data_status` are drawn
    (`components/TimelinePanel.tsx:201-205, 601-659`).
  - The searched / partly / not legend is page-composed over `data_status`.
  - The page alone can mark the top days (by `breakout_ratio` / `z_score`) and label the events. It can also drop the collection legend.
  - **No per-day price series is served to the timeline** (`TimelineRangeResponse`, 100-108), so a price line on the spine is a RESAPP ask.
- **News:**
  - Feed items (`CoverageItem`, `types.ts:583-597`) carry no mention count, relevance or summary, so ranking the feed by relevance is a
    RESAPP ask (SAW-06, SAW-07).
  - The "In the news" card's items DO carry served `mentions`, and the producer sorts them by mentions (`TopBand.tsx`,
    `top_band.py`). The page can merge the two surfaces into one, with each headline once (SAW-05, SAW-09).
  - The word cloud is served `word_cloud.terms` (SAW-08); the page may drop it or show the top few.
- **Absences:**
  - **Served verbatim:** the five Thesis notes (`dossier_sections[].reason`, `DossierSections.tsx:72`) and the Exec caption
    (`management.source_item`). The page may fold, show once or omit these; rewording them is a RESAPP ask.
  - **Page-composed, the page owns them outright:** "No drafted prose" (`ThesisTab.tsx:229`), the per-row "not stated" and "per
    Bloomberg, not the filing" (`ExecManagementTab.tsx:86-136`), "This table is the Bloomberg fallback" (298-306), the Peers absence
    sentences (`PeersTab.tsx:174-290`), the posture and dossier lines (`SecurityOverlay.tsx:148-293`, `PostureTab.tsx:96-106, 570-630`),
    "Worked" in the provenance panel, the chatter "Readings of ..." sentence (`SecurityOverlay.tsx:117-129, 327-334`), the
    "Earnings dates are not on file" line (`TimelinePanel.tsx:660-664`), and the tab subtitles.
- **Structure:** `SecurityAnalysis.tsx` mounts `IdentityHeader` -> `CoverageNote` -> `TopBand` -> `InputProvenance` -> tabs.
  `IdentityHeader` (`SecurityOverlay.tsx:428-551`) holds the tiles, the description (printed twice: `TopBand.tsx:98-107` `CompanyLine`,
  and `HeaderBrief.tsx:43-69`), the feed, the spine, the fold and the chatter strip.
- **Print:**
  - The preview title is page-composed from the raw key (`PrintExportAction.tsx:144-146`).
  - "date not stored with this figure" is in the server-rendered PDF (`lib/research/print/render_pack.py:486`), which is a RESAPP/print ask.

## Proposed cells (disjoint write sets; up to 6 workers)

| cell | findings | owned files (under `SA/`) |
|---|---|---|
| A. The spine | SAW-01, 02 (top days + labelled events, no price line), 03, 04, 08 | `components/TimelinePanel.tsx`, `components/TimelineWordCloud.tsx` |
| B. One news surface | SAW-05, 07 (the range matches the items; no why-line until served), 09 | `components/HeaderBrief.tsx`, `components/TopBand.tsx` |
| C. Page structure and plumbing out of the face | SAW-11 (the fold), 12, 14, 20, 21 (the overlay subtitle) | `SecurityAnalysis.tsx`, `components/SecurityOverlay.tsx`, `components/InputProvenance.tsx`, `components/CoverageNote.tsx` |
| D. Thesis + Posture absences | SAW-10, 11 (the tab), 18 (segment notes), 21 (the tab subtitles) | `tabs/ThesisTab.tsx`, `components/DossierSections.tsx`, `tabs/PostureTab.tsx`, `components/SegmentTable.tsx` |
| E. Exec + Peers absences | SAW-15, 16 | `tabs/ExecManagementTab.tsx`, `tabs/PeersTab.tsx`, `cscTable.ts` |
| F. Model + tiles + print title | SAW-17, 19 (the title only), 22 | `tabs/ModelTab.tsx`, `components/model/WhatChangedPanel.tsx`, `modelSheet.ts`, `components/HeaderCards.tsx`, `components/StatTile.tsx`, `components/PrintExportAction.tsx` |

- **Not a cell this round:**
  - SAW-13 (footers). `CardFooter.tsx` is called from 9 files, so the one-as-of rule cuts after A-F land, as its own cell, or folds
    into the merge.
  - SAW-23: already ruled.
- **Shared file `reasonWords.ts` (SAW-10, 11, 15, 16):** no cell edits it. Each cell changes where a sentence is placed, not its words.
- **`IdentityLine.tsx` (the per-tab "AMD US"):** it is mounted by all five tabs. Cell C removes it from the tab mounts only if the CTO
  rules that the tabs D/E/F may each drop their own mount line. Otherwise it is a follow-on cell.

## RESAPP asks (producer, not this project)

1. A per-day price series on the timeline route, for the spine's price line (SAW-02).
2. A relevance/mention field (and optionally a one-line summary) on feed items, for ranking and a why-line (SAW-06, SAW-07).
3. The print PDF's "date not stored with this figure" said once, not per line (SAW-19, `render_pack.py:486`).
4. Shorter served absence reasons (the five dossier notes, the Exec `source_item`), if the CTO wants their words changed rather than
   folded.
