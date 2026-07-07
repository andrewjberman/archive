# Task Order: NFRA_SEMCTL GOV-A -- unify GLDINV + PROMOTE + exercise-cert into ONE shared honesty/completion invariant-library

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-semctl-gov-a</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO + 3.0.0_SA_CVO (cross-project)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- BOTH halves ratified 2026-07-07 (NFRA drive, COO~B). CTO authored the library docs/architecture/NFRA_SEMCTL_HONESTY_INVARIANTS.md (b9f58b442); CVO CO-RATIFIED-CVO the validation/exercise-cert arm (7aad2f834), explicitly checked-and-cleared the "unification softens a per-case/fail-loud bind into aggregate/advisory" failure mode (binds read absolute). One shared doctrine (I1 honest-missing / I2 measure-per-case / I3 control-must-fire-when-exercised), grounded in the served-confirmed cot gold-review corpus (Rule 22).</status>
    <dispatch_state>CLOSED 2026-07-07. Deliverable: NFRA_SEMCTL_HONESTY_INVARIANTS.md (b9f58b442 + CVO co-ratify 7aad2f834). Follow-ons (non-blocking): (a) comp-honesty runnable checker build (§4.2, DS/AE lane -- CVO takes its exercise-cert when built) -> dispatch in an NFRA build wave; (b) GLDINV PRD adopts by reference (CTO lane); (c) PROMOTE-P1 cites §3 (folded into the PROMOTE-P1 GO). One CVO P2 precision edit (Rule 22a dual-grounding as explicit bind) routed to CTO -- refinement, non-blocking.</dispatch_state>
    <gate_note>COO-RESOLVABLE. CTO+CVO cross-project. Governance item (a) from the SEMCTL charter. CLOSED -- the shared acceptance instrument's validation arm is now the reference for subsequent NFRA honesty claims.</gate_note>
  </metadata>

  <objective>A single shared invariant-library binding the data-chain, learning-chain, AND validation: honest-missing (LOUD not silent) + measure-per-case-not-aggregate + control-must-fire-when-exercised. Unifies NFRA_GLDINV + PROMOTE's promotion-invariants + the exercise-cert discipline.</objective>

  <requirements>
    <requirement id="1">the 3 invariants codified as a reusable library (honest-missing, per-case, fire-when-exercised)</requirement>
    <requirement id="2">binds data-chain + learning-chain + validation</requirement>
    <requirement id="3">a cross-project TO, not three parallel doctrines</requirement>
  </requirements>
</task_order>
```
