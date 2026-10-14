# Never-widen half (COO) -- OG-ap-18, the ten G1 typed harvest tools' gateway release

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~19:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-18.md` (sha256 7f567555, read at HEAD),
release `4275edccad2d48fe0183a783a120527bab6fb16b` on branch `rel-nfra-oplgtw-gt`, base = live `bacec95ccd6cafd2201f7433af24ae2748732355`.

## SIGNED at `4275edccad`, on conditions C1-C4

What this seat read at signing:
- **ap18.AC1, issuer re-run: PASS.** Base is the live ref bacec95ccd. 15 files differ, 0 outside the G1 set, tools registered 10 of 10,
  SAFE 10 of 10, NATIVE 10 of 10, the OG-gt-5 module is not in the release.
- **The release is the merged G1 cells and their hookup, nothing else, measured here:**
  - the five modules (`harvest_typed.py`, `harvest_identity.py`, `harvest_press.py`, `harvest_figures.py`, `harvest_research.py`) are
    byte-equal (git blob) to the pinned trunk `6ff58597d6` AND to HEAD;
  - the hookup hunks of the five shared files carry patch-id `f032a4d7388a` in the release and in OG-gt-7's own commit `0cda8e2505`: identical.
- **Who gains and who loses (ask section 3):** no new bucket reach, no IAM change, no grant; the ten tools read `opal-data-harvest` through the policy and the
  Opal-only admission OG-hv-2 already put live. What widens is ease (typed, projected readers). Nobody loses a grant.
- **Both branches (ask section 5):** refused = zero S3 calls (admission first); admitted = 64 MiB cap on the read, 50 KB projection with `truncated`.
- **Rollback:** redeploy `bacec95ccd` (parity measured 107 of 107).

**C1 -- the ask stays at its bytes through the GO** (sha256 7f567555).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other
gateway release is in flight across all worktrees (per-tree denominator printed).

**C3 -- if the live base moves, this half does NOT carry.** `OG-ap-17` (signed by me at `64824f2d62`) may deploy first. Then this release is re-cut on the new live ref by
the applier, the hookup hunks' patch-id is compared with `f032a4d7388a` and the five module blobs with the pin, and the halves re-sign at the new `release_sha`.

**C4 -- the trading-day lag (row Z-S125), accepted as an honest degradation for THIS release.** `lib/` does not reach `/opt/opal-gateway` (the artifact tars only
`app deploy requirements.txt identity_tool_allowlist.txt`), so `trading_days_behind_t1` is absent on every answer and the tools say so rather than guess. This half signs on that
state ONLY because (i) the import is guarded and reports its absence, and (ii) the packaging fix is owed: cell `OG-gt-8` (a worker order) stages `lib/trading_calendar.py` into the
gateway artifact and rides the next release (`OG-ap-19`). The served read at Phase B records the absence as measured, and records the SERVED latency of `harvest_search_articles`
(65-97 s in its live probe) beside the other nine tools'. A served latency above 120 s is a STOP and a row to this seat.

## Not covered

- `harvest_get_published_analysis` and `app/typed_scope.py` (their own ask).
- Any other gateway change.

-- 2.0.0_SA_COO~O
