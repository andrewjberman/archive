# The Undiscriminating Clean Verdict — a puller failure class

**Author:** 0.6.2_AE_PartnerETL · **Date:** 2026-07-16 · **Grade:** P2 post-mortem (CTO-approved 20260716T133027Z)
**Origin:** 0.5.0_AE_OpalETL's finding 20260716T052941Z; the unresolved 2026-07-07 SI2 recurrence risk
**Scope:** artifact-read-only. No vendor egress was used to produce this (see §6).
**For:** SCHWABAUTO Gate-2/3 · the release playbook · any future puller

---

## 0. PRIOR ART — this class was already named, ratified, and then orphaned

**Added 2026-07-16 after this document was first committed (`841e5e04b`), on discovering the prior art
while characterizing an unrelated thread. The attribution leads because the priority is his.**

`0.6.0_AE_PartnerETL` named this class on **2026-07-09** in
`org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/FINDINGS_snapshot_zero_row_class_20260709.md`
(**CTO-ratified 200747Z / 202240Z**), and stated it **more generally than §1 below does**:

> *"An instrument reports confidently on something other than what it claims to measure, and the null it
> emits is produced by two different worlds — one healthy, one broken."*

**That is the general form. §1 is its puller special case.** His table already enumerates seven instances
on one data path — `s3_object_exists` passing on a 0-row stub; `bytes > 30KB` passing on a 0-row 94-col
parquet (46,277 B); `sorted(keys)[-1]` returning the newest *stub*; `row_count > 0` passing on 11,754 rows
at `nzf = 0.0000` (rows exist, values do not); a **latched** CloudWatch alarm whose silence is *the rail,
not the state*; a CloudTrail `ReadOnly` data-event selector making a write **"never captured"**
indistinguishable from **"never happened"**; and — item 7 — `grep -c` on a commit message returning `0`:
*"never written, **or written and executed away**."*

**Two facts about that document should outlive both it and this one:**

1. **It predicted the error made while writing this file.** Its item 7 is precisely the failure in the
   Companion Lesson below — a negative count from an unguarded read. The fabric had named my mistake, in a
   *ratified* document, a week before I made it.
2. **It went dark when its author did.** 0.6.0's session ended 2026-07-10; the deliverable was never
   inherited, and this document independently re-derived a narrower version of it six days later. **A
   ratified class taxonomy became invisible because nothing inherits a dead agent's deliverables** — which
   is itself an instance of the class: *the absence of a finding is indistinguishable from the absence of
   the finder.*

Read his document first. This one adds the puller-specific discriminator (§3), a reference implementation
(§4), a measured positive control (§5), and a ship checklist (§8).

---

## 1. The class, in one line (the puller case)

> **A puller whose clean verdict is emitted identically on "the source was empty" and "I failed to see what
> the source had" HAS NO VERDICT AT ALL — and it fails in the direction that looks healthiest.**

This is not "a bug in a box." It is a **shape**. Any retrieval component with a `no new files` /
`0 records` / `nothing to do` success path is a candidate, regardless of vendor, language, or transport.

## 2. Why it outranks an ordinary outage

An outage announces itself. This class does the opposite — it **manufactures the strongest possible
healthy reading**, because every downstream instrument agrees:

| Instrument | Reads | Why it is fooled |
|---|---|---|
| the run's exit code | `0` | the run genuinely completed |
| the run's log | `no new files` | literally true of what it saw |
| the schedule | fired on time | it did |
| the landing guard | `shortfall=0` | nothing was *planned*, so nothing is missing |
| the freshness alarm | quiet (or explained) | "vendor publishes late / T-1 / weekend" |

**The guard is the cruel part.** A set-identity landing guard verifies *planned vs landed*. If the
enumeration returned empty, the plan is empty, and the guard confirms — correctly — that all zero planned
files landed. **A guard downstream of a blind enumeration certifies the blindness.** The instrument is not
merely silent; it is *anti-correlated* — the more completely the puller failed to see, the greener the board.

Historical instance (2026-07-07, root mechanism never found): **14 consecutive clean scheduled cycles**,
each reporting `no new files`, while live data existed at the vendor. Recovered only by a human's manual
pull. Nothing alarmed. Nothing could have.

## 3. The discriminator (the whole fix, stated abstractly)

The verdict must be a function of **two** variables, never one:

```
                        source non-empty        source empty
  we could see          DOWNLOAD                LEGITIMATELY EMPTY  <- the only honest "clean"
  we could NOT see      SILENT MISS  <-- lethal PAGE
```

`no new files` collapses row 2 into row 1. **Every fix in this class is the same move: refuse to emit a
clean verdict until you have positively established which row you are in.** Concretely, at least one of:

- **an independent expectation** — a calendar, a manifest, a prior-day count. *Something the source cannot
  make empty.*
- **a positive control on the read itself** — did the enumeration path demonstrably work at all?
- **a loud refusal** when the read cannot be established.

**"The vendor sent nothing" and "I asked wrong" must not share an exit path.**

## 4. What the current puller does — the class is closed IN CODE, structurally

`sdd-daily-pull.ps1` (deployed, 35,842 bytes, `s3://opal-data-schwab/_ops/canonical-schwab-si2/`) already
implements the §3 discriminator. **This is the reference implementation; copy it, do not re-derive it.**

**(a) The independent expectation is the TRADING CALENDAR — and an empty read on a trading day PAGES:**
```powershell
# >>> ZERO ON A TRADING DAY IS A FAILURE, NOT A SHRUG. This is the exact cell the GUI channel died in. <<<
if ($ENUMERATED -eq 0) {
  if (Is-TradingDay $frontier) { Die 2 "ZERO files enumerated over a 30d window that CONTAINS trading days
    (frontier=...). The vendor does not publish nothing for 30 days. This is a DEAD CHANNEL, not a quiet one." }
  Log "zero files, and no trading day in window -- legitimately empty"    # <- row 2, EARNED
  exit 0
}
```
The calendar is the thing the vendor's silence cannot forge. Note the puller resolves the frontier
**itself** (`while (-not (Is-TradingDay $d)) { $d = $d.AddDays(-1) }`) — NEVER#1 satisfied in code, not by
an operator remembering.

**(b) A failed read is never an empty read:**
```powershell
if ([int]$resp.StatusCode -ne 200) { Die 2 "SDD search HTTP $ -- CANNOT ENUMERATE. This is a FAILURE, not an empty day." }
```

**(c) The denominator is the SOURCE's, never the selection's:**
```powershell
# The lesson of 2026-07-13: a self-consistent check over a truncated read PASSES. The denominator you
# print must be the SOURCE's (what the vendor said exists), never your selection's (what you happened to iterate).
$accounted = $dl + $skip + $fail       # MUST equal $ENUMERATED
```

**(d) It fails loud by construction:**
```powershell
# FAIL LOUD. The predecessor's fatal flaw was a benign-sounding rc=0 on a dead channel.
function Die($code, $msg) { ... sns publish "SCHWAB SDD DAILY PULL FAILED" ... }
```

**(e) Nothing is silently skipped** — undated files are *collected then RAISED*; a master-prefix mismatch or
an API-vs-filename date disagreement is a hard QUARANTINE, never a default (*"A default is an assumption
with a shorter name"* — CTO~B, 2026-07-13).

## 5. The measured proof that the discriminator works

The class demands a **positive control**: proof the clean verdict *can* come out dirty. Two consecutive
scheduled fires of the same code on the same box, read from their own persisted records:

```
0833  20260715T214552Z (maiden)  enumerated=267  downloaded=0   skipped=267  failed=0  guard ok
0833  20260716T094552Z           enumerated=266  downloaded=13  skipped=253  failed=0  guard ok
0824  20260716T101519Z           enumerated=230  downloaded=11  skipped=219  failed=0  guard ok
```

**The maiden reads `downloaded=0` — the exact shape of the 07-07 incident.** The next fire reads
`downloaded=13`. So the path **sees and fetches**: `downloaded=0` was honest inventory (267 enumerated, 267
already present), not blindness. And the downloads are real rather than a tally — `13` ties **1:1** to
exactly 13 bronze keys landing 09:46:02–09:46:41Z with bytes; `11` ties to exactly 11.

> **`downloaded > 0` on a later fire is the control the 07-07 investigation never ran.** Without it,
> `downloaded=0` is uninterpretable — and *uninterpretable was mistaken for healthy for 14 cycles.*

## 6. The method note that generalizes beyond this class

The natural ask was *"exercise the pull path against live Schwab."* **It was not run, and should not have
been** — two independent reasons:

1. **Vendor egress.** Schwab is not on the lifted list (ORION · SMARTX are); every other vendor needs
   Andrew's explicit per-use word. Availability is not authorization.
2. **It is the weaker test anyway.** *A pull you trigger proves that your pull works — not that the
   schedule's does.* The scheduled run's own artifacts answer the actual question; a manufactured pull
   answers a question nobody asked (NEVER#4's spirit).

**The verdict came from the SCHEDULED runs' persisted records. Zero egress, sharper answer.** Any future
post-mortem in this class should be scoped artifact-read-only from the start — the evidence is already
being written by the thing you are investigating, *if it persists a manifest*. Which is the deeper reason
the C5 "persisted per-pull meta manifest" property exists: **it is what makes a post-mortem possible
without touching the vendor.**

## 7. What is still OPEN — and must not be closed on §4/§5

**The 2026-07-07 mechanism remains unexplained.** §4 shows the *current* code cannot produce that failure;
§5 shows the *current* box discriminates. **Neither is evidence about what the old path did.** Today's
immunity says nothing about yesterday's mechanism — that is a claim about a different code vintage, and
closing it on present-day health would be exactly the substitution this document exists to name.

Recorded honestly: **the 07-07 root mechanism is UNDETERMINED and the channel it lived in is being
decommissioned (WP7), so it may never be determined.** That is an acceptable outcome *stated*, and an
unacceptable one *implied by silence*.

## 8. The checklist (for SCHWABAUTO Gate-2/3 + the release playbook)

Before any puller ships or a release passes:

- [ ] **Enumerate the clean-verdict paths.** For each, ask: *what else produces this exact output?* If a
      failure does, it is not a verdict.
- [ ] **Name the independent expectation** the source cannot forge (calendar / manifest / prior count).
      No expectation = no discriminator = **do not ship**.
- [ ] **A failed read must not share an exit path with an empty read.** Non-200 / timeout / auth failure →
      loud, distinct, never `0 records`.
- [ ] **Print the SOURCE's denominator**, not the selection's, and assert `accounted == enumerated`.
- [ ] **Persist a per-pull manifest** — it is the post-mortem's evidence, and the reason a future
      investigation needs no egress.
- [ ] **Exhibit the positive control**: a run where the clean verdict came out *dirty*. An instrument with
      no observed non-clean output has never been tested.
- [ ] **Guards inherit their input's blindness.** A landing guard downstream of a blind enumeration
      certifies the blindness. Guard the READ, not only the LANDING.

---

### Companion lesson from this window (same shape, different layer)

Producing this document, I claimed the puller had "zero HTTP call sites" and therefore "delegates to a .NET
assembly." **False.** The client is at `Invoke-Sdd :296` (`HttpWebRequest`); my grep pattern
(`Invoke-WebRequest|Invoke-RestMethod|HttpClient|WebClient|curl`) never matched it. **A negative result from
a pattern I never wrote became a claim about the artifact, then a mechanism.** Separately, an ASCII check
reported `"ASCII-clean (0 non-ASCII lines)"` on a file whose download had silently failed — *zero matches in
nothing.*

**Both are §1 in miniature: an output that means "I found nothing" is indistinguishable from one that means
"I looked wrong," unless a control forces them apart.** The class is not a property of pullers. It is a
property of *any* instrument whose negative result is unguarded — including the ones you write while
investigating it.

*Put the control on the retrieval, not the pattern.*
