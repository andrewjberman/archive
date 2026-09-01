# TO-R1-DE — PRE-REGISTERED PREDICTIONS for the post-push render read

**Written 2026-09-01 07:5xZ, BEFORE the portal DEV fast-forward lands** (dispatched to
`0.0.0_AB_MSTR` at COO 90948 s.1; local merge `7d0ca60c1d`, `origin/DEV` still `89ecfd8947`
at authoring time). Pinned here so the AC11 / GATE A verdicts cannot be fitted to whatever
the page happens to show.

This lane's own precedent: *"PREDICTIONS ON RECORD BEFORE THE ACT so they cannot be fitted
afterwards"* (TO-R1-DE issuer record, 16020 s.3).

---

## THE INPUT STATE, MEASURED

Served at `platinum/advi/49financial/` (`s3api list-objects-v2`, 2026-09-01 07:2xZ):

```
  SERVED      perfrp_book_advisor.json            15,001,561 B
              perfrp_performance_account.json      1,923,593 B
              perfrp_gainloss_account.json        11,896,644 B
              perfrp_gainloss_relationship.json    7,419,826 B
  NOT SERVED  perfrp_performance_relationship.json     <- the L3 performance leaf
              perfrp_allocation_account.json
              perfrp_allocation_relationship.json
              perfrp_transactions_relationship_sample.json   (deferred by ruling)
```

The push carries `perfrpLeafBase()`, which points every fetcher at exactly this key class.

---

## ⛔ THE HEADLINE PREDICTION, AND IT IS COUNTERINTUITIVE

**THE L3 PERFORMANCE CARD WILL STILL RENDER A SHELL AFTER A FULLY SUCCESSFUL PUSH.**

`AdvisorBookView.tsx` binds L3 from `perfrpRelationshipLeaf` = `getPerfrpPerformanceLeaf('relationship', …)`
→ `perfrp_performance_relationship.json` → **NOT SERVED** → 404 → null → shell.

>> **This is the card on Andrew's original screenshot, at the grain he was looking at.** A
   reader who sees it still empty after the push will conclude the push failed or the fetcher
   fix is wrong. **It will not be either.** The fix will be working correctly against a leaf
   that does not exist yet. <<

**Recording it now so that outcome is a CONFIRMED PREDICTION rather than a fresh alarm** —
this is the fourth time on this surface that a correct act would have been read as a defect.

## PER-CARD, L3 (relationship grain)

| card | leaf | served | PREDICTED |
|---|---|---|---|
| Activity Summary | none emitted | — | SHELL |
| Performance | `performance_relationship` | NO | **SHELL** |
| Allocation | `allocation_relationship` | NO | SHELL |
| Gain/Loss | `gainloss_relationship` | **YES** | **POPULATES — figures** |
| Transactions | `transactions_*` | NO (deferred) | SHELL + its 2 declared absences |

## PER-CARD, L4 (account grain)

| card | leaf | served | PREDICTED |
|---|---|---|---|
| Performance | `performance_account` | **YES** | **POPULATES** |
| Gain/Loss | `gainloss_account` | **YES** | **POPULATES** |
| Allocation | `allocation_account` | NO | SHELL |

## BOOK VIEW

`perfrp_book_advisor` is served → the four ruled KPI tiles **POPULATE**, and the L2
client table populates. ⚠ It carries the real client labels; that is Andrew-ruled and
not a blocker (01:2xZ, `cef11e66cd`).

---

## WHAT EACH OUTCOME MEANS — fixed in advance

```
  Gain/Loss populates at L3 AND Performance populates at L4
      -> GATE A DISCHARGED. The advi/{firm}/ key class is EXERCISED end-to-end:
         published -> served -> fetched -> rendered. This is the exercised half
         precondition #2 has never had.

  NOTHING populates anywhere
      -> the fetcher fix did NOT land, or landed and is wrong. Check ancestry FIRST
         (merge-base --is-ancestor 7d0ca60c1d origin/DEV, with a positive control)
         before touching any code. Deployed bytes are a third plane again --
         origin/DEV is not the bundle.

  Everything populates INCLUDING L3 Performance and Allocation
      -> MY INPUT STATE IS STALE. More leaves were served after 07:2xZ.
         Re-list before concluding anything. A better-than-predicted result is a
         signal to re-measure, not to celebrate.
```

## ⛔ ISSUER RULING 2026-09-01 08:5xZ (COO 91090) — AC11 IS BARRED FROM SCORING

**Added after this file was committed, because a stale prediction file is a carrier a future
reader hits first.** `2.0.0_SA_COO` has ruled: **do NOT score `PRFR1DE-AC11` until the
weighting harness is LIVE AND DISCRIMINATING. A green before then is INADMISSIBLE, not
merely weak.**

Ground (my own reasoning, adopted as the ruling's basis): a cross-level equality compares the
producer's parent against the producer's own children, so **both sides carry the same defect —
one artifact read twice, not two witnesses.** `0.4.0_DS_ClientPlatform~G`'s sign-flip fixture
makes it concrete: weighted `+2.01%` vs naive `-5.68%`, **opposite in sign**, and a
producer-to-producer comparison agrees at BOTH.

The harness (`perfrp_ac11_weighting_on_emit_path.py`) is DEAD and has not run green since a
Round-2 rewrite. Its repair rides ADVI_PERFRP as a **precondition of this criterion**, owned by
`0.4.0_DS_ClientPlatform~G`. ⛔ **This bars ONE CRITERION'S SCORING, not the TO** — every
AC11-independent criterion proceeds.
⚠ **And nobody may report "the rollup is naive" on the strength of a dead harness.** Whether the
rollup is actually unweighted is UNMEASURED and stays so until the arm runs. Absence is not a
verdict.

## ⛔ CORRECTION 2026-09-01 13:5xZ — AC11 IS A **RECOMPUTE**, NOT AN EQUALITY CHECK

**This file described AC11 in the TO's paraphrase. The authoritative cell says something
stronger, and I am fixing the carrier rather than leaving the weaker word in the file a
future reader opens first.**

`DECOMP.md:71`, `PRF-inv-3` oracle column, verbatim and read at source by this seat:
> **`DS+DE · recompute each level from the level below on the served block; print all three`**

```
  THE CELL (authoritative)          "RECOMPUTE each level from the level below"
  TO-R1-DE issuer records (derived) "cross-level EQUALITY" / "displayed-equality test"
```
⛔ **A RECOMPUTE DERIVES THE PARENT INDEPENDENTLY AND COMPARES IT AGAINST THE SERVED PARENT.**
So a naive-mean parent and an MV-weighted derivation DIFFER and the test FAILS — which is
exactly the discrimination the vacuity warning below said was missing. **The vacuity risk was
real for the EQUALITY form and does not apply to the form the cell actually specifies.**
⚠ **The guard below still stands and I now expect never to reach it** — which is the right
shape for a guard, not a reason to delete it.
⚠ **The scoring bar is UNAFFECTED and I did not ask for it to lift.** The weighting harness
tests a different plane (does `_performance` CALL the shared law), and the recompute cannot run
until `performance_relationship` is SERVED, which it is not.

## ⛔ AC11 IS **NOT** DISCHARGED BY ANY OF THIS, AND I AM SAYING SO BEFORE THE READ

AC11 is a CROSS-LEVEL displayed-equality test. It needs the **same entity** readable at two
levels. Performance is served at **account grain only**; the relationship grain is absent.
**So the cross-level leg cannot be constructed for performance no matter how the render
looks.** Gain/Loss is served at BOTH grains — so if AC11 is computable at all after this
push, it is computable **on gain/loss and on nothing else**, and any AC11 verdict must name
which family it was computed on.

⚠ And the fixture-key caveat survives the serve: a cross-level equality is meaningful only
if both levels key to the same real entity. Real keys make that possible; they do not make
it automatic. **The read will name the join entity or it is not a verdict.**

---

## WHAT WOULD FALSIFY THE WHOLE FRAME

If `perfrp_performance_relationship.json` appears in a later listing, the headline
prediction is void and L3 Performance should populate. **Re-list immediately before the
render read** — the input state above is a measurement with a timestamp, not a constant.
