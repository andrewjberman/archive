#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-1 (Muni to Custom) -- CHECK, 0.9.0_WK_MDPF_CANON~r11k2, 2026-10-16. Not issued.

The cell: the vendor account `Opal_Muni_Income` (63,241,218.96 on a measured date) leaves income_non_model_residual and
enters by_model / model_aua under a NEW registered custom key `opal_muni_income` whose display name is "Opal Municipal
Bonds". The sleeve (`Opal_Muni_Sleeve` -> opal_muni_sleeve) is unchanged, the new key is a SEPARATE key, and
`Opal Hewitt Moderate Income` stays in the residual. Registration files: data/assets/scripts/gold/
build_cottonwood_mdpf_slice.py (CUSTOM_KEY, CUSTOM_DISPLAY_NAME); data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py
and its byte-identical Lambda copy under infra/aws/lambda/opal-assets/opal-assets-daily-emitter/ (ModelEntry, the custom
list COTTONWOOD_CUSTOM_MODEL_KEYS, the display map GLOBAL_ACCOUNT_DIST_DISPLAY); GLOBAL_MODEL_KEYS in
data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py.

  python r11_cn_s_1.py pure      six arms: the producer's own build_slice on small in-memory fixtures (no file written,
                                 no S3, no network). The base reads 4 of 6 (A1 and A3 red) until the cell lands.
  python r11_cn_s_1.py seams     four arms on the registration files: S1 the two crosswalk copies are byte-identical;
                                 S2 both copies define the ModelEntry, the custom-list row and the display-map row;
                                 S3 GLOBAL_MODEL_KEYS holds the new key and still holds opal_muni_sleeve (the dim file is
                                 read with the ast module and its top-level expression is evaluated over the crosswalk
                                 names it imports); S4 the producer's key and display agree with the crosswalk. The base
                                 reads 1 of 4 (S1 only).
  python r11_cn_s_1.py selftest  issuer only: base reds; a scratch reference (temp copy with the cell's edits applied by
                                 script, read through R11_ROOT in a child process) reads pure 6 of 6 and seams 4 of 4;
                                 planted mutants each turn their named arm red. Temp roots are deleted; the repo is
                                 never written.

Root: env R11_ROOT, else the git toplevel. AWS guard: boto3.client and boto3.resource are refused while the arms run.
rebalancer_schemas is given its own test seed (OPAL_STRATEGY_CONFIG_SEED) through set_strategy_config, so the SMA name
rule never reads the S3 config list.
Output: `ROUND 11 CN-S-1 PURE: k of n arms`, `ROUND 11 CN-S-1 SEAMS: k of n arms`; exit 0 only when k == n. ASCII only.
"""
import ast
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # importing the repo's producer must not write __pycache__ into the worktree
N_ARMS = 6
N_SEAMS = 4
TOL = 0.005
DATES = ["2026-10-13", "2026-10-14"]
SLEEVE, SLEEVE_KEY, SLEEVE_DISPLAY, SLEEVE_DOLLARS = "Opal_Muni_Sleeve", "opal_muni_sleeve", "Opal Muni Sleeve", 12345678.90
MUNI, MUNI_DOLLARS = "Opal_Muni_Income", 63241218.96
HEWITT, HEWITT_DOLLARS = "Opal Hewitt Moderate Income", 1749334.30
MUNI2, MUNI2_DOLLARS = "Opal_Muni_Income_2", 1000000.00
PRIMARY, PRIMARY_DOLLARS = "Opal Short-Term", 5000000.00
NEW_KEY, NEW_DISPLAY = "opal_muni_income", "Opal Municipal Bonds"
ROWS = [(SLEEVE, SLEEVE_DOLLARS, 4), (MUNI, MUNI_DOLLARS, 1), (HEWITT, HEWITT_DOLLARS, 1),
        (MUNI2, MUNI2_DOLLARS, 1), (PRIMARY, PRIMARY_DOLLARS, 3)]
RUN_ROWS = {
    "full": ROWS,
    "nomuni": [r for r in ROWS if r[0] != MUNI],
    "nohew": [r for r in ROWS if r[0] != HEWITT],
}
RUN_NAMES = ("full", "nomuni", "nohew")

REL_PRODUCER = os.path.join("data", "assets", "scripts", "gold", "build_cottonwood_mdpf_slice.py")
REL_TEST = os.path.join("data", "assets", "scripts", "gold", "tests", "test_cottonwood_custom_and_sma.py")
REL_XW_GOLD = os.path.join("data", "mdpf", "scripts", "gold", "mdpf_revamp_model_crosswalk.py")
REL_XW_LAMBDA = os.path.join("infra", "aws", "lambda", "opal-assets", "opal-assets-daily-emitter",
                             "mdpf_revamp_model_crosswalk.py")
REL_DIM = os.path.join("data", "mdpf", "scripts", "gold", "dim_mdpf_aggregate_aua_timeseries.py")
REL_SILVER = os.path.join("data", "assets", "scripts", "silver")
REL_GOLD = os.path.join("data", "mdpf", "scripts", "gold")
REL_CALENDAR = os.path.join("lib", "trading_calendar.py")  # the canonical calendar the gold binding resolves (lib.*)


# ---------------------------------------------------------------- helpers over the producer's output
def near(a, b):
    return a is not None and b is not None and abs(float(a) - float(b)) < TOL


def same(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) < TOL


def total_of(rows):
    return round(sum(r[1] for r in rows), 2)


def at(sl, d):
    return sl["dates"].index(d)


def aua(sl, d):
    return sl["model_aua"][at(sl, d)]


def model_val(sl, key, d):
    return sl["by_model"][key]["model_value"][at(sl, d)]


def new_keys(sl):
    return [k for k, v in sl["by_model"].items() if v["display_name"] == NEW_DISPLAY]


def residual(sl, d):
    # the producer writes a dollars_by_date entry only when the date holds residual rows (build_slice: `if len(inc):`),
    # so an absent date is ZERO residual dollars, not an unmeasured one
    return sl["meta"]["income_non_model_residual"]["dollars_by_date"].get(d, 0.0)


def custom_detail(sl, d, name):
    return sl["meta"]["custom_residual_detail"]["by_date"].get(d, {}).get(name)


def model_equal(a, b):
    if sorted(a["by_model"]) != sorted(b["by_model"]):
        return False
    if not all(same(x, y) for x, y in zip(a["model_aua"], b["model_aua"])):
        return False
    return all(same(x, y) for k in a["by_model"]
               for x, y in zip(a["by_model"][k]["model_value"], b["by_model"][k]["model_value"]))


def gold_by_date(rows):
    import pandas as pd
    return {d: pd.DataFrame([{"model_name": n, "dollar_value": float(v), "account_count": int(c), "is_opal": True}
                             for n, v, c in rows]) for d in DATES}


def produce(mod, rows):
    mod.rs.set_strategy_config(mod.rs.OPAL_STRATEGY_CONFIG_SEED)
    sl, _report = mod.build_slice(list(DATES), gold_by_date(rows))
    return sl


# ---------------------------------------------------------------- the six pure arms
def a0(R):
    sl = R["full"]
    m = sl["by_model"].get(SLEEVE_KEY)
    if m is None:
        return False, "no by_model key %s" % SLEEVE_KEY
    vals = [m["model_value"][at(sl, d)] for d in DATES]
    ok = m["display_name"] == SLEEVE_DISPLAY and all(near(v, SLEEVE_DOLLARS) for v in vals)
    return ok, "display %r values %s" % (m["display_name"], vals)


def a1(R):
    sl = R["full"]
    ks = new_keys(sl)
    if not ks:
        return False, "no by_model key with display %r" % NEW_DISPLAY
    k = ks[0]
    vals = [model_val(sl, k, d) for d in DATES]
    res = [residual(sl, d) for d in DATES]
    in_res = [custom_detail(sl, d, MUNI) is not None for d in DATES]
    ok = (all(near(v, MUNI_DOLLARS) for v in vals)
          and all(near(r, HEWITT_DOLLARS + MUNI2_DOLLARS) for r in res)
          and not any(in_res))
    return ok, "key %s values %s residual %s muni-in-residual %s" % (k, vals, res, in_res)


def a2(R):
    full, nohew = R["full"], R["nohew"]
    det = [custom_detail(full, d, HEWITT) for d in DATES]
    in_res = all(x is not None and near(x["dollars"], HEWITT_DOLLARS) for x in det)
    no_model = model_equal(full, nohew)
    return in_res and no_model, ("residual detail %s; by_model and model_aua identical with and without Hewitt: %s"
                                 % ([x and x["dollars"] for x in det], no_model))


def a3(R):
    full, nomuni = R["full"], R["nomuni"]
    ks = new_keys(full)
    if not ks:
        return False, "no by_model key with display %r" % NEW_DISPLAY
    k = ks[0]
    if k == SLEEVE_KEY:
        return False, "the new key is the sleeve key"
    sleeve_same = all(same(model_val(full, SLEEVE_KEY, d), model_val(nomuni, SLEEVE_KEY, d)) for d in DATES)
    delta = [None if aua(full, d) is None or aua(nomuni, d) is None else round(aua(full, d) - aua(nomuni, d), 2)
             for d in DATES]
    no_double = all(near(x, MUNI_DOLLARS) for x in delta)
    return sleeve_same and no_double, ("new key %s; sleeve unchanged %s; model_aua delta %s"
                                       % (k, sleeve_same, delta))


def a4(R):
    off = []
    for name in RUN_NAMES:
        sl = R[name]
        total = total_of(RUN_ROWS[name])
        for d in DATES:
            a, r = aua(sl, d), residual(sl, d)
            if a is None or r is None or not near(a + r, total):
                off.append("%s %s" % (name, d))
    if off:
        return False, "off on " + ", ".join(off)
    return True, "model_aua + residual = fixture total on %d runs x %d dates" % (len(RUN_NAMES), len(DATES))


def a5(R):
    full = R["full"]
    det = [custom_detail(full, d, MUNI2) for d in DATES]
    in_res = all(x is not None and near(x["dollars"], MUNI2_DOLLARS) for x in det)
    ks = new_keys(full)
    k_ok, k_txt = True, "no new key"
    if ks:
        vals = [model_val(full, ks[0], d) for d in DATES]
        k_ok = all(near(v, MUNI_DOLLARS) for v in vals)
        k_txt = "key %s values %s" % (ks[0], vals)
    return in_res and k_ok, ("Opal_Muni_Income_2 residual %s; %s"
                             % ([x and x["dollars"] for x in det], k_txt))


ARMS = [
    ("A0 control: Opal_Muni_Sleeve lands under opal_muni_sleeve", ("full",), a0),
    ("A1 Opal_Muni_Income lands in by_model under a new key, out of the residual", ("full",), a1),
    ("A2 Opal Hewitt Moderate Income stays in the residual, not in by_model", ("full", "nohew"), a2),
    ("A3 new key differs from opal_muni_sleeve; sleeve unchanged; no double count", ("full", "nomuni"), a3),
    ("A4 control: model_aua + residual = fixture total", RUN_NAMES, a4),
    ("A5 control: Opal_Muni_Income_2 is not routed to the new key", ("full",), a5),
]
assert len(ARMS) == N_ARMS


def grade(mod):
    """Returns [(label, ok, detail)] for the six pure arms, in order."""
    R, errs = {}, {}
    for name in RUN_NAMES:
        try:
            R[name] = produce(mod, RUN_ROWS[name])
        except Exception as e:  # the producer raised on the fixture: the arm reads it as red
            errs[name] = "%s: %s" % (type(e).__name__, str(e)[:160])
    out = []
    for label, needs, fn in ARMS:
        missing = [n for n in needs if n not in R]
        if missing:
            out.append((label, False, "producer raised on %s: %s" % (",".join(missing), "; ".join(errs[n] for n in missing))))
            continue
        try:
            ok, txt = fn(R)
        except Exception as e:
            ok, txt = False, "%s: %s" % (type(e).__name__, str(e)[:160])
        out.append((label, bool(ok), txt))
    return out


# ---------------------------------------------------------------- loading (no AWS, no repo writes)
def git_top():
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def repo_root():
    return os.environ.get("R11_ROOT") or git_top()


def producer_path(root):
    return os.path.join(root, REL_PRODUCER)


def sibling_paths(root):
    sys.path[:0] = [os.path.join(root, REL_GOLD), os.path.join(root, REL_SILVER)]


def refuse_aws():
    import boto3

    def _refused(*_a, **_k):
        raise RuntimeError("AWS client refused inside the CN-s-1 check arms")
    boto3.client = _refused
    boto3.resource = _refused


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # registered first: dataclasses in the crosswalk look the module up by name
    spec.loader.exec_module(mod)
    return mod


def err(e):
    return "%s: %s" % (type(e).__name__, str(e)[:160])


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def read_text(path):
    return read_bytes(path).decode("utf-8")


def write_text(path, text):
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise RuntimeError("expected one occurrence of %r, found %d" % (old[:70], n))
    return text.replace(old, new)


# ---------------------------------------------------------------- the four seams arms (registration files)
def s1_control(root):
    a = read_bytes(os.path.join(root, REL_XW_GOLD))
    b = read_bytes(os.path.join(root, REL_XW_LAMBDA))
    ok = a == b
    return ok, "data/mdpf copy %d bytes, Lambda copy %d bytes, %s" % (len(a), len(b), "identical" if ok else "DIFFER")


def s2_both_copies(root):
    notes, ok = [], True
    for tag, rel, mod_name in (("data/mdpf", REL_XW_GOLD, "r11_cn_s_1_xw_gold"),
                               ("Lambda", REL_XW_LAMBDA, "r11_cn_s_1_xw_lambda")):
        xw = load_file(os.path.join(root, rel), mod_name)
        entries = [m for m in xw.CANONICAL_MODELS if m.model_key == NEW_KEY]
        e_ok = len(entries) == 1 and entries[0].display_name == NEW_DISPLAY
        c_ok = NEW_KEY in xw.COTTONWOOD_CUSTOM_MODEL_KEYS
        d_ok = xw.GLOBAL_ACCOUNT_DIST_DISPLAY.get(NEW_KEY) == NEW_DISPLAY
        notes.append("%s: ModelEntry %s, custom list %s, display map %s" % (tag, e_ok, c_ok, d_ok))
        ok = ok and e_ok and c_ok and d_ok
    return ok, "; ".join(notes)


def s3_global_keys(root):
    xw = load_file(os.path.join(root, REL_XW_GOLD), "r11_cn_s_1_xw_s3")
    dim = os.path.join(root, REL_DIM)
    tree = ast.parse(read_text(dim), filename=dim)
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "mdpf_revamp_model_crosswalk":
            for alias in node.names:
                ns[alias.asname or alias.name] = getattr(xw, alias.name)
    found = [n for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "GLOBAL_MODEL_KEYS" for t in n.targets)]
    if len(found) != 1:
        return False, "expected one top-level GLOBAL_MODEL_KEYS assignment in the dim file, found %d" % len(found)
    expr = ast.fix_missing_locations(ast.Expression(body=found[0].value))
    keys = eval(compile(expr, dim, "eval"), dict(ns))
    is_tuple = isinstance(keys, tuple)
    new_in = is_tuple and NEW_KEY in keys
    sleeve_in = is_tuple and SLEEVE_KEY in keys
    return is_tuple and new_in and sleeve_in, ("tuple %s; %s in it %s; %s in it %s; %d keys"
                                               % (is_tuple, NEW_KEY, new_in, SLEEVE_KEY, sleeve_in,
                                                  len(keys) if is_tuple else -1))


def s4_producer_agrees(root):
    sibling_paths(root)
    refuse_aws()
    prod = load_file(producer_path(root), "r11_cn_s_1_prod_s4")
    xw = load_file(os.path.join(root, REL_XW_GOLD), "r11_cn_s_1_xw_s4")
    ck, cd = prod.CUSTOM_KEY, prod.CUSTOM_DISPLAY_NAME
    maps = ck.get(MUNI) == NEW_KEY
    displays = cd.get(NEW_KEY) == NEW_DISPLAY
    sleeve = ck.get(SLEEVE) == SLEEVE_KEY
    entries = [m for m in xw.CANONICAL_MODELS if m.model_key == NEW_KEY]
    agrees = (len(entries) == 1 and entries[0].display_name == cd.get(NEW_KEY)
              and NEW_KEY in xw.COTTONWOOD_CUSTOM_MODEL_KEYS)
    ok = maps and displays and sleeve and agrees
    return ok, ("producer maps %s -> %s %s; displays %r %s; %s still maps to %s %s; crosswalk agrees %s"
                % (MUNI, ck.get(MUNI), maps, NEW_DISPLAY, displays, SLEEVE, ck.get(SLEEVE), sleeve, agrees))


def run_arm(label, fn, *args):
    try:
        ok, txt = fn(*args)
    except Exception as e:  # any load or evaluation failure reads the arm red, with its reason
        ok, txt = False, err(e)
    return label, bool(ok), txt


def seam_arms(root):
    sibling_paths(root)
    return [
        run_arm("S1 control: the two crosswalk copies are byte-identical", s1_control, root),
        run_arm("S2 both crosswalk copies define ModelEntry, custom-list row and display-map row", s2_both_copies, root),
        run_arm("S3 GLOBAL_MODEL_KEYS holds opal_muni_income and still holds opal_muni_sleeve", s3_global_keys, root),
        run_arm("S4 producer maps Opal_Muni_Income to the new key, displays it, agrees with the crosswalk", s4_producer_agrees, root),
    ]


# ---------------------------------------------------------------- scratch reference and planted mutants (temp roots only)
def build_scratch(dst, src):
    """Copies the import siblings and the five registration files from src into dst (no edits yet)."""
    os.makedirs(dst)
    for rel in (REL_SILVER, REL_GOLD):
        shutil.copytree(os.path.join(src, rel), os.path.join(dst, rel),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for rel in (REL_PRODUCER, REL_TEST, REL_XW_LAMBDA, REL_CALENDAR):
        os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(src, rel), os.path.join(dst, rel))


def cell_edits(root):
    """The cell's registration edits, applied by script to the temp copy only."""
    p = producer_path(root)
    t = read_text(p)
    nl = "\r\n" if "\r\n" in t else "\n"
    t = replace_once(t, '"Opal_Muni_Sleeve": "opal_muni_sleeve",',
                     '"Opal_Muni_Sleeve": "opal_muni_sleeve",' + nl + '    "%s": "%s",' % (MUNI, NEW_KEY))
    t = replace_once(t, '"opal_muni_sleeve": "Opal Muni Sleeve",',
                     '"opal_muni_sleeve": "Opal Muni Sleeve",' + nl + '    "%s": "%s",' % (NEW_KEY, NEW_DISPLAY))
    write_text(p, t)
    for rel in (REL_XW_GOLD, REL_XW_LAMBDA):
        p = os.path.join(root, rel)
        t = read_text(p)
        nl = "\r\n" if "\r\n" in t else "\n"
        t = replace_once(t, 'ModelEntry("opal_muni_sleeve", None, "Opal Muni Sleeve", "model", False),',
                         'ModelEntry("opal_muni_sleeve", None, "Opal Muni Sleeve", "model", False),' + nl
                         + '    ModelEntry("%s", None, "%s", "model", False),' % (NEW_KEY, NEW_DISPLAY))
        t = replace_once(t, '"opal_income", "opal_muni_sleeve",',
                         '"opal_income", "opal_muni_sleeve",' + nl + '    "%s",' % NEW_KEY)
        t = replace_once(t, '"opal_muni_sleeve": "Opal Muni Sleeve",',
                         '"opal_muni_sleeve": "Opal Muni Sleeve",' + nl + '    "%s": "%s",' % (NEW_KEY, NEW_DISPLAY))
        write_text(p, t)
    # GLOBAL_MODEL_KEYS (dim file) is NOT edited: it reads COTTONWOOD_CUSTOM_MODEL_KEYS from the crosswalk, so the
    # crosswalk's custom-list row reaches it. The check reads the resulting tuple, not the text.
    p = os.path.join(root, REL_TEST)
    t = read_text(p)
    t = replace_once(t, '("Opal_Muni_Sleeve", True, 4.0, 1), ("DIVZ SMA", False, 5.0, 1),',
                     '("Opal_Muni_Sleeve", True, 4.0, 1), ("%s", True, 3.0, 1), ("DIVZ SMA", False, 5.0, 1),' % MUNI)
    write_text(p, t)


def planted_mutant(ref_text):
    # substring match instead of the exact name, at both the key lookup and the registered-model test
    t = replace_once(ref_text, "return _CUSTOM_BY_NORM.get(_norm(model_name)) or canonical_key(model_name)",
                     "return next((v for k, v in _CUSTOM_BY_NORM.items() if k in _norm(model_name)), None) "
                     "or canonical_key(model_name)")
    t = replace_once(t, "is_registered = df.model_name.map(lambda n: _norm(n) in _CUSTOM_BY_NORM)",
                     "is_registered = df.model_name.map(lambda n: any(k in _norm(n) for k in _CUSTOM_BY_NORM))")
    return t


def mutant_lambda_only(root, src):
    """M1: only the data/mdpf crosswalk copy is edited; the Lambda copy keeps its base bytes."""
    shutil.copyfile(os.path.join(src, REL_XW_LAMBDA), os.path.join(root, REL_XW_LAMBDA))


def mutant_global_drops(root):
    """M2: the key is in both crosswalk copies but the dim file's GLOBAL_MODEL_KEYS filters it out."""
    p = os.path.join(root, REL_DIM)
    t = replace_once(read_text(p), "+ COTTONWOOD_CUSTOM_MODEL_KEYS)",
                     '+ tuple(k for k in COTTONWOOD_CUSTOM_MODEL_KEYS if k != "%s"))' % NEW_KEY)
    write_text(p, t)


def mutant_sleeve_key(root):
    """M3: the producer maps the vendor name to the sleeve's key."""
    p = producer_path(root)
    t = replace_once(read_text(p), '"%s": "%s",' % (MUNI, NEW_KEY), '"%s": "%s",' % (MUNI, SLEEVE_KEY))
    write_text(p, t)


def mutant_substring(root):
    """M4 (draft's planted mutant): substring match in the producer's custom lookup."""
    p = producer_path(root)
    write_text(p, planted_mutant(read_text(p)))


# ---------------------------------------------------------------- report and child runs
def report(word, arms, n):
    k = 0
    for label, ok, txt in arms:
        k += 1 if ok else 0
        print("  %s %s  [%s]" % ("PASS" if ok else "FAIL", label, txt))
    print("ROUND 11 CN-S-1 %s: %d of %d arms" % (word, k, n))
    return 0 if (k == n and len(arms) == n) else 1


def child(mode, root):
    """Runs this script in a fresh process: root None = the git toplevel, else R11_ROOT=root."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("R11_ROOT", None)
    if root is not None:
        env["R11_ROOT"] = root
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), mode], env=env, capture_output=True,
                           timeout=100)
    except subprocess.TimeoutExpired:
        return None, ""
    return p.returncode, p.stdout.decode("utf-8", "replace")


def arms_of(out):
    res = []
    for line in out.splitlines():
        if line.startswith("  PASS ") or line.startswith("  FAIL "):
            parts = line.split()
            res.append((parts[1], parts[0] == "PASS"))
    return res


def grade_child(mode, root, n):
    rc, out = child(mode, root)
    arms = arms_of(out)
    red = [lab for lab, ok in arms if not ok]
    return {"rc": rc, "n": len(arms), "red": red, "all_ok": rc == 0 and len(arms) == n and not red}


# ---------------------------------------------------------------- modes
def pure():
    refuse_aws()
    root = repo_root()
    sibling_paths(root)
    prod = producer_path(root)
    print("root: %s" % root)
    try:
        mod = load_file(prod, "r11_cn_s_1_producer")
    except Exception as e:
        print("ERROR: cannot import the producer %s: %s" % (prod, err(e)))
        return 2
    return report("PURE", grade(mod), N_ARMS)


def seams_mode():
    root = repo_root()
    print("root: %s" % root)
    return report("SEAMS", seam_arms(root), N_SEAMS)


def selftest():
    top = git_top()
    tmp = tempfile.mkdtemp(prefix="r11cns1_")
    try:
        base_p = grade_child("pure", None, N_ARMS)
        base_s = grade_child("seams", None, N_SEAMS)
        ref = os.path.join(tmp, "ref")
        build_scratch(ref, top)
        cell_edits(ref)
        ref_p = grade_child("pure", ref, N_ARMS)
        ref_s = grade_child("seams", ref, N_SEAMS)
        m1 = os.path.join(tmp, "m1")
        build_scratch(m1, top)
        cell_edits(m1)
        mutant_lambda_only(m1, top)
        m1_s = grade_child("seams", m1, N_SEAMS)
        m2 = os.path.join(tmp, "m2")
        build_scratch(m2, top)
        cell_edits(m2)
        mutant_global_drops(m2)
        m2_s = grade_child("seams", m2, N_SEAMS)
        m3 = os.path.join(tmp, "m3")
        build_scratch(m3, top)
        cell_edits(m3)
        mutant_sleeve_key(m3)
        m3_s = grade_child("seams", m3, N_SEAMS)
        m4 = os.path.join(tmp, "m4")
        build_scratch(m4, top)
        cell_edits(m4)
        mutant_substring(m4)
        m4_p = grade_child("pure", m4, N_ARMS)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("base (repo HEAD): pure rc=%s red %s; seams rc=%s red %s"
          % (base_p["rc"], base_p["red"], base_s["rc"], base_s["red"]))
    print("scratch reference (R11_ROOT): pure %d arms all_ok=%s; seams %d arms all_ok=%s"
          % (N_ARMS, ref_p["all_ok"], N_SEAMS, ref_s["all_ok"]))
    print("mutant M1 (one crosswalk copy only): seams red %s" % m1_s["red"])
    print("mutant M2 (key not in GLOBAL_MODEL_KEYS): seams red %s" % m2_s["red"])
    print("mutant M3 (vendor name to sleeve key): seams red %s" % m3_s["red"])
    print("mutant M4 (substring match): pure red %s" % m4_p["red"])
    checks = [
        ("base pure red exactly A1 A3", base_p["red"] == ["A1", "A3"]),
        ("base seams red exactly S2 S3 S4 (S1 green)", base_s["red"] == ["S2", "S3", "S4"]),
        ("scratch reference pure 6 of 6", ref_p["all_ok"]),
        ("scratch reference seams 4 of 4", ref_s["all_ok"]),
        ("M1 turns S1 and S2 red", {"S1", "S2"} <= set(m1_s["red"])),
        ("M2 turns S3 red", "S3" in m2_s["red"]),
        ("M3 turns S4 red", "S4" in m3_s["red"]),
        ("M4 turns A5 red", "A5" in m4_p["red"]),
    ]
    for name, ok in checks:
        print("  %s %s" % ("OK " if ok else "BAD", name))
    n_ok = sum(1 for _n, ok in checks if ok)
    good = n_ok == len(checks)
    print("CN-S-1 SELFTEST: %s (%d of %d checks)" % ("OK" if good else "NOT OK", n_ok, len(checks)))
    return 0 if good else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    modes = {"pure": pure, "seams": seams_mode, "selftest": selftest}
    if cmd not in modes:
        print(__doc__)
        sys.exit(2)
    sys.exit(modes[cmd]())
