# Task Order: OPAL_ANALYST.W8 — BBG blpapi pipe map (what is served where and how)

<task_order>
  <id>OPAL_ANALYST.W8.bbg-blpapi-pipe-map</id>
  <issued_to>4.0.0_SA_CRO~Z</issued_to>
  <issued_by>1.0.0_SA_CTO~Z</issued_by>
  <issued>2026-08-12</issued>
  <project>OPAL_ANALYST</project>
  <status>pending</status>

  <authorization>
    Andrew-direct 2026-08-12 ~1702Z at the CTO~Z terminal. Verbatim record:
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260812_OPAL_ANALYST_ACCESS_LAYERS_P1_P2_P3.md`
    @f09cbd13ef. He named this seat himself: *"a 4.0.0_SA_CRO~Z agent will be needed to explore the
    BBG blpapi pipes and know what is served where and how."*

    ⚠ **THIS TO DOCUMENTS THE WORK; IT DOES NOT PERMIT IT.** The authorization is Andrew's word above,
    relayed via MSTR~Z 170523Z. Increments 1 and 2 landed BEFORE this TO existed (@52f215db0f,
    @8c5d1c5674) and that was CORRECT — the seat did not idle on paperwork, and I said it should not.
    Recorded so the sequence is not later read as work-without-authorization.
  </authorization>

  <objective>
    Map the Bloomberg blpapi ingress and establish **what is served where and how**, joining the
    upstream vendor segment to the already-mapped downstream portal segment. Produce the architecture
    map and a registry of what it covers — **by traversal and read only.**
  </objective>

  <constraints>
    ⛔ **SOVEREIGN AND NOT SOFTENABLE (Andrew ~1702Z):**
    1. **Traversing the pipes: PERMITTED. Reading: PERMITTED.**
    2. **DOWNLOADS ARE EXPRESSLY FORBIDDEN.** Not minimized — forbidden.
    3. **A post-architecture verification pull is a SEPARATE, SIZED REQUEST TO ANDREW.** *"we are on a
       quota and large pulls will be flagged."* **Sizing means a number** — securities x fields x date
       span — **not an adjective.** Egress-widening goes to Andrew DIRECTLY, never as a relay summary
       (MSTR~Z's instruction, adopted).

    ⛔ **THE EGRESS BOUNDARY IS THE CALL SHAPE, NOT THE TOOL NAME — this seat's own correction to my
    weaker constraint, adopted verbatim into PRD §10.3 and credited:**
    > *"if a reference call starts looking like a data acquisition in disguise, it is a pull and it
    > stops and gets sized"*
    `bloomberg_reference_data` sits on the permitted side of a tool-name line and can still harvest
    content at N securities x M fields, iterated. **A name-based rule READS GREEN on that.**
    Field-count x repetition-count is the thing to watch. `reference_data` for schema/identifier
    resolution only; the moment the purpose is the values themselves, it is a pull.

    **Vendor-egress scope:** Andrew's ~1702Z word IS the per-use authorization CLAUDE.md requires, and
    its scope is EXACTLY traverse + read to map what is served where and how.

    ⛔ **NEVER#1 COUNTERWEIGHT IS MANDATORY WHEREVER THE SILENT-FAILURE MODE IS STATED.** The map
    records that a missing PKL means the pipeline never fires and the portal serves yesterday's
    artifact with yesterday's `data_as_of` — internally consistent and stale. **That statement must
    carry the trading-calendar counterweight in the same breath so it cannot be misread as a staleness
    alarm**, and it must not become an alarm/monitor proposal (moratorium).
    ⛔ **NO MONITORS, ALARMS, SNS, SES, OR FRESHNESS CHECKERS.** Findings land as findings.
    ⛔ **NO BLOOMBERG SIGN-IN ATTEMPT** — P0 gate, lockout risk. That surface is `0.0.3_BG_BBGTerminal`'s.
  </constraints>

  <acceptance_criteria>
    <!-- Machine-checkable. Each id below is minted by the issuer and appears in <expected_criteria>. -->
    W8-INGRESS-C1  — the blpapi ingress is ENUMERATED and grounded: service endpoint(s), transport,
                     session/request shape, with the instrument and its output cited per claim.
    W8-INGRESS-C2  — ZERO downloads occurred during increment 1, evidenced (the absence is asserted
                     with what would have shown one).
    W8-REQUNIV-C1  — the COMPLETE request universe with a DENOMINATOR: request count, request type,
                     service, identifier count, and the field vocabulary enumerated (not sampled).
    W8-REQUNIV-C2  — the SERVED JOIN with a denominator: which served artifacts are Bloomberg-origin
                     and which are not, plus per-page blast radius, each side counted.
    W8-REQUNIV-C3  — the silent-failure mode is stated WITH the NEVER#1 trading-calendar counterweight
                     in the same passage, and proposes NO monitor.
    W8-REGISTRY-C1 — a registry section recording what is served where and how, keyed so a consumer
                     can look a served artifact up and reach its upstream request.
    W8-REGISTRY-C2 — every UNVERIFIED PREMISE is named as unverified rather than carried as fact —
                     explicitly including the one-producer-two-homes claim (repo notebooks vs the
                     OneDrive production copies), which the README asserts as prose and which no
                     measurement in this run establishes.
    W8-PULLMENU-C1 — increment 3 delivers EITHER a sized-pull menu carrying exact numbers
                     (securities x fields x date span) per proposed pull, OR a declared
                     "no pull required" with the reason. **A need for a pull is never manufactured.**
    W8-PULLMENU-C2 — NO pull was executed absent Andrew's per-pull word, evidenced.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>W8-INGRESS-C1,W8-INGRESS-C2,W8-REQUNIV-C1,W8-REQUNIV-C2,W8-REQUNIV-C3,W8-REGISTRY-C1,W8-REGISTRY-C2,W8-PULLMENU-C1,W8-PULLMENU-C2</expected_criteria>
    <!-- MULTI-PIECE TO: a grammar, NOT a single path (protocol §proof_of_spec — a single declared
         path on a multi-group TO matched NONE of the landed instances on MDPF_49F_BUILD.P1, so a
         completion flip would have read absence as work-not-done). -->
    <instance_path_grammar>org/tier1_exec/4.0.0_SA_CRO/deliverables/PROOF_OF_SPEC_W8_{group}_{YYYYMMDD}.json</instance_path_grammar>
    <group id="INGRESS"  status="MINTED" instance_path="org/tier1_exec/4.0.0_SA_CRO/deliverables/PROOF_OF_SPEC_W8_INGRESS_20260812.json"/>
    <group id="REQUNIV"  status="MINTED" instance_path="org/tier1_exec/4.0.0_SA_CRO/deliverables/PROOF_OF_SPEC_W8_REQUNIV_20260812.json"/>
    <group id="REGISTRY" status="NOT_YET_MINTED"/>
    <group id="PULLMENU" status="NOT_YET_MINTED"/>

    <!-- VALIDATE BEFORE THE STATUS FLIP. THE ID SET IS POSITIONAL — there is NO flag form:
           python .tools/proof-of-spec-check.py <instance>.json W8-INGRESS-C1,W8-INGRESS-C2
         ⛔ CHECK THE RC, NEVER THE OUTPUT STRING. The usage banner contains the vocabulary of BOTH
         verdicts, so a grep for a success string matches "Exit 0 = VALID" in the banner of a call
         that validated NOTHING. rc=0 VALID / rc=1 INVALID / rc=2 usage-or-read error.
         And do NOT fall back to the 2-arg form on a usage error — it returns rc=0 with COVERAGE
         UNCHECKED, which is the one layer that catches a silently-omitted criterion. -->
  </proof_of_spec>

  <compiler_tools_mandate>
    BEFORE WRITE: `comp-which "<the question>"` to route; `comp-estate` for the already-mapped
      downstream segment — **Build-Ladder rung 2 is load-bearing here and this seat already honored it**
      (NFRA_BBGMCP_PRD carried the openService-probed service map; yang-pipeline-lineage-map carried 17
      portal artifacts at field grain but STARTS at data.pkl/model.pkl — W8 supplies the missing
      upstream segment and JOINS them rather than re-deriving either).
    BEFORE COMMIT: `.tools/commit-gate.sh` on any `.py`; denominators printed beside every count.
    AFTER COMMIT: the session log's Compiler Tools table, including any gap found.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    **`0.0.3_BG_BBGTerminal`** — shares the Bloomberg terminal surface. The half-healthy probe finding
    (`bloomberg_health ok:false`, no listener on 127.0.0.1:8194, `bbcomm` alive/Responding) is **BG's
    seat, already routed there by CRO~Z, FYI-only to CTO** — correctly NOT called an outage (this
    morning's 07:00 run succeeded end-to-end and the portal serves T-1 2026-08-11 correctly), cause
    UNDETERMINED with the seat's own probe not excluded as the trigger. **No sign-in, no alarm.**
    **`0.5.0_AE_OpalETL~Z` / `3.0.0_SA_CVO~Z`** — W8 shares NO artifact with W4b/W4c and needs no
    rectangle certification, which is why this fifth seat does not deepen the certifier bottleneck.
    **Surprise-channel items surfaced and deliberately NOT chased:** one-producer-two-homes (Rule 22a
    two-homes shape, recorded as an unverified premise — see W8-REGISTRY-C2); and
    `json/macro/vix_data.json` produced every run and consumed by nothing.
  </cross_domain_coordination>

  <deliverables>
    1. `org/tier1_exec/4.0.0_SA_CRO/deliverables/CROZ_W8_BBG_BLPAPI_PIPE_MAP_20260812.md`
       — increment 1 @52f215db0f (ingress), increment 2 @8c5d1c5674 (request universe + served join),
       increment 3 (sized-pull menu or a declared no-pull), plus the registry section.
    2. One PROOF_OF_SPEC instance per group, per the grammar above.
    3. A session log carrying a **Compiler Tools** section (mandatory; "N/A" is not acceptable —
       one sentence of why, if none were run).
  </deliverables>

  <notes>
    ⚠ **COMMIT AT EVERY INCREMENT BOUNDARY, not at deliverable close.** The 2026-08-12 07:52:45Z
    outage was a **planned N-able RMM (`winagent.exe`) restart as SYSTEM** to finish a Windows Update
    chain — it recurs on the MSP's schedule, on both devices, and **nothing respawns seats afterward.**
    A seat can vanish mid-unit with no warning. This seat's two-increment cadence is already the right
    shape; it is now mandatory rather than incidental.

    **The map being COMPLETE WITHOUT ANY PULL is the preferred outcome, not a shortfall.** If Andrew or
    CTO wants live verification of the identifier universe, exact numbers go in front of Andrew
    directly per W8-PULLMENU-C1.
  </notes>
</task_order>
