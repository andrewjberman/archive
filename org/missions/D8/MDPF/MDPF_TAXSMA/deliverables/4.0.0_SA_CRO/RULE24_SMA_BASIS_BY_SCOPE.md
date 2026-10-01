# Rule 24 record -- `SMA_BASIS_BY_SCOPE` (the SMA source basis, declared per firm where it differs)

**Author:** 4.0.0_SA_CRO (Chief Research Officer), under the MDPF_TAXSMA FAST lease
**Schema changed:** `data/mdpf/scripts/gold/mdpf_category_registry.py` -- new map `SMA_BASIS_BY_SCOPE`,
`sma_basis_of(member_id, scope=None)`
**Authority:** `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261001_033xZ_TAXSMA_TAX_PORTFOLIOS_ARE_SMAS_NOT_MODELS_SMA_CATEGORY.md`
**State:** CANDIDATE, not deployed. No value is added to the enum; the two values `carve_out` and `additive` stand.

## What changed

The basis of an SMA member was one value per member. It is now one value per (member, firm), stored as the
member's own value plus a row only where a firm differs. One row exists: `("tax", "cottonwood") -> carve_out`.

## The four postulates

**(i) MECE over a declared domain.** Domain: 6 SMA members x 4 scopes (49financial, cottonwood, inflection,
global) = 24 cells. Each cell resolves to exactly one of 2 values: the scope's row if one exists, else the member's
own value. By subtraction: 24 cells - 1 row - 23 cells on the member's own value = 0 uncovered. The import check
refuses a row naming a non-member or a value outside the enum.
Measured cells: 5 of 24 (divz, pfoe and tax at 49financial; tax at cottonwood; tax at global). The other 19 carry
no dollars today and are UNVERIFIED, as the registry already says of muni, idvz and pfde.

**(ii) Same grain.** Every row of the new map is at the (member, firm) grain. The member's own value is the same
fact read at every firm with no row. One caller grain is left on purpose: `taxsma_assets.check_sma_basis` and
`dim_mdpf_aggregate_aua_timeseries._tax_source_basis_or_raise` call `sma_basis_of("tax")` with no scope, because
they guard the ADDITIVE fold, which exists at 49financial and global only. Call sites in `data/mdpf/scripts`: 4;
scoped 2 (`_shape_category_views`, `_taxsma_by_model_entry`), unscoped 2 (the two guards named here).

**(iii) Intent coherence.** One axis, one intent, unchanged: does the member's money already sit inside the pool
the firm total is built from. At cottonwood that pool is the Black Diamond custody total, and both Tax accounts
are inside it (2 of 2 in `fact_holdings` 2026-09-29, 6,049,368.78). At 49financial the pool is the 0824 master and
the Tax accounts are outside it. Global holds none of Cottonwood's non-model money, so the member is additive there.

**(iv) State coherence.** A firm's accounts moving custodian changes that firm's row only. It does not move the
member's own value, another firm's row, or Global's. Adding dollars, a strategy id or a bucket moves no cell.

## What the row does on real data (one run, zero writes, valuation 2026-09-29)

| Cottonwood tree | Before | After |
|---|---|---|
| Models | 179,028,486.19 | 179,028,486.19 |
| SMA (ALT Strategies, Tax-Managed SMA) | 0.00 | 6,049,368.78 |
| Client | 362,884,540.60 | 356,835,171.82 |
| Total | 541,913,026.79 | 541,913,026.79 |

Negative arm (unit test): the same entry carrying `additive` at cottonwood is refused by the tree's own
two-declarations check.

## Not measured

Whether Cottonwood's `Client > Opal Supervised` figure (produced by `build_cottonwood_mdpf_pair`) already counts
the two Tax accounts. The carve-out lowers Client, so the Unsupervised leg, which is the complement, drops by the
Tax dollars. Owner: this lane, before activation.
