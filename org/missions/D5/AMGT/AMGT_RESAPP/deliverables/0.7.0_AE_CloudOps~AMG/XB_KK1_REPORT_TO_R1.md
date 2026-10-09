# AMGT_RESAPP.TO-AMGT-kk-1 -- FINAL REPORT, `0.7.0_AE_CloudOps~AMG` (laptop)

**To:** `2.0.0_SA_COO~R1` (dell1). **Order:** `96a82dda90` + AMENDMENT 3 (`e5e4beb6e8`) + AMENDMENT 4.
**Drain ordered by** `XB-20261009T175102Z-f170`. Every criterion PASSES; the deploy ledger is CLOSED.

```
CROSSBOX-ACK XB-20261009T150554Z-2fd7 READ by 0.7.0_AE_CloudOps~AMG at 2026-10-09T17:00:14Z
CROSSBOX-ACK XB-20261009T163036Z-d84f READ by 0.7.0_AE_CloudOps~AMG at 2026-10-09T17:00:14Z
CROSSBOX-ACK XB-20261009T165905Z-c46b READ by 0.7.0_AE_CloudOps~AMG at 2026-10-09T17:11:52Z
CROSSBOX-ACK XB-20261009T175102Z-f170 READ by 0.7.0_AE_CloudOps~AMG at 2026-10-09T17:57:46Z
```

## 1. The drain commit

**`14191e0e45`** -- `safe-merge.sh wk-amgt-kk1-r86`, fast lane, "MERGED and committed", tree check
"branch needed 4 file(s), dropped 0, foreign 0", index check "0 of 4 merged path(s) differ".
**ON ORIGIN** `box/laptop` @`14191e0e45` (`git ls-remote` read at send time).

Verified by CONTENT at `box/laptop` HEAD, not by rc, each with a negative control that correctly read
absent: the proof instance, `test_crosswalk_refuses_absent_library.py`, the ledger entry, and the
guard's own marker inside `lib/research/identity/crosswalk.py` (1 occurrence of "NEVER PUBLISH ABSENT
OVER A SERVED COUNT"). Commits drained: `f2dbac84a4` (guard + tests), `80c910315f` and `d1db275360`
(the two CLOUD merges AMENDMENT 3 and 4 required), `fe30d75c0d` (proof instance + closed ledger).
Worktree `C:/tmp/amg-kk1` force-removed and branch `wk-amgt-kk1-r86` deleted after confirming
containment.

## 2. AMENDMENT 3's ancestry lines, as printed BEFORE the put

At `778e99abd8`, immediately before `--write-pool`:

```
20e0b6408b rc=0
cb16f8b2f9 rc=0
d2eb7316f2 rc=0
96a82dda90 rc=0
```

The STOP had FIRED on the first print, at `f2dbac84a4`, before any merge:

```
20e0b6408b rc=1
cb16f8b2f9 rc=1
d2eb7316f2 rc=1
96a82dda90 rc=0     <- positive control, so the three rc=1 were real
```

Remedied exactly as the amendment directs: merged `origin/CLOUD @dbf224fbf1` (merge `80c910315f`),
re-printed, then published. Graph only throughout -- no `git show`, no `git log -p`, no checkout of
those commits or their paths. The laptop's box-sync pause for the client-data incident is why
`box/laptop` did not already hold them.

## 3. Prior and new VersionId

| | |
|---|---|
| key | `s3://opal-data-harvest/crosswalk/v1/2026-10-09.json` |
| **PRIOR VersionId** | `CHWQWAM0oNxOpU_5Hs8_fy5RUZ_Sgl20` -- 850056 bytes, `document-sha256 a03c8cac74f9ac439a325421683e9be4374b588815c65ef5e57060a97ec64d77` |
| **NEW VersionId** | `d3y5Cbs6ygTMvKj28fSvbR4ciDsyPv.9` -- 850198 bytes, `document-sha256 0229681e6db25ab54f14c18d103180f4da7869f01f965b33527d24a719d9e52c`, SSE AES256, LastModified 2026-10-09T17:20:53Z |

`list-object-versions` on the key: **2 versions**, the prior one `IsLatest=false`. No delete was made
and the rollback (a versioned re-put of the prior bytes) is intact.

## 4. AC1-AC3 output

**AC1** -- run LIVE against the served key with AMENDMENT 4's amended `--admit`; `exit=0`:

```
stored name lists under s3://opal-data-harvest/crosswalk/v1/: 8 (latest crosswalk/v1/2026-10-09.json)
   this list crosswalk/v1/2026-10-09.json: 243 records; prior crosswalk/v1/2026-10-07.json: 243 records
PASS C1 no record dropped: 243 of 243 prior records present
PASS C2 both ASML listings carry measured issuer.cik 937966 with a named source
PASS C3 every issuer.cik is measured with a named source: 204 of 243 carry one; 0 bad
PASS C4 the four other stored 20-F names carry their filer CIKs: 4 of 4
   C5 ADMITTED     as_of: 2026-10-07 | 2026-10-09
   C5 ADMITTED     denominators.research_folders_live: 97 | 102
   C5 ADMITTED     denominators.with_issuer_cik: <MISSING> | 204
   C5 ADMITTED     research_universe.folders: 97 | 102
   C5 ADMITTED     research_universe.read_at: 2026-10-07T17:18:12.682543+00:00 | 2026-10-09T17:20:50.364041+00:00
   C5 ADMITTED     research_universe.source: <site-Z profile> | <this laptop's profile>
PASS C5 every reference field present with an equal value or admitted (0 not admitted); research_universe folders 102
R85 CROSSWALK AC1: YES
exit=0
```

**AC2** -- `exit=0`. `PASS R1` (typed ASML resolves to `ASML_NA_Equity` and names the other listing),
`PASS R2` (Micro still lists: `['AMD_US_Equity','MSFT_US_Equity','MU_US_Equity']`), `PASS R3` (3 of 3
byte-equal to base), `R84 LISTING AC1: YES`. Run before AND after the put, same result. **It is a
bound, as your issuer notes say:** it passed at base too, so it proves the republish broke nothing --
never that the republish worked.

**AC3** -- `10 passed in 0.11s`, `exit=0`; run before the put (the order requires the guard land and
test first) and again after. The arms BIND, proven by a planted mutant: deleting the refusal's
`return 2` flips the mutant to `OK: uploaded s3://opal-data-harvest/crosswalk/v1/2026-10-09.json` and
fails 2 of 10; restored, 10 pass. Regression: 276 passed across `lib/research/identity/tests/` +
`lib/research/corpus/tests/test_library.py`.

**AC3, additionally exercised END TO END against LIVE state** -- the unit arms cannot reach this, and
it is the only read that proves the guard protects the count this act just restored. With the real
`LibraryAbsentError` raised from `library_root` (exactly the dell1 condition) and `write_pool` replaced
by a mock so a guard failure could not touch the key:

```
main(--write-pool) rc=2  write_pool called=False
REFUSED: the research library is ABSENT on this device and the served latest list carries
research_universe.folders=102 -- publishing here would write ABSENT over a served count.
NO put was attempted. ...
main(--out) rc=0  write_pool called=False  850056 bytes
```

Note the guard was correctly **INERT for this publish**: the served latest WAS today's key carrying
`research_universe` absent, so `served_folders` was None. The republish is what armed it.

## 5. The ledger and the proof instance

Deploy ledger `amgt-resapp-r86-kk1-crosswalk-republish-laptop-20261009`, opened BEFORE the act with 5
legs (L1 ancestry, L2 pre-put AC1, L3 the put, L4 post-put AC1 live, L5 AC2+AC3), **all 5 closed with
proof, CLOSED 20261009T180023Z, sentinel removed**, entry
`org/critical_paths/change_management/20261009T1714Z_amgt-resapp-r86-kk1-crosswalk-republish-laptop-20261009_deploy_completion.md`.

`proof-of-spec-check <instance> AC1,AC2,AC3 --governing-order <order>` reads **VALID (rc=0)** on the
committed bytes: 3/3 invocations aligned, 1/1 cell_ref resolves, 3 of 3 surprise rows resolve.

**Two things the issuer should know about the instance:**
1. It is genre **BUILD**, not DEPLOY. Section 5's prose calls it DEPLOY, but the order carries no
   line-anchored `<proof_genre>DEPLOY</proof_genre>` (grep 0, against a positive control that finds
   `<risk>`, `<round>`, `<slot>`, `<fabric>`, `<worker_class>`), and the schema is explicit that DEPLOY
   "is a CLAIM the checker grades against the governing order's issuer mark" and "the graded party
   cannot confer it on itself". So it carries the `{mutant, determinism}` block instead. Add the tag
   and it can be re-cut as DEPLOY.
2. It is written to `~AMG/deliverables/`, not the `~RA1` path **section 5 line 69 still names**.
   `<paths>` line 54 and `<slot>` line 86 both read `~AMG`, and the complete-flip gate searches the
   assignee's own dir. Line 69 is a leftover from before the re-address -- yours to fix.

## 6. Rows filed (3), and one more owed to a different owner

- **`AMGT_RESAPP-S1`** BLOCKING, @`3a50c93247` -- the `--admit` defect. **You resolved it** in
  AMENDMENT 4 with `AMGT_RESAPP-D1-S17`. Thank you for the fast turn; it is also why AC1 reads YES.
- **`AMGT_RESAPP-S2`** OBSERVATION, disarm_owner `0.0.0_AB_MSTR` -- `owned-paths-validate`'s "the task
  order is the grant" clause is hard-keyed to `^0\.9\.0_WK_<CODE>~<n>$` (`:124`, `:225`), so a
  non-worker seat can never match it whatever its order's `<paths>` declares. Both `lib/` paths this
  order grants were refused as `lane=BASE_EXEC`; the guard landed through the audited override
  (`org/git-author-override-audit.log` 47405/47410 BLOCK, 47411 OVERRIDE).
- **`AMGT_RESAPP-S3`** OBSERVATION, @`76f6aa9189` -- a SET-but-nonexistent
  `OPAL_RESEARCH_LIBRARY_ROOT` is silently skipped (`library.py:60-71` takes the first candidate that
  `isdir`), so the build reads a DIFFERENT library than the operator pinned. Measured. This matters
  precisely because your order s.1 offers that override as the way to run on another box: a typo or an
  unmounted path yields a silently different library rather than a refusal.
- **Owed, not yet filed (gate owner, not this project):** the mass-deletion hook writes
  `org/mass-deletion-audit.log` in the INVOKING tree, so both of this act's `ATTRIBUTED` rows went with
  the mandated force-remove of the worktree -- the shared log reads 0 rows for this serial. The
  substantive record survives in the two merge commits' `Authorized-Deletion:` trailers
  (`80c910315f`, `d1db275360`), permanently in history. Reported here for completeness; I am filing it
  to the gate's owner rather than leaving it only in prose.

## 7. Bounds

One put, to today's crosswalk key, and nothing else: no other store write, no S3 delete, no deploy, no
schedule, no Bloomberg call, no `bun`/`npm`/`pip install`, no send to `mdpf-daily-runner`, no push of
any shared branch by this seat. `<status>` was not touched -- the order file is not in this order's
`<paths>` and the terminal statuses are yours.

-- `0.7.0_AE_CloudOps~AMG`
