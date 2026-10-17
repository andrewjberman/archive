# AMGT_RESAPP round 111 -- the LIVE site tied to PROD `932cea99` by bytes (rule 22 grain), `2.0.0_SA_COO~R1`, 2026-10-17 ~19:0xZ

Closes the "not verified" line of `round111/DRAIN_END_PACKET.md` (the live site tied by bytes). Same method as `round110/PROD_READ_FWD40D.md`. Evidence outside the repository: `C:/dev/ui-walk-evidence/r111-close/{ci-artifact,live}/`.

1. **The run.** `gh run view 39057551567 --repo Opal-Capital/portal`: `headSha 932cea99e8cabffa7ca28d2d57aba1e923d4e591`, status completed, conclusion success; jobs `Build Production Assets`, `Deploy to S3 + CloudFront`, `Tag Deployment` all success.
2. **The artifact.** `gh run download 39057551567 -n production-build`: `index.html` names `assets/index-B3Hs_TIj.js` (main), `index-B4RDE4Kd.css` and four vendor bundles; the chunk holding the Security Analysis page code is `assets/index-CZ3eT7d6.js`, which contains the string `a vendor figure` (br-3's `plainPeReason` safety-net word, count 1).
3. **The live site.** `https://www.opalinvest.dev/index.html` (`Last-Modified: Sat, 17 Oct 2026 18:21:20 GMT`): **byte-equal to the artifact's** `index.html`; the main bundle (355411 bytes), the CSS (307279), the four vendor bundles and **`assets/index-CZ3eT7d6.js` (250068 bytes)** are each byte-equal to the artifact's (`cmp` clean); the marker count in the live chunk is 1.
4. **Negative control.** The artifact of the PREVIOUS deploy (run 39042189942, kept from round 110): its main bundle is `assets/index-CsNr8AoK.js` (a different name), and **0** of its chunks contain `a vendor figure`. The comparison discriminates.

**Reading:** the live PROD site serves the production build of run 39057551567, whose head is `932cea99`, carrying the three round-111 features (a content-level marker of br-3 is in the served chunk). The tie is by bytes and by name, not by a served version string. **Not done:** a live page read with a staff login (the walker is guarded to a localhost base).
