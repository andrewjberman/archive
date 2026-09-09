# SMS Toll-Free Number + Carrier Verification -- PROGRAMMATIC REQUEST DRAFT (NOT SUBMITTED)

**Author:** 0.0.0_AB_MSTR | **Date:** 2026-09-09 | **Status:** AT ANDREW'S GATE. DO NOT SUBMIT WITHOUT HIS WORD.
**Authorization so far:** Andrew-direct 2026-09-09 ~13:0xZ at the MSTR terminal, VERBATIM: *"We should be able to issue
the request programmatically as we did for the SES"* -- said after this seat reported the account still in the SMS
sandbox with no application on file. Read as: prepare the programmatic filing on the SES pattern (draft -> his approval
-> submit). The SES precedent: draft @756447f14, Andrew approved (COO relay 2026-07-09, msg to 0.7.0_AE_CloudOps~A),
filed with `sesv2 put-account-details`, GRANTED case 178727932800843.
**Account:** 313476888478, us-east-1 (`sts get-caller-identity` 2026-09-09 12:46Z, user Andrew_Berman).

---

## 1. What was MEASURED before writing (2026-09-09 12:46-13:30Z)

| surface | read | value |
|---|---|---|
| SNS SMS sandbox, 5 regions | `sns get-sms-sandbox-account-status` | IsInSandbox=true in us-east-1/2, us-west-1/2, eu-west-1 |
| End User Messaging tier | `pinpoint-sms-voice-v2 describe-account-attributes` | ACCOUNT_TIER=SANDBOX |
| spend limits | `describe-spend-limits` | every limb EnforcedLimit=1 MaxLimit=1 (sandbox default) |
| phone numbers / registrations / sender IDs | `describe-phone-numbers` etc. | 0 / 0 / 0 |
| verified destinations | `describe-verified-destination-numbers` | +1 786-261-7679 PENDING since 2026-06-25 (OTP never confirmed) |
| CloudTrail since 2026-06-11 (the 90-day floor) | EventName lookups | 0 CreateCase, 0 RequestPhoneNumber, 0 CreateRegistration, 0 RequestServiceQuotaIncrease |
| Support Center | console visit 2026-08-20 22:30 ET (Andrew_Berman_Console) | create-case form loaded (GetAttachmentUploadLinks), no CreateCase followed |
| Service Quotas, sms-voice | `list-service-quotas` | L-2325465C TextMessageMonthlySpend value=1.0 **adjustable=true** |
| Support API | `support describe-cases` | SubscriptionRequiredException (Basic plan) -- cases not listable by API |

**Conclusion:** nothing was ever filed. There is nothing pending at AWS to be approved.

---

## 2. The programmatic path (three acts, all API-driven; none needs the Support API)

The auth-handler sends through `@aws-sdk/client-pinpoint-sms-voice-v2` (`sms.ts:18`), so End User Messaging is the
plane that matters. SNS's own sandbox flag is a separate, console-only case and is NOT needed for this sender.

| act | command | effect | reversible? |
|---|---|---|---|
| **A. provision the toll-free number** | `pinpoint-sms-voice-v2 request-phone-number --iso-country-code US --message-type TRANSACTIONAL --number-capabilities SMS --number-type TOLL_FREE` | a TFN in this account within seconds; ~USD 2/month | yes, `release-phone-number` |
| **B. file the toll-free verification** | `create-registration --registration-type US_TOLL_FREE_REGISTRATION` -> `put-registration-field-value` x18 -> `create-registration-attachment` (opt-in image) -> `create-registration-association` (the TFN; ASSOCIATE_BEFORE_SUBMIT) -> `submit-registration-version` | carrier review, typically 1-3 weeks; unverified TFNs are blocked by US carriers | the version can be discarded before submit; after submit it is a filed representation |
| **C. leave the sandbox / raise the spend limit** | `service-quotas request-service-quota-increase --service-code sms-voice --quota-code L-2325465C --desired-value <N>` | AWS reviews; approval moves the account to production tier and lifts the USD 1 cap | a request can be closed; an approval is the account-level event the D12 watch item warns about |

Order: A, then B (B needs A's number to associate), then C. C is the act `sms.ts:38-44` calls out: the day it lands, the
sandbox's verified-destination guard is gone and only `SMS_VERIFIED_DESTINATIONS` in the code stands. The D12 watch item
(`org/critical_paths/.open_deploys/d12-sms-origination-identity-activation.json`, SP-3) already requires a reviewed
commit of that allowlist before/when this happens.

---

## 3. THE DRAFT FORM (US_TOLL_FREE_REGISTRATION field values, exactly as they would be PUT)

Field catalogue read live from `describe-registration-field-definitions` 2026-09-09. Values marked **[ANDREW]** are
representations only he can make and are NOT in the repo; everything else is sourced and cited.

### companyInfo
| field | value | source |
|---|---|---|
| companyName | `Opal Capital Management` **[ANDREW: exact legal name incl. LLC/Inc suffix]** | SES filing `put-account-details` (live `get-account`), deck templates |
| businessType | `PRIVATE_PROFIT` | registered investment adviser, privately held |
| taxId / taxIdAuthority / taxIdCountry | **[ANDREW: EIN]** / `EIN` / `US` | CONDITIONAL, but carriers verify a for-profit against it; omitting it invites a rejection round |
| website | `https://opalinvest.com` | SES filing WebsiteURL |
| address1 | `1825 NW Corporate Blvd` | Andrew-direct 2026-09-09 ~13:4xZ at this terminal, VERBATIM: *"no the opal address is 1825 NW Corporate Blvd, Boca Raton, FL 33432"* (corrects the Brickell address the deck index carries at `slide_index.json:20794`) |
| city / state / zipCode / isoCountryCode | `Boca Raton` / `FL` / `33432` / `US` | same |

### contactInfo
| field | value | source |
|---|---|---|
| firstName / lastName | `Andrew` / `Berman` | account owner |
| supportEmail | `andrew@opalinvest.com` | SES filing AdditionalContactEmailAddresses (same domain as website, as the field requires) |
| supportPhoneNumber | **[ANDREW: the number; +1 786-261-7679 is the one already on the sandbox list]** | |

### messagingUseCase
| field | value |
|---|---|
| monthlyMessageVolume | `1,000` (opal-users-v2 holds 48 accounts; login + enrolment codes; a `100` pick would be exceeded by a 30-user month) |
| useCaseCategory | `ONE_TIME_PASSCODES` |
| useCaseDetails (<=500) | see 3a |
| optInType | `DIGITAL_FORM` |
| optInDescription (<=1500) | see 3b |
| optInImage (ATTACHMENT, REQUIRED) | `SMS_OPTIN_FLOW_MOCKUP_20260909.png` (this folder) -- a mock-up of the in-app flow, which sits behind login; AWS's field text accepts a mock-up for a flow that "requires a log-in" |

**3a. useCaseDetails (as it would be filed):**
> Opal Capital Management operates a private client portal (Opal Invest, https://opalinvest.dev) for its advisory
> clients and partner-firm staff. This toll-free number sends one-time login verification codes (multi-factor
> authentication) to users who have chosen text message as their MFA channel and have verified ownership of their
> phone number inside the portal. Every message is triggered by that user's own login or enrolment action. No
> marketing, no promotional content, no recurring messages, no third-party traffic.

**3b. optInDescription (as it would be filed):**
> Opt-in happens inside the authenticated Opal Invest portal, after the user has signed in with their password. The
> user opens the "Text-message login codes" enrolment card, enters their mobile number, and is shown consent text
> stating that Opal Invest will send one-time login codes to that number, that message and data rates may apply,
> that message frequency depends on how often they sign in, and that they can reply STOP to opt out or HELP for help.
> The user taps "Send code"; a verification code is texted to the number; the number is stored against the account
> ONLY after the user enters that code correctly. Users can switch their MFA channel back to email at any time in the
> same settings surface, which stops all texts. Numbers are never imported, purchased, or added by staff; a number
> the user has not verified is never texted.

### messageSamples
| field | value | source |
|---|---|---|
| messageSample1 | `482913 is your Opal Invest login code. It expires in 30 minutes. Do not share it.` | `sms.ts:126` template; TTL `mfa.ts:69` CHALLENGE_TTL_SEC=1800 |
| messageSample2 | (none -- ONE body exists) | the enrolment send (SB-7, `auth.ts:791` and `:834`) calls the same `sendMfaCodeSms`, so the enrolment text is byte-identical to sample 1. Filing a second, different sample would describe a message the code does not send. |

---

## 4. What the fabric must line up BEFORE submit (not after)

1. **The shipped enrolment copy must say what 3b says.** SF-2 (`0.4.0_DE_ClientPlatform~Z`, site Z) is BUILDING the
   enrolment card; its consent text is not in this checkout. Carrier reviewers compare the description to the flow.
   Route: one line to the D12 owner on site Z with 3b attached, before submit.
2. **SB-7's enrolment message body is the login-code body** (measured, above). If the fabric wants the enrolment
   text to say "verification code" and carry STOP/HELP, that is a code change to `sms.ts` BEFORE filing, and the
   sample here changes with it; otherwise file one sample.
3. **Terraform, not the console, sets `SMS_ORIGINATION_IDENTITY`** (SP-2, on Andrew's GO after the TFN is verified);
   `sms-iam.tf`'s `sms-voice:SendTextMessage` grant is scoped to the TFN ARN act A returns.

## 5. Open at Andrew (blocking submission)
- exact legal name; EIN; contact phone (address CONFIRMED by Andrew 2026-09-09: 1825 NW Corporate Blvd, Boca Raton, FL 33432)
- the word to run A, then B, then C -- or A+B only, holding C (the sandbox exit) for a later word
