# TO OPAL_ADVIPOINTERS.T3-VENDORCLOCK — the vendor-clock anchor audit, one pass (TIGHTENING T3; Andrew-ratified)

<task_order id="OPAL_ADVIPOINTERS.T3-VENDORCLOCK" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T14:50Z</issued>
<dated>starts NOW (live + idle per CTO); one pass, complete when every vendor pull carries its recorded anchor — target 08-20 EOD</dated>
<status>staged -- GO paired this window</status>
<priority>P2 — front-runs the pre-publish-fire class instead of detecting it (today's bd49f retime, generalized ONCE)</priority>
<authority>Andrew-direct at the CTO terminal (verbatim in TIGHTENING_INCORPORATION_BRIEF_20260819.md @094df1d132: "I like all your recommendations ... hand it off to COO; they should go get it done") -> brief T3. The bd49f trio retime @807c3c9190/@ee18a14e09 + ledger 20260819T1430Z is the EXEMPLAR — same method per mismatch. CTO gates each apply as usual.</authority>
</task_order>

## Objective
Enumerate EVERY vendor pull schedule (~6 per the brief: schwab SDD x2 masters · the bd49f trio
[DONE 08-19, the exemplar] · orion · eclipse · the cot rebalancer bronze placeholder [06:00Z,
its own comment marks it unconfirmed] · smartx if any live pull remains — enumeration is yours,
materialised both namespaces, never page-1) and compare each cron against the vendor's
known/observed PUBLISH time (BD ~01:02 ET ruled; 0824 SDD observed ~08:37Z; others = read the
landing history — the observed LastModified series IS the publish record). Retime each mismatch
exactly as today's exemplar: targeted plan, ledger opened-before-apply, applied-plane verify.
Record every anchor + its AUTHORITY (ruled / observed-with-window / unconfirmed) in the P2 timing
map so no future schedule is minted clockless.

## Acceptance criteria
- T3-1 ENUMERATION: the vendor-pull census with denominator (both EventBridge namespaces
  materialised; each pull row = cron + vendor + the anchor evidence class).
- T3-2 ANCHORS: every pull carries a recorded vendor-publish anchor with its authority; an
  unconfirmable anchor is recorded UNCONFIRMED with what was read — never guessed.
- T3-3 RETIMES: each mismatch retimed per the exemplar (targeted plan / ledger / applied-plane
  cron read), CTO-gated per apply; zero pulls left firing before their vendor's publish window,
  or the exception recorded with its reason.
- T3-4 TIMING-MAP RECORD: the P2 timing map carries every anchor row (the CRO spec family home);
  one line per pull, authority cited.
- T3-5 proof instance VALID rc=0 positional: ids T3-1,T3-2,T3-3,T3-4,T3-5.

<proof_of_spec>
  <expected_criteria>T3-1,T3-2,T3-3,T3-4,T3-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.T3-VENDORCLOCK_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not (the brief's anti-scope IS the ratified scope)
- No freshness checkers, no monitors — the frontier READER roster is the standing eye and stays
  reader-only. Exceeding an anti-scope line needs a fresh Andrew word, not an interpretation.
- No vendor API calls beyond the standing authorized pulls (egress law unchanged).

## Reporting
COO (cc CTO per apply) at census-complete and at pass-complete. Surprise channel: one banked line
to COO. Session log with Compiler Tools section = deliverable.
