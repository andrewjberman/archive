#!/usr/bin/env python3
"""OG-pm-2 -- per-route request count + p95 from the ALB access-log cache (pm2_fetch.py) and the audit-lake cache
(pm2_audit_fetch.py). Usage: pm2_analyze.py <alb_cache> <audit_cache> <out PM2_CAUSE.json>
Pure local computation; reads the two caches, calls no AWS API. The CloudWatch ALB RequestCount per day is read once by
the caller and passed through the constants below (read verbatim from CloudWatch, see PM2_CAUSE.md)."""
import collections
import json
import re
import sys

ALB_REQUESTS = {}  # filled from argv[4] (json {"day": n}) when given


def p95(v):
    v = sorted(v)
    n = len(v)
    k = 0.95 * (n - 1)
    f = int(k)
    return v[f] + (v[min(f + 1, n - 1)] - v[f]) * (k - f)


def norm(path):
    if path.startswith("/.well-known/"):
        return path
    segs = path.split("/")
    out = []
    for i, s in enumerate(segs):
        if i >= 3 and segs[1] in ("hx", "sprint", "rivalfunds", "assets") or (segs[1] == "hx" and i >= 3):
            pass
        if s and (len(s) >= 20 or "%3A" in s or "%40" in s or re.fullmatch(r"\d{4}-\d\d-\d\d", s) or re.fullmatch(r"\d{8,}", s)):
            out.append("{id}")
        else:
            out.append(s)
    r = "/".join(out)
    if r.startswith("/assets/"):
        r = "/assets/{file}"
    return r


# The route set AT OG-p-1: the Gateway source at the commit the OG-p-1 AC1 digest-compared the running host against
# (7bd89b5d71, 50 of 50 per-file sha256 equal, BASELINE.json OGP1-AC1) -- every Route(...) / Mount(...) path in
# app/server.py at that commit, read with `git show 7bd89b5d71:infra/aws/ec2/opal-gateway/app/server.py`.
OGP1 = {"/.well-known/jwks.json", "/.well-known/oauth-authorization-server", "/.well-known/oauth-protected-resource",
        "/authorize", "/callback", "/graph/cypher", "/graph/health", "/health", "/login", "/ms/health",
        "/ms/onedrive_children", "/ms/search", "/ms/site_children", "/ms/sites", "/ms/token", "/otp/fetch",
        "/otp/health", "/otp/token", "/query/v0", "/register", "/sprint", "/sprint/", "/sprint/archive",
        "/sprint/{id}", "/teams/poll", "/token", "/mcp", "/mcp/"}


def main():
    alb = json.load(open(sys.argv[1], encoding="utf-8"))
    aud = json.load(open(sys.argv[2], encoding="utf-8"))
    out = sys.argv[3]
    cw = json.load(open(sys.argv[4], encoding="utf-8")) if len(sys.argv) > 4 else {}
    res = {}
    for day in ("2026-10-05", "2026-09-30"):
        rows = alb[day]["rows"]
        fwd = [r for r in rows if r["target"] != "-"]
        timed = [r for r in fwd if r["tgt_t"] >= 0]
        by = collections.defaultdict(list)
        for r in fwd:
            by[(r["method"], norm(r["path"]))].append(r)
        routes = []
        for (m, p), rr in sorted(by.items(), key=lambda kv: -len(kv[1])):
            t = [x["tgt_t"] for x in rr if x["tgt_t"] >= 0]
            st = collections.Counter(x["tgt_status"] for x in rr)
            routes.append({"route": "%s %s" % (m, p), "at_ogp1": p in OGP1, "requests": len(rr),
                           "timed_requests": len(t), "p95_seconds": round(p95(t), 4) if t else None,
                           "target_status": dict(st.most_common(4))})
        res[day] = {"routes": routes, "covered_requests": len(fwd), "alb_requests": cw.get(day),
                    "timed_requests": len(timed), "alb_log_rows_total": len(rows),
                    "elb_only_rows_not_forwarded": len(rows) - len(fwd),
                    "p95_all_seconds": round(p95([r["tgt_t"] for r in timed]), 4),
                    "audit_objects": aud[day]["objects"], "audit_read_errors": aud[day]["read_errors"]}
        # splits
        def sub(pred, label):
            t = [r["tgt_t"] for r in timed if pred(r)]
            n = sum(1 for r in fwd if pred(r))
            return {"requests": n, "timed": len(t), "p95_seconds": round(p95(t), 4) if t else None}
        def isold(r):
            return norm(r["path"]) in OGP1

        res[day]["split"] = {"at_ogp1_routes": sub(isold, "old"), "added_since": sub(lambda r: not isold(r), "new"),
                             "hx_teams_chats_exact": sub(lambda r: r["path"] == "/hx/teams/chats", "t"),
                             "hx_teams_all": sub(lambda r: r["path"].startswith("/hx/teams"), "t"),
                             "ms_site_children": sub(lambda r: r["path"] == "/ms/site_children", "s"),
                             "all_but_02Z": sub(lambda r: r["time"][11:13] != "02", "q"),
                             "all_but_02Z_and_hx_teams": sub(lambda r: r["time"][11:13] != "02" and not r["path"].startswith("/hx/teams"), "q2"),
                             "at_ogp1_all_but_02Z": sub(lambda r: r["time"][11:13] != "02" and isold(r), "q3"),
                             "at_ogp1_excl_site_children": sub(lambda r: isold(r) and r["path"] != "/ms/site_children", "q4")}
        hh = collections.Counter(r["time"][11:13] for r in fwd)
        res[day]["hourly_forwarded"] = [hh.get("%02d" % h, 0) for h in range(24)]
        hx = [r for r in fwd if r["path"] == "/hx/teams/chats"]
        hc = collections.Counter(r["time"][11:13] for r in hx)
        res[day]["hx_teams_chats_hourly"] = [hc.get("%02d" % h, 0) for h in range(24)]
        res[day]["hx_teams_chats_clients_distinct"] = len({r["client"] for r in hx})
        res[day]["hx_teams_chats_user_agents"] = dict(collections.Counter(r["ua"] for r in hx).most_common(3))
        q = [r for r in fwd if r["time"][11:13] != "02"]
        res[day]["quiet_hours_forwarded"] = len(q)
        res[day]["hx_teams_chats_share_of_quiet"] = round(sum(1 for r in q if r["path"] == "/hx/teams/chats") / len(q), 4) if q else None
        # per quiet hour p95 with and without the poller
        ph = []
        for h in range(24):
            hr = [r for r in timed if r["time"][11:13] == "%02d" % h]
            wo = [r["tgt_t"] for r in hr if r["path"] != "/hx/teams/chats"]
            ph.append({"hour": h, "n": len(hr), "p95": round(p95([r["tgt_t"] for r in hr]), 3) if hr else None,
                       "n_without_hx_teams_chats": len(wo), "p95_without_hx_teams_chats": round(p95(wo), 3) if wo else None})
        res[day]["hourly_p95_with_and_without_poller"] = ph
        # audit tool tally
        rs = [r for r in aud[day]["records"] if r["ts"] and r["ts"].startswith(day)]
        res[day]["audit_records_in_day"] = len(rs)
        res[day]["audit_tools"] = dict(collections.Counter((r["tool"] or r["event"] or "-") for r in rs).most_common(12))
        res[day]["audit_hx_teams_users"] = dict(collections.Counter(r["user"] for r in rs if r["tool"] == "hx_teams"))
        res[day]["audit_hx_teams_labels_routes"] = {"%s %s" % k: n for k, n in collections.Counter((r["dlabel"], "/".join((r["droute"] or "").split("/")[:4])) for r in rs if r["tool"] == "hx_teams").most_common(6)}
        res[day]["audit_hx_teams_hourly"] = [sum(1 for r in rs if r["tool"] == "hx_teams" and r["ts"][11:13] == "%02d" % h) for h in range(24)]
    ctx = {}
    for day in sorted(alb):
        fwd = [r for r in alb[day]["rows"] if r["target"] != "-"]
        timed = [r for r in fwd if r["tgt_t"] >= 0]
        old = [r["tgt_t"] for r in timed if norm(r["path"]) in OGP1]
        new = [r["tgt_t"] for r in timed if norm(r["path"]) not in OGP1]
        tc = [r for r in fwd if r["path"] == "/hx/teams/chats"]
        tct = [r["tgt_t"] for r in tc if r["tgt_t"] >= 0]
        ctx[day] = {"forwarded": len(fwd), "cw_request_count": cw.get(day), "p95_all": round(p95([r["tgt_t"] for r in timed]), 4),
                    "at_ogp1_requests": len(old), "at_ogp1_p95": round(p95(old), 4) if old else None,
                    "added_requests": len(new), "added_p95": round(p95(new), 4) if new else None,
                    "hx_teams_chats_requests": len(tc), "hx_teams_chats_p95": round(p95(tct), 4) if tct else None,
                    "hx_teams_chats_first": min((r["time"] for r in tc), default=None)}
        for rt in ("POST /mcp", "POST /token", "GET /ms/site_children"):
            m, p = rt.split(" ")
            t = [r["tgt_t"] for r in timed if r["method"] == m and norm(r["path"]) == p]
            ctx[day]["p95 " + rt] = (round(p95(t), 4) if t else None, len(t))
    res["context_days"] = ctx
    json.dump(res, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
    for d, v in ctx.items():
        print("CTX", d, v)
    for day, v in res.items():
        if day == "context_days":
            continue
        print("  audit labels/routes", v["audit_hx_teams_labels_routes"])
        print("==", day, "covered", v["covered_requests"], "alb", v["alb_requests"], "timed", v["timed_requests"], "p95_all", v["p95_all_seconds"])
        for r in v["routes"][:22]:
            print("  %5d  p95=%-7s old=%-5s %s %s" % (r["requests"], r["p95_seconds"], r["at_ogp1"], r["route"], r["target_status"]))
        print("  routes", len(v["routes"]))
        for k, s in v["split"].items():
            print("  split", k, s)
        print("  poller share of quiet", v["hx_teams_chats_share_of_quiet"], "distinct clients", v["hx_teams_chats_clients_distinct"], v["hx_teams_chats_user_agents"])
        print("  audit users", v["audit_hx_teams_users"], "hourly", v["audit_hx_teams_hourly"])


main()
