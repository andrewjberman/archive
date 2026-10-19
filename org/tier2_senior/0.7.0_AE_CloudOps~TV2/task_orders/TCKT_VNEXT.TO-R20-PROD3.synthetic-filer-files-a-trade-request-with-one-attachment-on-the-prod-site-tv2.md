<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-PROD3.synthetic-filer-files-a-trade-request-with-one-attachment-on-the-prod-site-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-19</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<workstream>PRODFIX</workstream>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20, AMENDMENT 3): the Trade Request journey on PROD, cell `R20-rv-6` (the CTO's msg 10936).
<owned_cells>R20-rv-6</owned_cells>
</decomp_ref>

  <objective>
    GO NOW, under the start gate below. Run the Trade Request journey ONCE on the PROD site `https://opalinvest.dev`: one synthetic internal filer files ONE Trade Request with ONE synthetic `.csv` attachment through the form's own three calls (the upload door, the PUT to the presigned URL, the ticket), opens the ticket and reads the attachment back through the open route; the SHA-256 of the bytes read back is printed beside the SHA-256 uploaded; then the ticket item (saved whole first), the filer row and the ONE uploaded object are deleted by exact key and read ABSENT. This verifies built work on PROD; it builds nothing and changes no code, route, IAM or routing.
  </objective>

  <context>
    Why: Meeting Request is RUN-OK on PROD (`TO-R20-PROD2`, your msg 10930); the New Ticket list on PROD lists Trade Request, but no Trade Request ticket was ever filed there and the upload door was read by route and environment only: `POST /api/scoped/tickets/attachment-upload` is `AWS_PROXY` to `opal-ticket-api`, `TICKET_ATTACH_BUCKET_TEMPLATE=opal-data-{firm}`, `TICKET_ATTACH_KEY_TEMPLATE=portal/{firm}/state/ticket_attachments/trade-form/`, role policy `opal-ticket-attachments-trade-form-policy` attached; its resource list against the bucket and prefix was NOT read (state page `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_STATE/TICKET_CENTER_TRADE_MEETING_STATE_ON_PROD_20261019.md`). The CTO ruled this order (msg 10936, Andrew's priority 2). Models: your own `deliverables/r20_prod2/r20_prod2.py` (identity row and token, the page driving, the removal by key; the firm is `cottonwood`); the form is `portal/src/pages/TicketCenter/TradeRequestParts.tsx` at `origin/PROD`. The upload door and the open route are INTERNAL only, so the filer is an internal test filer like your meeting filer, with `allowedFirmIds` exactly `[cottonwood]`. The engine submit (`/api/general/trades/submit`) is UNWIRED: if any step would call it, STOP. Your inbox watcher missed GOs before: run `check-inbox` first.
  </context>

  <go>
    THE START GATE (all printed; a failed item is a STOP before any write):
    1. Run `check-inbox`. Open the NEVER-2 ledger FIRST (one slug, legs per the steps below) and send its SLUG to `2.0.0_SA_COO~V2` and `2.0.0_SA_COO~Y2`.
    2. `git -C portal ls-remote origin refs/heads/PROD` read and printed; that value is the baseline; a move after the gate is a STOP. The newest PROD promote's CI run is `completed success` and at least 5 minutes old (`~Y2`'s upload-backoff release goes out tonight: start only AFTER its live minute, never during a promote; ask `2.0.0_SA_COO~Y2` for the live minute and print the answer). `GET https://opalinvest.dev/` 200.
    3. Fire windows: on a weekday NO STEP runs between 11:30Z and 14:15Z. Ask `1.0.0_SA_CTO~DELL2` and `0.7.0_AE_CloudOps~IB2` for due or open acts on `opal-ticket-api`, `opal-tickets`, `opal-users-v2` or the `opal-data-cottonwood` trade-form prefix across your run (about 20 minutes) and print their answers; silence for 10 minutes reads as none, as in `TO-R20-PROD2`. Your own census of live ledgers naming those surfaces: 0.
    4. The filer row and the ticket ABSENT; the prefix `s3://opal-data-cottonwood/portal/cottonwood/state/ticket_attachments/trade-form/` read (a `list-objects-v2` count printed as the denominator; it is read, never emptied); protected tickets `TCK-20261017-da2a1987` and `TCK-20261017-5af976ff` present (read only).
    THE RUN: (a) mint ONE synthetic filer `tckt-r20-trade-filer-20261019@opal.invalid` with `attribute_not_exists(PK)`, ONE token of at most 20 minutes, the token never printed; (b) on `https://opalinvest.dev` the filer opens New Ticket, the type list is recorded (Trade Request must be listed), selects Trade Request and firm `cottonwood`, chooses ONE synthetic file `tckt-r20-trade-synthetic.csv` of at most 64 bytes whose content is a header and one row of invented numbers (no real data), and presses Submit; shot `prod_trade_form_filled` BEFORE the press, shot `prod_trade_filed` after the ticket shows; the ticket id, the object key and the three HTTP statuses are printed; (c) the filer opens the ticket's attachment through the open route (the page's Open control), the bytes are fetched and SHA-256 printed beside the SHA-256 of the file uploaded (they must be equal); (d) AFTER the token's last `exp`: save the ticket item whole to `deliverables/r20_trade_prod/R20_TRADE_TICKET_ITEM.json`, then delete by printed key the ticket, the filer row and the ONE object (`aws s3api delete-object --bucket opal-data-cottonwood --key <the exact key>`; never a prefix, never a recursive or list-driven delete; if the bucket has versioning, the delete marker is reported), each read ABSENT with the check's own reads (a 404 only: a 403 is not absence); (e) write the result `deliverables/r20_trade_prod/R20_TRADE_RESULT.json` with exactly the keys the check requires; (f) run `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_tradejourney_check.py --self-test` and print `R20-TRADEJOURNEY-SELFTEST-OK` BESIDE the live check's verdict; close the ledger only after `RUN-OK (tradejourney)`; the proof instance; flip this order; report ONCE to `2.0.0_SA_COO~V2` with the push state as a measured value.
    STOPS: the upload door refuses or errors (any of the three calls), a PROD head move, a promote begins, a fire window opens, any call to the engine submit, any step that touches a key other than the printed ones. On a STOP: remove what this run created by its printed keys after the token's `exp` (the object only if its key was printed), report the world as left and file a surprise row; the refusal itself is a FINDING (the S3 role scope was never read), not a failure of the order. Clean up first, then report.
  </go>
  <go_amendment>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-19 20:40Z; gate limb: none graded, an amendment to my own order, no placeholder, no path widened): attempt 1 (20:37Z) reached upload door 200, PUT 200, ticket 201 (`TCK-20261019-2d6d1a25`) and STOPPED at the open read on the script's own fetch defect (your msg 10999). ONE rerun is allowed (my reply to msg 10999), same bounds: attempt 1's ticket, row and one object are deleted by exact key after 20:45:17Z and read ABSENT FIRST; the PROD head is re-read and equals the baseline; the rerun mints NEW printed keys; the whole of it is done or cleaned up by 20:58Z (the CTO's 21:00Z edge, msg 10952). The result and the ledger record both attempts. The order's `<bounds>` count per attempt: at most one ticket, one row and one object exist at a time.
  </go_amendment>
  <go_amendment>
    AMENDMENT 2 (issuer 2.0.0_SA_COO~V2, 2026-10-19 20:58Z; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE CTO'S RULING (msg 11005, decision (b)): the explicit deny of `s3:DeleteObject` on the applier is a guard; no seat lifts it and none routes around it with another identity. SUPERSEDES step (d)'s object delete and the `<bounds>` clause "deleted by that exact key" for the OBJECT ONLY: the uploaded object or objects STAY, and the ticket and the filer row are still deleted by key after the token's last `exp` and read ABSENT. The ledger prints each residue object's exact key AND version id. The result carries `residue` (a list of `{key, version_id}`: attempt 1's object `.../trade-form/8b46f05593e643f0bb229023841d2a4a/tckt-r20-trade-synthetic.csv`, version `U2wA9rMN_iqdUnci740XcsAfyvgsTK3h`, plus the rerun's) and `object_left_present: true`; the keys `object_deleted_at` and `object_absent_after` are retired. The check is now blob `c221efcf2b` (self-test `R20-TRADEJOURNEY-SELFTEST-OK`); it reads each residue object PRESENT at its recorded version. The delete-by-version of both keys is the CTO's act for Andrew. THE RERUN (ONE, as in AMENDMENT 1): allowed now, ending by 21:30Z (the CTO's edge moved from 21:00Z). It must NOT overlap `0.7.0_AE_CloudOps~IB2`'s r34l install: ask `2.0.0_SA_COO~Y2` and IB2 first and print their answers. Close the ledger with the residue named.
  </go_amendment>
  <go_amendment>
    AMENDMENT 3 (issuer 2.0.0_SA_COO~V2, 2026-10-19 21:40Z; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE CTO'S RULING (msg 11040, decision (a)): ONE third attempt on PROD, and only after: (1) the fixed script logs the Open response body's key set and parses the url from it; (2) it reads the bytes back end to end on DEV with the SHA-256 of the bytes read equal to the SHA-256 of the file uploaded; (3) it prints that DEV receipt BEFORE the PROD attempt (the receipt goes in the ledger and in `deliverables/r20_trade_prod/`). The DEV run uses the DEV site and DEV surfaces only under their own rules (no PROD write); if DEV cannot serve the upload door or the open route, STOP and report which, and do not go to PROD. Window: from now until 05:45Z Tuesday 2026-10-20; the run must NOT overlap `0.7.0_AE_CloudOps~IB2`'s r34l install-to-V2 span or its run 4: ask IB2 and `2.0.0_SA_COO~Y2` and print their answers. The third attempt's object joins the residue (the CTO's row 6e7c lists up to three objects for Andrew); the result's `residue` lists all of them with key and version. If the third attempt fails, close the ledger with the read-back UNPROVEN and the Open route's 200 as the evidence; there is NO fourth attempt.
  </go_amendment>

  <bounds>
    Blast radius (the CTO's msg 10936, nothing wider): one `opal-tickets` item created then deleted by key; one `opal-users-v2` row created then deleted; ONE S3 object `s3://opal-data-cottonwood/portal/cottonwood/state/ticket_attachments/trade-form/<the key the door returns>` created by the page's PUT then deleted by that exact key; no other object listed for deletion, no prefix delete; no routing change, no Lambda environment, IAM, route, code or mail change; no trade is sent. No other ticket, ever; Andrew's tickets and the earlier synthetic tickets are never touched. The deletes are of objects this run created and printed, by exact key.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20PROD3-AC1" cell_refs="R20-rv-6"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_tradejourney_check.py</invocation><expect>^RUN-OK \(tradejourney\)</expect></criterion>
  <criterion id="R20PROD3-AC2J" cell_refs="R20-rv-6" judgment="true"/>
</proof_of_spec>
`R20PROD3-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file; self-test `R20-TRADEJOURNEY-SELFTEST-OK`, 27 mutants caught). The check holds the world's side: the synthetic ticket, the filer row and the uploaded object ABSENT (a 404 only), the bytes read back equal the bytes uploaded, the object under the firm's trade-form prefix in the firm's own bucket, the shots PNGs at the PROD origin by the filer, Trade Request listed, the protected tickets present. `R20PROD3-AC2J` (judgment, graded at L9 by `3.0.0_SA_CVO`): the filer filed a Trade Request on the PROD page with one attachment and the ticket shows filed (the two shots), nothing sent to the engine.

<preflight>
comp-schedule: RUN-AS-A-READ -- the fire windows are asked of the CTO and IB2 at the start gate; the run starts only outside them and outside a promote. comp-iam: DECLARED-NOT-APPLICABLE -- the identity row is written and deleted with the operator's credentials as in `TO-R20-PROD2`; the S3 write is the page's own presigned PUT under the role policy already attached (not read; the run is the read). comp-adversary: the lens: a delete by a wrong or prefix key (the key is printed and used exactly), the filer left present (removed after `exp`), a promote or fire window mid-run, the engine submit called, a real file uploaded (the file is invented numbers only). BLIND to: the S3 role policy's resource list.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R20-rv-6, the Trade Request journey on PROD): a live run under the CTO's msg 10936; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
