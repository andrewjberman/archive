# Holes owned elsewhere -- round 9, cell BF-x-6 (0.9.0_WK_LGIC_BLANKFIX~3)

`check_holes_new_roots.py` reads the lines that begin `OWNED ` in this file and fails if one does not match a HOLE left on a
worked root, or if a HOLE left on a worked root has none. After the drafted rows of `REGISTRY_ROWS_round9.json` are applied to a
copy of the registry, the five worked roots (trade-pipeline 26, imo-pipeline 8, opsec 5, 49f-value-parity 1, estate-report 1)
print 0 HOLE lines, so this file carries no `OWNED` line.

**NOT-GRADED names (cell BF-x-1 rules them NOT-ASKED this round).** None of the 15 roots newly mapped at @1e660e15be carries a
verdict-NOT-GRADED name. The 10 H8 names that remain in the estate (hole 51 -> 10 once the drafted rows land) are the round-8 list, all
on older roots, owner `1.0.0_SA_CTO`, and are listed in `org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~4/HOLES_OWNED_round8.md`:
portal-auth (ROUTE53_RECORD x3, LOG_GROUP aws-waf-logs-opal-cloudfront), opal-gateway (ROUTE53_RECORD mcp.opalinvest.dev, LOG_GROUP
aws-waf-logs-opal-gateway), nfra-ctlpln-identity (IAM_USER x2), nfra-agentbus-alyssa01 (IAM_USER), website (IAM_USER). No draft here.

**What the registry owner (`4.0.0_SA_CRO`) still owes on the none_owed rows.** A `none_owed` row turns a HOLE into NOT-ASKED with a
reason; it does not name the thing the reason waits on. Three reasons wait:

- `trade` (22 name rulings, all of trade-pipeline): `systems.json` holds trade as an unresolved token (no directive owns the
  trade-submission pipeline). The rows are the astn precedent (`astn/kimi/api-key`). When the token is resolved, the 22 rows leave and
  each name takes its canonical form. The token ruling is the registry owner's.
- `opal-data-imo` and its seven `.keep` markers (8 rows): the bucket is retired by Andrew's card 9; the rows leave when the bucket does.
- `opal-data-security`, `opal-data-security-access-logs` and their two bucket policies (4 rows): the registry holds no scope row for
  security; the rows leave when the OpSec owner registers a scope.

**Two JUDGMENT calls in canonical rows**, marked in each row's evidence: the tier `state` for the sentinel allow list
(`opal-security-evidence` / `allowlists/partner-egress.json`, a reviewed configuration file, not workflow state in the R21 sense), and
the tier `state` for `config/last-trigger.json` in `opal-estate-report` (a per-run marker). The registry owner may rule either otherwise.

No cadence-reader defect was found on the five roots: no HOLE line of them carries a cadence clause, so `lib/opal_naming_cadence.py` and
its test are unchanged.
