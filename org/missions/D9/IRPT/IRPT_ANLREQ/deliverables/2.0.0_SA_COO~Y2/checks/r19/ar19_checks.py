"""ar19_checks.py -- the mechanical checks of IRPT_ANLREQ round 19, workstream Y.

Usage:  python ar19_checks.py <check> --root <worker worktree root>

  y191-scratch   AR-y-191: the start-state scratch-tree record covers the Lambda's door and re-open on the pinned pair, with the pins named and
                 each case carrying an outcome and its evidence                                                              -> Y191-SCRATCH-OK
  y192-census    AR-y-192: the release census names the map members, the four native unpinned members, the planned pin moves and the resident's
                 pin rule                                                                                                   -> Y192-CENSUS-OK
  y193-build     AR-y-193: the release build record names the package hash, a member manifest, and a planned-vs-actual member diff that agree  -> Y193-BUILD-OK
  y194-rule      AR-y-194: the widened rule and the value backstop over the stored population (every listed form matched, the count form
                 excluded only when its values are counts, every negative control unmatched)                                -> Y194-RULE-OK
  y194-backstop  AR-y-194: the named backstop tests exist and pass                                                            -> Y194-BACKSTOP-OK
  y194-keep      AR-y-194: the whole intake folder passes (floor 331) and READER_VERSION differs from r18.1                    -> Y194-KEEP-OK
  y195-delta     AR-y-195 (workstream YR): the resident package delta between the live resident's pin and the release pin names every differing
                 member with both hashes, the two reader members, and the other members grouped by owner                      -> Y195-DELTA-OK
  y196-install   AR-y-196: the install semantics (OVERLAY, REPLACE or NEW_ROOT_COPY) read from the installer with a scratch proof and denominators -> Y196-INSTALL-OK
  y197-four      AR-y-197: the four members the issuer reads (served.py, name_rulings.json, ops/status.py, resident_worker.py) each with old/new blob,
                 the resident's use of it, and the change in behaviour                                                       -> Y197-FOUR-OK
  y198-equal     AR-y-198: the five cross-box members each compared to the owner-released version                              -> Y198-EQUAL-OK
  y200-two       AR-y-200: the st32 build with ONLY the reader members (and what must move with them) swapped: the delta against the st32 rebuild is
                 exactly the allowed set, and the reader's named tests pass on that build                                  -> Y200-TWO-OK
  y201-live      AR-y-201 (workstream YR): the Lambda release rebuilt against the LIVE package read now: the four native holds re-pinned to commits
                 whose blobs equal the live members, and the release package differs from the live package in exactly the two reader members
                                                                                                                              -> Y201-LIVE-OK
  y202-portal    AR-y-202 (workstream YR): the portal's readers of the upload door's answer at the PROD and DEV commits, each with its key policy, and
                 the door answers of the pinned and the moved pair passed through them, the four new finding codes among the cases    -> Y202-PORTAL-OK
  y203-defer     AR-y-203 (workstream YR): the portal's readers given the DEPLOYED first answer of the template lane (the _defer body, reason
                 TEMPLATE_FINDINGS) built from the moved uploads.py, at PROD and DEV, for the three ERROR finding codes     -> Y203-DEFER-OK
  y199-recipe    AR-y-199: st32's full assembly recipe recovered, rebuilt at st32's pin (326 members by name and content) before the
                 release pin is built with it, and the delta redone                                                           -> Y199-RECIPE-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
INTAKE = IR + "/intake"
D = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r19/"
ROUND18_VERSION = "irpt-template-reader.r18.1"
TOKENS = {"y191-scratch": "Y191-SCRATCH", "y192-census": "Y192-CENSUS", "y193-build": "Y193-BUILD", "y194-rule": "Y194-RULE",
          "y194-backstop": "Y194-BACKSTOP", "y194-keep": "Y194-KEEP", "y195-delta": "Y195-DELTA", "y196-install": "Y196-INSTALL", "y197-four": "Y197-FOUR", "y198-equal": "Y198-EQUAL", "y199-recipe": "Y199-RECIPE", "y200-two": "Y200-TWO", "y201-live": "Y201-LIVE", "y202-portal": "Y202-PORTAL", "y203-defer": "Y203-DEFER"}
SHEETS = ("two_value_account_sheet", "total_row_sheet", "one_account_sheet", "two_sheet_workbook")
NATIVE_UNPINNED = ("acceptance.py", "submission.py", "submission_service.py", "durable_job.py")
S31_FORMS = ("Account Numbers", "Subaccounts", "Accnt", "Account Nos", "Account Seqno", "Account Serial", "Roth IRA Account", "Trust Account")
SEED_IDENTIFIERS = ("Account", "Account Number", "Acct", "Brokerage Account", "IRA Account", "Joint Account", "Subaccount", "Account Seq",
                    "Account Sequence", "No. of Account", "Sub-Account", "Custodian Acct", "Client Account") + S31_FORMS
SEED_ATTRIBUTES = ("Account Holder", "Account Manager", "Account Value", "Account Status", "Account Opened", "Account Type", "Account Name",
                   "Account Balance")
SEED_NOT_ACCOUNT = ("Custodian", "Accounting", "Portfolio", "Sleeve", "Model")
BACKSTOP_TESTS = (
    "test_an_account_root_header_with_two_identifier_values_is_read_as_an_account_column",
    "test_an_account_root_header_with_one_value_is_not_several_accounts",
    "test_no_of_accounts_holding_counts_is_excluded",
    "test_no_of_accounts_holding_identifiers_is_read_as_an_account_column",
    "test_the_backstop_words_say_what_is_seen_and_ask",
)


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def pytest(root, target, cwd):
    got = subprocess.run([sys.executable, "-m", "pytest", target, "-q", "-p", "no:cacheprovider"], cwd=str(root / cwd),
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    passed, failed = re.search(r"(\d+) passed", out), re.search(r"(\d+) failed", out)
    return got.returncode, int(passed.group(1)) if passed else 0, int(failed.group(1)) if failed else 0


def load(root, rel, problems):
    if not (root / rel).is_file():
        problems.append("no %s" % rel)
        return None
    return json.loads((root / rel).read_text(encoding="utf-8"))


def reader_module(root):
    spec = importlib.util.spec_from_file_location("ar19_template_reader", str(root / INTAKE / "template_reader.py"))
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root / INTAKE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print("usage: ar19_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y191-scratch":
        rec = load(root, D % "52" + "START_STATE_SCRATCH_RUN.json", problems)
        if rec:
            pins = rec.get("pins", {})
            for key in ("uploads.py", "template_reader.py"):
                if not pins.get(key):
                    problems.append("pins lacks %s" % key)
            cases = rec.get("door_cases", [])
            names = {c.get("sheet") for c in cases}
            for sheet in SHEETS:
                if sheet not in names:
                    problems.append("the door cases lack the sheet %s" % sheet)
            for c in cases + rec.get("reopen_cases", []):
                if not c.get("outcome") or not c.get("evidence"):
                    problems.append("a case lacks its outcome or evidence: %r" % c.get("sheet"))
            if not rec.get("reopen_cases"):
                problems.append("no re-open case (a pinned-stored template re-opened under the pinned pair and under the widened pair)")
            for member in ("scratch_tree", "claim", "not_read", "what_a_person_sees"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("door cases %d, re-open cases %d" % (len(cases), len(rec.get("reopen_cases", []))))
    elif check == "y192-census":
        rec = load(root, D % "51" + "YCHARTS_GENERATE_RELEASE_CENSUS.json", problems)
        if rec:
            native = {m.get("member") for m in rec.get("native_unpinned_members", [])}
            for name in NATIVE_UNPINNED:
                if name not in native:
                    problems.append("native_unpinned_members lacks %s" % name)
            for member in ("map_entry_members", "planned_pin_moves", "members_that_move", "resident", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            res = rec.get("resident") or {}
            for member in ("pin_rule", "current_pin", "builder", "deploy_path", "owner_lane"):
                if member not in res:
                    problems.append("resident lacks %r" % member)
            print("native unpinned named %d of 4; members that move %d" % (len(native & set(NATIVE_UNPINNED)), len(rec.get("members_that_move", []))))
    elif check == "y193-build":
        rec = load(root, D % "51" + "RELEASE_BUILD_RECORD.json", problems)
        if rec:
            for member in ("package_sha256", "member_manifest", "planned_members_that_move", "actual_members_that_differ_from_baseline", "baseline", "live_equivalent_baseline", "differs_from_unpatched_baseline", "base_commit", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if rec.get("planned_members_that_move") is not None and rec.get("actual_members_that_differ_from_baseline") is not None:
                if sorted(rec["planned_members_that_move"]) != sorted(rec["actual_members_that_differ_from_baseline"]):
                    problems.append("the planned members and the members that differ are not the same set")
            if not isinstance(rec.get("member_manifest"), dict) or len(rec.get("member_manifest", {})) < 20:
                problems.append("member_manifest must map at least 20 package members to their sha256")
            print("manifest members %d" % len(rec.get("member_manifest", {})))
    elif check == "y194-rule":
        pop = load(root, D % "59" + "ACCOUNT_HEADER_POPULATION.json", problems)
        if pop:
            reader = reader_module(root)
            ident, attr, other = pop.get("identifier_forms", []), pop.get("attribute_forms", []), pop.get("not_account_forms", [])
            neg = pop.get("word_negative_controls", [])
            for label, seeds, got in (("identifier_forms", SEED_IDENTIFIERS, ident), ("attribute_forms", SEED_ATTRIBUTES, attr),
                                      ("not_account_forms", SEED_NOT_ACCOUNT, other)):
                for seed in seeds:
                    if seed not in got:
                        problems.append("%s lacks the seed %r" % (label, seed))
            for form in ident:
                if not reader._is_account_header(form):
                    problems.append("identifier form not matched: %r" % form)
            for form in attr + other + neg:
                if reader._is_account_header(form):
                    problems.append("attribute, non-account or negative-control form matched: %r" % form)
            if len(neg) < 6:
                problems.append("word_negative_controls must hold at least 6 headers (one per new modifier or tail word, plus one for the backstop)")
            print("population: %d identifier, %d attribute, %d non-account, %d negative controls" % (len(ident), len(attr), len(other), len(neg)))
    elif check == "y194-backstop":
        path = root / INTAKE / "tests" / "test_account_value_backstop.py"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if not text:
            problems.append("no test_account_value_backstop.py")
        for name in BACKSTOP_TESTS:
            if text and ("def %s(" % name) not in text:
                problems.append("the test %s is absent" % name)
        rc, passed, failed = pytest(root, "tests/test_account_value_backstop.py", INTAKE)
        print("backstop tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < len(BACKSTOP_TESTS):
            problems.append("the named backstop tests must all pass")
    elif check == "y194-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 331:
            problems.append("the intake folder must pass with at least 331 (the round-18 count)")
        version = getattr(reader_module(root), "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND18_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check == "y195-delta":
        rec = load(root, D % "55" + "RESIDENT_PACKAGE_DELTA.json", problems)
        if rec:
            for member in ("old_pin", "new_pin", "builder_args_source", "only_in_old", "only_in_new", "differing", "moved_by_this_release",
                           "other_differing_by_owner", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            moved = {m.get("member") if isinstance(m, dict) else m for m in rec.get("moved_by_this_release", [])}
            for name in ("uploads.py", "template_reader.py"):
                if not any(str(x).endswith(name) for x in moved):
                    problems.append("moved_by_this_release lacks %s" % name)
            for row in rec.get("differing", []):
                if not (row.get("member") and row.get("old_sha256") and row.get("new_sha256")):
                    problems.append("a differing row lacks its member or a hash: %r" % row.get("member"))
                    break
            print("differing %d, only in old %d, only in new %d" % (len(rec.get("differing", [])), len(rec.get("only_in_old", [])), len(rec.get("only_in_new", []))))
    elif check == "y196-install":
        rec = load(root, D % "55" + "INSTALL_SEMANTICS_SCRATCH_PROOF.json", problems)
        if rec:
            if rec.get("install_mode") not in ("OVERLAY", "REPLACE", "NEW_ROOT_COPY"):
                problems.append("install_mode must be OVERLAY, REPLACE or NEW_ROOT_COPY")
            for member in ("installer_lines_read", "scratch", "before_member_count", "after_member_count", "unbuilt_members_before", "unbuilt_members_after", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if rec.get("install_mode") == "REPLACE":
                print("NOTE: the install REPLACES -- the release STOPS and goes back to the CTO")
            print("install_mode %s; unbuilt members before %s after %s" % (rec.get("install_mode"), rec.get("unbuilt_members_before"), rec.get("unbuilt_members_after")))
    elif check == "y197-four":
        rec = load(root, D % "54" + "RESIDENT_FOUR_MEMBERS_READ.json", problems)
        if rec:
            members = {m.get("member"): m for m in rec.get("members", [])}
            for name in ("served.py", "name_rulings.json", "status.py", "resident_worker.py"):
                hit = [m for k, m in members.items() if str(k).endswith(name)]
                if not hit:
                    problems.append("the record lacks the member %s" % name)
                    continue
                for key in ("old_blob", "new_blob", "commits", "resident_use", "behaviour_change"):
                    if not hit[0].get(key):
                        problems.append("%s lacks %r" % (name, key))
            for member in ("claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("members read: %d" % len(members))
    elif check == "y198-equal":
        rec = load(root, D % "51" + "CROSS_BOX_MEMBERS_EQUALITY.json", problems)
        if rec:
            members = {m.get("member"): m for m in rec.get("members", [])}
            for name in ("loaders.py", "exemptions.json", "scopes.json", "opal_naming.py", "firm_pages.json"):
                hit = [m for k, m in members.items() if str(k).endswith(name)]
                if not hit:
                    problems.append("the record lacks the member %s" % name)
                    continue
                if hit[0].get("verdict") not in ("EQUAL", "NOT_EQUAL", "CANNOT_TELL"):
                    problems.append("%s needs a verdict EQUAL, NOT_EQUAL or CANNOT_TELL" % name)
                if not hit[0].get("owner_released_version") or not hit[0].get("release_pin_blob"):
                    problems.append("%s lacks the owner's released version or the release-pin blob" % name)
            for member in ("claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("members compared: %d" % len(members))
    elif check == "y199-recipe":
        rec = load(root, D % "55" + "RESIDENT_RECIPE_AND_DELTA.json", problems)
        if rec:
            for member in ("recipe_source", "recipe_steps", "st32_rebuild", "release_build", "delta", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            rb = rec.get("st32_rebuild") or {}
            for member in ("members_total", "matched_by_name", "matched_by_content", "unmatched_names", "host_origin_names", "pass"):
                if member not in rb:
                    problems.append("st32_rebuild lacks %r" % member)
            if "pass" in rb and rb.get("pass") is not True:
                problems.append("st32_rebuild.pass is not true: the recipe does not yet rebuild st32's members by name and content")
            delta = rec.get("delta") or {}
            for member in ("only_in_old", "only_in_new", "differing", "moved_by_this_release", "other_differing_by_owner"):
                if member not in delta:
                    problems.append("delta lacks %r" % member)
            print("st32 rebuild: total %s, by name %s, by content %s, host-origin %s" % (rb.get("members_total"), rb.get("matched_by_name"), rb.get("matched_by_content"), len(rb.get("host_origin_names") or [])))
    elif check == "y200-two":
        rec = load(root, D % "55" + "RESIDENT_TWO_MEMBER_RELEASE.json", problems)
        if rec:
            for member in ("base_pin", "scratch_commit", "recipe_args_source", "minimal_import_set", "delta_vs_st32_rebuild", "tests", "tarball", "root_naming", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            allowed = {"uploads.py", "template_reader.py", "resident_bindings.json", "SHA256SUMS"}
            extra_ok = {str(x.get("member") if isinstance(x, dict) else x).rsplit("/", 1)[-1] for x in rec.get("minimal_import_set", [])}
            diff = rec.get("delta_vs_st32_rebuild") or {}
            names = [str(r.get("member") if isinstance(r, dict) else r).rsplit("/", 1)[-1] for r in diff.get("differing", [])]
            for name in names:
                if name not in allowed and name not in extra_ok:
                    problems.append("the build differs from st32 in %s, which is neither a reader member, the bindings, SHA256SUMS nor in minimal_import_set" % name)
            for name in ("uploads.py", "template_reader.py"):
                if name not in names:
                    problems.append("the delta lacks the reader member %s" % name)
            if diff.get("removed_members_count") not in (0, "0"):
                problems.append("the build must remove no member relative to st32")
            tests = rec.get("tests") or {}
            for member in ("named_tests", "passed", "failed", "denominator"):
                if member not in tests:
                    problems.append("tests lacks %r" % member)
            accepted = ("test_the_readers_output_on_the_fixtures_is_pinned_to_its_version",
                        "test_correction_words_are_the_envelopes_words")
            explained = [str(x) for x in tests.get("failures_explained") or []]
            if tests.get("failed") not in (0, "0"):
                # AMENDMENT 1 (issuer, after CTO msg 6778): S25 and S26 are accepted named limits; any OTHER failure, or an unexplained one, still fails.
                ok_explained = (isinstance(tests.get("failed"), int) and tests.get("failed") == len(explained)
                                and all(any(e.find(name) >= 0 for name in accepted) for e in explained))
                if not ok_explained:
                    problems.append("the reader's tests must pass on the build except the two CTO-accepted, explained failures (failed=%r)" % tests.get("failed"))
            print("differing %s; tests passed %s failed %s" % (names, tests.get("passed"), tests.get("failed")))
    elif check == "y201-live":
        rec = load(root, D % "56" + "LAMBDA_LEG_LIVE_REBASE.json", problems)
        if rec:
            for member in ("live_read", "hold_pins", "release_build", "differ_from_live", "patch", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            live = (rec.get("live_read") or {})
            for member in ("code_sha256", "read_at", "member_manifest"):
                if not live.get(member):
                    problems.append("live_read lacks %r" % member)
            lman = live.get("member_manifest") or {}
            rman = (rec.get("release_build") or {}).get("member_manifest") or {}
            if len(lman) < 20 or len(rman) < 20:
                problems.append("both manifests must map at least 20 members to their sha256 (live %d, release %d)" % (len(lman), len(rman)))
            else:
                differ = sorted(k for k in set(lman) | set(rman) if lman.get(k) != rman.get(k))
                if differ != ["template_reader.py", "uploads.py"]:
                    problems.append("the release package must differ from the live package in exactly template_reader.py and uploads.py (differs in %s)" % differ)
                if sorted(rec.get("differ_from_live") or []) != differ:
                    problems.append("differ_from_live does not equal the manifests' difference")
            pins = {h.get("member"): h for h in rec.get("hold_pins") or []}
            for name in NATIVE_UNPINNED:
                h = pins.get(name)
                if not h:
                    problems.append("hold_pins lacks %s" % name)
                    continue
                if not re.fullmatch(r"[0-9a-f]{40}", str(h.get("pin", ""))):
                    problems.append("hold pin for %s is not a full commit sha" % name)
                if h.get("blob_sha256") != lman.get(name):
                    problems.append("hold pin for %s: blob sha256 is not the live member's" % name)
            if rec.get("live_equivalent_differs_from_live") != []:
                problems.append("the live-equivalent build (holds only, reader pins unmoved) must differ from the live package in no member (got %r)" % rec.get("live_equivalent_differs_from_live"))
            print("live members %d, release members %d" % (len(lman), len(rman)))
    elif check == "y202-portal":
        rec = load(root, D % "57" + "PORTAL_UPLOAD_ANSWER_READERS.json", problems)
        if rec:
            for member in ("prod_commit", "dev_commit", "readers", "cases", "new_codes", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            for key in ("prod_commit", "dev_commit"):
                if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get(key, ""))):
                    problems.append("%s is not a full commit sha" % key)
            readers = rec.get("readers") or []
            if not readers:
                problems.append("no portal reader of the upload door's answer is named")
            for r in readers:
                for member in ("file", "line", "key_policy", "at_prod", "at_dev"):
                    if member not in r:
                        problems.append("a reader lacks %r: %r" % (member, r.get("file")))
            cases = rec.get("cases") or []
            seen = set()
            for c in cases:
                if c.get("outcome") not in ("RETURNED", "THREW"):
                    problems.append("a case outcome must be RETURNED or THREW: %r" % c.get("case"))
                if c.get("arm") not in ("BEFORE", "AFTER") or c.get("commit") not in ("PROD", "DEV"):
                    problems.append("a case names no arm (BEFORE/AFTER) or commit (PROD/DEV): %r" % c.get("case"))
                if c.get("arm") == "AFTER":
                    seen.update(c.get("codes") or [])
            for code in ("ACCOUNT_COLUMN_SEVERAL_VALUES", "HEADER_ROW_REPEATED", "SHEETS_NOT_READ", "TOTAL_ROW_PRESENT"):
                if code not in seen:
                    problems.append("no AFTER case carries the new finding code %s" % code)
            print("readers %d, cases %d, new codes covered %d of 4" % (len(readers), len(cases), len(seen & {"ACCOUNT_COLUMN_SEVERAL_VALUES", "HEADER_ROW_REPEATED", "SHEETS_NOT_READ", "TOTAL_ROW_PRESENT"})))
    elif check == "y203-defer":
        rec = load(root, D % "58" + "PORTAL_DEFER_SHAPE_READERS.json", problems)
        if rec:
            for member in ("prod_commit", "dev_commit", "cases", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            cases = rec.get("cases") or []
            seen, commits = set(), set()
            for c in cases:
                if not str(c.get("body_source", "")).startswith("_defer"):
                    problems.append("case %r: body_source must start with _defer (the deployed first answer)" % c.get("case"))
                keys = set(c.get("body_keys") or [])
                if not {"reason", "findings", "findings_total", "template", "state", "upload_id", "input_id"} <= keys:
                    problems.append("case %r: the body lacks a _defer member (has %s)" % (c.get("case"), sorted(keys)))
                if c.get("reason") != "TEMPLATE_FINDINGS":
                    problems.append("case %r: reason must be TEMPLATE_FINDINGS" % c.get("case"))
                if c.get("outcome") not in ("RETURNED", "THREW"):
                    problems.append("case %r: outcome must be RETURNED or THREW" % c.get("case"))
                if c.get("arm") not in ("BEFORE", "AFTER") or c.get("commit") not in ("PROD", "DEV"):
                    problems.append("case %r: arm or commit missing" % c.get("case"))
                if c.get("arm") == "AFTER":
                    seen.update(c.get("codes") or [])
                    commits.add(c.get("commit"))
            for code in ("ACCOUNT_COLUMN_SEVERAL_VALUES", "HEADER_ROW_REPEATED", "TOTAL_ROW_PRESENT"):
                if code not in seen:
                    problems.append("no AFTER _defer case carries %s" % code)
            if commits != {"PROD", "DEV"}:
                problems.append("AFTER cases must cover both PROD and DEV (got %s)" % sorted(commits))
            print("cases %d, AFTER codes %s" % (len(cases), sorted(seen)))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
