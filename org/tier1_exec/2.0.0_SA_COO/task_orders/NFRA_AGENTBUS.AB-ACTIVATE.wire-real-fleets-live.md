# Task Order: NFRA_AGENTBUS AB-ACTIVATE -- wire two REAL fleets live (the final activation inch)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-agentbus-ab-activate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>2.0.0_SA_COO (Andrew-Directive-gated)</issued_to>
    <date>2026-07-07</date>
    <status>SUPERSEDED -- Andrew-direct 2026-08-19 ~20:12Z</status>
    <reconcile_note>Status corrected 2026-07-20 by 2.0.0_SA_COO (Andrew-direct backlog review): was 'pending' but dispatch_state = WRITTEN-NOT-DISPATCHED, so factually 'staged'. GOVERNANCE-FENCED -- this activation (wire two REAL colleague fleets live) is held for an UN-ISSUED standing-access-class Directive (Andrew-only, sovereign; per NFRA_AGENTBUS.json the fence was honored exactly, the leg is deliberately NOT authored). NOT active work. The project NFRA_AGENTBUS itself stays active (Port-1 build S1/S2 done, S3/S4 held; Port-2 awaiting Andrew ratification). DEPRECATE-vs-KEEP-FENCED is Andrew's call -- surfaced 2026-07-20.</reconcile_note>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>GENUINELY-EXTERNAL: gated on the standing-access-class DIRECTIVE (Andrew, sovereign). SAME Directive as COMPTEAM-B2-ACTIVATE.</gate_note>
  </metadata>

  <objective>Wire cross-principal comms between two REAL agent fleets live (beyond the single-tenant simulated harness).</objective>

  <requirements>
    <requirement id="1">real cross-fleet comms live with all 5 controls enforced</requirement>
  </requirements>
</task_order>
```

---
## ⚖ SUPERSEDED — Andrew-direct 2026-08-19 ~20:12Z (VERBATIM "All approved"; record @1e0ec3b079)
Ruled on COO `/open-calls` card 10. **This TO is SUPERSEDED, not abandoned and not failed.**
**Why it is superseded rather than completed:** the agent bus is now **exercised in live cross-device
use** — the D7/D9/D6 sitez kickoffs of this very evening rode it, with bus ids on the record. The TO
was written to ACTIVATE a capability that has since been activated by use. Keeping it `staged` for
43 days misrepresented the board: it read as unstarted work when the thing it asked for was already
running.
**Not a deletion:** the file stands as the record. Nothing is removed and no artifact is torn down.
