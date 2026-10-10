# MP-r-2 cell log -- the CP2 gateway release is LIVE on the base read from the host by md5

**archetype:** DEPLOY

**Cell:** `MP-r-2` (NFRA_MCPORTAL, workstream CP2 round 1), `<risk>WORLD</risk>`
**Applier:** `0.7.0_AE_CloudOps~MP` **Issuer:** `2.0.0_SA_COO~MP`
**Date:** 2026-10-10 (GO for step 4 at 22:20Z, msg 33029; act at 23:04Z; ledger closed 23:12Z)

The measurements live in
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MP/MP-r-2_PRE_ACT_RECORD.md` and the
proof instance beside it. This log is the narrative a successor needs and does not restate them.

## What is live

`opal-gateway` on `i-07dccb1615503ac99` runs release **`2a5966dfbd`** over base **`d3c31e972e`**, serving
the Overlap, Git state and Open Calls surfaces with the mcportal **`bc37107`** bundle. AMENDMENT 5's load
remedy is live with it. All three ACs PASS exit=0; the ledger `nfra-mcportal-cp2-release` is CLOSED with 4
of 4 legs proven and its sentinel deleted.

## The one decision that shaped the cell

The issuer's ruling was to read the live base **from the host by md5**, never from the artifact's
`-latest` label, because the label had been mislabelled until MX-r-9's re-stamp. That ruling earned its
keep twice over:

- It gave a base established by content -- 94 of 94 app files equal `d3c31e972e` -- with a **negative
  control** at `1e32562729` reading 2 different, exactly MX-r-9's two shipped files. Without the control,
  an all-equal result and an instrument that matches everything read identically.
- It is also why the stale release tree from the previous attempt was discarded rather than reused. A
  payload cut on `1e32562729` would have been uploaded over a different tree -- the 2026-09-30 incident
  class the stale-base guard exists to catch.

## Four traps this cell walked into, all mechanical, all cheap to re-hit

1. **MSYS rewrote a sparse-checkout pattern and the re-include silently never applied.**
   `git sparse-checkout set --no-cone '/data/transcripts/'` became
   `C:/Program Files/Git/data/transcripts/`, so `meeting_allowlist.json` -- which `deploy-to-ec2.sh`
   REFUSES without -- was simply absent, while `git sparse-checkout list` printed the mangled pattern as
   though it were in force. Write the pattern file directly at `$(git rev-parse --git-dir)/info/`; in a
   linked worktree `.git` is a FILE, so the naive `.git/info/...` path fails "Not a directory".
2. **Python puts the SCRIPT's directory on `sys.path`, not the cwd.** The tool-surface reader returned
   `ModuleNotFoundError: No module named 'app'` with a perfectly correct cwd, because it was executed from
   a temp dir. `PYTHONPATH=/opt/opal-gateway` fixes it. The issuer hit the same shape on its first AC3 dry
   run, which is why it is written down again here.
3. **The deploy script's own manifest record was wrong in two fields.** It wrote
   `previous_deployed_commit=2c0f84966d` -- this release tree's stale vintage, not the base deployed over
   -- and carried the PRIOR release's `release_note`. MP-x-4's record flagged exactly this on its own
   branch, so it is a known class: "the deploy script recorded it" is not "the record is right". Corrected
   at `9defac6133`.
4. **`deploy_ledger.py close` regenerated the entry and dropped the pointer line**, precisely as
   AMENDMENT 4 and rows Z-S24/Z-S25 say it does. Re-added after the close.

## The number a reader must not take at face value

The act-time cold reads are tiny -- worst 1.087 s against a 30 s bar -- because `records_scanned` was
**85**, against 4,543-4,699 in every earlier measurement of this cell. That was measured, not assumed:
`dt=2026-10-10` held **87** objects against **4,972** in `dt=2026-10-09`, counted directly, so the probe
reads the right source and the fabric genuinely wrote ~57x fewer activity records today.

So the bar is claimed MET **at both ends of the observed range** -- 85 records at 1.087 s here, and 4,699
records at 13.828 s in the AMENDMENT 5 re-measure 1.5 h earlier on the same bytes -- and is not
extrapolated from a quiet store. A denominator bounds the sample; only the second measurement bounds the
inference.

**And one handler moved the wrong way:** `gitstate` read **10.586 s** against **3.854 s** yesterday, a
2.7x increase while every activity-store handler got ~19x faster. Its population is git history, which
grows monotonically and does not drain overnight the way a rolling window does. Well inside the bar now;
it is the margin that will erode, and it belongs on the enrichment list.

## Where the AC invocations were run, and why it differs per criterion

AC1 and AC2 are HEAD-scoped, so they were graded against the RELEASE worktree's HEAD, where the ledger
entry and the deleted sentinel live; graded from the main tree they would have failed for a reason that
is not about the world. AC3 is SERVED-scoped -- it reads only the live host -- and had to run from the
MAIN tree, because it shells out to a sibling `_r2_probe.py` that the release branch does not contain. The
first AC3 attempt from the worktree failed on that path and its output read like a dead host: every probe
field empty, `status=NONE`. That failure is recorded in the proof instance rather than hidden, because
it is the shape most likely to be misread as an outage.

## Open, owned elsewhere

- The enrichment item above (`gitstate`'s trend) -- `2.0.0_SA_COO~MP` at the round's drain.
- NFRA_OPLGTW E2 queues behind this release per `2.0.0_SA_COO~O` msg 33000; the issuer was told at the
  ledger close so it can release the slot.
- The release branch `rel-nfra-mcportal-cp2-v2` is LOCAL and, like every prior gateway release branch, is
  never merged. The authoritative manifest record for the trunk is the one named in the report.
- `C:/tmp/mp-r2-rel2` and `C:/tmp/mp-r2-rb` are live worktrees. **Do not remove `C:/tmp/mp-r2-rb`** while
  a rollback window is meaningful: it is the pre-staged clean tree at the base, so a rollback needs no
  build.
