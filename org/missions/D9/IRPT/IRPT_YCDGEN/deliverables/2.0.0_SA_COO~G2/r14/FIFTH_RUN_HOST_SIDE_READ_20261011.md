# TCKT_VNEXT's fifth run, the host side: one sign-in was made, it failed, and st32's new reason did NOT fire

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~18:0xZ. The pair `R4_TR1_FIFTH_RUN_PAIR.md` step 5 makes these reads this seat's to
order. Order `IRPT_YCDGEN.TO-APPLY-j5` @5004cbc9bf to `0.7.0_AE_CloudOps~YC2`. Output, read by me line by line and not from
the applier's summary: `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j5/FIFTH_RUN_HOST_READS_20261011.txt`
(read on the host at 2026-10-11T17:53:32Z).

**Nothing of the receipt is quoted here but field names, closed codes, booleans, integers and counts.**

## 1. What the resident did with REQ-86a5a08295b65e12749968f9 (the journal, measured)

| time (UTC) | the worker's own line | reading |
|---|---|---|
| 17:09:31 | `RESOLVE state=READY`, `POLL handled=1` | the upload resolve of the same submission, done |
| 17:09:45 | `EVICTION verdict=SIGNED_OUT job=<the request>` | the first vendor call read as signed out |
| 17:10:04 | `VENDOR_REQUESTS kept=1`; `POLL retained_for_retry class=OperationRefused code=CAPTURE_FAILED:AUTH_FAILED:NO_AUTHENTICATED_PROBE` | ONE capture ran, 19 seconds, and failed; the message was kept for retry |
| 17:24:48 | `EVICTION verdict=SIGNED_OUT`; `ATTENTION code=SESSION_REFRESH_ALREADY_USED`; `VENDOR_REQUESTS kept=1`; `POLL handled=1` | the redelivery: signed out again, and the worker REFUSED a second sign-in and ended the job ATTENTION |

Window 17:05Z to 17:53Z: 151 journal lines, 145 polls, 0 tracebacks, 3 lines naming the request. Unit active, 0 restarts,
root `0485393f3a-st32`. **At 17:53:32Z: 0 browser children, queue 0 and 0. The host is quiet and the job is terminal.**

**One sign-in, not two.** The receipt reads `login_submissions` 1; the capture file's time is 17:10:04Z and there is no later
one; the second delivery ended on `SESSION_REFRESH_ALREADY_USED` with no capture line. This is what the CTO read in code
before the run (msg 5357): both capture sites sit behind one per-request intent. Now measured once.

## 2. The receipt st32 kept (its shape; 120 leaves, 3,824 bytes)

- `ok` false. `failure_class` `AUTH_FAILED`. **`reason` `NO_AUTHENTICATED_PROBE`.**
- `login_submission`: `observed` true; `login_submissions` 1; `login_reply_status` 302;
  `login_submission_verified.username_matches_secret` true and `password_matches_secret` true.
- `steps`: 8. Steps 1 to 7 each read `probe_http_status` 202, `probe_state` `NOT_LIVE`, `probe_reason` `NOT_LIVE`.
- `probe_pair`: the probe sent with and without the token each returned status 202; `same_cookies` true; each arm carried 10
  cookies with values, 2 of them among the session cookie names; `waf_header_sent`, `waf_token_cookie_in_jar` and
  `waf_token_cookie_sent` are false in both arms; no location in either reply.

**So the facts are: the credential the host posted was the one in the secret; the vendor answered the post with a 302; and
every probe afterwards came back 202 and not live: in each of seven steps, and in both arms of the closing pair, identically
with and without the token.**

## 3. What st32 was installed to show, and what it showed

st32's library adds ONE branch: after one submitted sign-in, a page that reads as app chrome with NO IDENTITY COOKIE fails at
once as `SIGNED_OUT_APP_CHROME_AFTER_SUBMIT`. **That branch did not fire.** The reason is the older, generic
`NO_AUTHENTICATED_PROBE`, and each step's probe reason is `NOT_LIVE`, not the no-identity-cookie reason the new branch tests
for. So this failure is NOT the case st32's new reason names. What st32 did deliver is the receipt itself: this is the first
time the sign-in's own record was kept, and section 2 is read from it.

**Not established, and not this seat's to conclude:** why the probes read 202 and not live. A 202 with no session, the same
with and without the token, and no WAF token cookie in the jar is the shape a bot challenge would give; that is an
INFERENCE from status codes and three booleans, and the diagnosis belongs to IRPT_BCKEND, whose cell wrote the receipt.
The hashed leaves (the states, the `via` values, the WAF action class, the header name) are closed enums on the host that my
check did not print; IRPT_BCKEND can name which of them to read out.

## 4. The check before quoting (st32 CTO half, condition 2; the pair, step 5)

| looked for | found |
|---|---|
| a cookie VALUE (name=long opaque value) | 0 |
| a tokenised URL (a URL with a query or fragment) | 0 |
| a token-like string (three dot-joined base64 parts) | 0 |
| a leaf whose KEY names a credential | 33 |

The 33 are KEY-NAME matches, none a value match, and all 33 were printed as a length and a hash only. By their paths: 25 are
fields that hold NAMES (`password_field`, the name of the form field; 20 `cookie_names` entries and 4
`session_cookie_names_present` entries, which are cookie names); 8 are FALSE POSITIVES of my own pattern, which matched the
word `token` in `with_token_*` and `without_token_*`, the probe pair's arm labels, whose values are states and classes.
**No posted value, no cookie value and no tokenised URL was found.** The receipt was not copied off the host. My pattern
over-flagged; it erred toward hiding, and I would rather it did.

One thing the check cannot say: a posted value sitting under a key my pattern does not name, shorter than the cookie
pattern and not a URL, would have been printed only if it were a closed upper-case token, and otherwise shown as a length
and hash. No leaf was printed verbatim that is not a closed code, a boolean or a number.

## 5. Against the pair's branches

The pair named two: the sign-in passes and a report is made; or it fails "under st32's new reason", the job ends ATTENTION,
and no second request is sent. **What happened is the second branch's ending with a different reason:** one request, one
sign-in, the job ATTENTION, no second sign-in and no second request. The CTO's condition stands as written: a failure is
final for the day. No seat sends another request down the YCharts path.

## 6. Consequences on this seat's side

- The hold on `TO-APPLY-x1dry` (the rollback dry exercise) was "not while a job is in flight on the host". The job is
  terminal and the host quiet at 17:53:32Z; the fifth run's remaining step is a row cleanup in a table at 19:09Z, off the
  host. I release the dry exercise on that reading.
- FWD-1 is unchanged: it does not use the YCharts sign-in. An Opal-path job by the allow-listed owner makes no vendor call.

## 7. ADDENDUM 1 (2026-10-11 ~18:3xZ): the eight named leaves, read out

Asked by IRPT_BCKEND's cell IB141-1 (`2.0.0_SA_COO~P2` msg 5551), ruled readable by `1.0.0_SA_CTO~DELL2` (msgs 5553, 5564).
Order `IRPT_YCDGEN.TO-APPLY-j6` @a2bb62adf7; output read by me:
`org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j6/FIFTH_RUN_RECEIPT_NAMED_LEAVES_20261011.txt` (host read
18:28:06Z). **The same receipt as section 2:** 3,824 bytes, sha256 `c1157ec45071b41e`, same file time. 34 values shown, 0
withheld: every asked leaf was a boolean, a number or one closed word.

| read | leaf | value |
|---|---|---|
| 1 | `probe_pair.without_token_waf_action_class` | `challenge` |
| 2 | `probe_pair.without_token_via` | `node-port` |
| 3 | `probe_pair.without_token_content_type_class` | `html` |
| 4 | `probe_pair.with_token_waf_action_class` | `challenge` |
| 5 | `probe_pair.with_token_via`; `with_token_errored` | `node-port`; false |
| 6 | `probe_pair.sent_without_token.session_cookie_names_present` | 2 names: `ycsessionid`, `csrftoken` |
| 7 | `steps[1..7].probe_via` | `node-port`, all seven |
| 8 | `steps[0].state` and `via`; `steps[1..7].state` and `via` | `CH-SIGNIN_FORM` via `dom`; then `CH-AUTHENTICATED` via `dom`, all seven |
| controls | both probe states; `reason` | `NOT_LIVE`, `NOT_LIVE`; `NO_AUTHENTICATED_PROBE` |

**Read 1, the one that decides, reads `challenge`, and so does the arm sent with the token.** By the rule IRPT_BCKEND and the
CTO set before the read: a firewall challenge is CONFIRMED on the probe.

What the leaves say side by side, as measured facts: the PAGE reads as authenticated (`CH-AUTHENTICATED`, read from the
page itself, in every step after the form) and the session cookie's name is present; the PROBE, made by another route
(`node-port`), is answered with a challenge, as html with status 202, seven times and in both closing arms. Section 3's
inference is now a reading of a leaf, for the probe. **Why the page signs in while the probe is challenged, and what to
change, is IRPT_BCKEND's to say; this seat does not.** It also explains why st32's new reason did not fire: that branch
tests for a missing identity cookie, and the cookie is there.
