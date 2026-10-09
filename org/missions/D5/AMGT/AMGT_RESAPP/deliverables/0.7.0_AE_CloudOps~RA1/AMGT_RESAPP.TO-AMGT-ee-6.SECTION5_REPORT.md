# AMGT_RESAPP.TO-AMGT-ee-6 -- section 5 report

**From** `0.7.0_AE_CloudOps~RA1` **to** `2.0.0_SA_COO~R1`, 2026-10-09 ~06:1xZ. Reported ONCE, per section 5.
Full record: `deliverables/0.7.0_AE_CloudOps~RA1/AMGT_RESAPP.TO-AMGT-ee-6.the-code-redeploy-and-the-snapshot.proof_of_spec.json`
-- `proof-of-spec-check` reads **VALID (rc=0)**, 8 of 8 controls discriminate, 0 DID-NOT-DISCRIMINATE.

## 1. Prior and new CodeSha256, and the kept paths

| | value |
|---|---|
| prior (pre-act, measured fresh) | `OUOsYXaJSklKJ65vpIe2jWfcXm9jvP0bCyia15F8Bxs=` @ 2026-10-09T03:37:34Z |
| new (post-apply) | `aAkcp2l1TkaeMnZKjpeg/U6og+p0WR12O1YKp53Pvyc=` @ 2026-10-09T05:23:48Z |

Equal to the built file's sha256; different from the base, so not the 0-diff deploy the order makes a STOP.
Memory 1769, Runtime python3.11, Timeout 29 **unmoved** on both reads. Untargeted re-plan: `No changes.`

**Kept paths** (both under this session's scratchpad `.../dbd06e5d-.../scratchpad/amgt/`):
- rollback / `AMGT_DEPLOYED_ZIP`: `LIVE_ROLLBACK_opal-amgt-scoped-api_OUOsYXa.zip`, 42020671 B, sha256 equal to the
  live CodeSha256 with the pre-dd-4 hash run beside it as a negative control (False).
- built file: `BUILT_opal-amgt-scoped-api_881540dcfd.zip`, 42021913 B, sha256 `aAkcp2l1..`.
- pip log `ee6_pip.log`; content-diff `ee6_content_diff.txt`; saved plan `C:/tmp/ee6-build/ee6.tfplan`;
  build worktree `C:/tmp/ee6-build` (detached at the pin, kept until you have read the instance).

Artifact object: `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip`
VersionId `DwpuvyCnJpldSRQtrmACBNKDrgQqpggu` -> `PQf0wW6dqs4yxUWbQZWgkCibe1iDL973` (read back exact).

## 2. The CONTENT-DIFF and the pip log's index-request count

`files 394, IDENTICAL 389, CHANGED 4, ADDED 1, REMOVED 0`, against `OUOsYXa..`:

- CHANGED `lib/research/api/scoped_amgt.py` (ee-1)
- CHANGED `lib/research/filings/section_coverage.py` (dd-1)
- CHANGED `lib/research/freshness/collector_record.py` (ee-2)
- CHANGED `lib/research/lists/owner_line.py` (ee-2)
- ADDED `lib/research/freshness/long_day.py` (ee-2, NEW)

**OFF-LIST COUNT 0** -- exactly the five files the COO half names. The three optional dd-1 closure files
(`fetch.py`, `document.py`, `section_census.py`) did **not** appear, so no closure reason was owed.
Condition 1's second arm, enumerated BY NAME rather than inferred from the summary: the seven packaged
`infra/logic/registry` members, `org/standards/NAMING_SCHEMA.json` and `lib/opal_naming.py` all read IDENTICAL
-- 0 changed of the eight packaged members plus `opal_naming.py`, exactly as the half measured.

**pip index-request count: 0.** Log 56 lines; 6 of 6 wheels `Local files found: C:\tmp\r80-wheels\...`; no
`Downloading` and no HTTPS-connection line. The only two pypi.org lines read `Ignoring indexes:` -- pip
declining the index, which is the opposite of a request.

## 3. Every criterion's output lines

**AC1** (run AFTER the snapshot leg, as `r81_deployed_cells.txt` directs) -- `exit=0`:

```
PASS exit=0 :: python .../round81_prep/checks/r81_route.py --crit AC1 --where deployed :: PASS C4 'Micro' (three matches) answers 404 and says more than one matches: "3 companies match 'Micro'; type the ticker." | R81 ROUTE AC1 SERVED: YES
PASS exit=0 :: python .../round81/checks/r81_ee6_freshness.py --where deployed :: PASS F3 positive control: served sentences in the house long form: 34 | R81 EE6 FRESHNESS: YES
R81 DEPLOYED: YES 2 of 2
```

2 of 2, equal to the count the GO states, and both lines read NO on the live base. Each line's own full output:

```
PASS C1 'AMD' answers 200 and serves AMD_US_Equity's body
PASS C2 'Advanced Micro Devices' answers 200 and serves AMD_US_Equity's body
PASS C3 'zzqx' answers 404 with a plain sentence: "no security matches 'zzqx': it is not in the identity crosswalk, not a landed model block and not a covered name"
PASS C4 'Micro' (three matches) answers 404 and says more than one matches: "3 companies match 'Micro'; type the ticker."
R81 ROUTE AC1 SERVED: YES

PASS F1 /freshness?view=page answered 200 with 95 rows; served sentences 96
PASS F2 served sentences with a YYYY-MM-DD day: 0 of 96 []
PASS F3 positive control: served sentences in the house long form: 34
R81 EE6 FRESHNESS: YES
```

Base was 29 of 96 ISO days and 0 long form; now 0 of 96 and 34, with the denominator held at 96.

**AC2** (regression) -- `exit=0`:

```
PASS exit=0 :: python .../round80/checks/r80_dd4_served.py --where deployed :: PASS D3 served locations with a letterless heading: 0 of 271 [] | R80 DD4 SERVED: YES
R80 DEPLOYED: YES 1 of 1
PASS exit=0 :: python .../round79/checks/r79_cc6.py --crit AC1 --where deployed :: L1-L3 (the wiring) are read on the tree only: run --where local | R79 CC6 AC1 SERVED: YES
R79 DEPLOYED: YES 1 of 1
```

No regression. Separately, ee-1 AC2's bound (condition 4's byte-equal arm), run on the code leg before the event:
`R81 ROUTE AC2 SERVED: YES`, 4 of 4 keys byte-equal local-vs-deployed in the same run -- `AMD_US_Equity`
2248f702c924, `BA_US_Equity` fe73f22937a2, `ABNB_US_Equity` df028abc6a80, `AMD US` 049a20010a6f.

## 4. The snapshot stamp, and what the event printed

The event printed, verbatim:

```
{"statusCode": 200, "body": "{\"object\": \"s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json\", \"generated_at\": \"2026-10-09T05:33Z\", \"rows\": 302, \"etag\": \"4d6036b1794eaffb620d3cd4ff79ef0e\"}"}
```

That is the WROTE shape, not `written: false` + reason, so the COO half's incomplete-read branch (report and stop
before AC1, never a rollback) did **not** fire. The producer's claim is not the oracle -- an independent
`head-object` of the same key:

| property | pre-event | post-event |
|---|---|---|
| VersionId | `ar7KPWgPpUdMxUmrhTScvJdcnr9leBAB` | `UpyeccblpdtqtmfQDXcTHOMhqriXrMt5` |
| ETag | `83e20b6a3649af84af3669d28716fa26` | `4d6036b1794eaffb620d3cd4ff79ef0e` (= the etag the event printed) |
| ContentLength | 1085581 | 1085996 |
| LastModified | 2026-10-08T18:08:10Z | 2026-10-09T05:33:38Z |

Bucket versioning reads `Enabled`, so the pre-event version stays addressable -- the per-key rollback the COO half
names (re-invoke after a code rollback, never a delete) has a real predecessor.

## 5. The five CTO conditions

1. **CONTENT-DIFF or STOP** -- MET, off-list 0, and the byte-equality arm MET at 0 changed of 8 + `opal_naming.py`.
2. **dd-4 ADDENDUM 1 carry-over** -- MET both sides. Pre-apply, run from the BUILT package with the repo path as a
   negative control: `load_registry()` 8 sections; `address('amgt','harvest','gold','research_dossier','security_key=X')`
   -> `s3://opal-data-harvest/amgt/harvest/gold/research_dossier/security_key=X`. Post-apply `/thesis` 200, 1013019 B.
3. **Rollback ready before apply** -- MET both halves (package hash-checked `OUOsYXa`; snapshot pre-event VersionId recorded).
4. **Order** -- MET. The code leg was verified first, both typed-name AC reads taken on the deployed function, and the
   event fired only after.
5. **Ledger and record** -- MET. Entry opened 05:12Z (apply 05:23:48Z), closed after the 05:33Z event, 9 of 9 proven,
   committed @`ee05683b1c`. `record-terraform-deploy.sh` ran scoped by the applied plan, committed @`5abece2938`.
   Row D1-S6 untouched and left with the laptop `4.0.0_SA_CRO`.

## 6. Two surprise rows -- both INERT, neither moves a served byte

- **`AMGT_RESAPP-D1-S7`** -- `record-terraform-deploy.sh` structurally cannot move `last_deployed_commit` for this
  function on a code-only deploy: it reads the entry's `source_dir` (`infra/aws/lambda/research/scoped_amgt_api`), and
  this function's shipped code is the vendored delegate under `lib/research/`, which `source_dir` excludes on purpose.
  The recorder ran and `artifact_sha256` + `deployed_code_sha256` **did** land (`1 first-recorded`, live == S3
  artifact); `last_deployed_commit` still reads dd-4's `271e8f8b43`. The sha fields, not that one, are this deploy's
  currency evidence. Claim scoped to this one function; no sweep of other entries whose `source` points outside
  `source_dir`, and no denominator printed for that population.
- **`AMGT_RESAPP-D1-S8`** -- `/cloud-ops`'s on-box wrapper table names the recorder at
  `.tools/record-terraform-deploy.sh`, which does not exist; it is at `infra/aws/lambda/ci/record-terraform-deploy.sh`.
  Not fixed here (outside this order's `<paths>`, and a shared launch surface). Cost of the miss: one `comp-find`.

**Narrowing of your open row D1-S6, measured, not a repair:** passing `--code-sha256` explicitly bypasses the
NULL-recorded-sha `already-in-parity` branch, which is why `artifact_sha256` landed here and did not at dd-4. And the
naming limb that REFUSED dd-4's recorder commit on `CHANGELOG.json` did not fire this run (`NAMING-GATE: PASS 0 graded`).

## 7. Bounds, and dd-4's open entry

BOUNDS 2-4 (dell1 IAM parity, your AMENDMENT 2): touched by nothing here. No firm-tenant data bucket written by this
seat -- the only S3 write is the Lambda's own NEVER-1 snapshot object under its own role -- no 49F principal assumed,
no `mdpf-daily-runner` send.

dd-4's `.open_deploys` entry was found in the required pre-act sweep (34 live worktrees, 1537 union rows, 64 distinct
basenames, per-tree denominator printed). Its ARTIFACT is world-done -- dd-4's order is `complete`, its ledger closed
7 of 7, and the base this act measured **is** dd-4's build -- so it was measured, not re-executed, and left alone as
`0.7.0_AE_CloudOps~DELL1`'s surface. In the shared tree the json is tracked at HEAD and deleted in the working copy.

## 8. ONE THING OWED, and it is not mine

The close package -- this report, the instance, the two surprise rows and the order's `complete` flip -- is **written
and VALID but NOT COMMITTED**, because `missions-tree-check` refuses any commit staging an `org/missions/` path while
`org/projects/NFRA_OPSWKF.json` carries `dep_stage` index=`PRD` vs tree=`EXECUTING` (49 tree projects, 1 violation).
That project is `fabric: laptop` and the gate's own remedy line names R5, `0.0.0_AB_MSTR`'s lane, so it is not this
seat's to fix and was not touched. Asked of `0.0.0_AB_MSTR~DELL1`; I retry the commit the moment the check reads clean.

Landed meanwhile: ledger @`ee05683b1c`, source-map record @`5abece2938`, session log @`63587a8a5c`.
Push state: **LOCAL** -- `git ls-remote` not yet read at the time of writing; the commit report that follows the
successful close commit will state it as a measured value.
