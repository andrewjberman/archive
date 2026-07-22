<task_order>
<id>MDPF_3FIRMS.3F-B7</id>
<title>INF July anomaly validation + scoped backfill decision — establish the MECHANISM behind the 07-06 jump / 07-07 drop / 07-10 re-jump</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:23Z</issued_at>
<status>complete</status>
<!-- CLOSED 2026-07-22 ~21:20Z: verdict @dfa42659f, COO accepted 204814Z, CTO NO-GO ratified 204936Z (residual DEFER-TO-FLIP), CVO spot-verify PASS 211918Z @6bb15dbcb (dollar-exact independent confirmation, no rework) -->
<priority>ANDREW-PRIORITY — his own words: "some numbers are very contentious there ... that is something I want addressed and validated"</priority>
<authorization>Andrew-direct ~20:16Z @f526334e0 -> CTO ruling 202054Z (new TO, NOT a rider on B3/B4/G7) -> PRD v1.4 @36be68476.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md v1.4 @36be68476, §4 WS-B row 3F-B7; §5 ruling 10 (narrowed)</ref>
  <ref type="andrew_direct">org/tier1_exec/2.0.0_SA_COO/andrew_direct_20260722T2016Z_backfill_hold_is_cottonwood_only_inflection_july_in_scope.md @f526334e0</ref>
  <ref type="prior_work">@b47d2ff10 — orion repull 07-11..07-15, root cause "raw producer died after 07-10"</ref>
  <ref type="banked_partial">PRD RF-11 / LD-0330 item 1 — legacy served date axis carries market-closed days and omits real trading days; 07-06 corrected to 122,866,034/474</ref>
</references>

<andrew_verbatim>
> "there is some backfill and verification that needs to be done for Inflection with 0.6.2 because some
> numbers are very contentious there. Like I saw a jump on july 6 that dropped july 7 then came back on
> july 10 or a little later jumped back up again; that is just questionable and to me smells like
> changing methodology, so that is something I want addressed and validated, potentially repulling July
> for Inflection."
</andrew_verbatim>

<scope>
Establish, with SOURCE-GROUNDED evidence, the mechanism behind the Inflection July movement Andrew
observed. Three parts:

**(a) TEST THE TWO CANDIDATE MECHANISMS INDEPENDENTLY.**
  - **Candidate 1 — the banked RF-11 DATE-AXIS ARTIFACT:** the legacy served axis carries market-closed
    days and omits real trading days (07-06 corrected to 122,866,034 / 474 accounts).
  - **Candidate 2 — Andrew's METHODOLOGY-CHANGE hypothesis.**
  ⚠⚠ **THESE ARE DIFFERENT MECHANISMS AND MUST BE TESTED SEPARATELY. THE AXIS ARTIFACT MUST NOT BE USED
  TO WAVE OFF THE METHODOLOGY QUESTION.** The PRD says it in its own words: *"residual spikes need a
  census, not assumed covered."* A found class root cause is the most seductive way to close a
  still-open case — and this one is already banked, which makes it maximally tempting.
  ⚠ Andrew's hypothesis is a HYPOTHESIS (Rule 22). It cannot authorize a fix until source-confirmed.
  Confirming it and refuting it are equally acceptable outcomes; asserting it without source is not.

**(b) PER-DATE TRACE 07-01..07-15** across the full chain: raw Orion vendor values -> bronze -> silver
-> gold -> served. Every layer, every date, denominators printed.

**(c) RELATE IT TO @b47d2ff10.** Your own root cause was "raw producer died after 07-10." Andrew's
window (07-06 / 07-07 / 07-10-or-later) is ADJACENT TO AND PARTLY EARLIER THAN the 07-11..07-15 range
you repaired. Three live possibilities, currently UNDETERMINED — determine which:
  (i) the same defect reaching further back than diagnosed;
  (ii) a separate, distinct defect;
  (iii) real market movement that is not a defect at all.
**(iii) IS A FULLY ACCEPTABLE FINDING.** Do not manufacture a defect to explain a real move; equally,
do not dismiss a real defect as market movement without evidence. Both require the same grounding.

**REPULL IS CONTEMPLATED, NOT ORDERED.** Andrew said "potentially." A repull executes ONLY on a
validation verdict that names exactly what it would fix, and only on CTO's word. Sanctioned paths only:
Orion per the 07-11..07-15 repair pattern (per-date AS-OF rosters — the current roster yields correct
prices on the WRONG BOOK). ⛔ The eclipse `--date`-is-a-filename ban is UNDISTURBED and this TO does not
touch it.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-freshness</run>
      <expect>Inflection leg entries resolve on freshness_basis: trading-day-frontier.</expect>
      <if_mismatch>Flat-hours fallback = guaranteed false alarm. Record the gap; never raise staleness off it (NEVER#1).</if_mismatch>
    </step>
    <step>
      <run>Resolve the TRADING CALENDAR for 2026-07-01..07-15 via lib/trading_calendar.py BEFORE interpreting any movement</run>
      <expect>An explicit expected-trading-day set. 07-04 (Independence Day observed) and weekends resolved FIRST.</expect>
      <if_mismatch>STOP. NEVER#1: a movement across a market-closed day is not a data defect, and this is precisely the RF-11 artifact's mechanism. Any anomaly claim made before the calendar is resolved is void.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io on the Inflection gold producer(s) feeding the served series</run>
      <expect>READS/WRITES enumerated; COLUMN GAPS empty.</expect>
      <if_mismatch>⚠ KNOWN INSTRUMENT GAP (COO filed to CTO 07-22): comp-pipescript io does NOT surface cross-bucket served imports inside helper functions — it reported 1 read / no writes on dim_mdpf_aggregate_aua_timeseries.py while missing the opal-data-portal-v2 import at :476-500. Do NOT treat a clean io manifest as proof of no coupling; read the source.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Per-date value trace 07-01..07-15: raw vendor -> bronze -> silver -> gold -> served, with a POSITIVE CONTROL (a date you know is clean must read clean)</run>
      <expect>A complete table; every cell either a value or an explicit ABSENT with its denominator. The control date reads clean.</expect>
      <if_mismatch>A retrieval that returns empty is NOT a value of zero. Print the denominator of every scan ("N of M dates retrieved"). Never `2>/dev/null` a git show or an s3api call — a broken retrieval returns clean-empty and reads as absence.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 (explicit-Z timestamps) across the Inflection chain for the window</run>
      <expect>Object-level vintages for each layer/date.</expect>
      <if_mismatch>⛔ NEVER bare `aws s3 ls` for a load-bearing time — it prints LOCAL time with no TZ marker, silently 4h off UTC here (5 hits / 4 agents; the 5th falsified a TRUE claim).</if_mismatch>
    </step>
    <step>
      <run>Mechanism verdict per anomaly date, each with a file:line @ commit-ish citation or tool output</run>
      <expect>Every anomaly date carries ONE of: axis artifact / data defect / methodology change / real movement — source-confirmed.</expect>
      <if_mismatch>An unsupported causal claim is INFERRED and NON-ACTIONABLE (Rule 22). "proof / root cause / definitively / source-confirmed" are RESERVED WORDS, legal only on a source-confirmed claim. A LINE CITATION WITHOUT A VINTAGE IS NOT A CITATION.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the per-date table with denominators printed</run>
      <expect>Stable; no drift during the write window.</expect>
      <if_mismatch>Surface to COO — another producer likely wrote mid-flight.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>This TO is VALIDATION ONLY and patches no script. **No repull, no backfill, no
  re-ingestion executes inside it.** If the verdict recommends a repull, that is a follow-on TO with its
  own reprocess scope, its own sanctioned-path statement, and CTO's explicit word. Producing the
  verdict + a GO/NO-GO recommendation IS the deliverable.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="Inflection served/staged trend artifacts" shared_with="0.4.0_DS_ClientPlatform (3F-G7 spike census)">
    3F-G7 is WS-G-GATED and will not run for some time; this TO is deliberately ahead of it because
    Andrew wants it now. Your per-date table is the INPUT G7 will consume — do not duplicate G7's
    >=5%-move enumeration across all firms; stay on Inflection July.
  </resource>
  <resource path="orion/inflection bronze+silver" shared_with="3F-B3 (same lane, you)">
    B3 verifies 07-11..07-15 propagation. Sequence B3's census FIRST where practical — its output is
    direct evidence for part (c) here.
  </resource>
  <resource path="verification" shared_with="3.0.0_SA_CVO">
    CVO spot-verify is named in the lane. Route the verdict for independent read before closing.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.6.2_AE_PartnerETL~A" task="MDPF_3FIRMS.3F-B3" status="staged" blocking="false">
    Not hard-blocking, but B3's census materially informs part (c).
  </dependency>
</dependencies>

<acceptance_criteria>
1. Per-date table 07-01..07-15 across raw-vendor / bronze / silver / gold / served, **with denominators
   printed** and a positive control that could have failed.
2. **Each anomaly date carries a source-confirmed MECHANISM VERDICT** — axis artifact, data defect,
   methodology change, or real movement — with citations at vintage (`file:line @ commit-ish`, or tool
   output). An uncited causal claim is INFERRED and does not satisfy this.
3. **The two candidate mechanisms are tested INDEPENDENTLY**, with the RF-11 axis artifact explicitly
   NOT used to dismiss the methodology hypothesis. State both results even where they agree.
4. The @b47d2ff10 adjacency question is RESOLVED to one of (i)/(ii)/(iii) with evidence. "Real market
   movement" is an acceptable verdict.
5. A **repull GO/NO-GO recommendation to CTO**, naming exactly what a repull would fix. **NO repull is
   executed inside this TO** absent CTO's word.
6. The trading calendar is resolved BEFORE any anomaly interpretation (NEVER#1).
7. **Session log includes a Compiler Tools section reproducing EVERY `<run>` with observed output and
   explicit pass/fail vs `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; CTO holds the repull gate. Escalate immediately if the evidence indicates a
methodology change actually occurred — that has blast radius beyond this window and beyond Inflection.
</escalation>
</task_order>
