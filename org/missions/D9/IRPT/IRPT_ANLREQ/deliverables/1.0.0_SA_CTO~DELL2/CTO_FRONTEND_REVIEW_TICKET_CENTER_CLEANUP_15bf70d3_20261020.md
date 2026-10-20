# CTO front-end review: the Ticket Center Analysis Request form on cand/dell2/anlreq-ticket-center-cleanup @15bf70d3 (2026-10-20 ~01:2xZ)

**Asked by:** Andrew (relayed, MSTR msg 11150): "check the front-end flow is logical". It is a read of the code, not a run. Paths are under
`src/pages/TicketCenter/`; Parts = `AnalysisRequestParts.tsx`, aR = `analysisRequest.ts`.

**Ruling:** `2.0.0_SA_COO~Y2` cuts ONE repair cell on the cleanup branch BEFORE the DEV merge, carrying every MUST item. The SHOULD items
ride the same cell if cheap.

## The step order a staff user sees

1. Press New Ticket. The type starts as Service Request; the user picks Analysis Request, then fills Title.
2. Advisor (required), then Firm ("Loading firms..." until the list appears), then Household (required).
3. Five Opal-model checkboxes and a free-text "Other ETFs" field.
4. Needed by, then the holdings file (.csv or .xlsx).
5. A line saying why the button is held, then "File Analysis Request".
6. "Still processing the file", or findings with Yes / Replace / No per unknown ticker. Each press files again.
7. On success the form closes; a steps panel and a notice appear.
8. The ticket row offers Claim, Retry, Open report and Complete. Open report opens a panel with the figures first and a closed
   "Technical details".

## MUST (each breaks a v0.24 outcome or strands the user)

1. **A blank Advisor is refused** ("Advisor is required.", aR:71; the field is required at Parts:177). This contradicts FWD-1 and C-FIRM:
   staff are never refused for want of an advisor. Make it optional for staff, matching AR-y-415's owner fallback.
2. **The submit button is enabled on invalid forms.** A missing Household, an unknown ETF and more than 5 comparables are each refused only
   after the press (aR:71-73, 389-397, 514-526). Gate the button on them and name the reason in the held line.
3. **If the firm list fails to load, staff cannot file at all** (Parts:104 requires a listed firm).
   - Add a retry that also clears the stale "could not be loaded" banner (TicketCenter.tsx:333-337).
   - Show the reason.
4. **While firms load or have failed, the held line says "Choose the firm..." with no firm control on screen** (aR:395, Parts:179-187).
   Say what is actually happening.
5. **The ETF list goes stale.** Typed before a firm is chosen, it is fetched with no firm and never fetched again (TicketCenter.tsx:364).
   Re-fetch it when the firm changes.
6. **The Keep words are never seen.** A No press re-files and clears the findings (TicketCenter.tsx:396), and a successful re-file closes the
   form (:428), so the kept line (Parts:304-305) never shows. Show it in the success notice. Also replace aR:174's text with this seat's
   words (msg to `~Y2` 00:40Z): "<X> is kept as you typed it. It is not priced on this form; the report matches it to a comparable fund or
   lists it as not analysed."

## SHOULD

- The button reads "Uploading..." while it is actually fetching the ETF list (TicketCenter.tsx:374-379, 402, 831). Word it truthfully.
- The hint reads "Did you mean X? (row N: Y)" without the fund name (aR:166). Add the name where the catalogue has it.
- Open report renders below the whole board (TicketCenter.tsx:964). Render it by the ticket row, or scroll to it.

## Implemented as required

- No report type, email or commentary box.
- The models at first paint.
- The CSV or XLSX upload.
- "Technical details" closed by default.

-- 1.0.0_SA_CTO~DELL2
