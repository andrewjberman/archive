#!/usr/bin/env python3
"""MDPF_CANON round 4 -- issuer checks for cell CN-d-4 (M4, the count-source audit reads the canonical gold artifact).

One subcommand per criterion; every arm prints one `ARM <name>: PASS|FAIL <detail>` line, then
`ROUND 4 <NAME>: k of n arms`; exit 0 only when every arm passes. ASCII only. Terminates well under 120 s.

  reader   3 arms, offline (no network; S3 is a fake): the audit holds no old-place string and no typed firm bucket; its
           loader reads the NEWEST dated partition at the builder's address and returns the artifact shape the two audit
           legs consume; its firm-coverage leg lists no legacy prefix.
  seam     1 arm per firm (inflection, 49financial), real S3, READ-ONLY: the loader's per-model account_count series
           equals the legacy staging JSON's, date for date, over their common dates (DELTA=0); keys only one side
           carries are printed, never silently dropped.

  --audit <path>   the file under test (default: data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py). The issuer's
                   dry-run passes a reference copy here; a worker never needs it.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
GOLD_DIR = os.path.join(ROOT, "data", "mdpf", "scripts", "gold")
DEFAULT_AUDIT = os.path.join(GOLD_DIR, "mdpf_revamp_count_source_audit.py")
ARTIFACT = "aggregate_aua_timeseries"
LEGACY_KEY = "gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json"   # the check's own read of the OLD place
LEGACY_BUCKET = "opal-data-assets"
FIRM_BUCKET_RE = re.compile(r"opal-data-(49financial|inflection|cottonwood|mdpf)\b")


def _load(path: str):
    """Import the audit from `path` with the repo's gold dir on sys.path (it imports its siblings by bare name)."""
    for p in (GOLD_DIR, ROOT):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("audit_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Paginator:
    def __init__(self, fake):
        self.fake = fake

    def paginate(self, **kw):
        self.fake.lists.append(dict(kw))
        pre, delim = kw.get("Prefix", ""), kw.get("Delimiter")
        out = []
        for scope, dates in self.fake.partitions.items():
            parent = self.fake.parent(scope)
            if parent[1] == pre and delim == "/":
                out.append({"CommonPrefixes": [{"Prefix": "%s%s/" % (pre, "date=" + d)} for d in dates]})
        return out or [{}]


class _FakeS3:
    """Serves one synthetic wide parquet per (scope, date) at the address the builder returns."""

    def __init__(self, partition_uri, frames):
        self.partition_uri = partition_uri
        self.frames = frames                      # {scope: {date: DataFrame}}
        self.partitions = {s: sorted(d) for s, d in frames.items()}
        self.lists, self.gets = [], []

    def parent(self, scope):
        from urllib.parse import urlsplit
        u = urlsplit(self.partition_uri(scope, ARTIFACT, "2000-01-01"))
        return u.netloc, u.path.lstrip("/").split("/date=")[0] + "/"

    def get_paginator(self, name):
        return _Paginator(self)

    def get_object(self, Bucket, Key):
        from urllib.parse import urlsplit
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
    bad = []
    if "gold/mdpf_revamp" in src:
        bad.append("string 'gold/mdpf_revamp' x%d" % src.count("gold/mdpf_revamp"))
    hit = FIRM_BUCKET_RE.findall(src)
    if hit:
        bad.append("typed firm bucket literal %s" % sorted(set(hit)))
    arms.append(("NO-OLD-PLACE", not bad, "; ".join(bad) or "no legacy tree string, no typed firm bucket"))

    try:
        import pandas as pd
        mod = _load(path)
        gp = _load(os.path.join(GOLD_DIR, "mdpf_gold_parquet.py"))
        puri = gp.partition_uri
        scopes = list(gp.FIRM_SCOPES)
        nan = float("nan")
        old = pd.DataFrame({"date": ["2026-09-28", "2026-09-29", "2026-09-30"],
                            "by_model.opal_short_term.account_count": [1.0, 2.0, 3.0]})
        new = pd.DataFrame({"date": ["2026-09-28", "2026-09-29", "2026-09-30"],
                            "by_model.opal_short_term.account_count": [3.0, nan, 5.0],
                            "by_model.opal_short_term.model_value": [10.0, 11.0, 12.0],
                            "non_model_aua": [7.0, 8.0, 9.0]})
        frames = {s: {"2026-09-29": old, "2026-09-30": new} for s in scopes}
        fake = _FakeS3(puri, frames)
        mod._s3 = lambda: fake
        art = mod.latest_gold_artifact("inflection")
        exp_b, exp_k = None, None
        from urllib.parse import urlsplit
        u = urlsplit(puri("inflection", ARTIFACT, "2026-09-30"))
        exp_b, exp_k = u.netloc, u.path.lstrip("/")
        ok_shape = (art.get("dates") == ["2026-09-28", "2026-09-29", "2026-09-30"]
                    and art.get("by_model", {}).get("opal_short_term", {}).get("account_count") == [3, None, 5]
                    and set(art.get("by_model", {})) == {"opal_short_term"})
        ok_key = (exp_b, exp_k) in fake.gets and not any("mdpf_revamp" in k for _b, k in fake.gets)
        arms.append(("ADAPTER", ok_shape and ok_key,
                     "shape %s; newest partition read at the builder address %s; gets=%d"
                     % ("ok" if ok_shape else "WRONG (got %r)" % (art,), "ok" if ok_key else "WRONG", len(fake.gets))))
    except Exception as exc:  # noqa: BLE001 -- an arm that cannot run is a FAIL, printed
        arms.append(("ADAPTER", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))

    try:
        fake.lists.clear()
        got = mod.unaudited_firms()
        legacy_list = [k for k in fake.lists if "mdpf_revamp" in str(k.get("Prefix", ""))]
        ok = (got == ["cottonwood"]) and not legacy_list
        arms.append(("COVERAGE", ok, "unaudited_firms()=%r; legacy-prefix list calls=%d" % (got, len(legacy_list))))
    except Exception as exc:  # noqa: BLE001
        arms.append(("COVERAGE", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def _arms_seam(path: str):
    import boto3
    arms = []
    try:
        mod = _load(path)
        loader = mod.latest_gold_artifact
    except Exception as exc:  # noqa: BLE001
        return [("SEAM", False, "audit loader not importable: %s: %s" % (type(exc).__name__, str(exc)[:160]))]
    s3 = boto3.client("s3", region_name="us-east-1")
    for firm in ("inflection", "49financial"):
        try:
            gold = loader(firm)
            legacy = json.loads(s3.get_object(Bucket=LEGACY_BUCKET, Key=LEGACY_KEY.format(firm=firm))["Body"].read())
            gd = [str(x)[:10] for x in gold["dates"]]
            ld = [str(x)[:10] for x in legacy["dates"]]
            common = [d for d in gd if d in set(ld)]
            gi = {d: i for i, d in enumerate(gd)}
            li = {d: i for i, d in enumerate(ld)}
            shared = sorted(set(gold["by_model"]) & set(legacy["by_model"]))
            only_gold = sorted(set(gold["by_model"]) - set(legacy["by_model"]))
            only_legacy = sorted(set(legacy["by_model"]) - set(gold["by_model"]))
            cells = unequal = 0
            for k in shared:
                gs, ls = gold["by_model"][k]["account_count"], legacy["by_model"][k]["account_count"]
                for d in common:
                    a, b = gs[gi[d]], ls[li[d]]
                    a = None if a is None else int(a)
                    b = None if b is None else int(b)
                    cells += 1
                    unequal += int(a != b)
            ok = cells > 0 and unequal == 0 and not only_legacy
            arms.append(("SEAM-" + firm, ok, "cells=%d unequal=%d common_dates=%d shared_keys=%d keys_only_in_gold=%s "
                                             "keys_only_in_legacy=%s partition=%s"
                         % (cells, unequal, len(common), len(shared), only_gold, only_legacy, gold.get("gold_partition"))))
        except Exception as exc:  # noqa: BLE001
            arms.append(("SEAM-" + firm, False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("reader", "seam"))
    ap.add_argument("--audit", default=DEFAULT_AUDIT)
    a = ap.parse_args(argv)
    arms = _arms_reader(a.audit) if a.cmd == "reader" else _arms_seam(a.audit)
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
    n_ok = sum(1 for _n, ok, _d in arms if ok)
    print("ROUND 4 %s: %d of %d arms" % (a.cmd.upper(), n_ok, len(arms)))
    return 0 if n_ok == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
