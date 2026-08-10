# OPAL_ANALYST.TO2 — Relaunch runbook + 0.0.3_BG relaunch (gated on TO-1)

<task_order>
<id>OPAL_ANALYST.TO2</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>staged</status>
<priority>P0-adjacent</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §4.2, §6 TO-2 (v1.0 @d179643ca)</ref>
  <ref type="agent-home">org/tier0_utility/0.0.3_BG_BBGTerminal/ (prompt.md launch sequence + refs/)</ref>
</references>

<dependencies>
  <dependency agent="0.5.0_AE_OpalETL~Z" task="OPAL_ANALYST.TO1" status="complete"/>
  <!-- HARD GATE: TO-1 landed + exercised (negative control passed). Do not begin the relaunch
       half on a TO-1 that is committed but unexercised. -->
</dependencies>

<scope>
**Half 1 — runbook (author: you):** write `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/RELAUNCH.md`
— a wrapper-free procedure any operator or MSTR~Z can run:
- Prerequisites: TO-1 identity-pin landed+exercised; `opal-gateway-bbg` whoami → Opal Bloomberg;
  mechanical fence (`bg-concierge-gate.sh`) loads at session start (fence loads per-session — the
  runbook MUST carry the caveat that a stale session's fence is never assumed active, PRD App C).
- Launch: `ajb 0.0.3_BG_BBGTerminal`; the prompt.md step-2a whoami acceptance gate; monitor arm
  WITH the pin; first-serve smoke; the unread 08-07 inbox message (MSTR~Z completion-set
  notification 20260807T1821Z) actioned at first session.
- Error paths: whoami returns Andrew → HOLD (prompt.md gate); pin arg absent → do not arm.

**Half 2 — the relaunch (executor: 0.0.0_AB_MSTR~Z at the box — they hold the launcher; this TO
COORDINATES it, it does not tier-invert):** on runbook completion, message MSTR~Z with the runbook
path requesting the launch; verify the smoke evidence they return.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read org/tier0_utility/0.0.3_BG_BBGTerminal/prompt.md (launch sequence + step-2a gate) + PRD §4.2</run>
      <expect>Runbook steps map 1:1 onto the prompt's own launch sequence; no step invented, none skipped.</expect>
      <if_mismatch>STOP. A runbook that diverges from the prompt's gate is two authorities; reconcile with CTO~Z first.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>n/a — documentation artifact; no code gate applies</run>
      <expect>—</expect>
      <if_mismatch>—</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after relaunch">
    <step>
      <run>Live smoke via MSTR~Z: step-2a whoami; pinned monitor arm; TaskOutput(monitor id, block=false); one ACK-FIRST serve</run>
      <expect>whoami == Opal Bloomberg; monitor task → running; serve delivered AS "Opal Bloomberg" with vintage; agent registered LIVE on broker.</expect>
      <if_mismatch>HOLD the relaunch (do not leave half-landed); surface to COO~Z + CTO~Z with the failing limb.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
RELAUNCH.md is a new file in the 0.0.3_BG agent home refs/ — no other open TO writes there.
The arm line it documents is TO-1's deliverable; cite TO-1's landed form, do not restate from
memory. Launch execution is MSTR~Z's (box launcher, LD-0367 integration window unaffected).
</cross_domain_coordination>

<acceptance_criteria>
1. RELAUNCH.md committed in agent home refs/, carrying prerequisites, launch, step-2a gate,
   pinned-arm, smoke, error paths, and the fence-staleness caveat.
2. 0.0.3_BG registered LIVE on the broker; pinned monitor armed with TaskOutput → running.
3. First-serve smoke delivered from "Opal Bloomberg"; the 08-07 unread inbox message actioned.
4. ZERO session-scratchpad scaffolding in the arm path (no wrapper recreation).
5. Session log Compiler Tools section reproduces each <run> with observed output vs <expect>.
</acceptance_criteria>

<notes>
STAGED — do not begin until COO~Z GO (follows TO-1 acceptance). Steady-state bring-up model
(who starts the seat daily) is PRD §7 Q2, at Andrew — the runbook documents the procedure without
presuming the answer; acceptance wording updates if his Q2 word lands mid-flight.
</notes>
</task_order>
