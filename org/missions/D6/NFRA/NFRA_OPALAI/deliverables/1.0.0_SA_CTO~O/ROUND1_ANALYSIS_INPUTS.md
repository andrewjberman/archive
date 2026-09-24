# NFRA_OPALAI -- round-1 analysis inputs, held by the PRD owner

**Owner:** `1.0.0_SA_CTO~O`. **What this is:** rulings and design inputs this seat has made WHILE round 1 runs. They are
not spec changes: the round is frozen, and each one enters the round-1 analysis (L10), where the enrichment list is cut.
**Append-only**, newest last.

---

## I-1 (2026-09-24 ~23:4xZ) -- ruling on row NFRA_OPALAI-Z-W2-S1: how C10 applies to the portal catalog

**The row's question:** `opal_asker_query` cannot narrow a portal-catalog fetch by the asker's `datasets` grant,
because a catalog key has no dataset field. The row offers (a) a new catalog field mapping keys to datasets, which is a
schema widening Andrew would rule, or (b) ruling the catalog out of C10's asker scope. It names both as CTO/COO calls.

**Ruling: neither. C10 applies to the catalog on the catalog's OWN axis.**
- The portal catalog is scoped by principal CLASS and FIRM. `catalog_gate.gate(key, principal_class, principal_firm)`
  gives Opal-internal all rows and a firm only its own (`graphql_plumbing/catalog_gate.py`, rule 5).
- `opal_asker_query` evaluates that gate on the CALLING identity's class and firm (`asker_scope.py:170`,
  `query_v0._principal(calling_email)`). **That is the C10 defect on this surface: the gate reads the concierge, not
  the asker.**
- **The fix:** the effective verdict is `gate(asker) AND gate(calling identity)`, and neither alone widens the other.
  The asker's class and firm are resolved SERVER-SIDE from the asker's verified Entra identity:
  - tenant id equal to Opal's own tenant: Opal-internal;
  - any other tenant: a firm, ONLY through an explicit tenant-to-firm registry, which does not exist today, so the
    answer is deny by default;
  - never from the profile record's `email` field, which is display-only (`data_entitlement.py`).
- The Schwab grant's `datasets` dimension does NOT apply to the portal catalog. They are disjoint data domains, and
  no new dimension is minted. The grant's `operations` check ('query' required) stays as built.
- **Today's effect:** every asker is Opal staff in Opal's tenant, so gate(asker) is Opal-internal, the same as the
  concierge's. Nothing a colleague sees changes. What changes is that the day a non-Opal asker exists, they are
  confined to their firm or denied, never given Opal's reach.

**Why not (a):** a key-to-dataset mapping would bolt the Schwab custodial grant model onto a catalog of served portal
artifacts. That is a second scope axis on one surface, and Rule 24's same-grain postulate refuses it. **Why not (b):**
it would leave C10's own sentence false on the surface round 1 serves.

**Enrichment item this makes:** the round-2 repair of `asker_scope.py` (gate on the asker, intersected), paired with
Z-S5's repair (recency plus same-chat binding). Both touch the same function and belong in one cell.

## I-2 (2026-09-24 ~23:4xZ) -- inputs already on file elsewhere, indexed here so the analysis finds them

- **S15, the Bloomberg view:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_AI_S15_BLOOMBERG_VIEW_DESIGN_NOTE_20260924.md`
  @b99ab96fdf. The recommended shape is the operator-run loopback HTTP server. It flags a contract question: a
  server-side history cap for the agent-facing instance.
- **Z-S5, the cited-message bypass,** disarmed by Z-S6 (the tool is dark for the concierge). Its repair joins I-1's
  cell.
- **Z-W2-S2, the audit allowlist gap:** a one-line `_ARGS_ALLOWLIST` row for `opal_asker_query`, in a lane that can
  write `app/audit.py`.
- **G-GH retired** at PRD v0.5. It binds the round-2 cut of OA-t-3's successor.
