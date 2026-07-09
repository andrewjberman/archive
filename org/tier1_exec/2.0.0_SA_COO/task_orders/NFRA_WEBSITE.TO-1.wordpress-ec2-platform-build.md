# Task Order: NFRA_WEBSITE TO-1 (W1) -- stand up the WordPress-on-AWS platform (EC2 in Opal VPC) + hand WP-admin to TWLC

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-08-nfra-website-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~A</issued_to>
    <co_assignee>0.5.0_AE_OpalETL</co_assignee>
    <date>2026-07-08</date>
    <status>complete -- W1 CLOSED 2026-07-09T19:45Z. RAVC-4 ACCEPTED by 2.0.0_SA_COO after INDEPENDENT live re-verification of 4 of the 6 ACs (a verifier who accepts a producer's self-report is not a verifier): AC-4 `aws ec2 describe-security-groups sg-062bbb40a6c92509c` -> tcp/80 + tcp/443 ONLY, ZERO port 22; AC-4 `get-bucket-versioning`/`get-bucket-encryption` on opal-website-backups -> Versioning=Enabled, SSE=AES256; AC-4 `list-attached-role-policies opal-website-wp-role` -> AmazonSSMManagedInstanceCore ONLY (firm-sep intact, zero data-estate reach); AC-5 DNS opalcapital.com -> 72.167.58.121 (GoDaddy host untouched, rollback point preserved, no record changed -- cutover is W3). Both W1 deploy ledgers CLOSED via the tool (nfra-website-w1 6/6, nfra-website-iam 4/4); `deploy_ledger check --red` shows no nfra-website entry. Owner 0.7.0_AE_CloudOps~A exercised every AC against LIVE state per CLAUDE.md 22a -- none config-read. THE DELIVERABLE WAS THE CATCH, not the build: the WordPress DB user held `ALL PRIVILEGES ON *.*` because the least-priv enforcement regex matched the WRONG SIDE of `ON *.*` -- i.e. a control that existed, ran, reported success, and enforced nothing (fixed + exercised, f05629cf5). That is the session's through-line in its purest form -- an instrument whose own success condition was decoupled from the property it existed to guarantee -- alongside the deploy-ledger prose-vs-sentinel drift, cmtque-worker-down latched-in-ALARM, the parity alarms blind on a 401, the 18-day cot ingest guard asserting BYTES where the property is ROWS, fabric-check calling 5 legitimately-HELD ledgers "half-landed RISK", and COO's own `--quiet 2>/dev/null` stale read. Two self-found defects also closed: EC2_MANIFEST duplicate `opal-website-wp` key (c88de96f7) + stale infra/website README inventory. Grounded W3 de-risk banked: the apex resolves to the GoDaddy host DIRECT, not a Cloudflare edge IP, so Turnstile is CAPTCHA-widget-only and W3 is a clean apex-A flip with no proxy to unwind. NFRA_WEBSITE remains ACTIVE -- W2 (TLS/SMTP/backups/hardening) GO'd 194309Z; W3 (GoDaddy apex-A cutover) follows. This TO covers W1 only.</status>
    <dispatch_state>DISPATCHED + GO 2026-07-08 (Andrew-direct un-park + GO). NFRA_WEBSITE was HELD at PRD since 2026-07-01; Andrew greenlit it now + the 5 PRD open-decisions are resolved (see below). DEDICATED AE per Andrew: 0.7.0_AE_CloudOps~A = OWNER (CloudOps lane, spawn via MSTR), 0.5.0_AE_OpalETL = IMMEDIATE first-mover (online+idle now -- starts the TF scaffold + backup/signal grounding so we don't wait on the spawn). PRD: docs/architecture/NFRA_WEBSITE_PRD.md (CTO 2026-07-01, grounded vs the 2 backups). W1 of W1/W2/W3.</dispatch_state>
    <gate_note>Gates: none upstream (DNS already on GoDaddy). HARD LEASH (PRD): lift-and-shift (NO redesign); keep GoDaddy DNS (NO record changes in W1 -- cutover is W3); NEVER destroy/touch the old host; harden the public WP surface; network-isolate from the data estate. Deploy discipline: Terraform-only, safe-apply + HALTGT, deploy-ledger open->close, EC2_MANIFEST registration.</gate_note>
  </metadata>

  <objective>Stand up the AWS PLATFORM for the Opal Capital WordPress site (lift-and-shift into the Opal estate) so The White Label Creative's (TWLC) developer can migrate the existing Bricks site onto it. Opal provides the platform + WP-admin access; TWLC does the CONTENT migration. Per Andrew's 07-06 spec + the PRD SS3: one right-sized EC2 in the Opal VPC (NOT RDS, NOT Fargate, NOT Lightsail, NOT CloudFront), Elastic IP for the GoDaddy apex A-record, local MariaDB, S3 backups, Let's Encrypt TLS, hardened.</objective>

  <decisions_resolved>Andrew's emails + this GO resolve the PRD SS10 open decisions: (1) hosting = EC2-in-VPC (Andrew 07-06: "single small/medium EC2... don't see why we'd need RDS"); (4) CloudFront = NO/later ("hand an Elastic IP to GoDaddy and leave it at that"); (5) record shape = apex A -> EIP, www CNAME -> apex (W3). STILL to CONFIRM during the build (not W1 blockers): (2) email SES-vs-existing-SMTP (W2 -- default SES only if a DKIM-verified sender domain is clean per CLAUDE.md Rule 23, else keep existing SMTP); (3) is Cloudflare currently PROXYING the site or only the Turnstile CAPTCHA widget (ground it from the backup/DNS -- affects W3 cutover).</decisions_resolved>

  <requirements>
    <requirement id="1">TERRAFORM (infra/aws/terraform/website/): provision 1x EC2 t3.small/medium in the existing Opal VPC + an Elastic IP + a security group (80/443 public; NO open 22 -- SSM Session Manager only) + an IAM instance role scoped to an S3 backup bucket + the S3 backup bucket. Register in infra/aws/ec2/EC2_MANIFEST.json. safe-apply (HALTGT) + open a deploy-completion ledger entry at apply-start, close at completion.</requirement>
    <requirement id="2">STACK on the instance: OpenLiteSpeed + PHP 8.x + MariaDB LOCAL (16MB DB does not warrant RDS; OpenLiteSpeed keeps the site's litespeed-cache plugin working) + a base WordPress install (wordpress.org, self-hosted). Least-priv local DB user. Code/config delivered per the EC2 code-deployment standard (S3 -> box), NOT inline-in-SSM.</requirement>
    <requirement id="3">CREATE a WordPress ADMIN account for Patricia Barboza (patricia@thewhitelabelcreative.com) -- WP-admin ONLY, NOT any AWS/SSM/console access. This is the handoff point: her developer migrates the existing Bricks site (theme + 18 plugins + 16MB DB + 13MB media, per PRD SS2) onto this platform. Deliver her credentials securely (do NOT email a plaintext password; use a WP password-reset link to her address or a secure channel).</requirement>
    <requirement id="4">HARDEN (public WP attack surface, PRD SS6): SG-locked + SSM (no open SSH); OS+WP auto-updates; DISALLOW_FILE_EDIT; the site's own hardening plugins (wps-hide-login, wps-limit-login, Turnstile) carry over on TWLC's migration; UpdraftPlus->S3 offsite backup schedule + an AMI/EBS-snapshot schedule; network-isolate from the data estate (firm-sep: this box NEVER gets any data-pipeline IAM).</requirement>
    <requirement id="5">GROUND the 2 PRD signals (0.5.0 can do this immediately from the backups in-context / the PRD SS2): (a) does Cloudflare currently PROXY the site (front) or is it only the Turnstile CAPTCHA -- affects the W3 cutover; (b) confirm the OpenLiteSpeed choice keeps litespeed-cache working. Report both to COO for the W2/W3 plan.</requirement>
    <requirement id="6">LANE SPLIT: 0.5.0_AE_OpalETL (online NOW) starts req-1 TF scaffolding + req-5 grounding immediately as first-mover. 0.7.0_AE_CloudOps~A (dedicated owner, on spawn) owns the stack install (req-2), WP-admin handoff (req-3), hardening (req-4), and the end-to-end W1 close. Co-author the TF; coordinate directly so you don't collide on infra/aws/terraform/website/.</requirement>
    <requirement id="7" note="Andrew-direct 2026-07-08">ALL-TERRAFORM + ALL-LOGGED (non-negotiable, Andrew-direct): EVERY AWS resource in this project is Terraform-declared in infra/aws/terraform/website/ and applied via safe-apply(HALTGT) -- NO console/manual/click-ops resource, ever. EVERY resource is registered in infra/aws/ec2/EC2_MANIFEST.json; every apply opens+closes a deploy-completion ledger entry; the AE session log records it. Maintain the RESOURCE INVENTORY table in infra/website/README.md (the TF address of every resource) as the single source of truth as W1 lands.</requirement>
    <requirement id="8" note="Andrew-direct 2026-07-08">DOCS HOME = infra/website/ (Andrew-direct): all website documentation/architecture/related files live under infra/website/ (already seeded: README.md index + the 3 architecture SVGs current/target/migration). AUTHOR there as you build: the runbook (deploy/backup-restore/cutover/rollback), the network doc, the WP-admin credential-handoff record (Patricia @ TWLC), the W2 TLS/SMTP notes, the W3 cutover checklist. The canonical PRD stays at docs/architecture/NFRA_WEBSITE_PRD.md (convention); infra/website/ is the operational/build home + resource-inventory source of truth.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">comp-iam service (the new EC2 instance role -- confirm it's scoped to ONLY the S3 backup bucket, no data-estate access) + comp-aws blast on the website TF module (new resources, no collision with existing estate).</phase>
    <phase name="before_commit">.tools/commit-gate.sh on any .py; comp-iam gaps after the iam.tf (least-priv confirm); safe-apply drift-plan.</phase>
    <phase name="after_commit">comp-iam reconcile (applied vs desired on the new role); verify SG has no open 22 (live aws describe-security-groups); confirm SSM Session Manager reaches the box (exercise, not config-read).</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>TWLC (external, patricia@thewhitelabelcreative.com + her developer) does the CONTENT migration between W1 (this TO) and W2. Opal provides the platform + WP-admin. Notify COO when the platform is ready + Patricia's admin is created so COO can (via Andrew) tell Patricia it's ready for her dev.</item>
    <item>CVO live-verifies the served site at the W2 staging gate (pages render/Bricks, forms submit+email, TLS, no mixed-content) BEFORE any W3 cutover. NEVER destroy the old host until CVO-verified live.</item>
    <item>Firm-separation: this public WP box is network-isolated from the data estate; its IAM role NEVER touches any pipeline bucket. (NEVER#1-adjacent -- a public WP is a pivot surface.)</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>EC2 running in the Opal VPC, Terraform-managed (infra/aws/terraform/website/), registered in EC2_MANIFEST.json; deploy-ledger opened+closed.</criterion>
    <criterion>Base WordPress reachable on the Elastic IP (or a staging hostname/hosts-override) -- wp-admin loads.</criterion>
    <criterion>Patricia Barboza has a WORKING WP-admin account (WP-only, no AWS); credentials delivered securely (not plaintext email).</criterion>
    <criterion>S3 backup bucket + IAM instance role exist; SG has NO open port 22 (SSM-only, exercised); MariaDB local with a least-priv DB user.</criterion>
    <criterion>The old host is untouched + still live (rollback point preserved); no GoDaddy DNS record changed (that's W3).</criterion>
    <criterion>Cloudflare-proxying + LiteSpeed-cache signals grounded + reported to COO for W2/W3.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/NFRA_WEBSITE_PRD.md (CTO 2026-07-01, grounded vs the updraft + opalcapital backups)</ref>
    <ref type="project">org/projects/NFRA_WEBSITE.json</ref>
    <ref type="email">Patricia Barboza (TWLC) thread in andrew@opalinvest.com -- "Update on Wordpress for AWS" (Andrew's 07-06 EC2 spec) + 07-07 "setup wordpress.org on AWS, add me as WP admin, our dev migrates" + 07-08 nudge. DNS already moved WIX->GoDaddy (07-08).</ref>
  </references>
</task_order>
```
