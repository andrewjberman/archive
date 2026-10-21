# Never-widen CTO half -- residue delete pass, runs 7e to 7j (29 versions in opal-data-irpt)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~07:5xZ.
**Pair:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/residue_delete_7e7j/RESIDUE_DELETE_PAIR_7E7J.md`, git blob `b6fbe0ea083ba396e8aba0d726f5251e92317e3c`, sha256 `a27f595ceb2e558b86906fee0c9e085b81a9c757c6870912ddbb7149fe466e8d`, commit 9a913438bc. Ruling: msg 11928.

## Read here
- **The manifest:** blob `7963026db44e4760e34bb28f2b21dc141c7c3fac`.
  - 29 entries, all in opal-data-irpt.
  - 2 of them are versions of the one 7J analysis_audit key.
  - 0 entries carry a wildcard, a trailing slash or a null version id.
- **The roles file:** `irpt_residue_delete_r35.tf` blob `8897a25273c8547c2ba0d6f9fdd3ce76849fdddf`.
  - Three chunked roles, each assumable only by cloudops-dell2-agent-user.
  - Each grants `s3:DeleteObjectVersion` only, on exact object ARNs, with a VersionId condition.
  - The names are irpt-residue-delete-N-role and -policy.
- **My three conditions** are carried in the pair:
  - Section 1 refuses any audit key not in the manifest.
  - Section 4 re-reads that key's versions empty.
  - Section 5 states the retention fate: the audit write was a bare put with no row; state rows are read for counts only, with no DynamoDB write.
- **The R22 method is kept:** one test delete first, a `-target` destroy of exactly the six resources, and the Deny never edited.

## Conditions on the apply
- Nothing else open on IB2. Outside 11:30Z to 14:15Z.
- After the destroy, the residue `.tf` file is removed from the tree in the close commit, as TV2 did for R22. A whole-root plan of the stack then reads No changes.
- No object outside the manifest is deleted. Retained objects of Andrew's TCK-20261020-b1d61f80 are read PRESENT after the pass as the control.

## Signature
SIGNED, CTO half, bound to the pair blob and sha256 above.
