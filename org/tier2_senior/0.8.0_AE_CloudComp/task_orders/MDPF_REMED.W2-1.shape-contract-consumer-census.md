<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-r9-r12-shape-contract-census</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    Deliver the CONSUMER CENSUS that rows R-9 through R-12 of the MDPF remediation register each name
    as their closing condition. **Every one of those rows is blocked on the same missing measurement:
    who actually reads these fields.** This TO produces it. **It changes NO served shape and moves NO
    field** — three of the four rows need a decision that is not yours or mine once the census exists.
  </objective>

  <context>
    PRD: `docs/architecture/MDPF_REMEDIATION_REGISTER.md` @e5e932caf6 §2c. Andrew took the register AS
    THE PRD 2026-08-07 ~1910Z, VERBATIM: *"take the remediation plan as the PRD and decompose it to TOs
    for the relevant agents."*

    THE FOUR ROWS, and note each one's stated closing condition is a MEASUREMENT, not a change:

    **R-9** — `last_updated` is a PROCESS CLOCK inside the BUSINESS PAYLOAD (all 4 scopes,
    `aum-metrics`). Closes with: *move it to `_provenance`* — **"needs a consumer check + Andrew's
    word."** ⛔ The move is a SERVED-SHAPE change. You deliver the consumer check; the word is his.

    **R-10** — `inflection_non_model_aua`: a **FIRM-NAMED field at GLOBAL scope**, non-canonical under
    L-1. Closes with: *decide canonical-or-not, then retire ON EVIDENCE.* Referenced by
    `route_bindings.yaml` + leg pins, so it is not free-standing.

    **R-11** — five **GLOBAL-ONLY fields** in `aggregate-aua-timeseries`. Same shape as R-10.

    **R-12** — the `(scope, artifact-type)` pair model **NORMALISES `_` and `-` variants to one type**,
    which makes it **BLIND TO ANY FUTURE NAME VARIANT BY CONSTRUCTION.** The 3 underscore twins that
    motivated it are already executed @46d3bf3f32 — **the blindness OUTLIVES them.** Closes with:
    *completeness against the ACTUAL KEY LISTING, with unrecognised keys SURFACED.*

    >> WHY THIS SEAT: you closed NFRA_PYFIELD TO-1 by verifying the seven props keys against the LIVE
    portal artifact rather than your own constant, and you reconciled a denominator disagreement (4,904
    vs 4,896) by re-running someone else's probe instead of asserting yours. **That is exactly this
    job.** R-12 in particular is a normalisation hiding a population — the same shape as your own
    "a stricter rule produced a bigger number" finding.
  </context>

  <compiler_tools_mandate>
    Phase 1:
      <run>comp-which "what consumes the mdpf aum-metrics artifact"</run>
      <run>comp-find "last_updated" data/mdpf portal</run>
      <expect>Consumers with a PRINTED DENOMINATOR. Use `--all` wherever a count is load-bearing.</expect>
      <if_mismatch>⛔ An ABSENCE verdict here would authorize retiring a served field. An absence from
      a truncated scan is indistinguishable from a real absence — print the denominator and name what
      you could NOT see (the portal submodule, deployed-but-uncommitted code, another device's tree).
      ⚠ `comp-find` counts LINES, not nodes.</if_mismatch>
    Phase 2: <run>comp-transform schema-check [the consuming component]</run> for any portal reader you find.
    Phase 3: record every command, its denominator and its disposition in the log.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: the served MDPF artifacts + `data/mdpf/config/route_bindings.yaml`
    - ⚠ `route_bindings.yaml` IS BEING EDITED RIGHT NOW by `0.4.0_DS_ClientPlatform` under W1-1
      (re-declaring the 49F custody leg). **MCP them before reading it as settled, and do not edit it.**
    - This TO is READ-ONLY on every served artifact. It proposes; it does not move.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. **A CONSUMER CENSUS PER FIELD, WITH ITS DENOMINATOR AND VINTAGE.** For each of `last_updated`
       (×4 scopes), `inflection_non_model_aua`, and the five global-only fields: every reader, the
       retrieval command, the denominator, and what the scan could not see.
       ⛔ **"No consumer" is the finding that authorizes retiring a CLIENT-FACING FIELD. It must be
       SHOWN, not asserted** — and a PRESENCE verdict needs only one hit while an ABSENCE verdict needs
       exhaustiveness you cannot fully have. Say UNMEASURED where that is the honest answer.

    2. R-12: **COMPLETENESS AGAINST THE ACTUAL KEY LISTING.** Enumerate the real served keys and show
       which the `(scope, artifact-type)` pair model FAILS TO RECOGNISE. ⛔ The 3 underscore twins are
       ALREADY EXECUTED — do not re-report them as outstanding; **the deliverable is the BLINDNESS, not
       the twins.** Any unrecognised key is surfaced by name.

    3. >> **NOTHING MOVES. NO SERVED FIELD IS RENAMED, RELOCATED OR RETIRED UNDER THIS TO.** R-9's move
       needs Andrew's word and R-10/R-11 need a canonical-or-not decision on evidence you are producing.
       **Delivering the evidence and taking the decision are different acts, and this TO is the first.**

    4. EACH ROW GETS A RECOMMENDATION WITH ITS COST. Not a preference — what closing it would touch,
       what breaks if the field is wrong, and who must decide.

    5. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.8.0_AE_CloudComp/deliverables/MDPF_R9_R12_CONSUMER_CENSUS_20260807.md</file>
      <file action="reference">data/mdpf/config/route_bindings.yaml</file>
      <file action="reference">docs/architecture/MDPF_REMEDIATION_REGISTER.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Census every field named in R-9/R-10/R-11 with denominators.</requirement>
    <requirement id="2">Deliver R-12's completeness check against the actual key listing.</requirement>
    <requirement id="3">Recommend per row with cost; decide nothing that is served.</requirement>
    <requirement id="4">MCP `0.4.0_DS_ClientPlatform` before treating `route_bindings.yaml` as settled.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">The consumer census + R-12 completeness check + per-row recommendations.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT move, rename or retire any served field. Census only.</rule>
    <rule>DO NOT edit `route_bindings.yaml` — DS holds it under W1-1 right now.</rule>
    <rule>DO NOT report an absence without its denominator and its blind spots.</rule>
    <rule>DO NOT re-report the 3 underscore twins as outstanding — executed @46d3bf3f32.</rule>
    <rule>DO NOT surface findings as new threads mid-TO. ⛔ **THE FLOW IS: MAKE A PLAN, COMPLETE THE
    PLAN, THEN REVIEW** (Andrew-direct 2026-08-07). Anything you find that is outside this TO goes to
    the SURPRISE CHANNEL as ONE LINE to COO and is BANKED — it does not re-open this TO. The bar for
    breaking flow is EXISTENTIAL.</rule>
    <rule>DO NOT build any alert, alarm, checker or monitor.</rule>
  </do_not>
</task_order>
