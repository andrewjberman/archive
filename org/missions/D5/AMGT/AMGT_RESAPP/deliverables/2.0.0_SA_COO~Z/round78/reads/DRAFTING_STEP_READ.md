# READ 2 -- the drafting step: why the drafted Recommendation face is never a recommendation

Read for `2.0.0_SA_COO~Z`, AMGT_RESAPP round 78, 2026-10-07. Ruling:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_AMGT_RESAPP_ROUND78_CALLS_AT_THE_CUT_20261007.md`, "The draft
(producer): one read first". Workspace HEAD at the read `3366536af5`. Script:
`round78/checks/r78_read_drafting_step.py`; its literal output `round78/reads/drafting_step_read_output.txt`; every
row `round78/reads/DRAFTING_STEP_READ.json`.

## The answer in three lines

1. **Nothing asks for a recommendation.** The model is asked for six classes of finding from the company's own annual
   filing, and the "recommendation" section is filled by a fixed mapping from one of them: GUIDANCE, "the company's
   own forward statements". The two prompts hold 0 recommendation words.
2. **The face is the first GUIDANCE finding that quotes the filing.** 12 of 12 faces are exactly that, and 12 of 12
   recommendation sections hold GUIDANCE findings and nothing else.
3. **No stored draft holds a recommendation anywhere.** 0 of 63 served sentences, 0 of 26 held ones, and 0 of 897
   findings across all six classes in the 12 stored analyses state a view on the shares (7 carry a listed word; read
   by eye, none is a recommendation).

## What the step is asked for

There is no separate drafting model call. The filing analyzer makes two model calls per filing
(`lib/research/filings/analyze.py`), and the drafted document is laid out from its stored result by plain code
(`lib/research/filings/drafting_build.py`, class `FilingsProducer`: "NOT A MODEL CALL", `:276-281`).

| what | where | text |
|---|---|---|
| the first prompt's opening | `analyze.py:151-155` | "You are the filings analyzer for an internal research page read by one analyst. ... From the attached excerpt of this company's own annual filing, write findings under these six headings" |
| the six headings | `analyze.py:158-163` | GUIDANCE, SEGMENTS, RISKS, COMMENTARY, BIG BETS, BIG CHALLENGES (then THESIS DRIVER, `:167`) |
| **the instruction behind the recommendation section** | `analyze.py:181` | "- GUIDANCE findings are the company's own forward statements: outlook, targets, expectations, rates." |
| what a finding may be | `analyze.py:174-175` | "Each finding is ONE sentence of at most 45 words, and states something the excerpt actually says." / "CITE THE DOCUMENT FOR EVERY FINDING. A finding you cannot cite is a finding you must not write." |
| the second prompt | `analyze.py:237-271` | turns the notes into JSON; `class` is one of the six (`:250-251`) |
| the section mapping | `drafting_build.py:66-72` | `"recommendation": ("guidance",)` (`:71`); the module's own table says "recommendation        guidance" (`:20`) |
| the generic producer's stance | `lib/research/drafting/producer.py:85-89` | "A recommendation is Adam's editorial judgment, not a machine synthesis from one headline -- left for editorial"; it returns an empty list |

- Recommendation words in the first prompt: 0. In the second: 0. (The word rule of `r78_bb6.py`.)
- The word "recommendation" appears in `analyze.py` 0 times (Grep, this session). It enters only as a section NAME
  in `drafting_build.py` and `lib/research/drafting/pipeline.py:66`.
- The 12 stored analyses were made under prompt version `rj6-two-pass/1` (12 of 12); the code at HEAD is
  `rj6-two-pass/3`. The GUIDANCE instruction is the same sentence in both (read from commit `8abfd829a7`, the first
  version, 2026-09-15). The same commit set the `guidance` mapping.

## Which inputs it is given

- **The first call:** the excerpt of ONE filing and nothing else. The excerpt is cut from two named items of the
  annual report: risk factors and management's discussion (`lib/research/filings/fetch.py:89`,
  `EXCERPT_ITEMS = {"10-K": ["risk", "mdna"], "20-F": ["risk", "mdna"]}`).
- **The second call:** the first call's own notes.
- **Not given, to either call:** a share price, a valuation, the research team's model or cases, a price target, the
  peer set, news. So nothing the step reads bears on whether to own the shares.

Excerpt items of the 12 stored analyses (`source.excerpt_items`):

| excerpt | analyses |
|---|---|
| Item 1A Risk Factors + Item 7 Management's Discussion (10-K) | 6 |
| Item 7 Management's Discussion only (10-K) | 1 (HAL) |
| Item 3.D Risk Factors + Item 5 Operating and Financial Review (20-F) | 3 |
| Item 3.D Risk Factors only (20-F) | 2 (ASML, PBR) |
| sum | 12 of 12 |

ASML's analysis was made from risk factors alone and holds 12 findings, 2 of them GUIDANCE. That is why its face is a
sentence about the Dutch governance code: it is the only GUIDANCE finding that passed.

## Which sentence goes on the face, and by what rule

1. `FilingsProducer.draft` (`drafting_build.py:289-329`) lays out the analysis's GUIDANCE findings in the model's own
   order, at most 10 a section (`SECTION_LIMIT`, `:77`).
2. The verbatim gate keeps a sentence only if it carries a run of the filing's own words that clears the passage it
   cites; a sentence with no such run is held, never served (`lib/research/drafting/pipeline.py:46-58`; the adapter
   holds again at read, `lib/research/api/scoped_amgt.py:2960`).
3. The page shows the first sentence left: `sentences[0].text`
   (`portal/src/pages/SecurityAnalysis/components/ThesisCards.tsx:433`).

So the face is the first GUIDANCE finding, in the order the model wrote them, that quotes the filing. Measured:

| | names |
|---|---|
| stored drafts read, each with its analysis | 12 of 12 |
| recommendation sections whose every sentence is a GUIDANCE finding of the analysis | 12 of 12 |
| faces that are the first GUIDANCE finding carrying a quoted span | 12 of 12 |

| name | form | GUIDANCE findings | in the section | held, no quoted span | the face is GUIDANCE finding |
|---|---|---|---|---|---|
| ASML_NA_Equity | 20-F | 2 | 1 | 0 | #2 |
| BABA_US_Equity | 20-F | 10 | 9 | 0 | #1 |
| BA_US_Equity | 10-K | 15 | 9 | 1 | #1 |
| COST_US_Equity | 10-K | 10 | 4 | 6 | #2 |
| HAL_US_Equity | 10-K | 14 | 3 | 1 | #2 |
| HD_US_Equity | 10-K | 10 | 3 | 5 | #1 |
| INTU_US_Equity | 10-K | 10 | 10 | 0 | #1 |
| KMB_US_Equity | 10-K | 12 | 7 | 3 | #1 |
| NU_US_Equity | 20-F | 10 | 1 | 2 | #7 |
| PBR_US_Equity | 20-F | 10 | 6 | 1 | #3 |
| SAP_GY_Equity | 20-F | 8 | 5 | 3 | #3 |
| VLO_US_Equity | 10-K | 12 | 5 | 4 | #4 |
| sum | | 123 | 63 | 26 | |

The 63 equals the count of served sentences in `round78/reads/RECOMMENDATION_CARDS.json`. The 12 face sentences are in
`drafting_step_read_output.txt`, one per name.

## Do the stored drafts hold any recommendation at all

The word rule of `r78_bb6.py` (buy, sell, hold, overweight, underweight, outperform, underperform, accumulate,
recommend, rating, rated, price target, upside, downside, attractive, valuation, undervalued, overvalued, own the
shares, add to, trim, conviction), over four populations:

| population | with a listed word | of |
|---|---|---|
| the 12 faces | 0 | 12 |
| recommendation sentences the page serves | 0 | 63 |
| recommendation sentences held for no quoted span | 0 | 26 |
| sentences of all five sections of the 12 drafts | 1 | 210 |
| findings of all six classes in the 12 stored analyses | 7 | 897 |
| analyses whose stored first-pass text holds a listed word anywhere | 4 | 12 |

The 7 findings, read by eye. None states a view on the shares:

| name | class | word | the finding |
|---|---|---|---|
| BABA | risks | buy | "... investors buy shares of a Cayman holding company rather than the operating entities." |
| BABA | big_bets | sell | "... having agreed in May 2025 'to sell 85% of the equity interest in Trendyol GO ...'" |
| BA | risks | rating | "Boeing has experienced credit rating downgrades before ..." |
| BA | commentary | rating | "Boeing 'currently maintain[s] investment grade credit ratings across all three credit rating agencies' ..." |
| HAL | risks | valuation | "... an additional valuation allowance of $125 million was recognized on deferred tax assets ..." |
| HAL | big_challenges | valuation | "... income tax forecasting, legal matters, long-lived asset valuation and credit loss allowances." |
| KMB | commentary | valuation | "The effective tax rate rose to 29.2% from 18.3%, primarily due to a valuation allowance ..." |

By class: risks 3, commentary 2, big_bets 1, big_challenges 1, guidance 0. The one hit among the 210 section
sentences is the first BABA row, served in the risks section. The 4 analyses whose first-pass text holds a word are
the same four names.

**So: 0 of 897 findings is a recommendation.** The drafts do not hold one that the display is hiding; there is none
to promote to the face.

## What would have to change for a drafted recommendation to be one

Stated from what was measured, and no further:

1. **The step would have to be asked for one.** Today no instruction asks for a view on the shares; the section is a
   relabelled list of company guidance (`drafting_build.py:71`).
2. **It would have to be given something a recommendation can rest on.** Its only input is the risk and management
   discussion items of the company's own annual filing. A filing does not say whether to own its shares, and the
   prompt forbids writing anything the excerpt does not say (`analyze.py:174-175`).
3. **The gate, as it stands, would hold it.** Only a sentence carrying a run of the filing's own words is served. A
   sentence of judgment written by the model has no such run and is held (26 GUIDANCE findings are held today for
   that reason alone).

The other way to make the card true is to change nothing in the step and stop calling its output a recommendation:
what it holds is the company's stated guidance. Which of the two is wanted is not this read's call.

## NOT MEASURED

- **No model was called.** What the model WOULD write if asked for a recommendation is not known.
- **The prompt text of version `rj6-two-pass/2`** was not read; versions 1 and 3 were, and the GUIDANCE line is equal
  in both.
- **Why some of the first ten GUIDANCE findings are neither in the section nor held** (for example NU: 7 of 10; HAL:
  6 of 10). They were refused by the gate or dropped; the script counts them (`guidance_first_ten_split`) and does
  not say which.
- **The word rule is a word list.** A recommendation phrased with none of the listed words would be missed by the
  count. The 12 faces were read by eye (none is one); the 897 findings were not all read by eye, only the 7 hits.
- **The rendered page** was not opened. The face rule is read from `ThesisCards.tsx:433` and the served body.
- **The research team's own base case** (`model.team_cases`) is outside this read.
