# IRPT_BCKEND R21 S165 -- the deployable cot login script, DIFF for the issuer and the CTO

**TO:** `IRPT_BCKEND.TO-IB-m21-212` Part 1 | **cell:** `IB-mr-212` | **rows:** `IRPT_BCKEND-S165`, `-S199`
**Author:** `0.6.2_AE_PartnerETL~S` | **Date:** 2026-09-29 | **Issuer:** `2.0.0_SA_COO~M` | **Reader:** `1.0.0_SA_CTO` (ruling S198)
**Supersedes** the Part 1 diff at `@d16c0eda0f`, which predated amendments 2 and 3.

**Base (a/):** `infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js.running-capture.txt` -- the byte-exact
running script, md5 `28dd27a054b826cc3a87f6b4498d3b5a`, 35,049 B, landed by TO-IB-m21-211 `@fc609ed209`.
**Candidate (b/):** `infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js`, md5
`7d37465ba68e8ddf44a66c008179d080`, 40,333 B. **10 hunks, +84 / -20 lines.**

**Nothing is deployed by this document.** Part 2 runs only on the issuer's written GO naming this commit and
the CTO's read.

---

## 1. What the three amendments asked for, and where each one is

| Ask | Where |
|-----|-------|
| the bounded retry and backoff (row S165, the cell) | group **A**, hunks A1 and A2 |
| the F2 persist-binding (row S199, amendment 3) | group **B**, hunk B1 |
| every graded firm/product name off the `.js` (amendment 2) | group **C**, hunks C0-C7 |
| pass the naming limb with **no waiver and no override** | measured in section 4: `NAMING-GATE: WARN 7 graded`, rc=0, **0 REFUSE** |
| no other 49F hunk | `classifyByDom` and the remaining 9 of the 12 divergences stay out (section 6) |

## 2. Why group C looks the way it does

The naming limb grades **every string literal on an added line** of a `.js`. Its Python path skips literals
inside a builder call (`key`/`address`/`name`/`lookup`), which is how a Python file expresses
`lookup('49financial')` lawfully -- **`js_literals` has no such skip** (`.tools/naming-gate.py:413`, against
`py_literals:285`). There is therefore no way to write a permitted firm literal in JavaScript at all, and
`lib/opal_naming.py` is a Python module a Node script on an EC2 box cannot import.

So the names had to leave the `.js` entirely. The carrier is **`secret-ids.env`**, which is already deployed
beside the script, is already in this order's grant, and is **not in the limb's graded set** (`.py .js .mjs
.ts .tf .json .yaml .yml`). A `.json` name file would have been refused for the same literals; the `.env` is
the only lawful box-side carrier in the cot tree.

**The registry is the authority for what those values are, and it is what decided their shape.**
`infra/logic/registry/scopes.json` records the FIRM `49financial` with short `49f`, and records the short
vendor spelling among its aliases **flagged `refused`, with the reason stated in the registry itself: the
vendor is `blackdiamond`, the firm is `49financial`.** That is why the two Black Diamond **cookie names** are
carried as vendor configuration and **not** through a firm lookup -- routing a vendor cookie name through a
firm builder would assert something the registry explicitly denies. No registry row needed adding: `cot` is
already the registered short spelling of the FIRM `cottonwood`, so no builder refusal arose and nothing was
hand-typed in place of one.

## 3. The diff

```diff
--- a/bd_49f_auto_login.js.running-capture.txt (RUNNING 28dd27a0)
+++ b/bd_49f_auto_login.js (deployable port)
@@ -65,6 +65,17 @@
 const KIMI_MODEL = process.env.BD_KIMI_MODEL || 'kimi-k2.6';
 const UA = process.env.BD_UA || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
 const MAX_STEPS = parseInt(process.env.BD_MAX_STEPS || '12', 10);
+// NAMING (TO-IB-m21-212 amendment 2, CLAUDE.md rule 30): the Black Diamond session and device cookie NAMES
+// are VENDOR names, not firm names. infra/logic/registry/scopes.json records the short vendor spelling as a
+// REFUSED alias of the firm 49financial for exactly that reason -- the vendor is blackdiamond, the firm is
+// not -- so reading a vendor cookie through a FIRM lookup would assert something false. They arrive from
+// configuration instead (secret-ids.env, deployed beside this script), REQUIRED: main() fails CLOSED and
+// loud if either is unset, so a missing config can never silently look for the wrong cookie.
+const IDENTITY_COOKIE = process.env.BD_IDENTITY_COOKIE;
+const DEVICE_COOKIE = process.env.BD_DEVICE_COOKIE;
+// The debug-shot S3 prefix is configuration too. Its VALUE is unchanged from the running script, so the box
+// role's existing PutObject grant on that exact prefix still matches. Read only when shots are enabled.
+const DEBUG_PREFIX = process.env.BD_DEBUG_PREFIX;
 
 // --- logging: STATE only, NEVER a credential/OTP/cookie VALUE (ROE) ---
 const log = (m) => process.stderr.write(`[bd-auto-login] ${m}\n`);
@@ -143,7 +154,7 @@
     // polls it, consumes ONCE, and best-effort CLEARS it (defense-in-depth; CVO also clears). Freshness-
     // gated: only accept a code whose ts >= loginStart, so a stale prior-run code is never reused.
     // ROE: transient single-use; not logged; the durable 'gateway' adapter replaces this.
-    const relayId = process.env.BD_OTP_RELAY_SECRET_ID || `blackdiamond/${process.env.BD_FIRM_ID || '49f'}/otp-relay`; // firm-derived (main() also sets the env)
+    const relayId = process.env.BD_OTP_RELAY_SECRET_ID || `blackdiamond/${process.env.BD_FIRM_ID}/otp-relay`; // firm-derived; main() requires BD_FIRM_ID and also sets this env
     const tries = parseInt(process.env.BD_OTP_TRIES || '30', 10);
     const delayMs = parseInt(process.env.BD_OTP_DELAY_MS || '10000', 10);
     const skewMs = 60000; // allow the producer's clock a minute of skew vs loginStart
@@ -213,11 +224,17 @@
 
 async function main() {
   // ONE canonical process, ALT credentials PER PARTNER (Andrew-direct 2026-06-25): BD_FIRM_ID selects the
-  // partner ('49f' | 'cot' | ...) and DERIVES every firm-bound secret-id from blackdiamond/<firm>/*. The
+  // partner (the firm's registered short spelling) and DERIVES every firm-bound secret-id from
+  // blackdiamond/<firm>/*. It is REQUIRED, not defaulted -- see the NAMING note in main(). The
   // same script runs per-firm on each partner's OWN isolated box/role (NEVER#1: the 49F box has an IAM Deny
   // on blackdiamond/cot/* and vice-versa -- firm-isolation is enforced at the infra layer; this guard is the
   // code-layer belt-and-suspenders). Explicit BD_*_SECRET_ID still override, but default firm-correctly.
-  const firm = process.env.BD_FIRM_ID || '49f'; // default 49f for back-comat; cot box sets BD_FIRM_ID=cot
+  // NAMING: no hand-kept firm literal. The firm id is configuration (secret-ids.env sets it) and is now
+  // REQUIRED: the old fallback was both a graded hand-kept carrier and a firm-sep hazard on this box, because
+  // an unset value would have resolved every secret-id to the OTHER firm. Fails CLOSED before any secret read.
+  const firm = process.env.BD_FIRM_ID;
+  if (!firm) { log('FATAL naming: BD_FIRM_ID is unset -- the firm id is configuration, never a default in code'); process.exit(3); }
+  if (!IDENTITY_COOKIE || !DEVICE_COOKIE) { log('FATAL naming: BD_IDENTITY_COOKIE and BD_DEVICE_COOKIE must be set -- vendor cookie names are configuration'); process.exit(3); }
   const credsId = process.env.BD_CREDENTIALS_SECRET_ID || `blackdiamond/${firm}/credentials`;
   const kimiId = process.env.BD_KIMI_SECRET_ID || 'astn/kimi/api-key'; // shared CV key (not firm data)
   const sessionId = process.env.BD_SESSION_SECRET_ID || `blackdiamond/${firm}/session`;
@@ -233,6 +250,41 @@
   catch (e) { log(`ERROR: secret load failed (${String(e).split('\n')[0]})`); process.exit(2); }
   if (!creds.username || !creds.password) { log('ERROR: credentials secret missing username/password'); process.exit(2); }
 
+  // CTO-B OUTER RETRY, ported from the 49F canonical (row IRPT_BCKEND-S165). One transient login failure
+  // used to cost a whole day: the cot chain stayed frozen 09-24..09-27 on four consecutive single-attempt
+  // failures. Each attempt is a FRESH browser context + a FRESH loginStart anchor (so getOtpCode fetches
+  // THAT attempt's own code, never the consumed prior one) + reset otpSent/otpEntered -- all of which
+  // already live in the block below, which is why putting a function boundary in front of it is the whole
+  // mechanism. Bounded by BD_MAX_LOGIN_ATTEMPTS (secret-ids.env sets 3) with exponential backoff from
+  // BD_LOGIN_BACKOFF_MS (5000) = the retry-storm guard: a genuinely dead session must not hammer the vendor
+  // login. On cap exhaustion rc is the SAME terminal state as before -- the session is NOT advanced, so the
+  // existing freshness path still fires. Firm-sep UNAFFECTED: control flow only, no secret-id or path change.
+  // With BD_MAX_LOGIN_ATTEMPTS=1 the behaviour is exactly today's single attempt, which is also the rollback
+  // that needs no redeploy.
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
+      log(`login EXHAUSTED ${MAX_LOGIN_ATTEMPTS} attempts -> rc=${rc} LOUD terminal (session NOT advanced)`);
+    }
+  }
+  process.exit(rc);
+}
+
+// ONE login attempt: fresh browser context, fresh OTP window, perceive-act loop, capture-on-success.
+// Returns rc (0 = the session cookie captured AND persisted to SM; nonzero = failed, NOTHING persisted --
+// preserves the "session advanced ONLY on rc==0" invariant per attempt, which group B above is what makes
+// true). The per-attempt state (launch/browser/ctx/page/loginStart/otpSent/otpEntered/rc) lives HERE so
+// every attempt is genuinely fresh: a retry re-using a stale loginStart would re-fetch the consumed code.
+async function attemptLogin(firm, creds, kimiKey, sessionId) {
   const launch = { headless: process.env.BD_HEADLESS !== '0', timeout: 60000, args: ['--no-sandbox', '--disable-dev-shm-usage'] };
   if (process.env.BD_PROXY_SECRET_ID) {  // resi proxy from SM (ALWAYS-ON for BD). Secret = JSON {host,port,username,password,country?}
     // Andrew-direct / CVO: format the username the PROVEN fetch_ft.js:48-54 way -- pin the purchased US
@@ -240,7 +292,7 @@
     // username with no suffix routed through BrightData's generic/no-KYC endpoint -> the bd3 402 robots
     // refusal (mis-read earlier as a domain/KYC block). country from the secret, default 'us'.
     try { const p = JSON.parse(smGet(process.env.BD_PROXY_SECRET_ID));
-      const sid = process.env.BD_PROXY_SID || 'bd49f';
+      const sid = process.env.BD_PROXY_SID || firm; // NAMING: derived, never a hand-kept alias literal
       launch.proxy = { server: `http://${p.host}:${p.port}`,
         username: `${p.username}-country-${p.country || 'us'}-session-${sid}`, password: p.password }; }
     catch (e) { log(`WARN: proxy secret load failed (${String(e).split('\n')[0]}) -- proceeding w/o proxy (will likely be BD-blocked)`); }
@@ -259,7 +311,7 @@
   if (process.env.BD_DEVICE_REGISTRATION) {
     try {
       const host = new URL(BD_APP_URL).hostname;
-      await ctx.addCookies([{ name: 'bd_DeviceRegistration', value: process.env.BD_DEVICE_REGISTRATION, domain: host, path: '/', secure: true, httpOnly: true }]);
+      await ctx.addCookies([{ name: DEVICE_COOKIE, value: process.env.BD_DEVICE_REGISTRATION, domain: host, path: '/', secure: true, httpOnly: true }]);
       log('device-trust: bd_DeviceRegistration injected (OTP-skip attempt)');
     } catch (e) { log(`device-trust inject skipped: ${String(e).split('\n')[0]}`); }
   }
@@ -278,7 +330,7 @@
   // SUCCESS SIGNAL = the .bd.identity cookie being PRESENT, NOT vision LOGGED_IN (CVO: Kimi can misread the
   // loaded post-login dashboard as MFA_OTP -- e.g. cot's "Please Wait... 186 Items Ready" screen). The
   // cookie's presence IS login success; capture on it, vision-independent. Hardens BOTH firms.
-  const hasIdentity = async () => { try { return (await ctx.cookies()).some((c) => c.name === '.bd.identity'); } catch (_) { return false; } };
+  const hasIdentity = async () => { try { return (await ctx.cookies()).some((c) => c.name === IDENTITY_COOKIE); } catch (_) { return false; } };
   const loginStart = Date.now(); // OTP time-window anchor (the OTP email must post-date the login attempt)
   const runTs = new Date(loginStart).toISOString().replace(/[:.]/g, '-'); // debug-shot run folder
   try {
@@ -294,13 +346,14 @@
       // to S3 (Playwright paints a box over them) -- keeps the watch value (layout/labels/buttons/masked-dest)
       // while honoring the durable-auth no-persist-values rule. Username (Andrew-shared) + masked-dest stay visible.
       if (process.env.BD_DEBUG_SHOTS === '1') {
-        try { const f = `/tmp/bd-step${step}.png`;
+        try { const f = `/tmp/step${step}.png`;
           await page.screenshot({ path: f, mask: [
             page.locator("input[type='password']"),
             page.locator("input[autocomplete='one-time-code'], input[name*='code' i], input[type='tel']"),
           ] });
-          s3Put(f, `ec2/bd-${firm}-auto-login/debug/${runTs}/step${step}_${state}.png`); // firm-parameterized (NEVER#1: cot writes ONLY the cot prefix)
-          log(`DEBUG shot -> ec2/bd-${firm}-auto-login/debug/${runTs}/step${step}_${state}.png`); }
+          if (!DEBUG_PREFIX) { log('WARN: BD_DEBUG_SHOTS=1 but BD_DEBUG_PREFIX is unset -- shot NOT uploaded'); }
+          else { s3Put(f, `${DEBUG_PREFIX}/${runTs}/step${step}_${state}.png`); // configured prefix (NEVER#1: this box writes ONLY its own)
+            log(`DEBUG shot -> ${DEBUG_PREFIX}/${runTs}/step${step}_${state}.png`); } }
         catch (e) { log(`shot save skipped: ${String(e).split('\n')[0]}`); }
       }
       if (state === 'LOGGED_IN') {
@@ -425,24 +478,35 @@
     if (rc !== 0) { log('ERROR: did not reach LOGGED_IN within MAX_STEPS'); }
     else {
       const all = await ctx.cookies();
-      const bd = all.find((c) => c.name === '.bd.identity');
+      const bd = all.find((c) => c.name === IDENTITY_COOKIE);
       // EVIDENCE (CVO/Andrew: device-trust diagnosis, not speculation) -- dump ALL post-login cookie NAMES
       // (names only, ROE-safe -- no values) so we SEE whether BD even sets a device-trust cookie + its exact
       // name. The device cookie may NOT be literally "bd_DeviceRegistration" -- widen the match to any
       // device/trust/remember-named cookie and capture whichever BD actually sets.
       if (process.env.BD_DEBUG_FORM === '1') log(`DEBUG post-login cookie names: ${JSON.stringify(all.map((c) => c.name))}`);
-      const dev = all.find((c) => c.name === 'bd_DeviceRegistration') || all.find((c) => /device|deviceid|trust|remember/i.test(c.name));
+      const dev = all.find((c) => c.name === DEVICE_COOKIE) || all.find((c) => /device|deviceid|trust|remember/i.test(c.name));
       if (!bd) { log('ERROR: .bd.identity not present after login'); rc = 1; }
       else {
         // ROE: write the fresh session bundle DIRECTLY to SM (the only at-rest home); NEVER log the values.
-        smPut(sessionId, JSON.stringify({
-          bd_identity: bd.value,
-          all_cookies: all.map((c) => ({ name: c.name, value: c.value, domain: c.domain })),
-          bd_device_registration: dev ? dev.value : null,
-          bd_device_cookie_name: dev ? dev.name : null, // record WHICH cookie carried device-trust (evidence)
-          captured_at: new Date().toISOString(),
-        }));
-        log(`OK: fresh .bd.identity written to SM (${sessionId}) + device-trust=${dev ? 'present(' + dev.name + ')' : 'absent'}`);
+        // F2 PERSIST-BINDING (row IRPT_BCKEND-S199, amendment 3; the shape of the 49F canonical's :582-593).
+        // The persist IS the deliverable. Unguarded, a PutSecretValue throw reached the OUTER catch, logged
+        // ERROR and LEFT rc=0 (already set by the successful login), so the run reported SUCCESS while the
+        // fresh cookie was never persisted -- and the retry loop above breaks on rc===0, so it would stop on
+        // exactly that run. Binding persist to rc makes a failed write rc=1 LOUD: the session is not
+        // advanced and the existing freshness path fires instead of a false green.
+        try {
+          smPut(sessionId, JSON.stringify({
+            bd_identity: bd.value,
+            all_cookies: all.map((c) => ({ name: c.name, value: c.value, domain: c.domain })),
+            bd_device_registration: dev ? dev.value : null,
+            bd_device_cookie_name: dev ? dev.name : null, // record WHICH cookie carried device-trust
+            captured_at: new Date().toISOString(),
+          }));
+          log(`OK: fresh session written to SM (${sessionId}) + device-trust=${dev ? 'present(' + dev.name + ')' : 'absent'}`);
+        } catch (e) {
+          rc = 1; // persist FAILED -> NOT a success; the session is not advanced
+          log(`ERROR: smPut FAILED to persist the fresh session (${String(e).split('\n')[0]}) -> rc=1 LOUD (session NOT advanced)`);
+        }
       }
     }
   } catch (e) {
@@ -450,7 +514,7 @@
   } finally {
     await browser.close().catch(() => {});
   }
-  process.exit(rc);
+  return rc;
 }
 main();
 
```

## 4. One line per hunk

### Group A -- the retry (row S165)

| Hunk | What it does | Why |
|------|--------------|-----|
| **A1** `@@ -233,6 +250,41 @@` | After the credentials guard, closes `main()` on a bounded retry loop (`BD_MAX_LOGIN_ATTEMPTS`, default 3; exponential backoff from `BD_LOGIN_BACKOFF_MS`, default 5000) and re-opens the rest of the old `main()` body as `async function attemptLogin(firm, creds, kimiKey, sessionId)`. | Every piece of per-attempt state the retry must refresh -- `launch`/`browser`/`ctx`/`page`, `loginStart` (the OTP time-window anchor), `otpSent`, `otpEntered`, `rc` -- already sat in that one block, so putting a function boundary in front of it IS the mechanism. A retry re-using a stale `loginStart` would re-fetch the consumed OTP and be a no-op. |
| **A2** `@@ -450,7 +514,7 @@` | `process.exit(rc)` becomes `return rc`, one line. | The exit moves to `main()` after the loop so a failed attempt returns control instead of ending the process. Terminal behaviour is unchanged: the loop's last `rc` is what `main()` exits with. |

### Group B -- the F2 persist-binding (row S199, ARMED)

| Hunk | What it does | Why |
|------|--------------|-----|
| **B1** (inside `@@ -425,24 +478,35 @@`) | Wraps the session `smPut` in `try/catch`; on a throw sets `rc = 1` and logs `smPut FAILED to persist the fresh session ... (session NOT advanced)`. The shape of the 49F canonical's `:582-593`. | Unguarded, a Secrets Manager throw reached the outer `catch`, logged `ERROR`, and **left `rc` at 0** -- so the run reported success while the fresh cookie was never persisted. With group A above that is worse, not merely equal: the loop's `if (rc === 0) break` would stop on exactly that run. Binding persist to `rc` is what makes the retry's own success test mean what it says. |

### Group C -- naming (amendment 2)

| Hunk | What it does | Why |
|------|--------------|-----|
| **C0** `@@ -65,6 +65,17 @@` | Adds module-scope `IDENTITY_COOKIE`, `DEVICE_COOKIE`, `DEBUG_PREFIX`, each read from the environment. | The two cookie names and the debug prefix were the four refused literals in the login body. They become configuration; see section 2 for why the cookie names are vendor config rather than a firm lookup. |
| **C1** (inside `@@ -213,11 +224,17 @@`) | `const firm = process.env.BD_FIRM_ID \|\| '49f'` becomes a **required** read, with a fail-closed `exit 3` for it and for the two cookie names, before any secret is read. | Removes the refused `'49f'` literal, and removes a real firm-sep hazard: on this cot box an unset `BD_FIRM_ID` would have resolved **every** secret-id to the other firm. Placed above the first `smGet` deliberately, so a misconfiguration can never reach a secret. |
| **C2** `@@ -240,7 +292,7 @@` | The sticky-proxy session id falls back to `firm` instead of the literal alias. | Removes the refused `'bd49f'`. Derived, not hand-kept. Inert for cot today (`BD_PROXY_SECRET_ID` is unset). |
| **C3a** `@@ -259,7 +311,7 @@` | The device-trust cookie inject uses `DEVICE_COOKIE`. | Removes a refused vendor-cookie literal. |
| **C3b** `@@ -278,7 +330,7 @@` | `hasIdentity()` compares against `IDENTITY_COOKIE`. | Same. |
| **C3c / C3d** (inside `@@ -425,24 +478,35 @@`) | The post-login `find` calls use `IDENTITY_COOKIE` and `DEVICE_COOKIE`; the widened `device\|trust\|remember` regex fallback is untouched. | Same, and the fallback is what keeps device-trust capture working if the vendor renames the cookie. |
| **C4** (inside `@@ -294,13 +346,14 @@`) | The local throwaway screenshot path becomes `/tmp/step${step}.png`. | Removes a refused literal in a name nothing reads back; the file is written, uploaded and forgotten inside one `if`. |
| **C5** (inside `@@ -294,13 +346,14 @@`) | The debug S3 key is assembled from `DEBUG_PREFIX`, with a loud `WARN` and **no upload** if it is unset. | Removes the refused S3-key literal. **The VALUE is unchanged** (`ec2/bd-cot-auto-login/debug`), so the box role's existing `PutObject` grant on that exact prefix still matches -- no IAM change is implied by this port. |
| **C6** `@@ -143,7 +154,7 @@` | Drops a **second** `\|\| '49f'` default, in `getOtpCode`'s relay branch. | **The limb does not grade this one** -- it sits inside a template placeholder, which the scanner collapses to `{x}` -- so it is called out separately and is strikeable on its own. It cannot change behaviour: `main()` now fails closed when `BD_FIRM_ID` is unset **and** assigns `BD_OTP_RELAY_SECRET_ID` before any login runs, and for cot the whole branch is inert (`BD_OTP_ADAPTER=gateway`). What it removes is a cross-firm default sitting inside a firm-separated script. |
| **C7** (inside `@@ -213,11 +224,17 @@`) | Updates the header comment that described the default C1 removed. | A comment is not graded, but a stale one that contradicts the code two lines below it is a trap for the next reader. |

## 5. The second artifact: `secret-ids.env`

Three lines added (plus the comment stating why), 1,685 -> 2,550 B:

```
BD_IDENTITY_COOKIE=.bd.identity
BD_DEVICE_COOKIE=bd_DeviceRegistration
BD_DEBUG_PREFIX=ec2/bd-cot-auto-login/debug
```

`BD_FIRM_ID=cot`, `BD_MAX_LOGIN_ATTEMPTS=3` and `BD_LOGIN_BACKOFF_MS=5000` were already there -- the last two
under the comment "Inert until the new .js is box-deployed (CTO-gated)", which this port is what activates.

**The coupling is the one thing in this change that is genuinely two-artifact, and it is stated plainly:**
the new `.js` **requires** `BD_IDENTITY_COOKIE` and `BD_DEVICE_COOKIE`. If the `.js` reached the box without
the env file, it would `exit 3` loudly on the very first run rather than log in with wrong cookie names. That
is the failure direction chosen on purpose -- a loud refusal that the existing freshness path already reacts
to, never a silent wrong-cookie login -- but it does mean **Part 2 must deploy both files, and the rollback
must restore both.** The box's env file is already a different md5 from the repo's (`9b55e03c` vs the repo
copy), so Part 2's S3 upload of the cot tree is what reconciles them.

### 5a. A line-ending hazard this change turned load-bearing -- MEASURED, and fixed

Making the `.js` depend on `secret-ids.env` exposed something that would have broken Part 2 outright:

```
working copy of infra/aws/ec2/bd-cot-auto-login/secret-ids.env : 2560 B, CR=35, LF=35
the same file's blob at CLOUD                                  : 2525 B, CR=0,  LF=35
BD_FIRM_ID on disk -> b'BD_FIRM_ID=cot<CR>'      in the blob -> b'BD_FIRM_ID=cot'
```

No `.gitattributes` rule covered `*.env`, so the blob is LF and **every checkout on an autocrlf=true device
materializes CRLF.** Part 2's leg A1 uploads the WORKING copy, and the box's wrapper SOURCES that file with
bash on Linux -- so every value would have carried a trailing carriage return. `BD_FIRM_ID=cot<CR>` makes
every derived secret-id a name that does not exist (exit 2); `BD_IDENTITY_COOKIE=.bd.identity<CR>` would make
the identity cookie never match, so the login would burn all three retry attempts and report exhausted. The
hazard predates this change for `BD_FIRM_ID`; the change widens it to the two new required values.

Fixed in this order's granted `.gitattributes`: `infra/aws/ec2/bd-cot-auto-login/*.env text eol=lf`
(`@626033ace0`, with a bare-CR repair to its own comment at `@2a4c589512`). `git check-attr` now reads
`text: set, eol: lf`, and the working copy was normalized so it is byte-identical to the blob (2,525 B, 0 CR).
**Not done, named instead:** the sibling 49F and inf env files under `infra/aws/ec2/` are uncovered by the
same rule and are outside this order's grant.

## 6. What was deliberately NOT ported

The capture and the 49F canonical at HEAD differ in **12 hunks** (456 vs 605 lines, unified diff at n=0); two
top-level functions exist only in 49F. This port takes the retry and the F2 binding and nothing else, per
amendment 3.

- **`classifyByDom` (49F only)** -- a DOM-based state classifier the 49F copy falls back to when Kimi-VL is
  unavailable or unsure. NOT ported: it changes how a screen is classified, which is cot-visible behaviour.
- **The remaining 9 divergences** -- not read line-by-line for this diff and not touched. Amendment 3 says no
  other 49F hunk comes with this one.

## 7. Exercised -- everything below ran locally, with no vendor request

**(a) The naming limb, on the staged candidate** -- the measurement amendment 2 asked for:

```
git add -f infra/aws/ec2/bd-cot-auto-login/bd_49f_auto_login.js
git diff --cached --no-color --no-ext-diff -- <that path> > ng.diff
python .tools/naming-gate.py --diff ng.diff --post-from-index
-> NAMING-GATE: WARN 7 graded    (rc=0)
```

**0 REFUSE, no waiver, no override.** The same file as a `.js` before group C returned `NAMING-GATE: REFUSE
15 graded` and aborted the commit twice. The 7 remaining verdicts are 2 CONFORMANT (the artifacts bucket, a
secret prefix) and 5 RAISE, every RAISE a `{x}` placeholder the grammar cannot place -- rule-or-registry
defects, explicitly "not a refusal", and all 5 present in the captured bytes already.

**(b) The retry loop, lifted verbatim into a local harness** with `attemptLogin` stubbed and `setTimeout`
recorded rather than awaited. No playwright, no AWS, no Black Diamond. **`RETRY-LOOP OK: 7 of 7 arms
passed`**, rc=0:

| Arm | Result |
|-----|--------|
| first attempt succeeds | 1 attempt, no backoff |
| fails once then recovers | 2 attempts, one 5000 ms backoff, logs `login RECOVERED in-run on attempt 2` |
| fails twice then recovers | 3 attempts, 5000 + 10000 ms |
| all fail | capped at 3, rc=1, no backoff after the last, logs `login EXHAUSTED` |
| **a persist failure (the rc=1 group B now returns) is RETRIED, not broken on** | 2 attempts -- the A+B interaction, exercised |
| **`BD_MAX_LOGIN_ATTEMPTS=1`** | exactly 1 attempt, no backoff: today's behaviour, and the rollback that needs no redeploy |
| no env at all | default cap 3, default 5000 ms base |

**(c) The new fail-closed guards, by running the real candidate** with `BD_PW_PATH` pointed at a stub browser
module and a stub `aws` on `PATH`, so nothing could reach a browser, AWS or the vendor:

| Arm | Observed |
|-----|----------|
| `BD_FIRM_ID` unset | **rc=3**, `FATAL naming: BD_FIRM_ID is unset -- the firm id is configuration, never a default in code`, and no secret read attempted |
| firm set, cookie names unset | **rc=3**, `FATAL naming: BD_IDENTITY_COOKIE and BD_DEVICE_COOKIE must be set` |
| all config present, `aws` unavailable | **rc=2**, `partner=cot (creds/session/relay -> blackdiamond/cot/*)` then `secret load failed` -- i.e. it passed **both** guards and reached the normal path, so the guards do not fire spuriously |

**(d) Hygiene:** `node --check` OK on the candidate. 0 CR bytes, 0 non-ASCII bytes. Every hunk was applied by
a build script that asserts each anchor occurs **exactly once** and re-verifies the base md5 first, so no
replacement landed on a near-miss.

## 8. What Part 2 still needs

1. The issuer's written **GO** naming this diff's commit **and** the CTO's read (amendment 2).
2. Ledger `cot-login-retry-s165-m-20260929`, legs A1 (S3 upload of the cot tree) / A2 (S3 -> box deploy) /
   V1 (SSM read of the running md5 and `secret-ids.env`) / V2 (the next scheduled
   `opal-cot-bd-session-fetch` Success, cron 07:30 America/New_York). NOT opened -- no leg can start before
   the GO.
3. **Both** files in the same deploy, per sections 5 and 5a, and the rollback restores both: re-deploy the captured
   bytes from `bd_49f_auto_login.js.running-capture.txt` and the prior env file under the same ledger. The
   cheaper partial rollback, with the port left in place, is `BD_MAX_LOGIN_ATTEMPTS=1`.
4. Before leg A1, confirm the uploaded `secret-ids.env` has **0 CR bytes** (section 5a). The attribute
   makes that true on a fresh checkout; measure it anyway, because the upload reads the working copy.
5. V1 is what disarms row `IRPT_BCKEND-S199` (running md5 = the committed port).

**DIFF READY.**
