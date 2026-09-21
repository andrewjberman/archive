# Render latency measurement -- IB-rth-2 decision tree input

**Worker:** `0.9.0_WK_IRPT_BCKEND~3`, narrow bounded-measurement act, authorized by
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_BCKEND_W2-S62_RTH2_SUBMIT_WIRING_20260921.md`.
**Date:** 2026-09-21. **Row filed:** `IRPT_BCKEND-W3-S52`
(`org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`).

This is NOT the original `TO-IB-rth-2` task order -- that stays open, untouched. This is the separate,
CTO-ruled bounded measurement that feeds its decision tree.

---

## RESULT, HEADLINE

**The 29-second render-latency question is STILL UNMEASURED.** The render never completed and never
even began writing a PDF -- it was blocked by a portal authentication wall (`SESSION_ABSENT`) before
Chromium got past the print route's sign-in screen. This is a DIFFERENT structural block than the one
the ruling flagged as a known, disclosed risk (`RENDERER_MODULE_ABSENT`) -- that risk did **not** fire;
the renderer module was found this run.

What DID get independently, positively re-confirmed with live traffic (not just document text) is the
vendor-separation architecture: 11 of 11 browser requests went to the Opal portal origin, 0 foreign,
0 vendor.

---

## 1. Host start

```
.tools/aws ec2 describe-instances --instance-ids i-0167fd745ad906a66 (before): State=stopped
.tools/aws ec2 start-instances --instance-ids i-0167fd745ad906a66 --region us-east-1
  -> CurrentState=pending, PreviousState=stopped
.tools/aws ec2 wait instance-running --instance-ids i-0167fd745ad906a66 --region us-east-1
  -> rc=0
.tools/aws ec2 describe-instances --instance-ids i-0167fd745ad906a66 (after): State=running
.tools/aws ssm describe-instance-information --filters Key=InstanceIds,Values=i-0167fd745ad906a66
  -> PingStatus=Online, AgentVersion=3.3.4624.0, PlatformName=Amazon Linux 2023
```

Host started cleanly and reached `running` + SSM `Online` before anything was sent.
**Confirmed still `running` after both SSM sends below** (final `describe-instances` check).
**The host was NOT stopped at any point in this session, per the ruling's absolute instruction.**

## 2. ExportBundle located and confirmed already-captured / already-approved

Investigated `infra/aws/lambda/investor-reporting/export/{bundle.py,handler.py,exclusion.py}` and
`infra/aws/terraform/investor-reporting/export/ssm.tf` to find the bundle layout
(`firms/<firm>/generations/<gen>/attempts/<n>/exports/<rev>/bundle.json`, bucket
`opal-data-ycharts` via `EVIDENCE_BUCKET`).

```
.tools/aws s3api list-objects-v2 --bucket opal-data-ycharts --prefix firms/49financial/generations/
  -> two bundle.json objects, both under generation GENRT8PROOF:
     firms/49financial/generations/GENRT8PROOF/attempts/1/exports/rt8-a/bundle.json      (660 bytes, 2026-09-11)
     firms/49financial/generations/GENRT8PROOF/attempts/1/exports/rt8-render/bundle.json (606 bytes, 2026-09-11)
```

`GENRT8PROOF` is named in `exclusion.py:32-38` as the generation this exact cell's (`IB-rt-8`) own
prior proof battery minted on 2026-09-11 -- a labelled SYNTHETIC generation (`irpt-synthetic=true`
metadata), never real firm/client data, and never a fresh vendor pull. Chose `rt8-render` (the render
revision) because no `report.pdf` had ever been written at that prefix -- consistent with the blocking
row's finding that this render has never actually completed or been timed.

```
.tools/aws s3api get-object --bucket opal-data-ycharts \
  --key firms/49financial/generations/GENRT8PROOF/attempts/1/exports/rt8-render/bundle.json ...
  -> Metadata: irpt-export-id=EXP-184aaa5454d45e8eb6312fe2a175fa01
              irpt-attempt-id=ATT-de6ea6df67930b8ad027f3e8204ddaa5
              irpt-bundle-sha256=9094e35ca97886b357ae1ad05503eb4ca6b8cb404c77bcb9239cf89bdac2d3fc
              irpt-synthetic=true
```

Validated it as a real, intact `ExportBundle`, not just present:

```python
import bundle as bundle_mod, json
obj = json.load(open('.scratch/bundle_rt8_render.json', encoding='ascii'))
bundle_mod.validate(obj)          # -> True (against ExportBundle.schema.json)
bundle_mod.digest(obj)            # -> 9094e35ca97886b357ae1ad05503eb4ca6b8cb404c77bcb9239cf89bdac2d3fc
                                   #    == the object's own irpt-bundle-sha256 metadata, exactly
```

**Confirmed: an already-captured, schema-valid, hash-verified-intact ExportBundle, not synthesized by
this worker and not a fresh vendor pull.**

## 3. SSM document identified and confirmed distinct from the YCharts one

```
.tools/aws ssm describe-document --name irpt-export-render-run
  -> DocumentType=Command, Owner=313476888478
.tools/aws ssm list-documents --filters Key=Name,Values=irpt-ycharts-runner-deploy,irpt-ycharts-run,irpt-export-render-run
  -> ["irpt-export-render-run", "irpt-ycharts-run"]
```

Two distinct documents exist; `irpt-export-render-run` is the one invoked, `irpt-ycharts-run` was never
touched. This matches `dispatch.py`'s own default (`RENDER_DOCUMENT = os.environ.get(
"IRPT_EXPORT_RENDER_DOCUMENT", "irpt-export-render-run")`).

## 4. Independent read of `ssm.tf` -- vendor-separation claim (my own control, before touching a live host)

Read `infra/aws/terraform/investor-reporting/export/ssm.tf` directly (not just the ruling's summary).
It supports the claim in its own text, three times, exactly as the ruling states:

- Header (`:5-9`): *"ONE DOCUMENT, AND IT IS NOT THE YCHARTS ONE. ... this document opens the Opal
  portal's own print route and writes a PDF."*
- `description` field (`:26`): *"NOT a vendor call: the only origin opened is the Opal portal origin,
  and a vendor origin is refused before the browser opens."*
- `PortalOrigin` parameter description (`:35`): *"NEVER a vendor origin -- the host refuses one before
  the browser opens."*

**Independently confirmed BEFORE sending anything.**

## 5. The measurement itself -- two sends

### Run 1 (this worker's own configuration error -- not evidence about render latency)

`PortalOrigin` has no default anywhere in `ssm.tf`, `dispatch.py`, or the Lambda's
`render_request()` call, so it had to be supplied and I guessed wrong the first time
(`https://portal.opal.internal`).

```
send-command d4b2aa90-7e2a-4311-b3b9-ec560beec38d @ 2026-09-21T13:55:39Z
get-command-invocation:
  Status: Failed
  ExecutionElapsedTime: PT6.178S (13:55:43.031Z -> 13:55:49.031Z)
  StandardErrorContent: "page.goto: net::ERR_NAME_NOT_RESOLVED at https://portal.opal.internal/..."
```

This is a DNS failure on my own bad input -- the domain simply does not exist. Not a render-latency
measurement. Superseded by run 2.

### The correct portal origin, found (not guessed a second time)

```
infra/aws/terraform/investor-reporting/export/main.tf:83-92
  portal_origin = "https://opalinvest.dev"
  (comment: an EARLIER wrong guess, https://portal.opalcapital.co, was corrected by exactly this
   class of live-run discovery -- row IRPT_BCKEND-W4-S22)
infra/aws/terraform/investor-reporting/export/lambda.tf:68
  IRPT_PORTAL_ORIGIN = local.portal_origin
```

This is the deployed configuration value, not a second guess.

### Run 2 (correctly configured -- the actual measurement)

```
send-command 0a950a41-4a92-4302-8bc1-5a269d99d60a @ 2026-09-21T13:57:45Z
get-command-invocation:
  Status: Failed
  ExecutionStartDateTime: 2026-09-21T13:57:48.320Z
  ExecutionEndDateTime:   2026-09-21T13:57:52.320Z
  ExecutionElapsedTime:   PT4.483S
```

StandardOutputContent shows the renderer-module-discovery step that the ruling flagged as a known
risk SUCCEEDING this run:

```
OK: node playwright under /opt/investor-reporting-ycharts/research/20260911/node_modules
```

**`RENDERER_MODULE_ABSENT` did NOT fire.** The run then reached the render step and was blocked by a
DIFFERENT condition:

```
OK: rendering export EXP-184aaa5454d45e8eb6312fe2a175fa01 attempt ATT-de6ea6df67930b8ad027f3e8204ddaa5 (performance-landscape-letter)
GUARD: {"requests_total":11,"requests_by_origin":{"opalinvest.dev":11},"foreign_origin_requests":0,
        "foreign_origins":[],"vendor_requests":0,"allowed_origin":"opalinvest.dev",
        "denominator":"0 foreign of 11 request(s); vendor hosts checked: ycharts.com,api.ycharts.com,
        bd3.bdreporting.com,api.cloud.orionadvisor.com",
        "outcome":"REFUSED",
        "refusal":"BLOCKED: SESSION_ABSENT -- the print route answered with a sign-in screen.
                    This script never signs in; an authenticated session for the host is an
                    OPERATOR ACT."}
```

**No PDF was ever produced.** The render pipeline stopped at an authentication wall before Chromium
could load the actual report content, so the discriminating fact this whole measurement exists to
produce -- does a real render finish inside the API Gateway's 29-second hard ceiling -- **was never
exercised**. This is not a timing result; it is a different BLOCKED outcome, structurally analogous to
(but distinct from) the ruling's disclosed `RENDERER_MODULE_ABSENT` risk. Per the ruling ("That is
information, not a reason to skip the attempt") and my task's own step 5, this is reported plainly as
BLOCKED, not as a timing.

**What this run DID positively confirm, with live traffic rather than just document text:** the
vendor-separation architecture. 11 of 11 real browser requests during this render attempt went to
`opalinvest.dev` (the Opal portal origin); zero went anywhere foreign; zero went to any of the four
named vendor hosts. `assertNoVendorHost()` and the request-counting guard in
`infra/aws/ec2/investor-reporting-export/render_export.cjs` behaved exactly as documented under a real,
exercised run.

## 6. Did not attempt to work around SESSION_ABSENT

`render_export.cjs:141-144`'s own comment: *"This script never signs in; an authenticated session for
the host is an OPERATOR ACT."* I made no third attempt, supplied no credential, captured no session,
and made no further guess. Establishing a portal session is outside this cell's delegated authority and
adjacent to exactly the class of act (a sign-in / session capture) this project's standing doctrine
(PRD FWD-4, CLAUDE.md's vendor-call bar) treats with particular care, even though this specific origin
is not a vendor. Not my call to make.

## 7. Host state, final

```
.tools/aws ec2 describe-instances --instance-ids i-0167fd745ad906a66 (after both sends): State=running
```

**Host is RUNNING, left running, per the ruling's absolute no-stop instruction. No stop action was
taken.**

## 8. Auto-shutdown coverage for this instance -- what exists (read-only investigation, no action taken)

- `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-02/ec2-auto-shutdown-audit.md`: audits 9 named
  instances (moltbot, smartx-exporter, seeking-alpha-scraper, bd-gold-layer-runner, bd-exporter,
  bd-allocations, bd-transactions, bd-price-runner, bd-gold-detail-generator). **`irpt-ycharts-runner`
  / `i-0167fd745ad906a66` is not among them; this audit does not cover this instance at all.**
- `infra/aws/terraform/investor-reporting/ycharts/instance.tf:1-30`: this project's own root declares
  `aws_ec2_instance_state.runner = "stopped"` as the converged/return state, and says so explicitly:
  *"There is no EventBridge rule here"*; *"the instance role has no ec2 control-plane grant: the box
  cannot start itself"*; *"a host left running after a render is drift against this line, not a
  permission."*

**Conclusion: there is no automated shutdown mechanism (no EventBridge rule, no Lambda, no watchdog
timer) for this specific instance anywhere in the fabric.** The only existing "coverage" is the
Terraform root's own DECLARED state, which will read as **plan drift** the next time anyone runs
`terraform plan`/`apply` against this root while the host is running -- not an automatic stop, and any
actual stop via that path would still need to go through `safe-apply` and would itself still be
subject to CLAUDE.md's human-confirmation requirement for stopping an EC2 instance. **No stop action
was taken by this worker; the host remains running and its disposition (stop, via a one-line
confirmation, or otherwise) is COO~B's / the CTO's call, exactly as the ruling states.**

Note, independently found in the same file: `instance.tf:15-21` corroborates the ruling's authorization
from a THIRD source (beyond the ruling text and my own `ssm.tf` read) -- *"Andrew-direct 2026-09-11
~14:5xZ, VERBATIM 'Yes ycharts runner may be started' (1.0.0_SA_CTO 95983)"*.
