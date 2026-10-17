# AMGT_RESAPP round 112 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~20:3xZ; every order cut in round 112 is terminal (`bs-1`, `bs-2`, `bs-5` complete; `bs-3` and `bs-4` are the issuer's reads).** Round 112 is the CTO's round-111 analysis (`ledger/ROUND_ANALYSIS.round111.md`, msg 7711), issued at `8bdbdc8a94` under this seat's keys (decomposition s.121). `python .tools/round-close-check.py --project AMGT_RESAPP --round 112` reads `judgment=0 graded=0 ungraded=0 verdict=MAY-CLOSE`: the round carries NO judgment criterion, so no L9 grade is owed; the packet is the L8 compile and the ground for your L10 slug. Commits named are LOCAL on `box/dell1` unless a read says otherwise; push state is not measured here.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bs-1` | the producer of the stored model-block `unresolved` rows read at source; every token listed; the footer proven plain for each (W494-S1) | complete | worker ~496 at 3d1fccf474 (merged c6a2c69697); candidate `cand/dell1/amgt-sa-pe-footer-census` @618a39dd5f: a census fixture and a rendered-footer harness, NO product file; the issuer's re-run in a FRESH checkout `YES (5 of 5)`; 8 of 8 `unresolved.append(` sites, 25 entries, 8 reach the footer, distinct tokens on them `IS_EPS` and `PX_LAST` only (both already in the table, none safety-net-only); row 48c7; DEV `43827a50` only (the CTO: DEV and not the promote) |
| `AMGT-bs-2` | ONE price-currency helper read by the header tiles and the Peers table (W495-S2), plus the round-111 Peers harness's CRLF defect | complete | worker ~497 at 33dad39edb (merged 0a56033117); candidate `cand/dell1/amgt-sa-price-currency-rule` @937f15a01d (`priceCurrency.ts` new, `HeaderCards.tsx`, `PeersTab.tsx`, two harness files); the issuer's re-runs in a FRESH checkout: `PRICE CURRENCY RULE HARNESS YES (6 of 6)` and `PEERS CURRENCY HARNESS YES (6 of 6)` (K5 failed on the unedited head in such a checkout: git writes CRLF, row S58); row 32d8; DEV `9fa63689` |
| `AMGT-bs-3` | the 12 close-walk findings triaged by class | issuer read, done | `round112/WALK_FINDINGS_TRIAGE.md` @4ca13af51b: 12 findings, 8 classes, all present in round 110's walks; seven classes recorded in one row S59, no cell; `unconnected-field` belongs to the AIFILL workstream |
| `AMGT-bs-4` | the earnings row read on PROD `932cea99` and the live byte tie (W491-S2) | issuer read, done | `round112/EARNINGS_ROW_READ.md` @4ca13af51b: the row reads `2026-10-13 (2026:Q3), 135 entries` before and `136 entries` after in RIO LN's Oct 14 to Oct 17 pair, no raw JSON; the instrument that fired on the pre-fix candidate is silent; the byte tie `round111/LIVE_TIE_932CEA99.md` @b39f7d6e89 |
| `AMGT-bs-5` | the chosen-set PROD promote and the fold-back | complete | H2: PROD `932cea99` to `856fb37b` (ONE feature), CI run 39064168223 success, tag `portal-v2.1.237`; fold-back under the CTO's one-time named waiver (@9e98635af9, 116 shas, row f793): DEV `61664837e8ac` (issuer's fetch and `ls-remote` read), DEV tree unchanged, `origin/DEV..origin/PROD` = 0; AC1-AC4 PASS |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` @7bec5b4251 |

## 2. The issuer's real runs

- **Live site tied to PROD `856fb37b` by bytes** (`round112/LIVE_TIE_856FB37B.md` @4dbf2563c8): live `index.html`, the six entry assets and the Security Analysis chunk `index-Xr7bGoAp.js` (249963 bytes) byte-equal to run 39064168223's artifact; the previous deploy's chunk (`index-CZ3eT7d6.js`, 250068 bytes) differs.
- **Close walk on a local build of PROD `856fb37b`** over RIO LN, ICT PM and GOOGL US (every `Full figures` detail open, a throwaway walker copy with its cap raised, deleted; walker disarmed, build torn down; evidence `C:/dev/ui-walk-evidence/r112-close/`): 12 findings in the SAME 8 classes and the SAME counts as round 111's close walk (3 `timeline:no-event-element`, 2 `unconnected-field`, 2 `layout:clipped`, one each of `walker:control-missing`, `layout:truncated`, `timeline:no-day-bar`, `occluded-popover`, `format:dates`); **0 `raw-code` and 0 `format:money`**. So the round-112 change moved no walked state. (The cell's own case, a name whose `PX_LAST` has no currency and whose `CRNCY` is served, exists in no walked name; the harness fixture is its grade.)
- **The round-111 drain's mistake, corrected:** my round-111 re-run of the Peers harness passed in the worker's own worktree and the harness failed on any fresh checkout (CRLF). Every round-112 re-run was in a fresh checkout.

## 3. Findings for your judgment (read, none graded by the issuer)

1. **`W497-S2` (carried to round 113 as a row by the CTO):** the shared helper returns the header's UNTRIMMED currency code where the old Peers helper trimmed it; a whitespace-padded served currency reaches the Peers cells as served. No committed fixture carries one; unmeasured on live bodies. Ruling kept (the order said EXACTLY the header's rule).
2. **`W497-S1` / `W496-S1`** (worker rows): the schema file named by the order is absent from a sparse worktree; the SeekingAlpha classifier was outside the census cell's sparse checkout and was read with `git show`. INERT.
3. **`W495-S1` ruled not a defect:** the served peer body for the GOOGL US member SPCX states its price currency is unknown (`price_currency_reason`); the words `currency not stated` are the served truth and the cell is asserted unchanged (R6).
4. **Row `S59`** (the triage): seven walker classes recur unchanged; `format:dates` (the earnings row's ISO date beside long-form dates) and `occluded-popover` are round-113 cell candidates if the CTO wants them; FWD-5 and FWD-6 grades are the CTO's to read.

**Not verified by the issuer:** a content-level marker of the shared-helper change in the served chunk (it adds no string); the live pages read with a staff login; the earnings row's own `Full figures` detail opened on a live page; ICT PM's earnings row looked at in a shot; any live name with a `PX_LAST` that lacks a currency.

## 4. Open and carried

- Round 113 (the CTO's analysis): the padded-currency row, S59's candidates.
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew); row `S57` (the fold-back verb) is the portal manager's (NFRA_DEVPLN), and every fold-back waits on a named waiver until it exists.
