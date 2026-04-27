# Task Order: ADVI_INFGRD.005 — DS: Generalize Partner Firm Predicate (Post-MVP)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-infgrd-005</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>LOW — post-MVP, defer until second partner onboarding concrete need emerges</priority>
  </metadata>

  <objective>
    ADVI_INFGRD.002 wires the PARTNER_FIRM_TAGS dict and INFLECTION_ADVISOR_FIRM_TAG constant
    as a forward-compatible structure. This TO extracts the full `--partner` flag parameterization
    so a future partner (e.g., Keil-as-partner, or a third onboarding) can reuse the same
    silver script with a different `--partner` arg rather than forking convert_orion_to_silver.py.

    Do NOT begin until .001 + .002 + .003 lessons are validated and a second partner
    onboarding is in concrete planning. Premature abstraction risk is higher than the
    benefit at MVP.
  </objective>

  <scope>
    <task id="1" label="Extract partner param to _apply_scopefix()">
      Refactor:
        def _apply_scopefix(df, source_desc, partner='inflection'):
            firm_tag = PARTNER_FIRM_TAGS[partner]
            ...

      The `partner` param defaults to 'inflection' for backwards compatibility with
      existing callers. Add new CLI arg `--partner` to the silver script top-level
      argparse (default: 'inflection').
    </task>

    <task id="2" label="Parameterize Guard B bounds per partner">
      Guard B AUA bounds are currently hardcoded [$50M, $400M] for Inflection.
      Extend to a per-partner config:
        PARTNER_AUA_BOUNDS = {
            'inflection': (50_000_000, 400_000_000),
            # Future: 'keil': (X, Y), etc.
        }
    </task>

    <task id="3" label="Update silver schema spec + PARTNER_FIRM_TAGS">
      Document the `--partner` flag and PARTNER_FIRM_TAGS dict in silver schema spec.
      Add example for how to onboard a new partner: add tag to dict + bounds to config.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Pre-commit gate passes: .tools/ds-commit-gate.sh (all three checks exit 0).
    </criterion>
    <criterion id="2">
      Existing Inflection behavior unchanged: running without --partner flag produces
      identical output to ADVI_INFGRD.002 implementation (regression test via guard C
      diagnostic output comparison).
    </criterion>
    <criterion id="3">
      Running with --partner=inflection (explicit) also produces identical output.
    </criterion>
    <criterion id="4">
      from __future__ import annotations remains first import.
    </criterion>
    <criterion id="5">
      Commit uses --only pathspec. Author attributed to 0.4.0_DS_ClientPlatform.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>LOW priority. Do not start before .002 is validated in production (INFGRD.003
    chain run complete, INFGRD.004 smoke PASS). Lessons from .002 implementation may
    reveal better abstraction points.</constraint>
    <constraint>No emojis in code, logs, or print statements.</constraint>
    <constraint>Backwards compatibility required — no breaking change to existing
    silver script CLI behavior without explicit COO approval.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFGRD.002"
                status="open"
                note="Must be validated in production (INFGRD.003 + .004 complete)
                before abstracting. Premature abstraction before lessons are learned
                increases risk."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">convert_orion_to_silver.py with --partner flag + per-partner
    bounds config. Silver schema spec updated with onboarding guide.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO confirming backwards-compat regression
    verified.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md §5.4 — Generalize for future partner firms</ref>
    <ref type="gate">ADVI_INFGRD.002 — must be production-validated before this TO is dispatched</ref>
  </references>
</task_order>
```
