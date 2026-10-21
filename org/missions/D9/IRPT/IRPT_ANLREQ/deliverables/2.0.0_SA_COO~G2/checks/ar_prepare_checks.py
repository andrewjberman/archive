"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the Opal comparison path's frozen read (cell AR-g-182).
READ ONLY, offline, no AWS. Needs a python with jsonschema and referencing (not `-I`).

    python ar_prepare_checks.py frozen [--root <lambda tree root>]
    python ar_prepare_checks.py worker [--root <lambda tree root>]
    python ar_prepare_checks.py tests [--root <lambda tree root>]

Why: run 7I (a Multi-Comp filing on the r34q resident) stopped at P1 with `retained_for_retry class=RecipeRefused`. The inner message,
read by replaying the run's retained synthetic composition (fixtures/composition_7i_synthetic.json) through the module, is
`holdings row has no provider receipt`: the resident's Opal comparison path (AR-g-175, `_opal_comparables`) calls
`FrozenCompositionWorker.prepare`, which also builds the VENDOR upload (`prepare_normalized_upload`), and the run's holdings are priced from
history (security check reason YFINANCE_HISTORY, no provider receipt). An Opal job makes no vendor call and needs only the comparisons. A second
defect sits behind the first: `_opal_comparables` read `key`, `label` and `ticker` off the catalogue entry, but the retained catalogue's model
entries carry `name`, `namespace`, `security_type`, `source_id`, `vendor_id` and NO key (the key is the catalogue's own dict key), so the
producer would have received key None for every model.

`frozen`: the REAL FrozenCompositionWorker.prepare, with its collaborators stubbed (the retained composition and its normalized document are the
fixture's own bytes), run three ways: (a) the default call still refuses with RecipeRefused 'provider receipt' (the vendor path is unchanged);
(b) `upload=False` returns the prepared dict with `upload` None, `variant` multicomp and the new field `comparison_keys` (browser order);
(c) the comparisons are the two catalogue entries, names Opal Short-Term and Opal Long-Term.
`worker`: the REAL ResidentGenerationWorker._opal_comparables with a recording stand-in for `frozen`: it must call prepare with upload=False and
return one {key, label, ticker} per chosen key, key = the catalogue key, label = the entry's name, ticker None for a model and the entry's
key for an ETF.
`tests`: the two owned test files pass (25 at the base) and at least 27 ran, so each defect has a test of its own.
Prints one RESULT line: AR-PREP-<arm>-OK or AR-PREP-<arm>-FAIL <why>. ASCII only.
"""
import copy
import hashlib
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures", "composition_7i_synthetic.json")
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"

TEST_FILES = ['ycharts/generate/tests/test_frozen_worker.py', 'reports/tests/test_compare_ports.py']
MIN_TESTS = 27


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    sys.path[:0] = [os.path.join(base, p) for p in ("ycharts/generate", "ops", "reports", "intake", "_scope", "_ids", "_keys", "_authz",
                                                      "ycharts/research", "ycharts/session", "ycharts/extract", "ycharts/transport", "lib")] + [base]
    return base


def fail(arm, why):
    print("AR-PREP-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def stub_worker(doc, submission):
    """A FrozenCompositionWorker over stubs that serve the fixture's own retained bytes."""
    import frozen_worker as fw
    canon = submission.canonical_bytes
    res = doc["resolved"]
    data = canon(doc)
    owner = res["owner"]
    firm = owner["firm_id"]
    import acceptance
    request_id = acceptance.request_id_for(firm, owner["principal_id"], doc["browser"]["request_id"])
    comp_ref = {"artifact_id": "ART-" + hashlib.sha256(b"comp").hexdigest(), "sha256": hashlib.sha256(data).hexdigest(),
                "retention_ref": {"policy_revision": "irpt-x10-v1", "retention_id": "RET-comp"}}
    input_artifact = res["input_ref"]["artifact_ref"]
    deps = [input_artifact["retention_ref"]]
    deps.extend(s["retention_ref"] for s in res["source_descriptors"].values() if s.get("retention_ref") is not None)
    input_owner = submission.input_repository_owner(res)
    record = {"composition_ref": comp_ref, "owner": owner, "browser_sha256": submission.digest(doc["browser"]),
              "identity": {"request_id": request_id, "revision": 1}}

    class Retention:
        def require_live(self, principal, ref, **kw):
            if ref == comp_ref["retention_ref"]:
                return {"owner": owner, "dependencies": deps}
            return {"owner": input_owner, "dependencies": []}

    class Artifacts:
        retention = Retention()

        def get(self, principal, artifact_id, **kw):
            if artifact_id == comp_ref["artifact_id"]:
                return {"ref": comp_ref, "data": data}
            return {"ref": input_artifact, "data": canon(res["document"])}

    requests = types.SimpleNamespace(
        acceptance=types.SimpleNamespace(get=lambda f, r: copy.deepcopy(record)),
        _validate=lambda *a, **k: None, _final=lambda *a, **k: None,
        authorize_current=lambda *a, **k: True, artifacts=Artifacts())
    store = types.SimpleNamespace(tenant=firm, request_id=request_id, composition_sha256=comp_ref["sha256"],
                                  assert_current=lambda: None)
    admission = types.SimpleNamespace(validate=lambda document: data)
    worker = object.__new__(fw.FrozenCompositionWorker)
    worker.requests, worker.store, worker.admission = requests, store, admission
    return worker, {"firm_id": firm, "principal_id": owner["principal_id"]}, request_id


def arm_frozen():
    import submission
    doc = json.load(open(FIXTURE, encoding="utf-8"))
    worker, principal, request_id = stub_worker(doc, submission)
    from recipe import RecipeRefused
    try:
        worker.prepare(principal, request_id)
        fail("frozen", "the default prepare (the vendor path) no longer refuses a holding with no provider receipt")
    except RecipeRefused as exc:
        if "provider receipt" not in str(exc):
            fail("frozen", "the default prepare refused with a different message: %s" % str(exc)[:80])
    except Exception as exc:  # noqa: BLE001
        fail("frozen", "the default prepare raised %s, not RecipeRefused: %s" % (type(exc).__name__, str(exc)[:80]))
    try:
        got = worker.prepare(principal, request_id, upload=False)
    except TypeError as exc:
        fail("frozen", "prepare takes no upload=False option yet: %s" % str(exc)[:80])
    except Exception as exc:  # noqa: BLE001
        fail("frozen", "prepare(upload=False) raised %s: %s" % (type(exc).__name__, str(exc)[:100]))
    problems = []
    if got.get("upload") is not None:
        problems.append("upload is not None")
    if got.get("variant") != "multicomp":
        problems.append("variant %r" % (got.get("variant"),))
    if got.get("comparison_keys") != ["opal_short_term", "opal_long_term"]:
        problems.append("comparison_keys %r" % (got.get("comparison_keys"),))
    names = [c.get("name") for c in got.get("comparisons") or []]
    if names != ["Opal Short-Term", "Opal Long-Term"]:
        problems.append("comparison names %r" % (names,))
    if problems:
        fail("frozen", "; ".join(problems))
    print("AR-PREP-frozen-OK")


def arm_worker():
    import resident_worker as rw
    prepared_models = {
        "comparison_keys": ["opal_short_term", "opal_long_term"],
        "comparisons": [{"mapping_evidence": "x", "name": "Opal Short-Term", "namespace": "YCHARTS", "security_type": "model_portfolio",
                         "source_id": "opal_short_term", "vendor_id": "P:1"},
                        {"mapping_evidence": "x", "name": "Opal Long-Term", "namespace": "YCHARTS", "security_type": "model_portfolio",
                         "source_id": "opal_long_term", "vendor_id": "P:2"}]}
    prepared_etf = {
        "comparison_keys": ["opal_short_term", "IWM"],
        "comparisons": [prepared_models["comparisons"][0],
                        {"key": "IWM", "vendor_id": "IWM", "name": "iShares Russell 2000 ETF", "security_type": "etf",
                         "namespace": "YCHARTS", "mapping_evidence": "ETF_CLASSIFICATIONS:x"}]}
    calls = []

    def make(prepared):
        def prepare(principal, request_id, **kw):
            calls.append(kw)
            if kw.get("upload", True):
                raise RuntimeError("the vendor upload would be prepared")
            return copy.deepcopy(prepared)
        return types.SimpleNamespace(frozen=types.SimpleNamespace(prepare=prepare), store=types.SimpleNamespace(tenant="49financial"))

    problems = []
    for tag, prepared, want in (
            ("models", prepared_models, [{"key": "opal_short_term", "label": "Opal Short-Term", "ticker": None},
                                         {"key": "opal_long_term", "label": "Opal Long-Term", "ticker": None}]),
            ("model+etf", prepared_etf, [{"key": "opal_short_term", "label": "Opal Short-Term", "ticker": None},
                                         {"key": "IWM", "label": "iShares Russell 2000 ETF", "ticker": "IWM"}])):
        del calls[:]
        try:
            got = rw.ResidentGenerationWorker._opal_comparables(make(prepared), {"firm_id": "49financial", "principal_id": "p"}, "REQ-x")
        except Exception as exc:  # noqa: BLE001
            problems.append("%s: raised %s: %s" % (tag, type(exc).__name__, str(exc)[:80]))
            continue
        if got != want:
            problems.append("%s: got %r" % (tag, got))
        if not calls or calls[-1].get("upload") is not False:
            problems.append("%s: prepare was not called with upload=False (%r)" % (tag, calls))
    if problems:
        fail("worker", "; ".join(problems))
    print("AR-PREP-worker-OK")


def arm_tests(root):
    """The owned test files, run with plain python from the lambda tree: all pass and at least MIN_TESTS ran (the baseline plus the new tests)."""
    import re
    import subprocess
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + TEST_FILES
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < MIN_TESTS:
        print("AR-%s-tests-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % ("PREP", run.returncode, passed, MIN_TESTS,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-%s-tests-OK passed=%d" % ("PREP", passed))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("frozen", "worker", "tests"):
        print("usage: ar_prepare_checks.py frozen|worker|tests [--root <root>]")
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    if sys.argv[1] == "tests":
        arm_tests(root)
        return
    paths(root)
    {"frozen": arm_frozen, "worker": arm_worker}[sys.argv[1]]()


if __name__ == "__main__":
    main()
