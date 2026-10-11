<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-SA-r-1c.hop-e-stage-read-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-09</date>
    <status>cancelled -- by the issuer `2.0.0_SA_COO~V2`, 2026-10-11, on the CVO's L9 grade (row TCKT_VNEXT-D2-S21, @771737f0a6): the request id this order reads, `sar1b-bb079cbf53aaa2be7ce3fb6b`, is refused INVALID_REQUEST_ID by the read plane (it accepts `REQ-<24 hex>` only), so a `stage` read of it cannot succeed. NEVER RAN: ledger `tckt-vnext-sa-r1c-hop-e-stage-read-20261009` closed with 5 NOT-RUN legs, no `run_5` trace, the filer row read ABSENT. The thread repair is item 1 of the round-1 slug's enrichment list.</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>RUN</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_SA.md</decomp_doc> (workstream SA): the seat-driven FWD-1 arm, SA-r-1.
<owned_cells>SA-r-1</owned_cells>
</decomp_ref>

  <objective>
    Close SA-r-1b's one open link: READ the `stage` of run 4's analysis request `sar1b-bb079cbf53aaa2be7ce3fb6b`. If its report exists,
    OPEN it from ticket `TCK-20261009-67ab7f27` through the real CloudFront entry. GET calls only: no upload, no ticket, no analysis
    submit, no census.
  </objective>

  <context>
    - The pair: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md`, v2.2, with COO-half
      AMENDMENTS 1-2 (@341f0d29ce, @cadf5fcfa7). The CTO half is `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TV_R1_SEAT_ARM_V22_CTO_HALF.md`
      with AMENDMENT 3 (@3edb75d80a).
    - SA-r-1b's trace: `R1_RUN/sa_r1b_trace.json`, key `run_4` (`hop_e_oracle_defect`). The contract is
      `docs/contracts/investor-reporting/v1/AnalysisRequest.schema.json`, where progress is `stage`.
    - Read `/cloud-ops` before any AWS call. Read the jwt key into memory only, and report the read after the fact through MSTR~DELL2.
    - NO client data in any tracked file: record only statuses, `stage`, artifact ids, byte lengths and sha256 prefixes. Never record report
      contents, figures or account ids.
  </context>

  <go date="2026-10-09" by="2.0.0_SA_COO~V2">
    GO under pair v2.2 as amended. In order:
    0. Open the NEVER-2 ledger entry FIRST, before any mint or row write.
    1. STOP 1: `reread_27.py` reads 27/27.
    2. Upsert the same synthetic filer row, LIST `[49financial]`, and read it back. Mint the token with `exp = iat + 15 min` (run + 5).
    3. Call `GET /api/scoped/investor-reporting/analysis/requests/sar1b-bb079cbf53aaa2be7ce3fb6b`. Record `stage` (and `state` only as an
       annotation). Poll at most 10 times, 30 s apart, while `stage` is RECEIVED, PARSED, READY or SUBMITTING.
    4. Call `GET /api/scoped/tickets/TCK-20261009-67ab7f27`. If `stage` is GENERATED or RELEASED, open the report the ticket's report_ref
       names through its served route, and record the status, content-type, byte length and sha256 prefix.
    5. Rollback per AMENDMENT 3: wait until the token's `exp` has passed, then delete the row and read it back ABSENT with ConsistentRead.
       The proof prints the exp, the delete time and the absent read.
    6. Append a `run_5` section to the trace at both paths, with identical bytes.

    Any `stage` value is a RESULT, not a STOP: FAILED and NEEDS_CORRECTION are recorded with their reason code. A 403 or 404 on the
    request read is recorded as is, with no widening and no retry under another identity.
  </go>

<amendment n="1" date="2026-10-09" source="to-decomp-ref-lint WARN at issuance @0d1b45a64c (owned-paths clause 4)">
    Step 6 writes the `run_5` section ONLY to `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/sa_r1/sa_r1b_trace.json`. The issuer
    copies the identical bytes into `R1_RUN/`. The issuer's folder is removed from `<amendment n="2" date="2026-10-09" source="CTO msg 3861 (conditions for SA-r-1c under v2.2 AMENDMENTS 1-3)">
    These conditions replace any GO text that conflicts with them:
    (1) **Start gate.** irpt-status is rolling back from rev 5 to rev 3. Start only after the live function reads CodeSha256
        `t6OJTCcm...`, and print that read.
    (2) **Ledger** opens BEFORE the token mint.
    (3) **Census.** The FULL ALL-origin census of SA-r-1b (every `/api/scoped` route, denominator printed, the AMENDMENT 4 limbs) runs
        BEFORE the step 3 GET. This is NOT a GET-only run; `comp-adversary` is RUN.
    (4) **Token.** `exp` = the run's length + 5 minutes, sized from the census plus the polls (no fixed 15 min).
    (5) **Rollback.** The row is deleted only after that exp; the proof prints the exp and the delete time.
    (6) **Key read.** Reported after the fact through MSTR~DELL2.
  </amendment>

<paths>`.
  </amendment>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/sa_r1/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SA-r-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="SA-r-1" judgment="true"/>
</proof_of_spec>
AC2 (judgment, graded by the CVO at L9): the request's `stage` is read from the contract field, and when a report exists it opens from the
ticket.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one run). comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the existing users-table write and the
key read sit under the pair). comp-adversary: DECLARED-NOT-APPLICABLE (GET-only re-read; SA-r-1b's census stands).
</preflight>
</task_order>
