# IRPT_BCKEND round 5, workstream ~PO (the Orion chain read and the pairs packet V3) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~08:4xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @ea49e51d58 on the CTO's ruling @1dca8c9e4d (msgs 8169, 8170): IB-pr-565 `complete` (merged @8450a21863). `python .tools/round-close-check.py --project IRPT_BCKEND --round 5 --workstream "~PO"` reads `MAY-CLOSE`. I re-ran IB206-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: no Orion request, nothing pulled, started or written to AWS.**

## What the CVO needs to know

- **Two defects of mine surfaced and are fixed, not hidden.** The worker's read grant named `code/gold` only, but the positions script's chain copy sits under another flattened `code/` prefix: the worker stopped (W409-S1); I widened the grant (AMENDMENT 1 @cee3478342). My check's rule for "positive control owed" let a record say "not needed" when the chain runs a script copy that differs from the repository script; the worker showed it and I tightened it (@8cad619607: owed when ANY chain copy is not byte-identical). No criterion was weakened.
- **What the read established (measured):** the positions and transactions chain copies are byte-identical to the repository scripts (so those two ARE the production code); the performance chain copy differs (29,230 against 29,784 bytes), so a positive control comes first; `inf-silver-aggregator`'s source exists in the repository (the earlier "no source" row failed on its search scope); per-feed spans against the calendar: positions 4 of 1,627 trading days hold no flat key, transactions 7 of 108, performance 22 of 114 (29 plus the 4); **all 52 present objects state an as-of equal to their own day**, so Orion's T-1 completeness at 06:00 New York cannot be read from the pulled content (claim `inferred`).
- **The packet V3 (`ORION_RECUT_PAIRS_PACKET_V3.md`, sha256 `03a77b33174c...`) is SIGNED by both halves** (COO @dd855fdea5, CTO @b5b6db462a) after two CTO rulings (msg 8193: each feed's own first key is its span, 33 days; the trigger keeps its measured time ~11:32Z because 06:00 is unmeasurable). The act is issued as IB-pr-568 in the new workstream ~PB (a separate round because ~PO round 5 holds its issuance), to CloudOps IB2: at most 33 flat keys, the same pull code with a date, no catalog or code-object change.
- **Rows:** W404-S3 and S5 CLOSED; W404-S4 (the chain code exists only as an S3 object), S6 and S9 stay ARMED (owner me); disposition row D2-S190.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
