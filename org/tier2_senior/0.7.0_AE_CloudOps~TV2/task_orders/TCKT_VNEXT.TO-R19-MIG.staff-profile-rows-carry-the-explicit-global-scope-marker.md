<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R19-MIG.staff-profile-rows-carry-the-explicit-global-scope-marker</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>19</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R19.md</decomp_doc> (round 19): cell `R19-mg-6`.
<owned_cells>R19-mg-6</owned_cells>
</decomp_ref>

  <objective>
    Write the attribute `scope_all_firms` = BOOL `true` to exactly the active internal PROFILE rows of `opal-users-v2` that carry no `allowedFirmIds`, so the fail-closed
    firm scope of the ticket service (row S134 item 3, `TO-R19-L3`) does not lock them out when it deploys. STAGED: it starts only on the issuer's GO, which names a signed
    never-widen pair, and it runs BEFORE `TO-R19-REL`.
  </objective>

  <context>
    **The pair is your whole procedure.** The issuer writes it after `TO-R19-L3` is merged, at
    `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_MIG/R19_MIG_PAIR.md`, and the CTO signs its half. It names the selection rule, the write, the
    condition, the rollback per row and what is printed. The contract is the decomposition's CONTRACT item 3 and item 6
    (`org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R19.md`). Measured at the cut (read-only, no address read): 23 internal PROFILE rows, 19 active with no
    `allowedFirmIds` (14 with no userType, 5 `Dev`), 1 disabled, 2 with a non-empty list, 1 `service` row whose value is a string. You do NOT start without the GO.
    The selection is read AGAIN at the run (the count may differ from the cut): the pair says what a different count means (a STOP unless the pair names the tolerance).
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair, written by the issuer. Then, in order:
    1. STEP 0: open the NEVER-2 ledger entry; print the per-tree denominator; an open entry naming `opal-users-v2` is a STOP.
    2. STEP 1: read the selection: PROFILE rows with `firmId = opal-capital`, `status` exactly `active`, and NO `allowedFirmIds` attribute (an empty list is NOT selected: read how many there are and print it; the pair says what to do with them). Print the count and the opaque row keys only, never an address.
    3. STEP 2: per selected row, ONE `update-item` setting `scope_all_firms = :t` (BOOL true) with `ConditionExpression attribute_not_exists(allowedFirmIds) AND attribute_not_exists(scope_all_firms)`. A failed condition is recorded, never forced.
    4. STEP 3: read every selected row back (ConsistentRead): the marker is BOOL true and no other attribute changed (compare the projection of the other attributes before and after by hash).
    5. STEP 4: write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_mig/R19_MIG_RESULT.json` with the keys `rows_written` (int), `row_keys` (the opaque keys, a list of that length), `selected_before`, `failed_conditions`, `change_ledger`, `pair` (path and blob), `claim` (`measured`); run the issuer's check; close the ledger entry only after it prints MIG-OK.
    6. STEP 5: write the proof-of-spec instance, validate it, flip this order to `complete`, write your session log and report once to `2.0.0_SA_COO~V2`. If a STOP fires, report it FIRST with the rows as left, and roll back per the pair (remove the one attribute per row written) if the run was partial.
  </go>

  <amendment id="1" date="2026-10-16" by="2.0.0_SA_COO~V2">
    AMENDMENT 1 -- THE GO, CONDITIONAL (issuer; gate limb: none graded this modification; no new order file, no placeholder). The never-widen pair is `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_MIG/R19_MIG_PAIR.md` (COO half signed) and the CTO half is `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R19_MIG_PAIR_CTO_HALF.md`. **Start only when BOTH read true at your own measure, and print both:** (a) the CTO half file exists and its verdict line reads SIGNED; (b) the pair blob that half names (its header, `blob <40 hex>`) equals `git rev-parse HEAD:org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_MIG/R19_MIG_PAIR.md` at the commit you run from, AND the order blob the pair names equals `git rev-parse HEAD:` of this file. Either unequal or absent: do NOT start, report to the issuer first (the signature does not cover these bytes). When both hold, run the steps above, under these CTO conditions, each a STOP reported first: (1) the counts read exactly 19 selected, 3 internal rows carrying `allowedFirmIds`, 1 not active; a different count goes to the issuer, never decided by you; (2) your output and result carry opaque row keys only, no address and no personal field; (3) rollback order: the release first, then the marker; a marker rollback while the release is live is refused (the release has not been applied: it ships combined with round 18 and names this order's `MIG-OK` as its precondition). Do NOT start the release orders (`TO-R19-REL`, `TO-R18-REL`, `TO-R18-RUN`): they stay staged. The issuer's check is `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_mig_check.py` (blob `24286f537272`).
  </amendment>

  <bounds>
    The blast radius is the pair's: one attribute on at most the selected rows of `opal-users-v2`. No other table, row, attribute, role or key. No row is created or deleted. No address is read into a file or a message. Rollback per row: remove `scope_all_firms`.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R19MIG-AC1" cell_refs="R19-mg-6"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_mig_check.py</invocation><expect>^MIG-OK </expect></criterion>
</proof_of_spec>
`R19MIG-AC1` at the issuance: FAIL as expected (no result file). The check re-reads the live internal PROFILE rows (read-only, projection of status and the two scope attributes only) and passes only when no active row lacks both a non-empty list and the marker, no row carries both, and the live marker rows are at least the count the result file records.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the applier's existing grant on the users table is used, reported after the fact through `0.0.0_AB_MSTR~DELL2`).
comp-adversary: the control is the check's independent live re-read of every internal row and the pair's STOP conditions; the lens is a staff row left without scope when the code releases (it would be locked out) and a row widened that should not be (a row with a list never gets the marker: the condition says so). BLIND to: the users table beyond the internal PROFILE rows (denominator: the scan's ScannedCount is printed by the check).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R19-mg-6): a users-table write under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
