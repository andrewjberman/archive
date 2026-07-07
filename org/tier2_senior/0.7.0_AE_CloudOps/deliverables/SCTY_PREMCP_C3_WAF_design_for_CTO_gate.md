# SCTY_PREMCP C3-WAF -- WAF-on-ALB design (for CTO arch-gate)

**Author:** 0.7.0_AE_CloudOps~B | **Date:** 2026-07-07 | **TO:** SCTY_PREMCP C3-WAF (COO-assigned; 0.7.0~A coordinates)
**Gate:** CTO arch-gate REQUIRED before any apply. Then safe-apply (HALTGT) -> CVO cert.

## What / why

C3-WAF is the **network-layer complement** to the deployed **app-layer C1/C2 rate-limit**
(`infra/aws/ec2/m365-mcp-gateway/app/ratelimit.py`). A regional AWS WAFv2 WebACL on the
m365-mcp-gateway ALB (`aws_lb.gw`, internet-facing 443) stops volumetric + known-bad traffic
**at the edge, before the EC2 gateway** -- the app-layer limiter is the precise per-principal
guard; WAF is the coarse per-IP flood + signature guard.

**Grounded app-layer limits (to size the WAF, NOT duplicate):**
| C-layer | limit | scope | fail-mode |
|---|---|---|---|
| C1 ip_global | 300 req / 60s | per-IP, all paths | fail-OPEN (a limiter bug must not down traffic) |
| C1 ip_auth | 20 req / 60s | per-IP, /authorize /token /register /callback | fail-CLOSED |
| C2 mcp_identity | 120 req / 60s | per-authenticated-email | fail-CLOSED |
| (app body cap) | content_length_over_cap | per-request | 413 |

## Design (regional WAFv2 WebACL -> aws_wafv2_web_acl_association -> aws_lb.gw.arn)

Default action = **ALLOW** (WAF only acts on rule matches). Rules, in priority order:

| # | rule | action | FP risk | rationale |
|---|---|---|---|---|
| 0 | **Rate-based** (aggregate-key = IP, 5-min window, limit **2000**) | **BLOCK** | ~none | 2000/5min/IP is ABOVE the app-layer 300/60s (~1500/5min) -> WAF catches only egregious volumetric floods (DDoS-class); normal per-IP limiting stays with the app layer. Clean win, BLOCK from day 1. |
| 1 | **AWSManagedRulesAmazonIpReputationList** | **BLOCK** | low | AWS-curated malicious-IP list; near-zero FP. BLOCK from day 1. |
| 2 | **AWSManagedRulesKnownBadInputsRuleSet** | **COUNT -> BLOCK** | low-mod | Log4j/path-traversal/header-injection signatures. COUNT first (observe real MCP/OAuth traffic), flip to BLOCK after the observation window. |
| 3 | **AWSManagedRulesCommonRuleSet** | **COUNT -> BLOCK w/ exclusions** | **HIGH on this API** | OWASP-common. Two rules in it will FALSE-POSITIVE on the MCP/OAuth shapes and are pre-flagged for exclusion: **SizeRestrictions_BODY** (8KB cap -> MCP JSON-RPC bodies legitimately exceed it; the app body-cap is the right-sized guard) and **CrossSiteScripting_BODY / NoUserAgent_HEADER** (JSON-RPC payloads + a non-browser API client trip these). COUNT first, exclude the confirmed-FP rules, then BLOCK. |

**Logging:** WAFv2 -> CloudWatch Logs group `aws-waf-logs-m365-mcp-gateway` (native; the audit-lake
has NO Firehose + its S3 bucket isn't `aws-waf-logs-`-named, so a new CW log group is the clean sink).
Redact the `authorization` header + `x-amzn-oidc-*` in the logging config. The log is what makes the
COUNT-mode observation possible (we SEE what would-block before it blocks).

## The CTO decision I need gated

**COUNT-first-then-BLOCK (my recommendation) vs BLOCK-from-start-with-pre-exclusions** for rules #2/#3.
- COUNT-first = zero day-1 risk to Claude Code's MCP client + the OAuth flows; we flip to BLOCK after
  a short observation window (logs prove no legit traffic matches). The trade: a brief window where #2/#3
  only COUNT (rate-based #0 + IpReputation #1 + the app-layer C1/C2 still BLOCK throughout).
- BLOCK-from-start = full protection immediately, but risks a false-positive outage on real MCP/OAuth
  traffic we haven't yet observed against these managed rules.
- Rate-based #0 + IpReputation #1 BLOCK from day 1 either way.

**Also for CTO:** (a) the rate-based limit 2000/5min/IP -- OK or tune? (b) confirm the pre-exclusion list
(SizeRestrictions_BODY, CrossSiteScripting_BODY, NoUserAgent_HEADER) or add/remove; (c) new TF file
`infra/aws/terraform/m365-mcp-gateway/waf.tf`.

## Sequence (post-gate)
commit waf.tf -> `terraform plan` (WebACL + association + CW log group + logging config) -> RAVC plan ->
safe-apply (HALTGT) -> 0-diff -> deploy-ledger (opened at apply-start) -> CVO cert (WAF associated +
COUNT-logging live + a synthetic flood COUNTS + a legit MCP/OAuth request is NOT matched by #2/#3).
Pending 0.7.0~A input: exact MCP/OAuth request shapes to sharpen exclusions.
