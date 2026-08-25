<task_order>
<id>MDPF_3FIRMS.3F-B4</id>
<title>INF/Eclipse bronze leg — name the puller mechanism + CONCLUDE recoverability of 07-01/13/14/15 on vendor-side evidence</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:19Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_3FIRMS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<authorization>LD-0333 amendment 1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition. Andrew confirmed direct 20:16Z (@f526334e0).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md</ref>
  <ref type="prd_section">§2.2 six-leg table (INF-model row); §4 WS-B row 3F-B4; §8.2 (the --date ban); §6 D-3</ref>
  <ref type="andrew_direct">org/tier1_exec/2.0.0_SA_COO/andrew_direct_20260722T2016Z_backfill_hold_is_cottonwood_only_inflection_july_in_scope.md @f526334e0</ref>
  <ref type="prior_work">your eclipse census: 848/848 portfolios swept, zero failures; changed-portfolio counts 07-01=2, 07-13=14, 07-14=1, 07-15=7, 06-01=0</ref>
</references>

<scope>
Two deliverables, both currently UNKNOWN and both requiring vendor-side evidence:

**(a) NAME THE MECHANISM.** No `eclipse`-named EventBridge rule is visible. Something fires this
puller. Name it with an ARN/rule/cron or identify definitively that it is fired another way (EC2 cron,
SSM, manual). A leg whose ingest mechanism is unnamed has no freshness contract.

**(b) CONCLUDE RECOVERABILITY** of the mid-series gaps 07-01 / 07-13 / 07-14 / 07-15. The census is
already in hand (yours: 848/848, changed counts 2/14/1/7). What does NOT exist is a VERDICT. Produce
one, either way, on vendor-side evidence.

~~Also: determine vendor depth PRIOR to 2026-05-15 (silver currently starts there).~~
**(c) DELETED — ANSWERED BY ANDREW-DIRECT ~20:41Z (@0b06b5a14), VERBATIM:** *"Inflection only started
migrating models on May 15 2026, and anything before is inherently non-model; the interest in their
validation is a function of checking those July dates."*
⛔ **THERE IS NO PRE-05-15 MODEL HISTORY TO FIND. The 2026-05-15 silver floor is CORRECT, NOT A GAP.**
Do not spend vendor probes establishing depth below it. **What survives in this TO is the
07-01/13/14/15 recoverability verdict** — inside the July window Andrew actually cares about.
⚠ A design question arising from "inherently non-model" (whether pre-05-15 `model_aum` is KNOWN ZERO,
making `non_model` computable back to Orion's 2020-04-28 floor, vs merely ABSENT per PRD §1.1) is
**routed to CTO and NOT yours to act on either way.**

⛔⛔ **THE HARD PROHIBITION — THIS IS THE WHOLE TRAP OF THIS LEG:**
**The eclipse puller's `--date` is a FILENAME, NOT A QUERY.** It fetches CURRENT state and files it
under whatever date you pass. **It is BANNED as a backfill instrument, permanently and without
exception.** Using it to "fill" 07-01/13/14/15 would write today's state under July's dates — a
fabrication with a plausible filename, undetectable downstream. **Andrew's "potentially repulling July
for Inflection" does NOT license it** (that instruction is about Inflection broadly; Orion and Eclipse
are different legs with different recoverability, and this ban is standing law, PRD §8.2).

**A "NOT RECOVERABLE" VERDICT IS A COMPLETE AND ACCEPTABLE OUTCOME.** It is not a failure of this TO.
Per PRD §6 D-3 the permanently-absent list goes to Andrew, and the recommendation is honest gaps + a
methodology note — never interpolation. **What is NOT acceptable is leaving the verdict open a second
time, or concluding "unrecoverable" from the SHAPE of the puller rather than from vendor evidence.**
</scope>

<binding_principle>
**PRD §4 WS-B preamble, Andrew §0, and it is aimed squarely at this TO:** *never conclude "data doesn't
exist" from the shape of a pull script or an endpoint.* Named prior instances of exactly this error:
the eclipse `--date` defect itself; the BD portfolio-level vs ACCOUNT-level template selection (four
months of an empty column that looked like a vendor gap but was OUR selection); the orion repair
needing per-date as-of rosters (current roster = right prices, wrong book).

**So: "the puller can't do it" is NOT evidence the VENDOR can't. Ask what Eclipse holds, not what our
script fetches.**
</binding_principle>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "what fires the eclipse inflection puller"</run>
      <expect>A routed comp tool or an on-rails comp-grep/comp-glob run. Record what it returned even if NO CURATED RULE MATCHED.</expect>
      <if_mismatch>If nothing routes, that is itself the finding (an unnamed mechanism). Proceed to the rail-checked primitive below and record the coverage gap.</if_mismatch>
    </step>
    <step>
      <run>⛔ RE-DERIVE THE CENSUS YOURSELF — DO NOT INHERIT PRD §9's ABSENCE CLAIM (CTO ruling 204330Z, PRD v1.7).
# rail-checked: EventBridge applied-truth is not modeled by a comp tool
# (a) PAGINATED rules census -- print the TOTAL denominator, not just the matches
aws events list-rules   (paginate fully; report "N matched of M total rules")
# (b) SCHEDULER namespace -- a DIFFERENT API that list-rules STRUCTURALLY CANNOT SEE
aws scheduler list-schedules   (paginate; print denominator)
# (c) LAMBDA DESTINATIONS -- not a rule of any kind, invisible to every rules census
aws lambda get-function-event-invoke-config  on the candidate functions</run>
      <expect>A census across ALL THREE surfaces with the DENOMINATOR PRINTED for each. Either a named mechanism, or a measured absence that states what was searched and how many objects were examined.</expect>
      <if_mismatch>⛔ **PRD §9's "no eclipse-named puller rule" is RULED UNVERIFIED and you must NOT rely on it.** Its sibling claim in the same census sentence ("no smartx-named rule") DID NOT REPRODUCE -- 0.5.0 ran the identical query and got 3 of 141. **An under-enumerating census reports ABSENCE, and absence is the one result nobody re-verifies.** Two of the three smartx mechanism pieces (EventBridge Scheduler, Lambda OnSuccess destination) are STRUCTURALLY INVISIBLE to list-rules, so a rules-only search cannot conclude "not fired". Print your denominators; an empty result without one is not a finding.</if_mismatch>
    </step>
    <step>
      <run>⚠ INSTRUMENT WARNING, EXERCISED THIS SESSION by 0.5.0 -- do not lose a census to it:
`aws s3api list-objects-v2 --delimiter /` through Git Bash / the .tools/aws shim SILENTLY returns CommonPrefixes=EMPTY with rc=0.</run>
      <expect>You avoid it: derive partition censuses from FULL KEY LISTINGS, not from --delimiter grouping.</expect>
      <if_mismatch>Mechanism (instrument-grounded, AWS_SHIM_DEBUG=1): MSYS converts the bare `/` to `C:\Program Files\Git\` because it IS a real local path, so the CLI groups on a delimiter that never matches. **Clean exit, empty result, zero error** -- the same silent-absence class as the census above. It cost 0.5.0 three calls before a positive control caught it.</if_mismatch>
    </step>
    <step>
      <run>comp-freshness</run>
      <expect>eclipse/inflection entry resolves on the trading-day frontier.</expect>
      <if_mismatch>Missing freshness_basis: trading-day-frontier = flat-hours fallback = guaranteed Monday false alarm. Record; do not raise a staleness finding off it (NEVER#1).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Vendor-side temporal probe — establish whether Eclipse exposes AS-OF/historical retrieval at all, WITH A POSITIVE CONTROL</run>
      <expect>A definite answer plus a control that could have failed: a date you KNOW differs from current state must come back DIFFERENT. If every probe returns today's state, the control proves the surface is current-only.</expect>
      <if_mismatch>Without a positive control an "identical" result is uninterpretable — it cannot distinguish a frozen feed from a stable roster. NO VERDICT may be recorded without the control.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 --bucket opal-data-assets --prefix eclipse/inflection/silver/fact_portfolios_full/ --query 'Contents[].Key'</run>
      <expect>Partition floor confirmed at date=2026-05-15; the 07-01/13/14/15 absences re-confirmed at current HEAD state (denominator printed).</expect>
      <if_mismatch>If a gap has silently filled, STOP and determine WHO wrote it before doing anything else — an unexplained fill is more serious than a gap.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the gap census with denominators printed</run>
      <expect>Unchanged; verdict document matches measured state.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>No script is patched by this TO. It is mechanism-naming + a recoverability
  determination. **If the verdict is RECOVERABLE, the fill itself is NOT executed inside this TO** — it
  requires a sanctioned path, a reprocess scope, and CTO gating as a follow-on. Producing the verdict
  is the deliverable.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="eclipse/inflection/silver/fact_portfolios_full/" shared_with="0.4.0_DS_ClientPlatform (3F-S2)">
    Shared census surface — reconcile denominators with DS before publishing.
  </resource>
  <resource path="PRD §6 D-3 (permanently-absent dates)" shared_with="Andrew via COO">
    An UNRECOVERABLE verdict feeds an open Andrew decision. Route through COO; do not approach Andrew directly.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency type="none">Independent of 3F-B3. May run in parallel.</dependency>
</dependencies>

<acceptance_criteria>
1. The ingest mechanism is NAMED with applied-truth evidence (rule ARN + state + cron, or a
   definitively identified non-EventBridge mechanism). "Not found" is not a mechanism.
1a. **The mechanism census is RE-DERIVED BY YOU across all three surfaces (paginated `events list-rules`
   + `scheduler list-schedules` + Lambda event-invoke-configs) with the DENOMINATOR PRINTED for each.**
   PRD §9's absence claim is RULED UNVERIFIED (CTO 204330Z) and inheriting it does not satisfy this.
2. A RECOVERABILITY VERDICT for 07-01/13/14/15 exists, stated either way, resting on VENDOR-SIDE
   evidence — never on the shape of our puller.
3. The verdict cites a POSITIVE CONTROL that could have failed. A verdict without one is not accepted.
4. ~~Vendor depth prior to 2026-05-15 is stated with evidence.~~ **STRUCK — answered by Andrew-direct
   @0b06b5a14: models began 2026-05-15, anything prior is inherently non-model, so the floor is CORRECT
   and there is nothing to find below it. Do not spend probes here.**
5. ⛔ Zero use of the eclipse puller `--date` for any backfill purpose. Any such use voids the TO and is
   an incident.
6. If UNRECOVERABLE: the permanently-absent date list is handed to COO for Andrew's D-3 decision, with
   the recommendation of honest gaps + a methodology note (never interpolation).
7. **Session log includes a Compiler Tools section reproducing EVERY `<run>` with observed output and
   explicit pass/fail vs `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO. Escalate immediately if: a gap has silently filled; the probe suggests the
vendor DOES hold temporal data (that changes the whole leg); or anything touches Andrew's
07-06/07-07/07-10 window (carrier pending CTO ruling — surface, do not self-assign).
</escalation>
</task_order>
