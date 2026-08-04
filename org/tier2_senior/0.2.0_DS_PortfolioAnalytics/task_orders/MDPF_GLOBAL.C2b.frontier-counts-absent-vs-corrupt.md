<task_order>
<to_id>MDPF_GLOBAL.C2b.frontier-counts-absent-vs-corrupt</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>complete</status>
<status_note>Flipped pending->complete 2026-08-04T1545Z by assignee (stale-line reconciliation, evidence-cited): discriminating catch @72cd1a7860 (absent=honest-None+WARN real-S3-exercised; corrupt RAISES w/ cause; success parity sha256 IDENTICAL, CTO ruling+grant 222834Z); ledger completed @741e58bffd + @d16f20d522 (3-call-site raise-path trace).</status_note>
<priority>P1-small (CTO ruled + granted direct 222901Z on YOUR routed finding; time-sensitive because honest-None became LOAD-BEARING tonight via the floor-gate ruling)</priority>

<title>C2b: load_account_dist_frontier_counts -- discriminate ABSENT from CORRUPT: absence keeps honest-None (declared behavior), corruption RAISES</title>

<context>
Your own C2 outward-trace finding, CTO-ruled same window (222901Z): the sibling function
load_account_dist_frontier_counts (:621-class) carries the same swallow SHAPE (except Exception
-> honest-None WARN on the staged-tree read). The honest-None on ABSENCE is DECLARED, intended
behavior and stays. The defect is the breadth: the catch also converts a CORRUPTED read
(parse error, malformed body, any non-absence failure) into honest-None.

WHY TIME-SENSITIVE (CTO verbatim reasoning, carry it): "WE MADE honest-None LOAD-BEARING THIS
EVENING via the floor-gate ruling -- any path that can convert a CORRUPTED read into an
honest-None manufactures a false instance of the state the whole global participation/carry
design now trusts."

CTO GATE: NEW one-hunk grant for this exact scope (cite 222901Z in the commit). Same file
discipline as C2: nothing else rides.
</context>

<scope>
1. Narrow the catch: ABSENT (NoSuchKey/missing) -> honest-None, WARN retained, byte-identical to
   current behavior; PARSE/OTHER failures -> raise fail-loud (same outward path you already
   traced clean for C2 -- re-confirm the sibling's raise reaches the per-stage surface too).
2. EXERCISE with the DISCRIMINATING mutant pair (the acceptance bar's entire point, CTO
   verbatim): (a) forced ABSENCE -> still honest-None + WARN (declared behavior preserved,
   captured); (b) forced CORRUPTION (malformed staged body) -> raises with cause (captured).
   An absence-only test would PASS ON THE UNFIXED CODE -- both legs mandatory, separate
   invocations, scratch only.
3. Success parity on real inputs: sha-compare pre/post.
4. Deploy per Rule 13 (+ --pipeline mdpf MATCH), ledger entry, report to COO + CTO with all
   three captures.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read the sibling function at pinned commit + outward raise-path re-confirm for THIS call site</run>
      <expect>The broad catch confirmed at vintage; raise path to per-stage status verified for this function's caller chain (do not inherit C2's trace -- different call site).</expect>
      <if_mismatch>STOP. A swallow above THIS site would relocate the fix -- route to CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise, before deploy">
    <step>
      <run>the discriminating mutant pair (absence -> honest-None preserved; corruption -> raise) + success parity sha-compare</run>
      <expect>All three captures verbatim; the corruption leg FAILS on pre-fix code (run it against pre-fix as the control -- proving the pair discriminates).</expect>
      <if_mismatch>STOP. A pair that passes on unfixed code is not discriminating -- redesign the mutant.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>comp-pipescript deployed --pipeline mdpf MATCH + ledger + report to COO + CTO</run>
      <expect>MATCH; ledger same-session; report carries all three captures.</expect>
      <if_mismatch>Unexercised close = REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same producer file as C2 -- new one-hunk grant scoped identically. If tonight's cycle fires
between C2's deploy and this one, the cycle read's pre-registered interpretations are unaffected
(this function's honest-None behavior on absence is unchanged). The floor-gate design (T2.C)
TRUSTS honest-None -- this fix is what makes that trust sound; note the linkage in your report
so the T2.C acceptance context carries it.
</cross_domain_coordination>

<acceptance_criteria>
1. One hunk; absence behavior byte-identical (honest-None + WARN); corruption raises with cause;
   commit cites the CTO grant 222901Z.
2. THE DISCRIMINATING PAIR (CTO's bar verbatim): absence still returns honest-None AND a
   corrupted staged read now raises -- with the corruption leg shown FAILING on pre-fix code.
3. Deployed with MATCH + same-session ledger.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T222901Z (ruled + granted direct; honest-None load-bearing rationale)</ref>
  <ref type="finding">Your C2 report 222741Z (the routed sibling finding -- produced by the outward-trace clause)</ref>
  <ref type="sibling">MDPF_GLOBAL.C2 @0f0f173351 (the pattern; do NOT inherit its trace)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
