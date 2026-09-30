"""Shared loader for HVST-d-1 (S3 GET only: no put, no delete, no vendor call).

The OLD alias rule is the module AT THE BASE, read with `git show <BASE>:<path>` and executed as a
throw-away module, so 'old' is the pre-round-15 code itself and never a re-implementation of it."""
import os
import subprocess
import sys
import types

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

BASE = "e7e184d8ac"  # the round-15 issuance commit this worktree was cut from (module unchanged since)
MODULE_PATH = "lib/research/harvest/universe_securities.py"
DELIVERABLES = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                            "0.9.0_WK_AMGT_HARVST~41")
SECURITIES_NEW = os.path.join(DELIVERABLES, "securities.universe.json")

# Served snapshots this cell is graded against (task order clause 4).
SERVED_PINS = {
    "article_security_mention": "date=2026-09-24/part-20260924T105025Z",
    "chatter_daily": "part-20260924T105051Z",
}


def load_old_module():
    src = subprocess.run(["git", "show", "%s:%s" % (BASE, MODULE_PATH)], cwd=REPO, check=True,
                         capture_output=True).stdout.decode("utf-8")
    mod = types.ModuleType("universe_securities_BASE")
    mod.__file__ = "git:%s:%s" % (BASE, MODULE_PATH)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def newest_snapshot_key(table, client):
    """The key `publication_gold._latest_gold_snapshot_rows` reads: newest date=, newest part."""
    from lib.research.harvest import publication_gold as pg
    from lib.research.harvest import store
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    if not keys:
        return None
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
