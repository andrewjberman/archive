#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-n-1 -- the refusal arm DRIVEN (D1-W16-S1): the issuer's instrument.

One QA run of the gold consolidator's build_all (dry_run=True, so no S3 write) in which the three firm
artifacts built IN MEMORY by that very run are edited so the Global fold's pool is held by ONE firm on the
as-of date. The guard must refuse Global WHOLE, leave the siblings alone, log the refusal, and the served
prefix must be byte-identical before and after (zero writes). QA, never production evidence.

Read-only against AWS: every botocore call whose operation name is not Get/Head/List/Describe/Lookup/Simulate is
BLOCKED by the instrument itself (and recorded), so a dry run that tried to write would show it.

  python r7_cn_n_1.py guard [--date YYYY-MM-DD]      AC3. Offline over the SERVED unfolded objects of a date (default 2026-10-09):
        control (unplanted) -> the guard folds; planted single-firm pool -> the guard refuses Global whole through the
        production guard call path; siblings are the same objects; the inputs are not mutated. GETs only.
  python r7_cn_n_1.py plan [--date ...]              what the plant would do on the served objects of a date; no run.
  python r7_cn_n_1.py drive --run-dir DIR            THE QA RUN (the worker runs this ONCE; minutes; see the order). Writes
        DIR/{served_before.json, served_after.json, qa_run.json, qa_run.log, s3_ops.json}. The local A4 bodies go to a temp dir
        that is listed by NAME in qa_run.json (a4_files) and deleted: no served-level body is kept or committed.
  python r7_cn_n_1.py grade --run-dir DIR            AC1. Arms N1..N6 over the run record.
  python r7_cn_n_1.py served --run-dir DIR           AC2. Arms S1..S4: zero served writes, from the snapshots, the write-op
        log, and a LIVE head of the prior Global object by key and recorded VersionId.
  python r7_cn_n_1.py selftest                       offline: synthetic run record passes; four planted defects turn it red.

Prints `ROUND 7 CN-N-1 <GUARD|GRADE|SERVED>: k of n arms`; exit 0 only when every arm passes. Never prints an account id or a level.
"""
from __future__ import annotations

import contextlib
import copy
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
TYPE_TS = "aggregate-aua-timeseries"
FIRMS = ("49financial", "inflection", "cottonwood")
SCOPES = ("global",) + FIRMS
SERVED_PREFIXES = (PREFIX + "/", "gold/mdpf_revamp/")
REFUSE = "GLOBAL MIN-FIRMS FOLD REFUSED:"
READ_PREFIXES = ("Get", "Head", "List", "Describe", "Lookup", "Simulate")
DEFAULT_GUARD_DATE = "2026-10-09"   # the last unfolded dated objects (the round-6 selftest world)


# ------------------------------------------------------------------------------------------------ plumbing
def _root() -> str:
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _gc():
    root = os.environ.get("R7_ROOT") or _root()
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    if root not in sys.path:
        sys.path.insert(0, root)
    return importlib.import_module("mdpf_gold_consolidator")


def _s3():
    import boto3
    from botocore.config import Config
    return boto3.client("s3", region_name="us-east-1",
                        config=Config(read_timeout=30, connect_timeout=10, retries={"max_attempts": 2}))


def _arg(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def _report(arms, label):
    ok = sum(1 for a in arms if a)
    print("ROUND 7 CN-N-1 %s: %d of %d arms" % (label, ok, len(arms)))
    return 0 if ok == len(arms) else 1


def _idx(a):
    return {d: j for j, d in enumerate(a.get("dates") or [])}


def _val(entry, i):
    arr = (entry or {}).get("model_value") or []
    return arr[i] if i is not None and 0 <= i < len(arr) else None


# ------------------------------------------------------------------------------------------------ the plant
def plant_single_firm_pool(firm_arts: dict, fill=None) -> dict:
    """Edit the firm artifacts IN PLACE (the caller owns copies or in-memory builds) so that on the last date the
    model-class lines held by fewer than two firms (the fold set) are held by exactly one firm. Returns the record.
    Only `model_value` at the last-date index of other firms' fold lines is set to `fill`; nothing else moves. The guard arms
    use `fill=None`. The QA drive uses `fill=0.0`: the Global builder re-sets every frontier `account_count` from its own
    count source after the plant (the ROW11 frontier-stamp line of the log), so a None value beside that count fails the
    cross-axis presence gate (v) before the min-firms guard runs (D1-W21-S2, S5); a ZERO value is present, agrees with the
    count, and is not held (held means model_value > 0)."""
    arts = {f: a for f, a in firm_arts.items() if a and a.get("dates")}
    last_date = max(a["dates"][-1] for a in arts.values())
    ix = {f: _idx(a) for f, a in arts.items()}
    keys = sorted({k for a in arts.values() for k, e in (a.get("by_model") or {}).items()
                   if (e or {}).get("cohort_class") == "model"})

    def held(k):
        return [f for f in arts if (_val((arts[f].get("by_model") or {}).get(k), ix[f].get(last_date)) or 0) > 0]

    fold = [k for k in keys if 0 < len(held(k)) < 2]
    if not fold:
        return {"planted": False, "as_of": last_date, "reason": "no model line is held by exactly one firm on the as-of"}
    per_firm = {f: [k for k in fold if f in held(k)] for f in arts}
    keep = max(per_firm, key=lambda f: len(per_firm[f]))
    blanked = []
    for f in arts:
        if f == keep:
            continue
        for k in per_firm[f]:
            arr = arts[f]["by_model"][k]["model_value"]
            arr[ix[f][last_date]] = fill
            blanked.append((f, k))
    # every fold line is now held by `keep` alone or by nobody
    return {"planted": True, "as_of": last_date, "kept_firm": keep, "blanked_firms": sorted({f for f, _ in blanked}),
            "fold_lines": len(fold), "lines_blanked": len(blanked)}


# ------------------------------------------------------------------------------------------------ guard (AC3)
def _served_world(s3, date):
    arts = {}
    for sc in SCOPES:
        key = "%s/%s/%s/%s.json" % (PREFIX, sc, TYPE_TS, date)
        arts[sc] = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
    return arts


def _prod_isolated(errors: dict):
    """The same behaviour as build_all's `_isolated` closure (mdpf_gold_consolidator.py, build_all): run, and on any
    BaseException except KeyboardInterrupt record f'{type}: {msg}' under errors[scope] and return None."""
    def _isolated(scope, fn):
        try:
            return fn()
        except BaseException as e:  # noqa: BLE001
            if isinstance(e, KeyboardInterrupt):
                raise
            errors[scope] = {"error": "%s: %s" % (type(e).__name__, e)}
            return None
    return _isolated


def cmd_guard(argv):
    date = _arg(argv, "--date", DEFAULT_GUARD_DATE)
    gc = _gc()
    s3 = _s3()
    arts = _served_world(s3, date)
    arms = []

    def arm(name, ok, detail):
        arms.append(bool(ok))
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))

    print("  guard world: served unfolded objects of %s, scopes %s" % (date, ",".join(SCOPES)))
    # G1 control: unplanted -> the fold applies
    err0 = {}
    out0, rep0 = gc.guard_global_min_firms_fold(copy.deepcopy(arts), _prod_isolated(err0))
    arm("G1", out0.get("global") is not None and (rep0 or {}).get("applied") is True and not err0,
        "control (unplanted): the guard folds Global (as_of %s, fold lines %s, other_models emitted as-of %s)"
        % ((rep0 or {}).get("as_of"), len((rep0 or {}).get("fold_keys") or []), (rep0 or {}).get("other_models_emitted_as_of")))
    # G2 planted: refused whole through the production guard call path
    planted = copy.deepcopy(arts)
    before = copy.deepcopy(planted)
    rec = plant_single_firm_pool({f: planted[f] for f in FIRMS})
    err1 = {}
    out1, rep1 = gc.guard_global_min_firms_fold(planted, _prod_isolated(err1))
    msg = (err1.get("global") or {}).get("error", "")
    arm("G2", rec.get("planted") and out1.get("global") is None and rep1 is None and REFUSE in msg
        and ("held by 1 firm(s)" in msg) and (rec.get("as_of") or "?") in msg,
        "planted pool (%s lines blanked on %s firm(s), kept %s, as-of %s): Global refused whole; error text names the as-of and '1 firm(s)'"
        % (rec.get("lines_blanked"), len(rec.get("blanked_firms") or []), rec.get("kept_firm"), rec.get("as_of")))
    # G3 siblings untouched
    same = all(out1.get(f) is planted.get(f) for f in FIRMS)
    arm("G3", same and list(err1) == ["global"], "siblings %s are the same objects after the refusal; errors recorded for %s only"
        % (",".join(FIRMS), list(err1)))
    # G4 the plant is the only difference between control and planted inputs
    diffs = 0
    for f in FIRMS:
        for k, e in (planted[f].get("by_model") or {}).items():
            e0 = arts[f]["by_model"][k]
            if e.get("model_value") != e0.get("model_value"):
                diffs += 1
    other = all(planted[s] == arts[s] for s in ("global",)) and all(
        {k: v for k, v in planted[f].items() if k != "by_model"} == {k: v for k, v in arts[f].items() if k != "by_model"}
        for f in FIRMS)
    arm("G4", diffs == rec.get("lines_blanked") and other,
        "the plant moved model_value on %d line(s) (== %s blanked) and nothing else (global and every non-by_model field equal)"
        % (diffs, rec.get("lines_blanked")))
    # G5 no state leaked into the control through the planted call (arts of the control are still unplanted)
    arm("G5", before["global"] == planted["global"], "the Global input object itself was not edited by the refusal path")
    return _report(arms, "GUARD")


def cmd_plan(argv):
    date = _arg(argv, "--date", DEFAULT_GUARD_DATE)
    arts = _served_world(_s3(), date)
    rec = plant_single_firm_pool({f: copy.deepcopy(arts[f]) for f in FIRMS})
    print("  plant on the served objects of %s: %s" % (date, json.dumps(rec, sort_keys=True)))
    s3 = _s3()
    snap = snapshot(s3)
    print("  served snapshot now: %d object-version(s) over %s" % (len(snap), ", ".join(SERVED_PREFIXES)))
    return 0 if rec.get("planted") else 1


# ------------------------------------------------------------------------------------------------ the served snapshot
def snapshot(s3) -> list:
    """[[Key, VersionId, IsLatest, ETag]] sorted, over SERVED_PREFIXES, every version (list_object_versions)."""
    out = []
    for pre in SERVED_PREFIXES:
        tok = {}
        while True:
            r = s3.list_object_versions(Bucket=BUCKET, Prefix=pre, **tok)
            for v in r.get("Versions", []) + r.get("DeleteMarkers", []):
                out.append([v["Key"], v.get("VersionId"), bool(v.get("IsLatest")), v.get("ETag")])
            if not r.get("IsTruncated"):
                break
            tok = {"KeyMarker": r.get("NextKeyMarker"), "VersionIdMarker": r.get("NextVersionIdMarker")}
    return sorted(out, key=lambda x: (x[0], str(x[1])))


def _prior_global_ts(s3, snap) -> dict:
    ks = sorted({k for k, _v, latest, _e in snap if latest and k.startswith("%s/global/%s/" % (PREFIX, TYPE_TS)) and k.endswith(".json")})
    key = ks[-1]
    vid = [v for k, v, latest, _e in snap if k == key and latest][0]
    return {"key": key, "version_id": vid}


# ------------------------------------------------------------------------------------------------ write blocker
class _Ops:
    def __init__(self):
        self.calls = {}
        self.blocked = []


def install_op_guard(ops: _Ops):
    import botocore.client as bc
    orig = bc.BaseClient._make_api_call

    def guarded(self, operation_name, api_params):
        svc = self.meta.service_model.service_name
        ops.calls["%s.%s" % (svc, operation_name)] = ops.calls.get("%s.%s" % (svc, operation_name), 0) + 1
        if not operation_name.startswith(READ_PREFIXES):
            ops.blocked.append("%s.%s" % (svc, operation_name))
            raise RuntimeError("QA INSTRUMENT BLOCKED A NON-READ CALL: %s.%s" % (svc, operation_name))
        return orig(self, operation_name, api_params)
    bc.BaseClient._make_api_call = guarded
    return lambda: setattr(bc.BaseClient, "_make_api_call", orig)


class _Tee(io.TextIOBase):
    def __init__(self, *sinks):
        self.sinks = sinks

    def write(self, s):
        for k in self.sinks:
            k.write(s)
        return len(s)

    def flush(self):
        for k in self.sinks:
            k.flush()


# ------------------------------------------------------------------------------------------------ the QA run (drive)
def cmd_drive(argv):
    run_dir = _arg(argv, "--run-dir")
    if not run_dir:
        print("usage: drive --run-dir DIR")
        return 2
    os.makedirs(run_dir, exist_ok=True)
    gc = _gc()
    s3 = _s3()
    t0 = time.time()
    before = snapshot(s3)
    prior = _prior_global_ts(s3, before)
    with open(os.path.join(run_dir, "served_before.json"), "w", encoding="utf-8") as fh:
        json.dump({"objects": before, "prior_global_ts": prior}, fh)
    print("  served before: %d object-version(s); prior Global ts %s VersionId=%s" % (len(before), prior["key"], prior["version_id"]))
    ops = _Ops()
    restore = install_op_guard(ops)
    plant_rec = {}
    real_bg = gc.spine.build_global_artifact

    def planted_build_global(a49, ainf, acot, *a, **k):
        # the plant edits COPIES handed to the Global builder only: the firm artifacts the rest of build_all reads
        # (category-views peers, firm scopes) stay as built, so no other gate sees a planted total (D1-W21-S1)
        c49, cinf, ccot = copy.deepcopy(a49), copy.deepcopy(ainf), copy.deepcopy(acot)
        rec = plant_single_firm_pool({"49financial": c49, "inflection": cinf, "cottonwood": ccot}, fill=0.0)
        plant_rec.update(rec)
        print("  QA PLANT (in-memory copies for the Global builder of THIS run only): %s" % json.dumps(rec, sort_keys=True))
        return real_bg(c49, cinf, ccot, *a, **k)
    gc.spine.build_global_artifact = planted_build_global
    log_path = os.path.join(run_dir, "qa_run.log")
    a4_tmp = tempfile.mkdtemp(prefix="cn_n_1_a4_")
    manifest = {}
    with open(log_path, "w", encoding="utf-8") as lf:
        tee_o, tee_e = _Tee(sys.stdout, lf), _Tee(sys.stderr, lf)
        try:
            with contextlib.redirect_stdout(tee_o), contextlib.redirect_stderr(tee_e):
                manifest = gc.build_all({"kind": "qa-local(manual)", "detail": {"cell": "CN-n-1"}}, dry_run=True,
                                        out_dir=a4_tmp)
        except BaseException as e:  # noqa: BLE001
            lf.write("\nQA DRIVE: build_all raised %s: %s\n" % (type(e).__name__, e))
            manifest = {"run": {"status": "RAISED"}, "errors": {"_drive": {"error": "%s: %s" % (type(e).__name__, e)}}, "writes": []}  # the op guard, not this record, counts writes (D1-W21-S3)
    gc.spine.build_global_artifact = real_bg
    restore()
    a4_files = sorted(os.path.relpath(os.path.join(r, f), a4_tmp).replace(os.sep, "/")
                      for r, _d, fs in os.walk(a4_tmp) for f in fs)
    shutil.rmtree(a4_tmp, ignore_errors=True)
    after = snapshot(s3)
    with open(os.path.join(run_dir, "served_after.json"), "w", encoding="utf-8") as fh:
        json.dump({"objects": after, "prior_global_ts": _prior_global_ts(s3, after)}, fh)
    with open(os.path.join(run_dir, "s3_ops.json"), "w", encoding="utf-8") as fh:
        json.dump({"calls": ops.calls, "blocked": ops.blocked}, fh, sort_keys=True)
    rec = {"started": t0, "elapsed_s": round(time.time() - t0, 1), "dry_run": True, "plant": plant_rec,
           "trigger": (manifest.get("run") or {}).get("trigger"), "status": (manifest.get("run") or {}).get("status"),
           "a4_objects_built": (manifest.get("run") or {}).get("a4_objects_built"),
           "a4_expected": (manifest.get("run") or {}).get("a4_expected"),
           "manifest_errors": {k: (v or {}).get("error") for k, v in (manifest.get("errors") or {}).items()},
           "manifest_writes": manifest.get("writes"), "a4_files": a4_files}
    with open(os.path.join(run_dir, "qa_run.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True, default=str)
    print("  QA run done in %ss: status=%s errors=%s a4_objects_built=%s writes=%s blocked-calls=%d"
          % (rec["elapsed_s"], rec["status"], list(rec["manifest_errors"]), rec["a4_objects_built"], len(rec["manifest_writes"] or []), len(ops.blocked)))
    return 0


# ------------------------------------------------------------------------------------------------ grade (AC1) and served (AC2)
def _load(run_dir, name):
    p = os.path.join(run_dir, name)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def _text(run_dir, name):
    p = os.path.join(run_dir, name)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def cmd_grade(argv):
    run_dir = _arg(argv, "--run-dir")
    if not run_dir:
        print("usage: grade --run-dir DIR")
        return 2
    rec = _load(run_dir, "qa_run.json")
    log = _text(run_dir, "qa_run.log")
    arms = []

    def arm(name, ok, detail):
        arms.append(bool(ok))
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))

    if rec is None or log is None:
        print("  no run record at %s (qa_run.json / qa_run.log absent): the QA run has not been driven" % run_dir)
        for n in ("N1", "N2", "N3", "N4", "N5", "N6"):
            arm(n, False, "no run record")
        return _report(arms, "GRADE")
    plant = rec.get("plant") or {}
    errs = rec.get("manifest_errors") or {}
    gerr = errs.get("global") or ""
    arm("N1", plant.get("planted") is True and plant.get("kept_firm") and plant.get("as_of"),
        "single-firm pool planted in the run's own in-memory builds (kept firm %s, %s line(s) blanked on %s, as-of %s)"
        % (plant.get("kept_firm"), plant.get("lines_blanked"), plant.get("blanked_firms"), plant.get("as_of")))
    arm("N2", REFUSE in gerr and "held by 1 firm(s)" in gerr and str(plant.get("as_of")) in gerr,
        "Global refused by the min-firms guard: manifest errors.global names the refusal, the as-of and '1 firm(s)'")
    sib = [s for s in FIRMS if s in errs]
    arm("N3", not sib, "refused alone: no error recorded for the siblings (%s); errors = %s" % (",".join(FIRMS), sorted(errs)))
    n_built = rec.get("a4_objects_built")
    files = rec.get("a4_files")
    gl = [f for f in (files or []) if "global" in f.lower().replace("\\", "/").split("/")[-3:]
          or f.lower().rsplit("/", 1)[-1].startswith("global")]
    arm("N4", files is not None and len(files) > 0 and not gl and isinstance(n_built, int) and n_built < (rec.get("a4_expected") or 16),
        "whole: %s local A4 file(s) built, %d of them a Global body, and a4_objects_built %s is below a4_expected %s"
        % (len(files) if files is not None else "?", len(gl), n_built, rec.get("a4_expected")))
    arm("N5", (REFUSE in log) and ("global" in log.lower()),
        "the refusal is logged: qa_run.log carries the refusal prefix on a Global line")
    arm("N6", rec.get("dry_run") is True and str((rec.get("trigger") or {}).get("kind", "")).startswith("qa-local")
        and not (rec.get("manifest_writes") or []),
        "dry run: trigger kind %s, manifest writes %d" % ((rec.get("trigger") or {}).get("kind"), len(rec.get("manifest_writes") or [])))
    return _report(arms, "GRADE")


def cmd_served(argv, s3=None):
    run_dir = _arg(argv, "--run-dir")
    if not run_dir:
        print("usage: served --run-dir DIR")
        return 2
    b = _load(run_dir, "served_before.json")
    a = _load(run_dir, "served_after.json")
    ops = _load(run_dir, "s3_ops.json")
    arms = []

    def arm(name, ok, detail):
        arms.append(bool(ok))
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))

    if b is None or a is None or ops is None:
        print("  no run record at %s (served_before/served_after/s3_ops absent): the QA run has not been driven" % run_dir)
        for n in ("S1", "S2", "S3", "S4"):
            arm(n, False, "no run record")
        return _report(arms, "SERVED")
    ob, oa = b["objects"], a["objects"]
    arm("S1", ob == oa and len(ob) > 0,
        "served prefixes %s: %d object-version(s) before, %d after, identical (key, VersionId, IsLatest, ETag)" % (", ".join(SERVED_PREFIXES), len(ob), len(oa)))
    pg = b["prior_global_ts"]
    same_rec = pg == a["prior_global_ts"]
    arm("S2", same_rec, "prior Global ts %s: recorded VersionId before == after (%s)" % (pg["key"].rsplit("/", 1)[-1], pg["version_id"]))
    s3 = s3 or _s3()
    live = s3.head_object(Bucket=BUCKET, Key=pg["key"]).get("VersionId")
    arm("S3", live == pg["version_id"], "LIVE head of the prior Global ts by key: current VersionId %s the recorded one" % ("equals" if live == pg["version_id"] else "DIFFERS from"))
    writes = [c for c in (ops.get("calls") or {}) if not c.split(".", 1)[1].startswith(READ_PREFIXES)]
    arm("S4", not ops.get("blocked") and not writes,
        "the run made %d distinct botocore call kind(s), none a write (blocked %d, write kinds %d)" % (len(ops.get("calls") or {}), len(ops.get("blocked") or []), len(writes)))
    return _report(arms, "SERVED")


# ------------------------------------------------------------------------------------------------ selftest
class _FakeS3:
    def __init__(self, vid):
        self.vid = vid

    def head_object(self, Bucket, Key):
        return {"VersionId": self.vid}


def _synthetic(d, *, refusal=True, differ=False, write=False, logged=True, gl_body=False):
    msg = "%s the as-of date 2026-10-13 is held by 1 firm(s) on the fold line, and the fold line needs at least 2 on the as-of." % REFUSE
    errs = {"global": "SystemExit: " + msg} if refusal else {}
    rec = {"dry_run": True, "plant": {"planted": True, "kept_firm": "inflection", "as_of": "2026-10-13", "lines_blanked": 7,
                                       "blanked_firms": ["49financial", "cottonwood"]},
           "trigger": {"kind": "qa-local(manual)"}, "status": "non-green", "a4_objects_built": 12, "a4_expected": 16,
           "manifest_errors": errs, "manifest_writes": [],
           "a4_files": ["49financial/aum-metrics.json", "inflection/aum-metrics.json", "cottonwood/aum-metrics.json"]
                       + (["global/aum-metrics.json"] if gl_body else [])}
    obj = [["portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-13.json", "v1", True, "e1"],
           ["portal/gold/mdpf/inflection/aum-metrics/2026-10-13.json", "v2", True, "e2"]]
    obj2 = copy.deepcopy(obj)
    if differ:
        obj2[0][1] = "v9"
    pg = {"key": obj[0][0], "version_id": "v1"}
    pg2 = {"key": obj[0][0], "version_id": "v9" if differ else "v1"}
    calls = {"s3.GetObject": 40, "s3.ListObjectVersions": 4}
    if write:
        calls["s3.PutObject"] = 1
    for n, v in (("qa_run.json", rec), ("served_before.json", {"objects": obj, "prior_global_ts": pg}),
                 ("served_after.json", {"objects": obj2, "prior_global_ts": pg2}),
                 ("s3_ops.json", {"calls": calls, "blocked": ["s3.PutObject"] if write else []})):
        with open(os.path.join(d, n), "w", encoding="utf-8") as fh:
            json.dump(v, fh)
    with open(os.path.join(d, "qa_run.log"), "w", encoding="utf-8") as fh:
        fh.write(("  SCOPE FAILED (isolated): global -- SystemExit: " + msg + "\n") if logged else "cycle complete\n")


def cmd_selftest(argv):
    ok_all = True

    def run(label, want_green, **kw):
        nonlocal ok_all
        with tempfile.TemporaryDirectory() as d:
            _synthetic(d, **kw)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r1 = cmd_grade(["--run-dir", d])
                r2 = cmd_served(["--run-dir", d], s3=_FakeS3("v1"))
            green = (r1 == 0 and r2 == 0)
            good = green == want_green
            ok_all = ok_all and good
            print("  %s -> grade rc=%d served rc=%d %s" % (label, r1, r2, "OK" if good else "BAD"))
    run("synthetic good run record", True)
    run("PLANT refusal absent from the manifest", False, refusal=False)
    run("PLANT served object changed (VersionId differs)", False, differ=True)
    run("PLANT a write call recorded", False, write=True)
    run("PLANT refusal not in the log", False, logged=False)
    run("PLANT a Global body was built anyway", False, gl_body=True)
    # the plant function on a synthetic world
    arts = {f: {"dates": ["2026-10-12", "2026-10-13"],
                "by_model": {"m1": {"cohort_class": "model", "model_value": [1.0, 5.0]},
                             "m2": {"cohort_class": "model", "model_value": [None, 3.0] if f == "inflection" else [None, None]},
                             "m3": {"cohort_class": "model", "model_value": [None, 2.0] if f == "cottonwood" else [None, None]}}}
            for f in FIRMS}
    rec = plant_single_firm_pool(arts)
    p_ok = bool(rec.get("planted") and rec["lines_blanked"] == 1 and rec["kept_firm"] == "inflection"
                and arts["cottonwood"]["by_model"]["m3"]["model_value"][-1] is None
                and arts["inflection"]["by_model"]["m2"]["model_value"][-1] == 3.0
                and arts["49financial"]["by_model"]["m1"]["model_value"][-1] == 5.0)
    print("  plant on a synthetic world: %s -> %s" % (json.dumps(rec, sort_keys=True), "OK" if p_ok else "BAD"))
    ok_all = ok_all and bool(p_ok)
    print("ROUND 7 CN-N-1 SELFTEST: %s" % ("OK" if ok_all else "FAILED"))
    return 0 if ok_all else 1


def main() -> int:
    cmds = {"guard": cmd_guard, "plan": cmd_plan, "drive": cmd_drive, "grade": cmd_grade, "served": cmd_served, "selftest": cmd_selftest}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        return 2
    return cmds[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    raise SystemExit(main())
