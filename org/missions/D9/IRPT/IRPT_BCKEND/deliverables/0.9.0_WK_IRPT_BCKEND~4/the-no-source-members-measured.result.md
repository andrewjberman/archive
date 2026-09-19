# IB-rtf-1 RESULT -- the no-source members, measured then branched

**Cell:** `IB-rtf-1` (decomposition v0.6, s.R6). **Order:**
`IRPT_BCKEND.TO-IB-rtf-1.the-no-source-members-measured-then-branched.md`.
**Worker:** `0.9.0_WK_IRPT_BCKEND~4`. Battery: `battery_ib_rtf_1.py`; output:
`IB-rtf-1_R58-AC1_battery_output.txt` (final, clean run; rc=0, token printed).

---

## THE POPULATION -- 32 of 157, by subtraction from a fresh census

`battery_ib_rtf_1.py` re-ran IB-rte-4's served-zip census over all 9 investor-reporting functions
at their **CURRENT served bytes** -- read from the **LIVE DEPLOYED Lambda's own code**
(`aws lambda get-function --query Code.Location`, a presigned URL to the exact bytes `CodeSha256`
was computed over), **never** the S3 build-artifact bucket (see INSTRUMENT TRAP below). 157
declared+served members across 9 functions; **32 of 157** are NOT `TRACKED-AT-PATH-EQUAL` and NOT
declared through a VERIFIED `staged_from` entry. The population splits four ways:

| class | count | resolution |
|---|---|---|
| CANONICAL-ABSENT, pre-existing, no true source ever (rows W4-S34/S35) | 3 | PACKETED-AND-ROWED |
| Missing declaration entirely, canonical found by content-addressed search | 9 | DECLARED-AND-VERIFIED (row W4-S39, new) |
| Existing `staged_from` pin STALE (content no longer matches served bytes) | 17 | DECLARED-AND-VERIFIED, repointed (row W4-S40, new) |
| Caused by a SIBLING worker's mid-run redeploy (row W4-S41, new): 1 CANONICAL-ABSENT + 2 TRACKED-ELSEWHERE-MISMATCH | 3 | PACKETED-AND-ROWED |
| **TOTAL population** | **32** | k=26 declared, j=6 packeted, k+j=32 |

The **first 3 CANONICAL-ABSENT** members are exactly the same 2 distinct members (3 member-function
pairs) rows `IRPT_BCKEND-W4-S34`/`W4-S35` already named: `firm_registry.json` on
`irpt-intake-poller` and `irpt-ycharts-generate` (byte-identical served content, sha256
`cc3f2c63...`, re-verified this run), and `settings.json` on `irpt-ycharts-generate` (sha256
`a05bcea4...`). Both blob ids remain **ABSENT** from `git rev-list --objects --all` this run,
identical oids to the ones those rows recorded.

**29 members were NOT on the face's own "known at the cut" list.** 26 of them because the
population genuinely moved, exactly as the face warned it might: `IB-rte-6` (round 5) deployed 7
functions with a NEW shared member (`_ids/data/custodian_key_seam.json`) and an UPDATED
`_ids/ids.py`/`_authz/served.py`/`_authz/loaders.py`, through a manual packaging script rather than
`build-and-upload.sh`'s own declarative mechanism (rows `IRPT_BCKEND-W4-S39`, 9 missing
declarations, and `IRPT_BCKEND-W4-S40`, 17 stale pins -- both disarmed same-turn by this order's
own remedy commit). The remaining **3 -- `irpt-directory-search`'s `enforce.py`/`served.py`/
`data/custodian_key_seam.json`** -- are a DIFFERENT, LIVE event: `irpt-directory-search` was
redeployed at `2026-09-19T05:29:38Z`, 29 seconds before this order's own FINAL graded battery run
started, by a SIBLING worker's (`0.9.0_WK_IRPT_BCKEND~1`, cell `IB-rtf-2`) in-flight, not-yet-merged
commit editing the SAME shared `_authz/enforce.py`/`served.py` this order also declares. Filed as
row `IRPT_BCKEND-W4-S41` (ARMED, `disarm_owner: 2.0.0_SA_COO~B`) -- see the NEVER-WIDEN packet's
CLASS B section for the full account, including that `enforce.py`/`served.py` ARE reachable in the
shared object database (just not yet on this branch's `HEAD`) while `data/custodian_key_seam.json`
is not, even under that check.

## (a) THE CANONICAL SOURCE -- 28 of 32 named (26 verified/repointed + 2 named-but-mismatched), 4 of 32 ABSENT

- `data/custodian_key_seam.json` (6 functions) and `ids.py` (3 functions missing it entirely) ->
  `infra/aws/lambda/investor-reporting/_ids/{data/custodian_key_seam.json,ids.py}` @ HEAD.
- `ids.py`/`loaders.py`/`served.py` (17 stale-pin members across the 6 remaining affected
  functions, `irpt-directory-search` now excluded for `served.py` -- see below) -> the SAME shared
  frontier paths (`_ids/ids.py`, `_authz/loaders.py`, `_authz/served.py`) @ HEAD -- the true source
  was never in question, only the DECLARED pin was stale.
- `firm_registry.json` (x2) and `settings.json` -> **ABSENT**, content-addressed search
  (`git hash-object --no-filters` + `git cat-file -e` + a full `git rev-list --objects --all`
  index of ~376,000 objects) found nothing, exactly as rows W4-S34/S35 recorded.
- `irpt-directory-search`'s `enforce.py`/`served.py` -> canonical IS NAMED (the pre-existing
  `_authz/enforce.py`/`served.py` pin) but DELTA != 0 as of this run (59/567 and 42/606 lines
  differ) -- NOT an absence; a sibling worker's in-flight, not-yet-merged commit changed the served
  content mid-run (row W4-S41; NEVER-WIDEN packet CLASS B). `irpt-directory-search`'s
  `data/custodian_key_seam.json` IS genuinely **ABSENT** (content-addressed search found nothing,
  including under the out-of-band follow-up check) -- a different, unexplained finding.

## (b) THE DIFF -- printed before any label

Every one of the 26 resolvable members diffed **byte-identical** (0 of N bytes differ, both
directions) against its canonical source -- DELTA=0 for all 26. Of the 6 packeted members: 4 are
genuinely CANONICAL-ABSENT and diffed as `present-only-in-served=K of K keys; present-only-in-
canonical=0 of 0` (no canonical to diff against -- the full content IS the finding, nothing
invented); 2 (`irpt-directory-search`'s `enforce.py`/`served.py`) have a NAMED canonical with a
real, bounded line-by-line diff (59/567 and 42/606 lines) -- DELTA != 0, not an absence, per the
face's own branch (b): "DELTA != 0 (or CANONICAL-ABSENT)" covers both under the same remedy.

## (c) THE BRANCH -- k=26 declared, j=6 packeted

- **DELTA=0 (26 of 32):** `staged_from` declared/repointed in `infra/aws/lambda/ci/lambda-source-map.json`,
  every entry pinned to `c28c728a309ab0d83b2831c2972179791a2985fb` (this branch's own cut commit --
  content-identical to the exact last-touch commits for each shared file, verified live). No third
  copy committed; no served bytes committed as source.
- **DELTA!=0/ABSENT (6 of 32):** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-1.md` -- blast radius (full
  served content, no canonical to compare), rollback (`blob <served-sha256>`, re-derivable each run
  from `Code.Location`), writer census (see `R58-AC2_judgment.md` and the packet itself). NOT
  deployed, NOT committed as source. Rows W4-S34/W4-S35 stay ARMED, `disarm_owner:
  2.0.0_SA_COO~B to route`; row W4-S41 (new) is ARMED, same disarm owner, different cause.

## (d) THE CONTROL -- mutant fails exactly as expected; real manifest succeeds

Real build (whole pipeline, `BAU_PARITY_SKIP` never set): **6 of 9 functions build clean**
(`irpt-performance-adapter`, `irpt-narrative`, `irpt-directory-refresh`, `irpt-export-render`,
`irpt-holdings`, `irpt-status`); **3 of 9 fail**
(`irpt-directory-search`, `irpt-intake-poller`, `irpt-ycharts-generate`) -- the first ONLY because
of the sibling-collision (row W4-S41), the other two ONLY on the 3 pre-existing CANONICAL-ABSENT
members, matching `IB-rte-4`'s own irreducible core exactly.

Mutant (scratch-only manifest, `BAU_SOURCE_MAP_OVERRIDE`, real file never touched): the 26 newly
declared/repointed entries removed per affected function (up to 4 members per function: `served.py`,
`loaders.py`, `ids.py`, `data/custodian_key_seam.json`; `irpt-directory-search` mutated on its 2
remaining declared members, `ids.py`/`loaders.py`, since `served.py` is no longer this order's
declaration on that function) -- **7 of 7 mutant builds FAIL** with the exact `File not found`
lines for the removed members. The real (unmutated) manifest: **7 of 7** functions no longer show
ANY of those `File not found` lines (measured per-member, not by overall `rc`, since
`irpt-directory-search`/`irpt-ycharts-generate` still legitimately fail on OTHER, unrelated
CANONICAL-ABSENT members -- conflating the two would be exactly the shared-dependency blindness
CLAUDE.md Rule 22 warns against). `CONTROL=True`.

## INSTRUMENT TRAP, self-caught mid-run (same class as row W4-S37)

The battery's first two runs used the S3 **build-artifact bucket** (`download_served_zip`, the same
call `battery_ib_rte_4.py` used for its own census) as the "served" reference. That bucket is
overwritten by every real build THIS SAME BATTERY performs (arm d) -- so a re-run mid-session reads
its **own prior output**, not the true served baseline, and produced an internally-consistent but
WRONG population (16, then 21-of-16 already "fixed" by an earlier run). Caught because the SECOND
run's `ids.py`/`served.py`/`loaders.py` verdicts silently flipped from `MISMATCH` to `VERIFIED`
between runs with no manifest edit in between on those specific entries -- a result that cannot
change without a cause. Fixed by switching the census to `Code.Location` (the LIVE DEPLOYED
Lambda's own code, untouched by any of this battery's build calls), exactly the discriminator
`IB-rte-4`'s own result.md named for the DEPLOY-NEED question and this order re-applies to the
CENSUS question. Both contaminated manifest states were reverted (`git checkout --`, this worker's
own uncommitted working tree, never pushed or shared) before the clean run.

## SUMMARY

32 of 157 declared+served members needed this order's arms. 26 resolved cleanly to a named,
byte-verified canonical source and are now declared (`k`); 6 are packeted, not fabricated, not
deployed (`j`) -- 4 with no recoverable source anywhere in this repository's history (3 pre-existing,
1 new: `irpt-directory-search`'s `data/custodian_key_seam.json`), 2 with a named canonical whose
content a sibling worker's in-flight commit changed mid-run (`irpt-directory-search`'s
`enforce.py`/`served.py`, row W4-S41). `k+j=32=N`: every population member reached one of its two
terminal states. The battery's success token
(`IBR58-NO-SOURCE-MEMBERS-MEASURED-AND-BRANCHED`) prints; `rc=0`.
