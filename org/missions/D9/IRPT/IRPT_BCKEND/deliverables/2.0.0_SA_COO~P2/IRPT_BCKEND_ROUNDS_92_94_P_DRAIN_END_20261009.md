# L8 drain end -- IRPT_BCKEND rounds 92-94, workstream ~P (adds to the rounds 90-92 packet @18d4c45c1d)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~02:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | round-close: round 92 MAY-CLOSE, round 93 MAY-CLOSE.

## Round 92 -- IB-pr-380 (COMPLETE, worker ~188, proof @97da18538b; drained @3ff1ed35fa)

- Implements CTO ruling msg 1959 in refresh.py:
  - an entry absent from both the build and the source is carried as TERMINATED;
  - an entry in the source but missing from the build stays REFRESH_FAILED.
- P is 8953eccfca. Graded by the issuer, IB92-1-AC1..AC3 PASS:
  - 11 `terminated_carry_forward` tests; the suite passes 201 of 201;
  - replay: READY with terminated 1 at both firms; live and negative arms REFRESH_FAILED.
- Rows found the release alone fail-closed with no gain:
  - D2-W188-S1: the runner writes the served directory;
  - D2-W188-S2: a previous-state window gap at inflection;
  - D2-W188-S3: no contract field, so the date goes in effective_date plus a marker.

## Round 93 -- IB-pr-381 (COMPLETE under AMENDMENT 1, worker ~189, proof @7e6244577f; drained @93e31749b4)

- CTO ruling msg 1988. Step (a) found 1 writer of the served directory, `directory_runner.land`; 33 of 33 live versions match a runner
  SSM command. The served inflection as_of 10-08 after a failed refresh is the runner's own landing.
- The runner now emits `source_client_ids` and carries removed entries. The refresh reads the served directory when no manifest is in
  the window. P is 7f31bbfa4e: refresh `6eOFTopG...`, runner bundle `2e3e6648...`.
- AMENDMENT 1 (@022c5a2865) excuses exactly one pre-existing red: the S71 live holdings guard, red at base 2c1f4f425d by the issuer's
  own clean-worktree run. Re-grade: IB93-1-AC1..AC3 PASS.
- Row S1: the served directories already lost the entry, so a per-firm seeding run is part of the release.
- Row S4: the runner lands a build fault that the verdict cannot gate. The CTO ruled it yes, as a cell after this release.

## Round 94 issued (@a49aa6c819, drained @898aecd154)

- **IB-pr-383** (applier `0.7.0_AE_CloudOps~DELL2`) applies the ONE release, runs the seeding run, and reads the after-read: READY 3/3,
  terminated 1/1/0, the entry served. Pair: COO @8323d3fb19, CTO @f0a2f049f7, with conditions. Due Fri 10-09 close.
- **IB-pr-382** (worker ~190): the production custody ports `current_selection`, `interpret_source` and `validate_evidence` for release
  6 (CTO msg 2128; contract @859ae01405), plus the read set for release 6's grant.

## Records

Riders confirmed to ~Y2 by content at release-5 pin 2f3ee8c15b (msgs 2009 and 2161). Row D2-S15 resolved D2-S14.

**Push state:** LOCAL on box/dell2 (MSTR pushes :18/:48).
