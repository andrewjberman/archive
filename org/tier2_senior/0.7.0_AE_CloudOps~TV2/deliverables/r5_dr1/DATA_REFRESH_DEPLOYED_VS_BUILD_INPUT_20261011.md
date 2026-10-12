# `opal-data-refresh-api`: the deployed package against its build input, member by member

**Read by:** `0.7.0_AE_CloudOps~TV2` | **Date:** 2026-10-11 | **Order:** `TCKT_VNEXT.TO-READ-R5-dr1` @`c4374e733d`
**Cell:** `R5-dr-1` | **Answers:** row `TCKT_VNEXT-D2-W6-S2` (ARMED, owner `1.0.0_SA_CTO~DELL2`)
**Nothing was written to AWS.** Two read calls on one function plus a package download. No invoke, no route
call, no token, no IAM, no Terraform, no ledger entry.

---

## The answer in one line

```
MEMBERS 2 EQUAL 2 DIFFERENT 0 NOT_IN_SOURCE_DIR 0
```

**The deployed bytes are byte-identical to the build input at the recorded commit, and to this tree's HEAD.**
So the rule row `TCKT_VNEXT-D2-S17` read in the tree is the rule that is *running*. The CTO's round-5
analysis item 7 made that the closing condition: "Equal closes the row; unequal comes back as a release under
a pair." It is equal.

---

## Step 1 — the live configuration

| field | value | claim |
|---|---|---|
| CodeSha256 | `qHMjXkK1/1NhmBmkK/6Q+q+WdXMRoTOprNfTixBIxaM=` | measured |
| LastModified | `2026-10-09T07:59:39.000+0000` | measured |
| Runtime / Handler | `python3.11` / `lambda_function.lambda_handler` | measured |

Matches the issuer's 19:5xZ read on the `qHMjXkK1` prefix, so no re-read of the map was owed.

**Source-map entry `opal-data-refresh-api`**, read now, not carried:

| field | value |
|---|---|
| `source_dir` | `infra/aws/lambda/data_refresh` |
| `files` | `["lambda_function.py", "check_triggered_by.py"]` |
| `artifact_sha256` | `qHMjXkK1/1NhmBmkK/6Q+q+WdXMRoTOprNfTixBIxaM=` |
| `last_deployed_commit` | `d9539cc0b76dd07758ba0d8e4f4d1fcc759b472d` |
| `last_deployed_at` | `2026-10-09T07:59:39Z` |

The map's hash equals the live hash. That was already known at the issuance; it is **not** what this read
adds. A matching hash pairs a function with an artifact — it says nothing about whether the artifact's
*content* is the named commit's files. That is what follows.

## Step 2 — the downloaded package is provably the deployed one

| field | value |
|---|---|
| zip bytes | 20716 |
| zip sha256 | `a873235e42b5ff53619819a42bfe90faaf96757311a133a9acd7d38b1048c5a3` |
| that digest, base64 | `qHMjXkK1/1NhmBmkK/6Q+q+WdXMRoTOprNfTixBIxaM=` |
| live `CodeSha256` | `qHMjXkK1/1NhmBmkK/6Q+q+WdXMRoTOprNfTixBIxaM=` — **identical** |

Downloaded into a new empty folder outside the repository. `CodeSha256` is the base64 of the package's
sha256, so this equality is what makes every hash below a statement about the **running** bytes rather than
about a file that happens to sit somewhere.

**Members: 2**

| member | size | crc32 |
|---|---|---|
| `check_triggered_by.py` | 1825 | `bb875b5f` |
| `lambda_function.py` | 83888 | `9306cc2e` |

Both are exactly the two files the map's `files` lists, so no member is `NOT_IN_SOURCE_DIR` and there is no
vendored dependency or build stamp in this package.

## Step 3 and 4 — the three planes, bytes compared, nothing normalised

| member | size | deployed | recorded commit | HEAD | verdict |
|---|---|---|---|---|---|
| `check_triggered_by.py` | 1825 | `7e813322799f4f7a` | `7e813322799f4f7a` | `7e813322799f4f7a` | **EQUAL** |
| `lambda_function.py` | 83888 | `ead1011f45b91912` | `ead1011f45b91912` | `ead1011f45b91912` | **EQUAL** |

```
MEMBERS 2 EQUAL 2 DIFFERENT 0 NOT_IN_SOURCE_DIR 0
```

Per member, all three planes agree: **deployed == recorded_commit == HEAD**.
**Built-not-deployed changes at HEAD: NONE.** Nothing is sitting in the tree waiting to ship, and the
deployed artifact is not older than its own source.

### One instrument failure, and the control that caught it

My first pass reported **both members ABSENT at the recorded commit** — `git show` rc 128, "path ... does not
exist in d9539cc0b7". That was false, and it was my own instrument.

The member names came from a Windows `python print`, so each carried a trailing **CR**. `git show` was asked
for `lambda_function.py\r` and reported it missing, rendering the CR as `?` in its error:

```
fatal: path 'infra/aws/lambda/data_refresh/check_triggered_by.py?' does not exist in 'd9539cc0b7...'
```

The positive control that CLAUDE.md requires beside any ABSENT verdict — `git ls-tree` of the directory at
that same commit — listed **both files present**, which is what exposed the contradiction. A second control
(a genuinely nonexistent path) returned rc != 0, proving the instrument can still say "no" meaningfully.

Had I omitted the control, this read would have reported `MEMBERS 2 EQUAL 0 DIFFERENT 0 NOT_IN_SOURCE_DIR 2`
— the exact shape of "the deployed package contains nothing from its source dir", which would have escalated
a non-existent release problem. The law already names this trap twice (the corruption oracle: echo the
argument back; and never `2>/dev/null` a `git show`, because the mangle returns clean-empty), so it gets no
surprise row — it is a documented hazard that behaved exactly as documented.

## Step 5 — what the DEPLOYED `validate_user_type` admits

Read from the downloaded bytes, not from the tree. Line numbers are positions in the **deployed**
`lambda_function.py` (1956 lines, 83888 bytes).

| function | deployed line |
|---|---|
| `is_opal_internal` | **142** |
| `validate_user_type` | **168** |

`is_opal_internal` (the function `validate_user_type` calls to decide "Opal-internal"), lines 142-165:

```python
OPAL_INTERNAL_TIER = 'internal'        # line 138
OPAL_INTERNAL_FIRM_ID = 'opal-capital' # line 139

def is_opal_internal(context):
    context = context or {}
    tier = str(context.get('tier') or '').strip()
    firm_id = str(context.get('firmId') or '').strip()
    if tier == OPAL_INTERNAL_TIER:
        return True
    if firm_id == OPAL_INTERNAL_FIRM_ID:
        return True
    return False
```

`validate_user_type`'s three admission paths:

```python
# Method 1, authorizer context (lines 198-220)
user_type = authorizer_context.get('userType', 'null')
if user_type == 'null':
    user_type = ''
if user_type == 'Dev':
    return True, user_email
if is_opal_internal(authorizer_context):
    return True, user_email
return False, user_email

# Method 2, JWT claims (lines 228-243) -- the SAME rule
# Method 3, no authorizer context at all (line 245) -- REFUSES, fail closed
```

**The three sentences the order asks for:**

1. **Which userType values it admits:** exactly one — the string `Dev`, by exact match. Every other
   userType value, including any unrecognised string, is admitted *only* if the principal is independently
   recognisable as Opal-internal (`tier == 'internal'` or `firmId == 'opal-capital'`).
2. **Is a caller with NO userType admitted?** **No — not on that basis.** A missing, empty or `'null'`
   userType is normalised to `''` at line 204 and then refused at line 220 unless `is_opal_internal` returns
   True. The deployed comment records what this replaced: `if not user_type or user_type == 'Dev'` used to
   admit every principal carrying no userType, and a call with no authorizer context at all was admitted as
   `dev@test.com` by a "development fallback". Both paths are closed in the deployed bytes.
3. **Is a caller with tier `internal` and any userType admitted?** **Yes.** `is_opal_internal` returns True
   on `tier == 'internal'` before userType is consulted again, so an Opal-internal principal is admitted
   whatever its userType — including none.

Two details in the deployed bytes worth keeping, both defensive rather than gaps:

- `firmId` is compared by **exact match**, never by truthiness, because the authorizer defaults it to the
  *string* `'null'` when the claim is absent — `if firm_id` would be True for that string.
- Method 3 fails **closed**. An unauthenticated call is refused and says so in its log line, where it
  previously returned True as a fictional actor.

---

## What this read does and does not settle

**Settles:** the deployed function carries the rule, byte for byte, that row `TCKT_VNEXT-D2-S17` read in the
tree. A caller with no userType is **not** admitted by the absence of a userType. That is the question row
`TCKT_VNEXT-D2-W6-S2` armed.

**Does not settle, and is not mine:**

- **The row's disposition is the CTO's.** This read supplies bytes and verdicts; it changes no row.
- **Whether `tier == 'internal'` or `firmId == 'opal-capital'` is reachable by a caller who should not have
  it** is a property of the *authorizer* that mints those context fields, not of this function. This read
  looked at one function's bytes. The deployed comment states the authorizer grants all access on
  `tier === 'internal'` itself, so this Lambda is not the place that decision is made.
- **No route was called and no token was minted**, so nothing here is EXERCISED-AGAINST: the rule is read
  from code, and this function's 9 routes are a write path the FWD-1 runner is forbidden to probe. ABSENT of
  a live refusal is not evidence of one.
