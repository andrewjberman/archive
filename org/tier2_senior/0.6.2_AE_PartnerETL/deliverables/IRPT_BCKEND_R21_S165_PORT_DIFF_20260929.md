# IRPT_BCKEND R21 S165 -- the cot login retry port, DIFF for the issuer to read

**TO:** `IRPT_BCKEND.TO-IB-m21-212` Part 1 | **cell:** `IB-mr-212` | **row:** `IRPT_BCKEND-S165`
**Author:** `0.6.2_AE_PartnerETL~S` | **Date:** 2026-09-29 | **Issuer:** `2.0.0_SA_COO~M`
**Base:** the RUNNING bytes of `/opt/bd-cot-auto-login/bd_49f_auto_login.js` on `i-0643a5bee8a8feabf`
-- md5 `28dd27a054b826cc3a87f6b4498d3b5a`, 35,049 B, read under SSM command
`ea2016dd-1284-4a9e-9322-5497c80dd905` (Status Success) for TO-IB-m21-211.
**Ported candidate:** md5 `cd42a132606ad6cccaa7a7b756cbe89f`, 37,601 B.
**Nothing is deployed by this document.** Part 2 runs only on the issuer's written GO.

---

## 1. Where the candidate sits, and why it is not in the tree yet

Two things hold the ported `.js` out of the repo right now, and both are named rather than worked around:

1. **The naming limb refuses the path at all** -- row `IRPT_BCKEND-S198` (`@036fa7193b`). It refused the
   PRISTINE capture 15 times in ENFORCE mode; it will refuse the ported file for the same 8 hand-kept-carrier
   literals, which are inherited from the running bytes and not introduced here.
2. **`IBM21-211-AC1` md5s the WORKING file.** `r21_s166_build_input.py` reads
   `infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js` off disk and requires md5 `28dd27a0` / 35,049 B.
   The moment this port lands at that path, TO-IB-m21-211's criterion reads `NO-BUILD-INPUT` and FAILS.
   The two orders cannot both be true of the same working file at the same time. **This is the issuer's
   sequencing call, not something this seat resolved**: either 211 is graded (and the build input committed)
   before the port lands, or AC1 is re-pointed at the committed blob rather than the working file.

So the repo path still holds the pristine 28dd27a0 bytes (AC1 re-verified `BUILD-INPUT 28dd27a054b8` rc=0
after the port was lifted out), and the candidate is held outside the tree until the GO.

## 2. The diff, against 28dd27a0

```diff
--- a/bd_49f_auto_login.js (RUNNING 28dd27a0)
+++ b/bd_49f_auto_login.js (retry port)
@@ -232,6 +232,41 @@
   try { creds = JSON.parse(smGet(credsId)); kimiKey = smGet(kimiId); }
   catch (e) { log(`ERROR: secret load failed (${String(e).split('\n')[0]})`); process.exit(2); }
   if (!creds.username || !creds.password) { log('ERROR: credentials secret missing username/password'); process.exit(2); }
+
+  // CTO-B OUTER RETRY, ported from the 49F canonical (TO-IB-m21-212, row IRPT_BCKEND-S165). One transient
+  // login failure used to cost a whole day: the cot chain stayed frozen 09-24..09-27 on four consecutive
+  // single-attempt failures. Each attempt is a FRESH browser context + a FRESH loginStart anchor (so
+  // getOtpCode fetches THAT attempt's own code, never the consumed prior one) + reset otpSent/otpEntered --
+  // all of which already live in the block below, which is why moving it behind a function boundary is the
+  // whole mechanism. Bounded by BD_MAX_LOGIN_ATTEMPTS (cot secret-ids.env sets 3) with exponential backoff
+  // from BD_LOGIN_BACKOFF_MS (cot sets 5000) = the retry-storm guard: a genuinely dead session must not
+  // hammer BD login. On cap exhaustion rc is the SAME terminal state as before -- .bd.identity NOT advanced,
+  // so the existing freshness path still fires. Firm-sep UNAFFECTED: control flow only, no secret-id or
+  // path change. With BD_MAX_LOGIN_ATTEMPTS=1 the behaviour is byte-for-byte today's single attempt.
+  const MAX_LOGIN_ATTEMPTS = parseInt(process.env.BD_MAX_LOGIN_ATTEMPTS || '3', 10);
+  const BASE_BACKOFF_MS = parseInt(process.env.BD_LOGIN_BACKOFF_MS || '5000', 10);
+  let rc = 1;
+  for (let attempt = 1; attempt <= MAX_LOGIN_ATTEMPTS; attempt++) {
+    log(`login attempt ${attempt}/${MAX_LOGIN_ATTEMPTS}`);
+    rc = await attemptLogin(firm, creds, kimiKey, sessionId);
+    if (rc === 0) { if (attempt > 1) log(`login RECOVERED in-run on attempt ${attempt}`); break; }
+    if (attempt < MAX_LOGIN_ATTEMPTS) {
+      const backoffMs = BASE_BACKOFF_MS * Math.pow(2, attempt - 1);
+      log(`login attempt ${attempt} failed rc=${rc} -> backoff ${backoffMs}ms then retry with a FRESH OTP + browser context`);
+      await new Promise((res) => setTimeout(res, backoffMs));
+    } else {
+      log(`login EXHAUSTED ${MAX_LOGIN_ATTEMPTS} attempts -> rc=${rc} LOUD terminal (.bd.identity NOT advanced)`);
+    }
+  }
+  process.exit(rc);
+}
+
+// ONE login attempt: fresh browser context, fresh OTP window, perceive-act loop, capture-on-success.
+// Returns rc (0 = .bd.identity captured + fresh session written to SM; nonzero = failed, NOTHING written
+// -- preserves the "session advanced ONLY on rc==0" invariant per attempt). The per-attempt state
+// (launch/browser/ctx/page/loginStart/otpSent/otpEntered/rc) lives HERE so every attempt is genuinely
+// fresh: a retry re-using a stale loginStart would re-fetch the consumed code and be a no-op.
+async function attemptLogin(firm, creds, kimiKey, sessionId) {
 
   const launch = { headless: process.env.BD_HEADLESS !== '0', timeout: 60000, args: ['--no-sandbox', '--disable-dev-shm-usage'] };
   if (process.env.BD_PROXY_SECRET_ID) {  // resi proxy from SM (ALWAYS-ON for BD). Secret = JSON {host,port,username,password,country?}
@@ -450,7 +485,7 @@
   } finally {
     await browser.close().catch(() => {});
   }
-  process.exit(rc);
+  return rc;
 }
 main();
 
```

## 3. One line per hunk

| # | Hunk | What it does | Why |
|---|------|--------------|-----|
| 1 | `@@ -232,6 +232,41 @@` | After the credentials guard, closes `main()` on a bounded retry loop (`BD_MAX_LOGIN_ATTEMPTS`, default 3; exponential backoff from `BD_LOGIN_BACKOFF_MS`, default 5000) and re-opens the rest of the old `main()` body as `async function attemptLogin(firm, creds, kimiKey, sessionId)`. | This is the whole mechanism. Every piece of per-attempt state the retry must refresh -- `launch`/`browser`/`ctx`/`page`, `loginStart` (the OTP time-window anchor), `otpSent`, `otpEntered`, `rc` -- already sat in that block; putting a function boundary in front of it makes each attempt genuinely fresh, so a retry fetches ITS OWN OTP instead of re-reading the consumed one. |
| 2 | `@@ -450,7 +485,7 @@` | `process.exit(rc)` becomes `return rc`, one line. | The exit moves to `main()` after the loop, so a failed attempt can return control instead of ending the process. Terminal behaviour is unchanged: the loop's last `rc` is what `main()` exits with. |

**36 lines added, 1 line removed, 2 hunks.** The 217-line login body between them is **byte-for-byte
identical** to the running bytes (verified by extracting lines 236-452 of the capture and comparing them to
lines 271-487 of the candidate: equal). Its indentation is unchanged, which is why a 217-line move produces
no diff noise.

## 4. What was deliberately NOT ported

The cot running bytes and the 49F canonical at HEAD differ in **12 hunks** (456 vs 605 lines, unified diff at
n=0). This port touches the retry and nothing else. Two of the other eleven are worth the issuer's eye, and
neither is in this order's scope:

- **`classifyByDom` (49F only).** A DOM-based state classifier the 49F copy falls back to when Kimi-VL is
  unavailable or unsure. cot has no such fallback. NOT ported: it changes how a screen is classified, which
  is cot-visible behaviour, and this order asks for the retry only.
- **The F2 persist-binding (49F only).** In the 49F copy the `smPut` of the fresh session is wrapped so a
  failed write sets `rc = 1` ("persist FAILED -> NOT a success"). In the cot running bytes `smPut` is
  unguarded: a throw propagates to the outer `catch`, which logs `ERROR` and leaves `rc` at 0. **So a cot run
  can report success while the fresh cookie was never persisted** -- the silent-freeze class the 49F copy was
  hardened against on 2026-07-02. The retry does not create this and does not worsen it (the loop breaks on
  `rc === 0`, exactly as the single attempt exited on it), but it now sits one line away from ported code, so
  it is named here rather than left for the next reader. NOT ported: out of `<paths>` intent and out of this
  cell's stated change.

## 5. Exercise -- the loop, run locally, no vendor call

The ported loop was lifted VERBATIM into a local harness with `attemptLogin` stubbed and `setTimeout`
recorded rather than awaited. No playwright, no AWS, no Black Diamond: control flow and backoff arithmetic
are the whole subject. `node <harness>` -> **`RETRY-LOOP OK: 6 of 6 arms passed`**, rc=0:

| Arm | Result |
|-----|--------|
| first attempt succeeds | 1 attempt, no backoff |
| fails once then recovers | 2 attempts, one 5000 ms backoff, logs `login RECOVERED in-run on attempt 2` |
| fails twice then recovers | 3 attempts, 5000 + 10000 ms |
| all fail | capped at 3 attempts, rc=1, no backoff after the last, logs `login EXHAUSTED` |
| **`BD_MAX_LOGIN_ATTEMPTS=1`** | **exactly 1 attempt, no backoff -- today's behaviour reproduced** |
| no env at all | default cap 3, default 5000 ms base |

`node --check` on the full candidate: OK. 0 CR bytes, 0 non-ASCII bytes.

The cot box's `secret-ids.env` already carries `BD_MAX_LOGIN_ATTEMPTS=3` and `BD_LOGIN_BACKOFF_MS=5000`
under the comment "Inert until the new .js is box-deployed (CTO-gated)", so the deploy activates them with
no env change. The equivalence arm is the rollback assurance: setting that variable to 1 returns the box to
single-attempt behaviour without redeploying a `.js`.

## 6. What Part 2 still needs

1. The issuer's written GO naming this diff's commit.
2. A disposition on row `IRPT_BCKEND-S198` -- without it the `.js` cannot be committed at all, so the S3
   upload leg (A1) would have no committed source to upload.
3. The sequencing call in section 1 (211 graded before the port lands, or AC1 re-pointed).

Ledger `cot-login-retry-s165-m-20260929` is NOT opened: no leg of it can start before the GO.

**DIFF READY.**
