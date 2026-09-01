# TO D12_PLATFORM_OPS.DE3-SITEZ — the browser end-to-end exercise (the criterion W1 lost, rebuilt as its own TO)

<task_order id="D12_PLATFORM_OPS.DE3-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:4xZ</issued>
<status>ISSUED — DEP-BLOCKED on DE1 + DE2. Do not start before they land.</status>
<priority>P1 — this is the acceptance the whole workstream was missing.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ TO-series instruction (17286) + "obviously we need a frontend flow
that ties in with this." PRD `docs/architecture/D12_PLATFORM_OPS_PRD.md` WS-2 exercise, restored to its
original BROWSER grain. Decomp AMENDMENT 3.
</authority>
<proof_of_spec>
  <expected_criteria>DE3-1,DE3-2,DE3-3</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PLATFORM_OPS.DE3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. ⭐ WHY THIS IS ITS OWN TO AND NOT A LINE IN DE2

**This is the criterion the workstream already lost once**, and burying it inside a build TO is how it
got lost. The PRD's WS-2 exercise reads *"an account with MFA enabled **cannot reach the dashboard**
without a live code"* — a **browser** outcome. My W1 TO rendered it *"exercised end to end **against
the deployed handler**, not a unit test"* — an **API** outcome — and W1 then scored an honest **10 of
10** on a feature no human could use.

> **A CLAUSE THAT NAMES THE INSTRUMENT CAN RELOCATE THE SUBJECT WHILE READING AS TIGHTENING.**
> The defect was in my TO, not in anyone's build.

**Giving the browser outcome its own TO, its own id and its own proof row means it cannot be satisfied
by a proxy that happens to pass.**

## 2. OBJECTIVE

**A person, in a real browser, completes the whole MFA login and reaches the dashboard — and cannot
reach it without the code.**

## 3. ACCEPTANCE

| id | must observe |
|---|---|
| **DE3-1** | **THE POSITIVE PATH, END TO END IN A BROWSER:** password -> opt-in prompt -> confirm -> code arrives in a real mailbox -> typed -> **dashboard renders.** State the mailbox, the folder observed, and attach the screenshot you actually read. |
| **DE3-2** | ⛔ **TWO HALVES, AND A PASS WITHOUT THE FIRST IS `UNVERIFIABLE-BY-DISCRIMINATION`, NOT PASS — SEE §3b.** (i) the **RED BASELINE**, captured BEFORE the client fix; (ii) **THE REFUSAL, IN THE SAME BROWSER:** with the correct password and **no** code, the dashboard is **not reachable** — by URL, by back-navigation, or by refresh. ⛔ This is the security property. A success-path-only exercise scores identically whether the gate exists or not. **Name the input that makes it refuse, and run it.** |
| **DE3-3** | The whole flow renders correctly against the **silver-canvas colour law** — screenshot READ, not asserted. |

⛔ **NO ROW HERE MAY BE SATISFIED BY AN API CALL.** If it can be, it is the wrong row and this TO has
failed at the thing it exists for.

## 3b. ⏳ DE3-2 NEEDS ITS **RED** CAPTURED BEFORE THE FIX, OR ITS GREEN CANNOT DISCRIMINATE

Raised by `3.0.0_SA_CVO~Z` minutes before the client fix was to land, and it is the sharpest catch of
the night: **the remedy destroys the only chance to observe the failure.**

> ⛔ **AFTER THE FIX, DE3-2 WILL PASS — AND NOBODY WILL HAVE SEEN IT FAIL.** A green that could not have
> gone red scores identically whether the fix works, whether the branch was unreachable, or whether the
> test never touched the path at all.

⭐ **AND IT IS THE SECOND TIME IN THIS WORKSTREAM.** W1-3's honest 10/10 was the first — a criterion
satisfied while the outcome was never at risk. **This series exists to correct that defect; closing it
with a criterion carrying the same weakness would be the same error wearing the fix's clothes.**

### THE RED IS EXERCISABLE WITH NOTHING ENABLED — the barrier four seats accepted does not apply

*"0 of 48 accounts are gated and we may not enable one"* was treated as fixed. **All five rungs of F-2
are CLIENT-side; the server is already correct.** So the baseline needs **no MFA-enabled account, no
account change, no server change and no IAM act**:

> Serve the portal at its current pin, **intercept the `/auth/login` response only**, return HTTP 200
> with `{mfaRequired:true, challengeId, channel:'email'}` and **no accessToken** — exactly the shape
> `index.ts:167` already emits — and **observe where the browser lands.**
> **Expected RED:** `/market` is reached and `localStorage.accessToken === "undefined"`.

⚠ **BOUND, kept from its author so it is not oversold: a stub exercises THE CLIENT, not the integrated
system.** It cannot prove the server emits that shape — that is a separate source read, already done by
two seats. **It proves the half actually in dispute: that this client, in a real browser, admits a
tokenless 200.**
**Local, read-only, uncommitted. Not a deploy; it does not touch DEV.**

### SCORING

**DE3-2's evidence is the PAIR:** the RED baseline (pre-fix, browser-observed) **and** the GREEN
(post-fix, same instrument). ⛔ **A GREEN ALONE IS `UNVERIFIABLE-BY-DISCRIMINATION` — score it in those
words, never PASS.** If the RED was genuinely never capturable, say that instead of implying a
discriminating test ran.
⛔ **THIS IS NOT A NEW GATE.** `1.0.0_SA_CTO~Z`'s cohort gate stands unchanged; this only makes its
evidence real. If the RED is missed the gate still holds — it just closes on a PASS nobody can size.

## 4. ⛔ THE ACCOUNT PROBLEM — READ BEFORE PLANNING DE3-1

**Zero of 48 accounts have MFA enabled right now, deliberately.** Andrew was locked out of PROD tonight
by this exact flow and the revert is what cleared it.
- ⛔ **DO NOT ENABLE MFA ON ANY ACCOUNT TO CREATE YOUR TEST SUBJECT.** That is `2.0.0_SA_COO~Z`'s to
  arrange on Andrew's word.
- ⛔ **DO NOT CREATE A TEST ACCOUNT ON A LIVE HUMAN EMAIL ADDRESS.** One did exactly that tonight,
  mailed Andrew two production-shaped messages, and cost a false bug report plus ~40 minutes of three
  seats. The only tell was a greeting.
- **When you reach this cell, STOP AND ASK `2.0.0_SA_COO~Z` for a test subject.** Requesting one is one
  message; provisioning one yourself is how tonight's incident happened.

## 4b. ⛔ DE3-1 HAS **TWO** BLOCKERS AND ONLY ONE WAS ASKED ABOUT - and the second one changes WHERE it runs

`0.4.0_DE_ClientPlatform~Z` correctly stopped and asked for a test subject. **The subject is the
VISIBLE blocker. There is a second, and nobody has stated it:**
```
BLOCKER 1  the test subject          -- held at 2.0.0_SA_COO~Z; a PRODUCTION write (see 4c)
BLOCKER 2  THERE IS NOWHERE TO SERVE THE MFA UI
           production serves index-D9vMtGZu.js -- mfaRequired 0, mfa/verify 0, challengeId 0
           the UI exists ONLY at portal 087a456f, which is LOCAL AND UNPUSHED
           (3.0.0_SA_CVO~Z: unreachable from 0 of 364 remote refs; origin/DEV = be39451b)
```
>> **SO EVEN WITH A SUBJECT IN HAND, DE3-1 CANNOT RUN "AGAINST PROD" - THE SCREEN IT NEEDS IS NOT
   SERVED ANYWHERE.** It runs against a LOCAL serve of `087a456f`, or it does not run. **State this
   before planning, or the row waits on a promote that is not coming and reads as blocked on the
   subject alone.** <<

### ⭐ AND THAT IS AN UPGRADE, NOT A COMPLAINT - DE3-1 IS THE ACT THAT RETIRES F-2's OPEN LIMB
Every frame so far -- the DE RED, the CVO RED, the CVO GREEN -- **stubs the fetch boundary**, and all
four independence axes cannot cover the one thing they share: *an error inherent to stubbing is
invisible to every frame because every frame makes it.*
**DE3-1 as specified has NO STUB: a real browser, the real deployed handler, a real emailed code.**
> ### THAT IS THE INTEGRATED OBSERVATION F-2 HAS BEEN MISSING, AND IT IS THE ONLY ROW ON THE BOARD THAT PRODUCES IT.
**Wire the local serve at `087a456f` to the REAL API, not to a stub.** If that wiring is not trivial
(`Ha=""` means the client calls SAME-ORIGIN, so a local dev server needs its `/auth/*` proxied to the
live host), **say so** -- the proxy is part of the deliverable, and a DE3-1 run against a stubbed
backend would be a fourth frame on the same instrument rather than the observation.

## 4c. ⛔ THE SUBJECT IS A **PRODUCTION** ACT - which is why it is held rather than handed over

There is **no evidence of a separate DEV user store.** `https://opalinvest.dev` fronts the MFA-capable
handler (`/auth/mfa/verify` answers `401 {"error":"Invalid or expired code"}` -- the HANDLER's own body,
not the gateway's), and `opal-users-v2` holds its profiles. **Provisioning a gated test subject means
creating an account and enabling MFA in the LIVE production users table.**
⚠ **And the mailbox is the hard half, not the account.** The only readable mailbox used so far was
`andrew+d12mfatest@opalinvest.com` -- **a plus-address on a LIVE HUMAN mailbox**, which is precisely
what was barred after it caused tonight's false bug report. **A `.invalid` recipient sends but cannot
be READ, so it cannot satisfy "code arrives in a real mailbox -> typed".**
>> **THE OPEN QUESTION IS THEREFORE NOT "MAY WE ENABLE MFA" BUT "DOES A MAILBOX WE CONTROL AND NO
   HUMAN READS EXIST?"** Creating one is an M365 admin act, which this seat does not hold. **That is
   the question that goes up, and it is answerable cold.** <<
⛔ **Nothing here authorises provisioning. No account created, none enabled, no flag written.**

## 5. WHAT THIS TO DOES NOT DO

It does not re-enable Andrew's account (his word, via `2.0.0_SA_COO~Z`); it does not start the pilot
cohort (unnamed, and it cannot begin before this flow exists); it does not promote to PROD (a DT act);
and it does not touch IAM — **FINDING F-1 stays open with its own owner.**

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`. Push state MEASURED. Surprise items to
`0.0.0_AB_MSTR~Z`.
⭐ **And if a criterion here cannot be satisfied honestly, say so in those words.** Tonight
`UNVERIFIABLE-BY-INSTRUMENT` on a folder observation was upgraded to PASS by a different observer
hours later — **a bounded refusal survived contact with the truth, and a guess would not have.**


## ⛔ SCOPE FENCE — A RULE, NOT A LIST. **CORRECTED 2026-09-01 ~01:5xZ.**

> ### YOUR PROJECT IS `PLATFORM_OPS_USERMGMT` AND NOTHING ELSE.
> **Any task order that is not one of the D12 TOs addressed to your full suffixed serial is NOT YOURS
> — whatever any list says, and whatever a roster query returns. REPORT it to `2.0.0_SA_COO~Z` and
> keep working.**

⛔ **THIS REPLACES AN ENUMERATED BAR, AND THE ENUMERATION WAS WRONG IN BOTH DIRECTIONS.** I originally
named a fixed list of base-addressed TOs. Measured on the directory instrument afterwards, that list
was **under-inclusive** (open rows it never named) **and over-inclusive** (rows it named that are no
longer open, or whose files are not even in this folder). **A list that is wrong in both directions is
worse than no list, because it reads as complete.**
CLAUDE.md already carries this: **a guard is only as wide as its enumeration, and an enumerated ban
list lapses SILENTLY when a name changes.** The rule above cannot lapse.

### WHY A ROSTER QUERY WILL MISLEAD YOU — three measured instrument limits

1. **`to-check --assignee` OVER-matches:** it is a substring match and it matches the **ISSUER** as
   well as the assignee. A serial appears as author, recipient and owner; only the third is an
   obligation. **Read the ROWS, never the count.**
2. ⛔ **`to-check --assignee` also UNDER-matches, which is the dangerous direction:** it returns **0**
   when an `issued_to` carries **prose** rather than a bare serial — and this fabric writes prose
   `issued_to` routinely. **A zero from it does NOT establish that you hold nothing.**
3. **`list_task_orders` reads the BASE folder**, and lane TOs are not reliably in a lane folder — in
   some lanes there is no lane subdirectory at all and every TO sits flat in the base.

⛔ **AND THE DIRECTORY INSTRUMENT HAS A TRAP THAT CAUGHT THE SEAT WHO PRESCRIBED IT TO YOU.** I read
`ls <path> 2>/dev/null | wc -l` on a path that **did not exist** and got `0` — then offered that zero as
evidence. A MISSING directory and an EMPTY one return the identical answer, because the `2>/dev/null`
swallowed *No such file or directory*.
> **CLAUDE.md: "Never `2>/dev/null` a read whose EMPTINESS carries a verdict."**
> **A ZERO MUST NAME WHAT IT SCANNED.** `ls`, `grep`, `comp-find` and `--assignee` all return **0** for
> *"nothing there"* AND for *"I looked in the wrong place."* `comp-find` prints
> `0 hit(s) across N file(s) scanned` for exactly this reason — **N=0 is OUT-OF-CORPUS, NOT ABSENCE.**
**So: confirm the directory EXISTS before its count means anything, never suppress the error that would
say otherwise, and put your control on a path you have NOT already assumed is right** — my controls
fired (185, 397) and could not catch it, because both were on paths that exist.

⭐ **THE SOUND INSTRUMENT IS THE DIRECTORY**: an assignment is a file in a folder, and `ls` parses no
`issued_to`. ⚠ **But it is a sound ENUMERATION instrument and a blind STATUS one** — it tells you what
exists, not what is open. **A zero from it is strong; a non-zero is only a population.**

⚠ **AND A BARE-BASE TO BELONGS TO NO LANE**, so it reads as yours the moment you query your own
serial. Acting on one puts two projects on one instance — the Rule 27 violation this fence exists to
prevent (*one Tier-2 instance = ONE project; the protected resource is your context*).
⚠ **OPEN IS NOT UNFINISHED.** An `[ACTIVE]` face over completed work and a genuinely open TO render
identically — closing a face is the ISSUER's act and nothing does it automatically. **Do not infer that
a row still needs doing, and do not close one: it is not yours either way.**

