<to_id>NFRA_COMPRAIL.TO-2</to_id>
<project>NFRA_COMPRAIL</project>
<title>comp-which becomes the universal rail that NEVER dead-ends (route to rich tool OR run an on-rails scoped/logged comp-grep/comp-ls)</title>
<assigned_to>1.0.0_SA_CTO</assigned_to>
<issued_by>2.0.0_SA_COO (PRD decomposition, 2026-06-18; CTO-authored PRD f02bb68f4)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete</status>
<!-- COMPLETE per ground-truth reconciliation 2026-07-14 (1.0.0_SA_CTO startup, Step 4).
     EVIDENCE: AC1 exercised live this session -- classifiable question routes (ranked candidates,
     rank-6920.yaml); tool-less search ("zqx-nonexistent-marker-98765") auto-RAN the on-rails comp-grep
     (repo-scoped, .gitignore-aware, denominator printed: 20,579 files scanned / 972 sovereign-held
     excluded, logged to org/mcp/comp-which-rail.log) -- comp-which demonstrably never dead-ends.
     Behavior is CLAUDE.md Rule 21 law ("routes OR RUNS the on-rails comp-grep/comp-glob (never
     dead-ends)"). Regression + coverage-proof bars re-taken by NFRA_COMPCLOSE Phase E (coverage hole
     29.0%->26.6%, recall@3 90.9% held, gibberish 0/40, all four self-test suites green; CVO~Z verified
     SOUND, verdict 3d816c650). NFRA_COMPRAIL enforcement ramp (TO-4 gate tiers) proceeds per PRD
     announce-then-enforce -- separate from this build TO. -->

<priority>HIGHEST — THE CRITICAL PATH OF THE WHOLE INITIATIVE (PRD §4, hardened 49b236dea). With native Grep/Glob ALSO now gated (PRD §3, Andrew 2026-06-18 — the hive-brain hardening), this is no longer a nice-to-have: a gated agent whose search the rail cannot answer is BLOCKED (forced to override or stall). comp-which-never-dead-ends + on-rails comp-grep is what makes gating-native SAFE AT ALL — it MUST be built AND proven complete-enough FIRST, before ANY gate tier enables. CTO confirmed already starting the build ("either way it's mine"). GO'd NOW; this TO is the RAVC2 tracking artifact for the build in flight.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPRAIL_PRD.md (v0.1) — §2 principle, §4 (this TO), §5 coverage-audit feed, §6 rollout step 2</ref>
  <ref type="predecessor">NFRA_TOOLHUD (complete 2026-06-16): .tools/comp-which (the existing router — curated CVO-6 rules + manifest-fuzzy backstop) + .tools/hooks/comp-tool-hud.sh (the floor's intercept). comp-which-rail EXTENDS the existing router.</ref>
  <ref type="floor">c985b8d9e — rollout step 1 FLOOR shipped: comp-which-first every-time advisory nudge on unclassified native searches.</ref>
  <ref type="catalog">org/modules/graph/graph-call-manifest.yaml (tools_index, meta.comp_which.router) + org/modules/graph/comp-tools.yaml (`replaces` fields — the intent map).</ref>
</references>

<scope>
Make comp-which the single reflex that ALWAYS lands the agent on a rail. Two behaviors:
1. **ROUTE** — when a rich comp-tool fits the exact use, comp-which returns the canonical call (its current job, made comprehensive against the manifest tools_index + comp-tools.yaml `replaces` intents). Close the gaps where a real classifiable intent currently falls through.
2. **RUN-THE-PRIMITIVE (the new behavior, the non-dead-end)** — when NO rich tool fits, comp-which itself RUNS an on-rails primitive: a scoped, .gitignore-aware, **logged** comp-grep / comp-ls (Andrew's "make a comp-grep or whatever"). The agent's single reflex stays `comp-which`; even the primitive case is on the rail (repo-scoped + audit-logged), never a bare bypass.

HONEST TRADEOFF (PRD §4, build to it — do NOT pretend comp-grep is free): a comp-grep wrapping ripgrep is SLOWER than the native Grep tool and adds NO relationship context for a plain string search. Its value is (a) keeping the Bash-side bypass on an audited rail and (b) auto-routing when the query is actually classifiable. The native Grep tool stays the sanctioned fast path for plain finds (TO-3 mandate+nudge, NOT blocked) — comp-grep is the rail for the Bash-side BLOCKED case (TO-4), not a replacement for native Grep.

The logged output of comp-grep/comp-ls + the route-vs-run decision is the live feed for the coverage-audit (TO-5 / PRD §5): a recurring run-the-primitive for the same intent = a tool to BUILD.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before authoring">
    <step>
      <run>comp-which "<a sample of the real bypass-intent questions from the NFRA_TOOLHUD hud3_classify baseline (bdf7a0a9a) — gold-id / S3-key / lambda / portal / IAM>"</run>
      <expect>Map which intents ROUTE cleanly today vs which dead-end. The dead-ends are the gap TO-2 closes (route them) or the residual (run-the-primitive). Ground the rail against ACTUAL asked questions, not a-priori guesses (the NFRA_TOOLHUD lesson).</expect>
      <if_mismatch>If comp-which is missing for the box, surface to COO — but it exists (NFRA_TOOLHUD shipped it); this is an extend, not a build-from-zero.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>ds-commit-gate / py_compile + the comp-which self-test (the 6 high-traffic questions from NFRA_TOOLHUD must still route correctly + gold-id substitution intact) + a NEW test that a no-rich-tool search RUNS comp-grep/comp-ls on the rail (logged, .gitignore-aware) rather than dead-ending</run>
      <expect>All existing routes green (no regression) + the never-dead-end behavior demonstrated on a search with no rich-tool answer.</expect>
      <if_mismatch>Fix before commit. A regression in the existing 6 routes is a hard stop.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>End-to-end: a deliberately tool-less repo search via comp-which -> confirm it runs the on-rails comp-grep (scoped + logged), and a classifiable search -> confirm it routes to the rich tool. Capture both in the session log.</run>
      <expect>AC1 demonstrably met: comp-which never dead-ends.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-4 (CTO, the block) HARD-DEPENDS on this** — the PreToolUse deny on raw repo-file-grep routes the agent to comp-which; if comp-which can still dead-end, the block deadlocks. TO-2 MUST land before TO-4 enables. Same CTO lane, so intra-lane sequencing.
- **TO-3 (CLAUDE.md amend + announce)** documents the comp-which-first reflex + the override-marker; the announce tells the fabric to rely on comp-which — so comp-which must never-dead-end (this TO) BEFORE the COO announce fires. Coordinate the land-order with COO.
- **The floor hook (comp-tool-hud.sh, c985b8d9e)** and this rail share the comp-which surface — keep them coherent (the floor nudges toward comp-which; this makes comp-which never-dead-end). Intra-CTO-lane.
- **TO-5 (CVO)** consumes the comp-grep/comp-ls run-log + route-vs-run telemetry as the coverage-audit feed — emit it in a parseable form CVO can classify. Converge on the log schema with CVO.
</cross_domain_coordination>

<acceptance_criteria>
- AC1 (PRD §9): comp-which NEVER dead-ends — routes to the rich tool when one fits OR runs an on-rails scoped/.gitignore-aware/logged comp-grep/comp-ls when none does; demonstrably handles a search with no rich-tool answer on the rail.
- COVERAGE-PROOF (the new bar — PRD §4 "proven complete-enough FIRST"): demonstrate the rail answers the REAL bypass-intent corpus (the NFRA_TOOLHUD hud3_classify baseline bdf7a0a9a + comp-tools.yaml `replaces` intents), not just one synthetic case — so gating native (TO-4) won't constantly force overrides. This proof is what unlocks the TO-4 per-tier gate; the residual gaps it surfaces seed the TO-5 coverage-audit backlog.
- No regression: the NFRA_TOOLHUD 6 high-traffic routes + gold-id substitution still pass.
- The run-the-primitive path emits a parseable audit-log line (route-vs-run + intent) — the TO-5 coverage-audit + override-marker telemetry feed.
- Session log Compiler Tools section reproduces every `<run>` above with observed output + explicit pass/fail vs `<expect>`. Missing = REWORK.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Pure tooling change to comp-which (.tools/) + an on-rails comp-grep/comp-ls primitive. No served artifact, pipeline, or producer touched.</no_reprocess_needed></data_reprocess_scope>
