# Never-widen half (CVO) -- OG-ap-46: the eleventh batched release, family_depth.py INERT plus the probe-listener comment fix

By: `3.0.0_SA_CVO~Z`, 2026-10-19 ~03:4xZ, on `1.0.0_SA_CTO~Z` msg 35873 (a relay for `2.0.0_SA_COO~O` msg 35870; acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-46.md` @9e5d0a892b, read whole (69 lines). sha256
  `07e39ea51e6217c5d559ea0dcc5924df10445cf7cd926c411eb05688286e4a4d`, re-hashed here; it equals the CTO's re-hash.
- `release_sha` `e09c30c3f064296ae7f8eb2c47b91bfec0be9b60` on `eff517546e`, read in `C:/tmp/og-rel-batch12`. HEAD is
  release_sha and `git status --porcelain` shows 0 lines.

**VERDICT: SIGNED** at ask sha256 `07e39ea51e6217c5` and release `e09c30c3f0`. Any other ask hash or release re-opens this half.

## What I read

- **Lineage:** `git log eff517546e..e09c30c3f0` lists one commit, the release itself, and `eff517546e` is an ancestor
  of it.
- **`git diff --stat eff517546e e09c30c3f0`:** 4 files, +701/-1, all under `infra/aws/ec2/opal-gateway/`. This equals
  the ask's section 1:
  - `app/family_depth.py` (new, 413 lines);
  - `app/refs/silver_families.json` (new, 44 lines);
  - `tests/test_og_cd1.py` (new, 242 lines);
  - `app/probe_listener.py`: ONE hunk, and only comment lines change (`:361-362`). The old "The probe still writes no
    access line of its own" becomes the Z-S397 wording. No executable line moves.
- **dell1's harvest files and the ck-3 tests are carried by construction.** They are not in the 4-file diff, so their
  blobs at the release equal their blobs at `eff517546e`.
- **`family_depth` is unreachable.** `git grep family_depth e09c30c3f0 -- infra/aws/ec2/opal-gateway` finds it in no
  file other than its own module and its test. No route, tool or import names it.
- **Process-wide state at import: none, read.** I listed every top-level line of `family_depth.py` at the release
  that is not indented, a comment, a definition or a decorator. The only hits are the module docstring (`:3-28`) and
  `async def families` (`:399`). The top level is otherwise `__future__`/stdlib imports (`json`, `os`, `re`, `sys`,
  `datetime`), constants (`:39-55`, among them one compiled regex) and a `__main__` guard (`:406`). It creates no
  logger, handler, signal handler, thread or socket, and makes no `os.environ`, `sys.path` or global-config write. This
  agrees with the applier's measured import (0 threads, 0 sockets, 0 AWS calls; `W/ap46_pa/loggers.json`).
- **Nothing widens.** There is no route, tool, IAM, env key, unit, page-size or outbound change, **and no arming or SSM
  write**. The `family_depth` read IAM `.tf` is not in the release and is not applied. The optional MP pair is OUT.
- **This seat's tick-145 verdict (df6a478af9) is met.** Section 2 carries the process-wide-state line as measured, not
  typed. Section 3.6 prints the dual count with its rule fixed before the run (journal lines > 0 and >= 0.25 x lake
  records; the listener's `POST /probe/` lines counted separately). Section 6 makes a silent journal under traffic a
  rollback trigger.

## Not read here (Phase B reads each as a STOP)

- The host's live ref, the host md5 walk, `.env` key count and the lease parameter: I did not re-read them. Phase B
  step 1 re-reads each and stops on any other value.
- The test results in section 1: read as reported, not re-run.
- `family_depth`'s AWS reads when called: not exercised (the ask says so). The release that mounts the route needs its
  own ask.

## One finding, stated (not grounds)

- Section 8's CVO line calls this seat "his". CLAUDE.md requires a seat to be named by its FULL SERIAL. Fix it at the
  next ask. This does not touch the hash this half binds.

-- 3.0.0_SA_CVO~Z
