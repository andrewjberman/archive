<task_order>
  <metadata>
    <id>TRSB_PATHFIX.TO-3.ae-ses-alyssa-verify</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_implementer>Andrew (production-access form — account-root action only)</co_implementer>
    <date>2026-04-27</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: all 9 spec emails (austin/adam/yang/lauren/menachem/manav/aj/andrew/alyssa @opalinvest.com) returning VerificationStatus=Success in SES. SES still sandbox (ProductionAccessEnabled=false). AE actions complete. Pending non-AE: Andrew submits production-access form via AWS console using packet at infra/aws/ses/trade-pipeline-prod-access-request.md. Sandbox + 9-verified is acceptable interim per PRD §3 W3 (BROKERAGE_EMAILS override routes to andrew@). -->
    <project_code>TRSB_PATHFIX</project_code>
    <wave>W3 — SES unblock (can ship parallel with W2 after W1)</wave>
    <prd_ref>docs/architecture/TRSB_PATHFIX_PRD.md §3 W3 (2026-04-27)</prd_ref>
    <effort>30 min AE + Andrew action (form submission)</effort>
    <gates_on>TRSB_PATHFIX.TO-1 COMPLETE (W1 must ship first per PRD; W3 can run
    in parallel with W2 after W1 RAVC4)</gates_on>
    <tag>None (SES is operational, not infra-as-code in current state; TF
    coverage via TRSB_TFIMPT.W2)</tag>
  </metadata>

  <objective>
    Two gaps preventing Alyssa from receiving ANY trade emails:
    (1) alyssa@opalinvest.com is NOT a verified SES email identity — sandbox-mode SES
        will not deliver to any unverified address.
    (2) SES is still in sandbox (ProductionAccessEnabled: false) — external brokerage
        addresses cannot receive emails until production access is granted.

    Unblock: verify Alyssa same-session (AE action). Submit production-access form today
    (Andrew action). W3 is complete when Alyssa is verified and Andrew has submitted or
    confirmed submission of the production-access request.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - aws sesv2 get-account (capture sandbox status + send quota baseline)
      - aws ses list-identities --identity-type EmailAddress (confirm 8/9 spec members
        verified; expect alyssa@opalinvest.com missing)
      - aws ses get-identity-verification-attributes --identities
        austin@opalinvest.com adam@opalinvest.com yang@opalinvest.com
        lauren@opalinvest.com menachem@opalinvest.com manav@opalinvest.com
        aj@opalinvest.com andrew@opalinvest.com alyssa@opalinvest.com
        (full audit of spec members)
      - Read infra/aws/ses/trade-pipeline-prod-access-request.md (production-access
        packet from TRSB_TFIMPT.W2 — confirm it exists and is complete)
    </phase_1_before_write>
    <phase_2_after_verify>
      - aws ses verify-email-identity --email-address alyssa@opalinvest.com (issue
        verification request; AWS sends link to alyssa — she must click it)
      - aws ses get-identity-verification-attributes --identities alyssa@opalinvest.com
        (poll until Success — may take minutes to hours pending Alyssa clicking link)
      - Andrew action: submit production-access form via AWS console using packet at
        infra/aws/ses/trade-pipeline-prod-access-request.md. Document submission
        ticket number + date in session log. (Agent cannot perform this — account-root
        action only.)
    </phase_2_after_verify>
    <phase_3_after_complete>
      - aws sesv2 get-account (post-Andrew-submission; expect ProductionAccessEnabled:
        true within 1-3 business days OR documented decision to stay in sandbox)
      - End-to-end: after Alyssa's verification link clicked + W2 DDB row added —
        submit a test trade, verify CloudWatch shows SES delivery attempt to
        alyssa@opalinvest.com (trade-submission-handler logs).
      - Append to org/compiler-tools-log.md
    </phase_3_after_complete>
  </compiler_tools_mandate>

  <scope>
    AE actions:
    1. Run aws ses verify-email-identity --email-address alyssa@opalinvest.com.
    2. Confirm verification link sent; note in session log that Alyssa must click it.
    3. Poll aws ses get-identity-verification-attributes until Success (or confirm
       Alyssa clicked; do not block W3 RAVC4 on this if Alyssa is slow — document
       the pending status as the only open item).
    4. Confirm infra/aws/ses/trade-pipeline-prod-access-request.md is ready.
    5. Flag to Andrew: "submit this form today" with exact console path and packet ref.

    Andrew actions (cannot be delegated to agent):
    1. Submit the SES production-access form via AWS console using the packet at
       infra/aws/ses/trade-pipeline-prod-access-request.md.
    2. Document the submission ticket number + date. Share with AE for session log.
    3. AWS approves in 1-3 business days. No agent action until approval.

    Sandbox interim state (if Andrew chooses to defer production-access):
    - All 9 spec members individually verified: this IS sufficient for internal
      trade workflow emails.
    - Brokerage emails currently route to andrew@opalinvest.com anyway
      (config.py:19-24 BROKERAGE_EMAILS override) — so sandbox is acceptable
      until that override is removed.
    - Document this as deliberate decision in session log if chosen.

    Note from PRD: /api/public/trades/* routes on 7k3ed8px20 have AuthorizationType: NONE.
    This is a defense-in-depth gap. Out of scope for this TO. Flag for follow-up:
    TRSB_CLEANUP TO to either (a) upgrade to CUSTOM or (b) delete after confirming zero
    consumers. Do not fix in W3.
  </scope>

  <acceptance_criteria>
    1. aws ses get-identity-verification-attributes --identities alyssa@opalinvest.com
       returns Success (Alyssa has clicked the verification link).
    2. EITHER: aws sesv2 get-account returns ProductionAccessEnabled: true (post-AWS
       approval, 1-3 business days) OR: documented decision-rationale in session log
       that sandbox + all-9-verified is the deliberate intermediate state.
    3. Andrew has confirmed he submitted (or will submit today) the production-access form
       at infra/aws/ses/trade-pipeline-prod-access-request.md. Ticket number + date
       documented in session log.
    4. End-to-end CloudWatch evidence: after W2 DDB adds Alyssa's row + Alyssa verifies —
       a test trade submission triggers SES delivery attempt to alyssa@opalinvest.com
       visible in trade-submission-handler CloudWatch logs.
    5. No tag required for W3 (SES operations, not infra-as-code in this state).
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT try to submit the AWS production-access form on Andrew's behalf — it is
    an account-root console action that only Andrew can perform.</rule>
    <rule>Do NOT block RAVC4 waiting for AWS production-access approval (1-3 business
    days). RAVC4 fires when AE actions complete + Andrew confirms submission.</rule>
    <rule>Do NOT touch the /api/public/trades/* NONE authorization issue in this TO —
    that is a TRSB_CLEANUP follow-up.</rule>
    <rule>Do NOT remove the orphan API w8jnzvs21g — flagged for a separate cleanup TO
    after 30 days of zero CloudWatch traffic confirmation.</rule>
  </do_not>

  <deliverables>
    <deliverable type="infrastructure">alyssa@opalinvest.com SES verified identity</deliverable>
    <deliverable type="document">Session log with: pre-state audit, verify-email-identity
    output, Alyssa verification status, Andrew production-access submission confirmation
    (ticket + date or documented deferral decision)</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC4 outputs.
    AC2 may be pending AWS approval — document status at time of RAVC4.</deliverable>
  </deliverables>
</task_order>
