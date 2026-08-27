# `TL2DS-AC7` — THE `D1-h-r3` SITE LEDGER

**Lane:** `0.4.0_DS_ClientPlatform~Z` · **TO:** `D1_CATVIEWS.TO-L2-DS` (`AC7` amended to seven sites
`@f4e059cf7d`) · **Date:** 2026-08-27 ~21:3xZ
**Instrument:** `comp-find 'D1-h-r3' --files --all` — **23 hits / 27,290 files scanned; 1 UNREADABLE
and 1,822 BINARY NOT searched. BANDS: SURFACED=2, DOC=21, across 6 citing files.**

> ⭐ **SWEEP THE CITATION, NOT THE TOPIC.** `comp-find -i "SMA L1"` returns **16 files** — a candidate
> set needing classification. `comp-find 'D1-h-r3'` returns **the dependents**. Sweeping what a thing
> is *about* gives candidates; sweeping what *cites* it gives what breaks.

---

## THE LEDGER — 7 FILES, RECONCILED

**6 files cite `D1-h-r3` by name + 1 file encodes the struck premise without citing it = 7.**

### CODE — 3 files

| # | site | what it is | changes on |
|---|---|---|---|
| **1** | `data/mdpf/scripts/gold/mdpf_category_registry.py:906` | `# SMA L1 = members carrying a strategy_id (D1-h-r3).` — cites the cell **as authority**; `:909-912` **executes** the derivation; `:913-914` builds `un_noded_members` as its complement | **EDIT** |
| **2** | `portal/src/api/endpoints/aum.ts:687` | `/** SMA L1 node = a member carrying a strategy_id (D1-h-r3). */` — **the docstring ON the contract interface `MdpfCategorySmaL1Node`** | **EDIT** |
| **3** | `portal/src/components/CategoryViewTree.tsx:188, :245` | stale **comments**; the **code is data-driven** (`hasAmounts = rows.some(r => r.aum != null)`; ternary on `r.aum`) | ⛔ **DATA** |

### RECORDS — 4 files. ⛔ **PRESERVE. True at their pins.**

| # | site | disposition |
|---|---|---|
| **4** | `workflows/…/d1-catviews/20260824T195537Z/DECOMP.md` | the cell itself — **AMENDED `@2ce1e1b8d5`**: Claim A preserved verbatim + vintage-stamped, Claim B struck, its oracle struck |
| **5** | `…/task_orders/D1_CATVIEWS.TO-F3-DS…md` | `D1F3DS-AC3` — ⛔ **ALREADY DISPOSITIONED (`2.0.0_SA_COO~Z`). DO NOT RE-POINT.** It consumed the **membership** half; the struck half was **level**; invariant to the restructure |
| **6** | `…/task_orders/D1_CATVIEWS.TO-R1-DS…md` | closed TO, historical |
| **7** | `…/task_orders/D1_CATVIEWS.TO-L2-DS…md` | this TO — current-era, cites the cell deliberately |

---

## ⛔ THE THREE CATEGORIES ARE NOT INTERCHANGEABLE

```
EDIT   site 1 is THE WORK -- it emits, and it is the only one whose change is a producer change
EDIT   site 2 is a CONTRACT-VOCABULARY change, not a comment fix (below)
DATA   site 3 needs NO commit to change behaviour, and that is the one to PREDICT
```

### Site 3 — the latent activation, which must be predicted and not discovered

The producer already computes `sma_member_aum` (`mdpf_gold_consolidator.py:579, 596-597`,
`@407e1e057b`). **The moment that value reaches the client block, `r.aum` is non-null, `hasAmounts`
flips true, and the SMAs card starts showing amounts and a bar — with no frontend commit.**

⛔ **Predicted-and-observed is evidence; observed-and-explained is a scramble.** The seat most likely
to misread a new bar as a regression is whoever verifies the restructure.

⚠ **I originally called sites 3 "deliberate withholdings." That was WRONG** — I read the comments and
characterised the code. `3.0.0_SA_CVO~Z` corrected it; verified at source here.

### ⭐ Site 3's comment splits the way `D1-h-r3` did — one layer down

```
PREMISE    "SMA L1 carries a strategy id and NO amount"          -> STALE, struck derivation
REASONING  "rendering $0 would say 'this firm holds none of it'
            about a firm holding millions"                        -> CORRECT, STILL LOAD-BEARING
```

⛔ **Do not strike the block whole.** The reasoning is the *never claim a measurement nobody took*
rule — the same principle as `predicate: "unavailable"` never rendering as `Unsupervised = 0`. It
survives the restructure and protects the null case that will still exist.

### Site 2 — the type NAME, not just the docstring

Under Andrew's tree, SMA **L1** = `{ETF Strategies, ALT Strategies}` and the members are **L2**.
**So `MdpfCategorySmaL1Node` names the wrong level.** Striking its docstring leaves the wrong name
standing as the contract's vocabulary. *A comment is read by whoever opens the file; a type name is
read by everyone who uses the type.* (`1.0.0_SA_CTO~Z`.)

**BOUNDED — measured, so nobody sizes it as a migration:**

    comp-find 'MdpfCategorySmaL1Node' --files --all
      5 hits / 27,290 files | SURFACED=2 hits in ONE source file (aum.ts) | DOC=3
      .runtmp copies: 0

**A contained RENAME in one source file, not a contract migration.** ⭐ **It should RIDE scope-B** —
that interface is the exact one scope-B touches (the SMA L1 node that gains `aum`). **Two edits to
one interface in one session is how a contract acquires two vocabularies.**

⚠ One of the 3 DOC hits is **my own** `ANDREW_DIRECT_20260827_SMA_SYNCHRONIZE_AND_CLIENT_L1.md`.
**Preserved, not edited** — it records a directive at its vintage.

---

## BOUNDS

- ⚠ **PORTAL VINTAGE:** submodule HEAD **`dd80c624`, branch `DEV`, THIS BOX.** **NOT verified against
  `origin/DEV`, and this checkout is known to run stale** (measured 13 commits behind previously).
  **Nothing about SERVED bytes follows.** `0.4.0_DE_ClientPlatform~Z` owns that surface.
- ⚠ **`.runtmp` INFLATION applies to the CITATION sweep, NOT the type sweep:** 4 transient
  `.runtmp/portal-promote-*/…/aum.ts` copies carry the `D1-h-r3` citation, so **a naive census
  returns 5 portal hits where 1 is tracked.** The `MdpfCategorySmaL1Node` sweep has **0**. *(I hit
  this trap earlier reading the interface out of a `.runtmp` copy.)*
- **The 21 DOC hits are NOT a strike list.** Session logs and dated `ANDREW_DIRECT` records were true
  at their pins — the same preservation rule `AC6` applied to Claim A.
- ⛔ **`AC7`'s SECOND HALF (`un_noded_members` disposition) IS BLOCKED**, not outstanding work:
  `:913` builds it as the **exact complement** of the struck predicate, so its fate is **derivable
  from** the `idvz`/`pfde` bucket answer, not choosable independently. Inside ETF Strategies →
  complement empty → **field dissolves**. Outside → **still doing work**.

---

## ⭐ ANDREW-DIRECT ~21:3xZ — ARRIVED AFTER THIS LEDGER WAS DRAFTED, FOLDED IN BEFORE LANDING

Received at `3.0.0_SA_CVO~Z`'s terminal, relayed verbatim (their 10276):

> *"Yeah all of these should be based on if there is data to populate and theyre invisible otherwise.
> this is something that agents need to be better about which is making sure that when there are
> forked routes like this, that they are structured following the same pattern, versus 2 of the 3
> doing one thing and the other one having a unique pattern, that kind of architecture is not
> acceptable."*

**⭐ IT CONFIRMS SITE 3's CODE AND CONDEMNS SITE 3's COMMENTS.** `:243` already reads
`r.aum !== null ? formatAUM(r.aum) : <strategyId>` — **that IS "based on if there is data to
populate."** The branch was never the defect; `:188`/`:245`'s **categorical** assertion
(*"SMA L1 carries a strategy id and NO amount"*) is. **The code was already right by his rule and the
prose was wrong** — which is the same direction as my own error about these sites.

**⛔ AND IT CONSTRAINS `un_noded_members` WITHOUT UNBLOCKING IT.** An **always-empty-by-construction
emitted key** is the precise opposite of *"invisible otherwise."* **So his rule points at RETIRE** —
but the field is only always-empty **under one branch of the open question**, so the disposition
stays **derivable, not chosen**. The block holds; the constraint on the answer is new.

**⭐ AND IT MAKES THE ONE-ACT RATIONALE SOVEREIGN-BACKED.** *"Structured following the same pattern"*
is his earlier *"the shapes should all be the same in layout"* restated as an architecture rule. The
`TO-L2-DS` `one_act_fence` — that ETF/ALT at L1 makes SMAs structurally identical to Models and
Client — **is now his requirement, not this lane's design preference.**

⚠ **AND THE PART I AM DELIBERATELY NOT TREATING AS AN ANSWER.** Under the reading where `idvz`/`pfde`
fall outside both buckets, **SMA becomes the one-of-three with a unique shape — the exact pattern he
just called unacceptable.** That is **evidence bearing on the open question, not his answer to it**:
he could resolve it by a third bucket, or by those members leaving the SMA set. `3.0.0_SA_CVO~Z`
declined to read it as the answer and so do I. **The question stays open; the evidence has moved.**

## HOW THIS LEDGER WAS CORRECTED — recorded because the method is the finding

I first reported *"`:906` is the only `D1-h-r3` hit in `data/mdpf/`."* **Literally true, and scoped to
my own lane while the claim it served was estate-wide.** ⛔ **I had read `aum.ts:687` forty minutes
earlier and quoted the interface on the line directly below the citation without connecting it.**
`comp-find` **without a path argument** returns both in one call.

**A true sentence whose scope is narrower than the claim it serves** is the failure mode; a declared
bound does not stop the inference it invites.
