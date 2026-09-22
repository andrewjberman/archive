# AMGT-rk-125 -- LIVE-ORIGIN RENDER READ

`0.9.0_WK_AMGT_RESAPP~125`, round 31. READ-ONLY. All captures against `https://opalinvest.dev`
(the deployed origin, per `--origin`), unauthenticated (inert stub session -- `IDENTITY:
firmId=opal-capital userType=Dev role=admin firmRole=null`, no `--token`). Every PNG below was
opened and read with the Read tool before this file was written -- confirmed here explicitly, and
each row below states what was seen, not what was assumed.

## AC2 -- how a security is actually selected

**FINDING: the selection form is a ROUTE PATH SEGMENT, `/security-analysis/<securityKey>`, NOT a
query string, and it is NOT click-only.**

- Router: `portal/src/App.tsx:448` `<Route path="/security-analysis/:securityKey" element={...} />`
  (`:447` is the no-selection form, `/security-analysis`).
- Page: `portal/src/pages/SecurityAnalysis/SecurityAnalysis.tsx:43` `const { securityKey:
  routeSecurityKey } = useParams<{ securityKey?: string }>()`, `:47` `useSecurityAnalysisState(routeSecurityKey)`.
- Hook: `portal/src/pages/SecurityAnalysis/hooks/useSecurityAnalysisState.ts:22`
  `export function useSecurityAnalysisState(initialSecurityKey?: string)`, `:29-31` seeds
  `selectedSecurityKey` from it with `useState(initialSecurityKey ?? null)`.

The issuer's `?security=...` probe failed because that is the wrong form -- there is no query-param
reader anywhere in this chain. Navigating straight to `/security-analysis/BA_US_Equity` lands with
`LOC : /security-analysis/BA_US_Equity` (confirmed by direct capture, `ba_probe.png`) and the page
immediately shows the SELECTED state (Lead Panel switches from the ranked list to
`SecurityOverlay`, and the five tabs stop showing "Select a name..."). No click was needed. This is
the method used for all 10 captures below.

## The capture set -- 13 PNGs in `.scratch/r125/`, 10 of them the required set

TARGET was 10 (2 names x 5 tabs). Produced: all 10, plus 3 supplementary captures kept because
they carry findings this report cites -- none is a substitute for a missing target capture:

- `base_live.png` -- AC1's literal control capture (no selection), reproducing the issuer's
  cut-time evidence. Byte-for-byte reproduction: `IDENTITY`, `VIEWPORT`, `CANVAS rgb(244, 246,
  250)` and `LOC /security-analysis` all match what the order's record face already committed.
- `ba_probe.png` -- the AC2 selection-form probe (`/security-analysis/BA_US_Equity`, default
  Thesis tab). Superseded by `BA_US_Equity__thesis.png` below (same content) but kept as the
  evidence that the URL form works at all.
- `_diag_exec_longwait.png` -- a diagnostic re-capture of BA_US_Equity/Exec Management with
  `--clickwait 10000` instead of the default 2500ms, to see whether the "Loading..." seen in the
  standard-window capture ever resolves to something else. It does: it resolves to a BLANK PANEL
  with no text at all (see the Exec Management row below). Not one of the 10 target tabs; run to
  settle a question the 10-set alone could not answer.

Every one of the following 10 rows is a capture actually produced and read; none is missing.

## Per-capture table

Each row: NAME / TAB -- RENDER CLASS -- quoted on-screen text (verbatim from the PNG).

| # | Name | Tab | Render class | Quoted on-screen text |
|---|---|---|---|---|
| 1 | BA_US_Equity | Thesis | EMPTY-NO-EXPLANATION | Panel "THE BIG THING" header + subtitle "The thesis driver's series from the model block, or ABSENT with the reason" -- body area below is BLANK, no text. Panel "THESIS" header + subtitle "Machine sentences marked, each one above the source passage it rests on" -- body area below is also BLANK, no text. |
| 2 | BA_US_Equity | Exec Management | ABSENCE-WITH-REASON (transiently) then EMPTY-NO-EXPLANATION (settled) | At default 2500ms click-wait: "Loading...". At 10000ms click-wait (`_diag_exec_longwait.png`): the "Loading..." text is GONE and the panel body is BLANK -- no text, no icon, nothing. |
| 3 | BA_US_Equity | Peers | ABSENCE-WITH-REASON (transient only, not re-probed at long wait) | "Loading..." at the standard capture window. Given row 2's long-wait result and identical source shape (below), this is judged to settle the same way, but was not independently re-probed at 10s. |
| 4 | BA_US_Equity | Model | ABSENCE-WITH-REASON (transient only, not re-probed at long wait) | "Loading..." at the standard capture window. Same caveat as row 3. |
| 5 | BA_US_Equity | Posture | ABSENCE-WITH-REASON (transient only, not re-probed at long wait) | "Loading..." at the standard capture window. Same caveat as row 3. |
| 6 | 992_HK_Equity | Thesis | EMPTY-NO-EXPLANATION | Byte-identical (sha256) to row 1. Same two blank panel bodies. |
| 7 | 992_HK_Equity | Exec Management | ABSENCE-WITH-REASON (transient) | Byte-identical (sha256) to row 2's standard capture: "Loading...". Not independently long-wait-probed for this name, but see row 2's settle result -- the source is the SAME component regardless of name. |
| 8 | 992_HK_Equity | Peers | ABSENCE-WITH-REASON (transient) | Byte-identical (sha256) to row 3: "Loading...". |
| 9 | 992_HK_Equity | Model | ABSENCE-WITH-REASON (transient) | Byte-identical (sha256) to row 4: "Loading...". |
| 10 | 992_HK_Equity | Posture | ABSENCE-WITH-REASON (transient) | Byte-identical (sha256) to row 5: "Loading...". |

**The two names render BYTE-IDENTICAL PNGs per tab** (sha256 verified, not just eyeballed): the
five BA_US_Equity tab captures and the five 992_HK_Equity tab captures hash-match pairwise. Neither
name produces name-specific content in this unauthenticated run -- consistent with both requests
failing the same way against the live API (see below).

## THE DISCRIMINATOR -- per-tab verdict: could a viewer tell a failed read from an absent object?

**NO, on all 5 tabs, and this is confirmed at the SOURCE, not just from the captures.** Every one of
the five tab components shares the identical two-line render gate:

```
{isLoading && <p>Loading...</p>}
{!isLoading && data && <...real content...>}
```

- `ThesisTab.tsx:161,177` (two panels, same gate each)
- `ExecManagementTab.tsx:235-236`
- `PeersTab.tsx:164,166` (+167/173 for sub-states, all still gated on `data` truthy)
- `ModelTab.tsx:204-205`
- `PostureTab.tsx:379-381`

**There is no third branch.** When `isLoading` becomes `false` and `data` is still falsy -- which is
exactly what happens when the underlying `useQuery` (react-query, `retry: 2` at
`useLeadPanelApi.ts:120`) exhausts its retries against a failing fetch (e.g. this run's 401,
matching the Lead Panel's own diagnosis below) -- **both conditions are false and NOTHING renders.**
Not an error icon, not a sentence, not even an empty-state placeholder: a blank panel body. This
is the byte-for-byte state captured in every "settled" row above (row 1, row 6, and row 2's
long-wait diagnostic). The transient "Loading..." seen in rows 2-5 and 7-10 is not a stable state --
`_diag_exec_longwait.png` shows it is gone by 10s, replaced by the same blank nothing.

**Per tab:**
- **Thesis: NO.** Settles to two blank panel bodies. No isError read anywhere in the file.
- **Exec Management: NO.** Confirmed transient-to-settled by direct long-wait capture. Blank body once settled.
- **Peers: NO (by source parity with the other four; not independently long-wait captured).**
- **Model: NO (by source parity; not independently long-wait captured).**
- **Posture: NO (by source parity; not independently long-wait captured).** Note per the order's own
  warning: `PostureTab.tsx:323`'s `READ_FAILED` string is a SERVER-SIDE sub-object status
  (`posture.status === 'READ_FAILED'`), reachable only inside the `!isLoading && data` branch --
  i.e. only when the outer HTTP read already SUCCEEDED and returned a payload whose `posture` field
  itself carries that status. It cannot fire on a client fetch failure and does not contradict the
  finding above.

**0 of 5 tabs carry an `isError` branch**, confirmed both by the source read above and by what the
captures show at settle time: the identical blank-body class across Thesis (already blank in the
standard window) and the four others (blank once the retry budget is spent). `useThesisBundle` /
`usePeerSet` (`useLeadPanelApi.ts:105-133`) return `{ data, isLoading }` via destructuring in every
tab; react-query's `isError`/`error` fields exist on the query result object but are never read by
any of the five tab components.

## The positive control, quoted -- the Lead Panel CAN discriminate, in its no-selection state

The issuer's committed cut-time evidence (`round31_cut_evidence/live_origin_unauthenticated_20260922T2240Z.png`,
reproduced identically by this order's AC1 / `base_live.png`) shows the Lead Panel's ranked-list
read-failure block **naming the fault in plain language**:

> "Read failure -- the ranked names could not be read ... Error reported by the read: API request
> failed: 401 - {"error":"Invalid or expired token"}"

That block is `RankedList.tsx:139-160` -- it DOES carry a real failure branch and prints the actual
HTTP status and body. This is the contrast the cell exists to state: one component on this page
can tell a viewer a read failed and why; the five tabs cannot tell a viewer anything at all.

**Additional finding, not required by AC4 but relevant to the same discriminator:** once a security
IS selected, the Lead Panel's OWN content switches from `RankedList` to a different component,
`SecurityOverlay.tsx`. That component's empty state (`:73-74`) is `if (!bundle) return <div>No
overlay data for this name yet.</div>` -- the SAME undiscriminated shape as the five tabs (fires
whether `bundle` is undefined because of "still loading forever", "the fetch failed", or "genuinely
no data"). So the Lead Panel's discrimination capability shown in the positive control is specific
to its NO-SELECTION (ranked-list) state; in its SELECTED (overlay) state it degrades to the same
silent class as the tabs. This is named here because it directly touches the cell's discriminator
question and was found while reading the Lead Panel component the captures show; it is not one of
the 10 tab captures and is not counted toward AC3's target.

## Read confirmation

All 13 PNGs in `.scratch/r125/` were opened and read with the Read tool during this session:
`base_live.png`, `ba_probe.png`, `BA_US_Equity__{thesis,exec_management,peers,model,posture}.png`,
`992_HK_Equity__{thesis,exec_management,peers,model,posture}.png`, `_diag_exec_longwait.png`.
