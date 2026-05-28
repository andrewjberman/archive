# /verify-channel — FIND_INSURE .024 Phase 2A LinkedIn org-chart enrichment (first live LinkedIn channel)

**Verifier:** 3.0.0_SA_CVO (independent; empirical S3 read of the 24-IMO output, not self-report). **Requested:** COO 1456Z, gates .024 RAVC2-Accept. **Time:** 2026-05-28T~1515Z.
**Artifacts:** `corp/{slug}/{bronze,gold}/linkedin-scrape/2026-05-27/` across the 24 Option-B subset. High-leverage FIND_INSURE focus: "effective results or noise? correct locations + parsing/NLP."

## VERDICT: PASS-mechanical (enrichment real + right-company; .024 RAVC2-Accept clear) + CONCERN-meaning (employee-relevance scoring, refinement-class, non-blocking).

### Mechanical — GREEN (EXISTS/FRESH/SCALED + company-resolution correctness)
- 24/24 gold (_company_scored + employees_scored) @2026-05-27; 23/24 firmographics; 491 roster records total (matches DS report).
- **Company resolution CORRECT — the wrong-company risk (domain-vs-search-id) is cleared**, verified across the hardest disambiguations:
  - allianz-life → "Allianz Life" allianzlife.com (3,991 emp) — the US life subsidiary, NOT global Allianz SE parent.
  - lincoln-investment → "Lincoln Investment" lincolninvestment.com (945 emp) — the RIA/BD, NOT Lincoln Financial annuity carrier.
  - avantax/metlife/senior-market-sales/unkefer/sterlingbridge/hansen all resolved to correct entity + matching domain. Domain-scoped resolution (post the search-id catch) works.
- Roster records are REAL decision-relevant employees — real names, real linkedin.com/in URLs, plausible leadership (avantax: VP Advisory Solutions, Financial Advisor, Compliance Director; allianz-life: real Allianz Life C-suite). Not stub, not noise, not wrong-company.
- annuity-solutions: genuine no_company_match (score 0.0, lc 0, no firmographics) — not a silent drop. ✓
- series_licenses_detected=[] / series_license_count_weighted=0 on all records = CORRECT scoping (v0.7.2 org-chart-only, no contact-reveal → no license data). Not a bug. ✓

### Meaning (Step 3.5) — CONCERN on employee-relevance scoring (refinement, NOT a blocker)
The enrichment is effective; these are quality-of-ranking findings for the IR contact-target purpose:
- **(A) Keyword-collision false-positive (real, low-frequency):** "Team Lead of IT Asset Management and Access Removal" → `title_keyword_match=1.0`, ranked #2 at avantax (0.425). The matcher matched "asset management" in an IT/operational context (≠ financial AM). The matcher needs IT/tech/access negative-context (or financial-context requirement). Sample frequency low (1 clear case), but the class is real (any "IT Asset Management" / "Asset Management System" title recurs it).
- **(B) Seniority-without-domain-relevance (design observation):** at large carriers (allianz-life, national-life-group) the top-scored contacts are IT/cyber directors (CIO, Dir IT Security/Governance, Dir Cybersecurity; all `kw_match=0.0`, scored purely on seniority weight). High-seniority but low-AM-transition-relevance for the IR target list. The decision_relevance scoring weights seniority without down-weighting non-AM functional domains → IT/ops leaders dilute the "top contacts" ranking. Consider an AM-domain-relevance factor.
- **company_score_linkedin** (range 0.0-0.38) does NOT discriminate genuine-WM from annuity-carrier (eagle-strategies 0.375, metlife/american-equity 0.323 score ≈ avantax 0.323). This is acceptable IF it's understood as org-chart-leadership-density, NOT a WM re-classifier (that was Phase 1's am_prominence). Flag only so no downstream consumer misreads it as an AM-transition signal.

## Routing
PASS-mechanical → COO: **.024 RAVC2-Accept is CLEAR on the enrichment** (real, right-company, scaled, correctly-scoped). The enrichment delivers effective results, not noise — the central high-leverage risk (wrong-company / noise parsing) is empirically cleared.
CONCERN-meaning → DS~C (scoring owner): (A) keyword-collision matcher fix + (B) AM-domain-relevance weighting are v0.7.2+ refinements to the contact-target ranking quality — do NOT block .024 accept; route as scoring-refinement follow-on. CC CTO + DS~C.
