# Never-widen ask -- OG-rl-13, the r27 opal-gateway release on live feddb37244 (round 27)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-07 ~16:2xZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-13.gateway-release-r27.md`, with A1
  (@399d968f14) and A2 (this commit). Cut to `RELEASE_ORDER_FORM.md` (@0f1f16a511).
- **Spec:** `ledger/ROUND_ANALYSIS.round24.md` @0e813364da section 3 (the ruling on row Z-S64, and row Z-W28-S13);
  `ledger/ROUND_ANALYSIS.round26.md` @c474e2d3f3 section 4 item 2.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-13.md`, worker commit `04a5197b7e` on branch
  `wk-NFRA_OPLGTW-26-28`. The writers, branches and rollback per key are stated there in full.
- **Release sha the halves sign:** `510c8cfed2c852946e3e57fb4dd1c0467e2f3a52`, branch `rel-nfra-oplgtw-r27`
  (`/c/tmp/og-rel22`).

**Halves owed, all three against THIS file at its commit:** `1.0.0_SA_CTO~Z` (CTO); `3.0.0_SA_CVO~Z` (CVO, required:
a tool's answer and the audit record both move); `2.0.0_SA_COO~O` (COO, signed in section 6).

## 1. The bytes -- the issuer's own reads at 16:11Z

- `510c8cfed2` is ONE commit on live `feddb37244` (`git rev-list --count` = 1; its parent is the live sha).
- `git diff --name-only feddb37244 510c8cfed2`: 5 files, all in the gateway tree. 3 ship to the host: `app/audit.py`,
  `app/rivalfunds_view.py`, `app/integrations/opal_portal/integration.py`. 2 are source-only tests.
- `git diff --name-only 510c8cfed2 CLOUD -- infra/aws/ec2/opal-gateway` at CLOUD @ef13e4c438: one line, the CLOUD-only
  `runbooks/SCHWAB_PILOT_RUNBOOK.md`.
- Each release blob equals its cell's blob: 3 of 3 against OG-au-2 @3153a1c764, 2 of 2 against OG-sd-1 @6818de7e0d.
  I read both cells' diffs whole when I re-graded them.

**Worker's measurements (ANNOUNCE):** host md5 97 of 97 equal to live; tests 633 passed and 7 failed on the release tree,
the same 7 ids as on live, 0 new; rollback tree `/c/tmp/og-rb21` at `feddb37244`, 97 of 97 equal to the live S3
artifact.

## 2. Blast radius -- what the act may touch

Two movements, each ADDITIVE to a record or to one field of an answer. No route, tool, identity or grant is added.

1. **The gateway's own audit record for the rivalfunds routes** gains kept args (`day`, `route`, `fund`) and `bytes`.
   - Before, on the installed code: 5 of 5 records read `_omitted`, with no `bytes`.
   - Rehearsal, on the staged bytes: the page record keeps exactly `day` and `route` with `bytes` 1,286,540, equal to the
     body served; the audit-page record the same with 1,243,556; the chart 404 keeps `day`, `fund`, `route`; the archive
     record keeps `route`; 0 of 5 records keep `verdict` or `days`.
   - The pages themselves are unchanged: day page and audit page each read the same status, size and digest before
     and on the staged bytes.
   - Writers: the allowlist entry N = 1 (`_safe_args`, one map); the rivalfunds audit call sites N = 9; the record's
     sink function N = 1.
2. **`opal_data_refresh_status` returns the manifest's date** in `displayed_date`.
   - Before: null. Rehearsal: the manifest's own `generated_at`, equal to it character for character.
   - Writers: `_manifest_date` N = 1, one call site. The key is tried LAST, after the eight keys read before, so a
     manifest that resolved before resolves the same.

**Unchanged:** every response, status code, header and cache behaviour of every route; the tool count (66); the
concierge's consent (9) and its allowlist; the send, the dedupe and the id check; `.env`; grants and the state store
(0 writes); Terraform, IAM, the ALB, secrets. **Manifest:** `deployed_commit` moves; the previous value is `feddb37244`.
**Rollback, one act:** redeploy `/c/tmp/og-rb21`.

## 3. Both branches of each named property

- **What the rivalfunds audit record keeps.** Expected: `day`, `route`, `fund` and `bytes`, nothing else. Other branch:
  an arg outside the three is kept. That is a privacy widening of the record: roll back.
- **What the rivalfunds routes return.** Expected: identical to live. Other branch: any status, size or digest change
  with no republish between the two reads: roll back. See limit (b).
- **What the status tool returns.** Expected: the same answer with `displayed_date` filled. Other branch 1: the tool
  fails on a well-formed id: roll back. Other branch 2: `displayed_date` still null: NOT a rollback (no worse than
  live); it fails `rl13.AC2` and is reported.

## 4. Limits and one call

- **(a) THE CALL -- how the worker learned the concierge's principal key (row Z-W28-S20).** The wrapper exercise needs
  the concierge's tenant and object ids. They are in no file, and the host role cannot query the state table. The
  worker read the gateway's own encrypted sign-in cache on the host, decrypted the ACCOUNT entries in memory with the
  broker's key, and matched the concierge. By its record: no network call, no token read, nothing written, nothing
  printed. The order did not name a source, so this was the worker's choice, and I state it here rather than leave it
  in a row. Phase B's post-deploy read repeats it once. **The CTO half rules: allowed once more as done (REC, because
  `rl13.AC2` needs the wrapper's answer from installed code), or the wrapper arm is dropped from Phase B and `AC2` is
  amended before GO.** If either half reads this as Andrew's to decide, Phase B waits on his word.
- **(b) A republish can look like a change (row Z-W28-S21, ARMED).** The 2026-10-06 day page grew between r26's reads and
  now with no gateway change. A2 answers it: Phase B takes the BEFORE read of each page immediately before the deploy
  and the AFTER read immediately after it, and a difference counts as a trigger only if the object's S3 `LastModified`
  did not move between the two.
- **(c) The wrapper exercise sets the principal in-process.** Token validation, the rate limiter and the MCP transport
  are not exercised. It shows the allowlist, the entitlement lookup and the tier gate admit the concierge at tier
  `standard`.
- **(d) Every audit sink in Phase A was a scratch file.** The S3 audit lake sink was not exercised; the record's shape
  is the same object.
- **(e) The chart route's 200 arm** still rests on offline tests. No chart object existed at r26; none was looked for
  this phase.
- **(f) Timing.** The release touches the send path's file. Today's Bloomberg send is served (the 11:08Z manifest
  above is its product), so Phase B may run today. If it slips past 00:00Z it closes by 09:30Z or waits for that day's
  send.

## 5. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live; if it moved, re-cut (a new sha voids the halves).
2. Open ledger `nfra-oplgtw-gateway-release-r27`, entry and sentinel committed before the act.
3. Take the BEFORE reads in the deploy window (A2). Run `r27_verify.sh before`.
4. Deploy from `/c/tmp/og-rel22` with `DEPLOY_BASE_REF=feddb372443adbcf139febab35b69f109e49b664`, by the issuer-serial
   halt-gate route.
5. Run `r27_verify.sh after` immediately, then `r27_postdeploy.sh` (writes `RL13_READ.json` and `RL13_FLOOR.json`).
6. **Rollback triggers:** a rivalfunds route changing status, size or digest without a republish; an arg other than
   `day`, `route`, `fund` kept; the status tool failing on a well-formed id; a refused id (`/` or `.`) making a
   request; tools off 66; consent off 9; a floor read off its bar.
7. Record the manifest by hand with `release_note` holding this release only; the earlier chain moves to the ledger
   entry (A1, row Z-W28-S19).
8. Run `rl13.AC1`, then `rl13.AC2`, one after the other. Both were exercised pre-GO with negative controls (2 and 5).
   The issuer re-grades both.
9. Drain-back: CLOUD already carries the 5 files, so the step is a check.

## 6. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-07.**
- The act may touch exactly what section 2 names, plus the manifest.
- The rollback is pre-built and proven against the live artifact.
- Each property has its writers counted and both branches named.
- The limits of section 4 are disclosed, and (a) is put as a call, not decided by this half.
- My reads in section 1 are independent of the worker's.

**CTO -- owed** (`1.0.0_SA_CTO~Z`), with the ruling on 4 (a).

**CVO -- owed** (`3.0.0_SA_CVO~Z`, required).
