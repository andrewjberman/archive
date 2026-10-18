# AMGT_RESAPP round 114 -- the LIVE site tied to PROD `26d998f7` by bytes, `2.0.0_SA_COO~R1`, 2026-10-17 ~23:4xZ

Evidence outside the repository: `C:/dev/ui-walk-evidence/r114-tie/{new,old,live}/`. Method as `round113/LIVE_TIE_AND_CLOSE_WALK_D1BED0FB.md`.

1. **The run.** `gh run view 39080069302 --repo Opal-Capital/portal`: head `26d998f7f34015d3ad9d70360e9135ecf5d1ddfe`, completed, success (H2's receipt: release `release/20261017T234106Z`, tag `portal-v2.1.239`, the three round-114 features `bu-1`, `bu-2`, `bu-4`).
2. **The artifact.** `gh run download 39080069302 -n production-build`: the Security Analysis chunk is `assets/index-Bi-xI0II.js` (250923 bytes), the one chunk that contains the string `data-grid-scroll-cue` (and `Scroll sideways to see every year`).
3. **The live site.** `https://www.opalinvest.dev/index.html` (`Last-Modified: Sat, 17 Oct 2026 23:44:30 GMT`): byte-equal to the artifact's `index.html` (`cmp`); the six entry assets (the files `index.html` names) each byte-equal; `assets/index-Bi-xI0II.js` byte-equal, and the marker count in the live chunk reads 1.
4. **Negative control.** The previous deploy's artifact (run 39073112254, head `d1bed0fb`): **0** chunks contain `data-grid-scroll-cue` or the cue sentence. The comparison discriminates, and a content-level marker of this round's change is in the served chunk.

**Not verified:** the live page opened with a staff login (the walker is localhost-only; the running-page read is the local build of this exact head, `CLOSE_WALK_INTEGRATED.md` section 4); a content marker for `bu-1` (a currency-code helper: minified, no string) and for `bu-2` (the long-date helper calls: no unique string); the printed pack (`AMGT-bu-7`, not yet applied).
