# DESIGN QUESTION -- the directory-derived identifier fallback (AMGT-r-12, part (c))

**Not coded. Not exercised. Andrew's call, not this cell's.** AC3 refuses any version of it appearing
in `lib/research/identity/*.py`, and none does; this document exists so the trade-off can be ruled on
without re-deriving it.

## The example that motivates it: the "SAP GY"-style case

Round 1 (W7-S3/AC7) downgraded 16 research directories to UNRESOLVED because their one-pager
workbook's `Model` sheet carried an unfilled template default (the literal `AAPL US`, on sixteen
companies none of which is Apple) rather than the subject's own value. One of those sixteen is the
directory literally named `SAP GY` -- the same string a Bloomberg-shaped ticker for SAP would take.

This round's coverage pass (AMGT-r-12, source ii) resolved that one and one other (`Imperial Brands
IMB LN` -> `IMB LN`) *without* touching the directory's own name at all -- it re-read the SAME
workbooks more thoroughly and found a second, genuine `Overview` sheet the original per-folder scan
never reached (it stopped at the first file/sheet that produced any label match, which happened to be
the placeholder). Fourteen of the sixteen were **not** so lucky: their workbooks carry no second sheet
with real data, only the same unfilled `Model` template plus a FactSet-format identifier on the
excluded `Model NEW VERSION` sheet (e.g. `CLX-US`, `NESN-CH`) that is not Bloomberg-shaped and cannot
be turned into one without an exchange-suffix mapping table this order does not carry (GB -> LN? DE ->
GY? FR -> FP or PA? -- more than one Bloomberg exchange code can correspond to one country, so the
mapping is not 1:1 and guessing wrong would silently mis-tag a security).

For those fourteen (and Rio Tinto, whose own workbook carries only a `#N/A Invalid Security` artifact),
the directory's own name is themself the input to a possible fallback. The mechanism this document
describes -- and this cell refuses to build -- is:

> **Given a still-UNRESOLVED directory whose display name already looks like `<Company> <TICKER>
> <SUFFIX>` (the convention nearly every directory in this corpus follows -- e.g. `AstraZeneca AZN`,
> `Nestle NESN SW`, `SAP GY`), read the trailing Bloomberg-shaped token(s) off the directory's own name
> and assign that as the bloomberg_ticker value.**

## What it would infer, concretely

Applied to the 14 remaining shared-placeholder directories plus Rio Tinto, the trailing-token read
would produce (directory -> the value read off its own label):

| directory | value the rule would read |
|---|---|
| AstraZeneca AZN | `AZN` |
| Canadian National Railway CNR | `CNR` |
| Clorox CLX | `CLX` |
| Copa CPA | `CPA` |
| JD.com 9618 HK | `9618 HK` |
| Michelin ML FP | `ML FP` |
| Mitsubishi UFJ Financial Group 8306 JP | `8306 JP` |
| Nestle NESN SW | `NESN SW` |
| Nokia FH | `FH` (ambiguous -- see failure mode) |
| Orange ORA FP | `ORA FP` |
| Sanofi SAN FP | `SAN FP` |
| Shopify SHOP CA | `SHOP CA` |
| Tokyo Marine 8766 JP | `8766 JP` |
| Total Energies TTE FP | `TTE FP` |
| Rio Tinto RIO LN | `RIO LN` |

**The benefit, in one denominator's categories (never mixed):** this pass stands at **34 MEASURED** (the
measured workbook reads this round landed). The fallback above would add **up to 15 additional INFERRED
candidates** on top of that -- the two counts are never combined into one figure, because MEASURED and
INFERRED are different provenance classes and are counted separately (A VALUE MUST CARRY ITS CLAIM). It
is still the single largest lever available on this identity layer, larger than every workbook-read
source combined -- it is just not a MEASURED lever.

## Confidence and failure mode -- OBSERVED separated from HYPOTHETICAL

This is **not** a read of a company's identity; it is a read of **whoever named the directory's**
belief about that identity, with no independent confirmation. The two ways it can break are NOT the same
kind of claim and this document keeps them apart: one is OBSERVED, real in this exact corpus today; the
other is HYPOTHETICAL, a design risk that has not happened here and is not presented as a measured
result.

### OBSERVED (real in this corpus): an ambiguous trailing token

`Nokia FH` is the live example, already in this corpus, not a hypothetical: `FH` alone is not a securely
parseable Bloomberg exchange suffix without the company name in front of it staying attached to the
value (Nokia's real Bloomberg ticker is `NOKIA FH`, not the bare exchange code) -- a naive
trailing-token split can grab the wrong span depending on how many words precede it, and there is no
workbook cell to check the result against once the fallback IS the source. This is a MEASURED fact about
the corpus (the directory is named `Nokia FH` today), even though any fallback value read off it would
itself be INFERRED, never MEASURED.

### HYPOTHETICAL (not observed in this corpus): a future renaming

`Rio Tinto RIO LN` follows the convention and would read `RIO LN` cleanly today -- but nothing stops a
directory from being renamed `Rio Tinto` (no ticker at all) or `Rio Tinto - OLD` after a future re-org,
and the rule has no way to tell "no ticker present" apart from "ticker present but the read is wrong."
**No directory in this corpus is currently renamed this way -- this is a design risk about a re-org that
has not happened, not a measured failure mode observed here, and it is not counted in either the 34
MEASURED or the up-to-15 INFERRED figures.** A workbook cell fails LOUD (UNRESOLVED, reason named); a
directory-name read of the wrong token after such a renaming would fail SILENT (a plausible-looking wrong
ticker, still only INFERRED at best -- never promoted to MEASURED by any gate named below).

## The trade-off, stated for a ruling

- **Coverage gained, stated in two separate counts:** 34 MEASURED stands unchanged (this pass's measured
  workbook reads). The fallback would separately add up to 15 INFERRED candidates -- never combined into
  one number -- covering exactly the directories a workbook-based source structurally cannot reach (no
  second clean sheet, or no workbook at all for the 40 PDF-only directories -- though for those 40 there
  is no ticker-shaped token in the directory name to read either, e.g. `Visa V`, `Netflix NFLX`, so the
  fallback would not reach all 55 even if authorized).
- **Claim carried:** every value the fallback produces is INFERRED at best (a directory-naming
  *convention*, not a measurement of the company), never MEASURED (A VALUE MUST CARRY ITS CLAIM).

## Which gates still refuse INFERRED (downstream admissibility)

An INFERRED candidate is **not automatically served** -- today, before any code exists, two concrete
gates already in `lib/research/identity/` bear on it, named exactly, not both the same way:

1. **`coverage_pass.py`'s ACCEPTANCE RULE (the write side) already refuses it.** This is the ONLY code
   path that currently promotes a `bloomberg_ticker` to MEASURED status in `universe.json`, and it is
   coded to accept a candidate from exactly three named sources -- (i) `sa_ids.json`, (ii) a workbook-cell
   rescan, (iii) a coverage-universe cross-reference -- and the module's own docstring states plainly that
   a directory's own name "is NOT one of those sources and nothing below reads a directory's own name as
   evidence." So an INFERRED, directory-name-derived candidate has no path to becoming MEASURED through
   this gate; it would need an entirely new, never-authorized write path.
2. **`resolver.py`'s `render_together()` (C-IDENTITY-RESOLVED, the read side) does NOT yet refuse it --
   this is the open half of the question.** As coded today it refuses only when a depended-on key's status
   is UNRESOLVED (`resolver.py:180`); MEASURED and INFERRED are both currently ADMITTED without
   distinction. `bloomberg_ticker` has never carried an INFERRED status in this codebase (only
   `sa_symbol` can be INFERRED, via rule (c)) -- the fallback would be the first thing to produce one. If
   Andrew authorizes the fallback, whether `render_together()` (and any other downstream surface: peer
   sets, check-face, drafting) should treat an INFERRED `bloomberg_ticker` the same as UNRESOLVED, the
   same as MEASURED, or as a third case of its own, is a still-open design question this document does
   not answer -- it names the gap rather than closing it silently.

**The fallback stays UNIMPLEMENTED pending Andrew's decision (unchanged from AMGT-r-12).** If Andrew
authorizes it, the honest floor is INFERRED, with the directory's own name named as evidence (so a
reader can see exactly what was trusted and why) -- the same discipline `resolver.infer_sa_symbol()`
already applies to the `sa_symbol` key -- and the open admissibility question above is decided before,
not after, any value reaches a downstream surface.

**This cell takes no position on whether the trade is worth it.** It states the mechanism, the
directories it would touch, its OBSERVED and HYPOTHETICAL failure modes kept separate, and the
confidence ceiling (34 MEASURED, up to 15 INFERRED, never a combined figure) so Andrew can rule on it
without re-deriving any of the above.
