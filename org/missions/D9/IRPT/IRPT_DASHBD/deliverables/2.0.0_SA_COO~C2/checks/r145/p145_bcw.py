"""IRPT_DASHBD round 145, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- FWD-10 for Cottonwood: the coverage census (DB-c-22) and the screen read (DB-c-23). Read only.

  DBC145-1-AC1 the census `tables` section equals a FRESH measurement (partitions, first and last date, the absent trading days and their runs) for the four Cottonwood gold tables
  DBC145-1-AC2 the floor, the empty silver boundaries, the twelve-day gap, the partial-history count and the bounds
  DBC145-2-AC1 the four cases and the label: closed verdicts, every cited {file, line, text} re-read, the wrong-label flag re-searched
  DBC145-2-AC2 the eight members, the Cottonwood adapter flag and the bounds

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

D = "org/missions/D9/IRPT/IRPT_DASHBD/"
F1 = D + "deliverables/0.9.0_WK_IRPT_DASHBD~414/"
F2 = D + "deliverables/0.9.0_WK_IRPT_DASHBD~415/"
CENSUS = F1 + "COTTONWOOD_COVERAGE_CENSUS_R145.json"
CENSUS_NOTE = F1 + "COTTONWOOD_COVERAGE_CENSUS_R145.md"
SCREEN = F2 + "COTTONWOOD_SCREEN_COVERAGE_READ_R145.json"
SCREEN_NOTE = F2 + "COTTONWOOD_SCREEN_COVERAGE_READ_R145.md"
ORDER1 = D + "task-orders/IRPT_DASHBD.TO-DB-c-22.cottonwood-coverage-census-where-the-data-starts-and-which-days-are-absent.md"
ORDER2 = D + "task-orders/IRPT_DASHBD.TO-DB-c-23.what-the-page-says-about-coverage-today-the-four-fwd10-cases-read-from-the-code.md"
CHANNEL = D + "surprise-channel/investigations/INVESTIGATION_v1.md"
TABLES = ("filled_report_values", "account_return_daily", "holdings_performance_daily", "account_dim")
CASES = ("partial_history_account", "day_not_measured", "fallback_day", "window_before_news_data")
VERDICTS = ("EXPLAINED", "NOT_EXPLAINED", "NOT_REACHED", "WRONG_LABEL", "NOT_ESTABLISHED")
MEMBERS = ("FULL", "PARTIAL_HISTORY", "NO_LOTS", "FLOW_UNRECONCILED", "UNCLASSIFIED_HOLDINGS", "SOURCE_LAG", "FEE_RAIL_UNUSED", "MISSING_HISTORY")
LABEL_FILE = "portal/src/pages/InvestorReporting/tabs/reporting/MethodAndSources.tsx"
LABEL_TEXT = "Time-weighted, net of fees"
ADAPTERS = ("data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py")


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, timeout=60)
    need(r.returncode == 0, "git %s failed rc=%s: %s" % (args[0], r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def bounds(root, allowed):
    root = Path(root)
    head = git(root, "rev-parse", "HEAD").strip()
    mb = subprocess.run(["git", "-C", str(root), "merge-base", "HEAD", "box/dell2"], capture_output=True, text=True, timeout=60).stdout.strip()
    need(mb and mb != head, "no branch point to read the worker's commits from")
    changed = sorted({p for p in git(root, "log", "--first-parent", "--no-merges", "--name-only", "--format=", mb + "..HEAD").splitlines() if p.strip()})
    need(changed, "nothing changed since the branch point")
    extra = [p for p in changed if not any(p == a or (a.endswith("/") and p.startswith(a)) for a in allowed)]
    need(not extra, "files outside the grant changed: " + ", ".join(extra[:5]))


def absent_and_runs(root, first, last, have):
    code = ("import sys,json,datetime as dt; sys.path.insert(0,'lib'); import trading_calendar as tc; a=json.load(sys.stdin); have=set(a['have']);"
            "days=[str(x) for x in tc.trading_days_between(dt.date.fromisoformat(a['first']),dt.date.fromisoformat(a['last']))];"
            "ab=[d for d in days if d not in have]; runs=[]; idx={d:i for i,d in enumerate(days)}\n"
            "for d in ab:\n"
            "    if runs and idx[d]==idx[runs[-1]['end']]+1: runs[-1]['end']=d; runs[-1]['trading_days']+=1\n"
            "    else: runs.append({'start':d,'end':d,'trading_days':1})\n"
            "print(json.dumps({'absent':ab,'runs':runs}))")
    r = subprocess.run([sys.executable, "-c", code], cwd=str(root), input=json.dumps({"first": first, "last": last, "have": sorted(have)}),
                       capture_output=True, text=True, timeout=110)
    need(r.returncode == 0, "calendar helper failed: " + r.stderr.strip()[-200:])
    return json.loads(r.stdout.strip().splitlines()[-1])


def gold_prefix(naming, tbl):
    u = naming.address("irpt", "cottonwood", "gold", tbl, "date=2000-01-03", "data.parquet")
    b, k = re.match(r"s3://([^/]+)/(.*)$", u).groups()
    return b, k[: k.index("date=")]


def fresh_tables(root):
    naming, _cal = p114.lib(root)
    s3 = p114.s3client()
    out = {}
    for t in TABLES:
        b, pfx = gold_prefix(naming, t)
        d = sorted(set(p114.list_dates(s3, b, pfx)))
        need(d, "no partition for " + t)
        ar = absent_and_runs(root, d[0], d[-1], d)
        out[t] = {"partitions": len(d), "first_date": d[0], "last_date": d[-1], "absent_trading_days": ar["absent"], "runs": ar["runs"], "dates": d}
    return out, s3, naming


def ac_1_1(root):
    root = Path(root)
    rec = p114.load(root, CENSUS)
    p114.no_identifiers(rec)
    f, _s3, _n = fresh_tables(root)
    for t in TABLES:
        r, x = rec["tables"][t], f[t]
        for k in ("partitions", "first_date", "last_date", "absent_trading_days"):
            need(r[k] == x[k], "%s.%s differs from a fresh measurement" % (t, k))
        need([(q["start"], q["end"], q["trading_days"]) for q in r["runs"]] == [(q["start"], q["end"], q["trading_days"]) for q in x["runs"]], t + " runs differ")


def silver_alloc_prefix(root):
    code = ("import json,sys; sys.path.insert(0,'infra/aws/lambda/investor-reporting/account-dim-cot'); import lambda_function as L; "
            "print(json.dumps(L.silver_locations('2000-01-03')))")
    r = subprocess.run([sys.executable, "-c", code], cwd=str(root), capture_output=True, text=True, timeout=100)
    need(r.returncode == 0, "silver_locations failed: " + r.stderr.strip()[-200:])
    b, k = json.loads(r.stdout.strip().splitlines()[-1])["fact_allocations"]
    return b, k[: -len("date=2000-01-03/data.parquet")]


def footer_rows(s3, b, pfx, day):
    import pyarrow.parquet as pq
    keys = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix="%sdate=%s/" % (pfx, day)):
        keys += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith(".parquet")]
    need(keys, "no parquet under silver date=" + day)
    return sum(pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=b, Key=k)["Body"].read())).metadata.num_rows for k in keys)


def accounts(s3, b, key):
    import pyarrow.parquet as pq
    t = pq.read_table(io.BytesIO(s3.get_object(Bucket=b, Key=key)["Body"].read()), columns=["account_id"])
    return {str(v).strip() for v in t.column("account_id").to_pylist() if v is not None}


def ac_1_2(root):
    root = Path(root)
    rec = p114.load(root, CENSUS)
    p114.no_identifiers(rec)
    need(rec.get("claim") == "measured" and rec.get("pushed") is False and rec.get("deployed") is False, "record flags")
    need(rec["reads"].get("writes") == 0 and rec["reads"].get("invokes") == 0, "a write or an invoke is recorded")
    f, s3, naming = fresh_tables(root)
    floor = f["filled_report_values"]["first_date"]
    need(rec["floor"]["date"] == floor, "floor date differs from the first date of filled_report_values")
    sb, sp = silver_alloc_prefix(root)
    se = rec["floor"]["silver_empty"]
    need(se["table"] == "fact_allocations" and footer_rows(s3, sb, sp, se["first_empty"]) == 0 and footer_rows(s3, sb, sp, se["last_empty"]) == 0,
         "the empty silver boundaries are not empty in a fresh footer read")
    sdates = sorted(set(p114.list_dates(s3, sb, sp)))
    need(se["last_empty"] in sdates and se["first_nonempty_after"] in sdates and footer_rows(s3, sb, sp, se["first_nonempty_after"]) > 0, "the first non-empty partition after the empty run is wrong")
    need(sdates.index(se["first_nonempty_after"]) == sdates.index(se["last_empty"]) + 1, "the first non-empty partition is not the next one after the last empty")
    g = rec["twelve_day_gap"]
    if g.get("found"):
        need(g["table"] == "account_return_daily" and g["trading_days"] == 12, "the gap is not 12 trading days in account_return_daily")
        need(any(q["start"] == g["start"] and q["end"] == g["end"] and q["trading_days"] == 12 for q in f["account_return_daily"]["runs"]), "the gap is not a run in the fresh absent list")
    else:
        need(not any(q["trading_days"] == 12 for q in f["account_return_daily"]["runs"]), "a 12-day run exists in account_return_daily but the record says not found")
    hp_b, hp_p = gold_prefix(naming, "holdings_performance_daily")
    ad_b, ad_p = gold_prefix(naming, "account_dim")
    floor_accts = accounts(s3, hp_b, "%sdate=%s/data.parquet" % (hp_p, floor))
    new_accts = accounts(s3, hp_b, "%sdate=%s/data.parquet" % (hp_p, f["holdings_performance_daily"]["last_date"]))
    ad_accts = accounts(s3, ad_b, "%sdate=%s/data.parquet" % (ad_p, f["account_dim"]["last_date"]))
    ah = rec["account_histories"]
    need(ah["accounts_in_account_dim"] == len(ad_accts) and ah["accounts_with_holdings_on_the_floor_day"] == len(floor_accts)
         and ah["accounts_first_seen_after_floor"] == len(new_accts - floor_accts), "an account-history count differs from a fresh recount")
    nt = (root / CENSUS_NOTE)
    need(nt.is_file() and not p114.LONG_DIGITS.search(nt.read_text(encoding="utf-8")) and len(nt.read_text(encoding="utf-8").splitlines()) <= 50, "the census note is absent, too long or carries an identifier-like run")
    bounds(root, (F1, CHANNEL, ORDER1))


def evidence_ok(root, ev, what):
    need(isinstance(ev, list) and ev, what + ": evidence is empty")
    for e in ev:
        p = Path(root) / e["file"]
        need(p.is_file(), what + ": evidence file absent: " + e["file"])
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        ln = int(e["line"])
        need(1 <= ln <= len(lines) and len(e["text"]) >= 12, what + ": evidence line or text invalid")
        window = "\n".join(lines[max(0, ln - 3): ln + 2])
        need(e["text"] in window, what + ": the cited text is not at %s:%s" % (e["file"], ln))


def ac_2_1(root):
    root = Path(root)
    rec = p114.load(root, SCREEN)
    p114.no_identifiers(rec)
    for c in CASES:
        v = rec["cases"][c]
        need(v["verdict"] in VERDICTS and v["words"].strip() != "", "case %s: verdict or words invalid" % c)
        evidence_ok(root, v["evidence"], "case " + c)
    lb = rec["label"]
    p = root / LABEL_FILE
    need(p.is_file(), "MethodAndSources.tsx is absent from the worker's portal worktree")
    need(lb["wrong_label_present"] is (LABEL_TEXT in p.read_text(encoding="utf-8", errors="replace")), "wrong_label_present differs from a fresh search")
    if lb["wrong_label_present"]:
        evidence_ok(root, [{"file": lb["file"], "line": lb["line"], "text": lb["text"]}], "label")
    need(lb["words"].strip() != "", "label words missing")


def loc_ok(root, loc, what):
    if loc is None:
        return
    f, ln = (loc["file"], int(loc["line"])) if isinstance(loc, dict) else (loc.rsplit(":", 1)[0], int(loc.rsplit(":", 1)[1]))
    p = Path(root) / f
    need(p.is_file() and 1 <= ln <= len(p.read_text(encoding="utf-8", errors="replace").splitlines()), what + ": location does not exist: %s" % (loc,))


def ac_2_2(root):
    root = Path(root)
    rec = p114.load(root, SCREEN)
    need(rec.get("claim") in ("inferred", "measured") and rec.get("pushed") is False and rec.get("deployed") is False, "record flags")
    rd = rec["reads"]
    need(rd.get("writes") == 0 and rd.get("aws_calls") == 0 and rd.get("runs") == 0, "a write, an AWS call or a run is recorded")
    need(set(rec["members"]) == set(MEMBERS), "the members are not exactly the eight")
    for m in MEMBERS:
        v = rec["members"][m]
        need(v["words"].strip() != "", "member words missing: " + m)
        loc_ok(root, v.get("produced_by"), "member %s produced_by" % m)
        loc_ok(root, v.get("sentence_on_screen"), "member %s sentence_on_screen" % m)
    cs = rec["cottonwood_specific"]
    fresh_flag = any(re.search(r'coverage\s*=|"coverage"', (root / a).read_text(encoding="utf-8", errors="replace")) for a in ADAPTERS)
    need(cs["adapter_reads_coverage"] is fresh_flag, "adapter_reads_coverage differs from a fresh search of the two adapters")
    evidence_ok(root, cs["evidence"], "cottonwood_specific")
    nt = root / SCREEN_NOTE
    need(nt.is_file() and len(nt.read_text(encoding="utf-8").splitlines()) <= 50, "the screen note is absent or too long")
    bounds(root, (F2, CHANNEL, ORDER2))


ARMS = {"DBC145-1-AC1": ac_1_1, "DBC145-1-AC2": ac_1_2, "DBC145-2-AC1": ac_2_1, "DBC145-2-AC2": ac_2_2}


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
