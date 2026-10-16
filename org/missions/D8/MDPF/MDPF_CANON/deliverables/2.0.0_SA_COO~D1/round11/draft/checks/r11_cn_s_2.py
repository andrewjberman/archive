#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-2 (Cottonwood carried model legs) -- DRAFT check, 2.0.0_SA_COO~D1, 2026-10-15. Not issued.

Target: data/assets/scripts/gold/build_cottonwood_mdpf_slice.py, function compose_cottonwood_leg(daily, oneoff), run on small
in-memory fixtures (no S3, no network). The carry rule the cell asks for: a date with a measured total and NO model-leg
measurement, AFTER a measured leg, is emitted carried -- model_aua equals the last measured leg (never a chained value),
partner_custody_total stays the measured total, non_model_aua is the residual (total - carried leg), and the date is listed
in carried_dates. Nothing is carried across a date with no total, and nothing is carried before the first measured leg.

  python r11_cn_s_2.py pure       six arms (B0-B5) against the producer at HEAD, or the file named by env R11_PRODUCER
  python r11_cn_s_2.py selftest   issuer only: base red on B1 B2 B5 and green on B0 B3 B4; a SCRATCH carry wrapper (written to a
                                  temp dir, the repo producer untouched) green on all six; one planted mutant (carries across a
                                  no-total date) reddens B4

Output: `ROUND 11 CN-S-2 PURE: k of n arms`, exit 0 only when k == n.  ASCII only.

Premise note (read at HEAD 2026-10-15): compose_cottonwood_leg emits no carried_dates today. The Global carry is
compute_trend_groups in data/mdpf/scripts/gold/mdpf_gold_consolidator.py (TREND_CARRIED_KEY = "carried_dates"), and
apply_global_trend_groups writes [] for every non-Global scope, which is why the served Cottonwood carried_dates reads EMPTY.
This check tests the producer's own composed output, the emission the cell names; the locus is an issuer decision at the cut.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

N_ARMS = 6
TOL = 0.01
REL = os.path.join("data", "assets", "scripts", "gold", "build_cottonwood_mdpf_slice.py")
ONEOFF_DATE = "2026-07-10"          # an absent one-off row before every fixture's first measured date: nothing is spliced
BASE_RED = {"B1", "B2", "B5"}
BASE_GREEN = {"B0", "B3", "B4"}

WRAPPER = r'''
"""SCRATCH carry wrapper for the CN-s-2 selftest. Calls the producer's compose, then applies the carry rule. Never the repo file."""
import importlib.util


def _load(path):
    spec = importlib.util.spec_from_file_location("cn_s_2_scratch_producer", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make(producer_path, mutant=None):
    base = _load(producer_path).compose_cottonwood_leg

    def compose(daily, oneoff):
        art = base(daily, oneoff)
        dates = list(art["dates"])
        model = list(art["model_aua"])
        nm = list(art["non_model_aua"])
        tot = art["partner_custody_total"]
        carried, last = [], None
        for i, d in enumerate(dates):
            if model[i] is not None:
                last = model[i]
                continue
            if last is None:
                continue
            if tot[i] is None and mutant != "across_no_total":
                continue
            model[i] = last
            carried.append(d)
            if tot[i] is not None:
                nm[i] = round(tot[i] - last, 2)
        out = dict(art)
        out.update({"model_aua": model, "non_model_aua": nm, "carried_dates": sorted(carried)})
        return out

    return compose
'''


def close(a, b):
    return a is not None and b is not None and abs(float(a) - float(b)) <= TOL


def fixture(rows, covered):
    """rows: (date, total, model_aua, non_model_aua), None where absent. covered: the dates that carry a measured model leg."""
    return {
        "dates": [r[0] for r in rows],
        "meta": {"covered_dates": list(covered)},
        "model_aua": [r[2] for r in rows],
        "non_model_aua": [r[3] for r in rows],
        "partner_custody_total": [r[1] for r in rows],
        "by_model": {},
        "cohort_provenance": [],
    }


def oneoff():
    return {"dates": [ONEOFF_DATE], "model_aua": [None],
            "cohort_provenance": [{"date": ONEOFF_DATE, "model": "absent"}], "by_model": {}}


def run_compose(compose, rows, covered):
    try:
        return compose(fixture(rows, covered), oneoff()), ""
    except (Exception, SystemExit) as e:  # a producer refusal is an arm FAIL, never a crash
        return None, "raised %s: %s" % (type(e).__name__, str(e)[:120])


def arm_b0(compose):
    rows = [("2026-07-20", 100.0, 50.0, 50.0), ("2026-07-21", 102.0, 51.0, 51.0)]
    art, err = run_compose(compose, rows, ["2026-07-20", "2026-07-21"])
    if art is None:
        return False, err
    m, t, carried = art["model_aua"], art["partner_custody_total"], list(art.get("carried_dates") or [])
    ok = close(m[0], 50.0) and close(m[1], 51.0) and close(t[0], 100.0) and close(t[1], 102.0) and not carried
    return ok, "model %s total %s carried %s" % (m, t, carried)


def arm_b1(compose):
    rows = [("2026-07-20", 100.0, 50.0, 50.0), ("2026-07-21", 105.0, None, None)]
    art, err = run_compose(compose, rows, ["2026-07-20"])
    if art is None:
        return False, err
    m, t, carried = art["model_aua"], art["partner_custody_total"], list(art.get("carried_dates") or [])
    ok = close(m[0], 50.0) and close(m[1], 50.0) and close(t[1], 105.0) and "2026-07-21" in carried
    return ok, "D2 model %s total %s carried %s" % (m[1], t[1], carried)


def arm_b2(compose):
    rows = [("2026-07-20", 100.0, 50.0, 50.0), ("2026-07-21", 105.0, None, None), ("2026-07-22", 108.0, None, None)]
    art, err = run_compose(compose, rows, ["2026-07-20"])
    if art is None:
        return False, err
    m, t, carried = art["model_aua"], art["partner_custody_total"], list(art.get("carried_dates") or [])
    ok = (close(m[1], 50.0) and close(m[2], 50.0) and close(t[1], 105.0) and close(t[2], 108.0)
          and "2026-07-21" in carried and "2026-07-22" in carried)
    return ok, "model %s total %s carried %s" % (m, t, carried)


def arm_b3(compose):
    rows = [("2026-07-17", 90.0, None, None), ("2026-07-20", 100.0, 50.0, 50.0)]
    art, err = run_compose(compose, rows, ["2026-07-20"])
    if art is None:
        return False, err
    m, t, carried = art["model_aua"], art["partner_custody_total"], list(art.get("carried_dates") or [])
    ok = m[0] is None and "2026-07-17" not in carried and close(t[0], 90.0) and close(m[1], 50.0)
    return ok, "pre-measured model %s total %s carried %s" % (m[0], t[0], carried)


def arm_b4(compose):
    rows = [("2026-07-20", 100.0, 50.0, 50.0), ("2026-07-21", None, None, None), ("2026-07-22", 105.0, None, None)]
    art, err = run_compose(compose, rows, ["2026-07-20"])
    if art is None:
        return False, err
    m, t, carried = art["model_aua"], art["partner_custody_total"], list(art.get("carried_dates") or [])
    ok = m[1] is None and t[1] is None and "2026-07-21" not in carried
    return ok, "no-total date model %s carried %s" % (m[1], carried)


def arm_b5(compose):
    rows = [("2026-07-20", 100.0, 50.0, 50.0), ("2026-07-21", 105.0, None, None),
            ("2026-07-22", 108.0, None, None), ("2026-07-23", None, None, None)]
    art, err = run_compose(compose, rows, ["2026-07-20"])
    if art is None:
        return False, err
    m, nm, t = art["model_aua"], art["non_model_aua"], art["partner_custody_total"]
    checked, bad = 0, []
    for i, d in enumerate(art["dates"]):
        if t[i] is None:
            continue
        checked += 1
        if m[i] is None or nm[i] is None or abs(float(m[i]) + float(nm[i]) - float(t[i])) > TOL:
            bad.append(d)
    ok = checked > 0 and not bad
    return ok, "dates with total %d, failing %s" % (checked, bad)


ARMS = (
    ("B0", "control: a measured date is emitted unchanged and not carried", arm_b0),
    ("B1", "a no-leg date after a measured leg carries the leg, keeps its total, is listed", arm_b1),
    ("B2", "two consecutive no-leg dates carry the same last measured leg, both listed", arm_b2),
    ("B3", "control: a no-leg date before any measured leg is not invented", arm_b3),
    ("B4", "control: a no-total date is never carried and never listed", arm_b4),
    ("B5", "model_aua + non_model = total on every dated row, carried ones included", arm_b5),
)


def grade(compose):
    out = []
    for aid, label, fn in ARMS:
        try:
            ok, detail = fn(compose)
        except (Exception, SystemExit) as e:
            ok, detail = False, "arm raised %s: %s" % (type(e).__name__, str(e)[:120])
        out.append((aid, label, ok, detail))
    return out


def show(results):
    k = 0
    for aid, label, ok, detail in results:
        k += 1 if ok else 0
        print("  %s %s %s  [%s]" % ("PASS" if ok else "FAIL", aid, label, detail[:220]))
    return k


def producer_path():
    if os.environ.get("R11_PRODUCER"):
        return os.environ["R11_PRODUCER"]
    here = os.path.dirname(os.path.abspath(__file__))
    top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=here).strip()
    return os.path.join(top, REL)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pure():
    path = producer_path()
    try:
        compose = load(path, "r11_cn_s_2_producer").compose_cottonwood_leg
    except Exception as e:  # noqa: BLE001 -- a blocked import is the recorded output
        print("BLOCKED: cannot import %s: %s: %s" % (path, type(e).__name__, str(e)[:200]))
        print("ROUND 11 CN-S-2 PURE: 0 of %d arms" % N_ARMS)
        return 1
    print("TARGET: %s  compose_cottonwood_leg" % path)
    k = show(grade(compose))
    print("ROUND 11 CN-S-2 PURE: %d of %d arms" % (k, N_ARMS))
    return 0 if k == N_ARMS else 1


def selftest():
    path = producer_path()
    tmp = tempfile.mkdtemp(prefix="r11cns2_")
    try:
        wpath = os.path.join(tmp, "cn_s_2_scratch_wrapper.py")
        with open(wpath, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(WRAPPER)
        wrap = load(wpath, "cn_s_2_scratch_wrapper")
        base = grade(load(path, "r11_cn_s_2_producer").compose_cottonwood_leg)
        ref = grade(wrap.make(path))
        mut = grade(wrap.make(path, "across_no_total"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("[1] BASE (producer at HEAD, unmodified):")
    show(base)
    print("[2] SCRATCH REFERENCE (carry wrapper in a temp dir over the producer):")
    show(ref)
    print("[3] PLANTED MUTANT (carries across a no-total date):")
    show(mut)
    base_red = {a for a, _, ok, _ in base if not ok}
    base_green = {a for a, _, ok, _ in base if ok}
    ref_all = all(ok for _, _, ok, _ in ref)
    mut_red = {a for a, _, ok, _ in mut if not ok}
    good = base_red == BASE_RED and base_green == BASE_GREEN and ref_all and "B4" in mut_red
    print("base red %s; base green %s; reference all green %s; mutant red %s"
          % (sorted(base_red), sorted(base_green), ref_all, sorted(mut_red)))
    print("CN-S-2 SELFTEST: %s" % ("OK" if good else "NOT OK"))
    return 0 if good else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd not in ("pure", "selftest"):
        print(__doc__)
        sys.exit(2)
    sys.exit(pure() if cmd == "pure" else selftest())
