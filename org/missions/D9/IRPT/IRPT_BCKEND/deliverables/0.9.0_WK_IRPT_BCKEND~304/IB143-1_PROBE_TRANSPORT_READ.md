# IB143-1 -- What "node-port" is, why the probe uses it, what a job's calls would meet, and what changed on our side

By 0.9.0_WK_IRPT_BCKEND~304, 2026-10-11, on order IRPT_BCKEND.TO-IB-pr-446. A code and record read: no request to the vendor, no
sign-in, no host command, no AWS call. Nothing here proposes a change to how the vendor is reached; that question is not an
engineering call and is being put to Andrew. Every statement carries a claim word: measured (read from a line or a record),
inferred (reasoned from what was read), held (taken from a record without re-reading its source), absent (no record says).
Detail and line numbers: `IB143-1_probe_transport_read.json` (same folder).

## 1. What "node-port" is

- node-port is the capture library's own plain HTTP client, Node's built-in `https` module, not the browser. It lives in
  `ycharts_session.js` (:645-669) and runs inside the same Node process that drives the browser. Claim: measured.
- It makes one GET per call. It sends the library's fixed browser-like user agent, a Cookie header copied once from the browser
  context's jar, and three request headers (Accept, X-Requested-With, Referer). Claim: measured (:302-344, :833).
- The jar copy leaves out the firewall's token cookie by default (`aws-waf-token`, :311-312). The token and a matching header are
  added only in the second ("with token") arm, and only if the browser's jar holds a token. Claim: measured.
- In the fifth run the browser's jar held no token, so the "with token" arm sent exactly what the "without token" arm sent.
  Both were answered 202 with the firewall class `challenge`. Claim: measured (the receipt, read out on the host).
- The library has other ways to make a request or read identity: Playwright's request context (the fallback, used only if
  node-port throws or returns no status), the browser's own page loads, a read of the loaded page, and a read of the stored
  bundle. An in-page fetch existed once and is retired. All nine are listed with their lines in the JSON. Claim: measured.
- Every probe in the fifth run went by node-port, so the fallback was never used. Claim: measured.

## 2. Why the probe uses it and not the page

- The code states the reason. At :291-297 it says the node client is "the resident's own client class", that the browser's
  in-page fetch "is the class the WAF challenges for a non-navigation request", and that it "is NOT the class the resident ... is".
  So the probe goes through node-port to imitate what the later replay will do. Claim: measured (quoted from the code).
- The project's rule is that a session counts only after it is verified "from the transport that will use it" (PRD, FWD-4). The
  intent to use a stand-in for that transport is stated in the code. Claim: measured.
- The stand-in is not the same program. The replay client is Python `urllib` (`transport.py`:468-494); the probe is Node `https`.
  They differ at least in the Referer value and in how cookies are chosen. Claim: measured for those differences.
- Whether the vendor sees the two as alike on the wire has no record. Claim: absent.
- The replay's own client is checked separately after a capture (`broker.verify`). The fifth run never reached that step because
  the Node probe failed first. Claim: measured.

## 3. What a job's calls after a capture would meet

- A generation makes 12 vendor calls by the code: 10 by Python `urllib` with the stored cookies, 2 by Python `urllib` with no
  cookies (the PDF download and the ticker lookup). None is made by node-port or by the browser. Claim: measured.
- The first of them, the template read, is on the same route the probe reads. Claim: measured.
- Would they meet the same refusal? It cannot be told from code and records. Claim: absent.
- What the records do show: the Python path has been answered with a 202 carrying a firewall action before (three research runs
  on 2026-10-04 and 2026-10-05, each at its 7th call, and 14 journal lines `READ_BACK_PENDING:WAF_CHALLENGE` on five days from
  2026-09-29 to 2026-10-05). Claim: measured. On 2026-10-03 the resident runtime read the template route with 200 on a session
  seeded from a person's browser. Claim: measured.
- What the journal lines do not show: a challenge on the template route, on a write, or on any day after 2026-10-05; jobs reached
  READY on the same days (an undivided count), so the session was apparently usable then (inferred). No automated sign-in has succeeded since, so no record shows the Python path with a session issued
  after 2026-10-05. Claim: absent.

## 4. What changed on our side, and what the host runs

- Command: `git log --since=2026-10-04 --format='%h %ad %an %s' --date=iso-strict -- infra/aws/ec2/investor-reporting-ycharts/
  infra/aws/lambda/investor-reporting/ycharts/`. 72 commits. Claim: measured.
- The probe, its transport, its headers and its classification of a reply are byte-identical from 2026-09-24 to now (nine code
  segments hashed at six revisions). Claim: measured.
- The only change to the capture is commit 5d2b94f71d (2026-10-11): one new failure branch after the probe, and a kept receipt.
  It reached the host on 2026-10-11 at 16:09Z (release st32). Its branch did not fire in the fifth run. Claim: measured.
- The Python client that sends and classifies replies (`transport.py`, `controller.py`, `broker.py`) was not changed in the
  window. Claim: measured.
- The host's capture library was the same file (hash 857d90b8) from before 2026-10-03 until 2026-10-11T16:09Z. The releases read
  (st22 to st24 and st26 to st31; no record of an st25 was found) reached the host between 2026-10-06 and 2026-10-11; none moved
  the library or the wrapper. st32 moved the library.
  Claim: measured from the install records.
- No release landed between the last bundle write (2026-10-05T10:04Z) and the first failure after it (14:41Z). Claim: measured for
  releases; absent for any change made by hand.
- Ours or the vendor's? The records cannot say. Our capture code stood still. What did change on our side, outside that code,
  is that the host's Python path ran research traffic on the same account from 2026-10-04T18:42Z to 2026-10-05T13:01Z. Nothing in
  the repository records the vendor's rule or a change to it. Claim: absent.

## 5. Not established

- That captures worked until 2026-10-05. The 10:04Z time is the last change of the stored session. Since 2026-10-02 the resident
  also rewrites that session whenever the vendor rotates a cookie, so the write may not be a capture. The last automated sign-in
  success in the records is 2026-10-02. The same failure code, `NO_AUTHENTICATED_PROBE`, is already in the journal on
  2026-10-03T00:31Z. Claim: absent for which kind of write it was.
- Whether any earlier probe was challenged: only the fifth run's receipt survives. Claim: absent.
- How many captures succeeded: a success writes no journal line. Claim: absent.
- The host's environment settings, the browser build, the egress address the vendor sees, any hand change on the host, and
  whether a person signed in to the shared seat around the failures. Claim: absent.
