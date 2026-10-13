# STAGED enrichment item -- the derived article-link view (AMGT_HARVST, staged 2026-10-13 by `2.0.0_SA_COO~W1`, NOT cut)

**Why staged and not cut:** round 84 is in the drain; the spec and the decomposition are frozen mid-round (CLAUDE.md rule 27). This item rides the round-84 L10
and is cut in the first issuance after it, if the CTO's analysis lists it.

**Source of the item:** CTO ruling F3 on `org/tier1_exec/1.0.0_SA_CTO/deliverables/SERVABLE_PREFIXES_OPAL_DATA_HARVEST_20261013.md` (msg 5052): "CUT a derived link
view as AMGT_HARVST's enrichment item: url, title, publisher and date per article, no body."

**What was measured (v2 of that list):** `publication-links/v1/<security>/<publisher>/<hash>.json` (291 B) holds security_key, company, ticker, article_key,
publisher, first_discovered_at. It carries no url and no title. The url and title live in `publications/v1/<publisher>/<hash>.json` and the silver `article` tables
(`<publisher>/harvest/silver/article/`), both WITHHOLD (raw publisher text beside them).

## The cell (one chain of one)

- **Output:** one derived record per (security, article): `security_key`, `publisher`, `article_key`, `url`, `title`, `published_utc`, `first_discovered_at`. No
  `text`, no `body_blocks`, no `search_query`.
- **Address:** a NEW prefix, so a builder output of `lib/opal_naming.py address()` named in the order (CLAUDE.md rule 30), never hand-typed here. A new top-level
  or second-level prefix is WITHHOLD in the servable list until it is classed there; the cut adds its row.
- **Read side:** reads the index and the silver article table; writes only the new prefix; writes nothing under `publications/`, `publication-links/` or any silver
  table.
- **Open for the cut:** whether `title` is publisher text under Andrew's V1 rule. The CTO's F3 wording names the title as part of an "article link", so it is
  included; the same question already sits on `chatter_event.lead_headline` in the list (a one-column decision).
- **Criteria (at most three, mechanical):** (1) every record's key set equals the declared seven fields (a negative control with `text` added fails); (2) the record
  count equals the count of index records for the same securities (denominator printed); (3) a read by an asset-manager principal of one view object returns it
  and the same principal's read of the matching `publications/v1` object is refused.
- **Risk class:** SERVED (a write to the shared bucket that a served grant will read). The producer's run is site Z's, so the order is `0.7.0_AE_CloudOps~ZW`'s or
  a dell1 worker's, named at the cut.
- **Not in this item:** the grant and the catalog row (site Z, NFRA_MCPINDEX and NFRA_OPLGTW); the management view without `lusha_enrichment` (F4, AMGT_RESAPP's
  writer).
