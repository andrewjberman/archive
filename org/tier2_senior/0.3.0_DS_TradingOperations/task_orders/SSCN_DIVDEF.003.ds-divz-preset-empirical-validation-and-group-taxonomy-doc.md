<task_order>
  <metadata>
    <id>SSCN_DIVDEF.003</id>
    <slug>ds-divz-preset-empirical-validation-and-group-taxonomy-doc</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DS_TradingOperations</issued_to>
    <date>2026-05-19</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>SSCN_DIVDEF.002 (DT data refresh upload) RAVC2 close. DT 0.3.0 CC's DS 0.3.0 on the RAVC2 -- that message IS the GO. Do NOT start before that CC lands. Pulling `latest/` before the Lambda has overwritten it (AC4 anchor on TO-2) would validate against stale 2026-03-06 vintage and produce false-negative findings.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct directive 2026-05-19; HARD-GATES on TO-2 close. ~1.5h DS wall per CTO estimate.</priority>
    <sla>~1.5h DS wall. PARALLEL OK with TO-1 (FE) once TO-2 closes.</sla>
    <deadline>None -- ship at DS 0.3.0 pace once GO lands.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md (PRD v0.1, 1.0.0_SA_CTO~B, commit a5e1b7ef4 2026-05-19) -- section 6 TO-3 has the validation criteria; section 3.1 has the 13-factor preset; section 8 risks #1-#3 are the empirical risks this TO closes.</prd>
    <coo_section_7_rulings>None of the §7 rulings materially constrain DS work -- they shape FE (TO-1) and ops (TO-2). DS validation is empirically grounded against the actual `latest/` JSON output regardless of the §7 outcomes. The only relevant ruling: Q3 asOf = `2026-05-18` (DS verifies via `jq .asOf` on `latest/factor_metadata.json` as a sanity check).</coo_section_7_rulings>
    <upstream_dependency>SSCN_DIVDEF.002 (DT data refresh upload) MUST close before this TO begins. DT 0.3.0's RAVC2 CC IS the GO signal. Critical: pulling `latest/` before the Lambda has overwritten it would validate against stale 2026-03-06 vintage -- false-negative.</upstream_dependency>
    <registry_baseline>`infra/aws/lambda/opal_security_scanner_processor/factor_metadata_registry.json` (284 factors) -- bundled with the Lambda zip. CTO PRD section 5 verified all 13 Andrew signals present at PRD time. DS uses the registry as the authoritative source for `relationship` field (positive vs inverse) when verifying AC5.</registry_baseline>
    <factset_semantics_anchor>PRD section 6 TO-3 AC5 lists the expected relationship by factor:
      Positive (higher raw = higher score): dy_ntm, dps_gr_1yr, shldr_yield, ey_ntm, fcfy, ret_mom_252d, velocity_63d, pcta52wl, eps_est_rev_45d.
      Inverse (higher raw = LOWER score): accruals_bs, leverage, short_pct_chg_12m, days_to_cover.
      DS independently verifies these against FactSet documentation + the bundled registry's `relationship` field. A sign-flipped percentile would pollute the composite score; AC5 closes that risk.</factset_semantics_anchor>
  </references>

  <context>
    Empirical validation that the DIVZ preset, applied against the freshly-uploaded 2026-05-18 R1000 vintage, produces sane composite rankings + sane per-factor percentile distributions. Three distinct empirical risks (PRD section 8 #1, #2, #3) plus a taxonomy documentation gap that needs to persist beyond this TO so future preset authors don't re-derive Andrew's 4-group → registry-category mapping.

    This is empirical: pull `latest/universes/r1000/scanner_data.json` post-TO-2-close, run sanity probes in Python (numpy + pandas; not Lambda), produce a CSV artifact + group-taxonomy markdown sibling doc. The Lambda is correct or it isn't -- if any of the four risks materialize, FAIL-LOUD via RAVC2 BLOCKED to COO + CTO (do NOT silent-emit "validation passed" against degenerate data).
  </context>

  <scope>
    <step>Phase 1 (before validate) -- direct registry read + relationship sanity:
      - Read `factor_metadata_registry.json` for the 13 preset codes.
      - For each code, record: `category`, `relationship`, `factset_name` (or equivalent canonical field).
      - Compare relationship against PRD section 6 AC5 / references factset_semantics_anchor: any mismatch is a Phase 1 RAVC2 BLOCKED (the registry would be authoritative for the Lambda's percentile sign, so a wrong relationship in the registry pollutes the composite).
      - Input to AC4 group taxonomy doc (Andrew's 4 groups Dividend/Momentum/Value/Quality vs registry's `yield/growth/quality/sentiment/systematic` -- explicit mapping derived from PRD section 3.1).
    </step>
    <step>Phase 2 (validate) -- empirical pull + analysis:
      - Pull `latest/universes/r1000/scanner_data.json` to local: `aws s3 cp s3://opal-data-portal-v2/json/security_scanner/latest/universes/r1000/scanner_data.json /tmp/sscn_divdef_r1000_scanner.json`.
      - Pull `latest/factor_metadata.json`: confirm `.asOf == "2026-05-18"` (Q3 sanity).
      - For each of the 13 preset codes:
        AC1: pct non-null = (rows where `pctls[code]` is a finite number in [0,100]) / total_rows; expect >= 90% across Russell 1000 (~3,000 effective members modulo wt_iwb > 0 filter).
        AC2: KS test vs Uniform[0,100] -- D < 0.10 (or 10-bucket equal-count check: 10 buckets at expected ~300 members each within +/- 50% tolerance). Empirical sanity that the Lambda's `rank(pct=True, method='average')` produced a real ranking, not constant/degenerate output.
      - AC3: composite score for top-100 R1000 by `wt_iwb`:
        `composite[i] = sum_over_13codes(weight[code] * pctls[code])` (weighted-sum of percentiles).
        Output a CSV `/tmp/sscn_divdef_top100_composite.csv` with columns `ticker, composite_score, rank`.
        Sanity bounds: top-ranked composite >= 70.0 (the DIVZ tilt should pull dividend-yield-heavy names high); bottom-ranked composite <= 40.0 (low-dividend low-quality names should rank low). If bounds violated, escalate -- the preset may be misweighted OR the percentile compute is degenerate.
      - AC5: verify each of the 13 codes' `relationship` against FactSet semantics (positive vs inverse per anchor) AND against the Lambda's percentile sign (a top-ranked dy_ntm row should have HIGH `pctls.dy_ntm`; a top-ranked accruals_bs row should have LOW `pctls.accruals_bs` if relationship=inverse). Sample 3 tickers per inverse code as cross-check.
    </step>
    <step>Phase 3 (document) -- author the group-taxonomy doc:
      - Path: `docs/architecture/security-scanner-source/SSCN_GROUP_TAXONOMY.md` (or sibling doc under `docs/architecture/security-scanner-source/`).
      - Content: 4-group → registry-category mapping table (Andrew's UX taxonomy on one axis; registry `category` on the other); rationale for the divergence (the 4 user-facing groups are scoring-thesis groupings, the registry categories are FactSet/dataset categorizations); per-code mapping row for the 13 DIVZ codes; pointer to future preset authors to declare an explicit `group` field on preset entries rather than relying on registry `category` (per PRD section 3.1 critical note). 
      - This doc is the persistent artifact -- if SSCN_DIVDEF.001 (DE) ships and then the project closes, this doc is what makes the divergence understandable to a future preset author.
    </step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B with: AC1-AC5 evidence (per-code pct non-null + KS D-stat or bucket counts + top-10/bottom-10 composite tickers + 3-ticker inverse cross-check transcripts); attached CSV; new group-taxonomy doc commit SHA; the Phase 1 relationship-cross-check transcript. DS-mode: TO status -> complete on receipt.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">For each of the 13 preset factor codes, >= 90% of rows in `latest/universes/r1000/scanner_data.json` have a non-null `pctls[code]` value that is a finite number in [0,100]. Per-code transcript captured (13 lines).</ac>
    <ac id="AC2">For each of the 13 codes, the `pctls[code]` distribution across all rows is approximately uniform on [0,100]: either (a) Kolmogorov-Smirnov D < 0.10 vs Uniform[0,100], OR (b) 10-bucket equal-count check: 10 buckets at [0,10), [10,20), ... [90,100] each have row counts within +/- 50% of expected (total_rows / 10). Per-code transcript captured.</ac>
    <ac id="AC3">Composite score for the top-100 R1000 members by `wt_iwb`: composite = sum_over_13codes(weight[code] * pctls[code]) where weights are per PRD section 3.1. CSV at `/tmp/sscn_divdef_top100_composite.csv` (or session-log-relative path) with columns `ticker, composite_score, rank`. Top-ranked composite >= 70.0; bottom-ranked composite <= 40.0. If bounds violated, RAVC2 BLOCKED with the offending tickers + per-code pctls breakdown.</ac>
    <ac id="AC4">Group-taxonomy doc shipped at `docs/architecture/security-scanner-source/SSCN_GROUP_TAXONOMY.md` (or sibling) with: 4-group → registry-category mapping table, rationale for the divergence, per-code mapping for the 13 DIVZ codes, guidance for future preset authors (explicit `group` field on preset entries). Committed via `.tools/safe-commit.sh --author "0.3.0_DS_TradingOperations <0.3.0_DS_TradingOperations@opal.agent>"`. Commit SHA in RAVC2.</ac>
    <ac id="AC5">Empirical confirmation: for each of the 13 codes, the registry's `relationship` field matches FactSet semantics (positive: dy_ntm, dps_gr_1yr, shldr_yield, ey_ntm, fcfy, ret_mom_252d, velocity_63d, pcta52wl, eps_est_rev_45d; inverse: accruals_bs, leverage, short_pct_chg_12m, days_to_cover). Cross-check: sample 3 tickers per inverse code; confirm a HIGH-rank (low composite) member has HIGH raw values + LOW pctls on the inverse code, AND vice versa. Per-code transcript captured (13 + inverse-cross-check = 13 + 4 inverse codes * 3 tickers = 25 transcript rows).</ac>
    <ac id="AC6">`latest/factor_metadata.json :: .asOf == "2026-05-18"` (Q3 sanity).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      Direct registry read of `factor_metadata_registry.json` for the 13 preset codes (input to AC4 + AC5).
      `aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/universes/r1000/scanner_data.json` -- confirm LastModified > TO-2 RAVC2 timestamp (sanity that we are reading the fresh vintage, not stale).
    </before_write>
    <before_commit>
      N/A for SSCN_DIVDEF.003 -- this TO commits only the new taxonomy doc (no script touched). Run `python -m py_compile` on the analysis script if you keep one in the repo (data/sscn/probes/ or equivalent; AE-judgment whether to retain the script as a probe for future preset validation).
    </before_commit>
    <after_commit>
      The AC1-AC6 transcripts ARE the post-validate evidence. No graph-tool rerun needed (the validation runs against S3 outputs, not against a comp-graph node).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD-GATES on TO-2 close. DT 0.3.0's RAVC2 CC IS the GO signal (the RAVC2 lands in DS 0.3.0's inbox simultaneous with COO~B + CTO~B). Until that GO lands, DS 0.3.0 stays staged. No other cross-domain coordination -- the DS analysis touches only S3-read paths + a new doc file under `docs/architecture/security-scanner-source/` (no conflicting writers).
  </cross_domain_coordination>

  <deliverables>
    - CSV: `/tmp/sscn_divdef_top100_composite.csv` (or session-log-relative path) with the AC3 top-100 composite ranking.
    - New doc: `docs/architecture/security-scanner-source/SSCN_GROUP_TAXONOMY.md` with the 4-group → registry-category mapping + rationale + per-code mapping for the 13 DIVZ codes + future-preset-author guidance.
    - Session log under `org/tier2_senior/0.3.0_DS_TradingOperations/logs/YYYY-MM-DD/` with: AC1 13-line pct non-null transcript; AC2 13-line KS D-stat OR bucket-count transcript; AC3 top-10 + bottom-10 composite tickers + bounds-check; AC4 commit SHA for the new doc; AC5 25-line relationship + inverse cross-check transcript; AC6 .asOf jq output; Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B on close; SSCN_DIVDEF.json status -> ws=DS complete on receipt (COO~B updates JSON; DS just MCPs).
  </deliverables>

  <do_not>
    <rule>Do NOT pull `latest/` before the TO-2 RAVC2 CC lands. Pulling stale 2026-03-06 vintage produces false-negative findings (low pct non-null due to upstream registry drift in the 10-week gap).</rule>
    <rule>Do NOT modify the bundled `factor_metadata_registry.json` -- it is authoritative for the Lambda's percentile compute; modifying it in DS-lane bypasses the Lambda rebuild/redeploy cycle. If a relationship field is WRONG, RAVC2 BLOCKED with the offending code + the proposed correction + FactSet evidence; CTO + AE 0.6/0.7 will then author a separate TO to fix the registry + rebuild the Lambda layer.</rule>
    <rule>Do NOT compute composite scores in the Lambda or push the composite back to S3. v0.1 ships composite as a FE-side compute (the existing useScannerState hook does the weighted sum); this TO's CSV is a local one-off sanity artifact, NOT a new production output.</rule>
    <rule>Do NOT replace the registry `category` field assumptions used by the Factor Bank tab. The 4-group taxonomy is a DIVZ-preset-specific concern (per PRD section 3.1 critical note); the Factor Bank tab continues to use registry `category` for ordering/coloring -- the new doc clarifies the divergence but does NOT bridge it.</rule>
    <rule>Do NOT silent-pass AC3 if bounds are violated. The DIVZ-tilt is strong (40% Dividend, 30% Momentum); a top-ranked composite below 70 OR a bottom-ranked composite above 40 indicates either (a) preset is misweighted vs Andrew's intent, OR (b) percentile compute is degenerate. Either is BLOCKED-class -- escalate via RAVC2 BLOCKED with offending tickers + per-code pctls breakdown.</rule>
    <rule>No emojis in CSV header, doc, or session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
