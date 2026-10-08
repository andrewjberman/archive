# PLAN NOTE -- three Dell limits lifted in ONE plan: secrets, the resource-policy Deny (now the resource-policy ALLOW), self-simulate (NFRA_CTLPLN.TO-CT-a-1, amendments 9 and 10)

Author: 0.9.0_WK_NFRA_CTLPLN~14. Supersedes the amendment-8 version of this note; amendment 10 (`1.0.0_SA_CTO` msg 106731, ruling 1) adds the resource-policy Allow (section B) and the section "What this Allow can undo". NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE. NO SECRET VALUE WAS READ: this pass made no Secrets Manager call at all; the classification works from the saved listing (`tests/vendor_secrets_census.json`, taken 2026-10-07T21:00:45Z with `list-secrets`: names, descriptions, tags, key ids, dates) and from the code that uses each secret. Authority: Andrew-direct ~00:4xZ "lets start with lifting 1 2 3 6" (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_004xZ_LIFT_FOUR_DELL_LIMITS_SECRETS_FIRM_DATA_RESOURCE_POLICIES_PUSH.md`) and `1.0.0_SA_CTO` msg 106669.

## What the ONE apply would show -- by reading the configuration, NOT from a plan

Read from the configuration and the diff of this commit; no `terraform plan` was run. Relative to the state the previous pass left (the root as of its amendment 8):

| change | resource | action |
|---|---|---|
| A secrets | `aws_iam_policy.dell_agent_vendor_secrets[0]` (`cloudops-dell-agent-vendor-secrets-policy`, 66 exact secret ARNs, 5968 characters of 6,144) | created |
| A secrets | `aws_iam_group_policy_attachment.dell_agent_vendor_secrets[0]` to `cloudops-dell-agents-group` | created |
| B resource-policy Deny | `aws_iam_policy.dell_agent_respol` (`cloudops-dell-agent-respol-policy`) | destroyed |
| B resource-policy Deny | `aws_iam_group_policy_attachment.dell_agent_respol` | destroyed |
| B resource-policy ALLOW (amendment 10) | `aws_iam_policy.dell_agent_respol_allow[0]` (`cloudops-dell-agent-respol-allow-policy`, 70 actions, 2,195 characters of 6,144) | created |
| B resource-policy ALLOW (amendment 10) | `aws_iam_group_policy_attachment.dell_agent_respol_allow[0]` to `cloudops-dell-agents-group` | created |
| C self-simulate | `aws_iam_policy.dell_agent_create` (`cloudops-dell-agent-create-policy`): two statements added to its document: `SimulateOwnPolicyOnly` and (amendment 11) `ReadPublicAmiParameter`; document now 4,339 characters of 6,144, whitespace not counted | updated in place |

Expected: 4 to add (the secrets policy and attachment, the new Allow policy and attachment), 1 to change (the create policy, in place; its document gains TWO statements, `SimulateOwnPolicyOnly` and `ReadPublicAmiParameter`), 2 to destroy (the former Deny policy and its attachment). The group then holds six managed policies (deploy, create, routes-fn, routes-host, secrets, respol-allow) against the quota of ten (`check_identity.py` prints `group managed-policy attachments=6 quota=10`); neither new document needs the split rule (secrets 5,968 and respol-allow 2,195 of 6,144 characters). WHAT THIS NOTE CANNOT SAY: whether the earlier, merged work of this order (the two routes Deny policies, the dell2 SSM policy and the other per-user policies) is already applied. I did not read the backend. If any of it is not applied, the plan will show those as additional creates; that is not part of this change. The simulator and the configuration are read, not planned.

## A. SECRETS -- the new rule, over all 114 listed secrets

Four classes, one each, by NAME, DESCRIPTION, TAGS and the code that uses the secret, whether or not a Dell project's code names it today. Result: **VENDOR-CREDENTIAL 35, CLIENT-SESSION 32, PLATFORM-KEY 28, OTHER 19** (sum 114). **GRANTED 66** = those of the first two classes under the account's default key; **BLOCKED-BY-KEY 1** (`schwab/sdd/session`). The grant is ONE statement `ReadVendorCredentialsAndClientSessions`, `secretsmanager:GetSecretValue` only, on 66 exact ARNs (full ARN with the six-character suffix, no wildcard; each entry matches exactly one listed secret, and no listed secret outside the granted set is matched: simulation line `VENDOR-ONE-TO-ONE`). Document size: 5968 characters of 6,144 (whitespace not counted), so it is NOT split; headroom is 176 characters, so one or two further granted secrets will need the split, which is by class (one policy per granted class). The listing is of 2026-10-07T21:00:45Z; a secret created since is not in the grant, and a secret scheduled for deletion is not returned by `list-secrets`, so none was seen. Take the census again (`derive_vendor_secrets.py --live`) before the apply if the date matters.

Differences from the previous (amendment 8) grant of 9: IN now: 60 more, including `openai-api-key` (ruled IN by msg 106669). OUT now: `gateway/mail/bearer` (PLATFORM-KEY), `opal/auth/origin-verify` (PLATFORM-KEY), `opal/auth/irpt-render-jwt-public-key` (OTHER: a public key).

### GRANTED -- client sessions and logins (31 in the grant, 32 in the class)

- `aaii/credentials` -- cookie bundle (captured session) for aaii.com; description
- `astn/ft/credentials` -- Financial Times subscription login; description
- `astn/ft/session` -- Financial Times authenticated session cookie bundle; description
- `blackdiamond/49f/credentials` -- 49 Financial's Black Diamond login (username and password); description
- `blackdiamond/49f/session` -- 49 Financial's Black Diamond captured session; description
- `blackdiamond/cot/credentials` -- Cottonwood's Black Diamond login; description
- `blackdiamond/cot/session` -- Cottonwood's Black Diamond session cookie; description
- `bloomberg/session` -- Bloomberg.com parked session bundle; description and tag kind=site-session
- `bloomberg/terminal/login` -- Bloomberg Terminal sign-in for the daily-pull seat (a vendor login used to pull data); description
- `conferenceboard/credentials` -- cookie bundle (captured session) for conference-board.org; description
- `dowjones/barrons/session` -- Barron's session; no description, the name places it as a captured session
- `dowjones/credentials` -- shared WSJ and Barron's subscriber login; description
- `dowjones/wsj/session` -- WSJ session; no description, the name places it as a captured session
- `opal/bd/cottonwood/credentials` -- Black Diamond portal login for the Cottonwood tenant; description
- `opal/bd/credentials` -- Black Diamond portal login credentials; description
- `orion/credentials` -- Orion Advisor platform login; description
- `orion/eclipse_jwt/current` -- captured Eclipse session JWT of the Orion platform; description
- `orion/jwt/current` -- captured Orion Advisor session JWT; description
- `schwab/sdd-credentials` -- Schwab SDD login (user id and password), the custodian's portal; description
- `schwab/sdd/session` **(NOT in the grant: blocked by key)** -- Schwab SI2/SDD standing session blob (custodian session); description. Under a customer-managed key: left out as blocked-by-key
- `seeking-alpha/credentials` -- Seeking Alpha sign-in; description and tag kind=site-login
- `seeking-alpha/session` -- Seeking Alpha parked session bundle; description
- `smartx/cookie/current` -- SmartX session cookie slot; description
- `smartx/credentials/password` -- SmartX password; description
- `smartx/credentials/username` -- SmartX username; description
- `smartx/credentials/yaliu-bundle` -- SmartX account-tier credential bundle; description
- `smartx/credentials/yang-shared` -- a person's SmartX login shared with the firm; description and tag Vendor=SmartX
- `smartx/jwt/current` -- SmartX parked session JWT; description
- `ycharts/credentials` -- YCharts platform login; description
- `ycharts/login/credentials` -- YCharts report-automation login; description
- `ycharts/session/current` -- YCharts captured session cookie bundle; description
- `ycharts/session/research-20260911` -- YCharts session-transport experiment (captured session, no login password); description

### GRANTED -- vendor credentials (35)

- `FredApiKey` -- St. Louis Fed FRED data API key; no description, the name and data/yang_macros_re/adapters/fred_adapter.py:6 place it
- `ai/claude-api-key` -- model-provider API key; the name says Claude and the description says an OpenAI key for the SmartX exporter AI fallback; a vendor key either way
- `anthropic-api-key` -- Anthropic API key; no description, the name and infra/aws/lambda/exec-summary-generator/config.py:32 place it
- `astn/brightdata/residential-proxy` -- Bright Data residential proxy credential (host:port:user:pass per bd_49f_auto_login.js:27)
- `astn/kimi/api-key` -- Moonshot AI (Kimi) API key; description
- `brightdata-api-key` -- Bright Data Web Unlocker API key; description
- `find-dualbiz/bright-data/serp` -- Bright Data SERP API zone credential; description
- `find-insure/bright-data/api-key` -- Bright Data Crawler API key; description and tag Provider=BrightData
- `find-insure/bright-data/scraping-browser-creds` -- Bright Data scraping-browser zone credentials; description and tag Provider=BrightData
- `find-insure/job-board/builtin/api-key` -- Built In job-board credentials; description and tag Provider
- `find-insure/job-board/efinancialcareers/api-key` -- eFinancialCareers job-board credentials; description and tag Provider
- `find-insure/job-board/glassdoor/api-key` -- Glassdoor job-board credentials; description and tag Provider
- `find-insure/job-board/indeed/api-key` -- Indeed job-board credentials; description and tag Provider
- `find-insure/job-board/insurancejobs/api-key` -- InsuranceJobs.com job-board credentials; description and tag Provider
- `find-insure/job-board/linkedin-jobs/api-key` -- LinkedIn Jobs job-board credentials; description and tag Provider
- `find-insure/job-board/wellfound/api-key` -- Wellfound job-board credentials; description and tag Provider
- `find-insure/job-board/ziprecruiter/api-key` -- ZipRecruiter job-board credentials; description and tag Provider
- `find-insure/lusha-ai/api-key` -- Lusha API key; description and tag Provider=LushaAI
- `massive-api-key` -- Massive market-data API key; description
- `msci-api-credentials` -- MSCI Index API credentials (basic auth); description
- `multi-threadv2` -- OpenAI API key for the Corporeal multi-thread runtime; description
- `nopecha/api-key` -- NopeCHA captcha-solving service API key; description and tag kind=vendor-api-key
- `ocilar/credentials` -- Ocilar hCaptcha solver API key; description
- `opal/opalai/analyst-claude-oauth-token` -- Claude Code OAuth token for the Opal_AI analyst runtime (a model provider's account token); description. Judgment call: it signs in as one named account at the vendor, it does not act as Opal's platform
- `opal/openai/andrew-fideles` -- OpenAI key under the opal/openai/ namespace; no description, the name places it (one of five siblings)
- `opal/openai/aws-lambda-ki` -- OpenAI key under the opal/openai/ namespace; no description, the name places it
- `opal/openai/layer3-curation` -- OpenAI key; no description, the name and infra/aws/scripts/analyze_openai_costs.py:74 place it
- `opal/openai/market-update` -- OpenAI key under the opal/openai/ namespace; no description, the name places it
- `opal/openai/news-trending` -- OpenAI key; the code reads it as OPENAI_SECRET (infra/aws/lambda/keyword_intelligence_generator/lambda_function.py:46)
- `openai-api-key` -- OpenAI API key; name (ruling: msg 106669 says it is IN)
- `price_discovery` -- OpenAI API key for price-discovery ticker mapping; description
- `quo/api-key` -- Quo (messaging provider) API key; description and tag kind=api-key
- `rivalfunds/openai-api-key` -- copy of openai-api-key for the ETFS_RIVALS accounts; description and tag copy_of
- `seeking-alpha/bright-data-api-key` -- Bright Data API key for the Seeking Alpha scraper; description
- `twilio/credentials` -- Twilio account SID, auth token and phone number (messaging provider); description

### PLATFORM-KEY -- NOT granted (28); what holding each would let a box do

- `blackdiamond/49f/otp-gateway-token` -- Lets a box fetch the one-time sign-in codes of the 49 Financial Black Diamond account from the firm's own gateway, which completes that account's multi-factor sign-in.
- `blackdiamond/cot/otp-gateway-token` -- Lets a box fetch the one-time sign-in codes of the Cottonwood Black Diamond account from the firm's own gateway, which completes that account's multi-factor sign-in.
- `gateway/global/taxsma-workbook-token` -- Lets a box call the gateway's tax-workbook route as an authorised caller and read what it serves.
- `gateway/mail/bearer` -- Lets a box call the gateway's mail route (/hx/mail) as an authorised caller and read the mail it serves. (The previous plan granted this one.)
- `gateway/principals/rosters` -- Gateway read secret created for the principal rosters: lets a box read the gateway's list of authorised principals; kept PLATFORM-KEY because it could not be placed more narrowly.
- `gateway/teams/bearer` -- Lets a box call the gateway's Teams route as an authorised caller.
- `gateway/transcripts/bearer` -- Lets a box call the gateway's transcripts route as an authorised caller and read what it serves.
- `inf/otp-relay/token` -- Lets a box pass the gate of the firm's one-time-code relay service and read or post codes through it.
- `irpt/svc-irpt-analysis/password` -- Lets a box sign in as the firm's IRPT Analysis service account, with whatever that account may do.
- `opal/auth/irpt-render-jwt-private-key` -- Lets a box mint render tokens that the firm's edge accepts as genuine, which is acting as the render service.
- `opal/auth/jwt-private-key` -- Lets a box sign portal login tokens for any user, administrators included.
- `opal/auth/origin-verify` -- Lets a box call the portal's origin directly and skip the edge's checks (the CloudFront origin-verification secret). (The previous plan granted this one.)
- `opal/mcp/graph-read-token` -- Lets a box read the firm's estate-graph service as an authorised caller.
- `opal/mcp/ms-ingest-token` -- Lets a box call the gateway's /ms/* ingest endpoint as an authorised caller.
- `opal/mcp/opal-gateway-blackdiamond-reader-external-id` -- Is the external id of the gateway's Black Diamond read role; a box holding it can satisfy that role's trust condition when assuming it.
- `opal/mcp/opal-gateway-fernet` -- Lets a box decrypt, read and forge the gateway's cached tokens and OAuth state.
- `opal/mcp/opal-gateway-jwt` -- Lets a box sign tokens that the gateway accepts as its own authorisation server.
- `opal/mcp/opal-gateway-schwab-account-ref-key` -- Lets a box compute and verify the gateway's keyed references to the custodian's accounts.
- `opal/mcp/opal-gateway-schwab-reader-external-ids` -- Are the external ids of the gateway's Schwab reader roles; a box holding them can satisfy those roles' trust condition when assuming them.
- `opal/mcp/opalbloomberg-login` -- Lets a box sign in to the firm's directory as the gateway's Bloomberg identity (the multi-factor code still goes to Andrew).
- `opal/portal/svc-data-refresh` -- Lets a box call the firm's m365 gateway as the portal's data-refresh service.
- `opal/pseudonym/49financial` -- Lets a box reverse or recreate the pseudonyms of one client firm's data.
- `opal/pseudonym/opal-capital` -- Lets a box reverse or recreate the pseudonyms of the firm's own data.
- `opal/ticketing/svc-analyst-intake` -- Lets a box create and list tickets in the firm's ticket API as the analyst-intake service.
- `opalinvest/admin-seed` -- Lets a box create or sign in as the portal's administrator.
- `opalinvest/jwt-secret` -- Lets a box sign portal login tokens for any user (the shared signing secret).
- `schwab/anonymization-key` -- Lets a box reverse or recreate the Schwab data's anonymised identifiers.
- `schwab/ec2-credentials` -- Lets a box log in as Windows Administrator on the firm's Schwab EC2 box.

### OTHER -- NOT granted (19); for a person to rule

- `blackdiamond/49f/otp-relay` -- transient relay of a one-time code (a bridge value), neither a login nor a session; a person rules
- `blackdiamond/cot/otp-relay` -- transient relay of a one-time code (a bridge value), neither a login nor a session; a person rules
- `estate-report/github-token` -- read-only GitHub token for the firm's own repository (description, tags): a credential for the firm's own source, not a vendor data pull; doubt resolves to OTHER
- `find-insure/job-board/placeholder` -- namespace reservation (description, Provider=Reserved): holds no credential
- `github-token` -- no description; the code (.tools/comp-deadgrant.py, the daily-agenda generator) shows a GitHub token for private repositories, whose scope cannot be placed
- `google-cse-config` -- configuration bundle with no description (Google Custom Search); not placeable as a key
- `google/andrew-goldengate/credentials` -- a Google account login (identity account used for sign-in-with-Google flows), not a vendor data credential; doubt resolves to OTHER
- `google/officialmadeaux/credentials` -- a Google account login (identity account used for sign-in-with-Google automation), not a vendor data credential; doubt resolves to OTHER
- `opal/auth/irpt-render-jwt-public-key` -- a public key (RS256 verification); description
- `opal/auth/jwt-public-key` -- a public key (RS256 verification); description
- `opal/external-apis` -- configuration bundle with no description; not placeable
- `opal/finbert/config` -- configuration bundle with no description; not placeable
- `opal/mcp/opal-gateway-graph` -- the firm's own directory (Entra) application credential for the gateway's Graph client; description
- `opal/mcp/opal-gateway-login` -- the firm's own directory (Entra) application credential for the gateway's login; description
- `opal/portal/config` -- configuration bundle with no description; not placeable
- `opal/smartx/config` -- configuration bundle with no description; not placeable
- `opal/smartx/qa-models` -- configuration bundle with no description; not placeable
- `teams/global/owner-phone` -- Andrew's mobile number (description): personal data, not a credential
- `twilio/recovery-code` -- Twilio account recovery code: an account-reset item, not a key or a sign-in; doubt resolves to OTHER

### Where I chose the cautious class

`opal/auth/origin-verify` (AMENDMENT 9 lists "an origin-verify value" under OTHER; the issuer's dispatch says PLATFORM-KEY; both are not granted, I used PLATFORM-KEY under the doubt rule); `gateway/principals/rosters` (PLATFORM-KEY by doubt); `estate-report/github-token`, `github-token`, both Google account logins, `twilio/recovery-code`, the two one-time-code relays, the placeholder reservation and the configuration bundles (OTHER). Judgment calls that went the OTHER way (granted): `opal/opalai/analyst-claude-oauth-token` (a model provider's account token, VENDOR-CREDENTIAL), `smartx/credentials/yang-shared` (a person's vendor login shared with the firm, CLIENT-SESSION), the five `opal/openai/*` keys and `FredApiKey` (no description; classed by name and the code that reads them), and `bloomberg/terminal/login` (CLIENT-SESSION).

## B. THE RESOURCE-POLICY DENY COMES OFF, AND AN ALLOW GOES ON (amendment 10)

Removed (amendment 9): `aws_iam_policy.dell_agent_respol` and its group attachment (`iam.tf`), the Deny document that was `dell_respol_policy.json` (that path now holds the data, below), the old `tests/derive_respol_actions.py` (rewritten). Kept untouched: the routes Deny (`routes.tf`, `modules/routes_policy/`), `DenyPassRoleExceptNamed`, `DenyProtectedFunctions`, `DenyApiKeyReads`, `DenyEveryIamWrite`, `DenyCloudTrailWrites`, and `tests/read_queue_attribute_writers.py` with its saved file.

Removing the Deny alone freed one action (`sqs:SetQueueAttributes`, which the create policy already allows): 71 of the 75 stayed refused for want of an Allow. `1.0.0_SA_CTO` msg 106731 ruling 1 adds the Allow, and this pass builds it.

### The Allow: how many of the 75, and which are left out

**The Allow covers 70 of the 75.** One managed policy, `cloudops-dell-agent-respol-allow-policy` (name from `lib/opal_naming.name()`; `check_identity.py` MATCH), one statement `AllowResourcePolicyChanges`, Effect Allow, `Resource: "*"`, no condition, the 70 actions sorted. 2,195 characters of 6,144 (whitespace not counted), so it is NOT split. The list of 75 is DATA in `infra/aws/terraform/nfra-ctlpln-identity/dell_respol_policy.json` (per action `in_allow`, `exclusion`, `reason`, and for an excluded one the decision it must read). The lane gate refused a new file name, so the data sits at the path the order's grant already names, the path of the removed Deny; it is a DATA document, not an IAM policy (no `Statement` key), and nothing attaches it. The policy document is BUILT by Terraform from it, in the pure module `modules/routes_policy` (the way the secrets Allow is built from its census), and `tests/derive_respol_actions.py --write` renders the data while `--check` compares the data and the Terraform-built document (a printed LAST line `RESPOL-ALLOW actions=75 in_allow=70 excluded=5 ... ok=True`). The 75 are read from `git show c7c6d13b85:infra/aws/terraform/nfra-ctlpln-identity/dell_respol_policy.json` and the check re-reads them and requires equality.

**The 5 left out, by exclusion** (exactly the four of AMENDMENT 10 item 2; none added):

- (a) every `iam:` action (item 4 is not lifted) -- 1 action: `iam:UpdateAssumeRolePolicy`. It also reads explicitDeny by `DenyEveryIamWrite`.
- (b) the subject of the routes Deny -- 0 actions. The routes Deny names the ten Lambda write actions, three ECS actions, five SSM document actions and `s3:PutObject`; the intersection with the 75 is EMPTY (printed: `ROUTES-DENY-INTERSECTION none (empty)`).
- (c) already denied explicitly for every resource by a statement that stays -- 2 actions: `cloudtrail:DeleteResourcePolicy`, `cloudtrail:PutResourcePolicy` (`DenyCloudTrailWrites`). A Deny that covers an action only on some resources is not an exclusion: `s3:DeleteBucketPolicy` is denied by `DenyS3DeletesOnProductionData` on the `opal-data-*` buckets only, so it stays in the Allow (it reads allowed on the Terraform state bucket and explicitDeny on the three firm buckets, below).
- (d) the Secrets Manager resource-policy actions (the ISSUER'S exclusion, for the CTO to confirm or overrule in its half) -- 2 actions: `secretsmanager:DeleteResourcePolicy`, `secretsmanager:PutResourcePolicy`. Reason in the data: "would undo the secrets carve-out of this plan (issuer; CTO to confirm)". In one account a resource policy on a secret that names a Dell user is enough to let it read that secret, so these two would let a Dell grant itself the 28 platform keys this plan withholds. They read implicitDeny (the create policy does not allow them). If the CTO overrules, they come back by setting `in_allow` true in the data (and `summary.in_allow` with it, which a precondition in `iam.tf` compares) and re-rendering.

### What the simulator reads (both users, effective set = group policies + the user's per-user policies + the new Allow + the two routes Deny documents)

- `freed_allowed=70/70`: every `in_allow` action reads `allowed` for both Dell users on a representative resource of its service (line `FREED-COUNT in_allow actions reading allowed for both users 70 of 70`).
- `freed_excluded=5`: every excluded action reads its stated decision for both users (`FREED-COUNT ... 5 of 5`): `iam:UpdateAssumeRolePolicy` explicitDeny by `DenyEveryIamWrite`; both `cloudtrail:` actions explicitDeny by `DenyCloudTrailWrites`; both `secretsmanager:` actions implicitDeny.
- The control (same request WITHOUT the new Allow): no `in_allow` action reads explicitDeny, and exactly one reads allowed without it, `sqs:SetQueueAttributes` (the create policy), so the Allow adds 69 new abilities per user and nothing for that one.
- The routes arms (ROUTES-ARM 5), the pass-role arms, the nine protected-function arms, the API-key probe, the allowed (22) and remaining denied arms (15), the self-simulate arms and the SSM arms read exactly as before; `routes_ok=5/5`.

A Dell changing a resource policy does so under its own box's never-widen pair; the laptop is told and steps in on an overlap.

## C. SELF-SIMULATE

One statement `SimulateOwnPolicyOnly` in the group's create policy: Allow `iam:SimulatePrincipalPolicy` on `arn:aws:iam::313476888478:user/${aws:username}`. One statement serves both users; neither can simulate the other or any role. Simulation (context key `aws:username` set per user):

- SELFSIM-ARM 01 dell1 simulates ITSELF: iam:SimulatePrincipalPolicy on user/cloudops-dell1-agent-user -> allowed (want allowed) OK
- SELFSIM-ARM 02 dell1 simulates the OTHER Dell user (dell2): iam:SimulatePrincipalPolicy on user/cloudops-dell2-agent-user -> implicitDeny (want refused) OK
- SELFSIM-ARM 03 dell1 simulates a ROLE: iam:SimulatePrincipalPolicy on role/x -> implicitDeny (want refused) OK
- SELFSIM-ARM 04 dell1 simulates itself WITHOUT the statement (control): iam:SimulatePrincipalPolicy on user/cloudops-dell1-agent-user -> implicitDeny (want refused) OK
- SELFSIM-ARM 05 dell2 simulates ITSELF: iam:SimulatePrincipalPolicy on user/cloudops-dell2-agent-user -> allowed (want allowed) OK
- SELFSIM-ARM 06 dell2 simulates the OTHER Dell user (dell1): iam:SimulatePrincipalPolicy on user/cloudops-dell1-agent-user -> implicitDeny (want refused) OK
- SELFSIM-ARM 07 dell2 simulates a ROLE: iam:SimulatePrincipalPolicy on role/x -> implicitDeny (want refused) OK
- SELFSIM-ARM 08 dell2 simulates itself WITHOUT the statement (control): iam:SimulatePrincipalPolicy on user/cloudops-dell2-agent-user -> implicitDeny (want refused) OK
- SELFSIM-SHAPE statements named SimulateOwnPolicyOnly=1; action iam:SimulatePrincipalPolicy; resource arn:aws:iam::313476888478:user/${aws:username}; no wildcard OK

## What this Allow can undo (for the people who sign)

Method and its limit. Each reading below is the cloud's evaluator (`iam simulate-custom-policy`) on the Dell user's effective set, for both users, with the resource's ARN. **An identity-policy simulation does not include the resource's own policy** (a bucket policy, a key policy, a function policy): a Deny or a missing Allow written in the resource's own policy is not visible here. No bucket policy, key policy, object or secret value was read from AWS, and no KMS or Secrets Manager call was made; key ids come from the saved census (`tests/vendor_secrets_census.json`) and the saved transcripts read (`infra/aws/terraform/transcripts/tests/transcripts_access.json`), bucket names from the registry (`infra/logic/registry/scopes.json`) and the repository. Nothing here is excluded; each is reported. Printed by `simulate_policy.py` as `CANUNDO-...` lines.

**(i) A key that encrypts a withheld secret.** One secret is under a customer-managed key: `schwab/sdd/session` (a custodian session, granted class, left out as blocked-by-key), key `8863d4ac-891f-4b6d-8330-2fd105ad32b5`. Simulator: `kms:PutKeyPolicy` and `kms:CreateGrant` on that key read **allowed** for both users. Consequence: a Dell could give itself `kms:Decrypt` on that key. That alone does not read the secret: `secretsmanager:GetSecretValue` on that secret reads **implicitDeny** for both users, and the only way to give a Dell the read (a secret resource policy) is excluded under (d). The other 113 listed secrets, including the 28 platform keys and 19 unplaced ones, use the account's default (AWS-managed) key, whose key policy cannot be set by anyone, so key actions give nothing there.

**(ii) `lambda:AddPermission` on the ten protected functions.** The order expected the explicit Deny that stays to win. **It does not: all ten read allowed for both users, zero explicitDeny** (`CANUNDO-ii PROTECTED-ADDPERMISSION functions=10 explicitDeny: dell1=0 dell2=0 ... allowed: dell1=10 dell2=10`). `DenyProtectedFunctions` lists ten Lambda write actions and `lambda:AddPermission` is not among them; it was held back before only by the resource-policy Deny now removed. Consequence: a Dell could add a permission that lets any principal or service invoke the portal authorizers and the auth handlers; it still cannot change their code or configuration (those stay explicitDeny). Filed as row `NFRA_CTLPLN-W14-S15` (premise differs). To make the expectation true, `lambda:AddPermission` (and `RemovePermission`) would be added to `DenyProtectedFunctions`, which this pass did not touch, or excluded in the data; neither is done here. **AMENDMENT 12 UPDATE (CTO msg 106781, route 1 ruled OUT): NOW REFUSED.** `DenyProtectedFunctions` lists the Allow's four `lambda:` actions as well; the same simulation reads `CANUNDO-ii PROTECTED-ADDPERMISSION functions=10 explicitDeny: dell1=10 dell2=10 ... allowed: dell1=0 dell2=0`, matched statement `DenyProtectedFunctions(Deny)` (section E).

**(iii) `s3:PutBucketPolicy` on the three firm-fence buckets and the Terraform state bucket.** Simulator, both users: **allowed** on `opal-data-49financial`, `opal-data-cottonwood`, `opal-data-inflection` and on `opal-313476888478-terraform-state`. Consequence: a Dell could rewrite the per-firm Deny fence that keeps one firm's data from another firm's identities, or the state bucket's policy. The Dell group's separate S3 delete limit holds on the firm buckets: `s3:DeleteBucketPolicy` reads **explicitDeny** (`DenyS3DeletesOnProductionData`) on the three firm buckets, and **allowed** on the state bucket, but a Put replaces the policy as well as a delete removes it. Whether a policy already on those buckets stops this for the Dell users is not visible to this simulation.

**(iv) The transcripts key's policy.** Key `44a2284f-1e14-4ea1-b6cb-f6121bfde35a`. `kms:PutKeyPolicy` and `kms:CreateGrant` read **allowed** for both users. The key's own policy (saved read) gives the account root the actions `kms:Create*` and `kms:Put*`, which hands those two actions to IAM, so the identity-policy Allow is what decides them: a Dell could rewrite the key policy or grant itself use. Consequence: the transcripts decrypt change of this order's amendment 3 gives a Dell `kms:Decrypt` and `kms:DescribeKey` only; with this Allow a Dell could widen itself to encrypt, re-encrypt and key administration on the key that guards the transcripts store. Also `s3:PutBucketPolicy` on `opal-data-transcripts` reads allowed.

**Further cases found.**

- **The audit trail's log bucket.** `s3:PutBucketPolicy` on `opal-cloudtrail-logs-313476888478` reads **allowed** for both users. `DenyCloudTrailWrites` stops a Dell stopping or changing the trail, but a rewritten bucket policy could stop the trail from delivering to its bucket. This is the nearest thing to the audit-trail limit this Allow touches. **AMENDMENT 12 UPDATE (route 2 ruled OUT): NOW REFUSED** for `s3:PutBucketPolicy`, `s3:DeleteBucketPolicy`, `s3:PutBucketAcl` on the bucket and `s3:PutObjectAcl`, `s3:PutObjectVersionAcl` on its objects: explicitDeny, matched `DenyAuditTrailBucketPolicy(Deny)`, both users (section E). The bucket's configuration actions (lifecycle, logging, public access block and the like) are allowed by the create policy and were never in this Allow: row `NFRA_CTLPLN-W14-S16`.
- **The agentbus queues.** `sqs:AddPermission` and `sqs:SetQueueAttributes` read **allowed** on all four boxes' queues for both users, while `sqs:ReceiveMessage` reads implicitDeny for a Dell on every queue but its own. A queue policy naming a Dell can grant it receive on another box's queue, so the "receive only from its own queue" limit can be undone. (`sqs:SetQueueAttributes` was already allowed before this pass through the create policy; the Allow adds `sqs:AddPermission`.) **AMENDMENT 12 UPDATE (route 3 ruled OUT): NOW REFUSED** -- `sqs:AddPermission`, `sqs:RemovePermission`, `sqs:SetQueueAttributes` on the four queues read explicitDeny, matched `DenyAgentbusQueuePolicy(Deny)`, both users; receive on a Dell's own queue and send on the four read exactly as before (section E).
- **Object ACLs on production data.** `s3:PutObjectAcl` and `s3:PutBucketAcl` read **allowed** on `opal-data-assets`; the delete Deny on `opal-data-*` does not cover them. Consequence: a Dell could change who can read an object or a bucket there.
- **Not undone:** IAM (every `iam:` action stays refused), CloudTrail resource policies, a secret's resource policy (excluded), the routes Deny (no overlap), the protected functions' code and configuration.

## What this does NOT do / limits

- Reads only: the live SSM documents were not compared; no Secrets Manager call; no KMS call; no bucket policy or object read; the backend was not read. What the apply would show is read from the configuration, not planned.
- The grant lets a box READ the credential. Whether a given vendor call is one Andrew allowed for a given project stays the rule seats follow. `openai-api-key` is readable now; the whitelist line that scopes it to one project is unchanged.
- The create policy still lets a Dell WRITE a secret (`PutSecretValue`): the simulation shows the same decision with and without the secrets document.
- D (dell2's SSM parameter read) was not in that pass; it is section D below (amendment 11).

## D. ONE PUBLIC SSM PARAMETER READ, BY EXACT ARN (amendment 11)

One statement in the group's create policy, so it reaches both Dell users: Sid `ReadPublicAmiParameter`, Allow, Action `ssm:GetParameter` only, Resource exactly `arn:aws:ssm:us-east-1::parameter/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64` (empty account field, no wildcard). Why: `infra/aws/terraform/investor-reporting/ycharts/instance.tf` line 40 declares `data "aws_ssm_parameter" "al2023"` with that name; Terraform's data source calls `ssm:GetParameter`. Simulation (inside `ssm_ok`): both users read the exact parameter allowed; both users read `.../al2023-ami-kernel-6.1-x86_64` and the account parameter `arn:aws:ssm:us-east-1:313476888478:parameter/anything` implicitDeny. Plan by reading: no new resource; the change to `aws_iam_policy.dell_agent_create` is the same single in-place change, now with two added statements. Other public AMI parameters read by roots (listed, NOT added): `etfs-reports/instance.tf:20`, `estate-report/instance.tf:36`, `bd-49f-auto-login/instance.tf:24`, `astn-pipeline/instance.tf:20` (all the same x86_64 name as the granted one, covered by it), and `opal-gateway/main.tf:112` (`al2023-ami-kernel-default-arm64`, NOT covered).

## E. THREE EXPLICIT DENY STATEMENTS BY RESOURCE (amendment 12; `1.0.0_SA_CTO` msg 106781, "Each as an explicit Deny by resource ARN, in plan 2")

NOTHING WAS APPLIED, NO PLAN WAS RUN, NO LISTING WAS TAKEN FROM AWS: names and ARNs come from the repository; the only AWS call was `iam simulate-custom-policy`.

**1. `DenyProtectedFunctions` (widened, in `dell_deploy_policy.json`).** Effect Deny, the ten existing Lambda write actions plus the four `lambda:` actions of the Allow's data document (`dell_respol_policy.json`, `in_allow` true): `lambda:AddLayerVersionPermission`, `lambda:AddPermission`, `lambda:RemoveLayerVersionPermission`, `lambda:RemovePermission`. Resources: the SAME twenty entries (ten function ARNs and ten `:*` qualified forms), not retyped: the statement is rendered by `tests/derive_protected_functions.py`, whose action list now appends the data document's `lambda:` actions, and its resource list comes from `protected_functions.json` (the census; `--check` prints `in_sync=True`). Widening, not a sibling statement, because a JSON document cannot reuse a resource list and the existing `protected_ok=8/8` arms read `explicitDeny` from the same statement name as before. The document is 5,073 of 6,144 characters.

**2. `DenyAuditTrailBucketPolicy` (new, in `dell_create_policy.json`).** Deny, the 14 `s3:` actions of the Allow's data (`s3:CreateAccessGrant`, `s3:DeleteAccessGrant`, `s3:DeleteAccessGrantsInstanceResourcePolicy`, `s3:DeleteAccessPointPolicy`, `s3:DeleteAccessPointPolicyForObjectLambda`, `s3:DeleteBucketPolicy`, `s3:PutAccessGrantsInstanceResourcePolicy`, `s3:PutAccessPointPolicy`, `s3:PutAccessPointPolicyForObjectLambda`, `s3:PutBucketAcl`, `s3:PutBucketPolicy`, `s3:PutMultiRegionAccessPointPolicy`, `s3:PutObjectAcl`, `s3:PutObjectVersionAcl`), on `arn:aws:s3:::opal-cloudtrail-logs-313476888478` and `arn:aws:s3:::opal-cloudtrail-logs-313476888478/*`. The bucket name: `infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf` line 58 (`s3_bucket_name = "opal-cloudtrail-logs-313476888478"`), the trail `opal-organization-trail`.

**3. `DenyAgentbusQueuePolicy` (new, in `dell_create_policy.json`).** Deny, `sqs:AddPermission`, `sqs:RemovePermission`, `sqs:SetQueueAttributes` (the Allow's three `sqs:` actions), on four exact ARNs, no wildcard: `arn:aws:sqs:us-east-1:313476888478:` + `agentbus-ajbdev-sitez-to-laptop.fifo`, `agentbus-ajbdev-laptop-to-sitez.fifo`, `agentbus-global-dell1-queue.fifo`, `agentbus-global-dell2-queue.fifo`. Names: `org/devices/DEVICES.json` lines 24, 58, 91, 118 (each device's `inbound_queue`; the register holds exactly four devices) and the Terraform that creates them: `infra/aws/terraform/nfra-agentbus-port2/sqs.tf` lines 24 and 39, `infra/aws/terraform/nfra-ctlpln-agentbus/sqs.tf` lines 15 to 25 and 30 (`agentbus-global-<box>-queue.fifo` for dell1 and dell2). The Dell group's own Allows name the dell queues with a trailing `*` (`...-queue*`); the Deny does not, so it names the four queues only. It does NOT deny `sqs:ReceiveMessage`, `SendMessage`, `DeleteMessage`, `GetQueueAttributes`, `GetQueueUrl` or `ChangeMessageVisibility` (the simulation prints `message actions denied=none`).

**Placement.** Statements 2 and 3 went to the create policy: the deploy document, now 5,073 characters, has about 1,070 left, the two statements need about 1,030 more, and the renderers for `DenyProtectedFunctions` and the pass-role statements re-append statements by a hand-formatted layout. The create policy is 5,364 of 6,144 (whitespace not counted). No new managed policy; the group holds 6 of 10 (`check_identity.py`: `group managed-policy attachments=6 quota=10`, which already counts the Allow policy's attachment).

**What the simulator reads** (both Dell users; effective set = group policies + per-user policies + the new Allow + the two routes Deny documents; the same request on the same set WITHOUT the new statements is printed beside each reading as "before AMENDMENT 12"):

- Denied: `lambda:AddPermission` and `lambda:RemovePermission` on each of the ten functions and one qualified ARN: explicitDeny, `DenyProtectedFunctions(Deny)` matched, before = allowed (44 arms). `s3:DeleteBucketPolicy`, `s3:PutBucketAcl`, `s3:PutBucketPolicy` on the bucket and `s3:PutObjectAcl`, `s3:PutObjectVersionAcl` on an object of it: explicitDeny, `DenyAuditTrailBucketPolicy(Deny)` matched, before = allowed (10 arms). The three `sqs:` actions on each of the four queues: explicitDeny, `DenyAgentbusQueuePolicy(Deny)` matched, before = allowed (24 arms). 78 of 78.
- Controls, still allowed (26 of 26): the two `lambda:` actions on a non-protected function; the five applicable `s3:` actions on `opal-data-assets` (`s3:DeleteBucketPolicy` on `opal-x-test`, because the older `DenyS3DeletesOnProductionData` denies it on every `opal-data-*` bucket); the three `sqs:` actions on `other-queue-x` and on `agentbus-x` (an `agentbus-` name that is not one of the four).
- Receive and send unchanged (48 of 48; each reads the same before and after): `sqs:SendMessage` allowed on all four queues for both users; `sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:ChangeMessageVisibility` allowed on a Dell's OWN queue and implicitDeny on the other three; `sqs:GetQueueAttributes` and `sqs:GetQueueUrl` allowed on the four. Example: dell2 `sqs:ReceiveMessage` on `agentbus-global-dell2-queue.fifo` before=allowed after=allowed; dell2 `sqs:SendMessage` on `agentbus-global-dell1-queue.fifo` before=allowed after=allowed; dell2 `sqs:ReceiveMessage` on `agentbus-global-dell1-queue.fifo` before=implicitDeny after=implicitDeny.
- Shape check (1 of 1): the statements' action sets equal the data document's per service; the ten functions and the four queues equal the saved lists.
- `undo_denied=153/153` was these four groups before AMENDMENT 13 (it is 181/181 now, section E.AMENDMENT 13 below). The arms before are unchanged: `protected_ok=8/8`, `freed_allowed=70/70` (no representative resource of the freed block is a denied one), `ssm_ok=15/15`, `routes_ok=5/5`.

**What the Deny cannot do.** Eleven of the 21 actions listed take another resource type: `lambda:AddLayerVersionPermission` and `lambda:RemoveLayerVersionPermission` (a layer version, not a function) and nine `s3:` access-point, access-grant and multi-region access-point actions (not a bucket). They are in the statements as ordered; on a function or bucket ARN the evaluator reads them implicitDeny with no statement matched, except two access-grant instance-policy actions that it does match (printed as `UNDO-INERT`, not counted). Row `NFRA_CTLPLN-W14-S16`.

**What plan 2 would show: REPLACED by the three steps below (AMENDMENT 13). The older single list (the Allow, two policies in place) is withdrawn: the Allow now sits behind a switch.**

### E.AMENDMENT 13 -- seven more settings in the audit-trail Deny, and the THREE STEPS (`1.0.0_SA_CTO` msg 106838 and 106820)

NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND. The only AWS call was `iam simulate-custom-policy`.

**The seven.** `DenyAuditTrailBucketPolicy` gains the write action of each setting the create policy's Allow (`CreateUpdateTagS3OnOpalBuckets`) already lets a Dell change on the audit-trail bucket, same two resources, no reads: lifecycle `s3:PutLifecycleConfiguration`; logging `s3:PutBucketLogging`; notification `s3:PutBucketNotification`; encryption `s3:PutEncryptionConfiguration`; versioning `s3:PutBucketVersioning`; ownership controls `s3:PutBucketOwnershipControls`; public-access block `s3:PutBucketPublicAccessBlock`. S3 has no separate Delete action for any of the seven (the delete calls are authorised by the same Put action), so there is no `s3:Delete...` to add. Simulator on the audit bucket BEFORE the change: all seven read allowed, both users. AFTER: all seven read explicitDeny, `DenyAuditTrailBucketPolicy(Deny)` matched (14 arms). On `opal-data-assets` the seven read the same with and without the new statement: six allowed (`CreateUpdateTagS3OnOpalBuckets`), and `s3:PutLifecycleConfiguration` explicitDeny from the older `DenyS3DeletesOnProductionData` (14 control arms). The statement now holds 21 actions; the create policy is 5,565 of 6,144 characters (whitespace not counted; 6,844 with whitespace). `undo_denied=181/181` (was 153/153).

**The switch.** `variable "apply_respol_allow"` (bool, default false) in `iam.tf`. `aws_iam_policy.dell_agent_respol_allow` and `aws_iam_group_policy_attachment.dell_agent_respol_allow` have `count = var.apply_respol_allow && module.routes_policy.respol_policy_count == 1 ? 1 : 0` (the existing condition, the module's count output, which is `respol_json == null ? 0 : 1`). With the default, a plan of the root holds neither. Nothing else reads the variable. `terraform validate` passes with the default and with `TF_VAR_apply_respol_allow=true` (validate checks types and references, it does not evaluate a count; the true branch is read, not planned).

**STEP A -- the Denies (apply first; a targeted apply of the two policies changed in place).** `-target=aws_iam_policy.dell_agent_create -target=aws_iam_policy.dell_agent_deploy`. Would show, by reading:
- `aws_iam_policy.dell_agent_create`: updated in place; the document gains `SimulateOwnPolicyOnly`, `ReadPublicAmiParameter`, `DenyAuditTrailBucketPolicy` (21 actions), `DenyAgentbusQueuePolicy`; 5,565 of 6,144.
- `aws_iam_policy.dell_agent_deploy`: updated in place; `DenyProtectedFunctions` gains four actions (`lambda:AddLayerVersionPermission`, `lambda:AddPermission`, `lambda:RemoveLayerVersionPermission`, `lambda:RemovePermission`); 5,073 of 6,144.
- Plan: 0 to add, 2 to change, 0 to destroy.

**STEP B -- plan 1's remaining four resources (after A is applied; the create policy is already done).** `-target` the four. Would show:
- `aws_iam_policy.dell_agent_vendor_secrets[0]` created (66 exact secret ARNs, 5,968 characters) and `aws_iam_group_policy_attachment.dell_agent_vendor_secrets[0]` created.
- `aws_iam_policy.dell_agent_respol` (the old Deny policy) destroyed and `aws_iam_group_policy_attachment.dell_agent_respol` destroyed.
- Plan: 2 to add, 0 to change, 2 to destroy. The Denies of step A are already in force, so the three ruled routes and the audit-trail bucket's settings are refused at the moment the old Deny goes.

**STEP C -- the Allow (after A and B), `-var apply_respol_allow=true` on plan AND on apply.** Would show:
- `aws_iam_policy.dell_agent_respol_allow[0]` created (70 actions, 2,195 characters) and `aws_iam_group_policy_attachment.dell_agent_respol_allow[0]` created.
- Plan: 2 to add, 0 to change, 0 to destroy; the group then holds 6 managed policies of 10. Without the variable the same root shows no changes once A and B are applied.

**What this Allow can undo, after amendment 12.** Refused now: the three ruled routes (above). Stay as reported, accepted: a firm fence bucket's policy, the state bucket's policy, a KMS key policy on the one blocked-by-key secret's key, the transcripts key's policy (rows (i), (iii), (iv)); and the object-ACL finding on production data buckets (`s3:PutObjectAcl`, `s3:PutBucketAcl` on `opal-data-assets` still read allowed, the control arms above). New, not caused by the Allow: the audit-trail bucket's configuration actions, row `NFRA_CTLPLN-W14-S16`.

### E.AMENDMENT 14 -- step C is the last step; the default is now true (`1.0.0_SA_CTO` msg 106915, condition 6)

Step C is the last step. The Allow was applied on 2026-10-08 under order NFRA_CTLPLN.TO-APPLY-13, so `variable "apply_respol_allow"` now defaults to true: a plain plan or apply of this root, with no variable, carries the Allow and its attachment and proposes nothing about them. (With the old default of false, any such plan would have proposed to destroy both.) The variable remains as the one-line way to take the Allow off: `-var apply_respol_allow=false` on plan and apply plans its removal, and that is a never-widen act needing its own pair. A static check in `tests/check_identity.py` (`allow_default_true=`) reads the default from the `.tf` text and fails, naming this amendment, if it is ever false again. NOTHING WAS APPLIED AND NO PLAN WAS RUN AGAINST THE BACKEND.
