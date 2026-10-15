"""IRPT_DASHBD round 117, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the apply of the signed Cottonwood holdings_performance pair by 0.7.0_AE_CloudOps~DB2.

  DBC117-1-AC1 the gates, the shared-zip build (members differ from the live zip by handler.py only), the ledger and the plan (adds only the Cottonwood set; changes only the two shared-zip functions)
  DBC117-2-AC1 the 12-date catch-up: exactly the packet's 36 keys landed in the apply window, schema 1.2, nothing else moved, and the 1.1+1.2 reader check
  DBC117-3-AC1 the live state: the three functions share one CodeSha256 that equals the built zip, the Cottonwood role matches *-cot-*, the schedule is ENABLED at cron(15 8 ? * MON-FRI *) America/New_York
               on the Cottonwood function, and the planted listing test passes

The checker RECOMPUTES from fresh AWS and S3 reads (get_function_configuration, get_schedule, head/get/list) and the repo; it writes nothing.
Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import datetime as dt
import importlib.util
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

REC = p114.D + "0.7.0_AE_CloudOps~DB2/COTTONWOOD_APPLY_RECORD.json"
PACKET = p114.D + "0.9.0_WK_IRPT_DASHBD~403/NEVER_WIDEN_PACKET_DB-c-5_R115.md"
BLOB = "ad049d506cdb22d4fd729b85ef206a548aa4a6d2"
COO_HALF = p114.D + "2.0.0_SA_COO~C2/NEVER_WIDEN_DB-c-5_R115_COTTONWOOD_HOLDINGS_PERFORMANCE_COO_HALF.md"
CTO_HALF = p114.D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_DB-c-5_R115_COTTONWOOD_HOLDINGS_PERFORMANCE_CTO_HALF.md"
FN_49F = "irpt-holdings-performance-lambda"
FN_INF = "irpt-inf-holdings-performance-lambda"
FN_COT = "irpt-cot-holdings-performance-lambda"
SCHED = "irpt-cot-holdings-performance-daily"
ROLE = "irpt-cot-holdings-performance-role"
SHARED_CHANGES = ["module.irpt_holdings_performance.aws_lambda_function.this", "module.irpt_holdings_performance_inf.aws_lambda_function.this"]
READERS = ["data/assets/scripts/gold/irpt_reporting/account_return_daily.py", "infra/aws/lambda/investor-reporting/reporting-gold/handler.py", "infra/aws/lambda/investor-reporting/performance/holdings_gold.py"]
REGION = "us-east-1"


def clean(rec):
    """The record carries hashes, slugs, keys and addresses, so the digit-run rule applies to the words fields only."""
    for k, v in p114.walk(rec):
        if isinstance(v, str) and k in ("words", "basis_words", "note"):
            need(not p114.LONG_DIGITS.search(v), "a run of 8 or more digits in field " + k)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, encoding="utf-8")
    need(r.returncode == 0, "git " + " ".join(args[:2]) + " failed: " + r.stderr[:120])
    return r.stdout.strip()


def keys_for(naming, dates):
    out = []
    for d in dates:
        out.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_daily", "date=" + d, "data.parquet"))
        for o in ("data.parquet", "manifest.json"):
            out.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_manifest", "date=" + d, o))
    return out


def split(uri):
    m = re.match(r"s3://([^/]+)/(.*)$", uri)
    return m.group(1), m.group(2)


def ac_1(root):
    r = p114.load(root, REC)
    clean(r)
    g = r["gates"]
    need(git(root, "hash-object", PACKET) == BLOB == g["packet_blob"], "the packet blob is not the signed one")
    for half in (COO_HALF, CTO_HALF):
        t = (Path(root) / half).read_text(encoding="utf-8")
        need("ad049d506c" in t and "SIGNED" in t, "a half does not read SIGNED at the blob: " + half)
    need(g["coo_half_signed"] is True and g["cto_half_signed"] is True, "halves not recorded signed")
    need(g["role_name_matches_cot"] is True and re.fullmatch(r".*-cot-.*", ROLE) is not None, "the role name does not match *-cot-*")
    need(g["shared_zip_roles_carry_listing_grant"] is True, "step 0 (the 49F and INF roles carry the gold-listing grant) is not recorded")
    b = r["build"]
    need(b["upload_member_diff"] == ["handler.py"], "the built zip differs from the live zip by more than handler.py: " + str(b["upload_member_diff"]))
    need(b["built_equals_landed"] is True, "the landed zip is not the built zip")
    cands = list((Path(root) / "org/critical_paths/change_management").glob("*" + r["ledger_entry"] + "*"))
    need(len(cands) >= 1, "the ledger entry is absent: " + r["ledger_entry"])
    lt = cands[0].read_text(encoding="utf-8", errors="replace")
    need("shared zip" in lt.lower() or "shared-zip" in lt.lower(), "the ledger does not name the shared zip")
    pl = r["plan"]
    need(pl["destroy"] == 0 and pl["change_addresses"] == SHARED_CHANGES and pl["change"] == 2, "the plan changes are not exactly the two shared-zip functions")
    need(len(pl["add_addresses"]) == pl["add"] and pl["add"] > 0, "the plan add count differs from its list")
    need(all("irpt_holdings_performance_cot" in a or a.startswith("module.irpt_holdings_performance_cot.") for a in pl["add_addresses"]), "the plan adds a resource outside the Cottonwood set")
    need(pl["replan_no_changes"] is True, "the post-apply plan did not read No changes")
    rd = r["reads"]
    need(rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "vendor call or secret read")


def ac_2(root):
    naming, cal = p114.lib(root)
    r = p114.load(root, REC)
    clean(r)
    c = r["catch_up"]
    dates = c["dates"]
    need(len(dates) >= 1 and dates == sorted(dates) and all(cal.is_trading_day(p114.iso(d)) for d in dates), "catch-up dates are not ascending trading days")
    need(all(e["date"] == "2026-06-09" for e in c["excluded"]), "an exclusion other than 2026-06-09")
    s3 = p114.s3client()
    sd = p114.list_dates(s3, p114.SILVER_BUCKET, p114.SILVER_PREFIX)
    need(all(d in sd for d in dates), "a catch-up date has no silver partition")
    gb, gp = p114.gold_prefix(naming, "holdings_performance_daily")
    mb, mp = p114.gold_prefix(naming, "holdings_performance_manifest")
    keys = keys_for(naming, dates)
    need(c["keys"] == keys and c["count"] == len(keys) == 3 * len(dates), "recorded keys differ from the builder's addresses")
    start = dt.datetime.strptime(r["apply_started_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    for k in keys:
        b, key = split(k)
        h = s3.head_object(Bucket=b, Key=key)
        need(h["LastModified"] >= start, "a catch-up key predates the apply window: " + key)
    for d in dates:
        body = json.loads(s3.get_object(Bucket=mb, Key=mp + "date=" + d + "/manifest.json")["Body"].read().decode("utf-8"))
        need(str(body.get("schema_version")) == "1.2", "manifest schema is not 1.2 for " + d)
    landed = set()
    for (b, pfx) in ((gb, gp), (mb, mp)):
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=pfx):
            for o in page.get("Contents", []):
                if o["LastModified"] >= start:
                    landed.add("s3://" + b + "/" + o["Key"])
    need(landed == set(keys), "objects written in the window differ from the 36 keys: extra %d, missing %d" % (len(landed - set(keys)), len(set(keys) - landed)))
    rc = r["reader_check"]
    need(sorted(x["file"] for x in rc["readers"]) == sorted(READERS) and all((Path(root) / f).is_file() for f in READERS), "the reader set is not the three known readers")
    need(all(x["v11"] == "clean" and x["v12"] == "clean" for x in rc["readers"]), "a reader did not read both schemas clean")
    for tag, key in (("v11_date", "1.1"), ("v12_date", "1.2")):
        d = rc[tag]
        body = json.loads(s3.get_object(Bucket=mb, Key=mp + "date=" + d + "/manifest.json")["Body"].read().decode("utf-8"))
        need(str(body.get("schema_version")) == key, "partition %s is not schema %s" % (d, key))


def ac_3(root):
    r = p114.load(root, REC)
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    sch = boto3.client("scheduler", region_name=REGION)
    shas = {}
    for fn in (FN_49F, FN_INF, FN_COT):
        shas[fn] = lam.get_function_configuration(FunctionName=fn)
    need(len({v["CodeSha256"] for v in shas.values()}) == 1, "the three functions do not share one CodeSha256")
    need(shas[FN_COT]["CodeSha256"] == r["build"]["live_codesha256_after"], "the live CodeSha256 differs from the recorded one")
    need(re.fullmatch(r".*role/.*-cot-.*", shas[FN_COT]["Role"]) is not None and shas[FN_COT]["Role"].endswith("/" + ROLE), "the Cottonwood function's role is not " + ROLE)
    s = sch.get_schedule(Name=SCHED)
    need(s["State"] == "ENABLED" and s["ScheduleExpression"] == "cron(15 8 ? * MON-FRI *)" and s.get("ScheduleExpressionTimezone") == "America/New_York", "the schedule is not ENABLED at cron(15 8 ? * MON-FRI *) America/New_York")
    need(s["Target"]["Arn"].endswith(":function:" + FN_COT), "the schedule does not target the Cottonwood function")
    need("blackdiamond_z09" in s["Target"].get("Input", ""), "the schedule input does not name blackdiamond_z09")
    t = subprocess.run([sys.executable, "-m", "pytest", str(Path(root) / "infra/aws/lambda/investor-reporting/holdings-performance/tests/test_refused_listing_fails_loud.py"), "-q", "-p", "no:cacheprovider"], capture_output=True, text=True, cwd=str(root), timeout=110)
    need(t.returncode == 0 and re.search(r"\d+ passed", t.stdout) is not None, "the planted listing test did not pass")
    en = r["enable"]
    need(en["plan"] == {"add": 0, "change": 1, "destroy": 0} and en["after_read_before_enable"] is True, "the enable step is not a 0/1/0 plan after the after-read")
    need(r["ledger_closed"] is False, "the ledger was closed; the issuer closes it after the first scheduled fire")


ARMS = {"DBC117-1-AC1": ac_1, "DBC117-2-AC1": ac_2, "DBC117-3-AC1": ac_3}


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
