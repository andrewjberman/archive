"""IB-pr-390 replay driver. From the worktree root, scratch directory OUTSIDE the worktree:
    python replay/run_replay.py <scratch_dir> <pin> <out_replay_json>
<scratch_dir>/zips/<function>.1.zip are the BUILD_ONLY outputs (candidate map); the LIVE zips are read from AWS
(aws lambda get-function, read only) through release-census.py's own fetcher. Everything is extracted into <scratch_dir>
and run with `python -I authz_case_runner.py`. Nothing is written to AWS. ASCII only.
"""
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, out_path = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
FUNCS = ["irpt-49f-reporting-read-lambda", "irpt-directory-search", "irpt-export-render", "irpt-performance-adapter",
         "irpt-status", "irpt-ycharts-generate"]          # the 6 RELEASED hosts (AMENDMENT 1); holdings and narrative are held out
SVC_OPS = {"custody-report-persist", "analysis-requests", "submit-export"}
spec = importlib.util.spec_from_file_location("rc", str(ROOT / "infra/aws/lambda/ci/release-census.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

routes_path = scratch / "routes.json"
routes_path.write_bytes(subprocess.run(["git", "show", "%s:docs/contracts/investor-reporting/v1/routes.json" % pin],
                                       cwd=str(ROOT), capture_output=True, check=True).stdout)


def extract(data, dest):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(str(dest))


def layer_dirs(f):
    """The function's live layers, downloaded (read only) and extracted; -> [<layer>/python, ...] in layer order."""
    cfg = json.loads(subprocess.run(["aws", "lambda", "get-function-configuration", "--function-name", f, "--output", "json"],
                                    capture_output=True, check=True).stdout.decode("utf-8"))
    dirs = []
    for layer in cfg.get("Layers") or []:
        arn = layer["Arn"]
        dest = scratch / "layers" / arn.split(":layer:")[1].replace(":", "_")
        if not dest.exists():
            lv = json.loads(subprocess.run(["aws", "lambda", "get-layer-version-by-arn", "--arn", arn, "--output", "json"],
                                           capture_output=True, check=True).stdout.decode("utf-8"))
            import urllib.request
            with urllib.request.urlopen(lv["Content"]["Location"], timeout=120) as resp:  # noqa: S310 - presigned, read only
                extract(resp.read(), dest)
        dirs.append(str(dest / "python"))
    return dirs


results = {}
for f in FUNCS:
    layers = layer_dirs(f)
    live_zip = rc.fetch_live_zip(ROOT, f)
    extract(live_zip, scratch / "live" / f)
    built_zip = scratch / "zips" / (f + ".1.zip")
    extract(built_zip.read_bytes(), scratch / "built" / f)
    kind = "built"
    for side in ("built", "live"):
        out = scratch / ("case_%s_%s.json" % (side, f))
        r = subprocess.run([sys.executable, "-I", str(HERE / "authz_case_runner.py"), str(scratch / side / f), str(routes_path),
                            side, str(out), f] + layers, capture_output=True, cwd=str(scratch))
        if r.returncode:
            raise SystemExit("runner failed %s %s: %s" % (side, f, r.stderr.decode("utf-8", "replace")[-600:]))
        results[(side, f)] = json.loads(out.read_text(encoding="utf-8"))
        results[(side, f)]["kind"] = kind if side == "built" else "live"

# negative control (d): each svc host's built tree with infra/logic/registry removed from the extracted tree
noreg = {}
for host in ("irpt-export-render", "irpt-ycharts-generate"):
    nr = scratch / ("built_noregistry_" + host)
    if nr.exists():
        shutil.rmtree(nr)
    shutil.copytree(scratch / "built" / host, nr)
    shutil.rmtree(nr / "infra" / "logic" / "registry")
    out = scratch / ("case_noregistry_%s.json" % host)
    r = subprocess.run([sys.executable, "-I", str(HERE / "authz_case_runner.py"), str(nr), str(routes_path), "built_noregistry",
                        str(out), host] + layer_dirs(host), capture_output=True, cwd=str(scratch))
    if r.returncode:
        raise SystemExit("runner failed noregistry: " + r.stderr.decode("utf-8", "replace")[-600:])
    noreg[host] = json.loads(out.read_text(encoding="utf-8"))

# lookup() from the built zip, the way an importer of the zip resolves cottonwood (row D2-S26)
lookups = {}
for f in FUNCS:
    code = ("import sys; sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[1] + '/lib')\n"
            "import opal_naming; v = opal_naming.lookup('cottonwood'); print(v['long'], 'lib/opal_naming.py' if opal_naming.__file__.replace(chr(92), '/').endswith('/lib/opal_naming.py') else 'OTHER')\n")
    r = subprocess.run([sys.executable, "-I", "-c", code, str(scratch / "built" / f)], capture_output=True, cwd=str(scratch))
    lookups[f] = {"rc": r.returncode, "out": r.stdout.decode("utf-8", "replace").strip()[-160:],
                  "err": r.stderr.decode("utf-8", "replace").strip()[-120:]}


svc_lookup_ok = {f for f in FUNCS if str(results[("built", f)]["svc_firm_lookup"]).startswith("cottonwood")}


def sig(c):
    return (c["reached_firm_check"], tuple(c["roster"]) if c["roster"] is not None else None, c["code"])


def svc_admitted(c):
    return bool(c["roster"]) and "svc-custody-statement" in c["roster"]


arms = []
per_route = []
for r_ in json.load(open(routes_path, encoding="utf-8"))["routes"]:
    rk, op, fn = r_["route_key"], r_["operation"], r_["handler"]
    if fn not in FUNCS:
        continue
    b = results[("built", fn)]["routes"][rk]["cases"]
    lv = results[("live", fn)]["routes"][rk]["cases"]
    per_route.append({
        "route": rk, "operation": op, "function": fn, "built_kind": results[("built", fn)]["kind"],
        "internal_row_cottonwood_selecting_cottonwood": {"built": b["rowCotCot"], "live": lv["rowCotCot"]},
        "internal_row_cottonwood_selecting_inflection": {"built": b["rowCotInf"], "live": lv["rowCotInf"]},
        "internal_no_row_selecting_inflection": {"built": b["noRow"], "live": lv["noRow"]},
        "internal_row_ALL_string_selecting_inflection": {"built": b["rowAllStr"], "live": lv["rowAllStr"]},
        "internal_row_ALL_list_selecting_inflection": {"built": b["rowAllList"], "live": lv["rowAllList"]},
        "svc": ({k: {"built": b[k], "live": lv[k]} for k in ("svcCot", "svcInf", "svc49", "svcCotSel")}
                if op in SVC_OPS else {"svcOther": {"built": b["svcOther"], "live": lv["svcOther"]}})})

# the held-out hosts' routes are not replayed (AMENDMENT 1); the packet lists them as NOT YET NARROWED
HELD = {"irpt-holdings", "irpt-narrative"}
held_out_routes = [{"route": r_["route_key"], "operation": r_["operation"], "function": r_["handler"]}
                   for r_ in json.load(open(routes_path, encoding="utf-8"))["routes"] if r_["handler"] in HELD]
defects = []
per_route_all = per_route
n = len(per_route)
ok_narrow_admit = [p for p in per_route if p["internal_row_cottonwood_selecting_cottonwood"]["built"]["reached_firm_check"] == "cottonwood"
                   and p["internal_row_cottonwood_selecting_cottonwood"]["live"]["reached_firm_check"] == "cottonwood"]
ok_narrow_refuse = [p for p in per_route
                    if p["internal_row_cottonwood_selecting_inflection"]["built"]["reached_firm_check"] is None
                    and p["internal_row_cottonwood_selecting_inflection"]["built"]["code"] == "FIRM_BINDING"
                    and p["internal_row_cottonwood_selecting_inflection"]["live"]["reached_firm_check"] == "inflection"]
ok_all = [p for p in per_route if all(p[k]["built"]["reached_firm_check"] is None and p[k]["built"]["code"] == "FIRM_BINDING"
                                      for k in ("internal_row_ALL_string_selecting_inflection", "internal_row_ALL_list_selecting_inflection"))]
ok_norow = [p for p in per_route if sig(p["internal_no_row_selecting_inflection"]["built"]) == sig(p["internal_no_row_selecting_inflection"]["live"])
            and p["internal_no_row_selecting_inflection"]["built"]["reached_firm_check"] == "inflection"]
svc_routes = [p for p in per_route if p["operation"] in SVC_OPS]
ok_svc_admit = [p for p in svc_routes if p["svc"]["svcCot"]["built"]["reached_firm_check"] == "cottonwood" and svc_admitted(p["svc"]["svcCot"]["built"])
                and not svc_admitted(p["svc"]["svcCot"]["live"])]
ok_svc_other = [p for p in svc_routes if all(sig(p["svc"][k]["built"]) == sig(p["svc"][k]["live"]) and not svc_admitted(p["svc"][k]["built"])
                                              for k in ("svcInf", "svc49"))]
ok_svc_sel = [p for p in svc_routes if p["svc"]["svcCotSel"]["built"]["code"] == "FIRM_BINDING" and not svc_admitted(p["svc"]["svcCotSel"]["built"])]
non_svc = [p for p in per_route if p["operation"] not in SVC_OPS]
# a host whose tree cannot resolve the registry (directory-search) does not recognise the subject at all: not admitted, no roster entry
ok_svc_nonlisted = [p for p in non_svc if not svc_admitted(p["svc"]["svcOther"]["built"])
                    and (p["svc"]["svcOther"]["built"]["code"] == "NOT_AUTHORIZED" or p["function"] not in svc_lookup_ok)]
noreg_all = [(rk, v) for doc_ in noreg.values() for rk, v in doc_["routes"].items() if v["operation"] in SVC_OPS]
noreg_ok = [rk for rk, v in noreg_all if not svc_admitted(v["cases"]["svcCot"])]
lookup_ok = {f: v for f, v in lookups.items() if v["rc"] == 0 and v["out"].startswith("cottonwood")}
svc_hosts = {"irpt-export-render", "irpt-ycharts-generate"}

arms.append({"name": "svc-custody-statement admitted on custody-report-persist, analysis-requests, submit-export with a cottonwood claim through the built zip; refused through the live zip",
             "verdict": "expected-diff" if len(ok_svc_admit) == len(svc_routes) == 3 else "UNEXPECTED", "negative_control": False,
             "detail": "%d of %d svc routes: built reached the firm check bound to cottonwood with svc-custody-statement on the Opal roster; live did not put it on the roster. Routes: %s"
                       % (len(ok_svc_admit), len(svc_routes), ", ".join(p["route"] + " (" + p["function"] + ")" for p in svc_routes))})
arms.append({"name": "internal caller, profile row allowedFirmIds [cottonwood], selecting inflection: refused (FIRM_BINDING) through the built zip, admitted through the live zip",
             "verdict": "expected-diff" if len(ok_narrow_refuse) == n else "UNEXPECTED", "negative_control": False,
             "detail": "%d of %d routes (the routes of the 6 released hosts, each through its handler's built zip)" % (len(ok_narrow_refuse), n)})
arms.append({"name": "internal caller, profile row [cottonwood], selecting cottonwood (the admitted half of each narrowing pair): admitted through both zips",
             "verdict": "identical" if len(ok_narrow_admit) == n else "UNEXPECTED", "negative_control": False,
             "detail": "%d of %d routes" % (len(ok_narrow_admit), n)})
arms.append({"name": "AMENDMENT 1 (CTO msg 2569): internal caller whose profile row is the string ALL, or a list holding ALL, selecting inflection: refused FIRM_BINDING through the built zip (never an unrestricted spelling)",
             "verdict": "expected-diff" if len(ok_all) == n else "UNEXPECTED", "negative_control": False,
             "detail": "%d of %d routes, both forms; the live zip's outcome for the same caller is recorded per route in routes[]" % (len(ok_all), n)})
arms.append({"name": "unrelated Opal internal caller with no profile row, selecting inflection: identical through both zips (any-firm reach unchanged)",
             "verdict": "identical" if len(ok_norow) == n else "UNEXPECTED", "negative_control": False,
             "detail": "%d of %d routes, same (firm, roster, code) built and live, bound to inflection" % (len(ok_norow), n)})
arms.append({"name": "NEGATIVE CONTROL: svc-custody-statement with an inflection or 49financial claim is never admitted on the three svc routes, built or live",
             "verdict": "identical" if len(ok_svc_other) == len(svc_routes) else "UNEXPECTED", "negative_control": True,
             "detail": "%d of %d svc routes: svcInf and svc49 identical built vs live and neither on the Opal roster" % (len(ok_svc_other), len(svc_routes))})
arms.append({"name": "NEGATIVE CONTROL: svc-custody-statement (cottonwood) selecting inflection is refused FIRM_BINDING through the built zip (no any-firm selection)",
             "verdict": "expected-diff" if len(ok_svc_sel) == len(svc_routes) else "UNEXPECTED", "negative_control": True,
             "detail": "%d of %d svc routes" % (len(ok_svc_sel), len(svc_routes))})
arms.append({"name": "NEGATIVE CONTROL: svc-custody-statement (cottonwood) on an operation outside its three is refused NOT_AUTHORIZED through the built zip",
             "verdict": "expected-diff" if len(ok_svc_nonlisted) == len(non_svc) else "UNEXPECTED", "negative_control": True,
             "detail": "%d of %d non-svc routes" % (len(ok_svc_nonlisted), len(non_svc))})
arms.append({"name": "NEGATIVE CONTROL: each svc host built tree (export-render, ycharts-generate) with infra/logic/registry removed does not admit svc-custody-statement on any of its three svc routes",
             "verdict": "expected-diff" if len(noreg_ok) == len(noreg_all) == 3 else "UNEXPECTED", "negative_control": True,
             "detail": "%d of %d svc routes (export-render x2, ycharts-generate x1) not admitted with the registry absent (fail closed)" % (len(noreg_ok), len(noreg_all))})
arms.append({"name": "lib/opal_naming.py lookup('cottonwood') resolves from the built zip (row D2-S26)",
             "verdict": "expected-diff" if all(f in lookup_ok for f in svc_hosts) else "UNEXPECTED", "negative_control": False,
             "detail": "resolved from %d of %d built trees: %s; the svc host zips are %s; trees that do not resolve: %s"
                       % (len(lookup_ok), len(lookups), ", ".join(sorted(lookup_ok)), ", ".join(sorted(svc_hosts)),
                          ", ".join(sorted(set(lookups) - set(lookup_ok))) or "none")})
doc = {"pin": pin, "arms": arms, "held_out_routes_not_replayed": held_out_routes, "defects_not_counted_in_arms": defects, "lookup_cottonwood_from_built": lookups, "routes": per_route_all,
       "svc_firm_lookup_through_served": {f: results[("built", f)]["svc_firm_lookup"] for f in FUNCS},
       "built_kinds": {f: results[("built", f)]["kind"] for f in FUNCS},
       "harness": "replay/authz_case_runner.py; outcome = (firm_claims_match bound firm, Opal roster handed to enforcer_for, public_reason_code); offline, no AWS write, AWS reads only for the live zips"}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
for a in arms:
    print(a["verdict"], "|", a["name"][:90], "|", a["detail"][:100])
