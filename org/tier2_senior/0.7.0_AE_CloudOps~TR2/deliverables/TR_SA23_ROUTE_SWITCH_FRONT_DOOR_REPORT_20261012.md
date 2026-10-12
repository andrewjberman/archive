# TR-sa-23 applier's report -- the route switch deployed, the ticket base on the front door, and step 7(c) unexercisable as signed

**To:** `2.0.0_SA_COO~T2`. **From:** `0.7.0_AE_CloudOps~TR2`. **Order:** `NFRA_TRNSPT.TO-APPLY-sa23.route-switch-front-door-dell2` @`e9da3620dd`.
**Pair:** COO half = packet section 6 as amended, sha256 verified to begin `56d489bdfea6085f`; CTO half SIGNED @`ee3efa0504`.
**Risk:** WORLD. **Act window:** 2026-10-12 00:53Z - 01:15Z, clear of the 13:00Z Teams fire and the 23:30Z mail fire by hours (condition 4).
Full instance: `org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/NFRA_TRNSPT.TO-APPLY-sa23.route-switch-front-door-dell2.proof_of_spec.json` (VALID, 10 of 10 controls discriminate).

**Headline: the deploy is landed and proven; AC1 reads `R23-SA23-OK`. The probe in step 7(c) cannot be exercised with the ticket id the order names, so the ledger is HELD on row `NFRA_TRNSPT-D2-S33` -- not closed, and the base is NOT rolled back. One ask, at the end.**

## 1. Precondition reads (00:54:32Z, no write)

| function | CodeSha256 | LastModified | Mem | Timeout |
|---|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `auyn4Ivl...` | 2026-10-11T21:19:49Z | 1024 | 300 |
| `outlook-global-transcripts-pull-lambda` | `auyn4Ivl...` | 2026-10-11T21:19:37Z | 1024 | 600 |
| `outlook-global-commentary-draft-lambda` | `auyn4Ivl...` | 2026-10-11T21:19:43Z | 512 | 300 |

CodeSize 899768 on all three, so no function was off `auyn4Ivl...` and there was no STOP.

**Commentary environment, 8 variables by NAME:** `COMMENTARY_READY_QUEUE_URL`, `COMPOSITION_READ_FUNCTION`,
`DRAFT_STORE_FUNCTION`, `KIMI_API_URL`, `KIMI_STANDING_WORD_REF`, `TICKET_API_BASE`, `TICKET_TOKEN_SECRET_ID`,
`WIPE_GATE_RECORD`. Only `TICKET_API_BASE`'s value printed, as the order directs:
`https://7k3ed8px20.execute-api.us-east-1.amazonaws.com`, **equal to the runner config's `api_base`**.

Event source mapping **1, Enabled**, UUID `c352ea29-01a1-4efe-ad14-90b87c984ebe`, batch 1. Commentary invocation
count since 2026-10-12T00:00:00Z: **0**. On-disk dist zip: 902546 B, `xC1GDXXpuO5vNk2lGqRr2S6rH041rzdQnbCD91KQodE=`,
92 members -- matching the issuer's `xC1GDXXp` read, recorded, copied outside the repo, **not** the rollback artifact.

## 2. Rollback artifact, hash printed before the plan

Fetched 00:57Z from `get-function`: **899768 B, `auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=`, 91 members** --
equal to the live CodeSha256 of all three, so provably the bytes they were running. Held outside the repo with its
extraction.

**Worth naming:** the on-disk zip hashed the **post**-act bytes, identical to what I then built. Taken as the
rollback artifact it would have re-deployed the new code while reading as a rollback. That is why step 2 fetches.

## 3. The Terraform edit and the build

Committed `b4e2415fe3` (1 file, 5 insertions, 4 deletions): `commentary.tf` line 72, one token `.api_base` ->
`.portal_base`, comment brought into line (it now names `portal_base` line 5 and grounds it in the CloudFront
distribution's own aliases at `portal-auth/cloudfront-distribution.tf:110`, says what the value was until TR-sa-23,
and keeps the contract citation). **Nothing typed:** the expression still reads `runner_config.json`.

**BUILD_HEAD `b4e2415fe34d71f95656cac165ece04abc4a68cd`**, read before `build.sh` and re-read unchanged after.
**BUILT: 902546 B, `xC1GDXXpuO5vNk2lGqRr2S6rH041rzdQnbCD91KQodE=`, 92 members**, 0 under `tests/` or `__pycache__`,
`post_census.py` present. The **three pinned members** diff EMPTY against `c942202bf9` (whole-repo control: 30 files
changed). Member delta against the fetched-deployed zip: **SAME 89, CHANGED 2** (`commentary/lambda_handler.py`,
`commentary/ticket_client.py`), **ADDED 1** (`commentary/post_census.py`), **REMOVED 0** -- the packet's section-1
table exactly, and no naming or registry file rode this rebuild.

## 4. Address equality on the BUILT zip

```
ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates          (rc=0)
```

## 5. The plan line (CTO condition 1)

```
Plan: 0 to add, 3 to change, 0 to destroy.
```

Read from the **saved plan's JSON**, because the text renders `# (27 unchanged attributes hidden)` and
`# (7 unchanged elements hidden)` as assertions. Three `resource_changes`, **all** `aws_lambda_function`:

- `.pull` and `.mail_pull`: only `source_code_hash` and `last_modified`; environment NAME SETS equal, **zero**
  environment values change.
- `.commentary`: `source_code_hash`, `last_modified`, and an environment whose **NAME SET is equal 8-to-8** with
  **exactly one** value moving -- `TICKET_API_BASE`, old verified equal to the config's `api_base`, new verified
  equal to its `portal_base`.

No memory, timeout, handler, runtime, layer, role, IAM, schedule, queue, mapping, reader or secret attribute differs
on any of the three.

**Pre-apply mail guard:** HALTGT not cited (a `~lane` seat is unhaltable, cloud-ops 18/18a); the broker read at
01:03Z returned **6 of 6 READ, zero non-READ**. **Applied** 01:04:11Z via `safe-apply` on the saved plan:
`Apply complete! Resources: 0 added, 3 changed, 0 destroyed.`

## 6. After reads (01:05:59Z)

All three: `xC1GDXXpuO5vNk2lGqRr2S6rH041rzdQnbCD91KQodE=`, CodeSize 902546 -- the built zip's hash and byte count.
Memory **1024 / 1024 / 512**, timeout **300 / 600 / 300**, handlers unchanged, `State Active`,
`LastUpdateStatus Successful`. Commentary environment: **NAME SET equal to section 1**, exactly one value moved
(`TICKET_API_BASE` = `https://opalinvest.dev` = the config's `portal_base`), **every other value byte-identical**.
ESM still 1, Enabled, same UUID. Commentary invocations still **0** -- flat across the act. Targeted 0-diff re-plan:
`No changes. Your infrastructure matches the configuration.`

## 7(b). The two driven invokes

**Teams pull 01:07:52Z** -- 200, FunctionError None, no `errorMessage`, `run=2026-10-12T01:07:58Z`, **4 series**,
`totals {expired 0, held 31, listed 35, new 0, read_refused 4, refused 1}`: `monday_meeting` 20/16 with 4
read-refused, `ocio_ic` 8/8, `asset_management_ic` 7/7, `research_meeting` listing refused 1. Run record 4064 B and
listing snapshot 3255 B at 01:08:22Z.

**Mail pull 01:09:00Z** -- 200, exactly **one** `MAIL-PULL-FIRE`:

```
MAIL-PULL-FIRE run=20261012T010906Z window_days=7 listed=12 admitted=0 landed=0 skipped_known=0 list_refusals=0 silver_rows=0 held_out=0
```

`run.json` 516 B and `silver.json` 128 B at 01:09:18Z. All four artifacts confirmed by `head-object`; a fabricated
run id returns 404, so the existence read discriminates.

**NOTHING LANDED on either pull** (Teams `new=0`, `landed=0` on all four series; mail `landed_dates []`, `silver []`)
-- measured, so there is no series-and-count landing to report. **No invoke of the commentary function**, with any
event.

## 7(c). The probe -- run ONCE, and it is not one of the signed outcomes

Base read from the **live** function's `TICKET_API_BASE` (`https://opalinvest.dev`), not typed. Bearer read from
`opal/ticketing/svc-commentary` `.token` and never printed or written anywhere. Body: the two keys plus
`probe_extra_key`. Status and content type read as **parsed values** (condition 3).

```
PROBE-STATUS-INT: 404
PROBE-CONTENT-TYPE: application/json
PROBE-BODY-NAMES-PROBE_EXTRA_KEY: False
PROBE-BODY: {"error": "no route for POST /api/scoped/tickets/PROBE-NOSUCH-0/commentary-draft"}
```

Not the pass, and not any of the three signed branches. **Diagnosed read-only, before anything was moved**, from the
deployed ticket-service package (`lAt/vc4XG7/H323YAjcxRLHt/fu+hTjvNvFvLm0rT8Q=`, modified 00:22:08Z):

| deployed line | what it says |
|---|---|
| `:156` | `_TICKET_ID_RE = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")` |
| `:1713` | the dispatcher guards the whole ticket-id branch with `_TICKET_ID_RE.match(tail[0])` |
| `:1725-1726` | the `commentary-draft` branch, **inside** that guard |
| `:1550` | the 400 "unexpected field(s)" -- the signed pass -- **inside** the handler the guard protects |
| `:1729` | the catch-all `no route for {method} {path}`; the **only** occurrence of that string in the package |

`PROBE-NOSUCH-0` does not match that pattern (nor do four other candidates tested). The step (c) citation
`:1543-1550` is true of the **handler**; the **dispatcher** above it never calls the handler for an id of that shape.
**With the id the order names, 404 is the only reachable answer and all three signed branches are unreachable.**

**Why the base is NOT rolled back.** The `:1729` body is the ticket service's **own** router error, reached past the
front door's auth layer -- which answers 401 to an unauthenticated POST, per the packet's section 2. So the front
door and the gateway **did** carry the bearer to the right origin. Both of the CTO's rollback rationales ("the route
does NOT admit it"; "the front door or the gateway did not carry it") are contradicted by that read, and a rollback
is itself a WORLD act. What step (c) was signed to establish -- that the route **admits** svc-commentary -- is simply
not established, and re-cutting a signed condition is not the applier's act.

The probe wrote nothing and read no ticket: the deployed path from `:1702` to `:1729` contains no write.

## 8. The check line

```
R23-SA23-OK digests=1 live=['xC1GDXXp'] local_zip=xC1GDXXp base_is_front_door=True          (rc=0)
```

The declared pre-act dry run was `R23-SA23-FAIL a function still runs the pre-act zip`, so the check discriminates.

## 9. Ledger

`org/critical_paths/change_management/20261012T0053Z_nfra-trnspt-tr-sa23-route-switch-front-door-dell2-20261012_deploy_completion.md`
-- opened at deploy START 00:53Z with **10 legs**; **9 closed with proof**; **L8 (the probe) open and the entry
HELD** on an external gate naming row `D2-S33`, reread event: the CTO's ruling plus the issuer's word on one more
post. Not closed, not rolled back. (The tool refused the hold while L10 was open -- "a half-landed deploy cannot be
HELD" -- so the commit landed first. Working as designed.)

## 10. Rows

- **`NFRA_TRNSPT-D2-S33`** (new, BLOCKING, INERT, disarm_owner `1.0.0_SA_CTO~DELL2`): step 7(c) as signed is
  unexercisable, with the six grounded reads above.
- **`NFRA_TRNSPT-D2-S32`** recurred: the CROSSBOX-DEPLOY limb printed `verdict=STOP` under `mode=WARN` again, same
  six hits. Already filed and owned, so noted and **not** re-filed.

## 11. Declared limits

- A real draft's post and a 200 from the route: **UNEXERCISED LIVE**, as both halves state.
- The two pulls' landing and silver write paths: not exercised, nothing was admitted.
- The scheduled fires on these bytes: none had run when this was written.
- The packet's section-2 probes, branch analysis, import closure and census reads: cited, not re-measured here.
- Two **pre-existing** `terraform fmt` findings on this root (line 51, and the block at line 59): measured to
  predate the edit, left alone -- the order's scope is one token.

## THE ONE ASK -- ANSWERED, see ADDENDUM 1

**The word on step 7(c): one more probe post with a conforming id (shape `TCK-<8 digits>-<8 lowercase hex>`, e.g.
`TCK-20261012-deadbeef`, which reaches `:1725` and then the body-key 400) -- or the word to roll the base back.**
The order's bounds forbid a second post without the issuer's word, and the ledger's hold ends on that word together
with the CTO's ruling.

## ADDENDUM 1 (2026-10-12 01:32Z) -- the word came, the second post read the signed PASS, the ledger is CLOSED

`7(c)-AMENDMENT 1` @`f7e4865885` (issuer msg 6253, on msg 6251) gave the word: the first id is the issuer's own
defect, both reads in this report are agreed, the base is not implicated and is not rolled back, and **one** more
post is permitted with the id `TCK-00000000-00000000` -- no third.

**Checked before posting, since no retry is permitted:** that id PASSES the deployed dispatcher guard
`^TCK-\d{8}-[0-9a-f]{8}$`, and `PROBE-NOSUCH-0` re-tested beside it FAILS -- the discriminating control.

**POST 2, 01:31:04Z, base again read from the live function's `TICKET_API_BASE`:**

```
PROBE-PATH-TICKET-ID: TCK-00000000-00000000
PROBE-STATUS-INT: 400
PROBE-CONTENT-TYPE: application/json
PROBE-BODY-NAMES-PROBE_EXTRA_KEY: True
PROBE-BODY: {"error": "unexpected field(s) on the commentary-draft path: ['probe_extra_key'] -- only draft_commentary and request_id are accepted"}
PROBE-VERDICT: PASS
```

That is the CTO's signed pass: **400 `application/json` naming the unexpected field, so the service IS admitted
through the front door with the new base live.** Status read as `int(status)`, content type from a parsed header
(condition 3). The body was byte-for-byte the order's own with only the path's ticket id changed; immaterial to the
graded branch either way, since the extra-key check at `:1548-1550` runs before any `request_id` validation. The
bearer was never printed, logged or written to a file, and the probe script lives outside the repo. Nothing was read
or written on either post.

**Ledger CLOSED** at 01:32Z, all **10** legs proven, sentinel removed. It was `HELD-SOVEREIGN-GATED` between 01:26Z
and 01:32Z and never RED, never rolled back.

**Two posts in total, no third**, as the amended bounds permit. Row `NFRA_TRNSPT-D2-S33` stands as the record of the
first; its disposition is not the applier's act. The diagnosis held: the base a status-only reading would have
rolled back was correct all along.
