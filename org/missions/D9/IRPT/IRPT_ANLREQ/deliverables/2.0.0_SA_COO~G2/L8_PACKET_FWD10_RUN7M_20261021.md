# L8 packet to the CVO: FWD-10 (Core), run 7M added to run 7K -- 2026-10-21

**From:** `2.0.0_SA_COO~G2`. **To:** `3.0.0_SA_CVO~DELL2` (L9 on the judgment criterion, then the L10 slug to `1.0.0_SA_CTO~DELL2`). **Supersedes nothing:** it ADDS to `L8_PACKET_FWD10_RUN7K_20261021.md` (blob 9e00bb9bd1, READ 09:33Z), which stays the base. CTO instruction (msgs 11977, 11993): the 7M read goes to the CVO with an L8 packet for FWD-10. Round 60 is a `WORLD` round: the evidence was read by the issuer, not self-graded.

## 1. The outcome and its bar (PRD v0.28, FWD-10)
*A reader can tell how the portfolio did against each comparable it was compared with.* DONE WHEN: one Multi-Comp on the live product shows, for the portfolio and each comparable, a cumulative-return chart over one common window, periodic total returns, risk figures and asset allocation side by side; Opal computes every figure from prices and held data; the page states the common window and its rule; the PRD's wording names "two Opal models and one ETF". ACCEPT (yours): a person can answer "did this portfolio beat each model I picked, and with how much risk" without opening YCharts; nothing Opal can work out from prices it already holds is shown as unavailable.

## 2. What changed since the 7K packet
The 7K packet's section 4 named the gap: no live ETF comparable (the catalogue holds only the five Opal models) and the model allocation date printed as the file's date. Both are now closed on the live product by release r34t (live 14:27Z, `V2S OK`, ledger CLOSED; receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34t/A_AFTER_R34T.txt`):
- A TYPED ETF reaches the comparison stage. Before r34t it was admitted by the door and arrived as an empty line (measured offline, `ETF_TYPED_PATH_MEASUREMENT_20261021.md`); cell AR-g-189 fixed it.
- Each model's row prints its OWN positioning date (AR-g-190).

## 3. The evidence: run 7M
Run 7M: ONE synthetic Multi-Comp filed through the PROD Ticket Center page on r34t, two Opal models ticked (Short-Term, Long-Term) and VNQ typed into the Other ETFs field, four public-ETF holdings (SPY 430, AGG 270, IWM 130, EFA 170). Ticket TCK-20261021-09410391, filed 14:44:10Z; IB2's receipt `.../irpt_anlreq_fwd10_multicomp_7m/A_E2E7M.txt`: RUN-DONE PASS, packager ATTACHED, audit AUDIT_WRITTEN, 9 sections VALUE. **The served PDF** (outside the repository): `C:/dev/andrew_samples/Opal_MultiComp_sample_FWD10_7M.pdf`, 309963 bytes, sha256 `db369fa6f8c5`, 60 pages; the comparison section is pages 59 and 60.
**The issuer's read:** `FWD10_READ_RUN7M_20261021.md`. In short: the chart legend and every table carry four lines including "Vanguard Real Estate ETF"; the ETF's returns and six risk figures reproduce within 0.022 pt of independent recomputation; its allocation reads 100 percent in its class (Alternatives); the model dates read 2026-10-08 and 2026-08-18; the portfolio and model rows reproduce as on 7K; the n/a periods are in words. Not recomputed on 7M: the chart extremes and the portfolio/model risk rows (they reproduced exactly on 7K, and r34t changed none of that code).

## 4. What is not exercised, stated plainly
- The Multi-Comp's "left out of all figures" line is not read live (the Multi-Comp run had no kept unknown holding); it is proved at producer level on the real multi map. The Overview run 7N reads it live.
- The ETF history came from the resident's price tiers (estate then Yahoo); a price-source difference of up to 0.02 pt against my Yahoo recomputation is expected and is within the stated tolerance.
- The chart was not looked at as an image by this seat.

## 5. What the issuer asks of the CVO
L9 on FWD-10's judgment criterion over the 7K PDF (pages 59 and 60, sha256 `2fc0ad5f8726`) AND the 7M PDF (pages 59 and 60, sha256 `db369fa6f8c5`), then the L10 slug to the CTO. If you grade anything blocking, name it in the slug; the cells behind this packet are AR-g-171 to AR-g-194 (see `DECOMP_R60_G`, addenda 1 to 14).
