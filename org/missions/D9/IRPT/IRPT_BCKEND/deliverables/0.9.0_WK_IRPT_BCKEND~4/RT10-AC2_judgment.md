# RT10-AC2 -- JUDGMENT, RECORDED AND NOT SELF-GRADED

**Task order:** `IRPT_BCKEND.TO-IB-rt-10` | **cell** `IB-rt-10` (PRD row B10) | **worker** `0.9.0_WK_IRPT_BCKEND~4`
**Grader:** `3.0.0_SA_CVO` at L9. This document carries OUTPUT and NO VERDICT. The proof-of-spec row for
RT10-AC2 is `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming the CVO.

The criterion, verbatim from the face:

> State for `3.0.0_SA_CVO`: which glyphs beyond `fi` the three documents map differently; whether `REPORT`
> as a date claim could mislead a reader of a section that is genuinely stale; and which arm breaks first
> on a real client PDF.

Three questions. Each is answered below with what was measured and what is inference, kept apart.

---

## 1. WHICH GLYPHS BEYOND `fi` THE THREE DOCUMENTS MAP DIFFERENTLY

**MEASURED: 73 of 89 compared codes.** The comparison is between the PRIMARY TEXT FONT of each of the three
retained vendor specimens (`RobotoCondensed-Regular` in all three, as three different subsets:
`QXFAAA+`, `QTHAAA+`, `QTIAAA+`). The denominator 89 is the union of the codes those three subsets map;
73 of them mean different characters in at least two of the documents.

The structure of the disagreement is not random, and it is worth the CVO's attention because it explains
why the number is so large. **Pairwise agreement over the codes each pair has in common, measured:**

| pair | codes agreeing | of common codes |
|---|---|---|
| comparison vs overview | **75** | 87 |
| multicomp vs overview | **18** | 86 |
| multicomp vs comparison | **15** | 86 |

**Codes 1-8 are identical in all three** (`B u i l t <space> w h`, the start of the footer string). From code
9 on, overview and comparison stay together and **multicomp goes its own way**, because a subsetter assigns
codes IN FIRST-USE ORDER and the multicomp document's first page puts a different string in front of the
reader. Two of the three documents therefore agree on 75 of 87 codes, and **a table built from either of
them would have been right twice and wrong once** -- the shape of error that survives review, because the
first two files you test with confirm it.

**Specific divergences a reader should hold on to** (each measured over the three documents' PRIMARY text
font, `RobotoCondensed-Regular` as three different subsets `QXFAAA+`, `QTHAAA+`, `QTIAAA+`):

- code `9` is the digit `2` (U+0032) in overview and comparison, and the letter `S` (U+0053) in multicomp
- code `12` is `Y` (U+0059) in two documents and `.` (U+002E) in the third
- code `14` is `a` (U+0061) in two and `,` (U+002C) in the third -- **a letter in one file and a punctuation
  mark in another**, which inside a rendered number is the difference between `1,234` and `1a234`
- code `44` is `T` (U+0054) in two and `-` (U+002D) in multicomp; code `47` is `M` (U+004D) in two and `H`
  (U+0048) in multicomp
- codes `45` and `46` do NOT appear in this count, and the reason is worth stating: a code only counts as
  diverging when at least two documents map it, and each of these is mapped by exactly one of the three --
  the other two have their hole there. **The absence of 45 and 46 from the divergence list is the hole, not
  agreement.**

**AND THE DIVERGENCE IS ALSO INTRA-DOCUMENT, which is the finding I did not expect to have to make.** The
first version of `fonts.py` resolved a code through whichever of *this document's* fonts mapped it. That is
already "per-document", and it is still wrong: within the overview specimen, code 45 belongs to
`QXFAAA+RobotoCondensed-Regular` (unmapped) and is mapped by `QHGAAA+RobotoCondensed-Bold` to `8`. The
module now requires the name of the font that rendered the code, and `cross_font_control` prints what the
relaxed rule would have returned:

| document | the unmapped code | what the SAME DOCUMENT'S other font would say |
|---|---|---|
| overview | 45 | U+0038, the digit `8` |
| comparison | 45 | U+004D, the letter `M` |
| multicomp | 46 | U+0044, the letter `D` |

**The unit of a glyph map is the FONT RESOURCE, not the document and not the vendor.** A reviewer reading
"per-document font mapping" in the ruling should know that the phrase has a second, tighter reading and that
this cell took it.

**INFERENCE, marked as such:** `fi` is almost certainly what codes 45/45/46 render -- the surrounding text
is `signi_cant`, `_nancial`, `speci_c`. I have not written that anywhere an extractor can reach it and I am
not proposing to. It is stated here, in prose, for a human.

---

## 2. WHETHER `REPORT` COULD MISLEAD A READER OF A SECTION THAT IS GENUINELY STALE

**Yes, and this is the sharpest open question in the cell.** The measured facts first.

- All three vendor specimens carry a report header date of **2026-09-11** on page 1.
- All three also print per-block `Data as of` lines carrying **2026-09-09** and **2026-08-31** as well as
  2026-09-11. The August 31 blocks are **eleven days staler than the report header**.
- Under the rule this cell implements, a row whose page prints no `Data as of` line above it takes the
  report header date and is marked `REPORT`: **14 of 71 rows in overview, 40 of 91 in comparison, and 67 of
  118 in multicomp** -- a majority of the multicomp rows.

So the hazard is concrete: **a section whose real data is from August 31 but which prints no date line of
its own will carry `as_of_date: 2026-09-11` with `date_claim: REPORT`.** The value is honest about WHERE the
date came from and dishonest-by-omission about how old the data is, and a consumer that renders
`as_of_date` without reading `date_claim` shows a client an eleven-day-stale number under today's date.

**Three things reduce it and none of them closes it:**

1. The claim is in the artifact and is rejectable. A consumer CAN refuse or annotate a `REPORT` row. That is
   the entire reason the property was added to the contract rather than kept in a private key.
2. `REPORT` is never silently substituted for `SECTION`: the rule prefers the block's own line whenever one
   exists above the value, and certification leg L4 re-reads it from the document.
3. The alternative -- holding every `REPORT` row out, as round 1 effectively did -- would drop 67 of 118
   multicomp rows from the artifact, and **a smaller array reads to a consumer as a smaller document**, which
   is its own misrepresentation.

**What I could NOT settle, and am handing over:** the property is OPTIONAL in the contract (decomposition
v0.2 s.2 directs exactly that, so `additionalProperties:false` holds and round-1 instances stay valid). **An
optional field a producer may omit is a field a consumer cannot rely on for a refusal.** If the FNTEND half
must be able to refuse a report-level date rendered as a section date, `date_claim` has to be REQUIRED, and
requiring it is a contract break this cell has no standing to make. Channel row `IRPT_BCKEND-W4-S27` names
this for the CTO's L10 read; I raise it here too because it is the half of the question the CVO is being
asked to grade.

**A second-order point, offered and not pressed:** `REPORT` currently means "no date line governs this
value". It does not distinguish *"this document states no section dates at all"* from *"this document states
section dates elsewhere and simply not here"* -- and the second is much more worrying, because it means the
producer had the information and did not print it. That distinction is measurable from `multi_date_pages`
and `date_lines`, both of which the extractor already emits, but it is not in the enum and adding a fourth
member would be a taxonomy change outside this order.

---

## 3. WHICH ARM BREAKS FIRST ON A REAL CLIENT PDF

**The honest frame first: no real-client specimen exists, none was manufactured, and nothing below is
measured on one.** Everything here is inference from the structure of the arms and from what the synthetic
and vendor specimens did. This is the standing proof gap on FWD-4 and FWD-8 and it is why RT10-AC2 is a
judgment criterion rather than a mechanical one.

**My answer: the LABEL-NEIGHBOURHOOD leg (L2) breaks first, and it breaks by refusing rows that are
correct.** The reasoning:

1. **L2 is the leg that already needed re-engineering once for layout.** The comment in `certify.py` records
   that a fixed-width neighbourhood box failed 30 of 34 correctly-located rows on one layout and swallowed
   neighbouring labels on the other; it is now defined by the value's own TEXT ROW plus a shallow band
   above. That is robust to column width but **not** to a label that wraps onto two lines, which a real
   client name or a longer holding description will do and which these specimens never do.
2. **Every other leg degrades more gracefully.** L1 (value at coordinates) compares renderings and is layout-
   independent. L3 (units) reads the census and cannot be broken by a document. L4 (date provenance) depends
   only on the vertical order of date lines, which is a property of the vendor's template rather than of the
   client's data.
3. **The extractor's LOCATION step fails before certification even runs, and fails safe.** A field the
   census names that a real document renders differently comes back `UNLOCATED_ON_PAGE` -- a named absence,
   not a wrong number. Round 1 measured this failure mode at 58 of 58 fields when page hints were treated as
   an index, and the remedy (search hinted pages first, then the rest) is in place.

**The second thing to break, and the one with the worse consequence:** the `NON_SCALAR_UNITS` refusal. The
comment in `extract.py` records that a list value rendered across a column boundary produced overlapping
glyph runs and the extractor took fragments (`8,`, `6,`) as values -- **and they CERTIFIED, because those
characters really are at those coordinates.** The current defence is to refuse `list` and `table` units
outright. A real client document with more holdings will have more and longer wrapped values, and the
failure is invisible to every certification leg. I would put a reviewer's attention there before anywhere
else in this cell.

**What would NOT break, with reasons:** the glyph machinery. It reads whatever font resources a document
declares and exhausts them; a document with no ToUnicode, a different subsetter, or an embedded `cmap` table
is handled by a different branch of the same function rather than by a new rule. A real client PDF from this
vendor would use the same generator and differ only in its content.

**What I cannot say anything useful about at all:** whether a real client PDF contains section types the
field census does not name. `discover_uncensused` lists them as a discovery rather than inventing fields,
which is the right behaviour, but the SIZE of that list on a real document is exactly the thing three
synthetic-holdings specimens cannot tell anyone.

---

## THE STANDING PROOF GAP, ONCE MORE, UNHEDGED

Every specimen in this cell is one of: three real YCharts documents generated from **synthetic holdings**
(portfolio 2332257, SPY/AGG), three census-generated PDFs, or one hand-built fixture. **No representative
real-client document exists in this estate.** Nothing in the battery output or in this record is a
certification against real client input, and no arm here should be read as evidence that one has occurred.
