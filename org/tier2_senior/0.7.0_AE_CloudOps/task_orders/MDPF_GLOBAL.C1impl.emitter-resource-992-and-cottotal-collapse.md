<task_order>
<to_id>MDPF_GLOBAL.C1impl.emitter-resource-992-and-cottotal-collapse</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P1 (the C1 implementation leg promised at your 222054Z ACK -- DS's spec is COMPLETE @03ab006764 and their implementation report reached you 23:02:26Z. Sequencing with T2.C is yours per your no-interleaved-applies posture. >> ONE LEG IS SERVE-HELD FOR ANDREW -- see the split. <<)</priority>

<title>C1 implementation: re-source the emitter's legacy rows + :992 fail-loud + the cot_total fourth-site collapse -- one build, a SPLIT deploy discipline</title>

<context>
THE SPEC (DS @03ab006764, delivered to you directly; embed-by-reference at that pinned commit):
- RE-SOURCE: the legacy non-re-sourced set collapsed to ONE quantity -- etf_total_net_assets x4
  tickers feeding 3 row families; canonical source = opal-data-etfs/silver/netassets_daily.parquet
  (the runner was a pure two-hop pass-through); parity proven 12/12 exact on 3 sample dates keyed
  by stamped as-of. DELTA=0 BY CONSTRUCTION for these rows, evidenced.
- :992 RIDER (CTO-binding regardless of branch): _latest_key demoted to event-flagged walk-only;
  run_date event-derived; body=None becomes the DECLARED normal mode with an in-band degraded
  state; per-stage observable; NO alarms (moratorium).
- THE FOURTH SITE (DS 230639Z, measured to the cent): cot_total at channel_sources.py:446 reads
  columns=["Market Value"] ONLY -- identity columns never loaded, collapse impossible at that
  read; :452 whole-column sum. Fix per DS's spec rider: read
  ["Market Value","AccountID","AssetID"], drop_duplicates(subset=["AccountID","AssetID"]) BEFORE
  summing, WITH the dollar-equality assert across dual rows (different values for one
  (AccountID,AssetID) = a DATA question -> refuse loudly, never keep-first). Measured 07-31
  delta: -$205,070.77 exactly.

>> THE DEPLOY SPLIT (CTO serve-hold ruling 230622Z governs the collapse):
LEG A (re-source + :992): DELTA=0 evidenced -- deployable on its own evidence, no hold.
LEG B (cot_total collapse): DELTA != 0 on a SERVED client-facing value -- BUILT + EXERCISED +
COMMITTED but the corrected value must NOT reach the served surface until Andrew's disclosure
call (same hold as DS's DC1 sites). Mechanically: either two-stage deploys (A now, B on the
word) or one deploy held entirely for the word -- your call with CTO concurrence; state it in
the plan. The runner chain stays LIVE until T5.B regardless. <<
</context>

<scope>
1. Implement Leg A per the spec @03ab006764 (re-source + :992). Exercise: parity re-run on the
   3 spec dates + one fresh date; the :992 degraded mode forced in scratch (producer-absent
   simulation -> in-band degraded state surfaces per-stage, no silent aging).
2. Implement Leg B per the DS rider (collapse + equality assert at :446-:452). Exercise: the
   07-31 dual-day delta ties to -$205,070.77 EXACTLY; a clean-day control byte-identical; the
   equality-assert forced (synthetic unequal dual pair -> loud refusal).
3. Deploy discipline: full deploy law (TF-only where TF, commit-before-apply, safe-apply, 0-diff,
   tag, MSTR push, deploy-completion ledger, lambda-source-map). Leg A on its evidence; Leg B
   HELD-FOR-ANDREW; state your two-stage-vs-held-single plan to CTO+COO before the first apply.
4. Pre-register the post-deploy cycle interpretations: Leg A = ETF rows byte-identical (parity
   holds); Leg B (when cleared) = cottonwood channel row steps DOWN by the dual-day delta --
   expected, correct, not a regression.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read the spec @03ab006764 in full + the four cited mechanisms at pinned commits; comp-blast opal-assets-daily-emitter fns; comp-iam service on the Lambda (new read: opal-data-etfs silver -- Rule 22a: live simulate-principal-policy, ONE resource per call, positive control separate, if the role lacks the etfs read today)</run>
      <expect>Spec fully absorbed; IAM for the NEW bucket read verified on the live primitive, not comp-iam alone.</expect>
      <if_mismatch>STOP. A missing grant routes before any deploy; comp-iam GREEN alone is insufficient (fails green).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise, before deploy">
    <step>
      <run>Leg A parity re-run + :992 forced-degraded; Leg B delta-tie + clean-day control + forced unequal-pair refusal (all scratch, zero production writes)</run>
      <expect>All captures verbatim; Leg B delta EXACT to the cent; the assert refuses loudly on the synthetic pair.</expect>
      <if_mismatch>STOP. A delta that does not tie means a derivation disagreement -- route to CTO with both figures.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="deploy + after">
    <step>
      <run>the stated deploy plan (A-then-B-on-word, or held-single); MATCH/0-diff verifies; ledger opened+closed per leg; report to COO + CTO with all captures</run>
      <expect>Leg B never reaches serve before Andrew's word -- an acceptance item, not a courtesy; T5.A's C1 condition reads SATISFIED on Leg A + the ruling's terms.</expect>
      <if_mismatch>Serving Leg B early is a NEVER-rule violation; no override path.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
DS's DC1 (three slice/dim/pair sites) holds the SAME Andrew word -- coordinate so the serve-side
correction lands as ONE coherent event across both seats (one before/after story for Andrew, not
two partial steps; CTO orchestrates the word). T2.C sequencing yours (no interleaved applies on
one root). The runner chain stays live until T5.B -- Leg A removes the emitter's DEPENDENCE, it
does not kill the producer.
</cross_domain_coordination>

<acceptance_criteria>
1. Leg A: parity 12/12 + fresh-date re-run; :992 degraded mode exercised; deployed on evidence.
2. Leg B: delta ties EXACTLY; equality assert exercised both ways; HELD until Andrew's word,
   then deployed + cycle-step-down pre-registered.
3. IAM for the new etfs read verified on live primitives (one resource per call, separate
   positive control).
4. Deploy plan stated BEFORE first apply; ledgers per leg.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="spec">DS derivation + re-source spec @03ab006764 (embed-by-reference, pinned)</ref>
  <ref type="fourth-site">DS 230639Z (structural cite :446/:452 + measured delta + the collapse/assert rider)</ref>
  <ref type="rulings">CTO 221736Z item (a) (re-source default + :992 rider) + 230622Z (serve-hold, DELTA!=0)</ref>
  <ref type="verdict">~F T5.A @b877dbc0f5 (C1 = the last live runner-chain dependency)</ref>
</references>

<dependencies>
  <dependency agent="0.2.0_DS_PortfolioAnalytics" task="MDPF_GLOBAL.C1 derivation" status="complete (@03ab006764)"/>
</dependencies>
</task_order>
