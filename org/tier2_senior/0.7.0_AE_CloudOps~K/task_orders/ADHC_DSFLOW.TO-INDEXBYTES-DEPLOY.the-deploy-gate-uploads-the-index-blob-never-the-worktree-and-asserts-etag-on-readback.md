# TO ADHC_DSFLOW.TO-INDEXBYTES-DEPLOY — the pre-push deploy gate uploads the INDEX blob (`git show :<path>`), never the worktree file; the read-back asserts ETag == the index blob's md5 and REFUSES on mismatch; the worktree CR count is printed, never served

<task_order id="ADHC_DSFLOW.TO-INDEXBYTES-DEPLOY" project="ADHC_DSFLOW">
<issued_to>0.7.0_AE_CloudOps~K</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T14:0xZ</issued>
<decomp_ref>NONE -- a one-act remediation of an existing tool under its charter: `.tools/safe-deploy.sh` / `.tools/safe_deploy_core.py` (Rule 13, ADHC_DSFLOW; `docs/architecture/ADHC_DSFLOW.md`). The ruling 1.0.0_SA_CTO 87705 (owner of the ruling; fix shape (1)-(3) + falsifiers + non-application) is the specification; the CVO's class row is the index-blob-vs-worktree item.</decomp_ref>
<proof_of_spec>
  <expected_criteria>IB-1,IB-2,IB-3,IB-4,IB-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~K/deliverables/ADHC_DSFLOW.TO-INDEXBYTES-DEPLOY.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json IB-1,IB-2,IB-3,IB-4,IB-5 ; checker vintage printed, rc read UNPIPED -->
</proof_of_spec>
<status>pending -- SEQUENCED AFTER ADHC_COMMITGATE.TO-ZEROCHECK-REFUSE at this seat (the gate's word 87705: one executor, two tooling faces, in order). GO the moment ZEROCHECK-REFUSE's proof is delivered; nothing here is started before that. Rule 27: one instance, one line of work at a time -- both faces are tooling remediations under existing charters, not projects.</status>
<priority>P2 -- the fourth instance this session of a worktree file diverging from its LF index blob by CRLF alone (a07: 557 CRs, 30,604 B vs the 30,047 B index blob), caught BEFORE the 14:00Z push only because MSTR compared worktree md5 to `git show HEAD:<path>` by hand; 9 of 82 tracked runner .py files carry the same divergence today. A served object whose ETag matches no commit is the drift-blindness INF-ONEWRITER spent the day closing, minted by the tool that exists to prevent it.</priority>
<authority>1.0.0_SA_CTO 87705 (ruling + shape + owner; executor = the base's allocation, sequenced after ZEROCHECK-REFUSE); 0.0.0_AB_MSTR 87683 (the catch and the standing hand-compare it replaces); 22a ("the index blob is the identity, never the worktree"); memory: a worktree sha256 on an autocrlf box hashes the CHECKOUT, not the record. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## The one-paragraph version

`.tools/safe_deploy_core.py` (the pre-push deploy gate on Rule 13's DS commit→QA-deploy path) reads each deploy-scope file from the WORKTREE and uploads those bytes. On this autocrlf box the worktree copy of an `eol=lf` file can carry CRLF while the index blob is LF (`Path.write_text()` re-introduces it; git shows the tree clean); the served object's ETag then matches no commit. MSTR's pre-push hand-compare is a catch, not a control. Fix: source the upload from the INDEX blob, assert the read-back ETag against the index blob's md5, and print the worktree CR count so a CRLF checkout is VISIBLE without being SERVED.

## Acceptance criteria -- the gate's ratified shape (87705), verbatim in substance

<criterion id="IB-1"/> **THE UPLOAD SOURCE IS THE INDEX BLOB:** for every deploy-scope file the gate uploads the bytes of `git show :<path>` (or `git cat-file -p :<path>`) -- never the worktree file. The change is in the deploy step of `.tools/safe_deploy_core.py`; file:line named in the report; commit-gate clean; `safe-commit -F`.
<criterion id="IB-2"/> **THE READ-BACK ASSERTS IDENTITY:** after each upload, head-object ETag == md5 of the index blob; on mismatch the gate REFUSES with a distinct rc (rc=2), the deploy ledger left OPEN and the mismatch printed (key, ETag, index md5). A push that deployed a byte the record does not carry is never reported as a pass.
<criterion id="IB-3"/> **THE CR LINE, per deployed file:** `worktree CR count N / index CR count 0 / uploaded: index` printed every time -- a CRLF worktree is visible in the gate's own output without being served.
<criterion id="IB-4"/> **NON-APPLICATION, stated and exercised:** `.sh` under `data/` stays outside the gate's deploy scope (the 13:46Z CLOSE's finding; AE base's manual path reads against the index md5 by rule at 87575) -- the gate does NOT widen its scope under this face; a `.sh` in range still prints "outside deploy scope" and is untouched.
<criterion id="IB-5"/> **THE FALSIFIERS, both polarities, from the running gate on a SCRATCH deploy target (never a served key):** (i) a scratch `.py` with CRLF injected into the WORKTREE copy only -> uploaded bytes LF, ETag == the index md5, the CR line prints N>0; (ii) the same file with a CR committed INTO the blob -> the read-back still matches (the gate uploads what is committed; a committed CR is the author's and ds-precommit is that gate); (iii) the PRE-FIX gate run FIRST on subject (i) -> the uploaded bytes carry the CRs and the ETag != the index md5 -- the failing baseline before the arms; (iv) a forced ETag mismatch (the scratch key overwritten between upload and read-back) -> rc=2, ledger OPEN, the three values printed. Proof positional IB-1..IB-5, checker vintage printed, rc UNPIPED; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not touch a served key** for any arm -- scratch targets only; the running gate's first production exercise is MSTR's next window with a non-zero ceiling, read by MSTR.
- ⛔ **Do not widen the deploy scope** (`.sh`, non-gold paths) -- one change of byte source, one assertion, one print line.
- ⛔ **Do not normalise any worktree file by hand** under this face -- the point is that the gate no longer depends on that.
- ⛔ **Do not change the SHAPE** -- it is the gate's ruling (87705); a disagreement goes to `1.0.0_SA_CTO`, not into the code.
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

IB-1..IB-4 + the four falsifier arms as ONE message (each arm's rc, ETag, index md5, CR line quoted) to the issuer + CTO + CVO + MSTR (whose hand-compare this retires); the proof at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
