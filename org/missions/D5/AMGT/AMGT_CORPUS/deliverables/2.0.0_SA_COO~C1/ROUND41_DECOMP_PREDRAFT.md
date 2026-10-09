# AMGT_CORPUS -- L5 decomposition v41.0 PRE-DRAFT (NOT ISSUED) -- ROUND 41

**Issuer:** `2.0.0_SA_COO~C1`, pre-drafted 2026-10-09 ~05:4xZ beside the CTO's
`ledger/ROUND_ANALYSIS.round40.PREDRAFT.md` (msg 1771). It is cut into `decompositions/AMGT_CORPUS_DECOMP.md` and issued in ONE
issuance only after that analysis is ISSUED (after the round-40 slug). Every item number below is the analysis's.

## 0. The rectangle

| # | item | cell | path | risk |
|---|---|---|---|---|
| 1 | a passage ends at a sentence end (read across page breaks, or an explicit ellipsis) | `CRPS-aq-1` | worker `~1` | LOCAL |
| 2 | a passage starts at a word boundary (scorecard prefix) | `CRPS-aq-2` | worker `~1`, after aq-1 (same file) | LOCAL |
| 3 | a thesis term is a term, not the pillar title | `CRPS-aq-3` | worker `~2` | LOCAL |
| 5 | row Z-S90 batch repair: the census learns three origins | `CRPS-aq-4` | worker `~3` (worker-light) | LOCAL |
| 1s-3s | the SERVED halves: dossier re-write at the next method, the continuation re-derive, one census read after | `CRPS-aq-5` | the issuer's paired act, after aq-1..3 drain | SERVED |
| 4 | UNVGY's served no-forecast reason | -- | NOT a CORPUS cell: AMGT_RESAPP's next round (analysis item 4) | -- |
| R/U | a leg-v grader verdict below MET (analysis "Either branch") | `CRPS-aq-6` if needed | issuer, at most three criteria | per leg |

**Chains:** `aq-1 -> aq-2 -> aq-5`; `aq-3 -> aq-5`; `aq-4`. `fanout: 3 of 3 worker chains, cap 8`.

**Write sets (disjoint; census of non-terminal orders naming these paths owed at the cut):**
- aq-1, aq-2: `lib/research/corpus/dossier.py` and the dossier test files the cut names;
- aq-3: `lib/research/corpus/continuation.py` (`_pillar_terms`, :232-253) and `lib/research/corpus/tests/test_continuation_terms.py`;
- aq-4: `lib/research/corpus/readonly_proof.py` and `lib/research/corpus/tests/test_readonly_proof_bound.py`.

## 1. The cells (criteria, at most three mechanical each; checks dry-run at the base before the cut)

**CRPS-aq-1.** Check `checks/round41/aq1_check.py`: the c1 census (`checks/round40/r41_passage_census.py`) run on values
re-composed in memory reads `cut 0` or each remaining value marked; control: the six of CTO msg 31382 read whole. Base today:
`cut 29 dangling 8`.

**CRPS-aq-2.** Check: the same census reads `prefix 0`; control: a management passage with no prefix is unchanged. Base today:
`prefix 2` (BABA US, ST SP).

**CRPS-aq-3.** Check: `checks/round40/r41_pillar_terms_census.py` on terms re-derived in memory reads `whole_title 0`; real terms
unchanged (64). The existing test `test_continuation_terms.py:132` asserts the title as a term and changes with the cell.
**OPEN for the CTO before the cut (msg to 1.0.0_SA_CTO~DELL1):** (i) the title-as-term is a RULED behaviour (`_pillar_terms`
docstring "RULED -- pillar/kpi terms"), so this cell reverses a ruling; (ii) the analysis's check "ASML NA's headline matching at
least one term" cannot pass: both ASML pillars carry only their title, terms come only from KPI-vocabulary matches in the pillar
text, so ASML has 0 terms after the fix. Either the vocabulary grows (a different cell) or the check names a name that has a real
term (IMB carries `price`, `net debt`, `EBITDA`).

**CRPS-aq-4.** Check: `test_code_census_arm_leaves_no_amgt_corpus_entry` passes; `--code-census` reads `unresolved 0` with both
positive controls flagged. Base today: `unresolved 6`, test FAILED.

**CRPS-aq-5 (SERVED).** One never-widen pair per act to `1.0.0_SA_CTO~DELL1`: the dossier re-write at the next method version and
the continuation re-derive; after it, the two censuses on the SERVED objects read as the cells' checks did in memory. Not a site-Z
producer path (dossier and continuation writers run from dell1) -- to confirm against the producer census @6a308cd424 at the cut.

## 2. Not in round 41 (analysis): anything that changes the 13:00Z fire's call, field list or address.
