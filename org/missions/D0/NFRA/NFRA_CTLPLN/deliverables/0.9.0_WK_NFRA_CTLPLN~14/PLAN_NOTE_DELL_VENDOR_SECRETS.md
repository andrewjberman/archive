# PLAN NOTE -- three Dell limits lifted in ONE plan: secrets, the resource-policy Deny (now the resource-policy ALLOW), self-simulate (NFRA_CTLPLN.TO-CT-a-1, amendments 9 and 10)

**LATEST: section G (amendment 16, STEP E) widens the secrets grant to the 28 PLATFORM-KEY secrets and takes three Deny statements off; where sections A and B below say the PLATFORM-KEY class is NOT granted, section G governs.**

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

### PLATFORM-KEY -- (28) NOT granted under amendments 9 to 14; GRANTED by amendment 16 (section G); what holding each would let a box do

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

## F. STEP D -- the routes Deny removed (item 5) (amendment 15, re-seated by amendment 18; `1.0.0_SA_CTO` msg 106945 cell (1), msg 106987)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SECRET VALUE WAS READ. The AWS calls of this pass were `iam:SimulateCustomPolicy` and `iam:SimulatePrincipalPolicy` (read-only) and, inside the criterion `CTa1-AC5`'s own script, the read of the transcripts key policy it has always made. Authority: Andrew-direct 2026-10-08 ~13:2xZ, "1.) lIFT ITEM 5." (record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_132xZ_TEN_ANSWERS_LIFT_ITEMS_5_AND_4_WIDEN_BOTH_GRANTS_DELL2_RETRIES_DELL1_INSTALLS.md`, row 1: item 5 is "the Deny on 'writing or sending a command document, task definition or downloaded artifact prefix that runs as a privileged role'"); `1.0.0_SA_CTO` msg 106945 cell (1): "remove the Deny in cloudops-dell-agent-routes-host-policy for both Dells."

**This section assumes STEP E (`TO-APPLY-14`, section G) is APPLIED.** It was, on the live account, when read at 2026-10-08T18:22:24Z: `iam:SimulatePrincipalPolicy` on both Dell users read `secretsmanager:GetSecretValue` on `opal/mcp/graph-read-token` allowed by `cloudops-dell-agent-platform-secrets-policy` and `cloudtrail:PutResourcePolicy` allowed by `cloudops-dell-agent-respol-allow-policy`. If a plan of this root were run BEFORE step E, it would show section G's list as well (2 to add, 3 to change) and this step's two destroys; the applier must run step E first, as ordered.

### What exists today (item 1, read from `routes.tf`, `modules/routes_policy/` and the policy files)

`routes.tf` creates TWO managed policies and TWO group attachments, both on `cloudops-dell-agents-group` (so both users). The module builds each document from `tests/reached_roles_census.json` (175 roles read, 175 total; taken 2026-10-07T11:05:41Z); no file holds a name.

| policy (name from the builder) | address | attached by | statements |
|---|---|---|---|
| `cloudops-dell-agent-routes-host-policy` (the CTO's name; item 5) | `aws_iam_policy.dell_agent_routes_host[0]` | `aws_iam_group_policy_attachment.dell_agent_routes_host[0]` (group) | `DenyRoutesToPrivilegedRolesDocuments`, `DenyRoutesToPrivilegedRolesPrefixes` (1,445 characters) |
| `cloudops-dell-agent-routes-fn-policy` (the "second document") | `aws_iam_policy.dell_agent_routes_fn[0]` | `aws_iam_group_policy_attachment.dell_agent_routes_fn[0]` (group) | `DenyRoutesToPrivilegedRolesFunctions` (5,521 characters) |

In plain words, the hosts policy (REMOVED by this step) refused, for both Dell users:
- `DenyRoutesToPrivilegedRolesDocuments`: `ssm:UpdateDocument`, `ssm:UpdateDocumentDefaultVersion`, `ssm:CreateDocument`, `ssm:DeleteDocument`, `ssm:SendCommand` on twelve command documents, by exact ARN: `advi-49f-chain-dispatch`, `opal-bd-49f-session-fetch`, `opal-cot-bd-session-fetch`, `opal-cot-bronze-run`, `opal-cot-gold-run`, `opal-cot-silver-run`, `opal-inf-export-run`, `opal-inf-jwt-fetch`, `opal-inf-jwt-setup`, `opal-inf-test-login-stage1`, `-stage2`, `-stage3`. These are the documents that run on hosts whose role can reach IAM, the audit trail or production-data deletes (the census says YES-DELETE for `cot-exporter-ec2-role`, `inf-gold-layer-ec2-role`, `bd-exporter-ec2-role` and the smartx exporter role).
- `DenyRoutesToPrivilegedRolesPrefixes`: `s3:PutObject` on five code locations those hosts download and run: Cottonwood `opal-data-cot/code/bronze/cot_bronze_ingest.py`, `opal-data-cot/code/gold/*`, `opal-data-cot/code/silver/cot_silver_merge.py`; Inflection `opal-data-inf/code/exporter/inf-jwt-fetch.sh`, `opal-data-inf/code/exporter/stepwise/*`.
- Task definitions: the module has a task statement, but the census holds no task-definition route to a YES role, so the built document has NO task statement. A Dell is not refused `ecs:RegisterTaskDefinition`, `ecs:RunTask` or `ecs:UpdateService` today (the simulation reads all three allowed before and after).
- The Black Diamond code prefix (`opal-data-bd/code/{gold,silver,bronze}/`) is named by NEITHER routes document.

The functions policy (`routes-fn`, NOT removed) refuses `lambda:UpdateFunctionCode`, `UpdateFunctionConfiguration`, `PublishVersion`, `CreateAlias`, `UpdateAlias`, `DeleteFunction`, `DeleteAlias`, `PutFunctionConcurrency`, `UpdateFunctionUrlConfig`, `CreateFunctionUrlConfig` on the functions (66 ARNs, base and qualified) that run as a role able to write IAM (one role, `lambda-execution-role`) or delete production data. Why it stays: item 5 as put to Andrew is a Deny on "a command document, task definition or downloaded artifact prefix"; the functions policy's subject is updating a function, and its description in the record is different. If the issuer reads "the routes Deny" as both policies, removing the second is two more destroys (`aws_iam_group_policy_attachment.dell_agent_routes_fn[0]`, `aws_iam_policy.dell_agent_routes_fn[0]`) and the same kind of edit; I did not do it unasked (row `NFRA_CTLPLN-W14-S24`).

### The stop-condition read: which statement refused dell1's `s3:PutObject` on the cot and bd code prefixes

Read with `iam:SimulatePrincipalPolicy` on the LIVE users (2026-10-08 ~18:1xZ) and `iam:SimulateCustomPolicy` on the repository's documents:
- **Cottonwood code prefix: refused by the routes-host policy.** Live, both users: `s3:PutObject` on `opal-data-cot/code/gold/x.py`, `.../code/bronze/cot_bronze_ingest.py`, `.../code/silver/cot_silver_merge.py` read explicitDeny, the matched statement `cloudops-dell-agent-routes-host-policy` (`DenyRoutesToPrivilegedRolesPrefixes`). `.../code/silver/x.py` (a name the document does not list) reads allowed by `S3ObjectsOnOpalBuckets`.
- **Black Diamond code prefix: NOT refused by any identity statement, and so not by the routes policy.** Live, both users: `s3:PutObject` on `opal-data-bd/code/gold/x.py`, `code/silver/x.py`, `code/bronze/x.py`, `code/bronze/cot_bronze_ingest.py`, `code/bronze/templates/fees.json`, `code/gold/gold_dispatch.sh`, `code/gold/lib/advisor_nna_attribution.py` and `code/canonical-schwab-runner/run-canonical.sh` all read ALLOWED, matched statement `cloudops-dell-agent-deploy-policy` (`S3ObjectsOnOpalBuckets`). No Deny in `dell_deploy_policy.json`, `dell_create_policy.json`, the bus policies, `dell2_ssm_policy.json` or either routes document names a Black Diamond key. If dell1 measured a refusal there, it is NOT from the routes policy and NOT from an identity policy of this root: the candidate planes are the bucket's own resource policy, a service control policy, or a key policy; none of those is readable under this pass's bounds (the shared-infra root declares a fence only on `opal-data-49financial`, `opal-data-cottonwood` and `opal-data-inflection`, not on `opal-data-bd`). This step removes the routes policy and delivers the Cottonwood and Inflection prefixes; it does not and cannot change a Black Diamond refusal that is not an identity-policy refusal. Row `NFRA_CTLPLN-W14-S25`.

### The expected plan, by reading, resource by address (so the applier can TARGET it)

| resource address | action | what changes |
|---|---|---|
| `aws_iam_group_policy_attachment.dell_agent_routes_host[0]` | destroyed | the hosts Deny detached from `cloudops-dell-agents-group` |
| `aws_iam_policy.dell_agent_routes_host[0]` (`cloudops-dell-agent-routes-host-policy`) | destroyed | the hosts Deny policy deleted |

Expected: **0 to add, 0 to change, 2 to destroy.** The two addresses are the whole `-target` list (`terraform apply -target='aws_iam_group_policy_attachment.dell_agent_routes_host[0]' -target='aws_iam_policy.dell_agent_routes_host[0]'`). The group then holds **6 managed policies of 10** (`check_identity.py` prints `group managed-policy attachments=6 quota=10`; 7 before). The module still renders `hosts_policy_json` (nothing builds it into a policy); the secrets documents and the resource-policy Allow are BYTE-IDENTICAL before and after, read from the module's rendered JSON at HEAD and in this tree (sha256 prefixes: part one `575dd5b49e594e62`, part two `6e7ab7af76ec3980`, Allow `b683cfcf80767bc1`, functions Deny `69a302a285f7796f`, hosts document `c2ad39d2ad521046`; the whole module output, 25 keys, equal). `byte_identity_routes_step_d.py` in this folder reproduces it. The module, the census files and the Allow's data were not edited, which is why a plan shows nothing else.

### What each Dell can NEWLY do after this step, in plain words (from the simulation, both users)

`ROUTES-FREED-SUMMARY arms=138 allowed=90 (refused_today_by_hosts=82 already_allowed=8) still_refused=48`, per user 69 arms.
- **Write the code the Cottonwood and Inflection hosts download and run** (`s3:PutObject` on the five prefixes above: 5 arms per user, all FREED). Those hosts run as roles the census marks YES-DELETE: a Dell can now change the program that a role able to delete production data runs. This is what item 5 held shut.
- **Create, rewrite and re-point the twelve command documents** (`ssm:CreateDocument`, `ssm:UpdateDocument`, `ssm:UpdateDocumentDefaultVersion`: 36 arms per user, all FREED). A document's text is what a host executes as its own role.
- **Register task definitions** (`ecs:RegisterTaskDefinition`) and run or update services: already allowed before this step; nothing changes.
- **Black Diamond code prefix: already allowed**, nothing changes (see above).

### What STILL refuses a deploy route after this step, and why

- **Sending a command document (`ssm:SendCommand`) and deleting one (`ssm:DeleteDocument`) on the twelve documents stay refused for both users: 24 arms per user, implicitDeny, no Allow statement matches.** Not a Deny: no Allow in any of the group's six policies grants either action. dell2's own grant (`SendResidentDocumentsToResidentHost`) names two other documents and one instance; its `DenyShellDocuments` refuses the AWS shell documents. Getting SendCommand on these twelve would take another Allow.
- **The functions Deny (`routes-fn`)** stays: `lambda:UpdateFunctionCode` and the nine like it on the functions of a YES role (66 ARNs, base and qualified) (control arm: a function of a role that cannot reach IAM, audit or deletes reads allowed, before and after).
- **In other files of this root, untouched:** `DenyEveryIamWrite` (all `iam:Create*`, `Delete*`, `Put*`, `Attach*`, `Detach*`, `Update*`, `Add*`, `Remove*`, `Tag*`, `Untag*`, `Set*`, `Upload*`, `Enable*`, `Deactivate*` and `iam:ChangePassword`), `DenyPassRoleExceptNamed` (`iam:PassRole` except the named roles), `DenyProtectedFunctions` (ten deploy actions on the twenty protected-function resources), `DenyCloudTrailWrites` (the Stop and Update wildcards and the explicit Delete and Put actions), `DenyAuditTrailBucketWrites` (seven settings on the audit-trail bucket), `DenyS3DeletesOnProductionData` (`s3:DeleteBucket*`, `s3:DeleteObject*`, `s3:PutLifecycleConfiguration` on `opal-data-*`), `DenyTableAndDatabaseDeletes`, `DenyApiKeyReads`, and dell2's `DenyShellDocuments`.
- **Outside the identity policies, not read here:** bucket policies (including the firm fences), service control policies and key policies.

### Simulation, this step

`POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 routes_freed=90/138 routes_still_refused=48 vendor_ok=245/245 all_ok=True`. Every field before `routes_freed` reads exactly as at the base (`e80238bdab`); `routes_ok=5/5` is replaced by the two new fields. The 138 arms are the hosts document's own routes, 69 per user: 5 code prefixes + the Black Diamond arm, 5 document actions on 12 documents, 3 task arms. Each arm prints its decision after the removal AND the decision with the hosts document present (today), which must be an explicitDeny by a hosts statement for every document and prefix arm (130 of 130 read so: 82 are freed and 48 stay refused; the 8 other arms, allowed in both states, are the Black Diamond and task arms). Two further lines per user: a function of a YES-IAM role still reads explicitDeny by `DenyRoutesToPrivilegedRolesFunctions` (kept), and a function of a NO role reads allowed (control).

## G. STEP E -- the two grants widened (item 3, cell 2) (amendment 16; `1.0.0_SA_CTO` msgs 106945, 106987)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SECRET VALUE WAS READ (the secrets census was re-derived from the saved listing of 2026-10-07T21:00:45Z with `derive_vendor_secrets.py --reclass`: no AWS call at all). The only AWS call of this pass was `iam simulate-custom-policy`. Authority: Andrew-direct 2026-10-08 ~13:2xZ, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_132xZ_TEN_ANSWERS_LIFT_ITEMS_5_AND_4_WIDEN_BOTH_GRANTS_DELL2_RETRIES_DELL1_INSTALLS.md` row 3, "WIDEN THE TWO GRANTS, YES" to "the 28 platform keys, the audit trail and its bucket, the portal's protected functions and the four cross-box queues"; not widened: the 19 unplaced secrets and the one custodian session behind its own key. Sections A, B and the "NOT granted" headings above describe the state before this step: where they say the PLATFORM-KEY class is NOT granted, this section governs.

**The state this reads against.** Steps A, B and C of section E.AMENDMENT 13 are applied (09:19:39Z, 11:33:48Z, and step C under `NFRA_CTLPLN.TO-APPLY-13`), so the root's last applied form is: create policy with `DenyAuditTrailBucketPolicy` (21 actions) and `DenyAgentbusQueuePolicy`; deploy policy with `DenyProtectedFunctions` at 14 actions and `DenyCloudTrailWrites` at four wildcards; secrets policy part one with 66 ARNs; the Allow with 70 actions. I did not read the backend: if that is not the live state, the plan will show more than the list below.

### The expected plan, by reading, resource by address (so the applier can TARGET it)

| resource address | action | what changes |
|---|---|---|
| `aws_iam_policy.dell_agent_deploy` | updated in place | `DenyCloudTrailWrites` no longer names `cloudtrail:PutResourcePolicy` or `cloudtrail:DeleteResourcePolicy` (the four wildcards `Stop*`, `Delete*`, `Update*`, `Put*` become `Stop*`, `Update*` and seven explicit names); `DenyProtectedFunctions` loses four actions. 5,126 of 6,144 characters (whitespace not counted; 5,073 before). |
| `aws_iam_policy.dell_agent_create` | updated in place | `DenyAuditTrailBucketPolicy` (21 actions) becomes `DenyAuditTrailBucketWrites` (7 actions); `DenyAgentbusQueuePolicy` removed. 4,717 of 6,144 (5,565 before). |
| `aws_iam_policy.dell_agent_respol_allow[0]` | updated in place | two actions added to the Allow, 70 to 72: `cloudtrail:DeleteResourcePolicy`, `cloudtrail:PutResourcePolicy`. 2,260 of 6,144 (2,195 before). |
| `aws_iam_policy.dell_agent_platform_secrets[0]` (`cloudops-dell-agent-platform-secrets-policy`) | created | 28 exact secret ARNs, `secretsmanager:GetSecretValue` only. 2,707 of 6,144. |
| `aws_iam_group_policy_attachment.dell_agent_platform_secrets[0]` | created | to `cloudops-dell-agents-group`. |

Expected: **2 to add, 3 to change, 0 to destroy.** The group then holds **7 managed policies of 10** (`check_identity.py` prints `group managed-policy attachments=7 quota=10`). The five addresses are the whole `-target` list. Difference from the issuer's expectation, stated plainly: the issuer expected the existing secrets policy to change in place. It does not, by this split: `aws_iam_policy.dell_agent_vendor_secrets[0]` keeps its name, address, description and its 66 ARNs, and its document is byte-for-byte the one already applied (5,968 characters), so a plan shows no change for it. The platform keys are the class this amendment adds, so they are the new part; changing the existing policy's description would have forced a destroy and re-create (a description change is a replacement on an IAM policy), which the order forbids. Nothing else in the root changes; `routes.tf` and the routes Deny are untouched.

**The split rule, stated.** The document would pass 6,144 characters with the 28 added (5,968 + 2,707 = 8,675). The order names "one managed policy per granted class" as the rule `iam.tf` already names; applied literally that is THREE policies (vendor 35, client session 31, platform key 28) and 8 of 10, not the 7 the order expects. I split by the class set each part was built for: part one = VENDOR-CREDENTIAL and CLIENT-SESSION (the classes of amendments 5 to 14, document unchanged), part two = PLATFORM-KEY (the class amendment 16 adds). Stable: a future class is a new part, and a part is never re-cut.

### SECRETS -- 94 granted (was 66)

Census, re-derived from the saved listing: 114 secrets; VENDOR-CREDENTIAL 35, CLIENT-SESSION 32, PLATFORM-KEY 28, OTHER 19. GRANTED 94 = 35 + 31 + 28 (all 28 platform keys are under the account's default key); BLOCKED-BY-KEY 1 (`schwab/sdd/session`, a client session under its own key); OTHER 19 not granted. The line: `VENDOR-SECRETS secrets=114 ... granted=94 ok=True blocked_by_key=1 platform_key=28 other=19`. `opal/mcp/graph-read-token` is GRANTED (part two). What each Dell can newly do: read, with `secretsmanager:GetSecretValue`, each of the 28 below. What holding each lets a box do is the sentence under "PLATFORM-KEY" in section A; the headline ones: `opal/auth/jwt-private-key`, `opalinvest/jwt-secret` and `opal/mcp/opal-gateway-jwt` let a box sign login or gateway tokens as any user, administrators included; `opalinvest/admin-seed` lets it create or sign in as the portal's administrator; `opal/auth/irpt-render-jwt-private-key` lets it mint render tokens the edge accepts; `schwab/ec2-credentials` is a Windows Administrator login on the Schwab box.

The 28, by name: `blackdiamond/49f/otp-gateway-token`, `blackdiamond/cot/otp-gateway-token`, `gateway/global/taxsma-workbook-token`, `gateway/mail/bearer`, `gateway/principals/rosters`, `gateway/teams/bearer`, `gateway/transcripts/bearer`, `inf/otp-relay/token`, `irpt/svc-irpt-analysis/password`, `opal/auth/irpt-render-jwt-private-key`, `opal/auth/jwt-private-key`, `opal/auth/origin-verify`, `opal/mcp/graph-read-token`, `opal/mcp/ms-ingest-token`, `opal/mcp/opal-gateway-blackdiamond-reader-external-id`, `opal/mcp/opal-gateway-fernet`, `opal/mcp/opal-gateway-jwt`, `opal/mcp/opal-gateway-schwab-account-ref-key`, `opal/mcp/opal-gateway-schwab-reader-external-ids`, `opal/mcp/opalbloomberg-login`, `opal/portal/svc-data-refresh`, `opal/pseudonym/49financial`, `opal/pseudonym/opal-capital`, `opal/ticketing/svc-analyst-intake`, `opalinvest/admin-seed`, `opalinvest/jwt-secret`, `schwab/anonymization-key`, `schwab/ec2-credentials`.

Two cautions in the classes. (1) The class table's "doubt resolves to PLATFORM-KEY" rule was the cautious choice while the class was withheld; now it grants: `gateway/principals/rosters` and `opal/auth/origin-verify` are in the 28 by doubt (row `NFRA_CTLPLN-W14-S20`). (2) Simulation: `opal/mcp/graph-read-token`, `opal/auth/jwt-private-key` and `opalinvest/admin-seed` read allowed for both users, and without the two secrets documents implicitDeny; `twilio/recovery-code` (OTHER) and `schwab/sdd/session` read refused (named arms, counted in `vendor_ok`).

### THE AUDIT TRAIL, THE BUCKET, THE PROTECTED FUNCTIONS AND THE QUEUES -- where every action went

CloudTrail (`dell_deploy_policy.json`, `DenyCloudTrailWrites`). The 14 actions of the four prefixes (from the installed botocore 1.43.0 cloudtrail service model; the AWS service reference was not fetched): Stop: `StopEventDataStoreIngestion`, `StopImport`, `StopLogging`; Delete: `DeleteChannel`, `DeleteDashboard`, `DeleteEventDataStore`, `DeleteResourcePolicy`, `DeleteTrail`; Update: `UpdateChannel`, `UpdateDashboard`, `UpdateEventDataStore`, `UpdateTrail`; Put: `PutEventConfiguration`, `PutEventSelectors`, `PutInsightSelectors`, `PutResourcePolicy` (16 in all; 2 freed, 14 stay denied). Written: `cloudtrail:Stop*`, `cloudtrail:Update*` (wildcards kept, no member freed) and, explicitly, `DeleteChannel`, `DeleteDashboard`, `DeleteEventDataStore`, `DeleteTrail`, `PutEventConfiguration`, `PutEventSelectors`, `PutInsightSelectors`. Freed: `cloudtrail:DeleteResourcePolicy`, `cloudtrail:PutResourcePolicy`. Cost of the explicit form: a future CloudTrail action beginning `Put` or `Delete` that AWS adds is no longer denied by a wildcard (row `NFRA_CTLPLN-W14-S21`).

Audit-trail bucket (`dell_create_policy.json`). `DenyAuditTrailBucketPolicy` (21 actions) is split. LEAVE the Deny (14, all of AMENDMENT 12's, the ones present in the Allow's data): `s3:CreateAccessGrant`, `s3:DeleteAccessGrant`, `s3:DeleteAccessGrantsInstanceResourcePolicy`, `s3:DeleteAccessPointPolicy`, `s3:DeleteAccessPointPolicyForObjectLambda`, `s3:DeleteBucketPolicy`, `s3:PutAccessGrantsInstanceResourcePolicy`, `s3:PutAccessPointPolicy`, `s3:PutAccessPointPolicyForObjectLambda`, `s3:PutBucketAcl`, `s3:PutBucketPolicy`, `s3:PutMultiRegionAccessPointPolicy`, `s3:PutObjectAcl`, `s3:PutObjectVersionAcl` (all 14 are in the Allow's data and now allowed on `*`; 11 of them take another resource type, so on the bucket ARN the evaluator reads them implicitDeny, printed as `UNDO-INERT`). STAY, in `DenyAuditTrailBucketWrites`, same two resources (the bucket and `/*`): `s3:PutBucketLogging`, `s3:PutBucketNotification`, `s3:PutBucketOwnershipControls`, `s3:PutBucketPublicAccessBlock`, `s3:PutBucketVersioning`, `s3:PutEncryptionConfiguration`, `s3:PutLifecycleConfiguration` (lifecycle, logging, notification, encryption, versioning, ownership controls, public-access block).

Protected functions (`dell_deploy_policy.json`, `DenyProtectedFunctions`). Removed, and only these: `lambda:AddLayerVersionPermission`, `lambda:AddPermission`, `lambda:RemoveLayerVersionPermission`, `lambda:RemovePermission`, found by `git log -p` as added by commit `c777e72cbd` (AMENDMENT 12). The statement is again the ten deploy actions (`UpdateFunctionCode`, `UpdateFunctionConfiguration`, `PublishVersion`, `CreateAlias`, `UpdateAlias`, `DeleteFunction`, `DeleteAlias`, `PutFunctionConcurrency`, `UpdateFunctionUrlConfig`, `CreateFunctionUrlConfig`) on the same twenty resources; `tests/derive_protected_functions.py` renders it again and prints `in_sync=True`.

Queues (`dell_create_policy.json`). `DenyAgentbusQueuePolicy` is removed (`sqs:AddPermission`, `sqs:RemovePermission`, `sqs:SetQueueAttributes`). The per-user receive policies are untouched.

### What each Dell can NEWLY do after this step, in plain words

- **Read the 28 platform keys by name** (above).
- **Change the audit trail's resource policy** (`cloudtrail:PutResourcePolicy`, `cloudtrail:DeleteResourcePolicy`), on a trail's channel, event data store or dashboard.
- **Change the audit-trail bucket's policy and ACLs** (`s3:PutBucketPolicy`, `s3:DeleteBucketPolicy`, `s3:PutBucketAcl` on `opal-cloudtrail-logs-313476888478`; `s3:PutObjectAcl`, `s3:PutObjectVersionAcl` on its objects). A bucket policy can let any principal read or, with the bucket's other controls, remove audit logs; the seven settings below stay refused.
- **Change who may invoke the ten protected functions** (`lambda:AddPermission`, `lambda:RemovePermission` on the authorizers, the edge auth validator and the user and key handlers): a Dell can add a permission that lets another principal call a function that decides who may reach a portal surface. It still cannot change their code or configuration.
- **Change the four agentbus queues' policies and attributes** (`sqs:AddPermission`, `sqs:RemovePermission`, `sqs:SetQueueAttributes`): a Dell can add a permission that lets itself or another principal receive from another box's queue, which is how the boxes are kept apart today. Its own receive and send actions are unchanged (48 of 48 arms read as before).
- A Dell changing a resource policy does so under its own box's never-widen pair.

### What STILL refuses after this step

The seven audit-bucket settings (`DenyAuditTrailBucketWrites`, explicitDeny for both users); every other CloudTrail Stop, Update, Delete and Put action, 14 in all (`DenyCloudTrailWrites`); the ten deploy actions on the twenty protected-function resources (`DenyProtectedFunctions`); every IAM write (`DenyEveryIamWrite`, including `iam:UpdateAssumeRolePolicy`) and `iam:PassRole` except the named roles (`DenyPassRoleExceptNamed`); the API-key reads; deletes of production data buckets and objects and of tables and databases; the routes Deny (untouched); the 19 OTHER secrets and `schwab/sdd/session` (no Allow covers them); `secretsmanager:PutResourcePolicy` and `secretsmanager:DeleteResourcePolicy` (excluded from the Allow, implicitDeny: a resource policy on a secret naming a Dell would let it read the 20 secrets this step still withholds); `kms:` key policies stay as reported (section "What this Allow can undo"). The simulation reads these as `undo_still_denied=443` (all explicitDeny with the statement named) beside `undo_freed=167/167`.

### Simulation, this step

`POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 routes_ok=5/5 vendor_ok=245/245 all_ok=True`. `undo_freed` (167) = 118 freed arms (the two CloudTrail actions, the two Lambda permission actions on 20 function ARNs, the three bucket and two object ACL actions, the three queue actions on four queues, each for both users) + 48 receive and send arms + 1 shape check; the 11 actions that take another resource type (2 Lambda layer-version actions and 9 S3 access-point, access-grant and multi-region actions, printed as `UNDO-INERT`) are not counted. `undo_still_denied` (443) = 14 seven-bucket-write arms + 28 CloudTrail arms + 400 protected-function arms + 1 shape check.


## H. CELL D2 -- the Dells may SEND the command documents, and dell2's one time-boxed shell window (amendment 19; `1.0.0_SA_CTO` msgs 107113, 107120)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SSM COMMAND WAS SENT, NO SECRET VALUE WAS READ. The only AWS calls were `iam:SimulateCustomPolicy` and, inside the existing selfsim arms, `iam:SimulatePrincipalPolicy` (read-only). Built on the trunk that carries step D (the routes-host Deny removed) and step E. The live documents were not compared to the repository text.

### What the grant names (item 1, printed by `tests/derive_ssm_documents.py --check`, `SEND-GRANT-1a/1b/1c`)

- **The 12 documents** (the module's document list, read from the census, each declared by an `aws_ssm_document` in the repository): `advi-49f-chain-dispatch`, `opal-bd-49f-session-fetch`, `opal-cot-bd-session-fetch`, `opal-cot-bronze-run`, `opal-cot-gold-run`, `opal-cot-silver-run`, `opal-inf-export-run`, `opal-inf-jwt-fetch`, `opal-inf-jwt-setup`, `opal-inf-test-login-stage1`, `opal-inf-test-login-stage2`, `opal-inf-test-login-stage3`.
- **The 6 hosts** (host routes of the YES roles with at least one document; 6 of the 17 YES-role hosts; all 17 read YES-DELETE and all are `stopped`): `i-0090b823a4a0997e3` bd-gold-qa-runner, `i-00c7568bc510f7423` bd-transactions, `i-01003b035d2988dfb` bd-gold-layer-runner, `i-0800437d1dbb0b5cc` bd-allocations (role `bd-exporter-ec2-role`); `i-0643a5bee8a8feabf` cot-exporter (`cot-exporter-ec2-role`); `i-0ed5afded2ebd4ed4` inf-gold-layer-runner (`inf-gold-layer-ec2-role`). The other 11 (8 historical-prices-fetcher, bd-fees, bd-assets, smartx-exporter) have no document route and are not named (row `NFRA_CTLPLN-W14-S30`).
- **The F1 host is `i-0167fd745ad906a66`** (census name `irpt-ycharts-runner`, running, role `irpt-ycharts-runner-role`, verdict NO, not one of the 6). Confirmed in the repository: `org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP.md:36` (the runner runs on the resident host), `.../round6/NEVER_WIDEN_PACKET_BRANCH_B_ANDREWS_PRINCIPAL.md:10` (the resident package installs there; F1 follows its V1), `infra/aws/terraform/investor-reporting/ycharts/resident.tf:2`, `.../F1_RUN_CARD_20261007.md:48` (the issuer reads the resident host's journal).

### The expected plan with the DEFAULT (`open_dell2_f1_shell_window` false), by address

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell_agent_ssm_send[0]` (`cloudops-dell-agent-ssm-send-policy`) | created | statement `SendCommandDocumentsAndShellToPrivilegedHosts`: Allow `ssm:SendCommand` on 19 exact resources (12 document ARNs, `arn:aws:ssm:us-east-1::document/AWS-RunShellScript`, 6 instance ARNs); statement `ReadCommandResults`: `ssm:GetCommandInvocation`, `ssm:ListCommandInvocations`, `ssm:ListCommands`, `ssm:DescribeInstanceInformation` on `*` (these do not support resource-level scoping). 1,606 of 6,144 characters. No wildcard in a send resource; `ssm:DeleteDocument` is not granted. |
| `aws_iam_group_policy_attachment.dell_agent_ssm_send[0]` | created | to `cloudops-dell-agents-group` |

Expected: **2 to add, 0 to change, 0 to destroy**; `aws_iam_policy.dell2_ssm` does NOT change (the document is the file, byte for byte; `DenyShellDocuments` reads exactly as today). The group then holds **7 managed policies of 10** (`group managed-policy attachments=7 quota=10`; this count assumes step D is applied, 8 if it is not). The two addresses are the whole `-target` list.

### The expected plan with `-var open_dell2_f1_shell_window=true` (on plan and on apply), on top of the default

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell2_ssm` | updated in place | the document becomes `module.routes_policy.shellwin_open_json` (1,886 of 6,144 characters; 1,048 closed). No resource is created: dell2's window is a different document in the policy dell2 already has, because the Deny of the shell-script document sits in that same policy and an Allow cannot override a Deny. |

Expected with the variable: **2 to add, 1 to change, 0 to destroy**; add `-target='aws_iam_policy.dell2_ssm'`. The window document is the file with one change and three added statements (`SHELLWIN-WINDOW-DIFF ... OK`): `DenyShellDocuments` loses `arn:aws:ssm:*::document/AWS-RunShellScript` and nothing else; added `DenyStartSessionOnShellScriptDocument` (the shell-script document stays refused for sessions), `AllowShellScriptOnF1HostWhileWindowOpen` (`ssm:SendCommand` on the shell-script document and the F1 instance ARN only), and `DenyOtherPrivilegedHostsWhileShellWindowOpen` (`ssm:SendCommand` on the 6 hosts' instance ARNs, for every document). **Closing the window** is any plan or apply WITHOUT the variable (the default is false): `aws_iam_policy.dell2_ssm` is updated in place back to the file. Hard close 2026-10-09T06:00Z, on the same ledger legs as the svc-irpt window; a precondition refuses the plan if the F1 host ever becomes one of the 6.

### Item 3: which IAM form gives the pairing (row `NFRA_CTLPLN-W14-S27`)

`ssm:SendCommand` is authorised against the document and the instance as separate resources with the same request context. Both ARNs in one `iam:SimulateCustomPolicy` call, per-resource results read:
- FORM 1 (the Deny leaves the shell-script document; an Allow on the shell-script document and the F1 host): dell2 + RunShellScript + F1 = allowed, but dell2 + RunShellScript + a host of the group Allow = **allowed** too (the document side is allowed by the window, the instance side by the group Allow). Not the pairing.
- FORM 2 (FORM 1 plus a Deny of `ssm:SendCommand` on the 6 hosts' instance ARNs while open): dell2 + RunShellScript + F1 = allowed; + each of the 6 hosts = explicitDeny (`DenyOtherPrivilegedHostsWhileShellWindowOpen`); + an instance outside the Allow = implicitDeny; dell1 + RunShellScript + F1 = implicitDeny (the F1 host is not in the group Allow; dell1 is untouched by the window). Built.
- No condition key tells the instance-side evaluation which document is in the request, so no narrower form exists. **The cost, stated plainly:** while the window is open dell2 cannot send ANY document to the 6 hosts. A restriction only, and only while open.

### What a Dell can newly do, in plain words

- **Both Dells, permanently once applied:** send any of the 12 command documents, and run AWS-RunShellScript (a shell), on any of the 6 stopped hosts, each running as a role the census reads YES-DELETE (production-data deletes), and read a command's result. Because the document and the instance are authorised separately, every pairing of the 19 resources is allowed (a cot document on a bd host included). Several of the 12 interpolate a free-text parameter into a shell command line (`derive_ssm_documents.py --check` PARAM lines), so a send with a crafted parameter is a command as the host's role (row `NFRA_CTLPLN-W14-S28`).
- **dell2's standing rule** (no AWS-RunShellScript) is unchanged by the default. It is not a shell boundary once the group Allow applies, for the reason in the line above.
- **dell2, window open only:** `ssm:SendCommand` with AWS-RunShellScript against the F1 host `i-0167fd745ad906a66` alone (a shell on the runner host, whose role the census reads NO).
- **Still refused:** `ssm:DeleteDocument` (12 documents x 2 Dells, implicitDeny, `routes_still_refused=24`); every other shell and session document for dell2; the export render document for dell2; a document the Allow does not name against a host it does.

### Simulation, this step

`POLICY-SIM allowed_ok=22/22 denied_ok=15/15 passrole_ok=5/5 protected_ok=8/8 freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 sendcmd_ok=34/34 shellwin_ok=18/18 routes_freed=114/138 routes_still_refused=24 vendor_ok=245/245 all_ok=True` (run twice, outputs identical; file `NFRA_CTLPLN.TO-CT-a-1.amendment19.simulate_policy.outputs.txt`). `sendcmd_ok` counts, per user, the 12 documents to a host of the Allow (allowed), the shell-script document (dell1 allowed; dell2 explicitDeny by `DenyShellDocuments`, row `NFRA_CTLPLN-W14-S29`), `ssm:DeleteDocument` (refused), a document the Allow does not name to a host (refused), one of the 12 to an instance the Allow does not name (refused), and the result read (allowed). `shellwin_ok` counts the window-diff check and 17 arms (open and closed). `routes_freed` moved 90 to 114 and `routes_still_refused` 48 to 24 because the sends of the twelve documents now read allowed. `ssm_ok`'s arm "dell1 reads a command result" read denied at the base and reads allowed now (the group carries the read actions).

## I. CELL 3 -- item 4 lifted (IAM roles and policies) and the Dells' plan reads (amendment 20; Andrew-direct 2026-10-08 ~13:2xZ "2.) LIFT ITEM 4"; `1.0.0_SA_CTO` msg 107398)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SECRET VALUE OR PARAMETER VALUE WAS READ. The only AWS calls were `iam:SimulateCustomPolicy` and `iam:SimulatePrincipalPolicy` (read-only). The live documents were not compared to the repository text, except that `SimulatePrincipalPolicy` (the Dell users' live policies) and the repository documents without the new policies gave the same decision on all 416 plan-read rows. dell2's F1 shell window variable defaults to closed; every simulation reads the closed document, and no live arm was read.

### The expected plan, by reading (default variables), by address

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell_agent_iam_roles` (`cloudops-dell-agent-iam-roles-policy`) | created | statement `AllowIamRolesPoliciesAndInstanceProfiles` (28 actions on `*`: role create, delete, update, update description, update trust policy, tag, untag, inline put and delete, managed attach and detach, permissions boundary put and delete, service-linked role create and delete; managed policy create, delete, create version, delete version, set default version, tag, untag; instance profile create, delete, add and remove role, tag, untag); `AllowPassAnyRole` (`iam:PassRole` on `*`, no condition); `DenyIamUsersGroupsKeysAndAccount` (69 exact iam: write actions on `*`). 2,888 of 6,144 characters. |
| `aws_iam_group_policy_attachment.dell_agent_iam_roles` | created | to `cloudops-dell-agents-group` |
| `aws_iam_policy.dell_agent_plan_reads` (`cloudops-dell-agent-plan-reads-policy`) | created | statement `ReadSsmParametersPlanReads`: `ssm:GetParameter` and `ssm:GetParameters` on two exact ARNs (`parameter/mdpf/custody_source` and the public `.../al2023-ami-kernel-default-arm64`). No wildcard, no write action. 531 characters. |
| `aws_iam_group_policy_attachment.dell_agent_plan_reads` | created | to `cloudops-dell-agents-group` |
| `aws_iam_policy.dell_agent_deploy` | updated in place | the document loses `DenyEveryIamWrite` and `DenyPassRoleExceptNamed` (5,126 to 4,759 of 6,144 characters); nothing else in it changes. The policy's description still says "never change access" and is left (a description is ForceNew; row `NFRA_CTLPLN-W14-S36`). |

Expected: **4 to add, 1 to change, 0 to destroy.** The five addresses are the whole `-target` list. The group then holds **9 managed policies of 10** (`group managed-policy attachments=9 quota=10`). Nothing in the other group policy files, the routes module, the secrets documents or dell2's own policy changes.

### Item 1: what refused IAM writes, and what allowed them (printed from `dell_deploy_policy.json` at the base)

- `DenyEveryIamWrite`: Deny, Resource `*`, Action `iam:Create*, Delete*, Put*, Attach*, Detach*, Update*, Add*, Remove*, Tag*, Untag*, Set*, Upload*, Enable*, Deactivate*, ChangePassword`. REMOVED.
- `DenyPassRoleExceptNamed`: Deny, Resource `*`, Action `iam:PassRole` (the CT-c-3 form with no applied role record). REMOVED.
- No Allow covered an IAM write before (`iam:Get*`, `iam:List*` in `ReadOnlyForTerraformPlan`; `iam:SimulatePrincipalPolicy` on the user's own ARN in the create policy). Those stay.

### The narrow Deny (exact list), and why it lives in the new policy

The old Deny matched 97 IAM operations (the installed botocore model, version 1.43.0). 28 are in the Allow; the other **69 are the narrow Deny, exactly**: `AddClientIDToOpenIDConnectProvider, AddUserToGroup, AttachGroupPolicy, AttachUserPolicy, ChangePassword, CreateAccessKey, CreateAccountAlias, CreateDelegationRequest, CreateGroup, CreateLoginProfile, CreateOpenIDConnectProvider, CreateSAMLProvider, CreateServiceSpecificCredential, CreateUser, CreateVirtualMFADevice, DeactivateMFADevice, DeleteAccessKey, DeleteAccountAlias, DeleteAccountPasswordPolicy, DeleteGroup, DeleteGroupPolicy, DeleteLoginProfile, DeleteOpenIDConnectProvider, DeleteSAMLProvider, DeleteSSHPublicKey, DeleteServerCertificate, DeleteServiceSpecificCredential, DeleteSigningCertificate, DeleteUser, DeleteUserPermissionsBoundary, DeleteUserPolicy, DeleteVirtualMFADevice, DetachGroupPolicy, DetachUserPolicy, EnableMFADevice, EnableOrganizationsRootCredentialsManagement, EnableOrganizationsRootSessions, EnableOutboundWebIdentityFederation, PutGroupPolicy, PutUserPermissionsBoundary, PutUserPolicy, RemoveClientIDFromOpenIDConnectProvider, RemoveUserFromGroup, SetSecurityTokenServicePreferences, TagMFADevice, TagOpenIDConnectProvider, TagSAMLProvider, TagServerCertificate, TagUser, UntagMFADevice, UntagOpenIDConnectProvider, UntagSAMLProvider, UntagServerCertificate, UntagUser, UpdateAccessKey, UpdateAccountPasswordPolicy, UpdateDelegationRequest, UpdateGroup, UpdateLoginProfile, UpdateOpenIDConnectProviderThumbprint, UpdateSAMLProvider, UpdateSSHPublicKey, UpdateServerCertificate, UpdateServiceSpecificCredential, UpdateSigningCertificate, UpdateUser, UploadSSHPublicKey, UploadServerCertificate, UploadSigningCertificate` (every one prefixed `iam:`; the file is the authority and `tests/check_identity.py` prints `IAM-PARTITION ... overlap 0, unclassified none`). The statement is in the new policy, not the deploy policy, because 69 exact names pass the deploy policy's 6,144 characters. Operations the old Deny never matched (for example `ResyncMFADevice`, `Disable*` of organisation root settings, delegation accept and reject) stay refused by the absence of any Allow.

### Item 3: the Terraform roots, the reads and the table

Roots are INFERRED (row `NFRA_CTLPLN-W14-S35`): from each placed project's task-order `<paths>` blocks and `pipeline` field. 15 placed projects (dell1: MDPF_HEALGAP, MDPF_SECCLASS, MDPF_SECHIST, MDPF_STRATID, MDPF_TAXSMA; dell2: ADVI_BILLING, ADVI_COTBKF, DSGN_IRPTV1, IRPT_BCKEND, IRPT_CUSTDY, IRPT_DASHBD, IRPT_YCDGEN, NFRA_OPSWKF, NFRA_TRNSPT, TCKT_VNEXT); 29 of 83 Terraform roots; five projects name no root (ADVI_BILLING, DSGN_IRPTV1, IRPT_CUSTDY, MDPF_SECHIST, NFRA_OPSWKF). Every root was readable here: `origin/box/dell1` @16944312a9 and `origin/box/dell2` @846cbbe61e carry an `infra/aws/terraform` tree identical to this branch's. Roots by box: dell1 only: bd-pipeline, mdpf-secclass/new-security-classifier, mdpf-secclass/sector-writer, opal-assets, opal-gateway; dell2 only: bd-49f-auto-login, estate-report, partners-api, portal-auth, ticket-center, transcripts, ycharts-pipeline; both: cot-pipeline, mdpf-pipeline, shared-infra and the 14 `investor-reporting/*` roots. 358 `.tf` files were read; 275 reads (416 user-rows) from 22 data-source types plus `aws_ssm_parameter`; no block unmapped. The full table (root, address, action, ARN, live decision, repository decision before, after) is `NFRA_CTLPLN.TO-CT-a-1.amendment20.plan_reads_table.txt`; 412 of 416 rows read `allowed` already. The four that did not:

| user | root | address | action | ARN | before | after |
|---|---|---|---|---|---|---|
| dell1 | mdpf-pipeline | `aws_ssm_parameter.mdpf_custody_source` (`lambdas.tf:25`) | `ssm:GetParameter` | `arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source` | implicitDeny | allowed |
| dell2 | mdpf-pipeline | same | same | same | implicitDeny | allowed |
| dell1 | opal-gateway | `data.aws_ssm_parameter.al2023` (`main.tf:111`) | `ssm:GetParameter` | `arn:aws:ssm:us-east-1::parameter/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64` | implicitDeny | allowed |
| dell2 | portal-auth | `data.aws_secretsmanager_secret_version.irpt_render_jwt_public_key` (`irpt-render-secrets.tf:38`) | `secretsmanager:GetSecretValue` | `...:secret:opal/auth/irpt-render-jwt-public-key-EAL0l7` | implicitDeny | implicitDeny (HELD, row `NFRA_CTLPLN-W14-S31`) |

The held read: its secret is class OTHER in the secrets census (a public key), and the vendor block must keep OTHER refused, so it is not granted and not counted; a dell2 plan of `portal-auth` is refused at that read until the CTO rules. The grant is READ-ONLY (relay of the dell1 CTO's msgs 1218 and 1220): `ssm:GetParameter` and `ssm:GetParameters` on exact ARNs, never `ssm:PutParameter`; the parameter is type String, so no `kms:Decrypt`. Note (row `NFRA_CTLPLN-W14-S32`): the create policy already lets both Dells `ssm:PutParameter` on every parameter, this one included. Every other data-source read (STS identity, S3 objects and remote state on `opal-*` buckets, secret descriptions, Lambda layers and functions, DynamoDB tables, IAM reads, SNS, CloudFront policies, VPC, Route 53, KMS alias, SQS, SES identity) is already allowed by the `Get*`/`List*`/`Describe*` families.

### What a Dell can newly do, in plain words

- Create, change, tag and delete IAM roles, managed policies (every version), inline role policies, role attachments and instance profiles, and **pass any role to any service**. So it can give itself any permission a policy can express: it can create a role whose trust policy names its own user ARN with an administrator policy attached, and assume it; it can add a version to any managed policy attached to its group or to itself. This is the consequence Andrew's record states ("the Dell users become administrators of the account"); this pass adds no ceiling he did not ask for.
- Read the two SSM parameters above (its plan no longer stops at them).

### What still refuses, and why

- IAM users, groups, access keys, login profiles, MFA devices, SSH keys, signing and server certificates, service-specific credentials, SAML and OIDC providers, the account password policy and alias, delegation requests and organisation root settings (the 69, `explicitDeny` by `DenyIamUsersGroupsKeysAndAccount`, 69 of 69 for both users). Everything else that refused before refuses now, with one exception: `iam:UpdateAssumeRolePolicy` is one of the 75 resource-policy actions and now reads allowed through the IAM Allow (its row in `dell_respol_policy.json` records `expected_decision` allowed).

### What this step can undo (every remaining Deny on the Dell group is a policy a Dell can now rewrite)

The Deny statements that remain: `DenyCloudTrailWrites`, `DenyS3DeletesOnProductionData`, `DenyTableAndDatabaseDeletes`, `DenyApiKeyReads`, `DenyProtectedFunctions` (all in `cloudops-dell-agent-deploy-policy`); `DenyAuditTrailBucketWrites` (`cloudops-dell-agent-create-policy`); `DenyIamUsersGroupsKeysAndAccount` (the new policy); `DenyRoutesToPrivilegedRolesFunctions` (`cloudops-dell-agent-routes-fn-policy`); `DenyShellDocuments` (dell2's own `cloudops-dell2-agent-ssm-policy`). Each lives in a managed policy that `iam:CreatePolicyVersion` and `iam:SetDefaultPolicyVersion` (both now allowed, on `*`) can replace with a version that omits it, and a Dell can reach the same effect through a new role. `iam:DetachGroupPolicy`, `iam:AttachGroupPolicy`, `iam:PutUserPolicy` and the user and group calls stay refused, but the narrow Deny is itself one of the rewritable statements. The simulations grade the documents as written; they do not bind a Dell that rewrites them.

### Simulation, this step

The `POLICY-SIM` last line is in `NFRA_CTLPLN.TO-CT-a-1.amendment20.simulate_policy.outputs.txt`. `iamw_ok` counts, per user: 13 named arms (six allowed, three explicitDeny by the narrow Deny, four kept reads), two controls (CreateRole and PassRole read implicitDeny without the new policy), 97 partition arms (28 allowed, 69 explicitDeny by the narrow Deny), plus one shape arm. `planread_ok` counts every counted read for the Dell its root is placed on, one exactness arm (the policy's entries equal the set of reads the documents refuse without it; no wildcard, no write action) and six negatives (a neighbouring parameter and a different secret refused; `ssm:PutParameter` reads the same with and without the policy). One read is printed as `PLANREAD-HELD` and not counted. Existing arms that named a removed Deny were re-pointed at an action that stays refused (`iam:PutUserPolicy`, `iam:CreateLoginProfile`, `iam:CreateGroup`), so `denied_ok` keeps its count of 15; the second block (`passrole_ok`) now reads the real files and every arm reads allowed.
