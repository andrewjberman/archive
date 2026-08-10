# OPAL_ANALYST.TO1 — Durable identity pin in teams-watch.py (P0)

<task_order>
<id>OPAL_ANALYST.TO1</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>complete</status>
<!-- ACCEPTED 2026-08-10 1655Z by 2.0.0_SA_COO~Z. Evidence: fix @0f1bbcf0e (engine + SKILL.md
     arm line, author 0.5.0_AE_OpalETL~Z), session log @0ba5b674e with Compiler Tools section
     reproducing all runs. COO ground-check: pin code verified at source (filter-before-sort,
     _pin_fail no-token/expired/ambiguous paths present); positive 3/3, negative rc=2 no-fallback,
     bare-path compat + discriminating control all reported verbatim. Landed AND exercised —
     TO-2's gate reads satisfied. -->
<priority>P0</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §4.1, §6 TO-1 (v1.0 @d179643ca)</ref>
  <ref type="brief">org/tier1_exec/4.0.0_SA_CRO/deliverables/OPAL_ANALYST_STATE_BRIEF_20260810.md @92e7020f4</ref>
  <ref type="charter">org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/ANDREW_DIRECT_20260810_OPAL_ANALYST_PROJECT_SPINUP.md @1ac23a7e1</ref>
</references>

<scope>
`.claude/skills/teams-assist/teams-watch.py` (the shared /teams-assist monitor ENGINE, built by
0.5.0_AE 2026-06-24) + the `/bbg-teams-assist` SKILL.md monitor-arm line.

**The defect (CTO source-verified @ SITEZ HEAD 1ac23a7e1+):** `read_token()` (~:51-58) selects the
freshest-expiring `opalinvest.dev` token across ALL `mcpOAuth` records — identity-blind. With both
Andrew's (`opal-gateway`) and the concierge's (`opal-gateway-bbg`) tokens valid on this box,
whichever expires later wins — historically Andrew's. The 08-07 mitigation was a session-scratchpad
wrapper that died with its session; a 0.0.3_BG relaunch today re-runs the race.

**The fix (PRD §4.1 IO contract, binding):**
- Add `--server <substring>` / `--identity <sub/UPN>` argument set. When provided, filter
  `mcpOAuth` records to the named server/identity BEFORE the freshest-expiring sort.
- No matching token after the filter = LOUD exit non-zero with a named reason. Never fall back to
  another identity. Expired-only matches = same. Ambiguous multi-match after filter = same
  (never sort-and-hope).
- BARE invocation (no flag) keeps byte-identical current selection behavior — the engine is SHARED
  with Andrew's operator `/teams-assist`; the pin is an ADDITIVE argument, not a behavior change.
- Update `/bbg-teams-assist` SKILL.md so its monitor-arm line PASSES the pin.
- Do NOT recreate any wrapper (`teams-watch-bbg.py` pattern is dead by design — no shadow paths).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>.tools/comp-find "teams-watch"</run>
      <expect>Consumer set unchanged since PRD §5.2: engine at .claude/skills/teams-assist/teams-watch.py; consumers = /teams-assist (operator) + /bbg-teams-assist (concierge); gateway endpoint /teams/poll at infra/aws/ec2/m365-mcp-gateway/app/server.py:579. No new consumer.</expect>
      <if_mismatch>STOP. A new consumer means the additive-arg compatibility analysis is stale — surface to COO~Z before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>python .claude/skills/teams-assist/teams-watch.py --once</run>
      <expect>Bare invocation runs with selection behavior identical to today (operator path preserved). Record which token/identity it selected.</expect>
      <if_mismatch>STOP. Bare-path regression breaks Andrew's own skill. Fix before commit.</if_mismatch>
    </step>
    <step>
      <run>python .claude/skills/teams-assist/teams-watch.py --once --identity opalbloomberg  (exact flag form per your implementation; pin to the opal-gateway-bbg identity)</run>
      <expect>Selected token's identity == pinned identity, with both identities' tokens valid on this box.</expect>
      <if_mismatch>STOP. The pin is the entire point. Do not commit.</if_mismatch>
    </step>
    <step>
      <run>.tools/commit-gate.sh (via safe-commit path on the .py)</run>
      <expect>PASS (py_compile + ruff py39).</expect>
      <if_mismatch>STOP. Gate failure is never intentional; fix.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>NEGATIVE CONTROL (separate invocation, Rule 22a): pin to an identity with NO valid token on this box</run>
      <expect>Loud exit non-zero with a named reason (no-token-for-identity). No fallback selection occurs.</expect>
      <if_mismatch>Surface to COO~Z + CTO~Z: the fail-open path survives and TO-2 stays gated.</if_mismatch>
    </step>
    <step>
      <run>POSITIVE CONTROL (separate invocation): pinned run against the valid opal-gateway-bbg identity, N=3 consecutive</run>
      <expect>Selected token identity == pinned identity on 3/3 runs.</expect>
      <if_mismatch>Surface to COO~Z; do not report TO complete.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
`teams-watch.py` is SHARED with the operator's `/teams-assist` skill (Andrew's own use). The
bare-invocation compatibility requirement above IS the coordination contract — no other active TO
touches this file (verified via comp-find this session; only OPAL_ANALYST TOs are live on this
fabric per the exclusivity ruling). `/bbg-teams-assist` SKILL.md arm line is also touched by no
other open TO.
</cross_domain_coordination>

<acceptance_criteria>
1. With both identities' tokens valid on the box: pinned invocation's selected token identity ==
   pinned identity on N=3 consecutive runs (Phase 3 positive control, runs reproduced in log).
2. No-match / expired-only / ambiguous cases exit non-zero with a named reason (Phase 3 negative
   control reproduced in log).
3. Bare invocation selection behavior byte-identical to pre-change (Phase 2 step 1 recorded).
4. `/bbg-teams-assist` SKILL.md arm line passes the pin.
5. Session log includes a Compiler Tools section reproducing every `<run>` above with observed
   output and explicit pass/fail vs `<expect>`. Missing rows = REWORK.
6. Commit via safe-commit.sh under your own author line; NO push (site-Z integration is MSTR~Z's
   window, LD-0367).
</acceptance_criteria>

<notes>
Gates: none — this TO is the gate-clearer for TO-2 (relaunch). Effort: small. On completion,
report to 2.0.0_SA_COO~Z with commit hash + the three exercised-run outputs; TO-2 GO follows.
</notes>
</task_order>
