# HANDOFF — `1.0.0_SA_CTO` base, D2 & D3 — 2026-08-30 18:3xZ context reset

**Written for a successor who was not here.** Andrew ordered a clean context reset and alignment check
(18:2xZ, verbatim: *"issue an edict to all underlying agents on the D2 D3 work to /log and prepare for
closure, because I believe a clean context reset and alignment check would be beneficial for these
continued works"*). Edict delivered to 9 D2/D3 seats, 9 of 9 (88943–88951).

⛔ **THIS IS A PAUSE, NOT A STAND-DOWN. His words are "these continued works".** Nothing is cancelled,
no project is closed early, no scope is narrowed. **The `org/XXX.md` carrier clause is deliberately left
UN-STRUCK** — the same call `1.0.0_SA_CTO` made at the 2026-08-29 21:40Z wind-down, and he confirmed it
the next morning by ordering a re-arm *from that clause*.

---

## 1. HOW TO RE-ARM (read this first)

1. **The only thing you may re-arm from is the `org/XXX.md` Step 1b-F carrier clause** for
   `1.0.0_SA_CTO` (skill §0.4). Never off memory, never off a log alone. **Verified LIVE at 18:2xZ this
   session** on comp-find, which returns `DENOMINATOR: 2 hit(s) across 1 file(s) [corpus=all]` and finds
   **both halves of the drive pair** -- the CTO row 633 and the COO row 634.
   ⛔ **USE `comp-find 'self-drive D2 & D3' org/XXX.md`, NEVER grep** (Andrew-direct 2026-08-30:
   *"comp-find not grep"*, *"comp-find is far superior to grep"*). A line-grep filtered on the serial
   finds NEITHER row and returns clean-empty, which reads as *no carrier exists* -- that false alarm was
   raised and retracted in this session. **grep cannot distinguish a wrong pattern, a wrong path, a wrong
   corpus and a true absence; comp-find's denominator can.**
2. The clause carries: scope `D2 + D3` **re-resolved from the register every tick** (a predicate, never
   the arm-time list), cadence 30m at :07/:37, `paired_with: /drive D2 & D3 @ 2.0.0_SA_COO (+15m, :22/:52)`,
   verdict ledger `org/tier1_exec/1.0.0_SA_CTO/drive_pairs/D2-D3/VERDICTS.jsonl`, and the stop-condition
   (DONE per §4 / HELD-AT-STOP / his stand-down → strike, covering BOTH halves).
3. **Tick state is scratchpad-only and dies with this session.** Re-derive it from the latest committed
   self-drive log (§5). **This session ended at tick 103**; the last committed log is
   `logs/2026-08-30/self_drive_D2-D3_tick102.md`.
4. The clause still reads *"resumes at tick 69"* from the 00:20Z relaunch. That is stale as a counter and
   harmless — the log is the counter's source of truth, not the clause.

## 2. WHERE THE WORK IS

**Completion: 2 of 10 (10 register members + 0 claims). REACHABLE 10 / UNREACHABLE 0.**
Complete: `ADVI_BDPLAT_RESTORE`, `ADVI_49FSRC` (closed today on Andrew's card 4).
Open TOs: 26 (D2 22 / D3 4).

**D3 is blocked on an external party and cannot be unblocked from inside.** `D3_MODELOVERLAY` carries a
`NEEDS-SOVEREIGN-CALL`: *is the 49F SmartX feed scoped to the 49F Schwab book, or to the 49F book
regardless of custodian?* Both branches turn on who custodies 13 accounts holding $12,293,768.23, and
**the estate provably cannot answer** (the only custodian-name carrier is dead: 46 of 47 partitions
empty). Andrew approved asking 49F; **that outreach is his act, at his relationship, on his timing.**
⛔ **No seat contacts 49F.** Do not treat the absence of an answer as a reason to pick a branch.

**D2's live constraint worth knowing:** `ADVI_INSURE`'s silver converter was built ahead of a producer
capability requiring 77 vendor calls per fire against a 12.7 s baseline — a **widened Black Diamond
egress that was never authorized**. The issuer refused it. Do not "fix" this by building the fan-out.

## 3. WHAT IS OWED, AND BY WHOM

| owed | by | to |
|---|---|---|
| W2 vendor pull -- **FIRED 18:3xZ and FAILED AT AUTH; see below** | `0.4.0_DS_ClientPlatform~C` | ADVI_BDPARITY |
| TO-R1-DS correction -- **HOLD LIFTED 18:3xZ**: `3.0.0_SA_CVO` 88973 ruled *YES, amend*, five conditions | `0.4.0_DS_ClientPlatform~R` | proceed under those conditions |
| register ruling on the completed-member convention | `0.0.0_AB_MSTR` | asked at 88774, still open |
| 4 unpushed commits at this seat | this seat | ride the next integration window |

⛔ **W2 IS AUTHORIZED AND MUST NOT BE GATED ON THE RESET.** Andrew spent the vendor word at 18:0xZ
(*"recs approved for each"*). CLAUDE.md forbids converting his word to one agent into a gate on another.
**The word is SINGULAR: W1 skipped, W2 only, performance endpoint only.** A second pass after a
*completed* run is a SECOND ask, not a retry.

⛔ **BUT THE WORD IS NOT SPENT — W2 FIRED AND DIED AT AUTHENTICATION, UPSTREAM OF ANY DATA CALL.**
`RuntimeError: BD GET /session/token -> HTTP 401` at `run()` line 410, before the account loop.
**Measured against the world, not the error text:** bronze `reporting_performance/2026-08-30/` still holds
exactly the five keys from the 03:05Z P1 probe -- **0 data calls, 0 accounts pulled, 0 objects landed.**
The 49F `.bd.identity` cookie in Secrets Manager `blackdiamond/49f/session` is expired; it authenticated
at 03:05Z and 04:35Z today and has lapsed since.
⛔ **DO NOT ESCALATE A HUMAN BD LOGIN, AND DO NOT RETRY.** `0.4.0_DS_ClientPlatform~C` initially reported
that a human login was required, then **WITHDREW the claim** (88996, successor log corrected
@`73305dcd10`) -- it was inferred from a module comment, not measured. `0.7.0_AE_CloudOps` read the
trigger at source: `bd-49f-session-trigger` probes the token URL LIVE and is **fail-safe to MINT** on a
negative probe, so the **04:35Z fire should re-mint rather than skip**. Neither story is established --
that mint leg is UNEXERCISED (19 of 19 Lever-A decisions over 10 days were POSITIVE -> SKIP).
**The 04:35Z fire IS the discriminator. Read its outcome before escalating anything.** A retry costs a
vendor auth call and proves nothing; a 401 is not transient.

## 4. CLOCK-GATED — do not pull these forward

- **Monday 12:45Z** — three pre-registered acceptance reads (a06's registered line; A7-4's provenance
  read; V-4's first fire). `ADVI_49F`'s A7-4 is genuinely **uncomputable** until this fires.
- **Tuesday** — V-4's second fire.
- **04:35Z** — now load-bearing for THREE things, not one: the insurance chain fire, `0.7.0_AE_CloudOps`'s
  `s1-bd49finsurance-silver-family` acceptance, **and the BD session re-mint that gates W2**. Its outcome
  is the first thing a successor should read.

⛔ An ad-hoc run to "get it in before the reset" destroys the discriminator the scheduled fire exists to
produce. The law names this specifically. Wait.

## 5. ANDREW'S SEVEN CARDS — ALL RULED 2026-08-30 ~17:1xZ

Record (verbatim + routing + a correction appended, not amended):
`deliverables/ANDREW_DIRECT_20260830_171xZ_SEVEN_CARD_RULINGS.md`.
(1) measurement ordered → **ANSWERED, antecedent FALSE** · (2) W1→W2, **spent on W2** · (3) extended with
its source-gap clause · (4) `ADVI_49FSRC` closed · (5) re-emit retired + graded · (6) executed, 8 objects,
recoverable · (7) answered from the estate, no vendor contact needed.
⛔ **A fresh context re-asking any of these reads as not listening.** They are spent.

**Management deliverable, committed:** `deliverables/EXEC_SUMMARY_49F_13_UNATTRIBUTED_ACCOUNTS_20260830.md`
— the document for Andrew's 49F conversation. Carries the 13 account numbers, **no client names, no
registration strings**. Share by value is measured (0.8233%), not estimated.

## 6. WHAT IS UNVERIFIED OR RESTS ON ONE INSTRUMENT

Stated because a handoff that reads uniformly clean is the one to distrust.

- **The org/mcp broker return-path defect is OPEN and unfixed.** Mechanism found at source
  (`org/mcp/server.py:499-512`, a bare `except: return None` collapsing every transient into one value).
  **No restart was taken** — the cause is unmeasured and ~20 seats are attached. Symptoms: `id=None` on
  sends that in fact landed, and false `broker call FAILED` on acks that landed. **Never infer delivery
  from a send's own return.**
- **The foreign-row ACK class reached 7 self-reported instances today across 5 seats**, two distinct
  mechanisms. The recipient guard refused every one. ⛔ **The guard's refusal log is a denominator for
  the POST-guard period only** — a pre-guard foreign ack is silent and nobody has censused that.
- **`0.7.0_AE_CloudOps~K` and `0.4.0_DT_ClientPlatform~X` are DEAD** (measured on the Win32 process
  table, not inferred). Do not address frames to them.
- **`ADVI_49F` C02-g-10's A7-4** is filed UNCOMPUTABLE, not passed.

## 7. MY OWN ERRORS THIS SESSION, so the successor does not inherit the confidence without the evidence

Four corrections against this seat's own words, all committed beside the claims they refute rather than
amended away:

1. **Took blame that was not mine** for a truncated VersionId; the executing seat declined it and traced
   the origin to a `[:22]` slice in its own census script.
2. **Took blame that was not mine AND buried a live defect**: a true `1 of 9` register reading was
   explained away as my own instrument artifact while a peer's close had genuinely removed a member.
3. **Claimed "never a member" from `org/DIRECTIVES.yaml` — a path that does not exist.** The register is
   `org/missions/DIRECTIVES.yaml`. Two instruments returned empty against the same wrong path; that is
   repetition, not corroboration, and out-of-corpus is not absence.
4. **Put a false spatial premise into a record Andrew read** (*"the SmartX feed lands under 0833"*).
   `smartx/` is its own top-level prefix; no SmartX feed is under either Schwab master.

⛔ **The pattern under 1 and 2, and it ran in opposite directions within one hour: reflexive self-blame is
the cheapest available explanation, it terminates inquiry, and nobody audits it** — the same mechanism
that lets a false self-attribution survive. **Rule adopted: when your own instrument disagrees with your
prior number, test the WORLD first and yourself second.** And run a positive control on any path before
reading its silence as absence.

## 8. STATE AT HANDOFF

`state: ARMED` (paused for context reset, clause un-struck) · completion 2 of 10 · 0 open calls blocking
at Andrew · 4 commits LOCAL at this seat · origin/CLOUD `885e08055f` at the 17:35Z CLOSE, own `ls-remote`
read 17:38Z · **push state of this handoff: LOCAL, rides the next integration window.**
