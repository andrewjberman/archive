# MDPF_CANON round 11 -- FINAL drain-end packet, DRAFT (2.0.0_SA_COO~D1), prepared 2026-10-16 ~18:0xZ

**STATUS: DRAFT, not sent.** Sent to `3.0.0_SA_CVO` after the 2026-10-17 13:30Z gold fire and the 13:50Z publisher run are READ (sections marked FILL AFTER FIRE). It supersedes `round11/ROUND11_DRAIN_END.md` revision 2 and carries nothing the interim did not already put in front of the CVO except sections 2 to 4 below.

## 1. Orders (unchanged from revision 2 except CN-s-3 and CN-s-1)

| order | state at the final packet |
|---|---|
| CN-s-4 (the Variant 2 Models band never carried) | merged `532a25c852`; portal DEV `1d7ed40d`; AC3 graded MET (CVO v20, row C-S94); PROD at the next chosen-set promote |
| CN-s-5 | SUPERSEDED by the CTO's ruling; not landed |
| CN-s-3 (Cottonwood AUM Trend upgrade) | merged `532a25c852`, AMENDMENT 1 (carried-key labels, `7a88ca75`), AMENDMENT 2 (provenance guard, `7aefb45b`, worker merge `05c556a7d4`); portal DEV `fcbf2bce`; AC2 graded MET (CVO v21); PROD at the next chosen-set promote |
| CN-s-1 (Muni becomes "Opal Municipal Bonds", WORLD, no judgment criterion) | merged `66ae82d62d`; deployed by `ADHOC.canon-r11-muni-custom-redeploy` (ledger CLOSED 6 of 6) after a first deploy was stopped at D4 and rolled back; outcome = the fire read in section 4 |

## 2. The WORLD act and what stopped it once (MEASURED)

First deploy (`ADHOC.canon-r11-muni-custom-deploy`, GO 15:41Z): D2 16:22Z, D4 16:24Z, graded by `checks/diff_d4.py`: Cottonwood as predicted; Global `opal_aggregate_aua`, aum-metrics `total/aum` and `non_model_assets_detail.latest.enterprise_total` rose by the account's value (63.47M on 2026-10-15; 64.12M .. 63.03M on the seven dates 2026-10-07 .. 10-15) where the first never-widen pair had predicted `opal_aggregate_aua` equal and the CTO half had said headline totals cannot move. D4-STOP 16:32Z (row `MDPF_CANON-D1-S32`); rollback 16:36Z, read live by the issuer. Cause, read from the fold (`mdpf_gold_consolidator.py` L1837, `dim_mdpf_aggregate_aua_timeseries.py` L2296): Global takes a firm leg's MODEL dollars only and its `non_model_aua` is 49F non_model only, so a Cottonwood account moved into the model population adds its dollars to Global; the issuer's prediction was the error. The CTO ruled (msg 6876): accept with a new pair, no fold change. V2 pair `round11/NEVER_WIDEN_PAIR_R11_CN_S_1_V2.md` (sha256 `bccb5539...02b1`): COO half `f1d5ed7dcb`, CTO half `2055d5b2a4` (Andrew informed, not a gate). Redeploy: D2 16:52Z, D4b 16:53Z, graded `checks/grade_d4_v2.py` 11 of 11, D4-PASS 16:56Z. Live: CodeSha256 `W6/RdXMxXNQZfqkYyseS/gczQRSbw3AgRx2FhQ8xekA=`, `MDPF_GOLD_COMMIT` the full pin. D1 NOT DONE (runner modules import both gold scripts; `mdpf-code-equality` keeps printing DIFFER for those two names, a stated fact). The emitter was not touched (D2b held).

## 3. What the client-facing views now show (from the D4b bodies, before the fire)

**STALE QUALIFIER (CTO msg 6981, 2026-10-16 ~18:5xZ):** `mdpf-feeder-trigger` has not dispatched the feeder chain since 2026-10-12 (7 of 10 trading days; ADVI_FIRMBKTS B1 owns the fix and a catch-up for 10-13 to 10-16). Every ABSOLUTE Global level below for 2026-10-13 .. 10-16 (total AUM, model AUM, enterprise total, the percentages) is stale-qualified until that catch-up lands. The CN-s-1 DELTA is the Cottonwood account's dollars, read from Cottonwood inputs (newest `fact_model_assignment` partition 2026-10-16), so it is expected unaffected (INFERRED, not tested against a post-catch-up object). The issuer asked the CTO to sequence the catch-up after the 2026-10-17 13:30Z fire read.

The Global Trend, Aggregate and Custom Models views: Global total AUM +2.92% on 2026-10-15 (2,174.03M -> 2,237.50M); Custom Models group at Global and at Cottonwood includes the account; Cottonwood total unchanged, Other AUM down by the same dollars; Cottonwood Client Holdings distribution statistics change; the Custom group lists an unserved registry member at 49financial and inflection. The portal features CN-s-3 and CN-s-4 are on DEV and reach clients at the next promote, so the first fire shows the data change on the PROD views that read these served objects (INFERRED: the portal renders the served objects; not observed on PROD).

## 4. FILL AFTER FIRE: the 2026-10-17 13:30Z gold fire and 13:50Z publisher run

`fetch_served_as_response.py` (the newest served object of the 16 pairs, LastModified printed) then `grade_d4_v2.py --allow-append` against the saved baselines: arms V0-V9 read: FILL. Run manifest: `errors` empty FILL, `a4_objects_built` 16 FILL, `run.code.commit` equals the pin FILL; publisher manifest `all_present` True FILL; `r9_trend_groups_readback.py` 11 arms FILL; the portal render of the Cottonwood and Global Custom Models bands FILL (the CVO's, once PROMOTED; before that, a render from the served objects).

## 5. Rows and what is the CVO's

`MDPF_CANON-D1-S29` (ARMED, disarms on CN-s-4's PROD read); `D1-S30` (OBSERVATION: a non-internal Global session sees Custom Models only as the group total); `D1-S31` (OBSERVATION: the provenance-guard push refusal, repaired by CN-s-3 AMENDMENT 2); `D1-S32` (BLOCKING, ARMED -> disarmed by the rollback and the V2 redeploy; FILL: dispositioned when the fire is read). Judgment criteria: CN-s-4 AC3 and CN-s-3 AC2 are graded; CN-s-1 has none.
