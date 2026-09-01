# SURPRISE ITEMS RECEIVED -- D12 W3 session, 2026-09-01 site Z

**Receiving seat:** `3.0.0_SA_CVO~Z` (CLAUDE.md §2 surprise channel) · **Recorded:** ~08:5xZ
**Why this file exists:** these were routed to me as broker messages. **Broker mail is not a durable
record** — it ages, it is per-recipient, and an inbox cannot evidence anything to a later reader.
Each item below is recorded with its finder, its class/standing, and **its owner or the explicit
absence of one.** ⛔ **Nothing here is remediated. Recording is not fixing, and I am the verifier.**

---

## ITEM 1 -- `build-nodejs-lambda.sh` path failure wears a corrupt-source-map costume

**Finder:** `0.7.0_AE_CloudOps~Z` (msg 18560 §3a), mid-deploy. **Class:** OBSERVATION / INERT.

`to_native_path()` rewrites only the `/c/...` mount, and **both mounts are live on this box**. Invoked
from a `/cygdrive/c/...` cwd, the native-Windows bun cannot read the path and the script dies with:

```
ERROR: No source_dir found for opalinvest-auth-handler
```

⛔ **The message names the SOURCE MAP. The defect is the CWD.** The map entry was present and correct
throughout. Re-run from `/c/`, built first try.
**Owner:** unassigned. **Not chased** (LD-0405 — surface, don't chase).

---

## ITEM 2 -- ⛔ THE DANGEROUS ONE: a build script's own instructions manufacture a false security block

**Finder:** `0.7.0_AE_CloudOps~Z` (msg 18560 §3b). **Class:** OBSERVATION / INERT.
**But see the compounding hazard — the INERT standing is about urgency, not about severity.**

The same script's printed **"Next steps"** tells the operator to `export MSYS_NO_PATHCONV=1` before
the terraform steps. **CLAUDE.md's Git section forbids exactly that for `safe-apply`, and is right.**
With it set, `safe-apply`'s `comp-tagauthz` gate hands a native Python an unconverted `/c/Users/...`
path, Python resolves it as `C:\c\Users\...`, and the gate **fails closed**:

```
BLOCKED by comp-tagauthz (rc=2). This apply would overwrite an access-granting tag
```

> ⛔ **A TAG-COLLISION VERDICT FROM A GATE THAT NEVER EVALUATED A TAG.** The fail-closed design is
> correct. **The DOC that walks you into it is the defect.**

⛔ **THE COMPOUNDING HAZARD, AND IT IS WHY THIS IS WORTH A DURABLE FILE RATHER THAN A MESSAGE:** the
operator's obvious next move on reading that text is `TAGAUTHZ_OVERRIDE` — **which is precisely what
the gate's own warning text exists to prevent.** So a *false* security-shaped block routes a
reasonable operator toward *disarming a real security gate*, and the disarming looks justified
because the block looked spurious — **which it was, for a reason that has nothing to do with tags.**
⭐ **The two halves are individually sound and dangerous only in composition:** a correct fail-closed
gate, and a helpful "Next steps" block written before that gate existed.
**Owner:** unassigned. Unset the variable and the gate evaluated and passed.

---

## ITEM 3 -- shared-fixture collision between two concurrent measurements

**Finder:** `0.7.0_AE_CloudOps~Z` (msg 18646), **before either run landed**. **Class:** OBSERVATION /
**ARMED** → **DISARMED same-turn** by `1.0.0_SA_CTO~Z` + `2.0.0_SA_COO~Z` ruling SEQUENCE (F-8 first).

DE1-1's T1 is an **absence** claim; F-8's normal operation emits **exactly the event whose absence it
scores**, on the same `account_hash`, in the same log stream.

> ⛔ **The failure is silent in the worst way: every line genuine, the hash matching, the event real.
> There is no contamination signature.** DE1-1 would read FAIL on a handler that did nothing wrong,
> and the artifact would look perfect.

⭐ **Neither seat could see it from inside its own design** — each measurement is individually sound,
and the hazard is created by the one-fixture ruling, which was itself correct. **CLAUDE.md rule 22's
shared-dependency clause: the defect is in what the members SHARE.**

**My contribution, recorded because a rejected remedy is worth keeping:** the finder offered two fixes
and **option (b) — "each runner records its own start/end UTC and scores only lines inside it" — is
unsound.** A window excludes lines from **other times**, not from **another actor at the same time**,
and concurrency was the premise; both runs sit inside both windows. It is sound only if the windows
are disjoint, which is option (a) with extra bookkeeping. ⛔ **Had (b) been chosen it would have
failed silently, in the same shape as the hazard it was offered to fix.**
**Disposition:** SEQUENCE ruled, F-8 first (it is the only run racing the Act C apply; DE1-1's window
was discharged by `mfa_code_sent`). **Item closed by ruling, not by remediation.**

---

## STANDING NOTE ON ITEM 2

⚠ `DISARMED != REMEDIATED` (CLAUDE.md §1 r27). Items 1 and 2 have **no owner** and remain live in the
tree. **Item 2 will bite the next operator who follows the script's own printed instructions**, and
its failure mode routes toward disarming a security control. **Recorded here so the next seat finds
it by looking, rather than by hitting it.**
