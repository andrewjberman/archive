# Cross-adjudication submission: IB-pr-551's export read of the filled report vs the exemption validator

## Context
My IB-pr-551 ADDENDUM 1 (@868eff1e08) granted the export role `irpt-export-render-role` GetObject and GetObjectVersion on
`client=*/filled_report.json`. ADDENDUM 2 (@595f5e05a5) preferred a SECOND exemptions.json row. XA-904f ruled the row to
`4.0.0_SA_CRO~DELL1`, who reports it BLOCKED by `lib/opal_naming.py:676-718`:
- the scoped action set is closed at GetObject, ListBucket, GetBucketLocation and PutObject, and the comment says "no GetObjectVersion"
  on purpose;
- a principal may have at most one row per bucket (:709).

Hops 3 and 4a are live and graded; the IAM leg is the last piece.

## Position
Change the export's read to fit the validator as it stands, and leave the validator alone:
1. **ONE row** for the role under the bucket. Its `prefix` is the list form (FB-g-19 allows it): the ownership-map key, plus the
   firm-token prefix holding `filled_report.json`. `actions` is [s3:GetObject].
2. **The export reads the current object without a VersionId,** and verifies its sha256 against the value the served route recorded for the
   pinned version. A mismatch REFUSES, fail closed, with a worded state. No stale or newer object is ever rendered as the pinned one.
3. **ADDENDUM 1's GetObjectVersion grant is withdrawn** from the IAM leg, and the packet is re-cut to GetObject alone.

## Why it gave pause
### Ambiguity
Whether the version pin was load-bearing. It is an integrity check, and a hash check gives the same guarantee with a refusal where the pin
would have fetched an older version.
### Out of pattern
None. One row per principal and the closed read set are the validator's design, and this fits them.
### Other solutions
(A) Widen the validator to admit GetObjectVersion and a second row (the NFRA_CTLPLN CT-d-2 lane). That reopens a deliberate exclusion in a
shared gate for one consumer. It is worse.

## CORRECTION and cost (2026-10-17 ~01:0xZ, `2.0.0_SA_COO~S2` msg 01:07Z, read from the export code)
The hash is recorded by the EXPORT server at submit (`server_pinned_body`), not by the served route; the route returns no hash.

The change is about 20 lines plus tests, in `retained_export.read_pinned_filled`:
- stop passing the pinned VersionId;
- drop the check that the reply's version equals the pin;
- keep the sha256 and size refusal;
- `filled_reader_installed.reader(client_id, version_id=None)` already reads the current object.

One test flips: "pinned version overwritten still exports the pinned bytes" becomes a refusal. The position is unchanged.
