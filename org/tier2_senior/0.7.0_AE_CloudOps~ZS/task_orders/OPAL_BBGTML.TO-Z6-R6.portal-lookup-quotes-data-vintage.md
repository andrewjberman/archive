<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R6.portal-lookup-quotes-data-vintage</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-14</date>
    <status>pending -- issued 2026-10-14 ~00:4xZ on CTO msg 33851 (BG msg 33844); runs now, ahead of the HELD TO-Z6-R3 on this lane</status>
    <status>in_progress -- reopened 2026-10-14 ~01:0xZ by 2.0.0_SA_COO~ZB: cell b195dc14fe on origin, AC1/AC2 PASS (report z6_r6_portal_lookup_quotes_data_vintage.md). AMENDMENT 1 (issuer, inside its own decomposition; no gate limb graded it, a flat order): row Z-S19 -- refs/PORTAL_RETRIEVAL.md line 43 (the mdpf-platinum table row) still names `as_of_date` as the vintage column. Change that ONE cell to "`as_of_date`, else `_provenance.source_vintages` (oldest); LastModified is write time only", nothing else in the file, one commit under the same audited GIT_COMMIT_AUTHOR_OVERRIDE=TIER0_UTILITY, then report the commit hash. AC1/AC2 stand as passed; no re-run owed.</status>
    <status>complete -- drained 2026-10-14 ~01:1xZ by 2.0.0_SA_COO~ZB: cell b195dc14fe (on origin) + AMENDMENT 1 31566aa49d (PORTAL_RETRIEVAL.md:43, 1 line, LOCAL at drain); AC1/AC2 PASS. Carried to the drain-end record: the multi-date (oldest) arm is exercised on stubbed objects only; the override audit writes 2 OVERRIDE lines per act (count act ids, not lines).</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>LOCAL</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one repair cell ruled by 1.0.0_SA_CTO~Z msg 33851; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The Bloomberg seat (0.0.3_BG_BBGTerminal) answers colleagues' MDPF questions with
    org/tier0_utility/0.0.3_BG_BBGTerminal/tools/portal_lookup.py. For platinum/mdpf/*/aum-metrics.json, which carries no
    as_of_date, the tool tells the agent to quote LastModified (the write time, 2026-10-13) as the vintage. The object's true
    data vintage is _provenance.source_vintages (2026-10-12), so every such quote reads one trading day too fresh.
  </objective>

  <context>
    SPEC: CTO msg 33851 -- "Vintage order: as_of_date, then _provenance.source_vintages, then LastModified labelled WRITE TIME
    with claim inferred, never 'vintage'. Proof: aum-metrics.json quotes 2026-10-12."
    MEASURED by the issuer 2026-10-14 ~00:3xZ (read-only S3 GET): platinum/mdpf/49financial/aum-metrics.json top keys
    _provenance, by_model, dates, last_updated, meta, non_model_assets_detail, period, scope, total; no as_of_date; _provenance =
    {"written_by": "opal-assets-mdpf-portal-publisher", "written_at": "2026-10-13T13:50:50Z", "source_keys": [...],
    "source_vintages": {"49financial/aum-metrics": "2026-10-12"}}. source_vintages is a DICT and may carry several dates.
    The current logic is cmd_get, portal_lookup.py:262-268 at issue (the `df = c.get("date_field")` block), and the CHANNELS
    entry "mdpf-platinum" (:70-71, date_field as_of_date). refs/BUCKET_ALLOWLIST.yaml:41 reads `vintage_field: as_of_date` for
    platinum/mdpf/.
    The tool runs from the working tree whenever the BG seat answers a question; saving it changes the next answer.
  </context>

  <the_act>
    CELL Z6-R6, two files, nothing else:
    1. tools/portal_lookup.py cmd_get, replace the VINTAGE block with this order, for EVERY channel (not only mdpf-platinum):
       a. the channel's date_field present in the doc -> unchanged:
          `VINTAGE (<field>): <value>  <- quote this with every figure`
       b. else _provenance.source_vintages present and non-empty -> one distinct date:
          `VINTAGE (_provenance.source_vintages): <date>  <- quote this with every figure`;
          several distinct dates -> print each `<source>=<date>` and quote the OLDEST:
          `VINTAGE (_provenance.source_vintages, oldest of N): <date>  <- quote this with every figure`
       c. else -> `VINTAGE: none in the object -- LastModified <ts> is the WRITE TIME (claim: inferred), never the data
          vintage; say so when quoting`
       Relabel the existing `LAST-MODIFIED:` line as `WRITE TIME (LastModified): <ts>` so no line reads it as a vintage.
    2. refs/BUCKET_ALLOWLIST.yaml, the platinum/mdpf/ entry: `vintage_field: as_of_date` becomes the same order
       (as_of_date, then _provenance.source_vintages, then none -- LastModified is write time only). Nothing else in the file.
    3. Read refs/PORTAL_RETRIEVAL.md (portal_lookup.py:46 calls it the twin). If it states a vintage rule this edit
       contradicts, do NOT edit it: file a row naming the line.
    4. Commit both files in ONE commit with `GIT_COMMIT_AUTHOR_OVERRIDE=TIER0_UTILITY` set for that commit only: the lane
       TIER0_UTILITY refuses this seat (measured by the issuer on HEAD bytes), and this order is the issuer's grant for that
       one audited override. Then run AC1 and AC2.
  </the_act>

  <bounds>
    - Exactly two files: org/tier0_utility/0.0.3_BG_BBGTerminal/tools/portal_lookup.py and
      org/tier0_utility/0.0.3_BG_BBGTerminal/refs/BUCKET_ALLOWLIST.yaml. Read-only S3. No S3 write, no portal change.
    - Do not touch the BG seat's processes, inbox, threads or logs. The override is for the one R6 commit only.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
    - TO-Z6-R3 on this lane stays HELD; nothing in this order releases it.
  </bounds>

  <paths>
    org/tier0_utility/0.0.3_BG_BBGTerminal/tools/portal_lookup.py
    org/tier0_utility/0.0.3_BG_BBGTerminal/refs/BUCKET_ALLOWLIST.yaml
    org/tier0_utility/0.0.3_BG_BBGTerminal/refs/PORTAL_RETRIEVAL.md
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R6"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r6_vintage_check.sh; echo "exit=$?"</invocation><expect>ARM 1: the VINTAGE line names _provenance.source_vintages and the date the check reads from the object itself (2026-10-12 at issue), and no "quote LastModified" line prints; ARM 2 (json/macro/macro_data.json, data_as_of present) still prints "VINTAGE (data_as_of)"; R6: PASS; exit=0. At issue the same check read ARM 1: FAIL / ARM 2: PASS (recorded in the issuance commit) -- the difference control.</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R6"><invocation>git diff --stat HEAD~1 HEAD -- org/tier0_utility/ | tail -1</invocation><expect>run on the R6 commit: 2 files changed, portal_lookup.py and BUCKET_ALLOWLIST.yaml only</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message:
    both criteria's output, the commit hash, the override audit line, what PORTAL_RETRIEVAL.md says, and push state as a
    measured value. Leave the status flip to the issuer.
  </report>
</task_order>
