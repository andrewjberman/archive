# MP-x-4 -- the Control Plane release is LIVE on 1e32562729, over a base that moved mid-cell -- 0.7.0_AE_CloudOps~MP

**archetype:** DEPLOY
**secondary_archetypes:** VALIDATE

**Date:** 2026-10-09
**Task Order:** `NFRA_MCPORTAL.TO-MP-x-4` (round 5, E2; `<risk>WORLD</risk>`)
**Status:** COMPLETE (AC1 PASS, AC3 PASS, AC2 refused as UNVERIFIABLE-BY-INSTRUMENT with its measurement)

---

## Objective

Ship the narrow gateway release that serves the FWD-17 Control Plane page: MP-x-1's four files onto the
LIVE gateway base, with the mcportal `d60b4e0` dashboard bundle, under a never-widen pair, without the
page's first open being able to time out.

---

## Compiler Tools

Full table in the proof instance's `compiler_tools`. Not re-tabulated here and no tool was re-run to
populate a table. The four worth carrying:

| tool | result | the lesson |
|------|--------|------------|
| `safe-ec2-deploy.sh` | PASS on the 2nd call | The 1st was REFUSED, `DEPLOY_BASE_REF is required`, rc=1, nothing uploaded. The stale-base guard works and it is worth tripping |
| `deploy_ledger.py` | PASS, 1 defect routed | `hold` regenerated the entry and silently ate 115 lines of the required record at rc=0. Caught from the commit's insertion/deletion counts. Row Z-S24, fixed at source by MSTR~Z |
| `bun_cache_precheck.py` | PASS 77/77 | Run against `d60b4e0`'s OWN lockfile via `git show`, not a checkout's |
| `halt-gate-check.sh` | PASS rc=0 | Measured standalone BEFORE the act, so an rc=3 could not surface mid-deploy |

**What worked:** re-reading the instrument after the base moved. OG-tl-1 changed `deploy-to-ec2.sh`
itself, and that re-read caught both of the things that would have gone wrong (below).

**What failed:** my first cold-read driver, and the failure was mine -- I overlaid `admin_fabric.py` but
not its new `app/refs/fabric_boxes.json`, so `_roster()` raised `FileNotFoundError`. Also two sparse-list
omissions, each found by the instrument that needed the path, not by foresight.

**Gap found:** two, both filed. A check that reaches into the nested `mcportal` repo cannot run from a
linked worktree and degrades to a FALSE NEGATIVE because the call is wrapped in `2>/dev/null` (Z-S28).
And the page's cold read is under its bar but its margin shrinks through the working day (Z-S27).

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 0 | GO, then HOLD, then GO again | Issuer held the act so OG-ap-4/OG-tl-1 could go first; one gateway release in flight at a time |
| 1 | Live base re-read from `EC2_MANIFEST.json` | `91811b648a` -> **`c97232408d`**. The recorded base was NOT reused |
| 2 | Old release branch deleted, tree re-cut, MP-x-1 cherry-picked | `21eb975c11` |
| 3 | `mcportal_commit` = `d60b4e0` | `1e32562729`, one line (1 insertion, 1 deletion, measured) |
| 4 | **Census re-run vs the new base** | 4 files, 464 insertions, **0 outside** the gateway scope |
| 5 | bun cache pre-check | 77 of 77, rc=0 |
| 6 | Cold read re-measured on the host, 3 samples | 24.443 / 19.728 / 18.118 s vs the 30 s bar |
| 7 | Rollback re-pointed and content-verified | `opal-gateway-c97232408d.tar.gz` |
| 8 | Ledger released HELD -> OPEN | `48fff5205a` |
| 9 | **THE ACT** | refused once (no `DEPLOY_BASE_REF`), then rc=0 at 16:12:05Z |
| 10 | Independent read-back | `/health` 200, route 401, tools 66->66 |
| 11 | Manifest recorded on the trunk, 4 legs closed, entry CLOSED | `e9a1bf5127` |
| 12 | AC1/AC2/AC3 | PASS / UNVERIFIABLE-BY-INSTRUMENT / PASS |

---

## Verification

**`rc=0` is cited as proof nowhere.** The deploy's own read-back was taken, and then every figure was
re-measured independently (SSM `a356c9bf...`, Status=Success):

```
/health                        -> 200   {"ok":true}
/api/admin/fabric/boxes (none) -> 401   {"error":"no verified identity"}
service                        -> active;  MainPID 862375 -> 864717
deployed app/admin_fabric.py   -> md5 caa21f671e60c21e4b0a77c566c18149  == the release module's md5
app/refs/fabric_boxes.json     -> present   (both ABSENT live on three pre-act reads)
dashboard/index.html           -> present
MCP tool surface               -> 66 -> 66, 0 added, 0 removed, difference EMPTY
.env TRANSCRIPT_MEETING_ALLOWLIST -> non-empty before AND after
```

The md5 row is the one that matters: it compares DEPLOYED BYTES to the BUILD INPUT (22a's CODE layer). A
filename match proves nothing.

**Artifacts, read after the act:**

| key | bytes | ETag | git-ref |
|---|---|---|---|
| `opal-gateway-1e32562729.tar.gz` | 518165 | `b96315a5...` | `1e32562729...` |
| `opal-gateway-latest.tar.gz` | 518165 | `b96315a5...` | `1e32562729...` |
| `opal-gateway-c97232408d.tar.gz` (ROLLBACK) | 514278 | `16c5f801...` | `c97232408d...` |

`latest` moved, as predicted before the act -- which is why the rollback names the VERSIONED key. The
rollback target is intact and distinct afterwards, so recovery is available and unexercised.

---

## Decisions Made

1. **Discarded the whole prepared release when the base moved.** The hold let OG-tl-1 land first; rather
   than reuse `91811b648a`, the branch was deleted and the census, cold read, rollback and tool-surface
   baseline were all re-taken. This was not pedantry -- see 2 and 3.
2. **Re-read the deploy script after it changed, and that caught a hard stop.** OG-tl-1 added a
   precondition reading `data/transcripts/scripts/teams/meeting_allowlist.json` under `$WORKSPACE_ROOT`
   that REFUSES (exit 1, pre-upload) on an unreadable file. The sparse list had no `data/`. Added it and
   evaluated the script's own expression in the worktree (4 ids, shape matches) before acting.
3. **A stale-base deploy would have silently reverted OG-tl-1.** The old script hardcoded
   `TRANSCRIPT_MEETING_ALLOWLIST=` EMPTY; the `.env` is RENDERED, never merged. Building on the old base
   would have blanked an allowlist that landed 15 minutes earlier -- while this cell's blast radius says
   "no `.env` key". Measured non-empty before and after.
4. **Did NOT narrow the window despite the tightening margin.** Headroom fell 1.79x -> 1.23x during the
   cell. The order's remedy fires only above 30 s; every sample was under. Narrowing it un-triggered
   would have changed product behaviour the order does not authorise. Filed as Z-S27 instead, and the act
   was run promptly rather than deliberated, because delay makes the number worse.
5. **Refused AC2 rather than repairing it or working around it.** Three clauses pass; the fourth cannot
   be answered from a linked worktree. The check was not edited (read-never-write) and no symlink was
   created to fool it. Status `UNVERIFIABLE-BY-INSTRUMENT`, substance verified separately.
6. **Corrected my own wrong citation.** The `release_note` cited `Z-S26`; a peer took that id mid-cell.
   Re-read the next free k at write time and fixed the note to `Z-S27`.
7. **Wrote the manifest record by hand on the trunk**, because the deploy script's auto-record on the
   release branch sets `previous_deployed_commit=2c0f84966d` -- wrong, the value that tree held from its
   vintage. That branch is never merged; the trunk entry is the authority and names the error.

---

## Files Modified

see commit messages: `1e32562729` (release tree), `48fff5205a` (hold released), `e9a1bf5127` (legs
closed + manifest), `6efd9da3b6` (post-act record + citation fix), and in the SHARED tree `b23823ad78`
(Z-S24), `d9a121832e` (Z-S27 + Z-S28).

---

## Blockers

None outstanding. Two cleared during the cell: the issuer's HOLD for OG-ap-4 (released, msg 32840), and
`deploy_ledger.py`'s prose loss (fixed at source by `0.0.0_AB_MSTR~Z` @`a9d1b38f12`, disarmed by the
issuer's Z-S25/Z-S26).

---

## Current State

**The Control Plane page is LIVE.** `opal-gateway` runs release `1e32562729` over
`c97232408d`, serving the new owner-gated route `GET /api/admin/fabric/boxes` (401 without identity) and
the mcportal `d60b4e0` dashboard bundle with its 60-second refresh. `/health` 200, service active,
MainPID 864717. The MCP tool surface is unmoved at 66. OG-tl-1's transcript allowlist is intact.

Ledger `20261009T1414Z_nfra-mcportal-r5-control-plane-release_deploy_completion.md` is CLOSED, 4 legs
proven, sentinel removed. Rollback available and unexercised:
`opal-gateway-c97232408d.tar.gz` (the VERSIONED key, never `latest`).

Branch `wk-mcportal-r5-x4` at the proof commit in worktree `C:/tmp/mp-x4`, **NOT drained** -- the issuer
drains it. The release branch `rel-nfra-mcportal-r5-control-plane` in `C:/tmp/mp-x4-rel` is local and
never merged, as every prior gateway release branch; it exists only as the build provenance. All commits
LOCAL; `box/*` is pushed by an MSTR or `box-sync`.

**For whoever runs AC2 next:** run it from the MAIN tree after the drain. From a linked worktree its
mcportal clause is a false negative.

---

## Next Steps

1. `[2.0.0_SA_COO~MP]` Drain `wk-mcportal-r5-x4` and re-run the three checks on the merged index; AC2 is
   expected to PASS there (its logic run verbatim from the main tree already does).
2. `[2.0.0_SA_COO~MP]` Disposition `Z-S27` (the cold-read margin -- an enrichment-list item, with four
   options and their costs in the row; NOT a request for an alarm, which is under moratorium) and
   `Z-S28` (give `x4.AC2.sh` the `_main/mcportal` fallback `deploy-to-ec2.sh:40-44` already has, and drop
   the `2>/dev/null` that turns an absent repo into a `no`).
3. `[0.7.0_AE_CloudOps~MP]` Holds `NFRA_MCPORTAL.TO-MP-r-2` (CP2), `staged` with AMENDMENT 4, which
   adopts the pre-act-record pattern up front. Its GO comes by message.
