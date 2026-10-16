"""ADVI_COTBKF round 106 close read (issuer's script): what did the first scheduled silver fire and the gold builds that followed actually change?

Read-only against AWS (aws.cmd shim); writes only to the gitignored scratch folder .scratch/cotbkf_r106/ under the main checkout. Prints counts only; no account id.
  python dc1_fire_read.py baseline
      writes dim_baseline.parquet (the gold dimension as it stands) and prints BASELINE dim_version=<first 8 of VersionId> dim_rows=<n> attr_filled=<n> multibook=<n>
  python dc1_fire_read.py fire
      FIRE-READ silver_partitions=<n> newest=<date> dim_rebuilt=<bool> dim_rows=<n> attr_filled=<n> added_filled=<x>/<y> changed_agree=<x>/<y> multibook=<n>
      silver_partitions = keys under silver/account_attributes/; dim_rebuilt = the dimension's VersionId differs from the baseline's; added = accounts with no attributes
      in the baseline and some in the newest partition (y of them), added_filled = how many of those the dimension now fills; changed = accounts whose attributes differ
      between the baseline dimension and the newest partition (first row per account, as A_00 takes it), changed_agree = how many of those the dimension now equals the partition on.
  python dc1_fire_read.py snapshot
      writes mb_<VersionId8>.json (account -> portfolio_group for accounts with 2+ rows in the newest partition) and prints SNAPSHOT dim_version=<8> multibook=<n>
  python dc1_fire_read.py compare
      C1-COUNT builds=<n> multibook=<m> changed_portfolio_group=<k>   (the two newest snapshots, by file time; the CTO half's condition C-1)
  python dc1_fire_read.py selftest
      CONTROL same=<k0> mutated=<k1>   (compare on a snapshot against itself, then against a copy with some books changed: expect 0 then >0)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

BUCKET = "opal-data-cot"
REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".").resolve()
COMMON = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, cwd=str(REPO)).stdout.strip()
MAIN = (Path(COMMON) if Path(COMMON).is_absolute() else REPO / COMMON).resolve().parent
SCR = MAIN / ".scratch" / "cotbkf_r106"
AWS = str(MAIN / ".tools" / "aws.cmd")
ATTR = ["account_supervised", "account_billable", "position_only", "portfolio_group"]
DIM_KEY = "gold/dimensions/accounts_dimension_latest.parquet"


def aws(*a):
    r = subprocess.run([AWS, *a], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("aws %s rc=%d" % (" ".join(a[:3]), r.returncode))
    return r.stdout


def dim_version():
    return json.loads(aws("s3api", "head-object", "--bucket", BUCKET, "--key", DIM_KEY, "--output", "json"))["VersionId"]


def get_dim(dest):
    aws("s3", "cp", "s3://%s/%s" % (BUCKET, DIM_KEY), str(dest), "--only-show-errors")
    d = pd.read_parquet(dest)
    d["account_id"] = d["account_id"].astype(str).str.strip()
    return d


def newest_partition():
    lst = json.loads(aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "silver/account_attributes/", "--output", "json")).get("Contents", [])
    keys = sorted(o["Key"] for o in lst if o["Key"].endswith(".parquet"))
    tmp = Path(tempfile.mkdtemp(prefix="dc1_fire_")) / "p.parquet"
    aws("s3", "cp", "s3://%s/%s" % (BUCKET, keys[-1]), str(tmp), "--only-show-errors")
    p = pd.read_parquet(tmp)
    p["account_id"] = p["account_id"].astype(str).str.strip()
    return len(keys), keys[-1].rsplit("/", 1)[-1][:-8], p


def norm(df, cols):
    out = df[["account_id"] + cols].copy()
    for c in cols:
        out[c] = out[c].where(out[c].notna(), "").astype(str).str.strip()
    return out


def mb_map(p):
    dup = p[p.duplicated(subset=["account_id"], keep=False)]
    first = p.drop_duplicates(subset=["account_id"], keep="first").set_index("account_id")["portfolio_group"]
    return {a: str(first[a]) for a in dup["account_id"].unique()}


def count_changed(a, b):
    return sum(1 for k in a if k in b and a[k] != b[k])


mode = sys.argv[1] if len(sys.argv) > 1 else "fire"
SCR.mkdir(parents=True, exist_ok=True)
if mode == "baseline":
    v = dim_version()
    d = get_dim(SCR / "dim_baseline.parquet")
    (SCR / "dim_baseline.version").write_text(v, encoding="utf-8")
    n, _, p = newest_partition()
    print("BASELINE dim_version=%s dim_rows=%d attr_filled=%d multibook=%d" % (v[:8], len(d), int(d["account_supervised"].notna().sum()), len(mb_map(p))))
elif mode == "fire":
    base = pd.read_parquet(SCR / "dim_baseline.parquet")
    bv = (SCR / "dim_baseline.version").read_text(encoding="utf-8").strip()
    v = dim_version()
    cur = get_dim(SCR / "dim_now.parquet")
    n, newest, p = newest_partition()
    pf = p.drop_duplicates(subset=["account_id"], keep="first")
    pf = pf.rename(columns={"account_supervised": "account_supervised"})
    b, c, q = norm(base, ATTR).set_index("account_id"), norm(cur, ATTR).set_index("account_id"), norm(pf, ATTR).set_index("account_id")
    added = [a for a in q.index if (a not in b.index) or (b.loc[a, "account_supervised"] == "" and b.loc[a, "portfolio_group"] == "")]
    added_filled = sum(1 for a in added if a in c.index and (c.loc[a, "account_supervised"] != "" or c.loc[a, "portfolio_group"] != ""))
    changed = [a for a in q.index if a in b.index and a not in set(added) and not (b.loc[a] == q.loc[a]).all()]
    changed_agree = sum(1 for a in changed if a in c.index and (c.loc[a] == q.loc[a]).all())
    print("FIRE-READ silver_partitions=%d newest=%s dim_rebuilt=%s dim_rows=%d attr_filled=%d added_filled=%d/%d changed_agree=%d/%d multibook=%d"
          % (n, newest, v != bv, len(cur), int(cur["account_supervised"].notna().sum()), added_filled, len(added), changed_agree, len(changed), len(mb_map(p))))
elif mode == "snapshot":
    v = dim_version()
    n, newest, p = newest_partition()
    m = mb_map(p)
    (SCR / ("mb_%s.json" % v[:8])).write_text(json.dumps({"dim_version": v, "partition": newest, "map": m}), encoding="utf-8")
    print("SNAPSHOT dim_version=%s multibook=%d" % (v[:8], len(m)))
elif mode == "compare":
    snaps = sorted(SCR.glob("mb_*.json"), key=lambda f: f.stat().st_mtime)
    if len(snaps) < 2:
        print("C1-COUNT builds=%d multibook=0 changed_portfolio_group=-1" % len(snaps))
    else:
        a, b = (json.loads(f.read_text(encoding="utf-8"))["map"] for f in snaps[-2:])
        print("C1-COUNT builds=%d multibook=%d changed_portfolio_group=%d" % (len(snaps), len(b), count_changed(a, b)))
else:
    _, _, p = newest_partition()
    m = mb_map(p)
    mut = dict(m)
    for k in list(mut)[:3]:
        mut[k] = mut[k] + "x"
    print("CONTROL same=%d mutated=%d" % (count_changed(m, m), count_changed(m, mut)))
