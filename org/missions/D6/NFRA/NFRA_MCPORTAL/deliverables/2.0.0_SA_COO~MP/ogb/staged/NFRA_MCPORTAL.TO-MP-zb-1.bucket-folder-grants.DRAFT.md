# NFRA_MCPORTAL task order -- `MP-zb-1` -- WORKSTREAM OGB ROUND 1: the People panel grants a bucket or a folder per person (FWD-30)   [DRAFT: held, not cut]

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D6/NFRA/NFRA_MCPORTAL/decompositions/NFRA_MCPORTAL_DECOMP.md</decomp_doc>
<owned_cells>MP-zb-1</owned_cells>
</decomp_ref>
<to_id>NFRA_MCPORTAL.TO-MP-zb-1</to_id>
<issued_to>0.9.0_WK_NFRA_MCPORTAL~47</issued_to>
<issued_by>2.0.0_SA_COO~MP</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a front-end bundle; no cadence.
comp-iam: DECLARED-NOT-APPLICABLE -- a front-end bundle; no IAM.
comp-adversary: DECLARED-NOT-APPLICABLE -- the tests plant the contrary (an off or a restore must carry no confirm; an unconfirmed add must send nothing) as their own adversary arm.
EGRESS CLASS, declared: none. Make no network call (the tests mock fetch).
</preflight>

## 1. THE CELL -- `MP-zb-1` (workstream OGB round 1, decomposition section OGB1.1)

You have two worktrees, nested: the workspace worktree `C:/tmp/mp-ogb-47` (branch `wk-NFRA_MCPORTAL-47`) and, inside it, the mcportal worktree `C:/tmp/mp-ogb-47/mcportal` (branch `wk-NFRA_MCPORTAL-47-mcportal`), based on the mcportal commit the issuer names in the GO. `node_modules` is linked. Do not run `bun install` or `bun add`. Begin each shell call with `cd C:/tmp/mp-ogb-47 &&`. Commit code in the mcportal worktree with plain `git commit`, author `0.9.0_WK_NFRA_MCPORTAL~47 <0.9.0_WK_NFRA_MCPORTAL~47@opal.agent>`. Your proof-of-spec instance and any surprise row are committed in the workspace worktree via `.tools/safe-commit.sh --author "0.9.0_WK_NFRA_MCPORTAL~47 <0.9.0_WK_NFRA_MCPORTAL~47@opal.agent>" -F <msgfile> -- <paths>` (message file written with a non-shell writer). Never push either repo. Make NO network call of any kind. There is NO DOM under `bun test` here (bun 1.3.x has no `document`): test pure functions and server-rendered markup only; do not try to mount a component.

**What is wanted.** Andrew: "The entitlement layer is for accessing whole buckets, accessing buckets or maybe accessing various folders within those buckets." On `/opalgateway`, for the picked person, the owner switches a whole bucket, or a folder inside one, on or off in one act. The grant shape is RULED and needs no writer change: a grant is the string `bucket` or `bucket/prefix` in the person's `channels_allow`; `channels_deny` subtracts, and deny wins (the gateway reads it; the page only writes the strings). The writer accepts up to 64 strings of 128 characters per list. Any ADD to `channels_allow` is a WIDENING: the writer refuses it unless the event carries `widening_confirm: true`, which the owner's confirm sets. Subtracting (adding to `channels_deny`) and restoring (removing from `channels_deny`) never carry a confirm.

Build (in `mcportal/src/pages/opalgateway/` and `mcportal/src/pages/people/personAccess.ts`, plus the one small edit named):
1. **The list.** In the picked person's section on `/opalgateway`, a section `Buckets and folders`: one row per bucket (the channels of kind `bucket` that `getGatewayBreakdown` returns, read once with the page's other reads) and one row per `bucket/prefix` string already in the person's `channels_allow`; each row has a switch. A switch reads ON when its string is in `channels_allow` and NOT in `channels_deny`; OFF otherwise. A stopped person's switches read off and disabled as the existing `stoppedReadsOff` already does for tools and channels.
2. **Pure rules** (one exported function each in `personAccess.ts`, no component state): `grantOnChange(record, grant)` returns the change that adds `grant` to `channels_allow` (and removes it from `channels_deny` if present) and says it is a WIDENING; `grantOffChange(record, grant)` returns the change that adds `grant` to `channels_deny` and leaves `channels_allow` untouched; `grantRestoreChange(record, grant)` returns the change that removes `grant` from `channels_deny`. An `Add a folder` control takes a bucket (from the list) and a prefix (free text, trimmed, no leading or trailing slash, no `..`, at most 128 characters in total) and builds `bucket/prefix`; a bad prefix sends nothing and says why.
3. **The confirm.** Turning a switch ON for a grant not yet allowed shows the WIDENING label and a Confirm step before anything is sent; only the Confirm click sends the POST, with `widening_confirm: true` as one more key beside `change` and `expect_revision`. `src/api/admin.ts` gains that OPTIONAL boolean on the POST body and on nothing else (no other edit of that file). An off or a restore sends no `widening_confirm` key at all.
4. **THREE tests**, each by its exact name, as the literal first argument of its `test(...)` (bun 1.3.x prints a name only on FAILURE, so the check reads the names from your sources; synthetic fixtures only; in `src/pages/opalgateway/` or a sibling test file there):
   - `turning a bucket or folder on adds its string to channels_allow and needs the owner's WIDENING confirm before it is sent`
   - `turning a bucket or folder off adds it to channels_deny, restoring removes it, and channels_allow is never edited by either`
   - `widening_confirm rides only on the one confirmed add and never on an off or a restore`
All existing tests keep their names and pass (the 91 of mcportal a577f99 included). `bun test src` now reads 94 or more pass and 0 fail.

## 2. BOUNDS

1. Write surface: exactly the paths in section 3. No gateway (Python) file, no Lambda, no Terraform, no `package.json` or `bun.lock`, no deploy, no network call.
2. Do NOT flip this order's `<status>`: the order file is outside your `<paths>` and the issuer flips it.
3. If a criterion cannot be met without a file outside section 3, REFUSE it with what you measured and file a BLOCKING row. Never repair a criterion; the check scripts and the proof line are the issuer's.
4. Standing rules: no push and no vendor call; commit as above, each with your serial as author. Do not print a real name, email or account.

## 3. SURFACES

<paths>
mcportal/src/pages/opalgateway/
mcportal/src/pages/people/personAccess.ts
mcportal/src/pages/people/PersonAccessPanel.tsx
mcportal/src/pages/people/PersonAccessView.tsx
mcportal/src/api/admin.ts
org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~47/**
org/missions/D6/NFRA/NFRA_MCPORTAL/surprise-channel/investigations/**
</paths>

Read, never write: every other mcportal file, `C:/Users/Opal Bloomberg/Desktop/ajb_workspace/portal/DESIGN.md` (the colour law: use the page's existing classes; no new colours), and `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/ogb/checks/`.

Rows go to `org/missions/D6/NFRA/NFRA_MCPORTAL/surprise-channel/investigations/INVESTIGATION_v1.Z.md`, id `NFRA_MCPORTAL-Z-W47-S<k>` (k from 1). APPEND ONLY: add your row after the last one and leave every earlier byte untouched (the file carries some Windows line endings; do not rewrite or normalise them). `surfaced_at` = `date -u +%FT%TZ`. `disarm_owner` on an ARMED row is `2.0.0_SA_COO~MP`.

## 4. PROOF OF SPEC (literal; run after your commits)

<proof_of_spec>
  <criterion id="AC1" cell_refs="MP-zb-1"><invocation>cd C:/tmp/mp-ogb-47 && bash org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/ogb/checks/zb1.AC1.sh; echo "exit=$?"</invocation><expect>(?s)named tests present in sources 3 of 3.*fail=0.*RESULT: PASS.*exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="MP-zb-1"><invocation>cd C:/tmp/mp-ogb-47 && bash org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/ogb/checks/zb1.AC2.sh; echo "exit=$?"</invocation><expect>(?s)tsc rc=0.*RESULT: PASS.*exit=0</expect></criterion>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Write the instance at `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~47/NFRA_MCPORTAL.TO-MP-zb-1.bucket-folder-grants.proof_of_spec.json`, run `proof-of-spec-check.py` on it as the worker rules say, and report once, with: the output of AC1 and AC2; the mcportal commit hash or hashes and the workspace commit hash; every existing assertion you changed (file, test, old, new), or none; `bun run build` in the nested worktree (rc); any row.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES (DRAFT):** drafted 2026-10-21 ~16:0xZ at the CVO's word ("draft your FWD-30 cell now; cut it when COO~O's FWD-24 reading is live"), from PRD v0.11 FWD-30 and the CTO's shape ruling. HELD OUTSIDE `task-orders/` until the cut. Gates before the cut: (1) `2.0.0_SA_COO~O`'s FWD-24 gateway reading of `channels_allow` folder strings is live, with the `widening_confirm` carry (first release target 2026-10-23T06:00Z); (2) NFRA_OPLGTW's no-bronze cure (v3.19 @788a27f4ee) is landed. At the cut: fill the mcportal base commit in the GO, move this file to `task-orders/` as `<status>pending</status>` with the DRAFT mark and the held-note removed, provision slot ~47 with a nested mcportal worktree, dry-run `zb1.AC1.sh` (must FAIL at base: names 0 of 3) and `zb1.AC2.sh`, generate the face-only extract (`face_extract.py`), spawn the worker with the extract. Not decided and stated for the CTO: the draft shows only bucket-kind channels and `bucket/prefix` strings; a plain channel id already in `channels_allow` is not given a row. The folder list is typed (no route enumerates prefixes). The close run is `MP-zb-2` (decomposition OGB1.2), after the bundle release.

<status>held</status>
<round>1</round>
<workstream>OGB</workstream>
<slot>~47</slot>
<fabric>site-z</fabric>
<risk>LOCAL</risk>
<worker_class>worker</worker_class>
