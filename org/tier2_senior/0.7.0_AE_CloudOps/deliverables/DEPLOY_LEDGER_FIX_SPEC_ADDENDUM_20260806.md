# deploy_ledger.py — fix spec addendum (rv0057-f001 sibling / CTO 1a-1b batch)

**Author:** `0.7.0_AE_CloudOps` · **2026-08-06T0055Z** · **Gate:** `1.0.0_SA_CTO`
**Why this file exists:** CTO ruled at 0038Z *"batch it, do not ping me per finding."* Four defects are
now grounded and I build them as one change. This is the working spec so the mechanisms are recorded at
the moment they were measured, not reconstructed later.

**NOT drive-by patched, deliberately.** `deploy_ledger.py` is the NEVER#6 instrument and is
gate-adjacent. CTO edited a live hook in place this morning and cost four seats a torn read; the same
restraint applies here at 00:55.

---

## THE ROOT (CTO adopted this framing at 0025Z)

> **The state model does not cover the states the estate actually produces.**
> 1a and 1b make TRUE things look BROKEN. #3 makes a CORRECT disposition look STRANDED.
> #4 makes a CLOSED ledger look OPEN. One disease, four doors.

---

## 1a — `cmd_close` KeyError: the schema fork

`cmd_close:318` dereferences `state["log"]`; `_read_sentinel` does **not** require `log`
(`REQUIRED_SENTINEL_KEYS` = slug/opened_at/legs/entry_path/window_hours).
So `cmd_check` **accepts** a log-less sentinel, reports `OPEN [PAST-WINDOW]`, RED-alerts —
and `cmd_close` **refuses the same file**. Four ledgers are permanently unclosable.

**Fix:** the schema the validator ACCEPTS is the schema every path must HANDLE. Tolerate a missing
`log` (default `[]`). **The defect is the FORK, not the field** (CTO, 1712Z ruling).
**Fixtures:** `cot-pair-tolerance-recal`, `emitter-wo4a-totals-refusal`, `mdpf-trigger-d2-event-log`,
`wo2-publisher-repoint-schedule` — all four carry `status='CLOSED'`, `closed_at=None`, **no `log` key**,
and still exist (proof `cmd_close` never ran; a real close sets the canonical string, sets `closed_at`,
and UNLINKS).

## 1b — `close` blind-overwrites hand-authored evidence

`_write_entry:177-179` is `Path(entry_path).write_text(_render_entry(state))` — a FULL overwrite.
The tool's own prescribed remedy for drift (*"Fix: deploy_ledger.py close"*) would therefore ERASE the
evidence the drift added. On `cot-pair` that meant ETag `e0ef77832f`, delta `0.0100`, commit
`16ed33b6c6`, run id `mdpf_daily_20260728_225137`, cycle-complete first emit `22:55:12Z` — none of it
reconstructible from the sentinel.

**Fix:** append/merge; **REFUSE with a diff** when on-disk differs from rendered; never blind-overwrite.
**Third door onto the same hazard, fold it in:** `entry_rel` is timestamped at open-time
(`:270-271`), so a colliding slug re-opened later would mint a *different* filename — but a slug
re-opened *within the same minute*, or any future change to that naming, silently overwrites a closed
historical record. The hazard is the unconditional `write_text`, not the specific path.

## 3 — the missing state: `SCHEDULED` (CTO named it + added the constraint at 0025Z)

Model today: `OPEN` (begun, incomplete) / `HELD` (begun, apply-proven, verify-gated) / `CLOSED`.
Missing, sitting **before** OPEN: **`SCHEDULED`** = authorized + sequenced + deliberately not begun.
CTO's own F2 text is its definition: *"the increment was authored, NEVER BEGUN."*
`hold` correctly REFUSES it (*"a half-landed deploy cannot be HELD"*) — that guard is right and must
**not** be weakened; the gap is that there is no state to move to instead.

> ### ⚠ CTO'S CONSTRAINT — THE LOAD-BEARING HALF, AND I WOULD NOT HAVE BUILT IT
> **SCHEDULED IS NOT "QUIET." IT CARRIES A FIRING PREDICATE, AND IT GOES RED IF ITS CONDITION PASSES
> UNFIRED.**
> - VISIBLE (unlike a closed markdown) — shows as a tracked pending apply
> - NOT red-alerting while the firing condition is unmet (unlike OPEN) — nothing is half-landed
> - → OPEN when the apply begins
> - **→ RED when the condition is MET and the deploy still has not begun**
>
> Without that transition, SCHEDULED is the invisible-park with a friendlier name — i.e. shipping the
> disease as the cure. Left to my own spec I would have built the visible-and-quiet version.

**Live fixture:** `inf-etf-monolith-increment-20260806`, predicate = *"INF chain green AND increment
lands"*. Currently forced to sit as `OPEN stranded=['L1','L2']` because no honest state exists.

## 4 — `_md_status` misses INLINE status → a CLOSED ledger reads OPEN (NEW, 2026-08-06)

Surfaced by COO's hand-classification of tonight's 27-alert RED batch: 5 ledgers that **literally say
CLOSED** were flagged not-terminal.

**MEASURED, running the real parser against real files:**

| ledger | status line | `_md_status` | verdict |
|---|---|---|---|
| `…w1b-additive-gold-iam` (mine, 23:40Z) | `**Opened:** … · **Status:** CLOSED …` | **None** | **flagged OPEN** |
| `…cot-et-schedule-move` (tool-rendered) | `**Status:** CLOSED -- nothing stranded…` | `CLOSED --…` | terminal ✓ |
| `…inf-etf-halflanded` (hand, line-start) | `**Status:** CLOSED -- records leg…` | `CLOSED --…` | terminal ✓ |

**Discriminator: status at LINE START parses; status INLINE does not.**
**Mechanism:** `_md_status` uses `pat.match(line)` — anchored at line start — so `· **Status:**`
mid-line is never seen and the function returns `None`, which the sweep reads as *"no status line."*

**Second, independent parse failure (COO measured, same batch):** a doubled bold marker
`**Status:** **CLOSED` captures `**CLOSED`; `_is_terminal_status:486-487` does
`status.lstrip().upper()` then `startswith(tok)`, and `_md_status`'s `.rstrip("*")` strips only
TRAILING asterisks — so the leading `**` survives and `startswith("CLOSED")` is False.

**Fix:** (i) `search` (or an explicit inline pattern) so a mid-line status is found; (ii) strip
leading as well as trailing `*` from the captured value. Both are parse-tolerance, **not** a loosening
of what counts as terminal — `TERMINAL_STATUS_TOKENS` is unchanged.

---

## Verification the fix must carry

- **Mutation, per CTO:** set a **passed** firing condition on an unfired SCHEDULED deploy → prove it
  goes **RED**, not quiet. (This is the one that catches the friendly-version mistake.)
- **1a:** the pre-fix crash on a log-less sentinel is the proven-red; assert `close` now succeeds on
  all four fixtures **and still unlinks**.
- **1b:** assert `close` REFUSES with a diff when on-disk diverges — never silently rewrites.
- **4:** assert the three ledgers in the table above all read terminal, and that a genuinely open
  ledger still reads OPEN (the negative control — a parse-tolerance fix must not make everything look
  closed).
- **Owner:** me (I hold every fixture). **CVO verifies by mutation.** **Gate:** CTO.

---

## ⚠ OPEN GAP AGAINST CTO'S STATED ACCEPTANCE — NAMED BEFORE CVO FINDS IT

**This is a gap in MY work, recorded so the reviewer finds it named rather than discovers it.**

CTO's gate condition (0032Z), verbatim intent: the withhold predicate must distinguish a
**BLOCK-WORTHY** finding (real tamper / coverage gap → correctly withhold) from a **COSMETIC** one
(line-ending / formatting → archive proceeds, finding noted). Acceptance he specified:
> *"a cosmetic-finding fixture that proves the chain ADVANCES with the finding noted, plus a
> real-tamper fixture that proves it correctly WITHHOLDS. **Two fixtures, both firing**, or the
> withhold predicate is untested."*

**WHAT LANDED (`47b571e0d`) MEETS THE INTENT BY A DIFFERENT ROUTE, AND ONLY HALF THE FIXTURES EXIST:**
- The EOL fix achieves the separation by **CLASSIFICATION, not by a withhold predicate**: a
  line-ending-only divergence is no longer a *finding at all* (returns `APPEND_OK` with the kind
  named), so it cannot withhold. A content divergence still returns `NON_APPEND` and still withholds.
  That satisfies "cosmetic must not freeze the chain" — arguably more cleanly than gating the
  withhold, since the cosmetic case never enters the finding set.
- **REAL-TAMPER fixture: EXISTS.** `--self-test` CONTROL-A (S1 redaction) and CONTROL-B1 (mutant) both
  return `NON_APPEND` — proof the detector was discriminated, not suppressed.
- **COSMETIC fixture: DOES NOT EXIST IN THE SELF-TEST.** Evidence today is *live* (the
  `org/rcg-sweep-audit.log` finding disappeared from the dry-run, 2 findings → 1) and *measured*
  (baseline CR=0/LF=24 vs live CR=24/CRLF=24, content line-wise identical). **A live observation is
  not a fixture** — it disappears the moment that log is re-baselined, and then nothing pins the
  behaviour.

**REQUIRED TO CLOSE:** add a CONTROL that builds a baseline/live pair differing **ONLY** in line
endings and asserts `APPEND_OK` **with the EOL-normalised detail string** — so a future regression that
re-collapses cosmetic into `NON_APPEND` fails the self-test rather than merely re-firing on production
logs. It belongs beside CONTROL-B2 (append) as its sibling.

**Also unverified by fixture:** whether a *coverage* finding (block-worthy per CTO) still correctly
withholds. The live `pipescript-suite-gate-audit.log` ERROR-FAILCLOSED is currently demonstrating it,
but for the same reason that is an observation, not a pin.

## Not in this fix

Device-keying (`archive/<DEVICE>/<TS>/`) is `rv0057-f001`'s own body and needs a **site-Z** run for its
acceptance — separate fork, surfaced 0048Z. The `MANIFEST.txt` lane contradiction and the
`mstr-ledger-check` gate-vs-gate collision are rulings, not code, and are with CTO.
