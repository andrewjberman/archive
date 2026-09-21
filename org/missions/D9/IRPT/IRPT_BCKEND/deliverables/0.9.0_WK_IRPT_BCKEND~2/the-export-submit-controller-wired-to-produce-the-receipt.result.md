# RESULT -- IRPT_BCKEND.TO-IB-rth-2

**Worker:** `0.9.0_WK_IRPT_BCKEND~2` · **Branch:** `wk-irpt_bckend-8-2` · **Run:** 2026-09-21 · **HEAD:** `7df516b46e36da96b7ea446742bc0d0d08021739` (unchanged by this worker -- no source edit)

## SUMMARY: ARM (a)'S PREMISE MEASURED FALSE -- NO SOURCE EDIT, PACKET, LEDGER OR APPLY THIS PASS

Arm (a) instructed: "identify the MINIMAL wiring that makes a real submit produce a receipt at
the aligned address rtg-1 proved." MEASURE FIRST found that no such wiring exists, minimal or
otherwise, and that this is a structural fact about the deployed system rather than a gap this
cell's edit could close. Full grounding, citations and the disarm condition are in row
`IRPT_BCKEND-W2-S62` (`surprise-channel/investigations/INVESTIGATION_v1.md`, class BLOCKING,
hazard_standing ARMED, disarm_owner `2.0.0_SA_COO~B`).

**The five measured facts, in one line each (each independently re-derived this session, never
inherited):**

1. `entry.py`'s own `submit_export` -- the function actually bound to `OPERATION_SUBMIT` in the
   deployed `ENTRY` -- is still the unconditional `_ExportNotWiredHere`/`NOT_READY` stub (row
   `W1-S43` unchanged; confirmed by this worker's own read of `entry.py:157-199,221-226`, not by
   re-quoting the prior row).
2. `handler.py`'s `finalize_export` -- the function arm (b) names as the one a real wiring must
   reach, via `receipt.build()`/`persist_receipt()` -- has **zero call sites** anywhere under
   `export/` other than its own `def` line (13 files scanned), and `handler.py`'s own
   action-dispatching `lambda_handler` (which DOES branch on `action=="submit"`) is **dead
   code**: Terraform wires `entry.lambda_handler`, never `handler.lambda_handler`
   (`lambda.tf:46`). There is no route, action or callback anywhere in the deployed system that
   ever reaches `finalize_export`.
3. The render is genuinely asynchronous and deliberately host-gated. The render host
   (`irpt-ycharts-runner`, `i-0167fd745ad906a66`) is **live-measured `stopped`** this session
   (`ec2:DescribeInstances`, read-only). The controller's own IAM (`iam.tf:25-28`) deliberately
   withholds `ec2:StartInstances`/`StopInstances`, and `dispatch.py`'s own text names starting
   the host "an OPERATOR ACT, not a retry" -- outside this worker's delegated authority.
4. Even with the host running, a same-request wait-and-finalize is not viable: the API Gateway
   HTTP API integration in front of this route is configured `timeout_milliseconds = 29000`
   (`integrations.tf:58`) -- a **hard, measured 29-second ceiling** on the whole client-visible
   request, independent of this Lambda's own 120s timeout (`lambda.tf:47`) and the render
   document's own 900s script budget (`ssm.tf:41`). A render that takes longer than ~29s cannot
   be waited out inside one HTTP call under any code.
5. The published v1 response contract for `submit-export`
   (`docs/contracts/investor-reporting/v1/responses/submit-export.response.schema.json`) requires
   a **complete** `ExportReceipt` in `data` (`additionalProperties: false`, `data` in the
   top-level `required` array, `data.$ref` -> `ExportReceipt.schema.json`, itself requiring
   `artifact`/`facts`/etc unconditionally). There is no legal partial/pending SUCCESS shape for
   this operation -- only a refusal (a structurally different envelope) is legal when no render
   has completed.

Independently, the controller functions a real wiring would call are themselves correct in
isolation: the full offline suite (`tests/test_export.py` + `tests/test_rt8.py`) passes 68 of 68
this run.

## WHY NO SOURCE EDIT WAS WRITTEN

A partial wiring (freeze + persist + dispatch-decision only, no finalize) is real, in-bounds
progress on the DEFECT row `W1-S43` names (the unconditional raise), but it cannot legally answer
`submit-export`'s own published response contract with a 2xx `data` payload (fact 5) -- it could
only ever legally return a REFUSAL, exactly as today, just for an honest reason instead of an
unconditional one. Shipping it through the full never-widen + change-management + apply machinery
would not move R77-AC1 from FAIL to PASS, and BOUNDS confine this cell to "the submit-wiring
edit" -- not a new finalize/callback capability, which is what a conforming implementation would
actually require and which is a substantially larger, unbuilt piece of this system (fact 2).
Writing a fragile same-request poll-and-wait against an undocumented render latency and a hard
29s platform ceiling (fact 4) is inconsistent with this codebase's own measured-not-assumed
standard throughout `export/*.py`, and this worker cannot measure the real render latency without
the operator act barred by fact 3.

## THE BATTERY

`battery_ib_rth_2.py` is measurement-only: it re-derives facts 1-6 above live against the
worktree and AWS, prints a denominator for each, and -- correctly -- **never emits R77-AC1's PASS
token**, because no real submit -> receipt round trip was attempted (none would be honest). Output
`IB-rth-2_R77-AC1_battery_output.txt` sha256
`67f1546ee9a033f6d2c91c117e95f20764655e6903f1cd19026e047b8bfaa518`; rc 1; 6 of 6
premise-confirmation arms hold (all six SHOULD hold for the blocking row to be GROUNDED, and they
do).

## R77-AC1 / R77-AC2

R77-AC1 is graded **FAIL-by-measurement** in this order's `proof_of_spec` instance: the
invocation ran, the exact output is recorded, and the `<expect>` token is truthfully absent. This
is FAIL-BY-PREMISE-FAILURE, not FAIL-by-defect: the cell's own arm (a) instruction was to confirm
whether a minimal wiring exists, and the measured answer is that it does not. R77-AC2 (judgment)
is left `UNVERIFIABLE-BY-INSTRUMENT` for `3.0.0_SA_CVO` at L9, as no worker self-grades a judgment
criterion.

## `<status>` LEFT NON-TERMINAL

No `<status>` flip. No `NEVER_WIDEN_SIGNOFF_PACKET`, no build ledger, no change-management
ledger, no apply this pass -- none has a diff to cover. The order stays open. See row
`IRPT_BCKEND-W2-S62`'s `notes` field for the three-way disarm condition (a CTO/COO ruling on:
(a) operator starts the host + a NEW cell builds the finalize/callback path if latency clears the
29s ceiling; (b) the acceptance criterion is redefined for an asynchronous two-phase proof; or
(c) a ruling accepts the freeze/persist/dispatch-only partial wiring as sufficient progress,
explicitly waiving R77-AC1's literal "produces a receipt" consequence for this round).
