# IB-s-14 RESULT -- the export: frozen, rendered, receipted, and reauthorized at download

TO: `IRPT_BCKEND.TO-IB-s-14`
(`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-s-14.export-bundle-freeze-render-worker-receipt.md`)
Worker: `0.9.0_WK_IRPT_BCKEND~4` | Branch: `wk-irpt_bckend-1-4` | Worktree: `/c/tmp/wk-irpt-1-4`
Cell: `IB-s-14` (PRD row B14; FWD-8 / FWD-3 / FWD-4 contrib) | Fabric: laptop | Date: 2026-09-11

## 1. WHAT IS BUILT

`infra/aws/lambda/investor-reporting/export/` -- `assets.py` (verify, never fetch: five
named refusals and a URL-shaped reference refused BEFORE any lookup), `bundle.py` (the
canonical freeze and `rebrand()`, which asserts the performance revisions are carried
through), `render.py` (the renderer seam, the content hash, the PDF validation with the
narrative census), `receipt.py` (the immutable receipt, its id derived from two digests),
`download.py` (the guarded route and the Opal-signed short-lived URL check), `handler.py`
(the orchestration and the route table), `fixtures/render_package/` (a CONFORMING FIXTURE
package that validates against the shared contract, plus two print surfaces), `tests/`
(33 offline tests). `infra/aws/terraform/investor-reporting/export/` -- `main.tf` completed,
`iam.tf` (one role, logs only, with a named NOT-GRANTED list), `lambda.tf`.

## 2. ACCEPTANCE

### S14-AC1 -- PASS by output (9 of 9 arms)

`timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_s_14.py`
-> rc=0, final line `IBS14-EXPORT-REPRODUCIBLE`. Transcript committed as
`IB-s-14_S14-AC1_battery_output.txt`. Deciding numbers, each beside its denominator:

- **(a) SAME BUNDLE, SAME PDF.** Bundle sha256 equal across preview / render / retry,
  **3 of 3**. Content hash equal render-vs-retry. **The RAW digest is NOT equal and is not
  claimed to be** -- Chromium stamps a creation date and a document `/ID` into every PDF, so
  `artifact.sha256` is the raw digest of the bytes that exist and the reproducibility claim
  is on the content hash (page count + each page's media box + each page's content stream +
  the extracted text). Both are printed. Render 1 produced 2 pages, `PASSED`.
- **(b) BRANDING IS A NEW REVISION.** r1 -> r2, brand V.01 -> V.02: **2 of 2** identities
  moved (bundle sha256, receipt `export_id`) and **1 of 1** performance revision held at
  `[('REP-0001', 'rev-7')]`. `rebrand()` makes the same assertion in code.
- **(c) NO VENDOR CALL IN RENDER.** **0** external outbound attempts across 4 renders;
  **0 of 0** to a vendor host (denominator: bd3.bdreporting.com, api.cloud.orionadvisor.com,
  ycharts.com, api.ycharts.com). Loopback connects are PERMITTED and counted separately --
  the print path drives the browser over a local channel and asyncio builds its self-pipe
  with `socketpair()`; a guard that refused those would stop the render from starting and
  then report zero external connections for a render that never happened. POSITIVE CONTROL:
  the guard fired and the vendor counter moved **0 -> 1**.
- **(d) ASSETS VERIFIED, NOT FETCHED -- 5 of 5.** wrong firm -> `BINDING`; GIF declared as
  SVG -> `UNSUPPORTED_TYPE`; wrong digest -> `CHECKSUM`; SVG with `<script>` -> `UNSAFE_SVG`;
  a report field carrying `https://ycharts.com/logo.svg` -> `URL_FETCH`, refused before any
  lookup and with the socket counter unmoved. The APPROVED asset still verifies, so the arm
  is not passing by refusing everything.
- **(e) REAUTHORIZED EVEN WHEN THE ARTIFACT EXISTS.** Download 1 served with
  `artifact_existed=True`; the URL is Opal-signed on the firm's bucket with a **120 s** ttl
  and no vendor host (host WHITELIST, not a vendor blacklist). The fixture grant is then
  REVOKED with **the artifact still present and the cache NOT cleared** -- so a refusal
  cannot be explained by a cold cache or a missing object, the two things a reader would
  otherwise suspect. Download 2: **REFUSED, `EMPTY_GRANT`**.
- **(f) THE ANALYSIS EXPORT.** Same report revisions, same selected sections, same versions
  as the preview; orientation PORTRAIT -> **LANDSCAPE**; same brand revision. Narrative
  census in the rendered text: **0 of 1** markers. And structurally, the analysis template
  has no `{{NARRATIVE}}` slot, so a caller passing narrative text cannot render one -- two
  independent halves. **SECTIONS ARE FIXTURES and the battery says so**: IB-s-10 is `staged`
  at this vintage.
- **(amend) GUARDED, BOUND, SILENT.** `unguarded_routes()` over this cell's routes: **0 of 2**.
  `routes.json` does not exist at this vintage, so that census is printed AS VACUOUS and the
  CENSOR is proved instead with IB-s-7's two controls -- an unguarded handler censuses
  **1 of 1**, the same handler wrapped censuses **0 of 1**. A non-reconciling `FirmBinding`
  is **REFUSED with `FIRM_BINDING`**, not served empty. A parameter keyed by a client display
  name is **`KEY_REFUSED`** and the refused VALUE appears **0 times** in the whole envelope
  (body + reason + audit trail, 1,202 bytes) while its NAME is named.
- **(g) RECEIPT AND ARTIFACT; LEDGER CLOSED.** Key
  `firms/49financial/generations/GENIBS14SYN/attempts/1/exports/r1/report.pdf`, built by
  `_keys.s3_evidence_key` from the declared layout. The object was PUT and READ BACK:
  receipt `artifact_hash` == the stored object's sha256. `irpt-export-render` CodeSha256
  `HSuSKsWzsnqS4tIO/b+Zu4hYdpx2RNZxmeqavv7XwUw=` equals the built zip; layer
  `irpt-common:2` attached; ledger CLOSED and its sentinel removed by the close.
- **(v0.11) THE ANALYSIS EXPORT ON REAL VENDOR INPUT.** **3 of 3** SHA-256 verified against
  `pdf_validation.json` BEFORE use (`abab2ffe...` 573,677 B / `f01cbd48...` 820,984 B /
  `0a67ecf7...` 854,115 B). **3 of 3** rendered LANDSCAPE, stored, read back with the stored
  hash equal, **0** narrative markers each, and `vendor_synthetic_holdings: true` in the
  object metadata. An Opal-owned S3 read under KMS key `86324aae-...`, not a vendor call.

### S14-AC2 -- PASS by output
`timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/export plan -no-color -input=false -lock=false`
-> rc=0, `No changes. Your infrastructure matches the configuration.` Run after the apply
(4 added, 0 changed, 0 destroyed) and after the ledger closed.

### S14-AC3 -- JUDGMENT, RECORDED, NOT SELF-GRADED
Output at `S14-AC3_judgment.md`: what the fixture package cannot show (fonts -- the largest
gap and it changes the OUTPUT, not just the layout; the print entry point, which this cell
never invokes at all; page breaks, present but untested because fixture sections never
break), which arms must re-run at the swap (**(a), (f), (v0.11), (g)** -- and NOT (b), (c),
(d), (e), (amend), which read no rendered document); four ways a runtime's own fonts move
the hash between environments; and seven things a receipt reader cannot learn -- the
sharpest being that **a receipt for a FIXTURE-rendered export is indistinguishable from one
rendered by the counterpart's real package.**

## 3. CONTROLS

**Mutant.** Six difference controls, each required to fail: four bad-asset fixtures (each
differing from the approved one in exactly the dimension it tests); the URL-shaped reference;
the revoked grant with the artifact still present; the unguarded route in the censor's own
control; the non-reconciling firm binding; and the socket positive control, which moved the
vendor counter 0 -> 1 so the zero is a measurement. All fired.

**Determinism.** The battery was run twice end to end and the transcripts diffed: **14 diff
lines, 8 changed lines, and ALL of them are raw sha256 values and the export ids derived
from them.** Every bundle hash, content hash, page count, census, refusal code and verdict
is identical between runs. That is the precise statement the raw-hash instability allows,
and it is recorded as row `IRPT_BCKEND-W4-S12` rather than smoothed over.

## 4. THREE DEFECTS THIS CELL FOUND IN ITS OWN WORK

1. **A repo-relative path that is an IndexError in a Lambda.** `_HERE.parents[4]` raised at
   import in `/var/task`, killing the deployed function before it could report anything. The
   31 offline tests, the import-closure gate and the build all passed -- all three run where
   five ancestors exist. **And the fix had its own near-miss:** written with `levels=4` it
   landed on `infra/` and the suite STILL passed, because the fallback test accepts either
   branch of an absence on purpose. Caught by asserting the resolved root CARRIES
   `infra/aws/lambda` and `deck_generation`. Row `IRPT_BCKEND-W4-S11`.
2. **A capabilities report that died of the thing it exists to report.** It raised
   `ValidationUnavailable` instead of naming which contracts this runtime can check. Row
   `IRPT_BCKEND-W4-S10`.
3. **A socket guard that would have measured nothing.** Refusing loopback stopped the render
   from starting, and the arm would then have reported zero external connections for a render
   that never happened -- a detector that cannot go non-zero. Corrected before the first
   passing run; loopback is permitted and counted separately.

## 5. SURPRISE ROWS FILED UNDER THIS CELL

`IRPT_BCKEND-W4-S9` OBSERVATION / **ARMED** (disarm `2.0.0_SA_COO~B`) -- the deployed worker
cannot render; no headless runtime exists in a python3.12 Lambda and the egress to obtain one
was refused at IB-s-8. The mechanism is proved in the worktree against the estate's own
existing headless path; the CLOUD render does not exist.

`IRPT_BCKEND-W4-S10` OBSERVATION / **ARMED** (disarm `2.0.0_SA_COO~B`) -- the `irpt-common`
layer carries 2 of the 5 IRPT contracts; the three export contracts are absent and extending
the layer is outside this order's `<paths>`.

`IRPT_BCKEND-W4-S11` OBSERVATION / INERT -- the `parents[4]` IndexError, its `levels=4`
near-miss, and the control that can see a wrong root.

`IRPT_BCKEND-W4-S12` OBSERVATION / **ARMED** (disarm `2.0.0_SA_COO~B`) -- a retry of a
byte-identical bundle mints a NEW `export_id`, because the engine stamps time into the PDF.
The stable identity of an export is the BUNDLE hash, not the receipt id.

`IRPT_BCKEND-W4-S13` OBSERVATION / **ARMED** (disarm `2.0.0_SA_COO~B`) -- the battery writes
four real objects into the live evidence bucket under the unmistakable generation id
`GENIBS14SYN`, each labelled `irpt-synthetic=true` in object metadata, because arm (g) is
graded on a STORED object.

## 6. BOUNDS HELD

No live Black Diamond, Orion or YCharts call -- 0 external connections across 4 renders with
a live positive control; the three vendor PDFs are an Opal-owned S3 read. No model call. No
monitor, alarm, SNS topic or SES send. No schedule and no event source; the deployed function
is invoke-only and its renderer is explicitly `unavailable`. Logos are VERIFIED and never
fetched, never invented, never scraped -- the Opal fallback is the estate's own official
logo, labelled `OPAL_TEMPLATE_FALLBACK` with `pending_input`, and ABSENT-with-reason where
the gitignored source is not on the machine. The performance revision is immutable across
export revisions and `rebrand()` asserts it. The RenderPackage is labelled a fixture in
`packaging.executed_version`. No credential in any artifact or fixture. No served output
touched: the apply was 4 added / 0 changed / 0 destroyed and the `irpt-common` layer was READ
by name. Deploy via `.tools/safe-apply.sh` with `.tools/terraform.exe` by path, under a ledger
entry opened before the act and closed after, sentinel committed then removed by the close.
Scratch confined to `/c/tmp/wk-irpt-1-4/.scratch/`.
