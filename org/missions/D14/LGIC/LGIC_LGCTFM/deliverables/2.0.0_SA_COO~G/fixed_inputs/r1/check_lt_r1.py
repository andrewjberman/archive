#!/usr/bin/env python3
"""check_lt_r1.py -- LGIC_LGCTFM round 1's mechanical criteria, one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-1 issuance (decomposition v1 @686d196fa1 s.3a). Run from the
worktree root: `python <this file> <subcommand>`. Every subcommand prints its evidence, a DENOMINATOR
where one exists, and exactly one line `VERDICT: PASS-<X>` or `VERDICT: FAIL-<X>`, and exits 0. A missing
input is a FAIL verdict, never a traceback. No PASS string is a substring of another's, because
proof-of-spec-check greps <expect> UNANCHORED.

`--list` prints the subcommands. `selftest-arms` drives EVERY arm's PURE CORE against a GREEN fixture that
must PASS and a DOCTORED fixture that must FAIL, each arm alone (A-23: an arm that cannot be made to fail is
a constant wearing a measurement's clothes).

THE ONE DEPENDENCY OUTSIDE THE STANDARD LIBRARY: the schema arms import `jsonschema` (4.26 on this box at the
cut). A JSON schema cannot be graded without a validator, and re-implementing one here would be a second
carrier of the validator's rule. An absent `jsonschema` is a FAIL verdict naming it, never a pass.

THE INTERFACES THE ARMS READ are fixed in each order's WORKER FACE, not here: paths, CLI verbs, field names.
Where this file names a constant taken from a record (the row kinds, the tension kinds, the axes, the cell
statuses, R19's steps, the edge types), the record is cited beside it.

ASCII only. LF endings.
"""
from __future__ import annotations

import ast
import copy
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

# 9 levels: r1 / fixed_inputs / <serial> / deliverables / LGIC_LGCTFM / LGIC / D14 / missions / org
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
FIX = ROOT + "/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1"
W1 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~1"
W2 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~2"
W3 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~3"

SCHEMA = "org/standards/LGCTFM_CONTRACT.schema.json"
NAMING = "org/standards/NAMING_SCHEMA.json"
PLANTED = FIX + "/PLANTED_CONTRACT.json"
FORKS_FIX = FIX + "/FORK_CONTROLS.json"
SUBJECT_FIX = FIX + "/SUBJECT_CONTROL.json"
METHOD = "infra/logic/10_LEGACY_TRANSFORM.md"
SKILL = ".claude/skills/lgctfm/SKILL.md"
ENGINE = "lib/opal_lgctfm.py"
RENDER = "lib/lgctfm_render.py"
TESTS = "lib/tests/test_opal_lgctfm.py"
RUNHOME = "workflows/legacy_transform/run_home.py"
SUBJECT_DIR = "workflows/legacy_transform/blackdiamond-49financial"
RECV = ".tools/receiving-check.py"
GATE = ".tools/naming-gate.py"
ENFORCE_FLAG = "org/mcp/naming-gate.enforce"
REGISTRIES = ("infra/logic/registry/remediations.json",
              "infra/logic/registry/scopes.json",
              "org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json")
ADVI_CHANNEL = "org/missions/D8/ADVI/ADVI_FIRMBKTS/surprise-channel/investigations/INVESTIGATION_v1.md"

WALK = W1 + "/walk/contract.json"
WALK_PLANT = W1 + "/walk/PLANT.json"
UNTYPEABLE_PLANT = W1 + "/walk/PLANT_UNTYPEABLE.json"
FORKS_RUN = W1 + "/forks/contract.json"
PLAN_DIR = W2 + "/plan_r1"
DETERMINISM = W3 + "/DETERMINISM.json"
REFUSAL_DIR = W3 + "/PLANTED_REFUSAL"
REPRO = W3 + "/REPRODUCTION.json"
CARD = W3 + "/ANDREW_CARD.md"

# 11_LGCTFM_CONTRACT_SCHEMA_RECORD.md s.1.2 (row kinds), s.3 (cell statuses), s.4 (axis, kind)
ROW_KINDS = {"RESOURCE", "PLANE", "FORK"}
CELL_STATUSES = {"MEASURED", "UNMEASURED", "INFERRED", "NOT_MEASURABLE"}
AXES = {"A1", "A2", "A3", "A4", "A5", "PROCESS", "IDENTITY"}
TENSION_KINDS = {"HOME", "FORMAT", "GRAMMAR", "COMPUTE", "DECLARATION", "PROCESS", "IDENTITY"}
# PRD v1.4 DEC-8 / canon R19
R19_STEPS = ["MAP", "CLASSIFY", "RULE", "PORT", "REPOINT", "PROVE"]
# the record s.6, adopted from evidence-model.md
EDGE_TYPES = {"CALLS", "READS", "WRITES", "TRIGGERS", "INVOKES", "STARTS", "PUBLISHES", "SERVES",
              "AUTHORIZES", "MONITORS", "REPLACES"}
PACKAGE_FIELDS = ("objective", "dependencies", "reads", "writes", "acceptance_proof", "rollback", "owner",
                  "replacement_obligation")
SIGNOFF_OWNERS = {"1.0.0_SA_CTO", "2.0.0_SA_COO"}
BUILDER_FNS = {"name", "address", "grade", "lookup", "fence_patterns"}
REFUSAL_TOKENS = {"bare": "bare-value", "one_api": "trigger-denominator",
                  "no_instrument": "evidence-instrument", "no_vintage": "vintage"}
METHOD_TERMS = ("walk order", "fork test", "twin", "tension", "plan", "mark", "coverage hole")


# ============================================================================ plumbing
def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)
    return 0


def verdict(ok, pass_s, fail_s, lines):
    return say(pass_s if ok else fail_s, *lines)


def ab(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def read(path):
    p = ab(path)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_json(path):
    t = read(path)
    if t is None:
        return None, "absent: %s" % path
    try:
        return json.loads(t), ""
    except ValueError as exc:
        return None, "not JSON: %s (%s)" % (path, exc)


def run(argv, cwd=None, timeout=240, env=None):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=cwd or REPO, timeout=timeout, env=env)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds: %s" % (timeout, " ".join(argv))
    except OSError as exc:
        return 127, "did not run: %s" % exc


def quoted(out):
    """A subprocess's own output, each line behind a gutter, so a tool that prints its OWN 'VERDICT:' line can never
    add a second verdict line to this arm's output (proof-of-spec-check greps <expect> unanchored)."""
    return ["  | " + ln for ln in (out or "").splitlines()]


def git(*args):
    return run(["git"] + list(args), timeout=120)


def base_ref():
    rc, out = git("merge-base", "HEAD", "CLOUD")
    return out.strip() if rc == 0 and out.strip() else None


def is_cell(x):
    return isinstance(x, dict) and "value" in x and "status" in x and "evidence" in x


def cell_value(x):
    return x.get("value") if isinstance(x, dict) and "value" in x else None


# ============================================================================ schema cores (LT-s-1)
def validator_for(schema):
    try:
        import jsonschema  # noqa: F401  (the one non-stdlib import; see the docstring)
        from jsonschema import validators
    except ImportError:
        return None, "jsonschema is not importable -- the schema arms cannot grade and FAIL"
    try:
        cls = validators.validator_for(schema)
        cls.check_schema(schema)
        return cls(schema), ""
    except Exception as exc:  # noqa: BLE001
        return None, "the schema is not a valid JSON Schema: %s" % str(exc)[:200]


def validate(validator, doc):
    errs = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    return [("/".join(str(p) for p in e.path) or "<root>") + ": " + e.message[:120] for e in errs]


def doctor(contract, which):
    """The four planted INVALID contracts, derived from the valid one."""
    c = copy.deepcopy(contract)
    if which == "bare":
        c["rows"][0]["current"]["name"] = c["rows"][0]["current"]["name"]["value"]
    elif which == "one_api":
        c["trigger_denominator"].pop("list_schedules", None)
    elif which == "no_instrument":
        c["rows"][0]["current"]["name"]["evidence"].pop("instrument", None)
    elif which == "no_vintage":
        c["subject"]["vintage"].pop("registry_hash", None)
    return c


def core_schema_accepts(validator, contract):
    errs = validate(validator, contract)
    return not errs, ["planted VALID contract: %d validation error(s)" % len(errs)] + ["  " + e for e in errs[:8]]


def core_schema_refuses(validator, contract, which):
    errs = validate(validator, doctor(contract, which))
    return bool(errs), ["planted INVALID contract (%s): %d validation error(s)" % (which, len(errs))] + \
        ["  " + e for e in errs[:5]]


def schema_inputs(tag):
    schema, why = load_json(SCHEMA)
    if schema is None:
        return None, None, say("FAIL-%s" % tag, why)
    contract, why2 = load_json(PLANTED)
    if contract is None:
        return None, None, say("FAIL-%s" % tag, why2)
    v, why3 = validator_for(schema)
    if v is None:
        return None, None, say("FAIL-%s" % tag, why3)
    return v, contract, None


def s1_valid():
    v, c, done = schema_inputs("S1-PLANTED-VALID-ACCEPTED")
    if done is not None:
        return done
    ok, lines = core_schema_accepts(v, c)
    return verdict(ok, "PASS-S1-PLANTED-VALID-ACCEPTED", "FAIL-S1-PLANTED-VALID-ACCEPTED", lines)


def _s1_refuse(which, tag):
    v, c, done = schema_inputs(tag)
    if done is not None:
        return done
    ok, lines = core_schema_refuses(v, c, which)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def s1_bare_value():
    return _s1_refuse("bare", "S1-BARE-VALUE-REFUSED")


def s1_one_api():
    return _s1_refuse("one_api", "S1-ONE-API-REFUSED")


def s1_no_instrument():
    return _s1_refuse("no_instrument", "S1-NO-INSTRUMENT-REFUSED")


def core_node_types(schema, naming):
    got = set(((schema.get("$defs") or {}).get("node_type") or {}).get("enum") or [])
    by_kind = set(((naming.get("kind") or {}).get("by_type") or {}).keys())
    other = set((naming.get("types_not_graded_by_kind") or {}).keys())
    want = by_kind | other
    lines = ["NAMING_SCHEMA.json: kind.by_type %d + types_not_graded_by_kind %d = %d node types (disjoint: %s)"
             % (len(by_kind), len(other), len(want), not (by_kind & other)),
             "schema $defs.node_type.enum: %d value(s)" % len(got),
             "  in the vocabulary, absent from the schema: %s" % sorted(want - got),
             "  in the schema, absent from the vocabulary: %s" % sorted(got - want)]
    return bool(want) and got == want, lines


def s1_node_types():
    schema, why = load_json(SCHEMA)
    naming, why2 = load_json(NAMING)
    if schema is None or naming is None:
        return say("FAIL-S1-NODE-TYPES-BY-SUBTRACTION", why or why2)
    ok, lines = core_node_types(schema, naming)
    return verdict(ok, "PASS-S1-NODE-TYPES-BY-SUBTRACTION", "FAIL-S1-NODE-TYPES-BY-SUBTRACTION", lines)


def core_enums(schema):
    defs = schema.get("$defs") or {}
    want = {"row_kind": ROW_KINDS, "cell_status": CELL_STATUSES, "axis": AXES, "tension_kind": TENSION_KINDS}
    lines, ok = [], True
    for key, vals in sorted(want.items()):
        got = set((defs.get(key) or {}).get("enum") or [])
        same = got == vals
        ok = ok and same
        lines.append("  $defs.%-12s %-5s schema=%s record=%s" % (key, "OK" if same else "DIFF", sorted(got), sorted(vals)))
    return ok, ["the four enums the record adopts or mints (11_LGCTFM_CONTRACT_SCHEMA_RECORD.md s.1.2, s.3, s.4)"] + lines


def s1_enums():
    schema, why = load_json(SCHEMA)
    if schema is None:
        return say("FAIL-S1-ENUMS-FROM-RECORD", why)
    ok, lines = core_enums(schema)
    return verdict(ok, "PASS-S1-ENUMS-FROM-RECORD", "FAIL-S1-ENUMS-FROM-RECORD", lines)


# ============================================================================ receiving check (LT-s-2)
def parse_recv(out):
    m = re.search(r"^VERDICT:\s+(\d+) ACCEPT \| (\d+) HAND BACK(?: \| (\d+) NOT-BOUND)? \| (\d+) UNCHECKED", out, re.M)
    if not m:
        return None
    return {"ACCEPT": int(m.group(1)), "HAND BACK": int(m.group(2)), "UNCHECKED": int(m.group(4))}


def core_recv(out, expect, token=None):
    v = parse_recv(out)
    lines = ["receiving-check verdict line: %s" % v,
             "labelled lgctfm-contract: %s" % ("lgctfm-contract" in out)]
    if v is None:
        return False, lines + ["no VERDICT line read"]
    ok = v.get(expect) == 1 and sum(v.values()) == 1
    if expect != "UNCHECKED":
        ok = ok and "lgctfm-contract" in out
    if token:
        present = token in out
        lines.append("refusal names the defect token %r: %s" % (token, present))
        ok = ok and present
    return ok, lines


def _recv_on(contract_doc, name):
    d = tempfile.mkdtemp(prefix="lt_r1_recv_")
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(contract_doc, fh, indent=1, sort_keys=True)
    return run([sys.executable, ab(RECV), p], timeout=240)


def _s2(which, expect, tag):
    c, why = load_json(PLANTED)
    if c is None:
        return say("FAIL-" + tag, why)
    if not os.path.isfile(ab(RECV)):
        return say("FAIL-" + tag, "absent: %s" % RECV)
    doc = c if which is None else doctor(c, which)
    rc, out = _recv_on(doc, "planted.lgctfm-contract.json")
    ok, lines = core_recv(out, expect, REFUSAL_TOKENS.get(which) if which else None)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag,
                   ["planted: %s (rc=%d)" % (which or "VALID", rc)] + lines + ["--- output (first 25 lines) ---"]
                   + quoted(out)[:25])


def s2_accept_valid():
    return _s2(None, "ACCEPT", "S2-VALID-ACCEPTED")


def s2_refuse_bare():
    return _s2("bare", "HAND BACK", "S2-BARE-VALUE-HANDED-BACK")


def s2_refuse_one_api():
    return _s2("one_api", "HAND BACK", "S2-ONE-API-HANDED-BACK")


def s2_refuse_no_instrument():
    return _s2("no_instrument", "HAND BACK", "S2-NO-INSTRUMENT-HANDED-BACK")


def s2_refuse_no_vintage():
    return _s2("no_vintage", "HAND BACK", "S2-NO-VINTAGE-HANDED-BACK")


def s2_unchecked_regress():
    tag = "S2-UNKNOWN-TYPE-STAYS-UNCHECKED"
    if not os.path.isfile(ab(RECV)):
        return say("FAIL-" + tag, "absent: %s" % RECV)
    rc, out = _recv_on({"not": "a contract"}, "unrelated.data.json")
    v = parse_recv(out)
    ok = v is not None and v["UNCHECKED"] == 1 and v["ACCEPT"] == 0 and v["HAND BACK"] == 0
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["an unrecognised artifact: %s (rc=%d)" % (v, rc)])


def s2_selftest():
    tag = "S2-RECEIVING-SELFTEST-GREEN"
    if not os.path.isfile(ab(RECV)):
        return say("FAIL-" + tag, "absent: %s" % RECV)
    rc, out = run([sys.executable, ab(RECV), "--self-test"], timeout=240)
    return verdict(rc == 0, "PASS-" + tag, "FAIL-" + tag, ["receiving-check.py --self-test rc=%d" % rc]
                   + quoted(out)[-12:])


# ============================================================================ the walk (LT-e-1)
def control_members(subject_control):
    """(name, node_type) the hand-built control NAMES: its three buckets, their three policies and the
    pattern-rule sample with {a,b,c} expanded and parenthetical notes dropped."""
    buckets = ["opal-data-bd", "opal-data-inf", "opal-data-cot"]
    members = [(b, "S3_BUCKET") for b in buckets] + [(b, "S3_BUCKET_POLICY") for b in buckets]
    sample = ((subject_control.get("trigger_plane") or {}).get("named_pattern_rules_sample") or [])
    for raw in sample:
        s = re.sub(r"\s*\(.*\)\s*$", "", raw).strip()
        m = re.search(r"\{([^}]+)\}", s)
        if m:
            for part in m.group(1).split(","):
                members.append((s[:m.start()] + part.strip() + s[m.end():], "EVENT_RULE"))
        else:
            members.append((s, "EVENT_RULE"))
    return members


def rows_by_name(contract):
    out = {}
    for r in contract.get("rows") or []:
        cur = r.get("current") or {}
        nm = cell_value(cur.get("name"))
        if isinstance(nm, str):
            out.setdefault(nm, []).append(r)
    return out


def core_control(contract, members):
    idx = rows_by_name(contract)
    found, lines = 0, []
    for nm, nt in members:
        hit = any(r.get("node_type") == nt for r in idx.get(nm, []))
        found += hit
        if not hit:
            lines.append("  MISSING  %-16s %s" % (nt, nm))
    return bool(members) and found == len(members), \
        ["control members found as rows: %d of %d (denominator = the control's named members)" % (found, len(members))] + lines


def e1_control():
    tag = "E1-CONTROL-MEMBERS-WALKED"
    c, why = load_json(WALK)
    sc, why2 = load_json(SUBJECT_FIX)
    if c is None or sc is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_control(c, control_members(sc))
    s3keys = sum(1 for r in c.get("rows") or [] if r.get("node_type") == "S3Key")
    lines.append("context, not graded: S3Key rows %d (the control counted 228 at its 2026-09-13 vintage)" % s3keys)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_triggers(contract):
    td = contract.get("trigger_denominator") or {}
    lines, ok = [], True
    for api in ("list_rules", "list_schedules"):
        c = td.get(api)
        v = cell_value(c)
        inst = ((c or {}).get("evidence") or {}).get("instrument", "") if is_cell(c) else ""
        good = (is_cell(c) and c.get("status") == "MEASURED" and isinstance(v, int) and not isinstance(v, bool)
                and v >= 1 and re.search(r"comp[-_]trigger", inst or "") is not None)
        ok = ok and good
        lines.append("  %-15s value=%r status=%r instrument=%r -> %s" % (api, v, (c or {}).get("status") if isinstance(c, dict) else None, inst, "OK" if good else "BAD"))
    return ok, ["trigger denominator, BOTH APIs, each MEASURED >= 1 through comp-trigger (brief IV.6)"] + lines


def e1_triggers():
    tag = "E1-BOTH-TRIGGER-APIS-COUNTED"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_triggers(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_cells(contract):
    n_rows = n_cells = 0
    bad = []
    for r in contract.get("rows") or []:
        if r.get("kind") == "FORK":
            continue
        n_rows += 1
        for half in ("current", "desired"):
            for field, c in sorted((r.get(half) or {}).items()):
                n_cells += 1
                ev = c.get("evidence") if isinstance(c, dict) else None
                if not is_cell(c):
                    bad.append("%s %s.%s: bare value %r" % (r.get("row_id"), half, field, c))
                elif c.get("status") not in CELL_STATUSES:
                    bad.append("%s %s.%s: status %r" % (r.get("row_id"), half, field, c.get("status")))
                elif not isinstance(ev, dict) or not str(ev.get("instrument") or "").strip() \
                        or not str(ev.get("blind_spot") or "").strip():
                    bad.append("%s %s.%s: evidence.instrument/blind_spot empty" % (r.get("row_id"), half, field))
    lines = ["RESOURCE/PLANE rows %d, cells %d, defective %d" % (n_rows, n_cells, len(bad))] + ["  " + b for b in bad[:10]]
    return n_rows > 0 and not bad, lines


def e1_cells():
    tag = "E1-EVERY-CELL-NAMES-ITS-INSTRUMENT"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_cells(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_plant(contract, plant):
    nm = (plant or {}).get("name")
    rows = rows_by_name(contract).get(nm, []) if nm else []
    unm = [r for r in rows if any(isinstance(c, dict) and c.get("status") == "UNMEASURED"
                                  for c in (r.get("current") or {}).values())]
    return bool(nm) and bool(unm), ["planted name: %r" % nm, "rows carrying it: %d; with an UNMEASURED current cell: %d"
                                    % (len(rows), len(unm))]


def e1_unmeasured_plant():
    tag = "E1-PLANT-SURFACES-UNMEASURED"
    c, why = load_json(WALK)
    p, why2 = load_json(WALK_PLANT)
    if c is None or p is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_plant(c, p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_method(text):
    heads = [ln.lower() for ln in text.splitlines() if ln.startswith("#")]
    missing = [t for t in METHOD_TERMS if not any(t in h for h in heads)]
    return not missing, ["headings read: %d; terms required in a heading: %d; missing: %s"
                         % (len(heads), len(METHOD_TERMS), missing)]


def e1_method():
    tag = "E1-METHOD-DOCUMENT-SECTIONED"
    t = read(METHOD)
    if t is None:
        return say("FAIL-" + tag, "absent: %s" % METHOD)
    ok, lines = core_method(t)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_skill(text):
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    fm = m.group(1) if m else ""
    ok = bool(m) and re.search(r"^name:\s*lgctfm\s*$", fm, re.M) is not None and ENGINE in text
    return ok, ["frontmatter present: %s; name: lgctfm: %s; body invokes %s: %s"
                % (bool(m), re.search(r"^name:\s*lgctfm\s*$", fm, re.M) is not None, ENGINE, ENGINE in text)]


def e1_skill():
    tag = "E1-SKILL-INVOKES-ENGINE"
    t = read(SKILL)
    if t is None:
        return say("FAIL-" + tag, "absent: %s" % SKILL)
    ok, lines = core_skill(t)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def local_modules():
    d = ab("lib")
    return {f[:-3] for f in os.listdir(d) if f.endswith(".py")} if os.path.isdir(d) else set()


def core_stdlib(src, local):
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return False, ["does not parse: %s" % exc]
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    std = set(getattr(sys, "stdlib_module_names", ()))
    foreign = sorted(n for n in names if n not in std and n not in local and n not in ("lib", "__future__"))
    return not foreign, ["top-level imports %d: %s" % (len(names), sorted(names)), "outside stdlib and lib/: %s" % foreign]


def e1_stdlib():
    tag = "E1-ENGINE-STDLIB-ONLY"
    t = read(ENGINE)
    if t is None:
        return say("FAIL-" + tag, "absent: %s" % ENGINE)
    ok, lines = core_stdlib(t, local_modules())
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_ascii(raw):
    n = sum(1 for b in raw if b > 127)
    return n == 0 and len(raw) > 0, ["bytes %d, non-ASCII %d" % (len(raw), n)]


def e1_ascii():
    tag = "E1-ENGINE-ASCII-ONLY"
    p = ab(ENGINE)
    if not os.path.isfile(p):
        return say("FAIL-" + tag, "absent: %s" % ENGINE)
    ok, lines = core_ascii(open(p, "rb").read())
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ desired + forks (LT-e-2)
def import_naming():
    sys.path.insert(0, ab("lib"))
    try:
        import importlib
        return importlib.import_module("opal_naming"), ""
    except Exception as exc:  # noqa: BLE001
        return None, "lib/opal_naming.py did not import: %s" % exc


def core_reproduce(contract, builders):
    n = ok_n = 0
    bad = []
    for r in contract.get("rows") or []:
        d = r.get("desired") or {}
        b = cell_value(d.get("builder"))
        if not isinstance(b, dict) or b.get("fn") not in BUILDER_FNS:
            continue
        n += 1
        fn = builders.get(b["fn"])
        try:
            got = fn(*(b.get("args") or []), **(b.get("kwargs") or {}))
            raised = None
        except Exception as exc:  # noqa: BLE001
            got, raised = None, exc
        if raised is not None:
            v = cell_value(d.get("verdict"))
            if v == "NOT_COVERED":
                # LT-e-3 mints NOT_COVERED for a row whose node type the SCHEMA does not cover: grade()
                # raises G1.1 and the engine must return the row NOT GRADED. Accepting it here needs both
                # halves, or this branch would launder a fabricated form: the raise must be the coverage
                # error, and the contract must carry NO form. A registry-defect RAISE keeps its own branch.
                good = ("is not a node type" in str(raised)) and cell_value(d.get("form")) is None
            else:
                good = v == "RAISE" and bool(str(cell_value(d.get("missing_registry_row")) or "").strip())
        else:
            good = got == cell_value(d.get("form")) or str(got) == str(cell_value(d.get("form")))
        ok_n += good
        if not good:
            bad.append("%s %s(%s) -> %s ; contract form=%r verdict=%r" % (r.get("row_id"), b["fn"], b.get("args"),
                       ("RAISE " + str(raised)[:60]) if raised else repr(got)[:80], cell_value(d.get("form")),
                       cell_value(d.get("verdict"))))
    return n > 0 and ok_n == n, ["rows with a builder call the checker can make: %d; reproduced: %d" % (n, ok_n)] + \
        ["  " + x for x in bad[:10]]


def e2_reproduce():
    tag = "E2-DESIRED-EQUALS-BUILDER"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    mod, why2 = import_naming()
    if mod is None:
        return say("FAIL-" + tag, why2)
    builders = {k: getattr(mod, k) for k in BUILDER_FNS if hasattr(mod, k)}
    ok, lines = core_reproduce(c, builders)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def _stem(member):
    s = re.split(r"\{| \(", member)[0]
    return s, "_legacy" in member


def fork_rows(contract):
    rows = {r.get("row_id"): r for r in contract.get("rows") or []}
    out = []
    for r in contract.get("rows") or []:
        if r.get("kind") != "FORK":
            continue
        paths = []
        for mid in r.get("members") or []:
            m = rows.get(mid) or {}
            p = cell_value((m.get("current") or {}).get("arn_or_path"))
            paths.append((mid, str(p or "")))
        out.append((r, paths))
    return out


def _match_positive(members, paths):
    used, ok = set(), True
    for m in members:
        stem, legacy = _stem(m)
        hit = next((mid for mid, p in paths if mid not in used and stem in p and (("_legacy" in p) == legacy)), None)
        if hit is None:
            ok = False
            break
        used.add(hit)
    return ok


def core_forks(contract, controls):
    frs = fork_rows(contract)
    lines, found = [], 0
    positives = controls.get("positives") or []
    for pc in positives:
        hit = None
        for r, paths in frs:
            if _match_positive(pc.get("members") or [], paths):
                hit = r
                break
        canon = cell_value((hit or {}).get("canonical_member"))
        marked = hit is not None and (canon == "RULING-OWED" or canon in (hit.get("members") or []))
        found += bool(hit) and marked
        lines.append("  %-7s %-5s canonical=%r  %s" % (pc.get("id"), "FOUND" if hit else "ABSENT", canon, pc.get("label")))
    return bool(positives) and found == len(positives), \
        ["positive fork controls found as FORK rows with the canonical member marked: %d of %d (FORK_CONTROLS.json)"
         % (found, len(positives)), "FORK rows in the contract: %d" % len(frs)] + lines


def e2_forks():
    tag = "E2-POSITIVE-FORKS-FOUND"
    c, why = load_json(FORKS_RUN)
    f, why2 = load_json(FORKS_FIX)
    if c is None or f is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_forks(c, f)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_negative(contract, controls):
    neg = (controls.get("negative") or [{}])[0]
    a, b = [_stem(m)[0] for m in (neg.get("members") or ["", ""])[:2]]
    allpaths = [str(cell_value((r.get("current") or {}).get("arn_or_path")) or "") for r in contract.get("rows") or []]
    has_a = sum(1 for p in allpaths if a and a in p)
    has_b = sum(1 for p in allpaths if b and b in p)
    bad = [r.get("row_id") for r, paths in fork_rows(contract)
           if any(a in p for _, p in paths) and any(b in p for _, p in paths)]
    lines = ["negative control %r: rows reaching %r: %d, reaching %r: %d (both must be > 0, or the zero is vacuous)"
             % (neg.get("id"), a, has_a, b, has_b), "FORK rows joining them: %s" % bad]
    return bool(a and b) and has_a > 0 and has_b > 0 and not bad, lines


def e2_negative():
    tag = "E2-SMARTX-PAIR-NOT-A-FORK"
    c, why = load_json(FORKS_RUN)
    f, why2 = load_json(FORKS_FIX)
    if c is None or f is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_negative(c, f)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_raise(contracts):
    raises = oop_raise = 0
    for c in contracts:
        for r in c.get("rows") or []:
            d = r.get("desired") or {}
            v = cell_value(d.get("verdict"))
            miss = str(cell_value(d.get("missing_registry_row")) or "").strip()
            if v == "RAISE" and miss:
                raises += 1
            if v == "OUT-OF-PATTERN" and miss:
                oop_raise += 1
    return raises >= 1 and oop_raise == 0, ["RAISE rows naming their missing registry row: %d" % raises,
                                            "OUT-OF-PATTERN rows carrying a missing registry row (a guessed grade): %d" % oop_raise]


def e2_raise():
    tag = "E2-RAISE-ROW-NAMES-MISSING-ROW"
    cs = [x for x in (load_json(WALK)[0], load_json(FORKS_RUN)[0]) if x is not None]
    if not cs:
        return say("FAIL-" + tag, "absent: %s and %s" % (WALK, FORKS_RUN))
    ok, lines = core_raise(cs)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["contracts read: %d" % len(cs)] + lines)


# ============================================================================ tensions (LT-e-3)
def core_rule_printed(contract):
    rule = str(contract.get("ranking_rule") or "")
    pos = [rule.find(t) for t in ("irreversible", "client_facing", "live", "rules_colliding", "object")]
    ok = all(p >= 0 for p in pos) and pos == sorted(pos)
    return ok, ["ranking_rule: %r" % rule[:200], "positions of irreversible/client_facing/live/rules_colliding/object: %s" % pos]


def e3_rule():
    tag = "E3-RANKING-RULE-PRINTED"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_rule_printed(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_factors(contract):
    ts = contract.get("tensions") or []
    bad = []
    for t in ts:
        f = t.get("factors") or {}
        for k, pat in (("irreversible", r"."), ("client_facing", r"07_ROUTING_REDERIVATION|LEGACY_SERVED_PATHS"),
                       ("live", r"trading_calendar"), ("rules_colliding", r".")):
            c = f.get(k)
            inst = str(((c or {}).get("evidence") or {}).get("instrument") or "") if is_cell(c) else ""
            if not is_cell(c) or c.get("status") not in CELL_STATUSES or not re.search(pat, inst):
                bad.append("%s factor %s: instrument %r" % (t.get("tension_id"), k, inst[:60]))
    return bool(ts) and not bad, ["tensions %d; factor cells %d; defective %d" % (len(ts), 4 * len(ts), len(bad))] + \
        ["  " + b for b in bad[:10]]


def e3_factors():
    tag = "E3-FOUR-FACTORS-MEASURED"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_factors(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def rank_key(t):
    f = t.get("factors") or {}

    def b(k):
        return bool(cell_value(f.get(k)))
    rc = cell_value(f.get("rules_colliding"))
    rc = rc if isinstance(rc, int) and not isinstance(rc, bool) else 0
    oc = t.get("object_count") if isinstance(t.get("object_count"), int) else 0
    return (not b("irreversible"), not b("client_facing"), not b("live"), -rc, -oc)


def core_order(contract):
    ts = contract.get("tensions") or []
    given = [t.get("tension_id") for t in ts]
    want = [t.get("tension_id") for t in sorted(ts, key=rank_key)]
    first = next((i for i, (a, b) in enumerate(zip(given, want)) if a != b), None)
    return bool(ts) and given == want, ["tensions %d; re-sorted by the printed rule; first divergence at index %s" % (len(ts), first)]


def e3_order():
    tag = "E3-ORDER-REPRODUCED-FROM-CELLS"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_order(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_types(contract):
    ts = contract.get("tensions") or []
    bad = [t.get("tension_id") for t in ts
           if t.get("axis") not in AXES or t.get("kind") not in TENSION_KINDS
           or not t.get("deciding_rules") or not all(re.match(r"^R\d+$", str(x)) for x in t.get("deciding_rules"))]
    return bool(ts) and not bad, ["tensions %d; off the closed type set: %d %s" % (len(ts), len(bad), bad[:8])]


def e3_types():
    tag = "E3-TENSION-TYPES-CLOSED"
    c, why = load_json(WALK)
    if c is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_types(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_untypeable(contract, plant):
    """The untypeable node is RETURNED, never silently graded -- in either carrier shape (R-36).

    OLD shape, round 1's first walk: the row sat in contract.rows carrying desired.verdict NOT_COVERED.
    NEW shape, R-36: the row is NOT in contract.rows at all; it is carried in PLANT_UNTYPEABLE.json with
    verdict NOT_COVERED and counted. Both grade here, so the historical artifact keeps its verdict and the
    amendment's runs get graded on what they actually write.
    """
    entries, count = _carrier(plant)
    if entries is None:
        return False, ["the untypeable carrier is not an object"]
    if any(e.get("_shape") == "old" for e in entries):
        nm = entries[0].get("name")
        rows = rows_by_name(contract).get(nm, []) if nm else []
        ids = {r.get("row_id") for r in rows}
        nc = [r for r in rows if cell_value((r.get("desired") or {}).get("verdict")) == "NOT_COVERED"]
        graded = [t.get("tension_id") for t in contract.get("tensions") or [] if t.get("row_id") in ids]
        return bool(nc) and not graded, ["OLD carrier shape; planted untypeable name %r: rows %d, "
                                         "NOT_COVERED %d, tensions on it %s" % (nm, len(rows), len(nc), graded)]
    names = [e.get("name") for e in entries]
    by_name = rows_by_name(contract)
    in_rows = [n for n in names if by_name.get(n)]
    nc = [e for e in entries if e.get("verdict") == "NOT_COVERED"]
    ok = bool(entries) and len(nc) == len(entries) and not in_rows and         (count is None or count == len(entries))
    return ok, ["NEW carrier shape; carried %d, NOT_COVERED %d, also present in contract.rows %d %s, "
                "carrier count %r" % (len(entries), len(nc), len(in_rows), in_rows[:3], count)]


def e3_untypeable():
    tag = "E3-UNTYPEABLE-RETURNED-NOT-GRADED"
    c, why = load_json(WALK)
    p, why2 = load_json(UNTYPEABLE_PLANT)
    if c is None or p is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_untypeable(c, p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ the plan (LT-p-1)
def core_pkg_fields(plan):
    pk = plan.get("packages") or []
    bad = ["%s missing %s" % (p.get("package_id"), [f for f in PACKAGE_FIELDS if f not in p or p.get(f) in (None, "")])
           for p in pk if any(f not in p or p.get(f) in (None, "") for f in PACKAGE_FIELDS)]
    return bool(pk) and not bad, ["packages %d; missing one of the eight fields: %d" % (len(pk), len(bad))] + ["  " + b for b in bad[:8]]


def _plan():
    return load_json(PLAN_DIR + "/plan.json")


def p1_fields():
    tag = "P1-EIGHT-FIELDS-EVERY-PACKAGE"
    p, why = _plan()
    if p is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_pkg_fields(p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_r19(plan):
    pk = plan.get("packages") or []
    steps = [p.get("step") for p in pk]
    idx = [R19_STEPS.index(s) if s in R19_STEPS else -1 for s in steps]
    ok = bool(pk) and -1 not in idx and idx == sorted(idx)
    return ok, ["packages %d; steps in order read: %s" % (len(pk), steps[:30])]


def p1_r19():
    tag = "P1-R19-ORDER"
    p, why = _plan()
    if p is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_r19(p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_served(plan, contract):
    served = {}
    for r in contract.get("rows") or []:
        if cell_value((r.get("current") or {}).get("client_facing")) is True:
            served[r.get("row_id")] = str(cell_value((r.get("current") or {}).get("arn_or_path")) or "")
    need = bad = 0
    for p in plan.get("packages") or []:
        ws = [str(w) for w in p.get("writes") or []]
        moves = any(w in served or any(sp and (sp in w or w in sp) for sp in served.values()) for w in ws)
        if not moves:
            continue
        need += 1
        owners = set(p.get("signoff_owners") or [])
        if p.get("never_widen_signoff_owed") is not True or not SIGNOFF_OWNERS <= owners:
            bad += 1
    return need > 0 and bad == 0, ["client-facing rows %d; packages writing a served row %d; missing the never-widen flag "
                                   "or an owner %d" % (len(served), need, bad)]


def p1_served():
    tag = "P1-SERVED-KEYS-OWE-SIGNOFF"
    p, why = _plan()
    c, why2 = load_json(PLAN_DIR + "/contract.json")
    if p is None or c is None:
        return say("FAIL-" + tag, why or why2)
    ok, lines = core_served(p, c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_not_executed(plan):
    pk = plan.get("packages") or []
    bad = [p.get("package_id") for p in pk if p.get("status") != "PLANNED"]
    return plan.get("executed") is False and bool(pk) and not bad, ["executed=%r; packages %d; status != PLANNED: %s"
                                                                     % (plan.get("executed"), len(pk), bad[:8])]


def p1_not_executed():
    tag = "P1-NOTHING-EXECUTED"
    p, why = _plan()
    if p is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_not_executed(p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def p1_regenerates():
    tag = "P1-PLAN-REGENERATES-BYTE-EQUAL"
    src = ab(PLAN_DIR)
    if not all(os.path.isfile(os.path.join(src, f)) for f in ("contract.json", "plan.json", "plan.md")):
        return say("FAIL-" + tag, "absent: %s/{contract.json,plan.json,plan.md}" % PLAN_DIR)
    d = tempfile.mkdtemp(prefix="lt_r1_plan_")
    with open(os.path.join(src, "contract.json"), "rb") as a, open(os.path.join(d, "contract.json"), "wb") as b:
        b.write(a.read())
    rc, out = run([sys.executable, ab(ENGINE), "plan", d], timeout=240)
    same = [f for f in ("plan.json", "plan.md") if os.path.isfile(os.path.join(d, f))
            and open(os.path.join(d, f), "rb").read() == open(os.path.join(src, f), "rb").read()]
    return verdict(rc == 0 and len(same) == 2, "PASS-" + tag, "FAIL-" + tag,
                   ["lib/opal_lgctfm.py plan <copy> rc=%d; byte-equal to the committed files: %s of 2" % (rc, same)]
                   + quoted(out)[-6:])


# ============================================================================ the renderer (LT-r-1)
def render(contract_path, outdir, verb="render"):
    return run([sys.executable, ab(RENDER), verb, contract_path, "--out", outdir], timeout=180)


def _planted_to(d, doc):
    p = os.path.join(d, "contract.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    return p


def _files(d):
    return {f: open(os.path.join(d, f), "rb").read() for f in ("flow.current.md", "flow.desired.md")
            if os.path.isfile(os.path.join(d, f))}


def _r1_setup(tag):
    c, why = load_json(PLANTED)
    if c is None:
        return None, say("FAIL-" + tag, why)
    if not os.path.isfile(ab(RENDER)):
        return None, say("FAIL-" + tag, "absent: %s" % RENDER)
    return c, None


def r1_identical():
    tag = "R1-TWO-RENDERS-BYTE-IDENTICAL"
    c, done = _r1_setup(tag)
    if done is not None:
        return done
    outs = []
    for _ in range(2):
        d = tempfile.mkdtemp(prefix="lt_r1_render_")
        rc, _o = render(_planted_to(d, c), d)
        outs.append((rc, _files(d)))
    ok = all(rc == 0 and len(f) == 2 for rc, f in outs) and outs[0][1] == outs[1][1]
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["render rc: %s; files: %s; identical: %s"
                                                       % ([o[0] for o in outs], [sorted(o[1]) for o in outs], outs[0][1] == outs[1][1])])


def core_edit(before, after, old, new):
    cur_a = before.get("flow.current.md", b"").decode("utf-8", "replace").splitlines()
    cur_b = after.get("flow.current.md", b"").decode("utf-8", "replace").splitlines()
    changed = [ln for ln in difflib.unified_diff(cur_a, cur_b, lineterm="", n=0)
               if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    stray = [ln for ln in changed if old not in ln and new not in ln]
    desired_same = before.get("flow.desired.md") == after.get("flow.desired.md") and "flow.desired.md" in before
    ok = bool(changed) and not stray and any(new in ln for ln in changed) and desired_same
    return ok, ["current render: changed lines %d, lines not about the edited name %d" % (len(changed), len(stray)),
                "desired render unchanged by a current.name edit: %s" % desired_same] + ["  " + s[:100] for s in stray[:5]]


def r1_edit():
    tag = "R1-EDIT-CHANGES-ONLY-ITS-ROW"
    c, done = _r1_setup(tag)
    if done is not None:
        return done
    d1, d2 = tempfile.mkdtemp(prefix="lt_r1_a_"), tempfile.mkdtemp(prefix="lt_r1_b_")
    old = c["rows"][0]["current"]["name"]["value"]
    new = "zz-planted-edit"
    e = copy.deepcopy(c)
    e["rows"][0]["current"]["name"]["value"] = new
    rc1, _ = render(_planted_to(d1, c), d1)
    rc2, _ = render(_planted_to(d2, e), d2)
    ok, lines = core_edit(_files(d1), _files(d2), old, new)
    return verdict(ok and rc1 == 0 and rc2 == 0, "PASS-" + tag, "FAIL-" + tag, ["render rc %d / %d" % (rc1, rc2)] + lines)


def r1_hand_edit():
    tag = "R1-HAND-EDIT-FAILS-CHECK"
    c, done = _r1_setup(tag)
    if done is not None:
        return done
    d = tempfile.mkdtemp(prefix="lt_r1_hand_")
    p = _planted_to(d, c)
    rc, _ = render(p, d)
    with open(os.path.join(d, "flow.current.md"), "ab") as fh:
        fh.write(b"\n<!-- a hand edit -->\n")
    rc2, out = render(p, d, verb="check")
    return verdict(rc == 0 and rc2 != 0, "PASS-" + tag, "FAIL-" + tag,
                   ["render rc=%d; check after a hand edit rc=%d (must be non-zero)" % (rc, rc2)] + quoted(out)[-4:])


def r1_fresh():
    tag = "R1-FRESH-RENDER-PASSES-CHECK"
    c, done = _r1_setup(tag)
    if done is not None:
        return done
    d = tempfile.mkdtemp(prefix="lt_r1_fresh_")
    p = _planted_to(d, c)
    rc, _ = render(p, d)
    rc2, out = render(p, d, verb="check")
    return verdict(rc == 0 and rc2 == 0, "PASS-" + tag, "FAIL-" + tag,
                   ["render rc=%d; check on the untouched render rc=%d (must be 0)" % (rc, rc2)] + quoted(out)[-4:])


# ============================================================================ the run home + diff (LT-h-1)
def parse_diff(out):
    sec, got = None, {"CLOSED": [], "OPENED": [], "UNCHANGED": []}
    for ln in out.splitlines():
        m = re.match(r"^(CLOSED|OPENED|UNCHANGED):\s*(\d+)\s*$", ln)
        if m:
            sec = m.group(1)
            continue
        if sec and ln.startswith("  ") and ln.strip():
            got[sec].append(ln.strip())
    return got


def tkey(t):
    return "%s|%s|%s|%s" % (t.get("row_id"), t.get("axis"), t.get("kind"), ",".join(sorted(t.get("deciding_rules") or [])))


def core_diff(out, closed, opened, unchanged):
    got = parse_diff(out)
    want = {"CLOSED": sorted(closed), "OPENED": sorted(opened), "UNCHANGED": sorted(unchanged)}
    ok = all(sorted(got[k]) == want[k] for k in want)
    return ok, ["%-9s want %s got %s" % (k, want[k], sorted(got[k])) for k in want]


def _two_runs(root, prose_change):
    base = json.loads(read(PLANTED))
    t_closed = {"row_id": "R-9001", "axis": "A2", "kind": "HOME", "deciding_rules": ["R1"]}
    t_same = {"row_id": "R-9002", "axis": "A3", "kind": "GRAMMAR", "deciding_rules": ["R5", "R6"], "note": "before"}
    t_open = {"row_id": "R-9003", "axis": "PROCESS", "kind": "DECLARATION", "deciding_rules": ["R18"]}
    runs = []
    for i, ts in enumerate(([t_closed, t_same], [dict(t_same, note="after" if prose_change else "before"), t_open])):
        rid = "20260917T00000%dZ-planted%d" % (i, i)
        rc, out = run([sys.executable, ab(RUNHOME), "new", "--root", root, "--subject", "planted-subject",
                       "--run-id", rid, "--repo-head", "000000000%d" % i, "--graph-built", "2026-09-1%dT00:00:00Z" % i,
                       "--registry-hash", "hash%d" % i], timeout=120)
        d = os.path.join(root, "planted-subject", rid)
        doc = copy.deepcopy(base)
        doc["tensions"] = ts
        if os.path.isdir(d):
            _planted_to(d, doc)
        runs.append((rc, d, rid, out))
    return runs, tkey(t_closed), tkey(t_open), tkey(t_same)


def _h1_guard(tag):
    if not os.path.isfile(ab(RUNHOME)):
        return say("FAIL-" + tag, "absent: %s" % RUNHOME)
    if read(PLANTED) is None:
        return say("FAIL-" + tag, "absent: %s" % PLANTED)
    return None


def h1_headings():
    tag = "H1-DIFF-CLOSED-OPENED-UNCHANGED"
    g = _h1_guard(tag)
    if g is not None:
        return g
    root = tempfile.mkdtemp(prefix="lt_r1_home_")
    runs, kc, ko, ku = _two_runs(root, prose_change=False)
    rc, out = run([sys.executable, ab(RUNHOME), "diff", runs[0][1], runs[1][1]], timeout=120)
    ok, lines = core_diff(out, [kc], [ko], [ku])
    return verdict(ok and rc == 0, "PASS-" + tag, "FAIL-" + tag, ["new rc %s; diff rc %d" % ([r[0] for r in runs], rc)] + lines)


def h1_identity():
    tag = "H1-DIFF-KEYED-ON-IDENTITY"
    g = _h1_guard(tag)
    if g is not None:
        return g
    root = tempfile.mkdtemp(prefix="lt_r1_home_")
    runs, kc, ko, ku = _two_runs(root, prose_change=True)
    rc, out = run([sys.executable, ab(RUNHOME), "diff", runs[0][1], runs[1][1]], timeout=120)
    ok, lines = core_diff(out, [kc], [ko], [ku])
    return verdict(ok and rc == 0, "PASS-" + tag, "FAIL-" + tag,
                   ["a PROSE field of the unchanged tension differs between the runs; it must stay UNCHANGED"] + lines)


def h1_no_overwrite():
    tag = "H1-SECOND-RUN-NEVER-OVERWRITES"
    g = _h1_guard(tag)
    if g is not None:
        return g
    root = tempfile.mkdtemp(prefix="lt_r1_home_")
    argv = [sys.executable, ab(RUNHOME), "new", "--root", root, "--subject", "planted-subject", "--run-id",
            "20260917T000000Z-same", "--repo-head", "0000000000", "--graph-built", "2026-09-16T00:00:00Z",
            "--registry-hash", "h"]
    rc1, _ = run(argv, timeout=120)
    d = os.path.join(root, "planted-subject", "20260917T000000Z-same")
    snap = {f: open(os.path.join(d, f), "rb").read() for f in (os.listdir(d) if os.path.isdir(d) else [])}
    rc2, out = run(argv[:-1] + ["h-different"], timeout=120)
    after = {f: open(os.path.join(d, f), "rb").read() for f in (os.listdir(d) if os.path.isdir(d) else [])}
    ok = rc1 == 0 and bool(snap) and rc2 != 0 and snap == after
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["first new rc=%d files %s; second new (same run-id) rc=%d; first run's "
                                                       "bytes unchanged: %s" % (rc1, sorted(snap), rc2, snap == after)])


def core_manifest(text, triples):
    missing = [t for t in triples if not all(x in text for x in t)]
    return bool(triples) and not missing, ["runs %d; runs whose id + triple the manifest omits: %s" % (len(triples), missing)]


def h1_manifest():
    tag = "H1-MANIFEST-LISTS-EVERY-RUN"
    g = _h1_guard(tag)
    if g is not None:
        return g
    root = tempfile.mkdtemp(prefix="lt_r1_home_")
    runs, _a, _b, _c = _two_runs(root, prose_change=False)
    rc, out = run([sys.executable, ab(RUNHOME), "manifest", "--root", root, "--subject", "planted-subject"], timeout=120)
    mpath = os.path.join(root, "planted-subject", "MANIFEST.md")
    text = out + (open(mpath, encoding="utf-8").read() if os.path.isfile(mpath) else "")
    triples = [(runs[i][2], "000000000%d" % i, "2026-09-1%dT00:00:00Z" % i, "hash%d" % i) for i in range(2)]
    ok, lines = core_manifest(text, triples)
    return verdict(ok and rc == 0, "PASS-" + tag, "FAIL-" + tag, ["manifest rc=%d" % rc] + lines)


# ============================================================================ determinism (LT-d-1)
def d1_pytest():
    tag = "D1-DETERMINISM-SUITE-PASSES"
    if not os.path.isfile(ab(TESTS)):
        return say("FAIL-" + tag, "absent: %s" % TESTS)
    rc, out = run([sys.executable, "-m", "pytest", "-q", "--color=no", TESTS], timeout=280)
    m = re.search(r"(?m)^(\d+) passed", out)
    ok = rc == 0 and m is not None and not re.search(r"(?m)\b\d+ (failed|error)", out)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["pytest rc=%d" % rc] + quoted(out)[-5:])


def core_determinism(rec, copy_ok, engine_differs):
    n = rec.get("negative_arm") or {}
    p = rec.get("positive_arm") or {}
    order = str(n.get("recorded_utc") or "") < str(p.get("recorded_utc") or "~") and bool(n.get("recorded_utc"))
    ok = n.get("outputs_differ") is True and p.get("identical") is True and order and copy_ok and engine_differs
    return ok, ["negative arm: outputs_differ=%r at %r on copy %r (copy committed: %s, its bytes differ from the engine: %s)"
                % (n.get("outputs_differ"), n.get("recorded_utc"), n.get("copy_path"), copy_ok, engine_differs),
                "positive arm: identical=%r at %r; negative recorded FIRST: %s" % (p.get("identical"), p.get("recorded_utc"), order)]


def d1_negative_first():
    tag = "D1-NEGATIVE-ARM-FIRED-FIRST"
    rec, why = load_json(DETERMINISM)
    if rec is None:
        return say("FAIL-" + tag, why)
    cp = str((rec.get("negative_arm") or {}).get("copy_path") or "")
    in_folder = cp.startswith(W3 + "/")
    copy_ok = in_folder and os.path.isfile(ab(cp)) and git("ls-files", "--error-unmatch", cp)[0] == 0
    eng = ab(ENGINE)
    differs = copy_ok and os.path.isfile(eng) and open(ab(cp), "rb").read() != open(eng, "rb").read()
    ok, lines = core_determinism(rec, copy_ok, differs)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines + ["copy inside %s/: %s" % (W3, in_folder)])


# ============================================================================ the first real run + mark (LT-x-1)
RUN_FILES = ("contract.json", "flow.current.md", "flow.desired.md", "plan.json", "plan.md", "VINTAGE.json")


def subject_runs():
    d = ab(SUBJECT_DIR)
    if not os.path.isdir(d):
        return []
    return sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))


def graded_run():
    """The run directory LT-x-1's criteria grade, named by its OWN R-40 manifest and never by position.

    This used to be `subject_runs()[0]` -- the earliest run id under the subject -- and that is precisely the
    label-is-not-an-identity defect R-40 was issued against (LGIC_LGCTFM-S3): a later cell's commit dropped four
    regenerated artifacts into the earliest directory and `x1-run-dir` read PASS on bytes LT-x-1's run never
    produced, while a fresh coherent run would have sorted LAST and gone ungraded. Returns (run_id, abs_path,
    why) and REFUSES to guess: no manifest, or more than one, is a FAIL with its denominator, never a fallback to
    position -- a fallback would re-open the hole.
    """
    runs = subject_runs()
    carrying = [r for r in runs if os.path.isfile(os.path.join(ab(SUBJECT_DIR), r, "HASHES.json"))]
    note = "run directories under the subject: %d; carrying an R-40 HASHES.json: %d %s" % (len(runs), len(carrying), carrying)
    if len(carrying) != 1:
        return None, None, note + " -- exactly one run carries the manifest that names the graded run (R-40)"
    return carrying[0], os.path.join(ab(SUBJECT_DIR), carrying[0]), note


def x1_run_dir():
    tag = "X1-RUN-DIRECTORY-COMPLETE"
    rid, first, note = graded_run()
    if rid is None:
        return say("FAIL-" + tag, note)
    missing = [f for f in RUN_FILES if not os.path.isfile(os.path.join(first, f))]
    schema, why = load_json(SCHEMA)
    contract, why2 = load_json(os.path.join(first, "contract.json"))
    errs = ["schema or contract unreadable: %s" % (why or why2)]
    if schema is not None and contract is not None:
        v, why3 = validator_for(schema)
        errs = validate(v, contract) if v is not None else [why3]
    ok = not missing and not errs
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, [note, "graded run: %s" % rid,
                                                      "missing of the %d run files: %s" % (len(RUN_FILES), missing),
                                                      "schema errors on its contract: %d" % len(errs)] + errs[:5])


HASHED_FILES = RUN_FILES + ("MARK.json", "FWD10.json")


def core_hashes(run_id, manifest, actual):
    """R-40 (1.0.0_SA_CTO, 2026-09-18, msg 97741): a criterion whose subject is a RUN or a PRODUCED ARTIFACT is
    graded against that artifact's CONTENT HASH, not against the label that names it. `manifest` is the cell's own
    HASHES.json, written at production time; `actual` is {name: git hash-object} recomputed now. A later commit that
    replaces a file in the run home then FAILS this arm instead of silently satisfying the one that reads the
    directory. The declared set is compared to the required set in BOTH directions (Rule 24(i) by subtraction), so a
    manifest that simply omits the file it broke does not pass either.
    """
    declared = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(declared, dict):
        return False, ["HASHES.json carries no `files` map (R-40's manifest is the identity, not the path)"]
    bad = []
    if manifest.get("run_id") != run_id:
        bad.append("run_id declared %r, directory is %r -- the manifest describes another run"
                   % (manifest.get("run_id"), run_id))
    missing = [f for f in HASHED_FILES if f not in declared]
    undeclared = [k for k in sorted(declared) if k not in HASHED_FILES]
    mism = []
    for f in HASHED_FILES:
        if f in declared and actual.get(f) != declared[f]:
            mism.append("%s: declared %s, bytes now %s" % (f, str(declared[f])[:16], str(actual.get(f))[:16]))
    ok = not bad and not missing and not undeclared and not mism
    return ok, (["required %d file(s); declared %d; missing from the manifest: %s; declared but not required: %s"
                 % (len(HASHED_FILES), len(declared), missing, undeclared),
                 "hash mismatches: %d of %d" % (len(mism), len(HASHED_FILES))] + bad + mism[:6])


def x1_hashes():
    tag = "X1-RUN-ARTIFACTS-BOUND-TO-THEIR-HASHES"
    runs = subject_runs()
    carrying = [r for r in runs if os.path.isfile(os.path.join(ab(SUBJECT_DIR), r, "HASHES.json"))]
    lines = ["run directories under the subject: %d; carrying an R-40 HASHES.json: %d %s"
             % (len(runs), len(carrying), carrying)]
    if len(carrying) != 1:
        return say("FAIL-" + tag, *(lines + ["exactly one run directory carries the manifest, or this arm cannot "
                                             "name the run it grades -- which is the defect R-40 exists to stop"]))
    rid = carrying[0]
    d = os.path.join(ab(SUBJECT_DIR), rid)
    man, why = load_json(os.path.join(d, "HASHES.json"))
    if man is None:
        return say("FAIL-" + tag, *(lines + [why]))
    actual = {}
    for f in HASHED_FILES:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            rc, out = git("hash-object", p)
            actual[f] = out.strip() if rc == 0 and out.strip() else "git rc=%d" % rc
    ok, why2 = core_hashes(rid, man, actual)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines + why2)


def contains(doc, needle):
    if doc == needle:
        return True
    if isinstance(doc, dict):
        return any(contains(v, needle) for v in doc.values())
    if isinstance(doc, list):
        return any(contains(v, needle) for v in doc)
    return False


def core_marks(marks, files):
    entries = marks.get("marks") or []
    bad = []
    for e in entries:
        f = e.get("file")
        if f not in files or e.get("project") != "ADVI_FIRMBKTS" or "entry" not in e or not contains(files[f], e["entry"]):
            bad.append("%s -> %s" % (f, json.dumps(e.get("entry"))[:80]))
    return bool(entries) and not bad, ["MARK entries %d; registries read %d; entries absent from their file, off the three "
                                       "files, or not under ADVI_FIRMBKTS: %d" % (len(entries), len(files), len(bad))] + ["  " + b for b in bad[:8]]


def x1_marks():
    tag = "X1-MARK-ROWS-IN-THE-THREE-REGISTRIES"
    rid, d, note = graded_run()
    if rid is None:
        return say("FAIL-" + tag, note)
    m, why = load_json(os.path.join(d, "MARK.json"))
    if m is None:
        return say("FAIL-" + tag, note, why)
    files = {}
    for f in REGISTRIES:
        j, _w = load_json(f)
        if j is not None:
            files[f] = j
    ok, lines = core_marks(m, files)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_fwd10(rec):
    a = rec.get("aws") or {}
    s = rec.get("served") or {}
    b, af = a.get("before") or {}, a.get("after") or {}
    shape = all(isinstance(x.get("nodes_scanned"), int) and x.get("nodes_scanned") > 0 and str(x.get("built") or "")
                for x in (b, af))
    inst = "comp-find --corpus aws" in str(a.get("instrument") or "")
    zero = a.get("delta_outside_run") == [] and s.get("before", {}).get("routes_sha256") == s.get("after", {}).get("routes_sha256") \
        and bool(s.get("before", {}).get("routes_sha256"))
    return shape and inst and zero, ["aws before/after nodes_scanned + built present: %s; instrument named: %s" % (shape, inst),
                                     "aws delta outside the run: %r; served routes sha before==after: %s"
                                     % (a.get("delta_outside_run"), zero)]


def x1_fwd10():
    """The THIRD arm of this cell, and the one this seat MISSED when it added graded_run().

    It read `subject_runs()[0]` -- the earliest run id -- so on the re-hand it graded the FIRST hand's
    FWD10.json and not the hand's own. The worker running it said so in its report rather than letting
    a PASS stand on the wrong object, which is the only reason this is fixed. Same position-not-identity
    hole R-40 exists to close; repointed here so the arm grades the run the R-40 manifest names.
    """
    tag = "X1-LIVE-PLANE-ZERO-DELTA"
    rid, d, note = graded_run()
    if rid is None:
        return say("FAIL-" + tag, note)
    r, why = load_json(os.path.join(d, "FWD10.json"))
    if r is None:
        return say("FAIL-" + tag, note, why)
    ok, lines = core_fwd10(r)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, [note, "graded run: %s" % rid] + lines)


def core_footprint(paths, allowed_prefixes):
    stray = [p for p in paths if not any(p == a or p.startswith(a) for a in allowed_prefixes)]
    return bool(paths) and not stray, ["paths changed on this branch: %d; outside the run home, the three registries and "
                                       "this project's own tree: %d %s" % (len(paths), len(stray), stray[:8])]


def x1_footprint():
    tag = "X1-REPO-FOOTPRINT-BOUNDED"
    b = base_ref()
    if not b:
        return say("FAIL-" + tag, "git merge-base HEAD CLOUD did not resolve")
    rc, out = git("diff", "--name-only", b, "HEAD")
    paths = [p for p in out.splitlines() if p.strip()]
    allowed = ["workflows/legacy_transform/", ROOT + "/"] + list(REGISTRIES)
    ok, lines = core_footprint(paths, allowed)
    return verdict(ok and rc == 0, "PASS-" + tag, "FAIL-" + tag, ["base %s" % b[:10]] + lines)


def x1_r16():
    tag = "X1-MARK-COMMIT-PRINTS-TARGETS"
    b = base_ref()
    if not b:
        return say("FAIL-" + tag, "git merge-base HEAD CLOUD did not resolve")
    rc, out = git("log", "--format=%H%x1f%B%x1e", "%s..HEAD" % b, "--", *REGISTRIES)
    commits = [c for c in out.split("\x1e") if c.strip()]
    printed = [c for c in commits if re.search(r"(?m)^\s*TARGETS:\s*\d+", c)]
    ok = bool(commits) and len(printed) == len(commits)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["commits touching the three registries: %d; carrying a TARGETS: line "
                                                       "(lib/opal_naming.py targets, R-16): %d" % (len(commits), len(printed))])


# ============================================================================ the planted refusal (LT-x-2)
def core_refused(rc, out):
    return rc != 0 and "ADVI_FIRMBKTS" in out, ["naming-gate --enforce rc=%d; names ADVI_FIRMBKTS: %s" % (rc, "ADVI_FIRMBKTS" in out)]


def core_passes(rc, out):
    return rc == 0, ["naming-gate --enforce rc=%d (must be 0)" % rc]


def _gate_on(diff_name):
    p = ab(REFUSAL_DIR + "/" + diff_name)
    if not os.path.isfile(p):
        return None, "absent: %s/%s" % (REFUSAL_DIR, diff_name)
    return run([sys.executable, ab(GATE), "--diff", p, "--enforce"], timeout=240), ""


def x2_adding():
    tag = "X2-ADDED-USE-REFUSED"
    res, why = _gate_on("add.diff")
    if res is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_refused(*res)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines + quoted(res[1])[-8:])


def x2_removing():
    tag = "X2-REMOVED-USE-PASSES"
    res, why = _gate_on("remove.diff")
    if res is None:
        return say("FAIL-" + tag, why)
    ok, lines = core_passes(*res)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines + quoted(res[1])[-6:])


def x2_flag_untouched():
    tag = "X2-ESTATE-FLAG-UNTOUCHED"
    b = base_ref()
    if not b:
        return say("FAIL-" + tag, "git merge-base HEAD CLOUD did not resolve")
    rc1, log = git("log", "--oneline", "%s..HEAD" % b, "--", ENFORCE_FLAG)
    rc2, st = git("status", "--porcelain", "--", ENFORCE_FLAG)
    ok = rc1 == 0 and rc2 == 0 and not log.strip() and not st.strip()
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["commits on this branch touching %s: %r" % (ENFORCE_FLAG, log.strip()[:80]),
                                                       "uncommitted state of it: %r" % st.strip()[:80]])


# ============================================================================ the second run (LT-x-3)
def x3_two_runs():
    tag = "X3-TWO-RUNS-ON-ONE-SUBJECT"
    runs = subject_runs()
    good = [r for r in runs if all(os.path.isfile(os.path.join(ab(SUBJECT_DIR), r, f)) for f in ("contract.json", "VINTAGE.json"))]
    return verdict(len(good) >= 2, "PASS-" + tag, "FAIL-" + tag, ["run directories %d; with contract.json + VINTAGE.json: %d %s"
                                                                   % (len(runs), len(good), good[-3:])])


def _last_two():
    runs = [r for r in subject_runs() if os.path.isfile(os.path.join(ab(SUBJECT_DIR), r, "contract.json"))]
    if len(runs) < 2:
        return None
    return os.path.join(ab(SUBJECT_DIR), runs[-2]), os.path.join(ab(SUBJECT_DIR), runs[-1])


def x3_diff_reproduced():
    tag = "X3-COMMITTED-DIFF-REPRODUCES"
    pair = _last_two()
    if pair is None:
        return say("FAIL-" + tag, "fewer than two runs under %s" % SUBJECT_DIR)
    committed = read(os.path.join(pair[1], "DIFF.md"))
    if committed is None:
        return say("FAIL-" + tag, "absent: DIFF.md in the latest run")
    rc, out = run([sys.executable, ab(RUNHOME), "diff", pair[0], pair[1]], timeout=180)
    ok = rc == 0 and parse_diff(out) == parse_diff(committed) and any(parse_diff(out).values())
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["diff rc=%d; sections equal to the committed DIFF.md: %s"
                                                       % (rc, parse_diff(out) == parse_diff(committed))])


def x3_nontrivial():
    tag = "X3-WAVE-MOVED-SOMETHING"
    pair = _last_two()
    if pair is None:
        return say("FAIL-" + tag, "fewer than two runs under %s" % SUBJECT_DIR)
    got = parse_diff(read(os.path.join(pair[1], "DIFF.md")) or "")
    n = len(got["CLOSED"]) + len(got["OPENED"])
    return verdict(n >= 1, "PASS-" + tag, "FAIL-" + tag, ["CLOSED %d + OPENED %d = %d (a practice wave that moves nothing "
                                                           "exercises nothing)" % (len(got["CLOSED"]), len(got["OPENED"]), n)])


def core_filed(opened, before_ids, after_ids):
    new = sorted(set(after_ids) - set(before_ids))
    return len(new) >= opened, ["OPENED tensions %d; ADVI_FIRMBKTS channel rows added on this branch %d %s" % (opened, len(new), new[:6])]


def x3_opened_filed():
    tag = "X3-OPENED-ROWS-FILED"
    pair = _last_two()
    b = base_ref()
    if pair is None or not b:
        return say("FAIL-" + tag, "fewer than two runs, or merge-base unresolved")
    opened = len(parse_diff(read(os.path.join(pair[1], "DIFF.md")) or "")["OPENED"])
    rx = r'"id"\s*:\s*"(ADVI_FIRMBKTS-[^"]+)"'
    rc, before = git("show", "%s:%s" % (b, ADVI_CHANNEL))
    after = read(ADVI_CHANNEL) or ""
    ok, lines = core_filed(opened, re.findall(rx, before if rc == 0 else ""), re.findall(rx, after))
    return verdict(ok and bool(after), "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ the reviewer (LT-v-1)
def v1_reproduced():
    tag = "V1-SAMPLE-REPRODUCED-BY-CALL"
    rec, why = load_json(REPRO)
    if rec is None:
        return say("FAIL-" + tag, why)
    c, why2 = load_json(str(rec.get("contract") or ""))
    if c is None:
        return say("FAIL-" + tag, why2)
    mod, why3 = import_naming()
    if mod is None:
        return say("FAIL-" + tag, why3)
    builders = {k: getattr(mod, k) for k in BUILDER_FNS if hasattr(mod, k)}
    sample = set(r.get("row_id") for r in rec.get("results") or [])
    callable_rows = [r for r in c.get("rows") or [] if isinstance(cell_value((r.get("desired") or {}).get("builder")), dict)
                     and cell_value(r["desired"]["builder"]).get("fn") in BUILDER_FNS]
    need = min(20, len(callable_rows))
    sub = dict(c, rows=[r for r in callable_rows if r.get("row_id") in sample])
    ok, lines = core_reproduce(sub, builders)
    ok = ok and len(sub["rows"]) >= need and need > 0
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["callable rows in the contract %d; sample required %d; sampled %d"
                                                       % (len(callable_rows), need, len(sub["rows"]))] + lines)


def v1_order():
    tag = "V1-REVIEWER-ORDER-EQUALS-RULE"
    rec, why = load_json(REPRO)
    if rec is None:
        return say("FAIL-" + tag, why)
    c, why2 = load_json(str(rec.get("contract") or ""))
    if c is None:
        return say("FAIL-" + tag, why2)
    given = [t.get("tension_id") for t in c.get("tensions") or []]
    want = [t.get("tension_id") for t in sorted(c.get("tensions") or [], key=rank_key)]
    rev = list(rec.get("order") or [])
    ok = bool(given) and rev == want == given
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["tensions %d; reviewer order == rule order: %s; contract order == rule "
                                                       "order: %s" % (len(given), rev == want, given == want)])


def core_not_author(authors):
    return bool(authors) and "0.9.0_WK_LGIC_LGCTFM~3" not in authors, ["authors of %s: %s" % (ENGINE, sorted(authors))]


def v1_not_author():
    tag = "V1-REVIEWER-IS-NOT-ENGINE-AUTHOR"
    rc, out = git("log", "--format=%an", "--", ENGINE)
    ok, lines = core_not_author(set(x.strip() for x in out.splitlines() if x.strip()))
    return verdict(ok and rc == 0, "PASS-" + tag, "FAIL-" + tag, lines)


def v1_card():
    tag = "V1-ANDREW-CARD-CARRIES-RULE"
    t = read(CARD)
    rec, why = load_json(REPRO)
    if t is None or rec is None:
        return say("FAIL-" + tag, "absent: %s" % (CARD if t is None else why))
    c, why2 = load_json(str(rec.get("contract") or ""))
    if c is None:
        return say("FAIL-" + tag, why2)
    rule = str(c.get("ranking_rule") or "")
    ids = [x.get("tension_id") for x in c.get("tensions") or []][:10]
    shown = [i for i in ids if i and i in t]
    ok = bool(rule) and rule in t and len(shown) == len(ids) and bool(ids)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["card carries the contract's ranking_rule verbatim: %s" % (bool(rule) and rule in t),
                                                       "top tensions shown: %d of %d" % (len(shown), len(ids))])


# ============================================================================ dispatch
# ==================================================== the round-1 AMENDMENT (LT-e-4, RULING R-36)
#
# R-36 answered LGIC_LGCTFM-W2-S2. The contract enum stays EQUAL to NAMING_SCHEMA.json's 33 graded types by
# subtraction -- that equality is what lets the contract say a type is ungraded at all (Rule 24(i)) -- so the
# untypeable PLANT becomes OPT-IN behind --plant-untypeable, and a node whose type the naming schema does not
# grade is neither written into contract.rows nor discarded: it is CARRIED in the run's own
# PLANT_UNTYPEABLE.json with verdict NOT_COVERED, and its COUNT is printed in the contract as a required cell.
# A printed zero is a measurement; an absent one is silence.
AMEND_RUNS = W2 + "/AMENDMENT_RUNS.json"
CARRIER_FILE = "PLANT_UNTYPEABLE.json"
# CELL_STATUSES is defined ONCE at the top of this file as a SET; a second, tuple-shaped
# definition here silently broke core_enums, which compares set(enum) == CELL_STATUSES.


def _naming_graded_types():
    """The node types NAMING_SCHEMA.json grades, read from the schema itself, never a literal list."""
    n, _why = load_json(NAMING)
    if n is None:
        return set()
    return set(((n.get("kind") or {}).get("by_type") or {}).keys()) | \
        set((n.get("types_not_graded_by_kind") or {}).keys())


def _carrier(plant):
    """(entries, count) from EITHER carrier shape, so the historical artifact still grades.

    OLD, round 1's first walk: {"name": "..."} -- one planted name whose ROW sat in contract.rows.
    NEW, R-36: {"untypeable": [{name, node_type, verdict, ...}], "count": n} -- the row is carried HERE and is
    absent from contract.rows. An entry carrying _shape=old is the first form, normalised.
    """
    if not isinstance(plant, dict):
        return None, None
    if isinstance(plant.get("untypeable"), list):
        return plant["untypeable"], plant.get("count")
    if plant.get("name"):
        return [{"name": plant.get("name"), "verdict": "NOT_COVERED", "_shape": "old"}], None
    return [], plant.get("count")


def _amend_run(which):
    d, why = load_json(AMEND_RUNS)
    if d is None:
        return None, "%s is unreadable: %s" % (AMEND_RUNS, why)
    p = (d or {}).get(which)
    if not p:
        return None, "%s names no %r run (keys: %s)" % (AMEND_RUNS, which, sorted((d or {}).keys()))
    return p, ""


def _run_pair(which):
    """(contract, carrier, lines_or_why) for one of the amendment's two named runs."""
    rel, why = _amend_run(which)
    if rel is None:
        return None, None, why
    c, why1 = load_json(os.path.join(rel, "contract.json"))
    p, why2 = load_json(os.path.join(rel, CARRIER_FILE))
    if c is None or p is None:
        return None, None, "%s: %s" % (rel, why1 or why2)
    return c, p, rel


def core_plant_off(contract, carrier, graded):
    """Default OFF: no row carries an ungraded node_type, the carrier is EMPTY, and the count PRINTS 0."""
    rows = contract.get("rows") or []
    off = [r.get("row_id") for r in rows if r.get("node_type") and r.get("node_type") not in graded]
    entries, count = _carrier(carrier)
    cnt = cell_value(contract.get("untypeable"))
    lines = ["rows %d; carrying a node_type NAMING_SCHEMA.json does not grade: %d %s"
             % (len(rows), len(off), off[:5]),
             "carrier entries %s; contract untypeable count printed as %r (0 required with the plant off)"
             % (len(entries) if entries is not None else "unreadable", cnt)]
    ok = entries is not None and not off and len(entries) == 0 and cnt == 0
    if count is not None and count != 0:
        ok = False
        lines.append("  DEFECT the carrier's own count reads %r beside an empty entry list" % count)
    return ok, lines


def core_flag_on(contract, carrier):
    """Flag ON: the untypeable node is CARRIED with NOT_COVERED, COUNTED, and absent from rows."""
    entries, count = _carrier(carrier)
    if entries is None:
        return False, ["the carrier is not an object"]
    names = [e.get("name") for e in entries]
    by_name = rows_by_name(contract)
    in_rows = [n for n in names if by_name.get(n)]
    nc = [e for e in entries if e.get("verdict") == "NOT_COVERED"]
    cnt = cell_value(contract.get("untypeable"))
    lines = ["carrier entries %d; NOT_COVERED %d; carried names found in contract.rows: %d %s"
             % (len(entries), len(nc), len(in_rows), in_rows[:3]),
             "contract untypeable count %r; carrier count %r (both must equal the entry count)" % (cnt, count)],
    lines = lines[0]
    ok = bool(entries) and len(nc) == len(entries) and not in_rows and cnt == len(entries) and \
        (count is None or count == len(entries))
    return ok, lines


def core_count_typed(contract):
    """The count is a CELL a consumer can reject on, never a bare integer (A VALUE MUST CARRY ITS CLAIM)."""
    u = contract.get("untypeable")
    if u is None:
        return False, ["the contract carries no untypeable count at all -- an absent zero is silence, not a measurement"]
    if not isinstance(u, dict):
        return False, ["untypeable is %s, not a cell: a bare value carries no claim" % type(u).__name__]
    val, status = u.get("value"), u.get("status")
    ev = u.get("evidence") if isinstance(u.get("evidence"), dict) else {}
    missing = [f for f in ("instrument", "blind_spot") if not str(ev.get(f) or "").strip()]
    lines = ["untypeable cell: value=%r (int required), status=%r (one of %s), evidence missing %s"
             % (val, status, "/".join(sorted(CELL_STATUSES)), missing or "nothing")]
    ok = isinstance(val, int) and not isinstance(val, bool) and status in CELL_STATUSES and not missing
    return ok, lines


def core_schema_valid_docs(validator, docs):
    """Every named contract validates against the REAL schema -- X1R1-AC1's own question, on real runs."""
    lines, bad = [], 0
    for label, doc in docs:
        errs = validate(validator, doc)
        bad += bool(errs)
        lines.append("  %-12s %d validation error(s)%s" % (label, len(errs), (" -- " + errs[0][:90]) if errs else ""))
    return (bad == 0 and bool(docs)), ["DENOMINATOR: %d run contract(s) validated; %d with errors" % (len(docs), bad)] + lines


def a4_plant_off():
    tag = "A4-PLANT-OFF-BY-DEFAULT"
    c, p, rel = _run_pair("default_off")
    if c is None:
        return say("FAIL-" + tag, rel)
    ok, lines = core_plant_off(c, p, _naming_graded_types())
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["run: %s" % rel] + lines)


def a4_flag_on():
    tag = "A4-FLAG-ON-CARRIES-AND-COUNTS"
    c, p, rel = _run_pair("flag_on")
    if c is None:
        return say("FAIL-" + tag, rel)
    ok, lines = core_flag_on(c, p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["run: %s" % rel] + lines)


def a4_count_typed():
    tag = "A4-COUNT-IS-A-TYPED-CELL"
    c, _p, rel = _run_pair("default_off")
    if c is None:
        return say("FAIL-" + tag, rel)
    ok, lines = core_count_typed(c)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["run: %s" % rel] + lines)


def a4_schema_valid():
    tag = "A4-BOTH-RUNS-SCHEMA-VALID"
    schema, why = load_json(SCHEMA)
    if schema is None:
        return say("FAIL-" + tag, why)
    v, why2 = validator_for(schema)
    if v is None:
        return say("FAIL-" + tag, why2)
    docs = []
    for which in ("default_off", "flag_on"):
        c, _p, rel = _run_pair(which)
        if c is None:
            return say("FAIL-" + tag, rel)
        docs.append((which, c))
    ok, lines = core_schema_valid_docs(v, docs)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def a4_e3_exercised():
    """R-36: LT-e-3's untypeable path stays exercised DELIBERATELY -- graded on the flag-on run's carrier."""
    tag = "A4-E3-PATH-STILL-EXERCISED"
    c, p, rel = _run_pair("flag_on")
    if c is None:
        return say("FAIL-" + tag, rel)
    ok, lines = core_untypeable(c, p)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, ["run: %s" % rel] + lines)


def _selftest_a4():
    """Every amendment arm driven ALONE: one fixture that must PASS, one doctored input that must FAIL."""
    out = []
    graded = {"S3_BUCKET", "SQS_QUEUE"}

    def cellv(n):
        return {"value": n, "status": "MEASURED",
                "evidence": {"instrument": "the walk's type read against NAMING_SCHEMA.json", "blind_spot": "none"}}

    off_contract = {"rows": [{"row_id": "R-0001", "node_type": "S3_BUCKET"}], "tensions": [], "untypeable": cellv(0)}
    off_carrier = {"untypeable": [], "count": 0}
    on_row = {"name": "opal-x-legacy-user-pool", "node_type": "COGNITO_USER_POOL", "verdict": "NOT_COVERED"}
    on_contract = {"rows": [{"row_id": "R-0001", "node_type": "S3_BUCKET"}], "tensions": [], "untypeable": cellv(1)}
    on_carrier = {"untypeable": [on_row], "count": 1}

    # plant-off: GREEN clean; RED an ungraded row still in rows; RED a non-zero printed count
    out.append(("a4-plant-off GREEN (no ungraded row, empty carrier, printed 0)",
                core_plant_off(off_contract, off_carrier, graded)[0]))
    leaked = {"rows": off_contract["rows"] + [{"row_id": "R-0002", "node_type": "COGNITO_USER_POOL"}],
              "tensions": [], "untypeable": cellv(0)}
    out.append(("a4-plant-off RED   (an ungraded row reached contract.rows)",
                core_plant_off(leaked, off_carrier, graded)[0] is False))
    out.append(("a4-plant-off RED   (carrier empty but count prints 1)",
                core_plant_off({"rows": off_contract["rows"], "tensions": [], "untypeable": cellv(1)},
                               off_carrier, graded)[0] is False))

    # flag-on: GREEN carried+counted+absent from rows; RED each half alone
    out.append(("a4-flag-on GREEN (carried, NOT_COVERED, counted, absent from rows)",
                core_flag_on(on_contract, on_carrier)[0]))
    out.append(("a4-flag-on RED   (carried name ALSO written into rows)",
                core_flag_on({"rows": on_contract["rows"] + [{"row_id": "R-0009", "current": {"name": {"value": on_row["name"]}},
                              "node_type": "COGNITO_USER_POOL"}], "tensions": [], "untypeable": cellv(1)},
                             on_carrier)[0] is False))
    out.append(("a4-flag-on RED   (verdict is not NOT_COVERED)",
                core_flag_on(on_contract, {"untypeable": [dict(on_row, verdict="RAISE")], "count": 1})[0] is False))
    out.append(("a4-flag-on RED   (count disagrees with the entry list)",
                core_flag_on(on_contract, {"untypeable": [on_row], "count": 4})[0] is False))

    # count-typed: GREEN a cell; RED a bare int, a missing key, a missing blind_spot
    out.append(("a4-count-typed GREEN (value/status/evidence)", core_count_typed(off_contract)[0]))
    out.append(("a4-count-typed RED   (bare integer, no claim)",
                core_count_typed({"untypeable": 0})[0] is False))
    out.append(("a4-count-typed RED   (absent key reads as silence)",
                core_count_typed({"rows": []})[0] is False))
    bad_ev = {"value": 0, "status": "MEASURED", "evidence": {"instrument": "x"}}
    out.append(("a4-count-typed RED   (evidence without a blind spot)",
                core_count_typed({"untypeable": bad_ev})[0] is False))
    out.append(("a4-count-typed RED   (status off the enum)",
                core_count_typed({"untypeable": dict(cellv(0), status="PROBABLY")})[0] is False))

    # schema-valid: GREEN both docs clean against a permissive validator; RED one doc failing
    v_ok, _w = validator_for({"type": "object"})
    v_strict, _w2 = validator_for({"type": "object", "required": ["untypeable"]})
    if v_ok is not None and v_strict is not None:
        out.append(("a4-schema-valid GREEN (both runs validate)",
                    core_schema_valid_docs(v_ok, [("default_off", off_contract), ("flag_on", on_contract)])[0]))
        out.append(("a4-schema-valid RED   (one run missing the required count)",
                    core_schema_valid_docs(v_strict, [("default_off", off_contract), ("flag_on", {"rows": []})])[0] is False))
        out.append(("a4-schema-valid RED   (no run named at all)",
                    core_schema_valid_docs(v_ok, [])[0] is False))

    # e3 still exercised, on the NEW carrier shape, and the OLD shape still grades
    out.append(("a4-e3 GREEN (new carrier shape grades)", core_untypeable(on_contract, on_carrier)[0]))
    out.append(("a4-e3 RED   (carrier empty -- nothing was exercised)",
                core_untypeable(on_contract, {"untypeable": [], "count": 0})[0] is False))
    old_contract = {"rows": [{"row_id": "R-0185", "current": {"name": {"value": on_row["name"]}},
                              "desired": {"verdict": {"value": "NOT_COVERED"}}}], "tensions": []}
    out.append(("a4-e3 GREEN (OLD carrier shape still grades)",
                core_untypeable(old_contract, {"name": on_row["name"]})[0]))
    out.append(("a4-e3 RED   (OLD shape, row graded by a tension)",
                core_untypeable({"rows": old_contract["rows"],
                                 "tensions": [{"tension_id": "T-1", "row_id": "R-0185"}]},
                                {"name": on_row["name"]})[0] is False))
    return out


SUBCOMMANDS = {
    "s1-valid": s1_valid, "s1-bare-value": s1_bare_value, "s1-one-api": s1_one_api,
    "s1-no-instrument": s1_no_instrument, "s1-node-types": s1_node_types, "s1-enums": s1_enums,
    "s2-accept-valid": s2_accept_valid, "s2-refuse-bare": s2_refuse_bare, "s2-refuse-one-api": s2_refuse_one_api,
    "s2-refuse-no-instrument": s2_refuse_no_instrument, "s2-refuse-no-vintage": s2_refuse_no_vintage,
    "s2-unchecked": s2_unchecked_regress, "s2-selftest": s2_selftest,
    "e1-control": e1_control, "e1-triggers": e1_triggers, "e1-cells": e1_cells, "e1-plant": e1_unmeasured_plant,
    "e1-method": e1_method, "e1-skill": e1_skill, "e1-stdlib": e1_stdlib, "e1-ascii": e1_ascii,
    "e2-reproduce": e2_reproduce, "e2-forks": e2_forks, "e2-negative": e2_negative, "e2-raise": e2_raise,
    "e3-rule": e3_rule, "e3-factors": e3_factors, "e3-order": e3_order, "e3-types": e3_types,
    "e3-untypeable": e3_untypeable,
    "p1-fields": p1_fields, "p1-r19": p1_r19, "p1-served": p1_served, "p1-not-executed": p1_not_executed,
    "p1-regenerates": p1_regenerates,
    "r1-identical": r1_identical, "r1-edit": r1_edit, "r1-hand-edit": r1_hand_edit, "r1-fresh": r1_fresh,
    "h1-headings": h1_headings, "h1-identity": h1_identity, "h1-no-overwrite": h1_no_overwrite, "h1-manifest": h1_manifest,
    "d1-pytest": d1_pytest, "d1-negative-first": d1_negative_first,
    "x1-run-dir": x1_run_dir, "x1-marks": x1_marks, "x1-fwd10": x1_fwd10, "x1-footprint": x1_footprint, "x1-r16": x1_r16,
    "x1-hashes": x1_hashes,
    "x2-adding": x2_adding, "x2-removing": x2_removing, "x2-flag": x2_flag_untouched,
    "x3-two-runs": x3_two_runs, "x3-diff": x3_diff_reproduced, "x3-nontrivial": x3_nontrivial, "x3-filed": x3_opened_filed,
    "v1-reproduced": v1_reproduced, "v1-order": v1_order, "v1-not-author": v1_not_author, "v1-card": v1_card,
    "a4-plant-off": a4_plant_off, "a4-flag-on": a4_flag_on, "a4-count-typed": a4_count_typed,
    "a4-schema-valid": a4_schema_valid, "a4-e3-exercised": a4_e3_exercised,
}


# ============================================================================ self-test (A-23)
def _mini_schema():
    """An ISSUER fixture schema, only for driving the schema cores: it accepts the planted contract and refuses
    the four doctored ones. It is not LT-s-1's schema and grades nothing."""
    cell = {"type": "object", "required": ["value", "status", "evidence"],
            "properties": {"status": {"enum": sorted(CELL_STATUSES)},
                           "evidence": {"type": "object", "required": ["instrument", "blind_spot"]}}}
    half = {"type": "object", "additionalProperties": {"$ref": "#/$defs/cell"}}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$defs": {"cell": cell, "node_type": {"enum": ["A", "B"]}, "row_kind": {"enum": sorted(ROW_KINDS)},
                      "cell_status": {"enum": sorted(CELL_STATUSES)}, "axis": {"enum": sorted(AXES)},
                      "tension_kind": {"enum": sorted(TENSION_KINDS)}},
            "type": "object", "required": ["subject", "trigger_denominator", "rows"],
            "properties": {
                "subject": {"type": "object", "required": ["vintage"],
                            "properties": {"vintage": {"type": "object", "required": ["repo_head", "graph_built", "registry_hash"]}}},
                "trigger_denominator": {"type": "object", "required": ["list_rules", "list_schedules"]},
                "rows": {"type": "array", "items": {"type": "object", "properties": {"current": half, "desired": half}}}}}


def selftest_arms():
    res = []

    def arm(name, green, red, detail=""):
        res.append((name, bool(green) and not bool(red), detail))

    for _n, _g in _selftest_a4():
        res.append((_n, bool(_g), ""))
    planted = json.loads(read(PLANTED) or "{}")
    if not planted:
        return say("FAIL-ARMS-DISCRIMINATE", "absent: %s -- the self-test has no fixture" % PLANTED)
    v, why = validator_for(_mini_schema())
    if v is None:
        res.append(("schema-validator-available", False, why))
    else:
        arm("s1-valid", core_schema_accepts(v, planted)[0], core_schema_accepts(v, doctor(planted, "bare"))[0])
        for which in ("bare", "one_api", "no_instrument"):
            bad_schema, _ = validator_for({"type": "object"})
            arm("s1-refuse-" + which, core_schema_refuses(v, planted, which)[0],
                core_schema_refuses(bad_schema, planted, which)[0], "a permissive schema must FAIL the arm")
    naming = {"kind": {"by_type": {"A": 1}}, "types_not_graded_by_kind": {"B": 1}}
    arm("s1-node-types", core_node_types(_mini_schema(), naming)[0],
        core_node_types({"$defs": {"node_type": {"enum": ["A"]}}}, naming)[0], "one type short")
    doct = copy.deepcopy(_mini_schema())
    doct["$defs"]["tension_kind"]["enum"] = sorted(TENSION_KINDS | {"FORK"})
    arm("s1-enums", core_enums(_mini_schema())[0], core_enums(doct)[0], "FORK as a tension kind")

    good_out = "  HAND BACK  lgctfm-contract x\n  bare-value\nVERDICT: 0 ACCEPT | 1 HAND BACK | 0 UNCHECKED\n"
    arm("s2-handback-token", core_recv(good_out, "HAND BACK", "bare-value")[0],
        core_recv(good_out.replace("bare-value", "defect"), "HAND BACK", "bare-value")[0], "token absent")
    arm("s2-accept", core_recv("ACCEPT lgctfm-contract\nVERDICT: 1 ACCEPT | 0 HAND BACK | 0 UNCHECKED", "ACCEPT")[0],
        core_recv("UNCHECKED unrecognised\nVERDICT: 0 ACCEPT | 0 HAND BACK | 1 UNCHECKED", "ACCEPT")[0], "UNCHECKED is not ACCEPT")

    sc = {"trigger_plane": {"named_pattern_rules_sample": ["opal-{x,y}-guard (note)", "plain-rule"]}}
    mem = control_members(sc)
    arm("e1-control-expansion", ("opal-x-guard", "EVENT_RULE") in mem and ("plain-rule", "EVENT_RULE") in mem,
        ("opal-{x,y}-guard (note)", "EVENT_RULE") in mem, "braces expanded, notes dropped")
    rows = [{"node_type": nt, "current": {"name": {"value": n, "status": "MEASURED", "evidence": {}}}} for n, nt in mem]
    arm("e1-control", core_control({"rows": rows}, mem)[0], core_control({"rows": rows[:-1]}, mem)[0], "one member dropped")
    arm("e1-triggers", core_triggers(planted)[0], core_triggers(doctor(planted, "one_api"))[0], "one API")
    z = copy.deepcopy(planted)
    z["trigger_denominator"]["list_schedules"]["value"] = 0
    arm("e1-triggers-zero", core_triggers(planted)[0], core_triggers(z)[0], "a zero schedule count")
    arm("e1-cells", core_cells(planted)[0], core_cells(doctor(planted, "bare"))[0], "a bare value")
    arm("e1-cells-instrument", core_cells(planted)[0], core_cells(doctor(planted, "no_instrument"))[0], "no instrument")
    pl = copy.deepcopy(planted)
    pl["rows"][1]["current"]["live"]["status"] = "UNMEASURED"
    arm("e1-plant", core_plant(pl, {"name": "cot-bronze-complete"})[0], core_plant(planted, {"name": "cot-bronze-complete"})[0],
        "the plant with no UNMEASURED cell")
    heads = "\n".join("## " + t for t in METHOD_TERMS)
    arm("e1-method", core_method(heads)[0], core_method(heads.replace("## fork test", "fork test"))[0], "a term in prose only")
    sk = "---\nname: lgctfm\n---\nrun python %s\n" % ENGINE
    arm("e1-skill", core_skill(sk)[0], core_skill(sk.replace("lgctfm\n---", "other\n---"))[0], "wrong name")
    arm("e1-stdlib", core_stdlib("import json\nimport opal_naming\n", {"opal_naming"})[0],
        core_stdlib("import json\nimport yaml\n", {"opal_naming"})[0], "yaml")
    arm("e1-ascii", core_ascii(b"abc")[0], core_ascii(b"ab" + bytes([0xC3, 0xA9]))[0], "one non-ASCII byte")

    builders = {"name": lambda s, *a: s + "-x", "address": lambda *a: "/".join(a)}

    def bad_name(*a):
        raise ValueError("no row")
    builders_raise = dict(builders, name=bad_name)
    rc = {"rows": [{"row_id": "a", "desired": {"builder": {"value": {"fn": "name", "args": ["sys"]}},
                                               "form": {"value": "sys-x"}, "verdict": {"value": "CONFORMANT"}}}]}
    arm("e2-reproduce", core_reproduce(rc, builders)[0], core_reproduce(rc, builders_raise)[0], "a builder that raises")
    rc2 = copy.deepcopy(rc)
    rc2["rows"][0]["desired"]["form"]["value"] = "typed-by-hand"
    arm("e2-reproduce-typed", core_reproduce(rc, builders)[0], core_reproduce(rc2, builders)[0], "a typed desired form")
    arm("e2-reproduce-vacuous", core_reproduce(rc, builders)[0], core_reproduce({"rows": []}, builders)[0], "no callable row")
    # LT-e-3's NOT_COVERED branch (row LGIC_LGCTFM-W1-S1). GREEN: the coverage raise with NO form.
    # RED, each alone: the same verdict with a form typed in anyway, and the same verdict on a raise
    # that is NOT the coverage error (a registry defect must keep going through the RAISE branch).
    def uncovered(*a, **k):
        raise ValueError("G1.1: 'COGNITO_USER_POOL' is not a node type of NAMING_SCHEMA.json")
    builders_uncovered = dict(builders, name=uncovered)
    rc_nc = {"rows": [{"row_id": "nc", "desired": {"builder": {"value": {"fn": "name", "args": ["sys"]}},
                                                   "form": {"value": None},
                                                   "verdict": {"value": "NOT_COVERED"}}}]}
    rc_nc_formed = copy.deepcopy(rc_nc)
    rc_nc_formed["rows"][0]["desired"]["form"]["value"] = "opal-typed-anyway"
    arm("e2-not-covered", core_reproduce(rc_nc, builders_uncovered)[0],
        core_reproduce(rc_nc_formed, builders_uncovered)[0], "NOT_COVERED carrying a form must FAIL")
    arm("e2-not-covered-wrong-raise", core_reproduce(rc_nc, builders_uncovered)[0],
        core_reproduce(rc_nc, builders_raise)[0], "NOT_COVERED on a non-coverage raise must FAIL")

    def prow(rid, path):
        return {"row_id": rid, "kind": "RESOURCE", "current": {"arn_or_path": {"value": path}}}
    fc = {"positives": [{"id": "F", "members": ["a/x/{p,q}_legacy/", "a/x/{p,q}/"]}],
          "negative": [{"id": "N", "members": ["s/platform/", "s/account/{uuid}/"]}]}
    fk = {"rows": [prow("1", "b/a/x/p_legacy/"), prow("2", "b/a/x/p/"), prow("3", "s/platform/"), prow("4", "s/account/9/"),
                   {"row_id": "F1", "kind": "FORK", "members": ["1", "2"], "canonical_member": {"value": "2"}}]}
    unmarked = copy.deepcopy(fk)
    unmarked["rows"][-1]["canonical_member"]["value"] = ""
    arm("e2-forks", core_forks(fk, fc)[0], core_forks(unmarked, fc)[0], "canonical member not marked")
    nolegacy = copy.deepcopy(fk)
    nolegacy["rows"][0]["current"]["arn_or_path"]["value"] = "b/a/x/q/"
    arm("e2-forks-legacy", core_forks(fk, fc)[0], core_forks(nolegacy, fc)[0], "the _legacy member missing")
    joined = copy.deepcopy(fk)
    joined["rows"].append({"row_id": "F2", "kind": "FORK", "members": ["3", "4"], "canonical_member": {"value": "3"}})
    arm("e2-negative", core_negative(fk, fc)[0], core_negative(joined, fc)[0], "SmartX joined as a fork")
    vac = {"rows": [r for r in fk["rows"] if r["row_id"] not in ("3", "4")]}
    arm("e2-negative-vacuous", core_negative(fk, fc)[0], core_negative(vac, fc)[0], "no SmartX rows at all")
    arm("e2-raise", core_raise([planted])[0], core_raise([{"rows": planted["rows"][:1]}])[0], "no RAISE row")
    oop = copy.deepcopy(planted)
    oop["rows"][1]["desired"]["verdict"]["value"] = "OUT-OF-PATTERN"
    arm("e2-raise-guessed", core_raise([planted])[0], core_raise([oop])[0], "a refusal graded OUT-OF-PATTERN")

    arm("e3-rule", core_rule_printed(planted)[0], core_rule_printed(dict(planted, ranking_rule="order by live, then irreversible"))[0],
        "wrong order")
    nf = copy.deepcopy(planted)
    nf["tensions"][0]["factors"]["live"]["evidence"]["instrument"] = "a calendar day"
    arm("e3-factors", core_factors(planted)[0], core_factors(nf)[0], "live not read against trading_calendar")
    sw = copy.deepcopy(planted)
    sw["tensions"].reverse()
    arm("e3-order", core_order(planted)[0], core_order(sw)[0], "order reversed")
    tt = copy.deepcopy(planted)
    tt["tensions"][0]["kind"] = "FORK"
    arm("e3-types", core_types(planted)[0], core_types(tt)[0], "FORK as a tension kind")
    un = copy.deepcopy(planted)
    un["rows"][1]["desired"]["verdict"]["value"] = "NOT_COVERED"
    un["tensions"] = un["tensions"][:1]
    arm("e3-untypeable", core_untypeable(un, {"name": "cot-bronze-complete"})[0],
        core_untypeable(dict(un, tensions=planted["tensions"]), {"name": "cot-bronze-complete"})[0], "the plant graded anyway")

    pkg = {p: "x" for p in PACKAGE_FIELDS}
    plan = {"executed": False, "packages": [dict(pkg, package_id="P1", step="MAP", status="PLANNED", writes=["R-0001"],
                                                 never_widen_signoff_owed=True, signoff_owners=sorted(SIGNOFF_OWNERS)),
                                            dict(pkg, package_id="P2", step="PORT", status="PLANNED", writes=["R-0002"])]}
    miss = copy.deepcopy(plan)
    miss["packages"][1].pop("rollback")
    arm("p1-fields", core_pkg_fields(plan)[0], core_pkg_fields(miss)[0], "rollback missing")
    rev = copy.deepcopy(plan)
    rev["packages"].reverse()
    arm("p1-r19", core_r19(plan)[0], core_r19(rev)[0], "PORT before MAP")
    ns = copy.deepcopy(plan)
    ns["packages"][0]["never_widen_signoff_owed"] = False
    arm("p1-served", core_served(plan, planted)[0], core_served(ns, planted)[0], "a served key without the flag")
    ex = copy.deepcopy(plan)
    ex["packages"][0]["status"] = "DONE"
    arm("p1-not-executed", core_not_executed(plan)[0], core_not_executed(ex)[0], "a package DONE")

    a = {"flow.current.md": b"[opal-data-bd] --> x\nlegend\n", "flow.desired.md": b"d\n"}
    b = {"flow.current.md": b"[zz-planted-edit] --> x\nlegend\n", "flow.desired.md": b"d\n"}
    b2 = {"flow.current.md": b"[zz-planted-edit] --> x\nlegend moved\n", "flow.desired.md": b"d\n"}
    arm("r1-edit", core_edit(a, b, "opal-data-bd", "zz-planted-edit")[0], core_edit(a, b2, "opal-data-bd", "zz-planted-edit")[0],
        "a stray line changed")

    out = "CLOSED: 1\n  k1\nOPENED: 1\n  k3\nUNCHANGED: 1\n  k2\n"
    arm("h1-diff", core_diff(out, ["k1"], ["k3"], ["k2"])[0],
        core_diff(out.replace("CLOSED: 1\n  k1\n", "CLOSED: 0\n").replace("UNCHANGED: 1\n  k2", "UNCHANGED: 2\n  k1\n  k2"),
                  ["k1"], ["k3"], ["k2"])[0], "closed listed as unchanged")
    arm("h1-manifest", core_manifest("run1 h1 b1 r1", [("run1", "h1", "b1", "r1")])[0],
        core_manifest("run1 h1 b1", [("run1", "h1", "b1", "r1")])[0], "registry hash omitted")

    rec = {"negative_arm": {"outputs_differ": True, "recorded_utc": "2026-09-17T01:00:00Z", "copy_path": "c"},
           "positive_arm": {"identical": True, "recorded_utc": "2026-09-17T02:00:00Z"}}
    late = copy.deepcopy(rec)
    late["negative_arm"]["recorded_utc"] = "2026-09-17T03:00:00Z"
    arm("d1-negative-first", core_determinism(rec, True, True)[0], core_determinism(late, True, True)[0], "negative after positive")
    arm("d1-branch", core_determinism(rec, True, True)[0], core_determinism(rec, True, False)[0], "the broken copy equals the engine")

    files = {"f.json": {"remediations": [{"project": "ADVI_FIRMBKTS", "surfaces": [{"kind": "s3-prefix", "prefix": "p/"}]}]}}
    mk = {"marks": [{"file": "f.json", "project": "ADVI_FIRMBKTS", "entry": {"kind": "s3-prefix", "prefix": "p/"}}]}
    mk2 = {"marks": [{"file": "f.json", "project": "ADVI_FIRMBKTS", "entry": {"kind": "s3-prefix", "prefix": "q/"}}]}
    arm("x1-marks", core_marks(mk, files)[0], core_marks(mk2, files)[0], "an entry absent from its file")
    hman = {"run_id": "R", "files": dict((f, "hash-of-" + f) for f in HASHED_FILES)}
    hact = dict((f, "hash-of-" + f) for f in HASHED_FILES)
    hact_moved = dict(hact)
    hact_moved["MARK.json"] = "hash-of-something-else"
    hman_short = {"run_id": "R", "files": dict((f, "hash-of-" + f) for f in HASHED_FILES if f != "MARK.json")}
    arm("x1-hashes", core_hashes("R", hman, hact)[0], core_hashes("R", hman, hact_moved)[0],
        "one artifact's bytes changed after production")
    arm("x1-hashes-runid", core_hashes("R", hman, hact)[0], core_hashes("OTHER", hman, hact)[0],
        "the manifest describes a different run")
    arm("x1-hashes-omitted", core_hashes("R", hman, hact)[0], core_hashes("R", hman_short, hact)[0],
        "a manifest that omits the file it would have to account for")
    fw = {"aws": {"instrument": "comp-find --corpus aws", "before": {"nodes_scanned": 10, "built": "t1"},
                  "after": {"nodes_scanned": 10, "built": "t2"}, "delta_outside_run": []},
          "served": {"before": {"routes_sha256": "s"}, "after": {"routes_sha256": "s"}}}
    fw2 = copy.deepcopy(fw)
    fw2["aws"]["delta_outside_run"] = ["arn:x"]
    arm("x1-fwd10", core_fwd10(fw)[0], core_fwd10(fw2)[0], "a delta outside the run")
    allowed = ["workflows/legacy_transform/", ROOT + "/"]
    arm("x1-footprint", core_footprint(["workflows/legacy_transform/s/r/contract.json"], allowed)[0],
        core_footprint(["workflows/legacy_transform/s/r/contract.json", "lib/opal_naming.py"], allowed)[0], "a builder edited")

    arm("x2-adding", core_refused(1, "REFUSE ... ADVI_FIRMBKTS")[0], core_refused(0, "WARN ADVI_FIRMBKTS")[0], "rc 0 in WARN")
    arm("x2-removing", core_passes(0, "")[0], core_passes(1, "")[0], "refused")
    arm("x3-filed", core_filed(1, ["A-S1"], ["A-S1", "A-S2"])[0], core_filed(1, ["A-S1"], ["A-S1"])[0], "an OPENED row not filed")
    arm("v1-not-author", core_not_author({"0.9.0_WK_LGIC_LGCTFM~1"})[0], core_not_author({"0.9.0_WK_LGIC_LGCTFM~3"})[0],
        "the reviewer wrote the engine")

    ok = all(r[1] for r in res)
    print("DISCRIMINATING SELF-TEST -- denominator %d arm(s) (A-23); each GREEN must pass and its DOCTORED twin must fail"
          % len(res))
    for name, good, detail in res:
        print("  %-28s %-5s %s" % (name, "PASS" if good else "FAIL", detail))
    covered = sorted(set(r[0].split("-")[0] for r in res))
    print("cells whose pure cores are driven here: %s" % covered)
    print("NOT driven here, stated: the subprocess arms (s2-*, r1-identical/hand-edit/fresh, h1-headings/identity/no-overwrite, "
          "p1-regenerates, d1-pytest, x2-*, x3-two-runs/diff/nontrivial) invoke the worker's CLI; their verdict logic is the "
          "cores above, and each FAILS on an absent input, which is the measured state at the cut.")
    return say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE",
               "an arm that cannot be made to fail is a constant wearing a measurement's clothes")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l"):
        for k in sorted(SUBCOMMANDS):
            print(k)
        print("selftest-arms")
        return 0
    if args[0] == "selftest-arms":
        return selftest_arms()
    fn = SUBCOMMANDS.get(args[0])
    if fn is None:
        return say("FAIL-NO-SUCH-SUBCOMMAND", "unknown subcommand: %s" % args[0])
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001
        return say("FAIL-ARM-RAISED", "the arm raised %s: %s -- a traceback is never a verdict" % (type(exc).__name__, str(exc)[:200]))


if __name__ == "__main__":
    sys.exit(main())
