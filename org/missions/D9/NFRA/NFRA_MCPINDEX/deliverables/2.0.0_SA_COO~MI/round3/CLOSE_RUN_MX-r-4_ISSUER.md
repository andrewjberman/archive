# MX-r-4 close run -- run by the issuer through a principal session (2.0.0_SA_COO~MI, 2026-09-29 ~03:3xZ)

Material for `3.0.0_SA_CVO~O`'s r4.J1. This record has no verdict; the CVO grades.

**Why the issuer ran it.** The worker had no authenticated route (`CLOSE_RUN_MX-r-4.md` in the worker's deliverables,
NOT RUN). At ~03:30Z, this seat's own MCP connection to the Opal gateway listed the 5 new tools (`opal_discover`,
`opal_describe`, `mdpf_get_aum_metrics`, `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua`) after the enable.
The run used that session. Every call was read-only.

The host served deploy-only 0bce8d322a (gateway tree = pin 3371f18803).

## One question per A2 surface

### 1. `platinum/mdpf` -- "total model portfolio AUM for the firm"
- `opal_discover` routed to 8 catalogued rows, 3 servable. The first match is `mp.01.aum-metrics`
  (`platinum/mdpf/{scope}/aum-metrics.json`).
- The purpose-built tool was `mdpf_get_aum_metrics(scope=global)`:
  - status ok;
  - key `platinum/mdpf/global/aum-metrics.json`;
  - `as_of` 2026-09-25, read from the object's `period`;
  - total.aum 2,083,228,453.05, account_count 8,242, model_aum 1,788,338,510.93;
  - `_provenance.written_at` 2026-09-28T13:50:50Z.
- The portal's served object, read directly from `opal-data-portal-v2` at the same key: VersionId
  `N_KOsRfVbwJr7danRAxFjAmYOfhCViGu`, LastModified 13:50:51Z. It holds period 2026-09-25, total.aum 2,083,228,453.05,
  account_count 8,242, model_aum 1,788,338,510.93 and written_at 13:50:50Z.
- **Figure and as-of: EQUAL on all four fields.** 2026-09-25 is the last completed trading day at the 13:50Z
  Monday publish: T-1 = Friday.

### 2. `platinum/etfs` -- "ETF holdings and fund flows"
- `opal_discover` said catalogued, 4 datasets, 4 servable. **All four are positioning/portfolio rows:**
  `json/positioning/holdings_attribution_data.json`, `.../allocation_summary.json`, `.../positioning_data.json` and
  `json/portfolios/aum-metrics.json`. **No `platinum/etfs` row matched.**
- No purpose-built ETF tool exists; FWD-5 is DEFERRED.
- The next tool named is `query_v0` for each row.
- **Not answered from the ETF surface.** The router matched on the common word ("holdings"), which is the
  one-common-word signature of row Z-W2-S8, still standing for this ask.

### 3. `platinum/advi` -- "advisor intelligence rep production ranking"
- `opal_discover` answered NOT_CATALOGUED, with no dataset and no tool.
- **An honest absence, not an answer.** The advisor-intelligence surface is not in the catalog for this principal.

### 4. `json/*` -- "model portfolio benchmark returns"
- `opal_discover` said catalogued, 14 datasets, 6 servable. First match `mp.04.model-portfolio-timeseries`, second
  `mp.05.model-portfolio-benchmarks` (the "did the model beat its benchmark" table), then `mp.06.etf-returns`.
- The caveat travels with it: MODEL-DESIGN returns, never client-realized.
- The next tool is `query_v0`. It is not in this session's tool list, so no figure was fetched.
- **Routed to the right family, but not answered by a purpose-built tool** (none exists for json/*). The ranking put
  the timeseries ahead of the benchmark table for a benchmark ask.

## Two findings across all four surfaces (candidate rows for the analysis, not filed as defects here)

- **A. discover never routes to the purpose-built tool.**
  - Every `next_tool` names `query_v0`, including mp.01's.
  - mp.01's purpose-built tool is `mdpf_get_aum_metrics`, and it answered correctly when called directly.
  - FWD-1 reads "discover routes a cold question" to the right tool. Today the route and the purpose-built tool are
    not joined.
- **B. discover's freshness `latest_value` is the catalog's CERTIFICATION vintage, not the served object's.**
  - mp.01 shows `2026-08-10`, labelled `claim: held`, while the object carries `2026-09-25`.
  - The claim label is honest ("not re-read from the served artifact").
  - But a user sees a date 7 weeks older than what the tool returns one call later.

## Scope of this run

- 4 of 4 A2 surfaces asked.
- 1 answered with a figure and as-of equal to the portal's (`platinum/mdpf`).
- 1 honest absence (`advi`).
- 2 routed without a purpose-built answer: `etfs` mis-routed to positioning, `json/*` routed correctly with no tool.
- The asker is this seat's principal session, not a non-author asker. The FWD-1 cold run is G-B / G-ASKER (Andrew's
  speed test first).
