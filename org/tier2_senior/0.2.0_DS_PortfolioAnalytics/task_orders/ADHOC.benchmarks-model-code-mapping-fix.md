<task_order>
<to_id>ADHOC.benchmarks-model-code-mapping-fix</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-04</date>
<status>complete</status>
<status_note>Complete 2026-08-04T2003Z, all four acceptance criteria evidenced: (1) drop mechanism file:line + live-run WARNs (RequestId dc51d3bc) + post-fix regen 5/5 (content capture in window logs); (2) re-keyed all three artifacts zero old-code residue (legacy incl., zero live FE call sites per DE census); (3) FE-first wall evidenced (portal v2.1.157 PROD w/ 70c884ae in ancestry, COO-verified 193242Z; commit shipped after); (4) DE Phase-3 render verify ON RECORD 200116Z (scatter + heatmap all 5 incl. LT/ULT on the REAL 19:51Z artifact through PROD code; screenshot portal/.frontend-dev/screenshots/benchmark-tab-live-artifact.png). Chain: commit @0ce5aa5ada -> DT apply (tag yang-pipeline-v1.5.2, live CodeSha256 verify) -> regen 19:51:04Z -> content-verify -> render verify.</status_note>
<priority>P1 (Andrew-active thread: his FE-first Teams ruling to Yang this morning + the DE sweep executing at his direction; CTO routing 155310Z)</priority>

<title>Benchmarks producer: carry Yang's renamed model codes (LTA->ULT, LTC->LT) -- the regen currently DROPS the renamed portfolios at the data layer</title>

<context>
DE's grounded finding (154958Z, en route to Andrew's FE mapping sweep):
json/benchmarks/model_portfolio_timeseries.json regenerated 12:36:59Z TODAY carries ONLY
[INT, ST, UST] -- the renamed portfolios are ABSENT AT THE DATA LAYER (the producer's tag
mapping dropped the renamed tags rather than passing them; Yang's exact symptom). And
model_portfolio_benchmarks.json still keys the OLD codes [LTA, LTC]. So the Benchmark-tab
charts are missing two portfolios today regardless of any FE work.

ONE THREAD (CTO 155310Z): this TO is the producer half; DE's FE sweep (new codes internally +
display, old-code aliases normalized at artifact-read seams) is the consumer half, executing
now at Andrew's direction, DT deploys it after. MSTR's morning ST-manifest-regression relay is
the same defect family -- fold its content from MSTR's record into your Phase-1 context
(CTO notes the relay never reached his inbox; a resend ask is with MSTR separately).

SEQUENCING WALL (Andrew's own Teams ruling to Yang this morning, verbatim per CTO: "we needed
to change that portal side prior to any change in upload"): the FE sweep + DT deploy land
FIRST. Your fix lands AFTER that deploy -- OR ships transition-compatible (carries BOTH code
sets) if the deploy order inverts. The TO's Phase-2 gate enforces this: confirm the FE deploy
state before your artifact-changing commit, or demonstrate transition-compatibility.
</context>

<scope>
1. Producer tag mapping: the regen carries LT + ULT (the renamed codes) alongside INT/ST/UST --
   five codes total. Ground the drop mechanism first (file:line where the old tags stopped
   matching after Yang's rename).
2. model_portfolio_benchmarks.json re-keys LTA->ULT, LTC->LT.
3. Fold MSTR's ST-manifest-regression relay content (from MSTR's record) -- if it names
   additional artifacts in this family, enumerate them; widen ONLY with CTO's word.
4. Transition compatibility decision stated explicitly: land-after-FE-deploy (confirm the
   deploy), or both-code-sets (show the artifact carries both and consumers tolerate it).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast model_portfolio_timeseries + comp-blast model_portfolio_benchmarks (artifact consumers)</run>
      <expect>Consumer set enumerated -- expect the Benchmark-tab components (heatmap, return-vol scatter) at minimum; any consumer NOT in DE's FE census gets named to DE before you re-key.</expect>
      <if_mismatch>STOP. An unenumerated consumer keying old codes breaks silently on re-key -- surface to DE + CTO first.</if_mismatch>
    </step>
    <step>
      <run>ground the drop: the producer's tag mapping at source, file:line @ commit, showing why renamed tags vanish</run>
      <expect>Mechanism cited, not inferred -- "the mapping dropped them" becomes a specific line.</expect>
      <if_mismatch>STOP. A fix without the drop mechanism named risks patching the symptom.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>sequencing gate: confirm DE's FE sweep is DEPLOYED (DT deploy state), OR demonstrate the both-code-sets artifact renders on the CURRENT deployed FE</run>
      <expect>One of the two, evidenced -- Andrew's FE-first ruling is the wall.</expect>
      <if_mismatch>STOP. Do not land a producer change that strands the deployed FE on missing codes.</if_mismatch>
    </step>
    <step>
      <run>regen against the fixed mapping, content-read the output</run>
      <expect>All FIVE codes present with plausible series; old-code keys absent (or both-sets per the transition choice, stated).</expect>
      <if_mismatch>STOP. Fix until the regen carries the roster.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit + regen">
    <step>
      <run>notify DE for the render verify (heatmap + return-vol scatter show LT/ULT) + report to me + CTO with pre/post artifact captures</run>
      <expect>DE confirms render; report cites the drop mechanism, the fix commit, both artifact states.</expect>
      <if_mismatch>REWORK -- a producer fix without its consumer render verify is half a close.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
ONE THREAD, three seats: DE owns the FE sweep (executing, Andrew-direct) and the Phase-3 render
verify; DT owns the FE deploy; you own the producer. The sequencing wall (FE first) is
Andrew's own ruling -- any pressure to invert routes through CTO, never absorbed silently.
Your own EMIT-1/aum-metrics lane is untouched by this TO.
</cross_domain_coordination>

<acceptance_criteria>
1. Drop mechanism cited file:line @ commit; post-fix regen carries all five codes (content
   capture in the log).
2. Re-keyed benchmarks artifact; no consumer keys the old codes anywhere DE's FE census found
   (or both-sets transition explicitly demonstrated).
3. Sequencing wall evidenced (FE deploy confirmed, or transition-compat shown).
4. DE render verify on record.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="routing">CTO 155310Z (producer-side routing + scope + sequencing); DE 154958Z (the grounded gap)</ref>
  <ref type="authority">Andrew Teams ruling to Yang (FE-first, this morning, verbatim in CTO's routing); Andrew-direct FE sweep order at DE's session</ref>
  <ref type="family">MSTR morning ST-manifest-regression relay (fold from MSTR's record; resend ask at MSTR)</ref>
</references>

<dependencies>
  <dependency agent="0.4.0_DE_ClientPlatform" task="FE mapping sweep (Andrew-direct)" status="in-flight -- Phase-2 gate enforces the sequencing, not a hard file dependency"/>
</dependencies>
</task_order>
