# POSN_ASTTAX.TO-W2-1 -- W2-AC9 JUDGMENT READINGS (slot `0.9.0_WK_POSN_ASTTAX~25`)

**JUDGMENT criterion. GRADED AT L9 BY `3.0.0_SA_CVO~Z`. NO VERDICT IS OFFERED HERE.**
Both readings are recorded against measured state on the rendered page (dev server 5181,
fixtures built from the SERVED bytes: `characteristics.json` VersionId
`74d9.pGWF16Ox7cXKGax.zQw.lhwi5yI`, `holdings.json` `67GP52SdV1rw6QFVNPytU6ec4TvhwJh3`).

---

## READING 1 -- a fund-level fact on a position row

**What the page literally says now.** One Holdings Breakdown row carries TWO GRAINS side by
side, with nothing between them naming the difference:

| cell | whose fact | whose clock |
|---|---|---|
| WEIGHT `8.34` | THIS SATELLITE's holding of GLD | Black Diamond, `holdings.json` as_of 2026-09-14 |
| MC `147.7` | the FUND's total assets (147,692.4 mm) | Yang / Bloomberg, the producer's own input vintage |
| FEE `40` | the FUND's expense ratio | same |

The column group above them is headed **ETF CHARACTERISTICS**, and the Basic Info group to
their left is headed **BASIC INFO** with ASSET CLASS / SUB ASSET / TICKER / NAME / WEIGHT.

**Three things measured, offered as the material rather than as an argument:**

1. **The same fund shows the SAME fund-level number in two different satellites.** GLD's MC
   reads `147.7` in Opal Satellite 15 (weight `8.34`) and `147.7` in Opal Satellite 80
   (weight `2.11`). That is the correct behaviour for a fund-level fact -- and it is also
   exactly the tell that the number is NOT the position's: nothing on the row scales with
   the position.
2. **The double grain is not new to this TO.** Models mode has drawn the same seven columns
   on its own rows since before round 6 (measured: the pre-edit Models dump carries FEE 7 /
   MC 2.4 / YIELD 3.71 on CLIP with the same WEIGHT column beside them). What IS new is that
   a **Black Diamond position row** and a **Yang fund fact** now sit in one line, from two
   producers on two clocks -- and this TO put the mode's own clock in the panel header and
   footer (`Source: Black Diamond, holdings as of 2026-09-14`), which names the POSITION's
   vintage on a panel that also shows the FUND's numbers.
3. **The header word that would settle it was not changed.** `ETF CHARACTERISTICS` is in
   `HoldingsTab.tsx`, this TO's file -- but the TO names four hunks (the Active cell, the two
   footers, the two headers, the legend) and a column-group rename is not one of them. It is
   left alone rather than quietly widened.

**The open question, stated without answering it:** does an analyst reading
`GLD ... 8.34 | 40 | 147.7` take `147.7` as "this satellite holds 147.7 of something" or as
"the fund is 147.7bn"? The only on-screen disambiguator today is the group heading.

---

## READING 2 -- one glyph for two different silences

The table renders `-` for BOTH:

- **"no source carries this measure for this holding"** -- CASH's every cell (`source: none`);
  GLD's yield / duration / credit / beta (Bloomberg has no column for them);
- **"this column does not apply to this class"** -- Duration on any Equity row
  (`HoldingsTab.tsx:1576`, "Hide duration for Equity ETFs per Yang's spec") and Beta on any
  Fixed Income row (`:1590`).

**MEASURED on the rendered rows** (`w25_dash_census.py`, attributing a dash to the CLASS RULE
only where the rule alone would produce it, and to BOTH where the rule and a served null are
both true -- because a cell the evidence cannot separate must not be filed under one cause):

| satellite | dash cells | of characteristic cells | class rule ONLY | absent measure ONLY | BOTH, inseparable |
|---|---|---|---|---|---|
| Opal Satellite 15 | 34 | 112 (16 rows x 7) | **0** | 19 | **15** |
| Opal Satellite 80 | 40 | 112 (16 rows x 7) | **0** | 26 | **14** |

**The finding that surprised this worker:** on today's payload **NOT ONE dash is caused by
the class rule alone**. Every Duration-on-Equity and Beta-on-Fixed-Income cell ALSO has a
null served value, so the class rule is currently invisible -- 29 of the 74 dashes are
OVERDETERMINED. The ambiguity the criterion asks about is therefore **structural and latent**
rather than currently visible: the day a producer serves a duration for an Equity ticker,
that cell will read `-` for a reason no other cell on the page shares.

**A fourth glyph in the same table, counted beside it.** The performance plane renders an EM
DASH (`—`) for a null, not a hyphen: 9 of 128 cells in Opal Satellite 15 and 10 of 128 in
Opal Satellite 80 -- CASH's eight windows in each, plus PFDE's `1Y` (and PFOE's `1Y` in
Satellite 80), which are served null. So one row can carry a hyphen for an absent
characteristic and an em dash for an absent return, and they mean the same thing.

**And a third state now exists in one column only.** This TO gave ACTIVE three states
(`YES` / `NO` / `-`) because the two-state cell asserted "passive" about every row of a
payload that carried no such field. Measured: 2 of 32 rows (the two CASH rows) now read `-`
where they read `NO` before, and 22 of 22 Models rows are byte-identical. **The remedy chosen
there was to SPEND A GLYPH rather than to overload one** -- which is the same choice this
reading asks about for Duration and Beta, decided the other way in the same file.

---

**NO VERDICT. Recorded for `3.0.0_SA_CVO~Z` at L9.**
