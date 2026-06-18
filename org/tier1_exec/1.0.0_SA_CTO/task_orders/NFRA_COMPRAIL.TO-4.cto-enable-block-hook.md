<to_id>NFRA_COMPRAIL.TO-4</to_id>
<project>NFRA_COMPRAIL</project>
<title>Enable the PreToolUse GATE in hardness order: raw-aws-INSPECTION -> repo-file-grep -> native Grep/Glob LAST (permission/override, verified contract, exhaustive FP tests); native Read NOT gated</title>
<assigned_to>1.0.0_SA_CTO</assigned_to>
<issued_by>2.0.0_SA_COO (PRD decomposition, 2026-06-18; hardened per CTO DELTA 49b236dea)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>staged</status>
<priority>HIGH — but GATED + SEQUENCED. The enforcement wall (PRD rollout step 4, hardened). Three enable tiers in HARDNESS ORDER, each enabling ONLY after its rail-coverage is proven; native Grep/Glob is the LAST + broadest + most friction-sensitive tier. DO NOT enable ANY tier until (a) TO-2 landed + proven-complete-enough (rail never-dead-ends — else gating DEADLOCKS) AND (b) TO-3 landed (CLAUDE.md amended + fabric announced — else surprise wall). A gate on EVERY Bash + native Grep/Glob is the highest-stakes change in this initiative; the build phase owns the test burden. COO flips staged->pending + GO's per-tier as gates clear.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPRAIL_PRD.md (49b236dea) — §3 hardened enforcement table, §3 Permission/override section, §6 rollout step 4 (hardness order + per-tier coverage gate), §7 VERIFIED deny mechanism (do not re-derive), §8 risks, AC2</ref>
  <ref type="verified-mechanism">PRD §7 (claude-code-guide 2026-06-18, verified — do NOT re-derive): PreToolUse DENY = stdout {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"<reason>"}} + EXIT 0. permissionDecisionReason surfaced to the MODEL (self-corrects). ALLOW = exit 0 + no permissionDecision. ADD-CONTEXT = additionalContext (the floor's mechanism). permissionDecision:"ask" = literal human prompt (Andrew interactive only). Exit 2 = block but JSON ignored -> use exit-0 + deny-JSON. Matcher gates which calls hit the hook; decide inside from .tool_name + .tool_input.command.</ref>
  <ref type="floor-coexistence">.tools/hooks/comp-tool-hud.sh (c985b8d9e FLOOR, additionalContext nudge on Grep/Glob) — the new gate must COMPOSE with the floor (floor nudges, gate denies).</ref>
  <ref type="dependencies">TO-2 (comp-which proven complete-enough) + TO-3 (Rule-20 amend + announce) — BOTH hard prerequisites for ANY tier.</ref>
</references>

<scope>
Enable the gate in THREE tiers, HARDNESS ORDER (PRD §6 step 4), EACH tier enabling only after its rail-coverage is proven:

**TIER 1 — Raw-aws-INSPECTION in Bash (first; cleanest, full comp coverage, no deadlock):**
deny `aws iam get*/list*`, `aws s3api get-bucket-policy`, `aws lambda get-policy`, `aws dynamodb scan/get-item/query`, `aws cloudfront ...`, `aws apigateway ...` -> deny-reason routes to comp-iam / comp-aws / comp-freshness / comp-routes. EXEMPT operational aws (invoke/cp/sync/deploy/update/TF/start-build) + generic `s3 ls`.

**TIER 2 — repo-file-grep in Bash (pipe-scoped):**
deny `grep`/`rg`/`find` targeting repo files/dirs -> route to comp-which / on-rails comp-grep. SCOPED: a pipe/output grep (`cmd | grep ...`) is NOT gated (post-processing command output, not searching the estate).

**TIER 3 — native Grep / Glob tools (LAST; the permission/override model — the hardened addition):**
deny-by-default; the agent proceeds ONLY via the auditable override-marker (PRD §3 permission section — the scalable "ask permission for a turn of grep"; logged; repeat-override-for-same-intent = coverage-gap -> build the tool). This is the broadest + most friction-sensitive tier — enable LAST, only after TIER 1+2 are stable AND comp-which coverage is proven complete-enough that gating native won't constantly force overrides. Native **Read NOT gated** (reading a known file is not a search; optional soft nudge only if it looks like a search-substitute). Optional `permissionDecision:"ask"` true-human-prompt wired ONLY for Andrew's interactive sessions.

**Across all tiers:** override-marker honored + logged (exact convention defined HERE, quoted in TO-3's rule + announce — single source of truth); exhaustive false-positive test suite (the high-stakes burden, PRD §8); deny-JSON contract exactly per §7 (exit-0 + deny-JSON, reason surfaced to model).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before ANY tier enables (the gate check)">
    <step>
      <run>Verify TO-2 RAVC2-accepted (comp-which proven complete-enough) + TO-3 RAVC2-accepted (CLAUDE.md amended + fabric announced). Confirm with COO that both gates cleared. For TIER 3 specifically: confirm the coverage-proof shows the rail answers the native-search intents (else gating native deadlocks/over-overrides).</run>
      <expect>Both prerequisites GREEN before TIER 1; the TIER-3 coverage-proof additionally GREEN before native Grep/Glob enables. If any is open, that tier stays staged.</expect>
      <if_mismatch>HOLD that tier. Surface to COO; no tier enables on an open prerequisite. Native Grep/Glob NEVER enables before its coverage-proof.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit (per tier)">
    <step>
      <run>The exhaustive FP test suite for that tier: TIER1 — blocked-inspection-aws (denied+reason) vs operational-aws (allowed); TIER2 — repo-file-grep (denied) vs pipe-grep (allowed); TIER3 — native Grep/Glob (denied w/o marker; allowed+logged WITH marker) vs native Read (allowed). All tiers: deny-JSON contract exit-0 + correct shape per §7.</run>
      <expect>Every case green. ZERO false-blocks on the exempt set (operational aws, pipe-greps, native Read). Override-marker honored + logged. Deny-JSON reaches the model.</expect>
      <if_mismatch>A false-block on operational aws / pipe-grep / native Read is a HARD STOP — fix the patterns. The build phase owns this burden.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after each tier enables">
    <step>
      <run>Live smoke per tier: TIER1 — real `aws iam get-role-policy` denied+routes to comp-iam + model self-corrects; real `aws lambda invoke` NOT blocked. TIER2 — repo `grep` denied; `git log | grep` NOT blocked. TIER3 — native Grep denied w/o marker, proceeds WITH `# rail-checked:` marker (logged); native Read NOT blocked.</run>
      <expect>AC2 demonstrably met per tier; no exempt-set breakage; native Grep/Glob gating works via override.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **HARD gate on TO-2 + TO-3** (both, all tiers); TIER 3 (native Grep/Glob) additionally gated on the coverage-proof (PRD §4/§6 — "each tier enables only after its coverage is proven"). COO confirms per-tier before flipping staged->pending.
- **Floor-hook coexistence (intra-CTO-lane):** the new deny + the existing comp-tool-hud.sh floor (additionalContext on Grep/Glob) both attach to PreToolUse — they MUST compose (floor nudges, this denies; neither swallows the other). Verify the combined hook-chain in the FP suite.
- **settings.json hook registration** — CTO/infra lane; the matcher gates which calls hit the hook (decide inside from tool_name + command).
- **WHOLE-FABRIC blast (amplified by TIER 3):** gating native Grep/Glob affects EVERY agent's core search reflex — this is why announce-then-enforce (TO-3) is a hard prerequisite and native enables LAST. Any agent hitting a false-block / unexpected wall escalates COO -> CTO immediately; the override-marker is the interim unblock.
- **TO-5 (CVO):** the override-marker hits + the per-tier deny/allow log are CVO's telemetry feed (AC5) + the live coverage-gap feed (AC4) — emit them parseable.
</cross_domain_coordination>

<acceptance_criteria>
- AC2 (PRD §9): PreToolUse hook gates raw-aws-INSPECTION + repo-file-grep in Bash AND native Grep/Glob (deny+reason, verified §7 contract, permission/override honored + logged); operational aws + pipe-greps + native Read NOT gated; exhaustive FP suite GREEN; native Grep/Glob enables LAST (after its coverage is proven).
- Sequenced in hardness order: TIER 1 (aws-inspection) -> TIER 2 (repo-file-grep, pipe-scoped) -> TIER 3 (native Grep/Glob, permission/override) — each enabling only after its prerequisites + coverage-proof.
- ZERO false-blocks on the exempt set (operational aws, pipe-greps, native Read) in the FP suite + live smoke.
- The deny-JSON exactly matches §7 (exit-0 + deny-JSON; reason surfaced to the model); optional `ask` mode (Andrew-interactive) does not fire for autonomous agents.
- Override-marker convention matches the one documented in TO-3's CLAUDE.md rule + announce (single source of truth).
- Session log Compiler Tools section reproduces every `<run>` (per tier) with pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>PreToolUse hook + settings.json registration (.tools/, .claude/). No served artifact, pipeline, or producer.</no_reprocess_needed></data_reprocess_scope>
