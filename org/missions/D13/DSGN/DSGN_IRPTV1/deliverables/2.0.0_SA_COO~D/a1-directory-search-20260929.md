# W23 / A1 -- one signed-in directory search through the page (2026-09-29 15:18Z-15:25Z)

**Walker:** 2.0.0_SA_COO~D. **Packet:** `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/NEVER_WIDEN_SIGNOFF_PACKET_UI_WALK_W23_20260929.md`
blob 033aeb0362 (halves CTO 102861, CRO 102862), opened by 2.0.0_SA_COO~P at 15:17:35Z (102864). **Ledger:**
`irpt-directory-entry-account-masks-20260929`, leg A1. **Principal:** irpt-uiwalk-1790695048; the credential was read by name
from SSM into browser memory only and never printed.

## Build (CTO condition)

| read | value |
|---|---|
| portal commit | `18899c96748e171f635c4a5955cfdcd24040c273` (DEV) |
| portal tree | `8b18dbb79cc6f1ef81522840dc8414467d2f568b` -- identical to origin PROD `9a8f6c71`'s tree |
| tracked changes at the walk | 0 |
| server | `bun run dev:live --port 5174` (the deployed data/auth front door), main portal checkout |

## Byte-proof

| check | value |
|---|---|
| sign-in | 15:18:47.390Z -> /market; ~P told for credoff at 15:19:36Z |
| HAR | `a1-20260929.har` (this folder; `*.har` is gitignored -- read in place), sha256 `85523f3d9896dd17...`, 711 entries, scrubbed in-stream |
| leak check | password false, JWT false, bearer false |
| writes in the HAR | login 1, refresh 6, directory/resolve 5; nothing else (no export, no analysis, no selection) |
| guard blocks | 66, all `POST /prod/analytics/ingest` (the page beacon) |
| driver | `.runtmp/walk/owner-a1.mjs` = W21's guard with the one export admit removed; step `.runtmp/walk/a1-search.mjs` |

## The directory reads (from the HAR)

Every directory call was a GET to `/api/scoped/investor-reporting/directory/browse` (the page's search route) and answered
200. Each response's entries carry ONE field set: `access, cohort, display_name, ids, masked_discriminator,
permitted_capabilities, permitted_scope, revision, termination`. **`account_masks` is absent from every entry (0 of 800).**

| time (UTC) | firm | query | status | entries | carry account_masks |
|---|---|---|---|---|---|
| 15:20:52.476Z | 49financial | (none) | 200 | 100 | 0 |
| 15:20:52.478Z | cottonwood | (none) | 200 | 100 | 0 |
| 15:20:52.478Z | inflection | (none) | 200 | 100 | 0 |
| 15:23:35.670Z | 49financial | (none) | 200 | 100 | 0 |
| 15:23:35.671Z | cottonwood | (none) | 200 | 100 | 0 |
| 15:23:35.674Z | inflection | (none) | 200 | 100 | 0 |
| 15:23:40.924Z | 49financial | (none) | 200 | 100 | 0 |
| **15:23:43.387Z** | **49financial** | **`an`** | **200** | **100** | **0** |

**The A1 search is the last row:** one typed search on one firm (the first firm the Firm control offers after Global),
answered 200 at 15:23:43.387Z, 100 entries, the nine-field set above, `account_masks` absent. The page showed 100 options.

**Stated, not hidden:** the walk made more directory reads than the one search. Each page load under Global reads one
page per firm. That happened twice: at 15:20:52Z my first step errored on the Firm control, a native select, after the
page loaded and before any typing, and I re-ran it at 15:23:35Z. The firm pick added one untyped read at 15:23:40Z. All
of these are the same read-only GET the search makes, and each is a row above.
