<task_order>
  <metadata>
    <id>SSCN_DIVDEF.002</id>
    <slug>dt-production-data-refresh-2026-05-18</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct directive 2026-05-19; production data stale since 2026-03-06 (LastModified on latest/factor_metadata.json); fresh 2026-05-18 FactSet vintage available locally; gates TO-3 DS validation. ~30min DT wall per CTO estimate (one s3 cp + Lambda fire watch).</priority>
    <sla>~30min DT wall. Independent of TO-1 (FE change is vintage-agnostic). PARALLEL OK with TO-1. HARD-GATES TO-3.</sla>
    <deadline>None -- ship at DT 0.3.0 pace; Pod 3 ~0.5 effort-day if all 3 TOs run in parallel.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md (PRD v0.1, 1.0.0_SA_CTO~B, commit a5e1b7ef4 2026-05-19) -- section 3.3 has the exact upload key and Lambda flow; section 4.2 confirms no code/Terraform change.</prd>
    <source_file>C:\Users\AndrewBerman\Downloads\Screening_DIVZ_IDVZ_20260518.xlsx -- 3,017 rows x 331 cols, FactSet Universal Screening export dated 2026-05-18. Structural compat verified at PRD time (section 5 / section 2.3): header row 5 = "ticker" matches Lambda `pd.read_excel(buf, header=4)`; all 13 Andrew signals present; `wt_iwb` universe column present (Russell 1000).</source_file>
    <coo_section_7_rulings>Q3 (asOf format) -- accept CTO recommendation: use ISO `2026-05-18` (matches prior production key `2026-02-26/` convention). The file name `Screening_DIVZ_IDVZ_20260518.xlsx` is independent of the S3 key path segment. Q5 (upload mechanism) -- accept CTO recommendation: v0.1 ops `aws s3 cp` (this TO); defer portal DataRefresh tile to a separate project. Andrew may override either ruling by amending this TO before DT starts.</coo_section_7_rulings>
    <lambda_baseline>`opal-security-scanner-processor` (current tag `security-scanner-v1.0.2`) -- event-triggered via S3 ObjectCreated on `opal-data-portal-v2/security_scanner/uploads/{asOf}/`. No code/Terraform change in this TO. CTO PRD section 5 verified IAM via `comp-iam service opal-security-scanner-processor` -- role `sscn_processor` has `s3:PutObject` + `s3:GetObject` already granted.</lambda_baseline>
    <output_pattern>Lambda writes outputs to BOTH `json/security_scanner/{asOf}/...` AND `json/security_scanner/latest/...` (overwrites prior latest). Portal reads only `latest/` -- once the Lambda completes, the portal serves fresh data on next React Query staleTime expiry (5min per `SSCN_STALE_TIME`). The `latest/` overwrite is the critical signal that the Lambda has finished writing all six universes (sp500 / r1000 / r1000v / acwx / eafe / eafev).</output_pattern>
  </references>

  <context>
    Andrew has provided a fresh 2026-05-18 FactSet vintage XLSX that needs to land in production. The existing `opal-security-scanner-processor` Lambda is event-triggered on S3 ObjectCreated -- a single `aws s3 cp` to the canonical upload key fires the entire pipeline. No code change, no Terraform change, no new IAM scope (PRD section 4.2 + 5 explicit).

    The Lambda runs all six universes per upload (sp500 / r1000 / r1000v / acwx / eafe / eafev), writes 12 per-universe JSONs (6 universes x 2 files each: universe_data.json + scanner_data.json), 1 factor_metadata.json, and updates `json/latest/manifest.json:screening_excel`. All outputs land at both `json/security_scanner/2026-05-18/...` (dated) and `json/security_scanner/latest/...` (overwritten).

    This TO opens the `2026-05-18/` snapshot in S3 and gates TO-3 (DS validation pulls `latest/` post-upload). TO-1 (DE portal changes) is vintage-agnostic and can ship in parallel.
  </context>

  <scope>
    <step>Phase 1 (before upload) -- baseline compiler + S3 state probe:
      - `comp-iam service opal-security-scanner-processor` -- verify Lambda role still has `s3:PutObject` + `s3:GetObject` on `opal-data-portal-v2/security_scanner/*` and `opal-data-portal-v2/json/security_scanner/*`. (CTO PRD section 5 ran this 2026-05-19 ~11:13Z; re-run to detect cache drift.)
      - `aws s3 ls s3://opal-data-portal-v2/security_scanner/uploads/` -- snapshot state (expect only `2026-02-26/`).
      - `aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json` -- record current LastModified (expect 2026-03-06 12:20:30 UTC per PRD section 2.2 baseline) as the "before" anchor for AC4.
      - Verify ops user has `s3:PutObject` on `opal-data-portal-v2/security_scanner/uploads/*` (existing SSCN ops policy per PRD section 5). If gap, surface to AE 0.6/AE 0.7 for ops policy extension -- but expected to already be in place.
    </step>
    <step>Phase 2 (upload) -- record TO-start timestamp; `aws s3 cp` the file:
      ```
      TO_START_TS=$(date -u +%FT%TZ)
      aws s3 cp "C:\\Users\\AndrewBerman\\Downloads\\Screening_DIVZ_IDVZ_20260518.xlsx" \
        s3://opal-data-portal-v2/security_scanner/uploads/2026-05-18/Screening_DIVZ_IDVZ_20260518.xlsx
      ```
      Confirm exit 0 + non-zero size in S3 (AC1).
    </step>
    <step>Phase 3 (during) -- tail CloudWatch logs `/aws/lambda/opal-security-scanner-processor` for the new invocation (expect within ~5min of upload event). Capture the invocation log: `INFO: asOf=2026-05-18`, `INFO: Identified N scoring factor columns` with N >= 280, `INFO: Manifest updated` (final). Save log excerpt to session log.</step>
    <step>Phase 4 (after) -- verify outputs:
      - `aws s3 ls s3://opal-data-portal-v2/json/security_scanner/2026-05-18/` -- expect 13 files (factor_metadata.json + universes/{sp500,r1000,r1000v,acwx,eafe,eafev}/{universe_data,scanner_data}.json = 1 + 12).
      - `aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json` -- LastModified > TO_START_TS (AC4 -- the critical signal that Lambda finished).
      - `aws s3 cp s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json - | jq .asOf` -- expect `"2026-05-18"`.
      - `aws s3 cp s3://opal-data-portal-v2/json/security_scanner/latest/universes/r1000/scanner_data.json - | jq -r '.rows[0:3] | .[] | .ticker'` -- expect 3 non-empty ticker strings; for each ticker, `.pctls.dy_ntm` is a finite number in [0,100] (spot-check that all 13 Andrew signals percentile-resolve in R1000 outputs).
      - `aws s3 ls s3://opal-data-portal-v2/json/latest/manifest.json` -- LastModified > TO_START_TS (Lambda updates `manifest.json:screening_excel` per `lambda_function.py:388-396`).
    </step>
    <step>Phase 5 (RAVC2) -- RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B + DS 0.3.0 (TO-3 owner) with: TO_START_TS, upload S3 URL, Lambda invocation log excerpt (asOf=, N factors=, Manifest updated=), all 8 AC evidences, latest/ LastModified anchors (before vs after). DT-mode: TO status -> complete on receipt; DS 0.3.0 receives the GO for TO-3 simultaneously (gated on this RAVC2).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">`aws s3 ls s3://opal-data-portal-v2/security_scanner/uploads/2026-05-18/` returns `Screening_DIVZ_IDVZ_20260518.xlsx` with non-zero size (expect ~ several MB, FactSet XLSX vintage typical).</ac>
    <ac id="AC2">CloudWatch logs for `opal-security-scanner-processor` show a successful invocation referencing the new key within 5min of upload; log line `INFO: asOf=2026-05-18`; log line `INFO: Identified N scoring factor columns` with N >= 280 (the registry has 284 factors); final log line `INFO: Manifest updated` (or equivalent terminal-success marker). Log excerpt captured in session log.</ac>
    <ac id="AC3">`aws s3 ls s3://opal-data-portal-v2/json/security_scanner/2026-05-18/` shows the expected output set: `factor_metadata.json` + `universes/{sp500,r1000,r1000v,acwx,eafe,eafev}/{universe_data.json,scanner_data.json}` = 13 files total.</ac>
    <ac id="AC4">`aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json` LastModified > TO_START_TS (the critical signal that the Lambda overwrote `latest/`; this is the gate that unblocks TO-3 and FE staleTime expiry).</ac>
    <ac id="AC5">`aws s3 cp s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json - | jq .asOf` returns `"2026-05-18"` (CTO Q3 ruling enforced -- ISO format).</ac>
    <ac id="AC6">`aws s3 cp s3://opal-data-portal-v2/json/security_scanner/latest/universes/r1000/scanner_data.json - | jq -r '.rows[0:3] | .[] | .ticker'` returns 3 non-empty ticker strings; for each of the 3 sampled tickers, `.pctls.dy_ntm` is a finite number in [0,100] AND `.pctls.ret_mom_252d` is a finite number in [0,100] (the two-signal spot-check confirms the percentile compute ran across the new vintage for the 13 preset signals; full distribution validation is TO-3).</ac>
    <ac id="AC7">`aws s3 ls s3://opal-data-portal-v2/json/latest/manifest.json` LastModified > TO_START_TS (the Lambda updates `screening_excel` key per `lambda_function.py:388-396`).</ac>
    <ac id="AC8">No Lambda errors in the new invocation's CloudWatch log -- no `ERROR:` lines, no Python traceback. If Lambda errors out, FAIL-LOUD via RAVC2 BLOCKED to 2.0.0_SA_COO~B + 1.0.0_SA_CTO~B with full error log; do not retry-loop without escalation.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-iam service opal-security-scanner-processor` -- expect role `sscn_processor` with `s3:PutObject` + `s3:GetObject` on the SSCN keys; no Lambda IAM change in this TO (PRD section 5 baseline).
      `aws s3 ls s3://opal-data-portal-v2/security_scanner/uploads/` (state snapshot before upload).
      `aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json` (record before-LastModified for AC4 anchor).
    </before_write>
    <before_commit>
      N/A -- this TO is an S3 ops operation, not a code commit. The Lambda code is unchanged; no Terraform change; nothing to commit beyond the session log.
    </before_commit>
    <after_commit>
      The AC1-AC8 checks ARE the post-deploy verification. No graph-tool rerun needed (the `opal-security-scanner-processor` Lambda surface is uninstrumented in `comp-blast` per PRD section 6 / trade-pipeline-island pattern -- direct empirical substitutes ARE the canonical evidence). Session log captures the full Lambda invocation transcript.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None for the upload itself. TO-3 (DS DIVZ preset validation) HARD-GATES on this TO's close -- the RAVC2 message from DT 0.3.0 IS the GO signal for DS 0.3.0 to start TO-3 (it CCs DS 0.3.0 per Phase 5). DS 0.3.0 pulls `latest/` only after this RAVC2 lands. TO-1 (DE) is vintage-agnostic and runs independently.
  </cross_domain_coordination>

  <deliverables>
    - S3 object: `s3://opal-data-portal-v2/security_scanner/uploads/2026-05-18/Screening_DIVZ_IDVZ_20260518.xlsx`.
    - Session log under `org/tier2_senior/0.3.0_DT_TradingOperations/logs/YYYY-MM-DD/` with: TO_START_TS, S3 ls transcripts (before / 2026-05-18/ / latest/), CloudWatch log excerpt (asOf= + N factors= + Manifest updated=), AC1-AC8 evidence including jq output for asOf + dy_ntm + ret_mom_252d spot-check, Compiler Tools section (comp-iam result + S3 ls snapshots).
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B + CC 0.3.0_DS_TradingOperations on close (the CC to DS IS the GO for TO-3).
  </deliverables>

  <do_not>
    <rule>Do NOT modify the Lambda Python code (`infra/aws/lambda/opal_security_scanner_processor/`) -- this TO is a data ops + verification operation only.</rule>
    <rule>Do NOT modify Terraform (`infra/aws/terraform/security-scanner-pipeline/`) -- already shipped `security-scanner-v1.0.2`; no change needed.</rule>
    <rule>Do NOT delete or overwrite the `2026-02-26/` historical upload -- it stays untouched as historical record.</rule>
    <rule>Do NOT rename the S3 key segment to `20260518` (file-name format). CTO Q3 ruling: use ISO `2026-05-18` to match prior production convention.</rule>
    <rule>Do NOT retry-loop on Lambda failure -- FAIL-LOUD via RAVC2 BLOCKED with the full CloudWatch error log; surface to COO~B + CTO~B for adjudication. Likely root cause if a failure occurs: file format drift or header structure change; the empirical probe at PRD time confirmed header=4 + 13 signals present, but FactSet could have a regression.</rule>
    <rule>No emojis in session log or CLI transcripts (CLAUDE.md ASCII-only rule).</rule>
    <rule>Do NOT trigger the Lambda manually via `aws lambda invoke` -- the S3 ObjectCreated event is the canonical trigger. Manual invoke bypasses the event-source mapping and produces different log entries.</rule>
  </do_not>
</task_order>
