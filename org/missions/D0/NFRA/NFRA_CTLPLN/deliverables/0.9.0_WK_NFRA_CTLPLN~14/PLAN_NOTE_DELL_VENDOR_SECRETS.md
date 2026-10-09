# PLAN NOTE -- three Dell limits lifted in ONE plan: secrets, the resource-policy Deny (now the resource-policy ALLOW), self-simulate (NFRA_CTLPLN.TO-CT-a-1, amendments 9 and 10)

**LATEST: section G (amendment 16, STEP E) widens the secrets grant to the 28 PLATFORM-KEY secrets and takes three Deny statements off; where sections A and B below say the PLATFORM-KEY class is NOT granted, section G governs.**

**NEWEST: section L (amendment 23, one more secret ARN, svc-commentary). Expected plan: 0 to add, 1 to change, 0 to destroy.**

**PREVIOUS: section J (amendment 21, three follow-ups on step F: one more secret ARN, one cutover-parameter Deny, one stale test retired). Expected plan: 0 to add, 2 to change, 0 to destroy.**

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


## J. FOLLOW-UP CELL TO STEP F -- the IRPT render public key granted, writes to the cutover parameter denied, one stale PassRole test retired (amendment 21; `1.0.0_SA_CTO` msg 107457 on CTO half @b51c573d66; rows `NFRA_CTLPLN-W14-S31`, `-S32`, `-S33`, new rows `-S37`, `-S38`, `-S39`)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SECRET VALUE WAS READ (the census was re-derived from the saved listing with `--reclass`: no AWS call). The only AWS calls were `iam:SimulateCustomPolicy` and, in one table run, `iam:SimulatePrincipalPolicy` on the live Dell users. The live documents were not compared to the repository text. Step F was already live when this pass ran: the live plan-read rows read `allowed` for the two SSM parameters (`derive_plan_reads.py --table`, 2026-10-08T23:41:33Z to 23:42:17Z), and the one live row that reads `implicitDeny` is the secret this cell grants. The custom-policy simulation ran 23:39:14Z to 23:40:04Z and again, as criterion CTa1-AC2, 23:43:23Z to 23:44:24Z, with identical results; no live arm changed between runs.

### The expected plan, by reading (default variables), by address

Relative to the state step F leaves (nine managed policies on the group):

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell_agent_platform_secrets[0]` (`cloudops-dell-agent-platform-secrets-policy`) | updated in place | the one statement `ReadPlatformKeys` gains one exact ARN: `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/irpt-render-jwt-public-key-EAL0l7`. 28 ARNs become 29; 2,707 characters become 2,806 of 6,144. Nothing else in the document changes. |
| `aws_iam_policy.dell_agent_deploy` (`cloudops-dell-agent-deploy-policy`) | updated in place | the document gains one Deny statement, `DenyCutoverParameterWrites` (below), placed before `DenyProtectedFunctions`. 4,759 characters become 5,046 of 6,144. Nothing else in the document changes. |

Expected: **0 to add, 2 to change, 0 to destroy.** The two addresses are the whole `-target` list. Secrets part one (`aws_iam_policy.dell_agent_vendor_secrets[0]`, 66 ARNs, 5,968 characters) is byte-for-byte unchanged; no attachment, no count, no description changes (a description is ForceNew, so none was touched: the part-two description still names signing keys, seeds, admin credentials and gateway bearer tokens, row `NFRA_CTLPLN-W14-S37`). The group still holds **9 managed policies of 10**.

### The three changes, in plain words

1. **S31 -- a public key is granted.** The secret `opal/auth/irpt-render-jwt-public-key` is the verifying half of the key pair that signs the firm's IRPT render tokens. It verifies tokens and signs nothing. The census moves it from OTHER to PLATFORM-KEY (granted; there is no public-key class, row `-S37`). Both Dells can then read its value by the exact ARN. dell2's plan of `portal-auth` reads it (`data.aws_secretsmanager_secret_version.irpt_render_jwt_public_key`, `irpt-render-secrets.tf:38`) and stopped at that read before. Census: secrets 114, granted 94 to **95**, platform_key 28 to **29**, other 19 to **18**, blocked_by_key 1 (unchanged). Plan-read rows: the held row is allowed, so `planread_ok` counts it (422 counted and 1 held becomes **423 counted, 0 held**).
2. **S32 -- the cutover parameter is protected from writes.** `DenyCutoverParameterWrites` (Effect Deny, in `cloudops-dell-agent-deploy-policy`, the group policy with room): actions `ssm:PutParameter`, `ssm:DeleteParameter`, `ssm:DeleteParameters`, `ssm:LabelParameterVersion`, `ssm:AddTagsToResource`, `ssm:RemoveTagsFromResource`; Resource exactly `arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source` (the bd-to-schwab cutover value). Reading the parameter (the plan-reads grant, `ssm:GetParameter` and `ssm:GetParameters`) is unchanged and still allowed. After step F a Dell can rewrite this policy, so the Deny guards against an accident, not an intent (the CTO's words, msg 107457). Row `-S32` was ARMED with the CTO as disarm owner: this commit builds the disarm, which is real only once applied.
3. **S33 -- one stale test is retired.** `tests/render_passrole.py` asserted the PassRole Deny that step F removed and stopped with an error. It was NOT deleted, because `tests/derive_protected_functions.py` imports two helpers from it. Its renderer and `--write` mode (which could have re-created the retired Deny) are removed; `--check` now asserts the current truth: the deploy policy holds none of `DenyPassRoleExceptNamed`, `AllowPassNamedRoles`, `DenyEveryIamWrite` and no `iam:PassRole` action, and the IAM-roles policy holds `AllowPassAnyRole` (an Allow of `iam:PassRole` on `*`) and no PassRole Deny. Its last line is now `PASSROLE-CHECK ... ok=True` (row `-S38`).

### Arms (simulation block twelve, `cutover_ok=23/23`, both Dell users)

- Each of the six write actions on the exact ARN reads `explicitDeny`, matched statement `DenyCutoverParameterWrites` (12 of 12).
- `ssm:GetParameter` and `ssm:GetParameters` on it read `allowed` (4 of 4).
- `ssm:PutParameter` on a different parameter (`parameter/other/some_parameter`) reads **allowed**, exactly as it reads with the statement taken out of the deploy policy (today's decision, from the create policy's `CreateUpdateTagCompute` on `*`); the same for a parameter whose name only begins with the cutover name (`parameter/mdpf/custody_source_other`) (4 of 4).
- Control: with the statement taken out, `ssm:PutParameter` on the cutover parameter reads `allowed` (2 of 2), so the Deny is the cause.
- Shape: one statement of that name, six actions, one exact ARN, no wildcard (1 of 1). Total 12 + 4 + 4 + 2 + 1 = 23.
- Vendor block: `vendor_ok` 245 of 245 becomes **249 of 249**. The public key reads `allowed` for both Dells and `implicitDeny` without the two secrets documents (one arm per user in the full sweep); two named arms were added per user: the public key (allowed) and `opal/auth/jwt-public-key` (OTHER, still refused); `twilio/recovery-code` and `schwab/sdd/session` stay refused.

### What this cell can undo

`DenyCutoverParameterWrites` is a statement in a managed policy a Dell can replace with a new version (step F, section I); it protects against accident only. Granting a public key adds no capability a Dell did not have through the IAM Allow (a Dell can already grant itself any read), and the key is public.

### Not done

`tests/plan_reads_census.json` was not re-derived: the registers now place one more Dell project (`MDPF_DEMQUE`) than the saved census (row `NFRA_CTLPLN-W14-S39`); whether its roots add a refused read is unread.

## K. THE UI-WALKER PASSWORD READ, BY EXACT ARN (amendment 22; `1.0.0_SA_CTO` msg 107538, superseding 107534 on dell1's correction)

Metadata read (describe-parameters, no value): `/opal/ui-walker/password` is a SecureString under `KeyId alias/aws/ssm` (the AWS-managed key), so no KMS statement is written.

Expected plan by reading: ONE policy changed in place, `aws_iam_policy` for `dell_planreads_policy.json` (the group's plan-reads policy, 430 -> 630 characters, far under 6,144). Nothing created, nothing destroyed; the group's managed-policy count is unchanged (9 of 10).

The statement: Sid `ReadUiWalkerPassword`, Allow `ssm:GetParameter` ONLY on `arn:aws:ssm:us-east-1:313476888478:parameter/opal/ui-walker/password`. No `GetParameters`, no `GetParametersByPath`, NO `ssm:DeleteParameter`, no wildcard.

Blast radius: both Dells can read that one password (the decrypt happens under the AWS-managed key, which any principal allowed GetParameter may use). They still cannot delete it (a delete would erase the version history; simulated implicitDeny) and cannot read any sibling parameter. `ssm:PutParameter` on it reads as before the change (allowed, from the existing deploy grant), so a Dell can write a new version and now also read it back. Re-enabling the walker login is a separate decision.

Simulation: `walker_ok=11/11` (both Dells; GetParameter allowed, DeleteParameter and GetParameters implicitDeny, GetParameter on `/opal/ui-walker/other` implicitDeny, PutParameter allowed with and without the statement, plus the shape check).

## L. ONE MORE SECRET ARN: `opal/ticketing/svc-commentary` (amendment 23; dell2 `2.0.0_SA_COO~V2` msg 2046, relay `RELAY_20261009T0122Z_DELL2_SVC_COMMENTARY_SECRET_GRANT`; both never-widen halves signed @b70dd6fbad)

Metadata read only (secretsmanager ListSecrets: names, descriptions, tags, key ids; no value). The live listing holds 115 secrets in us-east-1 (17 regions listed, 0 listing errors); the saved census held 114. The ONLY difference is this secret: nothing removed, renamed or changed in description, tags or key.

Census row: `opal/ticketing/svc-commentary`, class PLATFORM-KEY (a service bearer token, RS256, 90-day TTL, create-only on the firm's own ticket API; the same kind as `opal/ticketing/svc-analyst-intake`), default key (`kms_default` true, no customer-managed key), decision GRANTED, arn `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-commentary-pXsmuU`. The census was extended by exactly this one record from the live listing (the six-minute repository scan was not re-run: every other record, reference, placement and grant is byte-for-byte as saved) and re-classed with `--reclass`: granted 95 -> 96, platform_key 29 -> 30, granted_platform_key 29 -> 30, other 18, blocked_by_key 1.

Expected plan by reading: ONE policy changed in place, the PLATFORM-KEY secrets part (`ReadPlatformKeys`, built by the module from the census): one ARN added, 29 -> 30 entries, 2,898 characters against 6,144 (part one, vendor and client sessions, is unchanged at 66 entries, 5,968). Nothing created, nothing destroyed; the group's managed-policy count is unchanged. Action `secretsmanager:GetSecretValue` only, exact ARN, no wildcard.

Simulation: `vendor_ok` 249/249 -> 255/255 (both Dells: the per-secret sweep gains this secret allowed, and without the secrets documents implicitDeny; the NAMED arm for it allowed; an unlisted sibling `opal/ticketing/svc-commentary-other` refused; per user 3 new arms).

What a Dell can newly do: read that one token (create analysis requests as the commentary service). It can write neither a user-policy nor a resource policy on it under its own box's never-widen pair (dell2 measured PutUserPolicy explicitDeny, PutResourcePolicy implicitDeny).


## M. DELL2 SHELL PARITY, STANDING, AND THE WINDOW RETIRES (amendment 24; Andrew-direct ~02:5xZ 2026-10-09 "the DELLS should not be waiting on us for this function"; `1.0.0_SA_CTO` msg 107664, CTO half signed @de8b26aa1f)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE, NO SSM COMMAND WAS SENT, NO SECRET VALUE WAS READ. The only AWS calls were `iam:SimulateCustomPolicy` and `iam:SimulatePrincipalPolicy` (read-only). The live documents were not compared to the repository text.

### Expected plan by reading (addresses)

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell2_ssm` (`cloudops-dell2-agent-ssm-policy`) | updated in place | the document becomes the file `dell2_ssm_policy.json` as rendered by `tests/derive_ssm_documents.py --write` (1,206 characters without whitespace, of 6,144). Name, description and tags are byte for byte as before, so the change is an in-place new policy version, not a replacement. |

Expected: **0 to add, 1 to change, 0 to destroy.** Nothing else moves: `aws_iam_user_policy_attachment.dell2_ssm` is unchanged; dell1's policies, the group Allow (`aws_iam_policy.dell_agent_ssm_send[0]`) and the three group policy files are untouched; the group's managed-policy count is unchanged (9 of 10). The variable `open_dell2_f1_shell_window` and the module outputs `shellwin_open_json`, `shellwin_open_chars`, `shellwin_f1_in_send_hosts` and the module input `dell2_ssm_base` are removed from the configuration; none is a resource, so none appears in a plan. Whichever of the two former documents the account holds today (the closed file, or the window-open derivation if a window was applied), the next plan shows the same single in-place change, and a plain plan can no longer re-close the access. `-target='aws_iam_policy.dell2_ssm'` is the whole target list. The transcripts root: **no change** (item 4: all six written prefixes already read allowed; see below).

### The document, before and after (statement Sid and the documents it names)

| statement | before | after |
|---|---|---|
| `SendResidentDocumentsToResidentHost` (Allow `ssm:SendCommand`) | instance `i-0167fd745ad906a66`, `irpt-ycharts-deploy`, `irpt-ycharts-run` | the same three, plus `arn:aws:ssm:us-east-1::document/AWS-RunShellScript` |
| `ReadCommandResults` (Allow) | 4 read actions on `*` | unchanged |
| `DenyShellDocuments` (Deny `ssm:SendCommand`, `ssm:StartSession`) | AWS-RunShellScript, AWS-RunPowerShellScript, AWS-RunRemoteScript, AWS-StartInteractiveCommand, AWS-StartNonInteractiveCommand, AWS-StartSSHSession, AWS-StartPortForwardingSession*, `irpt-export-render-run` | the same eight MINUS AWS-RunShellScript |
| `DenyStartSessionOnShellScriptDocument` (Deny `ssm:StartSession`) | absent | added: `arn:aws:ssm:*::document/AWS-RunShellScript`, so a session on the shell document stays refused |

### What a Dell can newly do, in plain words

- **dell2, standing:** `ssm:SendCommand` with `AWS-RunShellScript` to the resident host `i-0167fd745ad906a66` (census role `irpt-ycharts-runner-role`, verdict NO): a shell as that host's role, with no window and no ledger leg. On the six privileged route hosts dell2 already had the same send through the group Allow, as dell1 does; that does not change.
- **dell1:** nothing changes. dell1 still cannot send anything to the resident host (the host is not in the group Allow).
- **Still refused for dell2:** AWS-RunPowerShellScript, AWS-RunRemoteScript, AWS-StartInteractiveCommand, the session documents, `ssm:StartSession` on the shell document, `irpt-export-render-run`, a send to any instance outside the resident host and the six, and `ssm:DeleteDocument`.
- **Cross-product note (unchanged in kind):** because IAM authorises the document and the instance as separate resources, dell2 may also pair its resident documents with the six hosts and the shell document with any of its allowed instances; every such pairing is a send dell2 already held or now holds by name.

### Simulation, this step

`POLICY-SIM ... ssm_ok=14/14 ... walker_ok=11/11 iamw_ok=225/225 planread_ok=423/423 sendcmd_ok=33/33 shellpar_ok=18/18 routes_freed=114/138 routes_still_refused=24 vendor_ok=255/255 all_ok=True` (file `NFRA_CTLPLN.TO-CT-a-1.amendment24.simulate_policy.outputs.txt`). Two arms changed expectation and moved into `shellpar_ok`: the `ssm_ok` arm "dell2 sends the shell document to the host" (explicitDeny before, allowed now; `ssm_ok` 15 to 14) and the `sendcmd_ok` arm "dell2 sends the shell-script document to a host of the Allow (window closed)" (explicitDeny before, allowed now; `sendcmd_ok` 34 to 33). `shellpar_ok` is 18 arms: dell2 allowed on the resident host and on one route host; refused on an outside instance, PowerShell, remote-script, interactive-command, a session on the shell and on the SSH document, the export render document; its resident document still allowed; DeleteDocument refused; and seven dell1 control arms. Controls: the same F1 send under the pre-change file reads explicitDeny, under the new file without the shell Allow resource reads implicitDeny, and the session arm without the new Deny reads implicitDeny.

### Transcript jobs (item 4)

Prefixes the NFRA_TRNSPT jobs write, from `NFRA_TRNSPT.TO-RUN-x9` and `-b11` (`teams/transcripts/silver/research_meeting/`, 29 keys) and `infra/aws/terraform/transcripts/` (`chat_assist.tf`: `teams/transcripts/bronze/chat_messages/`, `silver/chat_threads/`, `state/chat_assist/`; `pull.tf`: `teams/transcripts/`; `mail_pull.tf`: `outlook/transcripts/`). dell2 `s3:PutObject` on each reads **allowed** (6 of 6, matched `S3ObjectsOnOpalBuckets`), positive control allowed, negative controls refused. Nothing is refused, so **nothing was granted and the transcripts root is unchanged.** `check_transcripts_dell_decrypt.py` still prints `dell_write_refused=8/10`; no arm moved. Row `NFRA_CTLPLN-W14-S44`: the key grants the Dells Decrypt and DescribeKey only, so a Dell PutObject would still fail at `kms:GenerateDataKey`; not widened here.

## N. DELL2 ONLY GAINS kms:GenerateDataKey ON THE TRANSCRIPTS KEY (amendment 25; row `NFRA_CTLPLN-W14-S44`; `1.0.0_SA_CTO` ruling (b) msg 107696, record `ANDREW_DIRECT_20261009_025xZ_DELLS_RUN_THEIR_OWN_SCRIPTS_NO_LAPTOP_WAIT.md` @8fc644a586; COO half ADDENDUM 1)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED AND NO PLAN WAS RUN AGAINST THE BACKEND. The only AWS calls were `iam:SimulateCustomPolicy`, `iam:SimulatePrincipalPolicy`, `kms:DescribeKey`, `kms:GetKeyPolicy`, `sts:GetCallerIdentity` (read-only). No object was read, no bucket listed, no decrypt or data-key call was made.

### Writers of the key's policy (counted first)

One. `comp-find` over `infra/` for `aws_kms_key|aws_kms_key_policy|aws_kms_grant|aws_kms_alias` (87 hits, 1889 files scanned) and for the key's address and alias (36 hits, 1889 files): the only resource that sets the key policy is `aws_kms_key.transcripts` (its `policy` argument) at `infra/aws/terraform/transcripts/main.tf:75`. There is no `aws_kms_key_policy` resource anywhere under `infra/`. The other `transcripts` files only reference the key (`chat_assist.tf:81-82`, `mail_pull.tf:111`, `pull.tf:111`) or hold `aws_kms_grant` resources (`commentary.tf:90`, `mail_pull.tf:91`, `pull.tf:91`, and `modules/ldo/main.tf:311`), which are grants and do not write the policy.

### Expected plan, by reading (address)

| resource address | action | what |
|---|---|---|
| `aws_kms_key.transcripts` | update in place | `policy` only: one statement appended, `Dell2AgentUserGenerateDataKey` |

Nothing else. The new variable `dell2_agent_user_name` has a default and creates no resource. `aws_kms_alias.transcripts`, the bucket, its policy (it refers to the key's ARN, which does not change), the encryption configuration, the three `aws_kms_grant` resources in this root and the Lambda resources are untouched. Plan summary by reading: `0 to add, 1 to change, 0 to destroy`. The issuer measures the real plan.

### The key policy, before and after (statement Sid, principal, actions)

Before (live, read with `kms get-key-policy`, equal to the render of `5c1d0af92c`; 3 statements):
- `RootAdministersTheKeyAndCannotUseIt`: account root; administration actions only (unchanged).
- `NamedReadersUseTheKey`: `var.reader_principal_arns`; `kms:Encrypt`, `kms:Decrypt`, `kms:ReEncrypt*`, `kms:GenerateDataKey*`, `kms:DescribeKey` (unchanged, byte-identical).
- `DellAgentUsersDecryptOnly`: the two Dell agent users; `kms:Decrypt`, `kms:DescribeKey` (unchanged).

After (4 statements): the three above, then
- `Dell2AgentUserGenerateDataKey`: Allow; Principal the dell2 agent user alone (`arn:aws:iam::<account>:user/<var.dell2_agent_user_name>`; the variable's default is the builder's output for that user, `cloudops-dell2-agent-user`); Action exactly `kms:GenerateDataKey`; Resource `*`.

No other action. Not `kms:Encrypt`, not `kms:ReEncrypt*`, not `kms:GenerateDataKeyWithoutPlaintext`: the S3 PutObject of an SSE-KMS object asks the key for `kms:GenerateDataKey`; a multipart upload also asks for `kms:Decrypt`, which both Dells already hold. No evidence of a further action needed was found, so none is added.

### What dell2 newly can do, in plain words

Its S3 PutObject under the jobs prefixes (already allowed by its own S3 policy, row `NFRA_CTLPLN-W14-S44`) can now complete on the transcripts bucket, because S3 can obtain the data key. It can also call `kms:GenerateDataKey` directly on that key, which yields a data key encrypted under the transcripts key and a plaintext copy for the caller; the plaintext key of a key it generates itself reveals nothing about existing objects. dell1 does not gain it, and the reader's access does not move.

### Arms (simulation, `check_transcripts_dell_decrypt.py`)

- dell2 `kms:GenerateDataKey` on the key: implicitDeny before, allowed now (the one arm that moved).
- dell2 `s3:PutObject` on `teams/transcripts/silver/research_meeting/date=2026-10-08/x.parquet`: allowed (identity leg) and, with the key leg, allowed end to end. `dell2_generate_ok=True`.
- dell1, the same two arms: identity leg allowed (the group's S3 policy), key leg implicitDeny, composed PutObject refused. `dell1_generate_refused=True`.
- `dell_write_refused` is restated: 7/10 now (was 8/10). The three arms that read allowed, by name: dell1 `kms:PutKeyPolicy`, dell2 `kms:PutKeyPolicy` (the applied resource-policy Allow, accepted at amendment 17, unchanged) and dell2 `kms:GenerateDataKey` (new). The arm that moved: dell2 `kms:GenerateDataKey`, refused to allowed. No other arm moved, for either user, against the render of `5c1d0af92c`.
- The reader's Decrypt and Encrypt stay allowed; an unlisted user stays refused; the rendered document differs from the applied one by exactly one added statement (`statements_added=1`); the live key policy equals the `5c1d0af92c` render, so the check reads `ok=True` before the apply and reads `ok=False` after it by construction (the pre-apply guard of row `NFRA_CTLPLN-W14-S40`).
- Mutant controls (scratch copies of `main.tf`, `TRANSCRIPTS_MAIN_TF`): the new statement widened to both Dells reads `dell1_generate_refused=False ok=False`; `kms:Encrypt` added to the new statement reads `dell2_generate_ok=False ok=False` with the unexpected move named.

### Rollback

Remove the statement (revert this commit) and apply again: the key policy is a single in-place update and nothing depends on the new statement. Until the revert is applied, dell2 keeps `kms:GenerateDataKey`.

### Not done

The apply; a plan against the backend; a real PutObject through SSE-KMS (it needs the apply and is another route's). The simulator takes the union of identity and resource policies and does not model the KMS rule that a customer-managed key needs its key policy to permit use; the key leg here uses a neutral identity policy so only the key policy can allow, and the S3 leg is the user's live identity policies only.

## O. DELL1 AND DELL2 HOLD IDENTICAL PERMISSIONS (amendment 26; Andrew-direct ~03:5xZ 2026-10-09 "DELL1 and DELL2 should have the exact same permissions and layout"; `1.0.0_SA_CTO` msg 107701, record @910951a1e0; COO half `NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_DELL2_IDENTICAL_20261009.md`)

Author: 0.9.0_WK_NFRA_CTLPLN~14. NOTHING WAS APPLIED AND NO PLAN WAS RUN AGAINST THE BACKEND. AWS calls were read-only: `iam:SimulateCustomPolicy`, `iam` list calls for the two users and the group, `kms:DescribeKey` and `GetKeyPolicy`, `s3api get-bucket-policy` on the three fenced buckets (policy text only), `sts:GetCallerIdentity`. No object was read, no secret value read.

### The census (printed by `tests/simulate_dell_parity.py`, measured, writers counted)

| per-user grant | where | writers | before | after |
|---|---|---|---|---|
| `dell1_bus` (receive from `agentbus-global-dell1-queue*`) | identity root, 1 `aws_iam_policy`, 1 user attachment | 1 | dell1 only | unchanged (per box) |
| `dell2_bus` (the same, dell2's queue) | identity root, 1 policy, 1 user attachment | 1 | dell2 only | unchanged (per box) |
| `dell2_ssm` (resident documents, shell-script document, denies) | identity root, 1 policy, 1 user attachment | 1 | dell2 only | BOTH: a second attachment, `aws_iam_user_policy_attachment.dell1_ssm` |
| transcripts key `DellAgentUsersDecryptOnly` | `aws_kms_key.transcripts` policy | 1 | both users | unchanged |
| transcripts key GenerateDataKey | `aws_kms_key.transcripts` policy | 1 | (not applied: amendment 25 named dell2 only) | `DellAgentUsersGenerateDataKey`, BOTH users |
| bucket fences naming a Dell (`infra/logic/registry/exemptions.json`, built by `modules/opal_name` into the shared-infra bucket policies) | registry rows | 1 registry file, 4 `.tf` files read it | 3 buckets x 2 users | unchanged: the two users hold the same rows on the same 3 buckets |
| any other `aws_iam_user_policy`, `aws_iam_user_policy_attachment` or group membership naming a Dell outside the identity root | all `.tf` under `infra/aws/terraform/` | 0 | none | none |
| inline policies, other groups, other attached policies, live | `iam list-*` for each user | - | dell1: bus only; dell2: bus + ssm; no inline; both in the one group (9 attached) | dell1 gains ssm at the apply |

What moved to the group: nothing. What was mirrored: `dell2_ssm` to dell1 (one more attachment of the existing policy), the key's GenerateDataKey statement to both users. Why the attachment and not the group: the group holds nine managed policies today (quota ten); a tenth would sit exactly on the quota and leave nothing for the next grant, and moving the policy from the user to the group would create a group attachment and destroy a user attachment in one apply, which Terraform does not order (a possible gap in dell2's access). Attaching the same policy to dell1 is one create and touches nothing live. The policy keeps its name `cloudops-dell2-agent-ssm-policy`, address, description and tags (its `Device = dell2` tag and the word dell2 in the name are now cosmetic; a rename or description change would REPLACE the live policy and its dell2 attachment, so a rename is a separate step that must be ordered create-before-destroy).

Group managed-policy count: 9 of 10 (deploy, create, iam-roles, plan-reads, respol-allow, ssm-send, vendor-secrets, platform-secrets, routes-fn); `check_identity.py` prints `group_policies=9/10`.

### Expected plan, by reading, per root

Identity root `infra/aws/terraform/nfra-ctlpln-identity/` (last plan against the backend before this change: 03:53Z 2026-10-09, `No changes`, `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/dell2_shell_parity_20261009/replan.txt`):

| resource address | action | what |
|---|---|---|
| `aws_iam_user_policy_attachment.dell1_ssm` | create | attaches `cloudops-dell2-agent-ssm-policy` to `cloudops-dell1-agent-user` |

Plan summary by reading: 1 to add, 0 to change, 0 to destroy. NO resource is REPLACED or DESTROYED, so there is no ordering gap in dell2's access. The resource-address diff against the previous commit (`29f97ce54c`) is in `NFRA_CTLPLN.TO-CT-a-1.amendment26.plan_by_reading.txt`: one block added, none removed, none body-changed.

Transcripts root `infra/aws/terraform/transcripts/` (the live key policy equals the render of `5c1d0af92c`, three statements):

| resource address | action | what |
|---|---|---|
| `aws_kms_key.transcripts` | update in place | `policy` only: one statement appended, `DellAgentUsersGenerateDataKey` (both Dell users, `kms:GenerateDataKey`, Resource `*`) |

0 to add, 1 to change, 0 to destroy for this order's edit. AMENDMENT 25's variable `dell2_agent_user_name` is removed (never applied; it created no resource). THE ROOT ALSO CARRIES ANOTHER CELL'S PENDING CHANGES (row `NFRA_CTLPLN-W14-S46`): `data.terraform_remote_state.irpt_core` added and `aws_iam_policy.commentary` and `aws_lambda_function.commentary` body-changed, arriving with `424998b161` (NFRA_TRNSPT TO-TR-c17, "DESIRED, not applied"). An untargeted plan of the root would show those too; the apply of this change should be TARGETED at `aws_kms_key.transcripts`.

### Every dell1 arm that flipped (simulation, effective set as built)

Refused to allowed (3): `ssm:SendCommand` on the resident host (`i-0167fd745ad906a66`) with `irpt-ycharts-deploy`; the same with `irpt-ycharts-run`; the same with `AWS-RunShellScript`. Also refused to allowed on the transcripts key: `kms:GenerateDataKey`, and so a Dell PutObject of the jobs' output under SSE-KMS completes (composed S3 leg + key leg). Still refused, now by an explicit Deny instead of by silence (same effect, not a flip): `AWS-RunPowerShellScript`, `AWS-RunRemoteScript`, `AWS-StartInteractiveCommand` to the resident host, `ssm:StartSession` on the shell-script and SSH-session documents, and `irpt-export-render-run`. Unchanged: dell1 reads command results, sends the 12 documents and the shell-script document to the six privileged hosts, is refused on another instance, and cannot delete a document.

### Parity (`tests/simulate_dell_parity.py`)

`DELL-PARITY arms=1531 equal=1531/1531 unequal=0 ok=True`. Arms: 1,494 (action, resource) pairs from every statement of the 10 documents either user holds (wildcard actions expanded from the installed botocore service models; group documents sampled at their first and last resource per statement, per-user documents in full); 8 `symmetric_by_box` arms for the bus policies, compared BY ROLE (each user on its own queue, each on the other box's queue) and equal; 13 arms on the transcripts key policy as rendered from the Terraform; 12 arms on the live policies of the three fenced buckets (each reads `GetObject`, `PutObject`, `ListBucket` allowed and `DeleteObject` explicitDeny for BOTH users). Negative controls: iam.tf without the `dell1_ssm` attachment reads 18 unequal arms (`ssm:SendCommand` on the host and the documents), `ok=False`; the key statement narrowed to dell2 reads 1 unequal arm (`kms:GenerateDataKey`), `ok=False`. The LIVE account still shows dell1 without the ssm policy, as expected before the apply (`LIVE-VS-BUILT` line).

### What each Dell can newly do, in plain words

dell1 can send the two resident documents and the AWS shell-script document to the resident host and read the result, and can write the jobs' output into the transcripts bucket under its key. dell2 can write the same output under the key (amendment 25, now for both). Neither can send a PowerShell, remote-script, interactive or session document, or the export render document, or delete a command document.

### Not done

The apply; a plan against the backend; a real `SendCommand` or PutObject. The live bucket fences were read for three buckets only (the buckets whose registry rows name a Dell); the group documents are sampled at two resources per statement. `kms:GenerateDataKey` on the transcripts key for dell2 was never applied before this pass, so dell2's live key access today is Decrypt and DescribeKey only.

## P. BOTH DELLS RUN THE SHELL DOCUMENT ON mdpf-daily-runner, STANDING (amendment 27; dell2 `2.0.0_SA_COO~P2` relay msg 107720, row IRPT_BCKEND-D2-S25 @627f6fa99e, for IB-pr-383; both Dells by amendment 26)

### First read: where `i-02448edb624a7a7cf` stands (printed before the edit)

| question | answer | file:line |
|---|---|---|
| Does any explicit Deny in the identity root name this instance (by id or ARN)? | NO. The only occurrences of the id in the root are two census rows. No `instance/` ARN sits in any Deny of any policy file; the only `instance/` expression outside the ssm policy and the tests is the group send Allow's host list | `tests/reached_roles_census.json:1679`, `:6050`; `modules/routes_policy/main.tf:110` (an Allow) |
| Does a comment, ruling or census row EXCLUDE it on purpose? | NO. Its census row reads `route_status: NO-ROUTE-FOUND`, which says no document was found to run on it, not that it is excluded | `tests/reached_roles_census.json:1694` |
| Is it one of the routes' privileged hosts? | NO. The send Allow's hosts are the 6 host routes with at least one document; this host has `documents: []`. The routes hosts Deny is removed from the root (amendment 15, step D) | `tests/reached_roles_census.json:1685-1692`; `routes.tf:45-52` |
| Instance role (name only) | `mdpf-daily-runner-ec2-role` (instance profile `mdpf-daily-runner-profile`); the census gives the role no YES-IAM, YES-TRAIL or YES-DELETE verdict (`yes_any=10` does not include it) | `tests/reached_roles_census.json:1681-1684`, `:6046-6060` |
| Is the shell document already sent to it by repo code? | YES: `directory/refresh.py` and `holdings_refresh/refresh_dispatch.py` send `AWS-RunShellScript` to it (`EC2_MANIFEST.json services.mdpf-daily-runner`) | `tests/derive_ssm_documents.py --check` prints both under SENT-TO-THE-INSTANCE |
| State | census (taken 2026-10-07T11:05:41Z) says `stopped`; the live state was not read (no instance call is permitted) | `tests/reached_roles_census.json:1680` |

No deliberate Deny exists, so the order's STOP did not fire. Row `NFRA_CTLPLN-W14-S48` records two facts a signer may want beside the grant (the role's assume-chain to the 49 Financial source principal, and the resident-document cross pair).

### The policy diff (`dell2_ssm_policy.json`, rendered by `tests/derive_ssm_documents.py --write`; `--check` compares)

One statement added, between `SendResidentDocumentsToResidentHost` and `ReadCommandResults`; nothing else in the file moved:

```
{ "Sid": "SendShellScriptToDailyRunner", "Effect": "Allow", "Action": "ssm:SendCommand",
  "Resource": [ "arn:aws:ec2:us-east-1:313476888478:instance/i-02448edb624a7a7cf",
                "arn:aws:ssm:us-east-1::document/AWS-RunShellScript" ] }
```

Why a separate statement and not a third entry in the first: the first statement is the resident host's, and its Sid says so. The instance id is typed once in `derive_ssm_documents.py` (`DAILY_RUNNER_ID`) and the script checks it equals `EC2_MANIFEST.json services.mdpf-daily-runner.instance_id` (printed `manifest agrees: True`). Every other shell or session document stays in `DenyShellDocuments`; `ssm:StartSession` on the shell document stays in `DenyStartSessionOnShellScriptDocument`. The policy is 1,421 characters (limit 6,144). The group keeps 9 of 10 managed policies; no new policy, no new attachment.

### Arms that moved (simulation, both users, the policies as built)

- `shellpar_ok` 22/22 -> 32/32: ten arms added, five per user, on `mdpf-daily-runner`: shell document ALLOWED; PowerShell, remote-script and interactive-command documents explicitDeny by `DenyShellDocuments`; the export render document explicitDeny.
- The arms that used this host as "an instance outside both grants" (shellpar 03 and 14, `ssm_ok` 03 and 09, `sendcmd_ok` 16 and 32) now use `i-00abf626b065373bc`, the first census host in no grant, and still read `implicitDeny`. Same decisions on a different instance: the only lines that differ from the amendment-26 run besides the ten new arms. (Before this pass the former arms read `implicitDeny` on this host: the refusal dell2 measured.)
- Every other counter is unchanged: `ssm_ok=18/18 sendcmd_ok=33/33 walker_ok=11/11 iamw_ok=225/225 planread_ok=423/423 vendor_ok=255/255 routes_freed=114/138 routes_still_refused=24`, `all_ok=True`.
- Reported, not counted (IAM authorises instance and document separately): both Dells may also send `irpt-ycharts-run` and `irpt-ycharts-deploy` to this host (`allowed, allowed`); a group-Allow document sent to it is `implicitDeny` (`NFRA_CTLPLN.TO-CT-a-1.amendment28.a27_cross_pairs.outputs.txt`).

### Parity

`DELL-PARITY arms=1532 equal=1532/1532 unequal=0 ok=True` (1531 before: the new statement adds one arm; every arm equal for both users, because both hold the one file).

### Expected plan, by reading

Identity root `infra/aws/terraform/nfra-ctlpln-identity/`:

| resource address | action | what |
|---|---|---|
| `aws_iam_policy.dell2_ssm` | update in place | `policy` only: one statement added. Name, description and tags are untouched, so NOT replaced; the new version becomes the default and both attachments keep pointing at the same policy ARN, so there is no gap |

Relative to the amendment-26 built state: 0 to add, 1 to change, 0 to destroy. If amendment 26 has not been applied yet (no apply record for `dell1_ssm` found under `org/tier2_senior`; the last backend plan, 03:53Z, `No changes`, preceded it), the plan also carries `aws_iam_user_policy_attachment.dell1_ssm` as 1 create: 1 to add, 1 to change, 0 to destroy. Nothing else may move. Nothing is REPLACED or DESTROYED.

### Not done

The apply; a plan against the backend; a real `SendCommand`; the live state of the instance; the live documents.

## Q. THE GenerateDataKey STATEMENT IS SCOPED TO S3 AND THIS BUCKET (amendment 28 and the issuer's ruling; dell2 `2.0.0_SA_COO~T2` relay msg 107726/107740; `TO-RUN-a17` stopped at the key)

### What the key statement says now (`infra/aws/terraform/transcripts/main.tf`, `DellAgentUsersGenerateDataKey`)

Principals: both Dell users (`var.dell_agent_user_names`). Action: `kms:GenerateDataKey` alone. Resource `*` (the key). Exactly two conditions, both `StringEquals`:

```
"kms:ViaService"                   = "s3.us-east-1.amazonaws.com"
"kms:EncryptionContext:aws:s3:arn" = aws_s3_bucket.transcripts.arn
```

The bucket ARN is the Terraform reference, never a typed string. There is no per-prefix value at the key and no `kms:Encrypt`.

### Evidence for the two rulings

- Bucket Key is on: `bucket_key_enabled = true` at `infra/aws/terraform/transcripts/main.tf:157` (line 138 in `box/laptop` @8837887671, which the issuer cited as 137; 147 at this branch's HEAD before this pass and 157 after it: the lines above it are the key-policy and comment lines the amendment-26 pass and this pass added). With a Bucket Key the encryption context S3 sends is the bucket ARN, so a per-prefix condition would refuse every write. The prefix boundary is the S3 identity leg, unchanged. The live `get-bucket-encryption` was NOT re-read by this pass: the Terraform text is the evidence, and the issuer's ruling cites the same line.
- No `kms:Encrypt`: the evidence is dell2's measurement, quoted in the issuer's ruling (relay msg 107740): the a17/b17 code makes no direct KMS Encrypt call, the only KMS calls are `describe_key` (`pull.py:215`, `silver.py:277`, `gold.py:303`), and the writes are SSE-KMS PutObject, which needs `GenerateDataKey`. That code is not in this sparse worktree, so this pass did NOT re-read it: the claim is HELD (the issuer's), not measured here. Measured here: `kms:Encrypt` reads `implicitDeny` for both Dells in the check.
- The Dells already hold `kms:DescribeKey` (`DellAgentUsersDecryptOnly`), so the three `describe_key` calls need nothing added.

### The check (`tests/check_transcripts_dell_decrypt.py`)

For each user, the simulator takes `ContextEntries` for the S3 context. In scope: `s3:PutObject` under `teams/transcripts/silver/research_meeting/` (identity leg) allowed, and `kms:GenerateDataKey` with `kms:ViaService` and the bucket ARN (key leg) allowed, so the composed SSE-KMS write is allowed. Out of scope, each refused at the key: `kms:GenerateDataKey` with ANOTHER bucket's ARN as context (the registry's first other bucket), and with NO `kms:ViaService`. Both users print both legs; the last line is unchanged in shape, and `dellN_generate_ok` means allowed in scope AND refused out of scope. The check also asserts the rendered statement's Condition equals exactly the two values above.

LAST line: `TRANSCRIPTS-DELL-DECRYPT dell_decrypt=2/2 dell_write_refused=6/10 dell2_generate_ok=True dell1_generate_ok=True reader_unchanged=True unlisted_refused=True statements_added=1 ok=True`. Arms moved against the pre-amendment-25 state, unchanged since amendment 26: `kms:GenerateDataKey` implicitDeny -> allowed for each Dell (so 6/10 refused, 8/10 before). `kms:Encrypt`, `ReEncryptFrom`, `ScheduleKeyDeletion` stay refused for both; `PutKeyPolicy` stays allowed by design. The reader's statement is byte identical.

### Expected plan, by reading

Transcripts root `infra/aws/terraform/transcripts/` (the live key policy equals the render of `5c1d0af92c`, three statements, re-read this run: `live ... equals the before25 render: True`):

| resource address | action | what |
|---|---|---|
| `aws_kms_key.transcripts` | update in place | `policy` only: one statement appended, `DellAgentUsersGenerateDataKey`, now carrying the two `StringEquals` conditions above |

0 to add, 1 to change, 0 to destroy for this order's edit. THE ROOT STILL CARRIES ANOTHER CELL'S PENDING CHANGES (row `NFRA_CTLPLN-W14-S46`), so the apply is TARGETED. Target address: `-target=aws_kms_key.transcripts`. A targeted plan also walks the target's dependencies: `aws_s3_bucket.transcripts` (new: the key policy now references its ARN) and `data.aws_caller_identity.current`, which by reading show no change (the bucket block is untouched by this pass); the applier confirms that in the plan. Reference cycle: none (the bucket does not reference the key; the SSE configuration and the bucket policy reference both). `terraform fmt -check` rc=0 on both roots; `terraform init -backend=false` plus `terraform validate` ok on a scratch copy of the whole root outside the tracked tree (inputs stubbed as in the amendment-26 pass: the three NAMES.json files and runner_config.json from HEAD, placeholder lambda zips): `Success! The configuration is valid.`

### Not done

The apply; a plan against the backend; a real PutObject or GenerateDataKey; the live bucket encryption configuration read; the a17/b17 code re-read.
