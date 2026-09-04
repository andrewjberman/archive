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
| `s3:PutObject` | `opal-security-evidence/cases/*/actions.jsonl` | **CONDITIONAL -- only if the CLI appends its audit line to the case file.** If the audit lives solely in the table row, this pair is NOT required and granting it would be over-permissioning. **Resolve against source before verdicting.** |

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
