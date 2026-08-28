# TO D1_CATVIEWS.TO-R1-AE — THE RELAND + REFIRE, GATED ON "ONCE ALL FIXES ARE IN"

<task_order id="D1_CATVIEWS.TO-R1-AE" project="D1_CATVIEWS">
<id>D1_CATVIEWS.TO-R1-AE.reland-and-refire-on-andrews-word</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews-fullproduct/20260828T2130Z/DECOMP.md @ec7eda542e <owned_cells>CATVP-a-1, CATVP-a-2</owned_cells></decomp_ref>
<issued_to>`0.7.0_AE_CloudOps~Z` — warm and holding. Chain steps 2 and 3.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T21:4xZ</issued>
<status>pending -- CUT AND GATED. Fires when `D1_CATVIEWS.TO-F1-DE`'s render fixes are LANDED, not before.</status>
</task_order>

<proof_of_spec>
  <criterion id="CATV-TOR1-AC1" cell_refs="CATVP-a-1"/>
  <criterion id="CATV-TOR1-AC2" cell_refs="CATVP-a-1"/>
  <criterion id="CATV-TOR1-AC3" cell_refs="CATVP-a-2"/>
  <criterion id="CATV-TOR1-AC4" cell_refs="CATVP-a-2"/>
  <expected_criteria>CATV-TOR1-AC1,CATV-TOR1-AC2,CATV-TOR1-AC3,CATV-TOR1-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D1_CATVIEWS.TO-R1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4, firm-tokened `CATV-TOR1-ACn`. Cells: 2, pre-existing @ec7eda542e.</alignment_denominators>
</proof_of_spec>

## THE AUTHORIZATION AND ITS GATE

**ANDREW-DIRECT 2026-08-28 ~21:4xZ, VERBATIM: *"yes reland once all fixes are in"***

This is the explicit in-session word for a **RESERVED-CATEGORY S3 DELETE** of the 16 conflict-held
dated gold keys enumerated in the 21:3xZ dry-run off manifest
`_manifests/2026-08-27/20260828T211849Z.json`.
⛔ **IT IS GATED, NOT OPEN.** *"Once all fixes are in."* **A reland fired before the render fixes land
burns the act twice and stamps two generations of ad-hoc provenance onto the served plane for
nothing.** ⛔ **AND IT IS NOT A PROMOTE AUTHORIZATION** — that is a separate DT act on a separate gate.

## ACCEPTANCE CRITERIA

**AC1 `CATV-TOR1-AC1` — THE DELETE EXECUTES THE PRE-READ LIST, NOT A DISCOVERED ONE.**
Run against the **already-enumerated** 16 keys (4 each of `aggregate-aua-timeseries`, `aum-metrics`,
`account-distribution`, `category-views`). **Print the list you are about to delete and the list the
dry-run produced, and show they MATCH before `--confirm`.** ⛔ **A destructive act discovering its own
target mid-run is the thing the dry-run exists to prevent.**

**AC2 `CATV-TOR1-AC2` — THE AD-HOC STAMP IS DECLARED, NOT DISCOVERED, AND NEVER FORGED.**
The reland writes `_provenance.trigger = {"kind":"manual","detail":{"source":"adhoc"}}` into **ALL 16**
served objects — including the 12 unrelated to `category-views`. **State this in the instance as a
KNOWN AND ACCEPTED consequence, with its CLAUDE.md citation** (*"ad-hoc artifacts are never production
evidence"*).
⛔⛔ **NOBODY "FIXES" IT BY PASSING `{"source":"aws.events"}`. THAT IS FORGING A SCHEDULED PROVENANCE
AND IT IS FORBIDDEN.** ⚠ **AND THE CONSEQUENCE MUST BE CARRIED FORWARD, NOT BURIED:
`CATV-TON1-AC7` REQUIRES A SCHEDULED FIRE AND READS THIS FIELD — so a relanded object FAILS AC7 BY
CONSTRUCTION.** Name that in the instance. **Monday's scheduled fire is what discharges AC7; this
reland is what makes the values VISIBLE.** Do not let a reader conflate the two.

**AC3 `CATV-TOR1-AC3` — THE REFIRE REACHES PLATINUM, MEASURED AT THE SERVED OBJECT. ⭐ AMENDED 21:4xZ: THIS CRITERION NOW ALSO DELIVERS `D-1`.** The served member objects must gain the `aum` KEY — currently ABSENT entirely (`['display_name','member_id','served','strategy_id']`, all 9 `None`), which is why the L2 rows render `--`. **Post-reland: 8 of 9 carry values and EXACTLY ONE (Custom `members[0]`) remains a genuine `None` and MUST still render `--`.** ⛔ **A result where all 9 carry values means a number was invented.** Print the member key list before and after, per branch.
Floor re-run → publisher → `platinum/mdpf/{scope}/category-views.json` carries
`SMA.aum 22,794,766.25` and `Client.aum 267,632,047.22` at global ⛔ **— VALID ONLY AT `as_of` 2026-08-27, WHICH IS WHAT TONIGHT'S RELAND WRITES. The figure is MARKET-VALUED and moves ~$170-250k per trading day; scored against a LATER artifact these literals FAIL A CORRECT FIX.** If this criterion is ever re-scored (Monday's fire, a re-run), the literals go **`NA_BY_DATE` — never PASS, never FAIL — and the date-INDEPENDENT identities carry the verdict instead**, and the false `absent_reason` is
**GONE** for `global` and `49financial` while **RETAINED** for `cottonwood` and `inflection`.
⛔ **BOTH LIMBS OR IT IS NOT A PASS** — deleting the `absent_reason` everywhere is a FAIL; it is a
correct, sovereign-cited statement for the two firms that genuinely have no SMA members.
**Print the served `LastModified` + byte size + the values, per scope, with the denominator (4).**
⛔⛔ **AND `mdpf_refresh.py gold`'s OWN VERIFY PASS IS NOT ACCEPTANCE FOR THIS CRITERION.** Measured at source by `0.7.0_AE_CloudOps~Z`: `:104-105` hardcodes `platinum/mdpf/{scope}/aggregate-aua-timeseries.json` — **ONE artifact type of four, NEVER `category-views`** — and `:279-286` scores `as_of` recency AND write-freshness **on timestamps only, never opening a value.** >> **IT WILL PRINT `PASS` FOR ALL FOUR SCOPES WHETHER OR NOT THE SMA FIX REACHED THE SERVED PLANE.** << **That would have been the third false all-clear of the night, and the seat that would have quoted it is the one that found it.** **Acceptance here is the VALUES you read out of `category-views.json` yourself.**

**AC4 `CATV-TOR1-AC4` — NO COLLATERAL MOVEMENT ON THE OTHER THREE ARTIFACT TYPES.**
`aggregate-aua-timeseries`, `aum-metrics` and `account-distribution` are relanded too. **Show their
business content is UNCHANGED** — same values, only provenance moved. ⚠ **This is the criterion that
catches a reland doing more than intended**, and 12 of the 16 keys have nothing to do with this
product.

## BARRED / REPORTING

⛔ **Deploy ledger OPENS before the delete, CLOSES at completion** (NEVER#6). Chain with `&&`, never `;`.
⛔ **Do NOT promote** — DT's act, separate gate. ⛔ **Do NOT touch the render.**
⚠ **`aws s3 cp` has returned rc=0 and written nothing on this device** (POSIX-destination shim
rewrite). **Re-read every object you believe you wrote.**
RAVC to `2.0.0_SA_COO~Z` once, stating push state as a measured value.
