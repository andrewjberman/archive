# DSGN_AMGTV1 round 65 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~12:4xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round64.md` @3f30e42354 section 2: item 1 is AV-zzq-1; item 2 is AMGT_RESAPP jj-1's, not patched here |
| issuance | @c738ff1b78, fan-out 1 of 1, LF only |
| order | `TO-AV-zzq-1` -> ~140 (worker-light), drained @2a707f53f7; instance VALID |
| checks on both candidates | r62 6/6, r63a 3/3, r63b 5/5, r63c 5/5, r64a 4/4, r65 4/4; battery29 ALL PASS |
| DEV | candidate `2726bbe7` = origin DEV `686ced10` + `1fc854af` (`cand/dsgn-amgtv1-r65-dev`) |
| PROD | candidate `18364342` = PROD `c6c1eb2a` (portal-v2.1.209, rounds 63+64 live, msg 2431) + `1fc854af` (`cand/prod-dsgn-r65`); 0 files outside `src/pages/SecurityAnalysis/`; the SA tree equals the DEV candidate's. No PROD half is asked until the CVO grades AV-zzq-1. |
| rows | none. A worker note: proof-of-spec-check reads an `<expect>` as a regex, so "(0 skipped)" fails as written; ~140 recorded `BATTERY29: ALL PASS`, and the recorded output keeps "(0 skipped)". |

## The real run -- 12:43Z-12:46Z, `tmp/ui-walk/20261009T124316Z`, signed-in `dev:live` build of `2726bbe7`

`--security "ASML_NA_Equity" --window-press "[data-sentence-press]"`: 36 screenshots, 0 API issues, 0 guard aborts. The walker
disarmed and its login is refused (401).

| criterion | shot | what it shows |
|---|---|---|
| `TO-AV-zzq-1` AC3 | **007** (Investment-thesis window) | "COMPANY DESCRIPTION" shows once, as the heading. The served text under it begins "What started as a failing joint venture between ASM International and Philips..." with no repeated label. "FROM THE FILING" and the Item 5 lines follow, as in round 64. The missing space in "supply chain.ASML" is the producer's (AMGT_RESAPP jj-1), left as served. |

## Carried

- `round64/PREP.md`:
  - item 1, the MACHINE chip on its own line;
  - item 2, nothing tying an event title to its marker;
  - item 3, the picker's "type the ticker" words.
- **FWD-1:** Andrew's own signed-in walk on PROD. PROD now carries rounds 58-64 (`c6c1eb2a`).

## After the close (12:5xZ)

- **L9:** AV-zzq-1 MET (round-65 analysis @287424bb47). There is no round-66 list; the page's open items are closed.
- **Live:** portal DEV `2726bbe7` and PROD `18364342` (ls-remote read 12:57Z). PROD now carries rounds 58-65. The pair is CTO @287424bb47
  and COO @b4e5890be8.
- **Remaining outcome:** FWD-1, Andrew's own signed-in walk on PROD (open call `dell1-20261009T092027Z-2caa`, OPEN). Its text still
  names the earlier build `fa5ba2af`; PROD has since moved to `18364342`.
