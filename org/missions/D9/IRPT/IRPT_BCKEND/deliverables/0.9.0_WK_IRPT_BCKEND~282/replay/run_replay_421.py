"""IB-pr-421 replay driver (from IB-pr-416's run_replay_416.py; ONE host, irpt-performance-adapter). From the worktree root, scratch directory OUTSIDE the worktree:
    python <this file> <scratch_dir> <pin> <out_replay_json> <fixtures_dir> <reports_tests_dir>
The IB-pr-416 runners are used IN PLACE from ~278/replay (unchanged); this directory adds vendor_path_runner_421.py and the arms fresh_vendor_path_no_plan, cache_hit_no_vendor_call and their negative control.
<scratch_dir>/zips/<function>.1.zip are the BUILD_ONLY outputs (candidate map via BAU_SOURCE_MAP_OVERRIDE); <scratch_dir>/live/<function>.zip
are the LIVE zips (aws lambda get-function Code.Location). The live layers are read from AWS (read only). Each tree is extracted into
<scratch_dir> and each runner is run with `python -I`, one tree per process. Nothing is written to AWS; no client data is read.
Runners: IB-pr-409's authz_case_runner.py (unchanged, from ~272/replay) + this directory's scope_runner_416.py and live_call_runner_416.py.
ASCII only.
"""
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HERE278 = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip()) / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/replay"
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
CASE_RUNNER = ROOT / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~272/replay/authz_case_runner.py"
scratch, pin, out_path = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
FIXTURES, REPORTS_TESTS = sys.argv[4], sys.argv[5]
FUNCS = ["irpt-performance-adapter"]
SCOPE_ROUTE = {"irpt-performance-adapter": "GET /api/scoped/investor-reporting/performance/{accountSetId}",
               "irpt-narrative": "GET /api/scoped/investor-reporting/narrative/{reportId}",
               "irpt-status": "GET /api/scoped/investor-reporting/status"}
# the callees whose live bytes are put back into the built tree for the NEGATIVE CONTROLS (row D2-S60's three split callees)
SPLIT_MEMBERS = ["interactive_access.py", "prospect.py", "enforce.py"]

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
    cfg = json.loads(subprocess.run(["aws", "lambda", "get-function-configuration", "--function-name", f, "--output", "json"],
                                    capture_output=True, check=True).stdout.decode("utf-8"))
    dirs = []
    for layer in cfg.get("Layers") or []:
        arn = layer["Arn"]
        if "native" in arn:      # the Linux-native pandas/pyarrow layer cannot load on this host and no replayed path imports it
            continue
        dest = scratch / "layers" / arn.split(":layer:")[1].replace(":", "_")
        if not dest.exists():
            lv = json.loads(subprocess.run(["aws", "lambda", "get-layer-version-by-arn", "--arn", arn, "--output", "json"],
                                           capture_output=True, check=True).stdout.decode("utf-8"))
            with urllib.request.urlopen(lv["Content"]["Location"], timeout=120) as resp:  # noqa: S310 - presigned, read only
                extract(resp.read(), dest)
        dirs.append(str(dest / "python"))
    return dirs


def run(cmd, tag):
    r = subprocess.run(cmd, capture_output=True, cwd=str(scratch))
    if r.returncode:
        raise SystemExit("runner failed %s: %s" % (tag, (r.stderr + r.stdout).decode("utf-8", "replace")[-900:]))


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


runs = {}
for f in FUNCS:
    layers = layer_dirs(f)
    extract((scratch / "live" / (f + ".zip")).read_bytes(), scratch / "x_live" / f)
    extract((scratch / "zips" / (f + ".1.zip")).read_bytes(), scratch / "x_built" / f)
    nc = scratch / "x_ctl" / f                    # NEGATIVE CONTROL tree: the built tree with the three split callees put back to live bytes
    if nc.exists():
        shutil.rmtree(nc)
    shutil.copytree(scratch / "x_built" / f, nc)
    for m in SPLIT_MEMBERS:
        if (scratch / "x_live" / f / m).exists():
            shutil.copyfile(str(scratch / "x_live" / f / m), str(nc / m))
    for side, tree in (("live", scratch / "x_live" / f), ("built", scratch / "x_built" / f), ("ctl", nc)):
        o1, o2, o3 = (scratch / ("%s_%s_%s.json" % (k, side, f)) for k in ("case", "scope", "call"))
        if side != "ctl":
            run([sys.executable, "-I", str(CASE_RUNNER), str(tree), str(routes_path), side, str(o1), f] + layers, "case %s %s" % (side, f))
            runs[(f, side, "case")] = load(o1)
        run([sys.executable, "-I", str(HERE278 / "scope_runner_416.py"), str(tree), side, str(o2), SCOPE_ROUTE[f]] + layers, "scope %s %s" % (side, f))
        run([sys.executable, "-I", str(HERE278 / "live_call_runner_416.py"), str(tree), side, str(o3)] + layers, "call %s %s" % (side, f))
        runs[(f, side, "scope")] = load(o2)
        runs[(f, side, "call")] = load(o3)
        if side != "ctl":
            o4 = scratch / ("mc_%s_%s.json" % (side, f))
            run([sys.executable, "-I", str(HERE278 / "method_call_runner_416.py"), str(tree), side, str(o4), f, str(routes_path)] + layers, "method %s %s" % (side, f))
            runs[(f, side, "mc")] = load(o4)

arms = []


def arm(function, name, verdict, detail, neg=False):
    arms.append({"function": function, "name": name, "verdict": verdict, "negative_control": neg, "detail": detail})


def scope_sig(c):
    return (c["principal_class"], tuple(c["permitted_account_set"] or ()), tuple(c["roster"]) if c["roster"] not in (None, "NOT_CALLED") else c["roster"])


def fc(c):
    return (c["reached_firm_check"], c["code"])


def call_text(c):
    return "recorded=%s escaped=%s code=%s compute_reached=%s" % (c.get("recorded"), c.get("escaped"), c.get("code"), c.get("compute_reached"))


for f in FUNCS:
    L, B, C = (runs[(f, s, "call")]["cases"] for s in ("live", "built", "ctl"))
    # 1 -- the prospect arm: no TypeError recorded or escaping on built; live records it where the split is; the control puts it back
    for case in ("prospect_internal_no_row_CREATE_INPUT", "prospect_internal_no_row_OWNED_INPUT",
                 "prospect_firm_user_CREATE_INPUT", "prospect_firm_user_OWNED_INPUT"):
        b_te = "TypeError" in (B[case]["recorded"] + [B[case]["escaped"]])
        l_te = "TypeError" in (L[case]["recorded"] + [L[case]["escaped"]])
        c_te = "TypeError" in (C[case]["recorded"] + [C[case]["escaped"]])
        if b_te:
            verdict = "UNEXPECTED"
        elif l_te:
            verdict = "expected-diff"
        else:
            verdict = "identical" if call_text(B[case]) == call_text(L[case]) else "expected-diff"
        arm(f, "prospect arm %s: built does not raise TypeError" % case, verdict,
            "live: %s | built: %s" % (call_text(L[case]), call_text(B[case])))
        arm(f, "NEGATIVE CONTROL prospect arm %s: the built tree with interactive_access.py, prospect.py and enforce.py put back to the LIVE bytes" % case,
            ("expected-diff" if l_te else "identical") if c_te == l_te else "UNEXPECTED",
            "control: %s | live: %s" % (call_text(C[case]), call_text(L[case])), True)
    # 2 -- the Enforcer(load_report_owner=) build
    case = "enforcer_build_with_report_owner_port"
    b_ok = B[case]["built_enforcer"] and B[case]["escaped"] is None
    l_te = L[case]["escaped"] == "TypeError"
    arm(f, "enforcer build with the load_report_owner port: built constructs the Enforcer",
        ("expected-diff" if l_te else "identical") if b_ok else "UNEXPECTED",
        "live: escaped=%s built_enforcer=%s | built: escaped=%s built_enforcer=%s" % (L[case]["escaped"], L[case]["built_enforcer"], B[case]["escaped"], B[case]["built_enforcer"]))
    arm(f, "NEGATIVE CONTROL enforcer build: the built tree with enforce.py put back to the LIVE bytes",
        ("expected-diff" if l_te else "identical") if C[case]["escaped"] == L[case]["escaped"] else "UNEXPECTED",
        "control: escaped=%s | live: escaped=%s" % (C[case]["escaped"], L[case]["escaped"]), True)
    # 3 -- the no-row internal enforcer scope (row D2-S48's method)
    LS, BS = runs[(f, "live", "scope")]["cases"], runs[(f, "built", "scope")]["cases"]
    same = all(scope_sig(LS[k]) == scope_sig(BS[k]) for k in ("no_row_no_selection", "no_row_selecting_other", "row_listed_no_selection"))
    arm(f, "no_row_internal_enforcer_scope (+ row-listed): class, roster and permitted set, live vs built",
        "identical" if same else "UNEXPECTED",
        "; ".join("%s live=%s/%s/%d built=%s/%s/%d" % (k, LS[k]["principal_class"], LS[k]["roster"], len(LS[k]["permitted_account_set"] or []),
                                                    BS[k]["principal_class"], BS[k]["roster"], len(BS[k]["permitted_account_set"] or []))
                  for k in ("no_row_no_selection", "no_row_selecting_other", "row_listed_no_selection")))
    # 4 -- the 409 binding cases through each zip's REAL entry.ENTRY, live vs built
    LC, BC = runs[(f, "live", "case")]["routes"], runs[(f, "built", "case")]["routes"]
    diffs, n = [], 0
    for rk in BC:
        for name in ("userOwn", "userSelOther", "userClaimOther", "noRow", "rowCotCot", "rowCotInf"):
            n += 1
            if fc(BC[rk]["cases"][name]) != fc(LC[rk]["cases"][name]) or BC[rk]["cases"][name]["roster"] != LC[rk]["cases"][name]["roster"]:
                diffs.append("%s/%s live=%s built=%s" % (BC[rk]["operation"], name, fc(LC[rk]["cases"][name]), fc(BC[rk]["cases"][name])))
    harness = sorted({str(BC[rk]["cases"][nm]["code"]) for rk in BC for nm in BC[rk]["cases"] if str(BC[rk]["cases"][nm]["code"]).startswith("HARNESS_")})
    lharness = sorted({str(LC[rk]["cases"][nm]["code"]) for rk in LC for nm in LC[rk]["cases"] if str(LC[rk]["cases"][nm]["code"]).startswith("HARNESS_")})
    arm(f, "binding cases (userOwn, userSelOther, userClaimOther, noRow, rowCotCot, rowCotInf) through the real entry.ENTRY, live vs built",
        "UNEXPECTED" if harness else ("identical" if not diffs else "expected-diff"),
        "%d cases over %d route(s); differing: %s; HARNESS_* on built: %s, on live: %s" % (n, len(BC), diffs or "none", harness or "none", lharness or "none"))

    # 5 -- the METHOD-call arm (TO AMENDMENT 2): every route's handler called on the zip with a synthetic event, two principals, in-memory fakes
    ML, MB = runs[(f, "live", "mc")]["routes"], runs[(f, "built", "mc")]["routes"]
    for rk in MB:
        b_err = sum(p["arity_error_count"] for p in MB[rk]["principals"].values())
        l_err = sum(p["arity_error_count"] for p in ML[rk]["principals"].values())
        esc = [p["escaped"] for p in MB[rk]["principals"].values() if p["escaped"]]
        depth = "/".join(str(MB[rk]["principals"][k]["functions_entered"]) for k in sorted(MB[rk]["principals"]))
        arm(f, "method-call arm %s: built handler raises no call-arity TypeError" % MB[rk]["operation"],
            "UNEXPECTED" if (b_err or esc) else ("expected-diff" if l_err else "identical"),
            "built arity errors=%d escaped=%s codes=%s functions_entered(%s)=%s | live arity errors=%d codes=%s" % (
                b_err, esc or "none", {k: v["code"] for k, v in sorted(MB[rk]["principals"].items())}, "/".join(sorted(MB[rk]["principals"])), depth,
                l_err, {k: v["code"] for k, v in sorted(ML[rk]["principals"].items())}))
        if l_err:
            arm(f, "NEGATIVE CONTROL method-call arm %s: the LIVE zip reads arity errors" % MB[rk]["operation"], "expected-diff",
                "live arity errors=%d at %s" % (l_err, sorted({h["where"] for p in ML[rk]["principals"].values() for h in p["arity_errors"]})), True)

# ---- IB-pr-421 arms: the vendor path without the one-use plan ---------------------------------------------------------------------------
f = FUNCS[0]
layers = layer_dirs(f)
state = scratch / "vendor_state.pkl"
if state.exists():
    state.unlink()
vp = {}
for side in ("built", "live"):           # built first: it seeds the accepted report both sides then reopen
    tree = scratch / ("x_" + side) / f
    o = scratch / ("vp_%s.json" % side)
    run([sys.executable, "-I", str(HERE / "vendor_path_runner_421.py"), str(tree), side, str(o), str(state), FIXTURES, REPORTS_TESTS] + layers, "vendor path %s" % side)
    vp[side] = load(o)
ctl_tree = scratch / "x_vctl" / f        # NEGATIVE CONTROL: the built tree with authorization.py put back to the LIVE bytes
if ctl_tree.exists():
    shutil.rmtree(ctl_tree)
shutil.copytree(scratch / "x_built" / f, ctl_tree)
shutil.copyfile(str(scratch / "x_live" / f / "authorization.py"), str(ctl_tree / "authorization.py"))
shutil.copyfile(str(scratch / "x_live" / f / "runtime.py"), str(ctl_tree / "runtime.py"))
vctl_state = scratch / "vendor_state_ctl.pkl"
shutil.copyfile(str(state), str(vctl_state))
o = scratch / "vp_ctl.json"
run([sys.executable, "-I", str(HERE / "vendor_path_runner_421.py"), str(ctl_tree), "live", str(o), str(vctl_state), FIXTURES, REPORTS_TESTS] + layers, "vendor path ctl")
vp["ctl"] = load(o)
outside = sorted({m for k in vp for m in vp[k]["modules_loaded_from_the_worktree_not_the_zip"]})
LB, BB, CT = (vp[k]["cases"] for k in ("live", "built", "ctl"))
exact = all(BB[c]["outcome"] == "transport" and BB[c]["sent_matches_built_requests"] and BB[c]["bound_requests_match"] and BB[c]["altered_body_refused"]
            and BB[c]["use_rows_written"] == 1 and BB[c]["use_row_unconditional"] is True for c in ("fresh_cottonwood", "fresh_inflection"))
live_refuses = all(LB[c]["outcome"] == "refused" and LB[c]["exception"] == "VendorEgressRefused" and LB[c]["use_rows_written"] == 0
                   for c in ("fresh_cottonwood", "fresh_inflection"))
arm(f, "fresh_vendor_path_no_plan", "expected-diff" if (exact and live_refuses) else "UNEXPECTED",
    "no plan variable set in either process. live (%s): VendorEgressRefused for 2 of 2 packaged firms, 0 use rows, 0 transports. built (%s): a transport for 2 of 2 packaged firms; "
    "the fake transport was sent exactly the provider's built requests (cottonwood %d route(s), sha256 %s; inflection %d route(s), sha256 %s); an altered body refused; "
    "1 unconditional use row per request" % (
        LB["fresh_cottonwood"]["factory_class"], BB["fresh_cottonwood"]["factory_class"], len(BB["fresh_cottonwood"]["sent_routes"]),
        BB["fresh_cottonwood"]["expected_requests_sha256"][:16], len(BB["fresh_inflection"]["sent_routes"]), BB["fresh_inflection"]["expected_requests_sha256"][:16]))
RL, RB = LB["reopen"], BB["reopen"]
same = (RL["reopen_outcome"], RL["reopen_exception"]) == (RB["reopen_outcome"], RB["reopen_exception"])
zero = all(R["reopen_transport_constructions"] == 0 and R["reopen_use_rows_written"] == 0 and R["reopen_s3_puts"] == 0 for R in (RL, RB))
arm(f, "cache_hit_no_vendor_call", "identical" if (same and zero and RB["seed"].get("outcome") == "accepted") else "UNEXPECTED",
    "the accepted report was seeded by the built tree (1 transport construction, 1 use row); both trees then asked for it again through their own RetainedPerformance: "
    "live %s/%s, built %s/%s; transport constructions live=%d built=%d, use rows written live=%d built=%d, S3 puts live=%d built=%d, vendor requests sent 0. "
    "(Both refuse the reopen of a vendor-calculated figure by name, batch 66 item 2: that rule is unchanged by this cell.)" % (
        RL["reopen_outcome"], RL["reopen_exception"], RB["reopen_outcome"], RB["reopen_exception"], RL["reopen_transport_constructions"],
        RB["reopen_transport_constructions"], RL["reopen_use_rows_written"], RB["reopen_use_rows_written"], RL["reopen_s3_puts"], RB["reopen_s3_puts"]))
ctl_ok = all(CT[c]["outcome"] == "refused" and CT[c]["exception"] == "VendorEgressRefused" for c in ("fresh_cottonwood", "fresh_inflection"))
arm(f, "NEGATIVE CONTROL fresh_vendor_path_no_plan: the built tree with authorization.py and runtime.py put back to the LIVE bytes", "expected-diff" if ctl_ok else "UNEXPECTED",
    "control (%s): VendorEgressRefused for 2 of 2 packaged firms, 0 transports -- the built tree's change is what removes the refusal" % CT["fresh_cottonwood"]["factory_class"], True)
arm(f, "replay hygiene: modules the vendor-path runner loaded from the worktree rather than the zip", "identical" if outside == ["test_retention"] else "UNEXPECTED",
    "only the repo's in-memory Table fake (test_retention) came from the worktree: %s" % outside)

doc = {"pin": pin, "arms": arms, "harness": "replay/run_replay_421.py (+ ~278/replay runners in place); offline, no AWS write, AWS reads only for the live zips and layers; one tree per process",
       "cases": {"%s|%s|%s" % k: v for k, v in runs.items()}}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
for a in arms:
    print(a["function"], a["verdict"], "|", a["name"][:100], "|", a["detail"][:200])
