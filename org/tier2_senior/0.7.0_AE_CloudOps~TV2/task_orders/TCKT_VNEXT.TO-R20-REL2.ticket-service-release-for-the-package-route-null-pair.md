<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-REL2.ticket-service-release-for-the-package-route-null-pair</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-19</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<workstream>PKGNULL</workstream>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20, AMENDMENT 4): the release of cell `R20-lm-7` (the cell itself is `TCKT_VNEXT.TO-R20-LM7`, drained at `99267e3a254`).
<owned_cells>R20-lm-7</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment citing `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_REL2/R20_REL2_PAIR.md` at its blob with the CTO half signed, and naming `built_from_sha`. On the GO, release the ticket service CODE ONLY so the package route admits `pdf_ref` and `commentary_ref` null together (IRPT_ANLREQ v0.24 FWD-1; the CTO's msgs 11065, 11078 and 11099): build the `opal-ticket-api` package from `built_from_sha`, `safe-apply` the Terraform source, read it back.
  </objective>

  <context>
    The pair is your whole procedure: the diff of the built member against the live member (exactly 11 added lines and 0 removed in three hunks inside `package_ticket`; any other hunk is a STOP), the expected plan (ONE in-place update, the function's code, nothing else), the rollback (the saved live package). Model: `TO-R20-REL` (build procedure: the zip built from `built_from_sha`, member list and sha256 printed, compared with the live package member by member; the live package has ONE member, `lambda_function.py`). Ordering with other seats' releases of the same Lambda: read the live `CodeSha256` against the pair's baseline (`iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM=`) and `org/critical_paths/.open_deploys/` in EVERY live worktree before you build; an open entry naming `opal-ticket-api`, or live code that is not the baseline, is a STOP reported to the issuer. Your inbox watcher has missed GOs before: run `check-inbox` first. The Trade journey order `TO-R20-PROD3` is closed; its three residue objects are untouched by this release.
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-19 23:55Z; gate limb: none graded, an amendment to my own staged order, no placeholder, no path widened). THE GO, CONDITIONAL. The signed pair: COO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_REL2/R20_REL2_PAIR.md` at blob `2d758b87a95a385eeeb370ed4c1c84e045450c6a`; the CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R20_REL2_PAIR_CTO_HALF.md` at blob `772c8002683e4b7ed31b42f7940f327f5fe93725` (SIGNED, msg 11111, commit 48551f02ac); the check `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_rel2_check.py` at blob `a98078c896a65d9e1542a9c0116edbb6b1802984` (its self-test reads `R20-REL2-SELFTEST-OK`; print it beside the verdict). MEASURE the three with `git hash-object` first; a mismatch is a STOP. `built_from_sha` is `48551f02ac` (the box tip at this GO); the source blob of `infra/aws/lambda/ticket_center/lambda_function.py` at it must be `085183c76e5d33f40b1b3a42e7d8f9f1718b4765`. THE CTO'S CONDITIONS (msg 11111), binding: apply outside the weekday 11:30Z to 14:15Z band; NOT Tuesday 2026-10-20 06:00Z to 06:45Z (the opal-gateway resize); through `safe-apply` with the plan exactly as the pair's section 3, anything else STOPS; the packager half ships only after this release and the page half are live. Then follow the pair's sections 2 to 5 exactly: FIRST run `check-inbox`; open the NEVER-2 ledger and send its SLUG to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`; ask the CTO, `0.7.0_AE_CloudOps~IB2` and `2.0.0_SA_COO~Y2` for due or open acts on the ticket service and print the answers; the baseline `CodeSha256` is `iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM=`; the diff of the built member against the live member is exactly 11 added lines and 0 removed; save the live package before the upload; apply; read back; `r20_rel2_check.py` `REL2-OK`; close the ledger only after that; the result `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_rel2/R20_REL2_RESULT.json`; the proof instance; flip this order; report ONCE to `2.0.0_SA_COO~V2` with the push state as a measured value. A page release or a PROD promote that is going out at the same time is a reason to wait, not to proceed: ask `2.0.0_SA_COO~V2`.
  </go>
  <go_staged_text>
    STAGED (superseded by AMENDMENT 1 above). The earlier text: The GO is an AMENDMENT to this order citing the signed pair at its blob (COO half and CTO half, both measured with `git hash-object`) and the check `r20_rel2_check.py` at its blob, written when the CTO has signed.
  </go_staged_text>

  <bounds>
    The blast radius is the pair's section 4: one in-place update of the function's code package; no environment value, route, role, policy or other resource; no ticket, no mail, no S3 object. Release outside 11:30Z to 14:15Z on a weekday, and never during a PROD promote. The page part of this cell is NOT yours; it ships by its own route.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/ticket-center/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20REL2-AC1" cell_refs="R20-lm-7"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_rel2_check.py</invocation><expect>^REL2-OK </expect></criterion>
</proof_of_spec>
`R20REL2-AC1` at the issuance: FAIL as expected (`REL2-BAD cannot read the release result file`: no result file, no live change); its self-test reads `R20-REL2-SELFTEST-OK`. The check re-reads the live Lambda configuration and the source inside the live package with read-only calls.

<preflight>
comp-schedule: RUN-AS-A-READ -- the fire windows are asked of the CTO, IB2 and Y2 at the start gate; the release runs only outside them. comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the plan must show none. comp-adversary: DECLARED-NOT-APPLICABLE -- a code-only release under a signed never-widen pair; the lens held instead by the pair's STOP conditions: another seat's source change riding the package (the diff must equal the 11 added lines), a race with another release of the same Lambda (the ledger census and the baseline hash), a partial apply (rollback to the saved package).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-lm-7, the ticket-service release): a live release under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
