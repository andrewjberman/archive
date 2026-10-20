# FU-x-1 -- the stored Wealthscape credential is wrapped in angle brackets (structure only, no value)

**Issuer:** 2.0.0_SA_COO~P1, 2026-10-20 ~16:00Z.

**What the live trace showed** (SSM command af37ba6f, `FU-x-1_attempt5_trace_login.txt`): after the Next click the site's own
`POST /auth/api/redirect-info` answers 400 with body `{message: "Validation Failure", code: "0102"}`. Its request body is one key,
`userId`, non-empty, length class 9-32. Everything else the page does succeeds (document 200, cookie calls 200).

**What a structure-only read of the secret showed, run ON the box under the box role (SSM command, only booleans and counts printed;
the value never left the box and was never printed):** the secret `fidelity/alongside/wealthscape-credentials` is JSON with the keys
`username` and `password`, both present. `username` is 12 characters: 10 digits and exactly 2 other characters, which are `<` and `>`;
no letters, no whitespace, no non-ASCII. `password` is present and starts with `<` and ends with `>`.

**Reading:** both values were stored wrapped in literal angle brackets (a template-placeholder paste). The site validates the user id
and rejects it as a validation failure. The digits inside look like a real 10-digit identifier; I did not and will not print them.

**Not done, deliberately:** no code strips the brackets. The password cannot be tested without a real sign-in attempt, and a wrong
password counts toward a lockout; the clean fix is for the secret to hold the plain values.

**The act:** only Andrew writes the value: rewrite `fidelity/alongside/wealthscape-credentials` as JSON `{"username":"<plain>","password":"<plain>"}` with NO angle brackets.
