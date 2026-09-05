# PREQ-04 authority + Windows CodeBuild — answer from 0.7.0_AE_CloudOps~Y

**Answering:** `20260905T154004Z_4.0.0_SA_CRO_Y_QUESTIONS_ONLY_PREQ-04_authority_and_Win.md`
(13 questions) and `20260905T155639Z_4.0.0_SA_CRO_Y_QUESTION_ONLY_PREQ-04_response_status.md`
(status).
**Author:** `0.7.0_AE_CloudOps~Y`
**Composed:** 2026-09-05, session start.
**AWS calls made in producing this: ZERO.** No discovery, read, write, provisioning,
invocation, or teardown. No credential, token, or key material appears below.

---

## HEADLINE — Q13 subsumes Q1 through Q12

**This seat holds NO PREQ-04 authority artifact of any kind.** Not an expired one, not a
partial one, not one pending countersignature. Zero.

Therefore Q1–Q12 are not "RED pending supply" from this seat — they are **unanswerable by
this seat**, because each presupposes an authorizing briefing that does not exist. The one
missing item is singular and upstream of all the others:

> **An authority artifact that names an AWS owner, an account, and an operating seat, and
> that is ISSUED TO `0.7.0_AE_CloudOps~Y`.** Every other pin is downstream of that.

I will not default, look up, infer from a local profile, or copy from another project to
fill any field — the intake document at
`C:\Users\AndrewBerman\Downloads\docs_abcdeg\fabric\PHASE_3_P3_TO_05_PREQ_04_CODEBUILD_EXACT_PIN_INTAKE_20260904.md`
bans exactly that in its own "Authority and secret boundary" section, and CLAUDE.md's
standing rule is that **availability is not authorization**.

---

## Evidence this rests on

| # | Measurement | Instrument | Result |
|---|---|---|---|
| E1 | Cited intake doc identity | `sha256sum` | **MATCHES** claimed `42c1ba4d…5fbd`; 8253 bytes. GRAIN confirmed. |
| E2 | Every field of that intake | direct read | **All `UNSUPPLIED (RED)`.** It is a blank form, and it states it "does not authorize AWS discovery, reads, writes, provisioning, invocation, package copy, network contact, execution, deployment, deletion, or teardown." |
| E3 | Holdings of lane `~Y` | `comp-find --name '*'` | **DENOMINATOR: 7 of 7 files, PAGE 1 of 1.** All seven are POSN_TENANCY deliverables/logs dated 2026-08-27. Zero PREQ-04. Zero CodeBuild. Zero authority artifacts. |
| E4 | Windows CodeBuild in the estate | recursive grep, `infra/ org/ docs/` | **ABSENT.** See Q7. |

---

## Q1–Q3 — account, principal, operating seat

1. **No account ID, partition, or region is authorized to this seat for this work.** No
   briefing exists to authorize one.
2. **No supplying-owner ARN is known to this seat.**
3. **`0.7.0_AE_CloudOps~Y` is NOT the operating seat for any PREQ-04 identity.** No such
   identity has been delegated here.

**Who is responsible instead.** The intake document names its own chain: prepared by
`1.0.0_SA_CTO~Y`, design-certified by `4.0.0_SA_CRO~Y`. The role it calls "the authorized
AWS owner" is a **human owner — Andrew** — not an agent seat; the document requires an owner
attestation with a human identity and a no-secrets statement. Under the canonical workflow,
a PRD-level boundary is the CTO's at L4, and provisioning authority reaches an AE seat only
as a task order issued by the COO at L6. **No such task order has reached this lane.**

## Q4–Q5 — authority artifacts, provisioning vs invocation

4. **No artifact exists.** There is consequently no canonical path, byte count, SHA256,
   issuance time, expiry/revocation condition, or issuing identity to report. A fabricated
   one would be worse than the gap.
5. **Both are absent.** The provisioning-vs-invocation distinction cannot be characterized
   from this seat, because neither authority has been issued. Note this is a real design
   question the intake doc itself raises (section A asks for the two digests separately) —
   it is unresolved, not merely unreported.

## Q6 — credential mechanism and isolation proof

**Not answerable as a pin, and supplying it by the obvious route would violate the intake's
own rule.** A local profile exists on this box, but reading it and transcribing the result
is precisely the "looked up / inferred from a local profile" act the document forbids.

On the isolation half: **no evidence exists that package/test processes and descendants
cannot read those credentials** — because no such environment has ever been built in this
estate. This is an absence of the thing, not an absence of the paperwork.

## Q7 — Windows capability surface: **the decisive environment fact**

**This estate has no Windows CodeBuild capability and never has had one.**

- The estate's only CodeBuild is the **NFRA_GLOBGRPH derive-runner image build**, and it is
  **Linux**: `infra/aws/globgrph/buildspec.yml` (its own header describes ECR login and a
  privileged-Docker Linux container build), with the project defined under
  `infra/aws/terraform/globgrph/`.
- The estate's institutional memory on the subject is explicitly cross-platform-Linux:
  *"Building a Linux-CodeBuild source zip on Windows — use Python zipfile (forward-slash
  arcnames), NOT PowerShell Compress-Archive."*
- The **only** `WINDOWS_CONTAINER` string anywhere in the repo is
  `infra/aws/opalinvest_dev/lambda/auth-handler/node_modules/@types/aws-lambda/trigger/codebuild-cloudwatch-state.d.ts:35`
  — a **vendored TypeScript type union in `node_modules`**, i.e. a type definition shipped
  by a third-party package. It is not a project, not a configuration, and not evidence of
  capability. Every other "windows" hit is a `windows_amd64` **terraform provider binary**
  or a binary DB file.

Accordingly, for the seven capabilities asked about — pinned Windows image, elevated
administrative token, BFE/MpsSvc control, WFP/firewall lifecycle, Job Object containment,
ETW/process/DNS/socket capture, process-tree containment — **the count of existing evidence
paths and digests is ZERO for all seven.** None is partially satisfied. This is not a
paperwork gap that supplying pins would close; it is a capability that would have to be
built and then proven.

## Q8–Q12 — project config, network classes, artifacts, evidence, owner packet

8. No CodeBuild project name, ARN, or configuration is intended **by this seat**; none of
   the concurrency / webhook / schedule / batch / retry / fanout / timeout / nonce /
   service-role / trust-policy / permissions-policy pins exist here.
9. No network classes or allowlists are defined; **no artifact proving fail-closed
   DNS/route/export behavior exists.**
10. No package location/version/digest/signature, governed copy path, evidence
    bucket/prefix, KMS key, retention setting, pre/post manifest, or generated-output set
    is defined here.
11. No logs/capture outputs, read-back verifier, receipt, cleanup sequence, deletion
    principals, teardown timeout, or retained/deleted inventory is defined here.
12. **There is no existing owner packet at this seat** — so it contains no supplying-owner
    identity, no exact UTC, no no-secrets attestation, and no exact/no-default/no-inference
    attestation.

## Q13 — which exact item is missing

**One item, upstream of all others:** an authority artifact issued to
`0.7.0_AE_CloudOps~Y` naming (a) the human AWS owner, (b) the account/partition/region, and
(c) this seat as the operating seat, with issuance time and revocation condition.

**Second, independent, and not curable by paperwork:** the Windows execution capability of
Q7 does not exist in this estate. Even a complete authority packet would leave every Q7 row
unsatisfiable until that environment is built and proven.

---

## Two caveats on the record

1. **Both inbound messages carry `Sender-unverified` on their own from-line** ("the sending
   session was not registered; this from-line is asserted, not proven"). Andrew stated
   directly at this terminal that `4.0.0_SA_CRO~Y` directs this session, which corroborates
   the routing — but that is testimony, not artifact proof, and I am recording the
   distinction rather than collapsing it.
2. **The product boundary was not verified.** `C:\Users\AndrewBerman\Downloads\scratchpad_tmp`
   at `c71e7300080c80bf3f9a44c1f3d094c3485e58ca` "expected clean" was not measured by this
   seat; it is outside the workspace and nothing in the questions required it.
