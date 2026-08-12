# OPAL_ANALYST.W3 — W3a `/market` (page grain) + W3b NEWS SUBSYSTEM (the declared grain exception, ELEVATED BAR)

<task_order>
<id>OPAL_ANALYST.W3</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-11</date>
<status>complete</status>
<!-- CLOSED 2026-08-12 ~0450Z by 1.0.0_SA_CTO~Z. W3a CERTIFIED, W3b CERTIFIED + CLOSED @06f010123b,
     proof-of-spec VALID rc=0, 8 of 10 PASS. C9 (6 DDB tables) DELIVERED @db9b1cbe7d after I refused
     to descope it -- it was real work and it got done.
     ⛔ C1 AND C5 CLOSE AS *FAIL*, PERMANENTLY, AND ARE NOT ARGUED DOWN:
       C1 -- W3b carries no axis_declaration.json where 5 of 5 comparable runs do. NOT bookkeeping:
             it DEGRADED A LIVE GUARD TO ONE LIMB at closure, three hours later, on another seat's
             tool. Inherited from the predecessor seat; UNSATISFIABLE NOW because precedence cannot
             be re-established once measurement has begun.
       C5 -- no pre-filed prediction artifact for either unit. MY specification ambiguity (the W2
             predicate's inheritance into W3 was never stated); UNSATISFIABLE NOW because a
             prediction cannot be retro-filed.
     THE TO CLOSES BECAUSE THE WORK IS DELIVERED AND THESE TWO CRITERIA CANNOT BE SATISFIED BY ANY
     FURTHER WORK ON THIS UNIT -- not because they were met. Rewriting either to make it pass would
     be the retrofit this method exists to prevent, and the assignee refused to flip on a
     validator-clean instance (9.8.1-X) rather than take the cheap close.
     >> BOTH REMEDIES ARE DISCHARGED FORWARD ON W4b, WHICH IS WHAT DISTINGUISHES LEARNED FROM
     EXCUSED: axis+collapse rule committed BEFORE measurement with precedence evidenced by the commit
     graph @b30bd4460a, and PREFILED_PREDICTION.md @952dc14240 filed before Plane B with its scope
     limit stated. -->
<priority>P1</priority>
<!-- Two units, one TO, SEQUENCED W3a THEN W3b (the page's non-news surface first, so the subsystem
     run inherits a measured page context rather than measuring around an unmeasured one). GO is
     immediate on /macro's close. Andrew's own words govern W3b's bar: "The news definitely has to
     be atom_decomped and validated closely because theres some archival/unused stuff laying around
     that we still have to clean up." -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 @HEAD — §9.1.1 (grain exception), §9.5 (elevated bar), §9.8.1 A–M + K-series, §9.9 items 3+5</ref>
  <ref type="prior-art">ARTIFACT_CENSUS_NEWS.yaml @ddd918d8c (+ the fork-verdict corrections @c24cc4cab) — Option-C two-plane scope: news-DERIVED artifacts owned by news wherever rendered + the 4 active / 2 dormant DDB tables. INPUT, never evidence. The `/market` NON-news surface is UNCENSUSED — W3a is genuinely first-source.</ref>
  <ref type="residue">the 08-10 census F2: 720 orphaned history keys + the dead drilldown leg; features.ts USE_SEMANTIC_TRENDING DEPRECATED w/ deleted EventBridge schedules — PRIOR CLAIMS to re-ground, not facts</ref>
  <ref type="tools">your `enumerate_set.py` (CERT-7 guard) — REQUIRED for every W3 denominator; the news residue counts are exactly the class it exists for</ref>
</references>

<scope>
**W3a — `/market` at PAGE grain**, run home `runs/portal-page-market/<stamp>/`. The news plane is
W3b's and is POINTED AT, never re-censused (Option-C ownership). In scope beyond the panels: the
page-level relations plane (footer bindings vs the K11-narrowed predicate — pre-file the prediction;
`/market` is the page the whole register has been converging toward), and **§9.9 item 3 settled in
passing**: `/dev/page-surface-control`'s PROD reachability — one `comp-routes behaviors` + a bundle
grep; if reachable it becomes an owned blocking item THAT TURN, surfaced to me.

**W3b — NEWS SUBSYSTEM grain** (the one declared exception), run home
`runs/news-subsystem/<stamp>/`. Entities: the SentimentPanel surface + the 9-Lambda pipeline +
the 4 active / 2 dormant DDB tables + the news-derived S3 artifacts + **the residue families as
first-class entities** (the 720-key orphaned history family; the dead drilldown leg; the deprecated
semantic-trending chain with its deleted schedules and never-updating key). A pipeline stage is an
entity; a Lambda's IAM surface is a NAMED BOUNDARY (comp-tooling limit does not apply here — this is
an application run — but Rule 7 closure does).
</scope>

<requirements>
  <requirement id="1">Full §9.8.1 A–M regime, both units: K-derivation, K.1 exact packet (no c1/c2), K.2 attestation at certification, sealed plants (two units = two plants, sealed separately), evidence triples, lens-diverse DRY.</requirement>
  <requirement id="2">**Every denominator through `enumerate_set.py`** — set captured to a file, figures derived from the file, the printed denominator carrying its set's path. The 720-key residue claim is re-derived this way or reported as unverified; it is never inherited.</requirement>
  <requirement id="3">**W3b ELEVATED BAR (§9.5, his words):** (a) CLOSE validation — no INFERRED cell stands in the final rectangle without an owned-unknown entry; (b) **residue DISPOSITION with its denominator, per residue class** — DISPOSITION IS NOT DELETION (NEVER#3; the register is the deliverable, the act is Andrew's); (c) the declared/deployed/invoked separation run over the PIPELINE, not just the artifacts — a Lambda with no event source, a schedule that was deleted, and a key nothing updates are three DIFFERENT states and each gets its own cell.</requirement>
  <requirement id="4">**Predicate rows for both units** (K11 form, binding-surface precondition) with pre-filed predictions — and the SECOND defect class ("no date shown") checked explicitly on both surfaces.</requirement>
  <requirement id="5">Cadence: hand W3a to CVO~Z at DRY before W3b's runs begin their measurement — the certifier should not receive both units as one cliff, and W3b's plant should not be in the ground while W3a's is unresolved.</requirement>
  <requirement id="6">CVO~Z's trend-analysis CONCEPTS (Andrew's ask) ride their W3b certification hand-back, not your run — your rectangle gives them the measured substrate; you do not author concepts.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-estate` news thread first contact; `comp-routes behaviors` for W3a's serving claims + the §9.9-item-3 probe; DDB describe-table for live counts (stamped, per the census's own honesty rule).</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8,C9,C10   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — two certifications (W3a page, W3b subsystem), the trend-concepts deliverable on W3b, register extension both units.
- **1.0.0_SA_CTO~Z** — §9.9-item-3 outcome lands on me either way (settled or escalated); residue register routes to me for the Andrew disposition packet.
- **0.8.0_AE_CloudComp~Z** — comp-tool defects to them as prior claims, theirs to you likewise.
- Lane commits, no push; msgfiles per the shared-box convention.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bars committed BEFORE measurement, per unit (two declarations — the grains differ and one bar cannot serve both).</criterion>
  <criterion id="C2">W3a rectangle certified; news plane POINTED not re-censused; §9.9 item 3 settled with the probe's evidence (or escalated same-turn if PROD-reachable).</criterion>
  <criterion id="C3">W3b rectangle certified at SUBSYSTEM grain; pipeline stages as entities; the three dead-states (no-event-source / deleted-schedule / never-updated-key) separated per artifact.</criterion>
  <criterion id="C4">**Residue register: every residue class with a disposition + a file-backed denominator (enumerate_set.py), the 720-key claim re-derived or marked unverified.** Zero acts taken.</criterion>
  <criterion id="C5">Predicate rows both units, predictions PRE-FILED, second-class ("no date shown") checked explicitly.</criterion>
  <criterion id="C6">Both plants caught-or-VOIDed under K.2 attestations; consumables derived from dry; packets K.1-exact.</criterion>
  <criterion id="C7">CVO trend-concepts deliverable exists on the W3b hand-back (theirs; your criterion is that your substrate enabled it and your rectangle cites it).</criterion>
  <criterion id="C8">Census reconciliation both units; F2 prior claims verified/refuted at source.</criterion>
  <criterion id="C9">Declared exclusions + surprises; the DDB dormant tables' disposition stated.</criterion>
  <criterion id="C10">Session log; proof-of-spec instance validator-clean BEFORE any complete flip.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9,C10</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/OPAL_ANALYST.W3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Two run packages (portal-page-market, news-subsystem), full K-regime sets</deliverable>
  <deliverable type="document">**The residue DISPOSITION REGISTER** — the artifact Andrew's cleanup decision reads from</deliverable>
  <deliverable type="document">Proof-of-spec instance + session log</deliverable>
</deliverables>

<do_not>
  <rule>**Nothing is deleted, stopped, or disabled** — residue gets dispositions; the acts are Andrew's (NEVER#3, Rule 9, and his own "we still have to clean up" names a FUTURE act, not this TO's).</rule>
  <rule>No monitors/alerts (moratorium) — a dead schedule is a FINDING, not a thing to re-arm.</rule>
  <rule>News plane never re-censused in W3a (Option-C ownership boundary).</rule>
  <rule>No denominator off a pipeline (K10 + CERT-7; enumerate_set.py or unverified).</rule>
  <rule>No push.</rule>
</do_not>
</task_order>
