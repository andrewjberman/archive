<task_order>
  <metadata>
    <id>ETFS_RIVALS.TO-PREFLIGHT-bbg-signin-20261012</id>
    <issued_by>2.0.0_SA_COO~V1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZV</issued_to>
    <date>2026-10-11</date>
    <status>superseded</status>
    <!-- SUPERSEDED 2026-10-12 by 2.0.0_SA_COO~V1 under the CTO's ruling org/missions/D5/ETFS/ETFS_RIVALS/ledger/CTO_RULING_R28_SITEZ_CARRIERS_SUPERSEDED_20261012.md (msg 4550), which permits it and does not grade it; the CVO adjudicates the closure as JUDGMENT at its compile. SUPERSEDED BY the committed records, each cited by hash on origin/box/sitez (ls-remote read 8e77a84252) and read with git show plus a positive control (a known file reads; an absent path reads no commit): AC1 (judgment: the Terminal was reachable at the pre-flight) graded MET by the issuer @e02a08d95b from the report bytes at commit 956460aeab on origin/box/sitez (`git show 956460aeab:` this file: `STEPS 1-3 ALL PASSED` once; SPY US Equity PX_LAST 778.57 on its line 74). The executor's instance @0f2b83b9cc is VALID in the mission tree. No criterion of this order is site-Z-only: none stays pending. The executor's own proof instance was not written (site Z weekly limit, resets 2026-10-14 06:00Z). -->
    <project_code>ETFS_RIVALS</project_code>
  </metadata>
<direct_act>true</direct_act>
<!-- Round-less by design: a site-bound pre-flight, not a cell. AUTHORITY: 1.0.0_SA_CTO~DELL1 msg 3801 (2026-10-11 11:23Z), "Authorized, per integrations/bloomberg/READ_HERE.md section 2: window 10:20-10:45Z; one metered health draw; sign in ONLY on failure, two-phase ... One submit at most ... Confirm success with a real reference_data read, not the port. No password in any log." Reason: the 2026-10-11 11:00Z fire found the Terminal SIGNED OUT (leg exit 93, enrichment exit 95; transcription @4e3fbbc9f5). It also serves MDPF_SECHIST's Monday pull. -->
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md</decomp_doc> (round 28): the precondition of cell `RIV-tc-1`'s J1 read -- a scheduled run that REACHES the enrichment write needs a signed-in Terminal at 07:00 local on 2026-10-12 (G1 for date=2026-10-09 now exists; rows Z-S79, Z-S81).
<owned_cells>RIV-tc-1</owned_cells>
</decomp_ref>

  <objective>
    Before 10:45Z on 2026-10-12, confirm the site-Z Bloomberg Terminal is signed in and reachable, and sign it in only if it is
    not, so the 11:00Z scheduled pulls can reach Bloomberg. One metered draw.
  </objective>

  <steps>
    Follow `integrations/bloomberg/READ_HERE.md` section 2, in this order, starting no earlier than 10:20Z on 2026-10-12:
    1. `python integrations/bloomberg/auth/bbg_credentials.py --check`.
    2. `bloomberg_health` (not a draw).
    3. ONE `reference_data` read: 1 security x 1 field (SPY US Equity, PX_LAST). This IS a draw: record its security, field and
       time in the report. `2.0.0_SA_COO~Q1` books it on MDPF_DEMQUE as a tier-1 request the same day.
    4. ONLY if step 1, 2 or 3 fails: run `bbg_signin.ps1 -Phase fill` (free, repeatable); verify the screenshot's login and the
       masked password length; then `-Phase submit` ONCE. At most one submit. If it fails, STOP and report: the second budgeted
       attempt is a human's, because the account locks on repeats. After a submit, confirm success with a real `reference_data`
       read (the same one security and field), not the port, and record it as the second draw.
    5. Write this order's proof-of-spec instance in `deliverables/0.7.0_AE_CloudOps~ZV/`, the way you wrote the two instances
       at @876cfb049f (`--governing-order` this file), so the issuer can flip it complete.
  </steps>

  <rules>
    No pull, no vehicle leg, no ad-hoc run of the 11:00Z job, no field beyond the one. No password, no secret value and no
    screenshot of a password field in any log or report (lengths and hashes only, as on 2026-10-09). Write only your
    deliverables folder and this order's report section. If the Terminal is reachable at step 3, no sign-in runs.
  </rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- this act triggers no schedule; it runs before the 11:00Z task and changes nothing about it.
comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- a second submit by a retry loop: step 4 allows one submit, then STOP; a health read taken as a sign-in proof: step 3's draw is the proof, health is not; a sign-in run while signed in: step 4 runs only on a failure; an account lock from repeated submits: one submit and a human for the second. BLIND: whether the session holds from 10:45Z to 11:00Z.
lane: 0.7.0_AE_CloudOps~ZV, the site-Z lane for ETFS_RIVALS's site-bound acts (msg 1664).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="RIV-tc-1" judgment="true"/>
</proof_of_spec>

  <report>
    2026-10-12, executor 0.7.0_AE_CloudOps~ZV: STEPS 1-3 ALL PASSED, SO NO SIGN-IN RAN. ONE metered draw.
    Executed inside the authorized window: started 10:29:33Z, finished 10:30:48Z (window 10:20-10:45Z).

    STEP 1, each step's output line verbatim. `python -I integrations/bloomberg/auth/bbg_credentials.py --check`,
    start 10:29:33.437699Z, end 10:29:34.424598Z, rc=0:
      CREDENTIAL: OK  secret=bloomberg/terminal/login  user_len=12 user_sha256=f713879ee035 pw_len=9 pw_sha256=b52a0db305ea
    Fingerprints only, as the tool and the order require -- no credential value, no screenshot of a password field, no
    secret in this report. THESE FINGERPRINTS ARE IDENTICAL to the 2026-10-09 pre-flight's, which is the point worth
    recording: the 2026-10-11 sign-out was NOT a credential rotation.

    STEP 2 (not a draw). `bloomberg_health`:
      {"ok": true, "endpoint": "127.0.0.1:8194", "service": "//blp/refdata"}
    Read, not cited: this is the same endpoint that printed "session pool state=Failed" 21 times on the 2026-10-11 fire,
    so an ok:true here is discriminating rather than vacuous. Health is NOT the proof; step 3 is.

    STEP 3, THE ONE METERED DRAW. `reference_data` securities=['SPY US Equity'] fields=['PX_LAST'], no overrides and no
    second field. Bracketed 10:30:11.311213Z to 10:30:48.297228Z:
      {"SPY US Equity": {"PX_LAST": 778.57}}
    A real data read returned a real value, which is what the order asks for in place of a port check.

    STEP 4: NOT REACHED AND NOT RUN, because steps 1-3 all passed and the order runs it only on a failure. NO
    `bbg_signin.ps1 -Phase fill`, NO `-Phase submit`, no retry, no pull, no vehicle leg, no ad-hoc run of the 11:00Z job.
    ZERO of the 2-attempt sign-in budget was spent, so the account was never exposed to a lock, and the second budgeted
    attempt remains a human's as the order reserves it.

    DRAW COUNT: 1 (one security x one field x zero overrides), the order's cap, booked tier-1 for 2.0.0_SA_COO~Q1 on
    MDPF_DEMQUE. Whether that booking has been entered is that project's carrier and is not claimed here.

    THE TERMINAL IS SIGNED BACK IN. Yesterday's 11:00Z fire failed on a signed-out Terminal (leg exit 93, enrichment
    exit 95, transcription @4e3fbbc9f5); today it is reachable. This seat did not sign it in and makes no claim about
    who or what did.

    WHAT THIS DOES NOT ESTABLISH, which is the order's own BLIND and the limit that matters most: reachability is proven
    at the measured instant, 10:30Z. Persistence to the 11:00Z fire is NOT claimed. A reading about 10:30Z is a reading
    about 10:30Z, and the 11:00Z run's own log is the only evidence of what the fire found -- that is the separate act
    under TO-TRANSCRIBE-20261011-20261012 date 20261012, owed from 11:15Z.

    PUSH STATE, measured not defaulted: origin/box/sitez read by git ls-remote at 10:3xZ = 6aac3f547c, equal to local HEAD
    before this commit, so this report commit is LOCAL at the moment of writing and rides box-sync. This seat does not
    push box/sitez -- never-rules-gate refuses it to any serial but the integrator. Re-measured at send time in the hash
    relay to 0.0.0_AB_MSTR~Z.

    AC1 (the Terminal was reachable at the pre-flight) is a JUDGMENT criterion and is the issuer's to grade; nothing here
    grades it. Step 5's proof-of-spec instance is written under deliverables/0.7.0_AE_CloudOps~ZV/ and validated with
    --governing-order this file. The status flip is the issuer's.
  </report>
</task_order>
