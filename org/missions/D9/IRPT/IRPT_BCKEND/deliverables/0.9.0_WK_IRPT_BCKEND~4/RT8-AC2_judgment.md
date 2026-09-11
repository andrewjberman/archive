# RT8-AC2 -- JUDGMENT, RECORDED AND NOT SELF-GRADED

`0.9.0_WK_IRPT_BCKEND~4` on `IRPT_BCKEND.TO-IB-rt-8`. Graded by `3.0.0_SA_CVO` at L9. This file
carries OUTPUT and no verdict. Every number below is a read this cell performed; where a fact is
inherited from round 1 it says so and names the artifact it was read from.

---

## 1. WHICH HOST RENDERED, AND ITS LIFETIME, COST AND CONCURRENCY LIMITS

**IN ROUND 2: NO HOST RENDERED. The render step reads HUMAN-GATED.** Read from the deployed
controller, not asserted here: `aws lambda invoke irpt-export-render` with
`action=render_preflight` returns `decision=HUMAN_GATED`, host `irpt-ycharts-runner`
(`i-0167fd745ad906a66`) `state=stopped`, `document_exists=true`, and the operator's three commands
as data. Row `IRPT_BCKEND-W4-S14` carries the reason; the short form is that the blocker is not the
absence of a browser but the absence of a start this cell may perform.

**THE HOST THE SYSTEM IS BUILT FOR -- `irpt-ycharts-runner`, and its limits:**

| property | value | where it is declared |
|---|---|---|
| instance | `i-0167fd745ad906a66`, `t3.medium` (2 vCPU / 4 GiB) | `infra/aws/terraform/investor-reporting/ycharts/main.tf` `var.instance_type`, whose own description says "Chromium needs the headroom" |
| LIFETIME | none of its own. `aws_ec2_instance_state.runner` declares `stopped`, so the CONVERGED state of that root is a host that exists and is not running. It is started for an act and stopped after; nothing schedules it (no EventBridge rule in the root) and it cannot start itself (its instance role carries no ec2 control-plane grant) | `.../ycharts/instance.tf` |
| COST | EBS only while stopped (encrypted root volume); `t3.medium` compute for the minutes it runs. There is no idle compute charge because there is no idle RUNNING state | the declared state above |
| CONCURRENCY | **1, structurally.** `ssm:SendCommand` on the export document is granted against exactly ONE instance id and ONE document name, and the host is one box. Two exports do not render in parallel; they queue behind the operator | `infra/aws/terraform/investor-reporting/export/iam.tf` |
| ISOLATION | a SECOND SSM document, `irpt-export-render-run`, deliberately separate from `irpt-ycharts-run`. A render and a vendor sign-in are different documents on the same box, so an audit of what ran reads the document name rather than inferring intent | `infra/aws/terraform/investor-reporting/export/ssm.tf` |

**THE HOST THAT DID RENDER THE FOUR STORED PDFs, stated plainly because it matters to the grade:**
round 1's IB-s-14 rendered them on the DEVELOPMENT BOX through Playwright driving Chromium via
`channel="msedge"` -- an already-installed browser, chosen because an install off Opal
infrastructure was refused at IB-s-8 (rows W3-S1/S2). That host's lifetime was the battery process,
its cost was zero marginal, its concurrency was 1, and **it is not an estate host.** The round-2
work exists precisely because a laptop is not where an export renders.

**WHAT IS AND IS NOT BUILT.** Built, deployed and proven on the served service: the freeze, the
persist-before-render (`head-object` read back equal), the version gate, the identity, the dispatch
decision, the unsent request, the download reauthorization. Built and NOT exercised: the host half
(`infra/aws/ec2/investor-reporting-export/render_export.cjs`, its runner script, the SSM document,
the IAM). The ONE unexercised step is a browser opening the print route.

---

## 2. WHICH FONTS THE PDF ACTUALLY EMBEDDED VERSUS THE PACKAGE'S REQUIREMENT

**THIS IS THE SHARPEST DIVERGENCE IN THIS FILE AND IT IS MEASURED, NOT INFERRED.**

The counterpart's package DECLARES, at `portal/src/pages/InvestorReporting/render/manifest.ts`
(`portal` HEAD `32a744dcd3`): `fonts: ['Lato-Regular', 'Lato-Bold', 'Lato-Italic']`.

The four stored PDFs, read back from S3 and parsed by `render.fonts_embedded()`:

| object | embedded font subsets |
|---|---|
| `GENIBS14SYN/.../r1/report.pdf` | `AAAAAA+SegoeUI-Bold`, `BAAAAA+SegoeUI`, `CAAAAA+TimesNewRomanPSMT` |
| `.../v0-11-overview/report.pdf` | the same three |
| `.../v0-11-comparison/report.pdf` | the same three |
| `.../v0-11-multicomp/report.pdf` | the same three |

**0 of 3 declared fonts are embedded in 4 of 4 artifacts.** What IS embedded is the rendering
box's defaults -- Segoe UI is the Windows UI face and Times New Roman is the generic-serif
fallback. No Lato was present, and nothing failed: **a browser silently substitutes a missing
family and emits a perfectly valid PDF.** The declaration is a list of names with no shipper and no
checker.

Three consequences the grader should weigh, and this cell does not grade them:
1. The package declares fonts it does NOT ship. Whoever provisions the render host must install
   Lato, or the declaration must be changed to name what the host actually has. This cell holds
   neither the package nor the host provisioning.
2. `render.fonts_embedded()` exists and can answer this in one call, but NOTHING CALLS IT AS A
   GATE. A font census that runs only when someone asks is a description, not a control.
3. A substituted font changes line breaks and therefore PAGE COUNT, which is a field the receipt
   carries. Font drift is silently a pagination difference.

---

## 3. WHAT CHANGED BETWEEN TWO RENDERS OF ONE BUNDLE, AND WHY THE CONTENT HASH IS THE IDENTITY

**WHAT CHANGES: two fields, both stamped by the print engine and neither derived from the input.**
The PDF `/CreationDate` (and `/ModDate`) carry a wall-clock second, and the trailer's `/ID` is a
pair of engine-generated byte strings. Measured in round 1 on one frozen bundle rendered twice:
**25,231 bytes both times, two different raw `sha256`.** Same length, different digest -- which is
the signature of a fixed-width timestamp and a fixed-length id changing in place.

**MEASURED AGAIN IN ROUND 2 ON THE STORED OBJECTS**, as an independent instrument on the same
claim: the three `v0-11-*` objects have three DIFFERENT raw `sha256`
(`9aede5a2...`, `579b85d0...`, `6954433a...`) and ONE normalized content hash
(`b646b23012...`) -- so the normalizer removes exactly the fields that differ and nothing else.

**WHY THE CONTENT HASH IS THE IDENTITY OF THE ARTIFACT.** The question "is this the same document"
must not be answered by a digest that changes when nobody changed anything. `render.content_hash()`
zeroes the creation date and the `/ID` and hashes what remains, so two renders of one frozen bundle
are EQUAL and any change to the input is NOT.

**AND WHY ROUND 2 STOPPED USING EITHER DIGEST AS THE EXPORT'S IDENTITY.** Row `IRPT_BCKEND-W4-S12`:
round 1 keyed `export_id` on the ARTIFACT, so a byte-identical retry minted a NEW export id, which
made a retry indistinguishable from a new export. The round-2 split:

- `export_id` -- the LOGICAL identity, `sha256("irpt/export/v1|" + bundle_sha256 + "|" +
  contract_version)`, computed BEFORE any render and therefore independent of whether a render ever
  happens. Proven: 2 of 2 identical submits share `EXP-5c689ee8e1e860c4d5c32d011b01af83`; 1 of 1
  changed submit is `EXP-f4a19d4a46ec84f34c6a798552fc0a20`.
- `attempt_id` -- explicit, per render.
- the raw artifact digest -- stays in the receipt's `artifact.sha256`, where an artifact hash
  belongs, and is not an identity at all.

The content hash and the logical export id answer DIFFERENT questions -- "are these the same bytes
of output" and "is this the same export" -- and round 1's defect was using one answer for both.

**ONE FURTHER OBSERVATION, FILED AS ROW `IRPT_BCKEND-W4-S19` AND REPEATED HERE BECAUSE IT BEARS ON
THE GRADE OF ROUND 1, NOT ROUND 2:** the three `v0-11-*` exports were built from THREE DIFFERENT
bundles (round-1 battery: bundle digests `38753e307c2e`, `86c38f465c00`, `9f89d01d4fa7`) and their
rendered PDFs are CONTENT-IDENTICAL -- one content hash, and an identical decompressed
content-stream length (71,944 bytes) across all three. A renderer whose output does not vary with
its input cannot be evidence that the input was rendered. The round-1 fixture renderer is retired
from the render path in this commit for independent reasons; this is the measurement that says the
retirement was not merely tidy.

---

## 4. WHAT THE EXCLUSION PROOF DOES NOT COVER

The inventory and the per-reader census are in `RT8_synthetic_pdfs_inventory.md`: 5 of 5 objects
`EXCLUDED_BY_BOTH`, 4 of 4 readers admit 0 of 5, and the ordinary-object control shows
`export_status` and `download` still admit 1 of 1. **Here is what that does NOT establish.**

1. **A READER ADDED LATER IS NOT COVERED -- the criterion names this and it is true.** The four
   readers are a list this cell wrote by recall. Nothing in the estate forces a fifth to call
   `exclusion.is_excluded`: there is no type, no decorator and no gate. The next export-listing
   handler will be correct only because its author remembers.
2. **A READER OUTSIDE THIS REPOSITORY IS NOT COVERED AT ALL.** The portal's own fetch, an Athena or
   Glue read over the bucket, an S3 Inventory report, a lifecycle rule, and a human at the console
   all address these keys and none of them imports a Python module. Anyone who opens the bucket
   sees four PDFs that look like 49 Financial reports; the metadata says otherwise only if read.
3. **THE KEY PREDICATE IS AN ENUMERATION AND ENUMERATIONS LAPSE SILENTLY.** `SYNTHETIC_GENERATIONS`
   is a literal tuple. This cell's own generation was missing from it for one run
   (row `IRPT_BCKEND-W4-S18`) -- the exclusion proof's blind spot was demonstrated BY the exclusion
   proof. The `*SYN` suffix rule and the metadata predicate are the mitigations, and the metadata
   predicate only helps where something stamps the metadata.
4. **THE POPULATION WAS CHOSEN BY THE PROVER.** The census reads two prefixes this cell named. An
   object synthetic in fact and unlabelled by both predicates, under a third prefix, would not
   appear in the denominator -- and a narrow denominator is how an exclusion proof passes over the
   objects it missed.
5. **EXCLUSION IS NOT ABSENCE.** The objects still exist and still `head-object` 200. Deletion is
   Andrew's word and is carried on the proof instance unexercised. Until it is taken, the estate's
   position is "production reads will not surface them", not "they are gone".
