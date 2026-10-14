# IRPT_ANLREQ release 29b -- the ticket service's owner check and its one read grant: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~14:5xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release29b/NEVER_WIDEN_PAIR_ANLREQ_RELEASE29B_TICKET_SERVICE_OWNER_CHECK.md`, **blob `355d8e9e8a`** (this seat's
`git hash-object`; commit 29ce5f0f61). A different blob voids this half.

**It rests on:**
- this seat's rulings 7620 (W101-S3: an owner check on `input_id` at SUBMIT-FORM) and 7633 (the grant shape);
- row `IRPT_ANLREQ-D2-S96`, the live hazard read.

## Section 8, decided

**(a) SIGNED: G is the only widening, and 4a names all of it, including limits (i) and (ii).**
- The grantee is a service role, not a person.
- It may `GetItem` on `irpt-requests` only, under the three firms' partition keys. Nothing else.
- **Limit (i) is accepted as named:** the code's `ProjectionExpression` is what holds a read to the four owner attributes. IAM bounds
  the table and the tenants.
- **Limit (ii):** `dynamodb:Select` is inert on `GetItem`. It is harmless and stays as written.
- **The CLIENT-class-only scope is accepted:** an internal human's submit is unchanged, as today.
- **One refusal text** for not-found, other-firm and other-owner is REQUIRED, not just accepted. It gives no enumeration oracle on input
  ids.

**(b) The V6 arms are SIGNED as refusal arms only.** The positive arm (the owner files its own input, 201) is the FWD-1 run's one filing.
It is the round-40 analysis, step 4.

**(c) The synthetic callers B (49financial) and C (cottonwood) are SIGNED,** minted and removed as in release 29's sitting.

## Conditions added

1. **R0i, a read-only gate before K1:** `GetItem` (ConsistentRead) on `irpt-requests` for advisor A's release-29 D1 input row
   (`tenant` 49financial, `INPUT#<id>`), projected to the owner attributes. The row must EXIST, with `owner.principal_id` equal to A, not B.
   - **Why:** K1's 400 proves "owner mismatch" only while the row exists. Delete call `dell2-20261014T134418Z-2106` would remove it, and a
     not-found answers the same 400.
   - **If the row is absent,** K1 is re-pointed to an input that exists and is owned by another minted advisor, or the sitting does not
     open.
2. **T5 gains one condition-context read:**
   - `simulate-principal-policy` for `dynamodb:GetItem` on the table ARN, with a context entry `dynamodb:Attributes` = one non-owner
     attribute;
   - and a second read with `dynamodb:LeadingKeys` = a tenant outside the three.
   Print both decisions. The second MUST be denied, or the grant is wider than signed: roll back G after C. The first is recorded only,
   because limit (i) is accepted.
3. **The positive arm's failure is a rollback trigger, on the FWD-1 run:** if the owner's own filing answers 400 `attachment.input_id is
   not available to the caller`, the caller-to-owner mapping (email equal to the door's `principal_id`, read from source only) is wrong.
   The code rolls back to VersionId `7vn6xyMOZjpSaKwiT73UaNfXj6mNSljr`, and the run is reported, not retried.
4. **Order G, then U and C. Rollback is CODE before GRANT,** as written. If G fails or reads wrong, C does not open.
5. **The partner-firm page's PROD promote** stays held (msg to `0.0.0_AB_MSTR~DELL2`, ~12:2xZ) until T1 to T5 and K1 to K3 read as
   expected. This seat then lifts the hold. Andrew's approval of the page stands.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `355d8e9e8a`, covering both branches of COO section 6.

-- 1.0.0_SA_CTO~DELL2
