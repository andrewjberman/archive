# AMGT_RESAPP round 73 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`, 2026-10-06 ~05:3xZ

Round 73 is the CTO's round-72 analysis @bb75b180ab, section 4 (8 items). It ran on PRD v0.40 @d7b07c5a85, ADMITTED: FWD-1 and
FWD-18 were restated as on-demand seat acts. Issuance @1f36246bd3; decomposition s.81, with premise corrections in s.81a. **8 of 8
orders are terminal.** Deployed: `satkY3HXAhzfU7zYZ5fk+EmNHaqIRfj7bBtVlG4XfIY=`.

## 1. Orders

| order | outcome | drain / act | mechanical result (deployed satkY3HX unless named) |
|---|---|---|---|
| aw-1 | cold path (ruling 1) | @7c1c07bd20 | c51 (local) 0/0 model-block reads on the first request (from 24/25); bodies EQUAL 9/9. Names come from stored bronze refdata (no new grant). Local first request: rankings ~4.6 -> 2.5 s, chatter 7.0 -> 5.1 s. |
| aw-2 | FWD-5 print as a document | @edd7c8b57b | c48 YES: 0 unit codes, 0 long decimals, 0 reprs, 0 clipped spans over 3 prints (from 2719/86/3/742). |
| aw-3 | FWD-7 pack clock | @829ba218dd | c49 YES: 95 of 95 dated. The route now takes 10.3-11.8 s warm (row Z-S356). |
| aw-4 | FWD-7 /freshness page | @4921e89618 | Portal candidate 8adcf3f728 + hookup fb939c4a; CTO APPROVED @1434fdc5ee. **DEV push HELD** on speed (CTO @5b368c498e; ask withdrawn 04:29Z). |
| aw-5 | plain names + stored links | @9d2b7b3d7c | c50 YES: 383 names, 0 caps (from 131). The ft/wsj stored-link rule is in the producer; the gold rebuild is HARVST's (#6, CTO half @0b26f965af). |
| aw-6 | keep-prior pool universe | @fcfcef77ca | c52 YES: 95 of 95 named, 13 of 13 prior forms kept. |
| aw-7 | redeploy + pool write | close @e3da898d3b | 2lUlZomo -> satkY3HX; pool `universe/v1/2026-10-06.json` (13 kept, 51 new absent-shape); NEVER-2 7/7; no sec.gov call. |
| aw-8 | the walk (v0.40) | @cdc5184187 | FWD-31 census 42 of 42 with a reason; walker disarmed. |

The issuer's real run is `round73/REAL_RUN_r73_deployed_20261006.txt`: r73 c48/c49/c50 YES deployed, c52 YES, and r71 c38 plus r72
c39/c42/c43/c45 YES (no regression).

## 2. JUDGMENT for L9 (yours)

1. **aw-8 AC3: the walk, per FWD.** Artifact: `deliverables/0.9.0_WK_AMGT_RESAPP~251/WALK_ROUND73.md`, plus `FWD31_CENSUS.md` and
   `data/`. The captures (81 + 12 shots, 3 rendered prints) were in `tmp/ui-walk/` of the removed worktree. The worker's
   observations, with no verdict:
   - **FWD-18 (v0.40):** BA 3/3 and ASML_NA 3/3 driver-chart clicks open "The filing passage for this point is not shown on this
     page". The SERVED points carry `passage_text` (c42 YES), but the PAGE does not render it (row Z-W251-S1).
   - **FWD-31:** BABA and SAP_GY show the team passage above the roster. The roster rows are equal with and without the passage
     (7/7, 6/6); the without-arm is a local response edit, with nothing written. BA is in the absent arm.
   - **FWD-1 (v0.40):** on all 12 segment names, NO tab or disclosure draws the served `segment_breakdown`. The portal has 0
     references to it (row Z-W251-S2).
   - **FWD-5:** the three PDFs are clean by c48 but are plain monospace text with no brand styling (your judgment read).
   - **FWD-7:** the /freshness page lists 95 rows and shows the table ~12 s after load. It flags 95/95 stale (pack and web search
     NEVER), and its text is low contrast on a navy card. The sort buttons leave the first rows unchanged (row Z-W251-S3).
2. **The served-but-not-rendered pattern** (FWD-18, FWD-1) is page work: DSGN's file.

## 3. Rows (disarm_owner `2.0.0_SA_COO~Z`)

| row | standing | gist | disposition |
|---|---|---|---|
| Z-S356 | ruled | /freshness takes 10.3-11.8 s warm (~105 ledger reads per request) | DEV push held; round 74: cache or precompute, values equal on 292 rows (CTO @5b368c498e) |
| Z-W251-S1 | INERT | FWD-18: the served passage is not rendered by the page | a DSGN page item |
| Z-W251-S2 | INERT | FWD-1: the served segment breakdown is drawn by no tab | a DSGN page item |
| Z-W251-S3 | INERT | the /freshness page: 12 s, 95/95 stale, low contrast, ineffective sorts | round 74, with Z-S356, before any push |
| Z-W251-S4 | INERT | census 42 not 44; **BP/_LN and NG/_LN answer 404 on /thesis** (slash keys) | round 74: a served defect |
| Z-W245-S1, Z-W246-S1, Z-W249-S1 | INERT | raw/ ungranted (bronze used); the render_print path name; name re-casing | recorded |

## 4. Cold start (CTO ruling 1)

- **Local profile** (aw-1 PHASES.md): the names phase fell 2.5-3.4 s -> 0.7-1.5 s. The next phase is the mentions decode (~1.2-1.4
  s) and compute (~1.5 s) on chatter.
- **Deployed:** AE~A's `--label after` and AMGT_PHASE table are in the aw-7 instance @c85341be0d.
- **The CTO names the mentions decode (3.7 s) as the next cut** (round 74). Provisioned concurrency stays on Andrew's list while the
  cold read is above about 2 s.

## 5. For Andrew (cited, no new spend taken)

- **Provisioned concurrency,** if round 74's cuts leave the cold read above about 2 s.
- **The Bloomberg segment pull** for 83 names (Z-W240-S1).
- **The portal DEV push of /freshness,** once it is fast and fixed (Z-S356, Z-W251-S3).
- Carried: Z-W227-S1, FWD-2's uncovered pull, FWD-14's list owners, the analyst and PM walker accounts, and Z-S230.
