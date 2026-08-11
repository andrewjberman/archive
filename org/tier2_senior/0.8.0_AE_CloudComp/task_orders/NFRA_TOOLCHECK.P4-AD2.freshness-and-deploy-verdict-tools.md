# NFRA_TOOLCHECK.P4-AD2 — atom_decomp run 2: the FRESHNESS + DEPLOY verdict tools

<task_order>
<id>NFRA_TOOLCHECK.P4-AD2</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~Z</issued_to>
<date>2026-08-11</date>
<status>complete</status>
<!-- COMPLETE 2026-08-11 ~2215Z by 0.8.0_AE_CloudComp~Z. Run freshness-deploy-verdict-tools__20260811T2020Z
     CERTIFIED PASS @1dea476ca5 (CVO~Z; mutant caught as a fabricated coupling on three limbs; the
     in-family ssot_validate structural_changes finding independently reproduced + escalated).
     Proof-of-spec validated rc=0 VALID (positional, rc-checked) BEFORE this flip. Closure @d745c9a041.
     Crown deliverable: NEVER#1's mechanism resolved as a THREE-WAY SPLIT, exercised. C1-C8 all PASS. -->

<priority>P1</priority>
<!-- Run 2 of the instruments program. P4-AD1's TO is the TEMPLATE — everything there binds here
     unchanged (§9.8.1 A-M regime, K/K.1/K.2 + your shared-tree scratchpad practice, exercised-
     never-read, priors-under-test markers, CVO certifies, findings-only, boundary hard). This TO
     states only the DELTAS. GO immediate; no release gate — the program is running. -->

<references>
  <ref type="template">NFRA_TOOLCHECK.P4-AD1 @62b61357cd + its completed run `comp-verdict-tools__20260811T1931Z` (CERTIFIED @2c0946081a) — your own worked example now</ref>
  <ref type="priors">CLAUDE.md NEVER#1 (trading-calendar law) + Rule 20/21 HUD rows + `comp-freshness`'s `freshness_basis: trading-day-frontier` clause — ALL PRIORS-UNDER-TEST, marked per the seed-(a) ruling</ref>
</references>

<scope>
**ONE run. Subject: `freshness-deploy-verdict-tools`. Run home:
`runs/freshness-deploy-verdict-tools/<stamp>/`.**

**Entities, three:** `comp-freshness` (staleness verdicts — **the estate's NEVER#1 instrument**:
CLAUDE.md's first NEVER rule states a `comp-freshness` entry without `freshness_basis:
trading-day-frontier` "silently falls back to flat-hours and WILL false-alarm every Monday", and
that instrument's own verdict is named "not a second opinion, the same error" — no prior claim in
the estate carries higher stakes or has ever been exercised as a battery) · `comp-pipescript`
(the `deployed` MATCH/STALE/MISSING verdict surface + `io`'s rc=2 refusal contract) ·
`comp-estate` (its provenance/vintage header verdicts — the `UNKNOWN VINTAGE` and stale-snapshot
declarations Rule 20 makes load-bearing).

**The Monday question is this run's crown battery:** exercise `comp-freshness` across a
weekend-boundary fixture set (Friday-fresh artifacts read on a synthetic Monday/Tuesday frame) and
measure which verdicts each config shape actually produces. **If the flat-hours fallback fires
where the law says it will, that is the estate's most expensive documented defect CONFIRMED AS
CURRENT with an exercise; if it does not, a NEVER rule is resting on a stale mechanism — either
verdict is estate-grade.**

**Boundary unchanged and hard:** comp tooling only; DDB/S3 data-plane reads to build fixtures are
operational and fine; broker/supervision surfaces remain named boundaries.
</scope>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bar committed BEFORE measurement (fresh declaration — the AD1 axis does not automatically fit; state what carries and what does not).</criterion>
  <criterion id="C2">Rectangle schema-valid, evidence triples, file-backed denominators (`enumerate_set.py` discipline for any set you count).</criterion>
  <criterion id="C3">**Every verdict-mode claim EXERCISED** — the Monday battery above all: per config shape, the produced verdict cited from a run, with the fixture set file-backed. CLAUDE.md's NEVER#1 mechanism claim verified or refuted AS CURRENT, at source and by exercise, disagreement named loudly either way.</criterion>
  <criterion id="C4">DRY by convergence, lens-diverse.</criterion>
  <criterion id="C5">CERTIFIED by CVO~Z with K.2 attestation; plant caught or VOIDed-and-retained.</criterion>
  <criterion id="C6">Consumable derived from dry; K.1 packet (shared-tree scratchpad practice as in AD1); composition stated.</criterion>
  <criterion id="C7">METHOD READ — deltas only vs AD1's (what the second instrument run teaches that the first could not).</criterion>
  <criterion id="C8">Session log; proof-of-spec instance validator-clean BEFORE the flip.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TOOLCHECK.P4-AD2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package, full K-regime set</deliverable>
  <deliverable type="document">**The Monday-battery verdict** — the NEVER#1 mechanism confirmed-current or refuted-as-current, with fixtures</deliverable>
  <deliverable type="document">Proof-of-spec + session log + method-read delta</deliverable>
</deliverables>

<do_not>
  <rule>All of AD1's do_not rules verbatim. Plus: fixture artifacts land in scratchpad or your lane's test area, NEVER in served prefixes — a synthetic Friday artifact in a live bucket is a shadow-data act.</rule>
</do_not>
</task_order>
