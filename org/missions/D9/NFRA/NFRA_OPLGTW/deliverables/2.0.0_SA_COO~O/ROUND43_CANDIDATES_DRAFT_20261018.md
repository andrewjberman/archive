# NFRA_OPLGTW -- round-43 candidates carried from round 42 (2.0.0_SA_COO~O, 2026-10-18 ~02:1xZ) -- DRAFT, a carrier for the L10 slug, not an issuance

Round 42 is in flight (mid-round the spec and the decomposition are frozen); these are the findings that are NOT round-42 cells, kept so the round-42 slug lists them with their source rows.

1. **Pin the Graph host.** `graph.call` (`app/graph.py:52`) sends the bearer token to any absolute URL it is given, and two callers follow Graph's `nextLink` with no host check (`app/tools.py` near 1158 and 588, `app/asker_scope.py` near 276). The link is issued by Graph, not by a caller (`OG-sec-1` verdict CLEAN, row `Z-S384` / worker row `Z-W145-S2`), so this is hardening, not a controllable target: refuse an absolute URL whose host is not `graph.microsoft.com` in `graph.call`. One guard and one test.
2. **The SSRF audit's pattern misses two sites.** The two `PyJWKClient(...)` JWKS fetches at `identity.py:44` and `:115` are outbound HTTP the pattern does not match (the real denominator was 20, not 18); both URLs are config-sourced. A later audit adds the pattern `PyJWKClient\(`.
3. **`safe-merge.sh --lineage-only`** (round-41 slug item 6): `0.0.0_AB_MSTR`'s tool; noted to MSTR by the CTO, no gateway cell.
4. **Carried rows and what releases them:** `Z-S375` and `Z-S338` (disarm through the listener, `OG-ap-40`); `Z-S313` and `Z-S177` (when rows exist); `Z-S322`/`Z-S325` (a named principal list); `Z-S369` (the laptop CTO's probe); `Z-W94-S2` (dell2 `IB-hm-5` and the laptop CTO's reader grant).
5. **If `OG-ev-6` chooses 30:** `OG-en-29` is cancelled and `OG-ap-39` ships the tests and notes only; a later round revisits the page size only on new evidence (a larger account window).

Push state: LOCAL.
