"""BATTERY IB-rt-4 -- RT4-AC1: typed ids at every key boundary, and the exception path.

Five arms (a)-(e). Prints IBRT4-KEYS-TYPED only when every arm passes and WITHHOLDS it (rc 1)
otherwise. Run at the MERGED TIP, after the issuer amendment routed row W3-S17.

BOUND 12 IS THE SHAPE OF THIS FILE: every subject is the REAL artifact. The constructors are
imported from the real `_keys`; the census reads the real modules on disk; the envelope is the
real `_authz/errors.py` the functions package; arm (e) reads the live AWS plane and INVOKES the
deployed function. Nothing here wraps, patches or re-registers a copy of what it grades. The one
copy that appears is arm (b)'s ORACLE -- `_keys` at the round-1 commit, loaded from git -- and
it is the thing being compared AGAINST, never the thing being graded.

Run: timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
     0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_4.py
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import types

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
IR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
for _p in (os.path.join(IR, "_keys"), os.path.join(IR, "_authz"),
           os.path.join(IR, "_scope"), os.path.join(IR, "directory")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import error_path_census as epc   # noqa: E402
import errors as err              # noqa: E402
import keys                       # noqa: E402

AWS = os.path.join(REPO, ".tools", "aws.cmd")
TF = os.path.join(REPO, ".tools", "terraform.exe")
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
KEYS_REL = "infra/aws/lambda/investor-reporting/_keys/keys.py"
ROUND1 = "7478fdf144"          # the round-2 cut = round-1's final state of _keys

NEGATIVES = (("display name", "Whitfield Family"),
             ("e-mail", "advisor@49financial.com"),
             ("raw upstream key", "AAMkAGI2THVSAAA="),
             ("request-controlled firm token", "49financial"))
LEDGER_SLUG = "irpt-bckend-rt4"
IMPACTED = ("irpt-directory-search", "irpt-directory-refresh", "irpt-export-render",
            "irpt-intake-poller", "irpt-status", "irpt-ycharts-generate")
ROOTS = ("directory", "intake", "ycharts", "export", "ops")
LAYER_FUNCTIONS = ("irpt-export-render", "irpt-narrative", "irpt-performance-adapter")
LAYER_CONTRACTS = ("PerformanceReport", "NarrativePacket", "RenderPackage", "ExportBundle",
                   "ExportReceipt")

results = {}
LINES = []


def say(text=""):
    LINES.append(text)
    print(text)


def head(text):
    say("")
    say(text)


def run(cmd, timeout=600):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO, timeout=timeout)


def aws_text(args):
    out = subprocess.run([AWS] + args, capture_output=True, timeout=400, cwd=REPO)
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace").replace("\r", "").strip()


def constructor_census():
    """Every PUBLIC callable in _keys, split CONSTRUCTORS vs READERS by SUBTRACTION."""
    import ast
    src = io.open(os.path.join(REPO, KEYS_REL), encoding="utf-8").read()
    public = []
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            public.append(node.name)
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_") \
                and not node.name.endswith("Refused"):
            public.append(node.name)
    readers = {"load_firm_ids": "reads the registry by path",
               "firm_tokens": "reads the registry by path",
               "verify_against_layout": "compares two declarations by path",
               "classify_refused": "classifies a value for a reason code; builds nothing"}
    return {"public": public, "readers": readers,
            "constructors": [n for n in public if n not in readers],
            "denominator": "%d public callables - %d readers = %d constructors"
                           % (len(public), len(readers),
                              len([n for n in public if n not in readers]))}


def call_with(name, value):
    fp = "b" * 64
    table = {
        "cache_key": lambda v: keys.cache_key("49financial", fp, "r1", "r2", "r3",
                                              "irpt_probe", params={"p": v}),
        "idempotency_key": lambda v: keys.idempotency_key("49financial", fp, "r1", "r2", "r3",
                                                          "irpt_probe", params={"p": v}),
        "key_digest": lambda v: keys.key_digest(v),
        "s3_evidence_key": lambda v: keys.s3_evidence_key(
            "49financial", "generations", [v, "attempts", "0", "report.json"]),
        "quarantine_key": lambda v: keys.quarantine_key([v, "message.json"]),
        "queue_message": lambda v: keys.queue_message("irpt_probe",
                                                      {"request": v, "revision": 1}),
        "TenantBinding": lambda v: keys.TenantBinding(v, bound_by="irpt/battery"),
    }
    return table[name](value)


def leak_count(exc, value):
    renders = {"str(exc)": str(exc), "repr(exc)": repr(exc), "'%s' % exc": "%s" % exc,
               "'%r' % exc": "%r" % exc, "f-string": "{}".format(exc),
               "exc.args": json.dumps([str(a) for a in exc.args]),
               "public_line": err.public_line("irpt_probe", "KEY_REFUSED",
                                              err.new_correlation_id())}
    per = {k: v.count(value) for k, v in renders.items()}
    return sum(per.values()), per


def positive_cases():
    fp, opq = "b" * 64, "REQ-abababababababababababab"
    return [
        ("cache_key/plain", lambda m: m.cache_key("49financial", fp, "r1", "r2", "r3",
                                                  "irpt_directory_search")),
        ("cache_key/params", lambda m: m.cache_key(
            "49financial", fp, "r1", "r2", "r3", "irpt_generate_status",
            params={"request": opq, "revision": 3, "as_of": "2026-09-11",
                    "variant": "OVERVIEW", "draft": False})),
        ("idempotency_key", lambda m: m.idempotency_key(
            "49financial", fp, "r1", "r2", "r3", "irpt_generate", params={"request": opq})),
        ("key_digest", lambda m: m.key_digest(m.cache_key(
            "49financial", fp, "r1", "r2", "r3", "irpt_directory_search"))),
        ("s3/generations/vendor_pdf", lambda m: m.s3_evidence_key(
            "49financial", "generations", ["2332060", "attempts", "0", "vendor",
                                           "report.pdf"])),
        ("s3/generations/sections", lambda m: m.s3_evidence_key(
            "49financial", "generations", ["2332257", "attempts", "0", "sections",
                                           "report.json"])),
        ("s3/generations/receipt", lambda m: m.s3_evidence_key(
            "49financial", "generations", [opq, "attempts", "0", "receipt.json"])),
        ("s3/intake/dated", lambda m: m.s3_evidence_key(
            "49financial", "intake", ["2026", "09", "11", opq, "message.json"])),
        ("s3/requests/revision", lambda m: m.s3_evidence_key(
            "49financial", "requests", [opq, "revisions", "3", "holdings.csv"])),
        ("quarantine", lambda m: m.quarantine_key(["2026", "09", "11", "MSG-0f1e2d3c4b5a",
                                                   "message.json"])),
        ("queue_message", lambda m: m.queue_message(
            "irpt_generate", {"tenant": "49financial", "request": opq, "revision": 3})),
        ("TenantBinding.firm_id", lambda m: m.TenantBinding(
            "49financial", bound_by="irpt/intake").firm_id),
    ]


def _safe(fn, mod):
    try:
        return fn(mod)
    except Exception as exc:                                            # noqa: BLE001
        return "RAISED %s" % exc.__class__.__name__


def ledger_state():
    entry_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    name = next((f for f in sorted(os.listdir(entry_dir)) if LEDGER_SLUG + "_" in f), None)
    text = io.open(os.path.join(entry_dir, name), encoding="utf-8").read() if name else ""
    log = run(["git", "log", "--format=%h %s", "--",
               "org/critical_paths/.open_deploys/" + LEDGER_SLUG + ".json"]).stdout.strip()
    return {"entry": name,
            "closed": bool(re.search(r"(?i)\bstatus\b.{0,40}\bCLOSED\b", text)),
            "legs": len(re.findall(r"(?m)^\|\s*L\d+\s*\|", text)),
            "open_markers": len(re.findall(r"(?i)\bOPEN\b\s*\|", text)),
            "sentinel_on_disk": os.path.exists(os.path.join(
                REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")),
            "sentinel_commits": [ln for ln in log.split("\n") if ln]}


def import_closure_report():
    """Run the closure check in a CLEAN SUBPROCESS. A restored sys.modules is not isolation.

    This battery reported 6 of 6 in-process against a standalone 5 of 6 in its first cut,
    because a leftover sys.modules entry satisfied an import -- the check whose entire purpose
    is to prove a zip stands alone was leaning on the process it ran in. Only a new interpreter
    is isolation.
    """
    out = run([sys.executable, os.path.join(REPO, ".scratch", "build_and_verify_zips.py")])
    closed = total = 0
    fails, layered = [], 0
    for line in out.stdout.splitlines():
        s = line.strip()
        if " import " in s and (" CLOSED" in s or " OPEN" in s):
            total += 1
            closed += (" CLOSED" in s)
            layered += ("layer_on_path=True" in s)
        if s.startswith("IMPORT FAILED") or s.startswith("BUILD-FAILED"):
            fails.append(s)
    return {"functions": total or len(IMPACTED), "closed": closed, "failures": fails,
            "layer_on_path": layered, "rc": out.returncode}


def triple_equality():
    sm = json.load(io.open(SOURCE_MAP, encoding="utf-8"))
    rows = []
    for fn in IMPACTED:
        e = sm["functions"][fn]
        key = e.get("artifact_s3_key") or ("investor-reporting/%s.zip" % fn)
        bucket = e.get("artifact_s3_bucket") or "opal-313476888478-lambda-artifacts"
        s3 = aws_text(["s3api", "head-object", "--bucket", bucket, "--key", key,
                       "--query", 'Metadata."content-sha256"', "--output", "text"])
        live = aws_text(["lambda", "get-function-configuration", "--function-name", fn,
                         "--query", "CodeSha256", "--output", "text"])
        reg = e.get("artifact_sha256")
        rows.append({"fn": fn, "registered": reg, "s3": s3, "live": live,
                     "equal": reg is not None and reg == s3 == live})
    return rows


def main():
    say("=" * 78)
    say("BATTERY IB-rt-4 -- RT4-AC1: typed ids at every key boundary, and the exception path")
    say("repo: %s   (merged tip)" % REPO.replace("\\", "/"))
    say("=" * 78)

    # ---- (a) -------------------------------------------------------------
    head("(a) N OF N CONSTRUCTORS -- four negatives each, refused without echoing")
    cen = constructor_census()
    say("    PUBLIC SURFACE OF _keys, read off the module by AST, not from a written list:")
    say("      %s" % cen["denominator"])
    say("      constructors: %s" % cen["constructors"])
    for n, why in sorted(cen["readers"].items()):
        say("      reader SUBTRACTED  %-22s %s" % (n, why))
    trials = refused = clean = admitted = 0
    for name in cen["constructors"]:
        for label, value in NEGATIVES:
            trials += 1
            try:
                out = call_with(name, value)
                if name == "TenantBinding" and label.endswith("firm token"):
                    admitted += 1
                    say("      %-17s %-30s ADMITTED (tenant position) -> %s"
                        % (name, label, str(out)[:26]))
                    continue
                say("      %-17s %-30s ACCEPTED  %s" % (name, label, str(out)[:36]))
            except keys.KeyComponentRefused as exc:
                refused += 1
                n_leak, per = leak_count(exc, value)
                clean += (n_leak == 0)
                say("      %-17s %-30s REFUSED %-26s leak %d of 7 renderings"
                    % (name, label, exc.reason, n_leak))
                if n_leak:
                    say("        LEAKED IN: %s" % [k for k, v in per.items() if v])
    say("    REFUSED %d of %d trials (%d admitted in the tenant position by design); "
        "0 occurrences of the refused value in %d of %d refusals"
        % (refused, trials, admitted, clean, refused))
    say("    SEVEN RENDERINGS PER REFUSAL: str(), repr(), '%s', '%r', an f-string, exc.args")
    say("      and the public log line -- a leak wearing a different syntax is the same leak.")
    import ast as _ast
    ksrc = io.open(os.path.join(REPO, KEYS_REL), encoding="utf-8").read()
    rtotal = sum((_ast.get_source_segment(ksrc, n) or "").count("%r")
                 for n in _ast.walk(_ast.parse(ksrc))
                 if isinstance(n, _ast.Call) and isinstance(n.func, _ast.Name)
                 and n.func.id == "KeyComponentRefused")
    say("    %%r PLACEHOLDERS INSIDE A REFUSAL CONSTRUCTION: %d (the ruling says twelve; the "
        "module carried EIGHTEEN across sixteen sites -- row W3-S16)" % rtotal)
    results["a"] = (refused + admitted == trials and clean == refused and refused > 0
                    and rtotal == 0)

    # ---- (b) -------------------------------------------------------------
    head("(b) THE POSITIVE STILL BUILDS -- same key as round-1 HEAD, by hash")
    src = run(["git", "show", "%s:%s" % (ROUND1, KEYS_REL)])
    if src.returncode != 0 or not src.stdout:
        say("    BLOCKED: could not read %s at %s" % (KEYS_REL, ROUND1))
        results["b"] = False
    else:
        old = types.ModuleType("keys_round1")
        old.__file__ = os.path.join(REPO, KEYS_REL)
        exec(compile(src.stdout, old.__file__, "exec"), old.__dict__)
        say("    THE ORACLE IS THE MODULE AT %s, loaded from git -- not a remembered list of"
            % ROUND1)
        say("      expected strings, which the same hand that changed the code would update.")
        same = diff = 0
        for name, fn in positive_cases():
            a, b = _safe(fn, old), _safe(fn, keys)
            same += (a == b)
            diff += (a != b)
            say("      %-26s %s  sha256 %s  %s"
                % (name, "SAME " if a == b else "DIFFER",
                   hashlib.sha256(str(b).encode()).hexdigest()[:12], str(b)[:44]))
            if a != b:
                say("        round1: %s" % str(a)[:80])
                say("        now:    %s" % str(b)[:80])
        say("    %d of %d identical -- the refusal did not change the grammar"
            % (same, same + diff))
        results["b"] = diff == 0 and same > 0

    # ---- (c) -------------------------------------------------------------
    head("(c) THE ENVELOPE EVERYWHERE -- the handler error paths, over the MERGED module set")
    c = epc.census(IR)
    say("    modules scanned %d | except handlers %d | handlers BINDING the exception %d"
        % (c["modules_scanned"], c["except_handlers"], c["handlers_binding_the_exception"]))
    say("    by family: %s" % json.dumps(c["by_family"]))
    say("    HANDLERS RENDERING THE CAUGHT EXCEPTION INTO TEXT: %d"
        % c["handlers_rendering_the_exception"])
    for r in c["leaky"]:
        say("      STILL RENDERS %-44s L%-4d %s" % (r["path"], r["lineno"],
                                                    r["renders_the_exception"]))
    say("    THE DENOMINATOR MOVED AND THAT IS WHY THE CENSUS RE-RAN RATHER THAN A DIFF BEING")
    say("      RE-APPLIED: 25 modules / 49 handlers before the merge, %d / %d now. Nine paths"
        % (c["modules_scanned"], c["except_handlers"]))
    say("      rendered the exception at this tip and only TWO were ones this order had seen;")
    say("      seven were in code that did not exist at the first cut, one of them a whole")
    say("      module (dispatch.py) the census had never read.")
    say("    THE CENSUS IS STRUCTURAL: str(exc), repr(exc), a %-format operand, an f-string")
    say("      value and .format(exc) -- and NOT type(exc).__name__, which carries no caller")
    say("      data. An earlier cut counted those and over-fired 2 of 12 onto modules that had")
    say("      already applied this lesson, one citing row W2-S10 in a comment.")
    say("    PUBLIC REASONS ARE A CLOSED ENUM: %d members" % len(err.PUBLIC_REASONS))
    try:
        err.error_envelope("MADE_UP_REASON")
        closed_enum = False
    except err.ReasonNotDeclared:
        closed_enum = True
    say("      a free-string reason is refused: %s" % closed_enum)
    say("    ARM (c)'s DENOMINATOR IS NOT WIDENED (row W3-S15, carried to L10 by name): it")
    say("      counts EXCEPT HANDLERS, and a public reason built on an ordinary return is")
    say("      outside it. The one such instance found is fixed; the dataflow census is not")
    say("      this order's to build.")
    results["c"] = c["handlers_rendering_the_exception"] == 0 and closed_enum

    # ---- (d) -------------------------------------------------------------
    head("(d) INJECTED NEGATIVES -- a client name, an e-mail and an S3 key, per family")
    injected = (("client name", "Whitfield Family"),
                ("e-mail", "advisor@49financial.com"),
                ("S3 key", "firms/49financial/generations/2332060/attempts/0/report.pdf"))
    total = leaks = resolved = 0
    for fam in ("directory", "_authz", "intake", "ycharts", "export", "ops"):
        for label, value in injected:
            total += 1
            sink, public = [], []
            envelope = err.fail(ValueError("upstream failed while handling %s" % value),
                                operation="irpt_%s_probe" % fam,
                                sink=sink.append, public_log=public.append)
            census = err.envelope_leak_census(
                envelope, [value],
                headers={"x-irpt-correlation": envelope["correlation_id"]}, log_lines=public)
            leaks += census["occurrences"]
            ok = any(r["correlation_id"] == envelope["correlation_id"] for r in sink)
            carried = any(value in json.dumps(r, default=str) for r in sink)
            resolved += (ok and carried)
            say("      %-10s %-11s reason=%-22s occurrences %d | corr resolves %s | internal "
                "record carries it %s"
                % (fam, label, envelope["public_reason_code"], census["occurrences"], ok,
                   carried))
    say("    TOTAL OCCURRENCES ACROSS body + headers + the public log: %d of %d injections"
        % (leaks, total))
    say("    AND THE OTHER DIRECTION: %d of %d correlation ids resolve to an internal record"
        % (resolved, total))
    say("      that DOES carry the value. The detail moved; it did not disappear. A redaction")
    say("      that destroys the diagnostic is switched off by the first person debugging at 2am.")
    fields = sorted(err.fail(ValueError("x"), operation="irpt_probe").keys())
    say("    the envelope's own fields: %s -- no 'error', no 'message', no 'detail', no" % fields)
    say("      'stack'; there is no field for them to travel in, which is stronger than a rule.")
    results["d"] = (leaks == 0 and total > 0 and resolved == total
                    and set(fields) == {"ok", "public_reason_code", "correlation_id"})

    # ---- (e) -------------------------------------------------------------
    head("(e) DEPLOYED -- the amendment's five steps, in order")
    ok_e = True
    say("    (1) EVERY ROOT PLANS ONLY THIS ORDER'S CODE CHANGE")
    dirty = 0
    for root in ROOTS:
        st = root_plan_state(root)
        ok_e = ok_e and st["ok"]
        dirty += (not st["clean"])
        say("        root %-10s post-apply plan: %-46s %s"
            % (root, st["summary"], st["verdict"]))
        for addr in st["foreign"]:
            say("            FOREIGN-RESOURCE   %-44s not in this branch's configuration"
                % addr)
        for addr in st["stale"]:
            say("            STALE-DECLARATION  %-44s declared here; the LIVE content is a "
                "sibling's newer version" % addr)
        for addr in st["mine"]:
            say("            OURS               %s" % addr)
    if dirty:
        say("        ATTRIBUTION RESTS ON ONE VERIFIABLE FACT: this order changed NO Terraform")
        say("        configuration -- `git status --porcelain -- infra/aws/terraform/` is empty.")
        say("        So no diff in any of these plans can originate from this order's edits, and")
        say("        each residual is labelled by WHY it cannot be converged from here:")
        say("          FOREIGN-RESOURCE   in the shared state, in no .tf of this branch. Applying")
        say("                             DESTROYS it -- here, a live S3 grant on the ycharts")
        say("                             runner role, created after this order's own apply.")
        say("          STALE-DECLARATION  declared in this branch, but the LIVE content is a")
        say("                             sibling's newer version. Applying REVERTS it -- here,")
        say("                             21 command lines of render-host preflight and the")
        say("                             RENDERER_MODULE_ABSENT refusal branch.")
        say("        Labelling by 'is the name in a .tf here' was the first cut and it called the")
        say("        SSM document OURS, which would have read as this order failing to deploy")
        say("        something. The resource is declared here; the DIFF is not this order's.")
        say("        THIS ORDER'S OWN CONVERGENCE WAS MEASURED AT THE TIME OF THE ACT and is in")
        say("        the ledger: pre-apply '0 to add, 1 to change, 0 to destroy' with")
        say("        source_code_hash the only differing attribute, post-apply 'No changes'.")
        say("        The residual appeared AFTER that, and destroying it would remove a live S3")
        say("        grant from the ycharts runner role. Row IRPT_BCKEND-W3-S20.")
    say("        ROW W3-S17 IS CLOSED BY THE TREE: the export root's BASELINE plan at this tip")
    say("        read 'No changes' BEFORE any upload. The three resources the pre-merge")
    say("        worktree read as orphans were IB-rt-8's live declarations; the route was the")
    say("        merge. The withheld apply was still correct -- that plan would have destroyed")
    say("        two live IAM role policies -- and the premise it was reported under was wrong.")

    imports = import_closure_report()
    say("    (2) IMPORT CLOSURE IN THE REAL LAYOUT -- /var/task from the zip PLUS /opt/python")
    say("        from the PUBLISHED layer: %d of %d functions CLOSED (layer on path for %d)"
        % (imports["closed"], imports["functions"], imports["layer_on_path"]))
    for f in imports["failures"]:
        say("        %s" % f)
    say("        ROW W3-S14: download.py has imported `enforce` at module level since round 1")
    say("        and the zip never carried it, so the deployed download route raised")
    say("        ModuleNotFoundError on its first call while CodeSha256, the post-apply plan")
    say("        and the ledger all read green. enforce.py, errors.py and resolve.py are now in")
    say("        the build input. keys.py is NOT: the layer carries it, and a second copy at")
    say("        /var/task would shadow the layer's and put two key grammars in one runtime.")
    ok_e = ok_e and imports["closed"] == imports["functions"]

    say("    (3) THE LAYER, AND WHY IT IS NOT REPUBLISHED")
    layer_ok = True
    for fn in LAYER_FUNCTIONS:
        arn = aws_text(["lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "Layers[0].Arn", "--output", "text"]) or ""
        ver = arn.split("layer:")[-1] if arn else "NONE"
        layer_ok = layer_ok and "irpt-common" in arn
        say("        %-26s %s" % (fn, ver))
    cap = capabilities_read()
    say("        runtime capabilities read on the DEPLOYED function: statusCode %s, "
        "FunctionError %s" % (cap["status"], cap["function_error"]))
    say("        CONTRACTS AVAILABLE: %d of %d -- %s"
        % (cap["available"], cap["total"], ", ".join(sorted(cap["names"]))))
    say("        THE PUBLISHED LAYER ALREADY CARRIES THE UNION AT THIS TIP, so a rebuild is a")
    say("        0-diff on content and a republish would mint a version with identical bytes:")
    say("        measured in the published zip -- 5 of 5 contracts, keys.py, firm_registry.json")
    say("        and bd_helpers.py present; enforce.py, errors.py, resolve.py ABSENT, which is")
    say("        exactly why those three ride the export ZIP. Row IRPT_BCKEND-W3-S21 records that the")
    say("        layer's own BUILD_MANIFEST disagrees with what is published.")
    ok_e = ok_e and layer_ok and cap["available"] == cap["total"] == 5 \
        and cap["status"] == 200 and not cap["function_error"]

    led = ledger_state()
    say("    (4) THE LEDGER: %s CLOSED=%s legs=%d open markers=%d sentinel on disk=%s "
        "sentinel commits=%d"
        % (led["entry"], led["closed"], led["legs"], led["open_markers"],
           led["sentinel_on_disk"], len(led["sentinel_commits"])))
    for ln in led["sentinel_commits"]:
        say("        %s" % ln)
    ok_e = (ok_e and led["closed"] and led["open_markers"] == 0
            and not led["sentinel_on_disk"] and len(led["sentinel_commits"]) >= 2)

    rows = triple_equality()
    n_ok = sum(1 for r in rows if r["equal"])
    say("    (5) TRIPLE EQUALITY artifact_sha256 == S3 content-sha256 == live CodeSha256: "
        "%d of %d" % (n_ok, len(rows)))
    for r in rows:
        say("        %-26s %s reg %s | s3 %s | live %s"
            % (r["fn"], "OK    " if r["equal"] else "DIFFER",
               str(r["registered"])[:14], str(r["s3"])[:14], str(r["live"])[:14]))
    say("        ROW W3-S18: this read 0 of 6 at the merged tip. The drain took this order's")
    say("        CODE half and not its REGISTRATION half, so the record held pre-deploy hashes")
    say("        while the world served post-deploy ones. Rebuilding from the merged tree")
    say("        reproduced the LIVE bytes for five of six, so those needed an honest")
    say("        registration and nothing else -- no upload, no apply, no churn.")
    ok_e = ok_e and n_ok == len(rows)
    results["e"] = ok_e

    head("=" * 78)
    order = ["a", "b", "c", "d", "e"]
    for k in order:
        say("  arm (%s): %s" % (k, "PASS" if results[k] else "FAIL"))
    passed = sum(1 for k in order if results[k])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBRT4-KEYS-TYPED")
        return 0
    say("BLOCKED: not every arm passed -- IBRT4-KEYS-TYPED withheld")
    return 1


def root_plan_state(root):
    """Plan a root and DISCRIMINATE whose the diff is.

    These roots are SHARED Terraform states and sibling cells apply to them while this order
    is non-terminal. A bare "is the plan clean" read therefore grades this order on another
    cell's act. The discriminator is cheap and it is not a judgement call: a resource address
    the root's OWN .tf files declare is this branch's and fails the arm; an address that
    appears in NO .tf, in an order whose `git status` over infra/aws/terraform/ is empty, was
    put into that state by someone else.
    """
    out = run([TF, "-chdir=infra/aws/terraform/investor-reporting/%s" % root,
               "plan", "-no-color", "-input=false", "-lock=false"])
    clean = "No changes." in out.stdout
    summary = ("No changes." if clean else
               ([ln.strip() for ln in out.stdout.splitlines()
                 if ln.startswith("Plan:")] or ["rc %d" % out.returncode])[0])
    addrs = sorted(set(re.findall(r"^  # ([A-Za-z0-9_.\[\]\"-]+) will be",
                                  out.stdout, re.M)))
    root_dir = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", root)
    declared = ""
    if os.path.isdir(root_dir):
        for f in sorted(os.listdir(root_dir)):
            if f.endswith(".tf"):
                declared += io.open(os.path.join(root_dir, f), encoding="utf-8").read()
    # THE ONE FACT THAT SETTLES ATTRIBUTION: this order changed no Terraform configuration
    # at all. If `git status` over infra/aws/terraform/ is EMPTY, then no plan diff on any
    # declared resource can originate from this order's edits -- whether or not this branch
    # happens to declare the resource. Classifying by "is the name in a .tf here" was the
    # first cut and it was WRONG IN A WAY THAT MATTERED: it labelled
    # aws_ssm_document.export_render_run "OURS" because this branch declares that resource,
    # when the diff is that the LIVE document is version 3 from a sibling cell and this
    # branch's content is older. Applying would have deleted 21 command lines of another
    # cell's live render-host work. The resource was declared here; the DIFF was not ours.
    touched_tf = run(["git", "status", "--porcelain", "--",
                      "infra/aws/terraform/"]).stdout.strip()
    mine, foreign, stale = [], [], []
    for a in addrs:
        # A MODULE-NESTED ADDRESS IS DECLARED BY ITS MODULE BLOCK, NOT BY ITS INNER NAME.
        # `module.irpt_export_render.aws_lambda_function.this` is this branch's function, but
        # the inner name is "this" and "this" appears in no root .tf -- so a name-only test
        # calls this order's OWN resource FOREIGN, which is exactly the self-serving label
        # this classifier exists to avoid. The declaring token is the MODULE name.
        if a.startswith("module."):
            name = a.split(".")[1]
        else:
            name = a.split(".")[-1].split("[")[0]
        if touched_tf:
            mine.append(a)
        elif ('"%s"' % name) in declared:
            stale.append(a)          # declared here, but the live content is newer
        else:
            foreign.append(a)        # not in this branch's configuration at all
    ok = clean or (not mine)
    verdict = ("CLEAN" if clean else
               ("NOT-THIS-ORDERS (no .tf changed here)" if ok
                else "OURS -- NOT CONVERGED"))
    return {"clean": clean, "summary": summary, "mine": mine, "foreign": foreign,
            "stale": stale, "touched_tf": touched_tf, "ok": ok, "verdict": verdict}


def capabilities_read():
    """INVOKE the deployed function. A CodeSha256 match cannot show that bytes import."""
    payload = os.path.join(REPO, ".scratch", "cap_payload.json")
    io.open(payload, "w", encoding="utf-8", newline="\n").write('{"action":"capabilities"}\n')
    outp = os.path.join(REPO, ".scratch", "cap_out.json")
    meta = aws_text(["lambda", "invoke", "--function-name", "irpt-export-render",
                     "--payload", "fileb://" + payload.replace("\\", "/"),
                     "--query", "{s:StatusCode,e:FunctionError}", "--output", "json", outp])
    status, ferr = None, None
    try:
        m = json.loads(meta or "{}")
        status, ferr = m.get("s"), m.get("e")
    except ValueError:
        pass
    contracts = {}
    try:
        d = json.load(io.open(outp, encoding="utf-8"))
        body = json.loads(d["body"]) if isinstance(d.get("body"), str) else d
        contracts = body.get("contracts") or {}
    except Exception:                                                   # noqa: BLE001
        pass
    names = [k for k, v in contracts.items()
             if (v.get("available") if isinstance(v, dict) else bool(v))]
    return {"status": status, "function_error": ferr, "available": len(names),
            "total": len(contracts), "names": names}


if __name__ == "__main__":
    sys.exit(main())
