#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-1 (Muni to Custom) -- DRAFT check, 2.0.0_SA_COO~D1, 2026-10-15. Not issued.

The cell: the vendor account `Opal_Muni_Income` (63,241,218.96 on a measured date) leaves income_non_model_residual and
enters by_model / model_aua under a NEW registered custom key whose display name is "Opal Municipal Bonds". The sleeve
(`Opal_Muni_Sleeve` -> opal_muni_sleeve) is unchanged, the new key is a SEPARATE key, and `Opal Hewitt Moderate Income`
stays in the residual. Source: data/assets/scripts/gold/build_cottonwood_mdpf_slice.py (CUSTOM_KEY, CUSTOM_DISPLAY_NAME).

Each arm runs the producer's own build_slice on small in-memory fixtures (no file written to the repo, no S3, no network):

  python r11_cn_s_1.py pure       six arms on the producer at the repo HEAD; the base reads red on A1 and A3 until the cell lands
  python r11_cn_s_1.py selftest   issuer only: base red on exactly A1 A3; a scratch reference (one CUSTOM_KEY row and its
                                  display name, in a temp copy) reads six green; one planted mutant (substring match, not an
                                  exact name) reddens A5. The repo's producer is never edited.

Target: <git toplevel>/data/assets/scripts/gold/build_cottonwood_mdpf_slice.py, or the repo root in env R11_REPO.
AWS guard: boto3.client and boto3.resource are refused while the arms run. rebalancer_schemas is given its own test seed
(OPAL_STRATEGY_CONFIG_SEED) through set_strategy_config, so the SMA name rule never reads the S3 config list.
Output: `ROUND 11 CN-S-1 PURE: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # importing the repo's producer must not write __pycache__ into the worktree
N_ARMS = 6
TOL = 0.005
DATES = ["2026-10-13", "2026-10-14"]
SLEEVE, SLEEVE_KEY, SLEEVE_DISPLAY, SLEEVE_DOLLARS = "Opal_Muni_Sleeve", "opal_muni_sleeve", "Opal Muni Sleeve", 12345678.90
MUNI, MUNI_DOLLARS = "Opal_Muni_Income", 63241218.96
HEWITT, HEWITT_DOLLARS = "Opal Hewitt Moderate Income", 1749334.30
MUNI2, MUNI2_DOLLARS = "Opal_Muni_Income_2", 1000000.00
PRIMARY, PRIMARY_DOLLARS = "Opal Short-Term", 5000000.00
NEW_DISPLAY = "Opal Municipal Bonds"
ROWS = [(SLEEVE, SLEEVE_DOLLARS, 4), (MUNI, MUNI_DOLLARS, 1), (HEWITT, HEWITT_DOLLARS, 1),
        (MUNI2, MUNI2_DOLLARS, 1), (PRIMARY, PRIMARY_DOLLARS, 3)]
RUN_ROWS = {
    "full": ROWS,
    "nomuni": [r for r in ROWS if r[0] != MUNI],
    "nohew": [r for r in ROWS if r[0] != HEWITT],
}
RUN_NAMES = ("full", "nomuni", "nohew")


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


# ---------------------------------------------------------------- the six arms
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
    """Returns [(label, ok, detail)] for the six arms, in order."""
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
def repo_root():
    if os.environ.get("R11_REPO"):
        return os.environ["R11_REPO"]
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def producer_path(repo):
    return os.path.join(repo, "data", "assets", "scripts", "gold", "build_cottonwood_mdpf_slice.py")


def sibling_paths(repo):
    sys.path[:0] = [os.path.join(repo, "data", "mdpf", "scripts", "gold"),
                    os.path.join(repo, "data", "assets", "scripts", "silver")]


def refuse_aws():
    import boto3

    def _refused(*_a, **_k):
        raise RuntimeError("AWS client refused inside the CN-s-1 fixture arms")
    boto3.client = _refused
    boto3.resource = _refused


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_text(text, name, tmp):
    path = os.path.join(tmp, name + ".py")
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))
    return load_file(path, name)


# ---------------------------------------------------------------- selftest texts (temp copies only)
def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise RuntimeError("expected one occurrence of %r, found %d" % (old[:70], n))
    return text.replace(old, new)


def scratch_reference(text):
    nl = "\r\n" if "\r\n" in text else "\n"
    t = replace_once(text, '"Opal_Muni_Sleeve": "opal_muni_sleeve",',
                     '"Opal_Muni_Sleeve": "opal_muni_sleeve",' + nl + '    "Opal_Muni_Income": "opal_municipal_bonds",')
    t = replace_once(t, '"opal_muni_sleeve": "Opal Muni Sleeve",',
                     '"opal_muni_sleeve": "Opal Muni Sleeve",' + nl + '    "opal_municipal_bonds": "Opal Municipal Bonds",')
    return t


def planted_mutant(ref_text):
    # substring match instead of the exact name, at both the key lookup and the registered-model test
    t = replace_once(ref_text, "return _CUSTOM_BY_NORM.get(_norm(model_name)) or canonical_key(model_name)",
                     "return next((v for k, v in _CUSTOM_BY_NORM.items() if k in _norm(model_name)), None) "
                     "or canonical_key(model_name)")
    t = replace_once(t, "is_registered = df.model_name.map(lambda n: _norm(n) in _CUSTOM_BY_NORM)",
                     "is_registered = df.model_name.map(lambda n: any(k in _norm(n) for k in _CUSTOM_BY_NORM))")
    return t


def show(name, arms):
    print("%s: %s" % (name, " ".join("%s=%s" % (lab.split()[0], "ok" if ok else "RED") for lab, ok, _t in arms)))


# ---------------------------------------------------------------- modes
def pure():
    refuse_aws()
    repo = repo_root()
    sibling_paths(repo)
    prod = producer_path(repo)
    try:
        mod = load_file(prod, "r11_cn_s_1_producer")
    except Exception as e:
        print("ERROR: cannot import the producer %s: %s: %s" % (prod, type(e).__name__, str(e)[:200]))
        return 2
    arms = grade(mod)
    k = 0
    for label, ok, txt in arms:
        k += 1 if ok else 0
        print("  %s %s  [%s]" % ("PASS" if ok else "FAIL", label, txt))
    print("ROUND 11 CN-S-1 PURE: %d of %d arms" % (k, N_ARMS))
    return 0 if k == N_ARMS else 1


def selftest():
    refuse_aws()
    repo = repo_root()
    sibling_paths(repo)
    prod = producer_path(repo)
    with open(prod, "rb") as fh:
        text = fh.read().decode("utf-8")
    tmp = tempfile.mkdtemp(prefix="r11cns1_")
    try:
        base = grade(load_file(prod, "r11_cn_s_1_base"))
        try:
            ref_text = scratch_reference(text)
            mut_text = planted_mutant(ref_text)
        except RuntimeError as e:
            print("SELFTEST: cannot build the scratch reference or the mutant: %s" % e)
            return 2
        ref = grade(load_text(ref_text, "r11_cn_s_1_ref", tmp))
        mut = grade(load_text(mut_text, "r11_cn_s_1_mut", tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    show("base (repo HEAD)", base)
    show("scratch reference", ref)
    show("planted mutant", mut)
    base_red = sorted(lab.split()[0] for lab, ok, _t in base if not ok)
    ref_ok = all(ok for _l, ok, _t in ref)
    mut_red = sorted(lab.split()[0] for lab, ok, _t in mut if not ok)
    good = base_red == ["A1", "A3"] and ref_ok and "A5" in mut_red
    print("CN-S-1 SELFTEST: %s (base red %s; reference green %s; mutant red %s)"
          % ("OK" if good else "NOT OK", base_red, ref_ok, mut_red))
    return 0 if good else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"pure": pure, "selftest": selftest}.get(cmd, lambda: print(__doc__) or 2)())
