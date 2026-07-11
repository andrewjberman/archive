# comp-which routing-quality: TO-7 corpus handoff (conduit record) -- for 0.8.0's TO-7/TO-8 corpus on spawn

**`2.0.0_SA_COO`, 2026-07-11.** *Conduit capture. `3.0.0_SA_CVO` closed comp-which (`2777924da`) + routed the
routing-quality corpus material to me (CTO item 4): `0.8.0_AE_CloudComp` (the TO-7/TO-8 corpus owner) is NOT live,
and I hold the TO-7 provenance (the Andrew-P0 paired-run exercise), so I hold this until 0.8.0 spawns. **Pickup:
0.8.0 TO-8 corpus scope on spawn.** Durable > a message.*

---

## STATUS

comp-which fix LANDED + CLOSED (`2777924da`, CTO gate-GREEN): the 5 curated rules + `--json` + grep-fallback took
the scorecard **4/12 (33%) -> 10/12 (83%)** on the N=12 verbatim CLAUDE.md catalog labels; regression 12/12,
fixture 18/18. My comp-tooltip spot-check (3/3 fires) closed separately. **The curated-rule LAYER is fixed. The
ENGINE is not** -- see below; that is the corpus's real target.

## 1. THE REPRODUCIBLE HARNESS (durable, on origin)

`org/modules/graph/tests/test_compwhich_toolpass_rules.py` (18 tests, landed `2777924da`) -- the canonical
route-assertion harness: asserts the 5 fixed routes rank-1 + bidirectional non-vacuity + regression + the `--json`
contract, exercising the LIVE launcher via `--json --route-only` (side-effect-free). **In my comp-tool-tests CI
gate's scope -> auto-enforced** (a routing regression now fails CI). The ad-hoc N=12 scorecard scripts are
reproducible but session-local (scratchpad); CVO can durably commit a full sweep-runner if 0.8.0 wants it.

## 2. THE ENGINE-LEVEL FINDING (the load-bearing corpus target -- the curated rules do NOT fix this)

**The raw fuzzy backstop is near-useless on catalog vocabulary: 0/12 top-1, 1/12 top-2.** The 5 curated rules
carry ALL the hits; strip them and the fuzzy engine alone routes correctly for ZERO of the 12 catalog labels. The
posterior's manifest-keyword-overlap layer UNDER-scores the canonical tools. **So the structural improvement for
TO-8 is the ENGINE (the fuzzy/posterior scoring on catalog vocabulary), not another round of curated patches** --
curated rules are a per-label allowlist that will always lag the catalog; the engine is the thing that should
generalize. This is the real corpus work.

## 3. KNOWN PHRASING-SENSITIVITY (corpus notes, per CTO -- left un-forced)

- `"ad-hoc non-dispatch run"` -> comp-dispatch: the terse label literally contains "dispatch"; 2/3 natural
  phrasings route right; a rule would only create a near-tie. Un-forced.
- `comp-kuzu`'s manifest-text self-route: a near-tie, never rank-1 -- a pre-existing characteristic of the tool's
  own `use_case` text (a 0.8.0-track item, not a comp-which defect).

## 4. METHOD (TO-8 law honored, from my TO-7 founding exercise)

N=12 VERBATIM CLAUDE.md catalog labels (not router-authored phrasings -- two instruments sharing a predicate are
one instrument); a POSITIVE-CONTROLLED parser (aborts on a dead parser -- the TO-7 bug-2 that nearly published
"never falls back"); the RAW-ENGINE-ALONE baseline as the ground truth for the fuzzy gap.

## DISPOSITION

- **Conduit hold.** I hold this for the 0.8.0 TO-7/TO-8 corpus; picked up when 0.8.0_AE_CloudComp is active.
- **Registration note (separate, TOOLPASS-D1):** comp-which STILL has NO tools_index one-liner (`grep -cE
  '^  comp-which:'` = 0) -- my coverage-gap worked-example #1 (the router does not index the router) is UNCHANGED
  by the routing fix; it rides the D1 reconcile, not this corpus.

**Attribution:** comp-which fix + scorecard by `3.0.0_SA_CVO` (`2777924da`, `031520Z`); TO-7 provenance +
founding method + conduit capture by `2.0.0_SA_COO`.
