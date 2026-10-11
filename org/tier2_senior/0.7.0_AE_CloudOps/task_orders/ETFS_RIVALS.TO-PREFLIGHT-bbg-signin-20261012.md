<task_order>
  <metadata>
    <id>ETFS_RIVALS.TO-PREFLIGHT-bbg-signin-20261012</id>
    <issued_by>2.0.0_SA_COO~V1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZV</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
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
    (the executor's report goes here, committed before 10:50Z on 2026-10-12, hash to 0.0.0_AB_MSTR~Z: each step's output line,
    whether a sign-in ran, the draw count with security, field and time, and the measured push state. AC1 -- the Terminal was
    reachable at the pre-flight -- is the issuer's to grade.)
  </report>
</task_order>
