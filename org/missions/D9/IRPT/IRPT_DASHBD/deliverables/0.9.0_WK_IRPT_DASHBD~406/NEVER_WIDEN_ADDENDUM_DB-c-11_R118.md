# NEVER-WIDEN ADDENDUM DB-c-11 (round 118, workstream B-CW) -- the shared zip's registry pin and the second zip upload

STATUS: UNSIGNED. This packet carries no signature and records no approval. It is a proposal for the CTO's half and the issuer's half to sign or refuse before any second upload. Written by 0.9.0_WK_IRPT_DASHBD~406 (worker of 2.0.0_SA_COO~C2), order IRPT_DASHBD.TO-DB-c-11, LOCAL only; nothing is uploaded, planned, applied, invoked, pushed or deployed.

Live zip this packet starts from: S3 object investor-reporting/irpt-holdings-performance-lambda.zip in bucket opal-313476888478-lambda-artifacts, version vrBQAr57i.p3TMhjdSld3c_E5HMqX8iy (139628 bytes, 14 members, SHA-256 39ac0231a12aaa8f1289fbeb552634eb22d378a28217c370e751dc7950e1eba8, measured by one GET on 2026-10-15). That version is the first new zip, uploaded by the first catch-up attempt (TO-DB-c-9); it runs on the functions irpt-holdings-performance-lambda, irpt-inf-holdings-performance-lambda and irpt-cot-holdings-performance-lambda.

Why this packet exists: the first catch-up invoke on the Cottonwood function refused with registry lookup('z09') failed: KeyError. The live zip packages scopes.json from the old pin 14b52ca13a (11 scope rows, no z09). HEAD's scopes.json has 14 rows including z09. The producer derives the Cottonwood firm from the registry (firm_scope in holdings_performance.py), so the old pin is the cause. The measured record of the pins, the scope rows and the differential is org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~406/SCOPES_PIN_READ_R118.json.

## Change set

The source-map edit is one staged_from entry of the function irpt-holdings-performance-lambda in infra/aws/lambda/ci/lambda-source-map.json, the entry whose repo_path is infra/logic/registry/scopes.json. Only its two fields change:

- pin: 14b52ca13a467e4be0e47231fb6840611bbb134a changes to 69679b90e3dc52b670d33fddd96d06be1deaac90. This is the latest commit that touches scopes.json and it is an ancestor of HEAD.
- sha256: a4e0637257b6c50adf23de75d3f344b3d39db6bf9a024f4b47dd825131532be9 changes to 6ce64167c26588521fded21330dc59e0109450e9a01c92e0f6ca9aa90b53cfae, the SHA-256 of the blob at that pin (the same blob as HEAD).

Nothing else on that entry changes. The other six registry members keep their pins: systems.json, tiers.json, exemptions.json, remediations.json, resources.json and reporting_policies.json. Five of them differ from HEAD (tiers.json does not). The measured differential needed scopes.json alone, so no second member is re-pinned.

Upload-time writes that are not hand edits: after a successful upload, build-and-upload.sh writes artifact_s3_key and artifact_sha256 for the function (its write_sha_to_map step). The artifact_sha256 stamp is the one row IRPT_DASHBD-D2-S59 already records as owed. It is named here so it is not mistaken for a second edit.

No Terraform file changes. No file under infra/aws/terraform is edited, and no module, variable, role or schedule is touched.

## Build and member diff

Build from the commit that carries the source-map edit, with the build script in BUILD_ONLY mode first: BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh <pipeline> irpt-holdings-performance-lambda. The pipeline argument is the one the script's own usage accepts for this function; confirm it at build time, because the script's usage text does not list investor-reporting. BUILD_ONLY keeps the zip, prints its SHA-256 and skips the upload, the head-object verify and the source-map update.

Compare the built zip with the live version vrBQAr57i.p3TMhjdSld3c_E5HMqX8iy member by member, by name and by content. The member count is 14 in both. The member diff must be EXACTLY the re-pinned members, which is one member: infra/logic/registry/scopes.json. Its bytes must equal the blob at 69679b90e3 (SHA-256 6ce64167c26588521fded21330dc59e0109450e9a01c92e0f6ca9aa90b53cfae). Any other difference is a STOP before upload: an added or missing member, a changed handler.py, a changed holdings_performance.py, or a changed registry member other than scopes.json.

Only after that comparison passes is the zip uploaded under the same key. The upload creates a new object version. That new version id becomes the artifact the three functions read, and it is recorded in the ledger before the plan. The old version vrBQAr57i stays in the bucket (versioned) and is the rollback target below.

## Plan

A targeted or full plan of the holdings-performance stack, after the source-map commit and the upload, must read 0 to add, 3 to change and 0 to destroy. The three changed resources are the three function code updates:

- module.irpt_holdings_performance.aws_lambda_function.this (irpt-holdings-performance-lambda, the 49 Financial function)
- module.irpt_holdings_performance_inf.aws_lambda_function.this (the Inflection function)
- module.irpt_holdings_performance_cot.aws_lambda_function.this (irpt-cot-holdings-performance-lambda, the Cottonwood function)

Any other shape is a STOP: an addition, a deletion, a fourth changed resource, or a change to a role, a policy, a schedule or a layer. The plan is saved and applied with safe-apply from the saved plan file, never with a bare terraform apply.

## Resume at the catch-up

After the apply, the open ledger irpt-dashbd-cottonwood-holdings-performance-20261015 is CONTINUED at the legs it left open (row IRPT_DASHBD-D2-S58 names legs L5 to L8). A new ledger is not opened for this resume. The ledger is closed only after the enable step is graded.

The resume then runs exactly as steps 6 to 8 of IRPT_DASHBD.TO-DB-c-9:

1. The 12-date catch-up, by the handler event, against irpt-cot-holdings-performance-lambda with the blackdiamond_z09 source. The catch-up dates and keys are the first packet's, re-derived by the builders to the as-of date at the time of the run. They are not carried over from this packet, and no key is written by hand.
2. The after-read: a fresh LIST of both Cottonwood gold prefixes, the keys written in the window, and the Cottonwood function's CodeSha256 read back equal to the built zip's.
3. The 1.1 and 1.2 reader check: the three readers, each clean on one 1.1 and one 1.2 partition.
4. The planted listing test on the Cottonwood execution role.
5. The ENABLE of the schedule irpt-cot-holdings-performance-daily, only after a 0/1/0 plan that follows the after-read. The schedule was created DISABLED by the first apply and stays DISABLED until this step.

A STOP inside the catch-up stops the run. The ledger is left open and the state is reported as in the first packet.

## Both branches

Success: the three functions read the new zip version, and the new CodeSha256 is equal on all three. The 49 Financial and Inflection derivations are unchanged by the differential, which is measured for the three declared channels (schwab_08335338 resolves to 49financial, orion to inflection, both identical with and without the re-pin). The catch-up proceeds at Resume at the catch-up, steps 1 to 5.

Failure of the upload: nothing changed in S3 beyond whatever the failed attempt wrote. The live object is still vrBQAr57i. The three functions still run vrBQAr57i. Record what the upload returned and stop.

Failure of the apply after a successful upload: the live state is the new zip version on any function the apply already updated, and the old version on the rest. Read CodeSha256 on all three, record which carries which value, and stop. Roll back under Rollback before any further plan.

Failure midway in the catch-up: the state is as the first packet describes it. Keys already written stay written and are listed by the after-read. No key is deleted. The schedule stays DISABLED. The ledger stays open at the leg where it stopped.

## Rollback

The previous zip is S3 version vrBQAr57i.p3TMhjdSld3c_E5HMqX8iy. Rollback is restoring that version as the current object of the same key by a server-side copy over the same key, a write that creates a new version, never a delete. After the copy, a plan must read 0 to add, 3 to change and 0 to destroy, as the order states; the CTO's half is asked to confirm that this is the right shape (see the questions). The source map is reverted to the previous pin in the same commit that reverts the copy.

Not the rollback of this packet: the version before the first upload, S7DO3mEXQ2zsk0pkiJB127d_VSHCksbh (named in row IRPT_DASHBD-D2-S58). Restoring it would put back the old registry without z09 and reinstate the refusal, so it is not a fallback for this packet.

## Questions for the CTO's half

1. This is a second upload to the same key. The first pair (TO-DB-c-5, blob ad049d506c) covered the first upload only. Is this packet a new signed act that the CTO's half and the issuer's half sign before the second upload?
2. The pin: is scopes.json at HEAD's blob, pinned at commit 69679b90e3 (the latest commit touching the file, 2026-10-12), the intended pin, or should the pin name a different commit?
3. Do the other six members stay pinned at their old commits? Five of them differ from HEAD (systems, exemptions, remediations, resources, reporting_policies). Tiers does not.
4. The 49 Financial and Inflection functions run the same zip. Their next scheduled fires would run on the new zip. What are those fire times, and does the CTO's half accept them running on the new zip before the Cottonwood catch-up?
5. The changed scope rows for 49financial and inflection (between the old pin and HEAD) reach those two functions through the registry's other readers, which the differential did not cover. Does the CTO's half accept that, or should those readers be measured first?
6. The Cottonwood function has no source-map row (row IRPT_DASHBD-D2-S59), so record-deploy-scope refuses it. Is that owed patch to be included in the source-map commit of this act, or in a separate commit?
7. The rollback plan shape (0 to add, 3 to change, 0 to destroy) is the order's words. Is that the right read-back after a copy, or should it read 0 to change?
8. Andrew's word is needed for any delete. None is planned by this packet.

## Not in this packet

Not established by this packet: that the build reproduces the new zip byte for byte (no build was run); that the member diff is clean (it is measured at build time, not here); that the other six re-pins match what the builder would stage; that the ledger irpt-dashbd-cottonwood-holdings-performance-20261015 is in the state the first packet describes (it was not read); that the schedules' current states and next fire times are as stated (they were not read); that the 49 Financial and Inflection readers other than the firm derivation are unchanged by the re-pin; that the catch-up dates for the as-of day are the first packet's (they are re-derived at run time); and that any apply, invoke or upload would succeed. This packet does not sign, approve, record a decision or authorize any act.
