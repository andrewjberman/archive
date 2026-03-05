This is a Pattern 0 design-alignment thread for SSCN_PORTAL. The COO's directive is: SecurityScanner must mirror PortfolioManagement's visual language as closely as possible. PM is the most production-complete page in the portal. SSCN should reuse PM patterns rather than reinvent them.

The data architecture is already settled (SSCN_PORTAL-001):
- Server-side precompute monthly: per-factor percentiles per universe
- Client-side: composite score + rank (sum of pctls * weight / 100)
- API: GET /api/scoped/security-scanner/factors, /universe/{universeId}/data, /universe/{universeId}/scanner
- JSON row shape: { ticker, name, mktVal, sector, industryGroup, values: Record<FactorCode, number|null>, pctls: Record<FactorCode, number|null> }
- 6 universes: sp500/r1000/r1000v/acwx/eafe/eafev
- 284 scoring factor columns in source data

This thread resolves the DESIGN side:
1. Which PM utilities/patterns can be imported directly by SSCN (zero copying)?
2. Which PM patterns need abstraction to a shared location before SSCN uses them?
3. What new SSCN-specific components are needed (no PM equivalent)?
4. What does the SSCN DESIGN_SPEC.md skeleton look like?

The output is an approved component reuse plan that 0.3.4_RD_SecurityScanner can build against.
