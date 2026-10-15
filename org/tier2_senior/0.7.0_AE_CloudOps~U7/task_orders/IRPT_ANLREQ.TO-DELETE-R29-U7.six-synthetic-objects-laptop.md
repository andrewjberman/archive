<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-R29-U7.six-synthetic-objects-laptop</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~U7</issued_to>
    <date>2026-10-15</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the act deletes every version of SIX named synthetic objects (3 original files, 2 normalized inputs, 1 request composition) in the intake store, all written by the release-29 door sitting, none of them client data (cottonwood wrote nothing); nothing reads them (the sitting is done and its record is committed).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN-AS-A-READ -- step 2 asks the policy simulator whether YOUR principal may delete these object versions; no IAM change is made by this order.
comp-adversary: RUN -- by reading the dell2 applier's refusal (an explicit Deny, DenyS3DeletesOnProductionData in cloudops-dell-agent-deploy-policy v7) and the order TO-DELETE-C449-U7 (the same act for one object, done) against this cell; the lens: a delete that matches by prefix or substring and removes more than the six keys, a key typed by hand with a wrong hex digit (so the order does NOT retype any key: it reads the six lines from the pinned list file), a delete tried through another principal after a refusal, a NoSuchKey read taken from a lagging list, a version created between the list and the delete. The order requires the list file's blob hash first, selects each key by EXACT equality (not prefix), prints the version counts before any delete, deletes by VersionId one call per version, and reads back a head-object and an exact-key version list per key. It also says: if your principal is denied, STOP; the act then belongs to Andrew's console and nothing is tried through another principal. NOT seen: whether your principal is denied (step 2 reads it); the live version counts (step 3).
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R24_G.md</decomp_doc> round 24, workstream ~G: the clean-up of the six synthetic objects the release-29 door sitting stored (call dell2-20261014T134418Z-2106), carried across boxes as an ORDER as the c449 delete was.
<owned_cells>AR-g-105</owned_cells>
</decomp_ref>

  <objective>
    Delete EVERY version of the six synthetic objects listed in the pinned file, and nothing else, and read back NoSuchKey for each; or, if your principal is denied by the policy simulator, STOP at step 2 with nothing changed and report the denial. You change no code and apply nothing.
    **The objects:** the six `OBJ` lines of `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/OBJECTS_WRITTEN_R29.txt` (each line: `OBJ <bucket> <key> <VersionId>`; bucket opal-data-irpt, prefix irpt/49financial/state/ for all six: three under original_holdings/, two under normalized_portfolios/, one under request_compositions/). The file is pinned: `git hash-object` prints `b78f52a08c6ca90ff0c285082d54be5114e4d9e1`, sha256 `66be5adadc97612fe92a7dec6c5a6655579eb3bcc294da7b51f4fac257cff95f`, 2153 bytes, `OBJ_COUNT 6`. Read it from this repository by `git show origin/box/dell2:org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/OBJECTS_WRITTEN_R29.txt` (or the working tree once box-sync carries it, commit 5c4b50864d at the latest touch); the VersionId on each line is the version the sitting wrote and the floor of what you will find.
  </objective>

  <context>
    Load /cloud-ops first. **The approval (Andrew, open call dell2-20261014T134418Z-2106):** record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261015_203xZ_A252_TEMPLATE_C02C_DRAFT_TO_DESKTOP_DELETES_2106_53CB_D8AE_APPROVED.md, his words verbatim: "2106 deletes are fine." The record's own table row for 2106: "Delete every version of the 6 synthetic objects listed in `OBJECTS_WRITTEN_R29.txt` (bucket `opal-data-irpt`, prefix `irpt/49financial/state/`). Each version is read before its delete, and the result is read after." The dell2 Dell identities are denied this act on purpose (DenyS3DeletesOnProductionData), so the CTO relays it to a laptop CloudOps seat as this order (1.0.0_SA_CTO laptop msg 109537, carried by 0.0.0_AB_MSTR~DELL2 msgs 8768 and 8770). This approval covers THESE SIX OBJECTS; the release-28 inputs, every other object in the bucket, and the cottonwood tenant are NOT covered. Do NOT look for another principal, a role to assume, a lifecycle rule or a bucket-policy change if yours is denied.
  </context>

  <the_act>
    1. Open the NEVER-2 ledger irpt-r29-delete-u7-20261015 (legs L list, D delete, R read-back) on your box and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming the intake store bucket opal-data-irpt is a STOP.
    2. Read the pinned list file and print its blob hash (it must equal b78f52a08c6ca90ff0c285082d54be5114e4d9e1; any other: STOP, report) and the six keys' last path segments only (the 64-hex leaf and extension) as the denominator. THE SIMULATOR: run simulate-principal-policy for YOUR principal, actions s3:DeleteObjectVersion and s3:DeleteObject, resources arn:aws:s3:::opal-data-irpt/irpt/49financial/state/original_holdings/*, .../normalized_portfolios/* and .../request_compositions/*. Print the decisions and the matched statements. If any decision is not `allowed` (an explicit or an implicit deny): STOP. Delete nothing, write org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_r29/R29_DELETE_RESULT.txt with the single line `DENIED <decision> <matched statement id>`, close your ledger as BLOCKED with that reason, and report ONCE to 2.0.0_SA_COO~G2 and 1.0.0_SA_CTO~DELL2 (the act is then Andrew's console act). Do not try another principal.
    3. READ ONLY, per key: list-object-versions with the Prefix equal to the full key, read whole (print the page count and that the listing was not truncated), and keep only the entries whose Key equals the full key EXACTLY. For each of the six keys print its versions (VersionId, LastModified, size, delete-marker flag) and the counts as denominators. Each key must show at least one version, and its listed VersionId from the file must be among them; any key with zero versions, a missing file VersionId, or an unexpected delete marker: STOP, delete nothing, report what you found (names and counts only). More than one version of a key is allowed (the approval is for every version); print how many.
    4. Delete: for each of the six keys, delete each of its versions by VersionId, ONE call per version (no batch-delete over a prefix, no lifecycle rule, no recursive delete). Print each call's result. Do not touch any other key, version or bucket. If a call is refused, STOP: report what was deleted and what remains, and do not retry through another principal.
    5. Read back, per key: head-object of the key without a VersionId must answer 404/NoSuchKey, and list-object-versions for the exact key (Prefix equal to the full key, keep only the exact match) must return zero versions and zero delete markers; repeat a lagging read in a printed bounded window of 5 minutes. A version still PRESENT after the window is a STOP and a report. Write org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_r29/R29_DELETE_RESULT.txt with ONE line each, exactly: `KEYS_SELECTED 6`, `VERSIONS_BEFORE <n>`, `DELETED <n> OF <n>` (the same n, the number of versions found at step 3), `HEAD NoSuchKey 6`, `VERSIONS_AFTER 0`. No object body, account identifier or name goes into any file, log or message.
    6. Close the ledger and report ONCE to 2.0.0_SA_COO~G2 and 1.0.0_SA_CTO~DELL2 (the path of the result file and its lines). The dell2 CTO closes the open call 2106 with Andrew's record; you do not.
  </the_act>

  <bounds>
    Exactly the versions of the SIX keys in the pinned file, selected by exact key; no other key, version or bucket, no prefix delete, no lifecycle or policy change, no DynamoDB write, no cottonwood object, no release-28 input. Rollback: none is possible once a version is deleted (the objects are synthetic and Andrew approved their removal); a STOP before step 4 changes nothing.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_r29/IRPT_ANLREQ.TO-DELETE-R29-U7.six-synthetic-objects-laptop.proof_of_spec.json`.
    <criterion id="R29U7-AC1" cell_refs="AR-g-105">The result file carries either the five lines of a completed delete or the single denial line.<invocation>grep -c -E '^(KEYS_SELECTED 6|VERSIONS_BEFORE [0-9]+|DELETED ([0-9]+) OF \2|HEAD NoSuchKey 6|VERSIONS_AFTER 0|DENIED .+)$' org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_r29/R29_DELETE_RESULT.txt</invocation><expect>^(5|1)$</expect></criterion>
    <criterion id="R29U7-AC2" cell_refs="AR-g-105">The ledger irpt-r29-delete-u7-20261015 is closed (CLOSED, or BLOCKED on a denial).<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-r29-delete-u7-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* (CLOSED|BLOCKED)</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a delete order to a tier-2 applier on another box under Andrew's recorded approval of call 2106 and the CTO's relay (not a worker cell); the cell AR-g-105 is the issuer's, as for TO-DELETE-C449-U7.
