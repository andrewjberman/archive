# /verify-channel — FIND_INSURE Deliverable-6 curated contact-target list (Phase 2A analysis; Andrew morning-review)

**Verifier:** 3.0.0_SA_CVO (independent S3 read of all 24 companies' top-5). **Requested:** COO 1556Z, gates Deliverable-6 RAVC2-Accept. **Time:** 2026-05-28T~1546Z.
**Artifact:** `s3://opal-data-imo/serving/contacts-target-2026-05-27.json` (24 companies, 114 rows, top-5/company by decision_relevance_score; commits 49d8affdd v1+A → d535d4324 B+emit). My .024 refinements A (keyword-collision) + B (AM-domain weighting) folded in.

## VERDICT: PASS-meaning (deliverable is decision-useful; refinements A+B materially worked) + CONCERN (residual keyword-collision class, v1.x, non-blocking).

### Refinements A+B WORKED — the list surfaces the right people (vs raw .024 IT/ops noise)
Empirical top-5 spot-check across all 24:
- **Genuine-WM (present) companies CLEAN:** preferred-marketing (SVP/AVP/Dir Investment Services + 2 Portfolio Managers); pacific-capital (CEO + 4 Financial/Wealth Advisors); avantax (VP Advisory Solutions, Financial Advisor, Compliance — **IT-Asset-Management/Access-Removal GONE**, refinement A confirmed); lincoln-investment (EVP/COO, CFO, Sr Financial Advisor, Chief Bus Dev, VP Retirement Marketplace); integrity (SVP Wealth Management #1); gradient (Founder/CEO, Sr Investment Consultant); the-retirement-network (Dir Wealth Mgmt, RIA, Founder).
- **Adjacent companies demoted IT, surfaced AM:** allianz-life (Ventures + Distribution Sales — **CIO/IT directors GONE**, refinement B confirmed); senior-market-sales (VP Advisor Services, Chief Distribution Officer, Dir Annuity Sales); midland-national (Dir Regional Insurance Advisory, CFO, President/COO); unkefer (VP Distribution, VP Sales); sterlingbridge (Investment Compliance, Financial Advisor, SVP/VP Sales).
- Refinement B soft 0.15 down-weight did NOT wrongly bury AM-relevant people (verified COO item #2); AM leaders sit at top, IT/ops at bottom or gone.

### CONCERN — residual keyword-collision CLASS (v1.x precision, NON-BLOCKING)
Same class as refinement A but on different keywords — tech/architecture/data roles whose embedded AM-keyword ("portfolio"/"investments") floats them to #1. Clusters on 3 **annuity carriers** (where genuine-AM contacts are sparse so the collision wins #1):
- **eagle-strategies #1 (0.4875):** "Head of **Technology Portfolio**, Insurance and Annuities" — IT project portfolio, not investment portfolio.
- **metlife #1 (0.4875):** "Chief Architect and Head of Investments and Corporate **Systems Architecture**" — systems-architecture (tech), not investment decision-maker.
- **national-life #1 (0.4875):** "Director of **Portfolio Management Data and AI**" — data/AI role, not a portfolio manager.
Fix: extend `title-domain-taxonomy-v1.json` with the same negative-context treatment for "portfolio"/"investments" when adjacent to technology/systems/architecture/data/AI (the matcher caught "asset management" in IT context but not these). Low blast-radius: the genuine-WM companies (Andrew's real targets) are clean; the residual hits the lower-priority adjacent/annuity tail.

### Minor data-quality (eyes-open, route to DS)
- american-general/AIG: 4× "Chief Executive Officer" in top-5 (distinct names) — likely AIG sub-entity/region CEOs from resolving to the huge parent; confirm they're the right entity's leaders vs a parent-scoping artifact.
- hansen-brokerage: "Robert Stark" appears twice (BizDev + Brokerage) + "Robert **Undefined**" (surname parse failure) — name-parse/dedup glitch.
- lifepro: "Executive Assistant to CEO" ranked #1 (seniority classifier tagged c-suite-proximity) — an EA isn't a decision-maker.

## Routing
PASS-meaning → COO: **Deliverable-6 RAVC2-Accept is CLEAR** — the curated list is decision-useful for Andrew's morning review; refinements A+B delivered a real quality lift; the genuine-WM target companies are clean. CONCERN (residual collision class + 3 data-quality items) → DS~C as v1.x title-domain-taxonomy refinement — do NOT block accept (residuals on lower-priority adjacent carriers, eyes-open). CC DS~C + CTO. This + .024 = the Phase 2A LinkedIn-channel deliverables.
