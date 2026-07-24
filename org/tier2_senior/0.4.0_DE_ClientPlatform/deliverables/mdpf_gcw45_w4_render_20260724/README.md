# GC-W45 W-4 render evidence (2026-07-24)

Render commit: portal DEV `d1ba89b9` (pushed). TO: `MDPF_3FIRMS.GC-W45`.
Class set CONVERGED with `0.4.0_DS_ClientPlatform~A` (their confirm 153714Z) -- COO's blocking
precondition, cleared before this landed.

## AC-5 mutant + its controls

| PNG | REFAREAS | What it establishes |
|---|---|---|
| `AC5_CONTROL_5ra.png` | 5 | baseline on the real served bytes |
| `AC5_MUTANT_6ra.png` | **6** | ONE array element flipped (`count_provenance[331]` `measured`->`band_2firm`, 2026-03-03) moves the render |
| `CONTROL_valuemode_0ra.png` | 0 | VALUE mode unchanged -- Andrew's 2026-07-23 Global materiality ruling INTACT |
| (re-run of control, not retained) | 5 | determinism: 5->6 is the mutant, NOT run-to-run variance |
| `INVALID_prod_baseline_notcited.png` | n/a | **A FAILED MEASUREMENT, RETAINED DELIBERATELY.** Live-PROD baseline returned Total AUA $0 with no charts (the auth stub does not reach PROD data endpoints). Declared INVALID and NOT cited as evidence anywhere. |

Fixtures were proven byte-identical except that single element BEFORE rendering
(`account_count_total`, `dates`, `by_model` asserted equal). The mutant date carries a REAL count
(6322), so the bar plots either way and ONLY the class differs.

The band derives from the class alone -- no date range, no index, no hard-coded list -- which is
what makes the mutant a control rather than decoration.

## Read, not merely counted

A grep cannot see contrast. The PNGs were opened and read: the band renders subtle-slate over the
cottonwood-covered era only, the "Declared count basis" label is legible, and the contrast is legal
for the dark chart Panel per the portal colour law. The NEUTRAL idiom (COO ruling 153053Z) keeps the
alarm vocabulary UNSPENT for the `present < expected` error W-2 will fire.

## Reported, not fixed

`const raw = periodData ? (...) : 0` at HEAD `:2084` / `:2303` renders a missing per-model row as a
real ZERO ACCOUNTS bar -- visible as sharp vertical spikes in the daily count chart, found by
READING the screenshot. PRE-EXISTING (confirmed via `git show HEAD:` plus a diff proof that this
change touches neither site). Out of W-4 scope; routed by COO to CTO.

## Correctness against the CURRENT served artifact (COO ask, 154829Z) -- TESTED, not asserted

Rendered all three PER-FIRM views in count mode against the CURRENT served bytes, holes intact.
The band count is PREDICTABLE from the data -- |value-bearing non-measured classes|, grouped into
contiguous runs -- so this is a prediction-match, not an observation:

| View | value-bearing non-measured in the served bytes | PREDICTED bands | OBSERVED | |
|---|---|---|---|---|
| Global | 24 `band_2firm` + 1 `frontier_stamp` | 5 runs | **5ra** | MATCH |
| 49financial | 0 `band_2firm` + 1 `frontier_stamp` | 1 run | **1ra** | MATCH |
| inflection | none (only `measured` + `source_absent`) | 0 | **0ra** | MATCH |
| cottonwood | none (only `measured` + `source_absent`) | 0 | **0ra** | MATCH |

**Cottonwood is the extreme hole case in the estate** -- 445 of 447 dates `source_absent`,
`account_count_total` non-null on 2 dates only. It renders cleanly: the daily chart shows exactly
the two covered dates, no band, no error, no zero-cliff, panel intact (screenshot READ).

The 22 holes are VALUE-NULL classes, so they plot nothing and band nothing. The render never
consults a date, a firm name or a count -- only the class on the point -- so a hole-heavy series
and a filled one take the same path.
