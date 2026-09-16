#!/usr/bin/env python3
"""check_ln_r4.py -- the mechanical criteria of LGIC_NAMING round 4 (decomposition v6 s.0e), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-4 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line `VERDICT: PASS-<X>` or
`VERDICT: FAIL-<X>`, and exits 0. A missing input is a FAIL verdict, never a traceback. No PASS string is a substring
of another subcommand's PASS or FAIL string, because proof-of-spec-check greps <expect> unanchored.
`--list` prints the subcommands; `selftest-negative` runs every one and counts the PASS verdicts.

Round 4 re-cuts three cells (1.0.0_SA_CTO's round-3 analysis s.3):
  LN-g-1  GRADING_RULE.md complete at the schema it lands with (W3-S6, FN1d, AW1, V-2)
  LN-g-2  grade() in lib/opal_naming.py implements FN1d; the rule and grade() cover each other (C-S11)
  LN-f-1  the firm patterns re-graded, every {system} gap raised with its missing row (FWD-5, W4-S1)

THE FIELD GRAIN (W3-S6). A schema FIELD is a top-level key of NAMING_SCHEMA.json; where that key is an object in
both versions, each of its second-level keys is a field instead. A key added or removed whole counts once.
version, changelog and ratified_by are metadata and are not fields the rule covers. Measured at the cut:
v1.4 -> v1.7 reads 15 changed, 12 besides the metadata (round 3's worker counted the same), and v1.4 -> v1.8 reads
the same 12, because v1.8 moved only resource.function again.
"""
import copy
import fnmatch
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = "org/missions/D14/LGIC/LGIC_NAMING"
EX = BASE + "/deliverables/exercises"
EXR2 = EX + "/r2"
EXR4 = EX + "/r4"
FIX = BASE + "/deliverables/2.0.0_SA_COO~G/fixed_inputs"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
RULE = BASE + "/deliverables/GRADING_RULE.md"
LIB = "lib/opal_naming.py"
TESTS = "lib/tests/test_opal_naming.py"
REGRADE = EXR4 + "/g2-regrade.r4.tsv"
F1R4 = EXR4 + "/n4-firm-patterns.md"
CUT_PIN = "e04b802fe9"  # NAMING_SCHEMA.json v1.4, the version GRADING_RULE.md was cut at (round 1)
META = ("version", "changelog", "ratified_by")
FIRMS = ("49financial", "inflection", "cottonwood", "demo")
ALIAS_TOKENS = ("bd", "49f", "49financial", "inf", "inflection", "cot", "cottonwood", "demo")
FN1D_CASES = (("mdpf-lambda-lambda", "LAMBDA"), ("orion-orion-lambda-lambda", "LAMBDA"))
BASE_FAILING = frozenset()  # lib/tests/test_opal_naming.py at 7b5331c8c0: 75 passed, 0 failed (RULING RED's base)
LABEL = r"(?:[GNRSLBK]\d+(?:\.\d+)?[a-d]?|V-\d)"
COVERS_RE = re.compile(r"^- COVERS (\S+): (.+?)\s*$", re.M)
COVERAGE_RE = re.compile(r"^SCHEMA COVERAGE SINCE v1\.4: (\d+) of (\d+)\s*$", re.M)
GRADES_RE = re.compile(r"Grades against `?NAMING_SCHEMA\.json (v[0-9.]+)`?")


def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)


def read(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_json(path):
    t = read(path)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def fence_with(path, key):
    """The fenced json block of `path` that carries `key` -- never the first fence by position."""
    t = read(path)
    if t is None:
        return None
    for body in re.findall(r"```json\s*\n(.*?)\n```", t, re.S):
        try:
            d = json.loads(body)
        except ValueError:
            continue
        if isinstance(d, dict) and key in d:
            return d
    return None


def naming():
    """lib/opal_naming.py of THIS tree, loaded by path (lib/ has no __init__.py). (module, error)."""
    try:
        spec = importlib.util.spec_from_file_location("opal_naming_r4", LIB)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except (SystemExit, Exception) as exc:  # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, exc)


def schema_at(pin):
    r = subprocess.run(["git", "show", "%s:%s" % (pin, SCHEMA)], capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout.decode("utf-8"))
    except ValueError:
        return None


def field_diff(a, b):
    """THE FIELD GRAIN (module docstring). Returns the changed fields, metadata excluded, sorted."""
    out = []
    for k in sorted(set(a) | set(b)):
        if k in META:
            continue
        if k not in a or k not in b:
            out.append(k)
        elif a[k] == b[k]:
            continue
        elif isinstance(a[k], dict) and isinstance(b[k], dict):
            out.extend("%s.%s" % (k, s) for s in sorted(set(a[k]) | set(b[k])) if a[k].get(s) != b[k].get(s))
        else:
            out.append(k)
    return out


def rule_steps(text):
    """The steps GRADING_RULE.md DEFINES: a label in bold (**R5**, **G2.1**, **V-2**) or a section heading (## G3.)."""
    bold = set(re.findall(r"\*\*(" + LABEL + r")(?=[\s.*])", text))
    heads = set(re.findall(r"^## (" + LABEL + r")\.", text, re.M))
    return bold | heads


def parent(label):
    m = re.match(r"([A-Z])(\d+)", label)
    return m.group(0) if m and m.group(0) != label else None


def coverage(rule_text, schema):
    """(changed fields, covered fields, bad lines, printed (n, d) or None)."""
    base = schema_at(CUT_PIN)
    if base is None or not isinstance(schema, dict):
        return None, None, ["the v1.4 schema at %s or the working schema is unreadable" % CUT_PIN], None
    changed = field_diff(base, schema)
    steps = rule_steps(rule_text)
    covered, bad = set(), []
    for field, rhs in COVERS_RE.findall(rule_text):
        rhs = rhs.strip()
        if rhs.startswith("NO STEP -- ") and len(rhs) >= len("NO STEP -- ") + 8:
            covered.add(field)
            continue
        cited = [s.strip() for s in re.split(r"[,;]", rhs) if s.strip()]
        unknown = [s for s in cited if not re.fullmatch(LABEL, s) or (s not in steps and parent(s) not in steps)]
        if cited and not unknown:
            covered.add(field)
        else:
            bad.append("COVERS %s: %s -- cites no step the rule defines: %s" % (field, rhs, unknown or cited))
    m = COVERAGE_RE.search(rule_text)
    printed = (int(m.group(1)), int(m.group(2))) if m else None
    return changed, covered, bad, printed


# ---------------------------------------------------------------- LN-g-1: GRADING_RULE.md, complete
def g1_coverage():
    text = read(RULE)
    schema = load_json(SCHEMA)
    if text is None:
        return say("FAIL-COVERAGE-NO-RULE", "GRADING_RULE.md absent at %s" % RULE)
    changed, covered, bad, printed = coverage(text, schema)
    if changed is None:
        return say("FAIL-COVERAGE-NO-SCHEMA", *bad)
    n = len([f for f in changed if f in covered])
    listed = set(f for f, _ in COVERS_RE.findall(text))
    extra = sorted(listed - set(changed))
    missing = [f for f in changed if f not in covered]
    print("SCHEMA: v1.4 @%s -> the working tree's %s (%s)" % (CUT_PIN, SCHEMA, (schema or {}).get("version")))
    print("CHANGED FIELDS, DERIVED BY THIS CHECKER (metadata excluded): %d %s" % (len(changed), changed))
    for b in bad:
        print("NOT COVERED: " + b)
    print("UNCOVERED FIELDS: %d %s" % (len(missing), missing))
    print("COVERS LINES NAMING A FIELD THAT DID NOT CHANGE: %d %s" % (len(extra), extra))
    print("PRINTED BY THE RULE: %s  DERIVED: %d of %d" % (printed, n, len(changed)))
    ok = changed and printed == (n, len(changed)) and n == len(changed) and not extra and not bad
    say("PASS-COVERAGE-DERIVED" if ok else "FAIL-COVERAGE-SHORT")


def g1_doctored():
    text = read(RULE)
    schema = load_json(SCHEMA)
    if text is None or not isinstance(schema, dict):
        return say("FAIL-DOCTORED-NO-INPUT", "rule %s or schema %s unreadable" % (RULE, SCHEMA))
    changed, covered, bad, printed = coverage(text, schema)
    if changed is None:
        return say("FAIL-DOCTORED-NO-INPUT", *bad)
    n = len([f for f in changed if f in covered])
    base_ok = changed and printed == (n, len(changed)) and n == len(changed) and not bad
    print("UNDOCTORED: %d of %d  (printed %s)" % (n, len(changed), printed))
    if not base_ok:
        return say("FAIL-DOCTORED-BASE-SHORT", "the undoctored coverage does not read N of N, so the arm has nothing to discriminate")
    doctored = copy.deepcopy(schema)  # an in-memory copy: the committed schema is never written
    doctored["zz_doctored_field_r4"] = {"probe": "a field no step of the rule covers"}
    d_changed, d_covered, _, _ = coverage(text, doctored)
    dn = len([f for f in d_changed if f in d_covered])
    print("DOCTORED (one top-level field added in memory): %d of %d" % (dn, len(d_changed)))
    ok = len(d_changed) == len(changed) + 1 and dn == len(d_changed) - 1
    say("PASS-DOCTORED-READS-SHORT" if ok else "FAIL-DOCTORED-NOT-DISCRIMINATING",
        "THE DOCTORED ARM READS N-1 OF N: %s" % ok)


def g1_version():
    text = read(RULE) or ""
    schema = load_json(SCHEMA) or {}
    m = GRADES_RE.search("\n".join(text.splitlines()[:40]))
    named, have = (m.group(1) if m else None), schema.get("version")
    say("PASS-GRADES-WORKING-SCHEMA" if named and named == have else "FAIL-HEADER-NOT-WORKING-SCHEMA",
        "HEADER 'Grades against NAMING_SCHEMA.json <v>': %s  WORKING SCHEMA: %s" % (named, have))


def g1_g2():
    text = read(RULE) or ""
    m = re.search(r"^## G2\.(.*)$", text, re.M)
    head = m.group(1) if m else None
    wc = fence_with(RULE, "worked_cases") or {}
    case = [c for c in wc.get("worked_cases", []) if c.get("name") == "default" and c.get("type") == "SECURITY_GROUP"]
    verdict = case[0].get("verdict") if case else None
    ok = head is not None and "RAISE" not in head and verdict == "NOT-GRADED"
    say("PASS-G2-EXCLUDES" if ok else "FAIL-G2-STILL-RAISES",
        "G2 HEADING: %r  WORKED CASE default/SECURITY_GROUP VERDICT: %s (want NOT-GRADED: aws_fixed is outside the "
        "grade's domain, never a fourth verdict)" % (head, verdict))


def g1_v2():
    text = read(RULE) or ""
    schema = load_json(SCHEMA) or {}
    m = re.search(r"^- \*\*V-2\*\*(.*)$", text, re.M)
    in_rule = set(re.findall(r"\{(\w+)\}", m.group(1))) if m else None
    in_schema = set(re.findall(r"\{(\w+)\}", str(schema.get("grade", {}).get("placeholder", ""))))
    ok = in_rule is not None and in_schema and in_rule == in_schema
    say("PASS-V2-EQUALS-SCHEMA" if ok else "FAIL-V2-DIFFERS",
        "V-2 PLACEHOLDERS: %s  NAMING_SCHEMA.json grade.placeholder: %s" % (sorted(in_rule or []), sorted(in_schema)))


def g1_fn1d():
    text = read(RULE) or ""
    wc = fence_with(RULE, "worked_cases") or {}
    cases = wc.get("worked_cases", [])
    rows = []
    for name, typ in FN1D_CASES:
        c = [x for x in cases if x.get("name") == name and x.get("type") == typ]
        ok = bool(c) and c[0].get("verdict") == "RAISE" and "R5" in str(c[0].get("why", ""))
        rows.append((name, typ, c[0].get("verdict") if c else None, ok))
    for r in rows:
        print("WORKED CASE %s/%s: verdict %s  RAISE citing R5: %s" % r)
    two_steps = "**R5.b" in text or "**R5.a" in text
    print("R5 STILL SPLIT INTO R5.a / R5.b: %s" % two_steps)
    ok = all(r[3] for r in rows) and not two_steps
    say("PASS-FN1D-WORKED-CASES" if ok else "FAIL-FN1D-NOT-IN-RULE")


# ---------------------------------------------------------------- LN-g-2: grade() and the rule, both ways
def g2_fn1d():
    mod, err = naming()
    if mod is None:
        return say("FAIL-FN1D-NO-MODULE", "IMPORT %s: %s" % (LIB, err))
    rows = []
    for name, typ in FN1D_CASES:
        try:
            got = "RETURNED %s" % (mod.grade(name, typ),)
            ok = False
        except mod.RaiseDefect as exc:
            got = "RaiseDefect: %s" % exc
            ok = str(exc).startswith("R5")
        except Exception as exc:  # noqa: BLE001
            got, ok = "%s: %s" % (type(exc).__name__, exc), False
        rows.append((name, typ, got, ok))
    for r in rows:
        print("grade(%r, %r) -> %s  [RAISE naming R5: %s]" % r)
    say("PASS-FN1D-RAISES-IN-CODE" if all(r[3] for r in rows) else "FAIL-FN1D-CODE-ACCEPTS")


def r2_attributed():
    d = fence_with(EXR2 + "/n4-firm-patterns.md", "attributed") or {}
    return [(a.get("name"), a.get("canonical")) for f in FIRMS for a in (d.get("attributed") or {}).get(f, [])]


def g2_regrade():
    mod, err = naming()
    if mod is None:
        return say("FAIL-REGRADE-NO-MODULE", "IMPORT %s: %s" % (LIB, err))
    t = read(REGRADE)
    if t is None:
        return say("FAIL-REGRADE-NO-RECORD", "%s absent: the worker's re-grade record of round 2's attributed forms" % REGRADE)
    rec = {}
    for ln in t.splitlines():
        if ln.strip() and not ln.startswith("#"):
            c = ln.split("\t")
            if len(c) >= 2:
                rec[c[0].strip()] = c[1].strip()
    old = r2_attributed()
    v1 = sorted(mod._vocab().v1)
    bad = []
    for name, canon in old:
        try:
            now = mod.grade(name, "IAM_ROLE")[1]
        except Exception as exc:  # noqa: BLE001
            now = "RAISE %s" % exc
        pat = "^" + re.escape(canon or "").replace(re.escape("{system}"), "(?:%s|\\{system\\})" % "|".join(map(re.escape, v1))) + "$"
        if rec.get(name) != now:
            bad.append((name, "record says %s, grade() says %s" % (rec.get(name), now)))
        elif not re.match(pat, now or ""):
            bad.append((name, "round 2 %s -> round 4 %s: a change other than a {system} fill" % (canon, now)))
    for b in bad[:10]:
        print("DIFFERS: %s  %s" % b)
    ok = old and len(rec) >= len(old) and not bad
    say("PASS-REGRADE-UNCHANGED" if ok else "FAIL-REGRADE-MOVED",
        "ROUND 2 ATTRIBUTED FORMS: %d  IN THE RECORD: %d  RECORD == grade() AND == ROUND 2 (a {system} fill aside): %d"
        % (len(old), len(rec), len(old) - len(bad)))


def aws_fixed_probes(schema):
    out = []
    for typ, entries in (schema.get("aws_fixed", {}).get("by_name") or {}).items():
        for e in entries:
            out.append((e[len("prefix: "):] + "probe" if e.startswith("prefix: ") else e, typ))
    return out


def g2_aws():
    mod, err = naming()
    schema = load_json(SCHEMA) or {}
    if mod is None:
        return say("FAIL-AWSFIX-NO-MODULE", "IMPORT %s: %s" % (LIB, err))
    probes = aws_fixed_probes(schema)
    bad = []
    for name, typ in probes:
        try:
            got = mod.grade(name, typ)
        except Exception as exc:  # noqa: BLE001
            got = "%s: %s" % (type(exc).__name__, exc)
        ok = isinstance(got, tuple) and got[0] == "NOT-GRADED"
        print("grade(%r, %r) -> %s" % (name, typ, got))
        if not ok:
            bad.append(name)
    say("PASS-AWS-FIXED-NOT-GRADED" if probes and not bad else "FAIL-AWSFIX-STILL-GRADED",
        "NAMING_SCHEMA.json aws_fixed.by_name PROBES: %d  RETURNED NOT-GRADED: %d" % (len(probes), len(probes) - len(bad)))


def g2_twoway():
    text = read(RULE)
    src = read(LIB)
    if text is None or src is None:
        return say("FAIL-TWOWAY-NO-INPUT", "rule %s or %s absent" % (RULE, LIB))
    try:
        region = src[src.index("class RaiseDefect"):src.index("def _segment(")]
    except ValueError:
        return say("FAIL-TWOWAY-NO-REGION", "the grade() region (class RaiseDefect .. def _segment) is not found in %s" % LIB)
    region = re.sub(r"PRD S\d+", "", region)  # a PRD section cited as 'PRD S10' is not a rule step
    defined = rule_steps(text)
    cited = set(re.findall(r"(?<![A-Za-z0-9_])(" + LABEL + r")(?:\.[a-f])?(?![A-Za-z0-9_])", region))
    rule_not_code = sorted(s for s in defined if s not in cited and not any(parent(c) == s for c in cited))
    code_not_rule = sorted(c for c in cited if c not in defined and parent(c) not in defined)
    print("STEPS THE RULE DEFINES: %d  STEP LABELS THE grade() REGION CITES: %d" % (len(defined), len(cited)))
    print("RULE STEPS NO CODE CITES: %d %s" % (len(rule_not_code), rule_not_code))
    print("CODE LABELS THE RULE DOES NOT DEFINE: %d %s" % (len(code_not_rule), code_not_rule))
    say("PASS-STEPS-TWO-WAY" if not rule_not_code and not code_not_rule else "FAIL-STEPS-ONE-WAY")


def find_map(node):
    if isinstance(node, dict):
        if "aws_iam_role" in node and "IAM_ROLE" in json.dumps(node["aws_iam_role"]):
            return True
        return any(find_map(v) for v in node.values())
    if isinstance(node, list):
        return any(find_map(v) for v in node)
    return False


def g2_typemap():
    src = read(LIB) or ""
    schema = load_json(SCHEMA) or {}
    literal = '"aws_iam_role"' in src or "'aws_iam_role'" in src
    in_schema = find_map(schema)
    say("PASS-TYPEMAP-IN-SCHEMA" if in_schema and not literal else "FAIL-TYPEMAP-HAND-KEPT",
        "NAMING_SCHEMA.json (%s) CARRIES a Terraform-type map with aws_iam_role -> IAM_ROLE: %s" % (schema.get("version"), in_schema),
        "%s STILL CARRIES an aws_iam_role literal: %s" % (LIB, literal))


def g2_suite():
    t = read(TESTS) or ""
    fn1d_test = "mdpf-lambda-lambda" in t
    # --color=no AND an ANSI strip, belt and braces. Row LGIC_NAMING-W2-S8 measured the defect:
    # pytest COLOURISES on this device, so a colourised "FAILED ..." line begins with an escape
    # sequence and the anchored ^FAILED never matches -- the failed set reads EMPTY while tests
    # fail. That is a FALSE PASS, the one direction a grading checker must never fail in.
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider",
                        "--color=no", TESTS], capture_output=True, text=True)
    out = re.sub(r"\[[0-9;]*[A-Za-z]", "", r.stdout + r.stderr)
    failed = set(re.findall(r"^FAILED (\S+)", out, re.M))
    m = re.search(r"(\d+) passed", out)
    passed = int(m.group(1)) if m else 0
    new = sorted(failed - BASE_FAILING)
    print("SUITE %s: %d passed, %d failed; base failing set %d (7b5331c8c0: 75 passed, 0 failed)" % (TESTS, passed, len(failed), len(BASE_FAILING)))
    print("NEW FAILURES AGAINST THE BASE: %d %s" % (len(new), new[:5]))
    print("A TEST NAMES mdpf-lambda-lambda (FN1d): %s" % fn1d_test)
    ok = fn1d_test and passed > 0 and not new and "error" not in out.lower().split("passed")[-1][:40]
    say("PASS-SUITE-NO-NEW-FAILURE" if ok else "FAIL-SUITE-RED-OR-NO-FN1D")


# ---------------------------------------------------------------- LN-f-1: the firm patterns, re-graded
def f1_data():
    return fence_with(F1R4, "attributed") or {}


def population():
    live = (load_json(FIX + "/LIVE_NAMES.json") or {}).get("by_type", {}).get("IAM_ROLE", [])
    return live, [n for n in live if set(re.split(r"[-_]", n.lower())) & set(ALIAS_TOKENS)]


def f1_covered():
    d = f1_data()
    att, exc, rai = d.get("attributed") or {}, d.get("excluded") or [], d.get("raise") or []
    live, want = population()
    seen = set(a.get("name") for f in FIRMS for a in att.get(f, []))
    seen |= set(e.get("name") for e in exc if isinstance(e, dict) and e.get("reason"))
    seen |= set(x.get("name") for x in rai if isinstance(x, dict) and x.get("step"))
    miss = [n for n in want if n not in seen]
    say("PASS-POPULATION-COVERED" if want and d and not miss else "FAIL-POPULATION-GAP",
        "LIVE IAM_ROLE NAMES CARRYING A FIRM ALIAS TOKEN: %d of %d roles  ATTRIBUTED, EXCLUDED WITH A REASON, OR "
        "RAISED WITH A STEP: %d  MISSING: %s" % (len(want), len(live), len(want) - len(miss), miss[:5]))


def f1_regrade():
    mod, err = naming()
    if mod is None:
        return say("FAIL-FORMS-NO-MODULE", "IMPORT %s: %s" % (LIB, err))
    att = f1_data().get("attributed") or {}
    rows = [(f, a.get("name"), a.get("canonical")) for f in FIRMS for a in att.get(f, [])]
    bad = []
    for f, name, canon in rows:
        try:
            now = mod.grade(name, "IAM_ROLE")[1]
        except Exception as exc:  # noqa: BLE001
            now = "RAISE %s" % exc
        if now != canon:
            bad.append((name, canon, now))
    for b in bad[:10]:
        print("DIFFERS: %s  record %s  grade() %s" % b)
    say("PASS-FORMS-EQUAL-GRADE" if rows and not bad else "FAIL-FORMS-DIFFER-FROM-GRADE",
        "ATTRIBUTED CANONICAL FORMS: %d  EQUAL TO grade() AT THIS TREE: %d" % (len(rows), len(rows) - len(bad)))


def f1_gaps():
    d = f1_data()
    att, rai = d.get("attributed") or {}, d.get("raise") or []
    gaps = [a.get("name") for f in FIRMS for a in att.get(f, []) if "{" in str(a.get("canonical", ""))]
    raised = {x.get("name"): x for x in rai if isinstance(x, dict)}
    unraised = [n for n in gaps if not (n in raised and raised[n].get("step") and str(raised[n].get("missing_row", "")).strip())]
    say("PASS-EVERY-GAP-RAISED" if d and not unraised else "FAIL-GAP-UNRAISED",
        "ATTRIBUTED FORMS STILL CARRYING A PLACEHOLDER: %d  EACH RAISED WITH A STEP AND ITS missing_row: %d  UNRAISED: %s"
        % (len(gaps), len(gaps) - len(unraised), unraised[:5]))


def f1_catch():
    d = f1_data()
    pats, att = d.get("patterns") or {}, d.get("attributed") or {}
    total, missed = 0, []
    for f in FIRMS:
        for a in att.get(f, []):
            total += 1
            if not fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, "")):
                missed.append((f, a.get("canonical")))
    say("PASS-CATCHES-EVERY-OWN" if pats and total and not missed else "FAIL-OWN-FORM-MISSED",
        "ATTRIBUTED CANONICAL FORMS: %d  CAUGHT BY OWN FIRM'S PATTERN: %d  MISSED: %s" % (total, total - len(missed), missed[:5]))


def f1_cross():
    d = f1_data()
    pats, att = d.get("patterns") or {}, d.get("attributed") or {}
    cross = []
    for f in FIRMS:
        for g in FIRMS:
            if g != f:
                cross += [(f, g, a.get("canonical")) for a in att.get(g, []) if fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, ""))]
    say("PASS-NO-FIRM-CROSSES" if pats and att and not cross else "FAIL-FIRM-CROSSED",
        "CROSS-FIRM CATCHES: %d %s" % (len(cross), cross[:5]))


CHECKS = {
    "g1-coverage": g1_coverage, "g1-doctored": g1_doctored, "g1-version": g1_version,
    "g1-g2": g1_g2, "g1-v2": g1_v2, "g1-fn1d": g1_fn1d,
    "g2-fn1d": g2_fn1d, "g2-regrade": g2_regrade, "g2-aws": g2_aws,
    "g2-twoway": g2_twoway, "g2-typemap": g2_typemap, "g2-suite": g2_suite,
    "f1-covered": f1_covered, "f1-regrade": f1_regrade, "f1-gaps": f1_gaps,
    "f1-catch": f1_catch, "f1-cross": f1_cross,
}


def selftest_negative():
    passed = []
    for name in sorted(CHECKS):
        out = subprocess.run([sys.executable, __file__, name], capture_output=True, text=True).stdout
        v = [ln for ln in out.splitlines() if ln.startswith("VERDICT: ")]
        verdict = v[-1][9:] if v else "NO-VERDICT"
        print("%-12s %s" % (name, verdict))
        if verdict.startswith("PASS"):
            passed.append(name)
    print("SELFTEST-NEGATIVE: %d of %d subcommands PASS on this tree %s" % (len(passed), len(CHECKS), passed))


def main(argv):
    if len(argv) == 2 and argv[1] == "--list":
        print("\n".join(sorted(CHECKS)))
        return 0
    if not os.path.isdir("org") or not os.path.isdir(".tools"):
        print("run from the worktree root (org/ and .tools/ not found in %s)" % os.getcwd())
        print("VERDICT: FAIL-WRONG-ROOT")
        return 0
    if len(argv) == 2 and argv[1] == "selftest-negative":
        selftest_negative()
        return 0
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: check_ln_r4.py <%s>" % "|".join(sorted(CHECKS)))
        print("VERDICT: FAIL-USAGE")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
