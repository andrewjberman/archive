# DEC-4(ii) amended evidence clause -- LGIC_ENFORCE round 4, cell EN-d-26, ruling R-30

**This is a DELIVERABLE, not the PRD.** `prd/LGIC_ENFORCE_PRD.md` is `1.0.0_SA_CTO`'s surface (L4); this
worker's grant does not include it. The text below is written so the CTO can lift it VERBATIM into
DEC-4(ii)'s evidence clause. A one-line note below marks where the lift lands; making the edit to the PRD
itself is the CTO's act, not this worker's.

## Where it lands

DEC-4(ii) ("Existing writers first") currently states that cell E1 enumerates every principal that read or
wrote each firm bucket "from the CloudTrail data events card 3 made live on opal-data-bd, -inf, -cot and
-49financial". That sentence is the ONE evidence path DEC-4(ii) names for a `NOT_A_PRINCIPAL` disposition.
Round 3 measured that `opal-data-demo` sits in neither CloudTrail data-event selector this estate declares
(`LGIC_ENFORCE-W2-S12`), so on that bucket the named evidence path can never answer true or false. R-30
rules the fix as an amendment to this evidence clause, not an apply against the bucket.

## The amended text (insert as a new paragraph immediately after DEC-4(ii)'s existing evidence sentence)

> **The evidence rule, amended (R-30).** A `NOT_A_PRINCIPAL` disposition on a bucket that is **not** a
> member of a live CloudTrail **data-event** selector -- neither the organization trail's ReadOnly S3
> data-event selector (`infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf`,
> `local.org_trail_read_logged_buckets`) nor the served-key write trail's WriteOnly S3 data-event selector
> (`infra/aws/terraform/globgrph/item2e_served_write_trail.tf`, `local.served_write_trail_buckets`) names
> it -- is REFUSED. The prescribed CloudTrail evidence path cannot answer for a bucket neither selector
> ever covered, and a query against an uninstrumented bucket can only ever return zero for the trivial
> reason that nothing is recorded there, never because the instrument observed a true absence.
>
> On such a bucket the disposition instead comes from one of two remaining paths:
> - a **direct IAM-grant read**: `EXEMPTED` when a live, currently-scoped grant names the principal on the
>   bucket (the policy statement cited, not merely asserted); or `NOT_A_PRINCIPAL` cited to the **absence**
>   of any such grant across the role's attached and inline policies (each read and quoted, not asserted);
> - or, when neither a data-event trail nor a direct IAM-grant read can answer for the name, it is carded
>   **NOT-JUDGED** with the missing-instrument reason stated (which instrument is absent, for which
>   bucket).
>
> **Silence in a trail that never covered the bucket is never evidence.** A clean zero-count CloudTrail
> query against a bucket absent from both data-event selectors reads exactly like a genuine negative and
> must not be graded as one.

## Provenance

- Ruling: `org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260916.md` R-30
  (2026-09-17 ~17:4xZ), all four parts.
- Row disarmed by rule, not by instrumenting the bucket: `LGIC_ENFORCE-W2-S12`
  (`org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`), disarm owner
  moved to `1.0.0_SA_CTO` per R-30(3).
- Trail declarations read at this cut:
  `infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf:46-51` (org trail's ReadOnly S3
  data-event selector, `local.org_trail_read_logged_buckets = [opal-data-49financial, opal-data-bd,
  opal-data-cot, opal-data-inf]`), `infra/aws/terraform/globgrph/item2e_served_write_trail.tf:30`
  (served-key write trail's WriteOnly S3 data-event selector, `local.served_write_trail_buckets =
  [opal-data-inf, opal-data-bd, opal-data-cot]`). `opal-data-demo` is a member of neither.
- Guard that mechanizes this text: `fence_disposition_check.py`, this same deliverables folder.
- R-30(4): instrumenting `opal-data-demo` is explicitly NOT ordered by this text or this cell; nothing
  live moves here.
