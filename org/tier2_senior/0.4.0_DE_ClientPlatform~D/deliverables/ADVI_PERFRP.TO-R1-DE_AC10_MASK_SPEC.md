# ADVI_PERFRP TO-R1-DE — AC10(c) MASK SPEC + the AC10(a) closure denominator

**Author:** `0.4.0_DE_ClientPlatform~D` · **Issued against:** COO ruling @f696acb8f8 (msg 66842, "Bring the
mask spec with the evidence") · **Cell:** `PRF-inv-1` · **Criterion:** `PRFR1DE-AC10`
**Status:** evidence artifact, authored BEFORE any edit to the change surface. Nothing in the portal tree
has been modified by this seat.

---

## 0. Why this file exists

`PRF-inv-1`'s original oracle — *"build-output diff of `AdvisorsTab` / `DistributionTab` bundles = 0 bytes
changed"* — named an artifact the build does not emit (filed 66696/66706; amended into the cell and AC10
@ad503ce567; re-weighted @f696acb8f8). The replacement oracle has three limbs:

| limb | test | what it actually protects |
|---|---|---|
| **(a)** | source diff over the two tab files + their NON-SHARED closure, **denominator printed** | **2 files of 69** — see §1 |
| **(b)** | confinement at the `hideBookToggle` seam (`AdvisorPublicProfile.tsx:1201`) | the 67 shared files, by reachability argument |
| **(c)** | **masked pixel** comparison of pre/post captures, both protected tabs, READ | the rendered surface — this file |

COO's ruling is explicit that **(a) is quoted with its denominator or not quoted at all**, and that **(b)+(c)
are THE protection, not belt-and-braces.** This file supplies (c)'s mask and (a)'s denominator.

⛔ **`md5` / byte comparison of screenshots is BANNED in this criterion** (COO @f696acb8f8). See §3 — the
positive control that killed it.

---

## 1. AC10(a) — the closure denominator

Import-graph closure over `portal/src`, resolving `@/` and relative specifiers through
`.tsx/.ts/.jsx/.js` and `index.*`. Instrument: `ac10_closure.py` (committed beside this file).

```
PROTECTED closure (from AdvisorsTab.tsx + DistributionTab.tsx) : 69 files   (0 unresolved local specs)
CHANGE    closure (from the 5 d-cell entry points)             : 67 files   (0 unresolved local specs)
NON-SHARED = PROTECTED - CHANGE                                :  2 files
SHARED     = PROTECTED & CHANGE                                : 67 files
```

**The NON-SHARED 2 are `AdvisorsTab.tsx` and `DistributionTab.tsx` themselves. Nothing else.**

The 0-unresolved figure is load-bearing: it says the denominator is not hiding a silently dropped import.

Cause: `AdvisorsTab.tsx:23` imports `AdvisorPublicProfile` and `:566-570` renders it inline, which pulls
`AdvisorBookView` / `AdvisorBookClientDetail` / `AdvisorBookAccountModal` / `CanonicalBookView` and the whole
`api/endpoints` + `ui/components/panels` layer into **both** walks.

> **Read (a) as "do not edit the two tab files."** That is what it tests. It is worth testing and it is
> nearly free, but it is **not** a 69-file guarantee and must never be quoted as one.

---

## 2. AC10(c) — THE MASK

Derived from repeated captures of an **unchanged** tree. Any pixel that varies with no edit is render noise;
unmasked, it false-positives the comparison. Instrument: `ac10_maskcheck.py` (committed beside this file).

### The mask — PER TAB, not a union

| tab | frame | mask box (x0,y0,x1,y1) | area |
|---|---|---|---|
| **Advisors** | 1440 × 1003 | `(105, 904, 113, 912)` | 8×8 = 64 px |
| **Distribution** | 1440 × 1253 | `(105, 1154, 113, 1162)` | 8×8 = 64 px |

**Identified by cropping and LOOKING, not by inferring from coordinates:** the pulsing green status dot
preceding *"Black Diamond Connected"* in the `DATA SOURCE` panel. Same element on both tabs; the y differs
only because the Distribution page is 250 px taller, so the panel sits lower. Sampled colours across
captures: `(33,152,127)` vs `(34,146,123)` — green, varying luminance, i.e. animation phase.

⛔ **DO NOT union the two boxes.** A naive union across tabs yields `(105, 904, 113, 1162)` — an 8×258 box
masking ~2,064 pixels that are provably deterministic, which is a blind spot a real regression could hide in.
My own derivation script printed exactly that union as its proposal and it is **wrong**; the per-tab boxes
above supersede it. (Caught by reading the tool's output rather than accepting its summary line.)

### Pass rule

```
PASS  iff  dimensions match EXACTLY
      and  differing pixels OUTSIDE that tab's mask box == 0
```

A dimension change is an automatic FAIL — never resize-and-compare. The human READ stays alongside: a pixel
compare judges *whether* something changed, never whether a change that is there is *correct*.

---

## 3. Evidence

### 3.1 The control that banned `md5`

Two captures, same tree, same route, **no edits**:

```
baseline  md5 df5493048ef42cc5f80a3715b1b5127c   98,490 bytes
rerun     md5 4dfdb6b7410aa4ccf925f4a63a784e53   98,491 bytes   -> DIFFERENT
```

An md5/byte test would have reported a difference where there is none, **on every run**. It was one command
to find and would otherwise have been written into a frozen spec as the "strengthening."

### 3.2 Mask derivation — n=5 per tab, ALL pairs

All 10 pairs per tab compared (not each-vs-first: a first-capture artefact would otherwise define the mask).

| tab | dims | pairs | pixel-identical pairs | max differing px | union bbox over all pairs |
|---|---|---|---|---|---|
| Advisors | 1440×1003 **stable** | 10/10 | **0/10** | 60 of 1,444,320 (0.00415%) | `(105,904,113,912)` |
| Distribution | 1440×1253 **stable** | 10/10 | **0/10** | 60 of 1,804,320 (0.00333%) | `(105,1154,113,1162)` |

Per-pair spread: Advisors 40–60 px, Distribution 52–60 px. **The magnitude varies; the location never does** —
the bbox is byte-identical in all 20 pair comparisons.

**`0/10` pixel-identical pairs is the load-bearing number: variance is universal, so masking is REQUIRED, not
a convenience.** An unmasked pixel test fails 100% of the time on an unchanged tree.

### 3.3 Baseline pre-state

| surface | md5 | note |
|---|---|---|
| Advisors (protected) | `df5493048ef42cc5f80a3715b1b5127c` | TOP PERFORMERS / LEADERBOARD / DATA SOURCE |
| Distribution (protected) | `71f13180d270e753bfb63d69cce4cc3e` | SEGMENT ANALYTICS / DATA SOURCE |
| Books (change surface) | `09cc74b7266877d5df0d0996a60d5df8` | empty L2 list / DATA SOURCE |

All three READ; colour law clean (silver canvas `rgb(195,202,218)`, every content block inside a dark Panel,
tab strip dark-on-silver, no light text or ghost buttons on the canvas).

⛔ **The images are the read; the RECIPE is the durable half.** Pre-state vintage:

```
portal HEAD = d43b88c5124c0b6a8ca0db49a1a8bb5826d0ea1c   branch DEV   (on origin/DEV)
node scripts/ui-smoke.mjs advisor-intelligence <out.png> --port 5175 [--click "Distribution"|"Books"]
```

Anyone can regenerate the pre-state from that ref; nobody needs my session scratchpad.

⛔ **BOTH SIDES MUST BE AT A NAMED REF — THE POST-STATE TOO.** COO standing rule (67438,
2026-08-24): *evidence is captured at a named ref, never from the shared working tree.* This spec
originally pinned only the pre-state and left the post-state IMPLIED, which is precisely how I
skipped it: my interim d-1 and d-2 masked compares were rendered off the worktree and returned
"0 differing pixels" — a true statement about a tree that contained **six other commits and a peer's
uncommitted `CategoryViewTree.tsx`**, i.e. a superposition that exists nowhere and cannot be
reproduced or falsified. Nothing was claimed from those runs, but the wording read stronger than the
measurement.

**In a shared worktree the working tree is not "current state" — it is the superposition of every
live seat's uncommitted work, and it changes between two commands.** The mis-attribution runs both
ways: a peer's change moving a protected surface would return a NONZERO that reads as mine.

**AC10 flip precondition:** the post-state is captured at a named commit, the artifact cites BOTH
refs, and `git status --porcelain` is recorded at capture time so any dirt is on the face. If a
capture must be taken against in-flight work, it is labelled *"built against the worktree at
&lt;time&gt;, UNCOMMITTED, &lt;seat&gt;'s edit in flight"* — the flag is what makes it a probe
instead of a false record.

⛔ **Trap, banked:** the tab accessible names are **title-case** (`Distribution`, `Books`) — the uppercase is
CSS. Passing `DISTRIBUTION` yields `CLICK-FAIL` **and the script still writes a PNG at the requested path**,
containing the *Advisors* tab. Two files correctly named and wrong inside. On a pre/post comparison that
produces a large, plausible, meaningless diff. Always confirm the `CLICKED:` line.

---

## 4. What this does NOT cover — stated so no one over-reads a PASS

1. **Cross-machine / cross-session stability is unproven.** 5 captures per tab, one box, one tree. 60 px is
   the ceiling I have evidence for. Whoever runs the post-state **re-runs the control on their own box first**
   and confirms the mask still bounds the noise. The mask is declared with its measured basis, not asserted
   as universal.
2. **Interaction states are not covered.** These are default-render captures. A shared-file edit could change
   a protected tab's behaviour behind a click the screenshot never triggers. That residual belongs to **(b)**,
   which is why (b) must be a *reachability* argument — "my edits are reached only through Book-face paths" —
   and not merely "the diff looked confined."
3. **Empty-data environment.** The dev backend serves no rows; both protected tabs render empty states. A
   populated environment may expose variance this mask does not bound (timestamps, live counts). Re-derive
   before trusting the mask against populated data.
4. ⛔ **(a) protects 2 of N, and N IS NOT 69 ANY MORE — 69 was this file's 2026-08-24 vintage.**
   Re-measured at portal `@9957410e` (2026-08-28): **PROTECTED 80 / CHANGE 78 / NON-SHARED 2 /
   SHARED 78**, 0 unresolved specs. The original line said *"(a) protects 2 of 69"* and was the
   number most likely to be dropped when quoted; it turned out to be the number most likely to be
   **quoted after it stopped being true**. A printed denominator is a typed number sitting beside a
   derived one, and it goes stale in silence. **Re-run `ac10_closure.py` at quote time — never copy
   this row.** Direction matters and must be stated with it: the SHARE **grew** (67 → 78), so
   **(b)+(c) carry MORE of the protection than when the criterion was written**, not less.

---

## 5. Instruments (committed beside this file)

| file | purpose |
|---|---|
| `ac10_closure.py` | AC10(a): prints PROTECTED / CHANGE / NON-SHARED / SHARED denominators + both file lists |
| `ac10_maskcheck.py` | AC10(c): `baseline` derives the pre-state from the merge relationship and author-censuses the window (run FIRST); `derive` re-derives the mask from n captures; `compare` runs the masked pre/post assertion and exits non-zero on any differing pixel outside the mask |

Both print their own denominators. `compare` **fails loud** on a dimension mismatch rather than resizing.

---

## 6. ISSUER CLAUSE — THE BASELINE IS A RELATIONSHIP, NOT A REF

**Ruled by `2.0.0_SA_COO` (issuer) 2026-08-28T18:08Z, msg 78581, on `0.4.0_DE_ClientPlatform~D`'s
78572. Transcribed here at the issuer's direction. Concurred by `1.0.0_SA_CTO` (by list).**

> For any masked-pixel or diff-class acceptance, the pre-state is the **SECOND PARENT OF THE MERGE**
> that brought this lane's commits onto the published branch — **derived at run time from the merge
> itself**, never a ref pinned earlier. The run prints
> `git log --format=%an <base>..<post>` as its **first line**, with the author census
> (*N of N this lane's*); **a commit by any other author in that range INVALIDATES the baseline
> before a single pixel is read.**

**Mechanism, not prose:** `python ac10_maskcheck.py baseline <repo> <merge-ref> <post-ref> <author>`
— exits `0` only on an all-lane window, `1` naming the foreign authors, `2` if the ref is not a merge
(it refuses rather than guessing a parent). Exercised on all three arms 2026-08-28.

### Why this clause exists — the run that produced it

This spec **already warned**, in §2 above, that *"the mis-attribution runs both ways: a peer's change
moving a protected surface would return a NONZERO that reads as mine."* The warning was read. The run
mis-attributed anyway:

```
pre @d43b88c5 (this spec's own pinned baseline) -> post @9957410e
  Advisors      FAIL  528 px outside mask   bbox (14,653,32,763)
  Distribution  FAIL  528 px outside mask   bbox (14,653,32,763)   <- IDENTICAL bbox
```

Cropped and **looked** (this spec's own method for deriving the mask): the pre-state's left nav rail
carries a **paper-plane icon** the post-state does not, and every icon below shifts up. That is
`@18fd5b38` *"remove(D7_TICKETING): FULL REMOVAL of the Submit-a-Request page"* — **a peer's commit**
(`0.3.0_DT_TradingOperations`) in shared app chrome, unrelated to this lane or either tab's content.

⛔ **The report that was one step away was "AC10(c) FAILS — my change moved the protected tabs."
A FALSE CONFESSION IS AS DAMAGING TO THE RECORD AS A FALSE PASS, AND IT IS THE DIRECTION NOBODY
AUDITS** — a seat reporting a failure against itself reads as rigorous, so it gets believed and
filed. **Both halves of a FAIL are measurements: the fact AND the attribution.** Only the fact had
been measured.

⛔ **PINNING A REF DOES NOT KEEP IT A BASELINE.** `d43b88c5..3cfa7e8a` contains **40 commits from 6
seats**. A ref is a baseline only for the commits *actually yours* between it and the post-state; it
**decays the moment any peer commits**, while continuing to look exactly as authoritative as the day
it was pinned. **A warning is not a mechanism.** The relationship does not decay:
`481a31c5^2` = `57701d5c`, window = 9 commits, 9 of 9 this lane's, and `@18fd5b38` is an *ancestor*
of the base — excluded **by construction** rather than by anyone noticing it.

COO 67438's *"named refs on both sides"* **stands and is sharpened**: named, **and** derived from the
merge relationship, **and** author-censused.
