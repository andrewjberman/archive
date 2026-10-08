"""TO-DB-b-44 -- FWD-8's split Black Diamond pull: its OFFLINE plan and its live runner (the live run is the issuer's act).

Word: Andrew's per-use word relayed by 0.0.0_AB_MSTR~DELL2 msg 1103 (record @5ef6d33141): ONE read-only pull, 2,299 accounts, 2,299
calls, 4,598 date ranges, nothing wider. Ordered by 1.0.0_SA_CTO~DELL2 round-19 analysis @b402b7b2e3 section 2: each closure segment is
asked as TWO ranges, (segment start .. 2025-01-08) and (2025-01-10 .. segment end), so Black Diamond's own figure either side of the
2025-01-09 closure can be compared with Opal's. ONE call per account carries both ranges.

The denominator is `0.9.0_WK_IRPT_DASHBD~14/CLOSURE_ALIGN_E1P.json` rows (one closure segment per account, 2,299 rows).
Round 14's pull (`~6/bd_population_pull_e3.py`: map_account, load_xref, _address, the bd_adapter request body) and its concurrent
coordinator (`~8/bd_population_concurrent_e3.py`: shared bearer, pace, ramp, 429 halving, one retry, FAILED, abort, checkpoint, the
sweep refusal) are imported by path and reused; nothing of either is copied.

Usage: python bd_split_pull.py <repo_root> plan | run --go | sweep --go
  plan   OFFLINE (DRY_RUN=1, S3 list and read only). Maps each account with round 14's mapping, builds ONE request body with the two
         split ranges through bd_adapter.build_period_request, picks a NEW `pull=` token (refused if already landed), lists the
         `pull=` prefixes already under the round-14 landing template, writes SPLIT_PULL_PLAN.json and prints both denominators.
  run    LIVE, needs --go, the issuer's, never the worker that built it. Refuses unless --go is given, the plan exists with exactly
         2,299 requests and 4,598 ranges and no unmapped account, the plan's ruling is round 14's, the plan re-derives identically
         from a fresh S3 read, and nothing is landed yet under the plan's pull. Runs the plan through the concurrent coordinator and
         lands each 200 at its plan landing key. Writes SPLIT_PULL_RUN.json (checkpointed). Never logs a credential, bearer or body.
  sweep  LIVE, needs --go, the issuer's. The run record's FAILED set once more, under the same rules, inside the same 2,299.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
RECORD_PATH = DELIV / "0.9.0_WK_IRPT_DASHBD~14" / "CLOSURE_ALIGN_E1P.json"
B20_PATH = DELIV / "0.9.0_WK_IRPT_DASHBD~6" / "bd_population_pull_e3.py"
CONC_PATH = DELIV / "0.9.0_WK_IRPT_DASHBD~8" / "bd_population_concurrent_e3.py"
PLAN_NAME = "SPLIT_PULL_PLAN.json"
RUN_NAME = "SPLIT_PULL_RUN.json"
SWEEP_NAME = "SPLIT_PULL_SWEEP.json"
WORD = "Andrew per-use word via 0.0.0_AB_MSTR~DELL2 msg 1103; record @5ef6d33141; order 1.0.0_SA_CTO~DELL2 round-19 analysis @b402b7b2e3 section 2"
PULL = "split20261007"  # a NEW pull= token: not a YYYYMMDD of round 14's landings, so it can never share a prefix with them
LEFT_END, RIGHT_START = "2025-01-08", "2025-01-10"  # the closure is 2025-01-09
EXPECTED_REQUESTS, EXPECTED_RANGES = 2299, 4598
_KEY_RE = re.compile(r"(?:^|/)acct=(\d+)\.json$")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_b20():
    """Round 14's pull script, imported by path."""
    return _load(B20_PATH, "bd_population_pull_e3_split_imported")


def load_conc():
    """Round 14's concurrent coordinator, imported by path."""
    return _load(CONC_PATH, "bd_population_concurrent_e3_split_imported")


def split_ranges(segment):
    return [{"start": segment["start"], "end": LEFT_END}, {"start": RIGHT_START, "end": segment["end"]}]


def _canon(obj):
    return json.loads(json.dumps(obj, sort_keys=True))


def _prefix_of(b20, on):
    base = b20._address(on, "x", 0)
    bucket, key = base[len("s3://"):].split("/", 1)
    return bucket, key.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/"  # the reporting_performance/ prefix above every pull=


def list_existing_pulls(s3, on, b20):
    """The `pull=` tokens already landed under the round-14 landing template. S3 LIST reads only; paginated."""
    bucket, prefix = _prefix_of(b20, on)
    tokens = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("pull="):
                tokens.add(seg[len("pull="):])
    return sorted(tokens)


def list_landed_under(s3, on, b20, pull):
    """The bd internal ids already landed under pull=<pull>. S3 LIST reads only."""
    base = b20._address(on, pull, 0)
    bucket, key = base[len("s3://"):].split("/", 1)
    prefix = key.rsplit("/", 1)[0] + "/"
    ids = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            m = _KEY_RE.search(o["Key"])
            if m:
                ids.add(m.group(1))
    return ids


def derive_plan(rows, xref, xref_key, existing, pull, on, b20, bd_adapter, route_describe):
    """Pure: the same inputs give the same plan. One request per account, two split ranges, a builder landing key."""
    if pull in existing or ("pull=" + pull) in existing:
        raise SystemExit("ERROR: pull token %r is already landed under the round-14 landing template; choose a new one" % pull)
    reqs, unmapped, resolved, by_bd = [], [], {}, {}
    seen = set()
    for r in rows:
        a = r["account"]
        if a in seen:
            raise SystemExit("ERROR: account %s appears twice in the record; one call per account" % a)
        seen.add(a)
        bd, why = b20.map_account(a, xref)
        if bd is None:
            unmapped.append({"account": a, "reason": why})
        else:
            resolved[a] = bd
            by_bd.setdefault(bd, []).append(a)
    for bd, accs in by_bd.items():  # two accounts onto one id would share one landing key: never guess which
        if len(accs) > 1:
            for a in accs:
                del resolved[a]
                unmapped.append({"account": a, "reason": "bd internal id %d is shared by %d accounts; refusing to guess" % (bd, len(accs))})
    unmapped.sort(key=lambda u: u["account"])
    for r in rows:
        a = r["account"]
        if a not in resolved:
            continue
        bd, seg = resolved[a], r["segment"]
        ranges = split_ranges(seg)
        body, _idx = bd_adapter.build_period_request(int(bd), seg["start"], seg["end"], seg["start"], int(seg["end"][:4]), "Cumulative")
        body["parameters"]["dateRanges"] = [
            {"endDate": g["end"], "name": "Custom", "startDate": g["start"], "type": "Custom"} for g in ranges]
        body["parameters"]["asOfDate"]["asOfDate"] = seg["end"]
        reqs.append({"account": a, "bd_account": str(bd), "ranges": ranges, "body": body,
                     "landing_key": b20._address(on, pull, bd)})
    sha = hashlib.sha256(json.dumps([q["body"] for q in reqs], sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"word": WORD, "dry_run": True, "vendor_calls": 0, "pull": pull, "existing_pull_prefixes": list(existing),
            "route": route_describe, "xref_partition": xref_key, "record_rows": len(rows), "planned": len(reqs),
            "unmapped": unmapped, "range_count": sum(len(q["ranges"]) for q in reqs),
            "request_bodies_sha256": sha, "request_list": reqs}


def print_denominators(plan):
    print("denominators: record rows %d = planned %d + unmapped %d" % (plan["record_rows"], plan["planned"], len(plan["unmapped"])))
    print("requests %d, ranges %d, accounts %d, pull=%s, existing pull prefixes %d" % (
        len(plan["request_list"]), plan["range_count"], len({q["account"] for q in plan["request_list"]}), plan["pull"],
        len(plan["existing_pull_prefixes"])))


def check_plan_counts(plan):
    """The run's refusal on a widened (or short) plan: exactly 2,299 requests, 4,598 ranges, nothing unmapped."""
    reqs = plan.get("request_list") or []
    ranges = sum(len(q.get("ranges") or []) for q in reqs)
    if len(reqs) != EXPECTED_REQUESTS or ranges != EXPECTED_RANGES or plan.get("unmapped"):
        raise SystemExit("ERROR: the plan holds %d requests / %d ranges / %d unmapped; the word is for exactly %d and %d: refusing to call" % (
            len(reqs), ranges, len(plan.get("unmapped") or []), EXPECTED_REQUESTS, EXPECTED_RANGES))
    if len({q["account"] for q in reqs}) != len(reqs):
        raise SystemExit("ERROR: an account is planned twice; one call per account")


def refusal_checks(out_dir, argv, mode, conc):
    """Every refusal that needs no network. Returns the written plan."""
    if len(argv) < 4 or argv[2] != mode or "--go" not in argv:
        raise SystemExit("ERROR: live mode needs: %s --go" % mode)
    pp = out_dir / PLAN_NAME
    if not pp.is_file():
        raise SystemExit("ERROR: no plan %s; run plan first" % PLAN_NAME)
    written = json.loads(pp.read_text(encoding="utf-8"))
    check_plan_counts(written)
    if written.get("ruling") != conc.RULING:
        raise SystemExit("ERROR: the plan's ruling object is absent or differs from round 14's batches 249/250; re-run plan")
    return written


class PlanLanding:
    """Stands in for round 14's address module inside the coordinator: every landing is the PLAN's landing key for that account
    (verbatim builder output recorded in the plan), never a key composed at run time."""

    def __init__(self, plan):
        self.keys = {str(q["bd_account"]): q["landing_key"] for q in plan["request_list"]}

    def _address(self, on, pull, bd):
        return self.keys[str(bd)]


def _live_env(root):
    os.environ["DRY_RUN"] = "1"
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    b20, conc = load_b20(), load_conc()
    s3 = boto3.client("s3", region_name="us-east-1")
    return b20, conc, on, s3


def build_live_plan(root, b20, conc, on, s3, pull=PULL):
    sys.path.insert(0, str(root / "lib"))
    perf = str(root / "infra/aws/lambda/investor-reporting/performance")
    sys.path.insert(0, perf)
    import bd_adapter
    from tenants import verification_route_for, _LEGACY_SHORT_ID
    route = verification_route_for(_LEGACY_SHORT_ID["49F"])
    rows = json.loads(RECORD_PATH.read_bytes().decode("utf-8"))["rows"]
    xref, xref_key = b20.load_xref()
    existing = list_existing_pulls(s3, on, b20)
    plan = derive_plan(rows, xref, xref_key, existing, pull, on, b20, bd_adapter, route.describe())
    plan["ruling"] = json.loads(json.dumps(conc.RULING))
    return plan


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    root = Path(argv[1]).resolve()
    mode = argv[2] if len(argv) > 2 else ""
    out_dir = HERE
    if mode == "plan":
        b20, conc, on, s3 = _live_env(root)
        plan = build_live_plan(root, b20, conc, on, s3)
        (out_dir / PLAN_NAME).write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print_denominators(plan)
        print("vendor_calls %d dry_run %s" % (plan["vendor_calls"], plan["dry_run"]))
        print("request_bodies_sha256", plan["request_bodies_sha256"])
        for u in plan["unmapped"]:
            print("UNMAPPED", u["account"], u["reason"])
        return 0
    if mode not in ("run", "sweep"):
        raise SystemExit("ERROR: mode must be plan | run --go | sweep --go")
    conc = load_conc()
    written = refusal_checks(out_dir, argv, mode, conc)
    b20, conc, on, s3 = _live_env(root)
    fresh = build_live_plan(root, b20, conc, on, s3, pull=written["pull"]) if written["pull"] not in list_existing_pulls(s3, on, b20) \
        else None
    landed = list_landed_under(s3, on, b20, written["pull"])
    by_bd = {str(q["bd_account"]): q for q in written["request_list"]}
    if mode == "run":
        if landed:
            raise SystemExit("ERROR: %d account(s) already landed under pull=%s; this is the ONE pull, refusing to call" % (
                len(landed), written["pull"]))
        if fresh is None or _canon(fresh) != written:
            raise SystemExit("ERROR: the re-derived plan differs from the written plan; re-run plan, refusing to call")
        todo, target = [by_bd[b] for b in sorted(by_bd, key=int)], out_dir / RUN_NAME
    else:
        last = out_dir / RUN_NAME
        if not last.is_file():
            raise SystemExit("ERROR: no run record %s; nothing to sweep" % RUN_NAME)
        failed = json.loads(last.read_text(encoding="utf-8")).get("failed", [])
        conc.check_sweep_set(failed, written["ruling"]["failed_cap"])
        if any(str(f["bd_account"]) not in by_bd for f in failed):
            raise SystemExit("ERROR: a FAILED account is outside the plan's 2,299; refusing to call")
        todo = [by_bd[str(f["bd_account"])] for f in failed if str(f["bd_account"]) not in landed]
        print("sweep: FAILED set %d, still unlanded %d" % (len(failed), len(todo)))
        for f in failed:
            print("FAILED", f["account"], f["bd_account"], f["class"])
        target = out_dir / SWEEP_NAME
    for q in todo:
        q.setdefault("segments", q["ranges"])  # the coordinator counts a request's ranges as `segments`
    print_denominators(written)
    h = conc._lift_dry(root)
    conc._roll(target)
    path = written["route"]["paths"]["performancePeriod"]
    rec = conc.run_concurrent(todo, path, h, s3, on, PlanLanding(written), written["ruling"], landed_set=landed,
                              checkpoint=conc._writer(target))
    print("denominators: planned %d = landed before %d + landed this %s %d + FAILED %d + not requested %d + other %d" % (
        written["planned"], len(landed), mode, rec["landed_this_run"], rec["failed_count"], rec["not_requested"],
        len(todo) - rec["landed_this_run"] - rec["failed_count"] - rec["not_requested"]))
    if mode == "sweep":
        print("residue: %d account(s) still FAILED" % rec["failed_count"])
    print(json.dumps({k: rec[k] for k in ("vendor_calls", "bearer_mints", "landed_this_run", "failed_count", "aborted",
                                          "ramped", "workers_target")}, indent=1))
    return 1 if rec["aborted"] else 0


if __name__ == "__main__":
    sys.exit(main())
