# CG-s-19 -- THE RESIDUAL LOCAL STORES, DISPOSITIONED

**Cell:** CG-s-19 (decomposition v0.5) · **Task order:** `NFRA_CLDGRPH.TO-CG-E-3` · **Worker:** `0.9.0_WK_NFRA_CLDGRPH~3`
· **Worktree:** `C:/tmp/wk-cldgrph-5-3`, branch `wk-cldgrph-5-3`, HEAD `de466829e0` at the cut · **Recorded:** 2026-09-09 ~16:0xZ
· **Lane:** `0.8.0_AE_CloudComp`.

**WHAT THIS ORDER DID NOT DO, first, because it is the load-bearing bound:** nothing was deleted, moved, renamed or
rebuilt; no store was opened with any engine (`kuzu.Database` CREATES an absent store on open -- the CVO's C-S19 --
so every count below comes from a MANIFEST file or from `stat`, never from a query); no loader was run; no snapshot
was downloaded; nothing was written to S3. The two store files' sizes and mtimes are re-measured against the
issuer's census AFTER every act of this order and are unchanged (`STORE_BYTES_UNCHANGED=2 of 2`).

---

## 1. THE CENSUS (read-only), MAIN WORKSPACE `C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/`

| artifact | bytes | mtime (local) | git standing | manifest | builder | last known reader |
|---|---|---|---|---|---|---|
| `kuzu_db` | 9,224,192 | 2026-06-12 09:55 | gitignored (`infra/aws/globgrph/.gitignore:1`) | `kuzu_db._build_manifest.json`, 327 B before this order | `kuzu_load.py` (tracked) | NONE. 0 readers of 487 .py files (E3-AC2); the CVO's C-S22 read 0 of 982 over a wider scope |
| `kuzu_load.py` | 11,013 (pre-edit) | 2026-07-25 07:32 | TRACKED at HEAD | n/a | n/a (it IS the builder) | n/a -- BUILDER, not reader: `kuzu_load.py:30` names `kuzu_db` because it constructs `DEFAULT_DB_PATH` |
| `kuzu_ac7.db` | 4,050,944 | 2026-06-12 10:57 | gitignored (`infra/.gitignore:82`, `*.db`) | NONE before this order | `kuzu_ac_traversals.py`'s ancestor (NFRA_GLOBGRPH.ITEM-3, June 2026); no provenance record survives | NONE. `kuzu_ac_traversals.py` at `de466829e0` names `kuzu_ac7` in no CODE line; its only `--db` string is a docstring saying the flag is GONE |
| `.kuzu_nessie_load.0628067ab4da5610.lock` | 5 (`48708`) | 2026-09-04 12:53 | **neither tracked nor gitignored** | n/a | `kuzu_nessie_load.py:337-365` | n/a -- read only by `_acquire_singleton_or_exit()` for the SAME target db, which cannot be identified (W3-S9) |

Carried by their store, not dispositioned on their own: `kuzu_db._build_manifest.json` (edited by this order) and the
EMPTY directory `kuzu_ac7/` (0 entries, mtime 2026-06-09 11:08 -- an earlier build's leftover shell, not a store).
NOT this cell's: `kuzu_stitch_db` + its manifest (CG-s-20, TO-CG-E-4).

**`kuzu_db._build_manifest.json`, quoted whole BEFORE this order:**

```
{ "built_at": "2026-06-12T13:55:02.779461+00:00", "edge_count": 2488, "node_count": 1166, "schema_version": 1,
  "source_kind": "tarball",
  "source_vintage": { "snapshot_bucket": "opal-313476888478-globgrph", "snapshot_path": null,
                      "tarball_key": "snapshots/20260612/graph-20260612.tar.gz" } }
```

**The CVO's P7 row, quoted verbatim** (`org/tier1_exec/3.0.0_SA_CVO/deliverables/DIAL_RECORD_comp-kuzu_20260804.md:19`
@`de466829e0`):

> `| P7 residue audit | CENSUS DONE, deletions ruled-not-taken | NECESSARY: kuzu_nessie_db(+manifest), kuzu_cli.py, loaders, incremental_refresh. HISTORICAL: kuzu_db (Jun-12 scratch, 1,166 nodes), kuzu_cost_enrich.py (TO-D4 one-shot). HISTORICAL-AT-RISK (do NOT delete): kuzu_ac7.db + kuzu_ac_traversals.py -- tied to open NFRA_GLOBGRPH.ITEM-3 (AC-gates honestly UNVALIDATED). AT-RISK: kuzu_stitch_db = K4 |`

Two of the four artifacts P7 names have MOVED since 2026-08-04: `kuzu_cost_enrich.py` was DELETED on the CTO's ruling
@`1266d65641`, and `kuzu_ac_traversals.py` was REPOINTED through the served projection in TO-CG-D-7 pass 4. That is
the fact the re-statement now has to be made against, and it is why W3-S6 exists.

## 2. THE READERS PROBE

`no_readers.sh` (this folder) runs `_readers_ast.py` -- an **ast walk**, not a text grep -- twice: over the four tool
homes, and over `plant_e3/`, which holds one file that opens both stores and one that names them only in a docstring,
a comment and a prose string. Measured at `de466829e0`:

```
READERS=0 of 487 files
BUILDER_DECLARED=infra/aws/globgrph/kuzu_load.py
  BUILDER_EXCLUDED infra/aws/globgrph/kuzu_load.py:30 [PATH-SHAPED+ARG-OF:join+BOUND-TO:DEFAULT_DB_PATH] kuzu_db
READER_PROBE_CONTROL=FIRED     (the planted opener was CAUGHT -- 2 reader lines in a 2-file control scope)
READER_BAND_CONTROL=FIRED      (the docstring/comment/prose specimen was SEEN and scored ZERO readers)
PROSE_MENTIONS=3  DOCSTRING_MENTIONS=1  BUILDER_HITS=1  PARSE_FAILURES=0
NEAR_MISS_GLUED_FILES=2        (org/modules/graph/tsgraph_spike/load_scratch_kuzu.py 'out/scratch_kuzu_db';
                                org/modules/graph/tests/test_blast_kuzu_projection.py '__no_such_kuzu_db_zzz__')
```

Three things the zero is NOT hiding, each printed beside it rather than dropped: the three PROSE mentions
(`.tools/tool_index.py:1064` and `:1965`, `org/modules/graph/comp_aws_cli.py:2871` -- tool descriptions that name
`kuzu_db` in a sentence and open nothing), the one DOCSTRING mention
(`.tools/tests/test_cg7_status_read_battery.py:1`), and the two NEAR-MISS files whose tokens are GLUED into a longer
identifier and are therefore a DIFFERENT artifact. `PARSE_FAILURES=0` is printed so an unread file cannot hide inside
the denominator.

## 3. THE DISPOSITION RECORD

```json
{
  "cell": "CG-s-19",
  "task_order": "NFRA_CLDGRPH.TO-CG-E-3",
  "recorded_by": "0.9.0_WK_NFRA_CLDGRPH~3",
  "recorded_at": "2026-09-09T16:05Z",
  "vintage": "de466829e0",
  "workspace": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph",
  "disposition_vocabulary": [
    "RETIRE_WITH_TOMBSTONE",
    "ARCHIVE_UNDER_PROJECT",
    "KEEP_WITH_NAMED_READER",
    "HOLD_PENDING_P7"
  ],
  "p7_row_id": "NFRA_CLDGRPH-W3-S6",
  "readers_probe": {
    "instrument": "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/_readers_ast.py (ast walk)",
    "scopes": [".tools", "org/modules/graph", "org/modules/heatmap", "infra/aws/globgrph"],
    "readers": "READERS=0 of 487 files",
    "builder_declared": "BUILDER_DECLARED=infra/aws/globgrph/kuzu_load.py",
    "builder_excluded_line": "infra/aws/globgrph/kuzu_load.py:30 [PATH-SHAPED+ARG-OF:join+BOUND-TO:DEFAULT_DB_PATH]",
    "positive_control": "READER_PROBE_CONTROL=FIRED",
    "band_control": "READER_BAND_CONTROL=FIRED",
    "prose_mentions": 3,
    "docstring_mentions": 1,
    "parse_failures": 0,
    "near_miss_glued_files": 2
  },
  "artifacts": [
    {
      "artifact": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_db",
      "size_bytes": 9224192,
      "mtime": "2026-06-12 09:55 local (2026-06-12T13:55:12Z)",
      "manifest": "kuzu_db._build_manifest.json -- built_at 2026-06-12T13:55:02.779461+00:00, node_count 1166, edge_count 2488, schema_version 1, source_kind tarball, source_vintage.tarball_key snapshots/20260612/graph-20260612.tar.gz (bucket opal-313476888478-globgrph); THIS ORDER ADDED edge_count_claim=merge_attempts and artifact_claim=historical and changed nothing else (6 of 6 pre-existing keys byte-identical)",
      "disposition": "HOLD_PENDING_P7",
      "owner": "3.0.0_SA_CVO",
      "reason": "A 1,166-node June-12 copy of THIS graph, built from the S3 snapshot tarball, sitting one directory away from the served projection's tooling with zero readers (0 of 487) and a manifest whose edge_count is an upper bound, not a count. It is exactly the 'second, older copy' FWD-7 asks about, and this worker's reading is that it should RETIRE with a tombstone -- but P7 rules deletions not-taken over its whole census, kuzu_db included, and only P7's author may move that. So the disposition ON THE RECORD is HOLD, the store is untouched, and the ask is filed as NFRA_CLDGRPH-W3-S6.",
      "later_act_if_any": "RETIRE_WITH_TOMBSTONE by 0.8.0_AE_CloudComp -- delete kuzu_db and its manifest and leave a tombstone naming the vintage (snapshots/20260612/graph-20260612.tar.gz), the counts, the 0-reader measurement and this record -- ONLY AFTER 3.0.0_SA_CVO re-states or lifts P7. Not this order's act.",
      "p7_status": "HISTORICAL (not AT-RISK). The census-wide 'deletions ruled-not-taken' covers it; the explicit do-NOT-delete is on kuzu_ac7.db. Precedent that HISTORICAL is deletable by ruling: kuzu_cost_enrich.py, the other HISTORICAL item, was DELETED on the CTO's ruling @1266d65641."
    },
    {
      "artifact": "infra/aws/globgrph/kuzu_load.py (TRACKED)",
      "size_bytes": 11013,
      "mtime": "2026-07-25 07:32 local (pre-edit; this order edits the tracked file in the worktree, not the main workspace copy)",
      "manifest": "n/a -- it is the BUILDER. It calls _provenance.write_manifest(...) at kuzu_load.py:272-278 and, as of this order, _stamp_claim(mpath, edge_count_claim='merge_attempts', artifact_claim='scratch') immediately after.",
      "disposition": "KEEP_WITH_NAMED_READER",
      "owner": "0.8.0_AE_CloudComp",
      "reason": "P7 classes 'loaders' NECESSARY, and this is the only builder of kuzu_db: retiring the store without retiring its builder would leave a one-command path back to a second local copy, and retiring the builder while the store is held would strand the store. Its named live consumer is the operator path 'comp-kuzu --db-path <scratch>' -- comp-tools.yaml:144 declares the explicit --db-path surface for exactly the scratch DBs (kuzu_db tarball, kuzu_stitch_db, kuzu_ac7.db) -- and it is named a BUILDER, not a reader, in the E3-AC2 walk, where its only token hit (line 30, DEFAULT_DB_PATH) is declared and excluded. It carries the S53 obligation as a STAMP rather than as a manifest field.",
      "later_act_if_any": "If P7 is lifted and kuzu_db retires, kuzu_load.py's own retirement becomes a live question for 0.8.0_AE_CloudComp -- and the C3 moratorium binds it: a rebuilt local store is the shadow pipeline the doctrine vetoes. Not this order's act and not asked for here.",
      "p7_status": "NECESSARY ('loaders'). Unmoved by this order."
    },
    {
      "artifact": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_ac7.db",
      "size_bytes": 4050944,
      "mtime": "2026-06-12 10:57 local",
      "manifest": "NONE existed. THIS ORDER CREATED kuzu_ac7.db._build_manifest.json as a CLAIM CARD, not a build stamp: artifact_claim=historical, edge_count_claim=unknown, source='unknown (no builder manifest; NFRA_GLOBGRPH.ITEM-3, June 2026 ...)', source_kind='UNKNOWN (claim card written by CG-s-19, NOT a build stamp)', built_at='UNKNOWN (no build record ...)', NO node_count and NO edge_count -- because no count of this store exists that was not produced by opening it. Side effect filed as NFRA_CLDGRPH-W3-S8.",
      "disposition": "HOLD_PENDING_P7",
      "owner": "3.0.0_SA_CVO",
      "reason": "This is the artifact P7 names do-NOT-delete by name, and the hold's stated reason -- 'tied to open NFRA_GLOBGRPH.ITEM-3 (AC-gates honestly UNVALIDATED)' -- attaches the store to kuzu_ac_traversals.py, which no longer reads it: pass 4 of TO-CG-D-7 repointed the traversals through the served projection and removed its --db flag, so at de466829e0 nothing names kuzu_ac7 in CODE anywhere in the four tool homes. The premise of the hold has changed and the hold has not; only its author may say whether it still stands. HOLD is the honest record of that, and the store is untouched.",
      "later_act_if_any": "3.0.0_SA_CVO re-states (-> the store stays, carded, with the ITEM-3 tie re-affirmed) or lifts (-> RETIRE_WITH_TOMBSTONE or ARCHIVE_UNDER_PROJECT under NFRA_GLOBGRPH.ITEM-3 by 0.8.0_AE_CloudComp, the tombstone carrying what the card says: that nobody knows what built it). Either way a LATER act.",
      "p7_status": "HISTORICAL-AT-RISK, do NOT delete -- RE-STATEMENT ASKED FOR in NFRA_CLDGRPH-W3-S6, ARMED, disarm_owner 3.0.0_SA_CVO."
    },
    {
      "artifact": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/.kuzu_nessie_load.0628067ab4da5610.lock",
      "size_bytes": 5,
      "mtime": "2026-09-04 12:53 local",
      "manifest": "n/a -- a 5-byte singleton lock whose content is the holder pid '48708' (not running: tasklist /FI 'PID eq 48708' returns 'No tasks are running which match the specified criteria').",
      "disposition": "RETIRE_WITH_TOMBSTONE",
      "owner": "0.8.0_AE_CloudComp",
      "reason": "Residue with an UNRECOVERABLE REFERENT. Its name is sha256(normcase(abspath(db_path)))[:16] (kuzu_nessie_load.py:363-365) and no plausible local db path hashes to 0628067ab4da5610 -- 3,262 candidates tried with the loader's own expression, 0 matches, with a positive control that reproduces the distinct known hashes of kuzu_nessie_db, kuzu_db, kuzu_stitch_db and kuzu_ac7.db. So it locks a target that no longer exists and cannot be named, its holder is dead, and the loader's own stale-lock self-clear (kuzu_nessie_load.py:427-431) can never fire for it because that path runs only for a caller acquiring the SAME target. It is INERT -- the singleton refuses only same-target callers -- but it is not KEEPable: an artifact that cannot name what it protects has no named reader. It is also the one residue item that is neither tracked nor gitignored, so it sits in the untracked set where a wide git add could sweep it in.",
      "later_act_if_any": "DELETE the lock file and leave a one-line tombstone in the lane's record naming the hash, the dead pid and this measurement. NOT taken here: TO-CG-E-3 deletes nothing, and the deletion is trivial to execute once the record exists. P7 does not cover it, so it is not held on the CVO.",
      "p7_status": "OUT OF SCOPE OF P7 -- the lock post-dates the audit by a month (2026-09-04 vs 2026-08-04) and is named nowhere in it. Owner is the lane, not the CVO."
    }
  ]
}
```

## 4. THE CLAIM FIELDS (S53)

**The builder** (`infra/aws/globgrph/kuzu_load.py`, the one tracked edit): a module-level `_stamp_claim()` re-opens the
manifest `_provenance.write_manifest` just wrote and adds `edge_count_claim` and `artifact_claim`, called from `load()`
with those two keyword arguments. `bash .tools/commit-gate.sh infra/aws/globgrph/kuzu_load.py` -> `OK: pre-commit gate
clean for 1 of 1 file(s)`.

Why the value is `merge_attempts`: `kuzu_load.py` stamps `edge_count=loaded` where `loaded = len(g["edges"]) - skipped`
and `skipped` counts only the CREATEs that RAISED. A `CREATE` whose `MATCH (a {arn: $src}), (b {arn: $tgt})` binds
nothing writes no edge and raises nothing, so the stamped number is an **upper bound** on the edges present -- one field
name, two possible semantics, and (row S53) four modules writing that schema through one writer.

Why it is stamped in `kuzu_load.py` and not as a `write_manifest` keyword: `_provenance.write_manifest`'s signature is
keyword-only and closed, and `infra/aws/globgrph/_provenance.py` is **not in this order's `<paths>`**. That is filed as
**NFRA_CLDGRPH-W3-S7**, with the other half of the same finding: no consumer reads the claim either --
`format_provenance_header` prints `(1166 nodes / 2488 edges)` and never the field beside it.

**The stores.** `apply_manifest_claims.py` (this folder, idempotent, prints the file before and after):

| manifest | act | fields |
|---|---|---|
| `kuzu_db._build_manifest.json` | EDIT IN PLACE, 6 of 6 pre-existing keys asserted unchanged | `edge_count_claim: merge_attempts`, `artifact_claim: historical` |
| `kuzu_ac7.db._build_manifest.json` | CREATED (claim card) | `edge_count_claim: unknown`, `artifact_claim: historical`, `source: unknown (...)` |

`edge_count_claim: unknown` is a **third value** beside the `merge_attempts`/`edges` pair the order names: an artifact
with no `edge_count` field can honestly claim neither, and inventing one would be the defect this cell exists to fix.
Recorded rather than assumed.

## 5. E3-AC6 -- THE DISPOSITION READING (a reading act; no verdict; graded by `3.0.0_SA_CVO` at L9)

**`kuzu_db` -- HOLD_PENDING_P7, reading RETIRE_WITH_TOMBSTONE.** This is the artifact FWD-7 is actually about. It is not
a *different* graph a reader might stumble into; it is a June-12 copy of **this** graph with the same schema
(`CloudNode`/`CloudEdge`), 1,166 nodes, sitting beside the tooling that serves the projection. Everything that makes a
stale copy dangerous is present except a reader. The three arguments for retiring it: (i) its counts are wrong in a way
its own field name conceals; (ii) it is reachable by one flag (`comp-kuzu --db-path`) from a surface that advertises
scratch DBs; (iii) it is HISTORICAL in P7's own taxonomy, and P7's other HISTORICAL item has already been deleted by
ruling. The one argument against retiring it *now* is decisive and procedural: the hold is not this seat's to move.

**`kuzu_load.py` -- KEEP_WITH_NAMED_READER.** A builder is not a reader, and the temptation is to score it as one
because it names the store. Retiring the store without it leaves a one-command path back; retiring it without the store
strands the store. It stays, and it now stamps the claim its own numbers need.

**`kuzu_ac7.db` -- HOLD_PENDING_P7.** The interesting one: the hold's REASON has expired and the hold has not. P7 tied
the store to `kuzu_ac_traversals.py` and to open ITEM-3 gates; pass 4 cut the tie, and at `de466829e0` no CODE line in
the four tool homes names `kuzu_ac7`. What the author's re-statement changes is precisely this: a re-statement on the
ORIGINAL ground ("ITEM-3 is still open") keeps a store nothing can reach; a re-statement on NEW ground would have to say
what now depends on it; a LIFT converts the entry to RETIRE_WITH_TOMBSTONE or ARCHIVE_UNDER_PROJECT and hands the act to
the lane. It has no manifest and no surviving builder record, so whatever happens to it, the honest card written this
turn is the most anyone can say about it without opening it -- which is the one thing nobody may do.

**The lock -- RETIRE_WITH_TOMBSTONE.** Filed by its own row (W3-S9) because it taught something: a lock keyed by a
one-way hash **cannot say what it locked**. It is inert and it is unreadable, and those are different properties: the
first says leave it alone, the second says it can never be re-attached to a target, so it will never self-clear. Delete
it, note the hash and the dead pid, move on.

**Does FWD-7 close by DISPOSITION or only by DELETION?** Honestly: **by deletion, not by this record.** FWD-7's accept
reads "there is no second, older copy anyone could still be reading from". Two clauses. The *reading* clause is met and
measured -- 0 readers of 487 files, controls fired, the builder declared, the near-misses named. The *existence* clause
is not: `kuzu_db` is a second, older copy, and it is still there. What this order can prove is UNREACHABILITY; what
FWD-7 asks for at full strength is ABSENCE. A disposition record converts an unowned artifact into an owned one with a
named later act -- that is real, and it is not the same thing. The gap is exactly one act wide (a delete plus a
tombstone) and it is gated on one seat's word, which is why W3-S6 exists and why it is ARMED.

**What this order deliberately did not do:** it did not delete, move or rebuild anything; it did not open a store to
count it (`kuzu.Database` would have CREATED an absent one); it did not run a loader; it did not lift, narrow or
reinterpret P7 on its author's behalf; it did not widen the claim field into `_provenance.py` or into the other three
producers, though that is where the field belongs; and it did not treat the CVO's re-statement as something to wait
for -- the record is filed, the ask is filed, and the order is finished.

## 6. THE SCRIPTS

| script | criterion | what it can FAIL on |
|---|---|---|
| `dispositions_recorded.sh` | E3-AC1 | a missing/invalid disposition, owner or reason; an unresolvable `p7_row_id`; a planted ownerless entry passing the same parser |
| `no_readers.sh` | E3-AC2 | any reader in the four tool homes; a dead walker (positive control); a prose mention scored as a reader (band control) |
| `stores_untouched.sh` | E3-AC3 | a missing artifact; a store whose bytes or mtime moved from the cut's census (constants, not re-derived) |
| `manifest_claims.sh` | E3-AC4 | a builder that stops stamping the two claim keywords; a staying store missing either field |
| `commit_gate_all.sh` | E3-AC5 | any `.py` this order touches failing `py_compile` / ds-precommit / ruff |
