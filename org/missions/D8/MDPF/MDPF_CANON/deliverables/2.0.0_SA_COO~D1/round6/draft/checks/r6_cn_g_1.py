#!/usr/bin/env python3
"""MDPF_CANON round 6 -- issuer checks for cell CN-g-1 (M4, the non-model-assets builder reads the gold-tier aggregates).

One subcommand per criterion; every arm prints one `ARM <name>: PASS|FAIL <detail>` line, then
`ROUND 6 <NAME>: k of n arms`; exit 0 only when every arm passes. ASCII only. Terminates well under 120 s.

  reader   5 arms, offline (S3 is a fake): the file holds no staged-aggregate read (no `aggregate_aua_timeseries.json` string, and
           `gold/mdpf_revamp` survives only in the two key definitions STAGING_KEY and FROZEN_PRECUTOVER_KEY); the global loader
           reads the NEWEST global partition at the builder's address and maps `date`->dates, `base_excluding_tax_aua`->enterprise
           (NEVER `opal_aggregate_aua`), `model_aua`->model, NaN->None; the inflection loader maps `non_model_aua`, NaN dropped;
           a scope with no partition raises SystemExit naming the scope and reads nothing else; the pure derivation still self-tests.
  seam     3 arms, real S3, READ-ONLY: `build()` from the gold tier equals `build()` from the staged JSON, row for row (DELTA=0), at
           the SAME vintage; the served `opal_aggregate_aua` would NOT (control: the wrong column differs on >= 1 date); the gold
           partition's newest date equals the staged aggregate's `as_of_last`.

  --script <path>  the file under test (default: data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py). The issuer's dry-run passes
                   a reference copy; a worker never needs it.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
GOLD_DIR = os.path.join(ROOT, "data", "mdpf", "scripts", "gold")
DEFAULT_SCRIPT = os.path.join(GOLD_DIR, "dim_mdpf_non_model_assets.py")
ARTIFACT = "aggregate_aua_timeseries"
STAGED_BUCKET = "opal-data-assets"
STAGED_KEYS = {"global": "gold/mdpf_revamp/global/aggregate_aua_timeseries.json",
               "inflection": "gold/mdpf_revamp/inflection/aggregate_aua_timeseries.json"}  # the check's own read of the OLD place


def _load(path: str):
    for p in (GOLD_DIR, ROOT):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("nma_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Paginator:
    def __init__(self, fake):
        self.fake = fake

    def paginate(self, **kw):
        self.fake.lists.append(dict(kw))
        pre, delim = kw.get("Prefix", ""), kw.get("Delimiter")
        for scope, dates in self.fake.dates.items():
            if self.fake.parent(scope)[1] == pre and delim == "/":
                return [{"CommonPrefixes": [{"Prefix": "%sdate=%s/" % (pre, d)} for d in dates]}]
        return [{}]


class _FakeS3:
    """Serves one synthetic wide parquet per (scope, date) at the address the builder returns."""

    def __init__(self, partition_uri, frames):
        self.partition_uri = partition_uri
        self.frames = frames                       # {scope: {date: DataFrame}}
        self.dates = {s: sorted(f) for s, f in frames.items()}
        self.lists, self.gets = [], []

    def parent(self, scope):
        u = urlsplit(self.partition_uri(scope, ARTIFACT, "2000-01-01"))
        return u.netloc, u.path.lstrip("/").split("/date=")[0] + "/"

    def get_paginator(self, name):
        return _Paginator(self)

    def get_object(self, Bucket, Key, **kw):
        self.gets.append((Bucket, Key))
        for scope, by_date in self.frames.items():
            for d, df in by_date.items():
                u = urlsplit(self.partition_uri(scope, ARTIFACT, d))
                if u.netloc == Bucket and u.path.lstrip("/") == Key:
                    buf = io.BytesIO()
                    df.to_parquet(buf)
                    return {"Body": io.BytesIO(buf.getvalue())}
        raise KeyError("fake S3: no object %s/%s" % (Bucket, Key))


def _arms_reader(path: str):
    arms = []
    src = open(path, encoding="utf-8").read()
    import ast
    n_json = src.count("aggregate_aua_timeseries.json")
    tree = ast.parse(src)
    allowed, doc_ids = {"STAGING_KEY", "FROZEN_PRECUTOVER_KEY"}, set()
    for node in ast.walk(tree):                      # module / function docstrings are prose, not reads
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body \
                and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant):
            doc_ids.add(id(node.body[0].value))
    skip_ids = set()
    for node in ast.walk(tree):                      # the two key definitions are the only code that may name the tree
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in allowed for t in node.targets):
            skip_ids.update(id(n) for n in ast.walk(node.value))
    stray = sorted({n.lineno for n in ast.walk(tree)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str) and "gold/mdpf_revamp" in n.value
                    and id(n) not in doc_ids and id(n) not in skip_ids})
    arms.append(("NO-STAGED-AGGREGATE-READ", n_json == 0 and not stray,
                 "'aggregate_aua_timeseries.json' x%d; string literals naming gold/mdpf_revamp outside the two key definitions: %s"
                 % (n_json, stray[:5] if stray else "none")))
    mod = fake = None
    try:
        import pandas as pd
        mod = _load(path)
        gp = _load(os.path.join(GOLD_DIR, "mdpf_gold_parquet.py"))
        puri = gp.partition_uri
        nan = float("nan")
        old_g = pd.DataFrame({"date": ["2026-09-28", "2026-09-29"], "base_excluding_tax_aua": [1.0, 2.0],
                              "model_aua": [0.5, 1.0], "opal_aggregate_aua": [9.0, 9.0]})
        new_g = pd.DataFrame({"date": ["2026-09-28", "2026-09-29", "2026-09-30"],
                              "base_excluding_tax_aua": [100.0, nan, 300.0],
                              "model_aua": [60.0, 70.0, 80.0],
                              "opal_aggregate_aua": [111.0, 222.0, 333.0]})        # the WRONG column differs on every date
        old_i = pd.DataFrame({"date": ["2026-09-29"], "non_model_aua": [1.0]})
        new_i = pd.DataFrame({"date": ["2026-09-28", "2026-09-29", "2026-09-30"], "non_model_aua": [5.0, nan, 7.0]})
        fake = _FakeS3(puri, {"global": {"2026-09-29": old_g, "2026-09-30": new_g},
                              "inflection": {"2026-09-29": old_i, "2026-09-30": new_i}})
        mod._s3 = lambda: fake
        g = mod.load_global_aggregate(None)
        ok_g = (g.get("dates") == ["2026-09-28", "2026-09-29", "2026-09-30"]
                and g.get("enterprise") == [100.0, None, 300.0] and g.get("model") == [60.0, 70.0, 80.0]
                and g.get("etf") is None)
        arms.append(("GLOBAL-COLUMN-MAP", ok_g, "dates %s; enterprise %s (base_excluding_tax_aua, NaN->None); model %s; etf %s"
                     % (g.get("dates"), g.get("enterprise"), g.get("model"), g.get("etf"))))
    except Exception as exc:  # noqa: BLE001 -- an arm that cannot run is a FAIL, printed
        arms.append(("GLOBAL-COLUMN-MAP", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    try:
        inf = mod.load_inflection_nm(None)
        want = {"2026-09-28": 5.0, "2026-09-30": 7.0}
        old_reads = [k for _b, k in fake.gets if "mdpf_revamp" in k]
        arms.append(("INFLECTION-COLUMN-MAP", inf == want and not old_reads,
                     "got %s; want %s; reads naming the old tree: %d" % (inf, want, len(old_reads))))
    except Exception as exc:  # noqa: BLE001
        arms.append(("INFLECTION-COLUMN-MAP", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    try:
        empty = _FakeS3(puri, {"global": {}, "inflection": {}})
        mod._s3 = lambda: empty
        raised = None
        try:
            mod.load_global_aggregate(None)
        except SystemExit as se:
            raised = str(se)
        arms.append(("NO-PARTITION-RAISES", bool(raised) and "global" in raised and not empty.gets,
                     "SystemExit %r; gets=%d" % ((raised or "")[:90], len(empty.gets))))
    except Exception as exc:  # noqa: BLE001
        arms.append(("NO-PARTITION-RAISES", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    try:
        rc = mod._self_test()
        arms.append(("DERIVE-UNCHANGED", rc == 0, "_self_test rc=%s (the 2026-07-18 parity baseline holds)" % rc))
    except Exception as exc:  # noqa: BLE001
        arms.append(("DERIVE-UNCHANGED", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def _arms_seam(path: str):
    import boto3
    import pandas as pd
    arms = []
    mod = _load(path)
    gp = _load(os.path.join(GOLD_DIR, "mdpf_gold_parquet.py"))
    s3 = boto3.client("s3", region_name="us-east-1")
    # --- the staged (old place) arrays, read by the CHECK, READ-ONLY
    staged = {}
    for scope, key in STAGED_KEYS.items():
        staged[scope] = json.loads(s3.get_object(Bucket=STAGED_BUCKET, Key=key)["Body"].read())
    uris = {s: "s3://%s/%s" % (STAGED_BUCKET, k) for s, k in STAGED_KEYS.items()}
    # --- build from the staged JSON (explicit URI, the old read) and from the gold tier (the new default)
    mod._s3 = lambda: s3
    old_doc = mod.build(uris["global"], uris["inflection"], mod.FROZEN_PRECUTOVER_URI, mod.CUTOVER_DATE)
    try:
        new_doc = mod.build(None, None, mod.FROZEN_PRECUTOVER_URI, mod.CUTOVER_DATE)
        a, b = old_doc["time_series"], new_doc["time_series"]
        bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        arms.append(("SEAM-DELTA0", len(a) == len(b) and not bad and len(a) > 0 and old_doc["latest"] == new_doc["latest"],
                     "rows staged %d gold %d; unequal rows %d %s; latest %s"
                     % (len(a), len(b), len(bad), [a[i]["period"] for i in bad[:3]], new_doc["latest"].get("date"))))
    except Exception as exc:  # noqa: BLE001 -- the base cannot read the gold tier; printed as a FAIL
        arms.append(("SEAM-DELTA0", False, "gold-tier build raised %s: %s" % (type(exc).__name__, str(exc)[:120])))
    # --- control: the served opal_aggregate_aua is NOT the staged enterprise (the instrument can discriminate)
    u = urlsplit(gp.partition_uri("global", ARTIFACT, "2000-01-01"))
    prefix = u.path.lstrip("/").split("/date=")[0] + "/"
    dates = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=u.netloc, Prefix=prefix, Delimiter="/"):
        dates += [c["Prefix"][len(prefix):].strip("/")[5:] for c in page.get("CommonPrefixes", []) or []]
    latest = max(d for d in dates if d.startswith("20"))
    u2 = urlsplit(gp.partition_uri("global", ARTIFACT, latest))
    df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=u2.netloc, Key=u2.path.lstrip("/"))["Body"].read()),
                         columns=["date", "base_excluding_tax_aua", "opal_aggregate_aua"])
    wrong = sum(1 for x, y in zip(df["base_excluding_tax_aua"].tolist(), df["opal_aggregate_aua"].tolist())
                if not (x != x and y != y) and x != y)
    arms.append(("CONTROL-WRONG-COLUMN-DIFFERS", wrong >= 1,
                 "opal_aggregate_aua differs from base_excluding_tax_aua on %d of %d dates (must read >= 1)" % (wrong, len(df))))
    arms.append(("SAME-VINTAGE", latest == staged["global"].get("as_of_last"),
                 "newest gold partition %s; staged as_of_last %s" % (latest, staged["global"].get("as_of_last"))))
    return arms


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=["reader", "seam"])
    ap.add_argument("--script", default=DEFAULT_SCRIPT)
    args = ap.parse_args(argv)
    arms = _arms_reader(args.script) if args.which == "reader" else _arms_seam(args.script)
    passed = 0
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
        passed += 1 if ok else 0
    print("ROUND 6 %s: %d of %d arms" % (args.which.upper(), passed, len(arms)))
    return 0 if passed == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
