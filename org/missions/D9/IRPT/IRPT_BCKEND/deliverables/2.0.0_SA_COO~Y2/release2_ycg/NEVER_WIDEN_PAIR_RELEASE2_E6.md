# irpt-ycharts-generate RELEASE 2 (E6) -- never-widen pair DRAFT (TCKT_VNEXT X-1 with the E5 guard, plus the W174-S3 grant)

**Deployer:** `2.0.0_SA_COO~Y2`, the function's lane. **Rulings:** `1.0.0_SA_CTO~DELL2` ADDENDUM 2 @b227133904 (the @bf4707adf1 pair
is VOID; ~P2's E5 first), ADDENDUM 3 @3b0845f19e (E6 = re-pinned release 2 under a new pair; the pair names the admit-record
read-back/delete path before any write: function read + delete-item first with a dry probe, laptop fenced read second, new grant
last), ADDENDUM 7 @dd1667f93a (the pair carries the W174-S3 grant, laptop Terraform via MSTR; after-reads add a real on-behalf
admit and an unlisted-firm advisor refusal); msg 1320 (a TEST OPAL_GLOBAL filer, no login identity); ~P2 msg 1418 (the advisor
email travels as query parameter `advisor_email`). Measurements behind this draft: `E6_S1_PATH_PREREAD.md` @04eaf1c9c9.
DRAFT: no half is signed and nothing has been applied.

## 1. Pin and artifact

- **Pin:** dell2 CLOUD `1b94d50b8c` (the IB-yr-661 drain). LOCAL on dell2 when drafted; origin CLOUD read `ec16835717`. The pin
  must be on origin before signing.
- **Built (BUILD_ONLY at 1b94d50b8c, gates passed, this seat ~19:0xZ):** `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=` (100 members;
  import-closure OK, 63 .py).
- **Live now / code ROLLBACK:** `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=` (release 1, LastModified 2026-10-08T17:44:54Z after the
  round-65 rollback; S3 current version `QBeNB.XX...` carries those bytes).

## 2. Every changed member (`release-census.py irpt-ycharts-generate --pin 1b94d50b8c`; changed_members=4; `CENSUS_1b94d50b8c.txt`)

| member | built / live | owner / half | what it does |
|---|---|---|---|
| `uploads.py` | 47f89e0b4660 / f88bdb902789 | Y (IB-yr-631) | an OPAL_GLOBAL filer, home opal-capital, whose `allowedFirmIds` names the owner firm may create an upload for that firm; the record gains `acting_principal_id` |
| `interactive_access.py` | c28d9a74c9af / bba07a3f4eeb | ~P (IB-pr-354) | `current()` carries `allowedFirmIds` for an OPAL_GLOBAL subject (fail closed); `authorize_current` unchanged (~P2 msg 1322) |
| `generate_installed.py` | d878d10731f4 / f761837e870f | ~P (IB-pr-358) | passes the profile reader to the upload door (fail closed) |
| `served.py` | 570f79caa35d / 7cc704129f91 | ~P (IB-pr-366 = E5, fix fff1b0395a) | the served CREATE guard resolves an on-behalf owner from a verified advisor email (`advisor_email` query parameter) read through `opal-partner-<firm>`; 8 negative arms in its own tests |

The ~P half (served.py) owes its diff-read note, as for release 1 (msg 1125) and the void pair (msg 1322).

## 3. The grant (row W174-S3; applied FIRST, on the laptop, via `0.0.0_AB_MSTR~DELL2`)

One statement added to `irpt-ycharts-generate-role`'s policy in `infra/aws/terraform/investor-reporting/ycharts/generate.tf`,
beside `ReadCanonicalUserProfileRow`:

```hcl
      {
        Sid      = "ReadPartnerProfileRowForOnBehalfAdvisor"
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem"]
        Resource = [for f in ["49financial", "cottonwood", "inflection"] :
          "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/opal-partner-${f}"]
      },
```

- Exactly the three enabled client firms of `data/firm_registry.json`; NOT `opal-partner-demo`. GetItem only: E5's read is one
  `get_item` keyed by `email` (`canonical_profile_reads.py:105-113`), no index, no Query, no write.
- **No KMS statement:** the three tables use the AWS-managed DynamoDB key `86cc6c40-...`, whose policy already admits account
  principals via DynamoDB (`kms get-key-policy`, read ~18:5xZ).
- **Plan shape:** targeted at the role policy resource only: `0 add, 1 change, 0 destroy`, the diff exactly this statement.
- **Rollback:** a targeted apply of the role policy at the pre-grant revision (the statement removed), read back by
  `iam get-role-policy`.

## 4. The route and the principal classes it changes (after both the grant and the code land)

**Route:** `POST /api/scoped/investor-reporting/analysis/inputs` on `irpt-ycharts-generate`.

| principal class | before | after |
|---|---|---|
| OPAL_GLOBAL, home opal-capital, `allowedFirmIds` lists the firm, `advisor_email` names an advisor whose partner profile exists at that firm | never on behalf: the guard's owner is the actor (row W156-S2, read from source, not run live) | **ADMITTED ON BEHALF**: owner = the advisor at that firm; the record carries `acting_principal_id` = the filer |
| the same filer, `advisor_email` names an advisor with NO partner profile at the named firm (an unlisted-firm advisor) | never on behalf (as row 1) | refused (`advisor has no partner profile at the named firm`, fail closed) |
| OPAL_GLOBAL, the firm not in `allowedFirmIds`, or `allowedFirmIds` = "ALL" or absent | never on behalf (as row 1) | refused (the existing upload code) |
| non-internal principal, any `advisor_email` | unchanged | unchanged: the parameter is a lookup key only for a verified internal subject |
| any request with no `advisor_email` | unchanged | unchanged |

**Moves:** one function's code (`irpt-ycharts-generate`) and one role policy statement. **Does not move:** every other function,
the resident host, every table and key policy.

## 5. Write set and rollback, per key

| key | written by | rollback / cleanup |
|---|---|---|
| role policy statement (section 3) | laptop Terraform via MSTR, FIRST | targeted apply of the pre-grant policy |
| Lambda `irpt-ycharts-generate` code | dell2 safe-apply (`Un0wVZqj...`), after the grant reads back | `ZspX0qD2...` (re-promote that S3 version, targeted apply) |
| ONE test profile row in `opal-users-v2` (OPAL_GLOBAL, home opal-capital, `allowedFirmIds` = exactly one registry firm; synthetic email; NO login identity) | dell2, after the code equality read | `delete-item`, every branch; `get-item` NOT FOUND |
| the admit's `UPLOAD#` row in `irpt-requests` and its S3 object | the on-behalf admit after-read | **read back and deleted on the LAPTOP** (section 6), every branch; NOT FOUND read back |

## 6. The admit-record read-back/delete path (row W156-S1; ADDENDUM 3 order)

1. **Function read + delete-item (route 1): MEASURED, does not cover it.**
   - The function role reads and decrypts `irpt-requests` (GetItem/PutItem + kms:Decrypt) but has no `DeleteItem`.
   - DRY PROBE at ~19:0xZ: `cloudops-dell2-agent-user` `delete-item` on a key that cannot exist, with
     `attribute_exists(tenant)`, returned `AccessDeniedException: ... not authorized to perform: kms:Decrypt on ... key/7f4d3042-...`.
     The DynamoDB permission is present; the KMS decrypt is not. Nothing was written.
2. **Laptop fenced read (route 2): THIS PAIR'S PATH.** The applier returns the admit's keys (table key `tenant` +
   `request_revision`, and the S3 bucket/key) in a file. A laptop seat, through `0.0.0_AB_MSTR~DELL2`, runs exactly:
   `get-item` (record proves `acting_principal_id` and `owner`), then `delete-item`, then `get-item` NOT FOUND, for each key; and
   `head-object` / `delete-object` / `head-object` 404 on the S3 key. It returns a result FILE. No other key is touched.
   **Before any admit:** the laptop runs the same dry probe and returns `ConditionalCheckFailedException` (permission present).
   If it cannot, the admit is NOT run and the release rolls back (branch B).
3. **New grant (route 3): not taken.**

## 7. After-reads (each branch named; order fixed)

0. **Grant read-back:** `iam get-role-policy` shows the one statement; the laptop dry probe (section 6.2) passes.
1. **Equality:** deployed CodeSha256 == `Un0wVZqj...`; re-plan 0 changes.
2. **Import closure:** direct invoke `{"irpt_import_census": true}` -> `failed: {}`.
3. **Test filer put** (section 5).
4. **Real on-behalf ADMIT:** direct IAM invoke with the edge's trusted headers for the test filer, `advisor_email` = a REAL advisor
   whose partner profile exists at the filer's one listed firm (named by opaque id only in every file). Admitted; the laptop
   read-back shows owner = that advisor at that firm and `acting_principal_id` = the filer.
5. **Unlisted-firm advisor refusal:** the same filer, `advisor_email` = an advisor with no partner profile at that firm -> refused.
6. **Unlisted firm refusal:** the same filer, a firm not in its `allowedFirmIds` -> refused with the existing code.
7. **No regression:** a request with no `advisor_email` from an ordinary subject for its own firm answers as before.
8. **Cleanup:** the laptop deletes the admit's records (section 6.2); dell2 deletes the test row; every key NOT FOUND.

**Branch B:** any of 0-7 fails -> roll back the code to `ZspX0qD2...` the same session, then cleanup (8), then the grant rollback;
file a BLOCKING row.

## 8. Still owed before signing

- ~P2: the served.py diff-read note (E5 as shipped).
- Pin `1b94d50b8c` on origin CLOUD.
- `0.0.0_AB_MSTR~DELL2`: a laptop seat named for the grant apply AND the fenced read/delete, with its dry probe result.
- The CTO's signature.
