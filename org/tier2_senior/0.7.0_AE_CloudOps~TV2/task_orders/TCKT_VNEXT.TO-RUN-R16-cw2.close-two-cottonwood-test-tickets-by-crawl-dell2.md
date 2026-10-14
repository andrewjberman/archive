<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-R16-cw2.close-two-cottonwood-test-tickets-by-crawl-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-13</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>16</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R16.md</decomp_doc> (round 16): cell `R16-cw-2`, one crawl sitting for two test tickets.
<owned_cells>R16-cw-2</owned_cells>
</decomp_ref>

  <objective>
    Close two test tickets, `TCK-20261009-a1052909` and `TCK-20261012-13cd3a1d`, by CLAIM then COMPLETE pressed on the Ticket Center
    board in a browser on portal DEV, signed in as ONE synthetic internal identity that exists for this sitting only, then remove
    the identity. Authority is Andrew's card 7 ("Yes do it"), under a never-widen pair both halves of which are SIGNED.
  </objective>

  <context>
    **The pair is your whole procedure; read it first, in this order:**
    1. `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_CW1_CRAWL_PAIR.md`: sections 2 to 4 are the identity, the
       steps 0 to 7 and the blast radius; its COO-half AMENDMENT 1 (end of file) adds the second ticket, fixes the identity's address
       as `tckt-r2-crawler-20261013@opal.invalid`, and says what "both branches" means per ticket.
    2. `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R2_CW1_ONE_TICKET_CRAWL_CTO_HALF.md` @4fea908a37:
       section 3 conditions 1 to 6 and AMENDMENT 1. They bind this order as written. The mail branch is read after EACH claim.
    3. The shape the pair narrows, for the mint and the removal METHOD only (not its scope):
       `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md` v2.2 and your own earlier
       mint run under `F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md`.
    The CTO's conditions in one line each: the deployed ticket Lambda is the code read (live CodeSha256 against the tree's build,
    else STOP); CLAIM's trace records one `WE_CLIENT_*` line, and `WE_CLIENT_SENT` is a STOP before COMPLETE with a surprise row and
    the message id to `1.0.0_SA_CTO~DELL2`; the crawler opens the board and the target ticket only, and nothing of any other ticket
    goes into a file, a screenshot or a trace; both tickets' `requester.firm` are read BEFORE the mint and either one not
    `cottonwood` is a STOP returned to this seat; one token of at most 20 minutes for both tickets and a second token is not
    covered; a refused COMPLETE leaves the ticket `in_progress` and nothing writes the table directly.
    **`TCK-20261012-c546fead` is NOT a target and is not opened, read in detail, claimed or completed.** The check reads its
    status only, to prove it is untouched.
    **Nothing sensitive leaves memory:** the signing key and the token are held in memory and the one browser context only; never
    printed, written, committed or put in a trace. The identity's address is a synthetic `.invalid` name and may appear in the
    result file; no other address may. The key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`, as the pair says.
  </context>

  <go date="2026-10-13" by="2.0.0_SA_COO~V2">
    GO. Run the pair's steps 0 to 7, amended, in order. The points where this order adds to or tightens the pair:
    1. STEP 0: open the NEVER-2 ledger entry first and keep it open until the identity row reads ABSENT; print the per-tree
       denominator; an open entry naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` is a STOP.
    2. STEP 1, both tickets: ConsistentRead each; proceed only if it reads `status open`, `assignee` null, `created_by svc-commentary`
       and `requester.firm` `cottonwood`. The deployed-code check (CTO condition 1) runs here, before any write.
    3. STEP 2: ConsistentRead the identity key ABSENT; write the row with `attribute_not_exists(PK)` and `allowedFirmIds`
       `["cottonwood"]`; read it back PRESENT; mint ONE token (`exp` at most 20 minutes after `iat`). Record `iat` and `exp`.
    4. STEP 3, the one-firm proof, before any write, as the pair says.
    5. STEP 4, per ticket in this order, `TCK-20261009-a1052909` then `TCK-20261012-13cd3a1d`: print its prior `status` and
       `assignee`; press the board's claim control; read the one `WE_CLIENT_*` line the claim logged (`WE_CLIENT_SENT` is a STOP);
       print `status` and `assignee`; press the complete control; read the item. If the token's remaining life is under 3 minutes
       before the second ticket's claim, STOP rather than start it.
    6. STEPS 5 and 6: the board read and ConsistentRead of both items (`status completed`, `assignee` the identity's address); the
       zero-call read over `iat` to `exp` with its positive control (a count of 0 streams searched is VOID).
    7. STEP 7: wait until `exp` has passed, then delete the row and read it back ABSENT. Close the ledger entry only after that.
    8. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r16_cw2/R16_CRAWL_RESULT_20261013.json` with the keys `tickets` (the
       two ids), `identity` (the address), `firm_list` (`["cottonwood"]`), `token_exp` and `row_deleted_at` (both UTC ISO text, the
       second later), `row_absent_after` (true), `mail_branch` (an object: each ticket id to its `WE_CLIENT_*` token),
       `zero_call_read` (`streams_searched` and `count`), `token_printed` (false), `claim` (`measured`), plus the prior and later
       status values and the deployed CodeSha256. The file names no other ticket.
    9. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: both tickets' final status FIRST, then the mail tokens and the removal.
       If a STOP fires, report the STOP FIRST with the ticket's state as left; do not retry with a changed method.
  </go>

  <amendment id="1" date="2026-10-13" by="2.0.0_SA_COO~V2">
    AMENDMENT 1 (issuer, after your STOP msg 6920; gate limb: none graded this modification). Sitting 1 STOPPED at step 4 before
    any ticket write. The pair now carries COO-half AMENDMENT 2 @eb63f11d0a and the CTO's half AMENDMENT 2 @02234ccce1, bound to
    pair blob `b172afe6c4` (verified by this seat: `git show eb63f11d0a:<pair> | git hash-object --stdin` reads
    b172afe6c49113f37f37d4d176f1ea259c71c8bc). It authorises ONE second sitting under this same order, and it is final:
    1. Close sitting 1 first, as step 7 says: delete the row after `exp` 13:06:28Z and read it ABSENT. Sitting 2 starts only after that.
    2. Same identity address, same LIST `["cottonwood"]`, same two targets, one token of at most 20 minutes. A second ledger entry
       is not needed if sitting 1's entry is still open; keep it open until the row reads ABSENT after sitting 2.
    3. The only change to your method: wait for sign-in to finish and for the board tab to be present before the first click,
       dry-run against the live page with NO ticket write first. Print what the wait observed.
    4. Before the first CLAIM, re-read both targets: each must be `open` with `assignee` null. Anything else is a STOP.
    5. A STOP in sitting 2 is final for card 7; a third token is not covered. Report it first, with the tickets' state as left.
    The result file for the check is written by sitting 2 (`R16_CRAWL_RESULT_20261013.json`); sitting 1's STOP record stays as it is,
    committed under your deliverables folder.
  </amendment>

  <amendment id="2" date="2026-10-14" by="2.0.0_SA_COO~V2">
    AMENDMENT 2 (issuer; gate limb: none graded this modification; it adds no placeholder). The sitting stands as done and graded.
    The record is stale: your proof_of_spec.json reads AC1 FAIL, and `round-close-check --project TCKT_VNEXT --round 16` refuses on it
    (PROOF-BAD AC1). The check's two defects are fixed in the issuer's file: an absent item printed nothing and broke the parse
    (@12ba66c52b), and the card-1 clause read `open`, which is a state, so a staff filing that completed `TCK-20261012-c546fead`
    broke it (@6ab1df0771). The clause now fails only when that ticket is missing or its assignee is the crawl identity. The prose
    "or the card-1 ticket not `open`" in the AC1 note above is replaced by that clause. One act, read-only against the world:
    1. Run AC1 as written, `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R16_CHECKS/r16_cw2_close.py`, and keep
       the printed line verbatim.
    2. In the one file `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/TCKT_VNEXT.TO-RUN-R16-cw2.close-two-cottonwood-test-tickets-by-crawl-dell2.proof_of_spec.json`
       set AC1 `output_evidence` to that line, `status` to what it proves, and `status_reason` to the two fixes above by hash; leave
       the first FAIL run's text in `status_reason` as history. Update the `r16_cw2_close.py (AC1)` row of `compiler_tools` the same way.
    3. Commit, then set `<status>complete</status>` again. No ticket, row, table, secret, code or ledger write; no browser; no token.
  </amendment>

  <bounds>
    BLAST RADIUS: exactly the pair's section 4 plus AMENDMENT 1 point 6: items `TCK-20261009-a1052909` and `TCK-20261012-13cd3a1d`
    in `opal-tickets` (status, assignee, two events rows each); the `opal-users-v2` row for the identity, created then deleted; the
    distribution of one refused SES attempt per claim (read, not assumed). ROLLBACK per key: none by this seat for the tickets (a
    ticket has no un-claim route; a refused COMPLETE leaves `in_progress`, accepted); the row by delete and a ConsistentRead ABSENT.
    Nothing else is written: no other ticket, route, table, secret, IAM, code or Terraform change; no CREATE, REPORT, PACKAGE or upload;
    no write to any record by a direct table call. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON ids
    for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R16-cw-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R16_CHECKS/r16_cw2_close.py</invocation><expect>CW2-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the result file does not exist). The check also fails if the result names the card-1 ticket
or any address but the identity's, if the firm list is not exactly `["cottonwood"]`, if the row was not deleted after `exp`, if
a mail token is `WE_CLIENT_SENT`, if the zero-call read searched no stream or counted a call, or if a live re-read finds either
ticket not `completed` under the identity, the identity row PRESENT, or the card-1 ticket not `open`.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the key read and row write are grants the agent user already holds, reported after the fact).
comp-adversary: the control is the check's independent live re-read of both tickets, the identity row and the card-1 ticket, and the pair's STOP conditions.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R16-cw-2): one crawl sitting under a signed never-widen pair; not a worker cell (the act reads a signing key and drives a signed-in browser).
</task_order>
