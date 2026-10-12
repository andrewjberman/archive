# NFRA_OPLGTW round 34 -- TERMINAL at the drain (2.0.0_SA_COO~O, 2026-10-11 ~22:4xZ)

Issued @c1743ee57e (+ E9 into OG-db-1 @0edc89d046) on `1.0.0_SA_CTO~Z`'s round-33 analysis @2672b8d28a. Apply workstream
APPLY-R34 was issued @84f96b6bf3.

`round-close-check --project NFRA_OPLGTW --round 34` reads `verdict=MAY-CLOSE` (judgment criteria 0). Of 10 orders, 9 are
complete and 1 is superseded (held).

## The orders

| order | cell | result |
|---|---|---|
| OG-db-1 | E6 + E9 | The allowlist hunk is back on trunk (5 of 5 reads, 54 of 54 keys kept). The wrapper's `--preflight-only` refuses a dirty tree and a tree missing the manifest-commit import closure. Drained @53beca075e. |
| OG-br-1 | E4 | Runbook 7.2 names the live release (rb.AC2 PASS); 10 of 10 manifest checksums come from the served release; the dispatcher `_build_note` is corrected; the SI2 puller's lock release and array range are fixed (repo only, not reinstalled on SI2). @625b54f616 |
| OG-mu-1 | E1 | The `.pptx` key is intake's content-addressed form; one builder-fed PutObject grant. The grant was applied by OG-ap-8. The `.pptx` RELEASE is a round-35 release cell (COO half condition C). @f769ef6103 |
| OG-gw-1 | E2 | The grant-writer package carries the live entitlement code; plan 0/1/0. Applied by OG-ap-9. @975fb09fca |
| OG-wr-1 | E5 | The 13-month window is primed (274 of 274 on 8 pairs). Warm read max **12.1 s** < 60, so no fan-out is needed. The cold first-dataset cost is 142-147 s per master. |
| OG-dq-1 | E7 | The DLQ drain "actor" is the declared 16:00Z silver sweeps: each drains the WHOLE shared DLQ and reports other families' failures as its own (row Z-S91). @94ddb37165 |
| OG-bd-1 | E8 | **SUPERSEDED (held).** The census found 2 unprofiled callers (one master_admin, 4 calls) of blackdiamond_list_fees. That is the ruling's STOP: no deny was built and an Andrew admission call is owed (row Z-W57-S2, surfaced by MSTR~Z msg 33359). Re-cuts in round 35. |
| OG-ap-7 | queue | CT-i-11 `/hx/teams/*` is live: release 28ba9532b6, GET /hx/teams/teams **200** (was 404), routes 53 -> 56. Pointer row NFRA_CTLPLN-Z-S6. |
| OG-ap-8 | E1 apply | gateway-market-update-put-policy is live, with 1 statement: PutObject on market_update bronze only. |
| OG-ap-9 | E2 apply | mcportal-grant-writer-lambda is rebuilt; the deployed package accepts calendar_months 13 and the prior refused it (session-free read-back). |

E3 was not cut: OG-rf-1's R50 send-gate is live by content (rows Z-S89 and Z-S90).

## The one real run of each served outcome

- **GET /hx/teams/teams 200** on the served gateway (`W~Z/AP7_SERVED.json`). ap7.AC2 was re-run by the issuer: PASS.
- **The live IAM statement** for market_update, read now (ap8.AC2, issuer re-run): PASS.
- **The live grant-writer CodeSha256** equals the build, and the deployed parse_scope takes 13 months (ap9.AC2, issuer
  re-run on the corrected check): PASS.
- **The warm 13-month read**: 12.1 s max (SSM 095a641c).

## Rows for the compile

- **ARMED (owner 2.0.0_SA_COO~O):**
  - Z-S85 (allowlist drain-back) is REMEDIATED by OG-db-1, and is for disarm at the compile;
  - Z-W57-S2 (BD admission) is held on Andrew.
- **Issuer check defects, all repaired before any wrong grade landed:**
  - Z-W54-S1 (closure path);
  - Z-W55-S1 (a test outside the paths; A1);
  - Z-W56-S2 (gw1 regex);
  - Z-S93 (ap9 function name; repaired, Z-S94).
  The lesson is carried to the issuer's cut template: a live check names its resource from the declaring source and
  fails loudly; every check gets a positive control against a real artifact before the cut.
- **Other rows:**
  - Z-S91: per-family DLQ drain, a round-35 code cell;
  - Z-S92: the teams bearer's group holders (CTO observation);
  - Z-W56-S4: cold figure 142-147 s, not 221-235 s;
  - Z-W55-S2: the `.pptx` quarter argument, for the release pair;
  - Z-S88: runbook drift, now repaired by br-1 and ap-7.

## Round 35 carry (for the analysis)

- the `.pptx` market_update gateway release;
- the BD deny, on Andrew's answer;
- the per-family DLQ drain (Z-S91);
- the teams bearer's dell consumer (Z-S92);
- reinstalling the SI2 puller;
- the release-cut template clauses: runbook 7.2; checksums; the `-var market_update_s3_root`; the agent home in the
  release cone; and that a TF resource name is not the live policy name.

-- 2.0.0_SA_COO~O
