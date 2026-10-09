"""r1_backfill.py -- MDPF_CANON round 1, cell CN-a-3 (issuer 2.0.0_SA_COO~D1): THE BACKFILL.

Usage (repo root of the checkout under test): python <this file>      (R1_TREE=<dir> points it at a reference tree)

PRD v2.9 DEC-2 / M3: every historical date the JSON holds becomes one dated partition, its count printed against the
source's; no date is rewritten. Round 1's source is the legacy dated tree `portal/gold/mdpf/{scope}/{type}/{date}.json`
(the L5 fact sheet: 32-58 dates per series from 2026-07-20..30). Module under test:
data/mdpf/scripts/gold/mdpf_gold_backfill.py, its interface fixed by the order:
  SOURCE_TYPES   {"aggregate-aua-timeseries": "aggregate_aua_timeseries", "aum-metrics": "aum_metrics",
                  "account-distribution": "account_distribution", "account-units": "account_units"}
  plan(source_keys, existing)  -> sorted [(scope, artifact, date, source_key)] for every source key of the form
                                  portal/gold/mdpf/{scope}/{type}/{YYYY-MM-DD}.json with a SOURCE_TYPES type, minus
                                  (scope, artifact, date) already in `existing`; every other key is ignored
  summarize(plan_rows, source_keys, existing) -> one line per (scope, artifact):
                                  "BACKFILL {scope}/{artifact}: {n} of {m} source dates ({k} already present)"
  run(plan_rows, read_source, write) -> {"written": a, "unchanged": b, "conflict": c}; calls write(scope, artifact,
                                  date, records) once per row with records = read_source(source_key); never retries
Arms:
  1 MAP          the planted listing's artifact keys are planned with the right (scope, artifact, date).
  2 SKIP         a (scope, artifact, date) already present is not planned.
  3 IGNORE       category-views, non-model-assets, _manifests, _code and undated keys are never planned.
  4 COUNT        summarize prints the n-of-m line for each series, with the already-present count.
  5 RUN          run() writes each planned row once, in order, and tallies the verdicts write() returns.
  6 UNTYPED      the module types no new-home bucket (opal-data-mdpf, opal-data-49financial, -inflection,
                 -cottonwood, -demo) and no s3:// new address; writes go through the writer.
  7 WIRED        the consolidator's lambda_handler takes run_class "backfill" and calls mdpf_gold_backfill;
                 build_package.py ships mdpf_gold_backfill.py.
Prints one line per arm and "ROUND 1 BACKFILL: <k> of <n> arms"; exit 0 only when every arm passes.
"""
import importlib.util
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
TREE = os.environ.get("R1_TREE") or ROOT
GOLD_DIR = os.path.join(TREE, "data/mdpf/scripts/gold")
MOD = os.path.join(GOLD_DIR, "mdpf_gold_backfill.py")
CONS = os.path.join(GOLD_DIR, "mdpf_gold_consolidator.py")
PKG = os.path.join(TREE, "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py")
sys.path[:0] = [ROOT, GOLD_DIR]

P = "portal/gold/mdpf/"
LISTING = [
    P + "49financial/aum-metrics/2026-08-03.json",
    P + "49financial/aum-metrics/2026-08-04.json",
    P + "49financial/aggregate-aua-timeseries/2026-08-03.json",
    P + "cottonwood/account-units/2026-07-20.json",
    P + "global/account-distribution/2026-07-28.json",
    P + "global/category-views/2026-08-27.json",
    P + "global/non-model-assets/2026-07-27.json",
    P + "_manifests/2026-08-05/20260805T133000Z.json",
    P + "_code/mdpf-gold-lambda.zip",
    P + "49financial/aum-metrics/latest.json",
]
EXISTING = {("49financial", "aum_metrics", "2026-08-04")}
WANT = [
    ("49financial", "aggregate_aua_timeseries", "2026-08-03", P + "49financial/aggregate-aua-timeseries/2026-08-03.json"),
    ("49financial", "aum_metrics", "2026-08-03", P + "49financial/aum-metrics/2026-08-03.json"),
    ("cottonwood", "account_units", "2026-07-20", P + "cottonwood/account-units/2026-07-20.json"),
    ("global", "account_distribution", "2026-07-28", P + "global/account-distribution/2026-07-28.json"),
]


def load():
    spec = importlib.util.spec_from_file_location("mdpf_gold_backfill", MOD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


arms = []
M = {}


def arm(label, fn):
    f = []
    try:
        detail = fn(f) or ""
    except Exception as e:  # noqa: BLE001 -- an arm that raises is a failed arm, said in its line
        f.append("RAISED: " + (str(e).splitlines() or [repr(e)])[0][:200])
        detail = ""
    arms.append((label, not f, detail if not f else " | ".join(f)))


def a_map(f):
    if not os.path.exists(MOD):
        f.append(f"MISSING: {os.path.relpath(MOD, TREE)}")
        return ""
    M["m"] = m = load()
    rows = [tuple(r) for r in m.plan(LISTING, EXISTING)]
    M["rows"] = rows
    if rows != WANT:
        f.append(f"plan {rows!r} != {WANT!r}")
    return f"{len(rows)} rows planned, each (scope, artifact, date, source)"


def a_skip(f):
    rows = M.get("rows")
    if rows is None:
        f.append("INPUT: arm 1 did not run")
        return ""
    if any((r[0], r[1], r[2]) in EXISTING for r in rows):
        f.append("an existing partition was planned")
    return "the present 49financial/aum_metrics/2026-08-04 is not planned"


def a_ignore(f):
    rows = M.get("rows")
    if rows is None:
        f.append("INPUT: arm 1 did not run")
        return ""
    bad = [r for r in rows if any(x in r[3] for x in ("category-views", "non-model-assets", "_manifests", "_code", "latest"))]
    if bad:
        f.append(f"noise planned: {bad!r}")
    return "6 noise keys ignored"


def a_count(f):
    m = M.get("m")
    if not m:
        f.append("INPUT: module not loaded")
        return ""
    out = m.summarize(M["rows"], LISTING, EXISTING)
    lines = out if isinstance(out, list) else str(out).splitlines()
    want = "BACKFILL 49financial/aum_metrics: 1 of 2 source dates (1 already present)"
    if want not in lines:
        f.append(f"no line {want!r} in {lines!r}")
    for sc, art in (("cottonwood", "account_units"), ("global", "account_distribution")):
        if f"BACKFILL {sc}/{art}: 1 of 1 source dates (0 already present)" not in lines:
            f.append(f"no 1-of-1 line for {sc}/{art}")
    return f"{len(lines)} series lines"


def a_run(f):
    m = M.get("m")
    if not m:
        f.append("INPUT: module not loaded")
        return ""
    calls = []
    verdicts = iter(["written", "written", "unchanged", "conflict"])

    def write(scope, artifact, date, records):
        calls.append((scope, artifact, date, records))
        return next(verdicts)

    buf = io.StringIO()
    with redirect_stdout(buf):
        tally = m.run(M["rows"], lambda key: [{"src": key}], write)
    if [c[:3] for c in calls] != [r[:3] for r in M["rows"]]:
        f.append(f"write calls {[c[:3] for c in calls]!r}")
    if any(c[3] != [{"src": r[3]}] for c, r in zip(calls, M["rows"])):
        f.append("records were not read_source(source_key)")
    if dict(tally) != {"written": 2, "unchanged": 1, "conflict": 1}:
        f.append(f"tally {dict(tally)!r}")
    return "four writes, in order, verdicts tallied 2/1/1"


def a_untyped(f):
    if not os.path.exists(MOD):
        f.append("MISSING module")
        return ""
    src = open(MOD, encoding="utf-8").read()
    for lit in ("opal-data-mdpf", "opal-data-49financial", "opal-data-inflection", "opal-data-cottonwood", "opal-data-demo"):
        if lit in src:
            f.append(f"TYPED: {lit}")
    for m_ in re.finditer(r'["\']s3://([^"\']+)', src):
        if not m_.group(1).startswith("opal-data-assets/"):
            f.append(f"TYPED new address: s3://{m_.group(1)}")
    return "no new-home bucket typed"


def a_wired(f):
    cons = open(CONS, encoding="utf-8").read()
    pkg = open(PKG, encoding="utf-8").read()
    if not re.search(r'["\']backfill["\']', cons):
        f.append('the consolidator never names run_class "backfill"')
    if not re.search(r'(?m)^\s*(import mdpf_gold_backfill|from mdpf_gold_backfill import)|mdpf_gold_backfill', cons):
        f.append("the consolidator does not use mdpf_gold_backfill")
    if '"mdpf_gold_backfill.py"' not in pkg:
        f.append("build_package.py does not ship mdpf_gold_backfill.py")
    return 'run_class "backfill" wired; the package ships the module'


arm("MAP: the listing's artifact keys plan as (scope, artifact, date, source)", a_map)
arm("SKIP: a partition already present is not planned (history never rewritten)", a_skip)
arm("IGNORE: category-views, non-model-assets, manifests, code and undated keys are never planned", a_ignore)
arm("COUNT: one n-of-m line per series with the already-present count", a_count)
arm("RUN: each planned row written once, in order, verdicts tallied", a_run)
arm("UNTYPED: no new-home bucket and no new s3:// address typed in the module", a_untyped)
arm('WIRED: run_class "backfill" reaches mdpf_gold_backfill; the package ships it', a_wired)

ok = 0
for label, passed, detail in arms:
    ok += passed
    print(f"{'ARM PASS' if passed else 'ARM FAIL'} {label} :: {detail}")
print(f"ROUND 1 BACKFILL: {ok} of {len(arms)} arms")
sys.exit(0 if ok == len(arms) else 1)
