# pipeline-override: MDPF_CANON round 9 -- the round-9 issuance @94f8cbd3d9 is closed to new order files (ONE ISSUER PER ROUND), so the one-time publish of the Trend groups onto the as-of-2026-10-13 dated objects rides one CloudOps ADHOC order, on the MDPF_CANON round-2, 4, 6, 7 precedents and the sibling ADHOC.canon-r9-gold-trend-groups-deploy.
# TO MDPF_CANON CN-p-1: publish the Trend groups onto the eight as-of-2026-10-13 gold objects and their served copies, tonight, by Andrew's word (laptop-independent; DELL1 CloudOps)
<task_order id="ADHOC.canon-r9-trend-publish-tonight">
<to_id>ADHOC.canon-r9-trend-publish-tonight</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-14</date>
**CLOSED 2026-10-14 ~23:2xZ (2.0.0_SA_COO~D1) on the CloudOps report (msg 5959, ledger `20261014T2304Z_mdpf-canon-r9-trend-publish-tonight`).** Eight gold puts 23:10Z, one publisher run 23:11Z (18 published, failed none); the issuer re-measured the eight keys against their pre-splice versions: each differs ONLY by the CN-p-1 keys (Global also `meta.trend_groups`) or the one `muni` member. PROVENANCE (CTO condition C1): these eight objects are a splice authorised by Andrew's overwrite OK, not a lambda run, and are NEVER cited as evidence of the lambda; the first scheduled fire carrying the code (2026-10-15 13:30Z) is that evidence. CTO C2 was amended at `da6e7b36d0` (the publisher republishes all 18 pairs: 8 change, 10 data-identical). C3: no claim is made about PROD visibility (served-plane cache TTL 300 s; the PROD portal does not read the new keys). Criteria deviations accepted by the issuer: (1) three served category-views equal the built body plus the publisher's own Tax status keys (old and new alike); (2) the readback arm R6 compared the newest object with the previous dated object and failed on a routine one-cell restatement present before the splice: R6 now tolerates at most five restated cells per array and reads PASS (11 of 11 live); (3) four history leaves were republished data-identical.

<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P1 (Andrew-direct ~22:5xZ: "do it", overwrite OK; BEHIND the CTO half of ADDENDUM 1 and the issuer's written GO -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-p-1: eight gold objects (4 scopes x aggregate-aua-timeseries and category-views, as-of 2026-10-13) are overwritten ONCE with the existing body plus the Trend keys / minus the Muni member, by put_object of bodies built by the issuer's read-only builder; the publisher is hand-run once to copy them to the served plane; nothing is deleted, no lambda is changed</title>
<context>
The CN-p-1 code is deployed (your order `ADHOC.canon-r9-gold-trend-groups-deploy`, 22:50Z, D4 green). The first scheduled fire carrying it is 2026-10-15 13:30Z. Andrew wants the Trend groups served TONIGHT and gave an explicit OK to overwrite today's as-of 2026-10-13 objects (CTO record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_225xZ_MDPF_PUBLISH_TREND_TONIGHT_OVERWRITE_OK.md`).
**The lambda cannot do it.** A production invoke has no overwrite switch: `conditional_put` records `conflict` for a business-different body at an existing dated key (measured in the addendum, section 1). So the write is YOURS: eight `put_object` calls of bodies built by `round9/checks/build_publish_bodies.py`, then ONE hand-run of the portal publisher. The signed addendum is `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round9/NEVER_WIDEN_PAIR_R9_CN_P_1_ADDENDUM_1_PUBLISH_TONIGHT.md` (COO half signed; CTO half at `org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R9_GOLD_CN_P_1_ADD1_CTO_HALF.md`). Read it first: section 1 (the mechanism and its provenance), 2 (the eight keys and their prior VersionIds), 3 (branches), 4 (rollback per key).
Lessons that bind here: (1) `NEVER delete` -- the rollback is a copy-object of the prior VersionId; (2) the dry run you did (qa_local) wrote nothing; THIS order writes, so it is the first act that changes a served byte; (3) read every denominator before and after; (4) the bodies are the old bodies plus new keys: if the builder says otherwise it REFUSES and you stop.
</context>

<scope>
1. Open a deploy ledger (NEVER-2) BEFORE the first act, slug `mdpf-canon-r9-trend-publish-tonight`: legs L0 (preconditions), L1 (before print), L2 (build and verify), L3 (the eight puts), L4 (the publisher run), L5 (proofs), and the rollback route. Name in it the eight gold keys, the eight served keys, the publisher function and the pin. Open and COMMIT the sentinel `org/critical_paths/.open_deploys/mdpf-canon-r9-trend-publish-tonight.json` with it.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO is a broker message from `2.0.0_SA_COO~D1` naming this order and the instruments' hashes (below), sent after the CTO half of the addendum is signed. Without it this order is `staged` and WAITS; on the GO, flip the status to pending and start.
   b. Both halves of the addendum are SIGNED (read the two files; a signature is a line in a commit by that seat).
   c. The instruments are the graded ones: LF-normalised sha256 of `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round9/checks/build_publish_bodies.py` is `978f64b61b209fcda270a7ef19bcc1feaf9706b3b93e84101f293b9674456cb4` and of `.../r9_trend_groups_readback.py` is `0b49b04cd3717701463981877f8e1f39da5fd7342f46f7aa38e85f32ea392f98` (read from the checkout you run; a different hash means a later issuer edit: report it and stop).
   d. The deployed code is the pinned code: `mdpf-gold-lambda` `MDPF_GOLD_COMMIT` equals `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f` (your D2 record).
   e. No open deploy sentinel names `mdpf-gold-lambda`, `opal-assets-mdpf-portal-publisher` or the eight keys other than this order's own (read `org/critical_paths/.open_deploys/` in every live worktree: `git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`; union; print the per-tree denominator).
   f. The clock: no put starts within 45 minutes before the 2026-10-15 13:30Z gold fire or the 13:50Z publisher fire, and not while either function is running (read their last invocations first). If the order cannot finish by 12:44Z it STOPS before the first put.
3. **ORDER OF ACTS (the order is the safety):**
   a. **L1 Before print.** For each of the eight gold keys in the addendum section 2: `head-object` (VersionId, ETag, LastModified) and the sha256 of the body; equal to the addendum's prior VersionIds and 12-hex sha prefixes, else STOP (a prior version moved: report which). The eight SERVED keys `platinum/mdpf/<scope>/<type>.json` in bucket `opal-data-portal-v2` (the publisher's `SERVE_BUCKET` and `SERVE_ROOT`; read them from the deployed source, never typed): VersionId, ETag, sha256 of each (the rollback copy for the served plane). The mutable pointer `platinum/mdpf/_manifests/latest.json` VersionId. The publisher function's `CodeSha256`, `LastModified` and its EventBridge Scheduler schedule's target input verbatim. The 8 other served-plane objects' VersionIds you will NOT change are the control: print the whole served listing denominator for `platinum/mdpf/` with VersionIds (compare at L5).
   b. **L2 Build and verify (read-only).** `python org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round9/checks/build_publish_bodies.py --from-s3 --out <scratch dir outside the repository>`. It must print `OK` for four scopes and `BUILT: 8 bodies ...`; exit 0. Then `python .../r9_trend_groups_readback.py read --dir <that dir>`: ten of eleven arms PASS and the only FAIL is R9 (the run-manifest arm has no manifest tonight). `PUBLISH_PLAN.json` in the dir lists each key, its existing VersionId (must equal L1) and the new sha256. Any other output: STOP, report, put nothing.
   c. **L3 The eight puts.** For each of the eight objects, `put_object` to its existing gold key with the built body and `ContentType` `application/json` (nothing else: no metadata, no ACL, no tagging beyond what the bucket default does). Category-views first, then the timeseries, Global last. After EACH put read the key back: sha256 equals the built body's; record the new VersionId. If a put or read-back fails, STOP at once and run the rollback for every key already written (section 4); never retry a put with a different body.
   d. **L4 The publisher, ONCE.** Invoke `opal-assets-mdpf-portal-publisher` once with the schedule's recorded input verbatim (print it; add no key). Read the response and the lambda's own log line for each pair: the eight pairs `published`, every other pair `unchanged`; `failed` empty; `all_present` as the response says (print it; do not act on it). Then read the eight served keys: sha256 equals the gold body's (the publisher's own compare), new VersionIds recorded; the 8 control objects and every other served object print the SAME VersionIds as L1 (a changed one: file a BLOCKING row naming the key and stop). `latest.json` moved (expected: the publisher rewrites its own pointer; record the new VersionId).
   e. **L5 Proofs.** (i) `python .../r9_trend_groups_readback.py read` in S3 mode over the gold keys: R1-R8, R10, R11 PASS, R9 FAIL as the run-manifest arm (the newest manifest is the 2026-10-14 13:31Z run, not this act): print all eleven lines. (ii) The served-plane Global timeseries read back and parsed: the four new keys present, `carried_dates` equal to the nine no-total dates, `muni` absent from the served category-views of all four scopes. (iii) The CloudFront view of the served Global timeseries: a GET through the public host with the walker/service account's token is NOT authorised by this order; instead read and print the distribution's cache behaviour for `/api/general/mdpf/*` (TTL, cache policy name) so the issuer knows when a browser sees the new bytes; do NOT invalidate. (iv) The lambda's `CodeSha256`, `MDPF_GOLD_COMMIT` and the publisher's `CodeSha256` are unchanged from L1 (control).
4. **Rollback PER KEY (a copy of the prior version, never a delete):** if L2 refuses nothing was written. If L3, L4 or L5 fails or any control object moved: for each gold key written, `copy-object` of its recorded prior VersionId onto the same key, read back sha256 equal to the recorded prior sha256; then hand-run the publisher once more with the same input (it re-copies the restored gold bodies; read its response) or, for a served key the publisher did not restore, `copy-object` of that served key's recorded prior VersionId. Report which keys were restored and the readback of each. The pair's rollback of the lambda deploy is NOT part of this order.
5. Close the ledger (every leg proven or the reason named; the sentinel committed and closed). Report to `2.0.0_SA_COO~D1` with each leg's output and the ledger path, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the L1 before print of the eight gold keys, the eight served keys, latest.json and the served listing, then build_publish_bodies.py --from-s3 and r9_trend_groups_readback.py read --dir over its output</invocation>
  <expect>the eight prior VersionIds equal the addendum's; the builder prints BUILT with 8 bodies and exit 0; the readback reads ten of eleven arms PASS with R9 the only FAIL (no manifest tonight)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the eight put_object calls and the read-back of each key</invocation>
  <expect>each gold key's body sha256 equals the built body's sha256 in PUBLISH_PLAN.json; each key has a new VersionId; the prior VersionIds still exist</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the one publisher invoke with the schedule's recorded input, then the served-key and listing reads</invocation>
  <expect>the eight pairs published and every other pair unchanged, failed empty; the eight served keys equal their gold bodies by sha256; every other served object's VersionId equals its L1 value</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>r9_trend_groups_readback.py read (S3 mode), the served Global timeseries parsed, the cache behaviour read, the control reads, then python .tools/deploy_ledger.py check</invocation>
  <expect>R1-R8, R10 and R11 PASS (R9 the manifest arm, FAIL by design tonight); the served Global timeseries carries the four keys and no served category-views lists muni; the lambda and publisher code are unchanged; the ledger CLOSED with every leg proven and the sentinel committed and closed</expect>
</criterion>
</proof_of_spec>
</task_order>
