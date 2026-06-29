<to_id>NFRA_COMPRAIL.TO-5</to_id>
<project>NFRA_COMPRAIL</project>
<title>Coverage-audit backlog (intents -> tool/no-tool -> build list) + post-enforce hud-telemetry re-measure & tune</title>
<assigned_to>3.0.0_SA_CVO</assigned_to>
<issued_by>2.0.0_SA_COO (PRD decomposition, 2026-06-18; hardened per CTO DELTA 49b236dea)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete</status>
<!-- COMPLETE 2026-06-26 (3.0.0_SA_CVO). Both legs delivered + accepted; status reconciled
     2026-06-29 startup (was stale-pending). LEG A (AC4): coverage-audit backlog seed 0596969bd
     + CTO-RAVC fold a0aec78b7 -- intent->tool/no-tool prioritized build-list (aws_freshness P1
     candidate). LEG B (AC5): post-enforce telemetry 8b8795ac2 (COO-ACCEPTED) -- Gate-1 first full
     day, override rate collapsed 2.80%->0.19% (~15x), all 6 DENY classes tool-routed/0 escapes,
     LEG-A aws_freshness candidate de-escalated P1->P2 (0 overrides under enforce, comp-freshness F3
     258d968bb closed the gap), gap-B reason-capture CONFIRMED FIXED; recommended keep-enforcing +
     next-tier ramp. NFRA_COMPRAIL PROJECT remains active under TO-6 (CVO LEG-D); only TO-5 closes. -->
<priority>MEDIUM-HIGH — two legs, different gates. LEG A (coverage-audit backlog seed) can START EARLY (seeded from the existing HUD log + comp-tools.yaml `replaces` fields) — it informs TO-2's coverage-proof + TO-4's per-tier coverage gate, so an early seed is high-leverage. LEG B (post-enforce telemetry re-measure + tune) is GATED on TO-4 (needs a post-enforce window + the override-marker feed). Extends the NFRA_TOOLHUD hud3_classify CVO follow-on already on BACKLOG.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPRAIL_PRD.md (49b236dea) — §5 coverage audit, §6 rollout step 5, AC4 + AC5</ref>
  <ref type="baseline">NFRA_TOOLHUD hud3_classify baseline (bdf7a0a9a, CVO-owned): 425 arg-level transcripts; ~15-20% of clean repo relationship-searches comp-answerable; comp-pipescript + portal-tools = ~80% of bypass volume; 5 tuned regexes + the negative filter + 6 ranked question->tool mappings; reproducible hud3_classify.py = the BEFORE.</ref>
  <ref type="intent-sources">org/modules/graph/comp-tools.yaml `replaces` fields (the declared intent map) + the FLOOR/HUD log + the TO-2/TO-4 override-marker hits (the LIVE gap feed).</ref>
</references>

<scope>
**LEG A — coverage-audit backlog (AC4; can seed EARLY):**
Enumerate the inspection/relationship INTENTS agents actually have (from the HUD log + comp-tools.yaml `replaces` fields + the comp-which run-the-primitive log from TO-2). For each: is there a comp-tool? A recurring intent with NONE = a tool to BUILD, not a grep to bless. Output: a prioritized comp-tool coverage backlog (intent -> tool/no-tool -> build-priority). This is the data behind TO-2's "proven complete-enough" coverage-proof + TO-4's per-tier coverage gate — so seeding it EARLY (off existing data, before enforcement) directly de-risks the gate. Refine it continuously off the override-marker telemetry once TO-4 lands (the live feed of real graph holes).

**LEG B — post-enforce telemetry re-measure & tune (AC5; gated on TO-4):**
Re-run hud3_classify over the POST-enforce transcript window (the AFTER vs the bdf7a0a9a BEFORE). Measure: comp-tool usage UP / raw-bypass DOWN; the per-tier deny/allow + override-marker stream; native-tool gate friction (override rate, repeat-override intents); any material legit-work breakage. Tune COMPWHICH_EVERY + the gate patterns + the override convention to the DATA (not prior). Feed repeat-override intents back into LEG A's build-list.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="LEG A, before authoring the backlog">
    <step>
      <run>hud3_classify.py over the existing HUD-log window + a parse of comp-tools.yaml `replaces` -> the intent inventory + which intents route vs have no tool</run>
      <expect>A reproducible intent->tool/no-tool inventory grounded in REAL asked questions (the NFRA_TOOLHUD lesson — not a-priori guesses). The no-tool recurring intents = the build-list seed.</expect>
    </step>
  </phase>
  <phase id="2" when="LEG B, post-enforce">
    <step>
      <run>hud3_classify.py over the post-enforce window (the AFTER) + parse the TO-4 per-tier deny/allow + override-marker log</run>
      <expect>Quantified BEFORE->AFTER: comp-usage up / bypass down; override rate + repeat-override intents surfaced; no material legit-work breakage (or it's surfaced loud + routed). Tuning deltas recommended off the data.</expect>
      <if_mismatch>If bypass did NOT drop or override-friction is high on legit work, that is the tuning signal — recommend pattern/threshold/coverage changes; do NOT silently accept a flat result (the NFRA_TOOLHUD follow-on lesson).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **LEG A feeds TO-2 + TO-4 (de-risks the gate):** the coverage-audit backlog is the evidence behind "the rail is complete-enough to gate native." Converge with CTO on the intent taxonomy + the comp-which run-the-primitive log schema so the audit consumes it cleanly.
- **LEG B gated on TO-4:** needs the post-enforce window + the override-marker/deny-allow log TO-4 emits. Converge with CTO on that log's schema (parseable).
- **Repeat-override intents -> build-list:** CVO surfaces them; the actual tool-build is a CTO lane (or a new TO COO cuts off the backlog). CVO produces the prioritized list, not the builds.
- **No served-artifact / pipeline touch** — this is telemetry + an audit doc.
</cross_domain_coordination>

<acceptance_criteria>
- AC4 (PRD §9): coverage-audit backlog produced (intents -> tool/no-tool -> prioritized build list), fed initially by HUD log + comp-tools.yaml `replaces` and continuously by the override-marker telemetry. Reproducible.
- AC5 (PRD §9): post-enforce hud-telemetry shows comp-tool usage UP / raw-bypass DOWN vs the bdf7a0a9a BEFORE; override-friction + any legit-work breakage quantified + surfaced; tuning recommendations grounded in the data.
- LEG A delivered early enough to inform TO-2's coverage-proof + TO-4's per-tier gate (not only post-enforce).
- Session log Compiler Tools section reproduces every `<run>` with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Telemetry re-measure + an audit/backlog doc. No served artifact, pipeline, or producer touched.</no_reprocess_needed></data_reprocess_scope>
