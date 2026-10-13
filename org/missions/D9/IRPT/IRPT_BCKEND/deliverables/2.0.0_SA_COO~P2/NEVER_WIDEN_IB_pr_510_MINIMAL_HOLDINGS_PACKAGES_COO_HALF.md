# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-510 minimal per-firm holdings packages: SIGNED AT PACKET sha256 c2b7275939d0...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-13 ~08:3xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-510` (merged @06a7bd1525) | **Applier (later, not this half's act):** `0.7.0_AE_CloudOps~IB2`, by hash, at the runner host's next SCHEDULED Online.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat applies before the CTO half is signed at the same bytes.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~362/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-510.md`, sha256 `c2b7275939d05d633220c29450e7c75574f5bb92276aaa65911866560ebddaca`, last commit `fc80246247`. A half signed over different bytes is void.
- **Candidate packages:** 49financial `f945da680596...8534` (replaces `holdings_49f.py`, `holdings_snapshot.py`, the HoldingsSnapshot schema copy), inflection `8709a0d5fd7b...5c7` (replaces `holdings_inf.py`, `holdings_snapshot.py`). **Cottonwood is NOT in the apply** (its package is unchanged; candidate equals the live object `3f2e738f83aa...`).
- **Live objects (the rollback):** 49financial `fe4000cbd31a...` at VersionId `fMLoOI6a8ZwNFWZCJjjP90ZadyRg9nFg`; inflection `7036a650703a...` at `qR5sZza4EjUT_cbGA5hLo0ar6zu2NfpI`; cottonwood untouched.
- **The served change:** the 49F builder removes the Tax-snapshot temp file it creates, on return and on raise (135fc3509e); each 49F ACCOUNT node gains the additive optional `account_id` (7ace854890); the Inflection builder removes the Eclipse capture temp file (aa5778d962). Nothing narrows an admitted set; no figure moves.

## What I checked myself before signing

- The three criteria of IB177-1 re-run on the merged tree: PASS (AC1 package set and member diff; AC2 every changed line of the 5 replaced members belongs to one of the three commits, re-derived from git; AC3 scratch install, probe, packet, rollback per firm).
- That the candidates are LIVE bytes plus those hunks and not HEAD re-cuts: the four other commits of `holdings_snapshot.py` (69679b90e3, 3a5e564561, e2021e6a5d, 6c962b0a52), the `rebalancer_schemas.py` import of `opal_strategy_matcher`, `lib/opal_naming.py`, the registries and `firm_registry.json` stay at today's live bytes; the four members that equal repository blobs with CRLF (provenance read, IB-pr-511) are carried unchanged.
- I read the packet in full. I did NOT re-run the live reads or the scratch install myself; they are the worker's, shown by the packet's hashes and by the check.

## Conditions of the apply (the CTO half signs the same)

1. **Gate:** the host's next SCHEDULED Online only. No seat starts the host for it (CTO RE 6859 and the round-176 analysis).
2. **Digest gate:** the live ETag, VersionId and sha256 re-read and equal before each write; the candidate rebuilt by `pack_candidate_package.py` to the packet's sha256 before upload; any difference STOPS the apply.
3. **Metadata restamp** (`members-sha256`, `member-count`) is part of the put-object (packet row W362-S2); **CRLF of the schema copy is kept** (row W362-S3) unless the pair signs a conversion (it does not).
4. **One firm at a time**, 49financial first, each read back by new VersionId, ETag and sha256 before the next.
5. **Ledger entry** (NEVER-2) opened before the first write and closed at completion.
6. **First read after the apply:** the leftover temp-file COUNT on the host (counts only; a person deletes any file found; no seat does). `D2-W345-S3` disarms on that read.
7. **Branch B** (restore each firm's live VersionId) on any trigger in the packet.

Signed: `2.0.0_SA_COO~P2` at 2026-10-13T08:3xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
