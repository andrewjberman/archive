"""IB-pr-426 replay driver: irpt-ycharts-generate, LIVE package against the BUILT package, offline. From the worktree root:
    python <this file> <scratch_dir> <pin> <out_replay_json> [--tests-from <dir of earlier test-result json>]
<scratch_dir> (OUTSIDE the worktree) holds zips/irpt-ycharts-generate.1.zip (BUILD_ONLY output) and live/irpt-ycharts-generate.zip (the live
package). Each zip is extracted into <scratch>/r426/ and each probe runs with `python -I`, one tree per process, with boto3 replaced by an
in-memory fake and every socket connect refused. NO AWS call is made by this driver; no client data is read; every id is synthetic.
Evidence kinds, all in this directory: generate_probe_426 (every route of the Entry through the real generate_installed.build_boundary, the
packaged registry, loaders, svc subject), pair_probe_426 (acceptance + submission_service), resident_probe_426 (durable_job, resident_worker,
resident_main), schema_probe_426 (the packaged contracts), sites_probe_426 (the four carried method-call sites), the 409 binding-case runner
(~272/replay/authz_case_runner.py, unchanged), and the repository's own pin test files run against each zip's modules (mkmirror_426 +
runtests_426; PyMuPDF is not on this box, stubs/fitz.py lets test modules import, a test that needs a real PDF fails on both trees).
NEGATIVE CONTROLS put ONE member of the built tree back to its LIVE bytes (or corrupt a file) and show the behaviour reverts. ASCII only.
"""
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, out_path = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
TESTS_FROM = Path(sys.argv[sys.argv.index("--tests-from") + 1]) if "--tests-from" in sys.argv else None
FN = "irpt-ycharts-generate"
CASE_RUNNER = ROOT / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~272/replay/authz_case_runner.py"
W = scratch / "r426"
OUT = W / "out"
if W.exists():
    shutil.rmtree(W)
OUT.mkdir(parents=True)
(W / "routes.json").write_bytes(subprocess.run(["git", "show", "%s:docs/contracts/investor-reporting/v1/routes.json" % pin], cwd=str(ROOT),
                                                 capture_output=True, check=True).stdout)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def py(script, *args, ok=True):
    r = subprocess.run([sys.executable, "-I", str(script)] + [str(a) for a in args], cwd=str(W), capture_output=True, env=dict(os.environ, IB426_ROOT=str(ROOT)))
    if ok and r.returncode:
        raise SystemExit("FAILED %s %s: %s" % (script, args, (r.stderr + r.stdout).decode("utf-8", "replace")[-700:]))
    return r


# ---- trees
def extract(zip_path, dest):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)


extract(scratch / "live" / (FN + ".zip"), W / "x_live")
extract(scratch / "zips" / (FN + ".1.zip"), W / "x_built")


def control(name, members=(), corrupt=()):
    d = W / name
    shutil.copytree(W / "x_built", d)
    for m in members:
        shutil.copyfile(str(W / "x_live" / m), str(d / m))
    for m in corrupt:
        (d / m).write_text("{ not json", encoding="utf-8")
    return d


CTL = {"ctl_pair_a": control("ctl_pair_a", ["submission_service.py"]), "ctl_pair_b": control("ctl_pair_b", ["acceptance.py"]),
       "ctl_served": control("ctl_served", ["served.py"]), "ctl_loaders": control("ctl_loaders", ["loaders.py"]),
       "ctl_policies": control("ctl_policies", ["infra/logic/registry/reporting_policies.json"]),
       "ctl_firmreg": control("ctl_firmreg", ["firm_registry.json"]), "ctl_durable": control("ctl_durable", ["durable_job.py"]),
       "ctl_main": control("ctl_main", ["resident_main.py"])}
CORRUPT = {"c_exemptions": "infra/logic/registry/exemptions.json", "c_resources": "infra/logic/registry/resources.json",
           "c_systems": "infra/logic/registry/systems.json", "c_scopes": "infra/logic/registry/scopes.json",
           "c_naming_schema": "org/standards/NAMING_SCHEMA.json"}
for k, m in CORRUPT.items():
    CTL[k] = control(k, corrupt=[m])
TREES = {"live": W / "x_live", "built": W / "x_built", **CTL}

# ---- probes
probe, pair, resident, schema, sites = {}, {}, {}, {}, {}
for k, t in TREES.items():
    r = py(HERE / "generate_probe_426.py", t, k, OUT / ("probe_%s.json" % k), ok=False)
    probe[k] = load(OUT / ("probe_%s.json" % k)) if r.returncode == 0 else {"crashed": True, "error": (r.stderr.decode("utf-8", "replace").strip().splitlines() or ["?"])[-1][:160]}
for k in ("live", "built", "ctl_pair_a", "ctl_pair_b"):
    py(HERE / "pair_probe_426.py", TREES[k], k, OUT / ("pair_%s.json" % k))
    pair[k] = load(OUT / ("pair_%s.json" % k))
for k in ("live", "built", "ctl_durable", "ctl_main"):
    py(HERE / "resident_probe_426.py", TREES[k], k, OUT / ("resident_%s.json" % k))
    resident[k] = load(OUT / ("resident_%s.json" % k))
for k in ("live", "built"):
    py(HERE / "schema_probe_426.py", TREES[k], k, OUT / ("schema_%s.json" % k))
    schema[k] = load(OUT / ("schema_%s.json" % k))
    py(HERE / "sites_probe_426.py", TREES[k], k, OUT / ("sites_%s.json" % k))
    sites[k] = load(OUT / ("sites_%s.json" % k))
cases = {}
for k in ("live", "built"):
    py(CASE_RUNNER, TREES[k], W / "routes.json", k, OUT / ("case_%s.json" % k), FN)
    cases[k] = load(OUT / ("case_%s.json" % k))

# ---- the repository's own pin tests against each tree's modules
TEST_DIRS = ["ycharts/generate", "ops", "reports", "_authz", "_ids", "intake"]


def run_tests(tree, tag, dirs_files, mirror_tag):
    """dirs_files: {reldir: [test file names]} -> {reldir: result json}"""
    mirror = W / ("n_" + mirror_tag)
    py(HERE / "mkmirror_426.py", tree, mirror, pin)
    res = {}
    for d, files in dirs_files.items():
        o = OUT / ("tests_%s_%s.json" % (tag, d.replace("/", "_")))
        py(HERE / "runtests_426.py", mirror, d, o, *files)
        res[d] = load(o)
    shutil.rmtree(mirror)
    return res


tests = {"live": {}, "built": {}}
if TESTS_FROM is not None:
    for side in ("live", "built"):
        for d in TEST_DIRS:
            tests[side][d] = load(TESTS_FROM / ("all3_%s_%s.json" % (side, d.replace("/", "_"))))
else:
    for side in ("live", "built"):
        mirror = W / ("n_all_" + side)
        py(HERE / "mkmirror_426.py", TREES[side], mirror, pin)
        for d in TEST_DIRS:
            tdir = mirror / "infra/aws/lambda/investor-reporting" / d / "tests"
            files = sorted(p.name for p in tdir.glob("test_*.py")) if tdir.is_dir() else []
            if not files:
                continue
            o = OUT / ("tests_%s_%s.json" % (side, d.replace("/", "_")))
            py(HERE / "runtests_426.py", mirror, d, o, *files)
            tests[side][d] = load(o)
        shutil.rmtree(mirror)

# test-arm configuration: (arm name, reldir, test files, members the arm exercises, tree-control members)
TEST_ARMS = [
    ("pin test file test_acceptance_actor.py (acceptance actor recorded; the service passes it)", "ycharts/generate", ["test_acceptance_actor.py"],
     ["acceptance.py", "submission_service.py"], ["acceptance.py", "submission_service.py"]),
    ("pin test files for the owned-request history (rows state client_id and client_claim, whole-history newest-first read)", "ops",
     ["test_history_row_client.py", "test_history_pool.py", "test_history_client_scope.py", "test_owned_requests.py"],
     ["owned_requests.py"], ["owned_requests.py"]),
    ("pin test files for the named service subjects in the retained repository and retention (svc-commentary draft store)", "reports",
     ["test_svc_commentary.py", "test_commentary_draft_store.py"], ["repository.py", "retention.py"], ["repository.py", "retention.py"]),
    ("pin test file test_svc_custody_statement.py (the svc-custody-statement subject's operations)", "_authz", ["test_svc_custody_statement.py"],
     ["served.py"], ["served.py"]),
    ("pin test files for the id projection and the bundled custodian-key seam (None-like strings are unmapped)", "_ids",
     ["test_seam_none_strings.py", "test_ids.py"], ["ids.py", "data/custodian_key_seam.json"], ["ids.py", "data/custodian_key_seam.json"]),
    ("pin test file test_package_poll.py (the commentary_ready poll)", "ycharts/generate", ["test_package_poll.py"],
     ["resident_worker.py"], ["resident_worker.py"]),
]


def passed(res, d, files):
    out = {}
    for k, v in res[d]["results"].items():
        if any(k.startswith("tests/" + f) for f in files):
            out[k] = v
    return out


arms = []


def arm(name, verdict, detail, members=(), neg=False):
    arms.append({"name": name, "verdict": verdict, "negative_control": neg, "members": list(members), "detail": detail})


def sdiff(a, b, path=""):
    """paths whose values differ between two nested dicts (a key on one side only counts)"""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k == "label":
                continue
            if k not in a or k not in b:
                out.append(path + "/" + k)
            else:
                out += sdiff(a[k], b[k], path + "/" + k)
    elif a != b:
        out.append(path)
    return out


PL, PB = probe["live"], probe["built"]

# 1 -- composition
d = sdiff(PL["composition"], PB["composition"])
expected = {"/ingestion_revision"} | {"/schema_sha256/" + n + ".schema.json" for n in ("AnalysisReport", "ExportReceipt", "HoldingsSnapshot", "OwnedAnalysisRequest", "OwnedAnalysisRequestHistory")}
dest_same = PL["composition"]["destination_revision"] == PB["composition"]["destination_revision"]
arm("composition: generate_installed.compose_ports over in-memory clients, live vs built",
    "expected-diff" if set(d) == expected and dest_same else "UNEXPECTED",
    "ingestion_revision (a digest over the packaged contracts/ directory) moves: live %s built %s; the five changed schemas are the only differing files (%s). destination_revision (the X10 policy digest) IDENTICAL %s; declared routes IDENTICAL %s (%d: %s); composed ports IDENTICAL, absent producers IDENTICAL %s. Every request accepted after a deploy carries the new ingestion_gate_revision." % (
        PL["composition"]["ingestion_revision"][:20], PB["composition"]["ingestion_revision"][:20], ", ".join(sorted(x.split("/")[-1][:-12] for x in d if "schema_sha256" in x)),
        PB["composition"]["destination_revision"][:16], PL["composition"]["declared_routes"] == PB["composition"]["declared_routes"], len(PB["composition"]["declared_routes"]),
        "; ".join(PB["composition"]["declared_routes"]), PL["composition"]["absent_producers"]),
    ["contracts/AnalysisReport.schema.json", "contracts/ExportReceipt.schema.json", "contracts/HoldingsSnapshot.schema.json",
     "contracts/OwnedAnalysisRequest.schema.json", "contracts/OwnedAnalysisRequestHistory.schema.json"])

# 2 -- schemas as packaged
SL, SB = schema["live"], schema["built"]
exp = (SL["history_new_shape"], SB["history_new_shape"]) == ("invalid", "valid") and (SL["history_legacy_shape"], SB["history_legacy_shape"]) == ("valid", "invalid") \
    and SB["analysis_report_retained_ref"] == "valid" and SL["analysis_report_retained_ref"].startswith("unresolvable") \
    and (SL["holdings_asset_class_multi_asset"], SB["holdings_asset_class_multi_asset"]) == ("valid", "invalid") \
    and SL["holdings_asset_class_equity"] == SB["holdings_asset_class_equity"] == "valid" \
    and SB["export_receipt_covered_account_ids"] == "valid" and "covered_account_ids" in SB["export_receipt_facts_required"] \
    and "covered_account_ids" not in SL["export_receipt_facts_required"] and SB["owned_request_persist_inputs"] == "valid" \
    and SL["owned_request_persist_inputs"].startswith("unresolvable")
arm("contract schemas as the zip carries them (contracts/), synthetic documents, live vs built",
    "expected-diff" if exp else "UNEXPECTED",
    "history: the new row shape (client_id, client_claim, unreadable_rows) live=%s built=%s; the legacy shape live=%s built=%s. AnalysisReport.retained_ref: live=%s built=%s. "
    "OwnedAnalysisRequest.persist_inputs: live=%s built=%s. ExportReceipt facts.covered_account_ids: live=%s built=%s, and it becomes REQUIRED in facts (%s). "
    "HoldingsSnapshot asset_class 'multi_asset' (five enum nodes lose that value): live=%s built=%s; 'equity' live=%s built=%s." % (
        SL["history_new_shape"], SB["history_new_shape"], SL["history_legacy_shape"], SB["history_legacy_shape"], SL["analysis_report_retained_ref"], SB["analysis_report_retained_ref"],
        SL["owned_request_persist_inputs"], SB["owned_request_persist_inputs"], SL["export_receipt_covered_account_ids"], SB["export_receipt_covered_account_ids"],
        SB["export_receipt_facts_required"], SL["holdings_asset_class_multi_asset"], SB["holdings_asset_class_multi_asset"],
        SL["holdings_asset_class_equity"], SB["holdings_asset_class_equity"]),
    ["contracts/AnalysisReport.schema.json", "contracts/ExportReceipt.schema.json", "contracts/HoldingsSnapshot.schema.json",
     "contracts/OwnedAnalysisRequest.schema.json", "contracts/OwnedAnalysisRequestHistory.schema.json"])

# 3 -- the packaged registry as the function reads it
nd = sdiff({"naming": PL["naming"], "addresses": PL["addresses"]}, {"naming": PB["naming"], "addresses": PB["addresses"]})
def allowed(p):
    return (p.startswith("/naming/policies/irpt-anlreq-x10-v1") or p in ("/naming/policies/irpt-ycdgen-research-v1/firms", "/naming/policies/irpt-ycdgen-research-v1/policy_sha256")
                     or p.startswith("/naming/destinations/irpt-anlreq-x10-v1|") or p.startswith("/naming/destinations/irpt-ycdgen-research-v1|")
                     or p == "/naming/lookups/4698" or p == "/naming/registry_files_loaded")
unexpected = [p for p in nd if not allowed(p)]
x10 = "irpt-x10-v1"
x10_same = PL["naming"]["policies"][x10] == PB["naming"]["policies"][x10] and all(
    PL["naming"]["destinations"][k] == PB["naming"]["destinations"][k] for k in PL["naming"]["destinations"] if k.startswith(x10 + "|"))
arm("packaged registry as the function reads it: reporting_policy / reporting_destination / lookup / HoldingsPublication address, every policy revision, live vs built",
    "expected-diff" if not unexpected and x10_same and PL["addresses"] == PB["addresses"] else "UNEXPECTED",
    "differences are only: the new ACTIVE policy irpt-anlreq-x10-v1 (family ANALYSIS_COMMENTARY, firms %s) with its destinations; irpt-ycdgen-research-v1 firms widened %s -> %s (policy_sha256 %s -> %s, so 49financial and inflection destinations for its three families become writable); lookup('4698') resolves a MASTER row on built and raises on live. "
    "IDENTICAL: the X10 policy irpt-x10-v1 (policy_sha256 %s, every destination: %s), the other policies, %d holdings addresses (%s), lookups of the four firms. Unexpected differing paths: %s." % (
        PB["naming"]["policies"]["irpt-anlreq-x10-v1"]["firms"], PL["naming"]["policies"]["irpt-ycdgen-research-v1"]["firms"], PB["naming"]["policies"]["irpt-ycdgen-research-v1"]["firms"],
        PL["naming"]["policies"]["irpt-ycdgen-research-v1"]["policy_sha256"][:12], PB["naming"]["policies"]["irpt-ycdgen-research-v1"]["policy_sha256"][:12],
        PB["naming"]["policies"][x10]["policy_sha256"][:12], x10_same, len(PB["addresses"]), PL["addresses"] == PB["addresses"], unexpected or "none"),
    ["lib/opal_naming.py", "infra/logic/registry/reporting_policies.json", "infra/logic/registry/scopes.json", "infra/logic/registry/systems.json",
     "infra/logic/registry/exemptions.json", "infra/logic/registry/resources.json", "org/standards/NAMING_SCHEMA.json"])
PP = probe["ctl_policies"]
arm("NEGATIVE CONTROL registry: the built tree with reporting_policies.json put back to the LIVE bytes",
    "expected-diff" if PP["naming"]["policies"]["irpt-ycdgen-research-v1"] == PL["naming"]["policies"]["irpt-ycdgen-research-v1"] and "irpt-anlreq-x10-v1" not in PP["naming"]["policies"] else "UNEXPECTED",
    "control: irpt-ycdgen-research-v1 firms %s and policy_sha256 %s (the live values) and no irpt-anlreq-x10-v1 policy -- the policy file is what moves them." % (
        PP["naming"]["policies"]["irpt-ycdgen-research-v1"]["firms"], PP["naming"]["policies"]["irpt-ycdgen-research-v1"]["policy_sha256"][:12]),
    ["infra/logic/registry/reporting_policies.json"], True)
cor = {k: probe[k] for k in CORRUPT}
read_ok = all(cor[k].get("crashed") for k in ("c_exemptions", "c_resources", "c_systems", "c_scopes")) and all(
    str(v).startswith("ERR:") for v in cor["c_naming_schema"]["addresses"].values())
arm("NEGATIVE CONTROL runtime read: each of exemptions.json, resources.json, systems.json, scopes.json and NAMING_SCHEMA.json replaced by invalid JSON in the built tree",
    "expected-diff" if read_ok else "UNEXPECTED",
    "composition/naming raised for exemptions, resources, systems and scopes (%s); every holdings address raised for NAMING_SCHEMA.json (%d of %d) -- the function reads each file at runtime, so each is served." % (
        "; ".join("%s: %s" % (k, cor[k].get("error", "")[:60]) for k in ("c_exemptions", "c_resources", "c_systems", "c_scopes")),
        sum(str(v).startswith("ERR:") for v in cor["c_naming_schema"]["addresses"].values()), len(cor["c_naming_schema"]["addresses"])),
    ["infra/logic/registry/exemptions.json", "infra/logic/registry/resources.json", "infra/logic/registry/systems.json",
     "infra/logic/registry/scopes.json", "org/standards/NAMING_SCHEMA.json"], True)
FR = probe["ctl_firmreg"]
arm("firm_registry.json (class inert): the built tree with the LIVE firm_registry.json, every probe, against the built tree",
    "identical" if not sdiff(FR, PB) else "UNEXPECTED",
    "every probe result (composition, naming, 12 route cases, 7 svc operations, loaders, addresses, schemas) is IDENTICAL with either file; the two files differ only in the _generated header string.",
    ["firm_registry.json"])

# 4 -- routes of the real Entry
rd = sdiff(PL["routes"], PB["routes"])
errs = sum(v["arity_error_count"] for v in PB["routes"].values())
arm("every route of the function through the real generate_installed.build_boundary (analysis POST custody body and prospect body, upload POST, catalogue GET) x three principals, TypeError arity trace",
    "identical" if not rd and errs == 0 and not any(v["escaped"] for v in PB["routes"].values()) else "UNEXPECTED",
    "%d cases (3 routes, 4 bodies, 3 principals: internal row-listed, cottonwood firm user, svc-custody-statement), codes %s; IDENTICAL live vs built; call-arity TypeErrors on built: %d (live: %d); nothing escaped. The Entry is built over in-memory clients with stubbed deps, so a case that reaches the compute stops at the in-memory fakes (the pair, the history and the resident are replayed by their own arms)." % (
        len(PB["routes"]), sorted({v["code"] for v in PB["routes"].values()}), errs, sum(v["arity_error_count"] for v in PL["routes"].values())), ["served.py"])
sd = sdiff(PL["svc_operation"], PB["svc_operation"])
arm("the svc-custody-statement subject on direct-invoke events naming each operation (served.py allow-list), live vs built",
    "expected-diff" if set(sd) == {"/analysis-request-read/code", "/analysis-request-read/functions_entered"} and PL["svc_operation"]["analysis-request-read"]["code"] == "NOT_AUTHORIZED"
    and PB["svc_operation"]["analysis-request-read"]["code"] == "UNSUPPORTED_OPERATION" else "UNEXPECTED",
    "operation analysis-request-read: live %s, built %s (the new allow-list member passes the NOT_AUTHORIZED gate; this function has no handler for it). The six other operations are IDENTICAL: %s." % (
        PL["svc_operation"]["analysis-request-read"]["code"], PB["svc_operation"]["analysis-request-read"]["code"],
        {k: PB["svc_operation"][k]["code"] for k in sorted(PB["svc_operation"]) if k != "analysis-request-read"}), ["served.py"])
CS = probe["ctl_served"]["svc_operation"]["analysis-request-read"]["code"]
arm("NEGATIVE CONTROL svc subject: the built tree with served.py put back to the LIVE bytes", "expected-diff" if CS == PL["svc_operation"]["analysis-request-read"]["code"] else "UNEXPECTED",
    "control: analysis-request-read answers %s (the live code)." % CS, ["served.py"], True)
# the 409 binding cases
rl, rb = cases["live"]["routes"], cases["built"]["routes"]
n, diffs = 0, []
for rk in rb:
    if all(str(c["code"]).startswith("HARNESS_") for c in rb[rk]["cases"].values()):
        continue            # the upload route is not in entry.ROUTES; the 409 runner builds entry.ENTRY, so it cannot reach it (covered by the route arm above)
    for nm in rb[rk]["cases"]:
        n += 1
        a, b = rl[rk]["cases"][nm], rb[rk]["cases"][nm]
        if (a["reached_firm_check"], a["code"], a["roster"]) != (b["reached_firm_check"], b["code"], b["roster"]):
            diffs.append("%s/%s" % (rb[rk]["operation"], nm))
skipped = [rk for rk in rb if all(str(c["code"]).startswith("HARNESS_") for c in rb[rk]["cases"].values())]
arm("binding cases (userOwn, userSelOther, userClaimOther, noRow, rowCotCot, rowCotInf and the svc cases) through each zip's real entry.ENTRY, live vs built",
    "identical" if not diffs and n else "UNEXPECTED",
    "%d cases over %d route(s) of entry.ENTRY; (reached_firm_check, code, roster) IDENTICAL on %d, differing %s. Not reachable by this runner: %s (the runner builds entry.ENTRY, the upload route exists only in generate_installed.build_boundary; it is replayed in the route arm)." % (
        n, len(rb) - len(skipped), n - len(diffs), diffs or "none", skipped), ["served.py"])

# 5 -- loaders
LL, LB, LC = PL["loader"], PB["loader"], probe["ctl_loaders"]["loader"]
arm("loaders.load_directory with a latest.json pointer that names no usable key (absent, empty, not an object), live vs built",
    "expected-diff" if set(LB.values()) == {"FirmArtifactIncomplete"} and "FirmArtifactIncomplete" not in LL.values() else "UNEXPECTED",
    "live: %s ; built: %s (FirmArtifactIncomplete is the NOT_READY refusal named in loaders.py)." % (LL, LB), ["loaders.py"])
arm("NEGATIVE CONTROL loaders: the built tree with loaders.py put back to the LIVE bytes", "expected-diff" if LC == LL else "UNEXPECTED", "control: %s (the live outcomes)." % LC, ["loaders.py"], True)

# 6 -- the acceptance / submission_service pair
PRL, PRB = pair["live"], pair["built"]
arm("acceptance + submission_service: one new submission and one replay through the real service over an in-memory DynamoAcceptance",
    "expected-diff" if (PRB["acting_principal_id_present"] and PRB["acting_principal_id_is_the_verified_principal"] and not PRL["acting_principal_id_present"]
                       and PRL["transactions_written"] == PRB["transactions_written"] == 2 and PRL["transactions_after_replay"] == PRB["transactions_after_replay"]) else "UNEXPECTED",
    "live record keys %s; built record keys %s. acting_principal_id is on the built record and equals the verified principal's id; absent on live. Transactions written %d / %d (one request row, one job row), %d / %d after the replay (the replay writes nothing)." % (
        PRL["record_keys"], PRB["record_keys"], PRL["transactions_written"], PRB["transactions_written"], PRL["transactions_after_replay"], PRB["transactions_after_replay"]),
    ["acceptance.py", "submission_service.py"])
for key, what, who in (("ctl_pair_a", "built acceptance.py with the LIVE submission_service.py", "missing"), ("ctl_pair_b", "LIVE acceptance.py with the built submission_service.py", "unexpected keyword")):
    c = pair[key]
    arm("NEGATIVE CONTROL the pair split: %s" % what, "expected-diff" if c["first_submit"].startswith("TypeError") and c["transactions_written"] == 0 else "UNEXPECTED",
        "the submission raises %s and writes %d transactions: one member without the other is a TypeError on every new submission." % (c["first_submit"][:90], c["transactions_written"]),
        ["acceptance.py", "submission_service.py"], True)

# 7 -- the resident side
RL_, RB_ = resident["live"], resident["built"]
arm("durable_job: get_state and mark_i3_sent (the I3 send is recorded once, conditionally) over an in-memory job row",
    "expected-diff" if RB_["durable_job"]["marker_value_is_the_first"] is True and RB_["durable_job"]["i3_marker_updates"] == 1 and RL_["durable_job"]["mark_first"].startswith("EXC:AttributeError") else "UNEXPECTED",
    "built: first mark recorded, second mark a no-op (%d marker write), get_state then reports i3_sent_at (keys %s). live: mark_i3_sent does not exist (%s); get_state keys %s." % (
        RB_["durable_job"]["i3_marker_updates"], RB_["durable_job"]["get_state_after"], RL_["durable_job"]["mark_first"], RL_["durable_job"]["get_state_after"]), ["durable_job.py"])
sr = RB_["send_ready"]
arm("resident_worker: send_ready, mark_ready and producer_for over in-memory fakes (I3 once after READY; marker only after the send returned; the allow-list switch)",
    "expected-diff" if (sr["url_set_send_ok"]["sent"] == 1 and sr["url_set_send_ok"]["marks"] == 1 and sr["url_unset"]["sent"] == 0 and sr["send_fails"]["marks"] == 0
                       and sr["mark_fails"]["sent"] == 1 and RB_["mark_ready"]["i3_sends"] == 1 and RB_["producer_for"]["allow_listed_principal"] == "OPAL"
                       and RB_["producer_for"]["other_principal"] == "YCHARTS" and RL_["mark_ready"]["call"].startswith("EXC:AttributeError")) else "UNEXPECTED",
    "built: queue URL set and send ok -> sent %d, marked %d; URL unset -> sent %d (WARN logged); send fails -> marked %d (ERROR logged); mark fails -> sent %d, marked %d; mark_ready writes READY (%s) then sends I3 %d time(s); producer_for: allow-listed principal -> %s, any other -> %s. live: send_ready, mark_ready and producer_for do not exist (%s)." % (
        sr["url_set_send_ok"]["sent"], sr["url_set_send_ok"]["marks"], sr["url_unset"]["sent"], sr["send_fails"]["marks"], sr["mark_fails"]["sent"], sr["mark_fails"]["marks"],
        RB_["mark_ready"]["states_written"], RB_["mark_ready"]["i3_sends"], RB_["producer_for"]["allow_listed_principal"], RB_["producer_for"]["other_principal"], RL_["mark_ready"]["call"]),
    ["resident_worker.py", "durable_job.py"])
cd = resident["ctl_durable"]["send_ready"]["url_set_send_ok"]
arm("NEGATIVE CONTROL the I3 marker: the built tree with durable_job.py put back to the LIVE bytes", "expected-diff" if cd["sent"] == 1 and cd["marks"] == 0 and "ERROR: ANALYSIS_READY_MARK_FAILED" in cd["log_tokens"] else "UNEXPECTED",
    "control: send_ready sends %d, records %d markers and logs %s -- without mark_i3_sent the marker is never written." % (cd["sent"], cd["marks"], cd["log_tokens"]), ["durable_job.py", "resident_worker.py"], True)
pp = RB_["poll_package_once"]
arm("resident_worker.poll_package_once (the commentary_ready poll) over an in-memory SQS: attached, unknown outcome, malformed body",
    "expected-diff" if (pp["attached"]["deleted"] == 1 and pp["unknown_outcome_keeps_the_message"]["deleted"] == 0 and pp["not_json_refused_by_name"]["deleted"] == 1
                       and RL_["poll_package_once"]["attached"]["returned"].startswith("EXC:AttributeError")) else "UNEXPECTED",
    "built: ATTACHED deletes the message and prints outcome=ATTACHED; an unknown packager outcome raises %s and keeps the message; a non-JSON body is deleted with outcome=MESSAGE_NOT_JSON. live: poll_package_once does not exist." % pp["unknown_outcome_keeps_the_message"]["returned"],
    ["resident_worker.py"])
m5, m5l, m3, m3l = RB_["main_five_key_runtime_with_commentary_queue"], RL_["main_five_key_runtime_with_commentary_queue"], RB_["main_three_key_runtime"], RL_["main_three_key_runtime"]
arm("resident_main.main(--once) with a runtime that carries the commentary_ready queue and a packager (five keys)",
    "expected-diff" if m5["rc"] == 0 and m5["package_messages_deleted"] == 1 and str(m5l["rc"]).startswith("EXC:ValueError:INSTALLED_RESIDENT_RUNTIME_REQUIRED") else "UNEXPECTED",
    "built: returns %s, polls the package queue after the generation poll (stdout %s), %d package message deleted. live: %s." % (m5["rc"], m5["stdout"], m5["package_messages_deleted"], m5l["rc"]), ["resident_main.py", "resident_worker.py"])
arm("resident_main.main(--once) with the three-key runtime the live resident host passes", "identical" if m3 == m3l and m3["rc"] == 0 else "UNEXPECTED",
    "live and built both return %s and print %s." % (m3["rc"], m3["stdout"]), ["resident_main.py"])
mc = resident["ctl_main"]["main_five_key_runtime_with_commentary_queue"]["rc"]
arm("NEGATIVE CONTROL resident_main: the built tree with resident_main.py put back to the LIVE bytes", "expected-diff" if str(mc).startswith("EXC:ValueError:INSTALLED_RESIDENT_RUNTIME_REQUIRED") else "UNEXPECTED",
    "control: the five-key runtime raises %s." % mc, ["resident_main.py"], True)

# 8 -- the four carried method-call sites (AMENDMENT 1)
SL_, SB_ = sites["live"], sites["built"]
arm("carried method site publication .lookup(1 argument): foreign_firm_names -> the real opal_naming.lookup, firm registered and unregistered",
    "identical" if SL_["publication_lookup"]["outcomes"] == SB_["publication_lookup"]["outcomes"] and SB_["publication_lookup"]["line_hits"] >= 2 else "UNEXPECTED",
    "the source line was reached %d times on built, %d on live; lookup%s is the module function opal_naming.lookup, not DynamoAcceptance.lookup(owner, browser); outcomes IDENTICAL: %s (a registered firm passes the lookup and stops at the PDF-text backend, which is absent on this box; an unregistered one is refused REPORT_FIRM_UNREGISTERED by the KeyError the lookup raises)." % (
        SB_["publication_lookup"]["line_hits"], SL_["publication_lookup"]["line_hits"], SB_["publication_lookup"]["lookup_signature"], SB_["publication_lookup"]["outcomes"]), [])
pvb, pvl = SB_["publisher_validate"], SL_["publisher_validate"]
arm("carried method sites publisher .validate(2 arguments) x2: the Opal path and the vendor path of CertifiedReportPublisher.publish with a fake `reports` whose validate is (kind, payload)",
    "identical" if pvb == pvl and pvb["lines_reached"] == [191, 258] and pvb["opal_path"]["validate_calls"] and pvb["vendor_path"]["validate_calls"] else "UNEXPECTED",
    "both source lines (%s) were reached on live and on built; the callee was handed ('ANALYSIS', dict) at each; the Opal path ran to its return (%s), the vendor path stopped after the call at the fake build_publication's missing key. The PDF-text backend and certification are replaced by stand-ins (foreign_firm_names -> [], build_publication -> {fragment: {}}). The injected object is a fake shaped like repository.ReportRepository's validate attribute; the real one is not in this package. Results IDENTICAL on the two trees." % (
        pvb["lines_reached"], pvb["opal_path"]["outcome"]), [])
rvb, rvl = SB_["resident_renew"], SL_["resident_renew"]
arm("carried method site resident_worker .renew(ttl=900): ResidentGenerationWorker.guard() through the real broker._RecoveryObserver over a fake transport with renew(*, ttl)",
    "identical" if rvb["outcome"] == rvl["outcome"] == "returned" and rvb["transport_renewed_with_ttl"] == rvl["transport_renewed_with_ttl"] == [900] and rvb["line_hits"] >= 1 and rvl["line_hits"] >= 1 else "UNEXPECTED",
    "the source line was reached on both trees; _RecoveryObserver.__getattr__ forwarded renew to the transport, which recorded ttl=%s; store.renew() (DynamoGenerationStore.renew, no ttl) ran separately %d time. The transport is a fake shaped like ycharts/session/operation_lease.py renew(self, *, ttl); the real one is installer-supplied and not in this package. IDENTICAL on live and built." % (
        rvb["transport_renewed_with_ttl"], rvb["store_renews"]), ["resident_worker.py"])

# 9 -- the pin tests against each tree, per-test, with sensitivity controls
reg_total, fixed_total, both_total = 0, 0, 0
grand = {"live": {}, "built": {}}
for d in TEST_DIRS:
    for side in ("live", "built"):
        grand[side].update({d + "/" + k: v for k, v in tests[side][d]["results"].items()})
regress = sorted(k for k, v in grand["live"].items() if v == "PASSED" and grand["built"].get(k) != "PASSED")
fixed = sorted(k for k, v in grand["built"].items() if v == "PASSED" and grand["live"].get(k) != "PASSED")
guard = sum((tests[s][d].get("guard_attempts") or 0) for s in tests for d in tests[s])
arm("no regression: every pin test id that PASSES against the live zip's modules, run against the built zip's modules",
    "identical" if not regress else "UNEXPECTED",
    "%d test ids run on each tree (%d dirs: %s); PASSED on live and not on built: %d %s; PASSED on built and not on live: %d. Network connects attempted and refused by the offline guard: %d (tests that need a real S3/DynamoDB client fail identically on both trees). PyMuPDF is stubbed (import only)." % (
        len(grand["built"]), len(TEST_DIRS), ", ".join(TEST_DIRS), len(regress), regress[:5], len(fixed), guard), [])
for name, d, files, members, ctl_members in TEST_ARMS:
    L = passed(tests["live"], d, files)
    B = passed(tests["built"], d, files)
    fx = sorted(k for k, v in B.items() if v == "PASSED" and L.get(k) != "PASSED")
    rg = sorted(k for k, v in L.items() if v == "PASSED" and B.get(k) != "PASSED")
    # sensitivity control: the built tree with the named members at LIVE bytes, same files
    ctree = control("ctl_t_" + str(len(arms)), ctl_members)
    cres = run_tests(ctree, "ctl%d" % len(arms), {d: files}, "ctl%d" % len(arms))[d]["results"]
    CB = {k: v for k, v in cres.items() if any(k.startswith("tests/" + f) for f in files)}
    reverted = sorted(k for k in fx if CB.get(k) != "PASSED")
    arm(name + ": run against live and built", "expected-diff" if (fx and not rg) else ("identical" if not rg and not fx else "UNEXPECTED"),
        "%d test ids across %s; passed on built and not on live: %d; passed on live and not on built: %d. Tests that pass only on built: %s." % (
            len(B), files, len(fx), len(rg), sorted({k.split("::")[0].split("/")[-1] for k in fx})), members)
    arm("NEGATIVE CONTROL for the arm above: the built tree with %s put back to the LIVE bytes, same test files" % ctl_members,
        "expected-diff" if fx and len(reverted) >= 1 else "UNEXPECTED",
        "%d of the %d tests that pass only on built fail again with %s at live bytes, so those tests exercise these members; the other %d of the %d depend on other moved members and are not claimed for these." % (
            len(reverted), len(fx), ctl_members, len(fx) - len(reverted), len(fx)), members, True)
    shutil.rmtree(ctree, ignore_errors=True)

doc = {"pin": pin, "function": FN, "arms": arms,
       "harness": "replay/run_replay_426.py; offline: boto3 faked in-process, every socket connect refused (guard426 plugin and the probes), AWS never called; one tree per process; synthetic ids only",
       "arm_count": len(arms), "tests_run_per_tree": len(grand["built"]),
       "tree_sha256": {"live": os.environ.get("LIVE_SHA", ""), "built": os.environ.get("BUILT_SHA", "")}}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
bad = [a for a in arms if a["verdict"] not in ("identical", "expected-diff")]
for a in arms:
    print(a["verdict"], "NEG" if a["negative_control"] else "   ", a["name"][:110])
print("arms=%d unexpected=%d" % (len(arms), len(bad)))
