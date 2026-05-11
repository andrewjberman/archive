<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-4b</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] INF_D_08 nna_geo emits synthetic "Untagged" geo bucket — state_tagged_aua + untagged = total_aua canonical</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>active</status>
    <priority>P1 — parity gap (not partner-blocking; RD interim drop-subtotal covers demo)</priority>
    <authorized_by>CTO ruling 2026-05-11 on RD 5-regression report; pairs with RD interim drop subtotal under TO-3 scope</authorized_by>
  </metadata>

  <context>
    Andrew flagged Continuous Segment Analytics shows "$189M Cumulative AUA by Geography" — should be $203M canonical. Root cause: `state_tagged_aua` is a strict subset of `total_aua` (~$14M of accounts have no state attribution and are dropped from the chart).

    **Pattern parallel:** mirrors IWM catchall bucket (`inflection_wealth_management` for unattributed advisor accounts) + INFTGT TO-10 "Unassigned" relabel. Same architectural shape applied to geography.

    **RD interim ship (under TO-3 scope, Option B):** Drop the cumulative AUA-by-geography subtotal entirely from the Continuous view. Closes the visual confusion (no $189M sidebar) without invasive UI surgery.

    **This TO is the DS-side architectural fix:** INF_D_08 nna_geo emits a synthetic geo key (proposed: "Untagged" or "Unknown") for accounts without state attribution. After this lands, state_tagged_aua + untagged-bucket = total_aua canonical, and RD can re-add the subtotal in a follow-up if desired.
  </context>

  <scope>
    <step>Phase 1 — Trace + investigate:
      `comp-pipescript io INF_D_08`
      `comp-trace nna_geo --direction both`
      Examine INF_D_08.nmec_nmnc_nna.py:
      - How does it select accounts? Implicit state-tagged filter, or explicit?
      - What's the data shape for untagged accounts?
    </step>

    <step>Phase 2 — Define synthetic bucket:
      Proposed key: "Untagged" (consistent with INFTGT TO-10 "Unassigned" pattern for advisor catchall).
      Alternatives: "Unknown", "Other", "Unattributed-Geo".
      DS~A finalizes naming with RD coordination (the bucket needs a render-compatible label).
    </step>

    <step>Phase 3 — Implementation:
      For accounts with NULL or empty state attribution:
      - Aggregate AUA + count into synthetic geo bucket
      - Emit alongside the named-state entries in nna_geo output
      - state_tagged_aua + untagged_aua = total_aua canonical
    </step>

    <step>Phase 4 — Coordinate with RD on display:
      After this TO ships, ping RD to optionally re-add the cumulative subtotal (since coverage is now complete).
      RD may choose to keep dropped per UX simplification — joint call.
    </step>

    <step>Pre-commit gate per CLAUDE.md rule 14.</step>

    <step>Local verify: re-run INF_D_08; confirm cumulative geo AUA sums to canonical total_aua.</step>

    <step>Commit + push + S3 deploy + manual SHA verify.</step>

    <step>RAVC2 to COO with before/after totals + chosen bucket name.</step>
  </scope>

  <acceptance_criteria>
    1. INF_D_08 nna_geo emits synthetic geo key for untagged accounts.
    2. Sum across all geo buckets (named states + synthetic) equals canonical total_aua ($202.96M) ±0.1%.
    3. Synthetic bucket name documented + consistent with TO-10 pattern.
    4. No regression on existing named-state values.
    5. Pre-commit gate exits 0.
    6. S3 deploy MATCH.
    7. RAVC2 with before/after + bucket name + portal coordination note.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-pipescript io INF_D_08`
      `comp-trace nna_geo --direction both`
    </phase>
    <phase id="3" when="after commit">
      Manual SHA verify
    </phase>
  </compiler_tools_mandate>

  <notes>
    Not partner-blocking. RD's interim Option B (drop subtotal) covers the demo today. This TO is the architectural-correctness layer that lands tomorrow when DS~A is back.

    Bucket naming convention: synchronize with TO-10 "Unassigned" pattern — these are siblings in the "catchall residual" family. Future TOs may emit other synthetic buckets for unattributed-advisor / unattributed-cohort / etc.
  </notes>
</task_order>
