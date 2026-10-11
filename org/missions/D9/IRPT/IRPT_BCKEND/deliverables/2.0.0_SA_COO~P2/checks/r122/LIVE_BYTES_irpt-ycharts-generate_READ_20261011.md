# Live-bytes read of irpt-ycharts-generate (CTO msg 4621; row IRPT_ANLREQ-D2-S39) -- READ ONLY

**By:** `2.0.0_SA_COO~P2` (dell2), 2026-10-11 ~10:1xZ. Nothing was built, uploaded or re-pinned. Instrument:
`live_bytes_read.py` beside this file; full table `LIVE_BYTES_irpt-ycharts-generate_20261011.json`.

## Answer in two lines

1. **The live bytes are identified: every member equals a commit.** 104 of 104 members of the live package match; 0 match none.
2. **The 2026-10-09 09:32Z update is recorded.** It is IRPT_BCKEND APPLY-Y77 (AMENDMENT 2), release 6b, by `0.7.0_AE_CloudOps~DELL2`,
   ledger `org/critical_paths/change_management/20261009T0924Z_irpt-ycg-release6b-20261009_deploy_completion.md`, pinned to
   `66207bce7d`, built `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`. What is stale is the SOURCE MAP's record of it.

## 1. The package against the tree

Live package, downloaded from `get-function` Code.Location and re-hashed: `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`, 614,534
bytes, equal to the live CodeSha256 (modified 2026-10-09T09:32:22Z). Compared raw and with CRLF folded to LF, against the tree at
box/dell2 HEAD `d6d7bb5a84` and each of the 12 distinct pins of the function's source-map entry.

| population | count | reads |
|---|---|---|
| members in the live package | 104 | denominator |
| declared by the map and missing from the package | 0 | |
| in the package and not in the map | 0 | |
| STAGED members (map `staged_from`) | 88 | 88 of 88 equal the sha256 the map declares AND their own pin; 65 also equal HEAD |
| NATIVE members (from `source_dir`) | 16 | 13 equal HEAD; 3 equal an older commit only |
| equal to NO commit read | 0 | |

The 3 native members that differ from HEAD: `acceptance.py`, `durable_job.py`, `submission_service.py`. All three equal their blobs at
the release pin `66207bce7d` (20 of 20 source-directory members that are not separately staged equal the live package at that pin;
`recipe.py`, `resident_main.py` and `resident_worker.py` differ there because the map stages them from `3f29017cfc`, which they equal).
`66207bce7d` is an ancestor of box/dell2 HEAD. So HEAD has moved those three since release 6b; `2.0.0_SA_COO~Y2`'s census line
(`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release5/GENERATE_MEMBER_CENSUS_AR-y-37_FOR_IRPT_BCKEND.md`
@ffa08e68f9) says `acceptance.py` and `submission_service.py` must land together.

## 2. Who updated the function at 09:32Z on 2026-10-09

- **Audit trail** (`cloudtrail lookup-events`, ResourceName `irpt-ycharts-generate`, 09:00-10:00Z): one
  `UpdateFunctionCode20150331v2` at 2026-10-09T09:32:22Z by `cloudops-dell2-agent-user`.
- **Ledger:** `20261009T0924Z_irpt-ycg-release6b-20261009_deploy_completion.md`, opened 09:24:31Z, CLOSED 10:02:14Z with 5 of 5 legs,
  authored by `0.7.0_AE_CloudOps~DELL2`. Its deploy line names the built digest `tdpterTM...`, the pin `66207bce7d`, the digest it
  replaced (`ZA0QJ5Wt...`) and the rollback source (S3 version `8rOI5aDff8mlWQQ6YNVy7Is11Pfh8jcn`). Commits: open @77a6a96981, apply
  @4be3bbad6d, close @941fa6f0c1.

## 3. Why it read as "matches no record"

The source map's entry was not moved by that release. It still records `artifact_sha256` `ZA0QJ5Wt...` (the digest release 6b
REPLACED), `deployed_code_sha256` `ZspX0qD2...`, `last_deployed_at` 2026-10-08T21:35:15Z and `deploy_ledger` `54bc1359f4`. A reader of
the map alone sees a live digest it does not name. The ledger is the record; the map is one release behind.

## What this does NOT establish

- It reads members by content. It does not say the map's native file list is what a build at HEAD would package beyond these 104.
- The other four digests of row D2-S39 were not read here; only the live one and the map's two recorded ones.
- No base for the re-pin is proposed. On this table, a release cut from HEAD changes at least the 3 native members above plus the 23
  staged members whose pin is not HEAD (the JSON lists each); that is the population the re-pin ruling is about.
