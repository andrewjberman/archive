# DSGN_AMGTV1 round 66 -- the re-grade walk of FWD-7, FWD-8 and FWD-27 (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~14:3xZ)

**List:** `ledger/ROUND_ANALYSIS.round65.md` ADDENDUM 1 @efdadb720e. Round 66 is ONE re-grade walk on `2726bbe7` (its SA tree is
byte-equal to PROD `18364342`), graded by `3.0.0_SA_CVO` against each FWD's ACCEPT. No cell is cut; the walk is the issuer's act.

**The walk:** `tmp/ui-walk/20261009T142010Z` (dell1), 14:20Z-14:29Z.
- Run on a `dev:live` build of portal `2726bbe7` with no scratch edit, signed in with the walker service account against the real
  backend.
- `--security "NG/_LN_Equity" --security "BP/_LN_Equity" --security "AMD" --security "992_HK_Equity" --security "ASML_NA_Equity"
  --security-press 'role=button[name="News"]'`. Every tab of each name was walked.
- 151 screenshots, 0 API issues, 0 guard aborts. The walker disarmed, and its login is refused (401).

## FWD-7 -- "A PM sees who runs the company, for every covered name"

ACCEPT: "The management tab shows the company's officers and says where the list came from, even when the company's filing has no officer
section."

| name | shot | reads |
|---|---|---|
| NG/ LN (National Grid PLC) | 010 | EXEC MANAGEMENT "From Bloomberg's officer list": 9 officers with roles (Zoe A Yujnovich, Chief Executive Officer; Andrew Agg, Chief Financial Officer; ... Julian Baddeley, Secretary). "9 officer(s), as of October 7th, 2026". No filing has been read for this name ("company filings read for this name -- No company filing has been read for this name yet"). |
| BP/ LN (BP) | 039 | EXEC MANAGEMENT "From Bloomberg's officer list": 10 officers (Marguerite Eileen O'Neill, Chief Executive Officer; Katherine Anne Thomson, Chief Financial Officer; ... Benedict J S Mathews, Secretary), plus the research team's management note (Source: BP plc Research Pack 2026 04 03_v1). |

Round 46's board read "BP/ LN and NG/ LN served none". Both now show officers, with where the list came from, and neither has a filing on
file.

## FWD-8 -- "A PM reads the comparable companies as a clean table"

ACCEPT: "The peers table keeps what Andrew liked, shows readable tickers, explains missing columns once and neatly, and shows no internal
system text." The analysis's case is "one mixed-currency peer group showing its currency stated and no cross-currency figure".

| name | shot | reads |
|---|---|---|
| ASML NA | 131 | 12 comparables. The subject row reads "EUR 1,626 / EUR 541,932 / EUR 625,609". The peer Mkt Cap reads "USD ...". The peers' Price (last) values carry no currency, and the fold says once: "These peers report it with no stated currency, so the Average row shows no figure for Price (last)". The Median, Min and Max of Price read "--". The Mkt Cap / EV aggregates are over the 12 USD peers (n=12); the EUR subject is not mixed in. Missing columns are explained once in "What is not on file" (12 absent columns). |
| 992 HK (Lenovo) | 099 | The same UNSTATED price line (round 61). |

**For the grader, on FWD-8:**
- the column headers read "Mkt Cap (USD mm)" and "EV (USD mm)" while the subject row in those columns is stated in EUR;
- Tencent's ticker reads "BMMV2K" (served as is);
- SK hynix's ticker cell reads "This listing has only an exchange number; we have no company match for it yet."

Both bear on "readable tickers".

## FWD-27 -- "A PM reads plain words and figures that agree with each other"

DONE WHEN: a walk of every tab on 3 names reads 0 system-wording strings, one display name per security, one money format and one time
zone (ET) across the figures the PAGE formats, with served drafted prose graded as served.

| item | reads |
|---|---|
| Money format, page-formatted | Header tiles: "USD 645.86" (AMD), "GBp 1155.00" / "GBP 58.06B" (NG/ LN, the served pence and pound units), "EUR 1626.20" (ASML NA). For ASML the peers table writes the subject price "EUR 1,626", with a thousands separator, beside the tile's "EUR 1626.20" without one, so the same figure appears in two forms. |
| Walker check `format:money` | "USD 1,234 and $1,234 on one page", on BP's steps. BP's served research note writes "$40bn valuation", so this is served prose. |
| Walker check `format:dates` | "2026-09-22 \| September 22nd, 2026", on Thesis windows. These appear to be served drafted text; the CVO reads them. |
| Country case | The identity header reads "Utilities -- GB", "Energy -- GB", "Information Technology -- NL / US": one form, the served code. The round-46 "Country: UNITED STATES" form is gone. |
| The Filings line | "ABOUT THIS DATA -- company filings read for this name": ASML NA reads "20-F filed February 25th, 2026 -- used for the filing passages, the written sections, the segment breakdown"; NG/ LN and BP/ LN read "No company filing has been read for this name yet, so nothing on this page comes from one." |
| Time zone | Every page-formatted stamp reads ET ("October 9th, 2026, 9:07a ET"). |

## Carried (not of this walk's grade)

- From FWD-1 (`ADJUDICATION_v40`): Valero's thesis-driver chart is absent, and the header loads in 18.6 s.
