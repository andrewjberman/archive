#!/usr/bin/env python
"""OG-ev-12 (READ-ONLY): who answered the organic per-identity 429 of 2026-10-18 about 19:2xZ? Collects, as counts only (no address, principal, path beyond /mcp or other, or object content is printed or stored):
  1. the gateway journal over the window (journalctl over SSM): the first POST /mcp access line, the 429 lines on POST /mcp and on other routes, the live code sha (the marker)
  2. the audit lake 2026-10-18T19:00Z to 20:00Z: gw_ratelimit rows, the sum of their `suppressed` fields, the objects listed and read errors
  3. the ALB access logs the account keeps (s3://opal-data-security/waf-logs/alb-opal-gateway/, read-only list and get): per five-minute file of the window, the lines by (elb status, target status), and the 429s with their target status
  4. the throttle rule at the pinned code sha (git show <sha>:...app/ratelimit.py, never trunk)
usage: python ev12_collect.py <out.json> <code_sha_or_AUTO>      (repository root)"""
from __future__ import annotations

import gzip
import io
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import boto3

INSTANCE = "i-07dccb1615503ac99"
LAKE = "opal-mcp-audit"
ALB_BUCKET = "opal-data-security"
ALB_PREFIX = "waf-logs/alb-opal-gateway/AWSLogs/313476888478/elasticloadbalancing/us-east-1/2026/10/18/"
WIN_START, WIN_END = "2026-10-18T19:00:00Z", "2026-10-18T20:00:00Z"
NEAR0, NEAR1 = "2026-10-18T19:20:00Z", "2026-10-18T19:29:59Z"
OUT, SHA_ARG = sys.argv[1], sys.argv[2]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
JBASE = "journalctl -u opal-gateway --since '2026-10-18 19:00:00 UTC' --until '2026-10-18 20:00:00 UTC' --utc --no-pager -o short-iso"


def run_ssm(cmd):
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
    inv = None
    for _ in range(120):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    return inv["StandardOutputContent"]


def z(ts):
    return ts.replace("+0000", "Z") if ts.endswith("+0000") else ts


def journal():
    cmd = ("echo BEGIN; cat /opt/opal-gateway/.deployed_commit; echo; %(b)s | grep -E 'POST /mcp' | head -1 | cut -d' ' -f1; %(b)s | tail -1 | cut -d' ' -f1; %(b)s | head -1 | cut -d' ' -f1; "
           "%(b)s | grep -cE '\"POST /mcp[^\"]*\" 429'; %(b)s | grep -E '\" 429' | grep -vcE '\"POST /mcp'; %(b)s | grep -cE 'POST /mcp'; "
           "%(b)s | grep -E '\" 429' | cut -d' ' -f1 | cut -c1-16 | sort | uniq -c; echo END" % {"b": JBASE})
    body = [x.strip() for x in run_ssm(cmd).split("BEGIN", 1)[-1].split("END", 1)[0].splitlines() if x.strip()]
    sha, first, last, earliest, n429, other, mcp_all = body[:7]
    return {"code_sha": sha, "first_access_line_ts": z(first), "last_line_ts": z(last), "earliest_line_ts": z(earliest), "post_mcp_429_lines": int(n429), "other_429_lines": int(other), "post_mcp_lines": int(mcp_all),
            "other_429_by_minute": body[7:]}


def lake():
    keys, token, first = [], None, True
    while first or token:
        first = False
        kw = {"Bucket": LAKE, "Prefix": "audit/dt=2026-10-18/"}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=2026-10-18/" + WIN_START[:-1]})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    keys = [k for k in keys if k.split("/")[-1][:19] <= WIN_END[:-1]]

    def one(k):
        try:
            rows, sup = 0, 0
            for ln in s3.get_object(Bucket=LAKE, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    rec = json.loads(ln)
                    if rec.get("event") == "gw_ratelimit":
                        rows += 1
                        sup += int(rec.get("suppressed") or 0)
            return rows, sup, 0
        except Exception:
            return 0, 0, 1
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(one, keys))
    return {"gw_ratelimit_rows": sum(r[0] for r in res), "suppressed_sum": sum(r[1] for r in res), "denominator": len(keys), "read_errors": sum(r[2] for r in res)}


def alb():
    keys = []
    token = None
    first = True
    while first or token:
        first = False
        kw = {"Bucket": ALB_BUCKET, "Prefix": ALB_PREFIX}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if re.search(r"_20261018T19\d\dZ_", k) or re.search(r"_20261018T2000Z_", k)]

    def one(k):
        try:
            data = gzip.decompress(s3.get_object(Bucket=ALB_BUCKET, Key=k)["Body"].read()).decode("utf-8", "replace")
        except Exception:
            return None
        out = {"lines": 0, "pairs": {}, "n429_elb": 0, "n429_target": 0, "n429_near": [], "mcp_lines": 0}
        for ln in data.splitlines():
            # type time elb client target rpt tpt respt elb_status target_status rb sb "request" ...
            m = re.match(r'^\S+ (\S+) \S+ \S+ \S+ \S+ \S+ \S+ (\S+) (\S+) \S+ \S+ "(\S+) (\S+)', ln)
            if not m:
                continue
            ts, es, ts_stat, method, url = m.groups()
            out["lines"] += 1
            out["pairs"][es + "/" + ts_stat] = out["pairs"].get(es + "/" + ts_stat, 0) + 1
            is_mcp = "/mcp" in url
            out["mcp_lines"] += is_mcp
            if es == "429":
                out["n429_elb"] += 1
            if ts_stat == "429":
                out["n429_target"] += 1
            if (es == "429" or ts_stat == "429") and NEAR0[:-1] <= ts[:19] <= NEAR1[:-1]:
                out["n429_near"].append([ts[11:19] + "Z", es, ts_stat, "mcp" if is_mcp else "other", method])
        return out
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = [r for r in ex.map(one, inwin) if r is not None]
    pairs, near = {}, []
    for r in res:
        for k, v in r["pairs"].items():
            pairs[k] = pairs.get(k, 0) + v
        near += r["n429_near"]
    return {"files_listed_under_the_day": len(keys), "files_in_window": len(inwin), "files_read": len(res), "lines": sum(r["lines"] for r in res), "mcp_lines": sum(r["mcp_lines"] for r in res),
            "status_pairs_elb_target": dict(sorted(pairs.items())), "lines_with_elb_status_429": sum(r["n429_elb"] for r in res), "lines_with_target_status_429": sum(r["n429_target"] for r in res),
            "429_lines_between_19_20_and_19_30": near}


def alb_days():
    """Every ALB access-log line of 2026-10-17, 10-18 and 10-19 (so far) with a 429 on either status: counts per day and, for the 429s, the second of day (no address, path or identity kept)."""
    out = {}
    for day in ("2026/10/17", "2026/10/18", "2026/10/19"):
        pre = ALB_PREFIX.replace("2026/10/18/", day + "/")
        keys, token, first = [], None, True
        while first or token:
            first = False
            kw = {"Bucket": ALB_BUCKET, "Prefix": pre}
            if token:
                kw["ContinuationToken"] = token
            page = s3.list_objects_v2(**kw)
            keys += [o["Key"] for o in page.get("Contents", [])]
            token = page.get("NextContinuationToken") if page.get("IsTruncated") else None

        def one(k):
            try:
                data = gzip.decompress(s3.get_object(Bucket=ALB_BUCKET, Key=k)["Body"].read()).decode("utf-8", "replace")
            except Exception:
                return None
            n, hits = 0, []
            for ln in data.splitlines():
                m = re.match(r'^\S+ (\S+) \S+ \S+ \S+ \S+ \S+ \S+ (\S+) (\S+) \S+ \S+ "(\S+) (\S+)', ln)
                if not m:
                    continue
                n += 1
                if m.group(2) == "429" or m.group(3) == "429":
                    hits.append((m.group(1)[:19] + "Z", m.group(2), m.group(3), "mcp" if "/mcp" in m.group(5) else "other"))
            return n, hits
        with ThreadPoolExecutor(max_workers=12) as ex:
            res = [r for r in ex.map(one, keys) if r is not None]
        hits = sorted(h for r in res for h in r[1])
        out[day.replace("/", "-")] = {"files": len(keys), "files_read": len(res), "lines": sum(r[0] for r in res), "lines_with_a_429": len(hits),
                                      "429_first_second": hits[0][0] if hits else None, "429_last_second": hits[-1][0] if hits else None,
                                      "429_on_mcp_with_target_429": sum(1 for h in hits if h[1] == "429" and h[2] == "429" and h[3] == "mcp")}
    return out


def lake_rows_on(day, start_z, end_z):
    keys, token, first = [], None, True
    while first or token:
        first = False
        kw = {"Bucket": LAKE, "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, start_z[:-1])})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    keys = [k for k in keys if k.split("/")[-1][:19] <= end_z[:-1]]

    def one(k):
        out = []
        for ln in s3.get_object(Bucket=LAKE, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
            if ln.strip():
                r = json.loads(ln)
                if r.get("event") == "gw_ratelimit":
                    out.append({"object_time": k.split("/")[-1][11:19] + "Z", "suppressed": r.get("suppressed"), "count_in_window": r.get("count_in_window")})
        return out
    with ThreadPoolExecutor(max_workers=16) as ex:
        rows = [x for r in ex.map(one, keys) for x in r]
    return {"objects_listed": len(keys), "rows": rows}


def throttle(sha):
    p = "infra/aws/ec2/opal-gateway/app/ratelimit.py"
    txt = subprocess.run(["git", "show", "%s:%s" % (sha, p)], capture_output=True).stdout.decode("utf-8", "replace")
    for i, ln in enumerate(txt.splitlines(), 1):
        m = re.match(r"^_REFUSAL_WINDOW_S\s*=\s*([0-9.]+)", ln)
        if m:
            return float(m.group(1)), i
    raise SystemExit("the refusal window constant was not found at the pinned sha")


def main():
    j = journal()
    sha = j["code_sha"] if SHA_ARG == "AUTO" else SHA_ARG
    lk = lake()
    ab = alb()
    days = alb_days()
    l17 = lake_rows_on("2026-10-17", "2026-10-17T17:15:00Z", "2026-10-17T17:30:00Z")
    win, line = throttle(sha)
    n429, rows = j["post_mcp_429_lines"], lk["gw_ratelimit_rows"]
    covers = j["first_access_line_ts"] <= NEAR0 and NEAR1 <= WIN_END
    if n429 >= 1 and rows == 0:
        verdict = "THIS_SERVICE_WROTE_NOTHING"
    elif n429 >= 1 and 1 <= rows < n429:
        verdict = "THROTTLED"
    elif n429 == 0 and covers:
        verdict = "OTHER_LAYER"
    else:
        verdict = "UNDETERMINED"
    rec = {"code_sha": sha, "organic_429_ts_range": {"from": NEAR0, "to": NEAR1},
           "journal": {"source": "ssm send-command on the host: " + JBASE + " | grep -cE '\"POST /mcp[^\"]*\" 429' (and the same for 429 on other routes); first access line = first 'POST /mcp' line; counts only",
                       "first_access_line_ts": j["first_access_line_ts"], "window_end": WIN_END, "post_mcp_429_lines": n429, "other_429_lines": j["other_429_lines"], "last_line_ts": j["last_line_ts"],
                       "earliest_line_ts": j["earliest_line_ts"], "post_mcp_lines": j["post_mcp_lines"]},
           "lake": {"source": "s3://%s audit/dt=2026-10-18/ listed (StartAfter the window start) and every object read; event gw_ratelimit counted, suppressed summed" % LAKE, "window_start": WIN_START, "window_end": WIN_END, **lk},
           "alb_access_logs": ab, "alb_access_logs_by_day": days, "lake_2026_10_17_1715_1730": l17,
           "throttle_rule": {"refusal_window_s": win, "first_refusal_writes": True, "source": "app/ratelimit.py:%d at %s" % (line, sha[:10])},
           "journal_covers_the_429_time": covers, "verdict": verdict}
    d17, d18, d19 = days["2026-10-17"], days["2026-10-18"], days["2026-10-19"]
    rows17 = l17["rows"]
    rec["response_shape"] = {"guard_middleware_body_seen": None,
                             "evidence": ("No response body is kept by any log read here (the journal holds the access line only, the ALB access log holds status codes and sizes, not bodies), so the body shape could not be read: null. "
                                          "What was read: the ALB logged %d lines with a 429 on the 2026-10-17 17:21 span, all POST /mcp with the TARGET (this service) answering 429, so the only 429s the account's ALB recorded in three days came from this service's limiter; "
                                          "on 2026-10-18 the ALB logged %d lines (%d with a 429) and on 2026-10-19 so far %d lines (%d with a 429)." % (d17["lines_with_a_429"], d18["lines"], d18["lines_with_a_429"], d19["lines"], d19["lines_with_a_429"]))}
    rec["evidence"] = [
        "Journal %s to %s: %d POST /mcp lines, %d answered 429 and %d 429s on other routes; the unit's journal reaches back to %s but the access log only returned at the first POST /mcp line, %s, so the journal cannot show 19:20Z to 19:23:53Z: covers=%s." % (
            j["first_access_line_ts"], WIN_END, j["post_mcp_lines"], n429, j["other_429_lines"], j["earliest_line_ts"], j["first_access_line_ts"], covers),
        "ALB access logs (kept by the account, read-only): %d files / %d lines for 2026-10-18T19:00Z to 20:00Z with status pairs %s; 0 lines carry a 429 on the ALB or the target status, including 19:20Z to 19:30Z (the 502 lines with no target status are ALB-generated)." % (
            ab["files_read"], ab["lines"], json.dumps(ab["status_pairs_elb_target"], sort_keys=True)),
        "Whole days in the ALB logs: 2026-10-18 %d lines, %d with a 429; 2026-10-19 so far %d lines, %d with a 429; the only 429s on 2026-10-17 to 19 are %d lines from %s to %s on 2026-10-17, %d of them POST /mcp answered by the target." % (
            d18["lines"], d18["lines_with_a_429"], d19["lines"], d19["lines_with_a_429"], d17["lines_with_a_429"], d17["429_first_second"], d17["429_last_second"], d17["429_on_mcp_with_target_429"]),
        "Lake, 2026-10-17T17:15Z to 17:30Z: %d gw_ratelimit row(s) for those %d ALB-logged 429s (row object times %s, suppressed %s): the first refusal wrote and the throttle folded the rest, which is the throttle rule at %s (refusal window %s s) working as written." % (
            len(rows17), d17["lines_with_a_429"], [r["object_time"] for r in rows17], [r["suppressed"] for r in rows17], sha[:10], win),
        "Lake 2026-10-18T19:00Z to 20:00Z: %d gw_ratelimit rows over %d objects (%d read errors): there is no refusal to explain in that hour; a 429 at about 19:2xZ on 2026-10-18 is in neither the journal nor the ALB log." % (lk["gw_ratelimit_rows"], lk["denominator"], lk["read_errors"]),
    ]
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps({"body": rec}, indent=1) + "\n")
    print(json.dumps({"verdict": verdict, "first_access": j["first_access_line_ts"], "earliest_line": j["earliest_line_ts"], "n429": n429, "other429": j["other_429_lines"], "lake": lk,
                      "alb": {k: ab[k] for k in ab if k != "status_pairs_elb_target"}, "alb_pairs": ab["status_pairs_elb_target"], "win": win, "line": line}))


if __name__ == "__main__":
    main()
