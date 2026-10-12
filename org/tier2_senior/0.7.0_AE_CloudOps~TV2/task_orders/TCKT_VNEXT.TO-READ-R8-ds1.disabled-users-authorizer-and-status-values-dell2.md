<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-READ-R8-ds1.disabled-users-authorizer-and-status-values-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>8</round>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R8.md</decomp_doc> (round 8): cell `R8-ds-1`, the one read the CTO's contract change on a disabled users row waits on.
<owned_cells>R8-ds-1</owned_cells>
</decomp_ref>

  <objective>
    ONE READ in three parts, nothing written to AWS and nothing built: (1) what the portal's sign-in and authorizer do with a
    DISABLED user, from their code; (2) the two disabled internal users rows, by digest and form; (3) every status value the
    users table holds on a PROFILE row, with counts over all of them. The CTO will write a contract sentence from this that says
    which status values admit a caller to the ticket service and who that locks out.
  </objective>

  <context>
    Authority: the CTO's round-8 analysis
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_TCKT_VNEXT_ROUND_8_20261012.md` @8cccf94651, section 3, and row
    TCKT_VNEXT-D2-S50 (ARMED, owner the CTO): the ticket service's no-row refusal, live since 2026-10-12T00:22:08Z, reads whether
    a users row EXISTS and not its status.
    The issuer's pointers, each a starting place and not a finding:
    - the authorizer's source is `infra/aws/users/lambda/portal-authorizer/index.mjs` (450 lines; the Terraform comment at
      `infra/aws/terraform/portal-auth/lambdas.tf:61-63` names it). The issuer's grep of that file for `status` and `disabled`
      found no line that reads a users row's status: it verifies a token (around lines 376-394) and computes the firm list
      (`computeAllowedFirms`, line 293). A second authorizer sits beside it: `infra/aws/users/lambda/portal-rest-authorizer/index.mjs`.
    - what MINTS the token is not located by the issuer: find the sign-in function from `infra/aws/terraform/portal-auth/lambdas.tf`
      (each function's `# Source:` comment) and read whether it refuses a disabled user, and the token lifetime it sets.
    - your own count of round 7 (`deliverables/r7_ct1/INTERNAL_CALLERS_AND_PROFILE_ROWS_20261011.json` @8d900213a1): 56 PROFILE
      items; 23 internal, of which 2 read `disabled` (digests in that file).
    This is a read. It is not a deploy: open NO deploy ledger entry. No function is invoked and no sign-in is attempted.
    **No email address in any tracked file: digests only (sha256 of the stripped, lower-cased address, first 12 hex). No token,
    no secret, no key is read, printed or copied; a token's lifetime is read from CODE, never from a token.**
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. THE CODE. Read the sign-in function's source and both authorizers' source. Answer, each with path and lines:
       - (a) does sign-in refuse a user whose row is disabled? Which attribute and which values does it read?
       - (b) does a refresh refuse a user disabled since the last sign-in?
       - (c) does either authorizer read the users row's status on a request? If not, a token issued before the disabling keeps
         working until it expires: say so, and give the token lifetime and the refresh lifetime as the code sets them.
       - (d) is the DEPLOYED authorizer this source? One read: the function's CodeSha256 and LastModified beside the build
         artifact's recorded hash if the source map holds one. If you cannot tie them, say NOT TIED; do not download and diff.
       If a source is not in this checkout, say which and stop that limb; it is carried to its owner.
    2. THE TWO DISABLED INTERNAL ROWS, by digest: for each, person or non-human by form and `userType`; the date it was disabled
       if the row carries one (name the attribute; if none, say none); the row's last-updated attribute if any; and the date of
       its last event on a ticket (one scan of `opal-tickets`, 27 items at the last read; dates only), or "none".
    3. THE STATUS VALUES. Over ALL PROFILE items of `opal-users-v2` (56 at your last read; auto-paginate, count client-side,
       print items scanned and PROFILE items): every distinct value of `status`, INCLUDING an absent attribute as its own value,
       with its count; the counts must sum to the PROFILE total. The same split for the internal rows alone (firm
       `opal-capital`). If any other attribute looks like it carries the same meaning (`enabled`, `active`, `disabledAt`,
       `deleted`), name it and count its values too.
    4. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r8_ds1/DISABLED_USERS_READ_20261012.json` with EXACTLY these top-level keys plus any you need: `authorizer` (the answers of step 1, and
       `files_read`, a list of `path` or `path:line` strings that exist), `disabled_internal_rows` (a list, step 2),
       `status_values` (`profile_rows`, an integer, and `counts`, a map of value to count summing to it, plus the internal
       split), `what_was_not_read`, `claim` (`measured` or `inferred`).
    5. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the answer to 1(a) and 1(c) FIRST, then the status counts, then the two
       rows by digest. If either disabled row reads as a PERSON, say so first of all.
  </go>

  <bounds>
    Read-only: source files; scans of two tables with projections; one `get-function-configuration` per function read. No write,
    no delete, no update, no invoke, no sign-in, no token, no secret, no IAM, no ledger entry. No `allowedFirmIds` value and no
    ticket content leaves the read. No address in a tracked file. A zero from a filter is not an absence until a positive
    control has matched (your row D2-S51). A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R8-ds-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R8_CHECKS/r8_ds1_read.py</invocation><expect>DS1-READ-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the file does not exist). The check also fails if the file holds an address, if the
status counts do not sum to `profile_rows`, or if a cited path does not exist.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one read, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; reads this seat's identity already makes).
comp-adversary: DECLARED-NOT-APPLICABLE (a read; nothing is applied). The control is the sum of the status counts against the PROFILE denominator.
</preflight>

# pipeline-override: a READ order to the dell2 applier for an issuer cell (R8-ds-1): source files and two table reads, nothing written to AWS; not a worker cell.
</task_order>
