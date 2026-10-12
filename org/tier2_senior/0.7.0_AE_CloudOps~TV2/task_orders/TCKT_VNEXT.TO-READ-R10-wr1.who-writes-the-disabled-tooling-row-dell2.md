<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-READ-R10-wr1.who-writes-the-disabled-tooling-row-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>10</round>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R10.md</decomp_doc> (round 10): cell `R10-wr-1`, the one read of your own row TCKT_VNEXT-D2-S54.
<owned_cells>R10-wr-1</owned_cells>
</decomp_ref>

  <objective>
    ONE READ in four parts, nothing written to AWS, nothing enabled and nothing built: what wrote the users row of the DISABLED
    tooling identity (digest `e95c05c7ae90`) at 2026-10-11T22:41:40Z and at 2026-10-12T01:03:31Z. Two readings differ in kind
    and the read must tell them apart: a tool that rewrites its own row on a clock, or a SIGN-IN ATTEMPT as that address that
    updates the row before it is refused.
  </objective>

  <context>
    Authority: the CTO's round-10 analysis
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_TCKT_VNEXT_ROUND_10_20261012.md` @65e5badffb, section 3, and your
    row TCKT_VNEXT-D2-S54. The CTO's word: "A sign-in attempt on a disabled identity comes to this seat the same hour, before any
    sizing."
    What is already read, by you: the row's `updatedAt` was 2026-10-11T22:41:40.809Z at round 8's read and 2026-10-12T01:03:31Z at
    round 9's step 2; its `status` (`disabled`) and `userType` (`Dev`) held; no PROFILE row carries a disabled-date or an audit
    attribute. Sign-in's source is `infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts` (status test at lines 106, 255, 538;
    the deployed function is tied to it by your three reads).
    **A POINTER FROM THE ISSUER, a starting place and NOT a finding (read at 02:1xZ, not exercised):** the workspace holds a
    skill `.claude/skills/ui-walk/` whose `SKILL.md` (lines 29-37) says the UI walker's account sits at `status disabled` at
    rest, that `ui_walker_account.py arm` takes a lease on its row (a conditional write of `armedBy` and `armedAt`) for one
    walk, and that `disarm` returns it. If the identity of digest `e95c05c7ae90` IS that account, an arm and a disarm are two
    writes of its own row by its own tool, and for the length of a walk the row reads ACTIVE. Confirm or refute this from the
    script's code (which attributes `arm` and `disarm` write, and whether they set `updatedAt`) and from the row's own
    attribute NAMES (does it carry `armedBy`, `armedAt` or their traces). Another seat ran a UI walk on this box tonight (the
    CTO's msg 6332 mentions "the walked build"); if a walk's own record gives its arm and disarm times, set them beside the two
    write times. Do NOT run `arm`, `disarm` or `secret`; `status` is a read and may be run once.
    This is a read. It is not a deploy: open NO deploy ledger entry. No function is invoked, no sign-in is attempted, and nothing
    is switched on (no stream, no export, no point-in-time setting).
    **No email address in any tracked file or in any printed log line: digests only. No token, no secret, no credential, no
    password-reset or one-time code is read, printed or copied; if a log line you count would carry one, count it and do not
    print it. The row of digest `1af514167abb` (row D2-S53) is not read, named or probed by this order.**
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. THE ROW'S CHANGES. Read the row now: its attribute NAMES and its `updatedAt`. State which attributes can be shown to have
       changed at each of the two writes, by NAME and changed / unchanged / cannot tell, never a value. You hold two earlier
       projections of the row (rounds 8 and 9): say exactly which attributes those projections covered, since an attribute outside
       them cannot be compared. Then say what history the table holds: is a stream enabled, is point-in-time recovery enabled
       (one `describe-table` and one `describe-continuous-backups`); if neither holds the answer, say so. **Enable nothing and
       restore nothing.**
    2. THE WRITERS, FROM CODE. Every place in the workspace that writes a PROFILE item of `opal-users-v2` (a put, an update, a
       transact or batch write): the function or script, the path and line, which attributes it writes, and whether it sets
       `updatedAt`. For the sign-in handler say, with lines: does a sign-in ATTEMPT write the row (a last-login stamp, a failure
       counter, a lockout field), and does that write happen BEFORE or AFTER the status test, so that a refused attempt on a
       disabled row would still move `updatedAt`. State the denominator of the search (which folders, how many files matched the
       table's name) so a zero elsewhere is not read as an absence.
    3. SIGN-IN'S ACTIVITY AROUND THE TWO TIMES. For the sign-in function, in the ten minutes centred on each time (five before,
       five after; state the exact start and end you used, in epoch milliseconds and in UTC): the invocation count from the
       metric, and from its log group the count of lines that record a refusal for a disabled account. Use a QUOTED filter
       pattern and run a positive control FIRST that must match (your row D2-S51); print the control's count beside each zero.
       Counts only. Then the same two windows for any other writer step 2 found that is a deployed function.
    4. THE WORKSPACE. One native search (the Grep tool, repo root) for the identity's local part: every file that names it, split
       into code, configuration, schedules and dated records, with the count of each. Say whether any schedule or tool runs as it.
    5. THE VERDICT, one of: `A_TOOL_REWRITES_ITS_OWN_ROW`, `A_SIGN_IN_ATTEMPT_WRITES_THE_ROW`, `ANOTHER_WRITER`, `NOT_DETERMINED`,
       with the evidence that decides it and what would have to be read to move a NOT_DETERMINED.
       **If the verdict is, or may be, a sign-in attempt: say so FIRST in your report; the issuer takes it to the CTO the same
       hour.**
    6. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r10_wr1/WHO_WRITES_THE_DISABLED_TOOLING_ROW_20261012.json` with these top-level keys plus any you need: `row_changes` (step 1), `profile_row_writers` (a list, each
       with `where` as an existing `path` or `path:line`), `sign_in_activity` (step 3, with the windows and the controls),
       `workspace_mentions` (step 4), `verdict`, `what_was_not_read`, `claim` (`measured` or `inferred`). No address in the file.
    7. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the verdict FIRST, then the counts with their controls.
  </go>

  <bounds>
    Read-only: the one row and two table descriptions; source files; metric and log reads of functions with counts only; one
    native search. No write, no delete, no update, no invoke, no sign-in, no token, no secret, no IAM, no ledger entry; no
    stream, export or recovery setting is changed. No address and no credential in any tracked file or printed line. A zero is
    not an absence until a positive control has matched. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R10-wr-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R10_CHECKS/r10_wr1_read.py</invocation><expect>WR1-READ-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the file does not exist). The check also fails if the file holds an address, if the
verdict is outside the closed set of four, or if a writer's path does not exist.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one read, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; reads this seat's identity already makes).
comp-adversary: DECLARED-NOT-APPLICABLE (a read; nothing is applied). The control is the positive control beside every zero and the verdict's closed set.
</preflight>

# pipeline-override: a READ order to the dell2 applier for an issuer cell (R10-wr-1): one row, source files, metric and log counts, nothing written to AWS; not a worker cell.
</task_order>
