"""IRPT_ANLREQ AR-g-85 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g85_checks.py g85       the variant selection answers its direct cases (loader, make_opal_stores, the accept stamp),
                                      and the thirteen named new tests exist and pass
    python ar_g85_checks.py regress   seven existing test files (run one at a time) still pass, 65 tests in all

Prints one RESULT line: AR-G85-OK / AR-G85-FAIL or AR-G85-REGRESS-OK / AR-G85-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/"
NEW_TESTS = {
    R + "ycharts/generate/tests/test_report_variant_stamp.py": [
        "test_accept_stamps_overview_without_comparison_keys",
        "test_accept_stamps_comparison_for_one_key",
        "test_accept_stamps_multicomp_for_two_or_more_keys",
        "test_replay_returns_the_prior_record_unchanged",
        "test_client_cannot_send_report_variant",
    ],
    R + "reports/tests/test_opal_variant_binding.py": [
        "test_loader_reads_each_variants_pinned_map",
        "test_loader_default_is_overview",
        "test_unknown_variant_is_refused",
        "test_missing_variant_binding_is_refused_while_overview_still_loads",
        "test_absent_and_changed_pin_name_the_binding",
        "test_make_opal_stores_selects_the_map_by_the_record_variant",
        "test_record_without_variant_takes_overview_with_no_argument",
        "test_bogus_variant_refused_before_any_client_opens",
    ],
}
EXISTING = [R + "ycharts/generate/tests/test_acceptance_actor.py", R + "ycharts/generate/tests/test_commentary_requested_member.py",
            R + "ycharts/generate/tests/test_ready_signal_ticket_gate.py", R + "ycharts/generate/tests/test_producer_actor.py",
            R + "ycharts/generate/tests/test_opal_thread_integration.py", R + "reports/tests/test_resident_installed.py",
            R + "reports/tests/test_generate_installed.py"]
FIRM = "synthetic-firm-one"
OWNER = {"firm_id": FIRM, "principal_id": "synthetic-staff-one", "advisor_id": "synthetic-staff-one", "ownership_fingerprint": "b" * 64}
REF = {"artifact_id": "ART-one", "sha256": "a" * 64, "version_id": "version-one"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error|skipped)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0, text


def refusal(fn, *args):
    try:
        fn(*args)
    except Exception as exc:
        return type(exc).__name__ + ":" + str(exc)
    return "NO-REFUSAL"


def put_map(folder, name, doc):
    path = Path(folder) / name
    path.write_text(json.dumps(doc), encoding="utf-8")
    return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def load_modules():
    root = Path(R)
    for rel in ("reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "_scope", "_ids", "_keys", "_authz", "intake", "ops"):
        sys.path.insert(0, str(root / rel))
    sys.path.insert(0, "lib")
    import acceptance
    import resident_installed
    import submission
    return acceptance, resident_installed, submission


def loader_cases(ri):
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        bindings = {"opal_map": put_map(tmp, "o.json", {"report_type": "OVERVIEW"}),
                    "opal_map_comparison": put_map(tmp, "c.json", {"report_type": "COMPARISON"}),
                    "opal_map_multicomp": put_map(tmp, "m.json", {"report_type": "MULTI"})}
        load = ri._opal_map_loader(bindings, tmp)
        out["each variant reads its own pinned map"] = (load("overview")["report_type"] == "OVERVIEW"
            and load("comparison")["report_type"] == "COMPARISON" and load("multicomp")["report_type"] == "MULTI")
        out["no argument is the overview"] = load()["report_type"] == "OVERVIEW"
        out["an unknown variant is refused by name"] = all(
            refusal(load, v) == "ResidentInstallRefused:OPAL_VARIANT_UNKNOWN" for v in ("x", "", None, 5, "OVERVIEW"))
        partial = ri._opal_map_loader({"opal_map": bindings["opal_map"]}, tmp)
        out["a variant with no binding is refused while the overview still loads"] = (
            refusal(partial, "comparison") == "ResidentInstallRefused:OPAL_MAP_BINDING_REQUIRED"
            and refusal(partial, "multicomp") == "ResidentInstallRefused:OPAL_MAP_BINDING_REQUIRED"
            and partial()["report_type"] == "OVERVIEW")
        gone = dict(bindings, opal_map_comparison={"path": "nope.json", "sha256": "0" * 64}, opal_map={"path": "nope.json", "sha256": "0" * 64})
        absent = ri._opal_map_loader(gone, tmp)
        out["an absent file names its binding"] = (refusal(absent, "comparison") == "ResidentInstallRefused:PINNED_FILE_ABSENT:opal_map_comparison"
            and refusal(absent) == "ResidentInstallRefused:PINNED_FILE_ABSENT:opal_map")
        wrong = ri._opal_map_loader(dict(bindings, opal_map_multicomp={"path": "m.json", "sha256": "f" * 64}, opal_map={"path": "o.json", "sha256": "f" * 64}), tmp)
        out["a changed file names its binding"] = (refusal(wrong, "multicomp") == "ResidentInstallRefused:PINNED_FILE_DIFFERS:opal_map_multicomp"
            and refusal(wrong) == "ResidentInstallRefused:PINNED_FILE_DIFFERS:opal_map")
    return out


def stores_cases(ri):
    out = {}
    seen, opened = [], []

    def load_map(*args):
        seen.append(args)
        return {"variant": args[0] if args else "overview"}

    def make():
        return ri.make_opal_stores(dynamodb="D", s3="S", artifacts="A", load_map=load_map,
                                   open_objects=lambda firm, rid: opened.append("objects") or "O",
                                   open_classifier=lambda: opened.append("classifier") or "C", clock=lambda: 1)
    stores = make()
    principal = {"firm_id": FIRM, "principal_id": "p"}

    def record(**extra):
        rec = {"owner": {"firm_id": FIRM, "principal_id": "nobody@example.invalid"},
               "identity": {"tenant_firm_id": FIRM, "request_id": "REQ-INVENTED01"},
               "composition_ref": {"retention_ref": {"id": "ret-one"}}, "ticket_confirmed": True}
        rec.update(extra)
        return rec
    got = stores(principal, record(report_variant="comparison"))
    out["a comparison record gets the comparison map"] = got["map"] == {"variant": "comparison"} and seen[-1] == ("comparison",)
    got = stores(principal, record(report_variant="multicomp"))
    out["a multicomp record gets the multicomp map"] = got["map"] == {"variant": "multicomp"} and seen[-1] == ("multicomp",)
    got = stores(principal, record())
    out["a record with no variant calls load_map with no argument"] = got["map"] == {"variant": "overview"} and seen[-1] == ()
    got = stores(principal, record(report_variant="overview"))
    out["an overview record calls load_map with no argument"] = got["map"] == {"variant": "overview"} and seen[-1] == ()
    before = (len(seen), len(opened))
    out["a bogus variant is refused before any map or client"] = (
        all(refusal(stores, principal, record(report_variant=v)) == "ValueError:OPAL_VARIANT_UNKNOWN" for v in ("bogus", None, 5, ""))
        and (len(seen), len(opened)) == before)
    out["an unlisted principal is still refused first"] = refusal(
        stores, principal, record(ticket_confirmed=False, report_variant="comparison")) == "PermissionError:OPAL_PRINCIPAL_NOT_LISTED"
    return out


def accept_cases(acceptance, submission):
    out = {}
    from unittest.mock import Mock
    with tempfile.TemporaryDirectory() as tmp:
        registry = Path(tmp) / "firm_registry.json"
        registry.write_text(json.dumps({"firms": [{"firm_id": FIRM, "enabled": True, "kind": "client"}]}), encoding="utf-8")
        acceptance.keys._find_registry = lambda: str(registry)

        def browser(keys):
            return {"request_id": "areq-1234", "client_id": None, "account_ids": [], "snapshot_id": None,
                    "input_id": "portfolio_" + "a" * 64, "variant": "auto", "comparison_keys": keys,
                    "report_title": None, "prepared_for": "Synthetic recipient"}

        def stamp(keys):
            client = Mock()
            client.get_item.return_value = {}
            store = acceptance.DynamoAcceptance(client, now=lambda: 100)
            accepted = store.accept(OWNER, browser(keys), REF, ingestion_revision="v1", destination_revision="v1",
                                    acting_principal_id=OWNER["principal_id"])
            stored = json.loads(client.transact_write_items.call_args.kwargs["TransactItems"][0]["Put"]["Item"]["record"]["S"])
            return accepted.get("report_variant"), stored.get("report_variant")
        out["no comparison key stamps overview"] = stamp([]) == ("overview", "overview")
        out["one comparison key stamps comparison"] = stamp(["cmp-one"]) == ("comparison", "comparison")
        out["two or three comparison keys stamp multicomp"] = stamp(["cmp-one", "cmp-two"]) == ("multicomp", "multicomp") and stamp(
            ["cmp-one", "cmp-two", "cmp-three"]) == ("multicomp", "multicomp")
        out["a client-sent report_variant is refused"] = refusal(
            submission.validate_public_request, dict(browser([]), report_variant="comparison")).startswith("SubmissionRefused")
    return out


def main(mode):
    if mode == "g85":
        try:
            acceptance, ri, submission = load_modules()
        except Exception as exc:
            print("AR-G85-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        got = {}
        for fn, args in ((loader_cases, (ri,)), (stores_cases, (ri,)), (accept_cases, (acceptance, submission))):
            try:
                got.update(fn(*args))
            except Exception as exc:
                print("AR-G85-FAIL a case group raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
                return 1
        wrong = [k for k, ok in got.items() if not ok]
        missing = []
        for path, names in NEW_TESTS.items():
            rc, line, passed, text = pytest_run([path], extra=("--collect-only",))
            have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
            missing += [n for n in names if n not in have]
        rc, line, passed, text = pytest_run(list(NEW_TESTS))
        need = sum(len(v) for v in NEW_TESTS.values())
        print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
        print("named tests missing: %s" % (missing or "none"))
        print("new tests: %s" % line)
        if wrong or missing or rc != 0 or bad_count(line) or passed < need:
            print("AR-G85-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G85-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < 65:
            print("AR-G85-REGRESS-FAIL files=%s passed=%d (need >= 65)" % (bad or "none", total))
            return 1
        print("AR-G85-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g85_checks.py g85|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
