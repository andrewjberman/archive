# L8 drain end -- IRPT_BCKEND round 117, workstream ~P (adds to the round 116 packet)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~03:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (3 orders),
LOCAL (1) | **Judgment criteria:** 0 | **round-close:** round 117 is MAY-CLOSE (`round-close-check.py`: orders=4, complete=4,
proof_ok=4, judgment=0)

## Round 117 (issuance @361c44fa9d): 4 of 4 COMPLETE

- **IB-pr-416** (`~278`, WORLD, row D2-S60 ruled by D2-S61): irpt-performance-adapter, irpt-narrative and irpt-status rebuilt from ONE
  commit (361c44fa9d), each built twice byte-identical, nothing uploaded. Live zips read 1 / 1 / 1 name mismatches; built zips read 0 on
  the name, attribute and method limbs.
  - The worker died in the 2026-10-10 crash mid-cell and was re-seated on the same worktree. It could not commit its six rows: its stale
    base still carried a served account number on channel line 9574 (redacted on box/dell2 since). The issuer landed rows
    D2-W278-S1..S6 verbatim @1a0316684f under an audited surprise-row override, then drained @04fbbd0a91.
  - **Issuer re-grade at box/dell2: AC1 PASS, AC2 PASS, proof VALID.** Flipped @c2644f24a4.
  - Pair: COO half @c362f7e0fb; CTO half @d29ccddb17 (conditions 1-9). The pair names THREE widenings that ride with the one commit:
    `analysis-request-read` for svc-custody-statement (IB-pr-405), `svc-commentary` on retention reserve, and `svc-irpt-packager` reading
    ANALYSIS_COMMENTARY (both 3fc99be70f).
- **IB-pr-417** (`~279`, WORLD): the 49F narrow bundle = IB-pr-410's members + IB-pr-414's memory fix. Three halves signed at packet blob
  36621e44cb (COO @c7b3f175b7, CTO @89003a204b, dell1 `2.0.0_SA_COO~M1` blob 8f0ef159d3).
- **IB-pr-418** (`~280`, LOCAL): the containment code cell; drained @cc4aba9d25, AC1 and AC2 PASS on the issuer re-run.
- **IB-pr-419** (`~281`, WORLD, read-only): the live-call read of D2-S60; it read irpt-performance-adapter as FAILING closed on
  performance-report.

## Rows for the compile

- **D2-W278-S1..S6** (IB-pr-416): S2 is ARMED, disarm owner `2.0.0_SA_COO~P2`. Its state is met: the three candidate source-map entries
  landed @5c35a6f9f9 (`~IB2`, TO-IB-pr-420 step 1; issuer read the three entries equal to the candidate). The resolving row is owed by
  this seat. S1, S3, S4, S5, S6 are INERT observations.
- **D2-S64** (`~IB2`): `checks/r114/p114_cells.py` still graded IB-pr-410's artifact after AMENDMENT 3. An issuer check defect, repaired
  by TO-IB-pr-413 AMENDMENT 5 @cdb4fec479. The resolving row is owed by this seat.
- Channel line 9574 on any stale branch base: a client account number that IB-pr-418's scope (code files) did not cover. On box/dell2
  it is redacted; a worker branch cut before that redaction refuses the channel file at commit.

## Carried, not closed by this round

- **Round 114, IB-pr-413** (`~IB2`): IB-pr-417's bundle is LANDED on the 49F key (version `fMLoOI6a8ZwNFWZCJjjP90ZadyRg9nFg`, ETag
  `8b482c8db26c2e913aeee72023bacc7e`; the issuer re-read both). Replay on the uploaded bytes and the memory peak (0.863 of the limit) are
  `~IB2`'s report, not re-read here. Its first fire is Monday 2026-10-12 14:15Z; IB-pr-404's L6 closes on the same read.
- **Round 118, IB-pr-420** (`~IB2`, issued @cdd88ba4cb): applies the adapter, then the narrative, under the IB-pr-416 pair. Not applied
  at the time of writing: both functions read their pre-apply CodeSha256 at 03:47Z. irpt-status's apply is `2.0.0_SA_COO~Y2`'s.
- **The one real run of round 117's outcome** is the live-call arm at each apply (IB-pr-420, and ~Y2's irpt-status apply). Round 117
  itself built and applied nothing, so no served run exists yet; ABSENT, not exercised.

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes); re-measured in the send.
