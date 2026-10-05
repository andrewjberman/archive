"""TO-DB-b-21 -- the completion mode of the ONE Black Diamond population pull (E3 / P-5): the complement only, the bearer re-minted.

Ruled by 1.0.0_SA_CTO RULINGS batch 248 (msg 105044): the completion run over the accounts not yet answered IS the same pull. It
requests only the complement of what is already landed, prints both denominators, and re-mints the ClientView bearer before the
measured expiry (the first bearer died after 18 calls; this script re-mints every MINT_EVERY = 10 calls). The DB-b-20 script
(bd_population_pull_e3.py) is imported by path and its address builder, plan name and transient set are reused, never copied.

Usage: python bd_population_complete_e3.py <repo_root> plan | run --go
  plan  OFFLINE (DRY_RUN=1, S3 list reads only). Reads the DB-b-20 plan, lists the landed keys under pull=20261004, writes
        BD_POPULATION_COMPLETION_PLAN_E3.json (requests_planned, landed, landed_accounts, complement, complement_accounts,
        vendor_calls 0, dry_run) and prints both denominators.
  run   LIVE, needs --go, and is run by the issuer, never by the worker that built it. Refuses unless: --go is given; the
        completion plan exists and is re-derived identically from a fresh S3 listing; E3_SHAPE_RULING.json exists in the DB-b-20
        folder (its pace_rps is the pace). Then it requests ONLY the complement accounts, each once, re-mints the bearer every
        10 calls, retries one transient error per run, aborts the whole run on the first non-transient error (a 401 directly
        after a fresh mint is a stop, never a retry), lands each response at the builder's address, and writes
        BD_POPULATION_COMPLETION_E3.json. A credential, cookie or token is never written or printed.
"""
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
B20_DIR = HERE.parent / "0.9.0_WK_IRPT_DASHBD~6"
B20_SCRIPT = "bd_population_pull_e3.py"
PULL_DATE = "20261004"  # the ONE pull's partition: the completion lands beside the 19 already there
MINT_EVERY = 10
COMPLETION_PLAN_NAME = "BD_POPULATION_COMPLETION_PLAN_E3.json"
COMPLETION_NAME = "BD_POPULATION_COMPLETION_E3.json"
_KEY_RE = re.compile(r"(?:^|/)acct=(\d+)\.json$")


def load_b20():
    """The DB-b-20 script, imported by path (importlib); nothing of it is copied."""
    spec = importlib.util.spec_from_file_location("bd_population_pull_e3_imported", str(B20_DIR / B20_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def list_landed(s3, on, b20):
    """The bd internal ids already landed under pull=PULL_DATE: S3 LIST reads only, paginated, parsed from acct=<id>.json keys."""
    base = b20._address(on, PULL_DATE, 0)
    bucket, key = base[len("s3://"):].split("/", 1)
    prefix = key.rsplit("/", 1)[0] + "/"
    ids = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            m = _KEY_RE.search(o["Key"])
            if m:
                ids.add(m.group(1))
    return ids


def derive_plan(e20_plan, landed_ids):
    """The completion plan: the DB-b-20 request list minus the landed set. Pure; the same inputs give the same plan."""
    reqs = e20_plan["request_list"]
    plan_ids = [str(r["bd_account"]) for r in reqs]
    in_plan = set(plan_ids)
    landed_in_plan = sorted(in_plan & set(landed_ids), key=int)
    comp = [b for b in plan_ids if b not in set(landed_in_plan)]
    return {"word": e20_plan.get("word"), "dry_run": 1, "vendor_calls": 0, "pull": "pull=" + PULL_DATE,
            "requests_planned": len(reqs), "request_bodies_sha256": e20_plan["request_bodies_sha256"],
            "landed": len(landed_in_plan), "landed_accounts": landed_in_plan,
            "landed_outside_plan": sorted(set(landed_ids) - in_plan, key=int),
            "complement": len(comp), "complement_accounts": comp}


def print_denominators(plan):
    print("denominators: planned %d = landed %d + complement %d" % (plan["requests_planned"], plan["landed"], plan["complement"]))
    print("denominators: landed accounts %d, complement accounts %d, landed keys outside the plan %d" % (
        len(plan["landed_accounts"]), len(plan["complement_accounts"]), len(plan["landed_outside_plan"])))


def _canon(obj):
    return json.loads(json.dumps(obj, sort_keys=True))


def refusal_checks(out_dir, b20_dir, argv):
    """Every refusal that needs no network. Returns (parsed completion plan, shape ruling)."""
    if len(argv) < 3 or argv[2] != "run" or "--go" not in argv:
        raise SystemExit("ERROR: live mode needs: run --go")
    cp = out_dir / COMPLETION_PLAN_NAME
    if not cp.is_file():
        raise SystemExit("ERROR: no completion plan %s; run plan first" % COMPLETION_PLAN_NAME)
    rp = b20_dir / "E3_SHAPE_RULING.json"
    if not rp.is_file():
        raise SystemExit("ERROR: E3_SHAPE_RULING.json missing in %s; the CTO's shape ruling is required" % b20_dir)
    ruling = json.loads(rp.read_text(encoding="utf-8"))
    if not ruling.get("pace_rps"):
        raise SystemExit("ERROR: E3_SHAPE_RULING.json must name pace_rps")
    float(ruling["pace_rps"])
    return json.loads(cp.read_text(encoding="utf-8")), ruling


def _status_of(exc):
    msg = str(exc)
    return int(msg.split("HTTP ")[1].split(":")[0]) if "HTTP " in msg else -1


def run_complement(e20_plan, plan, h, s3, on, b20, ruling, sleep=time.sleep, clock=time.monotonic):
    """Request ONLY plan['complement_accounts'], each once. Returns the completion record (the caller writes it)."""
    path = e20_plan["route"]["paths"]["performancePeriod"]
    interval = 1.0 / float(ruling["pace_rps"])
    by_bd = {str(r["bd_account"]): r for r in e20_plan["request_list"]}
    landed_set = set(plan["landed_accounts"])
    todo = [by_bd[b] for b in plan["complement_accounts"]]
    if any(str(r["bd_account"]) in landed_set for r in todo) or len(todo) != plan["complement"]:
        raise SystemExit("ERROR: the complement overlaps the landed set or its count is wrong")
    retries_left, aborted, stop_reason = 1, None, None
    mints, calls_since_mint, calls, last_t = 0, 0, 0, 0.0
    token = None
    records, seen = [], set()
    for r in todo:
        bd = str(r["bd_account"])
        if bd in seen:
            raise SystemExit("ERROR: account %s requested twice" % bd)
        seen.add(bd)
        rec = {"account": r["account"], "bd_account": bd, "ranges": len(r["segments"])}
        while True:
            if token is None or calls_since_mint >= MINT_EVERY:  # re-mint BEFORE the call, never after the expiry
                token = h.get_clientview_token(h.load_bd_session())
                mints += 1
                calls_since_mint = 0
            wait = last_t + interval - clock()
            if wait > 0:
                sleep(wait)
            last_t = clock()
            fresh = calls_since_mint == 0
            calls += 1
            calls_since_mint += 1
            try:
                payload = h._request("POST", path, token=token, body=r["body"], raw=True)
                rec["http_status"] = 200
                try:  # a landing failure is non-transient and is recorded, so the record always exists
                    json.loads(payload)
                    addr = b20._address(on, PULL_DATE, bd)
                    bkt, key = addr[len("s3://"):].split("/", 1)
                    s3.put_object(Bucket=bkt, Key=key, Body=payload, ContentType="application/json")
                    rec["landed"] = addr
                except Exception as e:
                    rec["error"] = "landing: %s" % type(e).__name__
                    aborted = rec["error"]
                break
            except RuntimeError as e:  # HTTP error from the estate client; only the status code is kept, never the body
                status = _status_of(e)
                rec.update({"http_status": status, "error": "HTTP %d" % status})
                if status == 401 and fresh:
                    stop_reason = "401 directly after a fresh mint: a stop, not a retry"
                    aborted = rec["error"]
                    break
                if status in b20.TRANSIENT_HTTP and retries_left > 0:
                    retries_left -= 1
                    rec["retried"] = True
                    sleep(interval)
                    continue
                aborted = rec["error"]
                break
            except (urllib.error.URLError, OSError, TimeoutError) as e:  # transport error
                rec.update({"http_status": 0, "error": "transport: %s" % type(e).__name__})
                if retries_left > 0:
                    retries_left -= 1
                    rec["retried"] = True
                    sleep(interval)
                    continue
                aborted = rec["error"]
                break
        records.append(rec)
        if aborted:
            break
    return {"word": plan.get("word"), "endpoint": "performancePeriod", "ruling_id": ruling.get("ruling_id"),
            "batch": "1.0.0_SA_CTO RULINGS batch 248 (msg 105044)", "pace_rps": ruling["pace_rps"], "pull": plan["pull"],
            "mint_every_calls": MINT_EVERY, "session_token_mints": mints, "requests_planned": plan["requests_planned"],
            "complement_planned": plan["complement"], "vendor_calls": calls, "aborted": aborted, "stop_reason": stop_reason,
            "retries_used": 1 - retries_left, "landed_this_run": sum(1 for x in records if x.get("landed")),
            "plan_sha256": plan["request_bodies_sha256"], "records": records,
            "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    root = Path(argv[1]).resolve()
    mode = argv[2] if len(argv) > 2 else ""
    out_dir = HERE
    if mode == "plan":
        os.environ["DRY_RUN"] = "1"
        sys.path.insert(0, str(root))
        from lib import opal_naming as on
        import boto3
        b20 = load_b20()
        e20 = json.loads((B20_DIR / b20.PLAN_NAME).read_text(encoding="utf-8"))
        s3 = boto3.client("s3", region_name="us-east-1")
        plan = derive_plan(e20, list_landed(s3, on, b20))
        (out_dir / COMPLETION_PLAN_NAME).write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print_denominators(plan)
        print("vendor_calls %d dry_run %d" % (plan["vendor_calls"], plan["dry_run"]))
        return 0
    written, ruling = refusal_checks(out_dir, B20_DIR, argv)
    os.environ["DRY_RUN"] = "1"
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    b20 = load_b20()
    e20 = json.loads((B20_DIR / b20.PLAN_NAME).read_text(encoding="utf-8"))
    s3 = boto3.client("s3", region_name="us-east-1")
    plan = derive_plan(e20, list_landed(s3, on, b20))
    if _canon(plan) != written:
        raise SystemExit("ERROR: the re-derived completion plan differs from the written plan; re-run plan, refusing to call")
    print_denominators(plan)
    # The estate client refuses egress while DRY_RUN=1; lift it only here, after every refusal passed.
    os.environ["DRY_RUN"] = "0"
    sys.path.insert(0, str(root / "infra/aws/lambda/investor-reporting/performance"))
    import bd_adapter
    h = bd_adapter.load_bd_helpers(force=True)
    if h.DRY_RUN:
        raise SystemExit("ERROR: helper still DRY")
    rec = run_complement(e20, plan, h, s3, on, b20, ruling)
    done = out_dir / COMPLETION_NAME
    if done.exists():  # an earlier (aborted) record is kept, never overwritten
        done.rename(out_dir / ("BD_POPULATION_COMPLETION_E3.%s.json" % datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")))
    done.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"vendor_calls": rec["vendor_calls"], "mints": rec["session_token_mints"], "aborted": rec["aborted"],
                      "retries_used": rec["retries_used"], "landed_this_run": rec["landed_this_run"]}, indent=1))
    return 1 if rec["aborted"] else 0


if __name__ == "__main__":
    sys.exit(main())
