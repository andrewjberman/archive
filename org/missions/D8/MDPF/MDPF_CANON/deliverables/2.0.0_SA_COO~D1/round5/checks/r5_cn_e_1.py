#!/usr/bin/env python3
"""MDPF_CANON round 5 -- issuer checks for cell CN-e-1 (M4, the aum-timeseries instrument reads the canonical gold artifact).

One subcommand per criterion; every arm prints one `ARM <name>: PASS|FAIL <detail>` line, then
`ROUND 5 <NAME>: k of n arms`; exit 0 only when every arm passes. ASCII only. Terminates well under 120 s.

  reader   5 arms, offline (S3 is a fake): the script holds no old-place string; its loader `latest_gold_aggregate` reads the
           NEWEST dated global partition at the builder's address and returns the dict `build_aum_timeseries` consumes,
           with `cohort_class` taken from the producer's model registry (never from the parquet); a missing core model
           still stops `build_aum_timeseries` by name; a scope with no partition raises and reads nothing else.
  seam     1 arm, real S3, READ-ONLY: `build_aum_timeseries(loader())` equals `build_aum_timeseries(<legacy staging JSON>)`
           cell for cell over their common dates (DELTA=0); keys and dates only one side carries are printed.

  --script <path>  the file under test (default: data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py). The issuer's dry-run
                   passes a reference copy; a worker never needs it.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
GOLD_DIR = os.path.join(ROOT, "data", "mdpf", "scripts", "gold")
DEFAULT_SCRIPT = os.path.join(GOLD_DIR, "dim_mdpf_aum_timeseries.py")
ARTIFACT = "aggregate_aua_timeseries"
SCOPE = "global"
LEGACY_KEY = "gold/mdpf_revamp/global/aggregate_aua_timeseries.json"   # the check's own read of the OLD place
LEGACY_BUCKET = "opal-data-assets"
CORE = ("opal_ultra_short_term", "opal_short_term", "opal_intermediate", "opal_long_term_conservative",
        "opal_long_term_aggressive")


def _load(path: str):
    for p in (GOLD_DIR, ROOT):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("aumts_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Paginator:
    def __init__(self, fake):
        self.fake = fake

    def paginate(self, **kw):
        self.fake.lists.append(dict(kw))
        pre, delim = kw.get("Prefix", ""), kw.get("Delimiter")
        if self.fake.parent()[1] == pre and delim == "/":
            return [{"CommonPrefixes": [{"Prefix": "%sdate=%s/" % (pre, d)} for d in self.fake.dates]}]
        return [{}]


class _FakeS3:
    """Serves one synthetic wide parquet per date at the address the builder returns for the global scope."""

    def __init__(self, partition_uri, frames):
        self.partition_uri = partition_uri
        self.frames = frames                      # {date: DataFrame}
        self.dates = sorted(frames)
        self.lists, self.gets = [], []

    def parent(self):
        from urllib.parse import urlsplit
        u = urlsplit(self.partition_uri(SCOPE, ARTIFACT, "2000-01-01"))
        return u.netloc, u.path.lstrip("/").split("/date=")[0] + "/"

    def get_paginator(self, name):
        return _Paginator(self)

    def get_object(self, Bucket, Key, **kw):
        from urllib.parse import urlsplit
        self.gets.append((Bucket, Key))
        for d, df in self.frames.items():
            u = urlsplit(self.partition_uri(SCOPE, ARTIFACT, d))
            if u.netloc == Bucket and u.path.lstrip("/") == Key:
                buf = io.BytesIO()
                df.to_parquet(buf)
                return {"Body": io.BytesIO(buf.getvalue())}
        raise KeyError("fake S3: no object %s/%s" % (Bucket, Key))


def _frame(pd, dates, with_cores=True, extra=None):
    nan = float("nan")
    data = {"date": dates}
    if with_cores:
        for i, k in enumerate(CORE):
            data["by_model.%s.model_value" % k] = [100.0 * (i + 1) + j for j in range(len(dates))]
            data["by_model.%s.account_count" % k] = [3.0 + i, nan, 5.0 + i][: len(dates)]
    data.update(extra or {})
    return pd.DataFrame(data)


def _arms_reader(path: str):
    arms = []
    src = open(path, encoding="utf-8").read()
    n = src.count("gold/mdpf_revamp")
    arms.append(("NO-OLD-PLACE", n == 0, "string 'gold/mdpf_revamp' x%d" % n if n else "no legacy tree string"))
    mod = fake = None
    try:
        import pandas as pd
        mod = _load(path)
        gp = _load(os.path.join(GOLD_DIR, "mdpf_gold_parquet.py"))
        puri = gp.partition_uri
        dates = ["2026-09-28", "2026-09-29", "2026-09-30"]
        old = _frame(pd, dates)
        new = _frame(pd, dates)
        # the newest partition differs from the older one, so a wrong pick is visible
        new["by_model.opal_short_term.model_value"] = [1.5, 2.5, 3.5]
        fake = _FakeS3(puri, {"2026-09-29": old, "2026-09-30": new})
        mod._s3 = lambda: fake
        agg = mod.latest_gold_aggregate()
        from urllib.parse import urlsplit
        u = urlsplit(puri(SCOPE, ARTIFACT, "2026-09-30"))
        node = agg.get("by_model", {}).get("opal_short_term", {})
        ok_shape = (agg.get("dates") == dates and node.get("model_value") == [1.5, 2.5, 3.5]
                    and node.get("account_count") == [4, None, 6]
                    and set(agg.get("by_model", {})) >= set(CORE))
        ok_key = (u.netloc, u.path.lstrip("/")) in fake.gets and not any("mdpf_revamp" in k for _b, k in fake.gets)
        arms.append(("ADAPTER", ok_shape and ok_key, "shape %s; newest partition read at the builder address %s; gets=%d"
                     % ("ok" if ok_shape else "WRONG (got keys %s)" % sorted(agg.get("by_model", {})), "ok" if ok_key else "WRONG",
                        len(fake.gets))))
    except Exception as exc:  # noqa: BLE001 -- an arm that cannot run is a FAIL, printed
        arms.append(("ADAPTER", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))

    try:
        cc = {k: agg["by_model"][k].get("cohort_class") for k in CORE}
        from mdpf_revamp_model_crosswalk import entry_for_key
        reg = {k: entry_for_key(k).cohort_class for k in CORE}
        doc = mod.build_aum_timeseries(agg)
        arms.append(("COHORT-FROM-REGISTRY", cc == reg and all(v == "model" for v in cc.values()) and bool(doc),
                     "cohort_class %s equals the registry's %s; build_aum_timeseries ran" % (sorted(set(cc.values())), sorted(set(reg.values())))))
    except Exception as exc:  # noqa: BLE001
        arms.append(("COHORT-FROM-REGISTRY", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))

    try:
        import pandas as pd
        short = _frame(pd, ["2026-09-28", "2026-09-29", "2026-09-30"], with_cores=False)
        for k in CORE[1:]:
            short["by_model.%s.model_value" % k] = [1.0, 2.0, 3.0]
            short["by_model.%s.account_count" % k] = [1.0, 2.0, 3.0]
        fake2 = _FakeS3(gp.partition_uri, {"2026-09-30": short})
        mod._s3 = lambda: fake2
        stopped = ""
        try:
            mod.build_aum_timeseries(mod.latest_gold_aggregate())
        except SystemExit as e:
            stopped = str(e)
        arms.append(("MISSING-CORE-STOPS", "opal_ultra_short_term" in stopped,
                     "a frame without opal_ultra_short_term stops build_aum_timeseries: %r" % stopped[:90]))
    except Exception as exc:  # noqa: BLE001
        arms.append(("MISSING-CORE-STOPS", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))

    try:
        empty = _FakeS3(gp.partition_uri, {})
        mod._s3 = lambda: empty
        raised = ""
        try:
            mod.latest_gold_aggregate()
        except SystemExit as e:
            raised = str(e)
        arms.append(("NO-PARTITION-RAISES", bool(raised) and not any("mdpf_revamp" in k for _b, k in empty.gets) and not empty.gets,
                     "no dated partition raises (%r) and no object is read" % raised[:80]))
    except Exception as exc:  # noqa: BLE001
        arms.append(("NO-PARTITION-RAISES", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def _arms_seam(path: str):
    import boto3
    try:
        mod = _load(path)
        loader = mod.latest_gold_aggregate
        build = mod.build_aum_timeseries
    except Exception as exc:  # noqa: BLE001
        return [("SEAM", False, "loader not importable: %s: %s" % (type(exc).__name__, str(exc)[:160]))]
    s3 = boto3.client("s3", region_name="us-east-1")
    try:
        gold = loader()
        legacy = json.loads(s3.get_object(Bucket=LEGACY_BUCKET, Key=LEGACY_KEY)["Body"].read())
        gdoc, ldoc = build(gold), build(legacy)
        gd = [str(x)[:10] for x in gold["dates"]]
        ld = [str(x)[:10] for x in legacy["dates"]]
        common = sorted(set(gd) & set(ld))
        cells = unequal = 0
        shared = sorted(set(gdoc["by_model"]) & set(ldoc["by_model"]))
        only_gold = sorted(set(gdoc["by_model"]) - set(ldoc["by_model"]))
        only_legacy = sorted(set(ldoc["by_model"]) - set(gdoc["by_model"]))
        gi = {r.get("period"): r for r in gdoc.get("aggregate", [])} if isinstance(gdoc.get("aggregate"), list) else {}
        li = {r.get("period"): r for r in ldoc.get("aggregate", [])} if isinstance(ldoc.get("aggregate"), list) else {}
        for k in shared:
            gm = {r["period"]: r for r in gdoc["by_model"][k]}
            lm = {r["period"]: r for r in ldoc["by_model"][k]}
            for d in common:
                a, b = gm.get(d), lm.get(d)
                cells += 1
                unequal += int(a != b)
        for d in common:
            if gi or li:
                cells += 1
                unequal += int(gi.get(d) != li.get(d))
        ok = cells > 0 and unequal == 0 and not only_legacy
        return [("SEAM", ok, "cells=%d unequal=%d common_dates=%d shared_models=%d only_gold=%s only_legacy=%s partition=%s"
                 % (cells, unequal, len(common), len(shared), only_gold, only_legacy, gold.get("gold_partition")))]
    except Exception as exc:  # noqa: BLE001
        return [("SEAM", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("reader", "seam"))
    ap.add_argument("--script", default=DEFAULT_SCRIPT)
    a = ap.parse_args(argv)
    arms = _arms_reader(a.script) if a.cmd == "reader" else _arms_seam(a.script)
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
    n_ok = sum(1 for _n, ok, _d in arms if ok)
    print("ROUND 5 %s: %d of %d arms" % (a.cmd.upper(), n_ok, len(arms)))
    return 0 if n_ok == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
