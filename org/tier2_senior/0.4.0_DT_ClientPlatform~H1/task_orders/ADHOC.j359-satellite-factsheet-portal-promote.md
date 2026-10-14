# pipeline-override: J359 is a REMOTE JOB (/remote-drive; Andrew-directed 2026-10-14), not a registered project: no PRD, no decomposition, no tree. The portal promote of its approved candidate rides one DT ADHOC order, on the ADHOC deploy orders in the sibling CloudOps folder and the CTO's instruction (msg 5768) to issue it to 0.4.0_DT_ClientPlatform~H1.
<task_order id="ADHOC.j359-satellite-factsheet-portal-promote">
<to_id>ADHOC.j359-satellite-factsheet-portal-promote</to_id>
<issued_by>2.0.0_SA_COO~J1</issued_by>
<issued_to>0.4.0_DT_ClientPlatform~H1</issued_to>
<date>2026-10-14</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (Andrew-approved; finish before tonight's 21:00Z dell1 restart or after the re-seat)</priority>

<title>J359: promote the satellite factsheet (cand/dell1/satellite-factsheet-prod @6e69a05e43) to PROD -- merge-forward to DEV, the chosen-set release on current PROD, /prod-deploy, and the CI conclusion read</title>
<context>
Andrew approved this candidate after his own smoke on localhost:5174. His words, relayed by `1.0.0_SA_CTO~DELL1` (msg 5768, 19:27Z): "Just smoked the 5174 build, looks good push it". Record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_192xZ_J359_SMOKE_PASSED_PUSH_IT.md`. His earlier words: "Ok get this pushed when done via 0.4.0_DT" (`org/tier1_exec/2.0.0_SA_COO~J1/deliverables/ANDREW_DIRECT_20261014_J359_PUSH_VIA_DT.md`, on origin `wk-remote-J359` @`d7d9a9ed1a`), and, on the smoke: "if i approve, then we shoudl get that promoted to PROD".

THE APPROVAL ROW: `dell1-20261014T192307Z-de27`, CLOSED approved, by andrew, head `6e69a05e43774a140d28e6e6a5e21fcb27f55c27`, 3 commits, class client-facing, pages "Positioning (Satellites mode, factsheet popup)". `python .tools/open-calls.py approval-status --branch cand/dell1/satellite-factsheet-prod` reads `state=APPROVED valid=yes` (read 19:28Z by the issuer).

THE CANDIDATE: branch `cand/dell1/satellite-factsheet-prod` @`6e69a05e43`, on origin (`git ls-remote`), cut from PROD `fa10e75861` with three commits, four files under `src/components/` (SatelliteModal.tsx, SatelliteFactsheetSections.tsx, satelliteFactsheet.ts, satelliteFactsheet.test.ts). The earlier branch `cand/dell1/satellite-factsheet` was refused at registration for dev-overlap (7 of 9 commits already on DEV) and is NOT the candidate. No new fetch, route or producer: the popup reads data the Positioning page already holds.

THE DATA IT DEPENDS ON IS LIVE: `s3://opal-data-cot/platinum/satellites/characteristics.json` VersionId `6z8c7qDDQTd2Q9k8qSoPpO78CxlsWAgZ` (2026-10-14T18:57:08Z), read back by the AE seat, the CTO and the issuer. The sequence the CVO set (producer live and read back before the portal) is met.

The issuer ran `.tools/portal-merge-forward.sh cand/dell1/satellite-factsheet-prod` WITHOUT `--push` at 19:28Z: result MERGED, merge commit `8a1b5976445962678f9611cc8f14bd82fa466fc6`, `pushed=no`, DEV unchanged at `9e637fe51e`. That merge is local and is NOT a landing. A non-DT seat cannot push DEV or PROD in the portal repo (never-rules-gate); the push is yours.
</context>

<scope>
1. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. `approval-status --branch cand/dell1/satellite-factsheet-prod` reads `state=APPROVED valid=yes` with `head_sha` equal to the branch's tip (`git ls-remote origin refs/heads/cand/dell1/satellite-factsheet-prod`). A tip that differs from `6e69a05e43` is a stale head: STOP and report.
   b. The clock: read it. Start only if at least 45 minutes remain before 21:00Z, else wait until the re-seat. No leg is left open across 21:00Z.
   c. No other promote or deploy is in flight: read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; and read the portal's last CI run (`gh run list`) for one still in progress.
2. **ORDER OF ACTS:**
   a. **DEV.** `bash .tools/portal-merge-forward.sh cand/dell1/satellite-factsheet-prod --push` (the script fetches DEV and the branch itself, and merges only on the approved row). Read its result line: `result=MERGED`, `pushed=yes`; confirm `git ls-remote origin refs/heads/DEV` moved to the merge it printed. A refusal token on the result line is a STOP: report it, do not work around it.
   b. **The chosen-set release.** `bash .tools/portal-release-build.sh --features cand/dell1/satellite-factsheet-prod` on CURRENT PROD (the CTO read PROD `fa10e75861`; re-read it, and if PROD has moved, build on the current one). It never pushes. Then `bash .tools/portal-release-build.sh --check <the release branch it printed>`. Any refusal token (`not-approved`, `stale-head`, `commits-differ`, `unapproved-commits`, `conflict`) refuses the whole release: STOP and report.
   c. **PROD.** Run `/prod-deploy` for that release, in its own order and with its own gates (clean DEV, zero TypeScript errors via `bun run typecheck`, local PROD re-asserted from origin, merge forward in the ephemeral worktree, push, CI deploys and tags, verify the CI conclusion with `gh run view --json`, the workspace submodule pointer on CLOUD, teardown, confirm DEV, end at the workspace root). The push receipt names the page changed and its class: `Positioning (Satellites mode, factsheet popup)`, client-facing, Andrew's word cited above.
   d. **The served read.** After CI reports success, read the DEPLOYED bundle (the portal's public site, found the way /prod-deploy's own verification finds it; never a typed host) for the strings `data-asset-class-chip` and `Trailing Returns` (both are new in this candidate). Print the denominator: the number of bundle files read. A bundle without them is Branch B.
3. **If anything fails after the PROD push:** the ordinary /prod-deploy rollback (re-promote the prior PROD `fa10e75861` through the same route) in the same session; report loudly. Before the PROD push, a failure leaves PROD untouched: report which leg.
4. Report to `2.0.0_SA_COO~J1` and to `1.0.0_SA_CTO~DELL1`: the DEV head and merge, the PROD head, the CI run id and conclusion, and the served read's result. The issuer relays to Andrew and to the requester (Yang Liu, for CW), whose check is to open each satellite popup on Positioning.
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
  <invocation>python .tools/open-calls.py approval-status --branch cand/dell1/satellite-factsheet-prod, then git ls-remote origin refs/heads/cand/dell1/satellite-factsheet-prod, then the merge-forward result line and git ls-remote origin refs/heads/DEV</invocation>
  <expect>state=APPROVED valid=yes with head_sha equal to the branch tip 6e69a05e43...; the result line reads result=MERGED pushed=yes; origin DEV moved to the merge the line printed</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>portal-release-build.sh --features cand/dell1/satellite-factsheet-prod, then --check on the release branch, then /prod-deploy's own steps, then gh run view --json on the CI run it names</invocation>
  <expect>the release builds on current PROD with no refusal token and --check passes; the PROD push receipt names Positioning (Satellites mode, factsheet popup) as client-facing; the CI run's conclusion is success; PROD's head after the push is the release's merge</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the deployed bundle read for data-asset-class-chip and Trailing Returns, with the count of bundle files read</invocation>
  <expect>both strings present in the deployed bundle; the denominator printed; or, if absent, reported as Branch B with the CI run id</expect>
</criterion>
</proof_of_spec>
</task_order>
