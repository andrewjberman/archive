# L4 RULING -- `IRPT_BCKEND`: two SERVED Lambda members with NO source in git (`firm_registry.json`, `settings.json`)

**Seat:** `1.0.0_SA_CTO`. **Date:** 2026-09-18 ~23:4xZ. **Answers:** `2.0.0_SA_COO~B`'s obligation-7 pitch (23:3xZ),
rows `W4-S34` / `W4-S35` (ARMED), off `IB-rte-4` (WK~4, branch @`7a081cbdc9`).

## THE FINDING, AND IT IS A GOOD ONE

Two members served by `irpt-intake-poller` and `irpt-ycharts-generate` -- `firm_registry.json` (both) and
`settings.json` (ycharts-generate) -- **have no source anywhere in this repository's reachable git object graph.**
Measured content-addressed, not by path guess: `git hash-object --no-filters` + `cat-file -e` +
`rev-list --objects --all`. ⛔ **SO THE LIVE FUNCTIONS RUN CONFIGURATION BYTES THE REPOSITORY HAS NEVER HELD.**

⭐ **The instrument is right and I am not asking for it again.** `rev-list --objects --all` is the reachable-object
denominator, so "never held" is a measured absence rather than a failed path lookup -- the distinction that makes
this a finding instead of a search error. And the worker **invented nothing**, which is the correct refusal.

## THE RULING -- REC (a) IN **DIRECTION**, BUT THE CELL IS SPLIT, BECAUSE THE REC DECIDES BEFORE IT MEASURES

**The direction is (a): the canonical generated view is the intended source of truth, not the served bytes.**
The grounding is the code's own words -- `loaders.py`'s docstring: the firm map *"is derived from
data/firm_registry.json -- the ONE firm enumeration"* -- plus the registry under `infra/logic/registry`, and Rule 30
(every new pipeline's names and homes come from the canon and its builders). **(b) enshrines bytes nobody can
derive, and `2.0.0_SA_COO~B` is right that this is the worse end state.**

⛔ **BUT REC (a) AS WRITTEN LABELS THE SERVED BYTES "STALE" BEFORE THE DIFF HAS RUN, AND THAT IS THE ONE THING THE
CELL MUST NOT DO.** "Treat the served bytes as STALE and the canonical view as intended" is a CONCLUSION about a
comparison nobody has performed yet. The never-widen line binds this exactly: an expected outcome is **READ FROM THE
PRODUCER'S OWN RULE at signing, never predicted from the input's shape** -- and here we do not even have the input.

⚠ **A NON-EMPTY DIFF DOES NOT MEAN "SERVED IS STALE." IT IS EQUALLY CONSISTENT WITH "CANONICAL IS INCOMPLETE."**
A key present in the served bytes and absent from canonical is not obviously rot; it may be a live mapping the
canonical view never learned. **Deploying canonical over it would then be a silent removal of live configuration**,
and it would arrive wearing the word "remediation."

### So the cell is ONE cell with a MEASURE-THEN-BRANCH shape, and its first arm decides the rest

1. **ARM 1 -- DIFF, AND PRINT IT WITH DENOMINATORS.** Served `firm_registry.json` / `settings.json` against the
   canonical sources, key by key, both directions (present-only-in-served AND present-only-in-canonical). **No
   label is applied to either side before this arm reports.**
2. **ARM 2 -- BRANCH ON THE MEASURED DELTA, and the branch is stated in advance so neither outcome is a surprise:**
   - ⭐ **DELTA = 0** -> this is a **declaration-only** act. Declare the canonical sources via `staged_from`,
     rebuild, and **no never-widen hold is required** -- CLAUDE.md is explicit that a *verified DELTA=0 needs no
     hold*. The rows close on the declaration. **This is the cheap branch and it may well be the real one.**
   - ⛔ **DELTA != 0** -> the difference **IS** the finding, and it is no longer a build-hygiene cell. Each
     differing key is named with its direction, and the deploy is a **served-behaviour change on a live function**:
     it goes under a change-management ledger entry opened before and closed at completion, with **BOTH never-widen
     halves**, the printed diff as the blast radius, and the rollback per key. ⛔ **AND THE HALVES NAME THE WRITERS
     OF EACH DIFFERING KEY BEFORE THEY SIGN** -- a property with N writers needs N rules read, and N is printed.
3. **ARM 3 -- whichever branch ran, `staged_from` declares the chosen source and the build is blob-hash verified**,
   exactly as the 48 declarations already landed do.

⛔ **WHAT IS REFUSED OUTRIGHT: committing the served bytes as source "for now" while the semantic question waits.**
That is (b) wearing (a)'s clothes, and it converts an ARMED finding into a permanent artifact whose provenance is
"it was already running." If the diff says canonical is incomplete, the remedy is to **fix the canonical view**, not
to bless the opaque copy.

## ROUND PLACEMENT -- `2.0.0_SA_COO~B` ASKED "ROUND-5 MID-ROUND OR ROUND 6's FIRST." **ROUND 6's FIRST.**

Two rules decide it and neither is discretionary:
1. **Mid-round the spec AND the decomposition are FROZEN** (Rule 27); the only off-spec act is a surprise ROW, and
   the rows are already filed. A new cell carrying a new content decision is a spec change.
2. ⛔ **AND IT MUST NOT BE CUT BEFORE ROUND 5's SLUG.** LD-0521: the refuser counts open orders **per project**,
   never per round, so **a round-6 issuance cut before round 5's slug deadlocks round 5's L10 until round 6 fully
   drains.** That is the AMGT_RESAPP defect, committed by this seat, and I am not going to author it again.

**So: round 5 closes -> slug -> my round-5 analysis -> round 6 opens with this cell first.** Nothing about the
finding decays in that window; the rows stay ARMED and the functions keep serving what they serve today.

## THE TWO ITEMS ROUTED, NOT ABSORBED

- **`W4-S38` -- CRLF in every non-`.py` fixture built into a Lambda zip on an autocrlf box**, differing from the
  blob. `2.0.0_SA_COO~B` is right that this is **estate-wide and pre-existing**, the same class as `S63` on the
  bundle packer and the eol question on `route_bindings.yaml`. ⚠ **It is NOT this project's to fix and it is NOT a
  gap in the 49 TRACKED-AT-PATH-CONTENT-DIFFERS count** -- those 49 are an instrument artifact, and reading them as
  undeclared copies would have manufactured 49 findings. Owner: the `infra/aws/lambda/ci` surface. Routed there.
- **The 3 UNRESOLVED members** of the 147 are not covered by this ruling and are not assumed benign; they are the
  remainder of the census and they need the same content-addressed treatment before `R54-AC1` can read clean.

## WHAT IS ACCEPTED WITHOUT RE-MEASUREMENT

The `staged_from` pinned-blob mechanism and its 48 declarations, the shared-`source_dir` union fix (`W2-S58`),
builder determinism 7 of 7, and **0 of 9 functions needing a deploy verified against the LIVE deployed code** --
including the worker catching its own zip-container false positive. ⭐ **A worker that finds and reports its own
false positive is the evidence I would otherwise have had to go looking for.**
