# Task Order: OPAL_ANALYST.W7 — SharePoint reach + registry section

<task_order>
  <id>OPAL_ANALYST.W7.sharepoint-reach-and-registry</id>
  <issued_to>4.0.0_SA_CRO~Z</issued_to>
  <issued_by>1.0.0_SA_CTO~Z</issued_by>
  <issued>2026-08-12</issued>
  <project>OPAL_ANALYST</project>
  <status>pending</status>

  <authorization>
    Andrew-direct 2026-08-12 ~1702Z, **Part 2** of the three access layers. Verbatim record:
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260812_OPAL_ANALYST_ACCESS_LAYERS_P1_P2_P3.md`
    @f09cbd13ef — *"Part 2 is then making sure it is properly hooked up to read sharepoint documents and a
    registry section to know what is in there."*

    **Seat assignment is a CTO capacity call, not a sovereign one:** his word named this seat for Part 3
    and **reserved Part 2 to nobody**. Re-routed from `0.5.0_AE_OpalETL~Z` (saturated on W4b's 210-cell
    semantic half) 2026-08-12 ~1822Z. PRD §9.2 wave table + §10.2 owner line updated in the same act.
    ⚠ **THIS TO DOCUMENTS THE WORK; IT DOES NOT PERMIT IT** — same standing as W8. The seat was told not
    to wait for it.
  </authorization>

  <objective>
    Establish that the concierge is **properly hooked up to READ SharePoint documents**, then build **a
    registry section recording what is in there.** Two halves, same shape as W8: **the reach, then the
    inventory of what the reach covers.**
  </objective>

  <constraints>
    ⛔ **READ-ONLY.** Andrew's *"readonly by the way"* scopes the whole access-layer program, not just the
    portal half. **No writes, no uploads, no site mutations.** `upload_text_to_site` and
    `save_email_attachment_to_site` are OUT OF SCOPE for this wave.

    ⛔ **BUILD-LADDER RUNG 2 IS THE FIRST ACT, NOT A COURTESY.** The reach already partly exists:
    `find_sharepoint_site`, `list_site_drives`, `list_site_files`, `search_site_files`, `read_site_file`,
    `read_site_workbook`, `profile_site_file`, `get_site_item`. **VERIFY AND REGISTER WHAT EXISTS BEFORE
    BUILDING ANYTHING. THE DELIVERABLE IS THE REGISTRY, NOT A CLIENT.** *(This seat did exactly this on
    W8 — found the existing service map and lineage map and JOINED them rather than re-deriving, which is
    why W8 cost two vendor calls total.)*

    ⛔ **CARRY THE CALL-SHAPE RULE ACROSS — it is this seat's own and it generalises off Bloomberg.**
    A `search_site_files` iterated wide enough **is an enumeration**; a `read_document` loop across a
    library **is a harvest**. No published quota is known here, which is a reason for discipline rather
    than a licence: **apply W8 discipline rather than discover an unpublished limit.**

    ⛔ **NO MONITORS, ALARMS, SNS, SES, OR FRESHNESS CHECKERS** (standing moratorium). Findings land as
    findings.
    ⛔ **DO NOT chase the DAPI/transport limb.** It is escalated to Andrew as a credential ask via
    `0.0.3_BG_BBGTerminal`, that surface is BG's, and no sign-in is to be attempted (P0 lockout gate).
    **If BBG traversal opens mid-W7: commit the W7 increment boundary and switch.** Do NOT carry
    uncommitted W7 work into a traversal window — the RMM-restart class is live on this box and nothing
    respawns seats. **Ordering is Andrew's and this seat's, NOT CTO's** — CTO's earlier ordering
    reservation was withdrawn ~1825Z once he opened the traversal conversation directly at this terminal.
  </constraints>

  <acceptance_criteria>
    W7-REACH-C1     — the SharePoint reach is ENUMERATED against what already exists (tools + sites +
                      drives), each claim citing its instrument and output. **No new client built.**
    W7-REACH-C2     — every registered document class is reachable by an **EXERCISED READ**, never a
                      config read (Rule 22a: a behavioural claim needs the path exercised).
    W7-REG-C1       — a registry section recording **what is in there**, keyed so a consumer can look a
                      document class up and reach it.
    W7-REG-C2       — the registry **NAMES WHAT IT DOES NOT COVER**, and every unverified or inherited
                      premise is marked as such rather than carried as fact.
    W7-REG-C3       — a **DENOMINATOR** on the document universe, or a **DECLARED BOUND** stating why it
                      cannot be closed. ⚠ **An absence verdict NAMES THE SCOPE IT SEARCHED** (site/drive/
                      library) — the firm-partition lesson generalises to any partitioned store, and a
                      404 in the wrong library is the wrong question asked cleanly.
    W7-SCOPE-C1     — ZERO writes, uploads or site mutations occurred, evidenced (the absence asserted
                      with what would have shown one).
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>W7-REACH-C1,W7-REACH-C2,W7-REG-C1,W7-REG-C2,W7-REG-C3,W7-SCOPE-C1</expected_criteria>
    <instance_path_grammar>org/tier1_exec/4.0.0_SA_CRO/deliverables/PROOF_OF_SPEC_W7_{group}_{YYYYMMDD}.json</instance_path_grammar>
    <group id="REACH" status="NOT_YET_MINTED"/>
    <group id="REG"   status="NOT_YET_MINTED"/>
    <group id="SCOPE" status="NOT_YET_MINTED"/>
    <!-- Validate POSITIONALLY before any status flip; there is NO flag form:
           python .tools/proof-of-spec-check.py <instance>.json W7-REACH-C1,W7-REACH-C2
         ⛔ CHECK THE RC, NEVER THE OUTPUT STRING — the usage banner contains the vocabulary of BOTH
         verdicts. And do NOT fall back to the 2-arg form on a usage error: it returns rc=0 with
         COVERAGE UNCHECKED. Run a negative control (a bogus id ⇒ rc=1) as you did on W8. -->
  </proof_of_spec>

  <compiler_tools_mandate>
    BEFORE WRITE: `comp-which "<the question>"`; `comp-estate` for any already-mapped SharePoint/document
      surface — rung 2 applies to the ONTOLOGY as well as the code.
      ⚠ **`comp-estate` served-name and topology claims are PRIORS UNDER TEST** (CLAUDE.md Rule 21, and
      note its `header_metrics_fresh` example was itself corrected 2026-08-12 ~1745Z — the key is REAL,
      the defect was a firm-scoped absence generalised to nonexistence).
    BEFORE COMMIT: denominators printed beside every count; `.tools/commit-gate.sh` on any `.py`.
    AFTER COMMIT: the session log's **Compiler Tools** table, including any coverage gap found —
      per Rule 22 a comp-tool coverage gap is a DEFECT and routes to CTO, not into a log.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    **`0.0.3_BG_BBGTerminal`** — the concierge this reach ultimately serves, and the seat whose gateway
    identity is fenced (`bg-concierge-gate.sh` G4: `-bbg` server only; site-write tools denied). **W7 must
    not propose widening that fence.** Report what the reach IS; any entitlement change is Andrew's.
    **`3.0.0_SA_CVO~Z`** — semantics + certification.
    **No shared artifact with W4b / W4c** — W7 does not queue behind the certifier's rectangle lane.
  </cross_domain_coordination>

  <deliverables>
    1. `org/tier1_exec/4.0.0_SA_CRO/deliverables/CROZ_W7_SHAREPOINT_REACH_AND_REGISTRY_20260812.md`
       (increment-boundary commits, not one commit at close).
    2. One PROOF_OF_SPEC instance per group, per the grammar above.
    3. A session log with a **Compiler Tools** section (mandatory; "N/A" is not acceptable).
  </deliverables>

  <notes>
    **COMMIT AT EVERY INCREMENT BOUNDARY.** The 2026-08-12 07:52:45Z outage was a planned N-able RMM
    restart as SYSTEM; it recurs on the MSP's schedule, on both devices, and **nothing respawns seats.**
    This seat's W8 cadence was already the right shape.
  </notes>
</task_order>
