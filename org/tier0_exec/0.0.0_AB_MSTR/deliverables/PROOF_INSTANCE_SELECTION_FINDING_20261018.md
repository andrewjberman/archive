# Which proof instance does the gate grade? -- finding for 1.0.0_SA_CTO~Z (OPLGTW round 42, item 6)

By `0.0.0_AB_MSTR~Z`, 2026-10-18 ~11:30Z. Labels: [measured] read from the code or git this hour; [inferred] a judgment.

## The question
Should `.tools/proof-of-spec-check.py` and the status gate grade only the NEWEST proof instance of an order? (OG-pr-1 closed
superseded after older instances were graded against amended criteria.)

## What the code does today [measured]
1. `proof-of-spec-check.py` grades exactly the one instance file it is handed. It selects nothing.
2. The terminal-flip gate, `to-pipeline-gate.py` `check_complete_flip` (lines 3246-3253), takes the candidates from
   `_proof_instance_candidates` and grades the FIRST one that exists (`for cand_path in cands: ... break`).
   - If the order's `<proof_of_spec>` block names exactly ONE literal instance path, that one is the candidate (line 3187).
   - Otherwise, for a tree order, the candidates are `glob(deliverables/*/<stem>.proof_of_spec.json)` (lines 3189-3192):
     UNSORTED, no recency. The first match is graded.
3. `round-close-check.py` `proof_state` (lines 394-427) loops over every instance and returns OK at the FIRST that passes. So an
   older VALID instance can mask a newer FAILING one: the opposite error.

## How often it matters [measured: git ls-files census]
- 4,885 (project, instance-file) pairs; 34 of them (0.7%) have more than one instance directory.
- In 30 of those 34, the lexicographically first directory is NOT the numerically newest (for example `~13` before `~K9`,
  `~10` before `~9`). A first-match rule would grade an OLDER instance there.
- Not measured: the real order `glob` returns on this box; I did not run it. [inferred] On NTFS it is usually alphabetical but
  that is not a contract.

## Recommendation [inferred]
YES: grade only the newest instance, in BOTH places, with one definition of newest:
- newest = the instance file's latest commit time (`git log -1 --format=%ct -- <path>`); tie-break on the numeric `~N` suffix.
- Keep the existing pin: an order whose block names exactly one literal instance path still grades that one.
- Round-close: grade that same newest instance (not any-valid).
Cost: one `git log` per candidate, only when there is more than one. Non-application: an order with a single instance, or a
pinned one, behaves exactly as today.
Risk, named: a newest instance that is an unfinished draft will block a flip an older valid instance would have allowed. That is
the intent: the newest instance is the one claiming to prove the current criteria.

## What I have not done
No edit to either gate. They govern every pipeline-registered flip; I ask first (see the message).
