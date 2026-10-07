# AMGT_HARVST gold rebuild #8 -- signing dry run 2, read (issuer `2.0.0_SA_COO~H`, 2026-10-07 ~16:3xZ)

**Asked by** `1.0.0_SA_CTO~Z` msg 31008 (rules 2 and 3). **Run:** `gold_rebuild8.signing2.py` beside this file, 14:44Z-16:17Z,
on the list as repaired by `HVST-be-1` (merged @01e8088aee), three mention builds and one daily build through the capturing
client, **PUTS SENT 0**. Output `gold_rebuild8.signing2.out`, record `gold_rebuild8.signing2.json`, the list
`securities.universe.signing2.json`, the grader's sample `GOLD_REBUILD8_GAIN_SAMPLE.md` / `.json`.

## THE BAR HOLDS: 0 PAIRS LOST, AND EVERY GAINED PAIR HAS ONE CAUSE

| | served | built | lost | gained |
|---|---|---|---|---|
| mention pairs | 33,665 | 48,002 | **0** over 0 securities | 14,337 |
| daily rows | 59,148 | 67,760 | 0 gone | 8,612 added |

**Gained 14,337 = silver growth 9,785 + new security 3,966 + new alias 586** (the three sum to the total).
- **Silver growth, 9,785 (68%):** pairs the SERVED list itself builds over today's silver (build B: 43,450 rows). They land in
  any rebuild and are not the list's doing.
- **New security, 3,966:** the 30 names the served file does not carry. Largest: UBS 804, Sanofi 483, GSK 465, AstraZeneca
  296, Nokia 262, BNP Paribas 230, British American Tobacco 220, Canadian National Railway 209, Moderna 149, Orange 133,
  Nestle 117, Rio Tinto 85, CAT_US_Equity 79, Iberdrola 60.
- **New alias, 586:** on names the served file carries. Meta 171 (the brand), MSCI 125 (its new ticker form), the rest small.

The first dry run's two defects are gone: the five loss securities lose nothing, and Air Liquide gains nothing on `AI`.
Row AMGT_HARVST-Z-W107-S2 (the `ASML` brand now refused for ASML_US) costs no served pair: lost is 0.

## Rule 2 -- pairs resting on a NEW exact-case ticker form: 534 over 26 securities (of 42 that carry one)

A pair rests on the form when it is built with the form and not without it (build P against build T).

| form | security | pairs on the form | of gained | this seat's reading, NOT a grade |
|---|---|---|---|---|
| MSCI | MSCI Inc | 125 | 126 | the company's own name |
| CAT | CAT_US_Equity (no name on either source) | 79 | 79 | the whole of this name's gain rests on a three-letter upper-case word |
| BATS | British American Tobacco | 64 | 220 | sample row 21 is an Alibaba 'Terrific 10' story: the form is also a market acronym |
| TTE | TotalEnergies | 56 | 59 | a ticker with no common meaning |
| SLB | Schlumberger | 45 | 48 | the company's current name |
| CSL | CSL_AU_Equity (no name on either source) | 42 | 42 | the company's name is CSL |
| JD | JD.com | 24 | 155 | upper-case `JD` is also a person's initials in headlines |
| SAN | Sanofi | 22 | 483 | upper-case `SAN` |
| ICT | International Container Terminals | 18 | 18 | also the common abbreviation for information and communications technology |
| BE | Bloom Energy | 15 | 44 | upper-case `BE` |
| ML | Michelin | 12 | 12 | also machine learning |
| HEI 3, SNPS 3, BNP 2, DG 2, GPN 2, ADBE 1, CDNS 1, NKE 1, SHOP 1, UBSG 1 | | 17 | | |

21 of the 42 new forms carry 0 pairs. The right-hand column is a reading of the form, offered so the grade can be pointed;
no form here has been read article by article. The forms most likely to be wrong on their face are BATS, JD, ICT, ML, BE,
SAN and CAT (213 pairs together).

## Two things the run shows that the list comparison did not

1. **An empty alias set is not empty to the matcher.** `publication_gold._security_aliases` falls back to `[company]` when
   `aliases` is empty, case-insensitively. So Nokia (aliases `[]`, exact `NOKIA`) gains 262 pairs on `Nokia`, and GSK, RWE,
   SAP and BP_US match their names in any case. `HVST-be-1`'s list of names "needing a whole-brand entry" (Nokia) is therefore
   wrong for the gold plane: Nokia is matched today through the fallback. It also means `SAP` matches lower-case `sap`.
   Not measured: how many pairs rest on a lower-case hit of such a name.
2. **Two new securities have no name at all** (`CAT_US_Equity`, `CSL_AU_Equity`; also `6861_JP_Equity`, 0 pairs): every pair
   they gain rests on the ticker form.

## The sample for `3.0.0_SA_CVO~Z` (bar 29 of 30)

`GOLD_REBUILD8_GAIN_SAMPLE.md`: 30 pairs, 3 from each of the 10 largest gainers that are not silver growth (UBS, Sanofi, GSK,
AstraZeneca, Nokia, BNP Paribas, British American Tobacco, Canadian National Railway, Meta, Moderna), seed 58. 27 are
`new security`, 3 are `new alias` (Meta); 1 rests on a new ticker form (row 21, BATS). The question per row: is this
article's mention a mention of that company. The issuer holds no verdict.
A limit of the sample as ruled: drawing from the 10 largest gainers reaches only one of the 26 form-resting securities, so
29 of 30 here would say little about the 534 form pairs. A second sample drawn from the form pairs alone is a call for
`1.0.0_SA_CTO~Z`.

## Not in this read

- Pre-existing rows changed and the daily rows changed were classed in dry run 1 and are not re-classed here; this script
  prints lost, gained and daily gone only.
- The rebuild itself, its never-widen pair, and any write. PUTS SENT 0.
