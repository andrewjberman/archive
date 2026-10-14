# NEVER-WIDEN, COO HALF -- the gold ETF classifier serves the cash class for a canonical row typed Cash (IRPT_DASHBD DB-b-181 cell B): ONE S3 object

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-14 ~00:5xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md`), sha256 `cfc1dd8d01206badc657bbf17c46653482149c1904b708bd002ba1ff172b1fe6`
(computed by this seat on the file; 11,678 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's four questions (section 7).
**Nothing is applied until both halves are SIGNED on this sha256.** Ordered by the CTO's msg 7258.

## 1. What this half covers

ONE release: the object `s3://opal-data-bd/code/gold/lib/etf_classifier.py`, from the live bytes (sha256 `d2e6aa88086c...`, 18,606 bytes, S3 version `0jhXHH7axm_H934t5s5gVDVNJ6Y_WqI.`) to the committed bytes of `e340e07f4e` (sha256 `e7385264668e...`, 19,496 bytes), by `.tools/safe-deploy.sh` in explicit-files mode, by the AE applier `0.7.0_AE_CloudOps~IB2`. Nothing else is uploaded: no `_shared` client file, no other BD script, no Terraform, no Lambda.

## 2. What this seat measured (and re-ran), and what it did not

- **Live equals the pre-change git version.** `aws s3 cp` of the live object piped to sha256: `d2e6aa88...`, equal to `git show e340e07f4e^:<path>`. This closes the research pass's open item: no other change reached the key.
- **The count of what moves.** The worker's canonical scan (365 Cash-typed, 348 already cash, 17 move, FDRXX among them) was RE-RUN by this seat with its own read-only scan: the same numbers and the same class vocabulary. The worker's four classifier test files plus its new one were RE-RUN by this seat: 37 passed. The diff was read by this seat in full (27 lines; every canonical-row return goes through one helper).
- **Bucket versioning** `Enabled` and the live object's version id, size and time were read by this seat (one `get-bucket-versioning`, one `head-object`).
- **Not re-run by this seat:** the worker's served-positions scan (20 positions moving in 4,315 across 189 advisor files, 178 accounts by the newest holdings snapshot): it is a FLOOR (each file holds the top 25 positions per advisor) and is the worker's. The consumers, their triggers and the C_06 history behaviour come from a read-only research pass whose key lines this seat spot-checked (C_06 `--incremental` is pinned in the dispatch catalog; `reclassify_retained` revisits only a class outside the served six or `unclassified`; `cash` is in the published class lists); the EventBridge schedules and the D_04 overwrite behaviour were NOT re-read by this seat.

## 3. Writers of the changed property, counted: N = 1 rule, 4 consuming writers

`_row_class` is the one rule. D_04, D_03, C_06 and the silver asset-dim each consume it and write the served class; E_25 consumes it without a changed output. The packet reads each writer's behaviour on a changed class (its section 3) rather than predicting it from the rule. No writer outside the four imports this file; the Cottonwood copy, the partners Lambda's classifier and the Investor Reporting holdings snapshot path are NOT covered and keep serving what they serve.

## 4. Blast radius, and the two honest limits this half signs under

- The upload changes nothing served by itself. Served objects change at the next run of each consumer; what changes is where a position of one of the 17 rows is counted in a mix (fixed income to cash), with every total unchanged.
- **The C_06 history discontinuity is a stated consequence,** not a surprise: past dates stay `fixed_income`, new dates become `cash`, until a full rebuild this pair does not cover. This half does not sign the full rebuild.
- **The rollback is PARTIAL for C_06:** a rollback restores the module and the platinum and silver objects return at their next run, but C_06 dates already built under the new bytes stay `cash` until a targeted rebuild. The packet says so; this half signs on that understanding.
- `CASH_USD` is NOT in this release (it stays `fixed_income`); its question is the CTO's.

## 5. Both branches

Branch A (a run lands under the new bytes): section 2 and section 3 of the packet. Branch B (the module or a consumer fails): the applier's pre-upload tests and import smoke stop a bad module BEFORE the upload; a consumer that fails after it leaves its previous served objects in place; the rollback restores the previous module by copying the prior S3 version back and the same hash read-back.

## 6. Conditions of this half

1. **Ledger first,** bound to the packet's sha256 (`bd-gold-etf-classifier-cash-type-20261014`; legs git, s3-prefix, verify); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live bytes re-read at the moment of the apply** and equal to `d2e6aa88...`, else STOP; the upload verified by the tool's ETag/SHA read-back at `e7385264...` and `comp-pipescript deployed`. 3. **The tests and an import smoke at the pinned bytes** first, else STOP. 4. **Not while a gold chain run is in flight.** 5. **No full rebuild, no manual `--full`, no `main()` upload.** 6. **The applier is an AE seat the gates admit,** not a worker, and the apply is not made during another seat's open ledger entry on the BD gold tree. 7. **The first D_04 run after the upload is READ** (the advisor positions files: no position of the 17 rows still `fixed_income`, the moved count at least the 20 floor or the reason stated) before the ledger closes; until then the ledger reads known-held on that run.

## 7. The four questions, from this seat (the CTO's half decides them)

1. **C_06 discontinuity:** this seat recommends ACCEPT for this pair and a separate decision on a rebuild after Andrew has seen the new class on a page.
2. **`CASH_USD`:** this seat recommends LEAVE it as it is for this pair (its tests pin it as "kept exactly as it was", and the set it would move is not counted); if the CTO wants it moved, a second count and pair first.
3. **The other classifier copies:** accepted as out of scope here; Andrew's smoke was on an Inflection client's Opal report, and whether that page reads the platinum key at all is NOT ESTABLISHED; if it does not, FDRXX will still read fixed income there after this release, and a separate cell is owed.
4. **The silver legacy blend label** (`bd_coarse` for a coarse BD super-class with a cash canonical class): this seat recommends ACCEPT; only that column and its source label change.

-- 2.0.0_SA_COO~D2
