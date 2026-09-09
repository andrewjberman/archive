# CG-s-26 -- THE LOCAL STITCH STORE RETIRED

**Cell:** `CG-s-26` (PRD v0.6 s.7 row S26, CTO round-5 analysis @`30027295be`) ·
**TO:** `NFRA_CLDGRPH.TO-CG-F-6` · **Assignee:** `0.9.0_WK_NFRA_CLDGRPH~7`
(re-addressed from slot ~2 at 22:3xZ) · **Branch:** `wk-cldgrph-6-7` ·
**Worktree:** `C:/tmp/wk-cldgrph-6-7` · **Push state:** LOCAL.

**TERMINAL STATUS: OPEN.** Four of six criteria PASS by output, one is a judgment
act with no verdict, and **F6-AC3 and F6-AC5 read FAIL** -- both for reasons that
are recorded as rows and neither of which is the retirement itself. The WORK is
done and verified: the store, its manifest and the local scratch are archived to
S3 with S3-computed checksums equal to their pre-upload hashes, deleted from this
device behind a re-read guard, the builder is retired by `git rm`, and the
tombstone carries every field. The order stays open because a criterion that
reads FAIL leaves it open, and a VALID instance is not a met order.

---

## 1. THE ARTIFACTS -- before, archived, after

### 1a. BEFORE (f6_before.txt, 2026-09-09T22:49:01Z, nothing moved yet)

```json
{
  "read_by": "stat + sha256sum on ABSOLUTE paths in the MAIN workspace",
  "engine_opened": "NONE -- kuzu.Database CREATES an absent store, so no engine is imported anywhere in this order",
  "artifacts": [
    {
      "path": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db",
      "size_bytes": 9170944,
      "mtime_local": "2026-08-27 02:32:00.480352200 -0400",
      "sha256": "c6045d905b329e6d3038983bd6f1b78960e66153be928f27bec286415e275547",
      "claim": "measured"
    },
    {
      "path": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db._build_manifest.json",
      "size_bytes": 439,
      "mtime_local": "2026-09-09 12:33:22.527091400 -0400",
      "sha256": "a497adef7ec5b3afe3c6a30f873825232b2062aabbc6c037e9d12f400f844f87",
      "claim": "measured"
    },
    {
      "path": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/stitch_graph.json",
      "size_bytes": 25489187,
      "mtime_local": "2026-07-25 14:44:34.808710200 -0400",
      "sha256": "7ac11d015e0ce4a068d6afb86cd51edddb8171b227afd5fc9e40ffb8d5dd5363",
      "claim": "measured"
    }
  ],
  "fourth_name_checked_so_its_absence_is_measured": {
    "path": ".../kuzu_stitch_db.wal",
    "state": "ABSENT",
    "why_checked": "infra/aws/globgrph/.gitignore:6 carries it; an unchecked ignore entry is an unmeasured file"
  },
  "archive_prefix_before_upload": "archive/NFRA_CLDGRPH.CG-s-26/ -- list-objects-v2 returned NO Contents key (rc 0). The four objects below are a DELTA, not a coincidence.",
  "builder_at_head": {
    "path": "infra/aws/globgrph/kuzu_stitch_load.py",
    "last_commit": "8a074ba7ba488b4b930ed1569ceda695cf7e000d",
    "bytes_at_head": 6309,
    "blob_sha1": "a36198ad349dd3d9ee044ac12fa06d854f3d3c8c"
  }
}
```

**The face said 7,934 B for the builder; it measures 6,309 B at this HEAD.** CG-s-27
(`TO-CG-F-7`, slot ~3) moved its manifest call onto `_provenance.write_manifest`'s
claim kwargs and its local `_stamp_claim` helper went with it. The order anticipated
exactly this ("whatever it reads at your HEAD, it is RETIRED whole") so it is a
figure to record, not a divergence to file: the file is retired whole either way.

### 1b. ARCHIVED (f6_archive.txt, 22:50:30Z-22:50:49Z -- four PutObject acts, nothing else)

```json
{
  "bucket": "opal-313476888478-globgrph",
  "prefix": "archive/NFRA_CLDGRPH.CG-s-26/",
  "method": "put-object --checksum-algorithm SHA256, then head-object --checksum-mode ENABLED. The comparison is S3-COMPUTED-OVER-RECEIVED-BYTES against the local sha256 taken BEFORE the upload -- never local-vs-local, which agrees even when nothing was sent.",
  "objects": [
    {
      "key": "archive/NFRA_CLDGRPH.CG-s-26/kuzu_stitch_db",
      "size_bytes": 9170944,
      "sha256_hex": "c6045d905b329e6d3038983bd6f1b78960e66153be928f27bec286415e275547",
      "s3_ChecksumSHA256": "xgRdkFsynm0wOJg71vG3iWDmYVO+ko8nvsKGQV4nVUc=",
      "etag": "ccd41e28042b608ea7da90e080c23ac2",
      "sha256_equal": true
    },
    {
      "key": "archive/NFRA_CLDGRPH.CG-s-26/kuzu_stitch_db._build_manifest.json",
      "size_bytes": 439,
      "sha256_hex": "a497adef7ec5b3afe3c6a30f873825232b2062aabbc6c037e9d12f400f844f87",
      "s3_ChecksumSHA256": "pJet737Fs6/jxqMPhzglIysgYqq7xsA36dEvQA+ET4c=",
      "etag": "4c2b97a5b9fabd565f631161974e613a",
      "sha256_equal": true
    },
    {
      "key": "archive/NFRA_CLDGRPH.CG-s-26/stitch_graph.json",
      "size_bytes": 25489187,
      "sha256_hex": "7ac11d015e0ce4a068d6afb86cd51edddb8171b227afd5fc9e40ffb8d5dd5363",
      "s3_ChecksumSHA256": "esEdAV4M5KBo1q+4bNUe3duBcbInr9X8nkD/uNXdU2M=",
      "etag": "74757982ff67cc280a069beda97dedc6",
      "sha256_equal": true
    },
    {
      "key": "archive/NFRA_CLDGRPH.CG-s-26/ARCHIVE_MANIFEST.json",
      "size_bytes": 4623,
      "sha256_hex": "be789d5f5bd8fcc3c3973104ce31e3209a2e8b80668d6129b2f3485294fa1407",
      "s3_ChecksumSHA256": "vnidX1vY/MPDlzEEzjHjIJoui4BmjWEpsvNIUpT6FAc=",
      "etag": "8cd9002b258c7a7262fe4cec63ad96bf",
      "sha256_equal": true,
      "carries": "bytes_vs_manifest, builder_last_hash, sha256 (all three payloads), sizes, mtimes, the build manifest quoted whole, the served source, and the recovery command"
    }
  ],
  "prefix_after_upload": "exactly 4 keys, listed in f6_archive.txt -- nothing else was written to this bucket",
  "roundtrip_control": "ARCHIVE_MANIFEST.json was GOT BACK from S3 and re-hashed at F6-AC2: downloaded sha256 == the tombstone's recorded value, so the object a recoverer downloads is the object that carries the fields"
}
```

### 1c. AFTER (f6_after.txt, 22:58:31Z -- deletion LAST, behind a guard re-read there)

```json
{
  "guard": "for each payload, the expected size and sha256_b64 were read OUT OF THE TOMBSTONE (the tracked artifact a future reader holds) and compared against a FRESH head-object --checksum-mode ENABLED. Not carried from the upload script's memory.",
  "preconditions_checked_in_the_script": {
    "builder_still_in_worktree": false,
    "tombstone_present_before_delete": true
  },
  "guards": {
    "kuzu_stitch_db": "held",
    "kuzu_stitch_db._build_manifest.json": "held",
    "stitch_graph.json": "held"
  },
  "deletions_taken": "3 of 3",
  "after_ls_d": [
    "GONE C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db",
    "GONE C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db._build_manifest.json",
    "GONE C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/stitch_graph.json"
  ],
  "not_touched": "derive_stitch.py, extract_portal_stitch.py (the CLOUD producer's inputs), comp_debt.py (READ only, out of grant), projection_client.py, kuzu_nessie_load.py, kuzu_incremental_refresh.py, kuzu_cli.py, kuzu_db.TOMBSTONE.md, the stale .kuzu_nessie_load lock (a different act's disposition)"
}
```

### 1d. THE BUILDER, RETIRED

```json
{
  "path": "infra/aws/globgrph/kuzu_stitch_load.py",
  "act": "git rm, committed 6abd4a9d9415258d2e432130d965f5255105f730",
  "builder_last_hash": "8a074ba7ba488b4b930ed1569ceda695cf7e000d",
  "bytes_at_that_commit": 6309,
  "blob_sha1": "a36198ad349dd3d9ee044ac12fa06d854f3d3c8c",
  "recover_with": "git show 8a074ba7ba488b4b930ed1569ceda695cf7e000d:infra/aws/globgrph/kuzu_stitch_load.py",
  "why": "kuzu.Database(args.db) at :67 was a WRITE-open on a repo path -- the one-command path back to a second local copy of a graph that is now served. It was the LAST such builder in infra/aws/globgrph/ after TO-CG-F-1 retired kuzu_load.py.",
  "verified_absent": "git show HEAD:<path> -> rc 128 AND test -f -> absent, beside a positive control on the same verb and plane (git show HEAD:infra/aws/globgrph/projection_client.py -> rc 0)"
}
```

### 1e. THE REFUSAL (comp_debt.py:133-137 at this HEAD -- READ, never edited)

```json
{
  "file": "infra/aws/globgrph/comp_debt.py",
  "lines": "133-139 (the raise begins at 132)",
  "read_by_two_instruments": [
    "the source lines printed verbatim with line numbers",
    "an AST read of the SystemExit argument -- the string the tool would actually raise, not a text-local grep three functions away"
  ],
  "text": "REFUSE: the served cloud graph is unreachable (%s: %s).\n  BOTH REACHABILITY scopes are served nessie+stitch on this ONE graph: the\n  AWS-resource scope since NFRA_CLDGRPH R7 (CG-s-8) and the stitch scope\n  (GOLD_SCRIPT, S3_DATA_KEY) since CG-s-24 folded the cloud-produced stitch\n  into the derive. There is no local database to fall back to for either --\n  R7 retired the nessie copy and CG-s-25 stopped reading the stitch store --\n  and this tool will not score against a universe it could not read.",
  "names_served": true,
  "names_stitch": true,
  "names_no_local_database": true,
  "negative_control": "the same AST reader on a mutant refusal that names no source ('REFUSE: the graph is unreachable (%s).') scored FALSE -- REFUSAL_PROBE_CONTROL=FIRED",
  "the_run": "python infra/aws/globgrph/comp_debt.py from this worktree with no store anywhere -> rc 0, a full standing scan against graph vintage 2026-09-09T21:05:17Z. There is no .tools/comp-debt shim (S88), so the module was run directly. The crash C-S33 warned of is the control that DID NOT happen."
}
```

### 1f. WHAT TO READ INSTEAD (measured this tick)

```json
{
  "served_stitch_source": {
    "key": "s3://opal-313476888478-globgrph/stitch/stitch_graph.json",
    "size_bytes": 38845013,
    "last_modified": "2026-09-09T19:55:14Z",
    "etag": "f50001a195ee85434f29645cc42dd971-5"
  },
  "through_the_projection": {
    "invocation": "bash .tools/comp-kuzu \"MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY'] RETURN n.node_type, count(*)\"",
    "vintage": "2026-09-09T21:05:17.968166+00:00, manifest 09be45b5ff92",
    "stitch_source_line": "stitch-codebuild built 2026-09-09T19:55:00Z",
    "GOLD_SCRIPT": 1380,
    "S3_DATA_KEY": 294
  },
  "the_retired_store_for_comparison": {
    "node_count_claim": 3414,
    "edge_count_claim": 5329,
    "edge_count_semantics": "merge_attempts -- an UPPER BOUND on edges present, never a count",
    "built_at": "2026-07-07T15:46:38Z"
  }
}
```

---

## 2. W3-S11 TRAVELS WITH THE BYTES, IN A FIELD

The order required the archive manifest to carry the 51-day gap in a field, not
only in prose. It does, verbatim, and so does the tombstone:

> `"bytes_vs_manifest": "bytes 2026-08-27 newer than built_at 2026-07-07; undescribed by any manifest (W3-S11)"`

The detail field says what that means and refuses the obvious misreading:
`Modify == Change` at `2026-08-27 02:32:00.480` is a CONTENT write on NTFS, and
`kuzu_stitch_load.py` stamped a manifest at the end of every build -- so the write
that produced these bytes **was not a build**. `node_count 3414` and
`edge_count 5329` are claims about the JULY bytes. The capable mutator was
INFERRED as the deleted `kuzu_cost_enrich.py`; no instrument here identified it,
and the field says `"claim": "measured for the timestamps and the sha256; inferred
for the mutator"`. **The archived bytes are UNDESCRIBED and must never be quoted
as a counted graph.** That sentence is in the object in S3, not only in this file.

---

## 3. THE CRITERIA, AS MEASURED

| id | deciding line(s) | verdict |
|---|---|---|
| F6-AC1 | `STITCH_STORE_PRESENT=0 of 3 files` · `STORE_PROBE_CONTROL=FIRED` | **PASS** |
| F6-AC2 | `ARCHIVE_OBJECTS=4 of 4` · `SHA256_MATCH=3 of 3` · `ARCHIVE_MANIFEST_HAS=bytes_vs_manifest,builder_last_hash,sha256` | **PASS** |
| F6-AC3 | `LOCAL_KUZU_BUILDERS=2 of 486 files` · `STITCH_LOADER_AT_HEAD=false` · `BUILDER_PROBE_CONTROL=FIRED` | **FAIL** (row W7-S4) |
| F6-AC4 | `REFUSAL_NAMES_SERVED_STITCH=true` · `COMP_DEBT_RC_WITHOUT_STORE=0` | **PASS** |
| F6-AC5 | `TOMBSTONE_PRESENT=true` · `TOMBSTONE_NAMES=<all 7>` · `REGISTRY_MENTIONS=2 (row NFRA_CLDGRPH-W7-S2)` | **FAIL** (row W7-S3) |
| F6-AC6 | a reading act -- section 5 | `UNVERIFIABLE-BY-INSTRUMENT`, graded by `3.0.0_SA_CVO` at L9 |

**F6-AC3 FAILS on the criterion's own scope, and the cell's accept is MET.** The
criterion asks for a `kuzu.Database(<repo path>)` write-open census over
`infra/aws/globgrph/` **and the tool homes**; over the four tool homes it reads
**2 of 486 files**, both in `org/modules/graph/tsgraph_spike/`
(`load_scratch_kuzu.py:97`, `load_clusters_scratch.py:43`) -- tracked, not
gitignored, last touched 2026-06-17, and neither in this order's `<paths>`. Over
`infra/aws/globgrph/` alone -- which is what the cell's accept means by "beside
the projection" -- it reads **0 of 66 files**. Both numbers are printed by the
same run, and the narrower one was NOT substituted for the wider one: a scope
chosen after seeing the answer is not a measurement. Row `NFRA_CLDGRPH-W7-S4`.

**F6-AC5 FAILS on one character of a row-id coordinate.** Its `expect` admits
`row NFRA_CLDGRPH-W2-S[0-9]+` and this order was re-addressed to slot ~7, whose
rows the gate REQUIRES to mint `W7-S<k>`. The other two alternatives the regex
admits are both false here (`none` needs zero mentions needing disposition,
measured 2; `retired` needs an entry to mark, measured 0 entries whose subject is
a retired name). The honest line could not be made to match without lying or
minting an id the row gate would refuse. Row `NFRA_CLDGRPH-W7-S3`.

**Every probe carries a control that can fail, and each one fired:**

- F6-AC1: two positive controls resolved in the same directory (`controls_resolved=2 of 2`), so the three ABSENTs are readings and not a broken probe.
- F6-AC2: a negative control on a key that does not exist returned rc 255 / HTTP 404, so `head-object` discriminates; and the manifest was re-downloaded and re-hashed rather than read locally.
- F6-AC3: a planted builder that write-opens a repo path was CAUGHT (1 of 1) while the `read_only=True` open beside it was not counted and its docstring/comment mentions scored zero.
- F6-AC4: a mutant refusal naming no source scored FALSE.
- F6-AC5: a planted tombstone complete except `served_source` was caught, missing exactly that field.
- Determinism: two runs of the AC3 probe are byte-identical over 148 lines (only the timestamp line excluded).

---

## 4. THE REGISTRY CENSUS (R14 / R15)

Three carriers named by the order, plus the generated mirror of the first.
`TOTAL_MENTIONS=3`; `MENTIONS_R15_EXEMPT=1`; `MENTIONS_NEEDING_DISPOSITION=2`.

- `graph-call-manifest.yaml:140` -- a COMMENT citing the call form ("Stamped by
  kuzu_load / kuzu_nessie_load / kuzu_stitch_load"). **R15-exempt**: a record
  cites, it does not instruct.
- `graph-call-manifest.yaml:1237` -- the `freshness:` field of the LIVE canonical
  entry `xlayer.fullstack.firm_component_to_bucket`, naming db-path
  `infra/aws/globgrph/kuzu_stitch_db`. **Needs disposition** and is outside
  `<paths>` -> row `NFRA_CLDGRPH-W7-S2`.
- `.tools/tool_index.py:2443` -- the same string in the GENERATED mirror. Same row;
  the remedy is a regeneration, never a hand-edit.
- `comp-tools.yaml`: 0 mentions. `TOOL_MASTER.yaml`: 0 mentions.

**R14 was answered by LOADING the yaml, not by grepping it:** entries whose
`id`/`tool`/`name`/`alias` IS a retired name = **0** in all three carriers. There
is no entry to mark `status: retired`, which is precisely why R14's entry-grain
remedy does not reach the two live fields above -- and why they are a row.

---

## 5. F6-AC6 -- THE ARC, READ AT ITS END (a reading act; no verdict)

**Is "no machine is in the compile business" TRUE on this device for BOTH graphs?**

For the CANONICAL graph: yes, since `TO-CG-F-1` -- `kuzu_db`, `kuzu_ac7.db` and
`kuzu_load.py` are gone and tombstoned. For the STITCH graph: yes as of this
order -- `kuzu_stitch_db`, its manifest, the local `stitch_graph.json` and
`kuzu_stitch_load.py` are gone, `comp-debt` runs at rc 0 with no store anywhere,
and `LOCAL_KUZU_BUILDERS_BESIDE_PROJECTION=0 of 66`.

**But the sentence is only true when you scope it to the projection's home, and
the criterion did not.** Two tracked loaders in `org/modules/graph/tsgraph_spike/`
still `kuzu.Database(<repo path>)` a scratch store into
`tsgraph_spike/out/`. They compile a DIFFERENT graph (a portal-AST spike on the
same CloudNode/CloudEdge schema), they are not readers of anything retired here,
and they have not run since 2026-06-17 -- but they are a machine on this device in
the compile business, and `comp-kuzu`'s own schema is the one they build to, which
is exactly the confusion FWD-7 exists to prevent. This is the same population
`NFRA_CLDGRPH-W2-S25` declared at `TO-CG-D-7` pass 3, surfacing now against a
second criterion. **The estate has not decided about them; it has stepped around
them twice.**

**What remains that could re-enter the compile business.** Three routes, in
descending likelihood:

1. **The two spike loaders.** One command each, no arguments, and they rebuild a
   local Kuzu store under `org/modules/graph/`. Nothing gates them.
2. **`git show 8a074ba7ba:infra/aws/globgrph/kuzu_stitch_load.py`.** The
   INSTRUCTION plane is not the code plane: retiring a file removes the call, not
   the recipe. The tombstone names the hash on purpose -- a recoverable builder
   whose recovery is recorded is better than one nobody can find and nobody
   expected.
3. **`derive_stitch.py` / `extract_portal_stitch.py` run locally.** The order asks
   whether that is "a compile business". **My reading: not by itself.** They emit
   JSON; a JSON file is an INPUT to a compile, not a compiled artifact, and a JSON
   that nobody loads answers no query. What makes them dangerous is not what they
   WRITE but where a laptop-written artifact can LAND: `NFRA_CLDGRPH-S70`/`S71`
   record a post-commit hook that republished the stitch marker from a laptop
   clone 552 times since 2026-07-07. That is the live hazard on this pair, and it
   is a PUBLISHING hazard, not a compiling one. They stay, correctly, and this
   order did not touch them.

**What the CVO should read to grade FWD-7 REALIZED across the four JOIN cells.**
In order, because each cell's evidence is only meaningful behind the one before it:

- **CG-s-23** (`TO-CG-F-3`, slot ~2): the producer repaired -- 67 of 67 builds had
  FAILED and the served artifact was made by hand. Grade the CLOUD build, not the
  artifact: an artifact with a hand-made provenance passes every freshness check.
- **CG-s-24** (`TO-CG-F-4`): the projection carries the stitch source. The number
  that closes it is the served query above -- GOLD_SCRIPT 1380 / S3_DATA_KEY 294 at
  a projection vintage two months younger than the store just retired.
- **CG-s-25** (`TO-CG-F-5`, DONE @`b9917bc2e1`, instance re-validated VALID at this
  HEAD): comp-debt's second leg repointed. Its F5-AC3 is the load-bearing one --
  the tool opens no local store -- because it is what made THIS cell safe.
- **CG-s-26** (this order): the archive verified by head-object, the store absent,
  the builder gone, the refusal naming the served source, and the tool running at
  rc 0 with nothing local to fall back to.

And then the one thing none of the four cells measured: **the two spike loaders.**
FWD-7's EXISTENCE clause asks that no second copy remain that anyone could still be
reading from. Nobody is reading those two stores -- but the machine that makes them
is one command away, tracked, and in a tool home. Whether that is REALIZED or
NOT_REALIZED is the CVO's call, and it is the only open question this order leaves
that the CVO cannot answer from the four instances alone.

---

## 6. THE SCRIPTS

All under `org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7/`
(the order's face names `~2`; the owned-paths lane gate REFUSES that folder for
serial ~7 with 18 VIOLATION lines -- row `NFRA_CLDGRPH-W7-S1`, with the measured
refusal and the positive control quoted).

| file | what it is |
|---|---|
| `f6_before.sh` / `f6_before.txt` | step 1 -- verify before anything moves |
| `f6_archive_manifest.py` / `f6_ARCHIVE_MANIFEST.json` | the archive manifest; hashes taken once, three consumers |
| `f6_archive.sh` / `f6_archive.txt` | step 2 -- four PutObject acts, then head-object |
| `f6_delete.sh` / `f6_after.txt` | step 4 -- deletion behind a guard re-read from the tombstone |
| `f6_store_absent.sh` / `f6_ac1_run.txt` | F6-AC1 |
| `f6_archive_verified.sh` / `f6_ac2_run.txt` | F6-AC2 |
| `f6_local_builder_ast.py`, `f6_no_local_builder.sh` / `f6_ac3_run.txt` | F6-AC3 -- the builder walker, three runs |
| `f6_refusal_and_run.sh` / `f6_ac4_run.txt` | F6-AC4 -- two instruments on the refusal, then the run |
| `f6_tombstone_parse.py`, `f6_registry_census.py`, `f6_tombstone.sh` / `f6_ac5_run.txt` | F6-AC5 |
| `f6_plant/planted_builder.py`, `f6_plant/planted_tombstone_missing_field.md` | the two controls that must be able to fail |
