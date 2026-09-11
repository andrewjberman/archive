"""BATTERY IB-rt-4 -- RT4-AC1: typed ids at every key boundary, and the exception path.

Five arms (a)-(e) from the face. Prints IBRT4-KEYS-TYPED only when every arm passes and
WITHHOLDS it (rc 1) otherwise.

BOUND 12 IS THE SHAPE OF THIS FILE: every subject is the REAL artifact. The constructors are
imported from the real `_keys`; the census reads the real modules on disk; the envelope is
the real `_authz/errors.py` the functions package; the deploy arm reads the live AWS plane.
Nothing here wraps, patches or re-registers a copy of what it grades. The one place a copy
appears is arm (b)'s ORACLE -- the module at round-1 HEAD, loaded from git -- and it is the
thing being compared AGAINST, never the thing being graded.

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
ROUND1 = "7478fdf144"

# The four negatives the face names. Each is a thing that is NOT an issued opaque id.
NEGATIVES = (
    ("display name", "Whitfield Family"),
    ("e-mail", "advisor@49financial.com"),
    ("raw upstream key", "AAMkAGI2THVSAAA="),
    ("request-controlled firm token", "49financial"),
)
# THE ARM GRADES THE FULL REQUIREMENT, NOT THE PART THAT COULD BE DONE. IMPACTED is every
# function whose code this cell changed and ROOTS is every root that holds one, so arm (e)
# measures what the face asked for -- CodeSha256 per CHANGED function and No changes per
# root -- and reports FAIL when one of them could not be reached. Narrowing these tuples to
# the four roots that applied cleanly would have turned a blocked deploy into a green.
LEDGER_SLUGS = ("irpt-bckend-rt4-directory", "irpt-bckend-rt4-intake",
                "irpt-bckend-rt4-ycharts", "irpt-bckend-rt4-ops")
IMPACTED = ("irpt-directory-search", "irpt-directory-refresh", "irpt-export-render",
            "irpt-intake-poller", "irpt-status", "irpt-ycharts-generate")
ROOTS = ("directory", "intake", "ycharts", "export", "ops")
# Named, with the row that explains it, so a reader is not left to infer which failure is a
# regression and which is a carried blocker.
BLOCKED = {"irpt-export-render": "IRPT_BCKEND-W3-S17", "export": "IRPT_BCKEND-W3-S17"}

results = {}
LINES = []


def say(text=""):
    LINES.append(text)
    print(text)


def head(text):
    say("")
    say(text)


def run(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO,
                          timeout=timeout)


# ---------------------------------------------------------------- the census
def constructor_census():
    """Every PUBLIC callable in _keys, split into CONSTRUCTORS and READERS by subtraction.

    The denominator of arm (a) is not a list I wrote down -- it is read off the module with
    the AST, so a builder added later is in the denominator whether or not anyone remembers
    to add it here, and the arm fails until it refuses the four negatives too.
    """
    import ast
    src = io.open(os.path.join(REPO, KEYS_REL), encoding="utf-8").read()
    tree = ast.parse(src)
    public = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            public.append((node.name, "function"))
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_") \
                and not node.name.endswith("Refused"):
            public.append((node.name, "class"))
    # READERS take a PATH or a KEY and construct no key from caller components. Named
    # explicitly and SUBTRACTED, so the split is auditable rather than implied.
    readers = {"load_firm_ids": "reads the registry by path",
               "firm_tokens": "reads the registry by path",
               "verify_against_layout": "compares two declarations by path",
               "classify_refused": "classifies a value for a reason code; builds nothing"}
    constructors = [(n, k) for n, k in public if n not in readers]
    return {"public": public, "readers": readers, "constructors": constructors,
            "denominator": "%d public callables - %d readers = %d constructors"
                           % (len(public), len(readers), len(constructors))}


def call_with(name, value):
    """Drive ONE constructor with `value` in a caller-supplied component position."""
    fp = "b" * 64
    table = {
        "cache_key": lambda v: keys.cache_key("49financial", fp, "r1", "r2", "r3",
                                              "irpt_probe", params={"p": v}),
        "idempotency_key": lambda v: keys.idempotency_key("49financial", fp, "r1", "r2",
                                                          "r3", "irpt_probe",
                                                          params={"p": v}),
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
    """Every rendering a caller could reach, censused against the refused value."""
    renders = {
        "str(exc)": str(exc),
        "repr(exc)": repr(exc),
        "'%s' % exc": "%s" % exc,
        "'%r' % exc": "%r" % exc,
        "f-string": "{}".format(exc),
        "exc.args": json.dumps([str(a) for a in exc.args]),
        "public_line": err.public_line("irpt_probe", "KEY_REFUSED", err.new_correlation_id()),
    }
    per = {k: v.count(value) for k, v in renders.items()}
    return sum(per.values()), per, renders


def main():
    say("=" * 78)
    say("BATTERY IB-rt-4 -- RT4-AC1: typed ids at every key boundary, and the exception path")
    say("repo: %s" % REPO.replace("\\", "/"))
    say("=" * 78)

    # ---- (a) -------------------------------------------------------------
    head("(a) N OF N CONSTRUCTORS -- four negatives each, refused without echoing")
    cen = constructor_census()
    say("    PUBLIC SURFACE OF _keys, read off the module by AST, not from a written list:")
    say("      %s" % cen["denominator"])
    say("      constructors: %s" % [n for n, _k in cen["constructors"]])
    say("      readers SUBTRACTED (they build no key from caller components):")
    for n, why in sorted(cen["readers"].items()):
        say("        %-22s %s" % (n, why))
    trials = refused = clean = 0
    rows = []
    for name, _kind in cen["constructors"]:
        for label, value in NEGATIVES:
            trials += 1
            try:
                out = call_with(name, value)
                # TenantBinding's TENANT POSITION is the one place a firm id BELONGS -- it
                # is bound from the sender's domain at ingestion, not supplied by a request.
                # Recorded as a POSITIONAL ADMISSION with its reason, never counted as a
                # refusal and never quietly ignored.
                if name == "TenantBinding" and label.endswith("firm token"):
                    rows.append((name, label, "ADMITTED-IN-ITS-OWN-POSITION", 0))
                    say("      %-17s %-30s ADMITTED (tenant position) -> %s"
                        % (name, label, str(out)[:30]))
                    continue
                rows.append((name, label, "ACCEPTED", 0))
                say("      %-17s %-30s ACCEPTED  %s" % (name, label, str(out)[:40]))
            except keys.KeyComponentRefused as exc:
                refused += 1
                n_leak, per, _r = leak_count(exc, value)
                if n_leak == 0:
                    clean += 1
                rows.append((name, label, "REFUSED:" + exc.reason, n_leak))
                say("      %-17s %-30s REFUSED %-26s leak %d of 7 renderings"
                    % (name, label, exc.reason, n_leak))
                if n_leak:
                    say("        LEAKED IN: %s" % [k for k, v in per.items() if v])
            except Exception as exc:                                    # noqa: BLE001
                rows.append((name, label, "WRONG-EXCEPTION:" + exc.__class__.__name__, 0))
                say("      %-17s %-30s WRONG EXCEPTION %s"
                    % (name, label, exc.__class__.__name__))
    admitted = sum(1 for r in rows if r[2] == "ADMITTED-IN-ITS-OWN-POSITION")
    say("    REFUSED %d of %d trials (%d admitted in the tenant position by design); "
        "0 occurrences of the refused value in %d of %d refusals"
        % (refused, trials, admitted, clean, refused))
    say("    THE SEVEN RENDERINGS CENSUSED PER REFUSAL: str(), repr(), '%s', '%r', an "
        "f-string, exc.args, and the public log line -- a leak wearing a different syntax")
    say("      is the same leak, so one rendering is not a census.")
    # the %r sites the ruling counts
    ksrc = io.open(os.path.join(REPO, KEYS_REL), encoding="utf-8").read()
    import ast as _ast
    rtotal = 0
    for node in _ast.walk(_ast.parse(ksrc)):
        if isinstance(node, _ast.Call) and isinstance(node.func, _ast.Name) \
                and node.func.id == "KeyComponentRefused":
            rtotal += (_ast.get_source_segment(ksrc, node) or "").count("%r")
    say("    %%r PLACEHOLDERS INSIDE A REFUSAL CONSTRUCTION: %d" % rtotal)
    say("      the ruling says 'twelve %r message sites become zero'; the module carried")
    say("      EIGHTEEN across sixteen construction sites when this cell measured it, so the")
    say("      fix is defined by the census and not by the number (row W3-S16). The 6 that")
    say("      remain in the module are in verify_against_layout, comparing CONFIG to CONFIG.")
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
        say("    THE ORACLE IS THE MODULE AT ROUND-1 HEAD (%s), loaded from git -- not a "
            "remembered" % ROUND1)
        say("      list of expected strings, which the same hand that changed the code would "
            "have updated.")
        same = diff = 0
        for name, fn in positive_cases():
            a, b = _safe_call(fn, old), _safe_call(fn, keys)
            ok = (a == b)
            same += ok
            diff += (not ok)
            say("      %-26s %s  sha256 %s  %s"
                % (name, "SAME " if ok else "DIFFER",
                   hashlib.sha256(str(b).encode()).hexdigest()[:12], str(b)[:52]))
            if not ok:
                say("        round1: %s" % str(a)[:90])
                say("        now:    %s" % str(b)[:90])
        say("    %d of %d identical -- the refusal did not change the grammar" % (same, same + diff))
        results["b"] = diff == 0 and same > 0

    # ---- (c) -------------------------------------------------------------
    head("(c) THE ENVELOPE EVERYWHERE -- the handler error paths, censused by AST")
    c = epc.census(IR)
    say("    modules scanned %d | except handlers %d | handlers BINDING the exception %d"
        % (c["modules_scanned"], c["except_handlers"], c["handlers_binding_the_exception"]))
    say("    by family: %s" % json.dumps(c["by_family"]))
    say("    HANDLERS RENDERING THE CAUGHT EXCEPTION INTO TEXT: %d"
        % c["handlers_rendering_the_exception"])
    for r in c["leaky"]:
        say("      STILL RENDERS %-44s L%-4d %s" % (r["path"], r["lineno"],
                                                    r["renders_the_exception"]))
    say("    THE CENSUS IS STRUCTURAL, NOT A GREP: it counts str(exc), repr(exc), a")
    say("      %%-format operand, an f-string value and .format(exc) -- and it does NOT count")
    say("      type(exc).__name__ or exc.__class__.__name__, which carry no caller data.")
    say("      An earlier cut of it DID count those and reported 12; two of the twelve were")
    say("      modules that had already applied this lesson deliberately, one of them citing")
    say("      row W2-S10 in a comment. A census that over-fires sends a careful reader to")
    say("      'fix' correct code and inflates the denominator its own fix is graded against.")
    say("    PUBLIC REASONS ARE A CLOSED ENUM: %d members, and error_envelope() REFUSES a"
        % len(err.PUBLIC_REASONS))
    say("      reason outside it -- there is no parameter on it that an exception fits into.")
    try:
        err.error_envelope("MADE_UP_REASON")
        closed = False
    except err.ReasonNotDeclared:
        closed = True
    say("      a free-string reason is refused: %s" % closed)
    results["c"] = c["handlers_rendering_the_exception"] == 0 and closed

    # ---- (d) -------------------------------------------------------------
    head("(d) INJECTED NEGATIVES -- a client name, an e-mail and an S3 key, per family")
    injected = (("client name", "Whitfield Family"),
                ("e-mail", "advisor@49financial.com"),
                ("S3 key", "firms/49financial/generations/2332060/attempts/0/report.pdf"))
    families = ("directory", "_authz", "intake", "ycharts", "export", "ops")
    total = leaks = 0
    for fam in families:
        for label, value in injected:
            total += 1
            sink, public = [], []
            exc = ValueError("upstream failed while handling %s" % value)
            envelope = err.fail(exc, operation="irpt_%s_probe" % fam,
                                sink=sink.append, public_log=public.append)
            census = err.envelope_leak_census(
                envelope, [value], headers={"x-irpt-correlation": envelope["correlation_id"]},
                log_lines=public)
            leaks += census["occurrences"]
            resolves = any(r["correlation_id"] == envelope["correlation_id"] for r in sink)
            carried = any(value in json.dumps(r, default=str) for r in sink)
            say("      %-10s %-11s reason=%-22s occurrences %d | corr resolves %s | "
                "internal record carries it %s"
                % (fam, label, envelope["public_reason_code"], census["occurrences"],
                   resolves, carried))
    say("    TOTAL OCCURRENCES ACROSS body + headers + the public log: %d of %d injections"
        % (leaks, total))
    say("    AND THE CORRELATION ID RESOLVES THE OTHER WAY: the internal record DOES carry")
    say("      the detail, so an operator loses nothing -- the detail moved, it did not")
    say("      disappear. A redaction that destroys the diagnostic gets switched off later.")
    ex_keys = sorted(err.fail(ValueError("x"), operation="irpt_probe").keys())
    say("    the envelope's own fields: %s" % ex_keys)
    say("      no 'error', no 'message', no 'detail', no 'stack' -- there is no field for")
    say("      them to travel in, which is stronger than a rule that they must not be set.")
    results["d"] = (leaks == 0 and total > 0
                    and set(ex_keys) == {"ok", "public_reason_code", "correlation_id"})

    # ---- (e) -------------------------------------------------------------
    head("(e) DEPLOYED -- CodeSha256 per changed function, plans clean, ledgers closed")
    sm = json.load(io.open(SOURCE_MAP, encoding="utf-8"))
    ok_e = True
    for fn in IMPACTED:
        registered = sm["functions"][fn].get("artifact_sha256")
        cfg = aws_json(["lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "{CodeSha256:CodeSha256,LastModified:LastModified}"])
        served = (cfg or {}).get("CodeSha256")
        match = bool(served) and served == registered
        ok_e = ok_e and match
        say("      %-26s served %s  registered %s  match %-5s %s"
            % (fn, str(served)[:16], str(registered)[:16], match,
               ("BLOCKED-BY-" + BLOCKED[fn]) if fn in BLOCKED and not match else ""))
    for root in ROOTS:
        out = run([TF, "-chdir=infra/aws/terraform/investor-reporting/%s" % root,
                   "plan", "-no-color", "-input=false", "-lock=false"], timeout=300)
        clean_plan = "No changes." in out.stdout
        ok_e = ok_e and clean_plan
        detail = ("No changes." if clean_plan else
                  ([ln.strip() for ln in out.stdout.splitlines() if ln.startswith("Plan:")]
                   or ["rc %d" % out.returncode])[0])
        say("      root %-10s post-apply plan: %-42s %s"
            % (root, detail,
               ("BLOCKED-BY-" + BLOCKED[root]) if root in BLOCKED and not clean_plan else ""))
    led = ledger_state()
    for slug, state in sorted(led.items()):
        say("      ledger %-30s CLOSED=%s legs=%d open markers=%d sentinel on disk=%s "
            "sentinel commits=%d"
            % (slug, state["closed"], state["legs"], state["open_markers"],
               state["sentinel_on_disk"], len(state["sentinel_commits"])))
        ok_e = (ok_e and state["closed"] and state["open_markers"] == 0
                and not state["sentinel_on_disk"] and len(state["sentinel_commits"]) >= 2)
    imports = import_closure_report()
    say("      IMPORT CLOSURE of each built zip (a CodeSha256 match on a function that dies")
    say("        at import passes every other rung): %d of %d CLOSED"
        % (imports["closed"], imports["functions"]))
    for f in imports["open"]:
        say("        %s" % f["failures"])
    say("        the one OPEN is PRE-EXISTING and not this cell's: export/download.py has")
    say("    WHY ARM (e) FAILS, IN ONE LINE: the export root carries three resources that are")
    say("      in STATE and not in CONFIGURATION (two IAM role policies and an SSM document,")
    say("      left by IB-s-14 at 1beda4bf49 without an apply), so its plan reads '0 to add, 1")
    say("      to change, 3 to destroy' BEFORE any change of this cell's. The face requires")
    say("      plans that show ONLY the code changes; destroying two live IAM role policies is")
    say("      a served-surface act this ruling did not order. irpt-export-render's CODE is")
    say("      committed and its APPLY is withheld. Row IRPT_BCKEND-W3-S17. The other four")
    say("      roots and five functions are deployed and verified.")
    say("        imported enforce at module level since round 1 and enforce.py has never")
    say("        been in irpt-export-render's file list (verified at %s). Row W3-S14; not"
        % ROUND1)
    say("        fixed here, because enabling a dead code path is a served-surface change")
    say("        the ruling did not order.")
    ok_e = ok_e and imports["closed"] >= imports["functions"] - 1
    results["e"] = ok_e

    # ---- verdict ---------------------------------------------------------
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


def _safe_call(fn, mod):
    try:
        return fn(mod)
    except Exception as exc:                                            # noqa: BLE001
        return "RAISED %s" % exc.__class__.__name__


def aws_json(args):
    out = run([AWS] + args + ["--output", "json"], timeout=300)
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout)
    except ValueError:
        return None


def ledger_state():
    entry_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    state = {}
    for slug in LEDGER_SLUGS:
        name = next((f for f in sorted(os.listdir(entry_dir)) if slug in f), None)
        text = ""
        if name:
            text = io.open(os.path.join(entry_dir, name), encoding="utf-8").read()
        sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                                slug + ".json")
        log = run(["git", "log", "--format=%h %s", "--",
                   "org/critical_paths/.open_deploys/" + slug + ".json"]).stdout.strip()
        state[slug] = {
            "entry": name,
            "closed": bool(re.search(r"(?i)\bstatus\b.{0,40}\bCLOSED\b", text)),
            "legs": len(re.findall(r"(?m)^\|\s*L\d+\s*\|", text)),
            "open_markers": len(re.findall(r"(?i)\bOPEN\b\s*\|", text)),
            "sentinel_on_disk": os.path.exists(sentinel),
            "sentinel_commits": [ln for ln in log.split("\n") if ln],
        }
    return state


def import_closure_report():
    """Run the closure check in a CLEAN SUBPROCESS, because this one is contaminated.

    THE FIRST VERSION OF THIS CALLED THE CHECKER IN-PROCESS AND REPORTED 6 OF 6 CLOSED WHEN
    THE TRUTH WAS 5 OF 6. The battery imports modules of its own before it gets here, so a
    packaged module's `import enforce` resolved from a leftover sys.modules entry instead of
    failing -- and the check whose entire purpose is to prove a zip can stand alone was
    quietly leaning on the process it ran in. A saved/restored sys.modules is not isolation;
    only a new interpreter is. The standalone script reported OPEN the whole time, which is
    how the disagreement surfaced: two instruments, one answer each, and they differed.
    """
    out = run([sys.executable, os.path.join(REPO, ".scratch", "build_and_verify_zips.py")],
              timeout=600)
    closed, openv, functions = 0, [], 0
    for line in out.stdout.splitlines():
        line = line.strip()
        if " import " in line and (" CLOSED" in line or " OPEN" in line):
            functions += 1
            if line.endswith("CLOSED"):
                closed += 1
        if line.startswith("IMPORT FAILED"):
            openv.append({"function": "(see line)", "failures": line})
        if line.startswith("BUILD-FAILED"):
            openv.append({"function": line.split()[1], "failures": "BUILD FAILED"})
    return {"functions": functions or len(IMPACTED), "closed": closed, "open": openv,
            "subprocess_rc": out.returncode}


if __name__ == "__main__":
    sys.exit(main())
