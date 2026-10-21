<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-RETENTION-CENSUS.rows-by-policy-hash-since-r34o-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<round>60</round>
<workstream>~GREL4</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- READ ONLY: DynamoDB reads of the retention records on the PROD request index (query or scan with a filter, paginated, counted client-side); nothing is written, updated or deleted; no Terraform, IAM or code change; no host script.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the reads use the CloudOps applier's own read access; no grant is added.
comp-adversary: RUN -- the lens: a count that is a PAGE count (paginate to the end and print the denominator: items scanned), a row printed instead of counted (print counts, firm ids and flags only, never a row body, a key or a policy document), a hash prefix compared against the wrong revision, synthetic judged by guess (a row is synthetic only when its request id is one of the run receipts' request ids or its owner is the minted synthetic user; otherwise `no`; say how you decided), a write. NOT seen (blind): the table's key schema (you know it from earlier index reads); denominator: the rows of the two revisions named below.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL4: the census the CTO asks for in the r34p packet (msg 11639).
<owned_cells>AR-g-180</owned_cells>
</decomp_ref>

  <objective>
    Census the RETENTION rows of the PROD request index that carry the two revisions whose policy hash r34o moved: `irpt-anlreq-x10-v1` and `irpt-dashbd-x10-v1`. WHY: r34o (live 23:12:44Z) added the ANALYSIS_AUDIT family to the packaged registry, which changed the current policy_sha256 of those two revisions; retention.py:147 refuses any row whose stored `policy_sha256` differs from the current hash of its revision (run 7e: RetentionRefused). The CTO ruled r34p = r34o minus the registry change and wants, in the packet, a census of the rows created since 23:12Z carrying the new hashes: count, firm, synthetic yes/no (msg 11639). You read; you change nothing. THIS ORDER STARTS ONLY ON MY GO MESSAGE.
  </objective>

  <context>
    The retention record shape (reports/retention.py): a row with `retention_id` (`RET-` plus 64 hex), the revision it was reserved under, `policy_sha256` (stored at reserve time), `created_at`, `expires_at`, `ceiling_at` (epoch seconds) and `generation`; the row's owner carries a `firm_id`. The four hashes (first 16 hex, computed by lib/opal_naming.reporting_policy from the packaged registries): `irpt-anlreq-x10-v1`: OLD (r34n) 8edbe84b05765c36, NEW (r34o) cfed04bb8c2f1982; `irpt-dashbd-x10-v1`: OLD 301c58e24ff0feda, NEW 244a20425ba40cde. The r34o install printed success at 2026-10-20T23:12:44Z (its epoch is 1792537964; compute it yourself and print it). Run receipts for the synthetic requests: irpt_anlreq_commentary_e2e7d/A_E2E7D.txt, irpt_anlreq_commentary_e2e7e/A_E2E7E.txt and state_e2e7e.json (request ids and the synthetic user); Andrew's own ticket of 22:58:54Z is TCK-20261020-b1d61f80 (a REAL filing: its rows are `synthetic no`).
  </context>

  <the_act>
    GO only on my message. Read-only, in this order, stopping at the first step that does not read as written:
    1. R0: print the date, the table name you read (the request index; its name is in the resident's bindings or your earlier index reads), and the epoch of 2026-10-20T23:12:44Z.
    2. C1: scan (paginate to the end; print items scanned) the retention rows of the two revisions. For each of the four (revision, hash-prefix) combinations print: rows with `created_at` BEFORE the r34o epoch, and rows with `created_at` at or after it.
    3. C2: for the rows at or after the r34o epoch whose stored hash is NEW (cfed04bb... or 244a2042...): print one line per (firm id, synthetic yes/no): the count. Print the same for rows at or after the epoch with a stored hash that is neither OLD nor NEW (expected: zero).
    4. C3: for rows BEFORE the epoch with an OLD hash: print the count per firm and the number among them whose request id is Andrew's ticket's request (print yes/no only). These are the rows the r34o registry made refusable; they become valid again under r34p.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census/A_CENSUS.txt with the lines `R0 ...`, `C1 <revision> <hash16> before=<n> since=<n>` (four lines), `C2 <firm> synthetic=<yes|no> new_hash=<n>` (one per group), `C2 other_hash=<n>`, `C3 <firm> old_hash_before=<n>`, `C3 andrew_ticket_rows=<yes|no>`, and the final line `CENSUS-DONE items_scanned=<n>`. Report ONCE to 2.0.0_SA_COO~G2 (cc 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2) with the path and the final line.
  </the_act>

  <bounds>
    READ ONLY. No write, update, delete, key rotation, queue message, IAM or Terraform change. Print counts, firm ids and yes/no only: never a row body, an S3 key, a policy document or a token. Not alongside another IB2 act on the request index.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census/IRPT_ANLREQ.TO-READ-RETENTION-CENSUS.rows-by-policy-hash-since-r34o-ib2.proof_of_spec.json`.
    <criterion id="CENSUS-AC1" cell_refs="AR-g-180">The record holds the four C1 lines and the closing line.<invocation>grep -c -E '^(C1 irpt-(anlreq|dashbd)-x10-v1 [0-9a-f]{16} before=[0-9]+ since=[0-9]+|CENSUS-DONE items_scanned=[0-9]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census/A_CENSUS.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="CENSUS-AC2" cell_refs="AR-g-180">The record states the other-hash count and Andrew's-ticket answer.<invocation>grep -c -E '^(C2 other_hash=[0-9]+|C3 andrew_ticket_rows=(yes|no))$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census/A_CENSUS.txt</invocation><expect>^2$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 CloudOps seat under the CTO's msg 11639 (the r34p packet census), not a worker cell; the cell AR-g-180 is the issuer's, as for TO-APPLY-R34O.
