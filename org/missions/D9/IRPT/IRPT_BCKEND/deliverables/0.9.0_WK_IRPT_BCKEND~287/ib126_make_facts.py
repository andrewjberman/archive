"""IB126: writes ib126_route_facts.json (the static facts ib126_compare.py reads: where each answer and envelope is built,
which existing test was run, with what command). Run from the repo root. No value from any answer appears here."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~287"
IR = "infra/aws/lambda/investor-reporting"
ENV_SITE = IR + "/_authz/served.py:403"


def inv(sub, wrap, op, out, node, match=None, probe=False):
    m = (" IB126_MATCH='%s'" % match) if match else ""
    target = "$D/ib126_custody_read_probe.py" if probe else node
    pp = "$D:$PWD" if probe else "$D"
    return ("cd %s/%s && IB126_WRAP=%s IB126_OP=%s%s IB126_OUT=<repo>/.scratch/answers/%s PYTHONPATH=%s "
            "python -m pytest -q -p no:cacheprovider -p ib126_capture_plugin %s   (D=<repo>/%s)"
            % (IR, sub, wrap, op, m, out, pp, target, D))


facts = {
    "_method": (
        "For each route, an EXISTING handler test (or, for custody-report-read only, a probe that reuses the fixtures of an "
        "existing test) was run unaltered under ib126_capture_plugin.py, which wraps one callable and records the envelope the "
        "handler's boundary returned (synthetic test-fake values, kept in .scratch/, never copied). ib126_compare.py then "
        "validated the WHOLE envelope against the route's v1 response schema with test_seam_paired.py's own validator "
        "(_response_validator, imported) and compared the member names and JSON types of its `data` with the producer "
        "fixture's `instance`. A member present on one side only is optional_by_schema when the whole envelope still validates "
        "with it removed (tested, not assumed). Children of an empty object or array on either side cannot be compared and are "
        "listed as unobserved. Values are never compared or written. The recorded answers come from the tests' in-memory fakes: "
        "they show the SHAPE the handler's code emits for that fake world, not a byte read off the live function."),
    "routes": {
        "directory-browse": {
            "operation": "directory-browse", "route_key": "GET /api/scoped/investor-reporting/directory/browse",
            "function": "irpt-directory-search",
            "answer_built_at": IR + "/directory/entry.py:378",
            "envelope_built_at": IR + "/_authz/served.py:1321 (guarded Entry.handle) calling response_envelope defined at " + ENV_SITE,
            "evidence": "existing_test_run",
            "invocation": inv("directory/tests", "entry.ENTRY.handle", "directory-browse", "directory-browse.json",
                              "test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable",
                              "data.next_cursor=null"),
            "tests_run_unaltered": ["directory/tests/test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable "
                                    "(validates each page against responses/directory-browse.response.schema.json itself)"],
            "fixture": "DirectoryPage.valid.json", "answer_file": "directory-browse.json"},
        "analysis-request-history": {
            "operation": "analysis-request-history", "route_key": "GET /api/scoped/investor-reporting/analysis/requests",
            "function": "irpt-status",
            "answer_built_at": IR + "/ops/owned_requests.py:393",
            "envelope_built_at": IR + "/_authz/served.py:982 (Entry._handle_owner_read, mode CURRENT_OWNER_HISTORY) calling response_envelope defined at " + ENV_SITE,
            "evidence": "existing_test_run",
            "invocation": inv("ops/tests", "call", "analysis-request-history", "analysis-request-history.json",
                              "'test_owned_entry.py::test_actual_entry_current_owner_serves_typed_data_without_custody_input[history]'"),
            "tests_run_unaltered": ["ops/tests/test_owned_entry.py::test_actual_entry_current_owner_serves_typed_data_without_custody_input[history] "
                                    "(does not itself validate against the response schema; ops/tests/test_history_row_client.py validates the data "
                                    "payload against OwnedAnalysisRequestHistory.schema.json)"],
            "fixture": "OwnedAnalysisRequestHistory.valid.json", "answer_file": "analysis-request-history.json"},
        "analysis-input-upload": {
            "operation": "analysis-input-upload", "route_key": "POST /api/scoped/investor-reporting/analysis/inputs",
            "function": "irpt-ycharts-generate",
            "answer_built_at": IR + "/intake/uploads.py:504 (NORMALIZED answer; the RESOLVING answer is built at " + IR + "/intake/uploads.py:393)",
            "envelope_built_at": IR + "/_authz/served.py:1040 (Entry._handle_prospect, mode CREATE_INPUT) calling response_envelope defined at " + ENV_SITE,
            "evidence": "existing_test_run",
            "invocation": inv("intake/tests", "sys:served.Entry.handle", "analysis-input-upload",
                              "analysis-input-upload.normalized.json",
                              "test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input",
                              'data.state="NORMALIZED"'),
            "tests_run_unaltered": [
                "intake/tests/test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input "
                "(Entry from intake/upload_entry.py build_upload_entry: the same served.Entry, UploadService and CREATE_INPUT prospect mode "
                "the function's boundary uses, but NOT generate_installed.build_boundary; NORMALIZED answer)",
                "reports/tests/test_generate_installed.py::test_the_upload_route_publishes_resolving_and_sends_one_message "
                "(the function's own boundary, generate_installed.build_boundary; RESOLVING answer)"],
            "fixture": "AnalysisUploadResult.valid.json", "answer_file": "analysis-input-upload.normalized.json",
            "also": [{
                "label": "RESOLVING answer through the function's own boundary (generate_installed.build_boundary)",
                "answer_file": "analysis-input-upload.json", "answer_built_at": IR + "/intake/uploads.py:393",
                "invocation": inv("reports/tests", "sys:served.Entry.handle", "analysis-input-upload",
                                  "analysis-input-upload.json",
                                  "test_generate_installed.py::test_the_upload_route_publishes_resolving_and_sends_one_message")}]},
        "custody-report-read": {
            "operation": "custody-report-read", "route_key": "GET /api/scoped/investor-reporting/custody-report/{reportId}",
            "function": "irpt-export-render",
            "answer_built_at": IR + "/export/custody_read.py:78",
            "envelope_built_at": IR + "/_authz/served.py:1321 (guarded Entry.handle) calling response_envelope defined at " + ENV_SITE,
            "evidence": "in_process_call",
            "invocation": inv("export/tests", "entry.lambda_handler", "custody-report-read", "custody-report-read.json", "", None, True),
            "tests_run_unaltered": ["export/tests/test_custody_read.py (calls the compute function and sees the data payload only, so no existing test "
                                    "holds the whole envelope of this route; ib126_custody_read_probe.py reuses the fixtures of "
                                    "export/tests/test_custody_writer_composed.py and asks the real entry.lambda_handler for the report it just persisted)"],
            "fixture": "custody-report-read.response.valid.json", "answer_file": "custody-report-read.json"},
        "custody-report-persist": {
            "operation": "custody-report-persist", "route_key": "POST /api/scoped/investor-reporting/custody-report",
            "function": "irpt-export-render",
            "answer_built_at": IR + "/export/custody_persist.py:177",
            "envelope_built_at": IR + "/_authz/served.py:1321 (guarded Entry.handle) calling response_envelope defined at " + ENV_SITE,
            "evidence": "existing_test_run",
            "invocation": inv("export/tests", "entry.lambda_handler", "custody-report-persist", "custody-report-persist.json",
                              "test_custody_writer_composed.py::test_guarded_or_scheduled_a_verified_opal_caller_persists_through_the_entry"),
            "tests_run_unaltered": ["export/tests/test_custody_writer_composed.py::test_guarded_or_scheduled_a_verified_opal_caller_persists_through_the_entry"],
            "fixture": "custody-report-persist.response.valid.json", "answer_file": "custody-report-persist.json"},
    },
    "control": {
        "operation": "comparison-catalogue", "route_key": "GET /api/scoped/investor-reporting/analysis/comparisons",
        "function": "irpt-ycharts-generate",
        "answer_built_at": IR + "/ycharts/generate/comparison_catalogue.py:200",
        "envelope_built_at": IR + "/_authz/served.py:1321 (guarded Entry.handle) calling response_envelope defined at " + ENV_SITE,
        "evidence": "existing_test_run",
        "invocation": inv("ycharts/generate/tests", "sys:served.Entry.handle", "comparison-catalogue", "comparison-catalogue.json",
                          "test_comparison_catalogue.py::test_the_read_rides_the_entrys_guard_and_tenant_check"),
        "fixture": "ComparisonCatalogue.valid.json", "answer_file": "comparison-catalogue.json"},
}

with open(os.path.join(HERE, "ib126_route_facts.json"), "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=1)
    fh.write("\n")
print("OK: ib126_route_facts.json written")
