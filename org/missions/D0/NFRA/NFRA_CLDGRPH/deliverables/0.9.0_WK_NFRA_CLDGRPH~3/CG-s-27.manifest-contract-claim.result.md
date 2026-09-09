# CG-s-27 -- THE MANIFEST CONTRACT: the claim a consumer can reject on

**TO:** `NFRA_CLDGRPH.TO-CG-F-7` · **cell:** CG-s-27 (decomp v0.6, s.1a) · **PRD:** v0.6 s.7 row S27
· **worker:** `0.9.0_WK_NFRA_CLDGRPH~3` · **branch:** `wk-cldgrph-6-3` · **worktree HEAD at hand-off:**
`c6b16d8f04` · **push state: LOCAL** (never pushed, never merged, never rebased).

S53's consuming half. One writer stamps four fields; one reader prints them beside the counts they
qualify and keeps the `!!` prefix wherever the claim is missing or the bytes have moved.

```json
{
  "field_spec": {
    "writer": "infra/aws/globgrph/_provenance.py write_manifest(db_path, *, source_kind, source_vintage, node_count, edge_count, edge_count_semantics, artifact_claim, edges_skipped_missing_endpoint=None)",
    "schema_version": "UNCHANGED at 1 -- the four keys are ADDITIVE, so every manifest written before this cell still parses and still reads; the reader renders a pre-CG-s-27 manifest LOUD (`!! provenance_claim: absent`) rather than refusing it. A version bump would have invalidated the two E-3 claim cards and the served-pointer consumers for no gain.",
    "fields": [
      {
        "name": "edge_count_semantics",
        "required": "YES -- keyword-only with NO default, so a producer that omits it raises TypeError AT THE CALL; a silent absent claim is impossible FROM THIS WRITER",
        "vocabulary": ["stored", "attempted"],
        "meaning": "stored = edge_count counts edges IN the store (a post-MERGE count read back). attempted = edge_count counts MERGE ATTEMPTS, an UPPER BOUND: MERGE is idempotent, so two identical input edges increment it twice and create one edge.",
        "validated": "ValueError on any value outside the vocabulary -- a free string is a claim nobody can reject on"
      },
      {
        "name": "artifact_claim",
        "required": "YES -- same TypeError arm",
        "vocabulary": ["served_projection", "interim_local_projection", "historical"],
        "meaning": "what the built store IS. served_projection = the artifact the estate serves/swaps in. interim_local_projection = a local projection of a cloud artifact (CG-s-20's ruling for the stitch surface). historical = a copy kept for reference, never a serve target.",
        "validated": "ValueError outside the vocabulary"
      },
      {
        "name": "content_sha256",
        "required": "computed BY THE WRITER from db_path -- the caller cannot get it wrong",
        "definition": "a FILE store: sha256 of its bytes. a DIRECTORY store: sha256 over the sorted `<relpath>:<sha256>` lines, one per regular file (order-stable, so the same tree hashes the same on two machines). Kuzu materialises the store as either shape depending on version; one definition covers both.",
        "null_when": "the store path does not exist or is unreadable -- null, never a placeholder digest"
      },
      {
        "name": "bytes_written_at",
        "required": "computed BY THE WRITER from db_path",
        "definition": "UTC ISO of the store's mtime at manifest time -- the MAX mtime across a directory store's files AND the directory itself, because rewriting an inner file does not always bump the directory's own mtime",
        "purpose": "W3-S11: bytes NEWER than the manifest become DETECTABLE instead of silently served as the vintage the manifest describes"
      }
    ],
    "legacy_alias": {
      "key": "edge_count_claim",
      "direction": "READ ONLY -- the writer never writes it; the reader accepts it as an alias of edge_count_semantics when the new key is absent and renders it `edge_count_semantics=<value> (legacy key)`",
      "why": "E-3 (CG-s-20) stamped this spelling on two main-workspace claim cards through a local _stamp_claim helper; those cards must still READ, and the second spelling must be VISIBLE rather than silently normalised away",
      "retires": "when no manifest on disk carries edge_count_claim -- i.e. after every store carrying an E-3 card is rebuilt through this writer or retired (F-1/F-6 own those two stores). One round, not indefinitely."
    },
    "reader": {
      "function": "infra/aws/globgrph/_provenance.py format_provenance_header(db_path, *, age_warn_hours, check_nessie_distance) -- unchanged signature",
      "claim_line": "printed on the line IMMEDIATELY AFTER the `DB: <name>  (N nodes / M edges)` line it qualifies",
      "bang_arms_kept_or_added": [
        "!! UNKNOWN VINTAGE -- no _build_manifest.json beside this DB.   (KEPT verbatim: the negative arm the PRD keeps)",
        "!! provenance_claim: absent -- counts carry no semantics (S53)  (ADDED: a manifest missing either claim key)",
        "!! source_kind <kind> -- the origin of these bytes is NOT identified  (ADDED: any source_kind beginning UNKNOWN, case-insensitive)",
        "!! BYTES NEWER THAN MANIFEST -- store mtime <t1> > bytes_written_at <t0>  (ADDED, W3-S11)",
        "!! BYTES DIFFER FROM MANIFEST -- content_sha256 declared <a>.. observed <b>.. at an unchanged mtime  (ADDED: the second axis, for a rewrite that restores the mtime)"
      ],
      "never_silent": [
        "a manifest with no bytes_written_at -> `bytes-vs-manifest: UNKNOWN (no bytes_written_at)`, never a pass",
        "an absent/unreadable store path -> `bytes-vs-manifest: UNKNOWN (store path absent or unreadable)`",
        "a store over 64 MiB -> `content_sha256 check SKIPPED (store N bytes > 67108864)`, the skip PRINTED"
      ],
      "tolerance": "2.0 s between store mtime and bytes_written_at before the BYTES NEWER arm fires -- filesystem timestamp granularity and the same-second manifest write must not false-fire"
    }
  },
  "call_sites_at_this_head": {
    "head": "c6b16d8f04 (worktree branch wk-cldgrph-6-3, before this order's commits)",
    "denominator": "3 of 3 remaining producers under infra/aws/globgrph/ (AST walk, not grep)",
    "producers": [
      {"file": "infra/aws/globgrph/kuzu_nessie_load.py", "line_before": 252, "line_after": 252, "edge_count_expr": "edges_stored", "edge_count_semantics": "stored", "artifact_claim": "served_projection", "why": "edges_stored is the post-MERGE count read back from the store (S8), not the merge_attempts upper bound"},
      {"file": "infra/aws/globgrph/kuzu_incremental_refresh.py", "line_before": 254, "line_after": 256, "edge_count_expr": "re_", "edge_count_semantics": "stored", "artifact_claim": "served_projection", "why": "rn/re_ are the POST-APPLY counts read back out of the store by the correctness guard immediately above the call; this DB is swapped in as the served projection"},
      {"file": "infra/aws/globgrph/kuzu_stitch_load.py", "line_before": 153, "line_after": 123, "edge_count_expr": "written", "edge_count_semantics": "attempted", "artifact_claim": "interim_local_projection", "why": "written increments once per MERGE EXECUTED and MERGE is idempotent, so it is an UPPER BOUND on the edges in the store; CG-s-20 ruled the stitch surface's home is JOIN_PROJECTION, so a store built here is an interim local projection"}
    ],
    "excluded": [
      {"file": "infra/aws/globgrph/kuzu_load.py", "call_site": 305, "state": "STILL PRESENT at this HEAD", "reason": "TO-CG-F-1 (slot ~1) retires it in this same round and it is outside this order's <paths>. NOT edited, NOT counted. Its local _stamp_claim def (:185) is the one LEGACY_HELPER_SITES deliberately does not count; when F-1 lands, both go with the file. IF F-1 DOES NOT LAND, kuzu_load.py's write_manifest call will raise TypeError on the required kwargs the moment it runs -- stated here because that is the one way this cell's edit can break a file it is forbidden to touch."}
    ],
    "helpers_removed": [
      {"file": "infra/aws/globgrph/kuzu_stitch_load.py", "removed": "_stamp_claim(manifest_path, *, edge_count_claim, artifact_claim) at :37-72 (36 lines incl. its docstring) plus its 8-line call site at :164-171; `git diff --numstat` reads 9 insertions / 45 deletions on this file", "replaced_by": "the two kwargs at the write_manifest call -- one write instead of a write plus a read-modify-rewrite of the file just written"}
    ]
  },
  "test_denominators": {
    "new_suite": {
      "file": "infra/aws/globgrph/tests/test_provenance_claim.py",
      "invocation": "timeout 120 python -m pytest infra/aws/globgrph/tests/test_provenance_claim.py -q -p no:cacheprovider",
      "collected": 13,
      "passed": 13,
      "failed": 0,
      "arms": {
        "a": "test_a_writer_stamps_all_four_claim_fields + test_a_claim_is_required_and_vocabulary_closed (2 tests: the four fields present and correct on a file store AND a directory store; TypeError on each omitted kwarg; ValueError on each out-of-vocabulary value; and the refused calls leave NO manifest behind)",
        "b": "test_b_header_prints_claim_beside_counts (the claim line is index+1 from the counts line, not merely present somewhere)",
        "c": "test_c_no_manifest_still_prints_unknown_vintage",
        "d": "test_d_unknown_source_kind_keeps_the_bang_prefix (parametrised x3: UNKNOWN_tarball, unknown_local_copy, UNKNOWN -- case-insensitive)",
        "e": "test_e_manifest_without_claim_prints_provenance_claim_absent",
        "f": "test_f_bytes_newer_than_manifest_reads_so + test_f_directory_store_inner_rewrite_is_caught + test_f_same_mtime_different_bytes_is_caught_by_the_hash + test_f_untouched_store_reads_ok (4 tests: the loud arm, the directory shape, the mtime-restored rewrite the hash catches, and the arm that must NOT fire)",
        "g": "test_g_legacy_edge_count_claim_reads_with_legacy_key"
      },
      "bounds_honoured": "TEMP paths, FAKE bytes, no kuzu import, no engine opened, no loader run, no main-workspace store or manifest touched"
    },
    "callers_existing": {
      "invocation": "timeout 120 python -m pytest infra/aws/globgrph/tests/test_kuzu_incremental_refresh.py infra/aws/globgrph/tests/test_projection_worker.py -q -p no:cacheprovider",
      "collected": 10,
      "passed": 10,
      "failed": 0,
      "collected_by_file": {"test_kuzu_incremental_refresh.py": 0, "test_projection_worker.py": 10},
      "note": "THE ZERO IS THE FINDING -- see NFRA_CLDGRPH-W3-S16. test_kuzu_incremental_refresh.py is a main()-style self-test under `if __name__ == \"__main__\"`; pytest collects nothing from it, so F7-AC4 cannot fail on a caller left behind. Measured directly: kwargs stripped -> still '10 passed', rc=0."
    },
    "other_readers_of_the_header": {
      "invocation": "timeout 200 python -m pytest .tools/tests/test_cg8_seam_retired_battery.py -q -p no:cacheprovider",
      "passed": 6,
      "why_run": "it is the only OTHER live caller of format_provenance_header in the repository (:268, :277) and the header gained four branches in this cell -- an unscoped check that the added lines did not disturb an existing consumer"
    },
    "whole_tests_home_unscoped": {
      "invocation": "timeout 300 python -m pytest infra/aws/globgrph/tests/ -q -p no:cacheprovider",
      "result": "2 failed, 79 passed, 1 skipped in 37.67s",
      "failed": ["test_code_heat_emit.py::test_emit", "test_code_heat_parity.py::test_parity"],
      "cause": "RuntimeError: PARITY_FAIL repo=portal: zero rows emitted (empty heat view) -- the portal submodule is EMPTY in this linked worktree (ls portal -> 0 entries). Neither module references _provenance or write_manifest (0 hits / 298 lines). NOT caused by this cell and not fixable inside its grant. Filed as NFRA_CLDGRPH-W3-S15."
    },
    "substitute_control": {
      "invocation": "timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_signature_bind.py",
      "result": "SITES_BINDING=3 of 3; STRIPPED_CALLER_REFUSED=3 of 3; BIND_CONTROL=FIRED",
      "why": "the discriminating instrument F7-AC4 was supposed to be, run WITHOUT opening an engine (this order's BOUNDS): every producer call site's argument NAMES bound against inspect.signature(write_manifest), and the same bind with the CG-s-27 kwargs removed refused at every site with 'missing a required argument: edge_count_semantics'"
    }
  },
  "rendered_header_examples": {
    "source": "verbatim from bash org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_header_arms.sh -- real renders of format_provenance_header on temp stores with fake bytes",
    "arm_1_claim_beside_counts": [
      "=== comp-kuzu provenance ===",
      "  DB: kuzu_db_healthy  (1166 nodes / 2488 edges)",
      "  counts: 1166 nodes / 2488 edges (edge_count_semantics=attempted; artifact_claim=historical)",
      "  source: nessie",
      "  built: 2026-09-09T18:35:28.021333+00:00 (age: 0.0h)",
      "  bytes-vs-manifest: OK (mtime 2026-09-09T18:35:28.021334+00:00; content_sha256 matches)",
      "============================"
    ],
    "arm_2_no_manifest": [
      "  DB: kuzu_db_no_manifest",
      "  !! UNKNOWN VINTAGE -- no _build_manifest.json beside this DB.",
      "  !! Build provenance is unverifiable; rebuild via the loader to stamp it."
    ],
    "arm_3_unknown_kind": [
      "  DB: kuzu_db_unknown_kind  (1166 nodes / 2488 edges)",
      "  counts: 1166 nodes / 2488 edges (edge_count_semantics=stored; artifact_claim=historical)",
      "  source: UNKNOWN_tarball",
      "  !! source_kind UNKNOWN_tarball -- the origin of these bytes is NOT identified; the counts and the vintage below are unverified (S53)."
    ],
    "arm_4_claim_absent": [
      "  DB: kuzu_db_claimless  (1166 nodes / 2488 edges)",
      "  counts: 1166 nodes / 2488 edges (edge_count_semantics=absent; artifact_claim=absent)",
      "  !! provenance_claim: absent -- counts carry no semantics (S53): this manifest does not say whether edge_count counts EDGES STORED or MERGE ATTEMPTS, so a consumer cannot reject on it. Rebuild through _provenance.write_manifest to stamp it.",
      "  bytes-vs-manifest: UNKNOWN (no bytes_written_at)"
    ],
    "arm_5_bytes_newer": [
      "  DB: kuzu_db_bytes_newer  (1166 nodes / 2488 edges)",
      "  counts: 1166 nodes / 2488 edges (edge_count_semantics=attempted; artifact_claim=interim_local_projection)",
      "  built: 2026-09-09T18:35:28.035134+00:00 (age: 0.0h)",
      "  !! BYTES NEWER THAN MANIFEST -- store mtime 2026-09-09T18:36:28.039672+00:00 > bytes_written_at 2026-09-09T18:35:28.035135+00:00; the counts above describe an OLDER store (W3-S11)"
    ],
    "arm_5_negative_control": "the SAME store rendered BEFORE the rewrite carried no BYTES NEWER line (ARM_BYTES_NEWER_NEGATIVE_CONTROL=clean-before-rewrite) -- the arm is a measurement, not a constant"
  },
  "surprise_rows_filed": [
    "NFRA_CLDGRPH-W3-S14 -- OBSERVATION / INERT: the claim has no served render to reach",
    "NFRA_CLDGRPH-W3-S15 -- OBSERVATION / INERT: two red tests in the ordered tests home, from an empty portal submodule",
    "NFRA_CLDGRPH-W3-S16 -- OBSERVATION / ARMED (disarm_owner 0.8.0_AE_CloudComp): F7-AC4's control is dead; the in-grant substitute that is not"
  ]
}
```

## 1. What changed, in the order the deliverable names

**(1) The writer.** `write_manifest` gained two REQUIRED keyword-only parameters and computes two more
fields itself. The choice that carries the cell is that `edge_count_semantics` and `artifact_claim` have
**no defaults**. A default -- even `"unknown"` -- would have made every producer's omission silent and
recoverable-looking, which is precisely the state S53 objects to. With no default, a producer that does not
say what its number means does not run. The two hashes are computed from `db_path` rather than passed,
because a caller that must supply a digest of its own output is a caller that can supply the wrong one.

**(2) The reader.** Four `!!` arms and one `counts:` line. The `!! UNKNOWN VINTAGE` branch is untouched --
it is the negative arm the PRD keeps and the arm E-3's claim cards were measured to silence (W3-S8), so it
had to survive this edit unchanged and it did (arm 2 above renders it verbatim). The new arms sit strictly
*inside* the manifest-present path, so a manifest-less store still takes the old early return.

**(3) The three call sites.** Kwargs only, exactly as the face bounds it -- no derive or pin logic touched,
so slot ~2's F-4 edits to two of these files stay textually separable at the drain. The one structural
removal is `kuzu_stitch_load.py`'s local `_stamp_claim` helper: with the claim required at the writer, a
post-hoc read-modify-rewrite of the file just written is dead code, and leaving it would have kept a second
way to stamp a claim -- the two-carrier defect the row it was born from was filed against.

## 2. Can a consumer now REJECT on the claim? (the F7-AC5 reading is s.3 of this record)

Yes at the manifest, not yet at a served surface. `read_manifest(db)["edge_count_semantics"] != "stored"`
is a rejection a consumer can write today, on a field that is present-or-loudly-absent and drawn from a
two-value closed set. What does not exist is a **serve-path caller** of `format_provenance_header`: neither
`projection_client.py` nor `projection_server.py` nor `kuzu_cli.py` references `_provenance` at all
(W3-S14). The header is correct and the fields are stamped; the surface that would show them to an operator
is not wired, and wiring it is outside this order's `<paths>`.

## 3. THE CONTRACT, READ -- F7-AC5 (a reading act, NO verdict; graded by `3.0.0_SA_CVO` at L9)

### 3a. Which field, which value, at which read site -- what a consumer can refuse on

Three refusals are now expressible, in increasing strength.

*The weakest and most useful:* `artifact_claim != "served_projection"`. A consumer that intends to answer a
question about the estate's graph can refuse an `interim_local_projection` or a `historical` store outright,
without knowing anything about how either was built. This is the refusal E-3 wanted and could not have,
because its two cards were written by a helper only two of the four producers called: a consumer reading a
manifest with no card could not tell "not a served projection" from "nobody said". Now it can -- the absent
case renders `!! provenance_claim: absent` and reads `edge_count_semantics=absent` in a field, not as a
missing key a naive `.get()` turns into `None` and a truthiness test turns into "fine".

*The sharper one:* `edge_count_semantics == "attempted"` means the edge number is an **upper bound**. Any
consumer that compares two edge counts -- a parity check, a drift alarm, a "did tonight's build lose edges"
question -- is comparing an upper bound against a true count the moment one side is a stitch store, and that
comparison has been silently wrong for as long as both producers have written the same field name. The read
site is `read_manifest(db).get("edge_count_semantics")`, one dict lookup, no engine.

*The strongest, and the one that did not exist in any form before:* `bytes_written_at` and `content_sha256`
let a consumer refuse a manifest **that no longer describes the bytes beside it**. Every other field in this
schema describes the build; these two describe the *binding between the manifest and the store*, which is
the thing that actually goes stale. A consumer can now ask "is this manifest still about this store?" and
get an answer rather than an assumption.

The honest limit: all three refusals are available to a consumer that reads the manifest. None is *enforced*
anywhere. The consuming half of S53 is now possible; it is not yet mandatory, and this cell was not scoped
to make it so.

### 3b. What the served header will show the morning after F-4's derive lands

**Nothing -- and this is the one answer in this reading I would most want the L9 seat to check.** F-4's
derive, running through the cloud worker, will call this writer and its manifest will carry
`edge_count_semantics="stored"`, `artifact_claim="served_projection"`, a `content_sha256` over the built
store and a `bytes_written_at`. Rendered, that manifest produces arm 1 above. But *nothing renders it*: the
repo-wide census (W3-S14) finds one definition of `format_provenance_header` and three live call sites -- two
in test files, one in a sensor script under `org/tier2_senior/`. The C-S27 observation that "the served
header for `kuzu_db` still reads '1166 nodes / 2488 edges' with nothing beside it" describes a header that,
at this HEAD, no serving code path emits at all. So the morning after F-4 lands, an operator running the
serving client sees exactly what they see today; a seat that calls `format_provenance_header(db)` by hand
sees the full claim. The gap between those two is a wiring cell, and it is not this one.

There is a second-order caution for whoever cuts that wiring cell: `content_sha256` on a large served store
is not free, and the header renders on *every* invocation. This implementation already refuses to hash above
64 MiB and prints the skip -- but a serve path should probably compare mtime only, and reach for the hash
on demand.

### 3c. What the legacy alias costs, and when it retires

One spelling of one concept alive in two forms for one round, read-only, and rendered with `(legacy key)` so
it is never invisible. The cost is real but bounded and it is a *reading* cost: a future seat greping for
`edge_count_semantics` will miss the two E-3 cards on disk, and a future schema census will count two keys
where the taxonomy has one. The mitigation is that the writer can only ever produce the new spelling, so the
legacy set is closed at exactly the manifests already on disk -- it cannot grow.

It retires when no manifest on disk carries `edge_count_claim`. Concretely: the two main-workspace claim
cards belong to stores F-1 and F-6 own; when those stores are retired or rebuilt through this writer, the
alias has no reader left and the four lines that implement it can go. Naming the trigger matters more than
naming a date -- "one round" is how a legacy key becomes permanent. The retiring seat should also decide
whether `attempted` versus `merge_attempts` matters: E-3's cards spell the *value* `merge_attempts` while
this vocabulary spells it `attempted`, and the reader currently passes the legacy value through verbatim
rather than translating it, so a card renders `edge_count_semantics=merge_attempts (legacy key)`. That is
honest -- it shows what is actually written -- but it means the closed vocabulary is closed only for values
this writer produced.

### 3d. Could `!! BYTES NEWER THAN MANIFEST` false-fire on a legitimate copy?

**Yes, and this is the arm most likely to cry wolf.** The mechanism: the projection worker fetches a store
from S3 and writes it locally. The manifest is written by the *producer*, at production time, stamping the
producer's own local mtime. If the manifest travels with the store and the store's bytes are re-created on
the consumer's disk, the local mtime is the *copy* time -- necessarily later than `bytes_written_at`, often
by hours. The arm fires, loudly, on a store that is perfectly faithful.

Three things bound the damage, and none eliminates it:

1. **S3 has no client-settable mtime for a downloaded object.** `aws s3 cp` sets the local file's mtime to
   *now* unless the caller restores it. So the false fire is not a possibility, it is the *default* on any
   copy path that does not think about it. The disciplinary answer is that a copy path should either
   re-stamp the manifest through this writer after landing the bytes (which is correct: the local store's
   binding *is* new) or preserve mtimes deliberately.
2. **The hash is the discriminator and it is already computed.** A false fire has `content_sha256` matching
   and only the mtime moved; a true fire usually has both moved. This implementation checks mtime *first*
   and returns on the loud arm without consulting the hash -- which is the cheap ordering, and the wrong one
   for exactly this case. A serve-path wiring cell should invert it: mtime newer AND hash differs -> `!!
   BYTES NEWER`; mtime newer but hash matches -> a quieter `bytes-vs-manifest: copied (mtime moved, content
   identical)`. I did not make that change here because the face bounds this cell to the arms it names and
   because inverting it costs a hash on every render, which is a serve-path decision, not a writer one.
3. **The tolerance is 2 seconds**, which handles filesystem granularity and nothing else. It is not a
   defence against a copy.

So: the arm is correct as specified and as tested, it will false-fire on the projection worker's copy path
the first time that path renders a header, the fix is a four-line reordering plus a hash on the render, and
the reason it is not in this commit is that it is a change to what the arm *means* rather than to whether it
works. That is the L9 seat's call, and W3-S14's finding -- that no serve path renders this header yet --
means nobody is currently exposed to it.

### 3e. What this order deliberately did not do

Did not touch `kuzu_load.py` (F-1's, outside the grant) though it is still present and its `write_manifest`
call will TypeError on the required kwargs the moment it runs -- stated in the record and in the census
output rather than fixed. Did not edit `projection_server.py`: the file needs no edit, and finding out *why*
is W3-S14. Did not run any loader, open any store with an engine, or touch a main-workspace store or its
manifest. Did not correct `_provenance.py`'s module docstring where it claims `kuzu_cli.py` prints this
header on every `comp-kuzu` invocation (it does not, measured) -- correcting the sentence without the wiring
moves a false claim rather than removing it, and the wiring is out of grant. Did not give
`test_kuzu_incremental_refresh.py` a pytest-collectable surface, which would open kuzu engines this order's
BOUNDS forbid outright; filed as W3-S16 and routed to the lane instead.
