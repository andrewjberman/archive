<task_order>
<id>MDPF_3FIRMS.GC-W1</id>
<title>W-1 — MEASURE the Global count composition. For each of the 40 null dates: which core model cell was missing and why. Decompose the 07-17 -> 07-22 +408 BY FIRM. Confirm OR REFUTE the Cottonwood attribution.</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — W-1 IS THE DENOMINATOR. Nothing else in the wave gets designed until this lands.</workstream>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T14:10Z</issued_at>
<status>staged</status>
<authorization>Andrew-direct ~1310Z at CTO's terminal ("have COO decompose those to the relevant agents, and call MSTR for spawn") -> CTO PRD @5d7522128 -> COO decomposition. SCOPE-BOUNDED to MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT W-1..W-7. The broader MDPF_3FIRMS_PRD decomposition REMAINS HELD on Andrew's word (LD-0333).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT.md — §3.1 Defect A (all-or-nothing), §3.2 Defect B (three bases), §3.3 Defect C (value and count count different firms), §6 W-1</ref>
  <ref type="source">dim_mdpf_aggregate_aua_timeseries.py:1720-1741 @275b51aee — CTO's source-confirmed mechanism cite</ref>
</references>

<scope>
**THIS IS A MEASUREMENT, NOT A FIX. YOU ARE THE DENOMINATOR FOR THE ENTIRE WAVE.** W-2 (the composition
law), W-3 (basis coherence) and W-6 (which served artifact is canonical) are all HELD until this lands,
because deciding a composition law before measuring the composition is the same error the chart is
already making.

You have a DEDICATED lane for exactly this reason. CTO's instruction is "W-1 first and alone," and I gave
it an un-contended lane rather than queueing it behind base DS's retry-net and clock items — "first and
alone" has to mean something operational. **Do not pick up other work.**

**THREE MEASUREMENTS. Output is a TABLE, not a narrative.**

**(1) THE 40 NULLS.** Served bytes carry `account_count_total` non-null on 407 of 447 dates. For EACH of
the 40 null dates: which core model cell(s) were missing, and why. CTO's §3.1 established the mechanism —
one missing core-model cell nulls the WHOLE Global day (all-or-nothing) — so the question is not "why is
Global null" but "which cell, and what made THAT cell absent."
**NEVER#1 APPLIES AND CTO ALREADY DID HALF OF IT:** 24 of the 40 are ORDINARY TRADING DAYS (he resolved
the calendar FIRST). Do not re-litigate the calendar; do confirm his 24/40 split as your own starting
measurement rather than inheriting it, and state which resolver you used.

**(2) THE +408, BY FIRM.** 07-17 (7,686) -> 07-22 (8,094) is +408. CTO's §3.2 establishes this is a BASIS
SEAM, not growth. Decompose the 408 by firm. This is the number that tells us what actually changed.

**(3) CONFIRM OR REFUTE THE COTTONWOOD ATTRIBUTION — AND REFUTE IS A REAL, VALUABLE OUTCOME.**

⚠⚠ **THE SINGLE MOST IMPORTANT CONSTRAINT IN THIS TO, IN CTO'S OWN WORDS:** he has **explicitly labelled
as INFERRED** the claim that the +408 is Cottonwood entering via the frontier stamp. *The basis-seam part
is CONFIRMED; the attribution is NOT.* His instruction, verbatim: **"W-1 must MEASURE it, not inherit it
from me. If a TO quotes my attribution as established, that is the defect propagating."**

So: **do not start from Cottonwood and look for confirmation.** Decompose the +408 by firm from the data
and see what it says. If it is Cottonwood, you will find Cottonwood. If it is not, that refutation is the
most valuable thing this TO can produce, and reporting it costs you nothing with me or with CTO.
An ungrounded causal claim is `INFERRED` and NON-ACTIONABLE (Rule 22); a measurement that inherits an
inference and re-reports it as established is worse than no measurement, because it launders it.
</scope>

<grounding_requirements>
- **Measure on the SERVED artifact bytes**, not on the producer's self-report and not on a re-run.
  **NEVER#4: no ad-hoc gold runs to validate this** — measure what is served.
- **Cite `file:line @ commit-ish`** for every mechanism claim. A line citation without a vintage is not
  a citation.
- **PRINT THE DENOMINATOR OF EVERY SCAN** you reason from (Rule 22). "40 nulls" is a numerator; say what
  it is 40 *of*, and how you enumerated.
- **Explicit-Z timestamps only.** The host is UTC-4: `aws s3 ls` renders LastModified in LOCAL time and
  `git log --since` PARSES local. Use `s3api` / explicit-`Z` forms. A load-bearing timestamp read the
  wrong way will silently shift a date boundary — and this TO is entirely about which DATES carry what.
- **Enumerate before you explain.** Establish what a number is *of* (which bucket, which axis, which firm
  set) before explaining why it differs — a rigorous instrument on the wrong axis survives review.
</grounding_requirements>

<explicitly_out_of_scope>
- **Any fix, any design, any code change.** This is measurement only. If you find the fix obvious, write
  it in the notes and do not implement it — W-2's product ruling may make the obvious fix wrong.
- **W-2's composition law.** "What SHOULD Global do when one firm is un-estimated?" is a product question
  at CTO's gate and likely Andrew's word. You supply input; you do not decide it.
- **W-7 axis hygiene** (weekend rows / the 427-vs-447 docstring drift) — that is base DS's, separately.
- Do NOT touch the FE. W-4/W-5 are live with 0.4.0_DE under MDPF_3FIRMS.GC-W45.
</explicitly_out_of_scope>

<cross_domain_coordination>
`dim_mdpf_aggregate_aua_timeseries.py` is the producer behind BOTH the count series you are measuring and
the value series W-3 will reconcile. **You are READ-ONLY on it in this TO**, so there is no write conflict —
but flag in your report any line you believe W-3 will need to change, so the eventual writer inherits your
reading rather than re-deriving it.
0.4.0_DE holds GC-W45 (W-4/W-5) on the FE side concurrently. No shared files. Your measurement will
inform their render but does not block it — do not wait on each other.
**Name collision, live today:** the PRD's **W-6 (count-reconcile)** is NOT the MDPF-wave **W-6 (bell
clobber)** that COO closed this morning. Different scope, different artifact. Label yours explicitly.
</cross_domain_coordination>

<compiler_tools_mandate>
  <before_write>`comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py` (column gaps + portal consumers
    — you need the consumer set to know what your measurement is *of*); `comp-which` for any search you
    are unsure how to route.</before_write>
  <before_commit>`comp-validate` is N/A for a read-only measurement — say so explicitly in the log rather
    than leaving it blank. `comp-surface-check` BY HAND if you touch anything under a SEV1 surface (it
    cannot block and its silence is not a pass).</before_commit>
  <after_commit>Session log with a populated `## Compiler Tools` section; append the
    `org/compiler-tools-log.md` line in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **A TABLE of all 40 null dates**, each with: the missing core model cell(s), the reason, and the
   provenance class. Denominator stated (40 of 447) and the enumeration method named.
2. **The 24-of-40-are-ordinary-trading-days split independently confirmed or corrected**, with the
   calendar resolver named.
3. **The +408 decomposed BY FIRM**, summing to 408, with the per-firm figures traceable to served bytes.
4. **An explicit CONFIRMED / REFUTED / UNDETERMINED verdict on the Cottonwood attribution**, with the
   evidence that discriminates it. `UNDETERMINED` is an acceptable answer if the data cannot separate the
   candidates — an honest UNDETERMINED beats a confident inheritance. What is NOT acceptable is restating
   CTO's inference as a finding.
5. Every mechanism claim carries `file:line @ commit-ish`.
6. Machine-checkable: another agent can re-run your enumeration from your stated method and get your
   numbers.
</acceptance_criteria>

<deliverables>
  - The measurement report (table-first) at `org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/`.
  - Report to CTO (he gates W-2/W-3/W-6 on this) and COO in the same window.
  - Session log with `## Compiler Tools` populated.
</deliverables>

<notes>
Register as `0.4.0_DS_ClientPlatform~A` — the FULL suffixed serial. Registering under the base serial
means your `~A` inbox is never watched and you will silently miss every message addressed to this lane.
</notes>
</task_order>
