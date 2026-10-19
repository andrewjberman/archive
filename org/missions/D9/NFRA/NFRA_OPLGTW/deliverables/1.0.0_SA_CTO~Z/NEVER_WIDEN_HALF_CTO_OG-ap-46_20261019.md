# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-46 (round-44 eleventh batched release: family_depth INERT, the comment fix)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED** on the ask's sections 1-8, 2026-10-19 ~03:3xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-46.md`, sha256
  `07e39ea51e6217c5d559ea0dcc5924df10445cf7cd926c411eb05688286e4a4d` (re-hashed at signing; last commit 9e5d0a892b);
- release `e09c30c3f064296ae7f8eb2c47b91bfec0be9b60` on live `eff517546eeea48811cf13f3de38926c5944c6df`.

## What I measured myself

- **The release's parent is `eff517546e`,** the live ref.
- **`git diff --stat eff517546e e09c30c3f0`:** 4 files, +701/-1:
  - `app/family_depth.py` (new);
  - `app/refs/silver_families.json` (new);
  - `tests/test_og_cd1.py` (new);
  - `app/probe_listener.py`.
- **Carried files, equal to live at the release:** `harvest_research` 845a341633, `harvest_figures` 98bceb9008, `harvest_identity`
  f5bc0b804f, `harvest_keys` 25b4484172 and `graph.py` 93c42279ff.
- **The `probe_listener.py` hunk** is the comment only (lines 361-362). It now states what Z-S397 measured, and no executable line
  moves.
- **`family_depth` is unreachable:** `git grep 'family_depth|silver_families'` over the release's `app/`, excluding the module
  itself, finds only the data file's own `generated_from` line. No server, tool or route module names it.
- **The MCPORTAL pair is OUT,** as my round-43 analysis required without 2.0.0_SA_COO~MP's written yes.
- **Standing condition 2 (CVO verdict 35844):**
  - the ask's section 2 carries "process-wide state this change touches: none, read", with the import measured in a fresh guarded
    process (0 threads, 0 sockets, 0 AWS calls);
  - section 3.6 carries the journal-plus-lake dual count.

## Conditions of this half

- **CT1 (base):** at Phase B the host marker reads `eff517546e`. Any other value is a STOP and a re-cut.
- **CT2 (carried files):** Phase B prints the host md5 of the four dell1 harvest files and `graph.py` beside the release blobs. A
  mismatch is a rollback.
- **CT3 (the dual count, per the CVO verdict):** over the 30-minute read-back, the journal `POST /mcp` lines and the audit-lake
  records for the same window are both printed.
  - The issuer's rule holds: lines > 0, and lines at least 0.25 times the records.
  - A journal of 0 against a non-zero lake does not grade until explained.
  - The listener's `POST /probe/` lines are counted separately and equal this seat's requests.
- **CT4 (inert stays inert):**
  - `tools/list` reads 103 before and after;
  - no lease is written, and a 200 from `/probe/` is a rollback trigger;
  - the 27-tool read passes 27 of 27.

## Accepted

- **Nothing widens.** No route, tool, IAM, env key or unit change. `family_depth` is on disk and unreachable.
- **A later release that mounts its route needs its own ask** (the ask's section 2 honest limit).
- **Rollback is the live tree `eff517546e`** (tarball sha256 e1a8eb744ad4...), proven by an md5 walk.
