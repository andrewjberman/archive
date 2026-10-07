# AMGT_RESAPP round 74 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`, 2026-10-06 ~09:3xZ

Round 74 implements the CTO's round-73 analysis @cf0d03deb2, section 4, on PRD v0.40 (ADMITTED). The issuance is @495d89da62 and the
decomposition is s.82. **6 of 6 orders are terminal.** The function was redeployed from `satkY3HX` to
`0MZWPl7nGZzFI53w+vsKdS7hQpcxu4Mrd5wEMWWZQpA=` (08:00:43Z). Gateway `7k3ed8px20` gained one greedy CUSTOM security route.

## 1. Orders

| order | outcome | drain / act | mechanical result (deployed 0MZWPl7n unless named) |
|---|---|---|---|
| ax-1 | /freshness fast (ruling 3a) | @467456684e | c53 YES warm 646-679 ms (from 10.7-11.3 s). EQUAL 302 of 302 rows. A 60 s hold at the route, with ledgers read 16-wide on a miss. **The miss is 7.5 s: see 4.** |
| ax-2 | /freshness page (ruling 3b-3e) | @5378ac7af5 | Portal candidate `6de76f0509` (on fb939c4a), not pushed. 14 bun tests pass. Never-collected input stated once; brand tokens; the sorts reorder. |
| ax-3 | mentions-decode cut (ruling 5) | @aaed0da1f7 | c54 local YES at 307 ms (from 1,290). Deployed cold decode 3,720 -> 278 ms (AE~A). Bodies EQUAL 3 of 3. |
| ax-4 | FWD-5 Opal Brand print (ruling 2) | @55b7a7b626 | c56 YES: 3 of 3 prints Lato 1.00; 1 description, 1 current market cap, 0 raw markers; c48 floor 0. |
| ax-5 | redeploy + slash-key route | close @96b952efbe | Item 0 packaged the fonts; the build-only had left them out. CONTENT-DIFF CHANGED 5 + ADDED 3: the fifth, `publication_gold.py`, came from HARVST after the pin and was accepted by both halves (COO @d58a7907c4, CTO @8ded0241cd). Two STOPs, each ruled. c55 YES: 11 routes, 1 greedy; BP/NG 16 of 16 200. Proof VALID; NEVER-2 closed. |
| ax-6 | the walk | @46094b6b0f | 3 PDFs; walker disarmed; DISARMED relayed to MSTR~Z. |

The issuer's real run is `round74/REAL_RUN_r74_deployed_20261006.txt`: **12 of 12 YES**. That is r74 c53/c55/c56; r73 c48/c49/c50; r72
c39/c42/c43/c45; r71 c38 (9 Lead Panel reads under 2 s warm) and c35. Feed items with a url: 657 of 657, since HARVST gold #7
filled ft/wsj from the stored own-host links.

## 2. JUDGMENT for L9 (yours)

1. **ax-6 AC3: the walk, per FWD.** Artifact: `deliverables/0.9.0_WK_AMGT_RESAPP~256/WALK_ROUND74.md` and `print/` (3 PDFs). The
   worker's observations, with no verdict:
   - **FWD-5 (`:521-525`):** BA 23 pp, AMD 25 pp, ASML_NA 26 pp. Lato Regular 9 pt body; Lato Bold 11/14 pt headings; navy #163372 ink;
     hairline rules. No logo and no images. One "Label: value - as of <date> - Bloomberg" line per field, single column. 0 raw codes.
     **Row Z-W256-S1:** Recommendation, Investment thesis and Risks read "not written" in all three prints, while the BA page shows
     drafted cards. Every "as of" reads 2026-10-06, including the fiscal-year 2016-2024 lines.
   - **FWD-7 (`:539-542`):** /freshness lists 95 rows, light ground and dark text. First row at 9,135 ms on a cold load and 1,993 ms on
     the second visit. **95 of 95 flagged stale**; every Last refreshed reads 2026-10-04, so no stale name stands out (row Z-W256-S2).
     The flags are real: Seeking Alpha has never been read for 92 of 95 names (ax-2 row S2, ruled).
   - **FWD-4 (`:505-507`):** BA 72 of 78 feed items carry a url at the walk (gold #6). One link-out was followed to the barrons.com
     target with `target=_blank` and stopped there. Since then gold #7 has filled ft/wsj (657 of 657 deployed).
2. **ax-2 AC2:** the /freshness page render. `deliverables/0.9.0_WK_AMGT_RESAPP~253/render_freshness.txt` is over a deployed body;
   the walk's 9 captures are of the live page.

## 3. Rows (disarm_owner `2.0.0_SA_COO~Z`)

| row | standing | gist | disposition |
|---|---|---|---|
| Z-S356 | ruled | /freshness slow | warm fixed (646-679 ms); the miss is not (section 4) |
| Z-S357 | ruled | the targeted plan could not see the route-count guard | grading moved to an untargeted plan (AMENDMENT 2) |
| Z-W253-S1 | INERT | the pack-field premise did not reproduce | recorded |
| Z-W253-S2 | ruled | 95 of 95 stale | correct: Seeking Alpha is unread for 92 names |
| Z-W255-S1 | INERT | the Lato extraction artefact in the `.txt` | recorded |
| Z-W256-S1 | INERT | the print omits the drafted thesis/risks/recommendation; every "as of" reads today | for the round-75 analysis |
| Z-W256-S2 | INERT | /freshness gives no stale name prominence; 9.1 s cold | for the round-75 analysis |

## 4. /freshness: the cache miss, measured by the issuer after the walk

One direct invoke after ~28 minutes idle: **handler 7,488 ms** (Init 653 ms), 10.6 s end to end, body 2,850,172 B. The warm call right
after took **68 ms** in the handler and 599 ms end to end. The body carries no Content-Encoding from the function; CloudFront compresses
at the edge.
- **So the 60 s hold serves only a repeat visit within a minute.** A first visit pays ~7.5 s, which is what the walk saw (8.1 s read).
- **The remainder is the miss path** (the pack ledgers, 16-wide) and a 2.85 MB body for 302 rows, of which 95 are covered.

## 5. Cold start (CTO ruling 5)

- Deployed mentions decode 3,720 -> 278 ms (AE~A's phase table).
- The cold chatter read is still **3.7-4.7 s**, above about 2 s, so provisioned concurrency stays on Andrew's list.

## 6. For Andrew (cited, no new spend taken)

- **Provisioned concurrency:** the cold chatter read is 3.7-4.7 s, and a /freshness miss is 7.5 s.
- **The portal DEV push of /freshness** (candidate `6de76f0509`), after a CTO review from a render. Its precondition, warm under 2 s,
  is met; the first-visit time is not.
- Carried: the Bloomberg segment pull for 83 names (Z-W240-S1), Z-W227-S1, FWD-2's uncovered pull, FWD-14's list owners, the analyst
  and PM walker accounts, and Z-S230.
