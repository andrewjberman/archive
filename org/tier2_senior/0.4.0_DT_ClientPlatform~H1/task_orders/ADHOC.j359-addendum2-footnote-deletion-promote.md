# pipeline-override: J359 is a REMOTE JOB (/remote-drive; Andrew-directed 2026-10-14), not a registered project: no PRD, no decomposition, no tree. The portal promote of its second approved candidate rides one DT ADHOC order, on ADHOC.j359-satellite-factsheet-portal-promote in this folder (the first promote, closed: PROD 5ab67a651a62, CI success).
<task_order id="ADHOC.j359-addendum2-footnote-deletion-promote">
<to_id>ADHOC.j359-addendum2-footnote-deletion-promote</to_id>
<issued_by>2.0.0_SA_COO~J1</issued_by>
<issued_to>0.4.0_DT_ClientPlatform~H1</issued_to>
<date>2026-10-14</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (Andrew-approved; STAGED until the dell1 re-seat: no leg across the 21:00Z restart)</priority>

<title>J359 addendum 2: promote the two-sentence deletion under Trailing Returns (cand/dell1/satellite-returns-method @714f8e48c8) -- merge-forward to DEV, the chosen-set release on current PROD, /prod-deploy, and the deployed bundle read</title>
<context>
AMENDED 2026-10-14 ~20:56Z (second amendment), ANDREW-DIRECT via `1.0.0_SA_CTO~DELL1` msg 5899 (record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_205xZ_ONE_PROMOTE_TRSB_FIX_PLUS_J359_DELETION.md` @`4bbfec5238`): Andrew wants ONE PROD promote, as soon as possible, carrying BOTH this deletion and the TRSB Excel fix. The release is therefore TWO features: `cand/dell1/satellite-returns-method` (@`714f8e48c8`, the deletion) and `cand/dell1/trsb-history-excel-download` (@`040b152f41bf`, already in DEV at `bbad56e354e9`; row `dell1-20261014T204814Z-c2b9` APPROVED valid=yes by andrew, class opal-internal, page Trade Submission; read by the issuer 20:55Z). If a one-feature release was already built, REBUILD it with both features before any PROD push. Nothing else rides it.

THE ORDER WAS STAGED, NOT PENDING (superseded by the GO @27b8e82787 and the amendment above). It was cut at 20:5xZ, ten minutes before tonight's dell1 restart at 21:00Z. The CTO's condition 3 on both J359 never-widen pairs is that no leg straddles that restart, and the first promote took about 12 minutes (GO 19:29Z, done 19:41Z). UN-PARKING CONDITION: the issuer sends a GO message citing this order after the re-seat, to the then-live `0.4.0_DT_ClientPlatform~H1`. Until that message, do nothing; on it, flip `<status>` to `pending` and begin. If the issuer's seat is gone after the restart, any live seat holding the dell1 COO or CTO role may send it; the standing approval below does not expire.

Andrew approved this exact change. His words (typed in session at the issuer's terminal, 2026-10-14, after the served read): "go ahead with the deletion". Record: `org/tier1_exec/2.0.0_SA_COO~J1/deliverables/ANDREW_DIRECT_20261014_J359_ADDENDUM2_DELETION_GO.md` @`50234ae112` (LOCAL on box/dell1). His earlier words: "Ok get this pushed when done via 0.4.0_DT" (`ANDREW_DIRECT_20261014_J359_PUSH_VIA_DT.md`, on origin `wk-remote-J359` @`d7d9a9ed1a`).

THE APPROVAL ROW: `dell1-20261014T202134Z-fbdf`, CLOSED approved, by andrew, head `714f8e48c8517d1e14f7479693b8d8b5bbd5b538`, 1 commit, class client-facing, pages "Positioning (Satellites mode, factsheet popup)". `python .tools/open-calls.py approval-status --branch cand/dell1/satellite-returns-method` reads `state=APPROVED valid=yes` (read 20:51Z by the issuer).

THE CANDIDATE: branch `cand/dell1/satellite-returns-method` @`714f8e48c8`, on origin (`git ls-remote`), cut from PROD `5ab67a651a62` with ONE commit, three files under `src/components/` (SatelliteFactsheetSections.tsx, satelliteFactsheet.ts, satelliteFactsheet.test.ts). It deletes the hypothetical-returns disclaimer and the exclusions footnote under Trailing Returns (both describe the retired holdings-backcast method) and the builder code that only fed the footnote. No other frontend change. Tests 6 of 6, typecheck rc=0, eslint clean.

THE DATA IT ASSUMES IS LIVE: `s3://opal-data-cot/platinum/satellites/characteristics.json` VersionId `Qh56dS_IliDOh0owKxjToBgEjgJ0pb8v` (2026-10-14T20:15:50Z, trailing returns = the models' realized returns blended with GLD), read back by the AE seat and the issuer. Read the served key's VersionId before you start: if it is NOT `Qh56dS_I...` or a later version of the same producer, STOP and report (the page would then show the old backcast figures with no disclaimer).
</context>

<scope>
1. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO message citing this order is in hand. AMENDED 2026-10-14 ~20:55Z by the issuer, on the CTO's ruling (`1.0.0_SA_CTO~DELL1` msg 5895): Andrew held tonight's dell1 restart ("Dell1 Restart is being held til later", record `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261014_204xZ_DELL1_RESTART_HELD.md` @11a1d08ef0), so there is no 21:00Z restart to straddle, the first pair's condition 3 does not bind, and the GO is sent NOW rather than after a re-seat. Read the restart state yourself before starting (c below): a restart notice that has come back is a STOP.
   b. `approval-status --branch cand/dell1/satellite-returns-method` reads `state=APPROVED valid=yes` with `head_sha` equal to the branch tip (`git ls-remote origin refs/heads/cand/dell1/satellite-returns-method`). A tip that differs from `714f8e48c8` is a stale head: STOP and report.
   c. The clock: no leg is left open across a restart. Read the time and any restart notice before starting; if the hold has been lifted and a restart is due inside the leg (about 15 minutes), STOP and report.
   d. No other promote or deploy is in flight: read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; read the portal's last CI run (`gh run list`) for one in progress.
   e. The served key's VersionId is as the context states.
2. **ORDER OF ACTS:**
   a. **Before print (the positive control).** Read the DEPLOYED bundle (the portal's public site, found the way /prod-deploy's own verification finds it; never a typed host) for the string `holdings at today` and for `data-asset-class-chip`; and for TRSB, `download_url` in the trade-submission chunk (expect ABSENT now: it is the string the fix adds, so a present-before reading means the control proves nothing and you report it). Expect the first two present now (PROD `5ab67a651a62` carries the footnote and the chip). Print the number of bundle files read. If `holdings at today` is absent BEFORE the deploy, the after-read below proves nothing: STOP and report.
   b. **DEV.** `bash .tools/portal-merge-forward.sh cand/dell1/satellite-returns-method --push`. Read its result line: `result=MERGED`, `pushed=yes`; confirm `git ls-remote origin refs/heads/DEV` moved to the merge it printed. A refusal token is a STOP: report it, do not work around it.
   c. **The chosen-set release.** `bash .tools/portal-release-build.sh --features cand/dell1/satellite-returns-method,cand/dell1/trsb-history-excel-download` (comma-separated, as the script's own usage line gives it) on CURRENT PROD (re-read PROD; build on the current one). It never pushes. Then `bash .tools/portal-release-build.sh --check <the release branch it printed>`. Any refusal token refuses the whole release: STOP and report.
   d. **PROD.** `/prod-deploy` for that release, in its own order and with its own gates (clean DEV, zero TypeScript errors via `bun run typecheck`, local PROD re-asserted from origin, merge forward in the ephemeral worktree, push, CI deploys and tags, verify the CI conclusion with `gh run view --json`, the workspace submodule pointer on CLOUD, teardown, confirm DEV, end at the workspace root). The push receipt names BOTH pages: `Positioning (Satellites mode, factsheet popup)`, client-facing, Andrew's word cited above, and `Trade Submission`, opal-internal (row `dell1-20261014T204814Z-c2b9`).
   e. **The served read (after).** After CI reports success, read the DEPLOYED bundle again: `holdings at today` and `left out for lack of one` must be ABSENT; `data-asset-class-chip` and `Trailing Returns` must be PRESENT (the controls), and `download_url` must be PRESENT in the trade-submission chunk (the TRSB fix). Print the number of bundle files read and the 403 count. A bundle still carrying the sentence is Branch B.
3. **If anything fails after the PROD push:** the ordinary /prod-deploy rollback (re-promote the prior PROD `5ab67a651a62` through the same route) in the same session; report loudly. Before the PROD push, a failure leaves PROD untouched: report which leg.
4. Report to `2.0.0_SA_COO~J1` and to `1.0.0_SA_CTO~DELL1`: the DEV head and merge, the PROD head, the CI run id and conclusion, and both bundle reads. The issuer relays to Andrew and to the requester (Yang Liu, for CW).
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.4.0_DT_ClientPlatform~H1/
portal
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>python .tools/open-calls.py approval-status --branch cand/dell1/satellite-returns-method, then git ls-remote origin refs/heads/cand/dell1/satellite-returns-method, then the merge-forward result line and git ls-remote origin refs/heads/DEV</invocation>
  <expect>state=APPROVED valid=yes with head_sha equal to the branch tip 714f8e48c8...; result=MERGED pushed=yes; origin DEV moved to the merge the line printed</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>portal-release-build.sh --features cand/dell1/satellite-returns-method,cand/dell1/trsb-history-excel-download, then --check on the release branch, then /prod-deploy's own steps, then gh run view --json on the CI run it names</invocation>
  <expect>the release builds on current PROD with no refusal token and --check passes; the PROD push receipt names Positioning (Satellites mode, factsheet popup) as client-facing and Trade Submission as opal-internal; the CI conclusion is success; PROD's head after the push is the release's merge</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the deployed bundle read BEFORE (holdings at today, data-asset-class-chip, download_url in the trade-submission chunk) and AFTER (holdings at today, left out for lack of one, data-asset-class-chip, Trailing Returns, download_url), each with the number of bundle files read</invocation>
  <expect>before: the first two present and download_url absent (the controls); after: holdings at today and left out for lack of one absent, data-asset-class-chip, Trailing Returns and download_url present; denominators printed; or reported as Branch B with the CI run id</expect>
</criterion>
</proof_of_spec>
</task_order>
