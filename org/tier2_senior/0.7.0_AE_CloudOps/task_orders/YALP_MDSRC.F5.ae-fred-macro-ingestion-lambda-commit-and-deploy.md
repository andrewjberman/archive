<task_order>
  <metadata>
    <id>YALP_MDSRC.F5</id>
    <slug>ae-fred-macro-ingestion-lambda-commit-and-deploy</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — COO-issued, the AE deploy half of YALP_MDSRC.F4 (the FRED-ingestion implementation; F4 authoring is RAVC-complete). 0.7.0_AE_CloudOps owns the FRED Lambda work (F2/F3). May be sequenced behind F2/F3 — F5 is the FRED Phase-2 implementation deploy, not on a tight clock. NOTE the F2 coordination point in cross_domain_coordination — F5's Lambda shares the infra/aws/lambda/fred-data-ingestion/ directory with F2's target.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the deploy half of the FRED Phase-2 implementation segment. F4 (authoring) is done + verified; F5 lands the FRED macro pull in production. Sibling of F4, same author(DS)/deploy(AE) split as B1/B2.</priority>
    <sla>~1 effort-day — a new-Lambda terraform deploy + a deps layer; the pull code is authored + verified by F4.</sla>
  </metadata>

  <references>
    <f4>YALP_MDSRC.F4 (0.2.0_DS~A) — the parent. F4 authored + verified ingest_fred_macro.py (51 FRED indicators; gate-clean; dry-run 0 contract-drift; fidelity 45 EXACT / 4 CLOSE / 1 DIFF / 1 restored vs the served macro_data.json). RAVC-complete.</f4>
    <build_note>docs/briefs/mdsrc-f4-fred-ingestion-build-note-20260520.md (commit f42c2ab1a, origin/CLOUD) — CONSUME THIS AS THE BUILD INPUT. §5 has the deploy spec: deps (numpy/requests need a Lambda layer — NO pip install -t .), IAM (secretsmanager:GetSecretValue on opal/external-apis + s3:PutObject), sizing, the EventBridge schedule, the source-map entry.</build_note>
    <code>infra/aws/lambda/fred-data-ingestion/ingest_fred_macro.py — the F4-authored pull, in the shared working tree, uncommitted (~27.9 KB). Pulls 51 indicators; key from Secrets Manager opal/external-apis; emits json/macro/macro_data_fred.json (a SEPARATE artifact — not macro_data.json; no dual-writer).</code>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED, 73e4da697) — §3 step 2 (FRED key -> Secrets Manager: F4 already does this right) + §3 step 6 (contract-drift detection: F4 builds it in). The FRED integration is an INTEGRATION against the FRED API — never "scrape".</standard>
    <f2>YALP_MDSRC.F2 (your TO) — imports the EXISTING fred-data-ingestion (lambda_fred_ingestion.py) into Terraform. F5's Lambda shares that directory — see cross_domain_coordination.</f2>
  </references>

  <context>
    F4 (0.2.0_DS~A) authored + verified the FRED-macro-ingestion pull — 51 indicators, the implementation of the F1 Bloomberg->FRED mapping. The code (ingest_fred_macro.py) is AE-lane infra/aws/lambda code; F4's do_not bars DS from committing it. F5 is the AE half: commit it + deploy it as a Lambda. Same author(DS)/deploy(AE) split as B1/B2.

    IMPORTANT — F5's Lambda is NEW. ingest_fred_macro.py has never been console-deployed; it gets a fresh Terraform resource + apply — a standard new-Lambda deploy, Rule-1-clean natively. It does NOT need the F2-style terraform-import path (that path exists because the EXISTING fred-data-ingestion was console-deployed; F5's Lambda has no such history). So F5 is NOT gated on the F2 ruling — but it DOES share a directory with F2's target, so coordinate (below).
  </context>

  <scope>
    <in_scope>
      - Review ingest_fred_macro.py against infra/aws/lambda lane conventions — built + verified by F4, do not re-author; lane-convention adjustments only.
      - FUNCTION IDENTITY: ingest_fred_macro.py sits in infra/aws/lambda/fred-data-ingestion/ ALONGSIDE the existing lambda_fred_ingestion.py. Confirm F5's Lambda is a DISTINCT new function (F4 intends it so — separate 51-indicator pull, separate macro_data_fred.json artifact, its own EventBridge schedule). Recommend a distinct function name (e.g. fred-macro-ingestion) to avoid collision with the existing fred-data-ingestion function. Document the name chosen.
      - Commit ingest_fred_macro.py via .tools/safe-commit.sh.
      - Build the deps Lambda layer (numpy/requests) per build-note §5 — NO pip install -t . into the source dir (CLAUDE.md Rule 3); use/extend a layer.
      - Write the Terraform for the new Lambda: the function, the deps layer, the IAM (secretsmanager:GetSecretValue on opal/external-apis + s3:PutObject), memory/timeout sized for a 51-indicator pull (Rule 5), and a daily EventBridge schedule.
      - Update infra/aws/lambda/ci/lambda-source-map.json (Rule 4).
      - Full deploy cycle: code -> Terraform -> source map -> git commit -> terraform plan -> .tools/safe-apply.sh (HALTGT checkpoint) -> 0-diff -> git tag -> push --follow-tags.
      - Trigger one run; confirm json/macro/macro_data_fred.json is produced with all 51 indicators.
    </in_scope>
    <out_of_scope>
      - Re-authoring / re-verifying the pull logic — F4 built + verified it; F5 commits + deploys.
      - The F2 yield-curve fix + the import of the existing fred-data-ingestion — that is F2.
      - The FRED-vs-Bloomberg-residue MERGE (whether macro_data_fred.json merges into macro_data.json) — a v0.4 integration decision, flagged by F4; NOT F5. F5 ships the separate artifact F4 built.
      - Rationalizing any indicator overlap between ingest_fred_macro.py (51) and the existing lambda_fred_ingestion.py (8) — a v0.4 FRED-architecture-consolidation question; F5 deploys what F4 built, does not converge the two.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before deploy">
      <step>
        <run>comp-iam service on the new Lambda</run>
        <expect>Confirms the IAM (secretsmanager:GetSecretValue on opal/external-apis + s3:PutObject) is present before deploy.</expect>
        <if_mismatch>Add the missing IAM to iam.tf before deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh infra/aws/lambda/fred-data-ingestion/ingest_fred_macro.py</run>
        <expect>All three checks exit 0 — re-confirm F4's gate-clean result holds at commit time.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>comp-pipescript deployed + verify the terraform plan is 0-diff</run>
        <expect>Runner has the committed code (MATCH); 0-diff; macro_data_fred.json produced with 51 indicators.</expect>
        <if_mismatch>STALE/MISSING -> redeploy; non-0-diff -> investigate before tagging.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    F2 COORDINATION: F5's Lambda (ingest_fred_macro.py) and F2's target (lambda_fred_ingestion.py) share infra/aws/lambda/fred-data-ingestion/. You own both F2 and F5 — sequence them so the Terraform for the directory is coherent (F2 imports the existing function; F5 adds a new function; both can coexist in the same TF file/module — just author it deliberately, not as two conflicting drafts). HEADS-UP: ingest_fred_macro.py's presence in infra/aws/lambda/fred-data-ingestion/ means there is a main-repo copy of this Lambda family's code — if your F2 work assumed the family lived ONLY in portal/etl/orchestration/green/fred/, reconcile that (a main-repo copy + a portal-ETL copy = a dual-source-of-truth to be aware of; surface to CTO if it complicates the F2 import). F4 RAVC2-CC-CTO carries the FRED picture into v0.4. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.2.0_DS~A.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">ingest_fred_macro.py committed via safe-commit on origin/CLOUD; ds-commit-gate re-confirmed exit 0; the function identity confirmed (distinct new function; name documented, no collision with the existing fred-data-ingestion).</ac>
    <ac id="AC2">The new FRED-macro-ingestion Lambda deployed via terraform: the function + the deps layer (numpy/requests, no pip install -t .) + IAM + memory/timeout sized + a daily EventBridge schedule; lambda-source-map.json updated; full deploy cycle complete (commit -> plan -> safe-apply -> 0-diff -> tag -> push --follow-tags).</ac>
    <ac id="AC3">One run triggered; json/macro/macro_data_fred.json confirmed produced with all 51 indicators.</ac>
    <ac id="AC4">Phase-1 comp-iam + Phase-2 ds-commit-gate + Phase-3 comp-pipescript deployed + 0-diff reproduced in the session log Compiler Tools section. The F2-directory coordination + any dual-source-of-truth finding documented.</ac>
    <ac id="AC5">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.2.0_DS~A.</ac>
  </acceptance_criteria>

  <deliverables>
    - The committed + deployed FRED-macro-ingestion Lambda (51 indicators) + the deps layer; git tag; lambda-source-map entry.
    - Session log with the Compiler Tools section + the function-name choice + the F2-coordination note.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.2.0_DS~A.
  </deliverables>

  <do_not>
    <rule>Do NOT re-author or re-verify the pull logic — F4 built + verified it; F5 is review + commit + deploy.</rule>
    <rule>Do NOT deploy by any path other than terraform via .tools/safe-apply.sh (CLAUDE.md Rules 1 + 18). No console, no update-function-code.</rule>
    <rule>Do NOT pip install -t . into the source dir — deps go in a Lambda layer (Rule 3).</rule>
    <rule>Do NOT merge macro_data_fred.json into macro_data.json or converge the two FRED Lambdas — both are v0.4 decisions; F5 ships F4's separate artifact as built.</rule>
    <rule>Do NOT handle the FRED API key in chat / MCP / git / logs — reference the opal/external-apis secret by name only.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
