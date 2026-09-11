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

That would raise MEASURED-or-better coverage from this pass's 34 to as high as 49 of 89 -- the single
largest lever available on this identity layer, larger than every workbook-read source combined.

## Confidence and failure mode

This is **not** a read of a company's identity; it is a read of **whoever named the directory's**
belief about that identity, with no independent confirmation. Two concrete ways it breaks, both
already visible in this exact corpus:

1. **A renamed or generic directory.** `Rio Tinto RIO LN` follows the convention and would read
   `RIO LN` cleanly -- but nothing stops a directory from being named `Rio Tinto` (no ticker at all) or
   `Rio Tinto - OLD` after a re-org, and the rule has no way to tell "no ticker present" apart from
   "ticker present but the read is wrong." A workbook cell fails LOUD (UNRESOLVED, reason named); a
   directory-name read of the wrong token fails SILENT (a plausible-looking wrong ticker, MEASURED).
2. **An ambiguous trailing token.** `Nokia FH` is the live example: `FH` alone is not a securely
   parseable Bloomberg exchange suffix without the company name in front of it staying attached to the
   value (Nokia's real Bloomberg ticker is `NOKIA FH`, not the bare exchange code) -- a naive
   trailing-token split can grab the wrong span depending on how many words precede it, and there is no
   workbook cell to check the result against once the fallback IS the source.

## The trade-off, stated for a ruling

- **Coverage gained:** up to 15 more MEASURED-or-better entries (34 -> up to 49 of 89), covering
  exactly the directories a workbook-based source structurally cannot reach (no second clean sheet, or
  no workbook at all for the 40 PDF-only directories -- though for those 40 there is no ticker-shaped
  token in the directory name to read either, e.g. `Visa V`, `Netflix NFLX`, so the fallback would not
  reach all 55 even if authorized).
- **Claim carried:** every value the fallback produces is INFERRED at best (a directory-naming
  *convention*, not a measurement of the company), never MEASURED -- Rule "a value must carry its
  claim" requires this distinction survive into every downstream surface (peer sets, check-face,
  drafting) that currently REFUSES on an UNRESOLVED key; an INFERRED-not-MEASURED identity would need
  every one of those surfaces to decide whether INFERRED clears their own bar, which is a second design
  question this document does not answer for them.
- **What is NOT proposed:** silently promoting an INFERRED directory-name read to MEASURED. If Andrew
  authorizes this fallback, the honest floor is INFERRED, with the directory's own name named as
  evidence (so a reader can see exactly what was trusted and why) -- the same discipline
  `resolver.infer_sa_symbol()` already applies to the sa_symbol key.

**This cell takes no position on whether the trade is worth it.** It states the mechanism, the
directories it would touch, its two measured failure modes, and the confidence ceiling (INFERRED, never
MEASURED) so Andrew can rule on it without re-deriving any of the above.
