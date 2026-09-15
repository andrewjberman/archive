# EXERCISE_FWD1_SEARCH -- the second worker's search of the firm N+1 pipeline (LGIC_ENFORCE EN-d-2, FWD-1)

Worker `0.9.0_WK_LGIC_ENFORCE~8`, task order `LGIC_ENFORCE.TO-EN-d-2`, working in worktree `wk-lgic-enforce-1-8-d2`
(cut from CLOUD @9a05002d39). This is a new spawn. The same serial slot wrote the pipeline in EN-d-1, but that worker
has ended and this one did not write the file.

## What was searched

`deliverables/EXERCISE_FWD7.md` (merged @dd261d8b85) names the file in its json block. `scratch_branch` is
`prac-lgic-enforce-d1`. `commits.generated` is `92bc3b51bf2aac81152cd270aa146cadfb5159c7`. `pipeline_path` is
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~8/pipeline/qwt_positions.py`. The branch is local
and was never pushed. `git rev-parse --verify prac-lgic-enforce-d1` resolves to that commit, and
`git merge-base --is-ancestor 92bc3b51bf prac-lgic-enforce-d1` exits 0. The file was read at that commit with
`git show 92bc3b51bf2aac81152cd270aa146cadfb5159c7:<pipeline_path>` (rc 0), not from any working tree.

**Denominator: 1 file, 64 lines, 2,499 bytes.** `git ls-tree` at the commit lists 1 file at that path, and `wc -l` on
the shown bytes prints 64.

## Instrument and patterns

The search is `grep -F -i -c` over the `git show` output, one run per pattern, plus one combined
`grep -E -i -n 'opal-data-|s3://|(bronze|silver|gold|platinum)/'` that lists every matching line. It is case-insensitive.
The six patterns are the order's: a bucket name (`opal-data-`), `s3://`, and the four tier or key prefixes
`bronze/`, `silver/`, `gold/`, `platinum/`.

This is not the checker's instrument. `check_en.py d2-zero` re-searches the same bytes with its own Python regex
(`s3://|opal-data-[a-z0-9-]+|\b(?:bronze|silver|gold|platinum)/`). The two agree: 0 hits on the pipeline, 1 on the
planted copy.

## Result: 0 storage-location literals

| pattern | matching lines (of 64) |
|---|---|
| `opal-data-` | 0 |
| `s3://` | 0 |
| `bronze/` | 0 |
| `silver/` | 0 |
| `gold/` | 0 |
| `platinum/` | 0 |

The combined listing printed no line and exited rc 1, which is grep's "no match". The file gets every location from
`lib/opal_naming.py`: `lookup("qwt")` for the firm (:43), `key()` and `address()` for each location (:48-51).

**Disclosed, not counted as hits:** the bare tier words `"bronze"`, `"silver"` (:47) and `"gold"` (:50, :51) occur as
arguments to `key()` and `address()`. They carry no `/`, so they are not tier or key prefixes in the order's sense.
They are one path segment passed to the builder, which composes the path. The docstring (:4-6) uses the words "bucket",
"key prefix" and "tier path" in prose and contains no literal.

## Positive control

A scratch copy of the file (`<WS>/.scratch/d2/pipeline_planted.py`, never staged or committed) got exactly one added
line after `TABLES = ...`, at line 20:

```
PLANTED = "opal-data-quillwater"
```

`diff` against the unplanted copy prints exactly that one added line (`19a20`). On the planted copy (65 lines), the same
search reads `opal-data-` 1 line and the other five patterns 0 lines each. The combined listing prints
`20:PLANTED = "opal-data-quillwater"` (rc 0), and `grep -o` counts 1 match. The unplanted copy counts 0 with the same
`grep -o`. The checker's regex, run by hand over both copies as a second instrument, returns `['opal-data-quillwater']`
and `[]`. So the search finds a literal of this kind when one is there, and the zero above is a measured absence, not
a blind instrument.

One thing about the criterion itself: `check_en.py d2-control` grades the `control` field below as written. It does not
re-run the plant. See row LGIC_ENFORCE-W8-S3.

## Nothing live moved

Nothing was written to AWS and no Terraform command ran. The scratch branch was only read. Nothing was pushed, merged,
checked out or deleted.

```json
{
  "pipeline": {
    "branch": "prac-lgic-enforce-d1",
    "commit": "92bc3b51bf2aac81152cd270aa146cadfb5159c7",
    "path": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~8/pipeline/qwt_positions.py"
  },
  "patterns": ["opal-data-", "s3://", "bronze/", "silver/", "gold/", "platinum/"],
  "instrument": "git show <commit>:<path> | grep -F -i -c -e <pattern>, one run per pattern, plus git show <commit>:<path> | grep -E -i -n 'opal-data-|s3://|(bronze|silver|gold|platinum)/'",
  "denominator": {"files": 1, "lines": 64},
  "hits": [],
  "disclosed_not_hits": [
    {"line": 47, "text": "for tier in (\"bronze\", \"silver\"):", "why": "a bare tier word passed to key()/address(), no '/'"},
    {"line": 50, "text": "naming.key(SOURCE, scope, \"gold\", \"positions\", part)", "why": "a bare tier word passed to key(), no '/'"},
    {"line": 51, "text": "naming.address(SOURCE, scope, \"gold\", \"positions\", part, \"part-0000.parquet\")", "why": "a bare tier word passed to address(), no '/'"}
  ],
  "control": {
    "planted": "opal-data-quillwater",
    "planted_line": "PLANTED = \"opal-data-quillwater\" (line 20 of a 65-line scratch copy, never committed)",
    "hits": 1,
    "unplanted_hits": 0,
    "second_instrument": "check_en.py's d2-zero regex over the planted copy: ['opal-data-quillwater']; over the unplanted copy: []"
  }
}
```
