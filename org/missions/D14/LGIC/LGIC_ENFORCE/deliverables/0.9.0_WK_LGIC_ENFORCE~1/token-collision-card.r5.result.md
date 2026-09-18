# LGIC_ENFORCE.TO-EN-c-31-r5 -- result

`0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-5-3`, committed `f67dbcbbc0` (base `b87bb7d8db`).

Cards 5 and 6 of `OWNER_CARDS_R4.md` corrected per R-39 (row `LGIC_ENFORCE-W1-S30`). `security` remains
unminted anywhere in `infra/logic/registry/systems.json` (whole-value count 0, unchanged) and the vocabulary
is not reshaped. Both cards now state their reason as `TOKEN_COLLISION`: Card 5 (security-sweep tooling,
`NFRA_TERRAFORM`, closed and unregistered) names Card 6's `opal-data-security` group as the other side of
the collision; Card 6 states plainly it has a genuine, already-cited owner (D12 / `NFRA_OPSEC202609`,
`org/missions/DIRECTIVES.yaml` :485) and is carded only because the single `security` token cannot carry
both groups' distinct ownership, not for want of a search. No other card was touched, `systems.json` and
`resources.json` were not written, and `security-sweep-*` was not renamed.

## Criteria

- `C31R5-AC1` (c31-card): **PASS** -- `VERDICT: PASS-C31-TOKEN-COLLISION-CARDS-CORRECTED`, pre-commit, twice
  post-commit (determinism control), and once more after a mutant-and-restore cycle (3 of 3 post-commit runs).
- `C31R5-AC2` (c31-not-minted): **PASS** -- `VERDICT: PASS-C31-SECURITY-NOT-MINTED-WITH-A-LIVE-CONTROL`, guard
  held (this cell never wrote `systems.json`), positive control key `'mdpf'` printed to rule out a blind reader.
- `C31R5-AC3` (judgment): recorded `UNVERIFIABLE-BY-INSTRUMENT`, status_reason names `3.0.0_SA_CVO` at L9. No
  verdict given by this worker.

## Mutant control

Before committing this proof, replaced every `TOKEN_COLLISION` occurrence in the live file with
`TOKEN-CLASH-MUTANT` and re-ran `c31-card`: both Card 5's and Card 6's checks flipped to `False` and the arm
read `VERDICT: FAIL-C31-TOKEN-COLLISION-CARDS-CORRECTED`. Restored the exact committed bytes from a `.scratch`
copy (`git diff --stat` on the file showed no change against the committed blob afterward) and re-ran both
criteria: both `PASS` again. Fired as expected.

## Surprise filed

None. Both arms (`c31-card`, `c31-not-minted`) discriminated exactly as the order described; no defect was
found in `check_en_r5.py` itself on this cell, unlike the two prior cells in this round's queue.

## Proof

`LGIC_ENFORCE.TO-EN-c-31-r5.token-collision-card.proof_of_spec.json`, this directory.
