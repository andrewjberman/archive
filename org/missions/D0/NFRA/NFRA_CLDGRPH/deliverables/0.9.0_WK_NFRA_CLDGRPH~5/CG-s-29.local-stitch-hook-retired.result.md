THIS IS THE LAPTOP + INSTRUCTION-PLANE RECORD; SITE Z'S DEVICE RECORD IS THE OTHER HALF; THE CVO GRADES S29 AGAINST BOTH

# CG-s-29 -- the local post-commit stitch hook retired on three planes (laptop half)

`NFRA_CLDGRPH.TO-CG-F-9` · cell `CG-s-29` · PRD v0.7 row S29 + R16 @`a46abe413a` · worker
`0.9.0_WK_NFRA_CLDGRPH~5`, branch `wk-cldgrph-6-5`, worktree `C:/tmp/wk-cldgrph-6-5`, HEAD at hand-off
`2e8dd90435`. Push state: **LOCAL** on every commit below.

```json
{
  "record": "CG-s-29 -- laptop + instruction plane",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-9",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~5",
  "branch": "wk-cldgrph-6-5",
  "s3_objects_written_by_this_worker": 0,

  "keys_before_any_act": {
    "read_at": "2026-09-09T19:14:02Z",
    "stitch/stitch_marker.json": {"LastModified": "Wed, 09 Sep 2026 18:49:37 GMT", "ContentLength": 330, "ETag": "36fb4506de3a388614f607cedc97516a"},
    "stitch/stitch_graph.json": {"LastModified": "Wed, 09 Sep 2026 18:49:36 GMT", "ContentLength": 38845013, "ETag": "b5cfaf8f483d4195e7e7c2319bd5e7cd-5"},
    "marker_producer": "stitch-codebuild",
    "marker_built_at": "2026-09-09T18:49:23Z",
    "capture": "f9_keys_before.txt"
  },
  "keys_after_last_act": {
    "read_at": "2026-09-09T20:07:06Z",
    "stitch/stitch_marker.json": {"LastModified": "Wed, 09 Sep 2026 19:55:15 GMT", "ContentLength": 330, "ETag": "00dd8c738f236f2bafa9a84d04d0fd44"},
    "stitch/stitch_graph.json": {"LastModified": "Wed, 09 Sep 2026 19:55:14 GMT", "ContentLength": 38845013, "ETag": "f50001a195ee85434f29645cc42dd971-5"},
    "marker_producer": "stitch-codebuild",
    "marker_built_at": "2026-09-09T19:55:00Z",
    "capture": "f9_keys_after.txt",
    "EQUAL_TO_BEFORE": false,
    "why_not": "NOT this worker's hand. The keys moved TWICE during the order by the ISSUER's acts -- see key_movements below and row NFRA_CLDGRPH-W5-S4. Across every act THIS worker performed, both keys were byte-equal before and after (2 of 2, twice: the refusal exercise at 19:18:28Z and again at 20:05:57Z; and the silence test at 19:59-20:05)."
  },
  "key_movements_during_the_order": [
    {"at": "2026-09-09T19:45:44Z", "by": "this laptop's still-installed post-commit hook, fired by the ISSUER's own commit 6de9b76d93", "producer": "stitch-local", "nodes": 29320, "edges": 61835, "lastmodified": "artifact 19:45:51Z / marker 19:46:00Z", "note": "the S71 failure recurring INSIDE the order that retires it, 46 s before the device act; also the expiry of S71's premise that this laptop was inert (F-3's repaired derive now PASSES here). Corroborated by a SECOND instrument: the device's residue log OK-published count moved 552 -> 553."},
    {"at": "2026-09-09T19:55:00Z", "by": "the ISSUER's ad-hoc opal-stitch-produce build (CodeBuild)", "producer": "stitch-codebuild", "nodes": 29267, "edges": 61275, "lastmodified": "artifact 19:55:14Z / marker 19:55:15Z", "note": "re-asserts the cloud producer as the ONE writer; this is the state at the closing read."}
  ],

  "refusal": {
    "criterion": "F9-AC1",
    "invocation": "timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~5/f9_refuses.sh",
    "run_at": "2026-09-09T20:05:57Z (first run 19:18:28Z, same result)",
    "STITCH_REFRESH_RC": 3,
    "REFUSAL_NAMES": "opal-stitch-produce",
    "DERIVE_RAN": false,
    "derive_tells": "no derive/marker output line AND the local derive artifact in TMP untouched (1788534311:39722299 before and after)",
    "STDOUT_BYTES": 0,
    "KEYS_LASTMODIFIED_UNCHANGED": "2 of 2",
    "EQUALITY_CONTROL": "CAN-FAIL",
    "stderr_verbatim": "ERROR: stitch-refresh is RETIRED as a publisher (NFRA_CLDGRPH S29 @a46abe413a, R16): the stitch keys s3://opal-313476888478-globgrph/stitch/ have ONE writer, the cloud producer opal-stitch-produce (CodeBuild, rule opal-stitch-produce-nightly 03:00Z). No local derive is run and nothing is published. Re-enable only on Andrew's word (re-add the hook line; see .tools/git-hooks/stitch-refresh-post-commit.TOMBSTONE.md).",
    "capture": "f9_refusal.txt"
  },

  "publish_path_choice": {
    "choice": "DELETED",
    "what_was_deleted": "old .tools/stitch-refresh lines 44-87 -- the derive call, the marker build (producer=stitch-local) and the two `aws s3 cp` publishes",
    "what_was_kept": "lines 1-31 byte-for-byte (Andrew's 2026-07-07 words at 6-12), plus `set -u` and the constants BUCKET/ART_KEY/MRK_KEY as the record of the keys the script no longer writes",
    "why": "the issuer's stated preference and R14's spirit: a dead publish path is a route back",
    "recovery": "git show 2e8dd90435:.tools/stitch-refresh",
    "new_exit_code": "3 -- distinct from the header's documented 2 = grain-sentinel and 1 = failed publish; the semantics are extended, not reused",
    "file_now": "97 lines (was 87)"
  },

  "instruction_plane": {
    "criterion": "F9-AC2",
    "invocation": "timeout 120 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~5/f9_instruction_plane.sh",
    "run_at": "2026-09-09T20:06:15Z",
    "HOOK_SCRIPT_AT_HEAD": "false rc=128 (fatal: path '.tools/git-hooks/stitch-refresh-post-commit.sh' does not exist in 'HEAD')",
    "INSTALLER_AT_HEAD": "false rc=128 (fatal: path '.tools/git-hooks/install-stitch-refresh.sh' does not exist in 'HEAD')",
    "positive_controls": {"tombstone_at_HEAD": true, "hook_at_last_hash": true, "installer_at_last_hash": true},
    "retiring_commit": "26f3c88dd6e1b385bc97eb188ed5128484cd19cd",
    "last_hash_carrying_both_files": "2e8dd90435",
    "TOMBSTONE_NAMES": "superseded_word_verbatim,later_word,ruling_record,last_hash,reenable_path,s71_numbers",
    "SUPERSEDED_BLOCK_PRESENT": true,
    "ORIGINAL_WORDS_BYTE_KEPT": true,
    "lines_6_12_md5": {"parent_record": "b14be8d4866824d8fd58da1e198d4680", "head_record": "b14be8d4866824d8fd58da1e198d4680", "working_file_cr_stripped": "b14be8d4866824d8fd58da1e198d4680"},
    "BYTE_COMPARE_CONTROL": "CAN-FAIL (line 32 differs parent-vs-HEAD)",
    "TOMBSTONE_PROBE_CONTROL": "FIRED (a planted copy with the last hash stripped loses last_hash AND reenable_path; 4 of 6)",
    "capture": "f9_instruction_plane.txt"
  },

  "hook_lines_laptop": {
    "criterion": "F9-AC3",
    "before": {"read_at": "2026-09-09T19:14:30Z", "bytes": 1615, "TOTAL_LINES": 21, "STITCH_HOOK_LINES": 2, "stitch_pair_at": "lines 3-4", "other_entries": 5, "capture": "f9_hook_before.txt"},
    "poll": {"start": "2026-09-09T19:22:20Z", "cadence_s": 60, "cap_min": 30, "landed_at_poll_tick": "t=+25m, 2026-09-09T19:47:40Z read 0", "capture": "f9_hook_wait.txt"},
    "device_act": {"by": "1.0.0_SA_CTO (the device's live Tier-1 seat; the lane amended from 0.0.0_AB_MSTR)", "at": "~2026-09-09T19:46:3xZ", "record": "the CTO's adjudication section 19:46Z + row NFRA_CLDGRPH-S77 @ce0eee9f93"},
    "after": {"HOOK_READ_AT": "2026-09-09T19:49:20Z", "bytes": 1337, "STITCH_HOOK_LINES_LAPTOP": "0 of 19", "OTHER_HOOK_ENTRIES": 5, "entries": ["missions-refresh-post-commit.sh", "closeout-comp-state-post-commit.sh", "deploy-pipescript-check-post-commit.sh", "directives-check-post-commit.sh", "prd-header-notify-post-commit.sh"], "capture": "f9_hook_after.txt"},
    "note": "the face says SIX other entries and the file has FIVE; the face's own enumeration lists five. Row NFRA_CLDGRPH-W5-S3 corrects this seat's own W5-S1, which had copied the face's figure instead of measuring it."
  },

  "silence_test": {
    "criterion": "F9-AC4",
    "invocation": "timeout 240 bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~5/f9_silence.sh",
    "FILTER_COMMIT": "66f61f2fbf",
    "FILTER_COMMIT_AT_UTC": "2026-09-09T19:59:10Z",
    "FILTER_MATCHING_PATHS_IN_COMMIT": "1 (org/modules/graph/STITCH_HOOK_RETIRED.md)",
    "baseline": {"read_at": "2026-09-09T19:58:55Z", "artifact": "Wed, 09 Sep 2026 19:55:14 GMT", "marker": "Wed, 09 Sep 2026 19:55:15 GMT", "artifact_file": "f9_keys_pre_filter_commit.txt"},
    "WAITED_S": 137,
    "after": {"artifact": "Wed, 09 Sep 2026 19:55:14 GMT", "marker": "Wed, 09 Sep 2026 19:55:15 GMT"},
    "KEYS_LASTMODIFIED_UNCHANGED": "2 of 2",
    "KEYS_PREDATE_FILTER_COMMIT": "2 of 2",
    "EQUALITY_CONTROL": "CAN-FAIL",
    "MARKER_PRODUCER": "stitch-codebuild",
    "capture": "f9_silence.txt",
    "run1": {"filter_commit": "00ec6d1d96", "at_utc": "2026-09-09T19:50:38Z", "waited_s": 138, "keys_unchanged_vs_PRE-ORDER_baseline": "0 of 2", "keys_unchanged_across_the_window": "2 of 2 (19:45:51Z / 19:46:00Z both before and after, both predating the commit)", "marker_producer_then": "stitch-local", "capture": "f9_silence_run1.txt", "note": "kept verbatim; the 0 of 2 is a true statement about the KEYS and a false one about the COMMIT -- the baseline spanned the issuer's 19:45:44Z hook publish"},
    "run2": {"note": "same numbers as the final run; superseded only because FILTER_COMMIT_AT_UTC printed LOCAL time with a Z suffix (a --date=format literal-Z trap). Kept at f9_silence_run2.txt", "capture": "f9_silence_run2.txt"}
  },

  "residue": {
    "path": "C:/Users/ANDREW~1/AppData/Local/Temp/stitch-refresh.log",
    "deleted_truncated_or_moved": false,
    "at_19:16:01Z": {"bytes": 1707765, "lines": 16206, "ok_published": 552, "grain_sentinel_refusals": 145, "mtime_local": "2026-09-09 14:55:20 -0400"},
    "at_20:07:06Z": {"bytes": 1710748, "ok_published": 553, "mtime_local": "2026-09-09 15:45 -0400"},
    "first_line": "<unknown>:91: SyntaxWarning: invalid escape sequence '\\$'",
    "last_line_at_first_read": "ERROR: grain-sentinel FAIL -- refusing to publish a grain-violating stitch (no artifact).",
    "note": "the 552 -> 553 move is the SECOND instrument on the 19:45:44Z publish -- the device's own log, independent of the S3 key's LastModified"
  },

  "retired_files": [
    {"path": ".tools/git-hooks/stitch-refresh-post-commit.sh", "lines": 27, "last_hash": "2e8dd90435", "recover": "git show 2e8dd90435:.tools/git-hooks/stitch-refresh-post-commit.sh"},
    {"path": ".tools/git-hooks/install-stitch-refresh.sh", "lines": 31, "last_hash": "2e8dd90435", "recover": "git show 2e8dd90435:.tools/git-hooks/install-stitch-refresh.sh", "why_retired": "the WIDER reading of 'the two scripts': an installer of a retired hook re-creates the executable plane on any clone in one command"}
  ],

  "commits_on_wk-cldgrph-6-5": [
    {"hash": "26f3c88dd6", "what": "the acts: the refusal + SUPERSEDED block, both hook files git rm-ed, the tombstone, the first captures"},
    {"hash": "909396d8d1", "what": "the tombstone's verbatim quote completed and the later word un-wrapped, after the F9-AC2 probe caught both"},
    {"hash": "1d9a77ea1f", "what": "rows W5-S1, W5-S2"},
    {"hash": "00ec6d1d96", "what": "the first filter-matching commit"},
    {"hash": "66f61f2fbf", "what": "the second filter-matching commit, on a settled key"}
  ],

  "rows_filed": ["NFRA_CLDGRPH-W5-S1", "NFRA_CLDGRPH-W5-S2", "NFRA_CLDGRPH-W5-S3", "NFRA_CLDGRPH-W5-S4"]
}
```

## What this record proves, and what it cannot

**The instruction plane is retired and the retirement is exercised, not described.** `.tools/stitch-refresh`
does not refuse in a comment: it was RUN, under `timeout 120`, and exited 3 with the refusal on stderr naming
`opal-stitch-produce`, with no derive output, no local artifact touched, and both keys byte-equal across the
attempt. The two files that carried the executable plane into any fresh clone -- the hook body and its
installer -- are gone at HEAD (rc 128 beside three positive controls), and the tombstone carries all six
fields a grader can probe, with a planted copy proving the probe can still fail.

**Andrew's 2026-07-07 words are kept byte-for-byte.** Lines 6-12 of `.tools/stitch-refresh` hash identically
at the parent record, at HEAD, and in the working file (CR-stripped -- this box is `core.autocrlf=true`, so an
unstripped compare would false-FAIL and the record says so rather than hiding it). The SUPERSEDED block sits
directly beneath them and cites the later word, the PRD row, the rule and the ruling record. R16's whole point
is that the earlier word is never edited away and never silently demoted; the file now reads as two dated
words with the later one governing.

**The laptop's device plane is done, and it is not this worker's act.** The hook pair was removed at
~19:46:3xZ by `1.0.0_SA_CTO` (the lane the issuer amended to "the device's live Tier-1 seat or MSTR"); this
worker only READ the file, by absolute path, before and after, and polled for the change. `0 of 19` lines name
stitch-refresh; the five other entries are present and named, which is the positive control that the read is a
read and not an empty file.

**A filter-matching commit on this clone now publishes nothing.** `org/modules/graph/STITCH_HOOK_RETIRED.md`
is the path the retired regex matched; committing it and waiting 137 s left both keys exactly where they were,
and both keys' LastModified PREDATE the commit -- a limb no stale baseline can satisfy. The marker is the
cloud's.

**What only site Z's record can prove.** Site Z is not reachable from this device. Its hook line, its 120 s
silence, and the instant of its own device act live in its record, by its integrator. Until that lands, the
key has one writer on THIS clone and an unretired writer on the other: row `NFRA_CLDGRPH-S77` names site Z as
the live overwriter, `disarm_owner 0.0.0_AB_MSTR`, on Andrew's word. **S29 is not met by this document alone**,
and the CVO grades it against both halves.

## F9-AC5 -- one writer, read on both clones (a reading act; no verdict)

**What the laptop half proves.** Three things, each measured rather than asserted. (1) The publisher cannot
publish: exit 3, before the derive, with the cloud producer named in the refusal text a re-enabling seat will
read. (2) The instruction plane cannot be re-created from this repository: both the hook body and its
installer are absent at HEAD, so there is no one-command route back; the route that remains is a deliberate
`git show 2e8dd90435:` restore, which the tombstone spells out precisely because a reversal on Andrew's word
should be easy to do correctly and impossible to do by accident. (3) The device plane on this clone is clear,
and a filter-matching commit -- the exact event that fired 553 publishes since 2026-07-07 -- now moves nothing.

**What only site Z's device record can prove.** That its `.git/hooks/post-commit` has 0 lines naming
stitch-refresh beside its own positive control; that a commit touching a filter path there is followed by 120 s
of silence on both keys; and the instant of its uninstall. Site Z is the clone the CTO named FIRST, because at
the S71 read it was the live overwriter (17:53:55Z, `producer stitch-local`, a site-Z sha) while this laptop
was believed inert. **That belief expired inside this order** -- see below -- which makes site Z's half more
urgent, not less.

**Is the residue plane complete?** On this device, yes, in the sense the cell asks: the log is noted and not
deleted -- 1,710,748 bytes, mtime 15:45 local, first and last lines recorded, `OK: stitch published local`
counted at 552 and then 553. Two things about it are worth the CVO's attention. First, the count of grain
refusals at this read is **145**, not the 143 the S71 evidence carries; the log has kept running since that
read, which is what a residue file does, and neither number is wrong for its own instant. Second, and more
important, **the reason this laptop went quiet was never the retirement**: the S71 record says "on this laptop
the derive has refused on every run since 09-05 (grain sentinel), so this laptop is inert *by accident*". That
sentence stopped being true when F-3's repaired derive merged. At **19:45:44Z**, four minutes before the device
act and while this order was polling for it, the issuer's own commit `6de9b76d93` fired this laptop's hook and
published `producer: stitch-local`, 29,320 nodes / 61,835 edges, over the cloud's marker -- the 553rd publish,
visible in two independent instruments (the key's LastModified and the device's own log). The estate had, for
roughly the length of this order, **two live overwriters and not one**. The issuer re-asserted the cloud
producer with an ad-hoc build at 19:55:00Z. Row `NFRA_CLDGRPH-W5-S4` carries it.

**What would make the key two-writer again.** Four routes, in descending likelihood. (1) **Site Z's hook, which
is still installed** -- no repo act here touches it; its next commit on a filter path republishes the key with a
site-Z derive, and the two derives disagree by 53 nodes / 558 edges, so the disagreement is silent and
plausible-looking rather than loud. (2) **A clone checked out at or before `2e8dd90435`** running
`bash .tools/git-hooks/install-stitch-refresh.sh` -- the installer is idempotent on a marker string, prints
`OK: wired`, and needs no argument; retiring it here is exactly why that is now a two-step deliberate act.
(3) **A restore of `.tools/stitch-refresh` from before this commit** without restoring the refusal -- the
publish path was DELETED, not left dead, so this cannot happen by editing around a guard; it takes a
`git show` of a named hash. (4) **Andrew's word**, which is the only legitimate route and is the one the
tombstone documents, including the reminder that the two-writer question has to be settled first: either the
cloud producer stops or the local one does, and both cannot hold `s3://opal-313476888478-globgrph/stitch/*`.

**One reading the graders should not have to reconstruct.** The hook LINE in a device file carries no path
filter -- the filter lives inside the script it calls. So between the instruction act and the device act, every
commit on a clone whose line is still installed prints `sh: .../stitch-refresh-post-commit.sh: No such file or
directory` (row `W5-S2`, observed on this branch's first two commits and gone from the third). It is noise, not
a failure. But it means the ORDER of the three planes has a visible cost on every clone that lags, and site Z
will show it the moment this branch drains and before its integrator acts.
