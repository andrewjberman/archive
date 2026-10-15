# pipeline-override: MDPF_CANON round 9 -- the round-9 issuance @94f8cbd3d9 is closed to new order files (ONE ISSUER PER ROUND), so the portal promote of the Global Trend candidate rides one DT ADHOC order, on ADHOC.j359-addendum2-footnote-deletion-promote in this folder (the same two-step shape; its PROD head 5d64641891 is the base here).
<task_order id="ADHOC.canon-r9-trend-portal-promote">
<to_id>ADHOC.canon-r9-trend-portal-promote</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.4.0_DT_ClientPlatform~H1</issued_to>
<date>2026-10-15</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P1 (Andrew-direct 2026-10-15 ~01:1xZ: "let's get that sorted for PROD now"; STAGED until the CTO rules on DEV and the issuer's GO names this order)</priority>

<title>MDPF_CANON CN-p-2: promote the Global AUA Trend with Custom Models roll-forward (cand/dell1/mdpf-canon-global-trend-variant1-rf @15f7610285) as a one-feature chosen-set release on current PROD 5d64641891, /prod-deploy, and the deployed bundle read; /portfolios is client-facing</title>
<context>
Andrew approved this exact feature. His words (typed at the issuer's terminal, 2026-10-15 ~01:1xZ, after smoking the build on port 5174): "It looks good! ... Only thing is need rollforwards for the the Custom Models. This is good though, let's get that sorted for PROD now". Record: `org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261015_01xxZ_COO_D1_TREND_LOOKS_GOOD_CUSTOM_ROLLFORWARD_THEN_PROD.md` @9fbada016d. THE APPROVAL ROW: `dell1-20261015T013256Z-f411`, CLOSED approved, by andrew (the CTO closed it on that record, msg 5975), head `15f7610285f7719e837f3783fed51e03413a8671`, 6 commits, class client-facing, page "/portfolios (Model Portfolios: Global Trend, firm views, Other Models card)". `python .tools/open-calls.py approval-status --branch cand/dell1/mdpf-canon-global-trend-variant1-rf` reads `state=APPROVED valid=yes` (the CTO's read 01:33Z). The superseded row `dell1-20261014T230556Z-a196` is withdrawn: do NOT promote its branch `cand/dell1/mdpf-canon-global-trend-variant1`.

THE CANDIDATE: branch `cand/dell1/mdpf-canon-global-trend-variant1-rf` @`15f7610285`, on origin (the issuer read `git ls-remote` 01:35Z), cut from PROD `5d64641891` by six commits (CN-i-1, CN-l-2, CN-i-2 as cherry-picks, then CN-p-2 and its two amendments): `src/pages/ModelPortfolios.tsx`, `src/lib/trendGrouping.ts`, `src/lib/otherModelsAsOf.ts`, `src/components/CategoryViewTree.tsx`, `src/api/portal-proxy.ts`, `src/api/endpoints/aum.ts` (six files). What it changes on `/portfolios`: the Global AUA Trend draws the whole history, Nov 2024 to the as-of; Client Supervised, ETF Strategies and ALT Strategies are read from the served Global series; Custom Models rolls forward; carried points are marked; an internal session (opal-capital firm claim or the Dev user type) sees the per-model lines before 2026-05-15 stitched from the firm series and every other session sees one Models band; the approved edits ride it (lime Client Unsupervised, the Other Models "as of" line, the 49 Financial view). Issuer checks at the head: oracle 7 of 7, variants 12 of 12, wiring 10 of 10; `bun run typecheck` rc 0 (with a planted-error control rc 2); provenance guard OK.

THE DATA IT READS IS LIVE: `s3://opal-data-portal-v2/platinum/mdpf/global/aggregate-aua-timeseries.json` VersionId `s5Z3becVq3gTW09YzbVVb_HRopzUxFzC` (2026-10-14T23:10:55Z, carries `client_supervised_aua`, `etf_strategies_aua`, `alt_strategies_aua` and nine `carried_dates`; published by the one-time splice of `ADHOC.canon-r9-trend-publish-tonight`, a splice authorised by Andrew, NOT a lambda run). Read the served key's VersionId before you start: if it is not that version or a later one that still carries the four keys, STOP and report (the page would then draw no groups).

DEV IS NOT A LEG OF THIS ORDER. `portal-merge-forward.sh` REFUSED the branch with `reason=conflict` (DEV's ModelPortfolios.tsx and trendGrouping.ts hold the earlier, declined copy of the same feature, byte-equal to 34cd12d2). The CTO RULED (msg 5977, option a): PROD from the approved branch tonight; DEV converges separately by merge-forward of a resolution branch the issuer cuts (`cand/dell1/mdpf-canon-global-trend-variant1-rf-dev`). If `/prod-deploy` REFUSES because DEV lacks the feature, STOP and report that refusal text: the issuer converges DEV first and re-sends the GO. The chosen-set release builder merges from PROD, never from DEV. Do NOT merge anything to DEV and do NOT work around the refusal.
</context>

<scope>
1. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO message citing this order is in hand (it follows the CTO's ruling on DEV). Without it this order is `staged`; on the GO, flip `<status>` to `pending` and begin.
   b. `approval-status --branch cand/dell1/mdpf-canon-global-trend-variant1-rf` reads `state=APPROVED valid=yes` with `head_sha` equal to the branch tip (`git ls-remote origin refs/heads/cand/dell1/mdpf-canon-global-trend-variant1-rf`). A tip that differs from `15f7610285f7719e837f3783fed51e03413a8671` is a stale head: STOP and report.
   c. The clock: no leg is left open across a restart (Andrew held tonight's restart; read any restart notice before starting).
   d. No other promote or deploy is in flight: read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; read the portal's last CI run (`gh run list`) for one in progress.
   e. The served key's VersionId is as the context states.
2. **ORDER OF ACTS:**
   a. **Before print (the positive control).** Read the DEPLOYED bundle (the portal's public site, found the way /prod-deploy's own verification finds it; never a typed host) for these strings: `data-trend-composition`, `Carried forward (last known value)` and `models held at one firm are in the total` (all expected ABSENT now: they are what this feature adds, so a present-before reading means the after-read proves nothing and you report it) and `data-asset-class-chip` (expected PRESENT: the control). Print the number of bundle files read.
   b. **The chosen-set release.** `bash .tools/portal-release-build.sh --features cand/dell1/mdpf-canon-global-trend-variant1-rf` on CURRENT PROD (re-read PROD; build on the current one, expect `5d64641891`). It never pushes. Then `bash .tools/portal-release-build.sh --check <the release branch it printed>`. Any refusal token refuses the whole release: STOP and report.
   c. **PROD.** `/prod-deploy` for that release, in its own order and with its own gates (zero TypeScript errors via `bun run typecheck`, local PROD re-asserted from origin, merge forward in the ephemeral worktree, push, CI deploys and tags, verify the CI conclusion with `gh run view --json`, the workspace submodule pointer on CLOUD, teardown, end at the workspace root). The push receipt names the page `/portfolios (Model Portfolios)` as CLIENT-FACING, Andrew's word cited in the context above and the row id `dell1-20261015T013256Z-f411`.
   d. **The served read (after).** After CI reports success, read the DEPLOYED bundle again: `data-trend-composition`, `Carried forward (last known value)` and `models held at one firm are in the total` must be PRESENT; `data-asset-class-chip` must be PRESENT (the control). Print the number of bundle files read and the 403 count. A bundle still missing the strings is Branch B.
3. **If anything fails after the PROD push:** the ordinary /prod-deploy rollback (re-promote the prior PROD `5d64641891` through the same route) in the same session; report loudly. Before the PROD push, a failure leaves PROD untouched: report which leg.
4. Report to `2.0.0_SA_COO~D1` and to `1.0.0_SA_CTO~DELL1`: the PROD head (from an `ls-remote` read), the CI run id and conclusion, and both bundle reads. The CTO needs the PROD hash; the issuer relays to Andrew and to the CRO.
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
  <invocation>python .tools/open-calls.py approval-status --branch cand/dell1/mdpf-canon-global-trend-variant1-rf, then git ls-remote origin refs/heads/cand/dell1/mdpf-canon-global-trend-variant1-rf, then the served key's head-object VersionId</invocation>
  <expect>state=APPROVED valid=yes with head_sha equal to the branch tip 15f7610285...; the served key's VersionId is s5Z3becVq... or a later version that still carries the four Trend keys</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>portal-release-build.sh --features cand/dell1/mdpf-canon-global-trend-variant1-rf, then --check on the release branch, then /prod-deploy's own steps, then gh run view --json on the CI run it names</invocation>
  <expect>the release builds on current PROD with no refusal token and --check passes; the PROD push receipt names /portfolios as client-facing with the row id and Andrew's record; the CI conclusion is success; PROD's head after the push is the release's merge</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the deployed bundle read BEFORE (data-trend-composition, Carried forward (last known value), models held at one firm are in the total, data-asset-class-chip) and AFTER (the same four), each with the number of bundle files read</invocation>
  <expect>before: the first three absent and data-asset-class-chip present (the controls); after: all four present; denominators printed; or reported as Branch B with the CI run id</expect>
</criterion>
</proof_of_spec>
</task_order>
