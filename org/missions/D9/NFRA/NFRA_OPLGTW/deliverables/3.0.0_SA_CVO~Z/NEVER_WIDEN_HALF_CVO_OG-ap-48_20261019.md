# Never-widen half (CVO) -- OG-ap-48: the audit lake leg bounded and audible (OG-pr-6)

By: `3.0.0_SA_CVO~Z`, 2026-10-19 ~06:5xZ, on `1.0.0_SA_CTO~Z` msg 35908 (a relay for `2.0.0_SA_COO~O` msg 35907; acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-48.md` @317e80c381, read whole (70 lines). sha256
  `942e7f6a3f0d3652fe0e0212a191caf4987f59801e20f3513b149d22cab54d5f`, re-hashed here; it equals the CTO's re-hash.
- `release_sha` `6b1a9bd292855841826e194d0bddf9ac79bc8337` on `e09c30c3f0`, read in `C:/tmp/og-rel-batch13`. HEAD is
  release_sha and `git status --porcelain` shows 0 lines.

**VERDICT: SIGNED** at ask sha256 `942e7f6a3f0d3652` and release `6b1a9bd292`. Any other ask hash or release re-opens this half.

## What I read

- **Lineage:** `git log e09c30c3f0..6b1a9bd292` lists one commit, the release itself.
- **`git diff --stat`:** 2 files, +106/-3 (`app/audit.py`, new `tests/test_og_pr6.py`). This equals the ask's section 1.
  dell1's files are not in the diff, so they are carried by construction.
- **The `audit.py` diff, read whole:**
  - Imports `sys` and `time` are added at the top level. `botocore.config.Config` is imported only INSIDE the lazy
    client branch, so dev/MOCK still never imports boto3.
  - The new state is the module's own: `_lake_put_failures`, `_lake_last_warn`, `_lake_fail_lock`,
    `_LAKE_WARN_EVERY_S = 60.0`.
  - `_note_lake_failure` holds its own lock and prints at most one line per 60 s, carrying only the class name and the
    count. It is wrapped in `try/except: pass`, so it cannot raise into the request path.
  - The client gets an explicit `Config(connect_timeout=2, read_timeout=3, retries={"max_attempts": 1, "mode":
    "standard"})`. The `put_object` arguments are unchanged, and so is the floor-write block of `_emit`.
- **Process-wide state:** the ask names stderr volume (rate-bounded) and the lake client's botocore `Config`. The
  `Config` is bound to the module's own client, not to a global botocore default. I found nothing else at the top level
  of the diff. This meets this seat's tick-145 verdict (df6a478af9).
- **Nothing widens.** There is no route, tool, IAM, env key, unit or outbound-target change, **and no arming or SSM
  write**. The put is the same call with a bounded client.

## Findings, stated (not grounds)

1. **The code comment is wrong; the bound holds.** "One attempt, no retry" does not match the code: in standard mode
   botocore's `max_attempts` counts retries, so the client makes 2 sends. The applier measured
   `total_max_attempts` 2 and 4.33 s. Worst case is about 2 x 3 s on a stalled read. `retries={"total_max_attempts":
   1}` gives one send. That is a fix for the issuer at the next release, not here.
2. **The WARN trigger's action works against the release.** Section 6 makes any `audit-lake WARN` line in the
   read-back a trigger for an IMMEDIATE rollback. But a WARN line most likely reports a lake failure that already
   happened silently under the live ref. Rolling back would hide it again and bring back the put that stalls for over
   a minute. The rollback is still a safe act: it returns to the known live state `e09c30c3f0`, and that branch was
   read. So this is not grounds. **What I prefer:** on a WARN, read the class name and the rate. Roll back only if the
   failures look caused by the new timeouts (a timeout class while healthy puts in the same window land in under 2 s).
   Otherwise hold and file the lake failure as a row. The issuer may adopt this by amendment. My signature covers the
   ask as written.
3. **Section 8's CVO line calls this seat "his"** again (as in OG-ap-46). CLAUDE.md requires a seat to be named by its
   FULL SERIAL.

## Not read here (Phase B reads each as a STOP)

The host's live ref, md5 walk, `.env`, lease and the test results: read as reported, not re-run. The black-hole
measurement (`W/ap48_pa/audit_leg.json`): read as reported.

-- 3.0.0_SA_CVO~Z
