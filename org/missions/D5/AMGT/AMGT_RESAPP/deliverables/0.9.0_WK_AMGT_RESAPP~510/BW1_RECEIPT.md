# AMGT-bw-1 receipt -- the pack labels a money figure with the figure's own currency

Worker `0.9.0_WK_AMGT_RESAPP~510`, order `AMGT_RESAPP.TO-AMGT-bw-1.pack-currency-labels-from-the-figures-own-currency`,
issued by `2.0.0_SA_COO~R1`. Base `52a137e363` (the issuance commit). Branch `wk-AMGT_RESAPP-510`, local only. Offline:
no store, no deploy, no vendor, no model call, no push. The nested `portal` worktree was read only.

**Outcome in one line:** the labels now follow each figure's own served `currency`; the order's C1 and C2 alias clauses
are NOT met, because the existing same-value dedup drops the CRNCY_ADJ_MKT_CAP line once it prints the same code as
CUR_MKT_CAP (surprise row `AMGT_RESAPP-D1-W510-S1`, BLOCKING). The order stays open.

## Premise check (re-grounded at the base)

- The mechanism holds: `build_pack` reads `trading_cur` and `reporting_cur` once (`render_pack.py` base lines 766-767) and
  every money line used one of them. The page's rule is `StatTile.tsx` `formatStatValue` / `HeaderCards.tsx` `resolveFigure`
  with `priceCurrency.ts` `currencyCodeOf`: each figure's own `currency` key (`scoped_amgt.py` reads the same key:
  `fig.get("currency")`).
- The page's words for a valued money amount with no currency are `"<amount> currency not stated"` (`StatTile.tsx`
  `moneyNoCode`). The order names `CURRENCY_UNCONFIRMED_WORDS`; that constant is the tile's reason only for an UNMEASURED
  `currency_basis`, and that path withholds the amount. The pack uses the amount-level words (row `AMGT_RESAPP-D1-W510-S2`).
- Base output reproduces the order's table: ICT PM `Market cap: PHP 1,735,465.1 million`,
  `Market value, currency-adjusted: USD 1,735,465.1 million`; RIO LN `Market cap: GBp 115,578.9 million`.

## Currency census

Method: every function on the path from `build_pack` to a printed line was read at base (22 functions); each money or
currency site was classified. Machine copy: `lib/research/print/tests/fixtures/bw1_currency_fields.json`. Line numbers
are BASE lines. The `status` column is the state after the edit; the base reading is in the fixture's `status_at_base`.

Denominator: 22 functions read, 20 census entries, 10 entries bypassing the own currency at base.

| id | function (base line) | mnemonic or field | prints today, and how chosen | own served currency | disposition |
|---|---|---|---|---|---|
| BW1-C01 | _format_figure_value (504) | any figure with unit MILLIONS (e.g. CURR_ENTP_VAL, CRNCY_ADJ_MKT_CAP, NET_DEBT, HISTORICAL_MARKET_CAP, SALES_REV_TURN) | EQY_FUND_CRNCY (reporting_cur, else CRNCY) chosen by build_pack; not the figure's own code | the figure's served `currency` (present on served figures; ICT PM CURR_ENTP_VAL USD; RIO LN CURR_ENTP_VAL none) | fixed_here |
| BW1-C02 | _format_figure_value (510) | any figure with unit PRICE (PX_LAST) | CRNCY (trading_cur, else EQY_FUND_CRNCY) chosen by build_pack | the figure's served `currency` (ICT PM PX_LAST PHP; RIO LN PX_LAST GBp; GOOGL US has no PX_LAST row) | fixed_here |
| BW1-C03 | _format_figure_value (512) | any figure with unit PER SHARE (IS_EPS, BEST_EPS, BEST_DPS and the fiscal per-share rows) | EQY_FUND_CRNCY (reporting_cur, else CRNCY) | the figure's served `currency` (fiscal and forecast rows carry it on served data; the bw-1 fixtures carry none on them) | fixed_here |
| BW1-C04 | _format_figure_value (514) | any figure with unit ABSOLUTE (full currency units) (CUR_MKT_CAP) | CRNCY (trading_cur, else EQY_FUND_CRNCY) | the figure's served `currency` (ICT PM PHP; RIO LN none; GOOGL US USD) | fixed_here |
| BW1-C05 | _money (454) | the empty-code branch of every money line | the words 'local currency' when neither CRNCY nor EQY_FUND_CRNCY is present | none (this is the branch a figure with no own code reaches) | no_own_currency |
| BW1-C06 | _header_figures_for_print (640) | CRNCY_ADJ_MKT_CAP kept as a second market cap line | label 'Market value, currency-adjusted' on every kept alias, whatever the conversion; value by BW1-C01 or BW1-C03 rules | the alias's own served currency (ICT PM PHP; RIO LN none; GOOGL US USD) | fixed_here |
| BW1-C07 | _header_figures_for_print (636) | the dedup comparison of CRNCY_ADJ_MKT_CAP against CUR_MKT_CAP (compares printed strings) | no currency printed by the comparison itself | n/a | not_money |
| BW1-C08 | build_pack (766) | trading_cur = _currency_of(header_figs, CRNCY, EQY_FUND_CRNCY) | passed into every money line as the code for PRICE, ABSOLUTE and the empty-code branch | n/a (a block-level read of two text fields) | fixed_here |
| BW1-C09 | build_pack (767) | reporting_cur = _currency_of(header_figs, EQY_FUND_CRNCY, CRNCY) | passed into every money line as the code for MILLIONS and PER SHARE | n/a (a block-level read of two text fields) | fixed_here |
| BW1-C10 | build_pack (768) | every header figure line (_header_print_lines) | via BW1-C01 to BW1-C06 | per figure | fixed_here |
| BW1-C11 | build_pack (774) | every fiscal-year figure line (_plain_figure_line) | via BW1-C01 to BW1-C05 | per figure | fixed_here |
| BW1-C12 | build_pack (788) | the company description figure via _description_line (CIE_DES_BULK or CIE_DES) | none (a text figure) | none | not_money |
| BW1-C13 | _plain_figure_line (561) | the head of every figure line (value from _format_figure_value, then the raw value replaced by it) | passes through BW1-C01 to BW1-C05; adds no code of its own | n/a | not_money |
| BW1-C14 | _plain_label (410) | the label of a kept alias (_print_label) | 'Market value, currency-adjusted' is read from _print_label | n/a | not_money |
| BW1-C15 | build_pack (768) | the header text field CRNCY, printed as 'Currency: <value>' (plain label 'Currency') | the served text value (e.g. PHP) as written | none (the code IS the value of this text field) | not_money |
| BW1-C16 | build_pack (768) | the header text field EQY_FUND_CRNCY, printed as 'Reporting currency: <value>' | the served text value (e.g. USD) as written | none (the code IS the value of this text field) | not_money |
| BW1-C17 | _format_figure_value (496) | MILLIONS (share count), ABSOLUTE (share count), PERCENT, RATIO, TEXT, DATE, yes/no, lists, not-reported and unit-not-measured figures (branches at lines 496-497, 501-502, 505-508, 515-517) | no currency printed | n/a | not_money |
| BW1-C18 | _print_drafted (681) | served drafted sentences (recommendation, thesis, risks), printed as written, and verbatim quotations | a '$' or currency word inside served prose, as the sentence itself wrote it | the sentence's own words; no figure carries it | not_money |
| BW1-C19 | build_pack (794) | served company-description sentences ('Filed detail') printed as written | as the sentence wrote it | the sentence's own words | not_money |
| BW1-C20 | render_figure_line (lib/research/provenance/render_print.py, read only) (244) | the unit text of a figure ('PRICE (local trading currency, per share/unit)'), printed inside the rich export and as the head source of every pack line | no currency code: the unit text names the currency concept in words only | n/a | not_money |

Dispositions: `own_currency` (already right) is not used, because no money site was right at base; `fixed_here` nine
entries; `no_own_currency` one entry (BW1-C05, the words); `not_money` ten entries. Total 20.

## What changed

Against base `52a137e363` (line counts from `git diff --numstat`; new files from `wc -l`):

| path | change |
|---|---|
| `lib/research/print/render_pack.py` | 43 added, 11 removed. Currency-labelling only: `NO_CURRENCY_WORDS`, `_own_currency`, `_money`, the four money branches of `_format_figure_value`, `_CONVERTED_LABEL`, `_converted`, the alias label in `_header_figures_for_print`. `build_pack`, the dedup and the call shape are unchanged. |
| `lib/research/print/tests/test_bw1_currency_labels.py` | new, 187 lines: C1 to C7 by name, plus C8 (a converted alias). |
| `lib/research/print/tests/fixtures/bw1_header_figures.json` | new, 39 lines: SYNTHETIC header figures for ICT PM, RIO LN and GOOGL US, carrying the order's currency, value and unit facts. |
| `lib/research/print/tests/fixtures/bw1_pack_text_base_ICT_PM.txt` | new, 21 lines: base text, recorded from the unedited renderer. |
| `lib/research/print/tests/fixtures/bw1_pack_text_base_RIO_LN.txt` | new, 21 lines: base text, from the unedited renderer. |
| `lib/research/print/tests/fixtures/bw1_pack_text_base_GOOGL_US.txt` | new, 17 lines: base text, from the unedited renderer (control). |
| `lib/research/print/tests/fixtures/bw1_currency_fields.json` | new, 408 lines: the census (20 entries, 22 functions). |
| `lib/research/print/tests/fixtures/bu3_block_ICT_PM.json` | 6 lines changed: `currency` added to the six money figures, with the code the base printed (`GBP`). No value changed. |
| `lib/research/print/tests/fixtures/bu3_block_RIO_LN.json` | 4 lines changed: `currency` added to the four money figures (`GBp`). No value changed. |
| `lib/research/print/tests/test_aw2_print_as_document.py` | 24 added, 15 removed. Helpers take an optional `currency`; the money fixtures carry their own code; `test_currency_comes_from_the_block_trading_for_price_reporting_for_millions` is rewritten to assert the rule (own code wins; no code gives the words). |
| `lib/research/print/tests/test_ax4_brand_form.py` | 16 added, 10 removed. `_fig` takes an optional `currency`; the market-cap and money figures carry `USD`. `test_a_second_market_cap_with_a_different_value_stays_under_its_own_name` now expects `Market capitalisation: USD 100,000.0 million` and no "currency-adjusted", because both figures are USD and no conversion happened. |
| `lib/research/print/tests/test_bu3_pack_long_dates.py` | 2 lines changed: T5's two inline figures carry `currency` (`USD`, `GBP`). Expectations unchanged. |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | 104 lines added: four rows, `AMGT_RESAPP-D1-W510-S1` to `-S4`. |
| `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~510/` | this receipt, the proof instance and the session log. |

Existing tests changed: `test_aw2_print_as_document.py`, `test_ax4_brand_form.py`, `test_bu3_pack_long_dates.py` (T5). Each
expectation that encoded the removed fallback now asserts the rule; the reason is the rule itself. T6 and the bv2 control
(Q4, which runs T6) pass again through the fixture change. `test_av2_export_equals_page.py` is NOT changed: it already
fails at base on line 175 (row `AMGT_RESAPP-D1-W510-S4`).

## Test runs

Base run, unedited head `52a137e363`, new file (`.scratch/bw1_run_base.txt`):
`9 failed, 2 passed in 5.47s`. Passed: C3, and C4 for GOOGL_US. Failed: C1, C2, C4 (ICT_PM, RIO_LN), C5, C6, C8, and C7
(ICT_PM, RIO_LN). The C7 failures were my own vacuous assertion ("the edit changes money lines"), which fails on an unedited
head by construction; I removed it before the edit. C7 is otherwise unchanged.

Mutant control, the FINAL test file against the unedited base bytes of `render_pack.py` (read from `52a137e363`, run, then
restored from HEAD and compared): `6 failed, 5 passed`. Failed: C1, C2, C4 (ICT_PM), C4 (RIO_LN), C5, C8. Passed: C3, C4
(GOOGL_US), C6, C7 (ICT_PM), C7 (RIO_LN). C6 passes on base because it reads the census fixture, not the product; it is a
fixture check, not a product check.

Determinism: the new file was run three times on the edited head (after the edit, after the commit, and the final AC1 run),
each giving `2 failed, 9 passed`, with the same two failing tests.

Full print suite at base: `1 failed, 125 passed` (the av2 test; matches the order).

Full print suite after the edit (`.scratch/edit_run2.txt`): `3 failed, 134 passed`. The three FAILED lines:
- `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` (pre-existing, same line 175);
- `test_bw1_currency_labels.py::test_C1_ict_pm_each_figure_prints_its_own_code`: `assert 1 == 2` on the alias count;
- `test_bw1_currency_labels.py::test_C2_rio_ln_figures_without_a_code_print_the_words_not_a_code`: `assert 1 == 2` on the alias count.

Every other C1 and C2 clause passes: no `currency-adjusted` wording, no `USD` on the ICT PM market-value line, `PHP 1,735,465.1 million`
on the market cap, `USD 33,087.5 million` enterprise value, `PHP 860.00 per share`; for RIO LN no `GBp` or `USD` on the
market cap, `115,578.9 million currency not stated`, `173,616.0 million currency not stated`, `GBp 6,816.00 per share`.

## Dedup finding (the reason C1 and C2 are not met)

The alias line is dropped by the existing AMGT-ax-4 rule: a second market-cap line whose printed value equals the first's
is skipped. After the own-currency fix:

- ICT PM: CUR_MKT_CAP prints `PHP 1,735,465.1 million`, and CRNCY_ADJ_MKT_CAP prints the same string, so it is dropped.
- RIO LN: both print `115,578.9 million currency not stated`, so it is dropped.
- GOOGL US (the control, C3): both print `USD 4,143,539.9 million`, so the base already drops it.

C3 requires the GOOGL US text unchanged, so the same dedup must stay. The order's C1 and C2 require the alias printed for
ICT PM and RIO LN. No rule separates those cases from GOOGL US. The dedup is not changed here (outside the labelling
functions). The CVO or CTO must rule: keep the dedup and amend C1 and C2, or keep the alias and amend C3.

## What the rich export does

`format=rich` is `build_rich_text`. It prints every figure through `render_figure_line` (`_figures_table`, the RENDERED column,
verbatim). `render_figure_line` (`lib/research/provenance/render_print.py`, read only) prints `<value> <unit text> · <mnemonic>
(<definition>) · as of <vintage> · <source>`. It names no currency code, so it cannot label a figure with a wrong currency: a
PRICE row reads `6816.0 PRICE (local trading currency, per share/unit) · PX_LAST ...`. The rich export is therefore not
changed by this cell.

Model cases: `_model_case_line` / `_model_cases_markdown` (`render_pack.py` lines 1341 and 1373) label a case's value with the
block's CRNCY through `_case_currency`, which mirrors the page's `caseCurrency` rule (`ModelTab.tsx`). Nothing in
`render_pack.py` calls `_model_cases_markdown` (the only occurrence is its definition), so `build_rich_text` does not reach it
in this file. Not edited.

## Not verified

- The deployed Lambda serves the old renderer until the round-116 redeploy (`AMGT-bw-5`). No live pack was looked at here.
- The UNMEASURED `currency_basis` path (the page withholds the amount and shows `CURRENCY_UNCONFIRMED_WORDS`) is not mirrored
  (row `AMGT_RESAPP-D1-W510-S2`).
- The alias rule for a converted figure is covered by C8 with a synthetic EUR figure; no served converted figure was examined.
- `test_av2_export_equals_page.py` was not repaired (row `AMGT_RESAPP-D1-W510-S4`).
- The portal was not edited, and no portal test was run.
- Pre-commit risk reflex (HOLD on `render_pack.py`, comp-pulse): it cites the AMGT rs-2 redeploy record
  `org/critical_paths/change_management/20260926T0935Z_amgt-rs-2-the-redeploy_deploy_completion.md` (closed 20260926T125100Z).
  That record pins the deployed `render_pack.py` to the bytes of `a631ba6249`, and its L1 requires a closure diff at build-only
  against the deployed build input before any upload. This commit deploys nothing and changes no deployed byte; the redeploy
  (`AMGT-bw-5`) must carry that closure diff. The commit proceeded (all gates clean; the reflex is advisory).
- The pre-commit gate printed `WARN: [one-writer]` for the investigation file: it is the unsuffixed laptop file, written
  from dell1. The order names this path, so the rows went to it; per-box splitting is the channel owner's call.

## Surprise rows filed

| id | class | one line |
|---|---|---|
| `AMGT_RESAPP-D1-W510-S1` | BLOCKING, INERT | C1 and C2 alias clauses conflict with C3 under the existing dedup (see above). |
| `AMGT_RESAPP-D1-W510-S2` | OBSERVATION, INERT | The page's words for a valued amount with no currency are `currency not stated`; `CURRENCY_UNCONFIRMED_WORDS` is the UNMEASURED-only reason. |
| `AMGT_RESAPP-D1-W510-S3` | OBSERVATION, INERT | The bu3 block fixtures carried no per-figure `currency`; the base codes came from the fallback. `currency` added, values unchanged. |
| `AMGT_RESAPP-D1-W510-S4` | OBSERVATION, INERT | `test_av2` fails at base on line 175 for a date-stripping reason; its later `local currency` lines encode the removed fallback. Untouched. |
