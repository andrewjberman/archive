<task_order>
<to_id>MDPF_GLOBAL.T4A.exemplar-table-verdicts</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>pending -- ISSUER RECORD 2026-08-30 04:1xZ (2.0.0_SA_COO): addressed to the BASE serial, which has carried no session since the 08-28 drawdown; LIVE but UNSEATED -- artifact census by 0.4.0_DS_ClientPlatform~R (85373, corpus all, 136,670 files): ONE family-verdict artifact exists (MDPF_T4A/T4A_orion_eclipse_family_verdicts.md, 2026-08-03, the first tranche); SmartX / BD-cot / Schwab-0824 have NO verdict artifact -> 1 of 4 families delivered on the ARTIFACT instrument (03ff36daee's '4 T4.A tranches' is tranches, not families -- ambiguity stated, not smoothed). MDPF_GLOBAL is outside the live paired scope (D2 & D3); the remaining three families seat on a DS lane when the estate scope is re-armed or on Andrew's word; NOT a Rule-27 collision at ~R (the broker's pending list is folder-keyed, server.py:809-812). || PRIOR: pending</status>
<!-- self-activated 2026-08-03 ~2200Z on WS-1 completion (registry 39 rows @01ab614102, TO complete);
     first family per tranche order: Orion/Eclipse -->

<priority>P1 (spine: unblocked by your OVP WS-1 tranches 1-2 @f129fc1c80/@438a3c69b3 -- the Andrew-explicit prerequisite rows exist. SELF-ACTIVATING: begin when your WS-1 census completes (T3/T4 tranches done or explicitly parked with CTO word); this message-in-TO is the GO, no re-send needed. RESEARCH may overlap your remaining tranches at your discretion; CERTIFICATION waits for the as-of rows per Andrew.)</priority>

<title>T4.A: Exemplar table verdicts -- per MDPF-feeding silver family: stable key DECLARED + EXERCISED, measured duplicate rate, completeness verdict over the serve window</title>

<context>
MDPF_GLOBAL PRD Addendum C s.C.4 T4.A row: the MDPF-feeding silver families (SmartX, Black
Diamond/cot, Orion/Eclipse, Schwab-0824) get their stable keys + dedup verification +
completeness verdicts FIRST, as the priority exemplars of OPAL_VENDORPROVENANCE WS-4/WS-5 --
MDPF end-to-end acceptance consumes these verdicts. You authored the as-of rows these verdicts
key off; the dedup_stable_key TODO column in YOUR registry is exactly what this TO fills for the
exemplar tables.

YOUR OWN WS-1 FINDINGS ARE THE HAZARD MAP (each one binds a key or completeness choice):
- transactions.csv mutates into prior date keys next-day (EditedDate mutation) -- the key choice
  must handle it (tranche-1 finding, explicitly a WS-4 constraint).
- Weekend-labeled carry partitions (Sat/Sun bronze = Friday settled) -- completeness counts
  TRADING days, never calendar days (NEVER#1 mechanized).
- SmartX + Eclipse are the zero-date-param class (run-date labels; gaps permanently
  unfillable; false-vintage hazard) -- completeness_rule semantics differ structurally from BD's
  date-addressed backfillable class; the verdict must say WHICH class each table is.
- BD 0-row-shell mechanism (snapshot as-of not yet completed in ET returns a 4.6KB shell; 49f
  LAG=1 configured around it, cot snapshot LAG=0 exposure LIVE) -- a 0-row partition is not
  evidence of an empty day; dedup/completeness reads must not count shells as data.
- cot period-table filenames LEAD content by one ET day -- key/date resolution uses the
  registry's label_offset rule, never the filename.
- Dual-producer overlap (6 dim feeds, per-dim crons + EC2 orchestrator) -- duplicate-rate
  measurement must attribute BY PRODUCER where the overlap lives.

STANDING LAWS: Rule 17 binds hard -- this TO DECLARES and VERIFIES; it does not slim, fillna, or
filter. Serve-window scoping: completeness evaluated over 2024-11+ (standing law). UNKNOWN stays
legal and loud where a key cannot be established.
</context>

<scope>
1. Per exemplar table (the MDPF-feeding families across opal-data-assets + the firm buckets your
   registry rows cover): DECLARE the stable dedup key, with the reasoning row-cited to your own
   registry + source (file:line @ commit).
2. EXERCISE every declared key against a REAL duplicate -- not asserted: find (or construct in
   scratch from real rows) an actual duplicate pair and show the key collapses it and does NOT
   collapse a true-distinct pair (positive + negative control, separate invocations).
3. MEASURE the duplicate rate per table on live partitions; record it. Where the dual-producer
   overlap lives, attribute the rate by producer.
4. COMPLETENESS verdict per table: frontier arithmetic (expected_trading_days(window) minus
   present(resolved_trading_date)) vs the table's completeness_rule, over 2024-11+. A table with
   gaps is a FINDING with an owner, never a fix-in-place (OVP WS-5 law). Shells (0-row) do not
   count as present data.
5. LAND the verdicts as registry rows: fill the dedup_stable_key column + a completeness verdict
   annotation per exemplar row in data/_contracts/vendor_asof_registry.yaml (you are the single
   writer). Tranche-report to COO + CTO as families complete (Orion/Eclipse -> SmartX -> BD ->
   Schwab-0824 as its WS-1 rows land).
6. OUT OF SCOPE: any silver script edit, any dedup ENFORCEMENT change, any backfill -- verdicts
   only. Migration/enforcement lands under the OVP WS-3+ rollout with CTO gating.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before research per family">
    <step>
      <run>comp-pipescript io &lt;converter&gt; per touched family (KNOWN GAP: the assets tree is invisible until the 0.8.0~B coverage build lands -- hand-derive there and say so, citing the staged build TO)</run>
      <expect>READS/WRITES per converter; where the tool is blind, the hand-derivation is labeled as such.</expect>
      <if_mismatch>Tool-gap notes accumulate to the coverage build; never silently trust a blind tool's silence.</if_mismatch>
    </step>
    <step>
      <run>comp-estate &lt;vertical&gt; per family for chain context</run>
      <expect>Producers/consumers per table seeded; census-vintage drift noted where live contradicts.</expect>
      <if_mismatch>Ground live; note the drift.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="key exercise, before landing verdicts">
    <step>
      <run>per key: the real-duplicate collapse exercise + the true-distinct negative control (separate invocations, scratch only)</run>
      <expect>Key collapses the duplicate pair AND preserves the distinct pair; both captured verbatim.</expect>
      <if_mismatch>An unexercised key is a HYPOTHESIS -- record UNKNOWN-loud or keep researching; never land an asserted key.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after each tranche commit">
    <step>
      <run>tranche report to COO + CTO: registry commit + families closed + per-table {key, duplicate rate, completeness verdict} + UNKNOWN count</run>
      <expect>CTO validates against s.C.4 acceptance per family; MDPF end-to-end acceptance consumes the verdicts.</expect>
      <if_mismatch>A tranche report without measured rates + exercised-key evidence is REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Registry single-writer stays you -- no contention. T1.C (0.2.0_DS) restructures the cot MDPF leg
concurrently: your cot-table verdicts are INPUTS to their parity work, not blocked by it;
tranche-report promptly. The 0.8.0~B coverage build (staged) will make the assets tree visible
mid-TO -- adopt it when it lands, do not wait. The Schwab-0824 family is AE-ingested
(49-schwab-conv, SSE deny on DS) -- verdicts from code/records + silver reads only, no ingest
runs. Rule 17 collision guard: if a verdict reveals a legacy violator (slimming/fillna in a
silver converter), it is a FINDING routed to CTO -- migration is next-touch law, not this TO.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Per table: key EXERCISED against a real duplicate (not asserted); measured duplicate rate
   recorded; completeness = frontier arithmetic vs the table's completeness_rule.
2. Verdicts land as registry rows in the vendor as-of contract registry.
Plus standing norms: serve-window 2024-11+ scoping; trading-day arithmetic (never calendar);
every causal claim cites file:line @ commit or is labeled INFERRED; no new alarms/monitors;
Rule 17 untouched.
Plus the CTO item-3 elevation (225311Z, folded 2257Z): the BD RELATIONSHIP-GRAIN double-count
hazard closes by CONSUMER ENUMERATION, not annotation -- enumerate every consumer of BD
relationship-grain data and verify each collapses to (AccountID, AssetID) before aggregating.
Zero naive summers -> closes WITH EVIDENCE; any naive summer -> a real finding with a
served-number impact question (MP surfaces are must-always-be-right; the silent-summation shape
is undetectable by inspection).
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (s.C.2 T4 + s.C.4 T4.A row); docs/architecture/OPAL_VENDORPROVENANCE_PRD.md (s.3.3 + WS-4/WS-5)</ref>
  <ref type="registry">data/_contracts/vendor_asof_registry.yaml @f129fc1c80 + @438a3c69b3 (your rows ARE the substrate)</ref>
  <ref type="hazards">Your WS-1 findings (tranche 1 s.4 + tranche 2 as-of headlines) -- the hazard map above</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3 (T4 rides OVP per his explicit prerequisite ruling)</ref>
</references>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="OPAL_VENDORPROVENANCE.WS1.asof-endpoint-census" status="pending (self-sequenced: T4.A activates on WS-1 completion; research may overlap at your discretion)"/>
</dependencies>
</task_order>
