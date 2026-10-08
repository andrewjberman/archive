# PLAN NOTE -- three Dell limits lifted in ONE plan: secrets, the resource-policy Deny, self-simulate (NFRA_CTLPLN.TO-CT-a-1, amendment 9)

Author: 0.9.0_WK_NFRA_CTLPLN~14. Supersedes the amendment-8 version of this note. NOTHING WAS APPLIED, NO PLAN WAS RUN AGAINST THE BACKEND, NO IAM WRITE WAS MADE. NO SECRET VALUE WAS READ: this pass made no Secrets Manager call at all; the classification works from the saved listing (`tests/vendor_secrets_census.json`, taken 2026-10-07T21:00:45Z with `list-secrets`: names, descriptions, tags, key ids, dates) and from the code that uses each secret. Authority: Andrew-direct ~00:4xZ "lets start with lifting 1 2 3 6" (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_004xZ_LIFT_FOUR_DELL_LIMITS_SECRETS_FIRM_DATA_RESOURCE_POLICIES_PUSH.md`) and `1.0.0_SA_CTO` msg 106669.

## What the ONE apply would show -- by reading the configuration, NOT from a plan

Read from the configuration and the diff of this commit; no `terraform plan` was run. Relative to the state the previous pass left (the root as of its amendment 8):

| change | resource | action |
|---|---|---|
| A secrets | `aws_iam_policy.dell_agent_vendor_secrets[0]` (`cloudops-dell-agent-vendor-secrets-policy`, 66 exact secret ARNs, 5968 characters of 6,144) | created |
| A secrets | `aws_iam_group_policy_attachment.dell_agent_vendor_secrets[0]` to `cloudops-dell-agents-group` | created |
| B resource-policy Deny | `aws_iam_policy.dell_agent_respol` (`cloudops-dell-agent-respol-policy`) | destroyed |
| B resource-policy Deny | `aws_iam_group_policy_attachment.dell_agent_respol` | destroyed |
| C self-simulate | `aws_iam_policy.dell_agent_create` (`cloudops-dell-agent-create-policy`): one statement `SimulateOwnPolicyOnly` added to its document | updated in place |

Expected: 2 to add, 1 to change, 2 to destroy. The group then holds five managed policies (deploy, create, routes-fn, routes-host, secrets) against the quota of ten; the split rule is not needed (one policy fits). WHAT THIS NOTE CANNOT SAY: whether the earlier, merged work of this order (the two routes Deny policies, the dell2 SSM policy and the other per-user policies) is already applied. I did not read the backend. If any of it is not applied, the plan will show those as additional creates; that is not part of this change. The simulator and the configuration are read, not planned.

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

## B. THE RESOURCE-POLICY DENY COMES OFF

Removed: `aws_iam_policy.dell_agent_respol` and its group attachment (`iam.tf`), `dell_respol_policy.json`, `tests/derive_respol_actions.py`; the resource-policy block of `tests/simulate_policy.py` is now its mirror (the `FREED` arms). Kept untouched: the routes Deny (`routes.tf`, `modules/routes_policy/`), `DenyPassRoleExceptNamed`, `DenyProtectedFunctions`, `DenyApiKeyReads`, and `tests/read_queue_attribute_writers.py` with its saved file.

What each of the 75 formerly denied actions reads for a Dell user NOW (simulation, both users identical). Nothing is asserted allowed: an action no Allow covers stays refused.

- dell1 kms:PutKeyPolicy on arn:aws:kms:us-east-1:313476888478:key/x -> implicitDeny now; with the removed Deny added back -> explicitDeny OK
- dell1 lambda:AddPermission on arn:aws:lambda:us-east-1:313476888478:function:x -> implicitDeny now; with the removed Deny added back -> explicitDeny OK
- dell1 s3:PutBucketPolicy on arn:aws:s3:::opal-x-test -> implicitDeny now; with the removed Deny added back -> explicitDeny OK
- dell1 sqs:SetQueueAttributes on arn:aws:sqs:us-east-1:313476888478:agentbus-x -> allowed now; with the removed Deny added back -> explicitDeny OK

- FREED-COUNT dell1 of 75 former actions now read: allowed=1, explicitDeny=3, implicitDeny=71
- FREED-COUNT dell2 of 75 former actions now read: allowed=1, explicitDeny=3, implicitDeny=71
- FREED-LIST dell1 allowed: sqs:SetQueueAttributes
- FREED-LIST dell1 explicitDeny: cloudtrail:DeleteResourcePolicy cloudtrail:PutResourcePolicy iam:UpdateAssumeRolePolicy
- FREED-LIST dell2 allowed: sqs:SetQueueAttributes
- FREED-LIST dell2 explicitDeny: cloudtrail:DeleteResourcePolicy cloudtrail:PutResourcePolicy iam:UpdateAssumeRolePolicy

So the Deny's removal newly lets a Dell do exactly ONE thing the Deny blocked: `sqs:SetQueueAttributes` (the create policy allows it on any queue), which can change a queue's access policy. Every other former action still reads implicitDeny (no Allow covers it: for example `s3:PutBucketPolicy`, `kms:PutKeyPolicy`, `lambda:AddPermission`, all the ses, sns, ecr, logs, ec2-sharing and secret-policy actions) or explicitDeny by another statement that stays (`iam:UpdateAssumeRolePolicy` by `DenyEveryIamWrite`; `cloudtrail:PutResourcePolicy` and `cloudtrail:DeleteResourcePolicy` by `DenyCloudTrailWrites`). This means lifting the Deny alone does not let a Dell write a bucket, key or function policy: that would need an Allow added in a later step. A Dell that changes a resource policy does so under its own box's never-widen pair; the laptop is told and steps in on an overlap.

The control on each line ("with the removed Deny added back -> explicitDeny") adds the removed statement inline to the same request, proving the arm reads the old behaviour. Routes, pass-role, protected-function and API-key arms read exactly as before: the per-arm lines of those blocks (PASSROLE 5, PROTECTED 9, ROUTES-ARM 5, APIKEY probe, ALLOWED 22, SSM-ARM 10, and the remaining DENIED arms) are identical, line for line, to the previous pass's run; the four resource-policy DENIED arms that used to read explicitDeny (s3:PutBucketPolicy, lambda:AddPermission, kms:PutKeyPolicy, secretsmanager:PutResourcePolicy) are no longer asserted (denied_ok moves from 19/19 to 15/15).

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

## What this does NOT do / limits

- Reads only: the live SSM documents were not compared; no Secrets Manager call; the backend was not read.
- The grant lets a box READ the credential. Whether a given vendor call is one Andrew allowed for a given project stays the rule seats follow. `openai-api-key` is readable now; the whitelist line that scopes it to one project is unchanged.
- The create policy still lets a Dell WRITE a secret (`PutSecretValue`): the simulation shows the same decision with and without the secrets document.
- D (dell2's SSM parameter read) is not in this pass.
