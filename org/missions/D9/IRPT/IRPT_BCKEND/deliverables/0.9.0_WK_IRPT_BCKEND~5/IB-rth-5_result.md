# IB-rth-5 result -- session-establishment tooling for the export render host

**Cell:** `IB-rth-5`, `IRPT_BCKEND.TO-IB-rth-5`. **Worker:** `0.9.0_WK_IRPT_BCKEND~5`.
**Outcome this pass:** honest STOP, exactly as the task order's arm (d) names it. `<status>`
stays open (not touched by this worker, per this project's own precedent on `IB-rth-1`).

## What was built

- `infra/aws/ec2/investor-reporting-export/render_export.cjs` -- additive-only storageState
  reuse (`loadSessionContextOptions` + `SESSION_STATE_PATH`), proven wired and non-regressive
  by `battery_ib_rth_5.py` (7 of 7 static anchors unchanged, 4 of 4 scenarios, 1 of 1 negative
  control). **R80-AC1 PASSES this pass** -- that criterion's own bar is the code path, never a
  deploy.
- `infra/aws/ec2/investor-reporting-export/capture-session.cjs` + `capture-session.sh` (new) --
  the interactive capture tool and its SSM-shell wrapper.
- `infra/aws/ec2/investor-reporting-export/README.md` -- the operator runbook, in full, under
  "Session establishment (cell IB-rth-5)".
- `NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-5.md` -- the packet both halves sign against.
- `IRPT_BCKEND.TO-IB-rth-5....proof_of_spec.json` -- validated `VALID (rc=0)`.

Committed: `a05d2dcaafe3e3bdfc3122dd0b875f80297e77ec` (source + tooling + packet + battery),
`0680db7c6e` (the proof_of_spec instance). Branch `wk-irpt_bckend-8-5`, LOCAL only -- not
pushed, not merged.

## What is NOT done, and why

**Nothing is deployed.** The host (`i-0167fd745ad906a66`) was never started by this worker; no
SSM command or session was sent against it; nothing was uploaded to
`s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`. No real session was
captured, no MFA login was attempted, scripted, or synthesized anywhere in this pass.

## Exactly who needs to act next, and how

**1. `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`** -- sign the two never-widen halves against
`NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-5.md`'s committed blob
(`a05d2dcaafe3e3bdfc3122dd0b875f80297e77ec`), each in their own deliverables path:
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rth-5_*.md`
and `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rth-5_*.md`.
Both name the packet's blast radius (section 4), not just an intention.

**2. Once both halves are signed:** a worker (this one, resumed, or a successor cell) deploys
the four touched/new files to the S3 artifact prefix via the ESTABLISHED mechanism (`aws s3 cp`,
per `IB-rt-8`'s own deploy-completion record), opens a change-management ledger before the
upload, and runs arm (e)'s synthetic-storageState proof against the DEPLOYED bytes on the host
(never claiming a real session -- exactly as this pass's own local proof already demonstrates the
shape of, but against live bytes this time).

**3. The named human operator (Andrew, or a delegated operator holding valid Opal portal
credentials)** -- and ONLY after step 2 lands the tooling on the host -- runs the runbook in
`README.md`'s "Session establishment" section: starts the host, opens the SSM port-forward,
signs in to the Opal portal INCLUDING completing MFA in the exposed DevTools tab, and lets
`capture-session.cjs` re-verify and write `storageState.json`. **This is the one step no code,
no worker, and no packet in this project performs or can perform.** Once captured, `rth-2`'s
stalled render-latency measurement (row `IRPT_BCKEND-W3-S52`) can be re-attempted against an
authenticated session for the first time.

**4. A runbook precondition named but not verified by this cell:** whether the operator's own
AWS identity holds `ssm:StartSession` / `AWS-StartPortForwardingSession` on
`i-0167fd745ad906a66`. If absent, that is a separate IAM grant request -- outside this order's
`<paths>` and not a defect in this tooling.

Nothing in this pass is a failure; it is the honest stopping point the task order itself
prescribes for a production-host deploy awaiting its two required sign-offs.
