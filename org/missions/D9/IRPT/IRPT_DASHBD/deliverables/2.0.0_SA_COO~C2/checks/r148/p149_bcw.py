"""IRPT_DASHBD round 148, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the labelled TEST READ of the real Cottonwood publish through the page, cell DB-c-27 (read only; counts only).

  DBC149-1-AC1 the record's `python_truth` equals a FRESH read-only measurement made by this checker over the published prefix, and the page-side counts agree with it
               (every document read, none refused, none threw, the accounts printing the sentence equal the accounts with a non-empty list, no income coerced to zero)
  DBC149-1-AC2 the hygiene: no account identifier in the record or anywhere in the worker's folder, zero writes and invokes, no downloaded object left behind, only the worker's folder, the channel and its order changed

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
The checker's own read is S3 list_objects_v2 and get_object on the one prefix, through python boto3, region us-east-1; it prints counts only, never a key or a value.
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

BUCKET = "opal-data-cottonwood"
PREFIX = "irpt/cottonwood/platinum/reporting/"
FOLDER = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~419/"
RECORD = FOLDER + "TEST_READ_R148.json"
ID_RE = re.compile(r"z\d{8,}|account=|household", re.I)
ALLOWED = (FOLDER, "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md",
           "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-c-27.")


def truth(deadline=95):
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    keys, token, lists = [], None, 0
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
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
        return gzip.decompress(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())

    def man(k):
        return s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()

    with ThreadPoolExecutor(16) as ex:
        raws = list(ex.map(get, series))
        mans = list(ex.map(man, manifests))
    need(time.time() - t0 < deadline, "the fresh read took too long")
    out = {"objects_series": len(series), "objects_manifest": len(manifests), "objects_other": len(keys) - len(series) - len(manifests),
           "docs_total": 0, "docs_parse_ok": 0, "pair_present": 0, "pair_absent": 0, "nonempty_lists": 0, "total_listed_days": 0,
           "max_list_len": 0, "income_all_null_docs": 0, "income_any_number_docs": 0, "income_claim_present_docs": 0,
           "history_scope_counts": {}, "calendar_source_counts": {}}
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
    for raw in mans:
        try:
            m = json.loads(raw)
        except Exception:
            continue
        cs = str(m.get("calendar_source", "ABSENT"))
        out["calendar_source_counts"][cs] = out["calendar_source_counts"].get(cs, 0) + 1
    return out, lists, len(series) + len(manifests)


def ac_1(root):
    rec = p114.load(Path(root), RECORD)
    need(rec.get("claim") == "measured" and "TEST READ" in str(rec.get("label", "")), "the record is not labelled a TEST READ with claim measured")
    fresh, _, _ = truth()
    mine = rec["python_truth"]
    diff = [k for k in fresh if fresh[k] != mine.get(k)]
    need(not diff, "the record's python_truth differs from a fresh read in: " + ", ".join(diff))
    pg = rec["page"]
    need(fresh["docs_total"] > 0 and fresh["docs_parse_ok"] == fresh["docs_total"], "a published document did not parse")
    need(pg["read_ok"] == fresh["docs_total"] and pg["read_refused"] == 0, "the page reader refused or missed a document: %s" % json.dumps(pg))
    need(pg["performance_view_threw"] == 0, "performanceView threw on a document")
    need(pg["accounts_printing_sentence"] == fresh["nonempty_lists"], "accounts printing the sentence %s != accounts with a non-empty list %s" % (pg["accounts_printing_sentence"], fresh["nonempty_lists"]))
    need(pg["income_coerced_to_zero"] == 0, "the page coerced an income null to zero")
    need(pg["sentence_n_mismatch"] == 0, "a printed count differs from the length of the served list")


def ac_2(root):
    root = Path(root)
    folder = root / FOLDER
    need(folder.is_dir(), "the worker's folder is absent")
    for f in folder.rglob("*"):
        if f.is_file():
            need(not f.name.endswith((".gz", ".parquet")), "a downloaded object is left behind: " + f.name)
            if f.suffix.lower() in (".json", ".md", ".ts", ".tsx", ".py", ".txt"):
                need(ID_RE.search(f.read_text(encoding="utf-8", errors="replace")) is None, "an identifier-like token is in " + f.name)
    rec = p114.load(root, RECORD)
    reads = rec["reads"]
    need(reads["writes"] == 0 and reads["invokes"] == 0, "the record reports a write or an invoke")
    need(rec["pushed"] is False and rec["deployed"] is False and rec["ids_recorded"] is False, "pushed, deployed or ids_recorded is not false")
    base = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], cwd=str(root), capture_output=True, text=True).stdout.strip()
    need(base != "", "no merge-base with box/dell2")
    changed = [x for x in subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=str(root), capture_output=True, text=True).stdout.splitlines() if x.strip()]
    extra = [x for x in changed if not any(x.startswith(a) for a in ALLOWED)]
    need(not extra, "files outside the grant changed: " + ", ".join(extra[:5]))


ARMS = {"DBC149-1-AC1": ac_1, "DBC149-1-AC2": ac_2}


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
