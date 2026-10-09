"""IB-pr-391 replay driver: live versus built artifacts, offline. Writes IB97-4_release_replay.json.

  python -B run_replay.py <repo_root> <built_dir> <live_root> <scratch> <out.json>

  <built_dir>  the BUILT irpt-commentary-composition-read-lambda zip, extracted (flat)
  <live_root>  a directory holding the LIVE zips of irpt-performance-adapter, irpt-ycharts-generate, irpt-export-render and
               irpt-status, each extracted into <live_root>/<function>/
  <scratch>    a directory OUTSIDE the worktree (junit xml, mutated copies)
Nothing is read from AWS here (the live zips are fetched beforehand by the caller) and nothing is written to the tree.
ASCII only.
"""
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo, built, live_root, scratch, out = (Path(a).resolve() for a in sys.argv[1:6])
HERE = Path(__file__).resolve().parent
TESTS = repo / "infra/aws/lambda/investor-reporting/reports/tests"
LIVE = ["irpt-performance-adapter", "irpt-ycharts-generate", "irpt-export-render", "irpt-status"]
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "empty.ini").write_text("[pytest]\n", encoding="ascii")
arms = []


def pytest_run(tag, modules, files):
    xml = scratch / (tag + ".xml")
    plug = scratch / (tag + ".plugin.json")
    env = dict(os.environ, PYTHONPATH=str(HERE), REPLAY_MODULES=str(modules), REPLAY_REPO=str(repo),
               REPLAY_PLUGIN_OUT=str(plug), PYTHONDONTWRITEBYTECODE="1")
    cmd = [sys.executable, "-B", "-m", "pytest", "-p", "replay_preload", "-p", "no:cacheprovider", "-q", "-c",
           str(scratch / "empty.ini"), "--rootdir", str(scratch), "--junitxml", str(xml)] + [str(f) for f in files]
    r = subprocess.run(cmd, cwd=str(scratch), env=env, capture_output=True, text=True, timeout=900)
    res = {}
    if xml.is_file():
        for tc in ET.parse(xml).getroot().iter("testcase"):
            bad = tc.find("failure") is not None or tc.find("error") is not None
            skipped = tc.find("skipped") is not None
            res[tc.get("classname", "").split(".")[-1] + "::" + tc.get("name")] = "SKIP" if skipped else ("FAIL" if bad else "PASS")
    info = json.loads(plug.read_text(encoding="ascii")) if plug.is_file() else {}
    return {"rc": r.returncode, "tail": r.stdout.strip().splitlines()[-1:] + r.stderr.strip().splitlines()[-1:], "tests": res,
            "plugin": info}


def counts(res):
    c = {}
    for v in res.values():
        c[v] = c.get(v, 0) + 1
    return c


# ---- arm 1 + 2: the built surface (ten repo tests + four deployed-composition tests), own tenant OK / another tenant REFUSED
svc_files = [TESTS / "test_svc_commentary.py", HERE / "replay_extra_test.py"]
run_built = pytest_run("built_surface", built, svc_files)
t = run_built["tests"]
own = [k for k in t if "own_tenant" in k or "returns_the_document" in k or "ok_sha_equal" in k]
other = [k for k in t if "another_tenant" in k or "other_tenant" in k]
arms.append({
    "name": "own-tenant REQUEST_COMPOSITION read through the built surface",
    "verdict": "expected-diff" if run_built["rc"] == 0 and own and all(t[k] == "PASS" for k in own) else "FAIL",
    "negative_control": False,
    "detail": "pytest rc %s over the BUILT package (%s), counts %s. Own-tenant tests: %s. Asserted: status OK, sha256 equals "
              "composition_ref.sha256, no owner/principal/account text in the answer, redacted_count 2, one GetItem on "
              "analysis#<id>#1 in the tenant partition. The live artifact for this function is ABSENT (live_before), so the "
              "difference from live is the whole function; the packaged opal_naming policy irpt-x10-v1 (ACTIVE) and "
              "reporting_destination drive the deployed composition." % (run_built["rc"], run_built["plugin"].get("loaded"),
                                                                           counts(t), {k: t[k] for k in own}),
})
arms.append({
    "name": "another tenant REFUSED through the built surface",
    "verdict": "expected-diff" if run_built["rc"] == 0 and other and all(t[k] == "PASS" for k in other) else "FAIL",
    "negative_control": False,
    "detail": "tests %s (cottonwood, inflection, global, opal-capital against a 49financial request: status REFUSED, no "
              "composition and no sha256 in the answer; a service principal bound to cottonwood reading a 49financial "
              "artifact: ReportDenied, no blob read)." % ({k: t[k] for k in other},),
})

# ---- arm 3: existing ArtifactRepository.get() callers, identical through every live zip and the built one
diffs = {}
base = None
for name, d in [("built", built)] + [(f, live_root / f) for f in LIVE]:
    o = scratch / ("get_%s.json" % name)
    r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "replay_get_diff.py"), str(d), str(o)], capture_output=True, text=True)
    if r.returncode:
        diffs[name] = "HARNESS-FAILED rc %s %s" % (r.returncode, r.stderr[-200:])
        continue
    data = json.loads(o.read_text(encoding="ascii"))
    if name == "built":
        base = data
    diffs[name] = data
repo_hashes = {k: v["repository_sha256"][:12] for k, v in diffs.items() if isinstance(v, dict)}
same = {k: (v["outcomes"] == base["outcomes"]) for k, v in diffs.items() if isinstance(v, dict)}
arms.append({
    "name": "existing ArtifactRepository.get()/head()/put() callers: identical through the live and built repository.py",
    "verdict": "identical" if base and len(same) == 5 and all(same.values()) else "FAIL",
    "negative_control": False,
    "detail": "%d scenarios (own get/head, retry, other principal same firm, same name other firm, wrong data_firm, unknown and "
              "malformed ids, a USER named svc-commentary, unregistered family, conflicting bytes, put for another owner, "
              "object and row counts) driven over offline fakes; outcomes equal to the built repository.py for: %s. "
              "repository.py sha256 prefixes: %s (the built one is the only one carrying the service-subject rule)."
              % (len(base["outcomes"]) if base else 0, same, repo_hashes),
})

# ---- arm 3b: the repo's retained-repository suites (existing callers through retention) on the built package and on live
suites = [TESTS / n for n in ("test_repository.py", "test_retained_repository.py", "test_retention.py",
                              "test_repository_family_revisions.py")]
suites = [s for s in suites if s.is_file()]
run_suite_built = pytest_run("suites_built", built, suites)
run_suite_live = pytest_run("suites_live_export_render", live_root / "irpt-export-render", suites)
sb, sl = run_suite_built["tests"], run_suite_live["tests"]
common = sorted(set(sb) & set(sl))
disagree = [k for k in common if sb[k] != sl[k]]
arms.append({
    "name": "existing retained-repository suites (repository, retention, family revisions): built package versus the live irpt-export-render package",
    "verdict": "identical" if common and not disagree and run_suite_built["rc"] == run_suite_live["rc"] else "FAIL",
    "negative_control": False,
    "detail": "%d tests common to both runs; disagreeing: %s; built counts %s (rc %s), live counts %s (rc %s); path-loaded "
              "repository.py substituted by the package copy %d (built) and %d (live) times. irpt-export-render is the live "
              "function holding the previous repository.py (f01fcf549e8e, the parent of the IB-pr-386 change)."
              % (len(common), disagree, counts(sb), run_suite_built["rc"], counts(sl), run_suite_live["rc"],
                 len(run_suite_built["plugin"].get("substituted", [])), len(run_suite_live["plugin"].get("substituted", []))),
})

# ---- negative control 1: the LIVE repository/retention/composition cannot serve the subject (surface over the live modules)
mix = scratch / "mix_live_repo_built_surface"
if mix.exists():
    shutil.rmtree(mix)
shutil.copytree(live_root / "irpt-export-render", mix)
shutil.copy2(built / "commentary_composition.py", mix / "commentary_composition.py")
run_mix = pytest_run("neg_live_repo", mix, [TESTS / "test_svc_commentary.py"])
loaded = run_mix["plugin"].get("loaded", {})
fired = run_mix["rc"] != 0 and (str(loaded.get("commentary_composition", "")).startswith("IMPORT-FAILED") or
                                 any(v == "FAIL" for v in run_mix["tests"].values()))
arms.append({
    "name": "NEGATIVE CONTROL: the same surface tests over the LIVE repository.py/retention.py (no service-subject rule)",
    "verdict": "expected-diff" if fired else "FAIL",
    "negative_control": True,
    "detail": "pytest rc %s; plugin load of commentary_composition over the live modules: %s; counts %s. The control fires "
              "(non-zero, import or test failure), so the passing of arms 1 and 2 is carried by the built repository.py "
              "and not by an assertion that passes whatever it reads." % (run_mix["rc"], loaded.get("commentary_composition"), counts(run_mix["tests"])),
})

# ---- negative control 2: the get() harness detects a widened user rule (authorize check removed in a scratch copy)
mut = scratch / "mutant_built"
if mut.exists():
    shutil.rmtree(mut)
shutil.copytree(built, mut)
src = (mut / "repository.py").read_text(encoding="utf-8")
needle = "or self.authorize(principal, owner) is not True):\n            raise ReportDenied(\"artifact access denied\")"
assert src.count(needle) == 1, "mutation site not unique: %d" % src.count(needle)
(mut / "repository.py").write_text(src.replace(needle, "):\n            raise ReportDenied(\"artifact access denied\")"), encoding="utf-8")
mo = scratch / "get_mutant.json"
subprocess.run([sys.executable, "-I", "-B", str(HERE / "replay_get_diff.py"), str(mut), str(mo)], check=True, capture_output=True)
mdata = json.loads(mo.read_text(encoding="ascii"))
changed = sorted(k for k in base["outcomes"] if mdata["outcomes"].get(k) != base["outcomes"][k])
arms.append({
    "name": "NEGATIVE CONTROL: a repository.py with the user authorize check removed is caught by the get() harness",
    "verdict": "expected-diff" if changed else "FAIL",
    "negative_control": True,
    "detail": "mutant (scratch copy, one expression) changes outcomes %s; the identical verdict of the existing-callers arm is "
              "therefore a comparison that can fail." % (changed,),
})

# ---- negative control 3 is inside arm 1/2's run: test_deployed_composition_tampered_blob_is_refused
tb = [k for k in run_built["tests"] if "tampered" in k]
arms.append({
    "name": "NEGATIVE CONTROL: a blob changed after retention is refused by the built surface (integrity)",
    "verdict": "expected-diff" if tb and all(run_built["tests"][k] == "PASS" for k in tb) else "FAIL",
    "negative_control": True,
    "detail": "tests %s: the stored bytes replaced after the write -> status REFUSED, no composition returned." % ({k: run_built["tests"][k] for k in tb},),
})

# ---- flat import: the package imports with nothing but the zip directory on the path (no repo, no network)
code = ("import sys; sys.path.insert(0, %r); import commentary_composition as c, opal_naming as o; "
        "assert callable(c.lambda_handler); p = o.reporting_policy('irpt-x10-v1'); assert p['state'] == 'ACTIVE'; "
        "print('FLAT-IMPORT-OK', c.__file__.startswith(%r))" % (str(built), str(built)))
fr = subprocess.run([sys.executable, "-I", "-B", "-c", code], cwd=str(scratch), capture_output=True, text=True)
arms.append({
    "name": "the built package imports flat (python -I, only the extracted zip on the path) and its packaged registry resolves irpt-x10-v1 ACTIVE",
    "verdict": "expected-diff" if fr.returncode == 0 and "FLAT-IMPORT-OK True" in fr.stdout else "FAIL",
    "negative_control": False,
    "detail": "rc %s; %s %s" % (fr.returncode, fr.stdout.strip(), fr.stderr.strip()[-200:]),
})

out.write_text(json.dumps({"arms": arms}, indent=1), encoding="ascii")
for a in arms:
    print(a["verdict"], "|", a["name"][:100])
sys.exit(0 if all(a["verdict"] != "FAIL" for a in arms) else 1)
