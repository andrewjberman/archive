# ANCHOR SWEEP 2 — CTO's stated width (MDPF remediation record)

**archetype:** VALIDATE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**GO:** `2.0.0_SA_COO` 152141Z — commissioning the gap Sweep 1 §4 declared uncovered.
**Surface:** every timing figure in the MDPF remediation record predating
**2026-08-06T00:04:48Z** (the `ce99054e44` apply).

> **RESULT: TWO STALE ANCHORS FOUND — one of each failure class.** Sweep 1 returned zero on the
> narrow surface; the wide surface was not empty. **The gap was the work.**

---

## 1. Denominator and what it excludes

**SWEPT:** 24 files, **7,279 lines**.
`docs/architecture/MDPF_REMEDIATION_REGISTER.md` (311 lines, R-1..R-32) · **20 MDPF PRDs** ·
**4 CANPLAT P1/P2/P3 TOs** (P1-1 DS, P1-2, P2-1, P3-1).

**Class-2 candidate extraction:** clock-time adjacent to a delivery verb
(`lands|delivered|arrives|wrote|written|emitted|drops`), `cron(` excluded → **22 candidate lines**,
triaged by hand to **2 genuine pre-apply measured delivery clocks**.

**⛔ EXCLUDED — named, not swept:**
- **INF and cot timing figures outside the MDPF docs** (`data/inf/**`, `data/cot/**`, the INF/cot
  PRDs). COO's GO named "INF and cot timing figures"; I swept those *appearing in the MDPF
  remediation record*, not the INF/cot programs' own documents. **A third sweep, if wanted.**
- Non-MDPF-prefixed architecture docs, `org/tier*/deliverables/**`, and all session logs.
- **Class 1 (schedule expressions)** — re-derived by construction; all read live today.
- **Class 3 (observations dated 2026-08-07+)** — post-apply, in-regime.

---

## 2. FINDING A — `MDPF_3FIRMS_PRD`: "HOLDINGS lands **D+1 ~03:30Z**" is **WRONG ON BOTH AXES AND WAS NEVER TRUE**

**As recorded** (`MDPF_3FIRMS_PRD.md:481`, authored **2026-07-22** @`88c80b003a`, `1.0.0_SA_CTO`),
cited again at `:640` and `:765`:

> *"the mechanism is the **D+1 ~03:30Z holdings delivery cadence** (bronze object stamps, this session)"*
> *"`HOLDINGS_DAILY_{D}.xlsx` lands D+1 ~03:30Z"*

**RE-DERIVED — `opal-data-cot/forwardfill_v2/holdings/`, DENOMINATOR 47 objects, FULL retained
history 2026-06-09 → 2026-08-09:**

```
WRITE-HOUR HISTOGRAM (UTC):  02:xx=33   14:xx=7   20:xx=4   09:xx=1   10:xx=1   21:xx=1
ANY WRITE IN THE 03:xx HOUR?   *** ZERO OF 47. NEVER OBSERVED. ***
```

| axis | as recorded | measured | verdict |
|---|---|---|---|
| **hour** | `~03:30Z` | **02:0xZ** (33/47, the steady regime through 2026-08-05) → **20:3xZ** (08-06 onward) | **NEVER TRUE, *and then also* MOVED** |
| **lag** | `D+1` | **D+2**, on effectively every steady-state row (D+1 appears twice in 47, both at off-pattern hours) | **NEVER TRUE** |

**BOTH DEFECT CLASSES ON ONE FIGURE.** The hour was never 03:30Z at any point in the retained
history *and* it moved on the 08-06 apply. The lag was never D+1.

> **THIS IS THE SECOND INSTANCE OF THE CLASS CTO NAMED 30 MINUTES AGO, FOUND INDEPENDENTLY.**
> After Sweep 1's orion row, CTO widened their own standing check: *"MY CHECK CATCHES FIGURES THAT
> WENT WRONG. IT IS BLIND TO FIGURES THAT WERE NEVER RIGHT … EVERY TIMING FIGURE CARRIES ITS
> PROVENANCE."* A staleness-only sweep passes straight over this row — the pre/post-08-06 filter
> would have classified it "pre-apply, re-derive," found it moved, reported MOVED, and **never
> noticed that the recorded value was fiction in both regimes.** The widened rule catches it; the
> original does not. Sweep 2 validates the widening on a fresh case.

⚠ **The figure's own provenance line is the tell, and it is honest:** *"(bronze object stamps, this
session)"* — it declares its method. It is `MDPF_3FIRMS_PRD` §"Cottonwood bronze tails" (`:765`) that
promotes it to a **mechanism** other reasoning stands on. Where the 03:30Z/D+1 pair came from is
**NOT DIAGNOSED** — per the fence, MOVED/WRONG with both values, then stop.

---

## 3. FINDING B — `MDPF_DEBTCLEAN_PRD`: "every upstream channel lands by ~16:00Z" is **NOW FALSE**

**As recorded** (`MDPF_DEBTCLEAN_PRD.md:417`, authored **2026-07-28** @`f723d24cc0`, `1.0.0_SA_CTO`):

> *"**Cadence input:** every upstream channel lands by ~16:00Z at the latest (§2.4) … **A schedule
> materially later than the last channel's arrival is the only safe choice** — exact time is a
> D-item, not a guess."*

**RE-DERIVED — measured landings, this session:**

| channel | measured landing | vs the ~16:00Z bound |
|---|---|---|
| orion inflection silver | 14:16Z | within |
| cot rebalancer bronze | 06:00Z | within |
| **cot `forwardfill_v2`** | **20:31Z** | **VIOLATES by ~4.5h** |
| **eclipse inflection silver** | **22:31Z** | **VIOLATES by ~6.5h** |

**Verdict: MOVED.** True when written — on 2026-07-28 eclipse landed T+1 03:30Z and cot landed
02:01Z, so every channel *did* clear 16:00Z. **The 08-06 apply broke it**, and the figure is CTO's
original class exactly: correct when taken, silently invalidated, still sitting in a PRD as a
"cadence input."

⚠ **WHY THIS ONE IS LOAD-BEARING RATHER THAN COSMETIC:** the sentence immediately after it derives a
scheduling rule from it. **A schedule placed "materially later than 16:00Z" now fires BEFORE two of
its four channels land** — the identical shape as the 02:00Z cottonwood anchor, and the identical
consequence: a job that runs, exits clean, and reads data that is not there yet. Not diagnosed
further, not chased downstream; one line to COO per the fence.

---

## 4. Everything else on the surface — classified, not swept

| candidate | class | disposition |
|---|---|---|
| `R-23` "Measured live 2026-08-07 03:2xZ" (register :242) | 3 | POST-apply, in-regime |
| `R-18` run-time `latest_holdings_date` re-resolution (:241) | — | behavioural claim, not a delivery clock |
| `MDPF_GLOBAL_PRD` :700/:701/:829/:831 (07-31 11:00 ET; 15:00Z; 12:15 ET; 16:15:32Z) | 3 | dated **observations of specific past events**, not standing cadence anchors — nothing downstream schedules off them |
| `MDPF_MONOCLEANUP_PRD` :60 "legacy smartx Lambda (cron 11:30Z)" | 1 | schedule expression — re-derived by construction |
| `MDPF_CANONICAL_PLATINUM_DELIVERABLE_CONTRACT` :27/:274 "the 09:40 bridge" | 1 | names a schedule, not a measured delivery |
| `MDPF_CANPLAT.P3-1` :41 "before 10:00 ET (D1)" | 1 | a **requirement**, not a measurement |
| `MDPF_OWNTS` :347 "MCP delivered 2026-05-26 ~21:24Z" | 3 | message routing, not a data clock |
| `MDPF_3FIRMS` :354/:545/:548/:643/:703 | — | already carry in-file CORRECTED/STALE-AT-AUTHORING markers |

---

## 5. Compiler Tools

| Tool | Result |
|---|---|
| `git log -S "<claim text>"` | Pinned both claims' authoring commits + dates — **this is what made "pre-apply" a measured property rather than an assumption.** `88c80b003a` 07-22 · `f723d24cc0` 07-28 |
| `aws s3api list-objects-v2` (forwardfill_v2, full history) | 512 objects / 368 xlsx / 47 holdings — APPLIED reads, true UTC, never `aws s3 ls` |
| python triage over the 24-file corpus | 7,279 lines → 22 candidates → 2 findings, denominator printed at each narrowing |

**Method note worth keeping:** the finding came from a **HISTOGRAM, not a spot check.** Comparing the
recorded 03:30Z against the *current* value would have returned "MOVED" and stopped. Binning all 47
write-hours is what showed `03:xx` has **zero** occupancy across the entire retained history — i.e.
that the figure was never true, not merely out of date. **A spot check answers "is it still X"; a
distribution answers "was it ever X."** Only the second distinguishes CTO's two classes.

---

## 6. State

**Nothing applied. Nothing diagnosed. Both findings reported with both values and stopped**, per the
fence. Well inside the 2-hour bound. §1 declares what this sweep excludes — the INF/cot programs'
own documents remain unswept and my result says nothing about them.
