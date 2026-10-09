# AMGT_CORPUS -- L5 decomposition v41.0 PRE-DRAFT (NOT ISSUED) -- ROUND 41

**Issuer:** `2.0.0_SA_COO~C1`, pre-drafted 2026-10-09 ~05:4xZ; revised ~05:4xZ on the analysis pre-draft's AMENDMENT 1 (msg 1777) beside the CTO's
`ledger/ROUND_ANALYSIS.round40.PREDRAFT.md` (msg 1771). It is cut into `decompositions/AMGT_CORPUS_DECOMP.md` and issued in ONE
issuance only after that analysis is ISSUED (after the round-40 slug). Every item number below is the analysis's.

## 0. The rectangle

| # | item | cell | path | risk |
|---|---|---|---|---|
| 1 | a passage ends at a sentence end (read across page breaks, or an explicit ellipsis) | `CRPS-aq-1` | worker `~1` | LOCAL |
| 2 | a passage starts at a word boundary (scorecard prefix) | `CRPS-aq-2` | worker `~1`, after aq-1 (same file) | LOCAL |
| 3a | the header feed matches a headline only against `terms[1:]` (the matched vocabulary terms), never the pillar title; a name with no real terms shows no filtered feed and says so | `CRPS-aq-3` | worker `~2` | LOCAL (portal DEV candidate, CTO render review) |
| 3b | names with no real terms (112 of 163 pillars): the KPI vocabulary | -- | NOT cut: CRO research for round 42 (analysis AMENDMENT 1) | -- |
| 5 | row Z-S90 batch repair: the census learns three origins | `CRPS-aq-4` | worker `~3` (worker-light) | LOCAL |
| 1s-2s | the SERVED half: the dossier re-write at the next method, then the c1/c2 census on the served objects | `CRPS-aq-5` | the issuer's paired act, after aq-2 drains | SERVED |
| 4 | UNVGY's served no-forecast reason | -- | NOT a CORPUS cell: AMGT_RESAPP's next round (analysis item 4) | -- |
| R/U | a leg-v grader verdict below MET (analysis "Either branch") | `CRPS-aq-6` if needed | issuer, at most three criteria | per leg |

**Chains:** `aq-1 -> aq-2 -> aq-5`; `aq-3`; `aq-4`. `fanout: 3 of 3 worker chains, cap 8`.

**Write sets (disjoint; census of non-terminal orders naming these paths owed at the cut):**
- aq-1, aq-2: `lib/research/corpus/dossier.py` and the dossier test files the cut names;
- aq-3: ONE mount line in `portal/src/pages/SecurityAnalysis/components/SecurityOverlay.tsx` (:499 at the pre-draft, where the
  pillars' terms are FLATTENED before `HeaderBrief` sees them, so the per-pillar `terms[1:]` slice can only go there:
  `flatMap((p) => (p.terms ?? []).slice(1))`), plus `HeaderBrief.tsx`'s no-real-terms sentence (`FeedList`, :151-160); NOT
  `continuation.py` (its RULED shape stands);
- aq-4: `lib/research/corpus/readonly_proof.py` and `lib/research/corpus/tests/test_readonly_proof_bound.py`.

## 1. The cells (criteria, at most three mechanical each; checks dry-run at the base before the cut)

**CRPS-aq-1.** Check `checks/round41/aq1_check.py`: the c1 census (`checks/round40/r41_passage_census.py`) run on values
re-composed in memory reads `cut 0` or each remaining value marked; control: the six of CTO msg 31382 read whole. Base today:
`cut 29 dangling 8`.

**CRPS-aq-2.** Check: the same census reads `prefix 0`; control: a management passage with no prefix is unchanged. Base today:
`prefix 2` (BABA US, ST SP).

**CRPS-aq-3.** (analysis AMENDMENT 1 item 3a) The feed matcher drops the first term (the pillar label) before matching. Check
`checks/round41/page_check.cjs aq3`: on IMB LN's served terms, a headline naming `net debt` matches and a headline naming only
"Clean balance sheet for a Tobacco company" does not; control: a name whose pillars carry no real term renders the sentence that no
filtered feed exists, and no filter control. `_pillar_terms` and `test_continuation_terms.py` are untouched.

**CRPS-aq-4.** Check: `test_code_census_arm_leaves_no_amgt_corpus_entry` passes; `--code-census` reads `unresolved 0` with both
positive controls flagged. Base today: `unresolved 6`, test FAILED.

**CRPS-aq-5 (SERVED).** One never-widen pair to `1.0.0_SA_CTO~DELL1`: the dossier re-write at the next method version; after it,
the c1/c2 census on the SERVED objects reads as aq-1/aq-2's checks did in memory. Not a site-Z
producer path (dossier and continuation writers run from dell1) -- to confirm against the producer census @6a308cd424 at the cut.

## 2. Not in round 41 (analysis): anything that changes the 13:00Z fire's call, field list or address.
