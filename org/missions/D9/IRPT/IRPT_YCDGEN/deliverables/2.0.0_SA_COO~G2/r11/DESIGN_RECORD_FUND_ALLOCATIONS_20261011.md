# IRPT_YCDGEN round 11, cell YCD-g-11 -- design record: a fund's sector and country as WEIGHTS (no build)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, on the CTO round-11 analysis @457305b604 section 4 item 7. **For:**
`1.0.0_SA_CTO~DELL2`, who rules it. Nothing is built, pulled or changed by this record.

## 1. The gap

The Opal Overview's sector and region figures are computed by `ycharts/research/held_data.py`. Every rule today is a
LABEL SHARE (`_build_rules`, lines 114-133): a holding is placed WHOLE in one GICS sector (`GICS_SECTOR_NAME`) and whole in
its country of domicile (`CNTRY_OF_DOMICILE`), amount-weighted, renormalized over the holdings that carry the label.

A fund has no one sector. Measured in round 10 on the store's 172 rows
(`../r10/STORE_BY_KIND_AND_THE_ONE_ACCOUNT_20261011.md` @804449eb87): the 8 rows that carry a fund column carry a country
and NO sector; and the country they carry is the fund's domicile, not where its holdings are. So today a fund is left out of
every sector figure, and would be stated wholly in its home country in every region figure.

## 2. What the source serves for a fund

`integrations/bloomberg/READ_HERE.md` section 4 (lines 115-120): on an ETF ticker a plain reference request serves
`HB_INDUSTRY_SECTOR_ALLOCATION` (sector weights) and `HB_GEO_CNTRY_ALLOC`. `integrations/bloomberg/pipeline/etf_constituents_pull.py`
lines 69-72 already pulls both, as `sector_allocation` (`sector_name`, `pct_of_fund`) and `geo_allocation` (`region`,
`pct_of_fund`), for the four Opal funds (line 62).

**CURRENT-DAY ONLY** (READ_HERE.md lines 152-155): a historical request returns no rows for these fields; there is no
backfill; a day not captured is gone. So a report can state a fund's allocation only as of a day the pull ran for that fund.

NOT read here: the label vocabulary those two fields return (whether `sector_name` uses the 11 GICS sector names the
rules key on, and whether `region` is a country or a region), and whether they are served for a MUTUAL fund ticker. Section
4 of the guide was measured on ETFs with SPY as control.

## 3. The schema this project would author

A second kind of row beside the one-label row, and one rule form that reads either:

| | one-label row (today) | weight row (proposed) |
|---|---|---|
| key | `security` | `security` |
| sector | `GICS_SECTOR_NAME`: one label | `sector_weights`: a list of `{label, pct}` |
| country | `CNTRY_OF_DOMICILE`: one ISO-2 code | `country_weights`: a list of `{label, pct}` |
| as of | the dated folder | the dated folder, and it is the ONLY date the weights are true for |
| the rule's share for a group | 100 if the label is in the group, else 0 | the sum of `pct` over the labels in the group |

The rule stays one sentence: the holding contributes its amount times its share for the group. A one-label row is the
case where one label has 100. A row carries ONE of the two forms for a dimension, never both.

A weight row's `claim` field, in the sense of `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md`, on each dimension:
`measured` (the source returned weights that day), `absent` (the source returned none for this security), `partial`
(weights returned but summing to less than the floor in section 5). A consumer rejects on it: `absent` and `partial` are
not held, with the existing reason form.

## 4. Four-postulate record (CLAUDE.md rule 24)

**Domain declared:** the dimension value of ONE security row on ONE dimension (sector, or country) on ONE dated folder.

(i) **MECE.** The forms are `ONE_LABEL`, `WEIGHTS`, `NONE`. Every row and dimension is exactly one: it holds a label, or
a weight list, or neither. The uncovered member was hunted by subtraction on the one population measured, the store's 172
rows on the sector dimension: 164 carry a label, 8 carry none, 0 carry anything else; 164 + 8 = 172, remainder 0. That
subtraction's domain is the CURRENT store, which holds no weight row and no mutual fund or cash row, so it cannot show a
member the proposed form fails to cover: a fund of funds, a cash symbol, a security whose weights sum over 100. Those three
are named here as NOT covered by evidence, not as covered.

(ii) **Same grain.** One row, one security, one day. A weight list does not change the grain: it is the value of one
field of that row. What must NOT happen is a row per (security, label), which would make the store's row count mean two
things.

(iii) **Intent coherence.** One axis, one intent: `sector_weights` answers "what share of this security sits in each
sector". It does not answer "what the security is" (asset class) and is not reused for it. `country_weights` answers where
the holdings are; the fund's domicile stays in `CNTRY_OF_DOMICILE` and stops being read as exposure for a weight row.

(iv) **State coherence.** What ONE remedy does not move: pulling a fund's weights today moves `WEIGHTS` for today's
folder and for no earlier folder, ever. So a report on an earlier date cannot be remedied by a later pull; its fund rows
stay `NONE` for that date. And a `partial` row is not moved to `measured` by renormalizing: renormalizing hides the
missing share, it does not measure it.

**Token census** (word-boundary, the three proposed value names against the tree was NOT run): `ONE_LABEL`, `WEIGHTS`,
`NONE` are proposed names. A collision check over the repo is owed before any of them is written into code; this record
does not claim they are free.

## 5. Choices the CTO is asked to rule, none taken here

1. **The floor for `partial`.** A fund's weights can sum to under 100 (cash, unclassified). At what sum is the row held?
2. **Renormalization.** Today's rules renormalize over the holdings that carry a label. With weight rows, does a fund's
   unclassified share leave the denominator, or count as its own "not classified" share on the page?
3. **Vocabulary.** If the source's sector names are not the 11 the rules key on, who owns the map between them?
4. **The date.** Whether a report may state an allocation as of the store's latest day when the positions are of an
   earlier day. Cottonwood's positions are of 2026-05-06; the store's latest folder is 2026-10-09. Today's one-label rows
   already do this for a company's sector, which rarely changes; a fund's allocation does change.
5. **Who pulls.** The four Opal funds are pulled today. Any other fund is a universe change at site Z, the same act as
   `NEVER_WIDEN_PACKET_ONE_EQUITY_STORE_ROW_20261011.md` beside this file, and under the same owner.

## 6. What this record did not measure

The fields' label vocabulary and their behaviour on a mutual fund; whether the four pulled funds overlap the 14 symbols of
the sized list; the count of sector and region elements in the Overview map (my count script matched nothing and I state no
number); and any effect on the report contract, which names a method string per section.
