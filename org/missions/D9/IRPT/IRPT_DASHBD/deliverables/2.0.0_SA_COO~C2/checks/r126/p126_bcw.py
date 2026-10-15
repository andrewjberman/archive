"""IRPT_DASHBD round 126, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood FWD-1 TRACE (read only), cell DB-c-21.

  DBC126-1-AC1 the record's silver and gold sections equal a FRESH read made here (partition counts, newest dates, row counts, account_dim households and the crosswalk counts)
  DBC126-2-AC1 the reporting-gold section agrees with fresh reads and the code (next-run source partition and household count, evidence files, the output prefix LIST, the absent kinds, the hop verdicts)
  DBC126-3-AC1 the bounds: zero writes and invokes, no identifier value, only the worker's folder, the channel and its order changed

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

BASE = (HERE / "BASE_R126.txt").read_text(encoding="ascii").strip()
D = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = D + "deliverables/0.9.0_WK_IRPT_DASHBD~413/"
RECORD = FOLDER + "COTTONWOOD_FWD1_TRACE_R126.json"
NOTE = FOLDER + "COTTONWOOD_FWD1_TRACE_R126.md"
ALLOWED = (FOLDER, D + "surprise-channel/investigations/INVESTIGATION_v1.md",
           D + "task-orders/IRPT_DASHBD.TO-DB-c-21.cottonwood-fwd1-trace-silver-to-gold-to-reporting-gold-read-only.md")
TABLES = ("fact_holdings", "fact_allocations")
MISSING = ("account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily", "account_class_daily")
VERDICTS = ("HOLDS", "HOLDS_WITH_GAP", "BREAKS")
HOPS = ("silver_to_gold_holdings", "silver_to_gold_account_dim", "gold_to_reporting_gold_households", "reporting_gold_output")


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, timeout=60)
    need(r.returncode == 0, "git %s failed rc=%s: %s" % (args[0], r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def silver_prefixes(root):
    code = ("import json,sys; sys.path.insert(0,'infra/aws/lambda/investor-reporting/account-dim-cot'); import lambda_function as L; "
            "print(json.dumps(L.silver_locations('2000-01-03')))")
    r = subprocess.run([sys.executable, "-c", code], cwd=str(root), capture_output=True, text=True, timeout=100)
    need(r.returncode == 0, "silver_locations failed: " + r.stderr.strip()[-200:])
    locs = json.loads(r.stdout.strip().splitlines()[-1])
    out = {}
    for tbl in TABLES:
        b, k = locs[tbl]
        out[tbl] = (b, k[: -len("date=2000-01-03/data.parquet")])
    return out


def gold_prefix(naming, tbl):
    u = naming.address("irpt", "cottonwood", "gold", tbl, "date=2000-01-03", "data.parquet")
    b, k = re.match(r"s3://([^/]+)/(.*)$", u).groups()
    return b, k[: k.index("date=")]


def read_parquet(s3, b, k, columns=None):
    import pyarrow.parquet as pq
    return pq.read_table(io.BytesIO(s3.get_object(Bucket=b, Key=k)["Body"].read()), columns=columns)


def fresh(root):
    """The checker's own measurements: returns a dict of what it read."""
    naming, _cal = p114.lib(root)
    s3 = p114.s3client()
    out = {"silver": {}, "gold": {}}
    for tbl, (b, pfx) in silver_prefixes(root).items():
        d = sorted(p114.list_dates(s3, b, pfx))
        out["silver"][tbl] = {"partitions": len(d), "newest_date": d[-1] if d else None}
    for tbl in ("holdings_performance_daily", "account_dim"):
        b, pfx = gold_prefix(naming, tbl)
        d = sorted(p114.list_dates(s3, b, pfx))
        need(d, "no gold partition for " + tbl)
        out["gold"][tbl] = {"newest_date": d[-1], "bucket": b, "key": "%sdate=%s/data.parquet" % (pfx, d[-1])}
    ad = read_parquet(s3, out["gold"]["account_dim"]["bucket"], out["gold"]["account_dim"]["key"], ["account_id", "household_id"]).to_pylist()
    hh = {}
    for r in ad:
        h, a = r.get("household_id"), r.get("account_id")
        if h is None or str(h).strip() == "" or a is None:
            continue
        hh.setdefault(h, set()).add(a)
    out["gold"]["account_dim"].update({"rows": len(ad), "households": len(hh)})
    out["ad_accounts"] = {str(r["account_id"]).strip() for r in ad if r.get("account_id") is not None}
    out["ad_nohh"] = len({str(r["account_id"]).strip() for r in ad if r.get("account_id") is not None and (r.get("household_id") is None or str(r.get("household_id")).strip() == "")})
    out["s3"], out["naming"] = s3, naming
    return out


def ac_1(root):
    root = Path(root)
    rec = p114.load(root, RECORD)
    p114.no_identifiers(rec)
    f = fresh(root)
    for t in TABLES:
        need(rec["silver"][t]["partitions"] == f["silver"][t]["partitions"] and rec["silver"][t]["newest_date"] == f["silver"][t]["newest_date"],
             "silver differs from a fresh LIST: " + t)
    g = rec["gold"]
    for t in ("holdings_performance_daily", "account_dim"):
        need(g[t]["newest_date"] == f["gold"][t]["newest_date"], "gold newest date differs from a fresh LIST: " + t)
    hp = f["gold"]["holdings_performance_daily"]
    col = g["crosswalk"]["holdings_account_column"]
    tbl = read_parquet(f["s3"], hp["bucket"], hp["key"])
    need(col in tbl.column_names, "the holdings account column is not a column of the parquet")
    hp_rows = tbl.num_rows
    hp_accts = {str(v).strip() for v in tbl.column(col).to_pylist() if v is not None}
    need(g["holdings_performance_daily"]["rows"] == hp_rows, "holdings_performance_daily row count differs")
    ad = f["gold"]["account_dim"]
    need(g["account_dim"]["rows"] == ad["rows"] and g["account_dim"]["households"] == ad["households"], "account_dim rows or households differ")
    need(g["account_dim"]["accounts_without_household"] == f["ad_nohh"], "accounts_without_household differs")
    cw = g["crosswalk"]
    need(cw["overlap"] == len(hp_accts & f["ad_accounts"]) and cw["only_in_holdings"] == len(hp_accts - f["ad_accounts"])
         and cw["only_in_account_dim"] == len(f["ad_accounts"] - hp_accts), "the crosswalk counts differ from a fresh recount")


def ac_2(root):
    root = Path(root)
    rec = p114.load(root, RECORD)
    f = fresh(root)
    rg = rec["reporting_gold"]
    need(rg["next_run_source_partition"] == f["gold"]["account_dim"]["newest_date"], "next_run_source_partition is not the newest account_dim date")
    need(rg["next_run_households"] == f["gold"]["account_dim"]["households"], "next_run_households differs from the checker's own count")
    need(rg["scheduled_for_cottonwood"] in (True, False, "NOT_ESTABLISHED") and rg["evidence_words"].strip() != "", "scheduled_for_cottonwood or its words missing")
    need(len(rg["evidence_files"]) >= 1 and all((root / p).is_file() for p in rg["evidence_files"]), "an evidence file does not exist")
    cot_root = f["naming"].address("irpt", "cottonwood", "gold", "account_dim", "date=2000-01-03", "data.parquet")
    cot_root = cot_root[: cot_root.index("account_dim/")]
    op = rg["output_prefix"]
    if op is None:
        need(rg["output_object_count"] == 0 and rg["output_newest_key"] is None, "no output prefix but a count is recorded")
    else:
        need(op.startswith(cot_root) and op.startswith("s3://"), "the output prefix is outside the Cottonwood gold root")
        b, k = re.match(r"s3://([^/]+)/(.*)$", op).groups()
        keys = []
        for pg in f["s3"].get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=k):
            keys += [o["Key"] for o in pg.get("Contents", [])]
        newest = max(keys) if keys else None
        uri = "s3://%s/%s" % (b, newest) if newest else None
        need(rg["output_object_count"] == len(keys) and rg["output_newest_key"] in ((None,) if newest is None else (newest, uri)),
             "the output prefix count or newest key differs from a fresh LIST")
    w = rg["absent_kinds_words"]
    need(all(m in w for m in MISSING), "the four absent kinds are not all named in words")
    v = rec["verdicts"]
    need(all(h in v and v[h]["verdict"] in VERDICTS and v[h]["words"].strip() != "" for h in HOPS), "a hop verdict is missing or outside the closed set")


def ac_3(root):
    root = Path(root)
    rec = p114.load(root, RECORD)
    need(rec.get("claim") == "measured" and rec.get("pushed") is False and rec.get("deployed") is False, "record flags")
    need(rec["reads"].get("writes") == 0 and rec["reads"].get("invokes") == 0, "a write or an invoke is recorded")
    p114.no_identifiers(rec)
    note = (root / NOTE)
    need(note.is_file(), "the note is absent")
    nt = note.read_text(encoding="utf-8")
    need(not p114.LONG_DIGITS.search(nt), "a run of 8 or more digits in the note")
    need(len(nt.splitlines()) <= 60, "the note is longer than 60 lines")
    changed = sorted({p for p in git(root, "log", "--first-parent", "--no-merges", "--name-only", "--format=", BASE + "..HEAD").splitlines() if p.strip()})
    need(changed, "nothing changed since the base")
    extra = [p for p in changed if not any(p == a or (a.endswith("/") and p.startswith(a)) for a in ALLOWED)]
    need(not extra, "files outside the grant changed: " + ", ".join(extra[:5]))


ARMS = {"DBC126-1-AC1": ac_1, "DBC126-2-AC1": ac_2, "DBC126-3-AC1": ac_3}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
