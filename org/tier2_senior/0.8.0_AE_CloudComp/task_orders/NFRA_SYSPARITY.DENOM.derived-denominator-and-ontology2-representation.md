<task_order>
<to_id>NFRA_SYSPARITY.DENOM</to_id>
<title>THE PARITY DENOMINATOR IS FROZEN AT v1 — represent ONTOLOGY2 in /system, pin the rule-bank VERSION, and make the scope contract's unit list DERIVED instead of hand-maintained</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp (base lane — scope_contract.json is SYSPARITY WS-1's artifact)</issued_to>
<date>2026-07-24</date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_SYSPARITY, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P1 — the estate's parity metric currently reads 100% on an axis it cannot see</priority>

<authority>
ANDREW-DIRECT (2026-07-24): Andrew asked `3.0.0_SA_CVO~Z` directly to audit whether what it is
calibrated on for SYSPARITY is properly scoped. CVO~Z's audit (record `@fed09ce1a`) found the scope is
in-charter but the DENOMINATOR is v1-era and cannot see the TOOLSTACK program. Routed to `1.0.0_SA_CTO~Z`
for the structural half; ruling below. CVO~Z correctly declined to author the denominator it is measured
against (grantee-commits-its-own-grant would destroy verify independence) — so the LAND is this lane's,
the ontology-plane content is CTO~Z's, and CVO~Z verifies the result.
</authority>

<the_finding_independently_verified>
All three claims verified by CTO~Z with independent greps before ruling:
1. **Rule bank is `version: "1.2"`** (NFRA_ONTOLOGY2 P1 dynamic-rail fold, canonized `@5d1161d70`).
2. **`/system` represents v1** — "14 Roles / 10 Relations / 6 Variance" at `00_synthesis.md:19`,
   `01_substrate.md:32`, `03_comp_tools.md:6`, `07_maturity.md:6`.
3. **ZERO `/system` files** mention ONTOLOGY2 / TOOLARCH / TOOLSEM / TOOLBHVR / `type_tuple` /
   `dynamic_rails` / `c1_frontend_adapter`. All grep 0.
**`system_parity` reads 100% on all 4 domains BECAUSE the ontology units grep for v1-satisfiable text.**

>> THE MECHANISM, and it is the part that must not be lost: `07_maturity.md:6` asserts the v1 archetype
layer "IS REPRESENTED in /system" — **and that assertion is still TRUE.** ONTOLOGY2 landed ADDITIVELY
(only `binds_up` adapter arrays extended; nothing replaced). So the parity check is **not reading a
stale lie — it is reading a still-true v1 fact and concluding currency.**
**A PRESENCE-CHECK CANNOT DETECT AN ADDITIVE EXTENSION.** It can only fail if the base version is
REMOVED. Therefore *the safest kind of change — additive, non-breaking, the kind we deliberately
engineer for — is precisely the kind that defeats presence-based parity.* The better the change
discipline, the blinder the instrument. The fix is a VERSION pin and a COVERAGE check, **never more
presence greps.** <<
</the_finding_independently_verified>

<scope>
A. **REPRESENT ONTOLOGY2 IN `/system`** (act now — real gap). The canonized v1.2 layer: dynamic rails
   D1/D2/D3, the `(rail, grain, plane, scope)` type_tuple, the completeness axis, `c1_frontend_adapter`.
   CITE the canonical rule bank, do not COPY it — follow the existing `00_synthesis` "The archetype
   layer" precedent, which cites `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` rather than duplicating
   it. A copy would create a second drift source, which is the disease not the cure.
B. **PIN THE VERSION — add scope-contract unit `ont-rulebank-version-current`.** The existing
   `ont-cse-version-current` unit (asserts `cse_schema @0.4` ABSENT) is the exact pattern; mirror it.
   It must assert the rule bank's CURRENT `meta.version`, so a future canonization that does not update
   `/system` FAILS rather than passes. MUTANT REQUIRED: bump the rule-bank version (or point the unit at
   a version `/system` does not carry) and the unit must REDDEN. A version pin that cannot fail is the
   defect it was built to close.
C. **RESERVE COVERAGE UNITS for TOOLBHVR / TOOLSEM** so their absence becomes DETECTABLE when they land,
   rather than silently uncounted. These are design-stage — this is not a representation demand, it is a
   *detectability* demand.
D. **THE STRUCTURAL FIX — DERIVE THE UNIT LIST, do not hand-maintain it.** The scope contract's
   in-charter framework list must be ENUMERATED FROM A REAL SOURCE that grows when the estate grows
   (candidate sources: the `docs/architecture/NFRA_*_PRD.md` set, the program register). Assert that each
   enumerated in-charter framework HAS a unit; print the denominator (N frameworks enumerated, M with
   units, K without).
   >> **A HAND-MAINTAINED DENOMINATOR *IS* THE FROZEN-ENUMERATION CLASS.** This program has spent its
   entire life ruling that enumeration happens at run time from a real source and never from a hand-list
   — and then measured its own estate against a hand-list. <<
E. **TOOLARCH: partial, as it stabilizes.** Its censuses are still moving; representing an unstable
   surface creates a second drift source. Represent the tool-layer facts that have settled
   (`03_comp_tools` material), not the in-flight ones.
</scope>

<the_two_axes_do_not_collapse_them>
A **VERSION PIN** catches drift in a thing already REPRESENTED — the CURRENCY axis.
A **COVERAGE CHECK** catches a thing NEVER REPRESENTED — and a version pin structurally cannot do this,
because *a unit that does not exist cannot fail.*
Both are required, permanently. CVO~Z was running only the currency axis for ~30 ticks and reported bare
"AT PARITY" without stating what the parity was OF — a verdict without its denominator is unfalsifiable.
</the_two_axes_do_not_collapse_them>

<the_duty_this_establishes>
>> **CANONIZATION IS NOT COMPLETE UNTIL THE ESTATE'S DENOMINATOR CAN SEE IT.** A framework is LANDED
when it is represented AND a unit exists that would FAIL if it regressed. << This makes denominator-
growth part of the LANDING rather than a follow-up nobody owns — TRIGGER_LAYER applied to the
denominator itself. It binds the NEXT framework, not just this one. The root cause CVO~Z named is that
the PRDs reference `infra/system` only as a substrate they READ FROM ("Substrate:", "Consumer:") and
never as something to update back, and `NFRA_TOOLSTACK_PROGRAM` never mentions `/system` or SYSPARITY at
all. Fixing the artifacts without fixing the duty leaves the next framework to re-open this.
</the_duty_this_establishes>

<acceptance_criteria>
1. ONTOLOGY2 v1.2 layer represented in `/system`, CITED from the canonical rule bank, never copied.
2. `ont-rulebank-version-current` unit live, asserting the CURRENT rule-bank `meta.version`, with a
   MUTANT proving it REDDENS when `/system` lags the rule bank.
3. Reserved coverage units for TOOLBHVR / TOOLSEM — their future absence is detectable.
4. Scope-contract unit list DERIVED from an enumerable source, with the denominator printed
   (N enumerated / M with units / K without). No hand-list.
5. `system_parity` re-run: the ontology domain must now be able to FAIL. State what changed in the
   verdict and why — if it still reads 100%, prove that is a real 100% and not the old blindness.
6. The duty recorded where the NEXT framework will hit it (program record + the PRD template/checklist),
   not only in this TO.
7. Session log + compiler-tools-log line.
</acceptance_criteria>

<cross_domain_coordination>
`scope_contract.json` is SYSPARITY WS-1's artifact — this lane lands it. Ontology-plane CONTENT (what
the v1.2 layer says) is `1.0.0_SA_CTO~Z`'s; coordinate the wording with me before landing §A.
`3.0.0_SA_CVO~Z` VERIFIES the result and must NOT author any part of the denominator it is measured
against — do not accept CVO~Z edits to `scope_contract.json`; its role is verification only.
</cross_domain_coordination>

<verification>3.0.0_SA_CVO~Z — with specific attention to: does the version-pin mutant actually REDDEN,
and is the derived unit list genuinely derived (not a hand-list with a loop around it)?</verification>
</task_order>
