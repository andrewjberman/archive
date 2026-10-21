<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-RETENTION-CENSUS-R34Q.rows-under-dashbd-and-audit-revisions-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<round>60</round>
<workstream>~GREL5</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: DynamoDB reads of the retention records on the PROD request index (scan with a filter, paginated, counted client-side); nothing is written, updated or deleted; no Terraform, IAM or code change; no host script.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the reads use the CloudOps applier's own read access; no grant is added.
comp-adversary: RUN -- the lens: a count that is a PAGE count (paginate to the end and print the denominator: items scanned), a row printed instead of counted (print counts only, never a row body, a key or a policy document), a hash prefix compared against the wrong revision, a revision named by a different spelling (match the revision field exactly), a write. NOT seen (blind): the table's key schema (you know it from your earlier census A_CENSUS.txt); denominator: the rows of the two revisions named below plus items scanned.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL5: the census the CTO asks for in the r34q packet (CTO msg 11843 item 2; 2.0.0_SA_COO~Y2 msg 11819).
<owned_cells>AR-g-181</owned_cells>
</decomp_ref>

  <objective>
    Census the RETENTION rows of the PROD request index that carry two revisions whose registry entries r34q puts on the resident: `irpt-dashbd-x10-v1` (PENDING_ENFORCEMENT; its policy hash differs between r34n and r34q) and `irpt-anlreq-audit-x10-v1` (new, ACTIVE). WHY: retention.py:147 refuses any row whose stored `policy_sha256` differs from the current hash of its revision, so a row under either revision would change meaning when r34q lands. The CTO expects 0 rows under each, measured. You read; you change nothing. THIS ORDER STARTS ONLY ON MY GO MESSAGE.
  </objective>

  <context>
    The retention record shape (reports/retention.py): a row with `retention_id` (`RET-` plus 64 hex), the revision it was reserved under, `policy_sha256` (stored at reserve time), `created_at` (epoch seconds). The hashes (first 16 hex, computed by lib/opal_naming.reporting_policy from the r34q packaged registry): `irpt-dashbd-x10-v1`: r34n 301c58e24ff0feda, r34q 244a20425ba40cde; `irpt-anlreq-audit-x10-v1`: r34q 2b4f91d3feda649b; and for the control, `irpt-anlreq-x10-v1`: 8edbe84b05765c36 (unchanged in r34q; your earlier census found 10 rows under it). The table and the query shape are those of your earlier census (`org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census/A_CENSUS.txt`).
  </context>

  <the_act>
    GO only on my message. Read-only, in this order, stopping at the first step that does not read as written:
    1. R0: print the date, the table name you read, and the denominator method (paginated scan to the end).
    2. C1: scan the table to the end (print items scanned). For each of the four (revision, hash-prefix) combinations print the count of rows (all-time): `irpt-dashbd-x10-v1` 301c58e24ff0feda, `irpt-dashbd-x10-v1` 244a20425ba40cde, `irpt-anlreq-audit-x10-v1` 2b4f91d3feda649b, and the control `irpt-anlreq-x10-v1` 8edbe84b05765c36.
    3. C2: print the count of rows whose revision is `irpt-dashbd-x10-v1` or `irpt-anlreq-audit-x10-v1` with a stored hash that is none of the three above (expected 0), and the count of rows whose revision field contains the text `audit` or `dashbd` under any other spelling (expected 0).
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census_r34q/A_CENSUS_R34Q.txt with the lines `R0 ...`, `C1 <revision> <hash16> rows=<n>` (four lines), `C2 other_hash=<n> other_spelling=<n>`, and the final line `CENSUS-DONE items_scanned=<n>`. Report ONCE to 2.0.0_SA_COO~G2 (cc 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2) with the path and the final line.
  </the_act>

  <bounds>
    READ ONLY. No write, update, delete, key rotation, queue message, IAM or Terraform change. Print counts only: never a row body, an S3 key, a policy document or a token. Not alongside another IB2 act on the request index.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census_r34q/IRPT_ANLREQ.TO-READ-RETENTION-CENSUS-R34Q.rows-under-dashbd-and-audit-revisions-ib2.proof_of_spec.json`.
    <criterion id="CENSUSQ-AC1" cell_refs="AR-g-181">The record holds the four C1 lines and the closing line.<invocation>grep -c -E '^(C1 irpt-(anlreq|dashbd|anlreq-audit)-x10-v1 [0-9a-f]{16} rows=[0-9]+|CENSUS-DONE items_scanned=[0-9]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census_r34q/A_CENSUS_R34Q.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="CENSUSQ-AC2" cell_refs="AR-g-181">The record states the other-hash and other-spelling counts.<invocation>grep -c -E '^C2 other_hash=[0-9]+ other_spelling=[0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census_r34q/A_CENSUS_R34Q.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 CloudOps seat under the CTO's msg 11843 (the r34q packet census), not a worker cell; the cell AR-g-181 is the issuer's, as for TO-READ-RETENTION-CENSUS.
