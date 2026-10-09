<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-SA-r-1.fwd1-seat-arm-journey-tv2</id>
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
    record each hop's artifact in ONE trace file. This order is STAGED: it goes to `pending` only on the issuer's GO, which follows
    (1) `reread_27.py` printing `READ27 27/27` and (2) the CTO half v2.1 being GIVEN against this executor.
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
    GO. Preconditions met: READ27 27/27 rc 0 at 14:5xZ (@af69b2e049; irpt-narrative live 14:48:05Z). CTO half v2.1 GIVEN @85c6dc8fe7
    (`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TV_R1_SEAT_ARM_V21_CTO_HALF.md`, msg 3532). Its conditions bind the run:
    (1) the live one-firm proof (step 4) runs before any hop. If IRPT release 1 rev 4 has landed on irpt-status since 14:5xZ, re-run
        STOP 1 first. A NOT-RELEASED irpt-status is a STOP to report, never a pin to adjust;
    (2) the first read of the signing key is reported after the run;
    (3) the trace records each hop's status and artifact ID only: NO client figures, holdings values or report contents;
    (4) cleanup in the same session;
    (5) TV-r-1 (Alyssa's own filing) stays separate and is not touched.
  </go>

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

# pipeline-override: a RUN order to an MSTR-seated CloudOps lane for an issuer cell (TCKT_VNEXT SA-r-1, the seat-driven FWD-1 arm under pair v2.1); staged until 27/27 and the CTO half.
</task_order>
