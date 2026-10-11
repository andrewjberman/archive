# IB-pr-444 -- the fifth run's receipt: what the persisted leaves can say about "accepted, then challenged"

By 0.9.0_WK_IRPT_BCKEND~302, 2026-10-11. A code and record read: no vendor request, no sign-in, no host command, no AWS call.
Detail: `IB141-1_receipt_diagnosis.json` (same folder).

## Verdict: UNDECIDED (claim: inferred)

- **Accepted half: measured.** Every step's `probe_reason` is NOT_LIVE. In `ycharts_session.js` `probeSession`, a browser context
  returns NO_IDENTITY_COOKIE (:810-813) if `ycsessionid` is absent and IDENTITY_<refusal> (:848-856) unless the loaded
  dashboard document shows a signed-in user. NOT_LIVE is written at :915 from `classifyResponse` (:594) only after both passed.
  So the browser held the identity cookie and the dashboard page showed a signed-in user. A rejected or locked credential, and a
  redirect to a page that sets no session, are contradicted (if the deployed library equals this tree).
- **Challenge half: not settled.** A 202 is the status AWS WAF's Challenge answers with, but the app also answers 202 for pending
  work. The leaf that separates them, `probe_pair.without_token_waf_action_class`, is persisted but was printed only as a hash.

## What a 202 and NOT_LIVE are in the capture

`classifyResponse` (:584-595) knows 200, 201, 403 and 403 + "concurrent sign in"; every other status, 202 included, is NOT_LIVE
("probe HTTP 202"). The waf-action header and content type are copied into evidence (:904-908, :928); the body is never searched.
The probe has NO challenge test. The READ path has one (`session/controller.py:35-37`, `generate/transport.py:188-191`,
`resident_worker.py:233-244`): the waf-action header in challenge/captcha/block, then a 202/403/405 body holding "awswaf". Two
different tests; the header half can be applied to the receipt after the fact, the body half cannot (the body is not kept).

## Why the new reason did not fire

Condition (:1084): not authenticated AND reason == NO_IDENTITY_COOKIE AND a sign-in was submitted AND screen not "post-submit".
This run met the second-to-last parts and NOT the reason: it carried NOT_LIVE, reachable only after the identity cookie existed.
The branch's premise (no identity cookie after the submission) was false, so the loop ran the 8 steps to NO_AUTHENTICATED_PROBE
(:1188-1189). Given the hypothesis a sibling is needed: submitted, identity cookie and document identity present, reply read
as a firewall challenge by the read path's test; fail at once under its own code. Built: nothing.

## Deciding leaves (in order)

| leaf (persisted path) | confirms | kills | persisted |
|---|---|---|---|
| probe_pair.without_token_waf_action_class | challenge, captcha | allow, count | yes |
| steps[1..7].probe_reason (already read: NOT_LIVE) | NOT_LIVE and kin (accepted half) | NO_IDENTITY_COOKIE, IDENTITY_* | yes |
| probe_pair.without_token_content_type_class (weak, when the first is null) | html | json | yes |
| probe_pair.without_token_body_awswaf_marker (no such member) | true | - | NO |

## Not excluded

The app's own 202; a header-less interstitial (invisible to the kept leaves); a context fallback that returned no headers (read
`without_token_via`); a probe path overridden on the host (`probe_url_path` is not kept); the browser never earning an
aws-waf-token (the pair cannot tell: both arms are the same token-less request).

## Reads to ask the host reader (existing file, no new run)

1 `probe_pair.without_token_waf_action_class`; 2 `probe_pair.without_token_via`; 3 `probe_pair.without_token_content_type_class`;
4 `probe_pair.with_token_waf_action_class`; 5 `probe_pair.with_token_via` and `with_token_errored`;
6 `probe_pair.sent_without_token.session_cookie_names_present`; 7 `steps[1..7].probe_via`; 8 `steps[0..7].state` and `.via`.
