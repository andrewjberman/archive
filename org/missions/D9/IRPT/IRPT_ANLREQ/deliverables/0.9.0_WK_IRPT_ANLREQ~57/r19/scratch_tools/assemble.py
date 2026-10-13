import json
import os

S = "C:/dev/wk-irpt-anlreq-57/.scratch/r19"
W = "C:/dev/wk-irpt-anlreq-57"
OUT_DIR = W + "/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~57/r19"
OUT = OUT_DIR + "/PORTAL_UPLOAD_ANSWER_READERS.json"

PROD_SHA = "37aa1247ee4ba487e5610dc5b78d65ae28468a99"
DEV_SHA = "64980b4d3a1e11d8407b6a263ddcd5447dafaef2"

RECORD_SHEETS = {"two_sheet_workbook", "total_row_sheet", "two_value_account_sheet", "one_account_sheet",
                 "repair_header_two_values", "repair_header_one_value", "attribute_header_one_account",
                 "brokerage_two_account"}

raw = json.load(open(S + "/run_hr/readers_raw.json", encoding="utf-8"))
dep = json.load(open(S + "/run_hr/readers_deployed_shape.json", encoding="utf-8"))

READERS = [
    {"file": "src/pages/InvestorReporting/contracts/envelope.ts", "line": "246-273 (adaptAnalysisUpload); map entry 182",
     "reads": "upload_id; state (closed set of three); input_id; reason on NEEDS_CORRECTION; input_ref and portfolio on NORMALIZED; presence of findings/template on RESOLVING. Finding codes and descriptions are returned UNREAD.",
     "key_policy": "EXACT (state and reason)",
     "at_prod": "envelope.ts:246-273: unknown state refused at :271 (else return fail()); NEEDS_CORRECTION refused unless reason is a non-empty string at :255; findings returned unread at :272",
     "at_dev": "envelope.ts:247-274 (map entry :182): unknown state refused at :272; reason required at :256; findings returned unread at :273"},
    {"file": "src/pages/InvestorReporting/contracts/envelope.ts", "line": "328-335 keys and contract at 334-335; data adapter at 387-388",
     "reads": "the response envelope: allowed keys, contract_version, operation, firm_id, data (the door answer), unprojected_grant (required on every non-refused response)",
     "key_policy": "EXACT (envelope keys, contract_version, operation); data adapter throw becomes EnvelopeMismatch('data')",
     "at_prod": "envelope.ts:328 parseIrEnvelope; allowed keys :333; contract_version :334; operation :335; adapter call :387 (catch -> EnvelopeMismatch('data') at :387); grant check :427",
     "at_dev": "envelope.ts:329 parseIrEnvelope; allowed keys :334; contract_version :335; operation :336; adapter call :388"},
    {"file": "src/api/endpoints/investor-reporting.ts", "line": "1162-1164 (PROD); 1210-1212 (DEV) uploadAnalysisInput",
     "reads": "nothing: sends the upload body and returns the parsed envelope's data (the typed client's upload call)",
     "key_policy": "none (pass-through to parseIrEnvelope, row 2)",
     "at_prod": "investor-reporting.ts:1162-1164 -> send -> parseIrEnvelope (send at :1032, parse at :1055)",
     "at_dev": "investor-reporting.ts:1210-1212 (send and parse not re-read at DEV)"},
    {"file": "src/pages/TicketCenter/analysisRequest.ts", "line": "71-82 (PROD findingLines); 94 (DEV findingParts); UNREADABLE_ROW_LINE at DEV :83",
     "reads": "finding description (words), row, code; the words are shown, a bare code is shown only where no description exists",
     "key_policy": "OPEN (description shown as is)",
     "at_prod": "analysisRequest.ts:75 description shown as is; :79 bare code shown as CODE, row N where no description",
     "at_dev": "analysisRequest.ts:94 findingParts: description shown as is; no-description row -> UNREADABLE_ROW_LINE (:83) with the code moved to details"},
    {"file": "src/pages/TicketCenter/analysisRequest.ts", "line": "92-120 (PROD fileAnalysisRequest); 149-191 (DEV)",
     "reads": "result.state (NEEDS_CORRECTION, RESOLVING, else); result.reason; result.findings via the finding reader; the input_id on NORMALIZED",
     "key_policy": "PROD: reason OPEN (raw reason code shown in the message); DEV: reason TOLERANT-split (a raw code is withheld from the message and put in details)",
     "at_prod": "analysisRequest.ts:99 NEEDS_CORRECTION branch; :102 message uses result.reason verbatim; :106 any other non-NORMALIZED state shown as still checking",
     "at_dev": "analysisRequest.ts:164 NEEDS_CORRECTION branch; :166-170 raw-code reason replaced by 'the file needs a correction.' and kept in details; :174 RESOLVING; :178 other states REFUSED"},
    {"file": "src/pages/TicketCenter/AnalysisRequestParts.tsx", "line": "104-112 (PROD UploadFindings); 150-168 (DEV)",
     "reads": "message and the finding lines (and details at DEV)",
     "key_policy": "OPEN (rendered as text)",
     "at_prod": "AnalysisRequestParts.tsx:104-112 renders message and lines as text",
     "at_dev": "AnalysisRequestParts.tsx:150-168 renders message, lines, and a closed Details list of raw codes (:159-165)"},
    {"file": "src/pages/TicketCenter/TicketCenter.tsx", "line": "119, 176, 325 (PROD); 209, 312, 501 (DEV)",
     "reads": "the file outcome (message, findings, details) handed to UploadFindings",
     "key_policy": "pass-through (OPEN)",
     "at_prod": "TicketCenter.tsx:119 state, :176 setUploadReport from outcome.findings, :325 render",
     "at_dev": "TicketCenter.tsx:209 state, :312 setUploadReport with details, :501 render"},
    {"file": "src/pages/InvestorReporting/tabs/analysis/ProspectComposer.tsx", "line": "447-459 (PROD findings list); 459-471 (DEV)",
     "reads": "result.findings on NEEDS_CORRECTION: description, row, code, reason",
     "key_policy": "OPEN (description shown as is; bare code shown as CODE, row N)",
     "at_prod": "ProspectComposer.tsx:453-456 description shown as is with 'Row N: ' prefix; :456 code shown raw where no description",
     "at_dev": "ProspectComposer.tsx:465-468 the same expression as PROD (raw code shown where no description)"},
    {"file": "src/pages/InvestorReporting/tabs/analysis/ProspectComposer.tsx", "line": "52-57 (uploadStepStateFor, PROD); signature at 52 (DEV)",
     "reads": "result.state",
     "key_policy": "TOLERANT (any state other than NORMALIZED or NEEDS_CORRECTION maps to NOTHING_CHOSEN; not refused)",
     "at_prod": "ProspectComposer.tsx:54-56 NORMALIZED and NEEDS_CORRECTION named; all else falls to :56 NOTHING_CHOSEN",
     "at_dev": "ProspectComposer.tsx:52 signature (body not re-read at DEV)"},
    {"file": "src/pages/InvestorReporting/tabs/analysis/prospect.ts", "line": "24-26 (uploadState); 54-68 (proxyableFindings); codes at 36 and 60",
     "reads": "result.state (uploadState); for proxyableFindings: actions, code, value, suggestion",
     "key_policy": "TOLERANT (proxyableFindings skips codes outside its four proxy codes; not refused). uploadState passes the closed state through",
     "at_prod": "prospect.ts:60 a code outside PROXY_FINDING_CODES is skipped (continue), not refused; :61 value must match TICKER_VALUE",
     "at_dev": "prospect.ts:54-68 unchanged between the tips (no diff)"},
    {"file": "src/pages/InvestorReporting/tabs/analysis/stagedProspect.ts", "line": "165 (sendProspectUpload)",
     "reads": "nothing: sends the body through the client and returns its result",
     "key_policy": "none (pass-through)",
     "at_prod": "stagedProspect.ts:165", "at_dev": "stagedProspect.ts:165 (file unchanged between the tips)"},
    {"file": "src/pages/InvestorReporting/contracts/adapt.ts", "line": "848-916 (adaptAnalysisRequest, PROD); 866-872 findings map; client document map api/endpoints/investor-reporting.ts:1530",
     "reads": "the stored analysis request's findings: finding.code (findingRef, reasonCode), finding.severity, finding.detail (the message)",
     "key_policy": "TOLERANT on severity (unknown value mapped to info, not refused); OPEN on detail (shown as the message)",
     "at_prod": "adapt.ts:866-872: severity BLOCKING->blocking, UNCERTAIN->warning, else info (:868); message = finding.detail (:870); document map investor-reporting.ts:1530",
     "at_dev": "adapt.ts:859 function, findings map 877-882; client document map investor-reporting.ts:1578"},
    {"file": "src/pages/InvestorReporting/tabs/analysis/InputReview.tsx", "line": "25-26, 99-105, 156-158 (PROD and DEV, file unchanged)",
     "reads": "the adapted request findings by lineRef: message, reasonCode, severity",
     "key_policy": "OPEN (message rendered as is)",
     "at_prod": "InputReview.tsx:105 renders finding.message as is", "at_dev": "InputReview.tsx:105 (file unchanged between the tips)"},
    {"file": "src/pages/InvestorReporting/contracts/validate.ts", "line": "376-377 (validateAnalysisRequest)",
     "reads": "the document's findings and corrections: presence and array type only",
     "key_policy": "TOLERANT of finding contents (presence and type only; codes not checked)",
     "at_prod": "validate.ts:376 req(v, path, 'findings', 'array') checks presence and type only", "at_dev": "validate.ts:376 (file unchanged between the tips)"},
    {"file": "src/pages/InvestorReporting/contracts/owned-requests.ts", "line": "58-78 (readOwnedRequest; route map envelope.ts:183)",
     "reads": "identity, accepted_at, comparisons, composition. NO findings are read by this owned-request view",
     "key_policy": "EXACT (top-level keys at :61; identity keys at :68); findings not read",
     "at_prod": "owned-requests.ts:61 exact top-level keys; :68 exact identity keys", "at_dev": "owned-requests.ts:58 readOwnedRequest; :61 exact top-level keys; :68 exact identity keys (file changed at DEV; findings not read at either tip)"},
    {"file": "src/pages/InvestorReporting/contracts/wire/responses.ts", "line": "348 (PROD type); 451 operation list; 477 RESPONSE_STATUS_REQUIRED false (DEV 346, 459, 485)",
     "reads": "declaration of the analysis-input-upload response; no runtime check of findings",
     "key_policy": "TYPE-ONLY (no runtime check; status not required for this operation)",
     "at_prod": "responses.ts:477 analysis-input-upload: false", "at_dev": "responses.ts:485 analysis-input-upload: false"},
    {"file": "src/pages/InvestorReporting/contracts/wire/AnalysisUploadResult.ts", "line": "generated type (file unchanged between the tips)",
     "reads": "the three-state union and the findings member type (compile-time only)",
     "key_policy": "TYPE-ONLY (no runtime check)",
     "at_prod": "AnalysisUploadResult.ts (generated type)", "at_dev": "AnalysisUploadResult.ts (unchanged between the tips)"},
]


def words_from(shown):
    return shown or {}


def person_sees(row):
    rt = row.get("ticket_result") or {}
    if row["reader"].startswith("contracts/envelope.ts"):
        if row["outcome"] == "THREW":
            return "Nothing shown: the parser threw before any view was built (" + (row.get("error") or "") + ")."
        return "The parsed answer is handed on; no words are shown by this reader itself."
    if row["reader"].startswith("TicketCenter"):
        if row["outcome"] == "THREW":
            return "Nothing shown: the ticket path threw before any message was built."
        if rt.get("filed"):
            return "Ticket filed on NORMALIZED. " + ("The SHEETS_NOT_READ notice is not shown: no reader consumes portfolio.findings." if row["codes"] else "No finding words.")
        return "Message shown: " + str(rt.get("message")) + " Findings shown: " + json.dumps(rt.get("findings") or [], ensure_ascii=True)
    if row["reader"].startswith("InvestorReporting"):
        if row["outcome"] == "THREW":
            return "Nothing shown: the proxy reader was not reached (the adapter threw)."
        return "No proxy offered (proxy offers: " + json.dumps(row.get("proxy_offers") or [], ensure_ascii=True) + ")."
    return ""


cases = []
for row in raw:
    sheet = row["case"]
    source = ("START_STATE_SCRATCH_RUN.json door_cases (~52 record), re-run in r19" if sheet in RECORD_SHEETS
              else "CONSTRUCTED in r19: a CSV whose row 3 repeats the header (Ticker,Dollars); no record sheet produces HEADER_ROW_REPEATED")
    cases.append({
        "case": sheet,
        "source": source,
        "arm": row["arm"],
        "commit": row["commit"],
        "commit_sha": row["commit_sha"],
        "reader": row["reader"],
        "outcome": row["outcome"],
        "codes": row["codes"],
        "codes_location": row["codes_location"],
        "answer_state": row["answer_state"],
        "method": "RUN",
        "status_reason": (row.get("error") or None),
        "what_a_person_would_see": person_sees(row),
        "shown_per_code": row.get("shown_per_code") or None,
        "ticket_message": (row.get("ticket_result") or {}).get("message"),
    })

deployed = []
for row in dep:
    deployed.append({
        "case": row["case"],
        "arm": "AFTER",
        "commit": row["commit"],
        "commit_sha": row["commit_sha"],
        "reader": row["reader"],
        "outcome": row["outcome"],
        "codes": row["codes"],
        "method": "RUN",
        "body_source": row["body_source"],
        "body_keys": row["body_keys"],
        "status_reason": (row.get("error") or None),
        "ticket_message": (row.get("ticket_result") or {}).get("message"),
        "ticket_details": (row.get("ticket_result") or {}).get("details"),
        "shown_per_code": row.get("shown_per_code") or None,
    })

new_codes = [
    {"code": "ACCOUNT_COLUMN_SEVERAL_VALUES",
     "words_at_prod": "Row 1: Column C holds more than one account, and one file can hold only one account. Split the sheet into one file per account (one account per file) and upload each file on its own.",
     "words_at_dev": "Row 1: Column C holds more than one account, and one file can hold only one account. Split the sheet into one file per account (one account per file) and upload each file on its own.",
     "shown_by": "ticket path RUN on the deployed stored-row shape (deployed_path_cases); composer render expression READ at PROD 453-456 and DEV 465-468",
     "as_run_create_body": "not shown: every AFTER create body with this code threw at PROD and DEV (cases)"},
    {"code": "HEADER_ROW_REPEATED",
     "words_at_prod": "Row 3: Row 3 repeats the header row. Are the rows below it a second account? If they are, upload them as their own file; if they are the same account, remove the repeated header.",
     "words_at_dev": "Row 3: Row 3 repeats the header row. Are the rows below it a second account? If they are, upload them as their own file; if they are the same account, remove the repeated header.",
     "shown_by": "ticket path RUN on the deployed stored-row shape (constructed sheet header_repeated_csv); composer READ as above",
     "as_run_create_body": "not shown: the AFTER create body threw at PROD and DEV (cases)"},
    {"code": "SHEETS_NOT_READ",
     "words_at_prod": "not shown at PROD: no portal reader consumes portfolio.findings (the notice sits there in the NORMALIZED answer, severity NOTICE)",
     "words_at_dev": "not shown at DEV: no portal reader consumes portfolio.findings (same)",
     "server_words_unshown": "Only the first sheet was read; 1 other sheet(s) in this workbook were not. If another sheet holds holdings you want analyzed, upload it as its own file.",
     "shown_by": "no reader found (grep of non-test src at both tips: zero matches for portfolio.findings / notices)",
     "as_run_create_body": "AFTER NORMALIZED RETURNED at both commits; ticket filed with no notice"},
    {"code": "TOTAL_ROW_PRESENT",
     "words_at_prod": "Row 4: Row 4 is a total, not a holding. Remove the row and upload the file again; the report adds up your holdings itself.",
     "words_at_dev": "Row 4: Row 4 is a total, not a holding. Remove the row and upload the file again; the report adds up your holdings itself.",
     "shown_by": "ticket path RUN on the deployed stored-row shape (deployed_path_cases, total_row_sheet); composer READ as above",
     "as_run_create_body": "not shown: the AFTER create body threw at PROD and DEV (cases)"},
]

record = {
    "prod_commit": PROD_SHA,
    "dev_commit": DEV_SHA,
    "prod_commit_note": "origin/PROD tip read by git ls-remote (refs/heads/PROD 37aa1247ee4ba487e5610dc5b78d65ae28468a99); object present locally",
    "dev_commit_note": "origin/DEV tip read by git ls-remote (refs/heads/DEV 64980b4d3a1e11d8407b6a263ddcd5447dafaef2); object present locally",
    "readers": READERS,
    "readers_count": len(READERS),
    "cases": cases,
    "deployed_path_cases": deployed,
    "new_codes": new_codes,
    "claim": (
        "RUN, not inferred, on bun 1.4.2 against the portal's own functions in two archives (src of PROD 37aa1247 and DEV 64980b4d, "
        "archived under .scratch/r19). Door answers: the ~52 record's offline harness re-run in r19 (start_state_run.py, python 3.12.10) "
        "with the same fixtures, answer bodies dumped as returned by UploadService.create; one constructed sheet (header_repeated_csv) "
        "added because no record sheet produces HEADER_ROW_REPEATED. Readers run: contracts/envelope.ts parseIrEnvelope (which calls "
        "adaptAnalysisUpload), TicketCenter/analysisRequest.ts fileAnalysisRequest (fed through the same parser), prospect.ts proxyableFindings. "
        "RESULT, as the create body returns it: the AFTER arms of the four moved NEEDS_CORRECTION sheets THREW at BOTH PROD and DEV, on key "
        "reason (the create body carries no reason key; the reader requires a non-empty string); the four AFTER NORMALIZED sheets RETURNED at "
        "both commits. The pinned create body of the constructed NEEDS_CORRECTION sheet also THREW at both commits on the same key, so the "
        "gap is in the create-path shape, not introduced by the moved pair alone. DEPLOYED PATH: the upload POST is built by "
        "deferred_upload_service with request_resolution=send (intake/upload_resolution.py:102-113; reports/generate_installed.py:313,391), "
        "so the template lane answers through _defer and then the stored-row _answer, which carries reason (uploads.py:411-415). A body built to "
        "that shape from the moved findings (deployed_path_cases, CONSTRUCTED, not a door run) RETURNED at both commits and the ticket path "
        "shows the server words. Which body the live door serves is NOT measured (no live call). The four new codes are shown as the server's "
        "description with a 'Row N:' prefix at both commits; SHEETS_NOT_READ is shown by no reader. PROD and DEV differ in the ticket message "
        "for a raw reason code (PROD shows TEMPLATE_FINDINGS in the words; DEV shows 'the file needs a correction.')."
    ),
    "not_read": [
        "live PROD and DEV bundles and the served bodies: not read (no live call); only the branch tips were read",
        "the HTTP route (intake/upload_entry.py handle): not run; upload_entry.py names no reason or NEEDS_CORRECTION, so the body reaches the adapter unchanged as far as that file shows",
        "the deferred template path (uploads.py _defer and resolve_deferred, the resident's resolution): not run through the door; only the stored-row _answer shape was constructed from the moved findings",
        "the React render paths (ProspectComposer findings list, AnalysisRequestParts UploadFindings, TicketCenter.tsx, InputReview): READ at the line cited, not rendered (no DOM run)",
        "adaptAnalysisRequest (document 'AnalysisRequest') and validate.ts validateAnalysisRequest: READ only; no AnalysisRequest wire body is produced by the upload door, and callers of validateAnalysisRequest were not traced",
        "the owned-request view (readOwnedRequest): READ; it reads no findings at either tip, so no moved finding can reach it",
        "SHEETS_NOT_READ: no reader consumes portfolio.findings at PROD or DEV (non-test src, zero matches); the server words are unshown",
        "HEADER_ROW_REPEATED: produced by no record sheet; the cases for it use a constructed sheet, labelled in each case's source",
        "scripts/prospect-firm-exercise.mjs (matched the code search at both tips) is a script, not a product reader: not classified",
        "the portal search covered src, lambda, partners and scripts (tests excluded); no reader was found in lambda or partners",
        "the scratch tree (.scratch/r19/ar191) is a copy of the ~52 round's scratch tree from the session scratchpad; it was copied, not run in place",
    ],
}

os.makedirs(OUT_DIR, exist_ok=True)
text = json.dumps(record, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
open(OUT, "w", encoding="ascii", newline="\n").write(text)
print("wrote", OUT, "bytes", len(text), "cases", len(cases), "deployed", len(deployed), "readers", len(READERS))
