# Holes owned elsewhere -- round 8, cell BF-w-3 (0.9.0_WK_LGIC_BLANKFIX~4)

Each line below is a HOLE the root check still prints after every drafted registry row is applied (`check_holes_fill.py`
reads the OWNED lines and fails if one does not match a remaining hole or a remaining hole has none). The registry rows
for every other hole are in `REGISTRY_ROWS_round8.json` (owner `4.0.0_SA_CRO`).

Owner `1.0.0_SA_CTO`, text H8 of the FWD-6 owner table (`FWD6_DESIGN_round6.md`, row H8: "the grader gave verdict ... and no
form"): `opal_naming.grade` returns the verdict NOT-GRADED and no canonical form for the types ROUTE53_RECORD, IAM_USER and for a
log group named `aws-waf-logs-*`. The check has no rule for a type the canon deliberately does not grade, so it prints HOLE
where a NOT-ASKED line ("this type is outside the canon, no name is owed") would be true. What the CTO owes: one rule in
`lib/opal_naming_rootcheck.py` `decide()` that maps verdict NOT-GRADED to NOT-ASKED with that sentence (or a ruling that
the canon grades these types and the grammar rows that say how). No registry row can do it: the name rulings are read only
after the grader's verdict is known and a canonical form cannot be written for a type with no grammar.

OWNED portal-auth || ROUTE53_RECORD opalinvest.dev || 1.0.0_SA_CTO || rule: NOT-GRADED maps to NOT-ASKED, or a grammar for DNS records (infra/aws/terraform/portal-auth/email-auth-dns.tf:46)
OWNED portal-auth || ROUTE53_RECORD _dmarc.opalinvest.dev || 1.0.0_SA_CTO || same rule (email-auth-dns.tf:73)
OWNED portal-auth || ROUTE53_RECORD mail.opalinvest.dev || 1.0.0_SA_CTO || same rule (email-auth-dns.tf:101)
OWNED portal-auth || LOG_GROUP aws-waf-logs-opal-cloudfront || 1.0.0_SA_CTO || same rule; the aws-waf-logs- prefix is AWS's own requirement (waf-cloudfront.tf:276-277: wafv2 refuses a destination group whose name lacks it), so the name cannot be changed by the creator
OWNED opal-gateway || ROUTE53_RECORD mcp.opalinvest.dev || 1.0.0_SA_CTO || same rule (infra/aws/terraform/opal-gateway/main.tf:102)
OWNED opal-gateway || LOG_GROUP aws-waf-logs-opal-gateway || 1.0.0_SA_CTO || same rule and the same AWS prefix requirement (infra/aws/terraform/opal-gateway/waf.tf:22)
OWNED nfra-ctlpln-identity || IAM_USER cloudops-dell1-agent-user || 1.0.0_SA_CTO || same rule, or a grammar for IAM users (infra/aws/terraform/nfra-ctlpln-identity/iam.tf:19)
OWNED nfra-ctlpln-identity || IAM_USER cloudops-dell2-agent-user || 1.0.0_SA_CTO || same rule (iam.tf:24)
OWNED nfra-agentbus-alyssa01 || IAM_USER agentbus-alyssa01-fleet-alyssa-user || 1.0.0_SA_CTO || same rule (infra/aws/terraform/nfra-agentbus-alyssa01/main.tf:73)
OWNED website || IAM_USER patricia@thewhitelabelcreative.com || 1.0.0_SA_CTO || same rule; the name is a person's email address, set by the person's account, not by the canon (infra/aws/terraform/website/iam_patricia.tf:20)
