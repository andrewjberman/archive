# NEVER-WIDEN SIGNOFF PACKET -- IRPT_BCKEND IB-pr-518 (round 184, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-518 (issued by 2.0.0_SA_COO~P2, CTO round-184 analysis msg 7233). Worker: 0.9.0_WK_IRPT_BCKEND~367.
Scope: census and rebuild of `irpt-ycharts-generate` against its CURRENT live bytes, with the comparison-catalogue release
of IB-pr-517 (merged @0d0e9e1229). BUILD ONLY. Nothing was uploaded, applied, deployed, invoked or signed in. The source-map
edit was made in the scratch worktree only and was reverted.

Base commit (worker HEAD before the first commit): 0c0ae5a8f5cee99e9c7fa49b8043c146fed1d05e. Pin commit (IB-pr-517 merge):
0d0e9e1229c099817988758bce973b06a6a969a2, confirmed an ancestor of the base.

## The served change, in words

The comparison catalogue served by `GET /api/scoped/investor-reporting/analysis/comparisons` lists a fifth Opal model,
Opal Ultra Short-Term, keyed by Opal's own model identity (key `opal_ultra_short_term`, vendor id `UST`, namespace `OPAL`,
no YCharts id), in the canonical order: Opal Ultra Short-Term, Opal Short-Term, Opal Intermediate-Term, Opal Long-Term,
Opal Ultra Long-Term. The Analysis Request form lists the model entries of the served catalogue, so the fifth model appears
there without any portal change.

The four existing entries keep their key and label, but their served ORDER changes: Opal Long-Term moves from first place to fourth place (the canonical order), and the Analysis Request form renders served order, so the form's model checkboxes reorder for every firm.

Permission is UNCHANGED: the same three permitted firms and the same three principal classes. No figure moves. No route,
IAM grant, schedule or cache surface is touched.

Measured in the offline arms (synthetic, in memory from the extracted zip bytes, no invoke): the built zip serves the five
model labels in the canonical order (five_in_order); the four existing entries keep key and label (equal to live);
the new entry is admitted for each of the three permitted firms under FIRM_ADVISOR (15 of 15 firm-entry pairs); an altered
copy of the new entry (candidate name changed) is refused with MaintainedSourceUnauthorized.

## Live and built sha256

- Live (CodeSha256, base64 of the zip sha256, read 2026-10-13, LastModified 2026-10-13T13:01:13Z): hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg=
  (hex 86935f9212ed2d19747bd4c52fe55daf9922959d56f1b37718a3219739955e08). Equal to the source map artifact_sha256 and to the
  bytes downloaded to scratch. 104 members.
- Built (BUILD_ONLY, packed twice, byte-identical): hex c4fe3b3500e764d67c2ee8b55d0294c54b533136ac47c0a3fc0d6c4274436586
  (base64 xP47NQDnZNZ8Lui1XQKUxUtTMTasR8Cj/A1sQnRDZYY=). 104 members.
- Member-level: 102 members identical to live, 2 changed (below). Signature instrument: 0 signature mismatches on the built
  zip and 0 on the live zip; 0 attribute mismatches on either.

## The two changed members

Exactly two members differ from live: `templates.json` (native, `infra/aws/lambda/investor-reporting/ycharts/generate/templates.json`)
and `maintained_sources.py` (staged, `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py`). Each built member's
sha256 equals the repo blob's sha256 at the pin 0d0e9e1229:
- maintained_sources.py: 74c262b6db6d9d6c8c76b3668cad8d900f2977abe68325430836f26843ea2116 (built and repo blob, equal)
- templates.json: 87be046cf2bd0390a703d37be9e82a9037a3d867423e52e64a3db6415fe4728b (built and repo blob, equal)

`recipe.py` is NOT moved: the built recipe.py equals the live one, because the source map pins it to its live bytes.

## Source-map row diff (NOT committed by this order)

One `staged_from` row of `irpt-ycharts-generate`, two fields (diff saved as IB184-1_source_map_row_diff.txt in this folder):
`pin` 0642c9d00454a852068acdee3b1b9ccd8e6ddba2 -> 0d0e9e1229c099817988758bce973b06a6a969a2, and `sha256`
29c35dbfba72ca031a7d172d74f401b5976ef383d5fc4ef5deaa3a21ab2d1587 -> 74c262b6db6d9d6c8c76b3668cad8d900f2977abe68325430836f26843ea2116.
The apply seat commits this row together with the release, and updates artifact_sha256, deployed_code_sha256 and
last_deployed_* from the applied artifact. The source map in this worktree was restored: sha256 before equals sha256 after
(0cca8a75bff87c6130e9dd66bbd5109ed94b3d92150e77689513b5870de63c2f).

## Open ledgers and sequencing

Ledgers naming the function (56 change-management ledgers and the source map's own deploy ledger): all CLOSED on the base commit.
Open markers naming the function: three, at the HEAD of three worktrees (C:/dev/mstr-dell2-merge-0240 and C:/dev/mstr-dell2-merge-0805:
irpt-ycg-release1-20261007.json; C:/dev/rel-resident-r5: tckt-vnext-r2-tr1-fwd1-thread-rerun-run3-20261011.json). Their trunk
ledgers are CLOSED. These markers are stale views, not open deploys (CLAUDE.md section 5): the apply waits on their owners
closing them SUPERSEDED, and this worker closed nothing. Denominators: 1854 ledger files read, 50 of 52 worktrees read,
732 marker files read. The full list is in IB184-1_arms_and_ledgers.json.

## Branch A -- land digest-gated (never a mint)

1. Rebuild with the release source map and compare the rebuilt zip's sha256 with the signed built digest c4fe3b35...6586
   (base64 xP47NQDnZNZ8Lui1XQKUxUtTMTasR8Cj/A1sQnRDZYY=). On any difference ABORT.
2. Upload the built zip under its digest to opal-313476888478-lambda-artifacts (the build script, not this packet).
3. Terraform path `infra/aws/terraform/investor-reporting/ycharts/generate.tf`, module `irpt_ycharts_generate`: the change is
   `s3_object_version` and `source_code_hash` only. Plan to a planfile showing 1 change and 0 to destroy.
4. `bash .tools/safe-apply.sh` on that planfile.
5. Gates before the apply: both halves signed at the packet bytes; the ledgers above CLOSED (the three stale markers closed
   SUPERSEDED by their owners); the live CodeSha256 equal to the start value hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg=.

## Branch B -- restore the live version (rollback)

The live version is restored by pointing the function at the S3 object version whose content equals the live zip. Measured
now (read only): version ennO07toFOYlPWM64JC4MS9g.bVRr7fW of investor-reporting/irpt-ycharts-generate.zip in
opal-313476888478-lambda-artifacts (IsLatest, LastModified 2026-10-13T12:57:53Z, ContentLength 621567, content-sha256 metadata
equal to the live CodeSha256). It is re-named and re-read at the apply BEFORE any upload. Rollback per key: the function's
`s3_object_version` back to that id, `source_code_hash` back to the live value, and the source-map row reverted to the pin
0642c9d00454a852068acdee3b1b9ccd8e6ddba2 and sha256 29c35dbfba72ca031a7d172d74f401b5976ef383d5fc4ef5deaa3a21ab2d1587.

## Red list

`deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` names two target prefixes:
`infra/aws/lambda/investor-reporting/_contracts/` and `docs/contracts/investor-reporting/`. Neither changed member lies under
either prefix. changed_paths_touching_a_target is empty; the list's stop flag is false.

## Consumers (one read-through each)

- Portal Analysis Request form, `portal/src/pages/TicketCenter/TicketCenter.tsx` line 287: the models are the served entries
  with name_source model_catalogue. The fifth entry appears with no code change.
- `portal/src/pages/TicketCenter/AnalysisRequestParts.tsx` lines 112-121: each model is a checkbox in served order, labelled by
  comparisonLabel. The fifth entry renders in the canonical order.
- Catalogue route, `infra/aws/lambda/investor-reporting/ycharts/generate/entry.py` lines 150-166: the route key is unchanged; the
  read calls build_catalogue(tenant=ctx.tenant). No change of route.

## Other functions that stage maintained_sources.py

Eight functions stage `_scope/maintained_sources.py` in the source map. Seven others are NOT moved and keep their own pins:
irpt-performance-adapter, irpt-directory-search, irpt-narrative, irpt-export-render, irpt-holdings, irpt-status,
irpt-49f-reporting-read-lambda. Measured pins across the eight: five distinct commits and two distinct sha256 values (the
prior note said four pins; the source map says five). They do not serve this catalogue and keep the old copy: this release
gives them no new behaviour.

## Three conditions

(i) `recipe.py` is NOT moved. The OPAL-namespace refusal in the repo's recipe.py therefore does not ship with this release.
The YCharts path stays stopped; if it were re-enabled it would fail closed on a missing security_id. That refusal rides with
recipe.py's own release, together with the other cells' pending changes in that file.

(ii) The four custody tests that fail at BASE (test_custody_entry.py two, test_custody_retained.py two; row IRPT_BCKEND-D2-S150)
are pre-existing and are not this release's gate.

(iii) The after-read the CTO set: after the apply, the served catalogue lists Opal Ultra Short-Term in the canonical order and
the Analysis Request form shows it. This is a person's read on DEV; no seat can sign in to make it.

(iv) Measured order condition, from the offline arms: the four existing entries keep key and label, but Opal Long-Term moves.
The live served order is Long, Short, Intermediate, Ultra Long; the built order is Short, Intermediate, Long, Ultra Long, which
is the canonical order the five-model arm requires. The CTO rules which order governs. This is recorded as surprise row
IRPT_BCKEND-D2-W367-S1.

## The pair (both UNSIGNED)

- COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at the packet bytes.
- CTO half: 1.0.0_SA_CTO~DELL2 -- UNSIGNED at the packet bytes.

Both halves are signed at these packet bytes before Branch A may run.
