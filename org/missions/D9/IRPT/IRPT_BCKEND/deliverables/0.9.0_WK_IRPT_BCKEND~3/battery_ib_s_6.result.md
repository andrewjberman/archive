# `battery_ib_s_6.result.md` -- S6-AC1, seven arms, 7 of 7

**TO:** `IRPT_BCKEND.TO-IB-s-6` | **cell:** `IB-s-6` (PRD cell B6) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-1-3` | **worktree:** `/c/tmp/wk-irpt-1-3` | **base:** `95a34541f8`

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_6.py
```
**rc 0. Last line: `IBS6-INTAKE-DURABLE`. Full verbatim output:
`.../IB-s-6_S6-AC1_battery_output.txt`.**

---

## (a) PERSIST BEFORE CHECKPOINT -- the difference control, three runs

| run | kill point | checkpoint after the kill | killed message on restart |
|---|---|---|---|
| 1 | after attachments+receipt, **before** the mark | `None` (never advanced), message claimed = `False` | re-read; distinct objects **3 -> 3, DUPLICATES 0**; put calls 3 -> 6 (a byte-identical overwrite of the SAME key); checkpoint then advanced |
| 2 | after the mark, **before** the checkpoint | `None` | outcome `ALREADY_COMPLETE`, **NEW writes 0**, 4 requests created for the four messages the kill never reached, 1 already-complete; checkpoint then advanced |
| 3 | CONTROL: kill **after** the checkpoint advanced | advanced to `...deltatoken=final1` | **second scan re-read 0 messages and added 0 put calls**; checkpoint moved on to `...deltatoken=final2` |

The keys are derived from the message IDENTITY, which is what makes a re-read *harmless*
rather than merely survivable: run 1 wrote the same three keys again and the object set did
not grow. `InjectedKill` derives from `BaseException`, so no `except Exception` in the code
under test can absorb an injected crash and turn it into a handled error.

## (b) DELTA, PAGINATION, RESYNC, RETRY-AFTER -- `4 of 4`

- **pagination:** 3 pages, 5 messages, order matches the fixture chain exactly
  (`AAMk-49f-0001, AAMk-spoof-0002, AAMk-cot-0003, AAMk-opal-0004, AAMk-49f-0005`).
- **deltaLink persists:** stored as `.../messages/delta?deltatoken=final1`.
- **delta expiry -> resync:** a scripted `410 syncStateNotFound` against a held token produces
  `resyncs=1`, `resynced=True`, and the scan still returns all 5 messages. Declared behaviour, in
  code and printed: *discard the token and replay from `IRPT_INITIAL_CUTOFF=2026-09-01T00:00:00Z`,
  exactly once per run* -- a second resync in one run propagates, because a token that expires
  twice in one run is not a token problem.
- **Retry-After honoured:** a scripted `429` with `Retry-After: 7` gives
  `waits=[7]`, the injected clock recorded `[7]`, and all 5 messages arrive after the wait.
  Ceiling 300s, at most 3 retries, then `ThrottleExhausted` -- terminal and loud, with the
  checkpoint unmoved so the next window re-reads the same scan.

## (c) ONE REQUEST PER FORWARD; A NEW REQUEST FOR IDENTICAL HOLDINGS

- first delivery: 5 messages -> **5 requests**; the SAME messages delivered again:
  5 messages -> **0 new requests, 5 already-complete**; **queue sends across both deliveries: 5.**
- byte-identical holdings, two different messages:
  `att-0001.bin` and `att-0005.bin` have the same sha256 (`bytes_identical: true`), and the
  request ids are **`REQ-ae07aabff2062559d9d7904c` vs `REQ-87f5609a510bb1701f8be9c2` -- distinct.**
- keyed on **message IDENTITY** (`internetMessageId`, falling back to the mailbox `id`),
  **never a content hash alone**: a content hash would collapse the second case, which is a real
  advisor's real second request.

## (d) THE ORIGINAL SENDER, NOT DISPLAY From

| case | display From | VERIFIED original sender | gate |
|---|---|---|---|
| display From is a FIRM domain, the original is not | `advisor@49financial.com` | `stranger@unknown.example` (`FORWARDING_ARRANGEMENT_HEADERS`) | **Quarantined** -- "sender domain 'unknown.example' matches no enumerated firm and is not the Opal domain" |
| the inverse: display From is the forwarder | `requests@opalinvest.com` | `advisor@49financial.com` | **BoundRequest**, `firm_id=49financial` |

`display_from_used` is `False` in both -- the display From is read only to RECORD the
disagreement, never as proof. Verification requires `Authentication-Results` showing
`dmarc=pass` **AND naming that same domain**: `dmarc=pass` alone would verify the *forwarder*,
which passes DMARC on every message it forwards, and call it the advisor.

## (e) LANDS ONLY WHERE THE POLICY SAYS -- `14 of 14`

Enumerated prefixes, **read from the policy, not typed**: `firms/49financial/intake/`,
`firms/cottonwood/intake/`, `firms/inflection/intake/`, `quarantine/`.
Keys written 14, inside 14, **outside 0**. Per prefix:
`{49financial: 6, cottonwood: 3, inflection: 0, quarantine: 5}`.

**Negative fixture** (a cross-firm destination while bound), verbatim:
`destination_for: requested firm 'cottonwood' does not match the bound firm '49financial' -- a
write into a second firm's location is refused before any key is built`.

Two independent arms hold this: the gate refuses in-process **before a key is built**, and the
poller re-checks at the write (`_assert_inside`) that the key it is about to put is still under
the prefix the policy returned.

## (f) THE INSPECTION IS RECORDED

Printed from `infra/aws/lambda/investor-reporting/intake/ib_s_6_graph_inspection.md` (8451 bytes,
10 artifacts read and tabulated):

- **permission model found in the gateway: `DELEGATED`** (`graph.py`'s own docstring: *"Every call
  uses a specific user's delegated token"*).
- **one-mailbox `Mail.Read` grant: `UNVERIFIED`** -- and unverified because nothing in this estate
  establishes it, not because the read was skipped. `Mail.Read` IS present, as a *delegated scope*.
  Even the fixed-mailbox endpoints (`/otp/fetch`, `/ms/*`) use a server-held delegated token for a
  named human.
- **no `ApplicationAccessPolicy` anywhere in the corpus** (unscoped `comp-find`; the only
  first-party hit is the BD runner's CTO-ruled design comment, which says the mailbox is TBD and
  never landed). The brief's own boundary table: *"actual application permissions must be
  established"*.

## (g) NOTHING LEFT THE MACHINE; THE SCHEDULER IS DISABLED; THE LEDGER CLOSED

- **netguard (offline subprocess): 0 external of 0 connection attempts.** The denominator is zero
  because the suite opens **no socket at all** -- the recorded transport reads committed fixture
  files. A 0-of-0 refusal count is **vacuous on its own**, so the **POSITIVE CONTROL** is the
  load-bearing evidence: `graph.microsoft.com:443` attempted -> `refused=True`, guard external
  count `0 -> 1`, message `NETGUARD: refused external connection to graph.microsoft.com:443`.
- **served bytes:** `CodeSha256 = JbZrYN+jgVMNxU428sahOsan6ngXAUNHp555x9gnap0=`, **equal to the
  zip rebuilt from the worktree source** (49281 bytes, 28 members) **and to the source-map
  registration**. Verified by CONTENT, never by filename. `Layers: None`.
- **scheduler:** `get-schedule --name irpt-intake-poll -> State: DISABLED`,
  `cron(0/15 8-23 * * ? *) America/New_York`.
- **ledger:** `20260911T0149Z_irpt-bckend-s6_deploy_completion.md`, `CLOSED=True`, 6 legs declared,
  0 open-leg markers, sentinel absent, committed at `61fbbd22ae`.
  **DISCLOSED by the battery itself: `sentinel ever committed = False`** -- see row
  `IRPT_BCKEND-W3-S4`.

---

## Controls

**MUTANT -- two, both fired.** The central claim of arms (a) and (c) is that the **conditional**
completion mark is what makes a re-read a no-op. Removing exactly that, by monkeypatch, in a
process that edits no production file (`IB-s-6_mutant_control.py`, output
`IB-s-6_mutant_control_output.json`):

```
baseline                          first 5 requests, second 0 new, 5 already-complete, 5 sends -> predicate HOLDS
M1  is_complete always False      second 0 new but already_complete 0                        -> predicate BREAKS
M2  mark written unconditionally  second 5 NEW requests, 10 queue sends for 5 messages       -> predicate BREAKS
```

M2 is the sharper one: dropping the conditional write produces **ten queue sends for five
messages** -- the duplicate-request failure the acceptance clause exists to forbid. The battery
can therefore be observed failing on this exact claim.

**DETERMINISM.** Two full battery runs on the same inputs: **88 lines, byte-identical, zero
differing lines.** Both printed `IBS6-INTAKE-DURABLE` at rc 0. There is no ephemeral port here
(the suite opens no socket) and no timestamp on any deciding line, which is why this run is
byte-stable rather than merely verdict-stable.

## What this battery does NOT establish

- **The fixtures are SYNTHETIC.** No real forwarded specimen exists anywhere in this repository --
  the cell itself records the gap. A green arm proves the poller handles THIS model of a forward,
  not that a real forward looks like it. What a real one could carry that these do not is stated
  in the S6-AC3 judgment.
- **No mailbox was read, and none can be**: the application permission does not exist and
  `LiveTransport` refuses to construct on three independent grounds.
- **The schedule has never fired** and enabling it is the qualified live arm.
