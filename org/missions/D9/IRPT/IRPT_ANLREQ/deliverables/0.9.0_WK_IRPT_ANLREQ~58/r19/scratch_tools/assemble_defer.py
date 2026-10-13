"""r19 AR-y-203: assemble PORTAL_DEFER_SHAPE_READERS.json from the raw bun output and the builder output. Reads only the
scratch files; writes the record into the worker's deliverables folder. ASCII only."""
import json
import sys
from pathlib import Path

S = Path(sys.argv[1])
OUT = Path(sys.argv[2])
raw = json.loads((S / "readers_defer_raw.json").read_text(encoding="utf-8"))
built = json.loads((S / "bodies_AFTER.json").read_text(encoding="utf-8")) + json.loads((S / "bodies_BEFORE.json").read_text(encoding="utf-8"))
built_by = {(b["arm"], b["case"]): b for b in built}

cases = []
for r in raw:
    c = {k: r.get(k) for k in ("case", "arm", "commit", "commit_sha", "reader", "outcome", "error", "codes", "codes_location",
                               "reason", "state", "findings_total", "body_keys", "body_source", "method", "reader_version")}
    c["case"] = r["case"]
    c["codes"] = r["codes"]
    c["reader_version"] = r.get("reader_version")
    if r["reader"].startswith("contracts/envelope"):
        c["adapted_state"] = r.get("adapted_state")
        c["what_a_person_would_see"] = "No words: the parser hands the answer on (adapted state %s)." % r.get("adapted_state")
    elif r["reader"].startswith("TicketCenter"):
        tr = r.get("ticket_result") or {}
        c["ticket_message"] = tr.get("message")
        c["ticket_details"] = tr.get("details")
        c["ticket_filed"] = tr.get("filed")
        c["shown_per_code"] = r.get("shown_per_code")
        lines = tr.get("findings") or []
        c["ticket_lines"] = lines
        c["what_a_person_would_see"] = "Ticket message: %s. Lines: %s" % (tr.get("message"), " | ".join(lines))
    else:
        c["proxy_offers"] = r.get("proxy_offers")
        c["what_a_person_would_see"] = "No words: proxy offers %s." % json.dumps(r.get("proxy_offers"))
    cases.append(c)

new_codes = []
ticket = [c for c in cases if c["reader"].startswith("TicketCenter")]
words = {}
for c in ticket:
    for code, line in (c.get("shown_per_code") or {}).items():
        words.setdefault((c["arm"], code), {})[c["commit"]] = {"line": line, "case": c["case"]}
for (arm, code), by in sorted(words.items()):
    new_codes.append({"code": code, "arm": arm, "words_at_prod": by.get("PROD", {}).get("line"),
                      "words_at_dev": by.get("DEV", {}).get("line"),
                      "shown_by": "TicketCenter/analysisRequest.ts fileAnalysisRequest over the _defer body (%s); run, not read" % ", ".join(sorted({v["case"] for v in by.values()}))})

rec = {
    "record": "PORTAL_DEFER_SHAPE_READERS",
    "to_id": "IRPT_ANLREQ.TO-AR-y-203",
    "cell": "AR-y-203",
    "prod_commit": "37aa1247ee4ba487e5610dc5b78d65ae28468a99",
    "dev_commit": "64980b4d3a1e11d8407b6a263ddcd5447dafaef2",
    "commit_provenance": "PROD and DEV source archives in the worker scratch (portal_prod, portal_dev) were compared with git archive of each commit's src tree from the base portal repository (C:/dev/ajb_workspace/portal): diff -rq printed no lines at either commit (verify_PROD.diff, verify_DEV.diff, both empty). No fetch, checkout, push or deploy.",
    "builder": "build_defer_bodies.py (worker scratch r19): imports read_template from template_reader.py, _with_correction_words, MAX_STORED_FINDINGS and NEEDS_CORRECTION from the intake folder given on the command line; the body literal is the one uploads.py _defer returns (moved 069b8f797e lines 459-475).",
    "arms": {
        "AFTER": "moved pair: uploads.py and template_reader.py at 069b8f797e (template_reader READER_VERSION irpt-template-reader.r18.1)",
        "BEFORE": "pinned pair: uploads.py at f09b802cdc and template_reader.py at 3f29017cfc (no READER_VERSION); constructed body, see claim",
    },
    "cases": cases,
    "case_count": len(cases),
    "new_codes": new_codes,
    "built_bodies": [{"arm": b["arm"], "case": b["case"], "has_error": b["has_error"], "error_codes": b["error_codes"],
                      "all_finding_codes": b["all_finding_codes"], "reason": b.get("reason"), "findings_total": b.get("findings_total"),
                      "body_keys": b.get("body_keys"), "codes": b.get("codes"),
                      "findings_equal_to_prior_door_answer": b.get("findings_equal_to_prior_door_answer")} for b in built],
    "claim": (
        "RUN, not inferred. The deployed first answer of the template lane (the _defer body of uploads.py at 069b8f797e, "
        "lines 459-475) was built by calling the moved intake folder's own read_template, _with_correction_words, "
        "MAX_STORED_FINDINGS and NEEDS_CORRECTION, for the five sheets whose template carries an ERROR finding under the moved "
        "reader: total_row_sheet (TOTAL_ROW_PRESENT), two_value_account_sheet, repair_header_two_values, brokerage_two_account "
        "(ACCOUNT_COLUMN_SEVERAL_VALUES) and header_repeated_csv (HEADER_ROW_REPEATED and AMOUNT_NOT_A_NUMBER). Each body carries "
        "upload_id, input_id null, state NEEDS_CORRECTION, reason TEMPLATE_FINDINGS, findings, findings_total and template. "
        "The bodies were passed through the portal's own functions at PROD 37aa1247 and DEV 64980b4d with bun 1.4.2: "
        "contracts/envelope.ts parseIrEnvelope (analysis-input-upload), TicketCenter/analysisRequest.ts fileAnalysisRequest "
        "(fed through the same parser) and InvestorReporting/tabs/analysis/prospect.ts proxyableFindings. RESULT: 30 of 30 AFTER "
        "reader rows RETURNED at both commits (5 sheets x 2 commits x 3 readers); 0 AFTER rows THREW. The envelope reader returns "
        "state NEEDS_CORRECTION for every body (the reason key is present, so the NEEDS_CORRECTION guard passes). The ticket path "
        "files nothing and shows one line per finding. The proxy reader offers nothing (no proxy code). "
        "BEFORE arm: under the pinned pair, read_template finds an ERROR only for header_repeated_csv (AMOUNT_NOT_A_NUMBER); the "
        "other four sheets carry no ERROR under the pinned reader and are not first-answer cases. The pinned uploads.py _defer "
        "(f09b802cdc lines 370-386) has NO ERROR branch: it reads the template, publishes RESOLVING and dispatches; it does not "
        "return a NEEDS_CORRECTION body. The BEFORE body for header_repeated_csv is therefore CONSTRUCTED from the moved literal "
        "with the pinned uploads.py _with_correction_words and pinned constants, not the pinned door's own answer. 6 of 6 BEFORE "
        "reader rows RETURNED. "
        "COMPARISON: the synchronous create answer of the prior cell (its header_repeated_csv|moved door body) carried 3 findings; "
        "the _defer body carries 2 (HEADER_ROW_REPEATED and one AMOUNT_NOT_A_NUMBER). The synchronous path returns "
        "freeze_template_portfolio findings (moved uploads.py line 592); _defer does not call it. The other four sheets' findings "
        "are equal to the prior door answer's findings."
    ),
    "not_read": [
        "the HTTP route (intake/upload_entry.py handle): not run; the body was built by calling the functions, not through the door",
        "the resident's resolution (resolve_deferred and the resolution message round trip): not run; the _defer first answer is the body that returns before any resident work",
        "the deployed PROD and DEV bundles and the served bodies: not read (no live call); only the two portal commits' src trees were read, through git archive",
        "the React render paths (ProspectComposer, AnalysisRequestParts, TicketCenter.tsx, InputReview): read at the line cited in the prior cell, not rendered; the words in this record are what the ticket function returns",
        "the pinned pair's live wiring: whether the live Lambda builds its UploadService with request_resolution was not read; the BEFORE arm is a constructed body (claim)",
        "the prior cell's header_repeated_csv create body (3 findings) is not re-run here; the deferred body (2 findings) is the one this record carries",
        "scripts/prospect-firm-exercise.mjs and the other readers named in the prior cell's record: not repeated here; the three readers of this cell are the ones the order names",
        "the header_repeated_csv sheet is constructed (same literal as the r19 dump harness, line 93); the other four sheets are the round-18 harness INPUTS, extracted by AST and not retyped",
        "the upload_id values are the prior door run's values for the same sheet bytes (run_hr/answer_bodies.json), not re-derived",
    ],
}
OUT.write_text(json.dumps(rec, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
print("cases", len(cases), "AFTER", sum(1 for c in cases if c["arm"] == "AFTER"), "BEFORE", sum(1 for c in cases if c["arm"] == "BEFORE"),
      "outcomes", {o: sum(1 for c in cases if c["outcome"] == o) for o in ("RETURNED", "THREW")}, "new_codes", len(new_codes))
