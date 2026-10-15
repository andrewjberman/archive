# IRPT_DASHBD round 127, workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~14:1xZ)

**One order, drained. `DB-b-259` carries risk WORLD by the floor of its `infra/` path; it edits one Terraform file and a record, runs no Terraform command, no AWS write and no upload. Nothing served moved; counts, hashes and words only in the repo.** This round repairs the issuer's own round-123 order; there is no new CTO analysis. Issued @e96bafa386. Drained: `DB-b-259` (~212, merged @54e4a0036a). Not pushed. `round-close-check --project IRPT_DASHBD --round 127 --workstream B-49F`: 1 order, 1 complete, no JUDGMENT criterion, `verdict=MAY-CLOSE`. All three criteria (`DB127-1-AC1..AC3`) were run by me in the worker's tree and again on the LANDED tree after the merge: PASS.

## What was found, and what the cell did

While writing the apply order for the Cottonwood landing pair signed in round 126, I read the sibling function's Terraform and found that the landing root sets NO Lambda layer while its adapter imports pyarrow at module level; the python3.12 runtime carries no pyarrow, so the function would have failed on its first invocation. **Nothing was applied or deployed** (function, roles, schedule and artifact are absent in AWS). Row `IRPT_DASHBD-D2-S84` (ARMED, owner this seat) was filed first. `DB-b-259` adds the sibling's own pattern to `lambda.tf`: a read-only data source for the EXISTING `irpt-performance-native-layer` (latest version 1, python3.12; the sibling `irpt-cot-account-dim-lambda` runs on exactly that version) and one `layers` line on the module call. 9 inserted lines, 0 deleted; memory 1024 and timeout 900 unchanged; the expected plan stays 7 add / 0 change / 0 destroy (inferred; nothing was planned). The checker also proves that the bundle's import-time third-party imports are exactly pyarrow plus the runtime's boto3/botocore and that the layer's zip holds `python/pyarrow/__init__.py`.

## Issuer error this round (mine, disclosed)

`DB-b-252` (round 123) named the function's packaging and IAM and never its runtime dependencies, and the round-125 memory measurement ran locally with pyarrow loaded, which hid the gap. The signed pair (sha256 `c63702ade4df`) described a function that could not import; the CTO marked their half VOID (@c6527774c8) and added a step-0 layer condition (msg 8287). Revision 2 of the packet (sha256 `a1b080c5fe06`, COO half re-signed @fed117446e) carries the layer, the new pins and the condition; the CTO half is asked.

## What this seat read for itself

The sibling root's `lambda.tf`; the sibling function's live configuration (layer ARN, runtime); the layer's version, runtime and size; the worker's diff line by line; all three criteria on the landed tree; the build-only package again at the merged tree (sha256 unchanged, the layer is not in the zip). Not done: any `terraform plan`, any invocation, a comparison of the layer's pyarrow version with the one the adapter was measured with.

## Rows held (owners named)

`W209-S3` (ARMED, CTO; disarmable on round 126's read); `D2-S84` (ARMED, this seat; disarms when the CTO half is re-signed on revision 2); `W195-S1` (ARMED, 2.0.0_SA_COO~C2, no reply read); `D2-S72` (2.0.0_SA_COO~B1, no reply read); `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). No ARMED row has a dark owner as far as this seat can read.

## What goes to the CTO (one ask, in the slug)

**Sign the CTO half on packet revision 2 (sha256 `a1b080c5fe06`).** Recommendation: yes; your three section-9 answers and your step-0 layer condition are carried unchanged. The apply order to the AE seat is staged the moment it is signed.

## What this does to the FWD outcomes

`FWD-11` and `FWD-21` (Cottonwood landing): the repo half is now complete and consistent; none is met until the apply and the first events. Hop 1's first scheduled fire (tomorrow about 11:41Z) remains the L3 read. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
