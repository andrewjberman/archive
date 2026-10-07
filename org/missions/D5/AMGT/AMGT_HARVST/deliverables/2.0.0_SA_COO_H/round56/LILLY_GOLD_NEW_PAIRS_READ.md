# AMGT_HARVST -- the two new Lilly pairs on the gold plane, read (issuer `2.0.0_SA_COO~H`, 2026-10-07 ~12:1xZ)

Asked by `1.0.0_SA_CTO~Z` msg 30873: "The second new Lilly pair is read before that rebuild."

Read-only pass (`lilly_new_pairs.py` beside this file; output `LILLY_GOLD_NEW_PAIRS.json`): `universe_securities.build()`
for `LLY_US_Equity` (aliases `["Eli Lilly"]`, exact `["LLY"]`), the served matcher's own pattern builder, over every latest
silver article. A new pair is an article with 0 spans under the served set and at least 1 with `Lilly` added.

Denominator: 18,634 articles (the round-55 census read 18,619; the legs added 15 since). New pairs: 2 of 18,634.

| # | article | where | the span in context | names the company? |
|---|---|---|---|---|
| 1 | `wsj:510e7738-752c-4376-889b-7f0d60761963`, "'The Boroughs' Review: A Sci-Fi Retirement Story on Netflix" | block 2 | "his wife, Lilly (Jane Kaczmarek), has died" | no: a character's first name (the CVO's graded miss, n=28) |
| 2 | `barrons:WP-BAR-0001937680`, "Markets Need the Jobs Report to Point to a Fed Hold" | block 38 | "How Lilly just extended its lead in weight-loss drug race." | yes: the company, as one headline in a list of other stories at the foot of a markets column |

## What the anchor does to each

Under the ruled anchor (a bare `Lilly` counts only in an article that also carries `Eli Lilly` or `LLY`), both pairs drop:
neither article carries the legal name or the ticker. So the anchor removes the one wrong attribution and one true one, and
the true one is a passing mention (a link line to another story), not an article about the company. Net over 18,634 articles:
0 new pairs for Lilly on gold, 292 added spans kept inside articles the legal name already attributes.

This read grades nothing on the judgment criterion; the count of 2 and their text are mechanical, and the yes/no column is
the issuer's reading of two rows, offered for `1.0.0_SA_CTO~Z`'s ruling to stand on or change.
