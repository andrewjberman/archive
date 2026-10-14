# NEVER-WIDEN SIGN-OFF -- CTO HALF -- the BD gold ETF classifier: a cash-type sub-asset row serves `cash` (FDRXX)

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~00:4xZ. **Bound to:** packet `deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md`, sha256
`cfc1dd8d01206bad...` (this seat's `sha256sum`, equal to the COO half's), and the COO half `NEVER_WIDEN_FDRXX_CASH_CLASSIFIER_COO_HALF.md` @42f6089b94.
**Origin:** Andrew's smoke 2026-10-13 ("FDRXX should be listed as a "CASH" tagged asset, not Fixed Income"), and his Opal Shape word
(~18:2xZ: one mechanism, regardless of vendor).

## Signed

- **The rule:** one rule, `_row_class`, consumed by four writers (D_04, D_03, C_06 and the silver asset-dim). A canonical row whose
  `sub_asset_class` is `cash` serves `asset_class` `cash`. It is keyed on the row's type, not a ticker list.
- **The effect:** one S3 object; 17 canonical rows move; at least 20 served positions move.
- **The conditions are the COO half's six, as written:** the ledger first; the live bytes `d2e6aa88...` re-read at the apply; the tests at
  the pinned bytes; not during a gold chain run; no full rebuild or manual `--full`; no apply during another open ledger on the BD gold tree.

## The four questions

1. **C_06's one-day discontinuity: ACCEPTED.** Dates written before the release keep `fixed_income` for these rows; dates after read
   `cash`. A full C_06 rebuild rewrites served history, a wider act. It is cut under its own pair only if a page shows the jump to a person.
   The partial rollback for C_06 is accepted as stated.
2. **`CASH_USD` stays `fixed_income` IN THIS PAIR.** It is a cash sweep and belongs in `cash` too, but moving it changes a larger, uncounted
   set. The next round carries it as its own counted pair. This pair does not widen.
3. **NOT enough to close Andrew's smoke item.** His FDRXX was on an Inflection client's Investor Reporting holdings. The packet's
   section 8 does not establish that the IR holdings read this classifier at all. The next round reads the IR holdings' class source for
   FDRXX on that client:
   - if it is a separate copy, the same one rule is applied there under its own pair (one rule, the Opal Shape);
   - the smoke item closes only on that page reading CASH.
4. **The silver blend column's label change (`bd_coarse` in place of `etf_classifier_fallback`): ACCEPTED.** It is a legacy column, and no
   number moves.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** at packet sha256 `cfc1dd8d01206bad...`.

-- 1.0.0_SA_CTO~DELL2
