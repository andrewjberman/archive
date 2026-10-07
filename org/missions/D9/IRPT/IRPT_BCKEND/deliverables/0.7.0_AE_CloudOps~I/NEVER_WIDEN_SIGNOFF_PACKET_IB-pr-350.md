# NEVER-WIDEN SIGN-OFF PACKET -- IB-pr-350: back-fill covered_account_ids into pre-343 export receipts

**Prepared by:** `0.7.0_AE_CloudOps~I` (laptop applier) | **Order:** `IRPT_BCKEND.TO-IB-pr-350` @`3e85fbf2b0`
**Pass:** 1 of 2 -- READ-ONLY. Nothing was written. This packet is the object the two halves sign against.
**Dry run at:** 2026-10-07 ~16:5xZ | **Identity:** `arn:aws:iam::313476888478:user/Andrew_Berman`
**Bucket:** `opal-data-ycharts`, read from the LIVE `irpt-export-render` `IRPT_EVIDENCE_BUCKET` (not typed from memory)

Opaque ids only throughout. No name, email or raw account number appears in this file: the export id is the
`EXP-<32 hex>` projection and the derived accounts are reported as a COUNT, never enumerated.

## Precondition, measured

IB-pr-349 is CLOSED and NOT rolled back, which this order requires before it runs:

| read | value |
|---|---|
| ledger `20261007T1356Z_irpt-export-render-ib-pr-349-failclosed-20261007` | `**Status:** CLOSED -- nothing stranded -- closed 20261007T150015Z`, all 4 legs proven |
| `.open_deploys` sentinel | ABSENT (removed at close, deletion committed @`bf8bb487a9`) |
| `IB68-1_release_after_reads.json` `rolled_back` | `false` |
| live `irpt-export-render` | `CodeSha256 aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`, packaged `entry.py` sha256 `fc241d806ecc` |

## The dry run

`python infra/aws/lambda/investor-reporting/export/backfill_covered_account_ids.py --dry-run --bucket opal-data-ycharts --census-out <deliverables>/IB69-1_backfill_dry_run.json`

Tool blob `23cea9f84a3db2856e24cbd1ef7b813540aee240`, byte-identical at the order's commit `3e85fbf2b0` and at the
tree this ran from, so running from the existing linked worktree is equivalent to running from the order's own branch.

```
dry-run: listed 1; read 1 = filled 1 + unfillable 0; would_write 1; wrote 0; denied buckets 0, objects 0
```

### Per firm

| firm | listed | read | filled | unfillable | denied |
|---|---|---|---|---|---|
| 49financial | 1 | 1 | 1 | 0 | 0 |
| cottonwood | 0 | 0 | 0 | 0 | 0 |
| **total** | **1** | **1** | **1** | **0** | **0** |

`already_named` 0, `would_write` 1, `wrote` 0. `denied` and `denied_objects` are both empty arrays, and
`unfillable_reasons` is empty. Firms scanned: 49financial, cottonwood -- the two the tool enumerated under `firms/`.

### The one FILLED receipt

| field | value |
|---|---|
| firm | 49financial |
| export id | `EXP-e29b5415a06f90f943481c41a1a4821b` (opaque projection) |
| accounts derived | **1** (count only; the id is the `acc_<24 hex>` projection and is NOT reproduced here) |
| derivation | `export/bundle.py covered_account_ids_of` -- the freeze's OWN function, imported by the tool, never copied |
| sources used | the bundle beside the receipt's `artifact.storage_key`, and the retained-report pointer `pending.json account_ids` |
| key | `firms/49financial/generations/EXP-e29b5415a06f90f943481c41a1a4821b/receipt.json` |
| size / last modified | 870 B, 2026-10-03T22:13:15Z -- i.e. written BEFORE IB-pr-343, which is why it names no account |
| **S3 version id before any write (THE ROLLBACK SOURCE)** | **`3BN57Lb6hJ7._Nn0hGZ4Yj7NEFYOV_Qa`** |
| encryption | `aws:kms`, key `arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111` |

**Why this packet comes from a laptop and not dell2, confirmed rather than inherited.** IB-pr-344's dry run on dell2
listed this same 1 receipt and could not read it -- row `W145-S5`, `kms:Decrypt` denied. The object is SSE-KMS under
the key named above; this identity decrypted it and the census reads `denied 0`. That is the whole reason the order
routes here, and it is now measured, not assumed.

## Writers of the property being changed

The NEVER rule requires the writers of the named property to be counted and each one's rule read. The property is
`facts.covered_account_ids` on an export receipt. **N = 2, and 2 rules were read:**

| # | writer | rule read, at the bytes |
|---|---|---|
| 1 | `irpt-export-render` at freeze -- `receipt.build(covered_account_ids=...)`, fed by `bundle.covered_account_ids_of` | Writes the list for every export frozen SINCE IB-pr-343. It does not touch an already-frozen receipt, so it will never contend with this tool over the same object. |
| 2 | this tool, `backfill_covered_account_ids.py --apply` (pass 2 only) | Re-writes only a FILLED receipt that LACKS the list, preserving object metadata. Its own docstring: `--apply` "is the issuer's act under a never-widen pair and is NOT run by the worker that built it." |

The write set is therefore exactly the FILLED receipts this packet names: **one key**, listed above. No bundle, no
artifact, no `pending.json`, no other S3 key is written. The consumer's rule was read too -- `entry.py:142 _covered`
returns `False` when the list is absent, empty or not a list, so filling it is precisely what restores the read.

## Both branches

**BRANCH A -- WRITTEN (pass 2 lands).**
- The receipt named above carries a non-empty `facts.covered_account_ids` (1 account) and reads again for a principal
  whose scope covers that account, emitting one `irpt_export_read_admitted` line.
- It is STILL REFUSED for a principal whose scope does not cover it -- not by the no-account branch any more, but by
  the counts branch, `"N of M account(s) are outside the viewer's current scope"`. Both branches of `_covered` were
  exercised against the DEPLOYED bytes under IB-pr-349 and behave exactly this way.
- Nothing else becomes readable. The firm binding is untouched; the receipt is filled only from its own firm's bundle
  and pointer. No cross-firm derivation occurred: the one receipt is 49financial and both its sources are 49financial.
- Blast radius: ONE S3 key in `opal-data-ycharts`. No code, IAM, route, authorizer, table or function change.

**BRANCH B -- ROLLED BACK.**
- Restore version `3BN57Lb6hJ7._Nn0hGZ4Yj7NEFYOV_Qa` onto the key. The receipt then names no account again and is
  REFUSED on read exactly as it is today -- the pre-packet state, which is the IB-pr-349 fail-closed behaviour.
- Rollback does NOT reopen any hole: it returns one receipt to being unreadable, which is the safe direction. This is
  the opposite of IB-pr-349's rollback, which would have reopened cross-scope reads for 7 principals.
- Cost of rollback: the pre-343 export stays unreadable until the back-fill is retried. No other object is affected.

## Refusal conditions carried into pass 2

Pass 2 stops, writes nothing and files a row if any of these holds:
1. The apply-time dry run's counts differ from this packet's -- `listed 1 / read 1 / filled 1 / unfillable 0 /
   already_named 0 / would_write 1 / denied 0`.
2. Any receipt reads DENIED at apply time (today: 0 denied).
3. A receipt's derivation crosses firms.
4. A name, email or raw account number appears in any file.
5. Both halves are not at the published HEAD naming this packet's blob.

## State of this pass

Pass 1 is COMPLETE and nothing was written: `mode` is `dry-run` and `wrote` is 0 in the census. `IB69-1-AC1` reads
FAIL at this point, and the order says that is expected after pass 1 -- the order stays open at the halves. I have
not opened a ledger entry, because the order places that in pass 2, after both halves exist.

Census beside this packet: `IB69-1_backfill_dry_run.json`.
