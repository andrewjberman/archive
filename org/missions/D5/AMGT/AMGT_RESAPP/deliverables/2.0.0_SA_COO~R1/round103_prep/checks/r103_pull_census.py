"""AMGT_RESAPP round-103 PREP -- FWD-40 (c): the per-security PULL CENSUS (PRD v0.44): for each name, which pulls it makes and the time each takes.

  PYTHONPATH=<repo root> python r103_pull_census.py --selftest
  PYTHONPATH=<repo root> python r103_pull_census.py [--names K1,K2] [--limit N] [--shard I/N] [--out FILE.json]

The page calls six routes once a name is chosen (overlay, thesis, peers, coverage, versions, ledger). For each name and route this runs the checkout's OWN handler in-process on the live pool
(GET only, no write) with every botocore call RECORDED (service, operation, bucket, key or prefix, table, milliseconds, bytes returned), and attributes each call to the overlay phase that was
running (an `AMGT_PHASE` line ends a phase, so the calls since the previous line belong to it). A call is CLASSED into the pulls FWD-40 (c) names -- corpus, filings, management, news, price,
scanner -- by its key prefix; a call no rule classes is `other` and is PRINTED with its prefix (never folded into a named class).
What is measured: WHAT each name pulls (calls, objects, bytes) and the local milliseconds of each call. Lambda time is a different instrument (`r102_phase_table.py`, the per-phase lines):
local milliseconds do not transfer (rounds 99, 100 and 103).
Verdict: `R103 PULL CENSUS: RAN <n> of <names> names, <calls> calls, <other> unclassed` -- the census REPORTS.
"""
import argparse
import base64
import contextlib
import io
import json
import re
import statistics
import sys
import time

ROUTES = ("overlay", "thesis", "peers", "coverage", "versions", "ledger")
# FWD-40 (c) names six pulls (corpus, filings, management, news, price, scanner); the classes below are the six PLUS those the page also makes, each named from what the recorder saw
# (a call no rule classes is `other` and is printed with its prefix). The mapping, stated: corpus = the dossier gold, the model block, the pack ledger, the crosswalk, the identity;
# news = the article mention gold and the publication links and the chatter tables; price = the security-metrics rank and price generation and price history; scanner = Bloomberg
# refdata and segments and the classification tables (the fields the scanner slice fills).
PULLS = ("corpus", "filings", "management", "news", "price", "scanner", "posture", "peers", "scores", "drafting", "coverage")
RULES = (
    ("filings", lambda r: "/filings/v1" in r or r.startswith("filings/v1")),
    ("management", lambda r: "/management/v1" in r or r.startswith("management/v1")),
    ("news", lambda r: "article_security_mention" in r or "publication-links" in r or "chatter" in r or "social/v1" in r),
    ("posture", lambda r: "/posture/v1" in r or r.startswith("posture/v1")),
    ("peers", lambda r: "/peers/v1" in r or r.startswith("peers/v1")),
    ("scores", lambda r: "/scores/v1" in r or r.startswith("scores/v1")),
    ("drafting", lambda r: "/drafting/v1" in r or r.startswith("drafting/v1")),
    ("coverage", lambda r: "freshness_snapshot" in r),
    ("price", lambda r: "security-metrics" in r or "price_history" in r),
    ("scanner", lambda r: "bronze/refdata" in r or "bronze/segments" in r or "etf-classifications" in r or "universe/v1" in r),
    ("corpus", lambda r: "research_dossier" in r or "model_block" in r or "/packs/" in r or r.startswith("packs/") or "crosswalk" in r or "identity/v1" in r),
)


def pull_class(resource):
    for name, test in RULES:
        if test(resource):
            return name
    return "other"


class Recorder:
    def __init__(self):
        self.calls = []  # (t_start, service, operation, resource, ms, nbytes)
        self.phases = []  # (t_end, phase)

    def attribute(self):
        """{phase: [call, ...]}: a call belongs to the first phase line printed at or after its start; calls after the last line belong to `after`."""
        out = {}
        ends = sorted(self.phases)
        for call in self.calls:
            phase = "after"
            for t_end, name in ends:
                if call[0] <= t_end:
                    phase = name
                    break
            out.setdefault(phase, []).append(call)
        return out


def resource_of(service, operation, params):
    if service == "s3":
        return "%s/%s" % (params.get("Bucket", ""), params.get("Key") or params.get("Prefix") or "")
    if service == "dynamodb":
        return "table/%s" % (params.get("TableName") or ",".join(sorted((params.get("RequestItems") or {}).keys())))
    return "%s:%s" % (service, operation)


@contextlib.contextmanager
def recording(module):
    import botocore.client

    rec = Recorder()
    real = botocore.client.BaseClient._make_api_call
    real_phase = module._phase_log

    def spy(self, operation_name, api_params):
        t0 = time.monotonic()
        resp = real(self, operation_name, api_params)
        ms = (time.monotonic() - t0) * 1000
        nbytes = 0
        try:
            nbytes = int(resp.get("ContentLength") or 0)
        except (AttributeError, TypeError, ValueError):
            nbytes = 0
        rec.calls.append((t0, self.meta.service_model.service_name, operation_name, resource_of(self.meta.service_model.service_name, operation_name, api_params), ms, nbytes))
        return resp

    def phase(route, name, started):
        rec.phases.append((time.monotonic(), name))
        return real_phase(route, name, started)

    botocore.client.BaseClient._make_api_call = spy
    module._phase_log = phase
    try:
        yield rec
    finally:
        botocore.client.BaseClient._make_api_call = real
        module._phase_log = real_phase


PHASE_RE = re.compile(r"AMGT_PHASE route=overlay phase=(\S+) ms=(\d+)")


def parse_tail(text):
    """{phase: ms, 'handler_ms': n, 'init_ms': n|None} from the log tail of ONE overlay invoke (LogType=Tail returns the last 4 KB of the request's log)."""
    out = {m.group(1): int(m.group(2)) for m in PHASE_RE.finditer(text)}
    dur = re.search(r"REPORT .*?Duration: ([0-9.]+) ms", text)
    init = re.search(r"Init Duration: ([0-9.]+) ms", text)
    out["handler_ms"] = float(dur.group(1)) if dur else None
    out["init_ms"] = float(init.group(1)) if init else None
    return out


def deployed_overlay(lam, key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/overlay" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    resp = lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event).encode(), LogType="Tail")
    return parse_tail(base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace"))


def selftest():
    arms = []

    def arm(name, ok):
        arms.append(ok)
        print("   %s %s" % ("PASS" if ok else "FAIL", name))

    arm("A1 each pull class has a prefix that classes to it",
        [pull_class(r) for r in ("b/amgt/harvest/gold/research_dossier/x", "b/filings/v1/K/x.json", "b/management/v1/K/2026.json",
                                 "b/amgt/harvest/gold/article_security_mention/date=1/p.parquet", "table/opal-harvest-security-metrics",
                                 "b/bloomberg/harvest/bronze/refdata/security_key=K/x", "b/posture/v1/K/x.json", "b/peers/v1/K/x.json", "b/scores/v1/K/x.json",
                                 "b/drafting/v1/K.json", "b/amgt/harvest/state/freshness_snapshot/x")]
        == ["corpus", "filings", "management", "news", "price", "scanner", "posture", "peers", "scores", "drafting", "coverage"])
    arm("A2 an unknown prefix is `other`, never folded into a named class", pull_class("some-bucket/zzz/unknown.bin") == "other")
    rec = Recorder()
    rec.calls = [(1.0, "s3", "GetObject", "b/packs/k/a", 5.0, 10), (2.0, "s3", "GetObject", "b/filings/v1/k/a", 5.0, 10), (9.0, "s3", "ListObjectsV2", "b/x", 1.0, 0)]
    rec.phases = [(1.5, "identity"), (2.5, "feed")]
    att = rec.attribute()
    arm("A3 calls are attributed to the phase line printed at or after them; a later call is `after`",
        sorted(att) == ["after", "feed", "identity"] and att["identity"][0][3] == "b/packs/k/a" and att["feed"][0][3] == "b/filings/v1/k/a")
    t = parse_tail("START RequestId: x\nAMGT_PHASE route=overlay phase=feed ms=182\nAMGT_PHASE route=overlay phase=peers ms=2467\n"
                   "REPORT RequestId: x\tDuration: 3011.52 ms\tBilled Duration: 3012 ms\tInit Duration: 801.10 ms\n")
    arm("A4 a log tail parses to its phases, handler time and Init (None when warm)",
        t["feed"] == 182 and t["peers"] == 2467 and t["handler_ms"] == 3011.52 and t["init_ms"] == 801.10
        and parse_tail("REPORT RequestId: y\tDuration: 5.0 ms\n")["init_ms"] is None)
    ok = all(arms)
    print("arms passed %d of %d" % (sum(arms), len(arms)))
    print("R103 PULL CENSUS ARMS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def run_name(module, key):
    rows = {}
    for route in ROUTES:
        event = {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, route), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}}
        with recording(module) as rec, contextlib.redirect_stdout(io.StringIO()):
            t0 = time.monotonic()
            resp = module.handler(event)
            wall = (time.monotonic() - t0) * 1000
        rows[route] = {"status": resp.get("statusCode"), "wall_ms": round(wall), "by_phase": {
            phase: [{"service": c[1], "op": c[2], "resource": c[3], "ms": round(c[4], 1), "bytes": c[5], "class": pull_class(c[3])} for c in calls]
            for phase, calls in rec.attribute().items()}}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--names")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--shard")
    ap.add_argument("--out")
    ap.add_argument("--merge", nargs="+", help="shard result files (--out of earlier runs): combine them, run nothing local")
    ap.add_argument("--from-file", dest="src", help="one result file: read it, run nothing local (use with --deployed-phases)")
    ap.add_argument("--deployed-phases", action="store_true", help="after the local census, drive ONE overlay per name on the live function (a reader of it) and print its per-phase ms")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    result, failed = {}, []
    if a.merge or a.src:
        names = []
        for f in a.merge or [a.src]:
            d = json.load(open(f, encoding="utf-8"))
            result.update(d["result"])
            failed += d.get("failed", [])
            names += d["names"] + [x.split(":")[0] for x in d.get("failed", [])]
        names = sorted(set(names))
        if a.src and not a.out:
            a.out = a.src
    else:
        from lib.research.api import scoped_amgt
        from lib.research.corpus import dossier
        from lib.research.harvest import store

        names = a.names.split(",") if a.names else sorted(dossier._resolved_security_keys(client=store._default_client()))
        if a.shard:
            i, n = (int(x) for x in a.shard.split("/"))
            names = [k for j, k in enumerate(names) if j % n == i]
        if a.limit:
            names = names[: a.limit]
        for k in names:
            try:
                result[k] = run_name(scoped_amgt, k)
            except Exception as exc:  # a failed name is counted and named, never dropped
                failed.append("%s: %s %s" % (k, type(exc).__name__, str(exc)[:80]))
    total = {c: [0, 0, 0.0] for c in PULLS + ("other",)}
    other = {}
    for k, routes in result.items():
        for route, row in routes.items():
            for calls in row["by_phase"].values():
                for c in calls:
                    t = total[c["class"]]
                    t[0] += 1
                    t[1] += c["bytes"]
                    t[2] += c["ms"]
                    if c["class"] == "other":
                        other[c["resource"].rsplit("/", 1)[0][:90]] = other.get(c["resource"].rsplit("/", 1)[0][:90], 0) + 1
    print("PULLS over %d names x %d routes (class: calls / bytes / local ms)" % (len(result), len(ROUTES)))
    for c, (n, b, ms) in total.items():
        print("  %-11s %6d calls  %12d bytes  %10.0f ms" % (c, n, b, ms))
    print("UNCLASSED prefixes (%d): %s" % (len(other), sorted(other.items(), key=lambda kv: -kv[1])[:20]))
    if a.out:
        json.dump({"names": sorted(result), "failed": failed, "result": result}, open(a.out, "w", encoding="utf-8"), default=str)
    if a.deployed_phases:
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        rows, cold = {}, []
        for k in sorted(result):
            rows[k] = deployed_overlay(lam, k)
            if rows[k].get("init_ms") is not None:
                cold.append(k)
        print("LAMBDA OVERLAY over %d names, one request each, in order (cold container starts: %d %s)" % (len(rows), len(cold), cold[:5]))
        phases = sorted({p for r in rows.values() for p in r if p not in ("handler_ms", "init_ms")})
        for p in phases + ["handler_ms"]:
            vals = sorted(r[p] for r in rows.values() if r.get(p) is not None)
            if vals:
                print("  %-22s n %3d  median %7.0f  p95 %7.0f  max %7.0f ms" % (p, len(vals), statistics.median(vals), vals[min(len(vals) - 1, int(0.95 * len(vals)))], vals[-1]))
        over = sorted(k for k, r in rows.items() if r.get("handler_ms") and r["handler_ms"] >= 3000)
        print("  handler at or above 3,000 ms: %d names %s" % (len(over), over[:10]))
        print("R103 PULL CENSUS DEPLOYED: RAN %d of %d names" % (sum(1 for r in rows.values() if r.get("handler_ms")), len(rows)))
        if a.out:
            data = json.load(open(a.out, encoding="utf-8"))
            data["lambda_overlay"] = rows
            json.dump(data, open(a.out, "w", encoding="utf-8"), default=str)
    other_calls = total["other"][0]
    print("R103 PULL CENSUS: RAN %d of %d names, %d calls, %d unclassed" % (len(result), len(names), sum(v[0] for v in total.values()), other_calls))
    for f in failed[:10]:
        print("  FAILED %s" % f)
    return 0 if len(result) == len(names) else 1


if __name__ == "__main__":
    sys.exit(main())
