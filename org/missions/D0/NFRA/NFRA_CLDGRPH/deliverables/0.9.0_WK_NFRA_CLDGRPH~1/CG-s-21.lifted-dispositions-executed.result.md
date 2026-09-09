# CG-s-21 -- THE LIFTED DISPOSITIONS EXECUTED

**Cell:** `CG-s-21` (decomposition v0.6, round 6) · **TO:** `NFRA_CLDGRPH.TO-CG-F-1` ·
**Assignee:** `0.9.0_WK_NFRA_CLDGRPH~1` · **Branch:** `wk-cldgrph-6-1` (LOCAL; never pushed,
never merged, never rebased) · **Worktree:** `C:/tmp/wk-cldgrph-6-1` · **HEAD at hand-off:**
`c6b16d8f04cf46b55ed0aba12acb7537dd51b30d` · **Acts commit:** `dcdf0581b1`.

**WHAT THIS ORDER DID NOT DO, first, because it is the load-bearing half.** No engine was
opened -- `kuzu.Database` CREATES an absent store, so every count in this record comes from a
manifest read as a FILE and none from a query. No loader was run. `kuzu_stitch_db` and its
manifest were not touched: they are S26's, LAST in that chain, and CG-s-20's question, not this
order's; they are still on this device and `f1_after.txt` prints them so the scope is visible.
The stale `.kuzu_nessie_load.0628067ab4da5610.lock` was not deleted -- its disposition belongs to
a different act. Two objects were written to S3 and nothing else. Nothing in the main workspace
outside the five named paths was read, moved or removed.

## 1. THE RECORD

```json
{
  "order_of_acts": [
    "1. VERIFY BEFORE ANYTHING MOVED -- f1_before.sh -> f1_before.txt (18:23:16Z)",
    "2. ARCHIVE -- f1_archive.sh -> f1_archive.txt (18:24:15Z), two PutObject acts",
    "3. VERIFY THE ARCHIVE -- head-object --checksum-mode ENABLED, inside the same script",
    "4. TOMBSTONE -- infra/aws/globgrph/kuzu_db.TOMBSTONE.md written (tracked)",
    "5. RETIRE THE BUILDER -- git rm infra/aws/globgrph/kuzu_load.py",
    "6. RE-RUN THE READER CENSUS -- f1_no_readers.sh, builder exclusion now EMPTY",
    "7. DELETE, LAST -- f1_delete.sh -> f1_after.txt (18:28:43Z), each deletion behind a guard re-read inside the deletion script"
  ],
  "artifacts": [
    {
      "name": "kuzu_db",
      "location_before": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_db (MAIN workspace, gitignored -- no commit ever carried its bytes)",
      "before": {
        "size_bytes": 9224192,
        "sha256": "d7990739870c206c18697a75eaf60e2ab05ff21ae66f3cca6889ca3366925bc3",
        "mtime_local": "2026-06-12 09:55:12.930787700 -0400"
      },
      "disposition_executed": "RETIRE_WITH_TOMBSTONE",
      "archive_key": "NONE -- the tarball IS its archive; no upload was taken for this artifact",
      "recoverable_from": {
        "key": "s3://opal-313476888478-globgrph/snapshots/20260612/graph-20260612.tar.gz",
        "head_object": "ContentLength 71671, LastModified 2026-06-12T02:02:27Z, ETag 3925738fbea21729290cf6d9ae640e3d",
        "read_at": "18:23:1xZ before the deletions, re-read at 18:28:4xZ inside f1_delete.sh as GUARD_A, and again at 18:3xZ by f1_archives_verified.sh -- three reads, the middle one the one the deletion actually turned on"
      },
      "after": "ABSENT -- ls -d rc 2, beside a positive control on projection_client.py in the same directory"
    },
    {
      "name": "kuzu_db._build_manifest.json",
      "before": {
        "size_bytes": 403,
        "sha256": "c7fe612814314c75f39f308ac22a64cd27bf9edc6fcde97ec7ba417ec5aca2e9",
        "mtime_local": "2026-09-09 11:58:28.267894500 -0400"
      },
      "disposition_executed": "RETIRE_WITH_TOMBSTONE",
      "archive_key": "NONE -- its CONTENT is quoted whole inside the tombstone's manifest.content field",
      "content_quoted": "artifact_claim historical; built_at 2026-06-12T13:55:02.779461+00:00; node_count 1166; edge_count 2488 with edge_count_claim merge_attempts (an UPPER BOUND on edges present, not a count); source_kind tarball; source_vintage.tarball_key snapshots/20260612/graph-20260612.tar.gz",
      "after": "ABSENT"
    },
    {
      "name": "kuzu_ac7.db",
      "before": {
        "size_bytes": 4050944,
        "sha256": "6cdff04ad18c4ad64035c56b548418f7749314e37467285efc79e47fa13074cf",
        "mtime_local": "2026-06-12 10:57:51.598640000 -0400"
      },
      "disposition_executed": "ARCHIVE_UNDER_PROJECT then REMOVE",
      "archive_key": "s3://opal-313476888478-globgrph/archive/NFRA_GLOBGRPH.ITEM-3/kuzu_ac7.db",
      "head_object_after_upload": "ContentLength 4050944, ChecksumSHA256 bN/wStGMStZANcVrVIQY93STFON0Zyhe/Hnkf6EwdM8=, ChecksumType FULL_OBJECT, ETag adbf8d116615fbc3524fdba9707dba79, LastModified 2026-09-09T18:24:19Z",
      "sha256_equality": "S3-COMPUTED == LOCAL PRE-UPLOAD. base64(6cdff04a...74cf) = bN/wStGMStZANcVrVIQY93STFON0Zyhe/Hnkf6EwdM8=, which is what head-object --checksum-mode ENABLED returned. The comparison is local bytes vs bytes S3 hashed itself, not local vs local.",
      "after": "ABSENT"
    },
    {
      "name": "kuzu_ac7.db._build_manifest.json",
      "before": {
        "size_bytes": 908,
        "sha256": "44d1be62aa23bca9095cb4ab9bedde07b9e444d766ab80956c477ed6d0447542",
        "mtime_local": "2026-09-09 11:58:28.270575000 -0400"
      },
      "disposition_executed": "ARCHIVE_UNDER_PROJECT then REMOVE -- the claim card travels with the bytes it describes",
      "archive_key": "s3://opal-313476888478-globgrph/archive/NFRA_GLOBGRPH.ITEM-3/kuzu_ac7.db._build_manifest.json",
      "head_object_after_upload": "ContentLength 908, ChecksumSHA256 RNG+YqojvKkJXLSrm+3eB7nkRNdmq4CVbEd+1tBEdUI=, ChecksumType FULL_OBJECT, ETag ec06ece597a81c798033ca01d6103bb7, LastModified 2026-09-09T18:24:24Z",
      "sha256_equality": "S3-COMPUTED == LOCAL PRE-UPLOAD",
      "content_note": "a CLAIM CARD written by CG-s-19, not a build stamp: artifact_claim historical, edge_count_claim unknown, source unknown, NO counts -- because no count of this store exists that was not produced by opening it",
      "after": "ABSENT"
    },
    {
      "name": "kuzu_ac7/",
      "before": "an EMPTY directory, 0 entries, 2026-06-09",
      "disposition_executed": "REMOVE (rmdir on an empty directory; no recursive delete was used anywhere in this order)",
      "archive_key": "n/a -- nothing was in it",
      "after": "ABSENT"
    },
    {
      "name": "infra/aws/globgrph/kuzu_load.py",
      "location_before": "TRACKED in this repository (unlike the stores)",
      "before": {
        "size_bytes": 13318,
        "blob_sha1": "8880003ebe0e4327a44989c6d4705b5a688e4be0",
        "last_commit_that_modified_it": "85e33e98eed8d63709bb79fa0ca33c4978fedc8f"
      },
      "disposition_executed": "RETIRE -- git rm, NOT rescope",
      "why_not_rescope": "RESCOPE was the alternative the order named and it turns on finding a LIVE reader. This seat's own AST census found none: READERS=0 of 486 files over .tools, org/modules/graph, org/modules/heatmap and infra/aws/globgrph, with the builder exclusion EMPTY (no --builder flag), the planted opener CAUGHT and the docstring specimen scored ZERO. E-3's KEEP_WITH_NAMED_READER named no reader -- it named the store's own builder.",
      "builder_last_hash": "c6b16d8f04cf46b55ed0aba12acb7537dd51b30d",
      "recover_with": "git show c6b16d8f04cf46b55ed0aba12acb7537dd51b30d:infra/aws/globgrph/kuzu_load.py",
      "after": "git show HEAD:infra/aws/globgrph/kuzu_load.py -> rc 128, 'path does not exist in HEAD'; the same verb on kuzu_db.TOMBSTONE.md returns rc 0"
    }
  ],
  "tombstone": {
    "path": "infra/aws/globgrph/kuzu_db.TOMBSTONE.md",
    "tracked": true,
    "fields_present": "8 of 8 -- tarball_key, tarball_size, tarball_etag, manifest, archive_keys, archive_sha256, builder_last_hash, authority",
    "control": "f1_plant/planted_tombstone_missing_field.md, complete except archive_sha256, run through the SAME parser: MISSING_FIELDS=archive_sha256, FIELDS_PRESENT=7 of 8"
  },
  "s3_writes_taken": [
    "PutObject archive/NFRA_GLOBGRPH.ITEM-3/kuzu_ac7.db",
    "PutObject archive/NFRA_GLOBGRPH.ITEM-3/kuzu_ac7.db._build_manifest.json"
  ],
  "s3_writes_not_taken": "nothing else; the bucket is opal-313476888478-globgrph (the order names a near-identical typo as a BLOCKING row, and the digits were read off the manifest's own snapshot_bucket field before the first call)"
}
```

## 2. NOTHING WAS DELETED BEFORE ITS OBJECT WAS VERIFIED, AND THE GUARD IS INSIDE THE DELETING SCRIPT

This is the clause worth being pedantic about, because a guard that ran ten minutes and one
script earlier is a guard that could have been carried stale. `f1_delete.sh` does not trust
`f1_archive.sh`. It re-issues `head-object` on the tarball (GUARD_A: rc 0 AND ContentLength
71671) and on both archive objects with `--checksum-mode ENABLED` (GUARD_B: rc 0 AND size AND
`ChecksumSHA256` equal to the pre-upload value), and each `rm` sits behind the guard for the
object its bytes survive in. On a failed guard the script prints `SKIPPED ... GUARD_x did not
hold` and deletes nothing -- which is the honest failure mode F1-AC2 describes.

Both guards read true (`GUARD_A=true`, `GUARD_B=true`) and the five deletions were taken. The
negative control on the retrieval is in `f1_ac2_output.txt`: `head-object` on
`archive/NFRA_GLOBGRPH.ITEM-3/f1_no_such_object.db` returns rc 255 / 404, so a present object and
an absent one are distinguishable by this instrument -- without that line the two `PRESENT=true`
readings above would be assertions about a verb that might always succeed.

## 3. THE READER CENSUS, RE-RUN WITH AN EMPTY EXCLUSION

E-3 measured `READERS=0 of 487 files` with `infra/aws/globgrph/kuzu_load.py` DECLARED and
excluded by name. That zero was conditional on the exclusion. This run passes NO `--builder`
flag: nothing is excluded, and the denominator is 486 because the builder itself is gone from
the tree. `READERS=0 of 486 files`, `PARSE_FAILURES=0` (an unread file cannot hide inside the
zero), `PROSE_MENTIONS=1`, `DOCSTRING_MENTIONS=1`, and the two near-miss glued-token files
(`scratch_kuzu_db` in `tsgraph_spike`, a DIFFERENT artifact) printed rather than silently
dropped. Controls: `READER_PROBE_CONTROL=FIRED` (the planted opener caught at two lines) and
`READER_BAND_CONTROL=FIRED` (the docstring specimen seen and scored zero). The instrument is
E-3's own `_readers_ast.py`, reused under the order's SURFACES grant -- the same walker, a
weaker precondition, the same answer.

A note on grain, since this is the second seat to report this zero: it is the SAME INSTRUMENT as
E-3's, so this is repetition on that axis, not corroboration. The independent instrument is the
CVO's `comp-find` census (0 readers of 982 files at C-S22/C-S26), which this seat did not re-run
and does not claim.

## 4. F1-AC6 -- THE EXISTENCE READING (a reading act; no verdict; graded by `3.0.0_SA_CVO` at L9)

**Is "no second, older copy anyone could still be reading from" now TRUE on this device for the
canonical graph?** For the canonical graph, yes, and the qualifier is doing real work in that
sentence.

The two June-2026 local copies of the canonical graph are gone from this device: `kuzu_db`
(9,224,192 B, 1,166 nodes by its manifest) and `kuzu_ac7.db` (4,050,944 B, no counts anyone can
state honestly). `ls -d` reads `STORES_PRESENT=0 of 2` beside a control that prints a path in the
same directory, so the absence is a reading and not a broken probe. The BUILDER is gone too,
which is the half FWD-7's existence clause actually turns on: absence of a copy is a state, and a
state with a one-command path back to it is a state with a short half-life. `kuzu_load.py`'s
default DB path sat beside the projection's tooling; one invocation re-created the second copy.
That is what the CTO's row meant by *a builder beside the projection is the path back*, and it is
why RETIRE and not RESCOPE was the honest disposition once the census found no reader to name.

**What the tarball's continued presence in S3 means.** `snapshots/20260612/graph-20260612.tar.gz`
is still served, and that is the whole reason the CVO could lift the hold on `kuzu_db` rather
than archive it. But REPRODUCIBLE IS NOT PRESENT, and the difference is exactly the difference
FWD-7 is about. A tarball in S3 is not a store anything can read: nothing on this device opens it,
no tool path resolves to it, and rebuilding a Kuzu store from it now requires a loader this
repository no longer carries. It is recovery material, not a live copy. The estate lost nothing it
cannot rebuild; it lost the thing a reader could have silently read. Symmetrically, the
`kuzu_ac7.db` archive object is a copy of unreproducible bytes with unknown provenance -- kept
precisely because it CANNOT be rebuilt -- and it is equally unreadable as a graph: it sits under
an archive prefix that names a closed task order, with its claim card beside it saying it has no
known source. Neither object is a "second copy anyone could still be reading from" in any sense
that makes FWD-7's sentence false; both are the record that makes deleting the live copies safe.

**What would make the reading false again.** Three things, in descending likelihood. (1) A BUILDER
RE-LANDING. `git show c6b16d8f04cf46b55ed0aba12acb7537dd51b30d:infra/aws/globgrph/kuzu_load.py`
restores a working builder in one command -- this tombstone prints that command, deliberately,
because a recovery path a reader cannot find is not recovery. Anything that re-lands it, or
authors a new local loader with a default path under the tool homes, re-opens the clause; the C3
moratorium and this record are what stand against that, not a mechanism. (2) `kuzu_stitch_db`,
which is STILL ON THIS DEVICE (9,170,944 B, 2026-08-27) and was deliberately not touched: it is
S26's, last in its chain, and CG-s-20's question. It is not the canonical graph, which is why the
reading above is scoped to the canonical graph and says so; but a seat that reads FWD-7 as "no
local Kuzu store at all" has an open item there, and this order is not the place it closes. (3) A
REBUILD FROM THE TARBALL, which is legitimate recovery rather than drift -- but if anyone takes
it, the store that appears is a second, older copy again, and this tombstone is then stale.

The narrower thing this reading will not claim: it is about THIS DEVICE. `f1_stores_absent.sh`
reads one filesystem. The site-Z half of the existence question is a different order's, and a
copy on a machine this seat cannot see would not show up in any line above.

## 5. THE SCRIPTS AND THEIR OUTPUTS

| file | what it is |
|---|---|
| `f1_before.sh` / `f1_before.txt` | step 1, the pre-act state: presence, size, mtime, sha256, both manifests quoted whole, the tarball head-object, the archive prefix EMPTY |
| `f1_archive.sh` / `f1_archive.txt` | step 2, the two PutObject acts and their head-object verification |
| `f1_delete.sh` / `f1_after.txt` | step 4, the guarded deletions and the printed NOT-TOUCHED list |
| `f1_stores_absent.sh` / `f1_ac1_output.txt` | F1-AC1 |
| `f1_archives_verified.sh` / `f1_ac2_output.txt` | F1-AC2, expectations read out of the TOMBSTONE, not out of the uploader's memory |
| `f1_no_readers.sh` / `f1_ac3_output.txt` | F1-AC3, E-3's `_readers_ast.py` re-run with an empty exclusion |
| `f1_tombstone.sh` + `f1_tombstone_parse.py` / `f1_ac4_output.txt` | F1-AC4 and its planted specimen |
| `f1_plant/planted_tombstone_missing_field.md` | F1-AC4's control: a tombstone missing exactly `archive_sha256` |

## 6. SURPRISE

One row, `NFRA_CLDGRPH-W1-S32` (OBSERVATION, INERT, UNDER_INVESTIGATION): the order's
`compiler_tools_mandate` says *"No `.py` is added by this order; one is removed"* and this order
added one -- `f1_tombstone_parse.py`, the instrument F1-AC4's eight-field check and its planted
control both need. Both readings of the clause are named in the row; neither is assumed. Nothing
in this order's acceptance depends on which is taken. Channel denominator restated 152 -> 153 by
parsing every fenced block (124 -> 125 blocks).
