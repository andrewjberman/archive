# OG-ap-50 pre-read: process-wide state, read by 2.0.0_SA_COO~O before the ask arrives

Read at trunk `49de05db93` against live ref `6b1a9bd292` (git diff, not a worker's report). Purpose: the COO half of the never-widen ask needs the `process-wide state this change touches` line (CVO verdict 35844, item 1); this is the read behind it, so signing is not delayed by it.

## The diff (`app/admin_api.py`, `tests/test_og_cd2.py`)

- `app/admin_api.py`: exactly 2 added lines, 0 removed: `from . import family_depth` and `Route("/gateway/families", owner_only(family_depth.families), methods=["GET"])`.
- `tests/test_og_cd2.py`: 80 added lines, a new file.
- No other file differs between the live ref and trunk in the two take-list paths.

## Import-time side effects of `app/family_depth.py` (413 lines), top level read line by line

- Imports: `json`, `os`, `re`, `sys`, `datetime` (stdlib only, lines 31-37). No `boto3`, no app module, no logger.
- Module-level statements: path constants from `__file__` (lines 39-42), string and int constants (44-55). Nothing executes at import.
- `if __name__ == "__main__":` at line 406: the generate CLI, not reached on import.
- Searched for a logger, signal handler, `os.environ` read, `sys.path` change or global config at module level: 0 hits.

## Line for the ask

`process-wide state this change touches: the admin route table (one added entry, owner-gated); no logger, signal handler, environment read, sys.path change or global config at import, read.`

## Not covered by this read

- The route's runtime behaviour (the AWS calls it makes when called) is graded by `OG-cd-2` AC and by `ap50` AC3, not by this note.
- The grant it depends on (`OG-cd-3`) is live and COMPLETE.
