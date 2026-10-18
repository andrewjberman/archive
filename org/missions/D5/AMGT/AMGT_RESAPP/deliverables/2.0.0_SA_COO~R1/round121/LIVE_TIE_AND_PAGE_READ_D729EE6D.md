# AMGT_RESAPP round 121 -- the LIVE site tied to PROD `d729ee6d` by bytes, and the CEO profile read on the running Security Analysis page, `2.0.0_SA_COO~R1`, 2026-10-18 ~17:4xZ

Evidence outside the repository: `C:/dev/ui-walk-evidence/r121-tie/{new,old,live}/` and `C:/dev/ui-walk-evidence/r121-page/` (three screenshots, three fixtures, three logs; research data only, no client account). Push state of every commit named: LOCAL on box/dell1, unread. Method as `round115/LIVE_TIE_FF611566.md`.

## 1. The live site tied to PROD `d729ee6d` by bytes

1. **The run.** `gh run list --repo Opal-Capital/portal --branch PROD`: run `39149629746`, head `d729ee6d84565bfa4ce508ddf199d40ac0851482`, completed, success; H2's receipt `51cffedd1e`: release `release/20261018T172512Z` (ONE feature, `cand/dell1/amgt-sa-ceo-three-states` @43762e0d, client-facing 0), tag `portal-v2.1.241`, PROD `ff611566` to `d729ee6d` (an `ls-remote` read).
2. **The live site.** `https://www.opalinvest.dev/index.html` (`Last-Modified: Sun, 18 Oct 2026 17:28:48 GMT`): byte-equal to the artifact's `index.html` (`cmp`); **the six entry assets each byte-equal** (`index-BSYWDGQz.js`, `index-MWB7k_gj.css`, `vendor-query-a03VQeS3.js`, `vendor-react-DLAg9veD.js`, `vendor-recharts-DHYDCNR3.js`, `vendor-ui-DwHOHMaU.js`).
3. **A content marker in the served chunk (unlike rounds 114 and 115, this change carries unique strings).** The artifact's one chunk containing `No CEO profile has been written for this company yet.` is `assets/index-C6JNSUjT.js` (251548 bytes, the marker once); **the live chunk is byte-equal to it**, the marker count in the live chunk reads 1, and the third sentence `the state of this profile is not recognised by this page` is present in it.
4. **Negative control.** The previous deploy's artifact (run `39092905765`, head `ff611566`): **0** chunks contain the not-written sentence. The comparison discriminates, and the live site serves the new bundle.

## 2. The CEO profile on the running page (the CTO's round-120 grade, `AMGT-cb-2`)

The page `https://opalinvest.dev/security-analysis/<KEY>`, Exec Management tab, rendered by `portal/scripts/ui-smoke.mjs --origin https://opalinvest.dev --click "Exec Management"` in headless Edge with the stubbed auth session: the page's JavaScript is the LIVE bundle of section 1; **the stubbed session gets no data from the live API** (the identity header shows `The identity header could not be loaded` and the tab shows skeleton rows: the first run, screenshot read), so each read feeds the page the SERVED `/thesis` body of the name (read from `opal-amgt-scoped-api` at CodeSha256 `V9ZIXiUY..` at ~17:4xZ) through `--fixtures`, and the forced corrupt case a copy of TSM US's body whose management object carries a corrupt profile (`ceo_public_profile` the string `corrupt`; the reading `UNREADABLE_OBJECT`, no reason). Instrument: `round121_prep/checks/r121_running_page_read.py`. The three screenshots were READ:

| case | served reading | the sentence the page prints (read from the screenshot) |
|---|---|---|
| TSM US (live body) | `NOT_WRITTEN` | `CEO public profile: No CEO profile has been written for this company yet.` |
| TSM US (forced corrupt) | `UNREADABLE_OBJECT` | `CEO public profile: The CEO profile could not be read.` |
| HD US (live body) | `SEARCHED_NOTHING_FOUND` | `CEO public profile (EDWARD P. DECKER): searched, nothing found -- The CEO web search returned 10 url(s), none of them on ir.homedepot.com, so no page could be confirmed as the company's own (a redirect or short link can hide where it leads).` |

The three sentences differ from each other: a never-written profile and a failed read no longer read the same on the page (the defect of row `W518-S2`), and HD US keeps its existing searched sentence.

## 3. Not verified

- The live site opened with a staff login (the harness is the stubbed session; the page's data came from fixtures built from the served bodies, not from the page's own live calls; the identity header did not load in these reads, a property of the stubbed session, as in the first screenshot).
- The third sentence (an unknown or absent reading) on the running page (the harness covers it: T6; its string is present in the served chunk); a painted look beyond the Exec Management tab; names other than TSM US and HD US.
- The fold-back (`DEV..PROD` reads 1 at this stamp: H2 holds step 9 under the CTO's waiver `@3e87382a48`).
