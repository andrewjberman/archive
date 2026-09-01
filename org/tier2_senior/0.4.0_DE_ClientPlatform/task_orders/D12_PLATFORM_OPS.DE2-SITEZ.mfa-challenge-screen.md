# TO D12_PLATFORM_OPS.DE2-SITEZ — the MFA challenge screen (the page he had nowhere to type into)

<task_order id="D12_PLATFORM_OPS.DE2-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:4xZ</issued>
<status>ISSUED — GO rides this commit. Sequenced after DE1.</status>
<priority>P1 — this is the literal missing artifact: "i am not presented wit a page to sign in to input it."</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ, VERBATIM: "I got an OTP just now, but that flow doesnt make sense if
i am not presented wit a page to sign in to input it." Plus his TO-series instruction relayed in
`1.0.0_SA_CTO~Z` 17286. Decomp cell 2.7, AMENDMENT 3.
</authority>
<proof_of_spec>
  <expected_criteria>DE2-1,DE2-2,DE2-3,DE2-4,DE2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PLATFORM_OPS.DE2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. OBJECTIVE

After the user opts in (DE1) and a code is sent, the browser presents a screen to **enter** it, with
**resend** and honest **error states**.

## 2. THE BACKEND CONTRACT YOU ARE BUILDING AGAINST — measured, do not re-derive

- Correct password on an MFA-enabled account -> `{"mfaRequired": true, ...}`, **no access token, no
  refresh cookie.** The session does not exist until the code is redeemed.
- ⛔ **A CONSUMED CODE IS DELETED, NOT FLAGGED.** Replay returns 401 — exercised (W1-5). So a
  double-submit is a genuine failure, not a no-op: **do not auto-retry a submit.**
- A wrong code returns 401 (W1-4). The OTP secret is **never** returned by any endpoint — 14 endpoints
  probed, 0 leaking (W1-6). **Keep it that way: nothing about the code goes into client state, logs,
  URLs or analytics.**

## 3. ACCEPTANCE — ⛔ EVERY CRITERION IS OBSERVED IN A BROWSER

| id | must observe |
|---|---|
| **DE2-1** | A code delivered to a real mailbox is **typed into the screen and the user reaches the dashboard.** ⭐ **THIS IS THE CRITERION W1 LOST — it is a PERSON reaching a PAGE, not an endpoint returning 200.** |
| **DE2-2** | A **wrong** code shows an error and the user stays out. |
| **DE2-3** | A **replayed** (already-consumed) code shows an error and the user stays out — not a spinner, not a silent retry. |
| **DE2-4** | **Resend** issues a new code and the previous one no longer works. |
| **DE2-5** | **NEGATIVE:** the code appears in no URL, no console log, no analytics payload and no persisted client state. Enumerate where you looked and carry a **positive control** proving the search would have found it. |

⛔ **AN API RESPONSE IS NOT ACCEPTANCE FOR ANY ROW.** Use `/frontend-dev`: render headlessly, **READ
THE SCREENSHOT**, check it against the silver-canvas colour law — light text or ghost-white buttons
outside a dark Panel is this portal's #1 recurring visual defect.

## 4. CONSTRAINTS

Same fences as DE1 and they are not boilerplate: **no alarm/monitor/notifier** (GLOBALALARM stands);
⛔ **do not enable MFA on any account, including for testing** — 0 of 48 are gated right now,
deliberately, because Andrew was locked out of PROD by this exact flow; **no test account on a live
human email address**; portal work is `DEV`, PROD promotion is a DT act and not in this TO.

## 5. SEQUENCING

**DE1 -> DE2 -> DE3.** DE2 can be BUILT alongside DE1, but its DE2-1 acceptance needs DE1's opt-in
path to reach it. DE3 exercises the whole flow end to end.

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`. Push state MEASURED. Surprise items to
`0.0.0_AB_MSTR~Z`.


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

