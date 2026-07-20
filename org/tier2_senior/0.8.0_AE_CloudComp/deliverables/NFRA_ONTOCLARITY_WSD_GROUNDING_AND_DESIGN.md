# NFRA_ONTOCLARITY WS-D -- Log clarified defs in system/sdk (the seam-closer): grounding + design

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-20. **TO:** `NFRA_ONTOCLARITY.WS-D.log-clarified-defs-in-system-sdk`.
RIDES SYSPARITY WS-4 (COMPLETE) -- extends its representation, does NOT duplicate. Last WS -> ONTOCLARITY 4/4.
NO arch-decision (role_priority already CTO-ruled; representation is cite-not-copy per WS-4's established pattern).

## 1. Grounding -- the DELTA (WS-4 already represents most; what WS-A/B/C added that isn't yet represented)

| Clarified def | Already represented? | WS-D work |
|---|---|---|
| WS-A two-layer root (`meta.layers`) | YES -- `00_synthesis.md` "The archetype layer" (WS-4) cites it | none (no-op) |
| WS-A vocab authority / Observer / variance rename | YES -- WS-4 citations + WS-A's own canonical edits | none |
| WS-B crosswalk (5-scheme orthogonal-axes map) | YES -- `01_substrate.md` @d371bca1e | none |
| WS-B Relation-vs-Role lint (comp-ontolint) | YES -- `01_substrate.md` "machine-enforced by comp-ontolint" | none |
| **WS-C role_priority tie-breaker (polymorphic-Role)** | **NO -- not cited in the /system core docs (grep = 0)** | **THE DELTA: add a cite** |

**sdk (AC-1 + AC-3a):** every tenant `ontology_ref` (acme/company.yaml, acme-canon-patterns.yaml, the examples,
gensdk scaffold) CITES `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` (WS-4 Part B, vocabulary-bound). Because
role_priority now lives IN that canonical rule-bank, the sdk's citation REFLECTS it by construction -- no copy,
no stale/partial ordering in the sdk (cite-not-copy is the single-source discipline AC-3a demands). CONFIRMED by
the sweep: zero role_priority ORDERING copy anywhere outside RULE_BANK.

**The one drift risk (AC-3a "every enforcing copy"):** `comp_ontolint.py` self-test hardcodes a `PRIO` fixture
(the 14-role order) to seed the (a)-(d) mutants. That is a COPY of the ordering -- if RULE_BANK's role_priority
changes, the fixture silently drifts. Close it: assert the fixture == the live RULE_BANK role_priority (so a
divergence FIRES -- the every-enforcing-copy discipline made a self-test invariant).

## 2. Design (small, cite-not-copy, no new representation)
1. **/system role_priority cite (the delta):** add ONE line to `01_substrate.md` (the layer/role home) citing the
   WS-C polymorphic-Role tie-breaker: "polymorphic types resolve ONE role per instance; a node matching 2+ roles
   is arbitrated DETERMINISTICALLY by `role_priority` (the canonical `RULE_BANK.yaml`, WS-C spot-8), machine-
   enforced by `comp-ontolint role-resolve`." CITE the rule-bank, do NOT copy the ordering. (~A surface -> the
   commit carries `abstraction-ledger: n-a`.)
2. **Close the test-fixture drift (AC-3a):** add a comp_ontolint.py self-test assertion that the hardcoded `PRIO`
   == the live RULE_BANK `role_priority` (same 14, same sequence) -- a divergence FIRES. So the ONE ordering-copy
   outside RULE_BANK self-checks against the canonical (single-source, every-enforcing-copy).
3. **sdk:** no edit -- it already cites the rule-bank (confirmed). Record the no-op (don't duplicate WS-4 Part B).

## 3. Verify (Phase-3 mandate)
- `system_parity.py` ontology domain STAYS 100% (4/4) -- no regression; the role_priority cite is additive.
- comp-ontolint self-test PASS (incl. the new fixture==canonical drift-close).
- CVO SEMANTIC-verify (AC-3): the represented ontology matches the CLARIFIED (post-WS-A/B/C) truth, esp. AC-3a --
  the sdk reflects the RULE_BANK role_priority ordering (via citation), not a stale/partial copy.

## 4. Land path
COO review (small, no arch-decision) -> build (01_substrate cite + comp_ontolint fixture-drift-close) -> CTO
arch-gate if he wants (representation extension) -> RAVC -> CVO semantic-verify -> WS-D DONE -> ONTOCLARITY 4/4.
No RULE_BANK edit (role_priority already landed @317b3d0af) -> no WS-2 06-gate on the RULE_BANK; 01_substrate +
comp_ontolint.py are the surface.
