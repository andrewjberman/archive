<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-007</id>
    <project>ADVI_INFLEC</project>
    <title>Per-advisor active_since + radial_12m empirical S3 re-read — lift 2 YELLOW cells to GREEN</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- COMPLETE 2026-05-05. DS~A Phase 1+2: radial_12m GRAY-by-design (0 active TSX consumers); active_since GRAY-by-design (sole consumer AdvisorPublicProfile disabled layout.ts:45 + all 4 advisors null post-S7SUMFIX). CTO committed matrix v8 db9b70ecf. YELLOW 10->8, GRAY 12->14. Session log ea68ba261. RAVC5 sent to COO 20260505T180605Z. -->
    <priority>medium</priority>
    <estimated_effort>~30 min — pure empirical S3 reads + matrix v8 patch routed to CTO</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v7 (commit 15322b926) — line 150 (radial_12m YELLOW), line 151 (active_since YELLOW), line 218 follow-on entry</ref>
    <ref type="origin_carry_forward">session 58 carry-forward "AUDIT-007 (Orange Q4-Q6)" — rescoped per matrix v7 + DS~A scan 20260505T165938Z (Q5+Q6 RESOLVED in v7; line 218 role_breakdown already GREEN; radial_12m not in line 218 but is DS~A scope per matrix line 150)</ref>
    <ref type="prior_work">S7SUMFIX dispatch (commit 4c6c823df) populated INF_D_04 summary.json publisher to emit active_since; pre-fix value was `active_since: None` per DE RAVC3; post-fix empirical re-read pending</ref>
    <ref type="prior_work">INFLFE.002 (commit 72a6c1f4) resolved AdvisorBookView.tsx:223 hooks violation, unblocking L2 advisor drill render path; data fields previously not isolatable from FE crash</ref>
    <ref type="cross_pod_scope">DS~B is on AUDIT-003 (silver assets rep_id=6); DS~D is on AUDIT-008 (AUA strip stale); DS~C is on ADVI_RPBKTPI Phase 0 — none touch active_since or radial_12m artifacts</ref>
  </references>

  <context>
    Matrix v7 has 2 YELLOW cells in DS~A scope that are both pure render-isolation gaps with confirmed data presence:

    1. **`platinum/advisors/{id}/summary.json#active_since`** — S7SUMFIX dispatched (4c6c823df) the INF_D_04 summary publisher to emit this field. Pre-fix value was `None`. Post-fix S3 empirical re-read NOT yet performed for any of the 4 Inflection advisors (inflection_wealth_management, peter_lee, patrick_scanlan, joe_brandenburg).

    2. **`platinum/firm/header_metrics.json#radial_12m`** — Data is populated (S3 jq confirmed keys [0,1,2] len=3 per DSB-IWM Gap 1 FIXED via 937b6bef7). Render not specifically isolated in INFLFE.004 sweep (covered indirectly by L2 book overview).

    Goal: confirm post-S7SUMFIX + post-INFLFE.002 hooks-fix world. If data is correct in S3 for all 4 advisors, lift both cells YELLOW → GREEN in matrix v8. If data is wrong (e.g., active_since still None), surface root cause for follow-up.

    No code changes expected. Pure empirical investigation + matrix update.
  </context>

  <phase id="1" when="empirical S3 reads — before any matrix edit">
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/header_metrics.json - | jq '.radial_12m | {len: length, keys: keys, sample_first: .[0]}'</run>
      <expect>len=3 (or whatever current period count); keys=[0,1,2] (or equivalent integer-index array); sample_first has non-null structure with cohort decomposition fields. Field is non-empty and structurally well-formed.</expect>
      <if_mismatch>If radial_12m absent or empty array: data layer regression — flag to me, do not flip cell to GREEN. Most-likely cause: header_metrics writer (INF_D_05 or equivalent) has not run post-AUDIT-002 canonical_prices fix today (parallel to AUDIT-008 scope). If so, route to DS~D for chain re-run inclusion.</if_mismatch>
    </step>
    <step>
      <run>for advisor in inflection_wealth_management peter_lee patrick_scanlan joe_brandenburg; do echo "=== $advisor ==="; aws s3 cp s3://opal-data-inf/platinum/advisors/$advisor/summary.json - 2>/dev/null | jq '{advisor_id, active_since, generated_at, data_as_of}'; done</run>
      <expect>All 4 advisors emit non-null active_since (ISO date or formatted string per S7SUMFIX publisher contract). generated_at &gt; 2026-05-04T12:00:00Z (post-S7SUMFIX dispatch). Empirical confirmation of populated field per advisor.</expect>
      <if_mismatch>If any advisor still shows `active_since: null` post-S7SUMFIX: dispatch incomplete or publisher logic missed an advisor key. Root cause investigation: re-read INF_D_04 (or equivalent summary publisher) to verify all 4 advisor_keys are in its iteration set. Surface to me with per-advisor table.</if_mismatch>
    </step>
    <step>
      <run>comp-platinum reverse "platinum/advisors/{id}/summary.json#active_since" — confirm FE consumers</run>
      <expect>FE rendering paths for active_since enumerated (likely AdvisorBookView "Orion Connected — {date}" header, possibly summary card subtitle). At least 1 consumer confirmed.</expect>
      <if_mismatch>If 0 consumers: field is unused at FE; YELLOW reclassification to GRAY-by-design appropriate. If >0 consumers but all use optional-chaining fallbacks: still YELLOW (graceful) — note in matrix update.</if_mismatch>
    </step>
    <step>
      <run>comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m" — confirm FE consumers + render path</run>
      <expect>FE component(s) consuming radial_12m enumerated (likely an AdvisorBookView radial cohort decomposition viz or similar). Consumer chain identifies whether render is currently isolated or coupled to L2 book overview.</expect>
      <if_mismatch>If 0 consumers: field is unused; reclassify GRAY. If consumed but not visually isolatable in INFLFE.004 sweep: matrix note that render confirmation requires future targeted Playwright capture (RD scope, not blocking AUDIT-007 close).</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="matrix v8 patch authored in working tree — routed to CTO for commit">
    <step>
      <run>Edit docs/architecture/ADVI_INFLEC_AUDIT.md: flip line 150 (radial_12m) and line 151 (active_since) per Phase 1 evidence. Update matrix-v summary block lines 188-198 to reflect new GREEN/YELLOW counts. Bump status header to v8 with one-line evidence summary.</run>
      <expect>5-10 line diff. v7 cell count GREEN 27 / YELLOW 10 → v8 GREEN 27+N / YELLOW 10-N where N is the lift count (0/1/2 depending on Phase 1 outcomes).</expect>
      <if_mismatch>If you find additional cells that need flipping based on Phase 1 evidence (e.g., a third cell whose state changes): include in same v8 patch and note in commit message. Stay in DS~A scope only.</if_mismatch>
    </step>
    <step>
      <run>MCP 1.0.0_SA_CTO with the v8 unified diff (`git diff docs/architecture/ADVI_INFLEC_AUDIT.md` output) — same path as AUDIT-006 AC4 routing today (lane enforcement on docs/architecture/** = ANY_CTO).</run>
      <expect>CTO RAVC2 with diff applied + commit hash returned. Matrix v8 lands on CLOUD via CTO commit.</expect>
      <if_mismatch>If CTO requests revisions: rework patch + re-route. Do not retry direct commit (lane enforcement will block).</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="post-CTO commit — RAVC4 to me">
    <step>
      <run>Send RAVC4 MCP to 2.0.0_SA_COO with: (a) per-advisor active_since values observed, (b) radial_12m structure observed, (c) FE consumer enumeration from comp-platinum reverse, (d) CTO matrix v8 commit hash, (e) verdict on each cell (GREEN/YELLOW unchanged/GRAY).</run>
      <expect>RAVC4 message delivered. AUDIT-007 ready for COO close.</expect>
      <if_mismatch>If RAVC4 has any cell still YELLOW with reason: that's a follow-on TO trigger — surface explicitly so I can author next.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>None.</coord>
    <coord>DS~B is on AUDIT-003 (silver assets rep_id=6) — different artifacts (silver/api_dims/assets/{rep_id}/, gold/INF_I_D02b output). Zero overlap with AUDIT-007 scope (platinum/firm/header_metrics.json + platinum/advisors/{id}/summary.json).</coord>
    <coord>DS~D is on AUDIT-008 (Inflection AUA strip stale, page-header AUA value) — distinct artifact from AUDIT-007's two cells. If Phase 1 Step 1 finds radial_12m absent due to a stale chain (parallel to AUDIT-008 root cause), DS~A coordinates with DS~D directly via MCP — do not edit AUDIT-008 scope.</coord>
    <coord>DS~C is on ADVI_RPBKTPI Phase 0 (callsite analysis of latest_accounts_v2_key) — pure investigation, no S3 writes, zero overlap.</coord>
    <coord>CTO 1.0.0_SA_CTO commits matrix v8 on DS~A behalf (Phase 2 Step 2) — same lane-routing path used for AUDIT-006 AC4 today.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing any matrix edit">
      <step>
        <run>comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m"</run>
        <expect>FE consumer enumeration; ≥1 consumer or explicit zero (which triggers GRAY reclassification path).</expect>
        <if_mismatch>If comp-platinum reverse fails (cache stale): run `comp-build` first, then retry. Log the cache-staleness in session log.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse "platinum/advisors/{id}/summary.json#active_since"</run>
        <expect>FE consumer enumeration covering at least AdvisorBookView header.</expect>
        <if_mismatch>Same as above — comp-build, retry.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before routing v8 diff to CTO">
      <step>
        <run>git diff docs/architecture/ADVI_INFLEC_AUDIT.md | head -80</run>
        <expect>Diff output shows only target lines + summary block + status header v7→v8 bump. No spurious whitespace/CRLF noise.</expect>
        <if_mismatch>Clean diff. Re-run after fixing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after CTO matrix v8 commit lands">
      <step>
        <run>git pull --rebase origin CLOUD &amp;&amp; git log -1 --pretty=format:"%h %s" docs/architecture/ADVI_INFLEC_AUDIT.md</run>
        <expect>Latest commit on the file is the CTO v8 commit; cell counts updated.</expect>
        <if_mismatch>If git pull conflicts: surface to CTO; do not force-resolve.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Phase 1 Step 1 (radial_12m S3 read) executed; output captured in session log with `<run>` + observed value + pass/fail vs `<expect>`.</criterion>
    <criterion id="AC2">Phase 1 Step 2 (active_since per-advisor S3 read) executed for ALL 4 advisors; per-advisor table in session log.</criterion>
    <criterion id="AC3">Phase 1 Steps 3+4 (comp-platinum reverse for both fields) executed; consumer enumeration captured.</criterion>
    <criterion id="AC4">Matrix v8 patch authored in working tree; routed to CTO via MCP with unified diff; CTO commit hash returned.</criterion>
    <criterion id="AC5">Session log includes Compiler Tools section per SESSION_LOG_STANDARD.md with all comp-* runs + outputs + verdicts.</criterion>
    <criterion id="AC6">RAVC4 to COO with full evidence package (per-advisor active_since values, radial_12m structure, FE consumer enumeration, CTO v8 commit hash, per-cell verdict).</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T17:00:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Matrix v7 ratified by CTO (15322b926). DS~A scope-narrowing scan accepted (radial_12m added; role_breakdown removed). Begin Phase 1 immediately. Standing by for RAVC3 (Phase 1 evidence + Phase 2 patch ready) before CTO routing.</message>
  </go_signal>
</task_order>
