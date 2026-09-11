# `battery_ib_rt_8.py` -- RESULT

`IRPT_BCKEND.TO-IB-rt-8` -- THE EXPORT WORKER RENDERS. `0.9.0_WK_IRPT_BCKEND~4`,
branch `wk-irpt_bckend-2-4`.

```
invocation : timeout 1800 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rt_8.py
expect     : IBRT8-EXPORT-RENDERS
verdict    : 6 of 6 mechanical arms passed   rc=0   sentinel printed
transcript : IB-rt-8_RT8-AC1_battery_output.txt (177 lines, verbatim)
```

**BOUND 12 -- NO SELF-WRAPPING HARNESS AS EVIDENCE.** Every subject below is the real artifact:
the DEPLOYED `irpt-export-render` (arms (a) and (c) read it by `aws lambda invoke`, never by
importing the handler), the PUBLISHED layer, the objects that exist in `opal-data-ycharts`, the
counterpart's package at the checkout whose HEAD the battery prints, and the three real terraform
roots. The two places where nothing could be exercised say so in the word VACUOUS rather than
printing a pass.

---

## THE ARMS

### (b) THE REAL PACKAGE, VERSIONED -- PASS

`investor-reporting-render/1.0.0` read from `portal/src/pages/InvestorReporting/render/manifest.ts`
at `portal` HEAD `32a744dcd3`, printed rather than assumed because **`portal/` is a GITLINK: a
linked worktree carries an EMPTY portal, so the PRIMARY checkout is what answers.** Declared
runtime `browser` -- which is the sentence that makes a python3.12 Lambda unable to render it.
Four contracts each supporting `investor-reporting/1`; exactly one supported version, so the
identity's `contract_version` is unambiguous and an ambiguous package is REFUSED instead of
guessed. An unsupported `schemaVersion` raises `RENDER_PACKAGE_VERSION`. Round 1's fixture package
remains on disk as history and is referenced by **0 render-path modules and 0 of 10 packaged
files.**

### (a) SUBMIT TO READY TO DOWNLOAD, ON THE SERVED SERVICE -- PASS, render step HUMAN-GATED

One `submit` invoke, `statusCode=200` in 4.2 s. The FROZEN bundle is persisted BEFORE any render
at `firms/49financial/generations/GENRT8PROOF/attempts/1/exports/rt8-a/bundle.json`, 660 bytes,
read back EQUAL, and confirmed by an INDEPENDENT `head-object` carrying
`irpt-export-id`, `irpt-attempt-id`, `irpt-bundle-sha256`, `irpt-contract-version` and
`irpt-synthetic=true`.

Dispatch: `HUMAN_GATED (sent=False)` -- host `irpt-ycharts-runner` (`i-0167fd745ad906a66`)
`state=stopped`, document present. The reason and the three-command OPERATOR ACT are printed
VERBATIM, executable rather than described. **0 commands sent.** RT8-AC1 (a) admits this as the
arm's own rule; row `IRPT_BCKEND-W4-S14` carries why no reachable host may be started by this cell.

The download route returns an Opal-signed URL with a 120 s TTL after REAUTHORIZATION, and returns
`EMPTY_GRANT` after the grant is revoked while the artifact record is untouched -- the second half
is what shows the reauthorization is real and not a cache read.

**PRINTED AS VACUOUS, NOT AS A PASS:** "0 external connections during the render". No render ran,
so there is no host guard log to read. The guard exists in the host half and writes
`render_guard.json` beside the PDF with its own denominator; it is measured at the operator's run.
A detector that cannot go non-zero is not a measurement, and neither is one that was never called.

### (c) FIVE OF FIVE IN THE RUNTIME -- PASS

`contracts_available: 5 of 5` read from `/opt/python/irpt_contracts` INSIDE the Lambda
(`capabilities` invoke): `ExportBundle`, `ExportReceipt`, `NarrativePacket`, `PerformanceReport`,
`RenderPackage`. Layer version **5**, ONE distinct value across **3 of 3** functions
(`irpt-performance-adapter`, `irpt-narrative`, `irpt-export-render`) -- more than one would mean a
partial re-point. The layer also carries the shared key grammar `keys.py @3be9d03962` and
`firm_registry.json @1f54e16dfd`.

**THE ARM IS THE RUNTIME READ, NOT A DIGEST EQUALITY, AND THAT IS DELIBERATE.** The published
`CodeSha256` (`ZUcsQUOsc3lT2cKl...`, 644,526 B) does NOT equal this cell's local build
(`TjZRSAPsIAUdOB3p...`, 637,134 B) because `irpt-common` is a SHARED surface -- one S3 key, one
terraform-managed layer version, written by more than one round-2 cell. IB-rt-3's `ids.py` and
`raw_keys.json` sit in the published artifact beside this cell's five contracts, so the published
digest is a UNION and cannot equal any single cell's build. **Asserting equality would make a
correct, merged layer read as a failure.** The digest is PRINTED; the runtime read is ASSERTED.
Row `IRPT_BCKEND-W4-S15` records the collision and names its disarm owner.

### (d) STABLE IDENTITY -- PASS

Two submits of IDENTICAL input: one `export_id`, `EXP-5c689ee8e1e860c4d5c32d011b01af83`, twice.
**Round 1 minted a NEW id here** because it keyed on the ARTIFACT digest -- row
`IRPT_BCKEND-W4-S12`, which this arm closes. A CHANGED input gives
`EXP-f4a19d4a46ec84f34c6a798552fc0a20`. `attempt_id` is explicit and printed beside both. The raw
digest is in NEITHER id: a print engine stamps a creation date and a document `/ID` into every PDF,
so the raw digest cannot be a stable identity -- measured in round 1 at 25,231 bytes twice with two
different `sha256`.

### (e) EXCLUSION PROVED, AND NOTHING MOVED OR DELETED -- PASS

**5 objects** inventoried with sizes and metadata: the ruling's 4 under `GENIBS14SYN` plus this
cell's own proof bundle under `GENRT8PROOF`. All 5 classify `EXCLUDED_BY_BOTH` predicates.
**4 of 4 readers admit 0 of 5.** THE CONTROL: against one ORDINARY export object, `export_status`
and `download` still admit **1 of 1** -- a filter that excludes everything is not a filter, and
without that column the arm would pass vacuously. **0 deletes issued:** all 5 keys still
`head-object` 200 after the battery, and `exclusion.py` has no `put_object`, `copy_object` or
`delete_object` at all, asserted by a test. Deletion is Andrew's word and is CARRIED, not taken.

Detail: `RT8_synthetic_pdfs_inventory.md`.

### (f) LEDGERS AND PLANS -- PASS

Ledger `irpt-bckend-rt8` reads CLOSED, its sentinel removed by the close and the close committed at
`67aa231c29`. Post-apply re-plans: export `No changes`, performance `No changes`, narrative
`No changes` -- 3 of 3 roots, each with the vendored `.tools/terraform.exe`.

---

## WHAT THIS BATTERY DOES NOT ESTABLISH

Stated here because a 6-of-6 verdict reads as completeness:

1. **No PDF was rendered in round 2.** The render arm is HUMAN-GATED and the host half is BUILT AND
   UNEXERCISED. Everything around the render ran on the served service; the browser opening the
   print route did not.
2. **The "0 external connections" denominator is unmeasured**, for the same reason.
3. **The layer digest is a union this cell does not own.** Its CONTENT is correct as of this
   commit, and that correctness is a property of who published last, not of a control.
4. **The exclusion census population was chosen by this cell.** See `RT8-AC2_judgment.md` s.4.
