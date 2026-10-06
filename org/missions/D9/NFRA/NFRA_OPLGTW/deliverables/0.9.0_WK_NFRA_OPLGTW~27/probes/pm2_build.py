#!/usr/bin/env python3
"""OG-pm-2 -- assemble PM2_CAUSE.json from the pm2_analyze.py output and the pm2_cw.py CloudWatch read.
Usage: pm2_build.py <analysis.json> <cw.json> <out PM2_CAUSE.json>. Local only; no AWS call."""
import json
import sys

CAP = 0.5535 * 1.2


def main():
    an = json.load(open(sys.argv[1], encoding="utf-8"))
    cw = json.load(open(sys.argv[2], encoding="utf-8"))
    out = sys.argv[3]
    d5, d0 = an["2026-10-05"], an["2026-09-30"]
    days = {}
    for day, v in (("2026-10-05", d5), ("2026-09-30", d0)):
        days[day] = {
            "routes": [{"route": r["route"], "at_ogp1": r["at_ogp1"], "requests": r["requests"],
                        "timed_requests": r["timed_requests"], "p95_seconds": r["p95_seconds"],
                        "target_status": r["target_status"]} for r in v["routes"]],
            "covered_requests": v["covered_requests"], "alb_requests": cw[day]["request_count"],
            "timed_requests": v["timed_requests"], "alb_sample_count": cw[day]["sample_count"],
            "alb_cloudwatch_p95_seconds": cw[day]["p95_seconds"], "log_p95_seconds": v["p95_all_seconds"],
            "log_rows_total": v["alb_log_rows_total"], "log_rows_answered_by_alb_itself": v["elb_only_rows_not_forwarded"],
            "split": v["split"], "hourly_forwarded": v["hourly_forwarded"],
            "hourly_p95_with_and_without_hx_teams_chats": v["hourly_p95_with_and_without_poller"],
            "audit_objects": v["audit_objects"], "audit_read_errors": v["audit_read_errors"],
        }
    sp5, sp0 = d5["split"], d0["split"]
    q_share = d5["hx_teams_chats_share_of_quiet"]
    # SLOWDOWN test: the routes that existed at OG-p-1, 10-05 against 09-30
    old5, old0 = sp5["at_ogp1_routes"]["p95_seconds"], sp0["at_ogp1_routes"]["p95_seconds"]
    oldq5, oldq0 = sp5["at_ogp1_all_but_02Z"]["p95_seconds"], sp0["at_ogp1_all_but_02Z"]["p95_seconds"]
    slow = old5 > CAP or old5 > old0 * 1.2
    mix = d5["hx_teams_chats_share_of_quiet"] is not None and q_share > 0.5 and sp5["added_since"]["p95_seconds"] > CAP
    finding = "BOTH" if (slow and mix) else "SLOWDOWN" if slow else "MIX" if mix else "UNDETERMINED"
    rec = {
        "instrument": {
            "name": "ALB access logs of the gateway load balancer (access_logs.s3.enabled=true, s3://opal-data-security/waf-logs/alb-opal-gateway/), "
                    "per-request target_processing_time and request path; caller identity for the one steady caller taken from the gateway audit lake "
                    "(bucket opal-mcp-audit, audit/dt=<day>/) `detail` label, which carries NO latency",
            "cannot_see": [
                "requests the ALB itself answers (301/302 redirects, 403, 400): they have no target and no target latency (903 of 4231 rows on 2026-10-05; 1573 of 4083 on 2026-09-30) and are outside RequestCount",
                "the MCP tool inside POST /mcp: one route carries every tool call, so there is no per-tool latency; the audit lake names the tool but has no latency field",
                "caller identity beyond source IP and User-Agent (the ALB log has no principal); the hx_teams caller used 14 distinct source IPs on 2026-10-05",
                "requests with no target response (target_processing_time -1; 2 on 2026-10-05, 81 on 2026-09-30): counted as requests, null in latency",
                "health-check traffic (health_check_logs disabled and outside RequestCount) and on-host time spent before or after the ALB",
                "request bodies, headers, cookies, bearers and query strings (ALB logs carry none; the query string is also dropped at parse time)",
                "an exact CloudWatch p95: the log order-statistic p95 is within 0.012 s of CloudWatch's on 2026-10-05 (0.9358 vs 0.9473)",
            ],
        },
        "route_set_at_ogp1": {
            "source": "Gateway source at commit 7bd89b5d71 (infra/aws/ec2/opal-gateway/app/server.py Route/Mount paths): the commit OG-p-1 OGP1-AC1 digest-compared the running host against, 50 of 50 per-file sha256 equal "
                      "(deliverables/0.9.0_WK_NFRA_OPLGTW~2/BASELINE.json OGP1-AC1, 2026-09-15T10:53Z); ALB rules at that time from OGP1-AC3 (priorities 10, 20, 30-33, default OIDC)",
            "paths": ["/mcp", "/mcp/*", "/authorize", "/register", "/token", "/login", "/callback", "/health", "/.well-known/*",
                      "/otp/token", "/otp/fetch", "/otp/health", "/ms/sites", "/ms/site_children", "/ms/onedrive_children",
                      "/ms/search", "/ms/token", "/ms/health", "/graph/cypher", "/graph/health", "/query/v0", "/teams/poll",
                      "/sprint", "/sprint/", "/sprint/archive", "/sprint/{day}"],
            "note": "a path outside this set is at_ogp1 false: new routes (/hx/*, /ms/taxsma-workbook, /rivalfunds, /yearinreview, /, /assets/*) and 404 probe paths (/favicon.ico, /hx/teams/x)",
        },
        "days": days,
        "hypothesis_i": {
            "steady_caller_found": True,
            "route": "GET /hx/teams/chats",
            "caller": "audit label teamsassist (tool hx_teams, one audit user for all 1530 hx_teams records on 2026-10-05; User-Agent Python-urllib/3.12 in 1440 of 1440 ALB rows; 14 distinct source IPs)",
            "hourly_rate": 60,
            "p95_seconds": d5["split"]["hx_teams_chats_exact"]["p95_seconds"],
            "requests_2026_10_05": d5["split"]["hx_teams_chats_exact"]["requests"],
            "hourly_counts_2026_10_05": d5["hx_teams_chats_hourly"],
            "share_of_quiet_hour_requests_2026_10_05": q_share,
            "quiet_hours_definition": "the 23 UTC hours other than 02Z (1,972 forwarded requests; 1,380 of them are this poller)",
            "first_seen_utc": an["context_days"]["2026-10-02"]["hx_teams_chats_first"],
            "daily": {k: {"requests": v["hx_teams_chats_requests"], "p95_seconds": v["hx_teams_chats_p95"]}
                      for k, v in an["context_days"].items()},
        },
        "slowdown_test": {
            "at_ogp1_routes_p95_2026_10_05": old5, "at_ogp1_routes_p95_2026_09_30": old0,
            "at_ogp1_quiet_hour_p95_2026_10_05": oldq5, "at_ogp1_quiet_hour_p95_2026_09_30": oldq0,
            "same_route_p95": {k: {"2026-10-05": an["context_days"]["2026-10-05"]["p95 " + k], "2026-09-30": an["context_days"]["2026-09-30"]["p95 " + k]}
                               for k in ("POST /mcp", "POST /token", "GET /ms/site_children")},
            "cap_seconds": round(CAP, 4), "slowdown_if": "at-OG-p-1 routes p95 above the cap or more than 1.2x their 2026-09-30 value",
        },
        "context_days": an["context_days"],
        "finding": finding,
        "finding_numbers": {
            "full_day_p95_2026_10_05_cloudwatch": cw["2026-10-05"]["p95_seconds"],
            "routes_at_ogp1_only_p95": old5, "routes_added_since_p95": sp5["added_since"]["p95_seconds"],
            "added_since_requests": sp5["added_since"]["requests"], "at_ogp1_requests": sp5["at_ogp1_routes"]["requests"],
            "hx_teams_chats_share_of_added_since_requests": round(sp5["hx_teams_chats_exact"]["requests"] / sp5["added_since"]["requests"], 4),
            "cap_seconds": round(CAP, 4),
        },
        "writes": 0,
    }
    json.dump(rec, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
    print("finding", finding, "old", old5, old0, "oldq", oldq5, oldq0, "mix", mix, "slow", slow)


main()
