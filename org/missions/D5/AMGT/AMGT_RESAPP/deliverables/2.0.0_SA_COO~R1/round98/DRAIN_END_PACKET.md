# AMGT_RESAPP round 98 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~22:5xZ. Two orders, both complete: `AMGT-be-1` (the ONE redeploy from a MERGED pin carrying AMGT_CORPUS's /13 files, bd-1's serve kept; `opal-amgt-scoped-api`
`IpaCHo5h..` -> `mbGRmy1Hnh7M6Gtt9LchHPmt17lYS/oyCl6s10lJO+w=`, APPLIED and HELD under the CTO's KEEP) and `AMGT-be-2` (a read-only reading: which portal build reads which Thesis payload
key); `be-3` (pp-4) STAGED, no order.** Round 98 implements the CTO~DELL1 round-97 analysis `ledger/ROUND_ANALYSIS.round97.md` (msg 4123); decomposition s.106; issuance @23479c4c14. No
amendment. `round-close-check.py --round 98`: orders 2, proof_ok 2 of 2, judgment 1, ungraded 1, **verdict REFUSED until the CVO grades `be-2` AC2** (one JUDGMENT criterion).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-be-1` | 1: the /13 corpus redeploy from merged pin `a03d92221a`; bd-1's `scoped_amgt.py` `9b13bf0371d4` and `monthly_chatter.py` `38e9511ccc9c` unchanged; retires both scratch pins | complete, SERVED: applied 2026-10-11T22:14:54Z (LastModified 22:15:23Z) by `0.7.0_AE_CloudOps~RA1`, commit f339236817, ledger `amgt-resapp-r98-be1-corpus13-redeploy-dell1` CLOSED, proof VALID | pair `ledger/NEVER_WIDEN_ROUND98_CORPUS13_REDEPLOY_{COO,CTO}_HALF.md` (COO @926aa022b4, CTO msg 4135, ADDENDUM 1 KEEP msg 4153) |
| `AMGT-be-2` | 2: which of top-level `fiscal_year_figures`, `model.fiscal_year_figures` and `check_face` each portal build (DEV, PROD) reads | complete, merged @95ba1a1dae, proof VALID; AC2 UNGRADED (the CVO's) | worker ~394 @5722cc350b; reading `deliverables/0.9.0_WK_AMGT_RESAPP~394/BE2_PAYLOAD_KEY_READING_20261011.md` |
| `AMGT-be-3` | 3: the DEMQUE answer's reader (pp-4) | STAGED, no order | no quote, no answer; row `MDPF_DEMQUE-D1-S10` stands |

## 2. The issuer's ONE REAL RUN at close

- **be-1 (SERVED, WORLD): re-run by the issuer on the live function after the apply, not RA1's report.** `r98_thesis_fullbody_compare.py --after local` (the live function against the PIN's
  own handler, 95 names, all 200): **0 paths under `model.team_sheet`**, 4 generation clocks, 18 `float_repr` (the measuring checkout's Python 3.14 printing a request-time sum that the live
  Python 3.11 prints as it did before: the same 10 names, the same paths, as predicted before the apply), 0 other: `R98 THESIS FULLBODY: YES`. The deployed censuses read YES:
  `r97_sector_serve_census.py` 6 of 6, `r95_classification_census.py`, `r94_name_census.py`; and `r89_peers_deployed.sh`, `r89_deployed_close.sh --want amgt-corpus-dossier/13`,
  `r92_minor_unit_census.py`, `r95_casing_deployed.py` all YES.
- **C1's post-act read (msg 4144, an independent seat):** `aw4 names 95 team_sheet_equals_stored13 95/95 others_equal 95/95 max_response_bytes 1289805 (AZN_LN_Equity) margin_to_6MB 5001651
  over_6MB 0 growth_exceeds_delta 0`; `aw4 compare build 1/1`; rendered census on the live payloads 0 of 11,467 FIGURE rows unmapped. SNPS US did NOT exceed its delta live: the 11-byte
  excess seen in my prediction was the measuring runtime's float print, as the CTO's half read it.
- **RA1's compare** (`BE1_POST_APPLY_COMPARE_20261011.json`, a 527-request route baseline): second replay with no concurrent capture: status moved 0; 981 `team_sheet` paths on 10 subjects, 36
  clocks, 0 outside the table, 0 `float_repr`.
- **be-2 (LOCAL): re-run by the issuer.** `r98_payload_key_reading_check.py` 8 of 8 YES on the merged file; `git grep` of `origin/DEV` `44ec7e70a9` and `origin/PROD` `37aa1247ee` reproduces
  the worker's sites: top-level `fiscal_year_figures` (ModelTab.tsx, postureCites.ts) and `check_face` (ModelTab.tsx) are read by BOTH builds; `model.fiscal_year_figures` is read by neither as
  a property, only as footer string paths (CardFooter.tsx:187-188), entries of union lists that also name the top-level path.

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **My own live sweep overlapped RA1's first post-apply replay and a single overlay request timed out (29 s, 22:18:37Z).** I ran the whole-body thesis compare (4 threads of live invokes,
   ~22:16-22:18:41Z) while RA1 and C1 were capturing against the same function. RA1 read it as a Branch 2 literal and stopped; the CTO named KEEP (msg 4153) on byte-identical re-reads,
   an unchanged latency distribution and 0 overlay paths moved, and the second replay (no concurrent capture) read the table. **Cost: a STOP-class round-trip and about 20 minutes of RA1's
   window (STOP 22:27Z, KEEP 22:29Z, complete 22:46Z); the cause is a candidate, not proven.** The control I now keep: no live sweep of mine runs while an applier's replay or a peer's capture is open on the same function; my
   post-act re-run uses the pin's handler (local) beside ONE live read, announced to the applier.
2. **The AMGT_CORPUS half cites a stale PROD ref** (`origin/PROD` 18364342; the portal's PROD ref is `37aa1247ee`). Immaterial to its reading (the PROD-built page reads `team_sheet` in 0
   files at both refs) but the citation aged separately from the text it quotes; named to its author.
3. **My first reading-shape check had a tuple-formatting defect**, caught by its own dry run against a sample before the cut (cost: one edit). Reused arms were all run against a candidate
   before the cut this round (the round-97 lesson held).

## 4. JUDGMENT for L9

`be-2` AC2 (the CVO's): the three OUTCOME lines (all READ-BY-BOTH) follow from the evidence, the control (`team_sheet`: DEV 2, PROD 0, so the sweep distinguishes the builds) and the surfaces
named; READ-BY-NEITHER was not claimed anywhere, the built bundles are named NOT READ. Offered for your own re-run: `git grep -n -e fiscal_year_figures -e check_face origin/DEV -- src` and
the same for `origin/PROD` in the nested portal, and `r98_thesis_fullbody_compare.py --after local` (one live read per name; announce it to the applier first).

## 5. Rows filed this round

Worker: `AMGT_RESAPP-D1-W394-S1` (OBSERVATION, INERT: the model-block key is read only as string paths) and `S2` (OBSERVATION, INERT: `CardFooter.whatChangedSources` has no caller in either
build). RA1: none. Issuer: none. **Disarmed by this round:** none open.

## 6. For the next round (the ENRICHMENT LIST's inputs; the CTO's rulings at msgs 4139, 4140, 4153)

1. **The `/14` served effect, the SECOND redeploy (AMGT_CORPUS ax-7, CTO half signed msg 4140):** a merged pin with bd-1's two blobs unchanged and `dossier.py` at `6c4529c51a13`
   (`team_sheet.py` `3ba68a99a22f`, `factset_descriptions.json` `690950020aa5`, `template.py` `e03d6a8acf65`); baseline the function `mbGRmy1H..`; only its 252 rows' label, claim and cite
   move; post-act read live vs live, growth within each name's `/14` delta, 0 paths outside `model.team_sheet`, under 6 MB; FWD-20's rendered census follows.
2. **The overlay tail over 20 s per name over a day of real traffic** (CTO msg 4153), read before any remedy; AMGT_CORPUS FWD-12/20's rendered census on DEV follows the post-act read.
3. **The payload duplicate (CTO msg 4114), after the reading:** the top-level `fiscal_year_figures` and `check_face` are read by both builds and stay; `model.fiscal_year_figures` is read
   only through the footer's union lists. A removal needs a read first: the 95 names' `model.fiscal_year_figures` equal their top-level `fiscal_year_figures` on the footer's fields
   (`vintage`, `source`), then the drop under its own pair.
4. **CSL AU's sector reads as of 2026-09-30** (served with its date; whether a stale vintage is withheld past some age is the CTO's call).
5. **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6`, the portal PROD promote (`dell1-20261011T033643Z-e7f2`), FWD-16 and the model API key stay Andrew's.

checked 2 of 2 orders terminal, 2 of 2 proofs VALID, 1 judgment criterion ungraded (be-2 AC2)
