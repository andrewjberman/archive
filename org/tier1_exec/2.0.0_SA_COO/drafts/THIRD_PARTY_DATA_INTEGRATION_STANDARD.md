# Third-Party Data Integration Standard

Status: v0.1 DRAFT — authored 2026-05-20 by 2.0.0_SA_COO, pending 1.0.0_SA_CTO ratification + canonicalization to `docs/architecture/`.
Origin: Andrew-direct directive, 2026-05-20 (YALP_MDSRC). Verbatim: "this needs to be templated as the approach to all third party data, we do not 'scrape', we 'reverse engineer'."

## 1. Principle

Opal integrates third-party data by **reverse-engineering the provider's actual data API** — the backend contract the provider's OWN application uses to talk to its database. We integrate against that contract directly. This yields structured, high-fidelity, robust data.

We do **not** "scrape." Rendered-HTML / DOM parsing is brittle, low-fidelity, and breaks on cosmetic UI changes. It is the fallback of last resort — used only for a datum genuinely served no other way, and always explicitly flagged.

## 2. Terminology — binding

| Use | Do not use |
|-----|-----------|
| "reverse engineer", "integrate against the provider's API", "internal-API integration" | "scrape", "scraper", "scraping" |

This applies to task orders, briefs, code, comments, commit messages, session logs, and agent-to-agent messages. Andrew directive 2026-05-20: "we do not scrape, we reverse engineer."

## 3. The template — the method, per source

Applies uniformly whether the source fronts its data with a web app (YCharts) or a documented API (SmartX REST, FRED).

1. **Discover the real data contract.**
   - Web-app-fronted source: capture the internal XHR/fetch JSON API the app issues to its backend (browser devtools / capture proxy). That backend is the API to the provider's database — that is the integration target, not the rendered page.
   - API-fronted source (documented REST/key API): characterize the API **empirically**, not from documentation alone. A docstring/spec-attested constraint is an assumption, not evidence (ref: ADVI_INFINC.005 — a "TXN endpoint accepts no date params" docstring was empirically wrong; a probe found a firm-level windowed endpoint). Probe for undocumented depth, real param behavior, and real response shape.

2. **Characterize the auth / session model.** Cookies + CSRF token, JWT (ROPC or otherwise), API key — whichever the source uses: how it is obtained, its lifetime, how it is refreshed, and the observed rate limits.

3. **Map every requirement** to its endpoint + exact params + the JSON path to the value.

4. **Verify fidelity empirically** against the current source of truth (e.g. the Bloomberg-pkl values) — a measured per-requirement fidelity column, not an assumed match.

5. **DOM parsing is last-resort only**, per-datum, and flagged as such in the deliverable.

## 4. Scope — all third-party data sources

This standard governs every third-party data integration, current and future:
- **YCharts** — YALP_MDSRC.A3 (internal JSON API reverse-engineering).
- **SmartX** — YALP_MDSRC.B1 / S1, SXPL_RESTIN (the SmartX REST API; ROPC-JWT). Reverse-engineer the REST contract empirically — do not trust the docs blind.
- **FRED** — YALP_MDSRC.F1 + the FRED implementation TO (the official FRED API). Same empirical-characterization discipline.
- Any future source.

## 5. Deliverable framing

Every third-party data integration deliverable is framed as an **integration spec** — the reverse-engineered endpoint reference, the auth/session model, the requirement->endpoint mapping, the empirical fidelity check. It is never framed as a "scraping" guide.

---
Ratification note for CTO: fold this into PRD YALP_MDSRC v0.4 (or canonicalize standalone in `docs/architecture/`), and reference it from every source TO (A3, B1, S1, F1, C1, C2, D1, SXPL_RESTIN).
