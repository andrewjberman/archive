"""Shared import path for the round-20 ~P checks: the performance package of the worktree given as argv[1]."""
import sys
from pathlib import Path


def install(root):
    root = Path(root).resolve()
    package = root / "infra" / "aws" / "lambda" / "investor-reporting" / "performance"
    if not (package / "retained.py").is_file():
        raise SystemExit("FAIL: no performance package under %s" % root)
    for path in (package, package.parent / "reports", package.parent / "reports" / "tests", package.parent / "_ids",
                 package.parent / "_authz", package / "tests",
                 root / "data" / "assets" / "scripts" / "gold" / "runners_49f", root / "lib"):
        sys.path.insert(0, str(path))
    return root, package


def gold_frame(day, rows):
    """One holdings_performance_daily partition: rows of (raw_account, daily_return, account_value, status)."""
    import pandas as pd
    return pd.DataFrame([{"account_id": a, "business_date": day, "daily_return": r, "account_value": v,
                          "excluded_count": 0, "excluded_weight": 0.0, "status": s}
                         for a, r, v, s in rows])


class GoldS3:
    """In-memory S3 holding holdings_performance_daily partitions under `prefix`."""

    def __init__(self, prefix, days):
        import io
        self.objects, self.gets = {}, []
        for day, rows in days.items():
            buf = io.BytesIO()
            gold_frame(day, rows).to_parquet(buf, index=False)
            self.objects["%sdate=%s/data.parquet" % (prefix, day)] = buf.getvalue()

    def get_paginator(self, name):
        store = self

        class Paginator:
            def paginate(self, Bucket, Prefix, Delimiter=None, **kw):
                prefixes = sorted({k[:k.index("/data.parquet") + 1] for k in store.objects if k.startswith(Prefix)})
                yield {"CommonPrefixes": [{"Prefix": p} for p in prefixes],
                       "Contents": [{"Key": k} for k in sorted(store.objects) if k.startswith(Prefix)]}
        return Paginator()

    def list_objects_v2(self, Bucket, Prefix, **kw):
        return {"Contents": [{"Key": k} for k in sorted(self.objects) if k.startswith(Prefix)]}

    def get_object(self, Bucket, Key, **kw):
        import io
        self.gets.append(Key)
        return {"Body": io.BytesIO(self.objects[Key]), "VersionId": "v-" + Key[-24:-13], "ETag": '"e"'}
