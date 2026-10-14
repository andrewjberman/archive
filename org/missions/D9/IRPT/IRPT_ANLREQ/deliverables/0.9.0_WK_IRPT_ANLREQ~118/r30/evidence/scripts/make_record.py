"""Scratch generator of r30/RESIDENT_BUILD.json for AR-y-300 (outside the product tree). ASCII only.

Every digest is computed from the file on disk here, never typed. Writes one JSON document to argv[1].
usage: python -I make_record.py <out json>
"""
import hashlib
import json
import sys

R = "C:/dev/irpt-release-r28"
DELIV = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~118")
WT = "C:/dev/wk-irpt-anlreq-118/" + DELIV
TAR = R + "/irpt-resident-0485393f3a-r28.tar.gz"
BASE = "C:/dev/irpt-release-r19/irpt-resident-0485393f3a-r19.tar.gz"
HOST = WT + "/r30/resident_host_install_0485393f3a-r28.sh"
BUILDER = "C:/dev/irpt-r28-build/org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/build_resident_package.py"


def sha(path):
    with open(path, "rb") as fh:
        data = fh.read()
    return hashlib.sha256(data).hexdigest(), len(data)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


delta = load(R + "/out/pack_delta_r28.json")
dl = delta["delta"]
tar_sha, tar_bytes = sha(TAR)
base_sha, _ = sha(BASE)
host_sha, host_bytes = sha(HOST)
builder_sha, _ = sha(BUILDER)
pack = load(R + "/out/build_a2_stdout.json")
packb = load(R + "/out/build_b2_stdout.json")
cell_map = {
    "intake/template_reader.py": ("r19.3 reader (AR-y-245/r19.3 fold; AR-y-293 KEPT words)", "r19.3"),
    "intake/portfolio.py": ("AR-y-245 default price date; AR-y-293 KEPT", ""),
    "intake/uploads.py": ("AR-y-245 default price date; AR-y-293 KEPT (r19 base was 176682cb)", ""),
    "intake/security_resolution.py": ("AR-y-291 registry identity port; AR-y-293 KEPT", ""),
    "ops/status.py": ("AR-y-293 CORRECTION_WORDS +3 (words only)", ""),
    "ycharts/generate/resident_worker.py": ("AR-y-291 registry identity port (AR-y-291)", ""),
    "ycharts/research/opal_packager.py": ("AR-y-285 request_id; the r19 base already carries an older blob, so REPLACE not ADD", ""),
}
differing = []
for item in dl["differing"]:
    name = item["member"]
    if name == "SHA256SUMS":
        continue
    if name == "reports/resident_bindings.json":
        continue
    differing.append({"member": name, "old_sha256": item["old_sha256"], "new_sha256": item["new_sha256"],
                      "reason": cell_map.get(name, ("", ""))[0]})
delta_names = [item["member"] for item in dl["differing"]]
doc = {
    "record_id": "IRPT_ANLREQ.TO-AR-y-300.RESIDENT_BUILD",
    "cell": "AR-y-300",
    "issued_to": "0.9.0_WK_IRPT_ANLREQ~118",
    "workstream": "YU",
    "round": 30,
    "scope_statement": "BUILD ONLY. Nothing uploaded, installed, applied, invoked, deployed, pushed or fetched. No AWS call: the builder ran on --state-json. Scratch trees and the staged tarball are outside the product tree.",
    "build_guard": {"file": "infra/aws/lambda/ci/build-and-upload.sh", "BUILD_ONLY_count_at_pin_0485393f3a": 8,
                    "BUILD_ONLY_count_at_trunk_a4b7c48fad": 8, "note": "the resident is built by the python builder, which writes local files only; the CI script is not run"},
    "scratch_commit": {"made": False, "hash": None,
                       "reason": "safe-commit.sh refused the scratch commit in the throwaway worktree C:/dev/irpt-r28-build: owned-paths lane violations on all 8 paths (surprise row IRPT_ANLREQ-D2-W118-S1)",
                       "substitute": "builder-native --pin <trunk> --base-pin 0485393f3a --files-from <list> --member lib/trading_calendar.py=lib/trading_calendar.py"},
    "pin_source": {"package_pin": "a4b7c48fad0559ff06155e505b51e97b3c5f6437",
                   "package_pin_is": "origin/CLOUD as read at this run (no fetch); 0d83fda956 (the census trunk) is an ancestor",
                   "base_pin": "0485393f3ad0a7e564f4867f5e70003e2e62195b",
                   "files_from": "7 repo paths read from the package pin (trunk) instead of the base pin; sha256 of the list " + pack["files_from_sha256"]},
    "base_tarball": {"path": BASE, "sha256": base_sha,
                     "checked": "sha256sum read 2026-10-13; equals the order's 84df6479...; extracted for the delta to C:/dev/irpt-release-r28/pkg2 and pkg3 (scratch)"},
    "release_input": {
        "members": differing + [{"member": "lib/trading_calendar.py", "old_sha256": None,
                                 "new_sha256": delta["delta"]["only_in_new"][0]["new_sha256"] if False else None,
                                 "reason": "ADD: the r19 base does not carry it; the trunk blob is packaged flat-named lib/trading_calendar.py so that portfolio.py route 1 resolves through the resident's lib path"}],
        "builder": {"path": BUILDER.replace("C:/dev/irpt-r28-build/", ""),
                    "scratch_location": BUILDER,
                    "blob": "e1e58c2d94a8d0b6fc4c16320fa385bf39e5d8a8", "commit": "aaa458aa4f",
                    "sha256": builder_sha,
                    "diff": "none: the recipe builder was run UNEDITED; --research packages the research files at the base pin and --member packages the calendar, so no builder edit was needed",
                    "diff_path": DELIV + "/r30/evidence/builder_diff.txt",
                    "diff_sha256": sha(WT + "/r30/evidence/builder_diff.txt")[0],
                    "note": "the pin builder reports/build_resident_package.py (blob c8158cfc, 4723 bytes) is not the recipe builder and was not used"},
        "import_closure": {
            "opal_packager.py": "imports opal_producer (research dir: packaged), keys (_keys: packaged), reports/repository (packaged), durable_job (ycharts/generate: packaged; resolved only on the sys.path that resident_installed.py builds, not on resident_main.py's list); opal_producer imports held_data, keeper, layout_overview, runner (research: packaged); durable_job imports submission (ycharts/generate: packaged). Satisfied; nothing missing.",
            "trading_calendar.py": "imports pandas_market_calendars inside try/except ImportError (fallback _USE_PMC False). Not packaged by design of the module; the optional import degrades, it is not a missing name.",
            "intake/portfolio.py": "imports trading_calendar (route 1, resolves to lib/trading_calendar.py via the lib path), lib (route 2, the lib directory), custody_portfolio, security_resolution, template_reader: all packaged.",
            "reader_import_check": "r19 evidence import_check.py over the extracted package: 53 from/import names checked, 0 problems, IMPORT-CHECK-OK",
            "source": DELIV + "/r30/evidence/import_closure.json"},
    },
    "artifact": {"path": TAR, "sha256": tar_sha, "bytes": tar_bytes,
                 "member_count": pack["members"] + 1, "member_count_excluding_SHA256SUMS": pack["members"],
                 "sha256sums_check": "extracted to C:/dev/irpt-release-r28/pkg3: 298 entries, 0 mismatch, 0 unlisted (verify_pkg.py)",
                 "determinism_control": {"method": "two builds, the build clock held to 2026-10-11T15:29:02Z (run_builder_fixed_clock.py): build_a2 and build_b2",
                                         "package_manifest_sha256": pack["package_manifest_sha256"],
                                         "same_manifest": pack["package_manifest_sha256"] == packb["package_manifest_sha256"],
                                         "files_identical_by_name_and_sha256": "%d of %d" % (299, 299),
                                         "shipped_file": "the single packing of build_a2 (pack_one.py asserts the shipped tar carries exactly the build bytes)"}},
    "delta_vs_live": delta_names,
    "delta_vs_live_detail": "the differing member names against the release-19 tarball (the same list as delta.differing in out/pack_delta_r28.json)",
    "only_in_live": [],
    "only_in_old": [],
    "only_in_release": ["lib/trading_calendar.py"],
    "only_in_new": ["lib/trading_calendar.py"],
    "removed_members_count": 0,
    "unchanged_count": dl["unchanged_count"],
    "root_naming": {"NEW": "0485393f3a-r28", "OLD": "0485393f3a-r19",
                    "what_the_bindings_carry": "no root name and no root path. Changed inside reports/resident_bindings.json: provenance.package_pin 0485393f3a -> a4b7c48fad; provenance.member_overrides {template_reader, uploads at 069b8f79} -> {}; provenance.base_pin 0485393f3a and files_from_count 7 and files_from_sha256 ba5bd2c2 added; provenance.members_added gains lib/trading_calendar.py (the three etf/svg/calendar entries). Unchanged: generated_at 2026-10-11T15:29:02Z, census_pin, core_state_serial 5 (reconstructed, not live), queue, tables, capture hashes, opal_map.",
                    "HOST_ROOT": "/opt/irpt-resident/0485393f3a-r28"},
    "host_script": {"path": HOST, "sha256": host_sha, "bytes": host_bytes,
                    "lines_changed": "9 lines removed and 17 added across 5 hunks against the release-19 script: header comment (4 lines to 5), NEW, OLD, WANT_TAR, the resident_worker.py member check (value), seven added member checks (template_reader, portfolio, uploads, security_resolution, ops/status, opal_packager, lib/trading_calendar), and the ledger string in the cutover block",
                    "member_checks_equal_tarball": True,
                    "member_checks": "24 of 24 equal the extracted tarball bytes (host_checks.py); 17 original (16 members and the library) plus 7 added",
                    "diff_path": DELIV + "/r30/evidence/host_script_diff_r19_to_r28.txt",
                    "not_run": "the script was not run; the S3 key was not uploaded"},
    "rollback": {"running_root": "/opt/irpt-resident/0485393f3a-r19 (RECORD, not read live)",
                 "base_tarball_sha256": base_sha,
                 "note": "the rollback install of the running root is the host script's own install_root $OLD path"},
    "tests": {
        "named_files": 12,
        "named_tests_file": DELIV + "/r30/evidence/named_files.txt",
        "passed": 176, "failed": 2, "skipped": 0,
        "denominator": "178 collected across 11 of the 12 named files; intake/tests/test_kept_holding.py is not collected (ImportError: yfinance_check absent by design)",
        "run_against": "the EXTRACTED package at C:/dev/irpt-release-r28/pkgtest/infra/aws/lambda/investor-reporting (repo-depth layout, see harness additions), PYTHONPATH on the package root and the five trunk test folders, GIT_DIR=C:/dev/ajb_workspace/.git (graded run)",
        "graded_output": DELIV + "/r30/evidence/tests_graded_GIT_DIR_set.txt",
        "control_GIT_DIR_unset": {"passed": 173, "failed": 5, "output": DELIV + "/r30/evidence/tests_control_GIT_DIR_unset.txt",
                                  "failed_tests": ["3 stored-input tests: git show rc 128 (the same S2 condition as release 21)", "test_the_readers_output_on_the_fixtures_is_pinned_to_its_version (the S26 baseline)", "test_the_default_is_the_estates_one_calendar_and_its_prior_day (see below)"]},
        "harness_additions_outside_the_package": [
            "the five test folders (intake/tests, reports/tests, ycharts/session/tests, ycharts/generate/tests, ycharts/research/tests) copied from trunk commit a4b7c48fad with git archive (the same commit the members come from; the worktree HEAD blobs of the named test files were compared and equal)",
            "the package at repo depth under C:/dev/irpt-release-r28/pkgtest/infra/aws/lambda/investor-reporting, with a copy of its docs/ at C:/dev/irpt-release-r28/pkgtest/docs (the reports test computes its root with parents[5]/docs)",
            "a copy of lib/trading_calendar.py at C:/dev/irpt-release-r28/pkgtest/lib (a diagnostic only; it did not change the loaded path)"],
        "failures_explained": [
            "intake/tests/test_stored_input_contract.py::test_the_readers_output_on_the_fixtures_is_pinned_to_its_version -- FAILED: digest 12856189f4a3... against the pin 858b1282115b... for READER_PINS r19.3. The same digest as release 21 (its named S26 baseline). Cause: the reader's fixture set is the nine csv/xlsx files under intake/fixtures/holdings, and the builder packages only .py, .json, .sh and .md; the package's intake/fixtures/holdings holds FIXTURE_MANIFEST.json, generate_rt11_specimens.py and security_mapping.json only. Known baseline S26 (IRPT_ANLREQ-D2-W55-S26); not a new defect.",
            "intake/tests/test_price_date_default.py::PriceDateDefaultTests::test_the_default_is_the_estates_one_calendar_and_its_prior_day -- FAILED at line 124: the loaded calendar path (<package>/lib/trading_calendar.py) is compared with <repo root>/lib/trading_calendar.py. The two date assertions before line 124 pass. The bytes are the packaged member (sha256 9bc467c6..., verified in SHA256SUMS). No release-19 or release-21 baseline (not in their named sets). The test presumes a source checkout; the diagnostic run (diag_price_date_with_calendar_at_repo_lib.txt) still fails. New row IRPT_ANLREQ-D2-W118-S4.",
            "intake/tests/test_kept_holding.py -- NOT COLLECTED: ModuleNotFoundError yfinance_check (line 15). The module is not in this release by design (census S6; W113-S6). Diagnostic only: with the trunk module copied into the scratch package, 19 of 19 pass (diag_kept_holding_with_yfinance_check.txt). New row IRPT_ANLREQ-D2-W118-S5.",
            "release-21 S25 (correction words against the packaged status.py) is NOT failing here: ops/status.py now carries the trunk blob, and test_correction_words passes."],
    },
    "claim": "The release is the release-19 tarball with the seven cell members at their trunk HEAD blobs (six replaced, opal_packager.py replaced rather than added), lib/trading_calendar.py added, and the bindings and SHA256SUMS regenerated; nothing removed. The delta against the r19 tarball is 9 differing members (SHA256SUMS, reports/resident_bindings.json, intake/template_reader.py, intake/portfolio.py, intake/uploads.py, intake/security_resolution.py, ops/status.py, ycharts/generate/resident_worker.py, ycharts/research/opal_packager.py) and 1 only_in_new (lib/trading_calendar.py), 0 removed, 289 unchanged. The two-build determinism control is 299 of 299. On the extracted package the named tests give 176 passed and 2 failed (one known baseline, one new path-layout assertion), with test_kept_holding.py not collected. The host script carries 24 member checks, all equal to the tarball. Nothing was uploaded, installed, applied, invoked or deployed. The checker's expected lists treat opal_packager.py as an ADD: the instrument will FAIL on that (see surprise row IRPT_ANLREQ-D2-W118-S2).",
    "not_read": [
        "the live resident host (no SSH, SSM or sudo); the live root 0485393f3a-r19 and its cutover receipt",
        "the live core state document: the bindings' queue, tables and serial are the reconstructed st32 values (state_st32_from_bindings.json, which states it is circular)",
        "the live package bytes of irpt-resident (no S3 read in this order)",
        "the running resident's sys.path beyond the two installer lists read from the package source",
        "the trunk test suites beyond the named files; the 'tests' folders of the release-19 tarball (none carried)",
        "the portal, DEV and PROD bundles",
        "the r19 release's install state and the release-19 operator log"
    ],
    "surprise_rows": ["IRPT_ANLREQ-D2-W118-S1", "IRPT_ANLREQ-D2-W118-S2", "IRPT_ANLREQ-D2-W118-S3", "IRPT_ANLREQ-D2-W118-S4", "IRPT_ANLREQ-D2-W118-S5"],
}
# the one member the add-list names: its new sha256 from the tarball's own only_in_new entry
doc["release_input"]["members"][-1]["new_sha256"] = sha(R + "/build_a2/lib/trading_calendar.py")[0]
out = sys.argv[1]
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(doc, indent=1, sort_keys=False) + "\n")
print("wrote", out, "artifact sha", tar_sha, "host sha", host_sha, "builder sha", builder_sha)
