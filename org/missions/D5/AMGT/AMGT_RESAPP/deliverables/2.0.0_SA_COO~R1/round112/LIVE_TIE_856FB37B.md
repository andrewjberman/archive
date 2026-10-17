# AMGT_RESAPP round 112 -- the LIVE site tied to PROD `856fb37b` by bytes (rule 22 grain), `2.0.0_SA_COO~R1`, 2026-10-17 ~19:5xZ

Same method as `round111/LIVE_TIE_932CEA99.md`. Evidence outside the repository: `C:/dev/ui-walk-evidence/r112-tie/{new,live}/`.

1. **The run.** `gh run list --repo Opal-Capital/portal --branch PROD`: run 39064168223, `headSha 856fb37b785c4b8a10190771410e3dfc9ac8e789` (the release merge of `cand/dell1/amgt-sa-price-currency-rule`, PROD's only commit since `932cea99`: `git log 932cea99..origin/PROD` lists the feature commit `937f15a0` and the release merge), status completed, conclusion success.
2. **The artifact.** `gh run download 39064168223 -n production-build`: `index.html` names the main bundle `assets/index-CwNezb8b.js`; the chunk holding the Security Analysis page code (found by br-3's string `a vendor figure`) is `assets/index-Xr7bGoAp.js` (249963 bytes).
3. **The live site.** `https://www.opalinvest.dev/index.html` (`Last-Modified: Sat, 17 Oct 2026 19:52:41 GMT`): **byte-equal to the artifact's** `index.html`; the six entry assets it names (the main bundle, the CSS and the four vendor bundles) are each byte-equal to the artifact's (`cmp`); **`assets/index-Xr7bGoAp.js` is byte-equal** to the artifact's.
4. **Negative control.** The artifact of the PREVIOUS deploy (run 39057551567, head `932cea99`): its main bundle is `assets/index-B3Hs_TIj.js` (a different name) and its Security Analysis chunk is `index-CZ3eT7d6.js` (250068 bytes), whose bytes differ from the new chunk's. The comparison discriminates.

**Reading:** the live PROD site serves the production build of run 39064168223, head `856fb37b`, carrying the round-112 price-currency-rule feature. The tie is by bytes and name. **Not done:** a content-level marker of this feature in the served chunk (its change is a shared helper with no new string, so the evidence is the differing chunk bytes and the equal live bytes, not a marker); a staff-login read of the live page.
