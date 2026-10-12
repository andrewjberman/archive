<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-READ-R9-ct1.active-internal-rows-by-domain-and-the-twin-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>9</round>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R9.md</decomp_doc> (round 9): cell `R9-ct-1`, the count the CTO wants before any pair is put, and the candidates for the served twin.
<owned_cells>R9-ct-1</owned_cells>
</decomp_ref>

  <objective>
    ONE READ of the users table, numbers only, nothing written to AWS: (1) how many ACTIVE PROFILE rows carry the internal firm id
    `opal-capital` and an address on a domain that is NOT Opal's; (2) which ACTIVE internal rows are NON-HUMAN, re-read by form,
    as candidates for the served twin of the next release's proof; (3) sign-in's status test printed from its source lines.
  </objective>

  <context>
    Authority: PRD `org/missions/D7/TCKT/TCKT_VNEXT/prd/TCKT_VNEXT_PRD.md` v0.4 ADDENDUM 4 @fc2100e1e2, signed by `3.0.0_SA_CVO`
    @1fc5ceaef5; the CTO's msgs 6236 ("one count first, numbers only: ACTIVE rows carrying the internal firm id whose address is on
    a domain that is not Opal's ... an active one is an outsider classed internal estate-wide") and 6240 ("the count ... is back,
    and in the packet, before the release. A non-zero count comes to me before any pair is put"; and the packet "names sign-in's
    test by file and line ... quotes the comparison as printed from those lines").
    Your own reads this builds on: round 7's count (`deliverables/r7_ct1/`, 23 internal rows, 21 active, 2 disabled) and round 8's
    read (`deliverables/r8_ds1/`, 56 PROFILE rows: active 54, disabled 2). **Round 7's `reads_as` was made by a domain test you
    have since found wrong for one row; it is NOT reused here: every class below is re-read by form.**
    This is a read. It is not a deploy: open NO deploy ledger entry. No function is invoked and no sign-in is attempted.
    **No email address in any tracked file: digests only (sha256 of the stripped, lower-cased address, first 12 hex). A DOMAIN is
    not an address and IS written, since the count is by domain. Any address you must name goes ONLY in your message to
    `2.0.0_SA_COO~V2`.**
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. THE COUNT. Over ALL PROFILE items of `opal-users-v2` (auto-paginate, count client-side, print items scanned and PROFILE
       items; 56 expected): keep rows with `firmId` `opal-capital` and `status` exactly `active` (21 expected). Split them by the
       DOMAIN of the address. State FIRST which domains you count as Opal's and why (the domains the workspace itself uses for
       staff and for its own tooling); every other domain is non-Opal. Print each distinct domain with its count; the counts sum
       to the active internal total. A reserved test domain (`.test`, `.invalid`, `.example`) is its own class: say which side
       you put it on and count it separately as well.
    2. FOR EACH active internal row on a NON-OPAL domain: its digest, the domain, `userType`, whether it reads as a person or
       non-human BY FORM (say what in the form decides it), its firm-list class (ABSENT, EMPTY, LIST with its length, other), the
       row's `updatedAt`, and the date of its last event on a ticket or "none". **If the count is not zero, say so FIRST in your
       report: it goes to the CTO before any pair is put.**
    3. THE TWIN CANDIDATES. Every ACTIVE internal row that is NON-HUMAN by form (round 7 classed 4 so; re-read each, and the other
       17 for any it missed): digest, domain, `userType`, what in the form says non-human, firm-list class. A candidate must have
       exactly one PROFILE row, status `active`, and a firm list that is ABSENT or EMPTY (so it reads every firm and the control
       ticket is in scope). Name your FIRST CHOICE by digest and say why. If there is no clean candidate, say so: no person's
       address is ever used as a twin.
    4. SIGN-IN'S TEST, PRINTED. From `infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts` at HEAD, print lines 104-108,
       253-257 and 536-540 into your result file as text, with the file's blob hash (`git rev-parse HEAD:<path>`), and state
       whether the deployed sign-in is still tied to this source as you found it in round 8 (one configuration read; its
       CodeSha256 against the source map's artifact hash).
    5. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_ct1/ACTIVE_INTERNAL_ROWS_BY_DOMAIN_20261012.json`: `opal_domains_used` (a list, with the reason); `denominators`; `domains` (domain to count); `totals` with
       `active_internal_rows`, `on_an_opal_domain`, `on_a_non_opal_domain` (the two summing to the first) and
       `on_a_reserved_test_domain`; `non_opal_rows` (step 2); `twin_candidates` and `twin_first_choice` (step 3);
       `sign_in_test` (step 4); `what_was_not_read`; `claim`. No address in the file.
    6. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the non-Opal count FIRST, then the twin's digest, then the three
       comparisons as printed.
  </go>

  <bounds>
    Read-only: one scan of the users table with a projection, one scan of the ticket table for last-event dates, one
    configuration read, source files. No write, no delete, no update, no invoke, no sign-in, no token, no secret, no IAM, no
    ledger entry. No `allowedFirmIds` VALUE and no ticket content leaves the read. No address in a tracked file. A zero is not an
    absence until a positive control has matched (your row D2-S51). A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R9-ct-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R9_CHECKS/r9_checks.py ct-count</invocation><expect>CT-COUNT-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the file does not exist). The check also fails if the file holds an address or if the two
domain counts do not sum to the active internal total.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one read, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; reads this seat's identity already makes).
comp-adversary: DECLARED-NOT-APPLICABLE (a read; nothing is applied). The control is the sum of the domain counts against the active internal denominator.
</preflight>

# pipeline-override: a READ order to the dell2 applier for an issuer cell (R9-ct-1): two table reads and source lines, nothing written to AWS; not a worker cell.
</task_order>
