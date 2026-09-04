# TO-OP-S-22 PHASE 1 -- the action/resource pairs each sentinel-chain role must and must not have

**Seat:** `0.7.0_AE_CloudOps~W` · **Face:** `NFRA_OPSEC202609.TO-OP-S-22` · **Written:** 2026-09-04 ~01:1xZ
**Phase-1 mandate:** *"Read each role's ACTUAL code to derive the action/resource pairs it needs. A
verdict against a guessed permission list verdicts the guess."*

---

## ⛔ READ THIS FIRST -- THIS LIST IS SPEC-DERIVED, NOT CODE-DERIVED, AND THAT IS A REAL LIMIT

**The phase-1 mandate cannot be executed as written, because none of the three roles' code exists yet.**
Measured, not assumed:

| probe | result |
|---|---|
| `comp-find 'opal-ipset-reconciler\|opal-security-sentinel\|ipset_reconciler\|opsec-unblock'` | **11 hits across 51,747 files, ALL of them spec** -- PRD, decomp, task orders, inbox messages. **Zero implementation files.** |
| positive control, same instrument: `comp-find 'def lambda_handler'` | **474 hits.** The probe finds Lambda source when it is there, so the zero above is a real absence and not a broken query. |
| `aws iam list-roles`, full enumeration | **221 roles.** `ipset` 0, `reconcil` 0, `sentinel` 0, `unblock` 0. The only `opal-security*` matches are `opal-security-admin` (C-14's, created today) and `opal-security-scanner-processor-role` (March, unrelated). |
| positive control on that census | `lambda-execution-role` and `opal-portal-lambda-role` both found -- the probe sees roles that exist. |

⚠ **THE ROLE DENOMINATOR WAS NEARLY PUBLISHED WRONG.** A first pass used
`aws iam list-roles --query 'length(Roles)'` and got back **`100 / 100 / 21`** -- three values, because
the CLI auto-paginates and `length()` is applied PER PAGE. Reading the first number would have stated
**100 roles when the truth is 221**, a 2.2x understatement, on the very read that grounds an ABSENCE
claim. Counted client-side over the merged list instead. This is CLAUDE.md Rule 22a's named trap and it
fired on the first attempt.

**SO: every pair below is derived from the RATIFIED DESIGN** (PRD 7.2-7.3 @`3619ebecd9`, the S14/S15/S19
manifest rows, and the C-2/C-5/C-7/C-11 constraints), **not from source.** That is strictly weaker than
what the face asks for, and it is labelled rather than glossed.

⛔ **THIS LIST MUST BE RE-DERIVED AGAINST SOURCE BEFORE ANY VERDICT IS FILED.** A spec-derived list is a
better-informed guess, but it is still a guess: it cannot see a helper call the design never mentioned
(an SSM parameter read, a metric put, a second bucket), and *those* are precisely the pairs an
over-permissioned role gets padded with. The value of writing it now is that the moment an ARN lands the
simulation is mechanical -- **not that the verdict is pre-decided.**

---

## RESOLVED RESOURCE ARNs -- taken live so the simulations need no lookup later

```
TABLE      arn:aws:dynamodb:us-east-1:313476888478:table/opal-suspicious-addresses
STREAM     arn:aws:dynamodb:us-east-1:313476888478:table/opal-suspicious-addresses/stream/2026-09-03T08:29:37.404
           (StreamEnabled true, NEW_AND_OLD_IMAGES -- as C-2's design requires)
CMK        arn:aws:kms:us-east-1:313476888478:key/64f25291-4015-42c5-ad41-40e42325deb7  (alias/opal-security)
EVIDENCE   arn:aws:s3:::opal-security-evidence          (EXISTS, head-bucket)
LOGDEST    arn:aws:s3:::opal-data-security              (EXISTS, head-bucket -- NOT this chain's write target)
```

### ⚠ THE IP SETS ARE **FOUR**, NOT THE "TWO SETS" THE FACE AND THE PRD SAY

```
arn:aws:wafv2:us-east-1:313476888478:global/ipset/opal-blocked-ips-cloudfront/b2e008a6-40d9-4d07-bef5-1caa8b682bb3
arn:aws:wafv2:us-east-1:313476888478:global/ipset/opal-blocked-ips-cloudfront-ipv6/eb1a0caa-60a0-492e-a685-e5456cea8b7d
arn:aws:wafv2:us-east-1:313476888478:regional/ipset/opal-blocked-ips-regional/f073f448-eb85-4d23-9306-0cadf4573331
arn:aws:wafv2:us-east-1:313476888478:regional/ipset/opal-blocked-ips-regional-ipv6/85f90377-7cba-45dd-baca-397310d61f8e
```

`S22-AC3` is written as *"the reconciler ALLOWED `wafv2:UpdateIPSet` on **both sets**; the CLI and the
sentinel DENIED the same action on the same resources."* **The applied plane carries four.** PRD S18
says `opal-blocked-ips-{scope}` **x2** and separately `/32` v4, `/64` v6 -- the v6 siblings are the
built realisation of that, and `TO-OP-S-4-18` (complete) made four. Row `Z-S102` already refers to the
cloudfront set "and its IPv6 sibling", so four is known to the project; what is new is that **a verdict
written to "both sets" would cover 2 of 4 and read as complete.**

**Therefore this face's C-2/C-11 verdict runs against all FOUR ARNs per role, denominator printed as
4.** Since `UpdateIPSet` is the single action C-2 turns on, an unverdicted IPv6 set is a hole in exactly
the invariant the chain rests on -- an attacker's `/64` is written to the v6 set or to nothing.

---

## ROLE 1 -- `opal-sentinel` (S14, cell OP-s-14, owner `0.7.0_AE_CloudOps~S` via TO-OP-S-14-21)

*Design: subscription filter -> parse -> per-address counter -> ALLOW-list check -> WATCH or BLOCK row
-> case file -> one SES email per address per 24 h -> daily digest file.*

### MUST HAVE
| action | resource | why, from the design |
|---|---|---|
| `dynamodb:PutItem` | TABLE | writes the BLOCK row (status, why, since, expires_at, case_id) |
| `dynamodb:UpdateItem` | TABLE | WATCH path: increments `hits`, updates `last_seen` |
| `dynamodb:GetItem` | TABLE | reads the existing row before deciding WATCH vs BLOCK |
| `dynamodb:Query` | TABLE + `status-index` | ALLOW-list check (C-4: never override an ALLOW row) |
| `s3:PutObject` | `opal-security-evidence/cases/*` | `summary.json`, `waf-samples.jsonl`, `timeline.md`, `actions.jsonl` |
| `s3:PutObject` | `opal-security-evidence/reports/daily/*` | the daily digest FILE (C-6: a file, not an email) |
| `s3:GetObject` | `opal-security-evidence/allowlists/partner-egress.json` | read at cold start, per PRD 7.3 |
| `kms:GenerateDataKey`, `kms:Decrypt` | CMK | the table AND the evidence bucket are both CMK-encrypted; without these every write fails at the KMS layer, not the service layer |
| `ses:SendEmail` | the existing auth-handler SES identity | C-6, and C-6 says **no new sender identity** |
| `logs:CreateLogStream`, `logs:PutLogEvents` | its OWN log group | ordinary Lambda execution |

### MUST NOT HAVE -- these are the positive controls for `S22-AC2`
| action | resource | which constraint |
|---|---|---|
| **`wafv2:UpdateIPSet`** | **all four IP sets** | **C-2 -- the invariant. The sentinel decides; only the reconciler enacts.** |
| `dynamodb:DeleteItem` | TABLE | nothing in the design deletes a row; expiry is TTL + a status flip |
| `s3:DeleteObject` | `opal-security-evidence/*` | C-8 + versioning: evidence is append-only in intent |
| `kms:ScheduleKeyDeletion`, `kms:PutKeyPolicy` | CMK | never a data-plane principal's |

---

## ROLE 2 -- `opal-ipset-reconciler` (S15, cell OP-s-15, owner `0.7.0_AE_CloudOps~T` via TO-OP-S-15-19)

*Design: DynamoDB stream (NEW_AND_OLD_IMAGES) -> BLOCKED insert/modify = UpdateIPSet add; ALLOW /
EXPIRED / TTL remove = UpdateIPSet remove; plus a once-daily full reconcile. C-7: idempotent.*

### MUST HAVE
| action | resource | why |
|---|---|---|
| `dynamodb:DescribeStream`, `GetRecords`, `GetShardIterator`, `ListStreams` | STREAM | the event source |
| `dynamodb:Scan` **or** `Query` on `status-index` | TABLE + index | the once-daily FULL reconcile; `Query` on the GSI is the tighter grant and is preferred if the code allows |
| **`wafv2:UpdateIPSet`** | **all four IP sets** | **C-2: this role, and only this role** |
| `wafv2:GetIPSet` | all four IP sets | `UpdateIPSet` requires the current `LockToken`; without Get the update cannot be formed. **Easy to omit and it fails at first invocation, loudly** |
| `kms:Decrypt` | CMK | stream records from a CMK-encrypted table |
| `logs:CreateLogStream`, `logs:PutLogEvents` | own log group | ordinary execution |

### MUST NOT HAVE
| action | resource | which constraint |
|---|---|---|
| **`dynamodb:PutItem` / `UpdateItem` / `DeleteItem`** | **TABLE** | **C-2 read in its own direction: the table is TRUTH and the IP set is its PROJECTION. A reconciler that can write back to the table can manufacture the truth it is supposed to be enacting, and the drift would be self-confirming.** |
| `ses:SendEmail` | any | notification is the sentinel's, and the moratorium binds |
| `s3:PutObject` | `opal-security-evidence/*` | case files are the sentinel's |

---

## ROLE 3 -- the unblock CLI `.tools/opal-ipblock` (S19, cell OP-s-19, owner `0.7.0_AE_CloudOps~T`)

*Design: `opal-ipblock allow <addr> --reason "..."` -- audited, flips the ROW, `--reason` mandatory.*

### MUST HAVE
| action | resource | why |
|---|---|---|
| `dynamodb:UpdateItem` | TABLE | flips `status` to ALLOW and writes `unblocked_by`, `unblocked_at`, `notes` (the mandatory `--reason`) |
| `dynamodb:GetItem` | TABLE | read the row before flipping, so the CLI can refuse an address it does not hold |
| `dynamodb:Query` | TABLE + `status-index` | listing blocked addresses for the operator |
| `kms:GenerateDataKey`, `kms:Decrypt` | CMK | CMK-encrypted table |
| ~~`s3:PutObject`~~ | ~~`opal-security-evidence/cases/*/actions.jsonl`~~ | **RESOLVED 2026-09-04 ~01:33Z -- NOT REQUIRED, NOT GRANTED.** Settled against source by `0.7.0_AE_CloudOps~T` (msg 20089): the row already carries `unblocked_by`, `unblocked_at` and `notes`, and the address IS the partition key, so `S19-AC3`'s actor/address/reason/timestamp all fit with no S3 write. The repeat-unblock history gap (a row holds only the LATEST) is closed by a repo-side append-only audit log, this estate's existing convention -- durable history at ZERO additional AWS permission. **The conditional is discharged; granting this pair now would be exactly the padding this cell exists to catch.** One reading could still reopen it -- see the C-8 question below. |

### MUST NOT HAVE -- the C-11 control
| action | resource | which constraint |
|---|---|---|
| **`wafv2:UpdateIPSet`** | **all four IP sets** | **C-11, stated in the face in terms: "an AUDITED CLI that edits the ROW, NEVER the IP set." An unblock that touches the set directly bypasses the table and breaks C-2 in the same stroke.** |
| `dynamodb:DeleteItem` | TABLE | an unblock is a status flip, never a row deletion -- deleting loses the audit trail the `--reason` exists to create |

---

## WHAT THE VERDICT WILL NOT COVER -- drafted now for `S22-AC4`

`simulate-principal-policy` evaluates **identity-based policies plus the permission boundary and SCPs
it can see for the principal.** It does **NOT** evaluate:

- **Resource policies** -- the S3 bucket policy on `opal-security-evidence` (which denies any principal
  outside the sentinel / reconciler / `opal-security-admin`) and the **KMS key policy** on the CMK.
  ⭐ **This matters concretely here:** the CMK's `AllowViaDynamoDBAndS3InThisAccountOnly` grants via
  `kms:ViaService` for dynamodb and s3 **only**. A role calling KMS *directly* is not covered by that
  statement, so an identity-policy `allowed` for `kms:Decrypt` can still fail in production. Verified
  first-hand on this key earlier tonight under TO-OP-S-8R2B.
- **Service control policies** not visible to the simulator, and session policies.
- **Whether the code actually makes the call.** An allowed pair is not an exercised pair.

**Context entries to supply (`S22-AC4`):** any statement conditioned on `kms:ViaService`,
`aws:SourceAccount`, or `aws:SourceArn` needs its key supplied or the simulation returns an
`implicitDeny` **byte-identical to a real deny**. Each will be stated with its value and its reason.

---

## HANDOVER -- what the two owning faces can use before they apply anything

This list is being sent to `0.7.0_AE_CloudOps~T` (reconciler + CLI) and `0.7.0_AE_CloudOps~S`
(sentinel) **before their role applies**, deliberately: the cheapest moment to catch an
over-permissioned role is before it is written, and this cell exists because
**an over-permissioned role fails never.**

⛔ **This face does NOT edit any role's policy** (deliverable 4). These tables are an input to the
owning faces and a verdict target for this one -- never a patch.

**Two things each owner should push back on if the source disagrees:** the reconciler's
`wafv2:GetIPSet` (needed for the LockToken, easy to omit) and the CLI's conditional
`s3:PutObject` on `actions.jsonl` (grant it only if the code writes there).

---

# ADDENDUM 2026-09-04 ~01:4xZ -- WHAT WAS ACTUALLY BUILT, so the verdict grades the BUILT thing

`0.7.0_AE_CloudOps~T` DECLARED the reconciler and CLI roles at commit `3578b10a00`, in a separate file
`infra/aws/terraform/opsec/iam_reconciler_and_cli.tf` (kept separate so concurrent `iam.tf` edits by
`0.7.0_AE_CloudOps~S` cannot textually conflict). Plan reads **4 to add, 0 to change, 0 to destroy**;
UNSCOPED baseline on that root measured with the new file moved aside is `No changes`, rc=0.
**NOT APPLIED** -- the apply waits on the sentinel-role apply, and no function code deploys before this
verdict returns.

⛔ **THE VERDICT MUST GRADE THE BUILT POLICY, NOT THIS SPEC-DERIVED LIST.** Three deliberate divergences
are already recorded, and every one of them is TIGHTER than what this artifact specified. A verdict
run against the list above would mark two of them as gaps that are not gaps.

| what this list said | what was BUILT | reading for the verdict |
|---|---|---|
| reconciler: `dynamodb:Scan` **or** `Query` on `status-index` | **`Query` on `status-index` ONLY; `Scan` deliberately NOT granted** | C-9 requires the lockout question be answerable without a table scan, and the absence of `Scan` stops a later edit quietly reintroducing one. **Do NOT verdict a missing `Scan` as a gap.** |
| MUST-NOT pairs, expressed as omissions | **explicit `Deny` statements** -- reconciler denied `PutItem`/`UpdateItem`/`DeleteItem`/`BatchWriteItem` on the table; CLI denied `UpdateIPSet`/`CreateIPSet`/`DeleteIPSet` on every set | Strictly stronger. An omission is indistinguishable from an oversight and survives a careless widening; an explicit `Deny` cannot be overridden by any later `Allow`. It also makes `S22-AC2`'s positive controls return **`explicitDeny`** rather than `implicitDeny` -- a sharper result, and the instrument distinguishes them. |
| both roles: `kms:DescribeKey` among the KMS pairs | **REMOVED from both** | Measured first-hand by that seat: `DescribeKey` IS reachable via the `kms:ViaService` path, so the grant was not WRONG -- it was **UNUSED**, because neither role calls KMS directly. An unused grant fails never, which is this cell's whole premise, so it was removed rather than kept as harmless. Final: reconciler `Decrypt` only (it never writes the table); CLI `Decrypt` + `GenerateDataKey` (it reads and writes rows). |

## THE FOUR-SET FINDING IS CORROBORATED, AND THE PAGINATION TRAP CUTS BOTH WAYS

Two seats reached "four IP sets" independently and from opposite directions -- `0.7.0_AE_CloudOps~T`
by enumerating the applied plane to build the grant, this seat from the verdict side by noticing
`S22-AC3`'s prose says "both sets". **Two instruments on two planes agreeing is corroboration, not
repetition.**

⚠ **AND THIS SEAT'S ORIGINAL READ WAS RIGHT BY LUCK, WHICH IS WORTH RECORDING RATHER THAN GLOSSING.**
That seat reported its first `list-ip-sets` returned `NextMarker` TRUE on BOTH scopes, so the obvious
read was a PAGE. This seat's four came from exactly that unpaginated first call. **Re-verified properly
by walking `NextMarker` to exhaustion:**

```
  CLOUDFRONT  pages=2  count=2   opal-blocked-ips-cloudfront, opal-blocked-ips-cloudfront-ipv6
  REGIONAL    pages=2  count=2   opal-blocked-ips-regional,  opal-blocked-ips-regional-ipv6
  TRUE DENOMINATOR: 4
```

The count stands. **But the mechanism is worth carrying, because it misleads in BOTH directions:** page 1
was complete here, so a seat that stopped at it got the right answer for the wrong reason -- and a seat
that saw `NextMarker` present and *inferred more sets existed* would have been wrong the other way.
**A `NextMarker` is not evidence of more data any more than its absence is evidence of none.** Only
walking it settles the denominator. This estate's standing rule is "a page is not an answer"; the
mirror -- "a next-marker is not a promise" -- is the half that had not been written down.

## THE ONE OPEN QUESTION, ROUTED NOT DECIDED

`0.7.0_AE_CloudOps~T` invited pushback on exactly one point: **if C-8's case record is this framework's
audit OF RECORD, the unblock must land in `cases/*/actions.jsonl` and `s3:PutObject` becomes REQUIRED.**

**This face does not adjudicate that** -- deliverable 4 is explicit that roles belong to the faces that
declare them and this cell produces a VERDICT, never a patch. Routed to `2.0.0_SA_COO~Z`. This seat's
reading, offered as a recommendation and not a ruling:

- **Endorse NOT REQUIRED as built.** C-11 constrains the CLI to the ROW and is silent on S3; the row
  plus an append-only repo log satisfies `S19-AC3`'s four fields with strictly less privilege, and
  least privilege is this cell's entire subject.
- **ONE FORWARD RISK, named so it is not discovered later:** the repo log and the evidence bucket are
  on DIFFERENT durability and access planes. FWD-16's portal Admin page ("Security -> Blocked
  addresses -> Unblock") could not render unblock history from a repo file. The face calls that page
  an explicitly LATER increment, so this is not a defect today -- but if that page is later expected
  to show *who lifted a block and why*, the audit will have to move or be duplicated, and duplicating
  it is the two-carriers-diverge shape. **Better decided once, now, than migrated later.**
