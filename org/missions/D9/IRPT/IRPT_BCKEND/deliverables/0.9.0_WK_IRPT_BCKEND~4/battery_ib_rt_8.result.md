# `battery_ib_rt_8.py` -- RESULT

`IRPT_BCKEND.TO-IB-rt-8` -- THE EXPORT WORKER RENDERS. `0.9.0_WK_IRPT_BCKEND~4`,
branch `wk-irpt_bckend-2-4`.

```
invocation : timeout 1800 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rt_8.py
expect     : IBRT8-EXPORT-RENDERS
verdict    : 7 of 7 mechanical arms passed   rc=0   sentinel printed
transcript : IB-rt-8_RT8-AC1_battery_output.txt (241 lines, verbatim)
```

**TWO ANDREW-DIRECT WORDS LANDED AFTER THIS ORDER FIRST DRAINED COMPLETE, and both are arms now.**
13:48Z, *"yes on synthetic exports"* -> arm **(g)**, the four synthetic export PDFs deleted.
14:5xZ, *"Yes ycharts runner may be started"* -> arm **(a)** unlocked, the render RUN on the host.
Neither was taken by widening anything: each act has its own change-management ledger with the
sentinel committed BEFORE it, and each arm VERIFIES the world afterwards rather than re-performing
the act on every run -- a battery that deleted or started a host on every run would pass the first
time and fail the second.

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

### (a) SUBMIT TO READY TO DOWNLOAD, ON THE SERVED SERVICE -- PASS, render step SESSION-GATED

One `submit` invoke, `statusCode=200` in 4.2 s. The FROZEN bundle is persisted BEFORE any render
at `firms/49financial/generations/GENRT8PROOF/attempts/1/exports/rt8-a/bundle.json`, 660 bytes,
read back EQUAL, and confirmed by an INDEPENDENT `head-object` carrying
`irpt-export-id`, `irpt-attempt-id`, `irpt-bundle-sha256`, `irpt-contract-version` and
`irpt-synthetic=true`.

Dispatch: `HUMAN_GATED (sent=False)` from the CONTROLLER -- host `irpt-ycharts-runner`
(`i-0167fd745ad906a66`) `state=stopped`, document present, **0 commands sent by the function**.
That stays correct after the unlock: the controller holds no `ec2:StartInstances` by design, so a
render is an operator-initiated CYCLE and the function's job is to refuse to dispatch into a
stopped box and hand the act back.

**THE RENDER THEN RAN, on Andrew's word.** start -> `ssm send-command irpt-export-render-run` ->
stop, every step timestamped. On the host the document synced its own code, found node `v18.20.8`
and the cached Chromium `1187`, launched the browser and opened
`https://opalinvest.dev/investor-reporting/print` -- which answered with a SIGN-IN SCREEN, so
`render_export.cjs` refused `SESSION_ABSENT` and never signed in. The arm reads **`SESSION-GATED`**,
the branch the issuer's amendment names. The host is back to `stopped` on a LIVE read. Detail:
`RT8-a_render_record.md`; rows `-S22`, `-S23`, `-S25`.

**THE NETWORK DENOMINATOR IS MEASURED NOW, NOT VACUOUS:** 12 requests -- `opalinvest.dev` 10,
`fonts.googleapis.com` 1, `fonts.gstatic.com` 1. **2 foreign of 12, and 0 VENDOR of 12.** The
criterion's phrase "0 external connections" is not achievable against the portal as built; the
battery prints what it measured instead of what was wished for (row `IRPT_BCKEND-W4-S23`).

The download route returns an Opal-signed URL with a 120 s TTL after REAUTHORIZATION, and returns
`EMPTY_GRANT` after the grant is revoked while the artifact record is untouched -- the second half
is what shows the reauthorization is real and not a cache read.

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

### (e) EXCLUSION PROVED, ON A POPULATION THE WORD MADE SMALLER -- PASS

This arm used to read FIVE live objects and assert 5 of 5 still headed 200. **Four are gone by
Andrew's word** (arm (g)), so that assertion is no longer available -- and keeping it, or quietly
dropping the four from the denominator, would each misdescribe the world. The arm now has two
LABELLED halves: the **LIVE** census (1 of 1 `EXCLUDED_BY_BOTH`, 4 of 4 readers admit 0 of 1, the
ordinary-object control still admitting 1 of 1 on `download` and `export_status`), and the four
deleted keys re-run from the **COMMITTED RECORD** (4 of 4 `EXCLUDED_BY_BOTH`, 4 of 4 readers admit
0 of 4). The readers are pure functions of `(key, metadata)`, which the record supplies; what the
record cannot supply is whether the objects exist, and that is arm (g)'s live 404.

`exclusion.py` still has no `put_object`, `copy_object` or `delete_object` at all, asserted by a
test. Detail: `RT8_synthetic_pdfs_inventory.md`.

### (g) THE FOUR SYNTHETIC EXPORTS DELETED ON ANDREW'S WORD -- PASS

**`4 of 4 deleted, 0 of 4 remaining, 0 unexpected objects`.** Four `delete-object` calls on four
LITERAL keys -- never a prefix delete, never `--recursive` -- with the inventory re-read
immediately before and a gate that would have refused on a fifth object. The arm reads the LIVE
world for the 404s rather than trusting the receipts: **a receipt is a claim, the 404 beside it is
the measurement.** THE BLAST-RADIUS CONTROL is what makes four-of-four mean anything -- the object
the word does NOT cover still heads 200 at 660 bytes.

**THE GRAIN IS PRINTED, because "deleted" over-claims without it:** the bucket has versioning
ENABLED, so these are DELETE MARKERS -- every ordinary read 404s while the noncurrent versions stay
retrievable by `VersionId`. The permanent per-version delete is unrecoverable, is a different act,
and was not taken. Row `IRPT_BCKEND-W4-S20`. Detail: `RT8-g_synthetic_delete_record.md`.

### (f) LEDGERS AND PLANS -- PASS

Ledger `irpt-bckend-rt8` reads CLOSED, its sentinel removed by the close and the close committed at
`67aa231c29`. Post-apply re-plans: export `No changes`, performance `No changes`, narrative
`No changes` -- 3 of 3 roots, each with the vendored `.tools/terraform.exe`. **The `ycharts` root
is planned too, because this cell amended it, and its clean plan is reported WITH its limit:** the
amendment is a header comment and one output DESCRIPTION, neither of which Terraform holds in
state, so `No changes` proves nothing ELSE moved -- not that the description changed. The file is
the evidence for that.

Two further ledgers were opened and CLOSED in this order, each with its sentinel committed BEFORE
its act: `irpt-bckend-rt8-synthetic-delete` (4 legs) and `irpt-bckend-rt8-render` (5 legs).

---

## WHAT THIS BATTERY DOES NOT ESTABLISH

Stated here because a 6-of-6 verdict reads as completeness:

1. **STILL NO PDF.** The render reached the print route and refused `SESSION_ABSENT`; the host
   half is now exercised end to end EXCEPT for authentication. `head-object` reads MISSING on both
   `report.pdf` and `render_guard.json` -- the correct outcome for a refused render, not a gap in
   the evidence. The receipt's `artifact_hash`-equals-the-stored-object arm remains proven only
   where round 1 proved it.
2. **"0 external connections" is measured and is NOT zero** -- 2 foreign of 12, both Google Fonts,
   0 vendor. The bound this project carries (no vendor call) holds; the criterion's wording does
   not.
3. **The layer digest is a union this cell does not own.** Its CONTENT is correct as of this
   commit, and that correctness is a property of who published last, not of a control.
4. **The exclusion census population was chosen by this cell.** See `RT8-AC2_judgment.md` s.4.
