"""check_en.py -- LGIC_ENFORCE round-1 checker. Issuer fixed input (2.0.0_SA_COO~G, L6).

Every mechanical criterion of every LGIC_ENFORCE round-1 task order calls ONE subcommand of this file:

    cd <worktree> && timeout 120 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_en.py <sub>

Each subcommand prints its evidence lines, then exactly one line `VERDICT: <PASS-...|FAIL-...>`.
Exit code: 0 on PASS, 1 on FAIL. (LGIC_NAMING's checker exited 0 either way; its workers flagged it twice.)
The criterion's <expect> matches the VERDICT line, so the verdict is decided by a match, never by the worker.

`python check_en.py --list` prints every subcommand. `python check_en.py selftest-negative` runs every
subcommand and asserts that NONE prints PASS on a tree where the cells have not run (the issuer's
negative arm, run before issuance). Stdlib only. No non-ASCII.
"""
import fnmatch
import glob
import hashlib
import importlib.machinery
import importlib.util
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

D = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"
FI = D + "/2.0.0_SA_COO~G/fixed_inputs"
REG = "infra/logic/registry"
OPAL = "lib/opal_naming.py"
CHAN = "org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md"
TF49 = "infra/aws/terraform/shared-infra/s3-49financial.tf"
MODULE = "infra/aws/terraform/modules/opal_name"
LEDGER_SLUG = "lgic-enforce-fence-49financial"
SENTINEL = "org/critical_paths/.open_deploys/" + LEDGER_SLUG + ".json"
GATE = ".tools/naming-gate.py"
ENFORCE_FILE = "org/mcp/naming-gate.enforce"
VERDICT_LOG = "org/mcp/naming-gate-verdicts.log"
RULE = "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md"
BUCKET49 = "opal-data-49financial"
FOUR_BUCKETS = ["opal-data-bd", "opal-data-inf", "opal-data-cot", "opal-data-49financial"]
WINDOW_START = "2026-09-14T02:33:09Z"
PROBES = ["mdpf-49f-fenceprobe-role", "mdpf-cot-fenceprobe-role", "mdpf-fenceprobe-role"]
OLD_PATTERNS = ["role/cot-*", "role/inf-*", "role/mdpf-*", "role/opal-assets-mdpf-*"]
DEC5 = [
    ("data/firm_registry.json", None),
    ("infra/aws/lambda-edge/_shared/firm-config.mjs", 65),
    ("data/assets/scripts/gold/investor_reporting/directory_runner.py", 170),
    ("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py", 145),
    ("infra/aws/lambda/investor-reporting/_authz/loaders.py", 43),
    ("data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py", 57),
    (".tools/ds-precommit-check.py", 68),
    (".tools/ds-precommit-check.py", 110),
]
VIEW_OF = {  # EN-v-<n> -> the carrier paths it owns
    "1": ["data/firm_registry.json"],
    "2": ["infra/aws/lambda-edge/_shared/firm-config.mjs"],
    "3": ["data/assets/scripts/gold/investor_reporting/directory_runner.py",
          "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"],
    "4": ["infra/aws/lambda/investor-reporting/_authz/loaders.py"],
    "5": ["data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py"],
    "6": [".tools/ds-precommit-check.py"],
}
CONSUMER_TESTS = {
    "1": [["python", "-m", "pytest", "-q", "infra/aws/lambda/investor-reporting/_keys/tests/test_keys.py",
           "infra/aws/lambda/investor-reporting/_gate/tests/test_policy_completeness.py",
           "infra/aws/lambda/investor-reporting/_contracts/tests/test_seam_paired.py",
           "org/modules/graph/tests/test_comp_keys.py"]],
    "2": [["bun", "test", "test/"], "infra/aws/lambda-edge/shared-advisor-router"],
    "3": [["python", "-m", "pytest", "-q", "data/assets/scripts/gold/investor_reporting/tests/test_directory_runner.py"]],
    "4": [["python", "-m", "pytest", "-q", "infra/aws/lambda/investor-reporting/_authz/tests"]],
    "6": [["python", ".tools/ds-precommit-check.py", "lib/trading_calendar.py"]],
}
VERDICTS = {"CONFORMANT", "ALIAS", "OUT-OF-PATTERN", "NOT-GRADED"}


# ------------------------------------------------------------------ helpers
def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)
    sys.exit(0 if verdict.startswith("PASS-") else 1)


def read(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8").replace("\r\n", "\n")


def fenced_json(path):
    """The FIRST ```json fence of a record, parsed; None when the file or the fence is absent or broken."""
    if not os.path.isfile(path):
        return None
    m = re.search(r"```json\n(.*?)\n```", read(path), re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def run(cmd, cwd=None, env=None, timeout=110, stdin=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    try:
        p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, input=stdin)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds" % timeout
    except OSError as exc:
        return 127, "NOT RUNNABLE: %s" % exc


def git(*args):
    return run(["git"] + list(args))


def run_bash(script_args, env=None, timeout=110):
    """Run a bash script by the ABSOLUTE Git Bash the estate's resolver names (.tools/git_bash_resolver.py; CLAUDE.md:
    Python shelling to bash goes through it). A bare 'bash' on this box resolves to the WSL launcher (row
    LGIC_ENFORCE-W3-S5), and there is no aws.exe, only the .tools/aws shim, so the aws CLI runs as a bash script too
    (row LGIC_ENFORCE-W1-S16)."""
    try:
        b = load_module(".tools/git_bash_resolver.py", "git_bash_resolver_under_check").git_bash()
    except Exception as exc:  # noqa: BLE001
        return 127, "NOT RUNNABLE: the Git Bash resolver failed: %s" % exc
    if not b:
        return 127, "NOT RUNNABLE: .tools/git_bash_resolver.py found no Git Bash"
    return run([b] + list(script_args), env=env, timeout=timeout)


def load_module(path, modname, extra_path=None):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    added = []
    for p in ([extra_path] if extra_path else []) + [os.path.dirname(os.path.abspath(path))]:
        if p and p not in sys.path:
            sys.path.insert(0, p)
            added.append(p)
    try:
        loader = importlib.machinery.SourceFileLoader(modname, path)
        spec = importlib.util.spec_from_loader(modname, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        return mod
    finally:
        for p in added:
            if p in sys.path:
                sys.path.remove(p)


def opal():
    return load_module(OPAL, "opal_naming_under_check")


def registry_hash(reg_dir=REG):
    h = hashlib.sha256()
    for name in sorted(n for n in os.listdir(reg_dir) if n.endswith(".json")):
        h.update(name.encode("utf-8") + b"\n")
        with open(os.path.join(reg_dir, name), "rb") as fh:
            h.update(fh.read().replace(b"\r\n", b"\n"))
    return h.hexdigest()


def _first_line_matching(lines, pat):
    """The 0-based index of the first line matching pat, or -1."""
    return next((i for i, ln in enumerate(lines) if re.search(pat, ln)), -1)


def spawn_base():
    rc, out = git("merge-base", "HEAD", "CLOUD")
    return out.strip() if rc == 0 else ""


def channel_ids():
    if not os.path.isfile(CHAN):
        return set()
    ids = set()
    for m in re.finditer(r"```json\n(.*?)\n```", read(CHAN), re.S):
        try:
            ids.update(r.get("id") for r in json.loads(m.group(1)))
        except ValueError:
            pass
    return ids


def aws_json(args):
    rc, out = run_bash([".tools/aws"] + args + ["--output", "json"], timeout=60)
    if rc != 0:
        return None, out
    try:
        return json.loads(out[out.index("{"):] if "{" in out else out), out
    except ValueError:
        return None, out


# ---------------------------------------------------------- carrier exports (DELTA=0)
def exports_of(path, file_path):
    """The EXPORTED content of one carrier, read from file_path (a copy or the live file) as if it lived at path."""
    orig_dir = os.path.dirname(os.path.abspath(path))
    if path.endswith(".json"):
        obj = json.loads(read(file_path))
        if isinstance(obj, dict):
            obj.pop("_generated", None)
        return obj
    if path.endswith(".mjs"):
        runner = os.path.join(tempfile.mkdtemp(), "x.mjs")
        with open(runner, "w", encoding="utf-8") as fh:
            fh.write("import { pathToFileURL } from 'node:url';\n"
                     "const m = await import(pathToFileURL(process.argv[2]).href);\n"
                     "console.log(JSON.stringify(m.FIRM_CONFIG));\n")
        rc, out = run(["node", runner, os.path.abspath(file_path)])
        if rc != 0:
            raise RuntimeError("node could not load %s: %s" % (file_path, out[-300:]))
        return json.loads(out.strip().splitlines()[-1])
    mod = load_module(file_path, "carrier_" + hashlib.md5(file_path.encode()).hexdigest()[:8], extra_path=orig_dir)
    if path.endswith("ds-precommit-check.py"):
        return {k: sorted(map(repr, getattr(mod, k).items())) if isinstance(getattr(mod, k), dict) else repr(getattr(mod, k))
                for k in ("_CROSS_FIRM_FOREIGN_BUCKETS", "_CROSS_FIRM_FOREIGN_KEY_PREFIXES")}
    if "firm_bucket_map" in dir(mod) and path.endswith(("directory_runner.py", "holdings_snapshot.py")):
        return mod.firm_bucket_map()
    probe = ["49financial", "49f", "bd", "inflection", "inf", "cottonwood", "cot", "demo", "mdpf", "opal", "no-such-firm"]
    fn = getattr(mod, "bucket_for", None) or getattr(mod, "resolve_firm", None)
    if fn is None:
        raise RuntimeError("no exported function found in %s" % file_path)
    res = {}
    for t in probe:
        try:
            res[t] = repr(fn(t))
        except Exception as exc:  # the exception CLASS is part of the export
            res[t] = "raises " + type(exc).__name__
    return res


# ------------------------------------------------------------------ EN-c-1
def c1():
    d = fenced_json(D + "/CARRIER_CENSUS.md")
    return d if isinstance(d, dict) else None


def c1_denominator():
    d = c1()
    den = (d or {}).get("denominator", {})
    ok = d and d.get("instrument") and int(den.get("files_scanned", 0)) > 0 and int(den.get("hits", 0)) > 0
    say("PASS-DENOMINATOR" if ok else "FAIL-NO-DENOMINATOR", "INSTRUMENT: %s  DENOMINATOR: %s" % ((d or {}).get("instrument"), den))


def c1_dec5():
    d = c1() or {}
    have = {(c.get("path"), c.get("line")) for c in d.get("carriers", [])}
    paths = {c.get("path") for c in d.get("carriers", [])}
    missing = []
    for p, ln in DEC5:
        if ln is None:
            if p not in paths:
                missing.append(p)
        elif not any(hp == p and isinstance(hl, int) and abs(hl - ln) <= 3 for hp, hl in have):
            missing.append("%s:%s" % (p, ln))
    say("PASS-DEC5-PRESENT" if d and not missing else "FAIL-DEC5-MISSING", "DEC-5 DEFINITIONS: 8  PRESENT: %d  MISSING: %s" % (8 - len(missing), missing))


def c1_partition():
    d = c1() or {}
    n = len(d.get("carriers", [])) + len(d.get("excluded", []))
    hits = int(d.get("denominator", {}).get("hits", -1))
    no_reason = [e.get("path") for e in d.get("excluded", []) if not e.get("reason")]
    ok = d and n == hits and not no_reason
    say("PASS-PARTITIONED" if ok else "FAIL-NOT-PARTITIONED", "HITS: %d  CARRIERS+EXCLUDED: %d  EXCLUDED WITHOUT REASON: %s" % (hits, n, no_reason[:5]))


def c1_extra_filed():
    d = c1()
    if not d:
        say("FAIL-NO-CENSUS", "CARRIER_CENSUS.md absent or has no json fence")
    dec5_paths = {p for p, _ in DEC5}
    extra = ["%s:%s" % (c.get("path"), c.get("line")) for c in d.get("carriers", []) if c.get("path") not in dec5_paths]
    rows = d.get("outside_dec5_rows", {})
    ids = channel_ids()
    unfiled = [x for x in extra if rows.get(x) not in ids]
    say("PASS-EXTRA-FILED" if not unfiled else "FAIL-EXTRA-UNFILED", "CARRIERS OUTSIDE DEC-5: %d  FILED AS A ROW: %d  UNFILED: %s" % (len(extra), len(extra) - len(unfiled), unfiled[:5]))


# ------------------------------------------------------------------ EN-c-2
def c2():
    d = fenced_json(D + "/FENCE_WRITER_CENSUS.md")
    return d if isinstance(d, dict) else {}


def c2_buckets():
    b = sorted(c2().get("buckets", {}))
    say("PASS-FOUR-BUCKETS" if b == sorted(FOUR_BUCKETS) else "FAIL-BUCKETS", "BUCKETS: %s" % b)


def c2_tokens():
    d = c2()
    rows = [r for v in d.get("buckets", {}).values() for k in ("granted", "seen") for r in v.get(k, [])]
    bad = [r.get("principal") for r in rows if not r.get("principal") or not r.get("token")]
    say("PASS-TOKENS" if rows and not bad else "FAIL-TOKENS", "PRINCIPAL ROWS: %d  WITHOUT A TOKEN OR 'none': %s" % (len(rows), bad[:5]))


def c2_window():
    w = c2().get("window", {})
    ok = w.get("start") == WINDOW_START and isinstance(w.get("end"), str) and w.get("end") > WINDOW_START
    say("PASS-WINDOW" if ok else "FAIL-WINDOW", "WINDOW: %s  (start must be %s)" % (w, WINDOW_START))


def c2_unobserved():
    s = str(c2().get("unobserved_writes", ""))
    say("PASS-STATED" if "platinum/firm/" in s else "FAIL-NOT-STATED", "UNOBSERVED_WRITES: %s" % s[:200])


def c2_denominators():
    d = c2()
    bad = []
    for b, v in d.get("buckets", {}).items():
        den = v.get("denominators", {})
        for k in ("granted", "seen"):
            if den.get(k) != len(v.get(k, [])):
                bad.append("%s.%s" % (b, k))
    say("PASS-DENOMINATORS" if d.get("buckets") and not bad else "FAIL-DENOMINATORS", "MISMATCHED: %s" % bad)


# ------------------------------------------------------------------ EN-r-1
FILES5 = ["systems.json", "scopes.json", "tiers.json", "exemptions.json", "remediations.json"]


def r1_parse():
    bad = []
    for f in FILES5:
        p = os.path.join(REG, f)
        try:
            json.loads(read(p))
        except (OSError, ValueError) as exc:
            bad.append("%s (%s)" % (f, type(exc).__name__))
    say("PASS-PARSE" if not bad else "FAIL-PARSE", "FILES: 5  FAILING: %s" % bad)


def _validate(fixture):
    return run([sys.executable, OPAL, "validate", "--systems-file", fixture])


def r1_refuse_owner():
    rc, out = _validate(FI + "/tests/r1/systems_missing_owner.json")
    ok = rc == 1 and "owner_directive" in out
    say("PASS-REFUSES-MISSING-OWNER" if ok else "FAIL-ACCEPTED-MISSING-OWNER", "rc=%d  %s" % (rc, out.strip()[-300:]))


def r1_refuse_firm():
    rc, out = _validate(FI + "/tests/r1/systems_firm_key.json")
    ok = rc == 1 and "cottonwood" in out
    say("PASS-REFUSES-FIRM-SYSTEM" if ok else "FAIL-ACCEPTED-FIRM-SYSTEM", "rc=%d  %s" % (rc, out.strip()[-300:]))


def r1_scopes():
    try:
        rows = json.loads(read(os.path.join(REG, "scopes.json")))
    except (OSError, ValueError):
        say("FAIL-NO-SCOPES", "scopes.json absent or unparseable")
    rows = rows.get("scopes", rows) if isinstance(rows, dict) else rows
    rows = list(rows.values()) if isinstance(rows, dict) else rows
    bad = [r.get("key", "?") for r in rows if not all(r.get(k) for k in ("long", "short", "tenancy", "bucket"))]
    say("PASS-SCOPE-FIELDS" if rows and not bad else "FAIL-SCOPE-FIELDS", "SCOPE ROWS: %d  MISSING long/short/tenancy/bucket: %s" % (len(rows), bad))


def r1_bd():
    bad = []

    def walk(o, trail):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, trail + [str(k)])
        elif isinstance(o, list):
            for v in o:
                walk(v, trail)
        elif isinstance(o, str) and "bd" in re.split(r"[-_/.]", o):
            if not any(("alias" in t.lower() or "refused" in t.lower()) for t in trail):
                bad.append("/".join(trail) + "=" + o)
    for f in FILES5:
        try:
            walk(json.loads(read(os.path.join(REG, f))), [f])
        except (OSError, ValueError):
            say("FAIL-PARSE", "cannot read %s" % f)
    say("PASS-BD-CONTAINED" if not bad else "FAIL-BD-OUTSIDE-ALIASES", "OCCURRENCES OUTSIDE AN alias/refused FIELD: %s" % bad[:6])


def _compare_carriers(paths, left, right):
    """left/right: callables path -> file path. Returns (equal, mismatched)."""
    eq, bad = [], []
    for p in paths:
        try:
            a, b = exports_of(p, left(p)), exports_of(p, right(p))
            (eq if a == b else bad).append(p)
        except Exception as exc:
            bad.append("%s (%s: %s)" % (p, type(exc).__name__, str(exc)[:120]))
    return eq, bad


def r1_generate():
    out = ".scratch/en_gen_check"
    shutil.rmtree(out, ignore_errors=True)
    rc, txt = run([sys.executable, OPAL, "generate", "--out", out])
    if rc != 0:
        say("FAIL-GENERATE-RC", "rc=%d  %s" % (rc, txt.strip()[-300:]))
    paths = sorted({p for p, _ in DEC5})
    eq, bad = _compare_carriers(paths, lambda p: p, lambda p: os.path.join(out, p))
    say("PASS-DELTA0-ALL" if not bad else "FAIL-DELTA-NONZERO", "CARRIER FILES: %d  EXPORTS EQUAL: %d  DIFFER: %s" % (len(paths), len(eq), bad))


# ------------------------------------------------------------------ EN-b-1
def _call(expr):
    try:
        o = opal()
        return eval(expr, {"o": o}), None
    except Exception as exc:
        return None, "%s: %s" % (type(exc).__name__, exc)


def b1_key():
    v, err = _call('o.key("orion", "inflection", "bronze", "positions", "date=2026-09-13")')
    exp = "orion/inflection/bronze/positions/date=2026-09-13"
    say("PASS-KEY-EXACT" if v == exp else "FAIL-KEY", "RETURNED: %r  EXPECTED: %r  %s" % (v, exp, err or ""))


def b1_address():
    v, err = _call('o.address("orion", "inflection", "bronze", "positions", "date=2026-09-13")')
    exp = "s3://opal-data-assets/orion/inflection/bronze/positions/date=2026-09-13"
    say("PASS-ADDRESS-EXACT" if v == exp else "FAIL-ADDRESS", "RETURNED: %r  EXPECTED: %r  %s" % (v, exp, err or ""))


def b1_no_bucket():
    try:
        o = opal()
        params = {f: list(inspect.signature(getattr(o, f)).parameters) for f in ("key", "address")}
    except Exception as exc:
        say("FAIL-NOT-LOADABLE", "%s: %s" % (type(exc).__name__, exc))
    bad = [f for f, ps in params.items() if any("bucket" in p.lower() for p in ps)]
    say("PASS-NO-BUCKET-PARAM" if not bad else "FAIL-BUCKET-PARAM", "PARAMETERS: %s" % params)


def b1_name():
    v, err = _call('o.name("mdpf", "cottonwood", "publisher", "role")')
    say("PASS-NAME-EXACT" if v == "mdpf-cot-publisher-role" else "FAIL-NAME", "RETURNED: %r  EXPECTED: 'mdpf-cot-publisher-role'  %s" % (v, err or ""))


CONTROLS = [("cot-bd-session-daily-et", "SCHEDULE", "OUT-OF-PATTERN", None),
            ("blackdiamond/49f/credentials", "SECRET", "CONFORMANT", None),
            ("CloudWatchLogs", "IAM_POLICY", "OUT-OF-PATTERN", None),
            ("opal-data-inf/silver/x", "S3Key", "OUT-OF-PATTERN", "{source}")]


def b1_controls():
    try:
        o = opal()
    except Exception as exc:
        say("FAIL-NOT-LOADABLE", "%s: %s" % (type(exc).__name__, exc))
    good, lines = 0, []
    for n, t, want, must_contain in CONTROLS:
        try:
            v, canon = o.grade(n, t)
            ok = v == want and (must_contain is None or must_contain in str(canon))
        except Exception as exc:
            v, canon, ok = "raises " + type(exc).__name__, "", False
        good += ok
        lines.append("  %s (%s): %s -> %s  %s" % (n, t, v, canon, "OK" if ok else "WRONG, want " + want + (" naming " + must_contain if must_contain else "")))
    say("PASS-CONTROLS-4-OF-4" if good == 4 else "FAIL-CONTROLS", "CONTROLS: 4  CORRECT: %d" % good, *lines)


def b1_whole_segment():
    try:
        o = opal()
        v, canon = o.grade("mdpf-info-publisher-lambda", "LAMBDA")
    except Exception as exc:
        say("FAIL-NOT-GRADED", "%s: %s" % (type(exc).__name__, exc))
    segs = re.split(r"[-_/.]", str(canon))
    ok = "inf" not in segs and "info" in segs
    say("PASS-WHOLE-SEGMENT" if ok else "FAIL-SUBSTRING-MATCH", "grade('mdpf-info-publisher-lambda', LAMBDA) = %s -> %s  (inf must not become a slot; info must survive)" % (v, canon))


def b1_agree():
    cases = (fenced_json(RULE) or {}).get("worked_cases", [])
    try:
        o = opal()
    except Exception as exc:
        say("FAIL-NOT-LOADABLE", "%s: %s" % (type(exc).__name__, exc))
    bad = []
    for c in cases:
        want = c.get("verdict")
        try:
            v, canon = o.grade(c["name"], c["type"])
            if want == "RAISE":
                bad.append((c["name"], "RAISE", v))
            elif v != want or (want in ("ALIAS", "OUT-OF-PATTERN") and canon != c.get("canonical_form")):
                bad.append((c["name"], "%s %s" % (want, c.get("canonical_form")), "%s %s" % (v, canon)))
        except Exception as exc:
            if want != "RAISE":
                bad.append((c["name"], want, "raises " + type(exc).__name__))
    for b in bad[:12]:
        print("DISAGREE: %s  rule=%s  grade()=%s" % b)
    say("PASS-AGREE-ALL" if cases and not bad else "FAIL-DISAGREE", "WORKED CASES: %d  AGREE: %d  DISAGREE: %d" % (len(cases), len(cases) - len(bad), len(bad)))


def b1_tests():
    rc, out = run([sys.executable, "-m", "pytest", "-q", "lib/tests/test_opal_naming.py"])
    tail = out.strip().splitlines()[-1:] if out.strip() else ["(no output)"]
    say("PASS-TESTS" if rc == 0 else "FAIL-TESTS", "rc=%d  %s" % (rc, tail[0]))


# ------------------------------------------------------------------ EN-m-1
def _tf_files(d):
    return [os.path.join(dp, f) for dp, _, fs in os.walk(d) for f in fs if f.endswith(".tf")]


def m1_no_external():
    fs = _tf_files(MODULE)
    ext = [f for f in fs if re.search(r'data\s+"external"', read(f))]
    say("PASS-NO-EXTERNAL" if fs and not ext else "FAIL-EXTERNAL-OR-EMPTY", ".tf FILES: %d  WITH data \"external\": %s" % (len(fs), ext))


def _main_terraform():
    rc, common = git("rev-parse", "--path-format=absolute", "--git-common-dir")
    return os.path.join(os.path.dirname(common.strip()), ".tools", "terraform.exe")


def m1_vectors():
    try:
        vec = json.loads(read(os.path.join(MODULE, "tests", "vectors.json")))
        rows = vec if isinstance(vec, list) else vec.get("vectors", [])
    except (OSError, ValueError):
        say("FAIL-NO-VECTORS", "%s/tests/vectors.json absent or unparseable" % MODULE)
    tf = os.environ.get("SAFE_APPLY_TERRAFORM") or _main_terraform()
    rc1, o1 = run([tf, "-chdir=" + MODULE, "init", "-backend=false", "-input=false"])
    rc2, o2 = run([tf, "-chdir=" + MODULE, "test"])
    m = re.search(r"(\d+) passed, (\d+) failed", o2)
    ok = rc1 == 0 and rc2 == 0 and m and int(m.group(1)) >= len(rows) > 0 and int(m.group(2)) == 0
    say("PASS-VECTORS-MATCH" if ok else "FAIL-VECTORS", "VECTORS: %d  terraform test: %s  (init rc=%d, test rc=%d)" % (len(rows), m.group(0) if m else o2.strip()[-200:], rc1, rc2))


def m1_header():
    fs = [f for f in _tf_files(MODULE) if "GENERATED" in read(f)[:600]]
    h = registry_hash()[:16] if os.path.isdir(REG) else "NO-REGISTRY"
    ok = any(h in read(f)[:600] for f in fs)
    say("PASS-GENERATED-HEADER" if ok else "FAIL-HEADER", "GENERATED FILES: %s  CURRENT REGISTRY HASH: %s" % (fs, h))


# ------------------------------------------------------------------ EN-f-1, EN-f-2
def _writers_49():
    d = c2().get("buckets", {}).get(BUCKET49, {})
    return sorted({r.get("principal") for k in ("granted", "seen") for r in d.get(k, []) if r.get("principal")})


def f1_covered():
    try:
        pats = opal().fence_patterns("49financial")
        ex = json.loads(read(os.path.join(REG, "exemptions.json")))
    except Exception as exc:
        say("FAIL-NOT-EVALUABLE", "%s: %s" % (type(exc).__name__, exc))
    rows = ex.get(BUCKET49, ex.get("exemptions", {}).get(BUCKET49, [])) if isinstance(ex, dict) else ex
    named = {r.get("principal"): r for r in rows if isinstance(r, dict)}
    writers = _writers_49()
    bad = []
    for w in writers:
        arn = w if w.startswith("arn:") else "arn:aws:iam::313476888478:role/" + w
        by_pattern = any(fnmatch.fnmatchcase(arn, p) for p in pats)
        r = named.get(w) or named.get(arn)
        by_row = bool(r and r.get("reason") and r.get("signoff_ref"))
        if not (by_pattern or by_row):
            bad.append(w)
    say("PASS-EVERY-WRITER-COVERED" if writers and not bad else "FAIL-UNCOVERED", "WRITERS OF %s: %d  COVERED: %d  UNCOVERED: %s  PATTERNS: %s" % (BUCKET49, len(writers), len(writers) - len(bad), bad[:6], pats))


def _deny_region():
    t = read(TF49) if os.path.isfile(TF49) else ""
    i = t.find("DenyForeignFirmPrincipals")
    return t[i:i + 2500] if i >= 0 else ""


def f1_no_typed_list():
    r = _deny_region()
    typed = [p for p in OLD_PATTERNS if p in r] + re.findall(r'"arn:aws:iam::\d+:role/[^"]*"', r)
    ok = r and not typed and re.search(r"module\.opal_name|local\.", r)
    say("PASS-NO-TYPED-LIST" if ok else "FAIL-TYPED-LIST", "DENY REGION FOUND: %s  TYPED ARN LITERALS: %s" % (bool(r), typed[:6]))


def _worker_file(name):
    hits = [os.path.join(dp, f) for dp, _, fs in os.walk(D) for f in fs if f == name and "2.0.0_SA_COO~G" not in dp]
    return sorted(hits)[-1] if hits else None


def f1_plan():
    p = _worker_file("fence_plan.json")
    try:
        plan = json.loads(read(p))
    except (TypeError, OSError, ValueError):
        say("FAIL-NO-PLAN", "no fence_plan.json under a worker's deliverables folder")
    allowed = {("update", "aws_s3_bucket_policy"): 1, ("create", "aws_iam_role"): 3, ("create", "aws_iam_role_policy"): 3}
    seen, other, roles = {}, [], []
    for rc in plan.get("resource_changes", []):
        acts = [a for a in rc.get("change", {}).get("actions", []) if a != "no-op"]
        if not acts:
            continue
        k = (acts[0], rc.get("type"))
        seen[k] = seen.get(k, 0) + 1
        if k not in allowed:
            other.append("%s %s" % (acts, rc.get("address")))
        if k == ("create", "aws_iam_role"):
            roles.append((rc.get("change", {}).get("after") or {}).get("name"))
    over = [k for k, n in seen.items() if k in allowed and n > allowed[k]]
    ok = not other and not over and sorted(roles) == sorted(PROBES) and seen.get(("update", "aws_s3_bucket_policy")) == 1
    say("PASS-PLAN-SCOPED" if ok else "FAIL-PLAN-SCOPE", "PLAN: %s  CHANGES: %s  ROLES: %s  OTHER: %s" % (p, seen, roles, other[:5]))


def _live_policy():
    d, out = aws_json(["s3api", "get-bucket-policy", "--bucket", BUCKET49])
    if not d:
        return None, out
    try:
        return json.loads(d.get("Policy", "")), out
    except ValueError:
        return None, out


def f1_prior():
    p = D + "/FENCE_PRIOR_POLICY.json"
    try:
        prior = json.loads(read(p))
    except (OSError, TypeError, ValueError):
        return say("FAIL-NO-PRIOR", "%s absent or unparseable" % p)
    live, raw = _live_policy()
    ok = live is not None and prior == live
    say("PASS-PRIOR-VERBATIM" if ok else "FAIL-PRIOR-DIFFERS", "PRIOR == LIVE (read now): %s  %s" % (live is not None and prior == live, "" if live is not None else raw[-200:]))


def _sentinel():
    try:
        return json.loads(read(SENTINEL))
    except (OSError, ValueError):
        return None


def f1_ledger_open():
    s = _sentinel()
    legs = {leg.get("id"): leg for leg in (s or {}).get("legs", [])}
    l1 = legs.get("L1", {})
    proof_hash = re.findall(r"\b[0-9a-f]{10,40}\b", str(l1.get("proof", "")))
    exists = bool(proof_hash) and git("cat-file", "-e", proof_hash[0] + "^{commit}")[0] == 0
    ok = s and s.get("status") == "OPEN" and set(legs) >= {"L1", "L2", "L3", "L4"} and exists
    say("PASS-LEDGER-OPEN" if ok else "FAIL-LEDGER", "SENTINEL: %s  STATUS: %s  LEGS: %s  L1 PROOF COMMIT EXISTS: %s" % (SENTINEL, (s or {}).get("status"), sorted(legs), exists))


def _entry_path():
    """The ledger entry's path. The sentinel names it while the deploy is open; deploy_ledger.py close deletes the
    sentinel, so a closed deploy is found by its slug under change_management/ (row LGIC_ENFORCE-W1-S18). More than one
    match is no answer: the path stays empty and every reader of it fails."""
    p = (_sentinel() or {}).get("entry_path")
    if p:
        return p
    hits = sorted(glob.glob("org/critical_paths/change_management/*_%s_deploy_completion.md" % LEDGER_SLUG))
    return hits[0].replace("\\", "/") if len(hits) == 1 else ""


def _entry_text():
    p = _entry_path()
    return read(p) if p and os.path.isfile(p) else ""


def _entry_history_text():
    """Every committed version of the ledger entry, joined. deploy_ledger.py rebuilds the entry from its sentinel on each
    close-leg, so SIGNOFF lines written before the apply are gone from the file after L2 closes (row
    LGIC_ENFORCE-W1-S17); the criterion's question -- did both seats sign before the apply -- is read from the history."""
    p = _entry_path()
    if not p:
        return ""
    rc, out = git("log", "--format=%H", "--", p)
    texts = []
    for h in (out.split() if rc == 0 else []):
        r, body = git("show", "%s:%s" % (h, p))
        if r == 0:
            texts.append(body)
    return "\n".join(texts)


def _l2_closed_at():
    """L2's close time: from the sentinel while it exists, else from the entry's own log line, which the close keeps."""
    l2 = {leg.get("id"): leg for leg in (_sentinel() or {}).get("legs", [])}.get("L2", {})
    if l2.get("closed_at"):
        return str(l2["closed_at"])
    m = re.search(r"^- (\d{8}T\d{6}Z) LEG L2 closed:", _entry_text(), re.M)
    return m.group(1) if m else ""


def f2_signoff():
    t = _entry_text() + "\n" + _entry_history_text()
    applied = _l2_closed_at()
    signs = dict(re.findall(r"^SIGNOFF (1\.0\.0_SA_CTO|2\.0\.0_SA_COO~G) (\d{8}T\d{6}Z)", t, re.M))
    ok = len(signs) == 2 and applied and all(ts < applied for ts in signs.values())
    say("PASS-SIGNED-BEFORE-APPLY" if ok else "FAIL-SIGNOFF", "SIGNOFF LINES: %s  APPLY (L2 closed_at): %s" % (signs, applied or "none"))


def f2_policy_live():
    live, raw = _live_policy()
    if live is None:
        return say("FAIL-NO-LIVE-POLICY", raw[-200:])
    txt = json.dumps(live)
    sids = [st.get("Sid") for st in live.get("Statement", [])]
    stale = [p for p in OLD_PATTERNS if p in txt]
    ok = "DenyForeignFirmPrincipals" in sids and not stale and "49f" in txt
    say("PASS-POLICY-LIVE" if ok else "FAIL-POLICY", "SIDS: %s  OLD PATTERNS STILL PRESENT: %s  CARRIES 49f: %s" % (sids, stale, "49f" in txt))


def _probe(role, want):
    d = fenced_json(D + "/FENCE_PROBES.md") or {}
    rows = [p for p in d.get("probes", []) if p.get("role") == role]
    ok = rows and all(p.get("result") == want and p.get("evidence") for p in rows)
    return ok, rows


def f2_probe_49f():
    ok, rows = _probe("mdpf-49f-fenceprobe-role", "ALLOWED")
    say("PASS-49F-READS" if ok else "FAIL-49F-PROBE", "ROWS: %s" % rows)


def f2_probe_cot():
    ok, rows = _probe("mdpf-cot-fenceprobe-role", "DENIED")
    say("PASS-COT-DENIED" if ok else "FAIL-COT-PROBE", "ROWS: %s" % rows)


def f2_probe_unscoped():
    ok, rows = _probe("mdpf-fenceprobe-role", "DENIED")
    say("PASS-UNSCOPED-DENIED" if ok else "FAIL-UNSCOPED-PROBE", "ROWS: %s" % rows)


def f2_probe_exempt():
    d = fenced_json(D + "/FENCE_PROBES.md") or {}
    rows = [p for p in d.get("probes", []) if p.get("kind") == "exempt"]
    ok = rows and all(p.get("result") == "ALLOWED" and p.get("evidence") and p.get("role") not in PROBES for p in rows)
    say("PASS-EXEMPT-ALLOWED" if ok else "FAIL-EXEMPT-PROBE", "ROWS: %s" % rows)


def f2_removed():
    if not (fenced_json(D + "/FENCE_PROBES.md") or {}).get("probes"):
        return say("FAIL-NO-PROBES-RUN", "FENCE_PROBES.md has no probes: roles that were never created are not 'removed'")
    res = {}
    for r in PROBES:
        rc, out = run_bash([".tools/aws", "iam", "get-role", "--role-name", r], timeout=40)
        res[r] = "ABSENT" if rc != 0 and "NoSuchEntity" in out else ("PRESENT" if rc == 0 else "UNREAD: " + out.strip()[-80:])
    ok = all(v == "ABSENT" for v in res.values())
    say("PASS-PROBES-REMOVED" if ok else "FAIL-PROBES-REMAIN", "PROBE ROLES: %s" % res)


def f2_closed():
    """Closed = the sentinel is gone (or reads CLOSED) AND the entry carries both the tool's CLOSED status and the order's
    appended CLOSED line. The entry is found by slug once the close has deleted the sentinel (row LGIC_ENFORCE-W1-S18)."""
    s = _sentinel()
    p = _entry_path()
    t = _entry_text()
    entry_closed = bool(re.search(r"^\*\*Status:\*\* CLOSED\b", t, re.M)) and bool(re.search(r"^CLOSED \d{8}T\d{6}Z", t, re.M))
    ok = (s is None or s.get("status") == "CLOSED") and entry_closed
    say("PASS-LEDGER-CLOSED" if ok else "FAIL-LEDGER-OPEN", "SENTINEL: %s  ENTRY: %s  ENTRY CLOSED: %s" % ("absent" if s is None else s.get("status"), p or "not found", entry_closed))


# ------------------------------------------------------------------ EN-v-1..6
def _v_header(n):
    h = registry_hash()[:16] if os.path.isdir(REG) else "NO-REGISTRY"
    bad = [p for p in VIEW_OF[n] if not (os.path.isfile(p) and "GENERATED" in read(p) and h in read(p))]
    say("PASS-GENERATED-HEADER" if not bad else "FAIL-HEADER", "FILES: %s  WITHOUT A GENERATED MARK AT REGISTRY HASH %s: %s" % (VIEW_OF[n], h, bad))


def _require_generated(n):
    """An unchanged carrier trivially equals its base and passes its tests: DELTA=0 means nothing until the view is written."""
    missing = [p for p in VIEW_OF[n] if not (os.path.isfile(p) and "GENERATED" in read(p))]
    if missing:
        say("FAIL-NOT-GENERATED", "NOT YET A GENERATED VIEW: %s" % missing)


def _v_delta0(n):
    _require_generated(n)
    base = spawn_base()
    if not base:
        say("FAIL-NO-BASE", "git merge-base HEAD CLOUD failed")
    made = []

    def at_base(p):
        # Beside the live file, so a carrier's __file__-relative imports (lib/, its ids directory, its siblings) resolve
        # as they do for the live copy -- "as if it lived at path" (exports_of). Removed after the comparison.
        dst = os.path.join(os.path.dirname(p) or ".", ".check_en_base__" + os.path.basename(p))
        made.append(dst)
        rc, out = run(["git", "show", "%s:%s" % (base, p)])
        with open(dst, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out)
        return dst
    # A base copy sits in a temp directory, so its own imports (the repo's lib/, its sibling modules) resolve only if
    # those directories are on the path -- as they are for the live copy (row LGIC_ENFORCE-W1-S7).
    extra = [os.path.abspath("lib")] + sorted({os.path.dirname(os.path.abspath(p)) for p in VIEW_OF[n]})
    added = [x for x in extra if x not in sys.path]
    sys.path[:0] = added
    try:
        eq, bad = _compare_carriers(VIEW_OF[n], at_base, lambda p: p)
    finally:
        for x in added:
            if x in sys.path:
                sys.path.remove(x)
        for f in made:
            if os.path.isfile(f):
                os.remove(f)
    say("PASS-DELTA0" if not bad else "FAIL-DELTA-NONZERO", "BASE: %s  FILES: %d  EXPORTS EQUAL: %d  DIFFER: %s" % (base[:10], len(VIEW_OF[n]), len(eq), bad))


def _v_tests(n):
    _require_generated(n)
    spec = CONSUMER_TESTS[n]
    cmd, cwd = spec[0], (spec[1] if len(spec) > 1 else None)
    rc, out = run(cmd, cwd=cwd, timeout=110)
    tail = out.strip().splitlines()[-1:] if out.strip() else ["(no output)"]
    say("PASS-CONSUMER-TESTS" if rc == 0 else "FAIL-CONSUMER-TESTS", "CMD: %s  rc=%d  %s" % (" ".join(cmd), rc, tail[0]))


# ------------------------------------------------------------------ EN-g-1
def _gate(patch, enforce):
    cmd = [sys.executable, GATE, "--diff", FI + "/tests/g1/" + patch] + (["--enforce"] if enforce else [])
    return run(cmd)


def _enforce_absent():
    if os.path.exists(ENFORCE_FILE):
        say("FAIL-ENFORCE-FILE-PRESENT", "%s is present; the shipped state is ABSENT" % ENFORCE_FILE)


def g1_refuse_key():
    rc, out = _gate("01_new_key_literal.patch", True)
    ok = rc == 1 and re.search(r"NAMING (OUT-OF-PATTERN|REFUSE)\b.*opal-data-inf/silver.*->.*\{source\}", out)
    say("PASS-REFUSED-WITH-CANONICAL" if ok else "FAIL-NOT-REFUSED", "rc=%d  %s" % (rc, out.strip()[-400:]))


def g1_pass_builder_key():
    rc, out = _gate("02_key_builder.patch", True)
    say("PASS-CANONICAL-PASSES" if rc == 0 and "REFUSE" not in out else "FAIL-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_alias_warn():
    rc, out = _gate("03_existing_alias_touched.patch", True)
    ok = rc == 0 and re.search(r"NAMING ALIAS\b.*mdpf-cottonwood-publisher-role.*->.*mdpf-cot-publisher-role", out)
    say("PASS-ALIAS-WARNED" if ok else "FAIL-ALIAS", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_refuse_carrier():
    rc, out = _gate("04_new_hand_kept_mapping.patch", True)
    ok = rc == 1 and re.search(r"lookup", out, re.I)
    say("PASS-CARRIER-REFUSED" if ok else "FAIL-CARRIER-NOT-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_pass_lookup():
    rc, out = _gate("05_lookup.patch", True)
    say("PASS-LOOKUP-PASSES" if rc == 0 and "REFUSE" not in out else "FAIL-LOOKUP-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_refuse_name():
    rc, out = _gate("06_new_resource_literal.patch", True)
    ok = rc == 1 and re.search(r"cottonwood-publisher-lambda.*->", out)
    say("PASS-NAME-REFUSED" if ok else "FAIL-NAME-NOT-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_pass_name_builder():
    rc, out = _gate("07_name_builder.patch", True)
    say("PASS-BUILDER-PASSES" if rc == 0 and "REFUSE" not in out else "FAIL-BUILDER-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_pass_key_scope():
    rc, out = _gate("08_key_scope_long.patch", True)
    say("PASS-LONG-FORM-IN-KEY-PASSES" if rc == 0 and "REFUSE" not in out else "FAIL-LONG-FORM-REFUSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_refuse_generated():
    rc, out = _gate("09_generated_edit.patch", True)
    ok = rc == 1 and re.search(r"generat", out, re.I)
    say("PASS-GENERATED-EDIT-REFUSED" if ok else "FAIL-GENERATED-EDIT-PASSED", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_warn_mode():
    _enforce_absent()
    rc, out = _gate("01_new_key_literal.patch", False)
    ok = rc == 0 and re.search(r"NAMING-GATE: WARN", out)
    say("PASS-WARN-EXIT-0" if ok else "FAIL-WARN-MODE", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_error_nonblocking():
    _enforce_absent()
    rc, out = _gate("10_malformed.patch", False)
    ok = rc == 0 and "NAMING ERROR" in out
    say("PASS-ERROR-NONBLOCKING" if ok else "FAIL-ERROR-BLOCKS", "rc=%d  %s" % (rc, out.strip()[-300:]))


def g1_logged():
    before = len(read(VERDICT_LOG).splitlines()) if os.path.isfile(VERDICT_LOG) else 0
    _gate("01_new_key_literal.patch", True)
    after = read(VERDICT_LOG).splitlines() if os.path.isfile(VERDICT_LOG) else []
    new = after[before:]
    ok = any("opal-data-inf/silver" in ln for ln in new)
    say("PASS-LOGGED" if ok else "FAIL-NOT-LOGGED", "VERDICT LOG %s: %d new line(s)" % (VERDICT_LOG, len(new)))


def g1_stage():
    t = read(".tools/safe-commit.sh").splitlines()
    cg, ng, tp = _first_line_matching(t, r'commit-gate\.sh" "\$\{GATE_FILES'), _first_line_matching(t, r"naming-gate\.py"), _first_line_matching(t, r'to-pipeline-gate\.py" "\$\{TOGATE')
    ok = -1 < cg < ng < tp
    say("PASS-STAGE-PLACED" if ok else "FAIL-STAGE-ORDER", "LINES: commit-gate %d  naming-gate %d  to-pipeline-gate %d" % (cg + 1, ng + 1, tp + 1))


def g1_shipped_warn():
    rc, out = git("ls-files", "--error-unmatch", ENFORCE_FILE)
    built = os.path.isfile(GATE) and "naming-gate.py" in read(".tools/safe-commit.sh")  # "absent" means nothing until the limb exists
    ok = built and not os.path.exists(ENFORCE_FILE) and rc != 0
    say("PASS-SHIPPED-WARN" if ok else "FAIL-ENFORCE-SHIPPED", "%s present in tree: %s, tracked: %s" % (ENFORCE_FILE, os.path.exists(ENFORCE_FILE), rc == 0))


# ------------------------------------------------------------------ EN-t-1, EN-t-2
def t1():
    d = fenced_json(D + "/TF_LABEL_CENSUS.md")
    return d if isinstance(d, dict) else {}


def t1_apart():
    d = t1()
    ok = isinstance(d.get("labels"), list) and isinstance(d.get("name_attributes"), list) and d.get("labels") != d.get("name_attributes")
    say("PASS-REPORTED-APART" if ok else "FAIL-NOT-APART", "LABELS: %s  NAME ATTRIBUTES: %s" % (len(d.get("labels", []) or []), len(d.get("name_attributes", []) or [])))


def t1_denominators():
    d = t1()
    den = d.get("denominator", {})
    rc, out = git("ls-files", "infra/aws/terraform")
    tf = len([ln for ln in out.splitlines() if ln.endswith(".tf")])
    ok = den.get("labels") == len(d.get("labels", [])) and den.get("name_attributes") == len(d.get("name_attributes", [])) and den.get("tf_files") == tf
    say("PASS-DENOMINATORS" if ok and d else "FAIL-DENOMINATORS", "DENOMINATOR: %s  tracked .tf files at HEAD: %d" % (den, tf))


def t1_graded():
    d = t1()
    rows = (d.get("labels") or []) + (d.get("name_attributes") or [])
    bad = [r for r in rows if not isinstance(r, dict) or r.get("verdict") not in VERDICTS | {"RAISE"}]
    say("PASS-GRADED" if rows and not bad else "FAIL-UNGRADED", "ROWS: %d  WITHOUT A VERDICT: %d" % (len(rows), len(bad)))


def _stub_tf(marker):
    d = tempfile.mkdtemp()
    stub = os.path.join(d, "terraform-stub.sh")
    with open(stub, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("#!/usr/bin/env bash\necho \"$@\" >> '%s'\nexit 0\n" % marker.replace("\\", "/"))
    os.chmod(stub, 0o755)
    return stub


def _apply(tree):
    marker = os.path.join(tempfile.mkdtemp(), "called.txt")
    stub = _stub_tf(marker)
    # safe-apply's halt checkpoint resolves the invoker ONLY from org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial under
    # the repo root, which a worker worktree does not carry (row LGIC_ENFORCE-W3-S6). Seat the running serial there for
    # this one run under a synthetic session id, and remove the file afterwards.
    sid = "check-en-t2-%d" % os.getpid()
    sess = os.path.join("org", "mcp", "sessions", sid + ".serial")
    os.makedirs(os.path.dirname(sess), exist_ok=True)
    with open(sess, "w", encoding="utf-8", newline="\n") as fh:
        fh.write((os.environ.get("OPAL_AGENT_SERIAL") or "0.9.0_WK_LGIC_ENFORCE~3") + "\n")
    try:
        rc, out = run_bash([".tools/safe-apply.sh", "-chdir=" + FI + "/tests/t2/" + tree, "apply"],
                           env={"SAFE_APPLY_TERRAFORM": stub, "HALT_ACK": "1", "NAMING_GATE_ENFORCE": "1",
                                "CLAUDE_CODE_SESSION_ID": sid})
    finally:
        if os.path.exists(sess):
            os.remove(sess)
    return rc, out, os.path.exists(marker)


def t2_refuse():
    rc, out, called = _apply("bad_tree")
    ok = rc != 0 and not called and "->" in out and "BadQueueName" in out
    say("PASS-REFUSED-BEFORE-PLAN" if ok else "FAIL-NOT-REFUSED-BEFORE-PLAN", "rc=%d  terraform called: %s  %s" % (rc, called, out.strip()[-300:]))


def t2_pass():
    rc, out, called = _apply("good_tree")
    ok = called and "REFUSE" not in out and "NAMING-GATE: PASS" in out  # the stage must have RUN, not merely be absent
    say("PASS-STAGE-PASSES" if ok else "FAIL-GOOD-TREE-BLOCKED", "rc=%d  terraform called: %s  %s" % (rc, called, out.strip()[-300:]))


def t2_order():
    t = read(".tools/safe-apply.sh").splitlines()
    hg, ng, ta = _first_line_matching(t, r"halt_gate_check \"safe-apply\""), _first_line_matching(t, r"naming-(apply-)?gate\.py"), _first_line_matching(t, r"TAG-AUTHORIZATION pre-apply gate")
    ok = -1 < hg < ng < ta
    say("PASS-STAGE-ORDER" if ok else "FAIL-STAGE-ORDER", "LINES: halt gate %d  naming gate %d  tag-authz %d" % (hg + 1, ng + 1, ta + 1))


# ------------------------------------------------------------------ EN-s-1, EN-s-2
def s1():
    d = fenced_json(D + "/NAMING_CENSUS_REPORT.md")
    return d if isinstance(d, dict) else {}


def s1_planes():
    d = s1()
    planes = {r.get("plane") for r in d.get("rows", [])}
    ok = {"repo", "live"} <= planes and d.get("vintage") and d.get("denominators")
    say("PASS-BOTH-PLANES" if ok else "FAIL-PLANES", "PLANES: %s  VINTAGE: %s  DENOMINATORS: %s" % (sorted(p for p in planes if p), d.get("vintage"), d.get("denominators")))


def s1_all_judged():
    d = s1()
    den = d.get("denominators", {})
    live_rows = len([r for r in d.get("rows", []) if r.get("plane") == "live"])
    ok = den.get("live_nameable") and den.get("judged_live") == den.get("live_nameable") == live_rows
    say("PASS-ALL-JUDGED" if ok else "FAIL-NOT-ALL-JUDGED", "LIVE NAMEABLE: %s  JUDGED: %s  LIVE ROWS: %d" % (den.get("live_nameable"), den.get("judged_live"), live_rows))


def s1_row_shape():
    rows = s1().get("rows", [])
    bad = [r for r in rows if not all(k in r for k in ("current", "canonical", "verdict", "type", "plane"))]
    say("PASS-ROW-SHAPE" if rows and not bad else "FAIL-ROW-SHAPE", "ROWS: %d  MALFORMED: %d" % (len(rows), len(bad)))


def s1_raise_stops():
    rc, out = run([sys.executable, OPAL, "census", "--names", FI + "/tests/s1/unplaceable.tsv"])
    ok = rc != 0 and "zzqx-inf-foo-lambda" in out
    say("PASS-RAISE-STOPS" if ok else "FAIL-RAISE-DID-NOT-STOP", "rc=%d  %s" % (rc, out.strip()[-300:]))


def s2_three():
    d = fenced_json(D + "/NAMING_CENSUS_COMPARISON.md") or {}
    a = d.get("against", {})
    ok = all(k in a and a[k].get("denominator") for k in ("N2", "N6", "IV7"))
    say("PASS-THREE-COMPARED" if ok else "FAIL-COMPARISON", "COMPARED AGAINST: %s" % {k: (v or {}).get("denominator") for k, v in a.items()})


def s2_named():
    d = fenced_json(D + "/NAMING_CENSUS_COMPARISON.md") or {}
    dis = d.get("disagreements")
    bad = [x for x in (dis or []) if not (x.get("name") and x.get("census_verdict") and x.get("hand_verdict"))]
    say("PASS-DISAGREEMENTS-NAMED" if isinstance(dis, list) and not bad else "FAIL-DISAGREEMENTS", "DISAGREEMENTS: %s  MALFORMED: %d" % (None if dis is None else len(dis), len(bad)))


# ------------------------------------------------------------------ EN-p-1, EN-d-1, EN-d-2, EN-x-1
def _commit_exists(h):
    return bool(h) and git("cat-file", "-e", "%s^{commit}" % h)[0] == 0


def p1():
    return fenced_json(D + "/EXERCISE_FWD6.md") or {}


def p1_surface():
    """The first carrier, by (path, line), whose token grades OUT-OF-PATTERN. A RAISE is not OUT-OF-PATTERN, so the rule
    passes over a carrier whose grade raises RaiseDefect (row LGIC_ENFORCE-W2-S7); it is counted, not fatal."""
    d, c = p1(), c1()
    try:
        o = opal()
        cands = sorted((x.get("path"), x.get("line") or 0, x.get("token")) for x in (c or {}).get("carriers", []))
        want, raised, seen = None, 0, 0
        for p, _, tok in cands:
            if not tok:
                continue
            seen += 1
            try:
                verdict = o.grade(tok, "S3Key")[0]
            except o.RaiseDefect:
                raised += 1
                continue
            if verdict == "OUT-OF-PATTERN":
                want = p
                break
    except Exception as exc:  # noqa: BLE001
        return say("FAIL-NOT-EVALUABLE", "%s: %s" % (type(exc).__name__, exc))
    say("PASS-SURFACE-BY-RULE" if want and d.get("surface") == want else "FAIL-SURFACE",
        "RECORD: %s  BY RULE: %s  (carriers read: %d of %d, passed over on a RAISE: %d)" % (d.get("surface"), want, seen, len(cands), raised))


def p1_refused():
    d = p1()
    out = str(d.get("outputs", {}).get("refused", ""))
    ok = "NAMING-GATE: REFUSE" in out and d.get("surface", "@@") in out
    say("PASS-REFUSED" if ok else "FAIL-NOT-REFUSED", "GATE OUTPUT ON THE TOUCHING DIFF: %s" % out[:300])


def p1_passed():
    out = str(p1().get("outputs", {}).get("passed", ""))
    say("PASS-REMOVAL-PASSES" if "NAMING-GATE: PASS" in out and "REFUSE" not in out else "FAIL-REMOVAL", "GATE OUTPUT ON THE REMOVING DIFF: %s" % out[:300])


def p1_branch():
    d = p1()
    b = d.get("scratch_branch")
    h = d.get("commits", {}).get("plant")
    ok = b and _commit_exists(h) and git("merge-base", "--is-ancestor", h, b)[0] == 0
    say("PASS-EVIDENCE-ON-BRANCH" if ok else "FAIL-EVIDENCE", "BRANCH: %s  PLANTED-ROW COMMIT %s ON IT: %s" % (b, h, ok))


def d1():
    return fenced_json(D + "/EXERCISE_FWD7.md") or {}


def d1_firm():
    f = d1().get("firm", {})
    say("PASS-FIXED-FIRM" if f == {"long": "quillwater", "short": "qwt"} else "FAIL-FIRM", "FIRM: %s" % f)


def d1_order():
    c = d1().get("commits", {})
    a, b = c.get("expected_set"), c.get("generated")
    ok = _commit_exists(a) and _commit_exists(b) and a != b and git("merge-base", "--is-ancestor", a, b)[0] == 0
    say("PASS-EXPECTED-FIRST" if ok else "FAIL-ORDER", "EXPECTED-SET %s BEFORE GENERATED %s: %s" % (a, b, ok))


def d1_diff_equal():
    d = d1()
    c = d.get("commits", {})
    rc, out = git("diff", "--name-only", str(c.get("expected_set")), str(c.get("generated")))
    actual = sorted(ln for ln in out.splitlines() if ln and not ln.startswith(REG))
    want = sorted(d.get("expected_files", []))
    ok = rc == 0 and actual and actual == want
    say("PASS-DIFF-EQUALS-EXPECTED" if ok else "FAIL-DIFF", "EXPECTED: %d  ACTUAL (minus the registry): %d  ONLY EXPECTED: %s  ONLY ACTUAL: %s" % (len(want), len(actual), sorted(set(want) - set(actual))[:4], sorted(set(actual) - set(want))[:4]))


def d1_address_refused():
    s = str(d1().get("outputs", {}).get("hand_address_refused", ""))
    say("PASS-ADDRESS-REFUSED" if "REFUSE" in s and "qwt" in s or "quillwater" in s and "REFUSE" in s else "FAIL-ADDRESS", "OUTPUT: %s" % s[:300])


def d1_name_refused():
    s = str(d1().get("outputs", {}).get("hand_name_refused", ""))
    say("PASS-NAME-REFUSED" if "REFUSE" in s and ("qwt" in s or "quillwater" in s) else "FAIL-NAME", "OUTPUT: %s" % s[:300])


def d1_pipeline():
    d = d1()
    c = d.get("commits", {}).get("generated")
    p = d.get("pipeline_path")
    ok = _commit_exists(c) and p and git("cat-file", "-e", "%s:%s" % (c, p))[0] == 0
    say("PASS-PIPELINE-WRITTEN" if ok else "FAIL-PIPELINE", "PIPELINE %s AT %s: %s" % (p, c, ok))


def d2_zero():
    d = fenced_json(D + "/EXERCISE_FWD1_SEARCH.md") or {}
    pl = d.get("pipeline", {})
    rc, body = git("show", "%s:%s" % (pl.get("commit"), pl.get("path")))
    mine = re.findall(r"s3://|opal-data-[a-z0-9-]+|\b(?:bronze|silver|gold|platinum)/", body) if rc == 0 else ["UNREADABLE"]
    ok = d.get("hits") == [] and d.get("denominator") and rc == 0 and not mine
    say("PASS-ZERO-LITERALS" if ok else "FAIL-LITERALS", "WORKER HITS: %s  CHECKER RE-SEARCH HITS: %s  (%s:%s)" % (d.get("hits"), mine[:5], pl.get("commit"), pl.get("path")))


def d2_control():
    c = (fenced_json(D + "/EXERCISE_FWD1_SEARCH.md") or {}).get("control", {})
    say("PASS-CONTROL-FIRES" if c.get("hits") == 1 and c.get("planted") else "FAIL-CONTROL", "CONTROL: %s" % c)


def x1():
    return fenced_json(D + "/EXERCISE_FWD2.md") or {}


def x1_plan():
    d = x1()
    try:
        plan = json.loads(read(d.get("plan_json", "")))
    except (OSError, ValueError, TypeError):
        say("FAIL-NO-PLAN", "plan_json unreadable: %s" % d.get("plan_json"))
    nm = (d.get("resource") or {}).get("name")
    creates = [(rc.get("change", {}).get("after") or {}).get("name") for rc in plan.get("resource_changes", []) if "create" in rc.get("change", {}).get("actions", [])]
    ok = nm and nm in creates and "-49f-" in "-" + nm + "-"
    say("PASS-RESOURCE-IN-PLAN" if ok else "FAIL-RESOURCE", "RESOURCE: %s  CREATES IN PLAN: %s" % (nm, creates[:6]))


def x1_same_row():
    d = x1()
    try:
        pats = opal().fence_patterns("49financial")
    except Exception as exc:
        say("FAIL-NOT-EVALUABLE", "%s: %s" % (type(exc).__name__, exc))
    nm = (d.get("resource") or {}).get("name") or ""
    ok = "49f" in nm.split("-") and any("49f" in p for p in pats) and d.get("registry_row") == "49financial"
    say("PASS-SAME-ROW" if ok else "FAIL-ROW", "RESOURCE: %s  FENCE PATTERNS: %s  ROW: %s" % (nm, pats, d.get("registry_row")))


def x1_moves_both():
    d = x1()
    c = d.get("commits", {})
    rc, out = git("diff", str(c.get("before")), str(c.get("after")))
    new_short = d.get("new_short")
    name_lines = [ln for ln in out.splitlines() if ln.startswith("+") and new_short and new_short in ln and "role" in ln]
    fence_lines = [ln for ln in out.splitlines() if ln.startswith("+") and new_short and new_short in ln and "*" in ln]
    ok = rc == 0 and new_short and name_lines and fence_lines
    say("PASS-BOTH-MOVE" if ok else "FAIL-NOT-BOTH", "NEW SHORT FORM: %s  NAME LINES: %d  FENCE LINES: %d" % (new_short, len(name_lines), len(fence_lines)))


# ------------------------------------------------------------------ table
SUBS = {
    "c1-denominator": c1_denominator, "c1-dec5": c1_dec5, "c1-partition": c1_partition, "c1-extra-filed": c1_extra_filed,
    "c2-buckets": c2_buckets, "c2-tokens": c2_tokens, "c2-window": c2_window, "c2-unobserved": c2_unobserved, "c2-denominators": c2_denominators,
    "r1-parse": r1_parse, "r1-refuse-owner": r1_refuse_owner, "r1-refuse-firm": r1_refuse_firm, "r1-scopes": r1_scopes, "r1-bd": r1_bd, "r1-generate": r1_generate,
    "b1-key": b1_key, "b1-address": b1_address, "b1-no-bucket": b1_no_bucket, "b1-name": b1_name, "b1-controls": b1_controls,
    "b1-whole-segment": b1_whole_segment, "b1-agree": b1_agree, "b1-tests": b1_tests,
    "m1-no-external": m1_no_external, "m1-vectors": m1_vectors, "m1-header": m1_header,
    "f1-covered": f1_covered, "f1-no-typed-list": f1_no_typed_list, "f1-plan": f1_plan, "f1-prior": f1_prior, "f1-ledger-open": f1_ledger_open,
    "f2-signoff": f2_signoff, "f2-policy-live": f2_policy_live, "f2-probe-49f": f2_probe_49f, "f2-probe-cot": f2_probe_cot,
    "f2-probe-unscoped": f2_probe_unscoped, "f2-probe-exempt": f2_probe_exempt, "f2-removed": f2_removed, "f2-closed": f2_closed,
    "g1-refuse-key": g1_refuse_key, "g1-pass-builder-key": g1_pass_builder_key, "g1-alias-warn": g1_alias_warn, "g1-refuse-carrier": g1_refuse_carrier,
    "g1-pass-lookup": g1_pass_lookup, "g1-refuse-name": g1_refuse_name, "g1-pass-name-builder": g1_pass_name_builder, "g1-pass-key-scope": g1_pass_key_scope,
    "g1-refuse-generated": g1_refuse_generated, "g1-warn-mode": g1_warn_mode, "g1-error-nonblocking": g1_error_nonblocking, "g1-logged": g1_logged,
    "g1-stage": g1_stage, "g1-shipped-warn": g1_shipped_warn,
    "t1-apart": t1_apart, "t1-denominators": t1_denominators, "t1-graded": t1_graded,
    "t2-refuse": t2_refuse, "t2-pass": t2_pass, "t2-order": t2_order,
    "s1-planes": s1_planes, "s1-all-judged": s1_all_judged, "s1-row-shape": s1_row_shape, "s1-raise-stops": s1_raise_stops,
    "s2-three": s2_three, "s2-named": s2_named,
    "p1-surface": p1_surface, "p1-refused": p1_refused, "p1-passed": p1_passed, "p1-branch": p1_branch,
    "d1-firm": d1_firm, "d1-order": d1_order, "d1-diff-equal": d1_diff_equal, "d1-address-refused": d1_address_refused,
    "d1-name-refused": d1_name_refused, "d1-pipeline": d1_pipeline,
    "d2-zero": d2_zero, "d2-control": d2_control,
    "x1-plan": x1_plan, "x1-same-row": x1_same_row, "x1-moves-both": x1_moves_both,
}
for _n in "123456":
    SUBS["v%s-header" % _n] = (lambda n=_n: _v_header(n))
    SUBS["v%s-delta0" % _n] = (lambda n=_n: _v_delta0(n))
    if _n in CONSUMER_TESTS:
        SUBS["v%s-tests" % _n] = (lambda n=_n: _v_tests(n))

# Subcommands that read the LIVE plane or run the full build are excluded from the negative self-test's
# timing budget only; they still must not PASS on a pre-issuance tree.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_en.py <subcommand> | --list | selftest-negative")
        sys.exit(2)
    arg = sys.argv[1]
    if arg == "--list":
        print("\n".join(sorted(SUBS)))
        print("SUBCOMMANDS: %d" % len(SUBS))
        sys.exit(0)
    if arg == "selftest-negative":
        passed = []
        for s in sorted(SUBS):
            rc, out = run([sys.executable, os.path.abspath(__file__), s], timeout=115)
            v = (re.findall(r"^VERDICT: (\S+)", out, re.M) or ["NO-VERDICT rc=%d" % rc])[-1]
            print("%-24s %s" % (s, v))
            if v.startswith("PASS-"):
                passed.append(s)
        print("SELFTEST-NEGATIVE: %d subcommands, %d PASS on a tree where no cell has run%s" % (len(SUBS), len(passed), (": " + ", ".join(passed)) if passed else ""))
        sys.exit(0 if not passed else 1)
    fn = SUBS.get(arg)
    if not fn:
        print("unknown subcommand %r" % arg)
        sys.exit(2)
    try:
        fn()
    except SystemExit:
        raise
    except Exception as exc:  # a crash is a FAIL with its reason, never a silent pass
        say("FAIL-CHECKER-ERROR", "%s: %s" % (type(exc).__name__, exc))
