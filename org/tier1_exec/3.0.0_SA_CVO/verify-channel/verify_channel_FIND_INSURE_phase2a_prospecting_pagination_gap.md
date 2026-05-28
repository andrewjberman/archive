# /verify-channel — FIND_INSURE Phase 2A prospecting pagination + total-capture GAP (Andrew-flagged)

**Verifier:** 3.0.0_SA_CVO. **Trigger:** Andrew direct 2026-05-28 — "Lusha is probably paginated at 25, not limited; want a bigger basket + the total-employee count is a useful indicator we're missing." **Scope:** code read (data/find/imo/scripts), no live API call.

## FINDING: the 24-IMO LinkedIn enrichment captured only the FIRST PAGE per company + discarded the available-total. CONFIRMED (code-evidenced). Recommend rerun after fix.

### Evidence
1. **Pagination not wired.** `_util/lusha_client.py` `contacts_prospecting()` accepts `page: int = 0, page_size: int = 50` but the request `body` it builds is ONLY `{"filters": {"companies": {"include": {"domains": company_domains}}}}` — `page`/`page_size` are **never inserted into the body** (dead params). Every call = Lusha default first page; the bronze crawler has no page loop.
2. **Hard cap compounds it.** `crawl_linkedin_bronze.py` cost-budget config: `prospecting.per_imo_ceiling_results: 25`. So results truncate at 25 regardless. Empirically every large firm = exactly 25 (`contacts_prospected=25`), small firms fewer.
3. **available-total discarded.** Method docstring: "Results land in the `results` key with a **`pagination` block**." The crawler reads `results` only; the `pagination` block (total matching leadership contacts) is never captured to `_meta.json` or gold. We have firmographic `employeeCount` (whole-company headcount estimate) + `linkedinFollowers`, but NOT the prospecting `pagination.total` = the addressable leadership-bench depth (distinct, more useful for target sizing).

### Impact
- The current gold roster (≤25/company) is page-1, not the full leadership set. Large carriers (Allianz Life 3,991 emp, MetLife 45k) almost certainly have far more than 25 leadership contacts — we have a truncated basket.
- We're blind to the leadership-bench-depth signal (how deep is each company's addressable leadership), which is itself a useful AM-target indicator Andrew wants.

### Recommendation (DS code + COO drive; cost-aware)
1. **Wire `page`/`page_size` into the prospecting body** (currently dead) + add a page loop that pulls until the `pagination` block is exhausted OR a new per-IMO cap.
2. **Capture the `pagination` block total** into `_meta.json` + surface as a gold `_company_scored` field (e.g. `leadership_contacts_available` / `prospecting_total`) — the bench-depth indicator.
3. **Raise `per_imo_ceiling_results`** from 25 to a new cap (cost decision — COO/Andrew). OPEN QUESTION for DS: is prospecting charged per-result or per-call? (24 companies × ~25 results = only ~72 total credits ⇒ ~3/company ⇒ prospecting looks per-CALL or free-preview, not per-result. If so, deeper pagination is CHEAP and the case for a full pull is strong.)
4. **Rerun the 24-IMO subset** with pagination on → bigger basket + the total signal. Then re-emit Deliverable-6 (top-N now drawn from the full roster, not page 1).

### Routing
Code finding (OUT of CVO fix-scope) → DS~C (0.1.0_DS_MarketIntelligence~C, .024 owner): pagination wiring + total capture. → COO: drive the rerun + cost-cap decision. CC CTO. Verifier-≠-fixer: I confirm the gap empirically; DS implements; COO drives; I re-verify the rerun output (completeness + the new total field) when it lands.
