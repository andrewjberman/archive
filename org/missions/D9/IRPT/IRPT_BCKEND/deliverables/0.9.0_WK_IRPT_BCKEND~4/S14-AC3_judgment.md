# S14-AC3 -- JUDGMENT OUTPUT, RECORDED AND NOT SELF-GRADED

TO `IRPT_BCKEND.TO-IB-s-14` | cell `IB-s-14` | worker `0.9.0_WK_IRPT_BCKEND~4`
Oracle: `3.0.0_SA_CVO` at L9. This file carries the OUTPUT and NO verdict.

---

## 1. WHAT THE FIXTURE RenderPackage CANNOT SHOW ABOUT THE COUNTERPART'S REAL ONE

The fixture VALIDATES against the shared contract, so everything the contract can express
is exercised: supported versions, two deterministic PRINT components, the fonts and assets
requirements, the print entry point, two visual fixtures with real digests, and the
packaging block. **What a contract-conformant fixture cannot show is everything the
contract does not constrain** -- and that is where the three named risks live.

### (i) FONTS -- the largest gap, and it changes the OUTPUT not just the layout

The fixture DECLARES three Lato weights with their licence reference and does not PACKAGE
them; it renders through the fallback chain `Segoe UI, Arial, sans-serif`. The real package
carries the licensed local faces. Consequences, in the order they bite:

- **Every glyph advance changes.** Line breaks move, so page breaks move, so the page count
  can move. The performance export renders 2 pages here and the analysis 1; neither number
  survives the swap as a prediction.
- **The CONTENT HASH changes by construction.** It covers each page's content stream and
  extracted text, and a different font emits different text-positioning operators. So the
  reproducibility arm's *value* is specific to this font environment; the arm's *property*
  (same bundle twice -> same content hash) is not.
- **A missing licensed face degrades SILENTLY.** A browser substitutes and renders; nothing
  fails. There is no check in this cell that the font actually used was the font requested,
  because the print path does not report it.

### (ii) THE PRINT ENTRY POINT -- a shape, not a behaviour

The contract says `print_entry_point` is `{module, export_name}` and the fixture supplies
`fixtures/render_package/{kind}.html#printDocument`. The real package's entry point is a
JavaScript export the counterpart's components mount and call. **This cell never invokes a
JS entry point at all** -- it substitutes a named-slot HTML template with `str.replace` and
no expression language. So the fixture cannot show: whether the real entry point is
synchronous, whether it waits for data or fonts to settle before print, whether it needs a
viewport or a media emulation, or whether it can fail partially and still resolve. Those
are the four questions a real print surface usually gets wrong, and none is asked here.

### (iii) PAGE BREAKS -- exercised, but on a page that cannot really break

The templates carry `break-inside: avoid` on sections and `break-before: page` on the
narrative. With fixture sections of two short paragraphs, **nothing is ever forced to
break**, so the rules are present and untested. The real package's certified sections carry
tables and charts that span pages, and the cases that matter -- a table header repeating, a
chart split across a boundary, a section that avoids a break it cannot fit -- have no
fixture here.

### WHICH ARMS MUST BE RE-RUN AT THE SWAP

| arm | why it must re-run | what specifically could change |
|---|---|---|
| **(a)** same bundle, same PDF | the content hash is font- and layout-dependent | the hash VALUE moves; the equality property should hold and must be re-measured, not assumed |
| **(f)** the Analysis export | the narrative census reads the RENDERED TEXT; a real component could emit narrative content the fixture template has no slot for | `forbidden_hits` could go non-zero -- this is the arm most likely to actually fail |
| **(v0.11)** the three vendor variants | same as (f), three times, and the page counts move | |
| **(g)** receipt vs stored object | the raw digest changes with the bytes, so the receipt id changes | mechanical, but the arm must be re-taken against new bytes |
| **NOT (b), (c), (d), (e), (amend)** | they test the bundle, the network, the asset layer and the authorization wrapper -- none reads the rendered document | these survive the swap on their own evidence |

**And one arm that does not exist yet and should:** the swap needs a check that the package
being executed IS the counterpart's. `is_fixture_package()` reads
`packaging.executed_version` for the `+CONFORMING-FIXTURE-IB-s-14` mark, so the swap is
detectable -- but nothing today REFUSES to serve an export rendered from the fixture. That
is a product decision, not a rendering one.

---

## 2. WHERE THE HEADLESS RUNTIME'S OWN FONTS COULD CHANGE A PDF HASH BETWEEN ENVIRONMENTS

**This is not a hypothetical for this cell -- it is the reason the deployed function does
not render at all** (row `IRPT_BCKEND-W4-S9`). Four distinct ways the environment moves the
hash, from most to least likely:

1. **A DIFFERENT FALLBACK CHAIN RESOLVES DIFFERENTLY.** The templates ask for `Lato` and
   fall back to `Segoe UI, Arial, sans-serif`. Segoe UI is a Windows face; a Linux
   container has neither Lato nor Segoe UI unless they were installed, and resolves to
   whatever fontconfig offers -- DejaVu Sans, Liberation Sans, or nothing. Different
   glyphs, different advances, different content streams. **The document still renders and
   still validates.** Nothing in the PDF says which face was used for a fallback.
2. **THE ENGINE VERSION.** `renderer_version` names `chromium-print/msedge-channel` as a
   FAMILY, deliberately, because the exact build is not pinned and cannot be from here. A
   Chromium minor version can change text shaping, hyphenation and sub-pixel positioning.
   Two environments on the same "family" are not the same renderer.
3. **HINTING AND RASTERISATION SETTINGS.** For text these mostly affect the raster rather
   than the content stream, but `print-color-adjust`, DPI and `prefer_css_page_size`
   interact with the page box, and the media box is IN the content hash.
4. **THE LOCALE.** Number and date formatting in a document assembled by the template is
   ours, but anything the engine formats (e.g. a `<input type=date>` fallback, list
   markers) follows the environment's locale.

**What the hash actually certifies, stated precisely for the CVO:** two renders *in one
environment* of one frozen bundle produce one document. It does NOT certify that two
environments agree. The bundle pins the inputs and the versions it can name -- template,
renderer family, disclosure, brand revision -- and it cannot pin the font files or the
engine build, because neither is a value this cell is given. **A cross-environment
reproducibility claim needs the fonts packaged IN the render package and the engine pinned
by digest, and neither exists today.**

---

## 3. WHAT A READER OF THE RECEIPT CANNOT LEARN FROM IT

The receipt carries the export ref, the artifact (hash, bucket, key, `server_only`), the
facts (page count, validation status, failure count), the timestamps, the job state, the
download route with `requires_reauthorization`, and `vendor_signed_url_exposed`. It is
`additionalProperties: false`, so the list is closed. A reader therefore **cannot** learn:

1. **WHAT WAS IN THE DOCUMENT.** No section list, no account count, no date range. The
   receipt names an artifact; it does not describe one. Two exports of completely different
   scopes produce receipts distinguishable only by their hashes.
2. **WHETHER THE RENDER PACKAGE WAS THE FIXTURE OR THE REAL ONE.** This is the sharpest
   omission this cell can see. `package_is_fixture` is computed and printed by the worker
   and carried in the battery output -- and there is no field in the contract to put it in.
   **A receipt for an export rendered from the conforming FIXTURE is indistinguishable from
   one rendered from the counterpart's real package.**
3. **WHICH ASSETS WERE USED, OR REFUSED.** The bundle carries `approved_assets`; the receipt
   carries only `bundle_sha256`. A reader with the receipt alone cannot tell whether the
   firm's logo was used or the Opal template fallback was -- which is exactly the question a
   firm asks about its own branded document. The bundle answers it; the receipt points at
   the bundle by hash and the bundle is not attached.
4. **WHETHER THE PERFORMANCE REVISION CHANGED.** Arm (b)'s whole claim -- a branding change
   does not recalculate -- is a property of two BUNDLES. From two receipts a reader sees two
   different ids and two different hashes and cannot tell a rebrand from a recalculation.
5. **WHO AUTHORIZED IT, OR UNDER WHAT SCOPE.** No principal, no fingerprint, no entitlement
   revision. Deliberate -- a receipt is not an audit record and carrying a principal would
   put identity in an artifact that travels -- but it means the receipt cannot answer "was
   this person allowed to have this". Only the `_authz` audit trail answers that, and it
   lives elsewhere.
6. **WHAT `validation_status: PASSED` ACTUALLY CHECKED.** The enum is PASSED / FAILED /
   NOT_RUN with a failure COUNT. A reader cannot tell whether validation meant "the PDF
   parses and has pages" (which is what this cell implements) or something stronger. The
   count is 0 either way.
7. **WHETHER THE BYTES STILL EXIST.** The receipt is immutable and the object is not. A
   receipt that names a deleted or lifecycle-expired object reads exactly like one that
   names a present one; `verify_against_object()` is the check, and it needs the object.

**The honest summary:** the receipt is a good *pointer* and a poor *description*. Every gap
above is answerable from the BUNDLE, which the receipt names by hash -- so the missing piece
is not a field, it is that nothing in this round stores the bundle beside the artifact where
a reader can fetch it. That is one line of storage and it is not in this order's cell.
