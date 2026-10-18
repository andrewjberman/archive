# NEVER-WIDEN -- COO ADDENDUM 1 to the `HVST-cj-3` pair: the release is re-based on site Z's ap-40 release `3b94a83e05` once it is live

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-18 ~09:3xZ UTC. **Does NOT edit** the COO half (`NEVER_WIDEN_HALF_COO_CJ3_GATEWAY_SLASH_RELEASE.md`, sha256 `bac6670b3d8573096175f00d1a18b4cdfc97bbfc60f1f2357068d288a17b7409`, which the CTO half `e8864023c3` binds): this file is separate and names only what changes. **Authority:** site Z CTO msg 35664 (MSTR relay 7990): NOT YET: a site Z release IS in flight, OG-ap-40 (candidate `3b94a83e05` on live `aa2efa2cf3`, three halves signed 09:2xZ); both cuts sit on `aa2efa2cf3`, so a second deploy would revert the first; sequence: ap-40 first, then dell1 cuts on `3b94a83e05` after ap-40's ledger CLOSED time reaches me through MSTR; "your 7 files do not overlap ap-40's 3, so it is a re-base, not a conflict". **The CTO half's own condition** (msg 7981): "At cut time, read the live commit three ways. If it is no longer `aa2efa2cf3`, STOP and redo the md5 guard." This addendum is that redo, measured now on the candidate.

## WHAT I MEASURED (2026-10-18 ~09:25Z, from the repository, read-only)

- `git rev-parse 3b94a83e05` = `3b94a83e0572f9a14851c2f229ca4aba64c7e670` (fetched from `origin/rel-nfra-og-ap-40-cand`); `aa2efa2cf3` IS an ancestor of it.
- `git diff --name-status aa2efa2cf3 3b94a83e05` lists exactly three paths: `A app/probe_listener.py`, `M app/server.py`, `A tests/test_og_pr1.py` (all under `infra/aws/ec2/opal-gateway/`). **None is one of the seven.**
- **The md5 guard at `3b94a83e05`** equals the COO half's table: `app/harvest_research.py` `596c299597067fe5a8afb8e3493a0ed9`, `app/harvest_figures.py` `610eb6862918d2c6695c10d2de58734f`, `app/harvest_identity.py` `9c8d1fd69ffe0594968b4acd2751fba9`; `app/harvest_keys.py` is absent there (a path that does not exist at `3b94a83e05`).
- So the seven carried files apply clean on `3b94a83e05` exactly as on `aa2efa2cf3`; `git diff --name-status <3b94a83e05> rel-amgt-harvst-cj3` is the same seven paths (3 `M`, 4 `A`).

## THE CHANGE TO THE ACT

1. **The base is the live commit read three ways at the cut** (`EC2_MANIFEST.json`, the instance, `/opt/opal-gateway/.deployed_commit`). **It must read `3b94a83e0572f9a14851c2f229ca4aba64c7e670`** (ap-40 deployed) and ap-40's ledger must be CLOSED, which the issuer confirms to the seat in the GO (from site Z through MSTR). If the three readings are anything else, STOP: `aa2efa2cf3` means ap-40 has not deployed (do not cut: a second deploy would revert it), and any other commit means another release landed and the md5 guard is redone and shown to the CTO.
2. **`DEPLOY_BASE_REF` is that live commit** (`3b94a83e05` expected).
3. **The md5 guard** the seat prints at the cut is the table above, read at the LIVE commit it cut on.
4. **Everything else of the COO half stands:** the seven paths and their carried md5s from `34fb405b29`, the tests (75), the controls, the proof reads (BP and NG in both spellings), both branches, C-1 to C-10 (site Z told first; its GO before the deploy; the ref pushed to the shared lineage after).
5. **The window** is from the issuer's GO after ap-40's CLOSED time; site Z's window of 09:45Z to 12:00Z may extend and its CTO clears an extension on ask.

## WHAT THIS DOES NOT CHANGE

The blast radius, the served moves, the rollback (redeploy `previous_deployed_commit`, which after ap-40 is `3b94a83e05`, not `aa2efa2cf3`: the seat reads it at the start and prints it) and the files carried.

## VERDICT: SIGNED (COO). Not in force until the CTO confirms it at these bytes (one line is enough).
