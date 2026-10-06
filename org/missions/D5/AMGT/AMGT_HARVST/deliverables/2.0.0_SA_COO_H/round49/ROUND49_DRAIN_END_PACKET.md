# AMGT_HARVST -- ROUND 49 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-06 ~09:0xZ

**Round:** the round-48 analysis enrichment list (`ledger/ROUND_ANALYSIS.round48.md` @6d005e5261). Decomposition section 62, issued
@4a6e9000b8. **Class: LOCAL + SERVED.**

## 1. The cells

| cell | result | evidence |
|---|---|---|
| census at the cut | ft 171/185 stored records carry `html_meta["og:url"]` and 14 a top-level url; wsj 448/463 carry og:url + `articleData.sourceUrl` and 15 a top-level url. The sets are disjoint; their union is every stored article. Read-only, no publisher contact. | decomposition section 62 |
| `HVST-av-1` | **COMPLETE.** Worker ~98 @da3c89dc54 + @19839a8923; merged @a44bc80e9d. `article_url` for ft/wsj takes the top-level url, else the stored og:url, else wsj sourceUrl, accepted only on the publisher's own host (nothing constructed, nothing fetched). AC1 6/6; AC2 research harvest 361. | task order record face; `0.9.0_WK_AMGT_HARVST~98/av-1.link_census.out` |
| `HVST-av-2` | **DONE: served gold rebuild #7** under COO @0a1f637d71 + CTO @0666944946; NEVER-2 opened and CLOSED. Mention `part-20261006T082836Z`: 33,665 rows, url on **33,665** (ft 930/930, wsj 880/880). Daily `part-20261006T084420Z`: identical. VERIFY holds; no rollback. | `round49/av-2.act_20261006T075616Z.json`; `NEVER_WIDEN_HALF_COO_GOLD_REBUILD7.md` |

**av-1 census:**
- ft 185/185 with a link (14 top-level, 171 og:url);
- wsj 463/463 (15 top-level, 448 og:url; og:url == sourceUrl on 448/448);
- refused for a foreign host: 0.

**av-2 numbers:**
- url-fill (e): 1,746 (ft 900, wsj 846);
- every other field and row: unchanged (gone 0, changed 0, added 0).

**The ruling's byte-equality proof:** it could not run as written. The 64 articles that carry a stored top-level url and the
articles that carry og:url are DISJOINT sets, so no article holds both. The proof run instead:
- the og:url form is the publisher's own canonical form (`https://www.ft.com/content/<uuid>`; `https://www.wsj.com/...`), the
  same form as the stored urls;
- wsj og:url equals sourceUrl on 448 of 448.

**The resume** is not a cell; it waits on Andrew (Z-S89). Every collection leg is stopped.

## 2. For the CVO

- **To grade:**
  - FWD-4 links: every served mention row now carries the link to its original;
  - av-1 (plants + census);
  - av-2 against its signed rule.
- **Still a qualified wait:** the collection outcomes.
- **Surprise rows this round:** none.

Push: read at send time.
