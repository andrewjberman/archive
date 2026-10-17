# FEATURE RECEIPT -- AMGT-bs-1 (P/E footer census at source)

Serial `0.9.0_WK_AMGT_RESAPP~496`. Order `AMGT_RESAPP.TO-AMGT-bs-1.pe-footer-census-at-source`. Decomposition s.121, round 112.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-pe-footer-census` (nested portal worktree `C:/dev/wk-resapp-496/portal`), cut from PROD `932cea99`.
- Head: `618a39dd` (LOCAL, not pushed). Base: `932cea99`.
- Commits since base: `618a39dd AMGT_RESAPP AMGT-bs-1: P/E footer census harness and producer fixture`.
- Paths changed since `932cea99` (`git diff --name-only 932cea99..HEAD`):
  - `src/pages/SecurityAnalysis/__harness__/peFooterCensus.fixture.json` (new, 289 lines)
  - `src/pages/SecurityAnalysis/__harness__/peFooterCensus.harness.cjs` (new, 245 lines)
- `src/pages/SecurityAnalysis/tabs/ModelTab.tsx` is UNCHANGED (`git diff 932cea99 HEAD -- ModelTab.tsx` is 0 lines). The census found no token the table should name.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: `git diff 932cea99 HEAD -- package.json | wc -l` = 0
- `bun.lock`: `git diff 932cea99 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: `git diff 932cea99 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: `git diff 932cea99 HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build (port 5174 only): `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, names RIO LN and ICT PM, Model tab, Key Figures footer (`P/E not shown: ...`).
- Harness, from the portal root: `node src/pages/SecurityAnalysis/__harness__/peFooterCensus.harness.cjs` prints `PE FOOTER CENSUS HARNESS: YES (5 of 5 checks)`.

## Harness record

- Run 1 on the unedited head, first fixture: `PE FOOTER CENSUS HARNESS: NO (4 of 5 checks)`. C4 failed on 4 list-vs-scan mismatches (S02 to S05). Cause: my transcription of the fixture's `tokens` lists omitted the `IS_EPS` that sits in the shared served prefix `price / reported EPS (IS_EPS)`. The footer itself was not at fault: C2 and C3 passed and the rendered footer printed no token. The fixture lists were corrected to the scan.
- Run 2 on the unedited head, corrected fixture: `PE FOOTER CENSUS HARNESS: YES (5 of 5 checks)`. Footer tokens: `IS_EPS` and `PX_LAST`, both in the `plainPeReason` table. Safety-net-only tokens: none.
- No product edit was made. The branch's only footer tokens are already named in the table.

## Producer census

Producer: `integrations/bloomberg/research/model_block_pull.py`, read at outer checkout HEAD `8bdbdc8a94`. Served side: `lib/research/api/scoped_amgt.py` and `lib/research/checkface/scopes.py`. Fallback reasons: `integrations/bloomberg/research/sa_forecast_fallback.py`. Classifier: `integrations/seekingalpha/detectors.py`, read with `git show HEAD:` because the worktree's sparse checkout does not materialise it.

Denominator: `unresolved.append(` sites read = 8. Entries in `peFooterCensus.fixture.json` = 25 (producer 19, served 6). Reaching the footer = 8 (producer 2, served 6).

| site (model_block_pull.py) | scope | reasons (entry ids) | tokens in text | reaches footer |
|---|---|---|---|---|
| 1390 | forecast, mnemonic null | E01 `raw stamp {raw_stamp} carries no bestdata.json (pulled before C-MODEL-FORECASTS)` | none | no: forecast_reason only |
| 1403 | forecast, mnemonic null | E02 `period end dates not annual: BEST_FPERIOD_OVERRIDE not honoured` (constant at :354) | BEST_FPERIOD_OVERRIDE | no: forecast_reason only |
| 1421 | forecast, mnemonic `{x}` in FORECAST_FIELDS (16, includes BEST_PE_RATIO), FY1-FY3 | E03 `no BEST_PERIOD_END_DATE for this period` | BEST_PERIOD_END_DATE | no: forecast_reason only |
| 1542 | forecast, `{x}`, FY1-FY3 (gap fallback_status passthrough) | E04 `UNRESOLVED: no SA symbol candidate`; E05 `UNRESOLVED: entity test refused {sa_name!r} for {block_name!r}` (unresolved at source: vendor name text); E06 `STOPPED: TRANSPORT_ERROR`; E07 `STOPPED: REHARVEST`; E08 `STOPPED: FAILURE`; E09 `STOPPED: AUTH_FAIL`; E10 `STOPPED: SESSION_ERROR: {e}` (unresolved at source: runtime exception text); E11 `HELD_OFF: SA fallback held off by --no-sa-fallback; gap left unfilled`; E12 `ATTEMPTED-NO-VALUE: meaningful false`; E13 `ATTEMPTED-NO-VALUE: sa field absent` | E06 TRANSPORT_ERROR; E09 AUTH_FAIL; E10 SESSION_ERROR; E11 HELD_OFF; others none | no: forecast_reason only |
| 1674 | header, `{x}` in HEADER_FIELDS | E14 `{header_error}` = `header_errs[mnemonic]` (unresolved at source: the `__field_errors__` value from the refdata pull; test shapes include a dict, so a non-string reason can arrive); E15 `no row carried a readable announcement date ({n} row(s) left out)` (mnemonic ERN_ANN_DT_AND_PER); E16 `empty/no value returned` | none in templates | no: header scope is not read by the footer |
| 1712 | fiscal_year_line_item, mnemonic PE_RATIO (non-anchor-only HIST field) | E17 `not dated at the fiscal period end (non-December FYE, fye_join)` | none | yes: fiscal_unresolved PE_RATIO, printed as `P/E not shown: ...` |
| 1723 | fiscal_year_line_item, mnemonic PE_RATIO | E18 `empty/no value returned` | none | yes: fiscal_unresolved PE_RATIO |
| 1753 | fiscal_year_line_item, mnemonic null (excluded fiscal year) | E19 `fiscal year not closed/reported: no statement field in the merged group` | none | no: mnemonic null, and the footer reads PE_RATIO only |

Served-side footer reasons (second source, `reaches_footer` yes): S01 to S05 at `scoped_amgt.py` 2754-2764 (fiscal `pe_withheld`, carried in `fiscal_unresolved` at 5803-5807), each with the shared prefix `price / reported EPS (IS_EPS), FY{year}, is not shown:`; S06 at 2806 (`forecast_withheld`, BEST_PE_RATIO, estimate year).

### Tokens

- Tokens on reaching entries (footer): `IS_EPS` (table: `reported earnings per share`), `PX_LAST` (table: `share price`). Safety-net-only tokens on reaching entries: none.
- Tokens on producer entries that do NOT reach the footer: BEST_FPERIOD_OVERRIDE, BEST_PERIOD_END_DATE, TRANSPORT_ERROR, AUTH_FAIL, SESSION_ERROR, HELD_OFF. They route to `forecast_reason` or to header scope, which the footer never reads.
- Safety net: any of these would print `a vendor figure` if it ever reached the footer. The control `FOO_BAR` in C4 shows the net works.

### Routing finding

The footer reads two keys only. Historical years read `fiscal_unresolved` (PE_RATIO). Estimate years read `forecast_withheld`, and only the served `_derive_forward_pe` writes that key. The producer's estimate-year reasons (E03, E04 to E13 at FY1 to FY3) go to `forecast_reason` (`scoped_amgt.py` 5785-5798), which the footer does not read. So no producer estimate-year reason prints. Recorded as an OBSERVATION row (`AMGT_RESAPP-D1-W496-S2`).

## Recorded

- AC1: `PE FOOTER CENSUS HARNESS: YES (5 of 5 checks)`, exit 0.
- AC2: `R103 FEATURE GREEN: YES (typecheck rc 0, lint rc 0, harness 29 of 33 pass, base 25 of 32, regressions 0, pre-existing: assembled.harness.cjs exportCompare.harness.cjs peersCurrency.harness.cjs timelineFourStates.harness.cjs)`, exit 0.
