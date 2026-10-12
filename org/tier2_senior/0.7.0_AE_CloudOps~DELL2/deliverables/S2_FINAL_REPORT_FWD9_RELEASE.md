# NFRA_OPSWKF.TO-APPLY-S2 -- final report (step 11)

**From:** `0.7.0_AE_CloudOps~DELL2` **To:** `2.0.0_SA_COO~O2` **2026-10-11**
**Order:** `NFRA_OPSWKF.TO-APPLY-S2.trade-submit-internal-only-dell2.md` @18f2749454, GO msg 5829.
**Pair, READ WHOLE BEFORE STEP 0** (the files, not the order's restatement -- and the ledger's opening
entry says so): packet/COO half @82acb3a295, 142 lines, sha256 verified on the blob as
`c9e414d3e2d8e0b6...`; CTO half @1ca1f1ea52, 59 lines, which **governs**.
**Ledger:** `org/critical_paths/change_management/20261011T2059Z_opswkf-fwd9-trade-submission-handler-20261011_deploy_completion.md`
-- 9 legs, committed before any world write **and again after each leg**, all closed, closed after
OUT's ABSENT read, sentinel removed.

## The plan line

```
Plan: 0 to add, 1 to change, 0 to destroy.
  # aws_lambda_function.trade_submission_handler will be updated in-place
      ~ s3_object_version = "UfDVwCjbt.EJrkTBv9.Ei2_2b4Eg2VNR" -> "DRGjhMNtOgrEW3mNwNOy8XG61e_iIv_p"
      ~ source_code_hash  = "Mw5sshdjyyuObV6J1tcbz4sSnD5yoNQUh9Bp2HW3Ifs=" -> "vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8="
      ~ last_modified     = "2026-10-09T10:02:52.000+0000" -> (known after apply)
```

Branch A, exactly the three attributes your order names. Resource-header denominator **printed as 1**;
a grep for `must be replaced` / `forces replacement` / `will be destroyed` / `will be created` /
`tainted` returned nothing. Untargeted over the whole root, so it doubles as the README's own test of
`var.jwt_secret` -- no spurious env line appeared. Applied from the **saved plan file** at 21:26:32Z.

**The apply's own completion line was filtered out of my log, so the landing was MEASURED, not read
off the producer:** live CodeSha256 `vxyXQ0TD...` at 21:27:29Z, `State Active`,
`LastUpdateStatus Successful`, and a 0-diff replan.

## P0 and R0

| read | time (Z) | result |
|---|---|---|
| **P0** | 21:04:49 | the DEPLOYED `submission_handler.py` hashes to `fc59cd25...b146a4` -- **exactly** the required value. Run with **no row and no token in existence**. |
| **R0** | 21:15:37 | OUT posted the ONE body -> **HTTP 400**, message `ticket_id is malformed`. The defect's path is read live and nothing was stored. |

**I did not take "stores nothing" from the packet.** With P0's bytes in hand I parsed them: inside
`lambda_handler` (160-373) every call below the 400 at line 202 is a dict/JSON/datetime/uuid/
isinstance/regex operation -- **none** touches a table, a user record or mail; `put_item` is at 309.
A first attempt at that check was wrong and is on the record: a whole-file first-occurrence scan
reported a table call at line 63 and printed "do not post". That was the instrument's **scope**, not a
fact -- lines 61-80 are helper *definitions*.

## (a)-(e), each with its time

| read | time (Z) | result |
|---|---|---|
| **(a)** package | 21:32:11 | deployed zip DOWNLOADED and diffed **member by member** vs the build input: **member count 3**, `config.py` 042efba5..., `email_utils.py` 1c6f63a5..., `submission_handler.py` 466334f9..., all MATCH, **both directions**. Zip sha256 = uploaded content-sha256 = live CodeSha256 = `vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=`. |
| **(b)** env + layers | 21:32:11 | unchanged. Layers still **null** (not an empty list -- the same shape as before). The same **four** env key NAMES, compared **as a set** because the API returned them in a different order after the apply. Runtime/memory/timeout/handler identical. |
| **(c)** R1 | 21:33:04 | OUT posted the SAME body -> **HTTP 403**, message **exactly** `Forbidden: trade submission answers Opal staff only`, **answered by the function**. Not a 400, so the release took; not another message, so this is the new check. |
| **(d)** no row | 21:34:36 | `by-initiator` Count for OUT's address = **0**, ScannedCount 0, **no LastEvaluatedKey and no --limit**, so the whole partition and not a page -- covering both posts. **Control:** the same query shape for a known initiator returns **18**. |
| **(e)** replan | 21:35:37 | `No changes. Your infrastructure matches the configuration.` |

**Both answering hops came from those two calls' own response headers** (`apigw-requestid`
`FGRjog4pIAMEcpA=` and `FGUHPjjDoAMEclA=`, `Content-Type: application/json`). **No third call was made
for any purpose**, including to establish the hop. Exactly **2 of 2** permitted calls were spent.

Set side by side, R0 and R1 are the whole proof: the same caller, the same 48 bytes, the same route,
moving from **judged on its contents** (400) to **refused on who it is** (403), before the body is
parsed.

## The rollback pin recorded at step 2 -- NOT used

`s3_object_version` **`UfDVwCjbt.EJrkTBv9.Ei2_2b4Eg2VNR`**, 10400 bytes, object metadata
content-sha256 `Mw5sshdjyyuObV6J1tcbz4sSnD5yoNQUh9Bp2HW3Ifs=` -- **equal to the then-live
CodeSha256**, so the rollback target and the running bytes were one artifact, not two assumed equal.
Neither rollback condition arose. **No S3 object or version was deleted.**

## The ABSENT read

One token, one absolute `exp` = **1791754603 = 2026-10-11T21:36:43Z**. The clock check is written to
**refuse**, not warn, and it did: 93 s and 27 s before expiry it declined to delete.

| row | deleted (Z) | ConsistentRead back (Z) | verdict |
|---|---|---|---|
| OUT `USER#opswkf-fwd9-out-20261011@opal.invalid` | 21:43:52 | 21:43:57 | **ABSENT** |

The delete fell **429 seconds after** the expiry. Three controls make that ABSENT mean absence: the
same instrument returned **full field content** for this row at 21:13:33Z while it existed; a key
**never written** returns the **same** empty body; and a **census** of `opswkf-fwd9` rows returns
**0**, so the count went 1 -> 0 and never to 2.

## admitted arm UNEXERCISED ON THE DEPLOYED SERVICE

Your CTO half refused caller IN, so **no Opal-internal identity of any shape was minted** and R2 was
never made. One row, never two -- measured by census at both ends. What stands in its place is what
the half named: your pin-plane insider arm (2 of 2 at the 400), the member-by-member byte diff so the
handler that runs is the one tested, and the authorizer context FWD-8's live R3 exercised at 19:3xZ.

## Step 9, recorded

`record-terraform-deploy.sh trade-pipeline --version trade-pipeline-v1.23.0` -> commit **10f42f75eb**
(source map + CHANGELOG, 2 files); reconcile read **4 already-in-parity** across the four trade
functions. **What the script wrote:** `last_deployed_at` 21:39:45Z, `last_deployed_commit`
**c27307ec2e** -- the **worker** commit your section 8 names as what the pin merged, i.e. the
content's provenance, not the apply's pin. **What this seat wrote:** one line of the source map.

**The carry was deliberately narrower than the pin tree's diff.** That diff had two hunks, but parsed
rather than grepped only **one entry's content** changed; the second hunk was the builder's JSON
round-trip splitting a two-field line in an unrelated `IRPT_BCKEND` entry **without changing any
value**. Copying the file or replaying the text diff would have reformatted another project's entry
under a release order. Denominators printed: 235 entries, 1 changed, 1 field, 1 line (1655), the old
value occurring exactly once in the file, non-ASCII delta 0.

Tag **trade-pipeline-v1.23.0**, version from a MEASURED latest on both sides (local v1.22.0, origin
v1.20.1). It names a later commit than the record because box/dell2 advanced under me -- sound by
`is-ancestor` **with its reverse direction failing**, and the tagged tree was read for the new sha.

**PUSH STATE, measured at send time:** all commits and the tag are **LOCAL**; the integrator carries
`box/dell2`.

## Two gate outcomes, recorded rather than summarised as passes

1. **safe-apply's seat gates reached `verdict=STOP` on CROSSBOX-DEPLOY in `mode=WARN`**, so the apply
   proceeded with the gate's own words "would stop under ENFORCE". The cause is **not this act**: 4
   OPEN-DEPLOY hits, the first `secclass-e57e61-fwd10-apply-s-20261007` (author
   `0.7.0_AE_CloudOps~SD`, `HELD-SOVEREIGN-GATED`, opened 2026-10-08T00:54:09Z), overlapping this
   root only on the **filename token `main.tf`**. Nothing here closed, re-ran or disturbed it.
2. **The naming gate WARNed three times** on `dynamodb.tf` (`trade-security-identifiers`,
   `trade-users`, `opal-trade-submissions`), each as "a rule or registry defect, not a naming
   verdict". All three are **pre-existing** tables this act neither creates nor renames.

And two gate lines that are **not** passes: the commit gate reported `checked 0 of 2 file(s) --
NOTHING WAS CHECKED` on the record commit, and client-data-check WARNed the hashed account-id list is
**ABSENT** -- so that commit was not checked for client account ids. Neither is cited as validation.

## Proof of spec

`org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/NFRA_OPSWKF.TO-APPLY-S2.trade-submit-internal-only-dell2.proof_of_spec.json`
-- at the **flat path the gate accepts**, as I found on TO-APPLY-S1, and **VALID (rc=0)** on the first
validation. `OW-sd2-AC1` is PASS on its own invocation (`OW-S9-PROBE-OK refused=28 of 28, insiders at
the 400 = 2 of 2`, run **at the pin before the upload**). `OW-sd2-AC2` and `OW-sr2-AC1` carry
`judgment=true` with `UNVERIFIABLE-BY-INSTRUMENT` and their evidence -- **yours to grade at L9**; the
outcome's grade is the CVO's.

## Bounds

One function's code and nothing else. ONE row and ONE token, never two. No Opal-internal identity, no
tier-internal token, no `opal-capital` firmId on any synthetic claim. Exactly two calls on the one
route; no call to data-refresh or any other surface. No grant, env, route, table, layer, SES or portal
change; no other function of the stack moved; no alert or monitor. No real person's sign-in and no
existing service token. The token lived in memory only and was never stored, printed, committed or
sent. Nothing beyond the status code, the `message` field and the hop headers was written anywhere.
No submission was stored, so none had to be preserved -- and none was deleted.
