"""LGIC_LGCTFM ROUND 3 -- the fixed input. Four cells, fifteen mechanical arms.

ROUND 3 EXISTS BECAUSE FWD-1's REALIZED GRADE WAS RETRACTED (R-79 @0e9027c6dc). The ratified ACCEPT says
the person opening the 49 Financial migration "never has to go and list the SCHEDULES, MACHINES, ROLES
and BUCKETS by hand to fill a gap the contract left blank WITHOUT SAYING SO". The graded run carries 0 of
9 Lambdas, 0 of 1 EC2 instance and 0 of 1 DynamoDB table against the subject's own token, and its COMPUTE
column renders "(none)". Andrew, ~18:2xZ: the workflow "must be designed to create rows for these items".

THREE CONSTRUCTION RULES.

1. THE FLOOR IS RE-MEASURED AT GRADE TIME, WITH AN INSTRUMENT THAT IS NOT THE ENGINE. Every coverage arm
   runs `comp-find --corpus aws` over the subject's token itself and prints the cut's figure beside its
   own. A floor read from R3_BASE.json at grade time would be a stale figure acting as a bar -- the exact
   failure that hid LGIC_ENFORCE's W7-S4 for four rounds.

2. EVERY CORE IS DRIVEN BOTH WAYS, AND ONE OF THE NEGATIVES IS REAL. `selftest-arms` runs each core against
   a SIMULATED CORRECT record (PASS required) and a doctored one (FAIL required) -- and runs the coverage
   core against the ACTUAL graded run of 2026-09-18T01:16Z, which must read FAIL. A mutant written by the
   checker's author shares the author's assumption; the graded run does not.

3. THE RECORD SHAPE HAS ONE CARRIER (LGIC_ENFORCE-S85). The coverage block's shape lives ONLY in
   R3_BASE.json. The simulated positive records are BUILT FROM that file, and `selftest-arms` refuses if any
   round-3 order's quoted shape differs from it. Round 9 of LGIC_ENFORCE shipped two orders whose record
   block and checker named different fields, and 13 positive arms missed it because they were fed the
   checker's own vocabulary.

Every arm returns 0 and ends with ONE `VERDICT:` line. Any text a worker authored (a reason, a name) is
passed through _scrub() before it is printed, so evidence can never forge a verdict (LGIC_ENFORCE-S79).
"""

import copy
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
BASEFILE = os.path.join(HERE, "R3_BASE.json")
COMP_FIND = os.path.join(REPO, ".tools", "comp-find")
RECV = os.path.join(REPO, ".tools", "receiving-check.py")
ENGINE = os.path.join(REPO, "lib", "opal_lgctfm.py")
RENDER = os.path.join(REPO, "lib", "lgctfm_render.py")
RUN_HOME = os.path.join(REPO, "workflows", "legacy_transform")

_TYPE_RE = re.compile(r"^  \[([A-Za-z0-9_]+)\]\s*$")
_ENTRY_RE = re.compile(r"^    (.+?)  drift=(\S+) src=(\S+)\s*$")
_DENOM_RE = re.compile(r"DENOMINATOR:\s*(\d+) hit\(s\) across (\d+) aws node\(s\) scanned")
_VINTAGE_RE = re.compile(r"Built from the estate as of ([^.]+)\.")
_SECTION_RE = re.compile(r"^\s*-- ([A-Z]+) --\s*$")
_ORDER_SHAPE_RE = re.compile(r"COVERAGE BLOCK SHAPE[^\n]*\n+```json\n(.*?)\n```", re.S)


def _scrub(text):
    return str(text).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def say(tag, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + tag)
    return 0


def verdict(ok, pass_tag, fail_tag, lines):
    return say(pass_tag if ok else fail_tag, *lines)


def ab(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def load_json(p):
    try:
        with open(ab(p), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def base():
    return load_json(BASEFILE)


def run(argv, timeout=600, cwd=None):
    try:
        p = subprocess.run(argv, cwd=cwd or REPO, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 124, "RUN-FAILED: %s" % exc
    txt = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, txt


# ------------------------------------------------------------------ the floor (instrument: comp-find)
def parse_floor(text):
    cur = None
    names = {}
    for ln in text.splitlines():
        m = _TYPE_RE.match(ln)
        if m:
            cur = m.group(1)
            continue
        m = _ENTRY_RE.match(ln)
        if m and cur:
            names.setdefault(cur, set()).add(m.group(1))
    dm = _DENOM_RE.search(text)
    vm = _VINTAGE_RE.search(text)
    meta = {"hits": int(dm.group(1)) if dm else None, "scanned": int(dm.group(2)) if dm else None,
            "vintage": vm.group(1) if vm else None}
    return names, meta


def floor_now(b):
    fl = b["floor"]
    rc, txt = run([sys.executable, COMP_FIND, "--corpus", "aws", fl["pattern"], fl["flags"], "--all",
                   "--budget", "240"], timeout=420)
    names, meta = parse_floor(txt)
    if rc != 0 or meta["hits"] is None or meta["scanned"] in (None, 0):
        return None, meta, "floor NOT MEASURABLE (comp-find rc=%s, denominator %s) -- never a pass" % (
            rc, meta["hits"])
    got = sum(len(v) for v in names.values())
    note = "floor re-measured: %d node(s) across %d type(s); denominator %d hit(s) of %d scanned; vintage %s " \
           "| at the cut: %s" % (got, len(names), meta["hits"], meta["scanned"], meta["vintage"],
                                 fl["denominator"])
    return names, meta, note


# ------------------------------------------------------------------ contract helpers
def row_name(r):
    cur = r.get("current") or {}
    n = cur.get("name")
    if isinstance(n, dict):
        n = n.get("value")
    return str(n) if n is not None else ""


def row_path(r):
    cur = r.get("current") or {}
    a = cur.get("arn_or_path")
    if isinstance(a, dict):
        a = a.get("value")
    return str(a) if a is not None else ""


def rows_by_type(contract):
    out = {}
    for r in contract.get("rows") or []:
        nt = r.get("node_type") or ""
        out.setdefault(nt, []).append(r)
    return out


def is_rowed(name, rows):
    for r in rows:
        if row_name(r) == name or row_path(r).endswith("/" + name) or row_path(r).endswith(":" + name):
            return True
    return False


# ------------------------------------------------------------------ cores
def core_cov_shape(contract, floor_types):
    """The block exists, is shaped as R3_BASE says, and its arithmetic closes against the contract's rows."""
    cov = contract.get("coverage")
    if not isinstance(cov, dict):
        return False, ["no top-level `coverage` block"]
    bad = []
    legs = cov.get("legs")
    allowed = {"token", "trigger_target", "iam_grant", "source_text"}
    if not isinstance(legs, list) or not legs or not set(legs) <= allowed:
        bad.append("legs %s is not a non-empty subset of %s" % (_scrub(legs), sorted(allowed)))
    for k in ("instrument", "vintage"):
        if not str(cov.get(k) or "").strip():
            bad.append("`%s` empty" % k)
    tf = cov.get("token_floor")
    if not isinstance(tf, dict) or not str(tf.get("pattern") or "").strip():
        bad.append("token_floor.pattern missing")
    bnt = cov.get("by_node_type")
    if not isinstance(bnt, dict):
        return False, bad + ["by_node_type is not an object"]
    missing_types = sorted(set(floor_types) - set(bnt))
    if missing_types:
        bad.append("floor node_types absent from by_node_type: %s" % missing_types)
    have = rows_by_type(contract)
    for nt, ent in sorted(bnt.items()):
        if not isinstance(ent, dict):
            bad.append("%s: entry is not an object" % _scrub(nt))
            continue
        inv, rw = ent.get("involved"), ent.get("rows")
        nc, ex = ent.get("not_covered") or [], ent.get("excluded") or []
        if not isinstance(inv, int) or not isinstance(rw, int) or inv < 0 or rw < 0:
            bad.append("%s: involved/rows not non-negative ints" % _scrub(nt))
            continue
        if inv != rw + len(nc):
            bad.append("%s: involved %d != rows %d + not_covered %d" % (_scrub(nt), inv, rw, len(nc)))
        if rw > len(have.get(nt, [])):
            bad.append("%s: claims %d row(s) but the contract carries %d" % (_scrub(nt), rw, len(have.get(nt, []))))
        for e in list(nc) + list(ex):
            if not isinstance(e, dict) or not str(e.get("name") or "").strip() or not str(e.get("reason") or "").strip():
                bad.append("%s: an excluded/not_covered entry lacks name or reason" % _scrub(nt))
    return (not bad), (bad or ["shape OK: %d node_type(s), legs %s, arithmetic closes on every type"
                               % (len(bnt), _scrub(legs))])


def core_cov_floor(contract, floor_names):
    """Every floor node is a ROW of its type, or an EXCLUDED entry with a reason. Prints the denominator."""
    cov = contract.get("coverage") or {}
    bnt = cov.get("by_node_type") or {}
    have = rows_by_type(contract)
    lines, miss = [], []
    total = rowed = excl = 0
    for nt in sorted(floor_names):
        ex_names = {str(e.get("name")) for e in (bnt.get(nt) or {}).get("excluded") or [] if isinstance(e, dict)}
        r = x = 0
        for n in sorted(floor_names[nt]):
            total += 1
            if is_rowed(n, have.get(nt, [])):
                r += 1
            elif n in ex_names:
                x += 1
            else:
                miss.append("%s %s" % (nt, _scrub(n)))
        rowed += r
        excl += x
        lines.append("  %-20s floor %3d  rowed %3d  excluded %3d  unaccounted %3d"
                     % (nt, len(floor_names[nt]), r, x, len(floor_names[nt]) - r - x))
    lines.append("floor %d = rowed %d + excluded %d + unaccounted %d" % (total, rowed, excl, len(miss)))
    if miss:
        lines.append("UNACCOUNTED (first 20 of %d): %s" % (len(miss), "; ".join(miss[:20])))
    return (not miss and total > 0), lines


def core_cov_named(contract, floor_names, named):
    """For a NAMED class: every floor node is a ROW; excluded and not_covered are both empty."""
    cov = contract.get("coverage") or {}
    bnt = cov.get("by_node_type") or {}
    have = rows_by_type(contract)
    bad, lines = [], []
    for nt in named:
        fl = sorted(floor_names.get(nt, set()))
        ent = bnt.get(nt) or {}
        rowed = [n for n in fl if is_rowed(n, have.get(nt, []))]
        lines.append("  %-16s rowed %d of %d floor node(s); excluded %d; not_covered %d"
                     % (nt, len(rowed), len(fl), len(ent.get("excluded") or []), len(ent.get("not_covered") or [])))
        if len(rowed) != len(fl):
            bad.append("%s: %s not rowed" % (nt, ", ".join(_scrub(n) for n in fl if n not in rowed)))
        if ent.get("excluded") or ent.get("not_covered"):
            bad.append("%s: a NAMED class carries an exclusion or a not_covered entry" % nt)
    return (not bad), lines + bad


def receiving_accept(path):
    """ACCEPT as an lgctfm-contract.

    receiving-check.py routes BY PATH (:77): the lgctfm-contract route matches only
    `workflows/legacy_transform/<subject>/<run>/contract.json` or `*.lgctfm-contract.json`. A contract a
    CELL writes into its deliverables folder matches neither and reads `UNCHECKED unrecognised` -- so this
    arm could not pass for ANY correct record at the path the order mandates (row LGIC_LGCTFM-W1-S23,
    BLOCKING, disarmed here by the issuer). A path the router does not route is graded by the ROUTE'S OWN
    CHECKER instead, and the output says which instrument answered. The router's own gap is W1-S23's to
    carry; the bar is unchanged -- the same checker, the same ACCEPT.
    """
    routed = re.search(r"workflows/legacy_transform/[^/]+/[^/]+/contract\.json$|\.lgctfm-contract\.json$",
                       path.replace(os.sep, "/"), re.I) is not None
    argv = [sys.executable, RECV if routed else os.path.join(REPO, ".tools", "lgctfm-contract-check.py"), ab(path)]
    rc, txt = run(argv, timeout=240)
    ok = rc == 0 and re.search(r"^\s*ACCEPT\s+lgctfm-contract|^ACCEPT lgctfm-contract", txt, re.M) is not None
    return ok, "%s rc=%d %s: %s" % ("receiving-check" if routed else "lgctfm-contract-check (receiving-check "
                                    "does not ROUTE this path -- W1-S23)", rc, "ACCEPT" if ok else "NOT ACCEPT", path)


# ------------------------------------------------------------------ renderer cores
def render_to(contract_path, outdir):
    rc, txt = run([sys.executable, RENDER, "render", ab(contract_path), "--out", outdir], timeout=180)
    try:
        with open(os.path.join(outdir, "flow.current.md"), encoding="utf-8") as fh:
            cur = fh.read()
        with open(os.path.join(outdir, "flow.desired.md"), encoding="utf-8") as fh:
            des = fh.read()
    except OSError:
        return None, None, "render rc=%d produced no flow files: %s" % (rc, _scrub(txt[-300:]))
    return cur, des, "render rc=%d" % rc


def sections(md):
    out, cur = {}, None
    for ln in md.splitlines():
        m = _SECTION_RE.match(ln)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        if cur is not None:
            if ln.startswith("   -- ") or (ln and not ln.startswith(" ")):
                cur = None
                continue
            out[cur].append(ln)
    return out


def core_no_bare_none(texts):
    bad = [i for i, t in enumerate(texts) for ln in t.splitlines() if ln.strip() == "(none)"]
    return (not bad), "bare '(none)' lines: %d" % len(bad)


def core_not_measured(md, columns):
    sec = sections(md)
    lacking = [c for c in columns if not any("NOT MEASURED" in ln for ln in sec.get(c, []))]
    return (not lacking), "columns lacking a NOT MEASURED line: %s (of %d)" % (lacking, len(columns))


def column_sums(contract, node_type_column):
    sums = {}
    for nt, ent in ((contract.get("coverage") or {}).get("by_node_type") or {}).items():
        col = node_type_column.get(nt)
        if col is None or not isinstance(ent, dict):
            continue
        r, i = sums.get(col, (0, 0))
        sums[col] = (r + int(ent.get("rows") or 0), i + int(ent.get("involved") or 0))
    return sums


def core_coverage_lines(md, contract, columns, node_type_column):
    sec = sections(md)
    sums = column_sums(contract, node_type_column)
    bad = []
    for c in columns:
        r, i = sums.get(c, (0, 0))
        want = "%d row(s) of %d involved" % (r, i)
        if not any(want in ln for ln in sec.get(c, [])):
            bad.append("%s wants '%s'" % (c, want))
    return (not bad), ("every column prints its sum" if not bad else "; ".join(bad))


def render_mod():
    sys.path.insert(0, os.path.join(REPO, "lib"))
    try:
        import lgctfm_render as m  # noqa: E402
    finally:
        sys.path.pop(0)
    return m


# ------------------------------------------------------------------ simulated records, BUILT FROM R3_BASE
def simulated_contract(b, graded):
    """A CORRECT round-3 contract: the graded run's rows plus one row per named-class floor node, and a
    coverage block built from R3_BASE's own shape. Never hand-authored beside the checker."""
    c = copy.deepcopy(graded)
    shape = copy.deepcopy(b["coverage_block_shape"]["shape"]["coverage"])
    floor = {k: set(v) for k, v in b["named_classes"]["floor_names_at_cut"].items()}
    have = rows_by_type(c)
    n = 9000
    for nt, names in floor.items():
        for nm in sorted(names):
            if not is_rowed(nm, have.get(nt, [])):
                n += 1
                c["rows"].append({"row_id": "R-%d" % n, "node_type": nt, "kind": "resource",
                                  "subject": c.get("subject"), "mark": None, "desired": {},
                                  "current": {"name": {"value": nm, "status": "MEASURED"},
                                              "arn_or_path": {"value": nm, "status": "MEASURED"}}})
    have = rows_by_type(c)
    tmpl = shape["by_node_type"]["LAMBDA"]
    bnt = {}
    for nt in sorted(set(have) | set(floor) | set(b["floor"]["by_node_type"])):
        ent = copy.deepcopy(tmpl)
        ent["excluded"], ent["not_covered"] = [], []
        ent["rows"] = len(have.get(nt, []))
        ent["involved"] = ent["rows"]
        bnt[nt] = ent
    shape["by_node_type"] = bnt
    shape["instrument"] = "simulated: token leg plus trigger targets"
    shape["legs"] = ["token", "trigger_target"]
    shape["vintage"] = b["floor"]["vintage"]
    shape["token_floor"] = {"pattern": b["floor"]["pattern"], "hits": 88, "scanned": 2590}
    c["coverage"] = shape
    return c, floor


# ------------------------------------------------------------------ run discovery (never by position)
def newest_run_after_cut(b):
    subj = b["subject"]["run_home_subject"]
    cut = b["cut_at"].replace("-", "").replace(":", "").replace("Z", "")
    runs = []
    for d in glob.glob(os.path.join(RUN_HOME, subj, "*")):
        rid = os.path.basename(d)
        m = re.match(r"^(\d{8}T\d{6})Z-[0-9a-f]+$", rid)
        if m and m.group(1) > cut[:13] + "00" and os.path.isfile(os.path.join(d, "HASHES.json")):
            runs.append((m.group(1), d))
    runs.sort()
    return (runs[-1][1] if runs else None), len(runs)


# ------------------------------------------------------------------ arms: LT-e-5
def _e5_contract(b):
    c = load_json(b["e5_walk_output"])
    return c


def e5_coverage_shape():
    b = base()
    c = _e5_contract(b)
    if c is None:
        return say("FAIL-E5-COVERAGE-SHAPE", "no contract at %s" % b["e5_walk_output"])
    ok, lines = core_cov_shape(c, list(b["floor"]["by_node_type"]))
    return verdict(ok, "PASS-E5-COVERAGE-SHAPE", "FAIL-E5-COVERAGE-SHAPE", lines)


def e5_floor():
    b = base()
    c = _e5_contract(b)
    if c is None:
        return say("FAIL-E5-FLOOR", "no contract at %s" % b["e5_walk_output"])
    names, _meta, note = floor_now(b)
    if names is None:
        return say("FAIL-E5-FLOOR", note)
    ok, lines = core_cov_floor(c, names)
    return verdict(ok, "PASS-E5-FLOOR", "FAIL-E5-FLOOR", [note] + lines)


def e5_named_rowed():
    b = base()
    c = _e5_contract(b)
    if c is None:
        return say("FAIL-E5-NAMED-ROWED", "no contract at %s" % b["e5_walk_output"])
    names, _meta, note = floor_now(b)
    if names is None:
        return say("FAIL-E5-NAMED-ROWED", note)
    ok, lines = core_cov_named(c, names, b["named_classes"]["classes"])
    return verdict(ok, "PASS-E5-NAMED-ROWED", "FAIL-E5-NAMED-ROWED", [note] + lines)


def e5_schema():
    b = base()
    ok_new, l1 = receiving_accept(b["e5_walk_output"])
    ok_old, l2 = receiving_accept(os.path.join(b["graded_run_negative_control"]["run_dir"], "contract.json"))
    return verdict(ok_new and ok_old, "PASS-E5-SCHEMA", "FAIL-E5-SCHEMA",
                   ["new contract: " + l1, "graded run (frozen, R-43): " + l2])


# ------------------------------------------------------------------ arms: LT-r-2
def r2_no_bare_none():
    b = base()
    tmp = tempfile.mkdtemp(prefix="lt_r3_r2_")
    try:
        contracts = sorted(glob.glob(os.path.join(RUN_HOME, "*", "*", "contract.json")))
        texts, notes = [], []
        for i, cp in enumerate(contracts):
            od = os.path.join(tmp, str(i))
            os.makedirs(od)
            cur, des, note = render_to(cp, od)
            if cur is None:
                notes.append("UNRENDERABLE %s: %s" % (os.path.relpath(cp, REPO), note))
                continue
            texts += [cur, des]
        ok, line = core_no_bare_none(texts)
        graded = os.path.join(b["graded_run_negative_control"]["run_dir"], "contract.json")
        od = os.path.join(tmp, "graded")
        os.makedirs(od)
        cur, _des, _n = render_to(graded, od)
        nm_ok, nm_line = core_not_measured(cur or "", render_mod().COLUMNS) if cur else (False, "graded unrenderable")
        return verdict(ok and nm_ok and not notes and len(contracts) > 0, "PASS-R2-NO-BARE-NONE", "FAIL-R2-NO-BARE-NONE",
                       ["contracts rendered: %d of %d found under the run home" % (len(texts) // 2, len(contracts)),
                        line, "graded run: " + nm_line] + notes)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def r2_coverage_lines():
    b = base()
    graded = load_json(os.path.join(b["graded_run_negative_control"]["run_dir"], "contract.json"))
    sim, _floor = simulated_contract(b, graded)
    tmp = tempfile.mkdtemp(prefix="lt_r3_r2c_")
    try:
        cp = os.path.join(tmp, "contract.json")
        with open(cp, "w", encoding="utf-8") as fh:
            json.dump(sim, fh)
        od = os.path.join(tmp, "out")
        os.makedirs(od)
        cur, _des, note = render_to(cp, od)
        if cur is None:
            return say("FAIL-R2-COVERAGE-LINES", note)
        m = render_mod()
        ok, line = core_coverage_lines(cur, sim, m.COLUMNS, m.NODE_TYPE_COLUMN)
        nb_ok, nb = core_no_bare_none([cur])
        return verdict(ok and nb_ok, "PASS-R2-COVERAGE-LINES", "FAIL-R2-COVERAGE-LINES",
                       ["a contract built from R3_BASE's coverage shape: " + line, nb])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def r2_regen():
    """FWD-5's ACCEPT survives: rendering is deterministic, and changing a row changes the picture."""
    b = base()
    graded = os.path.join(b["graded_run_negative_control"]["run_dir"], "contract.json")
    tmp = tempfile.mkdtemp(prefix="lt_r3_r2g_")
    try:
        outs = []
        for k in ("a", "b"):
            od = os.path.join(tmp, k)
            os.makedirs(od)
            outs.append(render_to(graded, od)[0])
        c = load_json(graded)
        c["rows"] = c["rows"][:-1]
        cp = os.path.join(tmp, "edited.json")
        with open(cp, "w", encoding="utf-8") as fh:
            json.dump(c, fh)
        od = os.path.join(tmp, "e")
        os.makedirs(od)
        edited = render_to(cp, od)[0]
        det = outs[0] is not None and outs[0] == outs[1]
        moves = edited is not None and edited != outs[0]
        return verdict(det and moves, "PASS-R2-REGEN", "FAIL-R2-REGEN",
                       ["deterministic (two renders byte-identical): %s" % det,
                        "one row removed -> picture changes: %s" % moves])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ arms: LT-p-2
def _plan_on_copy(b):
    src = b["graded_run_negative_control"]["run_dir"]
    tmp = tempfile.mkdtemp(prefix="lt_r3_p2_")
    dst = os.path.join(tmp, os.path.basename(src))
    shutil.copytree(ab(src), dst)
    old = load_json(os.path.join(dst, "plan.json"))
    rc, txt = run([sys.executable, ENGINE, "plan", dst], timeout=300)
    new = load_json(os.path.join(dst, "plan.json"))
    return tmp, old, new, rc, txt


def _packages(plan):
    if isinstance(plan, dict):
        for k in ("packages", "plan"):
            if isinstance(plan.get(k), list):
                return plan[k]
    return plan if isinstance(plan, list) else []


def core_p2_renamed(new_plan):
    pk = _packages(new_plan)
    has_old = sum(1 for p in pk if isinstance(p, dict) and "dependencies" in p)
    has_new = sum(1 for p in pk if isinstance(p, dict) and "step_dependencies" in p)
    return (len(pk) > 0 and has_old == 0 and has_new == len(pk)), \
        "packages %d; carrying `dependencies` %d; carrying `step_dependencies` %d" % (len(pk), has_old, has_new)


def core_p2_values(old_plan, new_plan):
    po, pn = _packages(old_plan), _packages(new_plan)
    if len(po) != len(pn) or not po:
        return False, "package counts differ or empty: old %d new %d" % (len(po), len(pn))
    diff = sum(1 for a, c in zip(po, pn) if (a.get("dependencies") or []) != (c.get("step_dependencies") or []))
    pop = sum(1 for a in po if a.get("dependencies"))
    return diff == 0, "values compared package by package: %d of %d differ; %d populated" % (diff, len(po), pop)


def p2_renamed():
    b = base()
    tmp, _old, new, rc, txt = _plan_on_copy(b)
    try:
        ok, line = core_p2_renamed(new)
        return verdict(ok, "PASS-P2-RENAMED", "FAIL-P2-RENAMED", ["plan on a COPY of the graded run, rc=%d" % rc, line])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def p2_values_preserved():
    b = base()
    tmp, old, new, rc, _txt = _plan_on_copy(b)
    try:
        ok, line = core_p2_values(old, new)
        return verdict(ok, "PASS-P2-VALUES-PRESERVED", "FAIL-P2-VALUES-PRESERVED", ["plan rc=%d" % rc, line])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def p2_old_untouched():
    b = base()
    rd = b["graded_run_negative_control"]["run_dir"]
    h = load_json(os.path.join(rd, "HASHES.json")) or {}
    bad = []
    for fn, want in sorted((h.get("files") or {}).items()):
        rc, got = run(["git", "hash-object", ab(os.path.join(rd, fn))], timeout=60)
        if got.strip() != want:
            bad.append("%s: %s != %s" % (fn, got.strip()[:12], want[:12]))
    n = len(h.get("files") or {})
    return verdict(n > 0 and not bad, "PASS-P2-OLD-UNTOUCHED", "FAIL-P2-OLD-UNTOUCHED",
                   ["graded run's %d manifest file(s) re-hashed with git hash-object (HASHES.json's own "
                    "instrument): %d differ" % (n, len(bad))] + bad)


# ------------------------------------------------------------------ arms: LT-x-4
def _x4(b):
    d, n = newest_run_after_cut(b)
    return d, n


def x4_run():
    b = base()
    d, n = _x4(b)
    if not d:
        return say("FAIL-X4-RUN", "no run under %s newer than the cut with HASHES.json (%d found)"
                   % (b["subject"]["run_home_subject"], n))
    c = load_json(os.path.join(d, "contract.json"))
    ok_r, l1 = receiving_accept(os.path.join(d, "contract.json"))
    ok_s, lines = core_cov_shape(c or {}, list(b["floor"]["by_node_type"]))
    return verdict(ok_r and ok_s, "PASS-X4-RUN", "FAIL-X4-RUN",
                   ["run: %s (%d post-cut run(s))" % (os.path.relpath(d, REPO), n), l1] + lines)


def x4_floor():
    b = base()
    d, _n = _x4(b)
    c = load_json(os.path.join(d, "contract.json")) if d else None
    if c is None:
        return say("FAIL-X4-FLOOR", "no post-cut run contract")
    names, _meta, note = floor_now(b)
    if names is None:
        return say("FAIL-X4-FLOOR", note)
    ok1, l1 = core_cov_floor(c, names)
    ok2, l2 = core_cov_named(c, names, b["named_classes"]["classes"])
    return verdict(ok1 and ok2, "PASS-X4-FLOOR", "FAIL-X4-FLOOR", [note] + l1 + ["named classes:"] + l2)


def x4_render():
    b = base()
    d, _n = _x4(b)
    if not d:
        return say("FAIL-X4-RENDER", "no post-cut run")
    try:
        with open(os.path.join(d, "flow.current.md"), encoding="utf-8") as fh:
            cur = fh.read()
    except OSError:
        return say("FAIL-X4-RENDER", "no flow.current.md in the run")
    nb_ok, nb = core_no_bare_none([cur])
    comp = "\n".join(sections(cur).get("COMPUTE", []))
    want = b["named_classes"]["floor_names_at_cut"]
    missing = [n for k in ("LAMBDA", "EC2_INSTANCE") for n in want[k] if ("name=%s " % n) not in comp + " "]
    return verdict(nb_ok and not missing, "PASS-X4-RENDER", "FAIL-X4-RENDER",
                   [nb, "COMPUTE column names %d of %d cut-floor Lambda/EC2 node(s)"
                    % (len(want["LAMBDA"]) + len(want["EC2_INSTANCE"]) - len(missing),
                       len(want["LAMBDA"]) + len(want["EC2_INSTANCE"]))] +
                   (["missing: " + ", ".join(missing)] if missing else []))


def x4_no_registry_move():
    b = base()
    paths = ["infra/logic/registry/", "org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json"]
    rc, txt = run(["git", "diff", "--name-only", b["cut_pin"], "HEAD", "--"] + paths, timeout=60)
    changed = [ln for ln in txt.splitlines() if ln.strip()]
    rc2, _ = run(["git", "cat-file", "-e", b["cut_pin"] + "^{commit}"], timeout=30)
    return verdict(rc == 0 and rc2 == 0 and not changed, "PASS-X4-NO-REGISTRY-MOVE", "FAIL-X4-NO-REGISTRY-MOVE",
                   ["git diff %s..HEAD over the registries and LEGACY_SERVED_PATHS: %d path(s) changed (rc=%d, pin "
                    "resolvable=%s)" % (b["cut_pin"][:10], len(changed), rc, rc2 == 0)] + changed)


# ------------------------------------------------------------------ selftest
def selftest_arms():
    b = base()
    res = []

    def arm(name, ok, why):
        res.append((name, bool(ok), why))

    graded = load_json(os.path.join(b["graded_run_negative_control"]["run_dir"], "contract.json"))
    sim, floor = simulated_contract(b, graded)
    types = list(b["floor"]["by_node_type"])

    # POSITIVE: a correct record built from R3_BASE's own shape must PASS every coverage core.
    ok, why = core_cov_shape(sim, types)
    arm("POSITIVE-cov-shape", ok, "; ".join(why)[:160])
    arm("POSITIVE-cov-floor", core_cov_floor(sim, floor)[0], "every cut-floor named node rowed")
    arm("POSITIVE-cov-named", core_cov_named(sim, floor, b["named_classes"]["classes"])[0], "named classes rowed")
    ex = copy.deepcopy(sim)
    ex["coverage"]["by_node_type"].setdefault("LOG_GROUP", {"involved": 0, "rows": 0, "excluded": [], "not_covered": []})
    ex["coverage"]["by_node_type"]["LOG_GROUP"]["excluded"] = [{"name": "/aws/lambda/x", "reason": "a log sink"}]
    fl2 = dict(floor)
    fl2["LOG_GROUP"] = {"/aws/lambda/x"}
    arm("POSITIVE-cov-floor-exclusion", core_cov_floor(ex, fl2)[0], "an excluded non-named floor node with a reason")

    # MUTANTS
    m1 = copy.deepcopy(sim)
    m1["rows"] = [r for r in m1["rows"] if row_name(r) != "bd-49f-runner"]
    arm("MUTANT-cov-floor-drops-a-lambda", not core_cov_floor(m1, floor)[0], "a Lambda row removed -> FAIL")
    arm("MUTANT-cov-named-drops-a-lambda", not core_cov_named(m1, floor, b["named_classes"]["classes"])[0], "-> FAIL")
    m2 = copy.deepcopy(sim)
    m2["coverage"]["by_node_type"]["LAMBDA"]["excluded"] = [{"name": "bd-49f-runner", "reason": "x"}]
    arm("MUTANT-cov-named-exclusion", not core_cov_named(m2, floor, b["named_classes"]["classes"])[0],
        "a NAMED class exclusion -> FAIL")
    m3 = copy.deepcopy(sim)
    m3["coverage"]["by_node_type"]["LAMBDA"]["involved"] += 1
    arm("MUTANT-cov-arithmetic", not core_cov_shape(m3, [])[0], "involved != rows + not_covered -> FAIL")
    m4 = copy.deepcopy(sim)
    del m4["coverage"]
    arm("MUTANT-cov-absent", not core_cov_shape(m4, [])[0], "no block -> FAIL")
    m5 = copy.deepcopy(sim)
    m5["coverage"]["by_node_type"]["LAMBDA"]["rows"] = 999
    arm("MUTANT-cov-rows-overclaim", not core_cov_shape(m5, [])[0], "claims more rows than exist -> FAIL")

    # THE REAL NEGATIVE CONTROL: the actual graded run must FAIL the coverage cores.
    arm("REAL-NEGATIVE-graded-run-shape", not core_cov_shape(graded, types)[0], "graded run has no block -> FAIL")
    arm("REAL-NEGATIVE-graded-run-named", not core_cov_named(graded, floor, b["named_classes"]["classes"])[0],
        "LAMBDA 0 of 9, EC2 0 of 1, DDB 0 of 1 -> FAIL")

    # RENDER cores
    m = render_mod()
    cols = m.COLUMNS
    good_old = "\n".join("   -- %s --\n  coverage: NOT MEASURED (no coverage block)" % c for c in cols)
    arm("POSITIVE-not-measured", core_not_measured(good_old, cols)[0], "every column carries NOT MEASURED")
    arm("MUTANT-not-measured", not core_not_measured("   -- TRIGGERS --\n  (none)", cols)[0], "-> FAIL")
    arm("POSITIVE-no-bare-none", core_no_bare_none(["x\n  coverage: NOT MEASURED"])[0], "")
    arm("MUTANT-no-bare-none", not core_no_bare_none(["   -- COMPUTE --\n  (none)"])[0], "-> FAIL")
    sums = column_sums(sim, m.NODE_TYPE_COLUMN)
    good_new = "\n".join("   -- %s --\n  coverage: %d row(s) of %d involved node(s)" % (c, sums.get(c, (0, 0))[0],
                                                                                       sums.get(c, (0, 0))[1]) for c in cols)
    arm("POSITIVE-coverage-lines", core_coverage_lines(good_new, sim, cols, m.NODE_TYPE_COLUMN)[0], "sums printed")
    arm("MUTANT-coverage-lines", not core_coverage_lines(good_old, sim, cols, m.NODE_TYPE_COLUMN)[0], "-> FAIL")

    # PLAN cores
    old = {"packages": [{"id": "a", "dependencies": []}, {"id": "b", "dependencies": ["a"]}]}
    new = {"packages": [{"id": "a", "step_dependencies": []}, {"id": "b", "step_dependencies": ["a"]}]}
    arm("POSITIVE-p2-renamed", core_p2_renamed(new)[0], "")
    arm("MUTANT-p2-renamed", not core_p2_renamed(old)[0], "old field -> FAIL")
    arm("POSITIVE-p2-values", core_p2_values(old, new)[0], "")
    bad = {"packages": [{"id": "a", "step_dependencies": []}, {"id": "b", "step_dependencies": ["x"]}]}
    arm("MUTANT-p2-values", not core_p2_values(old, bad)[0], "a changed value -> FAIL")

    # SCRUB
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-X4-RUN"), "evidence cannot forge a verdict")

    # S85: every round-3 order QUOTES the one carrier, byte-for-meaning.
    want = b["coverage_block_shape"]["shape"]
    orders = sorted(glob.glob(os.path.join(REPO, ROOT, "task-orders", "LGIC_LGCTFM.TO-LT-*-r3.*.md")))
    quoting = 0
    for op in orders:
        with open(op, encoding="utf-8") as fh:
            t = fh.read()
        mm = _ORDER_SHAPE_RE.search(t)
        if mm is None:
            continue
        quoting += 1
        try:
            got = json.loads(mm.group(1))
        except ValueError:
            got = None
        arm("S85-order-quotes-carrier:%s" % os.path.basename(op)[len("LGIC_LGCTFM.TO-"):][:24], got == want,
            "quoted shape equals R3_BASE's")
    arm("S85-at-least-one-order-quotes", quoting > 0 or not orders,
        "%d of %d round-3 order(s) quote the shape" % (quoting, len(orders)))

    for name, ok, why in res:
        print("  %-44s %s  %s" % (name, "PASS" if ok else "FAIL", _scrub(why)))
    pos = sum(1 for n, _o, _w in res if n.startswith("POSITIVE-"))
    real = sum(1 for n, _o, _w in res if n.startswith("REAL-"))
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY built from R3_BASE's shape, %d REAL negative on the graded "
          "run, %d mutant/other)" % (len(res), pos, real, len(res) - pos - real))
    print("NOT driven here, stated: floor_now(), receiving_accept() and render_to(), which are live instrument "
          "calls with no fixture; the real arms exercise them and print their denominators.")
    allok = all(ok for _n, ok, _w in res)
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if allok else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {
    "e5-coverage-shape": e5_coverage_shape, "e5-floor": e5_floor, "e5-named-rowed": e5_named_rowed,
    "e5-schema": e5_schema,
    "r2-no-bare-none": r2_no_bare_none, "r2-coverage-lines": r2_coverage_lines, "r2-regen": r2_regen,
    "p2-renamed": p2_renamed, "p2-values-preserved": p2_values_preserved, "p2-old-untouched": p2_old_untouched,
    "x4-run": x4_run, "x4-floor": x4_floor, "x4-render": x4_render, "x4-no-registry-move": x4_no_registry_move,
    "selftest-arms": selftest_arms,
}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("unknown subcommand: %s" % (argv[1] if len(argv) > 1 else "<none>"))
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
