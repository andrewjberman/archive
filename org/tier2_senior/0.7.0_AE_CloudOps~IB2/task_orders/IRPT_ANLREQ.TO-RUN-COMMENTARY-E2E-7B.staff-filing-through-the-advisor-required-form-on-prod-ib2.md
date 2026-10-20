<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7B.staff-filing-through-the-advisor-required-form-on-prod-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ119</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is run 7's: one synthetic request filed through the PROD portal page by a minted synthetic staff user, every created key recorded at creation and deleted after the last read; no Terraform, no IAM change, no code change. Run 7's receipt (A_E2E7.txt) and rows S229 and S230 are the base.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- the grants of run 7 stand (ledger irpt-iamgrant CLOSED); this order adds none.
comp-adversary: RUN -- by reading run 7's receipt and the CTO's rulings (msgs 11385, 11403) against this order; the lens: a synthetic user whose name is blank, so the pre-filled Advisor is blank and the page holds the submit (a wrong test of the fix), a script that is run 7's untouched copy (it expects advisor=optional), a PROD page that is not yet the promoted branch, the two synthetic objects of run 7 left in place (row S229) mistaken for this run's, a second filing after a red hop. NOT seen (blind): the ticket service's answer to a filing with a typed Advisor on the deployed bytes (run 6 created a ticket through the API with an advisor text); denominator: one request.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ119: run 7b (cell AR-y-460).
<owned_cells>AR-y-460</owned_cells>
</decomp_ref>

  <objective>
    Run 7b is RUN 7 (order `IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7.staff-filing-through-the-portal-page-on-prod-ib2.md`, in this folder; receipt `irpt_anlreq_commentary_e2e7/A_E2E7.txt`, which stopped at B2) ON THE SAME TERMS, with the REPLACEMENTS below: one synthetic request filed through the PROD portal page by an unseeded synthetic staff user whose form Advisor is left AS THE PAGE PRE-FILLS IT, stopping at the first red hop. THIS ORDER STARTS ONLY ON MY GO MESSAGE. Read run 7's order in full first: its steps, its ledger legs (A mint, B browser, P poll, R route read, D delete), its R0 gates and its eighteen-line receipt apply unchanged except where the REPLACEMENTS say.
  </objective>

  <context>
    WHY: run 7 stopped at B2 because the page omitted a blank Advisor and the ticket service requires it (CTO msg 11385). The promoted branch `cand/dell2/anlreq-andrew-walk-v2` (CTO row 4664, PROD promote order IRPT_ANLREQ.TO-PROMOTE-WALK, DT lane) pre-fills the Advisor with the filer's name and holds a blank one. The CTO's terms (msg 11403): run 7b on run 7's terms, the filer leaving the pre-filled Advisor as it is.
    THE REPLACEMENTS. (R0) `prod=` must read the DT's promoted sha: the K3 line of `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_walk/A_PROMOTE_WALK.txt` names it, and `git -C portal merge-base --is-ancestor d5d2fdeab3af8fcbc1f74ef2d5f2eefd7a89c3d3 origin/PROD` must exit 0; the served site's Last-Modified is no earlier than that run's live minute; every other R0 read is run 7's (root `0485393f3a-r34n`, the three CodeSha256 values, grants, the DLQ depth before, the ledger sweep with its denominator). A red R0 mints NOTHING.
    (A) the synthetic staff user carries a NON-EMPTY synthetic NAME set at the mint (for example `E2E7B SYNTHETIC FILER`), because the page pre-fills the Advisor from that name; print the name (it is synthetic) as part of the A line. If the mint code cannot set a name: STOP before any filing and say so. (A2) advisor none-by-design is replaced by `A2 advisor prefilled-by-page` (the run types no advisor). (B) the browser instrument is the re-proved copy `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~325/run7_browser_leg.mjs` (order AR-y-459; its PAGE_NOTES.md lists where the new form differs; read it first, and run its `--offline` composite once as your own gate, expecting the OK line with `advisor=required advisor_prefilled=yes`), not the copy under ~323. B1 prints `advisor=required advisor_prefilled=yes`; if `advisor_prefilled=no`: STOP before the press and say so. Copy `e2e7_run.py` and `e2e7_cleanup.py` to `irpt_anlreq_commentary_e2e7b/` as `e2e7b_run.py` and `e2e7b_cleanup.py`, pointing the browser leg at the ~325 script; the holdings file is a NEW synthetic file whose sha256 differs from every earlier run's (print it). ONE press, no Keep, no second filing.
    (D) delete only keys recorded at creation. Run 7's two leftover state objects (row IRPT_ANLREQ-D2-S229; call dell2-20261020T152652Z-e76c) are NOT this run's: do not touch them, and if this run's own upload leaves objects your principal cannot delete, record keys by creation (the page makes the upload BEFORE a ticket id exists, so identify it by the synthetic address AND this run's unique holdings hash, record the keys, then delete what you can) and file the row.
    THE RECEIPT: write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7b/A_E2E7B.txt with run 7's eighteen lines (each answered or `NOT-RUN <the hop where the run stopped>`) and the closing line `RUN-DONE PASS` or `RUN-DONE STOP at <hop> code=<code>`; also print the HTTP status and closed body words of the ticket create when B2 is refused (the page shows them or the browser leg records the response status; run 7 could not read them).
  </context>

  <the_act>
    GO only on my message (it names TV2's RB1 terminal report, the promote's K3 line and the AR-y-459 VALID). Start at run 7's step 1 (with the ledger irpt-commentary-e2e-7b-20261020, legs A mint, B browser, P poll, R route read, D delete; commit it; the open-deploys denominator as there) and go on only while each step reads green. A red hop is a STOP. Report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2) with the receipt path and the closing line.
  </the_act>

  <bounds>
    One request, one press, no Keep, no second filing after a red hop. No Terraform, IAM or code change. No ticket other than this run's own synthetic one is touched. Run 7's leftover objects stay. The synthetic user and everything this run created are deleted after the last read, except what the principal cannot delete (recorded and filed as a row).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7b/IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-7B.staff-filing-through-the-advisor-required-form-on-prod-ib2.proof_of_spec.json`.
    <criterion id="E2E7B-AC1" cell_refs="AR-y-460">The record holds all eighteen lines, each answered or marked not run.<invocation>grep -c -E '^(R0|A|A2|L|B1|B2|B3|P1|P2|P3|P4|P5|P7|R|R2|DLQ|D) |^RUN-DONE (PASS|STOP at )' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7b/A_E2E7B.txt</invocation><expect>^18$</expect></criterion>
    <criterion id="E2E7B-AC2" cell_refs="AR-y-460">The run is honest about its ending (a pass, or a stop at a named hop).<invocation>grep -c -E '^RUN-DONE (PASS|STOP at [A-Z0-9]+ code=[A-Z0-9_]+)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7b/A_E2E7B.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="E2E7B-AC3" cell_refs="AR-y-460">The ledger irpt-commentary-e2e-7b-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-commentary-e2e-7b-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 CloudOps seat under ADDENDUM 9 as the CTO's msg 11403 carries it (run 7b on run 7's terms), not a worker cell; the cell AR-y-460 is the issuer's, as for TO-RUN-COMMENTARY-E2E-7.
