"""IRPT_DASHBD round 149, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- FWD-10 for 49 Financial: the coverage census of the gold tables and the labelled TEST READ of the published series through the page, cell DB-c-29. Read only; counts only.

  DBC150-1-AC1 the record's `gold` section equals a FRESH measurement (partitions, first and last date, the absent trading days and their runs) of account_return_daily and holdings_performance_daily
  DBC150-1-AC2 the record's `series_truth` equals a FRESH read of the published series prefix, and the page-side counts agree with it (every document read, none refused or threw, no income coerced, the unreported-days sentence count equals the documents with a non-empty list)
  DBC150-1-AC3 the hygiene: no account identifier in the worker's folder, zero writes and invokes, no downloaded object left behind, only the worker's folder, the channel and its order changed

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
The checker's own reads are S3 list_objects_v2 and get_object through python boto3, region us-east-1; it prints counts only, never a key or a value.
"""
import gzip
import importlib.util
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need
spec2 = importlib.util.spec_from_file_location("p145", str(HERE.parent / "r145" / "p145_bcw.py"))
p145 = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(p145)

D = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = D + "deliverables/0.9.0_WK_IRPT_DASHBD~420/"
RECORD = FOLDER + "FWD10_49F_CENSUS_R149.json"
NOTE = FOLDER + "FWD10_49F_CENSUS_R149.md"
CHANNEL = D + "surprise-channel/investigations/INVESTIGATION_v1.md"
ORDER = D + "task-orders/IRPT_DASHBD.TO-DB-c-29."
FIRM = "49financial"
TABLES = ("account_return_daily", "holdings_performance_daily")
SERIES_PREFIX_ARGS = ("irpt", FIRM, "platinum", "reporting")
ID_RE = re.compile(r"account=|household|\b\d{8,}\b", re.I)


def split(uri):
    b, k = re.match(r"s3://([^/]+)/(.*)$", uri).groups()
    return b, k


def gold_prefix(naming, table):
    b, k = split(naming.address("irpt", FIRM, "gold", table, "date=2000-01-03", "data.parquet"))
    return b, k[: k.index("date=")]


def series_prefix(naming):
    b, k = split(naming.address("irpt", FIRM, "platinum", "reporting", "account=X", "series.json.gz"))
    return b, k[: k.index("account=")]


def fresh_gold(root):
    naming, _cal = p114.lib(root)
    s3 = p114.s3client()
    out = {}
    for t in TABLES:
        b, pfx = gold_prefix(naming, t)
        d = sorted(set(p114.list_dates(s3, b, pfx)))
        need(d, "no partition for " + t)
        ar = p145.absent_and_runs(root, d[0], d[-1], d)
        out[t] = {"partitions": len(d), "first_date": d[0], "last_date": d[-1], "absent_trading_days": ar["absent"],
                  "runs": [(q["start"], q["end"], q["trading_days"]) for q in ar["runs"]]}
    return out


def truth(root, deadline=100):
    naming, _cal = p114.lib(root)
    s3 = p114.s3client()
    b, pfx = series_prefix(naming)
    keys, token, lists = [], None, 0
    while True:
        kw = {"Bucket": b, "Prefix": pfx}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        lists += 1
        keys += [o["Key"] for o in r.get("Contents", [])]
        token = r.get("NextContinuationToken")
        if not token:
            break
    series = [k for k in keys if k.endswith("/series.json.gz")]
    manifests = [k for k in keys if k.endswith("/manifest.json")]
    t0 = time.time()

    def get(k):
        return gzip.decompress(s3.get_object(Bucket=b, Key=k)["Body"].read())

    with ThreadPoolExecutor(32) as ex:
        raws = list(ex.map(get, series))
    need(time.time() - t0 < deadline, "the fresh read took too long")
    out = {"objects_series": len(series), "objects_manifest": len(manifests), "objects_other": len(keys) - len(series) - len(manifests),
           "docs_total": 0, "docs_parse_ok": 0, "pair_present": 0, "pair_absent": 0, "nonempty_lists": 0, "total_listed_days": 0,
           "max_list_len": 0, "income_all_null_docs": 0, "income_any_number_docs": 0, "income_claim_present_docs": 0,
           "history_scope_counts": {}, "first_data_date_min": None, "first_data_date_max": None, "as_of_counts": {},
           "day_quality_day_totals": {}, "return_basis_day_totals": {}}
    for raw in raws:
        out["docs_total"] += 1
        try:
            d = json.loads(raw)
        except Exception:
            continue
        out["docs_parse_ok"] += 1
        if "unreported_trading_days" in d and "unreported_trading_days_basis" in d:
            out["pair_present"] += 1
            n = len(d["unreported_trading_days"])
            out["total_listed_days"] += n
            out["max_list_len"] = max(out["max_list_len"], n)
            out["nonempty_lists"] += 1 if n else 0
        else:
            out["pair_absent"] += 1
        inc = d.get("income", [])
        if inc and all(x is None for x in inc):
            out["income_all_null_docs"] += 1
        if any(isinstance(x, (int, float)) for x in inc):
            out["income_any_number_docs"] += 1
        if "income_claim" in d:
            out["income_claim_present_docs"] += 1
        hs = str(d.get("history_scope"))
        out["history_scope_counts"][hs] = out["history_scope_counts"].get(hs, 0) + 1
        f, a = str(d.get("first_data_date")), str(d.get("as_of"))
        out["first_data_date_min"] = f if out["first_data_date_min"] is None or f < out["first_data_date_min"] else out["first_data_date_min"]
        out["first_data_date_max"] = f if out["first_data_date_max"] is None or f > out["first_data_date_max"] else out["first_data_date_max"]
        out["as_of_counts"][a] = out["as_of_counts"].get(a, 0) + 1
        for key, dest in (("day_quality", "day_quality_day_totals"), ("return_basis", "return_basis_day_totals")):
            for v in d.get(key, []):
                out[dest][str(v)] = out[dest].get(str(v), 0) + 1
    return out, lists


def no_ids(rec):
    text = json.dumps(rec)
    need(ID_RE.search(text) is None, "an identifier-like token is in the record")


def ac_1(root):
    root = Path(root)
    rec = p114.load(root, RECORD)
    no_ids(rec)
    f = fresh_gold(root)
    for t in TABLES:
        r, x = rec["gold"][t], f[t]
        for k in ("partitions", "first_date", "last_date", "absent_trading_days"):
            need(r[k] == x[k], "%s.%s differs from a fresh measurement" % (t, k))
        need([(q["start"], q["end"], q["trading_days"]) for q in r["runs"]] == x["runs"], t + " runs differ")
    need(rec.get("claim") == "measured" and "TEST READ" in str(rec.get("label", "")), "the record is not labelled a TEST READ with claim measured")


def ac_2(root):
    root = Path(root)
    rec = p114.load(root, RECORD)
    fresh, _ = truth(root)
    mine = rec["series_truth"]
    diff = [k for k in fresh if fresh[k] != mine.get(k)]
    need(not diff, "the record's series_truth differs from a fresh read in: " + ", ".join(diff))
    pg = rec["page"]
    need(fresh["docs_total"] > 0 and fresh["docs_parse_ok"] == fresh["docs_total"], "a published document did not parse")
    need(pg["read_ok"] == fresh["docs_total"] and pg["read_refused"] == 0, "the page reader refused or missed a document: %s" % json.dumps(pg))
    need(pg["performance_view_threw"] == 0, "performanceView threw on a document")
    need(pg["accounts_printing_unreported_sentence"] == fresh["nonempty_lists"], "unreported sentences %s != accounts with a non-empty list %s" % (pg["accounts_printing_unreported_sentence"], fresh["nonempty_lists"]))
    need(pg["sentence_n_mismatch"] == 0 and pg["income_coerced_to_zero"] == 0, "a printed count differs from its list, or an income null was coerced")


def ac_3(root):
    root = Path(root)
    folder = root / FOLDER
    need(folder.is_dir(), "the worker's folder is absent")
    for f in folder.rglob("*"):
        if f.is_file():
            need(not f.name.endswith((".gz", ".parquet")), "a downloaded object is left behind: " + f.name)
            if f.suffix.lower() in (".json", ".md", ".ts", ".tsx", ".py", ".txt"):
                need(ID_RE.search(f.read_text(encoding="utf-8", errors="replace")) is None, "an identifier-like token is in " + f.name)
    rec = p114.load(root, RECORD)
    need(rec["reads"]["writes"] == 0 and rec["reads"]["invokes"] == 0, "the record reports a write or an invoke")
    need(rec["pushed"] is False and rec["deployed"] is False and rec["ids_recorded"] is False, "pushed, deployed or ids_recorded is not false")
    nt = root / NOTE
    need(nt.is_file() and len(nt.read_text(encoding="utf-8").splitlines()) <= 50, "the note is absent or longer than 50 lines")
    base = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], cwd=str(root), capture_output=True, text=True).stdout.strip()
    need(base != "", "no merge-base with box/dell2")
    changed = [x for x in subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=str(root), capture_output=True, text=True).stdout.splitlines() if x.strip()]
    extra = [x for x in changed if not any(x.startswith(a) for a in (FOLDER, CHANNEL, ORDER))]
    need(not extra, "files outside the grant changed: " + ", ".join(extra[:5]))


ARMS = {"DBC150-1-AC1": ac_1, "DBC150-1-AC2": ac_2, "DBC150-1-AC3": ac_3}


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
