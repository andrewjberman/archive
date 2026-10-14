# CN-k-1 (repair cell, row MDPF_CANON-D1-S23) -- design note, 2.0.0_SA_COO~D1, 2026-10-14 ~01:4xZ

Draft only. The cell is cut with round 7 if the CTO's rectangle takes the repair; nothing here is issued.

## The defect

`.tools/mdpf-code-equality.py:117` `_md5_file(path)` hashes the WORKING-TREE bytes (`open(path, "rb")`, :119) and `:150` compares the S3 ETag with it. On
a CRLF checkout (`core.autocrlf=false` here, `git ls-files --eol`: `i/lf w/crlf`) a name whose S3 object equals the git blob reads DIFFER. Measured:
`data/mdpf/scripts/gold/mdpf_model_registry.json` S3 md5 6b89cc935c = blob 6b89cc935c, working tree fa784dd4ab.

## A correction to row D1-S23's note (rows are append-only; this is the record)

The row says "a named-file deploy from a CRLF checkout could write CRLF bytes (whether safe-deploy.sh normalizes was not verified)". It does not
write them. `.tools/safe_deploy_core.py:874-917` uploads the INDEX BLOB (`_index_blob`), asserts the returned ETag against that blob's md5, and only
prints the worktree CR count (IB-3, "worktree CR count N / index CR count M / uploaded: index"). So the deploy path is safe; the defect is confined to
the equality tool's READ side (false DIFFER).

## The repair (one LOCAL tool change plus a test)

Compare the S3 ETag with the md5 of the committed blob (`git show :<relpath>` bytes, the index blob, the same source safe-deploy serves), falling back to
the working tree only when the path has no index entry. State the basis in the tool's header and in each line it prints ("EQUAL (blob)"), so the
tool and the deploy path read the same bytes. A name that is EQUAL by blob and different in the working tree prints the working-tree CR count
(a fact, not a verdict).

Criteria shape (max three mechanical): (1) a unit test over a synthetic repo pair (LF blob, CRLF worktree): EQUAL by blob, no false DIFFER; (2) the
real name `mdpf_model_registry.json` reads EQUAL against S3 and `bronze_homes.json` still reads DIFFER (the true one-line difference); (3) the three
CN-d-1 deploy names still read EQUAL. Base: (1) and (2) FAIL, (3) passes. Owned files: `.tools/mdpf-code-equality.py`, its test under `.tools/tests/`.
Risk LOCAL (a read-only tool), the direct-act path applies.
