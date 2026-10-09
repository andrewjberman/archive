# NFRA_TRNSPT round 19 -- close record: the leak closed, the wipe built, three new acts (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `0f17922291` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R19.md`, CTO ADDENDUM 8/8.1). Five worker orders terminal and drained;
`round-close-check --round 19` MAY-CLOSE (5 orders); drain on the merged tree `data/transcripts/scripts/tests/` 406 passed (test_eod_voice.py
ignored, LDO-001's import error).

| cell | merged | check | what exists |
|---|---|---|---|
| TR-s-19 (W1-S8, ARMED) | 6509d14fa3 | R19-S8-OK 3 | `teams/holdout.py` `visible_rows`; both readers use it; a held-out row is never printed. **W1-S8 DISARMED.** A test that pinned the leak (`test_research_store.py`, turns=5) fixed at the drain @ca48d173a1 |
| TR-w-19 (W1-S7) | 4eb7ed184c | R19-W7-OK 3 | `teams/rewipe_silver.py` (dry-run default, every key listed) + wipe-on-landing in `parse_silver.py` with the planted-token test. The SERVED re-wipe of existing Teams silver still needs its pair and the applier |
| TR-e-19 (FWD-4) | bf9977e6b2 | R19-E4-OK 3 | a per-pull listing snapshot at `address(..., "state", "listing_snapshots", ...)`; `completeness.build` reaches `expired` from it. Its test drift (W3-S4, ARMED) fixed at the drain @1994c45467 |
| TR-i-19 (FWD-6) | 47322a7b09 | R19-I6-OK 3 | `updates/intake.py`: byte-exact landing + sidecar sha256 + a slide-text fingerprint that recognises a re-saved deck |
| TR-q-19 (FWD-9) | 3408102135 | R19-Q9-OK 4 | `query/securities_across.py`: one read-only question, per-security counts across meetings, mail updates and commentary, no text |
| TR-r-19 (FWD-2, issuer read) | this commit | -- | `R19_RESEARCH_403_READ.json`: Graph 3003 is MEETING MEMBERSHIP (the gateway reads as Andrew, not invited), not a scope; queued for Andrew (open call, OWN-BOX scope, an organizer or admin act) |

**Carried / open:** TO-APPLY-p18 (Teams pull) STOPPED at step 1 -- the bearer secret is absent and the Teams gateway transport is a STUB
(row D2-S10 @353bf58b5b); CTO ADDENDUM 9 @f586e1e6e7 rules a transport cell, cut on NFRA_OPLGTW's bearer name + route contract (asked via MSTR).
TO-APPLY-a18 (FWD-8 second reader) at the laptop via MSTR. The W1-S7 served re-wipe needs its pair. FWD-5's reader role waits on both wipes.
