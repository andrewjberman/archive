"""IB-pr-399 replay driver (from IB-pr-394's; narrative only, drives the zip's own entry.ENTRY). From the worktree root, scratch directory OUTSIDE the worktree:
    python <this file> <scratch_dir> <pin> <out_replay_json>
<scratch_dir>/zips/<function>.1.zip are the BUILD_ONLY outputs (the REAL source map, no override); the LIVE zips and the live
layers are read from AWS (read only). Each tree is extracted into <scratch_dir> and run with
`python -I authz_case_runner.py`. Nothing is written to AWS. ASCII only.

Host: irpt-narrative (one route, from docs/contracts/investor-reporting/v1/routes.json at the pin).
"""
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, out_path = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
FUNCS = ["irpt-narrative"]
OLD_ERRORS_PIN = "bc3727b3a37de412c48d70e3ece13fd7ed27aa6c"
spec = importlib.util.spec_from_file_location("rc", str(ROOT / "infra/aws/lambda/ci/release-census.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

routes_path = scratch / "routes.json"
routes_path.write_bytes(subprocess.run(["git", "show", "%s:docs/contracts/investor-reporting/v1/routes.json" % pin],
                                       cwd=str(ROOT), capture_output=True, check=True).stdout)
old_errors = subprocess.run(["git", "show", "%s:infra/aws/lambda/investor-reporting/_authz/errors.py" % OLD_ERRORS_PIN],
                            cwd=str(ROOT), capture_output=True, check=True).stdout


PRE_BINDING_PIN = subprocess.run(["git", "rev-parse", pin + "^"], cwd=str(ROOT), capture_output=True, check=True).stdout.decode().strip()
pre_entry = subprocess.run(["git", "show", "%s:infra/aws/lambda/investor-reporting/narrative/entry.py" % PRE_BINDING_PIN],
                           cwd=str(ROOT), capture_output=True, check=True).stdout


def extract(data, dest):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(str(dest))


def layer_dirs(f):
    cfg = json.loads(subprocess.run(["aws", "lambda", "get-function-configuration", "--function-name", f, "--output", "json"],
                                    capture_output=True, check=True).stdout.decode("utf-8"))
    dirs = []
    for layer in cfg.get("Layers") or []:
        arn = layer["Arn"]
        dest = scratch / "layers" / arn.split(":layer:")[1].replace(":", "_")
        if not dest.exists():
            lv = json.loads(subprocess.run(["aws", "lambda", "get-layer-version-by-arn", "--arn", arn, "--output", "json"],
                                           capture_output=True, check=True).stdout.decode("utf-8"))
            with urllib.request.urlopen(lv["Content"]["Location"], timeout=120) as resp:  # noqa: S310 - presigned, read only
                extract(resp.read(), dest)
        dirs.append(str(dest / "python"))
    return dirs


def run_tree(tree, label, f, layers, tag):
    out = scratch / ("case_%s_%s.json" % (tag, f))
    r = subprocess.run([sys.executable, "-I", str(HERE / "authz_case_runner.py"), str(tree), str(routes_path), label, str(out), f] + layers,
                       capture_output=True, cwd=str(scratch))
    if r.returncode:
        raise SystemExit("runner failed %s %s: %s" % (tag, f, r.stderr.decode("utf-8", "replace")[-600:]))
    return json.loads(out.read_text(encoding="utf-8"))


results, old_err_runs, pre_runs = {}, {}, {}
for f in FUNCS:
    layers = layer_dirs(f)
    extract(rc.fetch_live_zip(ROOT, f), scratch / "live" / f)
    extract((scratch / "zips" / (f + ".1.zip")).read_bytes(), scratch / "built" / f)
    results[("live", f)] = run_tree(scratch / "live" / f, "live", f, layers, "live")
    results[("built", f)] = run_tree(scratch / "built" / f, "built", f, layers, "built")
    # NEGATIVE CONTROL: the built tree with errors.py put back to the blob irpt-narrative staged BEFORE this cell
    oe = scratch / "built_olderrors" / f
    if oe.exists():
        shutil.rmtree(oe)
    shutil.copytree(scratch / "built" / f, oe)
    (oe / "errors.py").write_bytes(old_errors)
    old_err_runs[f] = run_tree(oe, "built_olderrors", f, layers, "olderrors")
    # NEGATIVE CONTROL 2: the built tree with entry.py put back to the bytes BEFORE this cell (no NarrativeEntry)
    pe = scratch / "built_prebinding" / f
    if pe.exists():
        shutil.rmtree(pe)
    shutil.copytree(scratch / "built" / f, pe)
    (pe / "entry.py").write_bytes(pre_entry)
    pre_runs[f] = run_tree(pe, "built_prebinding", f, layers, "prebinding")


def sig(c):
    return (c["reached_firm_check"], tuple(c["roster"]) if c["roster"] is not None else None, c["code"])


def case(side, f, rk, name):
    return results[(side, f)]["routes"][rk]["cases"][name]


routes = [r for r in json.load(open(str(routes_path), encoding="utf-8"))["routes"] if r["handler"] in FUNCS]
per_route = []
for r_ in routes:
    rk, fn = r_["route_key"], r_["handler"]
    row = {"route": rk, "operation": r_["operation"], "function": fn}
    for name in ("userOwn", "userSelOther", "userClaimOther", "rowCotCot", "rowCotInf", "noRow", "svcOther"):
        row[name] = {"built": case("built", fn, rk, name), "live": case("live", fn, rk, name)}
    row["old_errors_py"] = {n: old_err_runs[fn]["routes"][rk]["cases"][n]
                            for n in ("userOwn", "rowCotCot", "noRow")}
    row["pre_binding_entry"] = {n: pre_runs[fn]["routes"][rk]["cases"][n] for n in ("noRow", "rowCotInf")}
    per_route.append(row)
n = len(per_route)


def count(pred):
    return [p for p in per_route if pred(p)]


def rc_(c):
    return (c["reached_firm_check"], c["code"])


own_ok = count(lambda p: p["userOwn"]["built"]["reached_firm_check"] == "cottonwood" and rc_(p["userOwn"]["built"]) == rc_(p["userOwn"]["live"]))
# another firm is never reached: built refuses FIRM_BINDING; the live boundary either refuses the same way or ignores the selection and stays on the caller's own firm
sel_other = count(lambda p: p["userSelOther"]["built"]["code"] == "FIRM_BINDING" and p["userSelOther"]["built"]["roster"] is None
                  and p["userSelOther"]["live"]["reached_firm_check"] != "inflection")
sel_other_same = count(lambda p: sig(p["userSelOther"]["built"]) == sig(p["userSelOther"]["live"]))
claim_other = count(lambda p: p["userClaimOther"]["built"]["code"] == "FIRM_BINDING" and p["userClaimOther"]["built"]["roster"] is None
                    and p["userClaimOther"]["live"]["code"] == "FIRM_BINDING")
row_admit = count(lambda p: p["rowCotCot"]["built"]["reached_firm_check"] == "cottonwood")
row_refuse = count(lambda p: p["rowCotInf"]["built"]["reached_firm_check"] is None and p["rowCotInf"]["built"]["code"] == "FIRM_BINDING")
row_refuse_live = count(lambda p: p["rowCotInf"]["live"]["reached_firm_check"] == "inflection")
norow_same = count(lambda p: sig(p["noRow"]["built"]) == sig(p["noRow"]["live"]) and p["noRow"]["built"]["reached_firm_check"] == "inflection")
svc_never = count(lambda p: "svc-custody-statement" not in (p["svcOther"]["built"]["roster"] or []) and p["svcOther"]["built"]["code"] != "HARNESS_TypeError")
all_cases = [c for p in per_route for k in ("userOwn", "userSelOther", "userClaimOther", "rowCotCot", "rowCotInf", "noRow", "svcOther") for c in (p[k]["built"],)]
harness_codes = sorted({str(c["code"]) for c in all_cases if str(c["code"]).startswith("HARNESS_")})
old_typeerr = count(lambda p: all(str(c["code"]) == "HARNESS_TypeError" for c in p["old_errors_py"].values()))
live_harness = sorted({str(p[k]["live"]["code"]) for p in per_route for k in ("userOwn", "rowCotCot", "noRow") if str(p[k]["live"]["code"]).startswith("HARNESS_")})

arms = []


def arm(name, verdict, detail, neg=False):
    arms.append({"name": name, "verdict": verdict, "negative_control": neg, "detail": detail})


arm("plain firm user (x-firm-id cottonwood), no selection: bound to its OWN firm through the built zip, same (firm, code) as the live zip",
    "identical" if len(own_ok) == n else "UNEXPECTED", "%d of %d routes" % (len(own_ok), n))
arm("plain firm user selecting inflection: refused FIRM_BINDING through the built zip; the live zip never reaches inflection either (another firm is refused)",
    ("identical" if len(sel_other_same) == n else "expected-diff") if len(sel_other) == n else "UNEXPECTED",
    "%d of %d routes refused FIRM_BINDING on built and never reached inflection on live; %d of %d identical built vs live (%s)" % (
        len(sel_other), n, len(sel_other_same), n, "; ".join("%s live=%s/%s" % (p["function"], p["userSelOther"]["live"]["reached_firm_check"], p["userSelOther"]["live"]["code"]) for p in per_route)), True)
arm("plain firm user restating firm_id=inflection in the query: refused FIRM_BINDING through the built zip, same as the live zip",
    "identical" if len(claim_other) == n else "UNEXPECTED", "%d of %d routes" % (len(claim_other), n), True)
arm("internal caller WITH a profile row allowedFirmIds [cottonwood], selecting cottonwood: admitted and bound to cottonwood through the built zip (live ignores the selection)",
    ("identical" if len(row_admit) == n and len(count(lambda p: p["rowCotCot"]["live"]["reached_firm_check"] == "cottonwood")) == n else "expected-diff") if len(row_admit) == n else "UNEXPECTED", "%d of %d routes admitted on built (bound to cottonwood); live bound to cottonwood on %d (live zips: %s)" % (
        len(row_admit), n, len(count(lambda p: p["rowCotCot"]["live"]["reached_firm_check"] == "cottonwood")),
        ", ".join("%s=%s" % (p["function"], p["rowCotCot"]["live"]["reached_firm_check"]) for p in per_route)))
arm("internal caller, row [cottonwood], selecting inflection: refused FIRM_BINDING through the built zip (live: see detail)",
    "expected-diff" if len(row_refuse) == n else "UNEXPECTED", "%d of %d routes refused on built; live bound to inflection on %d (%s)" % (
        len(row_refuse), n, len(row_refuse_live), ", ".join("%s live=%s/%s" % (p["function"], p["rowCotInf"]["live"]["reached_firm_check"], p["rowCotInf"]["live"]["code"]) for p in per_route)), True)
def fc(c):
    return (c["reached_firm_check"], c["code"])


norow_ident = count(lambda p: fc(p["noRow"]["built"]) == fc(p["noRow"]["live"]) and p["noRow"]["built"]["reached_firm_check"] == "opal-capital")
norow_roster = ["%s built=%s live=%s" % (p["function"], p["noRow"]["built"]["roster"], p["noRow"]["live"]["roster"]) for p in per_route]
arm("no_row_internal_selects_other_firm",
    "identical" if len(norow_ident) == n else "UNEXPECTED",
    "an Opal internal caller (x-firm-id opal-capital) with NO profile row selecting inflection, through the REAL entry.ENTRY of each zip: "
    "%d of %d routes bind to the same firm with the same code (built %s, live %s); the Opal roster handed to enforcer_for (recorded, not part of the verdict): %s" % (
        len(norow_ident), n, ", ".join("%s/%s" % fc(p["noRow"]["built"]) for p in per_route),
        ", ".join("%s/%s" % fc(p["noRow"]["live"]) for p in per_route), "; ".join(norow_roster)))
pre_widen = count(lambda p: p["pre_binding_entry"]["noRow"]["reached_firm_check"] == "inflection")
arm("NEGATIVE CONTROL: the same built tree with entry.py put back to its pre-IB-pr-399 bytes binds the no-row internal caller to inflection (the widening this cell removes)",
    "expected-diff" if len(pre_widen) == n else "UNEXPECTED",
    "%d of %d routes bind to inflection without NarrativeEntry (pre-binding entry.py = %s)" % (len(pre_widen), n, PRE_BINDING_PIN[:10]), True)
row_unlisted_ok = count(lambda p: p["pre_binding_entry"]["rowCotInf"]["code"] == "FIRM_BINDING")
arm("a row-listed caller is narrowed identically with and without NarrativeEntry (row [cottonwood] selecting inflection: refused FIRM_BINDING)",
    "identical" if len(row_unlisted_ok) == n and len(row_refuse) == n else "UNEXPECTED",
    "%d of %d routes refused on built and %d of %d on the pre-binding entry" % (len(row_refuse), n, len(row_unlisted_ok), n))
def probe(side_runs, fn, rk):
    return side_runs[fn]["routes"][rk]["error_probe"]


STAGED_KEYS = ["correlation_id", "event", "operation", "public_reason_code"]


def staged_shape(p, op):
    return (p["escaped"] is None and p["ok"] is False and p["code"] == "UNEXPECTED" and not p["has_internal_correlation_id"]
            and len(p["log_events"]) == 1 and sorted(p["log_events"][0]) == STAGED_KEYS
            and p["log_events"][0]["operation"] == op and p["log_events"][0]["public_reason_code"] == "UNEXPECTED")


built_runs = {f: results[("built", f)] for f in FUNCS}
ie_ok = count(lambda p: staged_shape(probe(built_runs, p["function"], p["route"]), p["operation"]))
ie_old = count(lambda p: probe(old_err_runs, p["function"], p["route"])["escaped"] == "TypeError")
arm("internal_error_refusal",
    "identical" if len(ie_ok) == n else "UNEXPECTED",
    "an internal error (the enforcer cannot be built) is recorded and refused through the BUILT zip's real entry.ENTRY: %d of %d routes answer ok=false, public_reason_code UNEXPECTED, "
    "no internal_correlation_id on the wire status, nothing escapes the boundary (no TypeError), and print exactly one irpt_error line of the staged errors.py shape %s; built: %s" % (
        len(ie_ok), n, STAGED_KEYS, "; ".join("%s escaped=%s code=%s log_events=%d" % (p["function"], probe(built_runs, p["function"], p["route"])["escaped"],
                                                    probe(built_runs, p["function"], p["route"])["code"], len(probe(built_runs, p["function"], p["route"])["log_events"])) for p in per_route)))
arm("NEGATIVE CONTROL: internal_error_refusal through the same built tree with errors.py put back to the pre-IB-pr-394 blob (bc3727b3a3): the TypeError escapes the boundary",
    "expected-diff" if len(ie_old) == n else "UNEXPECTED",
    "%d of %d routes: escaped=%s" % (len(ie_old), n, ", ".join(str(probe(old_err_runs, p["function"], p["route"])["escaped"]) for p in per_route)), True)
arm("error path: no case through the built zips raises (no HARNESS_* code), i.e. served._record meets the staged errors.py without TypeError",
    "identical" if not harness_codes else "UNEXPECTED",
    "%d routes x 7 cases each; HARNESS_* codes on built: %s; on live: %s" % (n, harness_codes or "none", live_harness or "none"))
arm("NEGATIVE CONTROL: the same built trees with errors.py put back to the pre-IB-pr-394 narrative blob (bc3727b3a3) raise TypeError on the error path",
    "expected-diff" if len(old_typeerr) == n else "UNEXPECTED",
    "%d of %d routes answer HARNESS_TypeError in all three probed cases" % (len(old_typeerr), n), True)
arm("NEGATIVE CONTROL: svc-custody-statement (cottonwood) on these hosts' operations is never on the Opal roster through the built zip",
    "identical" if len(svc_never) == n else "UNEXPECTED",
    "%d of %d routes: built code %s" % (len(svc_never), n, ", ".join("%s=%s" % (p["function"], p["svcOther"]["built"]["code"]) for p in per_route)), True)

doc = {"pin": pin, "arms": arms, "routes": per_route,
       "harness": "replay/authz_case_runner.py; outcome = (firm_claims_match bound firm, Opal roster handed to enforcer_for, public_reason_code); offline, no AWS write, AWS reads only for the live zips and layers"}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
for a in arms:
    print(a["verdict"], "|", a["name"][:90], "|", a["detail"][:160])
