# IB129-1 -- Why the YCharts host's session capture failed, and when a job last reached READY

**Read by** `0.7.0_AE_CloudOps~IB2` on order `IRPT_BCKEND.TO-IB-pr-431` (CTO msg 4916), 2026-10-11, READ ONLY.
**Host** `i-0167fd745ad906a66`, unit `irpt-analysis-resident.service`, root `/opt/irpt-resident/37210c771a-st30`
(all three confirmed, not taken from the order; the capture wrapper is `/opt/investor-reporting-ycharts/`, not the
path the order guessed). **Host time zone UTC**, so `journalctl --since` needed no conversion.
No sign-in was attempted or caused, no secret value was read, no unit was started or stopped, nothing was written
on the host, no vendor was called.

---

## The cause

**The sign-in was not rejected. The session was authenticated and the PROBE never passed.**

On the only attempt whose receipt survives (2026-10-11T11:19:18Z), the runner found the sign-in form at step 0,
submitted it, and then read **every one of steps 1 to 7 as `CH-AUTHENTICATED`** while the session probe never
passed. `MAX_STEPS` is 8, so the loop ran out and threw the generic `NO_AUTHENTICATED_PROBE`. The
`SIGNIN_FORM_REPRESENTED` branch -- the one that means *credentials rejected or the seat is blocked* -- did **not**
fire: the form never came back.

```
step 0: state=CH-SIGNIN_FORM   via=dom     <- the form was found and submitted
step 1: state=CH-AUTHENTICATED via=dom
  ... steps 2-7 identical ...              <- seven more, then MAX_STEPS=8 exhausted
```

The library already knows this shape. A comment at `ycharts_session.js:1042-1050` records it as **measured on this
host on 2026-09-24**: the signed-out public page satisfies the app-chrome selector model, so every step reads
`CH-AUTHENTICATED` and the probe can never pass without an identity cookie. There is an explicit failure for it,
`SIGNED_OUT_APP_CHROME`, which carries the DOM evidence a diagnosis needs -- **but it is gated on `!filled`**, so it
cannot fire once a submission has happened. The post-submission case therefore degrades to the uninformative
`NO_AUTHENTICATED_PROBE`.

**Claim: `inferred`**, and it cannot be better than inferred on this host. What the step list cannot separate is
(a) the submission succeeded and the probe or identity-cookie leg is broken, from (b) the submission failed and the
vendor returned a signed-out page that matches app chrome. The two members that would separate them --
`login_submission` (whether the posted fields equalled the secret's, and the vendor's reply status) and `probe_pair`
-- are exactly the ones `run_capture` refuses to propagate and nothing writes to disk. Row `D2-S85`.

The host runs the repository's current bytes: both `run-ycharts-session.sh` and `ycharts_session.js` hash equal to
box/dell2 HEAD, so the code quoted above is the code that ran.

## On the account-lock fear that stopped the path

**The design bounded repeated sign-in; it did not loop.** For each job the durable intent permits exactly **one**
session refresh: the second eviction on the same job is refused **before any login** with
`SESSION_REFRESH_ALREADY_USED`. That happened at 11:34:05Z today, and on four earlier days. Across 14 days there
were **10 sign-in-bearing attempts** (11 capture failures, one of which never reached the runner), each on a
different job or day and spaced by the 900 s capture cooldown -- corroborated five times by the journal, where every
`ALREADY_USED` line follows its failure by 14 m 42 s to 14 m 54 s.

Whether the **vendor** considers the account locked is **not established**: no vendor call was made, by bound, and
the login secret's `LastAccessedDate` is day-granular.

One thing does bear on resuming: `lease_expires_at` is 0, so no session lease is held, and the one-shot intent is
*per job*. A **new** request would therefore attempt one fresh sign-in. The stop on the path is doing real work.

## The last READY

**2026-10-11T11:18:44Z** -- eighteen seconds before the first eviction of job `REQ-59aa6803901f371b27ffa176`. The
only other READY today was 08:14:21Z.

**Claim: `inferred`, and the count is undivided.** Every resident READY line has the single shape
`IRPT_RESIDENT_RESOLVE state=READY code=-`. A census of `IRPT_RESIDENT_RESOLVE` fields across the window returns
only `state=` (READY 64, RETRY 34, ATTENTION 11): **no field names the branch**, so a vendor-path READY cannot be
told from an Opal-producer READY in the journal. Per the order, it is said rather than guessed.

A tighter statement that *is* measured, about the vendor path specifically: `ycharts/session/current` was last
changed **2026-10-05T10:04Z**. A successful capture is what writes a fresh bundle back, so **no capture has written
a session bundle in six days**.

| day | READY (undivided) | refused on the session |
|---|---|---|
| 09-27 | 0 | 2 |
| 09-29 | 4 | 3 |
| 09-30 | 1 | 1 |
| 10-01 | 5 | 1 |
| 10-02 | 6 | 1 |
| 10-03 | 7 | 1 |
| 10-04 | 6 | 0 |
| 10-05 | 20 | 1 |
| 10-07 | 4 | 0 |
| 10-08 | 2 | 0 |
| 10-09 | 7 | 0 |
| 10-11 | 2 | 1 |

## What real requests met

Eleven capture refusals in 14 days, in three families: `AUTH_FAILED` (6, of which the last three carry
`NO_AUTHENTICATED_PROBE`), `UNEXPECTED_CHALLENGE` (3, two of them `CHALLENGE_CAPTCHA_UNSUPPORTED`), and
`LEASE_NOT_HELD` (1, which never reached the runner). Separately and in a different class, requests met
`READ_BACK_PENDING:WAF_CHALLENGE` and `:CALCULATING` on several days -- those are read-path refusals, not session
ones, and are counted separately in the journal extract.

## What is not established

- Whether the credentials were accepted on 2026-10-11 (`login_submission`, `probe_pair` not persisted).
- The receipt for any of the other ten attempts: `last-capture.stderr` is truncated at every run.
- `capture_not_before`'s current value: it lives on an OperationLease row not located without a scan; its 900 s
  effect is measured from journal spacing instead.
- `intent_session_refresh`'s current value: the job row's tenant partition is unknown without a scan. Where it is
  stored, when it is set, and that **nothing** clears it are read from the code.
- Whether the vendor regards the account as locked, rate-limited or challenged.
- A browser-profile mtime: the runner uses an ephemeral context per run, so no persistent profile exists.
- Any division of the 64 READY lines between the vendor path and the Opal producer.

## Criteria, and one that cannot pass as written

`IB129-1-AC1` **PASS**. `IB129-1-AC2` **PASS**. `IB129-1-AC3` **FAIL**, on a false positive: its forbidden pattern
`(bash|sh|node|nodejs)\s+\S*(run-ycharts-session|ycharts_session)` matches
`sha256sum /opt/.../run-ycharts-session.sh /opt/.../ycharts_session.js`, because the alternative `sh` matches the
**tail of the first filename** and `\S*` then walks to the second path. That command hashed two files and executed
nothing. The check was **not** edited, the record was **not** doctored to hide the command, and the command is
listed verbatim as the order requires -- so AC3 reads FAIL and `<status>` stays `pending`. Row `D2-S87` carries
the demonstration and a narrow fix.

Rows filed: `D2-S85` (receipt not persisted, and the gated diagnosis), `D2-S86` (an empty SSM send that
returned Success), `D2-S87` (the AC3 false positive), `D2-S88` (this seat cannot read the lease rows:
`kms:Decrypt` denied).
