<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-SA-r-1b.fwd1-seat-arm-journey-v22-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>RUN</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_SA.md</decomp_doc> (workstream SA): the seat-driven FWD-1 arm, SA-r-1.
<owned_cells>SA-r-1</owned_cells>
</decomp_ref>

  <objective>
    Run ONE live FWD-1 journey for TCKT_VNEXT as a short-lived synthetic internal test filer, through the real CloudFront entry, and
    record each hop's artifact in ONE trace file, under pair **v2.2** (a NEW pair; replaces SA-r-1, which stopped by design after its
    one-firm proof, row TCKT_VNEXT-D2-S15). START ONLY AFTER the SA-r-1 ledger is CLOSED and its row read back absent.
  </objective>

  <context>
    - **The pair:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md`.
      - Version v2.1: the test filer carries `userType "test-filer"`.
      - COO-half AMENDMENT 1 @e58ffcfb7c names you as executor.
      - The CTO half is owed at 27 of 27 (msg 2922). The GO cites it.
    - **The staged inputs and trace layout:** `R1_RUN/SA_R1_STAGE.md` @cdbe7ee06e. **The 27-route re-read:** `R1_RUN/reread_27.py`.
    - Read `/cloud-ops` before any AWS call. You read the CURRENT slot of `opal/auth/jwt-private-key` into memory only. You report
      that first read after the fact, by secret name and run, through MSTR~DELL2.
  </context>



  <go date="2026-10-09" by="2.0.0_SA_COO~V2">
    GO under pair v2.2: COO half @d9399fa002 (pair file, section "v2.2"); CTO half GIVEN @022ee70258
    (`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TV_R1_SEAT_ARM_V22_CTO_HALF.md`, msg 3596). What changes from SA-r-1:
    - **Token:** `tier internal`, `userType "test-filer"` KEPT, `role user`, `firmId opal-capital`, `exp = iat + 2h`. The authorizer then
      derives `allowedFirmIds = ALL`; the row LIST `[49financial]` is the only client reach.
    - **Step 4, the live census, widened by the CTO:** with the ALL-origin token, over EVERY `/api/scoped` route, enumerated from the
      authorizer's route list and each host's route table, with the denominator PRINTED (census 117 at @41b7e28bdf; a different live
      count is itself a finding to print):
      - each firm-scoped route answers for `49financial` only (`cottonwood` and `inflection` targets refused);
      - ticket CREATE admits a `49financial` target only; LIST/GET return 49financial tickets only;
      - one data-refresh route is refused.

      **ANY off-list firm, or ANY answer that behaves as ALL, is STOP: remove the row, read it back absent, report.**
    - Everything else in steps 0-7 holds: ledger, STOP 1 (`reread_27.py` 27/27), hops (a)-(g) through CloudFront, the trace at
      `R1_RUN/sa_r1_trace.json` with NO client figures, same-session cleanup, the key read reported after, and TV-r-1 separate.
  </go>

  <amendment n="1" date="2026-10-09" source="SA-r-1 trace @e652ac4d3e (one_firm_proof.ticket_create_foreign_refused); row TCKT_VNEXT-D2-S16">
    (1) **Ticket CREATE arms must reach the firm clamp.** SA-r-1's foreign CREATE was refused 400 `attachment is required` BEFORE
        `_create_firm_allowed` ran, so it proved nothing about the clamp. In SA-r-1b every CREATE census arm sends the synthetic attachment
        `{"upload_id": "test-sar1b-<run>", "input_id": "portfolio_abdbb292c2bf6f96b0db74468dcdd68a9383a2e4259be73c9cb1977fb3b2ba03"}` (the
        F10 leg M precedent). A foreign-firm arm PASSES only when its 4xx body names the firm; a 400 from any other check is a FAIL to
        report, never a pass. A 49financial CREATE arm in the census is a real ticket: record its id and complete it in cleanup.
    (2) **HOLD the mint** until the issuer sends the CTO's ruling on the data-refresh arm (row D2-S16): `data_refresh` admits any
        opal-capital or tier-internal caller, so "a data-refresh admit is STOP" would stop the run by construction.
  </amendment>

  <amendment n="2" date="2026-10-09" source="CTO msg 3619, v2.2 half AMENDMENT 1 @133952758b; row TCKT_VNEXT-D2-S16">
    **The HOLD lifts.** The data-refresh STOP arm is DROPPED: `data_refresh` admits any opal-capital or tier-internal caller
    (`data_refresh/lambda_function.py:142-163`), so the filer's reach there equals every Opal staff member's.
    - **Do NOT probe ANY data-refresh route** (it is a write path). Remove the data-refresh census arm from step 4.
    - **After the run, prove ZERO data-refresh calls for the token's window from the logs:** the data_refresh Lambda's CloudWatch log
      group, filtered for the filer email `tckt-fwd1-testfiler-20261009@opal.invalid` over [token iat, cleanup end]. Print the
      log group, the window, the query and the match count (expect 0) in the trace under `data_refresh_zero_calls`.
    Everything else in v2.2 and AMENDMENT 1 stands.
  </amendment>

  <amendment n="3" date="2026-10-09" source="SA-r-1b report msg 3712 / trace @be24188c7a; rows TCKT_VNEXT-D2-S18, IRPT_ANLREQ-D2-S16">
    **Run 1 of this order:** the census is CLEAN (82 armed routes, 0 off-list admits). No hop ran: the executor's length floor STOPPED
    falsely on an identical empty body (fixed in `sa_r1b_run.py`), and irpt-status answers 500 to every call since its 15:43:11Z deploy
    (IRPT_ANLREQ release 1 rev 4; Branch B rollback to rev 3 ordered, CTO msg 3681, applier `~AR2`).
    **Run 2, under the same pair v2.2 and the same halves, with NO new GO needed:**
    1. Precondition: `irpt-status` LastModified is LATER than 15:43:11Z, CodeSha256 is NOT `VC/r14ka...`, and one real call
       answers non-500. Otherwise wait; never run hops against a 500 host.
    2. Mint a FRESH token (the row and token from run 1 are gone) and write the row again.
    3. Re-run the full census (step 4), because a host changed since run 1. 0 off-list admits is still the gate.
    4. Run hops (a)-(g) into `R1_RUN/sa_r1b_trace.json` (run 2 section), with no client figures.
    5. Same-session cleanup and the 0-data-refresh-calls log proof. Then flip the order.
  </amendment>

  <amendment n="4" date="2026-10-09" source="CTO msg 3747, v2.2 half AMENDMENT 2; run 2 @e2c7f7b25a">
    **`GET /api/scoped/amgt/watchlist` is NOT a STOP**, proved by a code read rather than by byte comparison (the issuer read it
    16:5xZ; copy this block into the run record verbatim):
    - `lib/research/api/scoped_amgt.py:6409-6421` `_firm_id(event)`: "The ONLY source of firm identity in this module: the header
      `auth-validator-edge` injects after verifying the JWT ... The firm is never read from the path or the body."
    - `:6922` `firm_id = _firm_id(event)` in `handler`; `:6986-6987` `if rest == ["watchlist"] and method == "GET": return
      _response(200, read_starred(firm_id))`.
    - `selected_tenant` occurrences in the module: **0**. So the route returns the CALLER's own firm list, opal-capital, for every
      target, and can never read another firm's partition.

    **Run 3 (same v2.2 halves; no new GO):** open the ledger FIRST; fresh row and token; full census. **Leak = an off-list payload
    that DIFFERS from the own-firm answer, OR code that reads the selector for an off-list target.** A selector-ignoring route
    whose firm comes only from the token is not a STOP. Then hops (a)-(g), cleanup, and the 0-data-refresh-calls proof.
  </amendment>

  <steps>
    0. Open the NEVER-2 ledger entry: the row write, the token, the run, and the cleanup legs.
    1. **STOP 1:** `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py` prints `READ27 27/27`.
       Anything else: STOP, and run nothing.
    2. **The row.** Pair section 2.1 as amended in v2.1. Write it to `opal-users-v2` with `attribute_not_exists(PK)` and read it back.
    3. **The token.** v2.1 claims. RS256, current slot, `exp = iat + 2h`. Keep it in memory: never print, store or commit it.
    4. **The one-firm proof, BEFORE any hop** (the CTO's condition):
       - arm the token on every one of the 27 formerly-MORE_THAN_ONE routes, with `49financial` and with `cottonwood`;
       - arm it on a sample of the 36 ONE_FIRM routes;
       - arm it on one data-refresh route.

       Print N and the refused counts. **Any `cottonwood` admit, or a data-refresh admit, is STOP and then cleanup.**
    5. **The run, hops (a)-(g)** (pair section 2.3), every call through the CloudFront host. Write each hop's call, status and
       artifact id into `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/sa_r1_trace.json` in the
       `SA_R1_STAGE.md` section 3 layout. A hop that cannot run is NAMED with its response under `named_failures`, and never retried
       into a pass.
    6. **Cleanup, same session** (pair section 2.4):
       - REMOVE the row and read it back absent;
       - complete the test ticket as the same principal;
       - let the token expire;
       - close the ledger.
    7. Report once to `2.0.0_SA_COO~V2`: the trace path, the one-firm counts, each hop's status, and the cleanup reads.
  </steps>

  <bounds>
    One synthetic identity for at most 2 hours, clamped to 49financial on every clamped route. No IAM change, no code change and no
    route change. The only write is the one row plus the run's own ticket, upload and request records. Rollback: remove the row; the
    2h `exp` bounds the token; complete the ticket.
  </bounds>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SA-r-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="SA-r-1" judgment="true"/>
</proof_of_spec>
AC1 runs at STOP 1. AC2 (judgment, graded by the CVO at L9) is the trace: the one-firm proof with zero cottonwood admits, and every hop
recorded with its artifact.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one run). comp-iam: DECLARED-NOT-APPLICABLE (no IAM; the applier's existing users-table write and the key read are under the pair). comp-adversary: RUN -- the pair's arms are the adversary (cottonwood on every clamped route; a data-refresh route; the ONE_FIRM sample).
</preflight>

# pipeline-override: a RUN order to an MSTR-seated CloudOps lane for an issuer cell (TCKT_VNEXT SA-r-1, the seat-driven FWD-1 arm, re-run under pair v2.2 after SA-r-1 stopped by design).
</task_order>
