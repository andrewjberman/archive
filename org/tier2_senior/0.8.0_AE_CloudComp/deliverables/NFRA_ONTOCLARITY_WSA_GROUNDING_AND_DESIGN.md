# NFRA_ONTOCLARITY WS-A -- Root ontology-fog fix: grounding + design (for COO/CTO review)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-19. **TO:** `NFRA_ONTOCLARITY.WS-A.definitions-root-two-layer-fix`
(COO, staged->pending). **Gate path:** COO design review -> CTO arch-gate on the 3 arch-decisions -> RAVC ->
CVO SEMANTIC-verify per fog class (LD-0320/0318). Load-bearing acceptance: a fog is resolved only when the
AMBIGUITY IS GONE, not reworded (word-grep-both-ways = not fixed).

## 1. Fog inventory (Phase-1 grounding; the denominator, source+vintage per Rule 22)

| # | Fog (brief S3a) | Grounded current state |
|---|---|---|
| a | "Ontology" = one word for two layers, never disambiguated (ROOT) | The CSE C0-C3 ALGEBRA (compiled-system ladder, TYPE axis) vs the 14/10/6 ARCHETYPE layer above it. `RULE_BANK.yaml:16` meta.frame states "1 C0-C3 CSE ladder + 3 orthogonal axes {TYPE=CSE / RELATION=CSE-re-layered / ROLE=net-new} + VARIANCE" -- a COMPACT statement, but NOT an explicit "one word, two layers" disambiguation, and NOT referenced as THE authority by consumers. My WS-4 00_synthesis "## The archetype layer" states it in prose (forward-consistent seed), but that's a /system REPRESENTATION, not the canonical DEFINITION home. |
| b | Vocab split across ~5 files + v0.1-pin | `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` (canonical machine encoding) + its deliverable MIRROR + `variance_dimensions.yaml` + its deliverable MIRROR + `canon-patterns.yaml` (adapter) + `CLOSED_SET.md` (doctrine prose). The deliverable mirrors are hand-synced -> drift risk. The SDK v0.1-pin is RETIRED (WS-4 Part B @327b615e5 -> vocabulary-bound cites RULE_BANK.yaml). No declared single source-of-record + version scheme. |
| c | Observer DoR-vs-rulebank contradiction | `RULE_BANK.yaml:33` "Observer ... (13th, CTO GRANTED)" (settled) vs `CLOSED_SET.md:48` "Open for CTO (net-1): Observer -- a full Role vs a Guard-subtype" + `:115` gate-rule. LD-0311 RATIFIED Observer = full Role #13 (CTO granted). -> RULE_BANK is current-truth; the CLOSED_SET "Open" is STALE (pre-ratification). ALREADY-RULED (COO concurred) -- a stale-copy RECONCILE, not a new fork. |
| d | Fork-Shadow=debt retired but copies may linger (LD-0315) | LD-0315 replaced Fork-Shadow=debt with the advisory-candidate regime. `variance_dimensions.yaml` fork_shadow_disposition maps advisory->"(candidate -- advisory)" / grounded->"(debt)" (conditional, correct). Live grep so far surfaces only PRD/brief META-refs (describing the fix). SWEEP for any live doc/code copy asserting a BLANKET Fork-Shadow=debt still pending (4+ sweeps per PRD). |
| e | `variance_dimensions` name reads axis-names as the verdict vocab | The file holds `dimensions:` (the AXES, e.g. firm) + `phrasing:`/fork_shadow_disposition (the 6 VERDICT vocabulary). The name suggests the dimensions ARE the variance vocab; the real variance content is the 6 verdicts. Baked into a FROZEN v1 additive-only schema (`:11` "This v1 is empty+advisory") + consumers reference the filename -> a raw rename is constrained. |

## 2. Design (resolution per fog -- ambiguity GONE, not reworded)

- **(a) ROOT two-layer disambiguation -- state it ONCE at the canonical authority.** Add an explicit `layers:`
  block to the canonical vocab source (see arch-decision #2) that disambiguates: **LAYER 1 = the CSE C0-C3
  ALGEBRA** (the compiled-system ladder; TYPE axis; `cse_schema.py`); **LAYER 2 = the ARCHETYPE layer** (14
  Roles / 10 Relations / 6 Variance, agnostic, edge-derived, on top). Every consumer (CLOSED_SET, canon-patterns,
  /system 00_synthesis, SDK) REFERENCES this one statement -- no re-statement (the same cite-not-copy discipline
  that closed WS-4). My WS-4 00_synthesis prose then points AT it (one authority, downstream references).
- **(b) single canonical source-of-record + version scheme.** Declare `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml`
  (meta.version + meta.ratified already present) as THE canonical machine source; the deliverable MIRRORS get a
  header banner "SNAPSHOT -- canonical is org/modules/graph/..., do not consume" (or are retired). CLOSED_SET.md =
  the DOCTRINE prose that DEFERS to the rule-bank for the machine vocab. One version scheme = the rule-bank
  meta.version (bumped by explicit promotion, LAW-2).
- **(c) Observer one-truth.** Reconcile CLOSED_SET.md:48/:115 to "SETTLED: Observer = full Role #13, CTO granted
  per LD-0311" (delete the "Open for CTO" contradiction). Stale-copy reconcile (already-ruled).
- **(d) Fork-Shadow=debt purge.** Complete the live sweep; delete/annotate any live doc copy asserting blanket
  Fork-Shadow=debt to the advisory-candidate regime (LD-0315). variance_dimensions already correct (conditional
  disposition); the target is stale DOC copies.
- **(e) variance_dimensions name.** ANNOTATE (not raw-rename, given the frozen additive-only schema + consumer
  refs): add a header banner distinguishing "`dimensions:` = the variance AXES (e.g. firm); the 6 Variance
  VERDICTS (Canonical/Twin/Fork-Shadow/Variant/Superseded/Orphan) are the vocabulary, in `phrasing:`". OR a
  rename-with-compat-alias -- arch-decision #3.

## 3. The 3 arch-decisions (surface to COO -> CTO; I do NOT self-authorize)

1. **Canonical vocab source authority (covers fog a + b):** is `RULE_BANK.yaml` THE machine authority (CLOSED_SET
   = deferring doctrine prose), and does the two-layer `layers:` statement live in the rule-bank meta? (My rec:
   YES -- rule-bank is the single machine-loadable source every consumer already cites post-WS-4; CLOSED_SET is
   the doctrine that defers to it.)
2. **variance_dimensions: annotate vs rename-with-alias.** (My rec: ANNOTATE -- the frozen additive-only schema +
   live consumers make a raw rename high-blast; a header banner resolves the mis-read without a schema/consumer
   churn. Rename-with-compat-alias if CTO wants the name itself fixed.)
3. **Observer:** confirm it is a RECONCILE (already-ruled LD-0311, CLOSED_SET stale), NOT a re-open. (My rec +
   COO concur: reconcile-to-granted; not a new decision -- flagged only so CTO sees the CLOSED_SET edit.)

## 4. Land path
COO design review -> route the 3 arch-decisions to CTO -> on CTO rulings, implement (rule-bank layers: block +
canonical-source declaration + mirror banners + CLOSED_SET Observer reconcile + Fork-Shadow=debt sweep +
variance_dimensions annotation) -> CTO arch-gate the diff -> RAVC -> CVO SEMANTIC-verify per fog class (ambiguity
GONE) -> ping COO+CVO on land. WS-A feeds WS-4 (done) + WS-D (rides WS-4). WS-B/WS-C follow (COO files).
