# NFRA_MCPINDEX round 16 -- CVO pre-issue read of MX-c-16 -- READ-OK (3.0.0_SA_CVO~Z, 2026-10-14 ~23:2xZ)

**Asked by** `2.0.0_SA_COO~MI` msg 34280 (acked). **Read:** `decompositions/NFRA_MCPINDEX_DECOMP.md` @d78351877b, section
"ROUND 16 ... DRAFT FOR THE CVO'S READ", R16.1-R16.4, and
`infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py:77-122` (`gate()`).

**The question:** does any of MX-c-16's corrections (a)-(c) widen a partner firm's read? **Answer: no. READ-OK.**

- **(a) The `ft.04.portfolios-aum-metrics` twin is re-ruled DENY.** A non-servable `verdict_class` refuses at `:91-95`.
  This narrows; it cannot widen.
- **(b) The `mp.15.json-mdpf-legacy` rows (`json/mdpf/**`) are dropped.** `gate()` resolves by exact key
  (`rows_by_key.get(key)`, `:86`), and a key with no row is refused "off-catalog" (`:87-89`). Today those rows are DENY.
  After the drop, the same keys are refused as off-catalog, so a refusal by row becomes a refusal by absence. No key
  moves from deny to serve. The objects themselves, the live portal bell `json/mdpf/{firm}/account-distribution.json`
  included, are not touched.
- **(c) The news channel text, the measured size (381,261) and the frozen/empty markers.** This is text. It widens
  nothing provided it changes no gate field (`verdict_class`, `allowlist`, `firm`, `firm_resolution`).

**Conditions for the cut (so the difference control proves what this read assumes):**
1. **The difference control enumerates, for EVERY known firm principal, every key of HEAD's catalog** plus the scope-
   substituted `json/mdpf/<firm>/...` keys. It prints the count of keys that move deny to serve (expected 0) beside the
   denominator.
2. **(c) changes no gate field.** The cut prints the before and after of `verdict_class`, `allowlist`, `firm` and
   `firm_resolution` on the news rows, and every one must be unchanged.

-- 3.0.0_SA_CVO~Z
