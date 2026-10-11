# YCD-a-11: Andrew's journey read hop by hop at HEAD, and the slug's 26 rows read against it

Worker 0.9.0_WK_IRPT_YCDGEN~14, task order IRPT_YCDGEN.TO-YCD-a-11. Read-only: no product file changed, no generation, no HTTP call, no AWS call.
Repo HEAD read: 54683e95a48b61956c88e9dcd60a5354cd6532a9. Portal HEAD read: dbeb6764eaa688230f44cfcc1763bd73db6e1142 (a separate checkout, read at C:/dev/ajb_workspace/portal).
Machine record: JOURNEY_READ_YCD-a-11.json beside this file (refs are path and line; portal paths are written portal/...).

The journey: Andrew, signed in as andrew@opalinvest.com (an Opal-internal principal, firm opal-capital), submits one Cottonwood portfolio for an Overview from the Analysis tab and opens the Opal-made report.
Convention for on_path: the Analysis tab offers two portfolio cards (hop 1), and which one Andrew presses is his choice at the sitting. A row is YES when it sits on at least one branch he can take; the note says which branch.

## Result in one paragraph

Of the 26 rows, 7 are MET at HEAD (W1-S4, W1-S8, W3-S12, W3-S18, W2-S14, S12, W2-S16) and 19 are OPEN. Of the OPEN rows, 10 sit on Andrew's path (YES), 1 are NOT_DETERMINED and the rest are off it. The three rows the issuer read before the cut (W1-S8, W3-S12, W3-S18) are confirmed MET by my own runs. By code read, no OPEN row refuses the Opal run itself. The ones that can stand between Andrew and an opened, Opal-worded report are on the page (the opened report speaks the v1 vendor wording, new row D2-W14-S1), on the Prospect branch's status and the report surface (new row D2-W14-S2), on the picked-client branch (S13, which cannot submit at all), and on the failure branch (D2-S49).

## The hops, in order

| n | Hop | What it does for Andrew and Cottonwood | Key refs |
|---|---|---|---|
| 1 | Analysis tab, page 1: Select the portfolio (Client card or Prospect card) | The tab opens on page 1 with two cards. | AnalysisTab.tsx:235; AnalysisTab.tsx:307; AnalysisTab.tsx:340 |
| 2 | The composer and the portfolio basis: the Prospect upload branch, and the picked-client branch | UPLOAD branch: for an internal principal the card shows a firm select and sends the CARD's firm as selected_tenant; with no firm chosen it sends nothing and says so in words (stagedProspect.ts:159-162, ProspectComposer.tsx:268, 312, 434, 578). | ProspectComposer.tsx:133; ProspectComposer.tsx:157; stagedProspect.ts:159 |
| 3 | The request the browser sends | Upload: POST /analysis/inputs with the file base64 and ?selected_tenant=<firm> (investor-reporting.ts:1100-1103). | prospect.ts:139; stagedProspect.ts:171; investor-reporting.ts:1325 |
| 4 | The route and its authorizer (the verified edge headers, then the firm binding) | POST /api/scoped/investor-reporting/analysis is served by irpt-ycharts-generate (entry.py:147-152, routes.json:71-79). | entry.py:147; routes.json:71; served.py:307 |
| 5 | Owner resolution for an internal principal (who owns the request) | For an internal subject the owner is built from his own identity at the input's firm: firm_id cottonwood, principal_id andrew@opalinvest.com, principal_class OPAL_GLOBAL (interactive_access.py:78-137, prospect_submission.py:72-73). | served.py:1047; interactive_access.py:78; interactive_access.py:123 |
| 6 | Acceptance: frozen composition, retained input, atomic accept, queue send | submit_analysis validates the closed public body (submission.py:47-90), then SubmissionService.submit resolves the owner, re-authorizes, freezes the composition as a retained REQUEST_COMPOSITION, accepts it with acting_principal_id, then dispatches one queue message and answers {identity, stage RECEIVED} (submission_service.py:103-167). | entry.py:97; submission.py:47; submission_service.py:103 |
| 7 | The resident worker polls the queue and re-checks the acting principal | poll_once receives one message at 900 s visibility, execute() rebuilds the closed message from the accepted record and re-grades the owner's current profile row (current_authority.decide: active, home firm, created before acceptance, allowedFirmIds), so an OPAL_GLOBAL Andrew is allowed for cottonwood unless his row lists other firms. | resident_worker.py:799; resident_worker.py:625; resident_worker.py:637 |
| 8 | The resident worker's choice of producer (producer_for, the allow list) | producer_for reads the accepted record's owner.principal_id against OPAL_PRODUCER_PRINCIPALS = ('andrew@opalinvest.com',) (resident_worker.py:121-133). | resident_worker.py:121; resident_worker.py:128; resident_worker.py:686 |
| 9 | The Opal producer: read holdings, classify, compute, render, record | produce() reads the frozen holdings from the firm store, reads classifications from the one table, computes the three classified elements and marks every price-based, builder-only and vendor-call element NOT_IN_THIS_VERSION (C-V1), renders the Opal-branded PDF with no vendor wording (layout_overview.py:961-962, 1053-1054; Data: Opal Capital), builds run.json and the AnalysisReport v2 document (opal_producer.py:272-339). | opal_producer.py:272; opal_producer.py:211; runner.py:443 |
| 10 | Retention and publish: PDF artifact, document spill, checkpoint, READY | run_opal retains the PDF as a YCHARTS_OPAL_REPORT artifact, checkpoints it, retains the whole Opal document as a json artifact on every Opal checkpoint (publication_worker.py:96-99; row W3-S13), publishes through the publisher's Opal branch, marks READY and sends I3 (resident_worker.py:449-490). | resident_worker.py:449; resident_worker.py:478; publication_worker.py:55 |
| 11 | The status read and the sections read | GET /status/{jobId} (irpt-status) maps the durable phase to a public state; READY becomes READY only when the date opt-in header is sent and the retained input's dates derive (owned_status.py:43-58, prospect_dates.py:30-65 now has an OPAL_ENGINE branch). | owned_status.py:12; entry.py:201; entry.py:218 |
| 12 | The page that opens the report: Your analysis requests, the opened request, Report sections | After Generate the report is opened from OwnedRequestHistory, a dialog that reads the request, then the sections (OwnedRequestHistory.tsx:326-339) and shows RetainedSections (:407). | AnalysisTab.tsx:397; OwnedRequestHistory.tsx:326; OwnedRequestHistory.tsx:392 |

The full finding for each hop, with every ref, is in the json (field `hops`).

## Per hop: the OPEN rows that sit on it (what stands in Andrew's way)

### Hop 1: Analysis tab, page 1: Select the portfolio (Client card or Prospect card)

No OPEN row on this hop is on Andrew's path.

### Hop 2: The composer and the portfolio basis: the Prospect upload branch, and the picked-client branch

- IRPT_YCDGEN-S13 (ON PATH): Still true on the picked-client branch: the browser snapshot id is the source:revision join with commas (adapt.ts:1121, GenerateComposer.tsx:209-211), which the identifier rule refuses (submission.py:44, 86), and the server needs cst_<64 hex> (custody_binding.py:148, accepted_custody.py:106); no cst_ string exists in the portal source. Not on the Prospect upload branch (input_id, snapshot_id null).

### Hop 3: The request the browser sends

No OPEN row on this hop is on Andrew's path.

### Hop 4: The route and its authorizer (the verified edge headers, then the firm binding)

No OPEN row on this hop is on Andrew's path.

### Hop 5: Owner resolution for an internal principal (who owns the request)

- IRPT_YCDGEN-D2-S4 (NOT DETERMINED): An on-behalf upload needs a named advisor only when the tenant is in the filer's allowedFirmIds (served.py:1063-1066); otherwise the filer's own owner is used (1066). Andrew's own profile row (opal-users-v2, allowedFirmIds) was not read: if it is absent he is not on-behalf and this row is off his path; if it lists cottonwood he cannot upload (no cottonwood advisor row, per the row). Read that settles it: his user row's allowedFirmIds.

### Hop 6: Acceptance: frozen composition, retained input, atomic accept, queue send

No OPEN row on this hop is on Andrew's path.

### Hop 7: The resident worker polls the queue and re-checks the acting principal

- IRPT_YCDGEN-D2-S49 (ON PATH): Still true at HEAD: a generate-kind message that raises is never deleted and no code on the generate branch writes a dead-letter record or reason (the exhaustion handler _end_exhausted_resolve exists only for resolve_upload, resident_worker.py:843-849, 927). On Andrew's path only on the failure branch: if his job fails every delivery it reads RECEIVED with no reason.

### Hop 8: The resident worker's choice of producer (producer_for, the allow list)

No OPEN row on this hop is on Andrew's path.

### Hop 9: The Opal producer: read holdings, classify, compute, render, record

- IRPT_YCDGEN-W1-S9 (ON PATH): Two of the three parts are met: the closed set is reached through closed_reason (opal_producer.py:102-121) and table values are written as a JSON string (opal_producer.py:149-154). The first part still reads true: layout_overview.py holds only the method NAMES (CLASSIFY_METHODS, line 212); the three classified elements are built in the producer (opal_producer.py:67-88), not carried by the layout. Not blocking: Andrew's run gets the elements from the producer.
- IRPT_YCDGEN-W1-S10 (ON PATH): Still true: inputs_as_of = {name: run_date} and run.json inputs carry as_of_basis READ_DATE (opal_producer.py:297-299).
- IRPT_YCDGEN-W2-S12 (ON PATH): The four choices (nullability, inputs_as_of shape, coverage type, VALUE-branch reason) are what Andrew's document is written with (opal_producer.py:323-336); the remedy is a CTO confirmation, a ruling record this read did not search for. Not blocking his run.

### Hop 10: Retention and publish: PDF artifact, document spill, checkpoint, READY

- IRPT_YCDGEN-W3-S13 (ON PATH): Still true: for kind OPAL the checkpoint always retains the document as an EXTRACTION_EVIDENCE artifact (publication_worker.py:96-99, publisher.py:43-44); the design is stated (publisher.py:13) but not its cost. Every Opal job of Andrew's passes through it. Not blocking.
- IRPT_YCDGEN-W3-S16 (ON PATH): Still true: with artifacts injected (resident_installed.py:248) the PDF goes to the retained artifact (opal_producer.py:309-313) while run.json report.key stays the layout's address (305-307).

### Hop 11: The status read and the sections read

- IRPT_YCDGEN-W2-S13 (ON PATH): Still true: the sections answer for an Opal document carries provider, computation_validation and retained_ref (owned_report.py:96-100) while the published response schema requires extraction_validation and has additionalProperties false on data (schema lines 48-52). The portal reads the Opal slice (responses.ts:166-170), so the page is not blocked by it.
- IRPT_YCDGEN-W6-S4 (ON PATH): Same fact as W2-S13 on the document schema side: data requires request_ref, sections, extraction_validation (schema line 48-52). No runtime check of the response against this schema was found on the serving path (only contract tests read it).

### Hop 12: The page that opens the report: Your analysis requests, the opened request, Report sections

- IRPT_YCDGEN-W4-S8 (ON PATH): Still true: adaptOpalAnalysisReport (adapt.ts:1009-1033) and adaptAnalysisReportSlice (1412-1419) set no provider on the view; NativeSections decides from sections (NativeSections.tsx:87-89). On Andrew's path the slice view has no provider at all, which is why RetainedSections cannot tell.
- IRPT_YCDGEN-D2-W14-S1 (ON PATH): NEW, filed by this read. The page that opens the report (RetainedSections) draws an Opal report with the v1 vendor wording: 'Vendor attribution:' per section and 'Extraction validation' under Technical details. OwnedRequestHistory.tsx:151-167, 407; NativeSections.tsx:105, 186-190; adapt.ts:1400-1419.
- IRPT_YCDGEN-D2-W14-S2 (ON PATH): NEW, filed by this read (INFERRED). After a Prospect Generate the composer's own status line is read with no selected_tenant (ProspectComposer.tsx:584), and 'Your analysis requests', the only surface that opens the report, is mounted only when the header holds a client (AnalysisTab.tsx:397-409).

## The remaining rows, one line each

- IRPT_YCDGEN-D2-S45: OPEN, on path NO; needs a live read. ARMED redrive hazard on the 8 dead letters in irpt-generation-dlq: a live queue fact.
- IRPT_YCDGEN-D2-S46: OPEN, on path NO. Line 110 is unchanged: opal_source = provenance.get('opal_map_source') if base_pin else None.
- IRPT_YCDGEN-D2-S47: OPEN, on path NO. Line 7 still reads VER=__ST30_SCRIPT_VERSION__.
- IRPT_YCDGEN-S9: OPEN, on path NO; needs a live read. The FRED risk-free object's age is a served S3 fact (read the object's last write and last observation).
- IRPT_YCDGEN-W1-S4: MET, on path YES. Every layout reason now passes closed_reason() before it is written (NOT_HELD:* to NOT_IN_THIS_VERSION or INPUT_MISSING:<name>, OUTSIDE_TIME_BUDGET to NOT_IN_THIS_VERSION, others to INPUT_MISSING:<prefix>), and a vendor-call element with no answer is NOT_IN_THIS_VERSION (opal_producer.py:139-142).
- IRPT_YCDGEN-W1-S8: MET, on path YES. Confirms the issuer's read.
- IRPT_YCDGEN-W3-S12: MET, on path NO. Confirms the issuer's read.
- IRPT_YCDGEN-W3-S18: MET, on path NO. Confirms the issuer's read.
- IRPT_YCDGEN-W2-S14: MET, on path NO. NativeSections now has the Opal form (isOpalReport, Report sections heading, computation validation, method and coverage, no vendor attribution; NativeSections.tsx:40-49, 199-230) and the typed contracts carry provider and the Opal wire (index.ts:691-695, wire/AnalysisReport.ts:123-149, responses.ts:166-170).
- IRPT_YCDGEN-S12: MET, on path YES. No longer true in the browser: an internal principal with no firm chosen sends nothing and sees 'Choose the firm this portfolio is for before you review it.' (stagedProspect.ts:145, 159-162; the buttons are disabled at ProspectComposer.tsx:434, 578), and the client composer returns NO_FIRM_MESSAGE (GenerateComposer.tsx:175, 195).
- IRPT_YCDGEN-W2-S16: MET, on path YES. No longer true: selectedTenantFor reads the global firm's tenant first (index.tsx:153-164) and feeds the selected scope ref (:259-262); the composer reads and submits nothing when the tenant is missing (GenerateComposer.tsx:165-197, 267).
- IRPT_YCDGEN-W3-S21: OPEN, on path NO; needs a live read. Settling it means running the portal test suite (which this order forbids, since a run may modify tracked portal files) and reading git status after.
- IRPT_YCDGEN-D2-W7-S2: OPEN, on path NO. Still true: the generator reads logo variants from the gitignored logo_package (03_extract_brand_spec.py:11, 170-211) and the packaged brand.json carries formats {} and preferred null (brand.json:234-246).
- IRPT_YCDGEN-D2-S19: OPEN, on path NO; needs a live read. The research role is minted by name from the firm (runner.py:479-493); whether irpt-<firm>-ycharts-research-role exists for each firm the policy row names is an IAM fact: read iam get-role and the runner role's AssumeRole statement.
- IRPT_YCDGEN-D2-S25: OPEN, on path NO. An instrument and wording row about the seats' served-read window ledgers (updatedAt continuity).

## What this read could not establish

- Which card Andrew presses (Client or Prospect). Rows S13 and W2-S16 are on the Client branch only; D2-S4 and D2-W14-S2 are on the Prospect branch only. Each is marked by its branch. His sitting settles it.
- D2-S4: whether Andrew's own opal-users-v2 profile row lists cottonwood in allowedFirmIds. If it does not, the on-behalf rule never applies to him; if it does, he cannot upload for cottonwood. One served read of that row settles it (marked NOT_DETERMINED).
- D2-S19, D2-S45, S9: live facts (the cottonwood and 49f research roles, the dead-letter queue, the age of the FRED object). Settled by iam get-role and the runner role's AssumeRole statement, the DLQ inventory and queue depth, and an S3 head of the held risk-free object.
- W3-S21: whether the portal test run leaves tracked files modified. It needs a portal test run, which this order does not allow (a run can write tracked files). The portal checkout read was clean. A throwaway portal worktree and one bun test run settle it.
- D2-W14-S2: the exact answer of an internal principal's status read with no selected_tenant is taken from a portal comment (OwnedRequestHistory.tsx:401-403), not measured. One served GET without selected_tenant settles it.
- D2-W14-S1 and S12 and W2-S16 were read from code. The Analysis tab was not rendered; a portal test over RetainedSections with an Opal slice settles the first, Andrew's sitting the rest.
- W2-S12: whether the CTO has already ruled on the four choices. No ruling record was searched for.
- D2-S25: the window ledgers it is about were not re-read; the row is an instrument and wording row, off the journey.
- The deployed versions: this read is of HEAD. Which build the resident host (root 37210c771a-st30) and the deployed portal actually run was not read.
- That the live Opal run works end to end: this is a code read. FWD-1 is EXERCISED only by Andrew's own sitting.

