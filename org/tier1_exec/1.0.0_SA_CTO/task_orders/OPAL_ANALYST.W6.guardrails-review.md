# OPAL_ANALYST.W6 — guardrails review (terminal wave; a review + tightening, NEVER monitors)

<task_order>
<id>OPAL_ANALYST.W6</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>1.0.0_SA_CTO~Z</issued_to>
<date>2026-08-19</date>
<status>staged</status>
<priority>P1</priority>
<!-- TERMINAL WAVE by ruling (§10.6): reviews every access surface INCLUDING W5's catalog and the
     W7/W8 surfaces, so it certifies the system we ship, not a narrower one.
     GO gates: (1) the v0.2 index LANDED — W5's artifact, executing as D6_ANALYST.TO-CDBFG-SITEZ
     row TO-B at 0.5.0_AE_OpalETL~Z per the ~2015Z reconciliation (the OPAL_ANALYST.W5 TO is
     superseded-with-pointer; the gate follows the ARTIFACT, not the TO shell);
     (2) MSTR~Z's 08-20 07:00 WDAC acceptance.
     Joint: 3.0.0_SA_CVO~Z (second reads). Certification seat on any widening: Andrew (§9.2 table).
     Self-issued under this program's §9.8 issuance routing (Andrew-direct @219bbc246c: W5/W6
     issuance calls are CTO~Z's). -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md — §9.7 (scope + moratorium) · §10.6 (terminal sequencing) · §10.8 + §10.8.1 (firm isolation) · §10.8.2 (W8 size metering + endpoint mandate) · §10.8.3 (W9 boundary, spec-only) · §9.11 (BG fold: F6–F10 binding scope inputs) · §4.3 (gateway per-identity allowlist)</ref>
  <ref type="grounding">BG relay 20260819T192059Z (gate probes exercised live at the wiring layer: G4 gateway BLOCKED · G3 historical BLOCKED · G3 3-security BLOCKED · G3 1-security PASSED = positive control · G2 write BLOCKED · suite 34/34 under env -u) + BG record org/tier0_utility/0.0.3_BG_BBGTerminal/logs/2026-08-19/andrew_direct_1900Z_relay_findings_to_mstrz.md</ref>
</references>

<scope>
Review, as the completed program actually leaves them: `BLOOMBERG_GUARDRAILS.md` (view-never-download)
· `BUCKET_ALLOWLIST.yaml` (default-deny) · `PORTAL_RETRIEVAL.md` (safe-read discipline) · the gateway
per-identity tool allowlist (§4.3) · the Analyst's serve/deny surface over the certified verticals +
the W5 catalog · the W7 SharePoint surface (quota constraint) · the W8 blpapi surface (download
prohibition + BYTES metering, §10.8.2) · the W9 boundary (spec-only, §10.8.3) · firm isolation across
all of it (§10.8: Opal users see ALL firms, firm users see OWN firm only).
</scope>

<requirements>
  <requirement id="1">**F6 — review the control surface as MEASURED, not as described.** Deliverable core is a CONTROL CENSUS: every control row carries layer ∈ {MECHANICALLY-GATED, PROSE-DISCIPLINE, ABSENT} with exercised evidence for every GATED claim (its live block + a separate positive control). The answering layer (catalog classification, vintage rule, T-1 discipline, thread memory, ACK-FIRST) is PROSE — the review states that plainly; a tightening that assumes content-gating exists reviews a system we do not have.</requirement>
  <requirement id="2">**F7 — record reads-ungated as the true state** (G2 blocks writes only; `aws s3 cp` DOWN passes by the suite's own positive control; channel confinement is real only inside `portal_lookup.py`). Any read-side tightening lands as a GATE CANDIDATE PROPOSED TO ANDREW — never implemented on inference (no-inferred-gates law; §10.8 firm isolation is the one sovereign-backed gate request already on file).</requirement>
  <requirement id="3">**F8 — disposition the single-sourced fence identity** (`$OPAL_AGENT_SERIAL` only, because the fence blocks the serial-file write; unset → silent stand-down of all four classes). Tightening CANDIDATE: fail-closed-and-loud on unresolvable serial, the never-rules-gate's own pattern. Proposed to Andrew, not built.</requirement>
  <requirement id="4">**F9 — carry the DO-NOT-REFILE note**: the suite's 33/34 is the test shell leaking the serial into the gate's fallback (34/34 under `env -u`). It looks exactly like a real finding; the note exists so nobody burns the cycle again.</requirement>
  <requirement id="5">**F10 — exercise the server-side allowlist DENIALS from a NON-BG seat** (this seat or CVO~Z, via the gateway): the BG seat's local G4 blocks calls before the server sees them, so from there the server layer's denials are structurally unexercisable. Denial observed live; positive control in a SEPARATE invocation (a control batched with the target is corrupted by its own presence).</requirement>
  <requirement id="6">**Firm-isolation review per §10.8** across the W5 catalog rows, the W7 registry, and the serving routes — firm from PREFIX, never bucket name (§10.8.1); `trade-workflow-handler` is the working reference implementation (proven in source, one invocation in 30 days — unproven in use, say so).</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` routing; `comp-iam` for the gateway/identity view (DESIRED-only — ground any fresh IAM claim on live `aws iam get-role-policy` per Rule 22a); `comp-routes behaviors` for any serving-route claim.</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py` touched.</before_commit>
  <after_commit>python .tools/proof-of-spec-check.py &lt;instance&gt;.json C1,C2,C3,C4,C5,C6   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — joint reviewer; second reads on every layer classification (a control the author classified alone is a self-comparison).
- **0.0.3_BG_BBGTerminal** — probe provenance only; NO new work routes to that seat (its fold obligations closed with the relay).
- **Andrew** — certification seat on ANY widening; all gate candidates route to him.
- **2.0.0_SA_COO~Z** — RAVC validation of the deliverable.
- Lane commits only; no push.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Control census complete: denominator = the scope list above, every row present or DECLARED-excluded; every GATED claim carries its exercised block + separate positive control.</criterion>
  <criterion id="C2">BG's G1–G4 probes inherited WITH VINTAGE or re-derived; the F9 do-not-refile note carried.</criterion>
  <criterion id="C3">F10 denial exercise executed from a non-BG seat: live denial observed, positive control in a separate invocation.</criterion>
  <criterion id="C4">Firm-isolation findings recorded per surface (W5 catalog, W7 registry, serving routes).</criterion>
  <criterion id="C5">Every tightening classified {gate-candidate-to-Andrew | owned-blocking-item}; monitors proposed = ZERO.</criterion>
  <criterion id="C6">Proof-of-spec instance validator-clean BEFORE any status flip; session log with Compiler Tools section.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6</expected_criteria>
  <instance_path>org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_ANALYST.W6_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="document">W6 review deliverable (control census + dispositions + gate candidates) at `org/tier1_exec/1.0.0_SA_CTO/deliverables/` (lane-prefixed filename)</deliverable>
  <deliverable type="document">Proof-of-spec + session log</deliverable>
</deliverables>

<do_not>
  <rule>NO monitors, alarms, SNS, SES, freshness checkers — the moratorium, restated in §9.7 precisely because a guardrails review is where notification machinery gets proposed · no gate IMPLEMENTED without Andrew's word (proposals only) · no widening without Andrew · no push · no work routed to the BG seat.</rule>
</do_not>
</task_order>
