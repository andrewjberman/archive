# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-519 irpt-export-render (the ExportReceipt schema re-pin, root cause of the export-status failure, row D2-S152): SIGNED AT PACKET sha256 7d7888984731...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-13 ~23:5xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-519` (merged @295d98d389) | **Applier (a later order, not this half's act):** `0.7.0_AE_CloudOps~IB2`.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat applies before the CTO half is signed at the same bytes AND the conditions below hold at the apply.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~368/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-519.md`, sha256 `7d78889847312b5517d1d85172a93c5f1f993de30760c8f83d60c92079a7b53b` (9,710 bytes). A half signed over different bytes is void.
- **Live and built:** CURRENT live CodeSha256 `K74JEIjw0NKmy4YfEo7Sb7LcRxEII+/yaYtaKJ3qnD8=` (hex `2bbe0910...`, LastModified 2026-10-13T12:43:58Z), which I re-read at ~23:5xZ: unchanged and equal to the source map's `artifact_sha256`. Built CodeSha256 `5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4=` (hex `e7ff4b64...`, built twice byte-identical). **One changed member of 66:** `irpt_contracts/ExportReceipt.schema.json` (live blob `5a7bda2ecddd` at pin `8d08ee54e4`, built blob `118a3575eaf2` at pin `e8005582a1`); the old-to-new diff is the v1.2 change and nothing else (revision 1.1 to 1.2, `covered_account_ids` property and its `required` entry, the revision note).
- **The served change:** the receipt read passes a receipt that carries `facts.covered_account_ids`; today it fails with "Additional properties are not allowed" because the packaged schema is stale (my read of the live log and zip, row D2-S152). Under v1.2 the read still refuses a receipt that LACKS the field. No code path changes; no permission, route, IAM, schedule or table changes; no figure moves.
- **Never refuse a receipt that exists today (CTO RE 7262):** the store holds ONE receipt (the backfill tool's default dry run; a cross-check found one `receipt.json` among 47 objects), it carries the field, and it is refused TODAY; the release makes it readable. Zero receipts lack the field and zero are unreadable: branch `none_needed` **for this read only**.
- **Source map:** one `staged_from` row, two fields (`pin` `8d08ee54e4` to `e8005582a1`, `sha256` `5a7bda2ecddd` to `118a3575eaf2`), uncommitted by the order; the apply seat commits it with the release.

## What I checked myself before signing

- The three criteria of IB185-1 re-run on the merged tree: PASS. I read the packet in full, re-hashed it, and re-read the live CodeSha256. Before cutting the order I read the live log (one event, `covered_account_ids` unexpected) and the live zip's members against the pins and HEAD (row D2-S152).
- I read the reachability of the one latent defect the live zip carries (below). I did NOT re-run the build, the signature instrument, the arms or the receipt dry run myself; they are the worker's, shown by the packet's hashes and by the check. The packet leaves the portal consumers' read-through to the apply seat.

## Conditions of the apply (the CTO half signs the same)

1. **Gates, measured at apply time by the artifact:** both halves signed at the sha256 above; no open ledger and no open marker with an open trunk ledger naming the function (stale OPEN views counted and named, never closed by the seat: NEVER-2); the live CodeSha256 equal to `K74JEIjw...` at the start read (any other value: STOP and re-census); **the receipt store re-read at the start:** if any receipt now lacks `covered_account_ids`, STOP: the backfill runs first under its own signed pair (`--apply` is never a worker's), so the re-pin never goes live over a receipt it would refuse.
2. **Digest gate:** rebuild with the release source map to `5/9LZBbT...`; any difference ABORTS; the Terraform path moves `s3_object_version` and `source_code_hash` only; plan to a planfile (1 change, 0 destroy); `bash .tools/safe-apply.sh`; the Branch B S3 version named and re-read BEFORE any upload (the packet names `_LGUODZLsTpblhaTy2ODlBjRnwdx6cW1`).
3. **The latent defect, carried and not repaired:** the live zip and the built zip both carry one signature mismatch (`served:1026` passes `profile_reader=` to `InteractiveAccess`, which takes none): it sits on the prospect `CREATE_INPUT` path, which this function's operations never route to (my read of `export/entry.py:447-455`); row D2-S154 keeps it ARMED, owner me; no change to `served.py` ships.
4. **The red list is intersected, not crossed:** the changed member's repo path lies under the red list's `docs/contracts/investor-reporting/` prefix; no red test or red operation names the export receipt.
5. **Branch B** (restore the live version, rollback per key, the source-map row reverted) on any trigger in the packet; **ledger** (NEVER-2) opened before the first write; **the after-read is a person's:** one NEW export reaching a readable status on DEV, plus the one pre-existing receipt still readable through the v1.2 read (no seat can sign in); a read that disagrees triggers Branch B.

Signed: `2.0.0_SA_COO~P2` at 2026-10-13T23:5xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
