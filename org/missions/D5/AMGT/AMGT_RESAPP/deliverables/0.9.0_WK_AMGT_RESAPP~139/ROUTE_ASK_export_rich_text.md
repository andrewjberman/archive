# ROUTE ASK -- serve `build_rich_text` (FWD-30 branch (b)) on a live route

**Status: ASK, not built.** `C-PRESENTATION-ONLY` names `FWD-30` as one outcome that returns
to `1.0.0_SA_CTO~Z` BEFORE it is built -- this is that return. AMGT-rl-10 built and proved the
producer (`lib/research/print/render_pack.py:build_rich_text`, wired through `build_pack`'s new
optional `thesis_bundle`/`peer_set`/`posture` arguments) and the parity harness that measures it
against the page (`portal/src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs`,
`EXPORT-COMPARE OK` on BA_US_Equity: 162/162 figures, 43/43 cites, every page absence covered).
**Nothing below is built.** `lib/research/api/scoped_amgt.py` and
`portal/src/api/endpoints/amgt-lead-panel.ts` are untouched by this cell.

## 1. The leaf

Reuse the EXISTING print leaf rather than mint a new one -- it already carries the security-key
path parameter, the identity resolution and the `AdapterError` refusal shape `_print_pack` uses:

```
GET {ROUTE_PREFIX}/security/{security_key}/print
GET {ROUTE_PREFIX}/security/{security_key}/print?format=rich   <- NEW query parameter
```

`format` defaults to `pdf` (today's behaviour, byte-identical -- AC2's own negative control
proves `build_pack`'s PDF/txt are unchanged whether or not the new bundles are supplied).
`format=rich` is the ONLY new surface: no new route, no new path segment, no new method.

## 2. The shape

`_print_pack` (`lib/research/api/scoped_amgt.py:4047`) branches on `format` after its existing
identity resolution and `read_model_block` call:

```python
def _print_pack(security_key, identity=None, format="pdf"):
    ...  # unchanged: resolve identity, read_model_block, refuse on a made-up display form
    if format == "rich":
        from lib.research.print.render_pack import build_rich_text
        md_path = build_rich_text(
            display_form, block,
            thesis_bundle=read_thesis_bundle(resolved_key),   # already a function this module owns
            peer_set=read_peer_set(resolved_key),             # already a function this module owns
            posture=read_posture(resolved_key),                # already a function this module owns
            out_dir=<lambda tmp dir>,
        )
        with open(md_path, "r", encoding="utf-8") as handle:
            body = handle.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/markdown; charset=utf-8"},
            "body": body,
            "isBase64Encoded": False,
        }
    pdf_path, _ = build_pack(display_form, block)   # unchanged
    ...
```

## 3. The inputs the adapter ALREADY HOLDS, and where they hand over

Every input `build_rich_text` needs is already read by an EXISTING function in
`lib/research/api/scoped_amgt.py` for the Thesis/Exec/Peers/Posture tabs' own routes -- this ask
adds no new reader:

| `build_rich_text` param | Adapter function already reading it | Existing route that already serves it |
|---|---|---|
| `thesis_bundle` | `read_thesis_bundle(security_key)` | `GET .../security/{key}/thesis` |
| `peer_set` | `read_peer_set(security_key)` (peers leaf's own reader) | `GET .../security/{key}/peers` |
| `posture` | `read_posture(security_key, identity=None)` (`scoped_amgt.py:2854`) | (posture is ALSO embedded as `thesis_bundle["posture"]`, per `tabsFixture.BA_US_Equity.json`'s own captured shape -- either source is correct; `read_posture` is named here because `_print_pack` need not thread the identity dict `read_thesis_bundle` returns through a second lookup) |

The hand-over point is `_print_pack` itself: it already resolves `resolved_key` and already
calls `read_model_block(resolved_key)`; the three new calls sit right beside that one, gated by
`format == "rich"` so the default path never spends them (AC2's negative control's LIVE-route
mirror: an unchanged `format=pdf` request costs nothing new).

## 4. The content type and the client change

- **Content-Type**: `text/markdown; charset=utf-8` (GitHub-flavoured Markdown, per
  `build_rich_text`'s own output) -- API Gateway's binary-media-type handling is NOT needed
  (unlike the PDF path's `isBase64Encoded: True`): markdown is text, so `isBase64Encoded: False`
  and a plain UTF-8 body.
- **Client**: `requestPrintPack`'s sibling in `portal/src/api/endpoints/amgt-lead-panel.ts`:

  ```typescript
  export function printRichTextPath(securityKey: string): string {
    return `${BASE}/security/${encodeURIComponent(securityKey)}/print?format=rich`
  }

  export async function requestPrintRichText(securityKey: string): Promise<string> {
    const accessToken = localStorage.getItem('accessToken')
    const response = await fetch(printRichTextPath(securityKey), {
      headers: { ...(accessToken && { Authorization: `Bearer ${accessToken}` }) },
    })
    if (!response.ok) {
      throw new Error(`Print rich-text request failed: ${response.status} ${response.statusText}`)
    }
    return response.text()   // NOT .blob() -- this is text, not a binary PDF
  }
  ```

  `PrintExportAction.tsx` would need a second trigger/state (or a format toggle inside the
  existing preview modal) to call `requestPrintRichText` and render the returned markdown --
  out of THIS cell's write surface (bounds section 1 names this file read-only for the route/
  adapter/client layers; only its C11 idiom fix landed here).

## 5. Recommendation

Wire `format=rich` onto the EXISTING `/print` leaf (section 1-2 above) rather than mint a new
route: it reuses the identity resolution and refusal shape `_print_pack` already has correct,
every input is an EXISTING reader (`read_thesis_bundle`, `read_peer_set`, `read_posture` all
already live in `scoped_amgt.py`) with an EXISTING route already serving the same data, and the
default (`format=pdf`) path is untouched (proven byte-identical, AC2). The only genuinely new
work is the three-line client sibling (section 4) and the modal's own second trigger, both
outside this cell's granted paths.
