# /portfolios -- the BEFORE side of the Global fold card (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~21:1xZ)

Read-only. Numbers computed by `round7/checks/portfolios_card.py before` from the newest UNFOLDED dated global objects, re-deriving the page exactly as
`portal/src/pages/ModelPortfolios.tsx` does at this tree's HEAD (anchors below). The AFTER side is the same script, `after --date D`, run by the issuer after the
first folded scheduled fire (2026-10-14 13:30Z at the earliest). No account id is read or printed.

## Objects read (all unfolded; none carries `meta.by_model_fold` or an Other Models line)

| type | dated key | written | platinum served copy (`opal-data-portal-v2/platinum/mdpf/global/<type>.json`) |
|---|---|---|---|
| aum-metrics | 2026-10-12.json | 2026-10-13T13:31:49Z | EQUAL to it (ignoring `_provenance`), written 2026-10-13T13:50:53Z |
| account-distribution | 2026-10-13.json | 2026-10-13T13:31:49Z | EQUAL, same stamp |
| aggregate-aua-timeseries | 2026-10-12.json | 2026-10-13T13:31:49Z | EQUAL, same stamp |

Why three different keys: the distribution is keyed by the run date, aum-metrics and the time series by the frontier date (previous trading day). Each type takes its newest key <= the date asked.

## (1) Total Holdings (page :1238-1245)

**8,607** = `total.account_count` 8,422 + the by_model counts of the two blend keys that `getCanonicalModelName` maps into `BLEND_ARCHETYPES`
(Opal Blend 5050 Int Ltc 162 + Opal Blend 5050 St Int 23 = 185). After the fold the blend keys leave the distribution's `by_model`, so the headline reads 8,422: the pair's -185.

## (2) The archetype cards (page :690-723 with `rollBlendsIntoArchetypeModels` :207-224, `BLEND_ARCHETYPES` :163-166)

| card | AUM as shown (roll-in applied) | accounts as shown | raw (no roll-in) AUM | raw accounts |
|---|---|---|---|---|
| Ultra-Short Term | 70,032,009.37 | 192 | 70,032,009.37 | 192 |
| Short Term | 142,386,174.90 | 864 | 138,541,426.58 | 841 |
| Intermediate Term | 478,024,564.62 | 2,217 | 456,470,971.10 | 2,034 |
| Long Term | 906,634,507.31 | 3,636 | 888,925,662.11 | 3,476 |
| Ultra-Long Term | 211,424,742.86 | 1,431 | 211,424,742.86 | 1,431 |

Blends rolled in (aum-metrics rows): 50/50 ST/INT 7,689,496.64 over 23 accounts; 50/50 INT/LT 35,417,690.39 over 160 accounts; together **43,107,187.03**. Each blend's AUM is
split in half to each of its two archetypes and its full count is added to BOTH, so Short Term gains 3,844,748.32 and 23 accounts, Intermediate Term 21,553,593.52 and 183, Long Term
17,708,845.20 and 160. The cards therefore lose 43,107,187.03 in dollars (the pair's "-$43.16M" was measured at the 2026-10-09 as-of) and 366 account-card counts in all. The INT/LT blend reads 160 accounts here and
162 in the distribution (a declared basis seam, the CN-d-1 read); Total Holdings uses the distribution's 162.

## (3) The trend (page :782-857, `rollBlendsIntoArchetypeSeries` :171-204)

14 model series after the blend roll (5 canonical + 9 custom lines), over 495 dates, last 2026-10-12. The first date a canonical model has a value is **2024-11-01**; each canonical line carries a value on **486 of 495** dates.
The custom lines carry far fewer: Opal Moderate Income Portfolio 51, Opal 15/85 Income Portfolio 37, Fixed Income 34, Opal Income 23, Opal Income Portfolio - Gillham 18, Opal Moderate Income 13,
Opal Moderate Income Tax Efficient 11, Opal Muni Sleeve 11, Opal Moderate Income Portfolio (Tax Efficient) 8. After the fold the pair says per-model detail begins 2026-05-15.
Not counted here: the Non-Model band, the SMA sleeves and the aggregate line (the page adds them downstream), and the page's `globalCompleteFrontier` clamp (a suffix filter that does not change the first date).

## (4) The 20 core quarter cells (aum-metrics `by_model[].q0..q3`; dates q0 2026-09-30, q1 2026-06-30, q2 2026-03-31, q3 2025-12-31)

All **20 of 20 present** today (Ultra-Short, Short, Intermediate, Long, Ultra-Long Term, each q0 to q3). The pair's accepted delta is 10 of 20 absent after the fold (q2 and q3 fall before 2026-05-15).

## (5) The AFTER computation

`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/portfolios_card.py`:
- `before` prints the numbers above and pins them to `portfolios_card_before.snapshot.json` beside it; it refuses to pin if any object it reads is folded.
- `after --date D [--source a4|platinum] [--before-date B]` recomputes at D and prints a BEFORE / AFTER / DELTA table against the pin.

Dry-runs, this session: `before` printed the sections above and pinned the snapshot. `after --date 2026-10-13` (the same unfolded objects) printed **ROWS WITH A DELTA: 0** over all sixteen compared rows.
The expected after-fold deltas to read on 2026-10-14: Total Holdings -185; the blend roll-in leaving the cards (about -43.1M); trend series 14 to about 9 with first per-model date 2026-05-15; core quarter cells absent 0 to 10; an `Other Models` slice/series appearing.

## Not read or not computed

The rendered page (no ui-smoke look); the per-firm scopes; the `Other Models` slice's behaviour on the donut (an unknown name passes through `getCanonicalModelName`); whether the card (client-facing, Andrew's) wants the 2026-10-09 as-of figures the pair quoted (-$43.16M) or these 10-12 ones.
