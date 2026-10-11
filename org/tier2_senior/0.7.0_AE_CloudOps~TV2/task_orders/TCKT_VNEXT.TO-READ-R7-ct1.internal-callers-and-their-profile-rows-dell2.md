<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-READ-R7-ct1.internal-callers-and-their-profile-rows-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>7</round>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R7.md</decomp_doc> (round 7): cell `R7-ct-1`, the count the release's pair must hold before any apply.
<owned_cells>R7-ct-1</owned_cells>
</decomp_ref>

  <objective>
    ONE READ, nothing written to AWS: find every caller the ticket service would class INTERNAL and say, for each, how many
    users PROFILE rows the service's own lookup finds for it. A release is being built that REFUSES an internal caller with no
    PROFILE row; this read names, before that release, everyone and everything it would lock out.
  </objective>

  <context>
    The contract: PRD `org/missions/D7/TCKT/TCKT_VNEXT/prd/TCKT_VNEXT_PRD.md` v0.4, ADDENDUM 3 (line 226 on), signed by
    `3.0.0_SA_CVO` @b667a5fb11: "The release's pair reads, counts only, that every active internal user has exactly one PROFILE row
    found by the index the service uses; a staff member that read would lock out is named to this seat before the apply." And the
    CTO's word (msg in its IRPT_DASHBD note, 23:24Z): the pair "lists every caller classed INTERNAL with no PROFILE row, people and
    non-human identities alike, before the apply."
    How the service decides (`infra/aws/lambda/ticket_center/lambda_function.py` at HEAD): a caller is INTERNAL when it is not a
    service subject and its `firmId` is `opal-capital` (`principal_class`, lines 312-330). Its scope lookup is
    `_profile_scope` (360-391): a query of the users table's EMAIL INDEX (`USERS_EMAIL_INDEX`, default `email-index`) for the
    caller's lower-cased email, keeping items whose `SK` is `PROFILE`. More than one such item is a refusal today; none will be
    a refusal after the release.
    This is a read. It is not a deploy: open NO deploy ledger entry. Read `/cloud-ops` first.
    **People's addresses are not client data, but they are people's. NO email address is written to any tracked file. Tracked
    files carry counts and a 12-hex digest of each address (sha256 of the stripped, lower-cased address, first 12 hex). The
    addresses of callers with no row, or more than one, go ONLY in your message to `2.0.0_SA_COO~V2`, who names them to the CTO.**
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. THE POPULATION, from two sources, each with its denominator:
       - (a) the users table `opal-users-v2`: every PROFILE item whose `firmId` is `opal-capital`. Use a paginated scan with a
         filter and a projection of `PK`, `SK`, `email`, `firmId`, `status`, `userType` and whether `allowedFirmIds` is present,
         its type and its LENGTH (never its values). Auto-paginate and count client-side; print items scanned and items kept.
       - (b) the ticket table `opal-tickets` (27 items at the last read): every distinct address that appears as `created_by`,
         `assignee`, `claimed_by`, or as an event's actor, with the events' principal class if the row carries it. Drop the
         service subjects (`svc-...`) and count them separately. These are callers who have actually used the service.
    2. FOR EACH distinct address of (a) and (b) that the service would class INTERNAL: run the service's own lookup, a query of
       the email index for the lower-cased address, and count the items whose `SK` is `PROFILE`. Record the count: 0, 1, or more.
       Also record, for count 1, whether `allowedFirmIds` is ABSENT, an EMPTY list, a LIST (its length), the string `ALL`, or
       something else; and the row's `status`.
    3. NAME, in your MESSAGE only: every address with count 0 (it would be REFUSED after the release), every address with a count
       above 1 (it is refused today), and every address in (b) that is not a `status active` user in (a). For each say whether it
       reads as a person or a non-human identity, and why you think so (its form; `userType`).
    4. ALSO, counts only: how many rows of (a) have an email whose stored case differs from its lower-cased form, since the
       service looks up the lower-cased address and such a row would not be found.
    5. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_ct1/INTERNAL_CALLERS_AND_PROFILE_ROWS_20261011.json`: the two
       denominators; per address its DIGEST, the source (a, b or both), the row count, the firm-list class and the status; and
       the totals `internal_addresses`, `with_exactly_one_row`, `with_no_row`, `with_more_than_one_row`,
       `stored_case_differs`. No address in the file.
    6. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the totals FIRST, then the names of step 3.
       What this read CANNOT see, say it in the report: a caller who has never touched a ticket and has no users row at all
       (a constructed event, a non-human identity with an Opal firm id that is in neither table).
  </go>

  <bounds>
    Read-only: scans and queries of two tables, with projections. No write, no delete, no update, no token, no invoke of any
    function, no IAM, no ledger entry. No `allowedFirmIds` VALUE and no ticket content leaves the read. No address in a tracked
    file. A surprise is ONE row in `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read
    the file's headings AND its JSON ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R7-ct-1"><invocation>python -c "import json;d=json.load(open('org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_ct1/INTERNAL_CALLERS_AND_PROFILE_ROWS_20261011.json',encoding='utf-8'));t=d.get('totals',{});k={'internal_addresses','with_exactly_one_row','with_no_row','with_more_than_one_row','stored_case_differs'};print('CT1-TOTALS-OK' if k<=set(t) and t['internal_addresses']==t['with_exactly_one_row']+t['with_no_row']+t['with_more_than_one_row'] and '@' not in json.dumps(d) else 'CT1-TOTALS-FAIL')"</invocation><expect>CT1-TOTALS-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the file does not exist). Put the five totals under a top-level key `totals`. The check
also fails if the file contains an `@`: no address may be in it.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one read, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; reads of two tables this seat's identity already reads).
comp-adversary: DECLARED-NOT-APPLICABLE (a read; nothing is applied). The control is the check that the three row counts sum to the population and that no address is in the file.
</preflight>

# pipeline-override: a READ order to the dell2 applier for an issuer cell (R7-ct-1): two table reads, nothing written to AWS; not a worker cell.
</task_order>
