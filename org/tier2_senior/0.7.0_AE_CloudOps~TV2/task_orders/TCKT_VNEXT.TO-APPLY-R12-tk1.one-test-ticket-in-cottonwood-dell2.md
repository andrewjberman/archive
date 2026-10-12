<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R12-tk1.one-test-ticket-in-cottonwood-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>SERVED</risk>
<round>12</round>
<proof_genre>APPLY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R12.md</decomp_doc> (round 12): cell `R12-tk-1`, one test ticket.
<owned_cells>R12-tk-1</owned_cells>
</decomp_ref>

  <objective>
    File ONE ticket in the live ticket store through the existing create route, as the commentary service principal, in tenant
    cottonwood, titled as a test, and report its id. It is the ticket side of a pair for NFRA_TRNSPT TR-dp-24: `2.0.0_SA_COO~Y2`
    files a synthetic analysis request naming this ticket AFTER it exists. Nothing else is written, posted or deleted.
  </objective>

  <context>
    Authority: the CTO's ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_DELL2_RELAUNCH_THREE_ASKS_READ_AND_RULED_20261012.md`
    section 7 @2b020683c1: "ONE request through the intake door, as the project's existing synthetic filer (no identity minted), in
    tenant cottonwood, naming a ticket 2.0.0_SA_COO~V2 files FIRST, titled as a test." Conditions that bind this order: the content
    is synthetic (no real client value); the write set is the literal keys the act creates, listed in the record; nothing is
    deleted; this order sends no draft and calls no outside model.
    The route and body are in `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/FWD10_H6_H5_TICKET_WRITE_CONTRACT.md`
    section 2, and your own earlier run of it is `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/tckt_f10/F10-M_arms_result.json`
    (step 4: 201, ticket TCK-20261009-a1052909, with a synthetic attachment pointer). Follow that run's method for the token: read
    from the secret `opal/ticketing/svc-commentary` into memory, sent as a Bearer header only.
    **DRAFT AND REQUEST ID ARE OMITTED.** The create route accepts `draft_commentary` and `report_request_id` each on its own
    (`infra/aws/lambda/ticket_center/tests/test_commentary_write.py:111-119`); send NEITHER, so the ticket carries no draft and no
    request id and the drafter's first post has nothing to overwrite. If the deployed route refuses a body without a draft, STOP,
    send nothing further, and report the refusal text; do not add a placeholder draft on your own.
    **Notice side effect, known:** a CREATE fires the existing distribution-list notice (`notify_dl_isolated`), as your earlier run
    did. It carries no draft text. This order adds nothing to it.
    **No email address in any tracked file or printed line; no token printed, written or committed.** The body's requester fields
    are optional and are OMITTED.
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. PRE-READ. One `get-item` of the earlier ticket TCK-20261009-a1052909 (positive control: it reads status open) and one
       read of the live ticket function's configuration showing `COMMENTARY_ALLOWED_FIRMS` contains `cottonwood`. Print both.
    2. THE BODY, built from the contract's section 2 and your earlier run: `ticket_type` analysis_request; `title` beginning
       exactly `[TEST TCKT_VNEXT R12]` and saying it is a synthetic ticket for the NFRA_TRNSPT TR-dp-24 pair; `source`
       `commentary:r12-tk-1`; `answers` with `firm` cottonwood, a synthetic `advisor`, `report_type` Overview and
       `add_commentary` true (no `household` key); `attachment` a SYNTHETIC pointer as in AMENDMENT 2 of your earlier run
       (`upload_id` `test-r12-tk1-<run>`, `input_id` `portfolio_` plus the sha256 of a TEST label). No `draft_commentary`, no
       `report_request_id`, no requester email or name.
    3. THE ONE WRITE: `POST /api/scoped/tickets` ONCE. Do not retry on a 2xx. On a non-2xx, report the status and the response
       text and STOP; do not retry with a changed body. Read the ticket id from the response; never type one.
    4. READ BACK: one `get-item` of the new ticket. State its tenant (`requester.firm`), `ticket_type`, `status`, `created_by` and
       the title's first 22 characters, plus whether it carries `draft_commentary` and `report_ref` (names only).
    5. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r12_tk1/R12_TEST_TICKET_20261012.json` with keys `ticket_id`,
       `http_status`, `write_set` (exactly one entry, `ticket:<id>`), `deleted` (false), `token_printed` (false), `claim`
       (`measured`), plus the pre-read and read-back values. No address in the file.
    6. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the ticket id FIRST. The issuer relays the id to `2.0.0_SA_COO~Y2` and
       `2.0.0_SA_COO~T2`; you send it to no one else.
  </go>

  <bounds>
    BLAST RADIUS: one new item in `opal-tickets` (key = the id the service issues), the existing distribution-list notice, and the
    result file. ROLLBACK per key: none by this seat. A ticket has no delete route; a delete is a human act, the ruling forbids it
    here, and the item is a labelled test in tenant cottonwood whose routing is the board's own. Nothing else is written: no other
    table, no S3 object, no IAM, no secret, no function code, no environment variable, no ledger entry (this is a data write, not a
    deploy). Not touched: the earlier test tickets, every other tenant, the draft route, the request intake, any outside model.
    One create call in total. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R12-tk-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R12_CHECKS/r12_tk1_ticket.py</invocation><expect>TK1-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the result file does not exist). The check also fails if the id is one of the two earlier
test tickets, if the write set names anything but the one ticket, if the file holds an address, or if a live re-read of the id
differs on type, status, creator, tenant or title prefix.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the secret read is the grant this seat's agent user already holds).
comp-adversary: the control is the check's independent live re-read of the ticket by id, and the single-call, no-retry bound.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R12-tk-1): one ticket created through the existing route under the CTO's ruling; not a worker cell (the act reads a credential).
</task_order>
