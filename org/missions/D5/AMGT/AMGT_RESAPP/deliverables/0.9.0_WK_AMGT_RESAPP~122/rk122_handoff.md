# AMGT-rk-122 handoff -- routed to an AE seat via `0.0.0_AB_MSTR~Z`

**Cell:** `AMGT-rk-122` (round 30, row `AMGT_RESAPP-Z-S226`, ARMED). ONE `ordered_cache_behavior` for
`/api/scoped/amgt/*` on distribution `EVTSA9VEHNZVH`, so the Security Analysis page's 16 mounted routes stop
falling through to the SPA origin (`200 text/html`) and reach the portal API instead.

**Why routed, not applied by this worker:** `infra/aws/**` resolves to lane `CLOUD_OPS_OR_ETL` (AE-only,
`.owned-paths.yaml:1906`). The issuer measured, by exercising `.tools/git-hooks/owned-paths-check.sh` itself:
`0.7.0_AE_CloudOps` PERMIT; `2.0.0_SA_COO~Z`, `0.2.0_DT_PortfolioAnalytics` and `0.9.0_WK_AMGT_RESAPP~122` all
REFUSE. This worker re-measured the same three verdicts before editing (AC0, below) and got the identical result.
CTO ruling msg 24353 (Case B): route rather than override.

**Never-widen pair on file:** `org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND30_RK122_COO_HALF.md`
(signed at issuance @`bf5c280e48`) and `NEVER_WIDEN_ROUND30_RK122_CTO_HALF.md` (SIGNED `1.0.0_SA_CTO~Z`
2026-09-22 ~19:4xZ @`434039c5c7`). Read both before acting -- they carry the full blast radius, writer census,
expected outcome and rollback triggers; this file is the mechanical index, not a restatement.

## 1. The patch

`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~122/rk122_amgt_behavior.patch` --
`git diff` output for `infra/aws/terraform/portal-auth/cloudfront-distribution.tf` only. 36 insertions, 0
deletions (numstat). Appends ONE `ordered_cache_behavior` block immediately after behavior 15
(`/api/scoped/investor-reporting/*`, `:898-933`) and before the `# --- Custom Error Responses ---` comment,
becoming behavior 16 at the END of the ordered list. Copied from behavior 15 field-for-field; only
`path_pattern` (`"/api/scoped/amgt/*"`) and the leading comment differ. Carries the SAME single
`viewer-request` association to `local.auth_validator_edge_arn` (live `auth-validator-edge:20`) that every
sibling scoped family already carries -- this is part of the act, not an option.

## 2. Exact commit command (run by the routed AE seat, in its own worktree, after applying the patch)

```
git apply org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~122/rk122_amgt_behavior.patch
bash .tools/safe-commit.sh --author "<AE serial> <<AE serial>@opal.agent>" -F <msgfile> -- infra/aws/terraform/portal-auth/cloudfront-distribution.tf
```

(`<msgfile>` written by the Write tool / python, never a shell heredoc/printf, per CLAUDE.md 14a.)

## 3. Exact safe-apply command

A fresh worktree needs init first (row W94-S1; writes only the local `.terraform/` directory):

```
terraform -chdir=infra/aws/terraform/portal-auth init -input=false
```

Then, NEVER a bare `terraform apply`:

```
HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/portal-auth apply -target=aws_cloudfront_distribution.portal
```

**Plan bound (measured by this worker, AC1, CONFORMS -- Branch A, second variant):** the targeted plan read
`Plan: 0 to add, 2 to change, 0 to destroy.` naming ONLY `aws_cloudfront_distribution.portal` (exactly one
`+ ordered_cache_behavior`, 0 removed) and `aws_wafv2_web_acl.opal_cloudfront_protection` (3 managed-rule
blocks removed and re-added, same rule-name set both sides, zero differing visible fields -- the durable
read-normalisation no-op the CTO's ruling admits, owner `0.7.0_AE_CloudOps`). `aws_cloudfront_function.spa_fallback`
carries NO diff line (only the unconditional refresh-log line every untouched resource in state also carries --
see surprise row `AMGT_RESAPP-Z-W122-S1`). If the AE seat's OWN plan differs from this shape (any third
resource, or a second changed attribute on the distribution beyond the one appended behavior), that is Branch
B: STOP, no apply, a BLOCKING row -- never a route this order did not name.

## 4. Deploy ledger

```
python .tools/deploy_ledger.py open --slug amgt-rk122-edge-behavior --title "AMGT-rk-122: /api/scoped/amgt/* edge behavior" --author "<AE serial>"
```

Opened BEFORE the apply. Closed on the AC3(b) post-apply read (section 6 below). The COO half names this
slug (`ledger/NEVER_WIDEN_ROUND30_RK122_COO_HALF.md:27`).

## 5. Post-apply verification commands (AC3's script)

Run `python .scratch/r122/ac3.py` (or the copy at
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~122/` if the AE seat's worktree lacks the
scratch copy -- the script is inlined verbatim in the task order's proof_of_spec, criterion AC3) against the
live distribution and site, in this order:

1. `live_behaviors` reads **29** (this worker's AC0/AC3(a) pre-read: 28), `amgt` reads **1**, and the amgt
   pattern is **LAST** in the list.
2. The `amgt_behavior` line reads `/api/scoped/amgt/*  APIGateway-portal  <caching-disabled policy id>
   [('viewer-request', 'auth-validator-edge:20')]` -- exactly one association, no more.
3. `BA_US_Equity` FIRST, then `992_HK_Equity`: each `post` line reads `401 application/json ... json True html
   False` for an unauthenticated request -- **a 401 here is a PASS** (it proves the edge validator is
   attached and reachable); a `200 text/html` is a FAIL.
4. The two control families (`/api/scoped/advisor-intelligence/summary`, `/api/general/health`) are UNMOVED:
   still `401 application/json`, `json True html False`.
5. **Propagation:** a CloudFront update is global and takes time to return; the predecessor's apply took 47s
   to return and the distribution then read `Deployed`. A single post-apply read that still shows HTML is
   RE-READ ONCE before being called a failure.

Close the ledger entry on this read. If any check fails after the re-read, see Rollback below rather than a
second apply attempt.

## 6. Rollback (per key, never a delete)

1. A NEW commit removing the one appended `ordered_cache_behavior` block from
   `cloudfront-distribution.tf` (never `git revert`/history rewrite).
2. The SAME targeted apply: `HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/portal-auth apply -target=aws_cloudfront_distribution.portal`.
3. `get-distribution-config` must read the pre-act count (28) with the amgt pattern count back to 0, and the
   targeted plan must then read `No changes.` (modulo the durable WAF read-normalisation artefact, B4 in the
   CTO half).
4. The same propagation window applies to the rollback (a warm edge may briefly still serve the removed
   behavior).
5. **Rollback triggers (any one):** post-act behavior count is not AC0's count + 1, or the amgt pattern count
   is not exactly 1 or not LAST; the new behavior's origin/cache policy/Lambda@Edge association differs from
   behavior 15's; ANY of the 28 pre-existing patterns changed, moved or disappeared; either control family
   stops returning `401 application/json`; the WAF's `get-web-acl` Rules JSON differs before vs after
   (LockToken excepted); an amgt path still returns `text/html` after the propagation re-read.
6. **The distribution is NEVER deleted or disabled**, in either direction.

## 7. Lane (for the record)

`infra/aws/**` -> lane `CLOUD_OPS_OR_ETL` (`.owned-paths.yaml:1906`); members `0.5.0_AE_OpalETL`,
`0.6.x_AE_PartnerETL`, `0.7.0_AE_CloudOps[~A~B~C]`, `0.8.0_AE_CloudComp`, `4.0.0_SA_CRO~SWEEP`. This worker's
own gate exercise (AC0) reproduced PERMIT for `0.7.0_AE_CloudOps` and REFUSE for `2.0.0_SA_COO~Z` and
`0.9.0_WK_AMGT_RESAPP~122`.

## 8. What this cell does NOT touch

Every other behavior, origin, cache policy, WAF RULE (as distinct from B4's read no-op), Lambda@Edge
function/version, the API Gateway routes (already mounted), the adapter, the portal bundle, any S3 object.
Not `Z-S227` (missing `isError` branches) -- separate defect, separate remedy.
